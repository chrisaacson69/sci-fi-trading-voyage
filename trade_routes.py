#!/usr/bin/env python3
"""Rank two-stop round-trip trades in Sci-Fi Trading Voyage by profit per hour.

Model (see README.md for how each assumption was measured):
  * A trip is a cycle between two stops, A -> B -> A.
  * Margin per unit = buy price at destination - sell price at origin; a unit
    takes `size` cargo space.
  * Leg time = overhead + distance * seconds_per_gm. Measured for the first fleet:
    2.0 s/Gm and 0 s overhead (7 Gm took 14 s; 1700 Gm took 56:40).
  * Cash is unlimited and prices don't move as you trade (they shift daily).

Two loading modes:
  * continuous (default): the hold fills with the best margin-per-cargo good, as if
    fractional units could be bought. Gives a score per cargo unit that doesn't
    depend on the ship, and an upper bound on whole-unit loading.
  * whole units (--ships, or --cargo with --whole-units): goods are bought in whole
    units only, and each hold is packed with the best mix of goods (an unbounded
    knapsack). A hold smaller than a good's size can't carry that good at all.

Usage:
  py -3 trade_routes.py                            # per cargo unit, continuous
  py -3 trade_routes.py --ships 25200x12           # twelve separate 25,200 holds
  py -3 trade_routes.py --ships 130000x3,2000x2    # mixed fleet, separate holds
  py -3 trade_routes.py --cargo 302400 --whole-units   # one pooled fleet hold
  py -3 trade_routes.py --from Troy                # only round trips touching Troy
  py -3 trade_routes.py --max-alarm Medium         # both ports at most Medium alarm
  py -3 trade_routes.py --by-alarm --ships 130000x3   # best route under each alarm cap
  py -3 trade_routes.py --json > routes.json       # machine-readable, for ship pickers
  py -3 trade_routes.py --route "Free Port" Ares  # score one route (card)
  py -3 trade_routes.py --known-routes             # score every route in data/routes.csv
  py -3 trade_routes.py --ships hauler-28cpx3      # ship names from data/ships.csv work too
  py -3 trade_routes.py --oracle                   # compare predictions with the game's own $/hr
  py -3 trade_routes.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import re
import itertools
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, field
from functools import reduce
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent / "data" / "market.csv"
DEFAULT_PORTS = Path(__file__).resolve().parent / "data" / "ports.csv"
DEFAULT_ROUTES = Path(__file__).resolve().parent / "data" / "routes.csv"
DEFAULT_SHIPS = Path(__file__).resolve().parent / "data" / "ships.csv"
DEFAULT_ORACLE = Path(__file__).resolve().parent / "data" / "oracle.csv"
ALARMS = ["Low", "Medium", "High", "Extreme"]  # the game's port alarm levels, in order
SECONDS_PER_GM = 2.0  # measured, first fleet (2x FG300: 3CP, 2000 cargo each)
REF_WARP = 5000       # FG300's listed warp. Warp is NOT Gm/hr: FG300 measured 1800 Gm/hr.
                      # So warp is used as RELATIVE speed: s/Gm = SECONDS_PER_GM * REF_WARP / warp.


def seconds_per_gm_for(warp: float) -> float:
    return SECONDS_PER_GM * REF_WARP / warp


@dataclass(frozen=True)
class Quote:
    planet: str
    good: str
    size: int
    side: str   # 'S' = planet sells to you (buy here), 'B' = planet buys from you
    price: int


@dataclass
class Leg:
    origin: str
    dest: str
    good: str | None         # best good by margin per cargo; None = nothing profitable
    margin_per_cargo: float  # continuous model, credits per cargo unit
    load: dict = field(default_factory=dict)  # whole-unit mode: {good: units} across the fleet
    margin: float = 0.0      # credits for this leg: whole-unit packing, or margin_per_cargo * cargo


@dataclass
class RoundTrip:
    a: str
    b: str
    distance_gm: float
    out: Leg
    back: Leg
    margin_per_cargo: float      # continuous model, whole cycle, per cargo unit
    per_cargo_per_kgm: float     # ship-independent score: margin per cargo / 1000 Gm flown
    seconds: float               # cycle time at the given speed/overhead
    cycle_margin: float          # credits per cycle for the given cargo / fleet
    profit_per_hour: float       # travel time only -- pirate attacks are NOT modelled yet
    alarm_a: str = ""
    alarm_b: str = ""

    @property
    def alarm(self) -> str:
        """The route's worse port alarm."""
        return max((self.alarm_a, self.alarm_b), key=lambda a: ALARMS.index(a) if a in ALARMS else -1)


def load_ports(path: Path = DEFAULT_PORTS):
    """Return ({planet: (x, y)}, {planet: alarm}) from the ports CSV."""
    coords, alarms = {}, {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            p = r["planet"].strip()
            if p in coords:
                raise ValueError(f"{p}: listed twice in {path}")
            coords[p] = (float(r["x"]), float(r["y"]))
            a = r["alarm"].strip().capitalize()
            if a not in ALARMS:
                raise ValueError(f"{p}: alarm must be one of {ALARMS}, got {a!r}")
            alarms[p] = a
    return coords, alarms


def load_market(path: Path = DEFAULT_DATA, ports: Path = DEFAULT_PORTS):
    """Return (quotes, coords, alarms) from the market and ports CSVs."""
    coords, alarms = load_ports(ports)
    quotes = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            p = r["planet"].strip()
            if p not in coords:
                raise ValueError(f"{p}: in {path} but not in {ports}")
            side = r["side"].strip().upper()
            if side not in ("S", "B"):
                raise ValueError(f"{p}/{r['good']}: side must be S or B, got {side!r}")
            quotes.append(Quote(p, r["good"].strip(), int(r["size"]), side, int(r["price"])))
    return quotes, coords, alarms


def audit(quotes, outlier_ratio: float = 2.0):
    """Warn about likely typos. Every real typo we hit was one of these two kinds."""
    warnings = []
    by_good = defaultdict(list)
    for q in quotes:
        by_good[q.good].append(q)
    for good, qs in sorted(by_good.items()):
        sizes = {q.size for q in qs}
        if len(sizes) > 1:
            common = statistics.mode(q.size for q in qs)
            for q in qs:
                if q.size != common:
                    warnings.append(f"SIZE  {q.planet}/{good}: size {q.size}, others {common}")
        med = statistics.median(q.price / q.size for q in qs)
        for q in qs:
            r = (q.price / q.size) / med
            if r > outlier_ratio or r < 1 / outlier_ratio:
                warnings.append(f"PRICE {q.planet}/{good} ({q.side}): {q.price / q.size:.3f}/cargo "
                                f"is {r:.2f}x the median {med:.3f} -- typo or real?")
    return warnings


@dataclass(frozen=True)
class ShipType:
    name: str
    cargo: int
    cp: int
    cost: int | None = None
    limit: int | None = None   # build limit: most of this ship you can own
    dpm: int | None = None     # damage per minute
    hp: int | None = None
    warp: int | None = None    # relative speed, see REF_WARP

    @property
    def seconds_per_gm(self) -> float | None:
        return seconds_per_gm_for(self.warp) if self.warp else None


def load_ships(path: Path = DEFAULT_SHIPS) -> dict[str, ShipType]:
    if not path.exists():
        return {}
    num = lambda v: int(v.replace(",", "")) if v and v.strip() else None
    with open(path, newline="") as f:
        return {r["name"].strip(): ShipType(r["name"].strip(), num(r["cargo"]), num(r["cp"]),
                                            num(r.get("cost")), num(r.get("limit")), num(r.get("dpm")),
                                            num(r.get("hp")), num(r.get("warp")))
                for r in csv.DictReader(f)}


@dataclass
class Fleet:
    holds: list[int]
    ships: list[ShipType | None]   # None = a bare cargo number with no known stats

    def _sum(self, attr):
        vals = [getattr(s, attr) if s else None for s in self.ships]
        return None if any(v is None for v in vals) else sum(vals)

    cp = property(lambda self: self._sum("cp"))
    dpm = property(lambda self: self._sum("dpm"))
    hp = property(lambda self: self._sum("hp"))
    cost = property(lambda self: self._sum("cost"))

    @property
    def seconds_per_gm(self) -> float | None:
        """The slowest ship sets the pace (assumed, not yet verified in game)."""
        v = [s.seconds_per_gm if s else None for s in self.ships]
        return None if any(x is None for x in v) else max(v)

    def over_limit(self) -> list[str]:
        c = Counter(s.name for s in self.ships if s)
        by = {s.name: s for s in self.ships if s}
        return [f"{n} x {k} (limit {by[k].limit})" for k, n in c.items() if by[k].limit and n > by[k].limit]


def parse_ships(spec: str, types: dict[str, ShipType] | None = None) -> Fleet:
    """'25200x12,ST59x3' -> a Fleet. Each part is a cargo number or a ship name from
    ships.csv, optionally followed by xN."""
    holds, ships = [], []
    for part in spec.split(","):
        m = re.fullmatch(r"\s*(.+?)(?:x(\d+))?\s*", part)
        what, n = m.group(1), int(m.group(2) or 1)
        if types and what in types:
            holds += [types[what].cargo] * n
            ships += [types[what]] * n
        else:
            try:
                holds += [int(float(what))] * n
            except ValueError:
                raise ValueError(f"--ships: {what!r} is neither a number nor a ship in ships.csv "
                                 f"({', '.join(sorted(types or {}))})") from None
            ships += [None] * n
    if not holds or min(holds) <= 0:
        raise ValueError(f"bad --ships spec {spec!r}")
    return Fleet(holds, ships)


@dataclass
class RouteInfo:
    level: int | None
    cp_cap: int | None
    upgrade_cost: str
    notes: str


def load_routes(path: Path = DEFAULT_ROUTES) -> dict[frozenset, RouteInfo]:
    """Route levels and CP caps, as recorded in the game. Keyed by the unordered stop pair."""
    if not path.exists():
        return {}
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            key = frozenset((r["route_a"].strip(), r["route_b"].strip()))
            out[key] = RouteInfo(int(r["level"]) if r["level"].strip() else None,
                                 int(r["cp_cap"]) if r["cp_cap"].strip() else None,
                                 r.get("upgrade_cost", "").strip(), r.get("notes", "").strip())
    return out


def leg_options(origin, dest, sells, buys):
    """Profitable goods on this leg: [(good, size, margin per unit)]."""
    opts = []
    for good, q in sells[origin].items():
        b = buys[dest].get(good)
        if b and b.price > q.price:
            opts.append((good, q.size, b.price - q.price))
    return opts


def fill_hold(capacity: int, options) -> tuple[float, dict]:
    """Best whole-unit load for one hold: unbounded knapsack over the leg's goods."""
    opts = [o for o in options if o[1] <= capacity]
    if not opts:
        return 0.0, {}
    g = reduce(math.gcd, (o[1] for o in opts))
    cap = capacity // g
    sizes = [o[1] // g for o in opts]
    best = [0.0] * (cap + 1)
    pick = [-1] * (cap + 1)
    for c in range(1, cap + 1):
        best[c], pick[c] = best[c - 1], -1  # -1 = leave one cell empty
        for i, s in enumerate(sizes):
            if s <= c and best[c - s] + opts[i][2] > best[c]:
                best[c], pick[c] = best[c - s] + opts[i][2], i
    load, c = Counter(), cap
    while c > 0:
        if pick[c] < 0:
            c -= 1
        else:
            load[opts[pick[c]][0]] += 1
            c -= sizes[pick[c]]
    return best[cap], dict(load)


def make_leg(origin, dest, sells, buys, holds, cargo) -> Leg:
    opts = leg_options(origin, dest, sells, buys)
    good, mpc = None, 0.0
    for gname, size, m in opts:
        if m / size > mpc:
            good, mpc = gname, m / size
    leg = Leg(origin, dest, good, mpc)
    if holds is None:
        leg.margin = mpc * cargo
        return leg
    total, load = 0.0, Counter()
    for cap, n in Counter(holds).items():   # identical ships pack identically
        m, l = fill_hold(cap, opts)
        total += m * n
        for k, v in l.items():
            load[k] += v * n
    leg.margin, leg.load = total, dict(load)
    return leg


def round_trips(quotes, coords, cargo: float = 1.0, seconds_per_gm: float = SECONDS_PER_GM,
                overhead_s: float = 0.0, holds: list[int] | None = None, alarms=None):
    """Every unordered stop pair with any profit, best first.

    holds=None -> continuous model scaled by `cargo`; otherwise whole units per hold.
    """
    sells, buys = book(quotes)
    out = []
    for a, b in itertools.combinations(sorted(coords), 2):
        t = make_trip(a, b, sells, buys, coords, cargo, seconds_per_gm, overhead_s, holds, alarms)
        if t.cycle_margin > 0:
            out.append(t)
    out.sort(key=lambda t: t.profit_per_hour, reverse=True)
    return out


def book(quotes):
    sells, buys = defaultdict(dict), defaultdict(dict)
    for q in quotes:
        (sells if q.side == "S" else buys)[q.planet][q.good] = q
    return sells, buys


def make_trip(a, b, sells, buys, coords, cargo=1.0, seconds_per_gm=SECONDS_PER_GM, overhead_s=0.0,
              holds=None, alarms=None) -> RoundTrip:
    f = make_leg(a, b, sells, buys, holds, cargo)
    r = make_leg(b, a, sells, buys, holds, cargo)
    m = f.margin_per_cargo + r.margin_per_cargo
    cyc = f.margin + r.margin
    d = math.dist(coords[a], coords[b])
    secs = 2 * (overhead_s + d * seconds_per_gm)
    return RoundTrip(a, b, d, f, r, m,
                     per_cargo_per_kgm=m / (2 * d) * 1000 if d else math.inf,
                     seconds=secs, cycle_margin=cyc,
                     profit_per_hour=cyc * 3600 / secs if secs else math.inf,
                     alarm_a=(alarms or {}).get(a, ""), alarm_b=(alarms or {}).get(b, ""))


def fill_cap(a, b, sells, buys, coords, cap, ship_types, seconds_per_gm, overhead_s):
    """For each ship type: fill the route's CP cap with only that ship. Best first."""
    rows = []
    for st in ship_types.values():
        if not st.warp:
            continue  # unknown speed: guessing one would decide the ranking
        n = cap // st.cp
        if st.limit:
            n = min(n, st.limit)
        if n == 0:
            continue
        t = make_trip(a, b, sells, buys, coords, seconds_per_gm=st.seconds_per_gm,
                      overhead_s=overhead_s, holds=[st.cargo] * n)
        rows.append((t.profit_per_hour, st, n, t))
    rows.sort(key=lambda r: r[0], reverse=True)
    return rows


def route_card(a, b, quotes, coords, alarms, routes, ship_types, seconds_per_gm, overhead_s,
               fleet: Fleet | None = None):
    sells, buys = book(quotes)
    t = make_trip(a, b, sells, buys, coords, seconds_per_gm=seconds_per_gm, overhead_s=overhead_s,
                  alarms=alarms)
    info = routes.get(frozenset((a, b)))
    lvl = f"level {info.level}, cap {info.cp_cap} CP" if info and info.cp_cap else "level/cap not recorded"
    print(f"{a} <-> {b}: {t.distance_gm:,.0f} Gm, round trip {t.seconds / 60:.1f} min, "
          f"alarm {t.alarm_a}/{t.alarm_b}, {lvl}")
    if info and info.notes:
        print(f"  notes: {info.notes}")
    for o, d in ((a, b), (b, a)):
        opts = sorted(leg_options(o, d, sells, buys), key=lambda x: x[2] / x[1], reverse=True)
        if not opts:
            print(f"  {o} -> {d}: nothing profitable (flies empty)")
            continue
        print(f"  {o} -> {d}:")
        for g, size, m in opts[:4]:
            print(f"      {g:15} +{m:>11,}/unit  size {size:>9,}  {m / size:7.3f}/cargo  (needs a hold >= {size:,})")
    per_cargo_hr = t.margin_per_cargo * 3600 / t.seconds if t.seconds else math.inf
    print(f"  SCORE: {per_cargo_hr:,.2f} credits per cargo unit per hour at {seconds_per_gm:.2f} s/Gm "
          f"(fractional loading, travel only)")
    if info and info.cp_cap and ship_types:
        print(f"  filling the {info.cp_cap} CP cap with one ship type (whole units, own speed, build limits, travel only):")
        for pph, st, n, ft in fill_cap(a, b, sells, buys, coords, info.cp_cap, ship_types,
                                       seconds_per_gm, overhead_s):
            spd = f"{st.seconds_per_gm:.2f}s/Gm" if st.seconds_per_gm else "speed?"
            print(f"      {n:3} x {st.name:14} {n * st.cp:4} CP {n * st.cargo:>10,} cargo {spd:>10} -> {pph:14,.0f}/hr"
                  f"   [{_fmt_leg(ft.out, True)} / {_fmt_leg(ft.back, True)}]")
    if fleet:
        spg = seconds_per_gm  # already resolved in main(): --sec-per-gm, else the fleet's slowest ship
        ft = make_trip(a, b, sells, buys, coords, seconds_per_gm=spg, overhead_s=overhead_s,
                       holds=fleet.holds)
        cp_txt = "" if fleet.cp is None else f", {fleet.cp} CP"
        if fleet.cp is not None and info and info.cp_cap and fleet.cp > info.cp_cap:
            cp_txt += f" -- OVER the {info.cp_cap} CP cap"
        print(f"  your fleet ({len(fleet.holds)} ships, {sum(fleet.holds):,} cargo{cp_txt}, {spg:.2f} s/Gm, "
              f"round trip {ft.seconds / 60:.1f} min): {ft.profit_per_hour:,.0f}/hr"
              f"   [{_fmt_leg(ft.out, True)} / {_fmt_leg(ft.back, True)}]")
        if fleet.dpm is not None:
            print(f"      combat: {fleet.dpm:,} DPM, {fleet.hp:,} HP"
                  + (f", cost {fleet.cost:,}" if fleet.cost is not None else ""))
        for w in fleet.over_limit():
            print(f"      WARNING: over build limit: {w}")
    unknown = [st.name for st in ship_types.values() if not st.warp]
    if info and info.cp_cap and unknown:
        print(f"  not scored (no warp speed in ships.csv): {', '.join(unknown)}")
    print("  pirates are not modelled: every figure is a ceiling (see data/encounters.csv)")
    return t


def _fmt_leg(leg: Leg, whole: bool) -> str:
    if whole:
        return " + ".join(f"{n} {g}" for g, n in sorted(leg.load.items())) or "(empty)"
    return f"{leg.good} {leg.margin_per_cargo:.2f}" if leg.good else "(empty)"


def print_table(trips, label, whole):
    print(f"{label}\n")
    print(f"{'#':>3} {'profit/hr':>14} {'cycle':>9} {'dist Gm':>8}  {'alarm':9} {'A':15} {'B':15} "
          f"{'A -> B':28} B -> A")
    for i, t in enumerate(trips, 1):
        al = f"{t.alarm_a[:3]}/{t.alarm_b[:3]}"
        print(f"{i:3} {t.profit_per_hour:14,.0f} {t.seconds / 60:8.1f}m {t.distance_gm:8.0f}  {al:9} "
              f"{t.a:15} {t.b:15} {_fmt_leg(t.out, whole):28} {_fmt_leg(t.back, whole)}")
    print("\nprofit/hr counts travel time only; pirate attacks (time and losses) are not modelled yet")


def oracle_report(quotes, coords, ship_types, path: Path = DEFAULT_ORACLE):
    """Compare each logged game $/hr figure against the model's open choices:
    separate vs pooled holds, and warp-relative-to-FG300 vs warp-as-Gm/hr speed."""
    if not path.exists():
        print(f"no {path}")
        return
    sells, buys = book(quotes)
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        a, b, game = r["route_a"].strip(), r["route_b"].strip(), float(r["game_per_hr"])
        fleet = parse_ships(r["fleet"], ship_types)
        warps = [st.warp for st in fleet.ships if st]
        print(f"{r['date']}  {a} <-> {b}  fleet {r['fleet']}  game says {game:,.0f}/hr")
        if len(warps) != len(fleet.ships):
            print("   (a ship has no warp speed; skipped)")
            continue
        speeds = {"calibrated (FG300 timing)": fleet.seconds_per_gm,
                  "warp = Gm/hr": 3600 / min(warps)}
        for hold_name, holds in (("separate holds", fleet.holds), ("pooled hold", [sum(fleet.holds)])):
            for sp_name, spg in speeds.items():
                t = make_trip(a, b, sells, buys, coords, seconds_per_gm=spg, holds=holds)
                print(f"   {hold_name:15} {sp_name:26} {spg:5.2f} s/Gm -> {t.profit_per_hour:12,.0f}/hr"
                      f"  ({t.profit_per_hour / game:5.2f}x game)")


def selftest() -> int:
    """Check against values worked out by hand from the 2026-10-06 snapshot."""
    quotes, coords, alarms = load_market()
    trips = {(t.a, t.b): t for t in round_trips(quotes, coords, alarms=alarms)}
    checks = []

    def eq(name, got, want, tol=1e-3):
        ok = abs(got - want) <= tol
        checks.append(ok)
        print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.4f} (want {want})")

    def check(name, ok):
        checks.append(bool(ok))
        print(f"  {'ok ' if ok else 'BAD'} {name}")

    # Two timing runs: 7 Gm took 14 s and 1700 Gm took 3400 s, which gives 2.0 s/Gm and 0 s overhead
    spg = (3400 - 14) / (1700 - 7)
    eq("seconds per Gm from the two timings", spg, 2.0)
    eq("overhead from the two timings", 14 - 7 * spg, 0.0)
    t = trips[("AlphaCentA", "Proxima")]
    eq("Proxima->AlphaCentA ResearchData3 margin", t.back.margin_per_cargo,
       (3078000 - 2536500) / 100000)
    eq("  ...profit/hr per cargo", t.profit_per_hour,
       5.415 * 3600 / (4 * math.dist((1046, 1704), (1040, 1700))))
    t = trips[("BlackGoldStar", "Troy")]
    eq("BlackGoldStar->Troy Comm Comp", t.out.margin_per_cargo, (58604 - 18032) / 2000)
    eq("Troy->BlackGoldStar TrojiteCry3", t.back.margin_per_cargo, (7348000 - 6145600) / 240000)
    t = trips[("Ares", "Free Port")]
    eq("Free Port->Ares Collect2", t.back.margin_per_cargo, (245600 - 74400) / 8000)
    ranked = round_trips(quotes, coords)
    check(f"ranking: #1 {ranked[0].a}/{ranked[0].b}, #2 {ranked[1].a}/{ranked[1].b}",
          ranked[0].a == "AlphaCentA" and ranked[1].a == "BlackGoldStar")
    check("Proxima/AlphaCentA is an Extreme/Extreme route",
          trips[("AlphaCentA", "Proxima")].alarm == "Extreme")
    check("Ares/Free Port takes its worse end: Extreme", trips[("Ares", "Free Port")].alarm == "Extreme")
    check("BlackGoldStar/Troy is High/High", trips[("BlackGoldStar", "Troy")].alarm == "High")
    check("no size mismatches in the corrected snapshot",
          not any(x.startswith("SIZE") for x in audit(quotes)))

    # Whole units: ResearchData3 is 100,000 per unit
    whole = lambda holds: {(t.a, t.b): t for t in round_trips(quotes, coords, holds=holds)}
    check("25,200 hold can't carry ResearchData3 -> Proxima route drops out",
          ("AlphaCentA", "Proxima") not in whole([25200]))
    t = whole([130000])[("AlphaCentA", "Proxima")]
    eq("130,000 hold carries exactly 1 ResearchData3", t.back.load.get("ResearchData3", 0), 1)
    eq("  ...margin for one unit", t.cycle_margin, 3078000 - 2536500)
    t = whole([130000] * 3)[("AlphaCentA", "Proxima")]
    eq("three separate 130,000 holds carry 3", t.back.load["ResearchData3"], 3)
    t = round_trips(quotes, coords, holds=[390000])
    t = {(x.a, x.b): x for x in t}[("AlphaCentA", "Proxima")]
    eq("one pooled 390,000 hold also carries 3", t.back.load["ResearchData3"], 3)
    # knapsack sanity: a 4,000 hold on BlackGoldStar->Troy takes 2 Comm Comp (size 2000)
    t = whole([4000])[("BlackGoldStar", "Troy")]
    eq("4,000 hold: 2 Comm Comp to Troy", t.out.load.get("Comm Comp", 0), 2)
    eq("continuous model is an upper bound", float(
        all(w.cycle_margin <= c.cycle_margin + 1e-6
            for c in round_trips(quotes, coords, cargo=25200)
            for w in round_trips(quotes, coords, holds=[25200]) if (w.a, w.b) == (c.a, c.b))), 1.0)
    # ships / routes files
    types = load_ships()
    fl = parse_ships("ST59x3,2000x2", types)
    check("ship names parse: 3 x 130,000 + 2 x 2,000, CP unknown (bare numbers)",
          fl.holds == [130000] * 3 + [2000] * 2 and fl.cp is None)
    fl = parse_ships("ST59x3", types)
    eq("  ...named ships carry CP", fl.cp, 84)
    eq("  ...and DPM", fl.dpm, 3 * 27373)
    eq("FG300 (the timing fleet) runs at the measured 2.0 s/Gm", types["FG300"].seconds_per_gm, 2.0)
    eq("ST59 (warp 2250) is 2.22x slower", types["ST59"].seconds_per_gm, 2.0 * 5000 / 2250)
    eq("mixed fleet moves at its slowest ship", parse_ships("FG300x2,ST59", types).seconds_per_gm,
       2.0 * 5000 / 2250)
    check("build limit is flagged", parse_ships("FG300x16", types).over_limit() != [])
    routes = load_routes()
    check("routes.csv: Free Port/Ares is level 4, 160 CP either way round",
          routes[frozenset(("Ares", "Free Port"))].cp_cap == 160)
    sells, buys = book(quotes)
    rows = fill_cap("Free Port", "Ares", sells, buys, coords, 160, types, 2.0, 0.0)
    eq("160 CP would fit 20 AC721, but the build limit is 15", {r[1].name: r[2] for r in rows}["AC721"], 15)
    print("PASS" if all(checks) else "FAIL")
    return 0 if all(checks) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", type=Path, default=DEFAULT_DATA, help="market CSV (default data/market.csv)")
    ap.add_argument("--ports", type=Path, default=DEFAULT_PORTS, help="ports CSV (default data/ports.csv)")
    ap.add_argument("--cargo", type=float, default=1.0, help="cargo capacity (Size units)")
    ap.add_argument("--whole-units", action="store_true",
                    help="buy whole units only; --cargo is one pooled hold")
    ap.add_argument("--ships", help="separate holds, whole units: e.g. 25200x12, 130000x3,2000x2, "
                                    "or ship names from ships.csv like hauler-28cpx3")
    ap.add_argument("--route", nargs=2, metavar=("A", "B"), help="print a score card for one route")
    ap.add_argument("--known-routes", action="store_true",
                    help="score every route in routes.csv, filling its CP cap with the best ship type")
    ap.add_argument("--routes-file", type=Path, default=DEFAULT_ROUTES)
    ap.add_argument("--ships-file", type=Path, default=DEFAULT_SHIPS)
    ap.add_argument("--sec-per-gm", type=float, default=None,
                    help="travel time per Gm (default: from the fleet's slowest warp, else 2.0)")
    ap.add_argument("--overhead", type=float, default=0.0, help="fixed seconds per leg (dock/launch)")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--from", dest="stop", help="only round trips that include this stop")
    ap.add_argument("--max-alarm", choices=ALARMS, help="only routes whose BOTH ports are at most this alarm")
    ap.add_argument("--by-alarm", action="store_true", help="best route under each alarm cap")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--audit", action="store_true", help="only print likely-typo warnings")
    ap.add_argument("--oracle", action="store_true", help="compare predictions with data/oracle.csv")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    quotes, coords, alarms = load_market(args.data, args.ports)
    warnings = audit(quotes)
    if args.audit:
        print("\n".join(warnings) or "no warnings")
        return 0
    ship_types = load_ships(args.ships_file)
    routes = load_routes(args.routes_file)
    fleet = None
    if args.ships:
        fleet = parse_ships(args.ships, ship_types)
        holds = fleet.holds
        label = f"whole units, {len(holds)} separate holds, {sum(holds):,} cargo total"
    elif args.whole_units:
        holds = [int(args.cargo)]
        label = f"whole units, one pooled hold of {int(args.cargo):,}"
    else:
        holds = None
        label = f"continuous loading, cargo {args.cargo:g}"
    if args.sec_per_gm is None:
        args.sec_per_gm = (fleet.seconds_per_gm if fleet else None) or SECONDS_PER_GM
    if fleet and fleet.seconds_per_gm:
        label += f", {args.sec_per_gm:.2f} s/Gm (slowest ship)"
    if args.oracle:
        oracle_report(quotes, coords, ship_types)
        return 0
    for key in routes:
        for p in key:
            if p not in coords:
                ap.error(f"routes.csv names unknown stop {p!r}")
    if args.route:
        for p in args.route:
            if p not in coords:
                ap.error(f"unknown stop {p!r}; known: {', '.join(sorted(coords))}")
        route_card(*args.route, quotes, coords, alarms, routes, ship_types, args.sec_per_gm,
                   args.overhead, fleet)
        return 0
    if args.known_routes:
        sells, buys = book(quotes)
        rows = []
        for key, info in routes.items():
            a, b = sorted(key)
            best = fill_cap(a, b, sells, buys, coords, info.cp_cap or 0, ship_types,
                            args.sec_per_gm, args.overhead) if info.cp_cap else []
            t = make_trip(a, b, sells, buys, coords, seconds_per_gm=args.sec_per_gm,
                          overhead_s=args.overhead, alarms=alarms)
            rows.append((best[0][0] if best else 0.0, a, b, info, t, best[0] if best else None))
        rows.sort(key=lambda r: r[0], reverse=True)
        print(f"{'best fill/hr':>14}  {'route':34} {'lvl':>3} {'cap':>4}  {'alarm':9} {'per cargo/hr':>12}  best ship type")
        for pph, a, b, info, t, best in rows:
            pch = t.margin_per_cargo * 3600 / t.seconds if t.seconds else math.inf
            ship = f"{best[2]} x {best[1].name}" if best else "-"
            print(f"{pph:14,.0f}  {a + ' <-> ' + b:34} {info.level or '?':>3} {info.cp_cap or '?':>4}  "
                  f"{t.alarm_a[:3] + '/' + t.alarm_b[:3]:9} {pch:12,.2f}  {ship}")
        print("\ntravel time only; pirates are not modelled. Add routes to data/routes.csv as you learn them.")
        return 0
    trips = round_trips(quotes, coords, args.cargo, args.sec_per_gm, args.overhead, holds, alarms)
    if args.by_alarm:
        whole = holds is not None
        print(label + "\n\nbest route with both ports at or below each alarm level (travel time only):")
        for cap in ALARMS:
            ok = [t for t in trips if ALARMS.index(t.alarm) <= ALARMS.index(cap)]
            if ok:
                t = ok[0]
                print(f"  <= {cap:8} {t.profit_per_hour:14,.0f}/hr  {t.a} <-> {t.b} ({t.alarm_a}/{t.alarm_b}), "
                      f"{_fmt_leg(t.out, whole)} / {_fmt_leg(t.back, whole)}")
        return 0
    if args.max_alarm:
        trips = [t for t in trips if ALARMS.index(t.alarm) <= ALARMS.index(args.max_alarm)]
    if args.stop:
        if args.stop not in coords:
            ap.error(f"unknown stop {args.stop!r}; known: {', '.join(sorted(coords))}")
        trips = [t for t in trips if args.stop in (t.a, t.b)]
    trips = trips[: args.top] if args.top > 0 else trips
    if args.json:
        json.dump({"mode": label, "cargo": args.cargo, "holds": holds,
                   "seconds_per_gm": args.sec_per_gm, "overhead_s": args.overhead,
                   "warnings": warnings,
                   "round_trips": [dict(asdict(t), alarm=t.alarm) for t in trips]}, sys.stdout, indent=1)
        print()
    else:
        for w in warnings:
            print("warning:", w, file=sys.stderr)
        print_table(trips, label, holds is not None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
