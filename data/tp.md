# "I got XX tech points. Where do I put them?"

## The question

**TP is typed, and you do not choose the type** (Chris, 2026-10-09). Points arrive as cruiser points,
frigate points, destroyer points, and so on, in the proportions the blueprint drop table gives — see
`data/drops.csv`. So there is no decision to make about *which* type to invest in; the only decision
is, given 100 cruiser points, which of **your** cruisers they go into and in what order.

And it starts with **one hull**: what order do its upgrades go in, and where do the worthwhile ones
stop. Splitting a type's points across hulls is the second question, not the first.

```
python tools/tp_assign.py "Io A"                  # the whole ladder, in buy order
python tools/tp_assign.py 50301 --tp 40           # only what 40 points buy
python tools/tp_assign.py "Io A" --for trade
python tools/tp_assign.py --type cruiser --tp 100 --ships <roster.csv>   # across a type
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

**Which enemy you score against changes the answer more than anything else.** The other agent's
point, which Chris relayed: *"we tend to only hit BC at the larger fleet sizes"*. So `--vs small`
scores against pirate team 1010501 (30 CP: 4× Rager Torpedo, a frigate, plus a Frost Missile) and
`--vs large` against 1010801 (98 CP: an Indomitable battlecruiser, two KCCPV2.0 and two 066 cruisers,
four Stingrays). Each supplies both the thing you shoot at and the thing shooting back. Scoring a
small-fleet escort against a 120-armour battlecruiser is simply the wrong question, and it reversed
two of the recommendations in `data/families.md`.

`--for trade` scores warp instead: fleet speed is the **mean** cruise, so a cruise level is worth its
share of the fleet's credits per hour (`data/upgrades.md`). **`--for trade` is event-only** — in the
normal game a fleet travels at its slowest hull and speed does not affect combat, so a cruise level
there is worth having but cannot be bought as a force multiplier (Chris, 2026-10-09).

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
| 50+ | damage, then cooldown |

Two reasons, and Chris named both:

1. **The Io lives in the front line, so lasting longer is doing its job longer.** Another 2% of damage
   on a hull that already has the biggest guns in its class is worth less than not dying — which only
   shows up once survival is in the score.
2. **Its guns are spread over three systems, so damage has to be bought three times.** An enhancement
   belongs to one system, and the Io A carries three mounts on three separate system groups
   (5030101, group 2, group 3). The Quaoar Torpedo has both its guns on one system, so a single
   cooldown stack lifts both.

That second one is a general law, not an Io quirk. Median TP to **+50% DPM**, by how many system
groups carry the hull's guns:

| weapon systems | hulls | median TP |
|---|---|---|
| 1 | 26 | 23 |
| 2 | 44 | 31 |
| 3 | 9 | 36 |
| 4 | 1 (Spear of Uranus) | 62 |

So "how expensive is damage on this hull" is largely answered before you look at the weapons at all —
by how many systems they sit on. `tp_assign.py` prints the count in the header for that reason.

### And the tail is nearly worthless

Io A's full ladder is 104 TP for +69% BV/CP, but **the first 88 carry 99% of the gain**. The last 16
points buy 1%. That is the "good buys run out" effect in one line, and the tool marks the knee.

### 60 frigate points, for trade (event-only)

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

## What the types are

`SHIP_TYPE` 7 — which the client tables call *battleship*, and which holds FSV830, Ganymede and
Ediacaran — is the drop table's **Auxiliary Ship** (3%). Chris, 2026-10-09: in the English game these
are not combat hulls at all but **mobile bases**, used to build small ships and aircraft as
replacements. Expensive to make useful and expensive to run, and rarely worth it in play. So the drop
table covers all eight types after all, and nothing is missing.

## Constraints this has to respect (told, not derived)

1. **Blueprints arrive randomly**, so TP committed to the best design you have now is stranded when a
   better one turns up.
2. **Resets exist but are expensive** — not a routine move.
3. **Some TP cannot be removed at all.** It survives a reset, so assignment there is irreversible.
   The blueprints Chris has identified as carrying fixed TP, 2026-10-09: **FG300, AC721, CAS066
   (066), KCCP, ST59, CV3K, CVM (the M011 corvettes), 11003 (II003)**. SC002 was assumed to be one
   and turns out not to be — a reset on it would free 25 of its 38 points. This list is read off the
   game, not derived, and is the hard constraint on any reallocation plan.
4. **A reset is not actually available.** Chris, 2026-10-09: he has none, and buying one is too
   expensive to justify for a side event. So every recommendation here is about where the NEXT points
   go, not about moving the ones already committed.
5. **A family's pool is shared and can be directed at one variant** — see the README on `tp` vs
   `tp_pool`.
6. **A full playthrough fields 10+ hulls**, plus up to 125 aircraft across ~12 types. Maxing one or
   two hulls at the expense of the rest is not a stable distribution even where it scores well.

## Still open

- **Fighter and corvette TP cannot be priced at all.** They are 25% of the supply (10% + 15%), and
  neither has a `playable_weapons` entry, so `tp_assign.py` has no mounts to work from. `craft.csv`
  and `craft_matrix.csv` have the stats; the gap is a craft-shaped `hull()`.
- **Are the electronic-warfare and support hulls worth their CP at all?** The Balance Anderson is
  meant to interfere with opposing ships' accuracy, and others raise your own. Chris, 2026-10-09:
  they pick targets randomly, and even where that randomness can be narrowed it is not clear they
  earn their cost — "right now, these seem like they are not worth it". Settling it needs the
  targeting model extended to the accuracy effects and a measured engagement, which is real work.
  Until then nothing in these tools scores them, and they should not be assumed to be worth a slot.
- **Stranding risk is not priced.** It needs a blueprint arrival rate and the reset cost, neither
  recorded, and a list of which basic hulls carry unremovable TP — a hard constraint.
- **Combat and trade value are still separate scores.** `--roi` prices routes in credits per hour; a
  cruise level and an armour level should ultimately compete in that same currency, not in BV/CP and
  warp % side by side.
