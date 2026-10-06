# Sci-Fi Trading Voyage — trade-route calculator

Ranks every **two-stop round trip** (A → B → A) in the Sci-Fi Trading Voyage trading game by
**profit per hour**. On each leg the hold is filled with the single good that earns the most margin
per cargo unit; an empty leg counts as zero.

```
py -3 trade_routes.py                          # per cargo unit (fractional loading)
py -3 trade_routes.py --ships 130000x3         # whole units, three separate 130,000 holds
py -3 trade_routes.py --ships 25200x12,2000x2  # mixed fleet
py -3 trade_routes.py --cargo 302400 --whole-units   # whole units, one pooled fleet hold
py -3 trade_routes.py --from Troy              # only trips touching one stop
py -3 trade_routes.py --json > routes.json     # for other tools (e.g. a ship picker)
py -3 trade_routes.py --audit                  # likely-typo warnings only
py -3 trade_routes.py --selftest               # values checked by hand
```

## Data — `data/market.csv`

One row per (stop, good): `planet,x,y,good,size,side,price`.

- `side` **S** = the stop sells to you (buy here), **B** = the stop buys from you (sell here).
- `size` = cargo space one unit takes; `price` is for one unit.
- `x,y` = map coordinates; distance is straight-line, in Gm.

Snapshot: all 25 stops, recorded 2026-10-06. **Prices change daily**, so re-enter them before you
trust a ranking. That said, distance and choice of good have mattered more than the daily swings.

`--audit` flags the two kinds of typo seen so far: a `size` that doesn't match the other rows for
that good, and a per-cargo price more than 2× away from that good's median. A flagged price can be
real. The arbitrage *is* the outliers. These outliers were checked in the game and are real:
TycoLab Elec1, Troy Comm Comp.

## Model and how each assumption was measured

| Assumption | Basis |
|---|---|
| Leg time = `distance × 2.0 s/Gm`, no fixed overhead | Two timing runs: 7 Gm took 14 s, 1700 Gm took 56:40. Solving those gives 2.000 s/Gm and 0 s overhead. Measured on the first fleet (2× 3CP, 2000 cargo each). |
| Two-stop cycles only | Game rule: trade routes are cyclical between two stops. |
| Goods are bought in **whole units** | Game rule. `--ships` packs each hold separately (an unbounded knapsack over that leg's goods), so a hold smaller than a good's size can't carry it. `--whole-units` treats `--cargo` as one pooled hold. **Not yet confirmed:** whether the game pools a fleet's holds. Test: two 2,000 holds trying to buy one RefOre1 (size 4,000). |
| Unlimited cash | Chosen simplification; cargo space is what limits you. |
| Prices don't move within a session | Observed; prices shift on a daily schedule. |

The score that doesn't depend on the ship is **margin per cargo per Gm flown**. For a specific ship:

```
profit/hr = margin_per_cargo_round_trip × cargo × 3600 / (2 × distance × sec_per_gm + 2 × overhead)
```

so `--cargo` and `--sec-per-gm` cover any ship. Without `--ships`/`--whole-units` the hold fills
fractionally, which is an upper bound. The whole-unit numbers are what a fleet actually earns.

## Results (2026-10-06 snapshot, per cargo unit)

| # | Round trip | Cycle | Profit/hr per cargo |
|---|---|---|---|
| 1 | Proxima → AlphaCentA (ResearchData3), back empty | 29 s | ≈ 676 |
| 2 | BlackGoldStar ↔ Troy (Comm Comp / TrojiteCry3) | 72 min | ≈ 21.0 |
| 3 | Ares ↔ Free Port (Computer2 / Collect2) | 113 min | ≈ 14.5 |

Proxima and AlphaCentA are about 7 Gm apart, which puts that route roughly 30× ahead of the next one.

**Whole units change who can run it.** ResearchData3 is 100,000 cargo per unit, so with separate
holds only a ship with ≥100,000 cargo can carry it. At 2.0 s/Gm, whole units, separate holds:

| Fleet | CP | Cargo | Best route | Profit/hr |
|---|---|---|---|---|
| 12 × 25,200 | 96 | 302,400 | BlackGoldStar ↔ Troy (Proxima impossible) | 4.9 M |
| 2 × 150,000 | 80 | 300,000 | Proxima → AlphaCentA, 2 units | 135 M |
| 3 × 130,000 | 84 | 390,000 | Proxima → AlphaCentA, 3 units | 203 M |
| 50 × 2,000 (combat-fleet scale) | – | 100,000 | BlackGoldStar ↔ Troy | 1.7 M |

These all assume the measured 2.0 s/Gm. Bigger ships may be slower; pass `--sec-per-gm`.

## Not modelled yet

- **Fleet selection.** Fleets are capped at 100 CP, so the goal is to maximise cargo/CP × speed,
  plus enough combat strength to handle pirates. Use `--json` output alongside a ship-data tool.
- Ship speed differences (assumed: a fleet moves at one speed).
- Price changes as you trade, and supply limits.
- Routes with more than two stops (not allowed by the game).
