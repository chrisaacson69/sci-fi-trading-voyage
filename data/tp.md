# "I got XX tech points. Where do I put them?"

## The question

**TP is typed, and you do not choose the type** (Chris, 2026-10-09). Points arrive as cruiser points,
frigate points, destroyer points, and so on, in the proportions the blueprint drop table gives — see
`data/drops.csv`. So there is no decision to make about *which* type to invest in; the only decision
is, given 100 cruiser points, which of **your** cruisers they go into and in what order.

`lagrange-combat/tools/tp_assign.py` answers exactly that:

```
python tools/tp_assign.py cruiser 100 --ships <roster.csv>
python tools/tp_assign.py frigate 60 --for trade --fleet 14 --ships <roster.csv>
```

## How value is scored

The damage buys run out first, and what you are left choosing among is survivability, speed and
strategies — so a score that only counts DPM cannot answer the question at all. Combat value is

> **sqrt( outgoing DPM × seconds survived ) / CP**

- **outgoing DPM** against the Thunderbolt (60601), a real battlecruiser at armour exactly 120 — the
  band the 98 CP pirate team sits in — carrying 8% missile/torpedo interception, so projectile hulls
  are judged against something that shoots them down.
- **seconds survived** = HP ÷ the DPM pirate team 1010801 actually lands on this hull. That is what
  makes armour, evasion (per attacking weapon type) and energy resistance compete on equal terms with
  a weapon level.
- **÷ CP**, because a fleet is capped in CP and never in hull count.

`--for trade` scores warp instead: fleet speed is the **mean** cruise, so a cruise level is worth its
share of the fleet's credits per hour (`data/upgrades.md`).

Points are bought one **level** at a time — the ladder is 2 TP a level, five levels an enhancement —
always taking the level with the best value per TP.

## What it says for this account

### 100 cruiser points

| hull | CP | stock BV/CP | at 100 TP | gain | per TP | gains stop at |
|---|---|---|---|---|---|---|
| **Io A** | 18 | 81.7 | 138.1 | +69% | 0.575 | **98 TP** |
| Conamara Chaos Plasma | 20 | 76.5 | 128.4 | +68% | 0.524 | 99 TP |
| Conamara Chaos Railgun | 16 | 60.3 | 108.7 | +80% | 0.484 | — |
| Io Siege | 18 | 74.5 | 122.0 | +64% | 0.528 | **90 TP** |
| Io B | 18 | 81.3 | 127.7 | +57% | 0.473 | 98 TP |
| Chimera A | 18 | 56.9 | 102.2 | +80% | 0.459 | 99 TP |

**Spreading wins by +31%.** Best marginal value per TP, across the whole type: Io A 34 TP, Callisto
Drone 24, Io Siege 22, Io B 16, then scraps — **+73.7 BV/CP against +56.4** for putting all 100 into
the single best hull. That is Chris's playthrough rule, measured, and the "gains stop at" column is
the mechanism he described: the good buys genuinely run out, at 90–100 TP a hull.

### The buy order is not what you would guess

Io A spends its first 50 points on **defence**, not weapons:

| TP | buys |
|---|---|
| 1–11 | evasion, then evasion vs weapon type |
| 18–26 | hit rate vs type |
| 27–35 | HP |
| 37–42 | armour +30 |
| 50+ | damage |

Because the Io already has the biggest guns in its class, another 2% of damage is worth less than not
dying — which only shows up once survival is in the score.

### 60 frigate points, for trade

Cruise **runs out at 12 TP a hull** — that is the +30% `EFFECT_SPEED` ceiling from `data/upgrades.md`,
and the tool rediscovers it from the ladder. So 60 frigate points buys cruise on **five** frigates and
spreading is not a preference, it is forced. (For combat instead, Reliat Stealth is the standout at
0.775 BV/CP per TP, nearly double the next frigate.)

## The measured background

`tools/tp_curve.py` and `data/tp_curves.csv` carry the per-hull DPM ladder for 150 hulls: stock DPM,
DPM at each quarter of the ladder, and `concavity` = marginal DPM/TP in the last quarter over the
first.

**Returns are not generally diminishing**: median concavity 0.95, with 73 hulls diminishing, 23 flat
and **54 increasing** (ST59 ×1.20, Carilion Heavy Cannon ×1.40). Curve shape is a property of the
hull, not a law. What spreading really rests on is the two things above — the good buys run out per
hull, and the supply is typed — plus stranding risk, below.

## Constraints this has to respect (told, not derived)

1. **Blueprints arrive randomly**, so TP committed to the best design you have now is stranded when a
   better one turns up.
2. **Resets exist but are expensive** — not a routine move.
3. **Some TP cannot be removed at all.** Rare, and only on the **basic hulls**; that TP survives a
   reset, so assignment there is irreversible.
4. **A family's pool is shared and can be directed at one variant** — see the README on `tp` vs
   `tp_pool`.
5. **A full playthrough fields 10+ hulls**, plus up to 125 aircraft across ~12 types. Maxing one or
   two hulls at the expense of the rest is not a stable distribution even where it scores well.

## Still open

- **Fighter and corvette TP cannot be priced at all.** They are 25% of the supply (10% + 15%), and
  neither has a `playable_weapons` entry, so `tp_assign.py` has no mounts to work from. `craft.csv`
  and `craft_matrix.csv` have the stats; the gap is a craft-shaped `hull()`.
- **Battleship is not in the drop table.** FSV830 is `SHIP_TYPE` 7 and one of the best haulers on the
  account, so where its points come from is unknown — folded into battlecruiser or carrier, or simply
  not shown.
- **Stranding risk is not priced.** It needs a blueprint arrival rate and the reset cost, neither
  recorded, and a list of which basic hulls carry unremovable TP — a hard constraint.
- **Combat and trade value are still separate scores.** `--roi` prices routes in credits per hour; a
  cruise level and an armour level should ultimately compete in that same currency, not in BV/CP and
  warp % side by side.
