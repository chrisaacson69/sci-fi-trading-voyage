# Sci-Fi Trading Voyage — trade-route calculator

Ranks every **two-stop round trip** (A → B → A) in the Sci-Fi Trading Voyage trading game by
**profit per hour**. On each leg the hold is filled with the single good that earns the most margin
per cargo unit; an empty leg counts as zero.

```
py -3 trade_routes.py                          # per cargo unit (fractional loading)
py -3 trade_routes.py --ships 130000x3         # whole units, a fleet of three 130,000 ships (pooled)
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
py -3 trade_routes.py --premiums               # each price as a multiple of its class average
py -3 trade_routes.py --selftest               # values checked by hand
```

## Data

- **`data/ports.csv`**, one row per stop: `planet,x,y,alarm`. This is the only place coordinates are stored. `alarm` is the game's port alarm level: Low, Medium, High or Extreme.
- **`data/market/YYYY-MM-DD.csv`**: one price snapshot per **game day**, one row per (stop, good): `planet,good,size,side,price`. The calculator uses the latest file unless you pass `--date`.
- **`data/routes.csv`**: routes you've opened, with their in-game `level` and `cp_cap` (the most CP you can bring). Upgrading a route raises the cap, and upgrades cost more on better routes. `upgrade_cost` is blank until recorded. `bonus_pct` is the game's "+N% profit" for the route's level; the calculator multiplies the margin by it. Observed per-level rates: 3% (Low/Low), 6% (Med/Med and Ext/Med), 7% (Ext/Ext), i.e. apparently set by the route's *safer* port. Routes max out at level 5, and the CP cap is a fixed step × level: 20 CP per level on the short routes near Orgin Station (max 100), 40 per level on the mid routes (ArbreCAP/EpsiCentauri, Free Port/Ares; max 200). Proxima/AlphaCentA is 100 CP at level 2, which suggests 50 per level (max 250, not yet reached). Upgrade costs seen: Orgin/MuCentauri 30,000 (level 3→4) and 40,000 (4→5).
- **`data/route_tiers.csv`**: what each route tier gives and costs per level (`tier,level,cp_cap,bonus_pct,step_cost,total_cost,source`). Easy routes (near Orgin) step 20 CP and +3% per level, mid routes 40 CP and +6%, hard routes 50 CP and +7% (300 CP at level 5, a +100 jump). Upgrade costs: hard doubles each level (9M to 144M, 279M in total), mid triples (240K to 19.44M, 29.04M in total), easy runs 1K, 3K, 8K, 20K, 50K (82K in total). Blank cells are not yet read.
- **`data/ships.csv`**: ship types from the game's ship list: `name,cost,limit,cp,cargo,dpm,hp,cruise_min,cruise_max,warp,type,tp,notes`. `type` is the hull class (FF, DD small; CA, BC, CV cruiser and capital): a fleet mixing the two gets a warning (see Pirates). `tp` is upgrade points, shared within a class (the first word of the name) and spent on one variant; `dpm` is stock. `limit` is the build limit, a total across all your fleets, and `dpm` is damage per minute. In every row, `warp` is exactly 5 × `cruise_min`. `--ships` accepts these names, e.g. `ST59x3,FG300x2`, and then knows the fleet's CP, DPM, HP, cost and speed, and warns if you're over a build limit.
- **`data/oracle.csv`**: the game's own $/hr figure for a fleet on a route (`date,route_a,route_b,fleet,game_per_hr,bonus_pct,global_pct,notes`, fleet written like `--ships`; `bonus_pct` is the route's bonus and `global_pct` the global bonus *at the time*, since both change). `--oracle` compares each row against separate vs pooled holds, and mean vs slowest-ship fleet speed, using that day's prices (or the latest before it). Rows from another account are skipped unless you pass its `--ships-file`. `--selftest` checks the rows whose notes say CLEAN.
- **`data/timings.csv`**: stopwatch leg times (`date,route_a,route_b,fleet,leg_seconds,notes`, one-way). `--timings` compares them with both speed models, and `--selftest` requires the default model within 2% of each.
- **`data/carriers.csv`**: every carrier's bays — `fighter_bays,fighters,accepts_size,corvette_bays,corvettes`. Wing size is a property of the **bay**, not the craft: `EFFECT_CARRIER` packs `G CC` (the size it accepts, the craft in the wing) and runs 1–8. CV3000 carries 18 fighters across four bays, Marshal Crux 10, ST59 two bays of 2. Because craft die one at a time, a wing is worth **T(n) = n(n+1)/2** rather than n, so a craft in a 4-wing is worth 2.5× the same craft alone — see `data/families.md`.
- **`data/craft.csv`**: the mobile account's **fighters and corvettes** — `name,ship_id,kind,cp,seats,group,hp,armor,ev,flight_speed,dpm_vs_*,role,limit,tp,tp_max,class,notes`. `kind` is FT (fighter) or CO (corvette). These are **carried craft, not fleet hulls**: they have no cargo and `flight_speed` is a flight speed, not a warp stat, which is why the columns deliberately differ from `ships.csv` and why `trade_routes.py` excludes FT and CO from route fleets (`NOT_FLEET_TYPES`). `size_class` is **what size of bay the craft needs, not slots consumed** — every craft takes exactly one slot, and a bay accepts anything at or below its own size (1 small, 2 medium, 3 large), so a size-1 fighter fits everywhere. Corvettes do not use it; they take boat seats (`EFFECT_CARRIER_BOAT`). `class` is the **family**, read off the id (a craft id is family(3) + variant(2), so 126xx is BR050, 211xx M011, 209xx Nebula). `tp` is TP available to that variant as Chris read it in game, `tp_pool` is the family's shared pool (the max over its variants — see below), and `tp_max` is the most the variant's systems can absorb. Rebuild with `python tools/craft_csv.py --names <list> --out data/craft.csv` in `lagrange-combat`.
- **`data/drops.csv`**: the blueprint/TP type drop tables, from Chris's screenshots 2026-10-09 — `general` (the type distribution given that you got a blueprint; **Auxiliary Ship** is `SHIP_TYPE` 7, which the tables call battleship — mobile bases, not combat hulls), `standard` (the "10% to get a BP" box, whose every row is **exactly 0.1000 ×** the general table, with TECH POINTS at 90%), and `generic` (per item, item count random 3+; a *different*, small-hull-skewed mix that drops Fighter and Auxiliary entirely). **TP is grouped by the same types and arrives in the same proportions**, so this is the supply curve for tech points, not just for hulls.
- **`data/families.md`**: the Taurus, Eris and Ruby variant families upgraded side by side. Also the corvettes, and how much the in-game DPM overstates a "full firepower" upgrade (**+60% nominal is +36% effective** — an 18% gap — and prefix 115 is the only permanent upgrade in the tables that carries an accuracy penalty). **Eris Heavy Cannon more than doubles (+134%)** — the only hull of the nine that does — because its two guns share one system and its first 30 TP are a pure cooldown stack whose marginal value *rises* 2.6× along the way. Also records that **`40502` and `48701` are two different hulls both called "Taurus Assault"** in English (8 CP / edef 20 vs 11 CP / armour 30; the cheaper one ends 21% higher).
- **`data/tp.md`** and **`data/tp_curves.csv`**: where to assign tech points. The CSV is 150 hulls with stock DPM, DPM at each quarter of the TP ladder, and the marginal DPM/TP in the first vs last quarter (`concavity`). TP is **typed and you do not choose the type**, so the question is never which hull in the game deserves points — it is "I have 100 cruiser points, which of MY cruisers get them". `tools/tp_assign.py "<hull>"` prints one hull's whole upgrade path in buy order and marks where the worthwhile buys stop; `--type <type> --tp <n> --ships <roster>` splits a type's points across hulls. Both score **sqrt(DPM × seconds survived) / CP** so that armour, evasion and HP compete with weapon levels, or warp with `--for trade`. On this account 100 cruiser points spread across four hulls beat all-in on the best by **+31%**, and Io A spends its first 50 points on defence before any damage — it fights in the front line, and its guns sit on **three separate systems**, so damage has to be bought three times. That last point is a general law: median TP to +50% DPM is 23 / 31 / 36 / 62 for hulls whose guns sit on 1 / 2 / 3 / 4 systems. Io A's full ladder is 104 TP, but the first 88 carry 99% of the gain. The CSV carries the per-hull DPM ladder for 150 hulls; `concavity` shows returns are **not** generally diminishing (median 0.95 — 73 diminish, 54 *increase*), so spreading rests on the good buys running out per hull (90–100 TP) and on the typed supply, not on curvature. Rebuild with `python tools/tp_curve.py <ship ids> --csv data/tp_curves.csv`.
- **`data/upgrades.md`**: what tech points buy. Warp is a **+30% cap** and responds only to
  `EFFECT_SPEED`, not `EFFECT_CURVATURE_SPEED`, which shares the same propulsion slots; 40 hulls
  (Carilion, Reliat, FG300, Trader, Mare\*) are hard-capped at +15%, while every 16-20 CP cruiser
  reaches +30% for **6 TP**. Since fleet speed is the mean, that is +30% credits/hr for 6-12 TP a
  ship against 106-150 TP for a weapon max, so engines come first. Also holds the Quaoar
  railgun-vs-torpedo A/B, the maxed Io / Carilion figures, and the **cost of battle time**: each
  battle minute is ~2% of the hourly rate, so a 30-minute fight costs 38% of the hour. That is why
  a maxed Carilion Special tank fleet loses despite halving incoming damage - it needs 135 minutes
  to kill the 98 CP pirate team, against 2.5 minutes for 5x Io A.
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

### Goods classes and premiums (`--premiums`)

A good's trailing digit is its class: 1 is cheap, 3 is expensive. Comm Comp is class 2 and Int Nav
Sys is class 3; their names are recorded without the digit. Each class has an average price per
cargo unit:

| Class | Average per cargo | Source |
|---|---|---|
| 1 | 0.295 | Reach buys ConsumGood1 at 17,688 (size 2,000), shown in game as +2,898% over average |
| 2 | 10 | the game's figure |
| 3 | about 25–30, varies by good | estimated per good as the median of that day's quotes |

On 2026-10-06, stops **sold** at 0.88–1.01× the average. Every large deviation was a stop
**buying**. So the high prices are the signal, and the margin per cargo unit is roughly
`class average × (buyer's multiple − seller's multiple)`. A big premium on a cheap class earns
little: ArbreCAP pays ×3.15 for Food1, which is 0.66 per cargo unit. Even a ×1.5 class-2 buyer
earns about 5. SpecConGood2 is sold only at ArbreCAP, and 11 stops buy it at ×1.5–4.8, which is
the biggest premium in the game. No class-3 buyer pays more than ×1.16.

`--premiums` lists each good's sellers and buyers as multiples of the class average, then a per-day
trend for each class across every snapshot in `data/market/`. If class-3 goods become the most
profitable as the event goes on, it will show up there: class-3 buyers' premiums rise and class-2
premiums fall. The class-3 averages are estimated from the same day's quotes, so if every class-3
price shifts together the trend won't show it.

## Model and how each assumption was measured

| Assumption | Basis |
|---|---|
| Leg time = `distance × s/Gm`, no fixed overhead | Two timing runs: 7 Gm took 14 s, 1700 Gm took 56:40. Solving those gives 2.000 s/Gm and 0 s overhead. Measured on the first fleet (2 × FG300). |
| **Speed: s/Gm = 10,000 / warp** (`--speed-model timed`, default) | Calibrated on the FG300 run above, then confirmed to the second on ArbreCAP ↔ EpsiCentauri (630 Gm): 15 × FG300 (warp 5,000) took 21:00, 3 × Conomara (warp 2,250) took 46:40 (`data/timings.csv`). `--speed-model warp` (warp = Gm/hr) was the default until 2026-10-06 because it matched the game's $/hr on the first two oracle rows; that was coincidence, as it is 2.8× too fast against every stopwatch run. |
| **Trade speed = 5 × minimum cruise speed, not the warp stat** | Stock hulls all have warp = 5 × cruise_min, so the two only split after an upgrade. On Orgin ↔ DeepSpcArray (156.5 Gm) an IO warp upgrade (3,250 → 3,737) left the leg at 8:00; a standard-drive upgrade (cruise 650 → 845) cut it to 6:09, where 5 × 845 = 4,225 predicts 6:10, and the game's $/hr rose by the same 1.30×. So `ships.csv` records `cruise_min` for upgraded hulls, and the calculator uses it when present. `ships.csv` holds **current** stats; a logged reading taken before an upgrade states the old value in its fleet, e.g. `IO{cruise_min=650}x5`. |
| **A fleet flies at its ships' average speed** (`--fleet-speed mean`, default) | Not its slowest ship's. Fleet speed = floor(mean of each ship's cruise_min) × 5, counted per ship, not weighted by CP. Measured on Beta Lupi ↔ TycoLab (935 Gm): 4 Conomara (warp 2,250) + 2 IO (3,250) took 60:24 in flight. The slowest ship predicts 69:17, the plain mean (2,583) 60:21, and the floored mean (2,580) 60:25. It also explains the game's $/hr for every mixed fleet logged: ArbreCAP's 4 Conomara + 15 AC721 went from 0.62× to 0.999× and Free Port/Ares from 0.90× to 0.999×. So a fast hull speeds up a slow fleet as well as adding cargo. `--fleet-speed slowest` keeps the old assumption. |
| **Profit = listed margin × (1 + route bonus + global bonus)** | The bonuses add. Route bonus: the game's "+N% profit" per level (`bonus_pct` in `routes.csv`). Global bonus (`--global-bonus`): account-wide, source in game not yet identified, and it **changes over time**: 2026-10-06 readings imply +36% to +46%, 2026-10-07 and most of 2026-10-08 +30%, late 2026-10-08 +35% (seen at once on two routes with different goods), then back to +30% (the default) on four routes the same evening, so it moves within a day. `oracle.csv` records it per reading in `global_pct`. Measured from a sale: 126 Std Uniform1 on a +15% route made 3,628 on a listed margin of 2,268, which is ×1.600 rounded down. With it, the model matches the game's own $/hr on every clean `oracle.csv` row to within 0.5% (`--selftest` requires 2%). Rows marked OUTLIER/UNRELIABLE are fleets that may have changed mid-run. |
| Two-stop cycles only | Game rule: trade routes are cyclical between two stops. |
| Goods are bought in **whole units**, into **one pooled fleet hold** | The game's loading log for 10 Reliat T + 10 NOMA on Orgin Station ↔ BountPlanet: 126 Std Uniform1 for 10,080, and 9 RefOre1 (size 4,000, bigger than any ship's hold) for 10,170. Pooled packing predicts exactly 126 and 9; separate holds predict 120 and 0. `--selftest` checks both. `--ships` packs the fleet's total cargo with an unbounded knapsack; `--separate-holds` packs each ship on its own. |
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

**Whole units make hold size a threshold, but it's the *fleet's* total hold.** ResearchData3 is
100,000 cargo per unit. The game pools a fleet's cargo, so 12 × AC721 (302,400) carries 3 units even
though no single AC721 holds one. An earlier version of this table assumed separate holds, which
claimed small haulers couldn't run Proxima at all; that was wrong. Rerun with `--ships` for current
figures (`--separate-holds` reproduces the old assumption).

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

**Speed and combat pull in opposite directions.** A fleet flies at the average of its ships'
cruise speeds, so small fast hulls can lift a slow capital fleet's speed a lot: 20 frigates
would take 5 CV3K from warp 2,000 to about 3,800 in the model, untested. But the battle engine
assigns weapons to target classes and puts ships in rows, with the front rows hit most. Frigates
in a fleet of cruisers and capital ships draw every small-ship weapon and die quickly. **Rule of
thumb (Chris): don't mix FF/DD with CA and capital ships**, unless the small ships form a group
that could survive on its own, with its own screen and padding. The calculator's warning is a
flag, not a ban: ArbreCAP's 15 AC721 (DD) ride in front of 4 Conomara (CA) on purpose. They take the
direct fire and about 2 die per battle (~173K at 86,410 each), under 3% of the route's 6.3M/hr even
with a fight every 58-minute trip. The Conomaras give the best damage per CP, and AC721 DPM is too low
for a fleet of them to defend itself. Mixing is fine when the small ships are cheap to lose and the
big ones can carry the fight; it isn't when losing the screen exposes expensive hulls. So within a combat fleet, get
speed from drive upgrades (minimum cruise) or from faster hulls of the same class. The targeting
model itself (weapon classes, rows, armour) is the other agent's work in this repo
(`data/encounters.csv`, `data/npc_teams.csv`, `data/system_damage.md`).

**Damage type matters as much as DPM (Chris).** Ballistic weapons and most missiles and torpedoes
must get past armour, so each hit is reduced by it. Energy and beam weapons ignore armour.
High-damage hits (railguns, heavy torpedoes such as Quaoar's) lose less to armour. Pirates on the
hard routes have heavily armoured BCs, so energy hulls punch above their DPM there: Taurus (front-row
DD, energy) and Reliat T (one of the few energy-torpedo ships). Rows: Taurus are front row and
actually screen; Quaoar and AC721 are middle row. The calculator's strength figure (fleet DPM x HP vs
the pirate team's) ignores damage type and rows, so treat it as a rough first filter only.
TP upgrades raise a ship's cost and HP as well as its damage, so a variant that holds its class's
TP is not stock (e.g. AC721 Gen).

**Carriers are undercounted here (Chris).** A carrier is the ship *plus* its aircraft (fighters,
bombers or corvettes), and `dpm` in `ships.csv` is the hull alone, so every carrier's real damage is
higher than listed. Both the hull and its aircraft take upgrades, so carriers tend to out-damage
every other type. They are also hard to kill in numbers: ship weapons hit aircraft only about
15-25% of the time, against about 80% for anti-air aircraft. Even the best ship-mounted AA
(WingHussar AA) does far worse than AA aircraft. Fleets of gun ships tend to lose to carrier fleets. Measured on Troy (2026-10-08, `encounters.csv`): 5 CV3000
against a 126 CP pirate fleet dealt 601,362 damage to its 3 Indefatigable BCs, and the carriers' own
guns did 4,385 of it (0.7%). The aircraft did the rest. The fight took 4:17 with no losses.
Aircraft give diminishing returns as you stack more of them, and their quality varies a lot (Chris
rates the AT021 low: pulse weapons but little DPM), so carrier strength doesn't scale with carrier count.
A good shape for a hard route: BCs in front to screen, carriers behind for the damage.

The first run of the top route (Proxima → AlphaCentA, 3 × 130,000 haulers, 84 CP) was attacked
straight away by an 82 CP pirate fleet. The battle took 14.5 minutes, about 30 round trips' worth
of flying, and lost 1 ship; a second attack took the other 2. Every profit/hr figure here counts
travel time only, so treat it as a ceiling.

What's known about alarm levels so far:
- They roughly follow distance from Orgin Station, except Free Port (808 Gm away, Extreme) and the
  AlphaCent/Proxima cluster (Extreme, though some ports further away are only High).
- **They change.** At the 2026-10-07 changeover every Medium port became Low and Free Port went
  from Extreme to High. Now: 14 Low, 8 High, 3 Extreme (AlphaCentA, AlphaCentB, Proxima).
- A route has two ports. Proxima/AlphaCentA (Extreme/Extreme) met 82 CP fleets. Free Port/Ares
  (Extreme/Medium) has met only 60 CP fleets. So pirate strength isn't simply the worse of the two
  ports, but two routes can't say what the rule is.

**When fights happen (2026-10-08, 19 fights on two routes in `encounters.csv`).** Gaps between
fights are a whole number of legs plus one battle, within a few percent, so the chance is per leg.
ArbreCAP ↔ EpsiCentauri (Low/Low, 28.9-minute legs): gaps of 2 or 3 legs, 0.71 fights/hr, never on
back-to-back legs. At its ~36% per leg, 11 gaps without one back-to-back pair would happen under 1% of
the time, so there is probably also a short cooldown after each fight. Free Port ↔ Ares (Low/High,
113.4-minute legs): gaps of 1 or 2 legs, 0.30 fights/hr. Working hypothesis: **alarm sets a % chance
per leg, plus a cooldown.** A faster fleet then meets proportionally more fights per hour, so the
pirate cost stays a fixed share of income and speed still pays. Measured pirate cost: ArbreCAP ~7.5% of
nominal (battle time 5.6%, AC721 losses 2%); Free Port ↔ Ares ~19% (ST59 losses ~16%, 3 in 8 fights at
13.56M each).

The calculator shows both ports' alarms, and `--max-alarm` / `--by-alarm` filter routes so that
**both** ends are at or below a level. Turning alarm levels into attack rate, pirate CP, battle time
and losses needs more rows in `encounters.csv`.

> **Scope: the speed findings here are EVENT-ONLY.** Chris, 2026-10-09: fleet speed is the mean of
> every ship's cruise *in this trading event*, which ends in under a week. **In the normal game a
> fleet travels at its slowest hull**, as physics would have it, and speed does not affect combat at
> all. So everything that follows about cruise upgrades, speed ballast and fleet mean speed is a
> temporary exploit of this event's rules, not general advice. In the normal game a cruise upgrade is
> worth having but cannot be laundered into damage, and adding a fast cheap frigate to a slow fleet
> does nothing.

## Spending a budget: `--roi`

```
py -3 trade_routes.py --roi 87,000,000 --fresh --battle-min 3 --max-alarm High \
                      --ships-file data/ships/count-demonet.csv
```

Picks which route upgrades to buy, best marginal credits/hr per credit first, and says which fleet to
put on each. `--fresh` plans from scratch (an account with no routes opened); without it, it starts
from each route's recorded level. `--fleets N` caps how many routes run at once. `--battle-min M`
charges M minutes of fighting per round trip, `--max-alarm` and `--exclude` drop routes.

**Greedy is exact here, not an approximation.** In every tier the step cost grows faster than the value
it unlocks (easy 1K→50K for 20 CP a step, mid ×3 for 40 CP, hard ×2 for 50 CP), so each route's
marginal ratio strictly decreases and the precedence — you cannot buy level 4 before level 3 — never
binds. The knapsack trap, a cheap high-ratio step hidden behind an expensive low-ratio one, cannot
occur on these ladders.

A route's tier is **inferred, not guessed**: the three ladders give a different `cp_cap` at every level
except 200 CP, which is mid at level 5 and hard at level 4, and those differ in level — so
`(level, cp_cap)` is unique across all fifteen rows of `route_tiers.csv`. A route missing either is
reported, never assumed.

Build limits are account-wide, so each step is re-priced against what is **left** after the earlier
ones; the plan never spends the same hull on two routes.

### What it says, with 87M on a fresh account

Buy order is not close: **every easy route to level 5 first** (82K buys the whole ladder, and the first
step returns ~41M credits/hr per million spent), then mid routes opened at level 1 (240K, ~10M per
million), then up the mid ladder, and **hard tier last and only as far as level 2**. The hard tier is
dominated at every level below 5: hard level 4 is 200 CP and +28% for 135M, while mid level 5 is 200 CP
and +30% for 29.04M. Only hard level 5 sells something mid cannot — the 300 CP cap — at 279M.

### FF as speed ballast: the biggest single lever found so far — and event-only

Fleet speed is the **mean** cruise, so a cheap fast frigate is worth far more than its hold:

| fleet on Ares ↔ Free Port (200 CP, +30%) | cargo | s/Gm | round trip | credits/hr |
|---|---|---|---|---|
| 6× ST59 (168 CP) | 780,000 | 4.44 | 252.0 m | 8,073,168 |
| **6× ST59 + 10× FG300 Recon (198 CP)** | 802,000 | **2.44** | **138.6 m** | **15,093,639** |

Ten 3 CP frigates add 2.7% cargo and **+87% credits/hr**, because the ST59 is the slowest thing in the
game that carries and the FG300 Recon (cruise 1,040) drags the mean up. **This works only because the
event averages fleet speed.** In the normal game the fleet runs at the slowest hull, so the same ten
frigates would buy nothing at all — the ST59 would still set the pace. `--roi` therefore fills every
cap as a **core + ballast** mix rather than one hull type; `--route`'s one-ship-type table is a floor,
not the answer. Best of each class on that route, single-type: BC 8.07M (ST59), CV 6.88M (CV3000), BB
4.75M (FSV830), **DD 4.89M (15× AC721 Logistics, only 120 CP)**, CA 4.46M, FF 0.72M. DD are the best
*core* per CP after BC and leave 80 CP spare; FF are useless as a core and decisive as ballast.

Two things this needs before the numbers are trustworthy: pirate attack rates (so `--battle-min` is
measured rather than assumed) and confirmation that the game has no ship-count cap per fleet — the
plans above run 13 to 16 ships, and 22 has been seen in game.

## Craft names: what the account calls them vs the tables

The client has no official English names for craft, so `ship_variants.csv` carries literal
translations of the Chinese. Fourteen of the account's names needed identifying, and each was settled
against the data rather than spelling (`ALIAS` in `tools/craft_csv.py` records the reason per row).
**All fourteen were then confirmed by Chris against the game's own craft list on 2026-10-09**, so the
mapping is read, not inferred:

| account name | id | how it was identified |
|---|---|---|
| Newland | 11701 | cn 新大地 = new land/earth; `name_en` "New Earth" |
| Strix | 10901 | cn 林鸮 = wood owl; *Strix* is the owl genus |
| Balance Anderson | 11401 | cn 安德森 = Anderson, the only one |
| Vitas A021 / B010 | 11501 / 11601 | cn 维A / 维B; 维 transliterates Vee/Vita |
| **AT021 Interfer** | **12502** | AT021-战术 has no real gun (25 dmg) but `AVOID_PROB_INC` 30 + `PRIORITY_ATTACK` 1 — an unarmed decoy, i.e. interference |
| **HaleBopp MR / Dock** | **21501 / 21502** | the 海尔波普 pair is identical on stats; 21501 has `SHIP_PROB_ACTIVE_ON_CYCLE`, 21502 has `WEAPON_ADD_SKILL_ON_REPAIR` — repair-triggered is the dock |
| **Tempel Intf / Alert** | **21601 / 21602** | the 坦普尔 pair differs only in the skill it grants: 21601 → 9158 `EFFECT_TARGET_PRIORITY_CONFUSION` (interference), 21602 → 9159 `EFFECT_EARLY_WARN_EFFI_ADD` 20 (alert) |
| CV-11003 | 20401 | cn II003, read as 11003; CV = corvette |
| RedBeast | 20701 | cn RB7 = Red Beast 7 |
| Cellular Defender | 20801 | cn 蜂巢 = hive/honeycomb, i.e. cells |
| NebulaChaser Ball / Pulse | 20901 / 20902 | cn 星云A (ballistic) / 星云脉冲 (pulse) |
| Void Elfin | 21001 | cn 虚灵 = void spirit (Wraith) |
| **Silent Assassin** | **20301** | not resolvable from the tables — Chris: "the RAY, 5350 HP", which picks 鳐 (5,350) over 鳐SP (7,700) |

`Silent Assassin` was the one name no field could resolve, and it is **not** 22101 索姆河之影, which
was the closest on flavour and would have been the wrong ship id — a good reason the tool reports
unresolved names rather than guessing them. Chris's "5350 HP" is what separates 鳐 from 鳐SP.

The craft not on the account, for when they turn up: 20302 Ray SP, 20702 RB7SP, 21201 Wildfire (野火),
21701/21702 Wildfire A/B, 22101 Shadow of the Somme (索姆河之影), 22201/22202 Megrez A/B (天玑),
22301/22302 Sky Lance A/B (天枪), and on the fighter side 10701 Sand Dragon, 11201 Follower,
11301 Hale, 12001 Saber, 12401 Mistral, 12503 AT021 Attack, 12701 Reason A101,
12801–12803 Thunderfire V022, 15701/15702 Merak Fighter A/B.

## How to read `tp` and `tp_pool`

Settled by Chris, 2026-10-09. **The pool is per family and `ships.csv` was right all along** — the
number read in game is the TP available to *that variant*, and a shared pool can be **directed** at
one of them:

- *"I put all 44 in the Pulse leaving 0 for the Ballistic"* → NebulaChaser reads **0 / 44** on a single
  pool of 44, directed entirely at the Pulse. The Ballistic's 0 means *nothing is left for it*, not
  that anything has been consumed.
- *"the variants that all share the same TP … indicates I have not assigned any TP"* → M011 reads
  **6 / 6 / 6** on one undirected pool of 6.

So a family's pool is the **max** over its variants under either case — `max(0, 44) = 44`,
`max(6, 6, 6) = 6` — and never the sum, which would have read M011 as 18 and inflated the account's
whole TP budget by about 3×. `tp_pool` carries that figure on every row of the family; `class` is the
family, the first three digits of the ship id.

The pair to watch for is a *directed* one: a row with `tp` 0 but `tp_pool` 44 is not an un-upgraded
craft, it is the sibling of one that holds the family's whole pool.

Against capacity (`tp_max`, the most a variant's systems can absorb) the account's craft are early:
NebulaChaser 39%, CVT800 33%, RedBeast 33%, Cellular Defender 32%, Void Elfin 29%, BR050 11%,
M011 5%. Nine of the thirty rows have no pool at all.

## Not modelled yet

- **TP assignment in credits.** `tp_assign.py` scores combat in BV/CP and trade in warp %, side by
  side. Both should be priced in credits per hour, which `--roi` and the battle-time cost in
  `data/upgrades.md` now make possible.
- **Craft skills and utility hulls.** `tp_assign.py` now prices fighters and corvettes, but it scores
  weapons and survivability only. HaleBopp MR/Dock read ~4 BV/CP because they carry no gun at all, and
  Tempel Intf and Alert tie exactly because the only thing separating them is the skill they grant.
  Rating those needs the carrier/repair and skill models, which do not exist.
- **Electronic-warfare and support hulls.** The Balance Anderson interferes with enemy accuracy,
  others raise your own, and nothing here scores either. They pick targets randomly and may not earn
  their CP at all (Chris) — settling it needs the targeting model extended to accuracy effects.
- **Stranding risk.** Blueprints arrive randomly and resets are expensive, so TP in a hull you later
  stop fielding is a loss. Pricing that needs a blueprint arrival rate and the reset cost; neither is
  recorded. Nor is *which* basic hulls carry unremovable TP, and that is a hard constraint.

- **Pirate attacks:** how often, how strong, how long a battle takes, and what is lost (see above).
- **Fleet selection.** Fleets are capped at 100 CP, so the goal is to maximise cargo/CP × speed,
  plus enough combat strength to handle pirates. Use `--json` output alongside a ship-data tool.
- Price changes as you trade, and supply limits.
- Routes with more than two stops (not allowed by the game).
