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
  py -3 trade_routes.py --selftest
"""
from __future__ import annotations

import argparse
import csv
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
ALARMS = ["Low", "Medium", "High", "Extreme"]  # the game's port alarm levels, in order
SECONDS_PER_GM = 2.0  # measured, first fleet (2x 3CP, 2000 cargo each)


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


def parse_ships(spec: str) -> list[int]:
    """'25200x12,130000' -> twelve 25200 holds and one 130000 hold."""
    holds = []
    for part in spec.split(","):
        cap, _, n = part.strip().lower().partition("x")
        holds += [int(float(cap))] * (int(n) if n else 1)
    if not holds or min(holds) <= 0:
        raise ValueError(f"bad --ships spec {spec!r}")
    return holds


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
    sells, buys = defaultdict(dict), defaultdict(dict)
    for q in quotes:
        (sells if q.side == "S" else buys)[q.planet][q.good] = q
    out = []
    for a, b in itertools.combinations(sorted(coords), 2):
        f = make_leg(a, b, sells, buys, holds, cargo)
        r = make_leg(b, a, sells, buys, holds, cargo)
        m = f.margin_per_cargo + r.margin_per_cargo
        cyc = f.margin + r.margin
        if cyc <= 0:
            continue
        d = math.dist(coords[a], coords[b])
        secs = 2 * (overhead_s + d * seconds_per_gm)
        out.append(RoundTrip(a, b, d, f, r, m,
                             per_cargo_per_kgm=m / (2 * d) * 1000 if d else math.inf,
                             seconds=secs, cycle_margin=cyc,
                             profit_per_hour=cyc * 3600 / secs if secs else math.inf,
                             alarm_a=(alarms or {}).get(a, ""), alarm_b=(alarms or {}).get(b, "")))
    out.sort(key=lambda t: t.profit_per_hour, reverse=True)
    return out


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
    print("PASS" if all(checks) else "FAIL")
    return 0 if all(checks) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", type=Path, default=DEFAULT_DATA, help="market CSV (default data/market.csv)")
    ap.add_argument("--ports", type=Path, default=DEFAULT_PORTS, help="ports CSV (default data/ports.csv)")
    ap.add_argument("--cargo", type=float, default=1.0, help="cargo capacity (Size units)")
    ap.add_argument("--whole-units", action="store_true",
                    help="buy whole units only; --cargo is one pooled hold")
    ap.add_argument("--ships", help="separate holds, whole units: e.g. 25200x12 or 130000x3,2000x2")
    ap.add_argument("--sec-per-gm", type=float, default=SECONDS_PER_GM, help="fleet travel time per Gm")
    ap.add_argument("--overhead", type=float, default=0.0, help="fixed seconds per leg (dock/launch)")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--from", dest="stop", help="only round trips that include this stop")
    ap.add_argument("--max-alarm", choices=ALARMS, help="only routes whose BOTH ports are at most this alarm")
    ap.add_argument("--by-alarm", action="store_true", help="best route under each alarm cap")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--audit", action="store_true", help="only print likely-typo warnings")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    quotes, coords, alarms = load_market(args.data, args.ports)
    warnings = audit(quotes)
    if args.audit:
        print("\n".join(warnings) or "no warnings")
        return 0
    if args.ships:
        holds = parse_ships(args.ships)
        label = f"whole units, {len(holds)} separate holds, {sum(holds):,} cargo total"
    elif args.whole_units:
        holds = [int(args.cargo)]
        label = f"whole units, one pooled hold of {int(args.cargo):,}"
    else:
        holds = None
        label = f"continuous loading, cargo {args.cargo:g}"
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
