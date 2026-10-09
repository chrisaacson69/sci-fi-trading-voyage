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

## Scored against the right enemy: two recommendations reverse

Everything above this section scores against the **large** pirate team (1010801, 98 CP: a
battlecruiser, four cruisers, four Stingrays). The other agent's point, via Chris: *"we tend to only
hit BC at the larger fleet sizes"* — a small fleet meets team **1010501** instead (30 CP: 4× Rager
Torpedo, a frigate, plus a Frost Missile), and that changes the ranking enormously. `tp_assign.py
--vs small|large`.

| fighter | **small** | large | rank S | rank L | pool | |
|---|---|---|---|---|---|---|
| **Vitas B010** | **719.8** | **399.3** | 1 | 1 | 15 | best in both |
| **Balance Anderson** | **592.0** | 106.1 | **2** | 8 | 10 | +6 places small |
| **SC002** | **527.9** | 71.4 | **3** | 10 | **38** | +7 places small |
| BR050 Basic | 513.5 | 256.8 | 4 | 3 | 14 | |
| Stingray | 492.3 | 278.1 | 5 | 2 | 0 | |
| AT021 Interfer | 473.4 | 71.0 | 6 | 11 | 0 | +5 places small |
| Bullfrog | 435.1 | 221.4 | 8 | 4 | 0 | |
| Strix | 402.3 | 201.4 | 10 | 6 | 14 | |

| corvette | **small** | large | rank S | rank L | pool | |
|---|---|---|---|---|---|---|
| **Void Elfin** | **745.5** | 207.1 | **1** | 3 | 34 | +2 places small |
| **Cellular Defender** | 512.5 | **255.3** | 2 | 1 | 36 | strong in both |
| NebulaChaser Ball | 429.7 | 83.3 | 3 | 8 | 44 | +5 places small |
| CVM011 Miss | 410.1 | 98.7 | 4 | 7 | 6 | |
| NebulaChaser Pulse | 403.5 | 212.5 | 5 | 2 | 44 | |
| CVT800 | 376.1 | 197.4 | 7 | 4 | 37 | |
| SLevi9 | 360.9 | 193.8 | 9 | 5 | 0 | |

### What this reverses

- **The Void Elfin is not a misallocation — it is the best corvette on the account against a small
  fleet**, 745.5 and 46% clear of the next. Its 35 evasion, and the evasion-by-weapon-type rows its
  ladder opens with, are exactly what beats a team of four torpedo frigates and a missile destroyer.
  Against the large team, which fields fighters with good hit rates against small hulls, that defence
  collapses and it falls to third. **Do not reset it.**
- **SC002's 38 points are not the misallocation either.** Third of fourteen against a small fleet,
  tenth against a large one. Same mechanism: 50 evasion on a 1-size body. (And per Chris it is not
  after all one of the fixed-TP hulls, so a reset would free 25 of the 38 — but there is no reset to
  spend.)
- **Balance Anderson jumps from 8th to 2nd**, and that is *before* counting the accuracy interference
  it exists for, which nothing here scores. The open EW question in `data/tp.md` now looks more
  likely to resolve in its favour than against it.

Both of my "misallocation" calls were artefacts of scoring an escort against a battlecruiser.

### What it does not explain: Strix

Strix sits **10th against small and 6th against large** — below BR050 Basic and Bullfrog in both. So
the by-type view does not explain preferring it over them. **Bay compatibility does**: Strix is
size 2 and BR050 and Bullfrog are size 3, so on the account's size≤2 bays — the Predator Carrier at
4 fighters for 18 CP, Eternal Heavens, Tundra, Ceres — neither of the other two can fly at all. Strix
is the best fighter those bays can take, which is a correct recommendation reached by a different
route than enemy type.

## Where the account's corvette TP should go

Corvettes have **no size class** — they take boat seats (`EFFECT_CARRIER_BOAT`), and any corvette fits
any boat bay. So unlike the fighters there is no compatibility split; there is only the wing size.

Boat bays the account has:

| carrier | CP | stock | unlocked | wing ×(n+1)/2 |
|---|---|---|---|---|
| **Solar Whale** | 55 | **6** | 6 | **×3.5** |
| Jaeger Carrier | 20 | 4 | 4 | ×2.5 |
| XT 20 Escort | 18 | 4 | 4 | ×2.5 |
| CV3000 | 40 | 3 | 3 | ×2.0 |
| AC721 Amphibious | 12 | 2 | 2 | ×1.5 |
| Guardian Amphibious | 14 | 2 | 2 | ×1.5 |
| 066 Carrier | 18 | 2 | 2 | ×1.5 |
| Spear of Uranus / FSV830 / Ediacaran / Megrez | 35–40 | **none** | 3 | — |

The **Jaeger Carrier at 4 seats for 20 CP** is the efficient platform; the Solar Whale's 6-seat bay is
the biggest multiplier but costs 55 CP. Four hulls carry no boats at all until the module is unlocked.

| corvette | stock | maxed | full TP | pool | **still needs** | in a 6-wing |
|---|---|---|---|---|---|---|
| **Cellular Defender** | 182.3 | **311.5** | 79 | 36 | **43** | **1,090** |
| **NebulaChaser Pulse** | 176.2 | 280.9 | 77 | 44 | **32** | 983 |
| CVT800 | 179.9 | 261.3 | 78 | 37 | 41 | 914 |
| **SLevi9** | 157.0 | 248.1 | **118** | **0** | **118** | 868 |
| RedBeast | 110.2 | 204.6 | 106 | 35 | 71 | 716 |
| Void Elfin | 78.7 | 129.4 | 76 | 34 | 41 | 453 |
| NebulaChaser Ball | 63.9 | 94.0 | 63 | 44 | 19 | 329 |
| CVM011 Miss / Can / HS | 68.9 / 71.1 / 45.0 | 89.8 / 87.3 / 58.2 | 51 / 40 / 62 | 6 | 45 / 34 / 56 | 314 / 306 / 204 |
| CV-11003 | 49.9 | 71.4 | 66 | 19 | 47 | 250 |
| Silent Assassin (Ray) | 51.0 | 71.2 | 66 | 10 | 56 | 249 |
| *Tempel Intf / Alert* | 42.4 | 65.8 | 76 | 0 | 76 | 230 |
| *HaleBopp MR / Dock* | 3.8 | 4.8 | 46 | 0 | 46 | 17 |

### Where the Void Elfin's 34 points actually do most good

The plan was Void Elfin → SLevi9. SLevi9 is the right long-term target — 248 maxed, pool of zero — but
its ladder is **118 TP**, the longest of any corvette, so 34 points is 29% of the way and buys the
shallowest part of someone else's curve:

| 34 points into… | before | after | gain | in a 6-wing | |
|---|---|---|---|---|---|
| **Cellular Defender** | 248.7 | 310.6 | **+61.9** | **+217** | 9 short of finished |
| **NebulaChaser Pulse** | 231.2 | 280.9 | +49.6 | +174 | **finishes it** |
| CVT800 | 218.1 | 254.8 | +36.7 | +128 | 7 short |
| SLevi9 | 157.0 | 189.1 | +32.1 | +112 | 84 still needed |

**SLevi9 is the worst of the four**, by nearly 2× against Cellular Defender — not because it is a weak
hull, but because the other three are already 35–45 points up their curves and the steep part of
SLevi9's is still ahead of it. Finishing Cellular Defender or NebulaChaser Pulse first, then starting
SLevi9 with a later pool, beats splitting the difference. (If the 9 points to finish Cellular Defender
can come from anywhere, that is the single best corvette buy on the account.)

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


## Three new families on the oldest account (2026-10-09)

### Pangu — a bodyguard capital, not a gunship

**Megrez / Pangu Phecda** (61301, 盘古天权), battlecruiser, 35 CP, **191,970 HP**, armour 240 — the
highest hit points of any battlecruiser in the tables, against a single 200-damage ×4 missile mount.
That imbalance is the point. It carries the game's **escort mechanic**, which nothing else on the
account has:

| effect | what it is |
|---|---|
| `EFFECT_SHIP_PANGU_ESCORT_COVER` ×3 | three separate *cover* skills (95600, 95660, 95670) |
| `EFFECT_SHIP_PANGU_ESCORT_ADD_SELF_BUFF` ×2 | buffs itself while covering |
| `EFFECT_SHIP_PANGU_ESCORT_ADD_TARGET_BUFF` | buffs the ship it is covering |
| elsewhere in the tables | `..._ADD_COUNT`, `..._ADD_TIME`, `..._REPAIR_TARGET_ADD`, `..._STAGE`, `EFFECT_PANGU_SHARE_REPAIR_EFFICIENCY` |

So a Pangu hull **takes damage aimed at another ship** and buffs both ends of that arrangement, with
upgrades that extend how many ships it covers, for how long, and whether it repairs them. It is the
properly-designed version of what the Carilion Special tank was being asked to do: a hull that soaks
damage *for someone else* rather than merely surviving itself. It also brings 3 corvettes, a drone,
and +70/+80% aircraft attack.

The one thing not readable here is the magnitude — the parameters are skill ids (95600, 956201 …) and
the skill table has not been extracted, so how much it covers and for how long is unknown. Only
**Alioth-class Type B** (52002) shares the mechanic, at a smaller scale.

### Ranger — an anti-aircraft cruiser, a gun cruiser, and a cruise liner

| variant | id | CP | what it is |
|---|---|---|---|
| **Ranger Composite** | 51301 | 16 | **anti-aircraft**: `WEAPON_ATK_AIRCRAFT_HIT_RATE_INC` **+100%**, +40, +63 and `AIRCRAFT_WEAPON_ATTKACK_ADD` +85, +50, on four guns (450×2, 225, 85, 25×2) |
| Ranger Ion | 51302 | 18 | a straight gun cruiser: 750 ion + 700 energy, armour-ignoring, no AA |
| Ranger Cruiser | 51303 | 18 | 游骑兵**游轮** — 游轮 is a *cruise liner*. **No weapons at all**, armour 0, energy resist 0, 73,260 HP. Not a warship. |

All three are 73,260 HP cruisers. The **Composite is the interesting one**: +100% hit rate against
aircraft is the largest anti-air modifier seen so far, and the 98 CP pirate team fields four
Stingrays, which is the threat `data/tp.md` has had open as "ship-vs-aircraft AA not decoded".

### Thassa = the Fluorite-class, and it decodes the EW question

Chris, 2026-10-09: an EW destroyer in two flavours, **A** at 27,960 HP (AA with a jamming system) and
**B** at 29,570 HP (interference). Those hit points are an exact fingerprint:

| | id | HP | CP |
|---|---|---|---|
| **Thassa A** | 41401 | **27,960** | 7 |
| **Thassa B** | 41402 | **29,570** | 7 |

— **Fluorite-class Info** (萤石级信息) and **Fluorite-class Electronic** (萤石级电子). Both turned up in
the first EW search and were passed over in favour of a transliteration guess at the Antontas; the HP
settles it outright. (The Antontas Command Ship is a real and separate hull: 3 drones + 3 corvettes,
+40/+60 aircraft attack, −30% crit damage taken, 1,000-damage railgun.)

**How the jamming actually works.** Each carries a mount of `ACTION 7` doing **zero damage** whose
only job is to land `WEAPON_ADD_SKILL_ON_BUFF_HIT` — a skill that is nothing but
`EFFECT_HIT_RATE_DEC` on what it hits. The *application rate* is its weapon priority table:

| target | application rate |
|---|---|
| aircraft (100–105) and corvettes (200) | **100%** |
| frigates, destroyers | **75%** |
| cruisers | **30%** |
| battlecruisers and above | **20%** |

**That is the answer to the open EW question, and it is the small-fleet answer.** A jammer lands on a
frigate three-quarters of the time and on a battlecruiser one time in five, so electronic warfare is
worth roughly 3.75× as much against the small pirate team as against the large one — the same
direction as every other result in the section above, and much more sharply.

**A and B are the same ship, exactly as Chris suspected.** Identical 7 CP, armour 20, energy resist 2,
the same two mounts, the same 5% anti-missile, the same `BALLISTIC_INJURY_SUB 20`. Three differences,
no more:

| | Thassa A (41401) | Thassa B (41402) |
|---|---|---|
| HP | 27,960 | 29,570 |
| jams first | **corvettes** (rank 1), aircraft rank 2 | **aircraft** (rank 1), corvettes rank 2 |
| skill | 9189 — two `HIT_RATE_DEC` rows on the default curve | 9190 — two rows at **5 each, −10 points** |

So B jams harder and prefers aircraft; A jams softer and prefers corvettes. Against the 98 CP team's
four Stingrays, B is the one that matters.

Two things still unverified: whether `TARGET_TEAM 0` really means the debuff lands on the enemy rather
than buffing the firer (the zero-damage mount and the hit table make it very hard to read any other
way, but it is not proven), and the size of 9189's blank-parameter rows, which take the default
per-level curve rather than a stated number.

## Resets cap at 50 points

Chris's AC721, 2026-10-09: **205 TP on the family, 184 committed, and a reset returns only 50.** So
21 points are the unremovable kind — and, far more importantly, **a reset is capped at 50 points
however much is in the hull**. On a 184-point investment that recovers 27%.

That makes resets much worse than `data/tp.md` assumed. They are not "expensive but a clean slate";
they are expensive *and* partial, and the more a hull has absorbed the worse the ratio gets. On this
account the practical conclusion is that committed TP is close to permanent and the only real decision
is where the next points go.

**The 184 also confirms the pool model.** No single AC721 variant can absorb 184 — the tools give
Logistics 118, Missile 134, Amphibious 123, Ion 131 — so the 184 is **split across variants**, which
is exactly what Chris does with this family: *"you can use both the A and B models, as the A is the
hauler and helps mining while the B is the corvette carrier, a cheap way to bring in corvettes
early."* So a family pool can be **concentrated** on one variant (NebulaChaser, 44 all in the Pulse)
or **split** across several (AC721, 184 over at least two), and the per-variant capacity the tools
compute is consistent with the game's own number.
