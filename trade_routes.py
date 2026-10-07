#!/usr/bin/env python3
"""Rank two-stop round-trip trades in Sci-Fi Trading Voyage by profit per hour.

Model (see README.md for how each assumption was measured):
  * A trip is a cycle between two stops, A -> B -> A.
  * Margin per unit = buy price at destination - sell price at origin; a unit
    takes `size` cargo space.
  * Leg time = overhead + distance * seconds_per_gm, with seconds_per_gm = 10,000 / warp
    and 0 s overhead. Stopwatch runs (data/timings.csv) match this to the second.
  * Profit = listed margin * (1 + route bonus + global bonus). The route bonus is per level
    (bonus_pct in data/routes.csv); the global bonus (--global-bonus, default 45%) is account-wide.
  * Cash is unlimited and prices don't move as you trade (they shift daily).

Two loading modes:
  * continuous (default): the hold fills with the best margin-per-cargo good, as if
    fractional units could be bought. Gives a score per cargo unit that doesn't
    depend on the ship, and an upper bound on whole-unit loading.
  * whole units (--ships, or --cargo with --whole-units): goods are bought in whole
    units only, and the hold is packed with the best mix of goods (an unbounded
    knapsack). A fleet's cargo is ONE pooled hold (the game's own loading logs match
    this exactly); --separate-holds packs each ship on its own instead.

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
  py -3 trade_routes.py --timings                  # compare predicted leg times with the stopwatch
  py -3 trade_routes.py --premiums                 # each price as a multiple of its class average
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

MARKET_DIR = Path(__file__).resolve().parent / "data" / "market"   # one CSV per game day: YYYY-MM-DD.csv


def market_snapshot(date: str | None = None) -> Path:
    """The price file for a game day (YYYY-MM-DD), or the latest one."""
    files = sorted(MARKET_DIR.glob("????-??-??.csv"))
    if not files:
        raise FileNotFoundError(f"no price snapshots in {MARKET_DIR}")
    if date is None:
        return files[-1]
    f = MARKET_DIR / f"{date}.csv"
    if not f.exists():
        raise FileNotFoundError(f"no snapshot for {date}; have {', '.join(x.stem for x in files)}")
    return f


DEFAULT_DATA = None  # resolved to the latest snapshot at call time
DEFAULT_PORTS = Path(__file__).resolve().parent / "data" / "ports.csv"
DEFAULT_ROUTES = Path(__file__).resolve().parent / "data" / "routes.csv"
DEFAULT_SHIPS = Path(__file__).resolve().parent / "data" / "ships.csv"
DEFAULT_ORACLE = Path(__file__).resolve().parent / "data" / "oracle.csv"
DEFAULT_TIMINGS = Path(__file__).resolve().parent / "data" / "timings.csv"
ALARMS = ["Low", "Medium", "High", "Extreme"]  # the game's port alarm levels, in order
SECONDS_PER_GM = 2.0  # measured with a stopwatch, first fleet (2x FG300: 3CP, 2000 cargo each)
REF_WARP = 5000       # FG300's listed warp

# Two ways to turn warp into travel time. They disagree by 2.78x:
#   "timed" : s/Gm = 2.0 * 5000 / warp, calibrated on the FG300 stopwatch run (1700 Gm in 56:40).
#             Predicts every stopwatch leg in data/timings.csv to the second, for warp 5000 and
#             warp 2250 alike. DEFAULT.
#   "warp"  : warp is Gm/hr, so s/Gm = 3600 / warp. Matched the game's own $/hr figure on the first
#             two oracle rows, but that was coincidence: it is 1.3-1.8x on later rows, and it
#             contradicts every stopwatch run. Kept for comparison.
# Both are proportional to 1/warp, so they rank ships and routes identically; only absolute $/hr differs.
SPEED_MODELS = {
    "warp": lambda warp: 3600 / warp,
    "timed": lambda warp: SECONDS_PER_GM * REF_WARP / warp,
}
speed_model = "timed"
# The game pools a fleet's cargo into one hold: 10 Reliiat T + 10 NOMA (no hold over 2,000) loaded
# 9 RefOre1 (size 4,000) and 126 Std Uniform1 -- exactly the pooled-hold packing (separate: 0 and 120).
separate_holds = False
# Account-wide profit bonus, added to the route's. Measured 2026-10-06: Std Uniform1 sold on a +15% route
# made 3,628 on a listed margin of 2,268 (x1.600 = 1 + 0.15 + 0.45); 15 x FG300 and 3 x Conomara on a
# +12% route both imply +0.451. Its in-game source is not yet identified, and it may change over time.
GLOBAL_BONUS = 0.45
global_bonus = GLOBAL_BONUS


# Goods come in classes, written as the name's trailing digit: 1 is cheap, 3 is expensive. These two
# are recorded without the digit; their prices put them in classes 2 and 3.
CLASS_OVERRIDES = {"Comm Comp": 2, "Int Nav Sys": 3}
# The game's average price per cargo unit for each class. Class 1: Reach buys ConsumGood1 (size 2,000)
# at 17,688, which the game shows as +2,898% over average, so 17,688 / 2,000 / 29.98 = 0.295. Class 2:
# 10, the game's figure. Class 3's average varies by good (about 25 to 30), so it is estimated per good
# as the median of that day's quotes.
CLASS_AVG = {1: 0.295, 2: 10.0}


def good_class(good: str) -> int | None:
    if good in CLASS_OVERRIDES:
        return CLASS_OVERRIDES[good]
    m = re.search(r"(\d)\s*$", good)
    return int(m.group(1)) if m else None


def class_averages(quotes) -> dict[str, tuple[float, bool]]:
    """{good: (average price per cargo unit, estimated?)} -- the game's class average where known."""
    per_cargo = defaultdict(list)
    for q in quotes:
        per_cargo[q.good].append(q.price / q.size)
    out = {}
    for good, v in per_cargo.items():
        c = good_class(good)
        out[good] = (CLASS_AVG[c], False) if c in CLASS_AVG else (statistics.median(v), True)
    return out


def seconds_per_gm_for(warp: float) -> float:
    return SPEED_MODELS[speed_model](warp)


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


def load_market(path: Path | None = None, ports: Path = DEFAULT_PORTS):
    """Return (quotes, coords, alarms) from a price snapshot (default: latest) and the ports CSV."""
    path = path or market_snapshot()
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
            quotes.append(Quote(p, r["good"].strip(), int(r["size"].replace(",", "")), side,
                                int(r["price"].replace(",", ""))))
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

    @property
    def cargo_holds(self) -> list[int]:
        """The holds to pack: one pooled hold, or each ship's with --separate-holds."""
        return list(self.holds) if separate_holds else [sum(self.holds)]

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
    bonus_pct: float = 0.0   # the game's "+N% profit" for the route's level


def route_bonus(routes, a, b) -> float:
    """The route's profit bonus as a fraction (0.12 for +12%); 0 if not recorded."""
    info = (routes or {}).get(frozenset((a, b)))
    return info.bonus_pct / 100 if info else 0.0


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
                                 r.get("upgrade_cost", "").strip(), r.get("notes", "").strip(),
                                 float(r.get("bonus_pct") or 0))
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
                overhead_s: float = 0.0, holds: list[int] | None = None, alarms=None, routes=None):
    """Every unordered stop pair with any profit, best first.

    holds=None -> continuous model scaled by `cargo`; otherwise whole units per hold.
    routes -> apply each recorded route's level bonus.
    """
    sells, buys = book(quotes)
    out = []
    for a, b in itertools.combinations(sorted(coords), 2):
        t = make_trip(a, b, sells, buys, coords, cargo, seconds_per_gm, overhead_s, holds, alarms,
                      bonus=route_bonus(routes, a, b))
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
              holds=None, alarms=None, bonus: float = 0.0) -> RoundTrip:
    """bonus: the route's level bonus as a fraction. It is added to the global bonus, and the
    total multiplies the listed margin."""
    f = make_leg(a, b, sells, buys, holds, cargo)
    r = make_leg(b, a, sells, buys, holds, cargo)
    mult = 1 + bonus + global_bonus
    m = (f.margin_per_cargo + r.margin_per_cargo) * mult
    cyc = (f.margin + r.margin) * mult
    d = math.dist(coords[a], coords[b])
    secs = 2 * (overhead_s + d * seconds_per_gm)
    return RoundTrip(a, b, d, f, r, m,
                     per_cargo_per_kgm=m / (2 * d) * 1000 if d else math.inf,
                     seconds=secs, cycle_margin=cyc,
                     profit_per_hour=cyc * 3600 / secs if secs else math.inf,
                     alarm_a=(alarms or {}).get(a, ""), alarm_b=(alarms or {}).get(b, ""))


def fill_cap(a, b, sells, buys, coords, cap, ship_types, seconds_per_gm, overhead_s, bonus=0.0):
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
                      overhead_s=overhead_s, holds=[st.cargo] * n if separate_holds else [st.cargo * n],
                      bonus=bonus)
        rows.append((t.profit_per_hour, st, n, t))
    rows.sort(key=lambda r: r[0], reverse=True)
    return rows


def route_card(a, b, quotes, coords, alarms, routes, ship_types, seconds_per_gm, overhead_s,
               fleet: Fleet | None = None):
    sells, buys = book(quotes)
    bonus = route_bonus(routes, a, b)
    t = make_trip(a, b, sells, buys, coords, seconds_per_gm=seconds_per_gm, overhead_s=overhead_s,
                  alarms=alarms, bonus=bonus)
    info = routes.get(frozenset((a, b)))
    lvl = f"level {info.level}, cap {info.cp_cap} CP" if info and info.cp_cap else "level/cap not recorded"
    lvl += f", +{bonus:.0%} route bonus" if bonus else ", no route bonus recorded"
    lvl += f", +{global_bonus:.0%} global"
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
                                       seconds_per_gm, overhead_s, bonus):
            spd = f"{st.seconds_per_gm:.2f}s/Gm" if st.seconds_per_gm else "speed?"
            print(f"      {n:3} x {st.name:14} {n * st.cp:4} CP {n * st.cargo:>10,} cargo {spd:>10} -> {pph:14,.0f}/hr"
                  f"   [{_fmt_leg(ft.out, True)} / {_fmt_leg(ft.back, True)}]")
    if fleet:
        spg = seconds_per_gm  # already resolved in main(): --sec-per-gm, else the fleet's slowest ship
        ft = make_trip(a, b, sells, buys, coords, seconds_per_gm=spg, overhead_s=overhead_s,
                       holds=fleet.cargo_holds, bonus=bonus)
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


def diff_days(old: str, new: str, ports: Path = DEFAULT_PORTS):
    """What changed between two game days: goods added/removed, sizes, and price moves."""
    qa, _, _ = load_market(market_snapshot(old), ports)
    qb, _, _ = load_market(market_snapshot(new), ports)
    ka = {(q.planet, q.good, q.side): q for q in qa}
    kb = {(q.planet, q.good, q.side): q for q in qb}
    gone, added = sorted(set(ka) - set(kb)), sorted(set(kb) - set(ka))
    print(f"{old} -> {new}: {len(ka)} -> {len(kb)} quotes")
    for k in gone:
        print(f"  REMOVED  {k[0]} {k[1]} ({k[2]})")
    for k in added:
        print(f"  ADDED    {k[0]} {k[1]} ({k[2]}) size {kb[k].size:,} price {kb[k].price:,}")
    changes = defaultdict(list)
    for k in sorted(set(ka) & set(kb)):
        a, b = ka[k], kb[k]
        if a.size != b.size:
            print(f"  SIZE     {k[0]} {k[1]}: {a.size:,} -> {b.size:,}")
        changes[k[1]].append((b.price / a.price - 1) * 100)
    print("  price change by good (median % across stops, min..max):")
    for good, ch in sorted(changes.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f"    {good:15} {statistics.median(ch):+7.2f}%   ({min(ch):+.2f} .. {max(ch):+.2f}, {len(ch)} quotes)")


def premium_report(quotes, alarms, label: str):
    """Each price as a multiple of its class average. Stops sell at about the average; the premiums
    are on the buying side, so margin per cargo is roughly average x (buyer's multiple - seller's)."""
    avg = class_averages(quotes)
    by_good = defaultdict(list)
    for q in quotes:
        by_good[q.good].append(q)
    print(f"prices as a multiple of the class average ({label}); est = class 3, estimated per good")
    for good in sorted(by_good, key=lambda g: (good_class(g) or 9, g)):
        a, est = avg[good]
        qs = by_good[good]
        x = lambda q: q.price / q.size / a
        print(f"\n{good}  class {good_class(good) or '?'}  avg {a:,.3f}/cargo{' est' if est else ''}  "
              f"size {qs[0].size:,}")
        sellers = sorted((q for q in qs if q.side == "S"), key=x)
        buyers = sorted((q for q in qs if q.side == "B"), key=x, reverse=True)
        if sellers:
            print("  sold by   " + ", ".join(f"{q.planet} {x(q):.2f}x" for q in sellers))
        for q in buyers:
            margin = (q.price / q.size - sellers[0].price / sellers[0].size) if sellers else None
            m = f"  {margin:,.2f}/cargo over the cheapest seller" if margin is not None else ""
            print(f"  bought by {q.planet:15} {x(q):6.2f}x ({x(q) - 1:+.0%})  {alarms.get(q.planet, '?'):8}{m}")


def premium_trend(ports: Path = DEFAULT_PORTS):
    """Per class, per game day: the median seller's and buyer's multiple, and the best buyer."""
    print("\nby class, per game day (median seller, median buyer, best buyer):")
    for path in sorted(MARKET_DIR.glob("*.csv")):
        quotes, _, _ = load_market(path, ports)
        avg = class_averages(quotes)
        for c in sorted({good_class(q.good) for q in quotes}, key=lambda c: c or 9):
            qs = [q for q in quotes if good_class(q.good) == c]
            x = {q: q.price / q.size / avg[q.good][0] for q in qs}
            s = [x[q] for q in qs if q.side == "S"]
            b = [q for q in qs if q.side == "B"]
            top = max(b, key=x.get) if b else None
            print(f"  {path.stem}  class {c or '?'}  sellers {statistics.median(s) if s else 0:5.2f}x  "
                  f"buyers {statistics.median(x[q] for q in b) if b else 0:5.2f}x  "
                  + (f"best {x[top]:.2f}x ({top.planet} {top.good})" if top else ""))


def oracle_bonus(row, routes) -> float:
    v = (row.get("bonus_pct") or "").strip()
    return float(v) / 100 if v else route_bonus(routes, row["route_a"].strip(), row["route_b"].strip())


def load_timings(path: Path = DEFAULT_TIMINGS) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def timing_report(coords, ship_types, path: Path = DEFAULT_TIMINGS):
    """Predicted one-way leg time for each stopwatch run, under both speed models."""
    for r in load_timings(path):
        a, b = r["route_a"].strip(), r["route_b"].strip()
        fleet = parse_ships(r["fleet"], ship_types)
        d = math.dist(coords[a], coords[b])
        got = float(r["leg_seconds"])
        print(f"{r['date']}  {a} -> {b}  {d:,.0f} Gm  fleet {r['fleet']}  stopwatch {got / 60:.2f} min")
        warps = [st.warp for st in fleet.ships if st]
        for name, model in SPEED_MODELS.items():
            want = d * model(min(warps))
            print(f"   {name:6} {want / 60:8.2f} min  ({want / got:5.2f}x stopwatch)")


def oracle_report(quotes, coords, ship_types, routes=None, path: Path = DEFAULT_ORACLE):
    """Compare each logged game $/hr figure against the model's open choices:
    separate vs pooled holds, and timed (stopwatch) vs warp-as-Gm/hr speed. The route bonus is the
    row's own bonus_pct (the route's level can change), else routes.csv's."""
    if not path.exists():
        print(f"no {path}")
        return
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        snap = MARKET_DIR / f"{r['date'].strip()}.csv"
        day_quotes = load_market(snap)[0] if snap.exists() else quotes
        sells, buys = book(day_quotes)
        a, b, game = r["route_a"].strip(), r["route_b"].strip(), float(r["game_per_hr"])
        fleet = parse_ships(r["fleet"], ship_types)
        warps = [st.warp for st in fleet.ships if st]
        bonus = oracle_bonus(r, routes)
        print(f"{r['date']}  {a} <-> {b}  fleet {r['fleet']}  +{bonus:.0%} route +{global_bonus:.0%} global  game says {game:,.0f}/hr"
              f"  (prices: {snap.stem if snap.exists() else 'latest snapshot -- none for that day'})")
        if len(warps) != len(fleet.ships):
            print("   (a ship has no warp speed; skipped)")
            continue
        speeds = {"timed (stopwatch)": SPEED_MODELS["timed"](min(warps)),
                  "warp = Gm/hr": SPEED_MODELS["warp"](min(warps))}
        for hold_name, holds in (("separate holds", fleet.holds), ("pooled hold", [sum(fleet.holds)])):
            for sp_name, spg in speeds.items():
                t = make_trip(a, b, sells, buys, coords, seconds_per_gm=spg, holds=holds, bonus=bonus)
                print(f"   {hold_name:15} {sp_name:26} {spg:5.2f} s/Gm -> {t.profit_per_hour:12,.0f}/hr"
                      f"  ({t.profit_per_hour / game:5.2f}x game)")


def selftest() -> int:
    """Check against values worked out by hand from the 2026-10-06 snapshot."""
    quotes, coords, alarms = load_market(market_snapshot("2026-10-06"))
    global global_bonus
    saved_gb, global_bonus = global_bonus, 0.0  # the hand-worked values below are listed margins
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
    check("Ares/Free Port takes its worse end: High (Free Port, since the 2026-10-07 changeover)",
          trips[("Ares", "Free Port")].alarm == "High")
    check("BlackGoldStar/Troy is High/High", trips[("BlackGoldStar", "Troy")].alarm == "High")
    check("goods classes: Comm Comp 2, Int Nav Sys 3, Nuke Battery 2 2, Food1 1",
          [good_class(g) for g in ("Comm Comp", "Int Nav Sys", "Nuke Battery 2", "Food1")] == [2, 3, 2, 1])
    q = next(q for q in quotes if (q.planet, q.good) == ("Reach", "ConsumGood1"))
    eq("Reach ConsumGood1 is the game's +2,898% over the class average", q.price / q.size / CLASS_AVG[1], 29.98,
       tol=0.005)
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
    global speed_model
    saved, speed_model = speed_model, "timed"
    eq("timed model: FG300 (the stopwatch fleet) runs at the measured 2.0 s/Gm",
       types["FG300"].seconds_per_gm, 2.0)
    eq("timed model: ST59 (warp 2250) is 2.22x slower", types["ST59"].seconds_per_gm, 2.0 * 5000 / 2250)
    speed_model = "warp"
    eq("warp model: FG300 at 3600/5000 s/Gm", types["FG300"].seconds_per_gm, 0.72)
    eq("mixed fleet moves at its slowest ship", parse_ships("FG300x2,ST59", types).seconds_per_gm,
       3600 / 2250)
    speed_model = saved
    check("build limit is flagged", parse_ships("FG300x16", types).over_limit() != [])
    # the game's loading log, 10 Reliiat T + 10 NOMA on Orgin Station <-> BountPlanet
    fl = parse_ships("Reliiat Tx10,NOMAx10", types)
    sells, buys = book(quotes)
    t = make_trip("Orgin Station", "BountPlanet", sells, buys, coords, holds=fl.cargo_holds)
    eq("pooled hold: loads 126 Std Uniform1 at Orgin (game: 126 for 10,080)", t.out.load.get("Std Uniform1", 0), 126)
    eq("pooled hold: loads 9 RefOre1 at BountPlanet (game: 9 for 10,170)", t.back.load.get("RefOre1", 0), 9)
    routes = load_routes()
    check("routes.csv: Free Port/Ares is level 4, 160 CP either way round",
          routes[frozenset(("Ares", "Free Port"))].cp_cap == 160)
    sells, buys = book(quotes)
    rows = fill_cap("Free Port", "Ares", sells, buys, coords, 160, types, 2.0, 0.0)
    eq("160 CP would fit 20 AC721, but the build limit is 15", {r[1].name: r[2] for r in rows}["AC721"], 15)
    eq("routes.csv: Free Port/Ares (level 4) bonus is +24%", route_bonus(routes, "Ares", "Free Port"), 0.24)
    global_bonus = saved_gb
    t = make_trip("Orgin Station", "BountPlanet", sells, buys, coords, holds=[38000], bonus=0.15)
    eq("Std Uniform1 sale: 126 x (98 - 80) x (1 + 0.15 + 0.45) rounds down to the game's 3,628",
       math.floor(t.out.margin * (1 + 0.15 + global_bonus)), 3628)
    # the game's own $/hr, on rows where the fleet and its loads are known to be clean
    for r in csv.DictReader(open(DEFAULT_ORACLE, newline="")):
        if "CLEAN" not in r["notes"]:
            continue
        fl = parse_ships(r["fleet"], types)
        t = make_trip(r["route_a"], r["route_b"], sells, buys, coords, seconds_per_gm=fl.seconds_per_gm,
                      holds=fl.cargo_holds, bonus=float(r["bonus_pct"]) / 100)
        ratio = t.profit_per_hour / float(r["game_per_hr"])
        check(f"oracle {r['route_a']}/{r['route_b']} {r['fleet']}: predicted {ratio:.3f}x game", 0.98 <= ratio <= 1.02)
    # the stopwatch: the default (timed) model must predict every leg within 2%
    for r in load_timings():
        fl = parse_ships(r["fleet"], types)
        want = math.dist(coords[r["route_a"].strip()], coords[r["route_b"].strip()]) * fl.seconds_per_gm
        ratio = want / float(r["leg_seconds"])
        check(f"stopwatch {r['route_a']}->{r['route_b']} {r['fleet']}: predicted {ratio:.3f}x measured",
              0.98 <= ratio <= 1.02)
    print("PASS" if all(checks) else "FAIL")
    return 0 if all(checks) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", type=Path, default=None, help="a price CSV (default: latest in data/market/)")
    ap.add_argument("--date", help="use the price snapshot for this game day, YYYY-MM-DD")
    ap.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"), help="compare two game days' prices")
    ap.add_argument("--ports", type=Path, default=DEFAULT_PORTS, help="ports CSV (default data/ports.csv)")
    ap.add_argument("--cargo", type=float, default=1.0, help="cargo capacity (Size units)")
    ap.add_argument("--whole-units", action="store_true",
                    help="buy whole units only; --cargo is one pooled hold")
    ap.add_argument("--separate-holds", action="store_true",
                    help="pack each ship's hold on its own (default: the fleet's cargo is one pooled hold)")
    ap.add_argument("--ships", help="a fleet, whole units: e.g. 25200x12, 130000x3,2000x2, "
                                    "or ship names from ships.csv like hauler-28cpx3")
    ap.add_argument("--route", nargs=2, metavar=("A", "B"), help="print a score card for one route")
    ap.add_argument("--known-routes", action="store_true",
                    help="score every route in routes.csv, filling its CP cap with the best ship type")
    ap.add_argument("--routes-file", type=Path, default=DEFAULT_ROUTES)
    ap.add_argument("--ships-file", type=Path, default=DEFAULT_SHIPS)
    ap.add_argument("--sec-per-gm", type=float, default=None,
                    help="travel time per Gm (default: from the fleet's slowest warp, else an FG300's)")
    ap.add_argument("--speed-model", choices=sorted(SPEED_MODELS), default="timed",
                    help="timed = stopwatch-calibrated (default) or warp = Gm/hr (2.78x faster)")
    ap.add_argument("--overhead", type=float, default=0.0, help="fixed seconds per leg (dock/launch)")
    ap.add_argument("--global-bonus", type=float, default=GLOBAL_BONUS * 100,
                    help="account-wide profit bonus in percent, added to each route's (default %(default)g)")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--from", dest="stop", help="only round trips that include this stop")
    ap.add_argument("--max-alarm", choices=ALARMS, help="only routes whose BOTH ports are at most this alarm")
    ap.add_argument("--by-alarm", action="store_true", help="best route under each alarm cap")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--audit", action="store_true", help="only print likely-typo warnings")
    ap.add_argument("--premiums", action="store_true",
                    help="each price as a multiple of its class average, and the trend per class by day")
    ap.add_argument("--oracle", action="store_true", help="compare predictions with data/oracle.csv")
    ap.add_argument("--timings", action="store_true", help="compare leg times with data/timings.csv")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    global speed_model
    speed_model = args.speed_model
    global separate_holds
    separate_holds = args.separate_holds
    global global_bonus
    global_bonus = args.global_bonus / 100
    if args.diff:
        diff_days(*args.diff, ports=args.ports)
        return 0
    data = args.data or market_snapshot(args.date)
    quotes, coords, alarms = load_market(data, args.ports)
    if not args.json and not args.audit:
        print(f"prices: {data.name}", file=sys.stderr)
    if args.premiums:
        premium_report(quotes, alarms, data.stem)
        premium_trend(args.ports)
        return 0
    warnings = audit(quotes)
    if args.audit:
        print("\n".join(warnings) or "no warnings")
        return 0
    ship_types = load_ships(args.ships_file)
    routes = load_routes(args.routes_file)
    fleet = None
    if args.ships:
        fleet = parse_ships(args.ships, ship_types)
        holds = fleet.cargo_holds
        label = (f"whole units, {len(fleet.holds)} ships, {sum(fleet.holds):,} cargo "
                 + ("in separate holds" if separate_holds else "pooled"))
    elif args.whole_units:
        holds = [int(args.cargo)]
        label = f"whole units, one pooled hold of {int(args.cargo):,}"
    else:
        holds = None
        label = f"continuous loading, cargo {args.cargo:g}"
    if args.sec_per_gm is None:
        args.sec_per_gm = (fleet.seconds_per_gm if fleet else None) or seconds_per_gm_for(REF_WARP)
    if fleet and fleet.seconds_per_gm:
        label += f", {args.sec_per_gm:.2f} s/Gm (slowest ship)"
    if args.oracle:
        oracle_report(quotes, coords, ship_types, routes)
        return 0
    if args.timings:
        timing_report(coords, ship_types)
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
            bonus = info.bonus_pct / 100
            best = fill_cap(a, b, sells, buys, coords, info.cp_cap or 0, ship_types,
                            args.sec_per_gm, args.overhead, bonus) if info.cp_cap else []
            t = make_trip(a, b, sells, buys, coords, seconds_per_gm=args.sec_per_gm,
                          overhead_s=args.overhead, alarms=alarms, bonus=bonus)
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
    trips = round_trips(quotes, coords, args.cargo, args.sec_per_gm, args.overhead, holds, alarms, routes)
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
