#!/usr/bin/env python3
"""Rank two-stop round-trip trades in Sci-Fi Trading Voyage by profit per hour.

Model (see README.md for how each assumption was measured):
  * A trip is a cycle between two stops, A -> B -> A. On each leg you fill the
    hold with the single good that earns the most margin per cargo unit.
  * Margin per cargo = (buy price at destination - sell price at origin) / size.
  * Leg time = overhead + distance * seconds_per_gm. Measured for the first fleet:
    2.0 s/Gm and 0 s overhead (7 Gm took 14 s; 1700 Gm took 56:40).
  * Cash is unlimited and prices don't move as you trade (they shift daily).

The score that doesn't depend on the ship is margin per cargo per Gm flown. A
ship's profit/hr = that score * cargo * 3600 / seconds_per_gm.

Usage:
  py -3 trade_routes.py                       # top 20, 2.0 s/Gm, cargo 1
  py -3 trade_routes.py --cargo 4000 --top 10
  py -3 trade_routes.py --from Troy           # only round trips touching Troy
  py -3 trade_routes.py --json > routes.json  # machine-readable, for ship pickers
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
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent / "data" / "market.csv"
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
    good: str | None        # None = fly empty
    margin_per_cargo: float  # credits per cargo unit carried


@dataclass
class RoundTrip:
    a: str
    b: str
    distance_gm: float
    out: Leg
    back: Leg
    margin_per_cargo: float      # whole cycle, per cargo unit
    per_cargo_per_kgm: float     # ship-independent score: margin / 1000 Gm flown
    seconds: float               # cycle time at the given speed/overhead
    profit_per_hour: float       # for the given cargo


def load_market(path: Path = DEFAULT_DATA):
    """Return (quotes, coords) from a market CSV."""
    quotes, coords = [], {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            p = r["planet"].strip()
            xy = (float(r["x"]), float(r["y"]))
            if coords.setdefault(p, xy) != xy:
                raise ValueError(f"{p}: conflicting coordinates {coords[p]} vs {xy}")
            side = r["side"].strip().upper()
            if side not in ("S", "B"):
                raise ValueError(f"{p}/{r['good']}: side must be S or B, got {side!r}")
            quotes.append(Quote(p, r["good"].strip(), int(r["size"]), side, int(r["price"])))
    return quotes, coords


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


def best_leg(origin, dest, sells, buys) -> Leg:
    best = Leg(origin, dest, None, 0.0)
    for good, q in sells[origin].items():
        b = buys[dest].get(good)
        if b and b.price > q.price:
            m = (b.price - q.price) / q.size
            if m > best.margin_per_cargo:
                best = Leg(origin, dest, good, m)
    return best


def round_trips(quotes, coords, cargo: float = 1.0, seconds_per_gm: float = SECONDS_PER_GM,
                overhead_s: float = 0.0):
    """Every unordered stop pair with any profit, best first."""
    sells, buys = defaultdict(dict), defaultdict(dict)
    for q in quotes:
        (sells if q.side == "S" else buys)[q.planet][q.good] = q
    out = []
    for a, b in itertools.combinations(sorted(coords), 2):
        f, r = best_leg(a, b, sells, buys), best_leg(b, a, sells, buys)
        m = f.margin_per_cargo + r.margin_per_cargo
        if m <= 0:
            continue
        d = math.dist(coords[a], coords[b])
        secs = 2 * (overhead_s + d * seconds_per_gm)
        out.append(RoundTrip(a, b, d, f, r, m,
                             per_cargo_per_kgm=m / (2 * d) * 1000 if d else math.inf,
                             seconds=secs,
                             profit_per_hour=m * cargo * 3600 / secs if secs else math.inf))
    out.sort(key=lambda t: t.profit_per_hour, reverse=True)
    return out


def _fmt_leg(leg: Leg) -> str:
    return f"{leg.good} {leg.margin_per_cargo:.2f}" if leg.good else "(empty)"


def print_table(trips, cargo):
    print(f"{'#':>3} {'profit/hr':>14} {'cycle':>9} {'dist Gm':>8}  {'A':15} {'B':15} "
          f"{'A -> B':24} B -> A")
    for i, t in enumerate(trips, 1):
        mins = t.seconds / 60
        print(f"{i:3} {t.profit_per_hour:14,.0f} {mins:8.1f}m {t.distance_gm:8.0f}  "
              f"{t.a:15} {t.b:15} {_fmt_leg(t.out):24} {_fmt_leg(t.back)}")
    print(f"\n(profit/hr at cargo={cargo:g}; multiply by your ship's cargo if you left it at 1)")


def selftest() -> int:
    """Check against values worked out by hand from the 2026-10-06 snapshot."""
    quotes, coords = load_market()
    trips = {(t.a, t.b): t for t in round_trips(quotes, coords)}
    checks = []

    def eq(name, got, want, tol=1e-3):
        ok = abs(got - want) <= tol
        checks.append(ok)
        print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.4f} (want {want})")

    # Two timing runs: 7 Gm took 14 s and 1700 Gm took 3400 s, which gives 2.0 s/Gm and 0 s overhead
    spg = (3400 - 14) / (1700 - 7)
    eq("seconds per Gm from the two timings", spg, 2.0)
    eq("overhead from the two timings", 14 - 7 * spg, 0.0)
    t = trips[("AlphaCentA", "Proxima")]
    eq("Proxima->AlphaCentA ResearchData3 margin", t.back.margin_per_cargo,
       (3078000 - 2536500) / 100000)
    eq("  ...profit/hr per cargo", t.profit_per_hour, 5.415 * 3600 / (4 * math.dist((1046, 1704), (1040, 1700))))
    t = trips[("BlackGoldStar", "Troy")]
    eq("BlackGoldStar->Troy Comm Comp", t.out.margin_per_cargo, (58604 - 18032) / 2000)
    eq("Troy->BlackGoldStar TrojiteCry3", t.back.margin_per_cargo, (7348000 - 6145600) / 240000)
    t = trips[("Ares", "Free Port")]
    eq("Free Port->Ares Collect2", t.back.margin_per_cargo, (245600 - 74400) / 8000)
    ranked = round_trips(quotes, coords)
    checks.append(ranked[0].a == "AlphaCentA" and ranked[1].a == "BlackGoldStar")
    print(f"  {'ok ' if checks[-1] else 'BAD'} ranking: #1 {ranked[0].a}/{ranked[0].b}, "
          f"#2 {ranked[1].a}/{ranked[1].b}")
    w = audit(quotes)
    checks.append(not any(x.startswith("SIZE") for x in w))
    print(f"  {'ok ' if checks[-1] else 'BAD'} no size mismatches in the corrected snapshot")
    print("PASS" if all(checks) else "FAIL")
    return 0 if all(checks) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", type=Path, default=DEFAULT_DATA, help="market CSV (default data/market.csv)")
    ap.add_argument("--cargo", type=float, default=1.0, help="ship cargo capacity (Size units)")
    ap.add_argument("--sec-per-gm", type=float, default=SECONDS_PER_GM, help="ship travel time per Gm")
    ap.add_argument("--overhead", type=float, default=0.0, help="fixed seconds per leg (dock/launch)")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--from", dest="stop", help="only round trips that include this stop")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--audit", action="store_true", help="only print likely-typo warnings")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    quotes, coords = load_market(args.data)
    warnings = audit(quotes)
    if args.audit:
        print("\n".join(warnings) or "no warnings")
        return 0
    trips = round_trips(quotes, coords, args.cargo, args.sec_per_gm, args.overhead)
    if args.stop:
        if args.stop not in coords:
            ap.error(f"unknown stop {args.stop!r}; known: {', '.join(sorted(coords))}")
        trips = [t for t in trips if args.stop in (t.a, t.b)]
    trips = trips[: args.top] if args.top > 0 else trips
    if args.json:
        json.dump({"cargo": args.cargo, "seconds_per_gm": args.sec_per_gm, "overhead_s": args.overhead,
                   "warnings": warnings, "round_trips": [asdict(t) for t in trips]}, sys.stdout, indent=1)
        print()
    else:
        for w in warnings:
            print("warning:", w, file=sys.stderr)
        print_table(trips, args.cargo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
