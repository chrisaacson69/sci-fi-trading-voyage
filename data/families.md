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

## The mobile account's fighters

**Every craft takes exactly one slot** (Chris, 2026-10-09). The 1/2/3 on a craft is a **size class** —
small / medium / large — and a bay accepts anything **at or below** its own size, so a size-1 SC002
fits everywhere and a size-3 Stingray needs a large bay. It is a compatibility rule, not a cost.

The bay declares both, packed `G CC` in `EFFECT_CARRIER`: leading digit the size it accepts, last two
the **number of craft in the wing**. Wings run 1–8.

**But a carrier's bay modules are mutually exclusive.** They sit in systems, systems are grouped by
`GROUP`, and exactly one system is fielded per group — the same rule `maxout.build` documents for
enhancements. Summing them counts alternatives that can never be fitted together. The CV3000 reads
18 fighters that way; in fact group 101 is a **choice** of 5 fighters + 3 corvettes (the stock fit),
5 fighters alone, or 8 fighters, and group 201 a choice of 3 corvettes or three non-hangar modules:

| CV3000, 40 CP | fighters | corvettes |
|---|---|---|
| **stock** | 5 | 3 |
| best, every module unlocked | 8 | 3 |

And the alternatives are **not free** — a module has to be obtained, so the "best" column is a
ceiling, not a loadout. `data/carriers.csv` now gives both columns and lists every group's options.
(The stock CV3000 at 5 fighters + 3 corvettes is exactly what Chris described it as months before this
was read out of the tables.)

The figures below are **per craft**, which is what the blueprint detail screen shows; the overall
screens show wing totals.

### Where the account's fighter TP should go

Scored **per craft** against the pirate team, then multiplied by the wing it will actually fly in.
Compatibility does bind, but on the bay side: the account's cheapest wing platform, the **Predator
Carrier at 4 fighters for 18 CP**, is a size≤2 bay, so the best fighters cannot fly from it.

Fighter bays the account has, stock fits:

| accepts | bays |
|---|---|
| size ≤ 2 | **Predator Carrier 4F (18 CP, ×2.5)**, Eternal Heavens 3F (40 CP, ×2.0), Tundra 2F (9 CP), Ceres 2F (8 CP) |
| size ≤ 3 | **CV3000 5F (40 CP, ×3.0)**, KCCPV2.0 Carrier 2F (16 CP) |
| size ≤ 3, needs unlocking | **CV3000 8F (×4.5)**, Solar Whale 8F (×4.5), Solar Whale 5F, Eternal Heavens 4F, Ediacaran 2F |

**Size 3 — only the CV3000, Solar Whale, KCCPV2.0 or Ediacaran can carry these.** In a CV3000 5-wing:

| fighter | stock | maxed | full TP | pool | **still needs** | in a 5-wing |
|---|---|---|---|---|---|---|
| **Vitas B010** | 344.4 | **521.2** | 76 | 15 | **61** | **1,563** |
| **Stingray** | 231.6 | 349.1 | 73 | **0** | **73** | 1,047 |
| BR050 Basic | 213.5 | 320.4 | 80 | 14 | 66 | 961 |
| Bullfrog | 191.0 | 281.9 | 70 | 0 | 70 | 846 |
| BR050 Defense | 183.1 | 276.0 | 80 | 14 | 66 | 828 |
| BR050 Incendiary | 39.9 | 49.5 | 50 | 14 | 35 | 148 |

**Size ≤ 2 — fits every bay, including the Predator.** In a Predator 4-wing:

| fighter | stock | maxed | full TP | pool | still needs | in a 4-wing |
|---|---|---|---|---|---|---|
| **Strix** | 175.4 | **261.4** | 82 | 14 | **68** | **653** |
| AT021 Pulse | 141.8 | 180.4 | 54 | 0 | 54 | 451 |
| *Vitas A021* | 79.8 | 97.6 | 45 | 15 | 30 | 244 |
| AT021 Interfer | 58.5 | 87.4 | 53 | 0 | 53 | 218 |
| *Newland* | 53.1 | 65.3 | 45 | 0 | 45 | 163 |
| *Spore* | 6.3 | 7.9 | 45 | 14 | 31 | 20 |

**Size 1 — fits everywhere.** Balance Anderson 48.0 → 107.9 (pool 10, needs 60); SC002 34.5 → 68.9
(pool **38**, needs 32).

### The answer

1. **Vitas B010 first.** 521 per craft, 49% clear of the next fighter, and it is the one the CV3000
   exists to carry. Pool 15 of 76 — **61 points**.
2. **Stingray second, and it has a pool of zero.** 349 per craft *and* three-way system damage
   (primary weapon 35%/+125%, command 30%/+125%, propulsion 30%/+200%), so the hit-point score
   understates it. **73 points.**
3. **Strix is not a wasted investment** — it is the best fighter the Predator Carrier can take, and
   the Predator is 4 fighters for 18 CP against the CV3000's 5 for 40. Keep going: **68 points.**
4. **SC002 is the misallocation.** It holds **38 points, the largest fighter pool on the account**,
   and finishes 13th of 14 per craft. Same shape as the Void Elfin: a reset candidate.
5. The three *italicised* system-damage specialists hold 29 points between them that this score can
   neither justify nor condemn — see below.

**Before any of that, though: unlocking the CV3000's 8-fighter module takes its wing multiplier from
×3.0 to ×4.5.** That is +50% on every fighter in it, more than any amount of TP buys, and it costs a
module rather than points.

### The triangle rule: a wing is worth T(n), not n

Craft die one at a time, so a wing's damage is not linear in its size. If anti-air kills them
sequentially and each craft fires until it dies, craft *i* dies at time *i·T* and total damage is
proportional to **T(n) = n(n+1)/2**:

| wing | naive (n) | **T(n)** | per craft, T(n)/n |
|---|---|---|---|
| 1 | 1 | 1 | 1.00 |
| 2 | 2 | **3** | 1.50 |
| 3 | 3 | 6 | 2.00 |
| **4** | 4 | **10** | 2.50 |
| 5 | 5 | 15 | 3.00 |
| 8 | 8 | 36 | 4.50 |

Chris's two figures were *"5 fighters is 10× as strong as an individual while 2 fighters is only 3×"*,
and then: *"I was doing n−1, not n+1"*. That settles it — n(n−1)/2 gives 10 at n=5, which is where the
10 came from, while the 3 for a 2-wing is the n+1 form. **The rule is T(n) = n(n+1)/2**, so a 5-wing
is 15×, not 10×.

Consequence for scoring: **a craft in a 4-wing is worth 2.5× the same craft flying alone, and in a
2-wing 1.5×** — so the carrier matters as much as the fighter. None of the per-craft figures above
include this, and they should be multiplied by (n+1)/2 for the bay they will actually fly from.

### Four of these rows are meaningless, and it is the same failure as HaleBopp

*Italicised* rows are **system-damage specialists**: their gun is a rounding error and their job is
knocking out an enemy's modules, which a hit-point score cannot see. Decoding
`EFFECT_SYSTEM_BURST_DAMAGE` as `G CCC MMM` (group, chance %, bonus %) — the groups Chris confirmed
from his battle report, 1 = primary weapon, 3 = command, 5 = propulsion:

| fighter | gun | system damage |
|---|---|---|
| Spore | **5** | primary weapon **50%/+200%**, command 15%/+100%, propulsion 30%/+200% |
| Newland | **35** | primary weapon **60%/+250%**, command 25%/+200%, propulsion 30%/+200% |
| Vitas A021 | **65** | propulsion **75%/+150%**, grp2 20%/+150%, primary weapon 30%/+200% |
| Strix | 130 | command 35%/+200%, grp2 30%/+200%, primary weapon 30%/+200% |
| Bullfrog | 250 | command 35%/+150%, grp2 35%/+100%, primary weapon 30%/+200% |
| Stingray | 400 | primary weapon 35%/+125%, command 30%/+125%, propulsion 30%/+200% |
| BR050 Basic / Defense | 450 | command 20%/+200%, propulsion 30%/+200%, grp2 30%/+200% |

So **Spore scoring 4.0 is not a verdict** — it carries the second-highest weapon-knockout chance in
the roster on a 5-damage gun. **Newland at 32.7** has the highest of all, 60%/+250% against primary
weapons. **Vitas A021 at 48.8** disables propulsion 75% of the time. These are the bombers Chris
described doing system damage to the AC721s, and `data/system_damage.md` has the mechanic; what does
not exist is a score that combines it with hit-point damage.

**Stingray and BR050 Basic are the ones that do both** — a real gun *and* three-way system damage —
and Stingray has a pool of 0.

