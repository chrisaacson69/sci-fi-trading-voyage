# Variant families: Taurus, Eris, Ruby

What changes as you upgrade each variant, from `lagrange-combat/tools/tp_assign.py`. Value is
**sqrt(DPM vs a battlecruiser at armour 120 × seconds alive vs the 98 CP pirate team) / CP**, so a
weapon level and an armour level compete directly; see `data/tp.md` for the method. These are combat
figures only — nothing here depends on the event's speed rules.

## The headline: Eris Heavy Cannon is the best upgrade target in all three families

| family | variant | CP | HP | armour | ev | edef | stock | maxed | TP | gain | TP split |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Eris | **Heavy Cannon** | 9 | 30,540 | 20 | 25 | 2 | 38.5 | **90.0** | 100 | **+134%** | damage 60 / tank 40 |
| Eris | Cannon | 7 | 30,540 | 20 | 25 | 2 | 24.9 | 37.6 | 60 | +51% | tank 67 / damage 33 |
| Eris | Armor | 7 | 35,140 | 30 | 25 | 5 | 27.4 | 40.0 | 68 | +46% | tank 56 / damage 44 |
| Taurus | **Assault (48701)** | 8 | 36,040 | 20 | 0 | **20** | 58.0 | **84.2** | 76 | +45% | tank 53 / damage 47 |
| Taurus | Defense | 8 | 40,030 | 30 | 0 | 4 | 57.6 | 76.6 | 57 | +33% | damage 51 / tank 49 |
| Taurus | Assault (40502) | 11 | 40,030 | 30 | 0 | 4 | 46.1 | 69.6 | 78 | +51% | damage 64 / tank 36 |
| Taurus | Pulse | 11 | 36,040 | 20 | 0 | 2 | 42.6 | 65.5 | 76 | +54% | tank 53 / damage 47 |
| Ruby | Railgun | 5 | 16,520 | 5 | 0 | 0 | 40.6 | 59.7 | 88 | +47% | damage 68 / tank 32 |
| Ruby | Ion Cannon | 8 | 14,970 | 5 | 0 | 0 | 33.9 | 44.3 | 71 | +31% | damage 61 / tank 39 |
| Ruby | Defense | 5 | 17,550 | **40** | 0 | 0 | 24.5 | 33.1 | 76 | +35% | tank 66 / damage 34 |

**Eris Heavy Cannon more than doubles** — the only hull in these three families that does — and the
reason is its opening thirty points.

## Eris: the Heavy Cannon's cooldown stack is the whole story

Its two guns sit on **one system**, so a cooldown cut lifts both, and the system carries three
cooldown rows including prefix 115 "full firepower" (−40% CD, −15% hit). The first 30 TP buy nothing
else, and the marginal rate **rises** the whole way:

| TP | buys | value per TP |
|---|---|---|
| 10 | cooldown −40%, hit −15% | 0.619 |
| 12–20 | cooldown −15% | 0.536 → 0.763 |
| 22–30 | cooldown −15% | 0.845 → **1.383** |
| 31–42 | evasion (two rows, ×8) | 0.56 → 0.77 |
| 44+ | damage, 2%/level | 0.55 and falling |

Each cut multiplies with the ones before it, so the last cooldown level is worth **2.6× the first** —
textbook increasing returns, and the opposite of the diminishing curve you would assume. Stop reading
the ladder as "spend evenly": **on this hull the first 30 points are the investment and everything
after is maintenance.**

The plain **Eris Cannon** cannot do this — it has only one mount, so it spends 67% of its TP on tank
and gains half as much. **Eris Armor** is the tankiest (35,140 HP, armour 30, edef 5) but ends up
level with the Cannon. The Heavy Cannon costs 2 CP more than either and is worth roughly **2.4× the
Cannon maxed**.

## Taurus: two different hulls share one English name

`40502` and `48701` both read **"Taurus Assault"** in English — 斗牛-突击 and 斗牛攻坚 in the tables —
and they are not the same ship:

| | CP | HP | armour | edef | maxed BV/CP |
|---|---|---|---|---|---|
| Taurus Assault **48701** (斗牛攻坚) | **8** | 36,040 | 20 | **20** | **84.2** |
| Taurus Assault **40502** (斗牛-突击) | 11 | 40,030 | 30 | 4 | 69.6 |

**48701 is 3 CP cheaper and ends 21% higher.** Its edge is `edef 20` against everyone else's 2–4 —
energy resistance is the only defence against plasma and ion, which armour does not touch — and its
path spends its first 12 points on evasion before anything else. If a roster says "Taurus Assault",
check which one it means; that is worth settling in game before any TP goes in.

**Taurus Defense** is the efficient one at 8 CP: 57.6 stock, 76.6 maxed for only **57 TP**, the
shortest ladder of the family, and 98% of its gain lands in the first 50. **Taurus Pulse** is the
weakest of the four on every measure and should not be the family's TP sink.

## Ruby: a 5 CP frigate that upgrades like a warship

**Ruby Railgun** is the pick — 5 CP, and the only Ruby whose opening move is damage (a −15% cooldown
stack, five levels for 10 TP, before anything else). It takes 88 TP, long for a frigate, and returns
+47%.

**Ruby Ion Cannon** costs 8 CP for *less* HP (14,970 against 16,520) and ends 26% lower. Its ion gun
ignores armour, which the reference target at armour 120 should reward — and it still loses, because
3 extra CP is a lot on a frigate. **Ruby Defense** has armour **40**, by far the best in the family
and eight times the other two, but almost no offence: it ends lowest of the three despite spending
66% of its TP on tank. It is a body, not a gun.

## What this says in general

- **Count the systems before the guns.** The Eris Heavy Cannon and the Taurus family all carry their
  mounts on **one** system, which is why cooldown stacking pays so well; the Ruby variants are split
  over two. Median TP to +50% DPM is 23 / 31 / 36 / 62 for 1 / 2 / 3 / 4 weapon systems (`data/tp.md`).
- **Cheaper variants often win on BV/CP**, because the denominator is CP: Taurus Defense and the
  8 CP Assault both beat the 11 CP variants, and Ruby Railgun beats the 8 CP Ion Cannon.
- **A variant's stock profile predicts its path.** Hulls that already hit hard buy defence first
  (Io A, Taurus Pulse); hulls with one system and a cooldown row buy cooldown first and keep buying
  it (Eris Heavy Cannon, Ruby Railgun).

## Accuracy: how much the in-game DPM overstates a "full firepower" upgrade

Chris: *"some hulls have these upgrades that either add an extra shot, or massively increase damage at
the expense of accuracy. The in-game DPM shows huge gains, but without taking into account accuracy
these are misleading. OTOH they tend to still be a good upgrade."*

Both halves are right, and the size of the gap is 18%:

| hull | prefix 115, 10 TP | stock | **nominal** (penalty ignored) | **effective** | display overstates by |
|---|---|---|---|---|---|
| Eris Heavy Cannon | −40% CD, −15% hit | 1,677 | 2,659 (+59%) | 2,260 (+35%) | **18%** |
| Quaoar Railgun | −40% CD, −15% hit | 1,991 | 3,262 (+64%) | 2,773 (+39%) | **18%** |

So a +60% headline is really +36% — and it is *still* the best 10 TP on the hull, which is why
`tp_assign.py` buys it first on the Eris Heavy Cannon. The model nets the penalty because
`system_mods` handles `EFFECT_HIT_RATE_DEC`; ignoring it banked the cooldown and threw away the
downside, which Chris caught earlier.

Worth knowing how contained this is: **prefix 115 is the only permanent upgrade in the tables that
carries an accuracy penalty.** 8004 and 8006 are seasonal adjustments (excluded as unknowable), and
every other one — 9038, 9044, 9189–9199, 9348, 9360, 9403–9405, 9521, 9525, 9779–9798 — is a `9xxx`
timed strategy, not a permanent buff. So the "misleading DPM" problem has exactly one instance in the
upgrade trees, and it is handled.

## The mobile account's corvettes

Craft were unpriceable until now because `matrix.craft_mounts` never set `system_group`, which is what
`apply_upgrades` matches a mount to its system by — so **every weapon upgrade on a fighter or corvette
was silently skipped** and their ladders read as 100% tank. Fixed; a craft slot id `0101` sits on
system `<id>01` exactly as a ship's does.

| corvette | id | HP | armour | ev | stock | maxed | TP | gain | pool | TP split |
|---|---|---|---|---|---|---|---|---|---|---|
| **Cellular Defender** (Hive) | 20801 | 6,650 | 2 | 0 | 182.3 | **311.5** | 79 | +71% | 36 | damage 68 / tank 32 |
| NebulaChaser Pulse | 20902 | 5,400 | 2 | 0 | 176.2 | 280.9 | 77 | +59% | **44** | tank 65 / damage 35 |
| CVT800 | 21301 | 7,500 | 2 | 0 | 179.9 | 261.3 | 78 | +45% | 37 | damage 62 / tank 38 |
| SLevi9 | 21401 | 6,000 | 2 | 0 | 157.0 | 248.1 | **118** | +58% | **0** | damage 61 / tank 39 |
| **RedBeast** (RB7) | 20701 | 5,200 | 2 | 0 | 110.2 | 204.6 | 106 | **+86%** | 35 | damage 62 / tank 38 |
| Void Elfin | 21001 | 5,200 | 2 | 35 | 78.7 | 129.4 | 76 | +64% | 34 | tank 59 / damage 41 |
| NebulaChaser Ball | 20901 | 6,300 | 2 | 0 | 63.9 | 94.0 | 63 | +47% | 44 | tank 65 / damage 35 |
| CVM011 Miss | 21101 | 7,500 | 2 | 0 | 68.9 | 89.8 | 51 | +30% | 6 | damage 51 / tank 49 |
| CVM011 Can | 21102 | 7,500 | 2 | 0 | 71.1 | 87.3 | 40 | +23% | 6 | tank 75 / damage 25 |
| CV-11003 | 20401 | 4,900 | 2 | 0 | 49.9 | 71.4 | 66 | +43% | 19 | tank 70 / damage 30 |
| Silent Assassin (Ray) | 20301 | 5,350 | 6 | 0 | 51.0 | 71.2 | 66 | +40% | 10 | tank 70 / damage 30 |
| Tempel Intf / Alert | 21601/2 | 7,100 | 2 | 0 | 42.4 | 65.8 | 76 | +55% | 0 | tank 84 / damage 16 |
| CVM011 HS | 21103 | 7,500 | 2 | 5 | 45.0 | 58.2 | 62 | +30% | 6 | damage 52 / tank 48 |
| HaleBopp MR / Dock | 21501/2 | 7,000 | 0 | 0 | 3.8 | 4.8 | 46 | +24% | 0 | tank 100 |

Reading it against what the account has actually done:

- **NebulaChaser Pulse is the right call.** The family's whole 44-point pool is directed at it and it
  needs 77 — so it is the one corvette already pointed at a hull that deserves it. The Ballistic
  sibling ends at 94 against the Pulse's 281; directing the pool was correct.
- **SLevi9 has the longest ladder of any corvette, 118 TP, and a pool of 0.** It is also the only one
  whose stock value is near the top (157) with nothing invested. Biggest untouched opportunity.
- **Cellular Defender is the best corvette in the account** and has 36 of the 79 it wants.
- **RedBeast gains the most in relative terms (+86%)** but wants 106 TP against a pool of 35.
- **Void Elfin has 34 points in it and ends at 129**, below five corvettes that have less invested.
  Worth a second look before more goes in.
- **HaleBopp MR and Dock score ~4** because they carry no weapon at all. Correct, not a modelling
  failure — they are utility hulls (cycle ability, repair-triggered skill) and combat TP there is
  wasted. Rating what they *do* needs the carrier/repair model, which does not exist yet.
- **Tempel Intf and Alert are identical at 42.4 → 65.8**, because the only thing separating them is
  the skill they grant (9158 targeting confusion vs 9159 early warning) and nothing here scores
  skills. The model cannot tell them apart; do not read the tie as "they are the same hull".
