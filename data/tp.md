# Where to assign tech points

## The constraints (Chris, 2026-10-09 — told, not derived)

These are the rules the assignment problem has to respect. None of them are in the client tables.

1. **Blueprints arrive randomly.** You spend TP on the best design you have *now*, and a better hull
   can turn up afterwards with nothing in it. TP already committed is stranded.
2. **Resets exist but are expensive.** A reset strips a design's TP and lets you reallocate; the cost
   is high enough that it is not a routine move.
3. **Some TP cannot be removed at all.** A rare mechanic, and only on the **basic hulls**: that TP is
   bound to the hull and survives a reset. Assignment there is irreversible.
4. **A family's pool is shared and can be directed at one variant.** See the README on `tp` vs
   `tp_pool` — NebulaChaser reads 0 / 44 on one pool of 44, all of it committed to the Pulse.
5. **Chris's working rule** is to spread TP across every design he actually fields in a playthrough,
   rather than maxing one, on the grounds that TP has diminishing returns.

## What is measured: the returns are NOT generally diminishing

`lagrange-combat/tools/tp_curve.py` buys TP one **level** at a time — the ladder is 2 TP a level, five
levels an enhancement — always taking the level that adds the most effective DPM per TP, and records
the curve. DPM is measured, not scored: `per_shot` against a real reference target, the **Thunderbolt
(60601)**, a battlecruiser whose armour is exactly 120 (the band the 98 CP pirate team sits in) and
which carries 8% missile/torpedo interception, so projectile hulls are judged against something that
actually shoots them down. Results for 150 hulls are in `data/tp_curves.csv`.

Comparing marginal DPM per TP in the **last** quarter of a hull's ladder against the **first**:

| shape | hulls |
|---|---|
| diminishing (< 0.90) | 73 |
| flat (0.90 – 1.10) | 23 |
| **increasing (> 1.10)** | **54** |

Median 0.95 — essentially flat, with the quartiles at 0.52 and 1.31. So the curve shape is a property
of the individual hull, not a law. Examples:

| hull | CP | TP | stock | 25% | 50% | 75% | 100% | first → last DPM/TP |
|---|---|---|---|---|---|---|---|---|
| Io A | 18 | 56 | 17,761 | 21,144 | 23,921 | 27,084 | 29,234 | 242 → 154 (×0.64) |
| Quaoar Torpedo | 6 | 70 | 2,029 | 3,508 | 4,405 | 5,403 | 6,511 | 85 → 63 (×0.75) |
| Quaoar Railgun | 6 | 50 | 1,991 | 2,953 | 4,381 | 5,974 | 6,870 | 77 → 72 (×0.93) |
| Taurus Pulse | 11 | 36 | 3,540 | 4,012 | 4,686 | 5,122 | 5,610 | 52 → 54 (×1.03) |
| **ST59** | 28 | 72 | 8,559 | 10,360 | 11,686 | 13,300 | 15,452 | 100 → **120 (×1.20)** |
| **Carilion Heavy Cannon** | 5 | 40 | 1,165 | 1,362 | 1,619 | 1,937 | 2,212 | 20 → **28 (×1.40)** |

**So the diminishing-returns premise does not survive measurement**, and spreading TP needs a different
justification — which it has, two of them, below. (Note the `maxTP` column is the TP that buys *DPM*,
40–100 on most hulls. The total a hull can absorb is 106–150; the rest goes to HP, armour, evasion and
cruise, which this curve does not score. A hull's TP does not "run out" at 56 — only its DPM TP does.)

## What actually varies: DPM per TP between hulls, by 100×

| hull | CP | TP | stock → maxed | DPM/TP | DPM/TP/CP |
|---|---|---|---|---|---|
| Constantine the Great | 35 | 97 | 21,673 → 41,619 | 205.6 | 5.88 |
| **Io A** | 18 | 56 | 17,761 → 29,234 | 204.9 | **11.38** |
| Chimera B | 20 | 50 | 8,637 → 18,185 | 191.0 | 9.55 |
| Conamara Chaos Plasma | 20 | 73 | 17,879 → 31,021 | 180.0 | 9.00 |
| Callisto Heavy | 20 | 76 | 14,886 → 28,096 | 173.8 | 8.69 |
| Io Siege | 18 | 52 | 14,778 → 22,868 | 155.6 | 8.64 |
| … | | | | | |
| Tundra Tactical | 9 | 20 | 249 → 334 | 5.4 | 0.60 |

**Io A is the best TP buy in the game per CP** and Constantine the best in absolute terms. The spread
from best to worst is about 38× on DPM/TP and 19× on DPM/TP/CP — an order of magnitude more than any
within-hull curvature. **Which hull you spend on dominates how much you spend on it.**

## The two real arguments for spreading

Spreading is still right, but not because of diminishing returns:

1. **Each hull's DPM-buying TP caps out well short of a real budget.** 120 TP shared across
   Q-Torpedo / Io A / ST59 / Taurus Pulse / Carilion HC, best-marginal-first, lands on ST59 59 TP
   (49%), Io A 50 (42%), Q-Torpedo 10 (8%), and **nothing** on Taurus Pulse or Carilion HC — total
   56,776 DPM, against 50,427 for putting all 120 into Io A. **Spreading wins by +12.6%, purely
   because Io A cannot absorb 120 TP of DPM.** That is a capacity argument, not a curvature one, and
   it says concentrate on two or three hulls to their caps — not spread evenly.
2. **Stranding risk under random blueprint arrival.** This is the argument the DPM model cannot
   price, and it is the stronger one. With resets expensive and some basic-hull TP unremovable, TP in
   a hull you later stop fielding is a loss, so the right objective is not maximum DPM today but
   something closer to minimum regret across the blueprints you might draw. Nothing here measures
   that yet.

## The task, as it stands

Open: **given a fleet plan and a TP budget, where should the TP go?** What is needed to answer it
properly, in order:

- **Score the fleet, not the hull.** `--roi` already picks fleets per route, and `data/upgrades.md`
  established that fleet speed is the mean and that each battle minute costs ~2% of the hourly rate.
  So a cruise level on a ballast frigate and a damage level on the core compete *in credits per hour*,
  which is the only common currency — DPM/TP is a proxy that cannot see either.
- **Price the defensive TP this curve ignores.** HP, armour, evasion and energy resistance are 50–100
  TP a hull and currently score zero. Survival is worth credits too (lost hulls, and `data/upgrades.md`
  section 6 for what the Carilion's evasion systems actually buy).
- **Price the stranding risk.** Needs a blueprint arrival rate and the reset cost — neither recorded.
  Which basic hulls carry unremovable TP is also not recorded, and that is a hard constraint, so it
  should go in `data/ships.csv` notes as it is discovered.

What is already usable today: if the question is narrowly "which hull converts TP into damage best",
the answer is **Io A first, then Constantine, Chimera B and Conamara Plasma**, to roughly 50–75 TP
each, and **the Carilion and the Taurus should get none of it** on damage grounds.
