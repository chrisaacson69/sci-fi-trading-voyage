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
py -3 trade_routes.py --max-alarm Medium       # both ports at most Medium alarm
py -3 trade_routes.py --by-alarm --ships 130000x3   # best route under each alarm cap
py -3 trade_routes.py --json > routes.json     # for other tools (e.g. a ship picker)
py -3 trade_routes.py --audit                  # likely-typo warnings only
py -3 trade_routes.py --route "Free Port" Ares --ships hauler-8cpx20   # score card for one route
py -3 trade_routes.py --known-routes           # score every route in routes.csv
py -3 trade_routes.py --oracle                 # predictions vs the game's own $/hr
py -3 trade_routes.py --selftest               # values checked by hand
```

## Data

- **`data/ports.csv`**, one row per stop: `planet,x,y,alarm`. This is the only place coordinates are stored. `alarm` is the game's port alarm level: Low, Medium, High or Extreme.
- **`data/market/YYYY-MM-DD.csv`**: one price snapshot per **game day**, one row per (stop, good): `planet,good,size,side,price`. The calculator uses the latest file unless you pass `--date`.
- **`data/routes.csv`**: routes you've opened, with their in-game `level` and `cp_cap` (the most CP you can bring). Upgrading a route raises the cap, and upgrades cost more on better routes. `upgrade_cost` is blank until recorded. `bonus_pct` is the game's "+N% profit" for the route's level; the calculator multiplies the margin by it. Observed per-level rates: 3% (Low/Low), 6% (Med/Med and Ext/Med), 7% (Ext/Ext), i.e. apparently set by the route's *safer* port.
- **`data/ships.csv`**: ship types from the game's ship list: `name,cost,limit,cp,cargo,dpm,hp,cruise_min,cruise_max,warp,notes`. `limit` is the build limit, a total across all your fleets, and `dpm` is damage per minute. In every row, `warp` is exactly 5 × `cruise_min`. `--ships` accepts these names, e.g. `ST59x3,FG300x2`, and then knows the fleet's CP, DPM, HP, cost and speed, and warns if you're over a build limit.
- **`data/oracle.csv`**: the game's own $/hr figure for a fleet on a route (`date,route_a,route_b,fleet,game_per_hr,bonus_pct,notes`, fleet written like `--ships`; `bonus_pct` is the route's bonus *at the time*, since levels change). `--oracle` compares each row against the model's open choices: separate vs pooled holds, and timed vs warp-as-Gm/hr speed. It is an observation, not a pass/fail check: the game's figure is not yet explained.
- **`data/timings.csv`**: stopwatch leg times (`date,route_a,route_b,fleet,leg_seconds,notes`, one-way). `--timings` compares them with both speed models, and `--selftest` requires the default model within 2% of each.
- **`data/encounters.csv`** logs pirate attacks, one line per trip or attack. Safe trips count too. Nothing reads it yet; it's the evidence a pirate model will be calibrated from.

In the price files:

- `side` **S** = the stop sells to you (buy here), **B** = the stop buys from you (sell here).
- `size` = cargo space one unit takes; `price` is for one unit.
- Distance is straight-line between the `ports.csv` coordinates, in Gm.

### Daily update (the game day resets at 7 pm)

Prices change at the reset; during this event they have been ramping up. Each day:

1. Write the new prices to `data/market/<game-day>.csv`, same columns as before. Commas inside
   numbers are fine (`18,424`). Planet names must match `data/ports.csv` exactly.
2. `py -3 trade_routes.py --diff <previous-day> <game-day>` lists goods added or removed at each
   stop, any size changes, and each good's median price change.
3. Rerun the routes. `--oracle` compares each `oracle.csv` row against the prices **for that
   row's own day**, so a new day never changes an old comparison.

This file is the interface for any tool that captures prices automatically: write one CSV per game
day in this format and nothing else needs to change.

`--audit` flags the two kinds of typo seen so far: a `size` that doesn't match the other rows for
that good, and a per-cargo price more than 2× away from that good's median. A flagged price can be
real. The arbitrage *is* the outliers. These outliers were checked in the game and are real:
TycoLab Elec1, Troy Comm Comp.

## Model and how each assumption was measured

| Assumption | Basis |
|---|---|
| Leg time = `distance × s/Gm`, no fixed overhead | Two timing runs: 7 Gm took 14 s, 1700 Gm took 56:40. Solving those gives 2.000 s/Gm and 0 s overhead. Measured on the first fleet (2 × FG300). |
| **Speed: s/Gm = 10,000 / warp** (`--speed-model timed`, default) | Calibrated on the FG300 run above, then confirmed to the second on ArbreCAP ↔ EpsiCentauri (630 Gm): 15 × FG300 (warp 5,000) took 21:00, 3 × Conomara (warp 2,250) took 46:40 (`data/timings.csv`). `--speed-model warp` (warp = Gm/hr) was the default until 2026-10-06 because it matched the game's $/hr on the first two oracle rows; that was coincidence, as it is 2.8× too fast against every stopwatch run. A fleet moves at its slowest ship (assumed). |
| **Route bonus** multiplies the margin | The game shows "+N% profit" per route level (`bonus_pct` in `routes.csv`). |
| **Open: the game's own $/hr figure** | With real leg times and the bonus, the model still predicts only 0.39–0.71× the game's figure (`--oracle`). Candidates: global profit bonuses, or backhaul the model can't fit in separate holds (see next row). Until it's explained, a balance-before/after over one round trip is the real check. |
| Two-stop cycles only | Game rule: trade routes are cyclical between two stops. |
| Goods are bought in **whole units**, **each ship's hold separately** | Game rule. `--ships` packs each hold separately (an unbounded knapsack over that leg's goods), so a hold smaller than a good's size can't carry it. The game's $/hr for 10 Reliiat T + 10 NOMA matched separate holds under the old warp speed model; under the stopwatch model pooled fits better (0.76× vs 0.39×), because a pooled hold can carry a RefOre1 (size 4,000) backhaul. Open: check in game whether a fleet carries goods bigger than any single ship's hold. `--whole-units` still treats `--cargo` as one pooled hold if you need it. |
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

*(The fleet tables below predate per-ship speeds; they assume 2.0 s/Gm for every ship. With ST59's
measured-relative 4.44 s/Gm, 3 × ST59 on Proxima → AlphaCentA is about 91 M/hr, not 203 M/hr.)*

**Whole units change who can run it.** ResearchData3 is 100,000 cargo per unit, so with separate
holds only a ship with ≥100,000 cargo can carry it. At 2.0 s/Gm, whole units, separate holds:

| Fleet | CP | Cargo | Best route | Profit/hr |
|---|---|---|---|---|
| 12 × 25,200 | 96 | 302,400 | BlackGoldStar ↔ Troy (Proxima impossible) | 4.9 M |
| 2 × 150,000 | 80 | 300,000 | Proxima → AlphaCentA, 2 units | 135 M |
| 3 × 130,000 | 84 | 390,000 | Proxima → AlphaCentA, 3 units | 203 M |
| 50 × 2,000 (combat-fleet scale) | – | 100,000 | BlackGoldStar ↔ Troy | 1.7 M |

These all assume the measured 2.0 s/Gm. Bigger ships may be slower; pass `--sec-per-gm`.

## Route cards — scoring a route

`--route A B` prints:
- distance, round-trip time, both alarms, and the level and CP cap if recorded
- the profitable goods each way, with margin per unit and the smallest hold that can carry one
- **SCORE**: credits per cargo unit per hour with fractional loading. This doesn't depend on the
  ship, so it says which routes deserve your biggest holds.
- if the cap is known: what each ship type in `ships.csv` earns if it fills the whole cap
- with `--ships`, what that exact fleet earns, and whether it exceeds the cap

`--known-routes` ranks every route in `routes.csv` by its best fill-the-cap figure.

Fill-the-cap assumes a fleet made only of haulers, with no escorts. It shows what the cap is worth,
not a fleet that will survive pirates.

## Pirates — the travel-only ranking is not the real ranking

The first run of the top route (Proxima → AlphaCentA, 3 × 130,000 haulers, 84 CP) was attacked
straight away by an 82 CP pirate fleet. The battle took 14.5 minutes, about 30 round trips' worth
of flying, and lost 1 ship; a second attack took the other 2. Every profit/hr figure here counts
travel time only, so treat it as a ceiling.

What's known about alarm levels so far:
- They roughly follow distance from Orgin Station, except Free Port (808 Gm away, Extreme) and the
  AlphaCent/Proxima cluster (Extreme, though some ports further away are only High).
- A route has two ports. Proxima/AlphaCentA (Extreme/Extreme) met 82 CP fleets. Free Port/Ares
  (Extreme/Medium) has met only 60 CP fleets. So pirate strength isn't simply the worse of the two
  ports, but two routes can't say what the rule is.

The calculator shows both ports' alarms, and `--max-alarm` / `--by-alarm` filter routes so that
**both** ends are at or below a level. Turning alarm levels into attack rate, pirate CP, battle time
and losses needs more rows in `encounters.csv`.

## Not modelled yet

- **Pirate attacks:** how often, how strong, how long a battle takes, and what is lost (see above).
- **Fleet selection.** Fleets are capped at 100 CP, so the goal is to maximise cargo/CP × speed,
  plus enough combat strength to handle pirates. Use `--json` output alongside a ship-data tool.
- Ship speed differences (assumed: a fleet moves at one speed).
- Price changes as you trade, and supply limits.
- Routes with more than two stops (not allowed by the game).
