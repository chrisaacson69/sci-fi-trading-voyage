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

**Returns usually do diminish, but far from always**: median concavity **0.79**, with **87 hulls
diminishing, 23 flat and 40 increasing**. Curve shape is a property of the hull rather than a law, but
the majority runs Chris's way.

An earlier version of this file said the opposite — median 0.95, 73 against 54 — and that was a
pricing bug, not a finding. The tools were charging an *average* cost per level where **23% of
enhancement rows have a non-uniform cost ladder** and `1,1,2,2,2` is the second commonest shape in the
game. Averaging it overpriced the cheap opening rungs by 60%, which flattened the early part of every
such curve and made the late part look relatively better. Pricing the real rung steepens the openings
and moves the median from 0.95 to 0.79. What spreading really rests on is the two things above — the good buys run out per
hull, and the supply is typed — plus stranding risk, below.

## Reading an account's blueprint list (Chris, 2026-10-12)

The format Chris uses for an account's blueprints. `py -3 blueprints.py <account>` parses the verbatim
`data/blueprints/<account>_raw.txt` into `data/blueprints/<account>.csv`; an optional third column gives the class.

- **Name + letter** (`KCCPA`, `IO A`): the family and its variant, A-D. A is the base hull and the
  letters follow ship-id order (Taurus A = id 40501, B = 40502, ...). Variants of a family **share
  one TP pool**, so the number repeats across them; count it once per family.
- **A whole number** is the TP spent on the family (unspent TP is not in the list), and means the variant is **owned**.
- **A decimal** (`0.35`) means the variant is **not owned yet**: the fraction of its unlock done.
  A blueprint for a family you lack gives the base hull; a variant has a 15-100% chance per hit
  that **accumulates** across hits; the decimal is the progress so far (0.6-0.7 is usually 2-3 hits).
  See "How a box pick works" below.
- **Capital ships read `TP/modules`** (`16/9`): TP awarded, then modules owned. A repeat pick of a
  capital gives an extra module, not a second hull. Every capital starts with 2 modules, except the
  Solar Whale, Thunderbolt, Ediacaran and Marshal Crux with 3. So ST59 `16/9` is 16 TP and 7 earned modules: **8 BP** (the hull plus 7).

BP per account = owned non-capital variants + for each capital (1 + modules earned). On Del05Hades
that gives 89 BP against 1,091 TP, about 1:12 (CnC04Cavalry: 81 BP, 572 TP, about 1:7; Countlesmoney: 110 BP, 1,444 TP, about 1:13; Count DeMonet: 162 BP, 4,034 TP, about 1:25; CountDeMonet: 157 BP, 4,617 TP, about 1:29), not the 1:9 the boxes suggest
(`drops.csv`: a box is 10% blueprint, 90% TP). Repeat picks are the reason: a duplicate variant is not
a new BP.

**TP/BP rises with account age (Chris).** 11 BP come from play rather than boxes, so a young
account sits below the boxes' 9:1 (CnC04Cavalry, 7.1). As it ages, repeat picks add TP or modules but
no new BP, so the ratio climbs (Del05Hades, 12.3; Countlesmoney, 13.1; Count DeMonet, the first account, 24.9; CountDeMonet, 29.4). Total TP is a fair measure of an account's age
and strength, or more exactly of how much it has been played: CnC04Cavalry started on server 425, before
Del05Hades on 432, but missed a season or two and sits lowest. TP and boxes are earned only by logging in and taking part: side events
(like the trading event) give some, but most TP comes from season play. So "age" here means seasons played. The player id (player screen, 11 digits) ends in
the starting server; `data/accounts.csv` records it as `player_id`. Six accounts in all; five are recorded so far.

### How a box pick works (Chris, 2026-10-13)

Told, not derived; this replaces earlier guesses here (Claude assumed class changes and a 10 TP
repeat that Chris does not use or the game does not give).

**Sources.** Boxes come from playing (season play mostly; side events like the trading event some).
TP can also be **bought**, which is how an account reaches, say, 20K TP. Most boxes are the
**standard box**, the default below; other boxes differ in which blueprints they offer or add extras
such as double TP.

**Standard box.** It holds 2+ items. Most are in-game goods (ship experience, upgrade technologies)
and can be ignored for blueprints. Each item rolls separately, and long ago a big box could rarely give
more than one blueprint; not seen recently. The blueprint/TP roll:

1. **Roll the class** on the type table (`drops.csv`, general row: FF 28, DD 24, CO 15, CA 12, FT 10,
   BC 5, auxiliary 3, CV 3).
2. **90%: one TP for that class.** You also get **one research point (RP)**.
3. **10%: a blueprint** of that class. Then:
   - you lack the family's **base (A) hull** → you get it, free. For a capital, you get the capital.
   - you have the A → **choose**: a variant you lack, **+5 TP** for that hull, or **+5 RP**.
     With every variant owned, only +5 TP / +5 RP.
   - capital you already have → a **module** you lack, **+10 TP** for that hull, or **+5 RP**.
   - **Variants are not automatic:** choosing one adds 15-100% toward it, and the progress
     **accumulates** until it reaches 100%, so a variant can take several hits.

**Guaranteed-blueprint box, for 15+ RP.** Same class ratios, always a blueprint, then the same choice
as above. Before choosing you may (a) spend in-game currency to **change the class**, or (b) spend
**5 more RP to reroll** from a narrower list, up to **twice**. Bad rolls can still leave only
duplicates and maxed variants, forcing +5 TP / +5 RP.

Chris has **never** spent currency on a class change, and nearly always takes a capital's **module**
over its +10 TP, since few of his capitals have all their modules.

**Capitals look rare in TP.** Spent TP gives capitals 4.5-7.5% on all five lists (CnC04Cavalry 7.5,
Del05Hades 4.6, Countlesmoney 7.2, Count DeMonet 4.5, CountDeMonet 6.0) against 11% in the table. Under the rules above
there are two reasons that is expected, before any question of luck:
- a capital blueprint repeat becomes a **module** (BP), while a non-capital repeat chosen as TP adds
  **+5 TP** to its class, so non-capital TP is inflated relative to capital TP;
- TP **spent** (the list numbers) is not TP **earned** where TP was bought or came from double-TP or
  event boxes, and those need not follow the table.
How far the first can push capitals below 11% depends on how many +5 TP choices were taken.

**TP per roll and box purchases (Chris, 2026-10-13).** Most boxes give **1 TP** per roll. Event boxes
can give **2x TP**, and capital boxes have given 2+ TP, not always in the capital class (possibly left
over from the older system, where a box held X items that each rolled separately). A standard box
costs **300 proxima** (in-game currency) and is offered at **half price twice a day**; Chris buys at
least one half-price box daily. Event boxes at **450 proxima** add extras (2x TP, a better chance at a
particular hull); Chris usually buys the first, which is often half price (225). These are rare and,
in Chris's view, **do not shift the odds much**, so the spent TP on the lists is close to box-earned TP,
though how much of it was bought cannot be separated.

**Season boxes and where the "excess" TP comes from (Chris, 2026-10-13).** Most season rewards are a
**guaranteed-blueprint box**, like the RP box but with no reroll or class change on a duplicate. That
is a large source of blueprint outcomes beyond the 10% roll, which closes the gap a box-rolls-only count
leaves: on Count DeMonet, rolls and RP boxes alone give about 300 blueprint outcomes, while the +5 TP
choices plus owned BP needed to dilute capitals to 4.5% come to about 650. Within a class **every
hull is equally likely** (worked out by players elsewhere; clearer in the older system, where RP bought
blueprints directly), so the class table is the built-in rarity. Common hulls (FG300, AC721) are hit
over and over; with every variant owned, the choice is +5 TP or +5 RP, and Chris takes **+5 TP**
(spending 15-25 RP on a pick to get 5 RP back feels bad). **Duplicates are therefore most of the TP
beyond the 1-TP rolls**, and they land on the common classes, which is why capitals look rare in TP.
**Variant misses** (a hit that only adds progress) soak up blueprint hits too, giving neither a BP nor TP.

**+5 TP or +5 RP on a duplicate? (2026-10-13, unsettled)** The theory: always take RP, because capitals
are the limit and every RP is a try at one; the small classes' TP arrives anyway. In numbers, 5 RP is a
third of a guaranteed box, which rolls a capital 11% of the time, so **about 27 duplicates taken as RP
buy one capital pick** (before rerolls or a class change). The question is whether 5 TP on a hull is
worth 1/27 of a capital pick. Chris: an FG300 variant costs about **130 TP to max**, so about 400 for
the family (Count DeMonet has spent 178), so even his biggest account is not at "useless TP" yet, and
the FG300 would reach 400 long before a BC maxes, likely even taking RP. Full TP-to-max per hull is not
in this repo (`tp_curves.csv` `max_tp` is the DPM ladder only); it would come from
`lagrange-combat/tools/maxout.py`.

## What the types are

`SHIP_TYPE` 7 — which the client tables call *battleship*, and which holds FSV830, Ganymede and
Ediacaran — is the drop table's **Auxiliary Ship** (3%). Chris, 2026-10-09: in the English game these
are not combat hulls at all but **mobile bases**, used to build small ships and aircraft as
replacements. Expensive to make useful and expensive to run, and rarely worth it in play. So the drop
table covers all eight types after all, and nothing is missing.

## The two ladders are independent

Chris, 2026-10-10: *"TP cost ≠ effect increase. I have seen +2% on 5 levels with costs like
1,1,2,2,2."* Every enhancement carries **two** per-level sequences and they are unrelated:

| | field | example | notes |
|---|---|---|---|
| **cost** | `ENHANCE_COST` on the enhancement row | `(1, 1, 2, 2, 2)` = 8 TP | **23% of 26,351 rows are non-uniform**; `1,1,2,2,2` is the second commonest shape at 2,416 rows |
| **effect** | `EFFECT_PARAM_LEVEL` on the effect row | `1,200;2,400;3,600;4,900;5,1200;` = 12% | cumulative, in the units `EFFECT_PARAM` would use; **1,014 rows carry one**, and the steps are often uneven (2,2,2,3,3) |

Both had been collapsed to averages, and both are now read per rung — `maxout.cost_ladder()` and
`matrix.ladder_at()`. This matters most to the greedy allocators: the cheapest rungs on a hull are
exactly what they should buy first, and an average hid them.

## Levelling the low accounts (2026-10-12)

`lagrange-combat/tools/bp_roster.py` turns a blueprint list into ship ids, which is what the TP tools
need. The two rules come from the other agent's write-up above: a variant letter indexes the family's
ships in **ship-id order** (A = `...01`, the base hull), and variants of a family **share one pool**.

```
python tools/bp_roster.py dela5hades --out data/ships/dela5hades.csv
```

**DelA5Hades** 79 of 79 owned blueprints resolved, 1,091 TP over 33 families.
**Cnc04Cavalry** 73 of 73, **572 TP — exactly the other agent's figure**, which is an independent
check on the pool arithmetic from a completely different direction.

Chris settled all three on 2026-10-12, and the first two were my search being too literal:

- **Swordbearer is the Antontas** (608). Family 608 holds one hull, 60801, whose Chinese name
  安东塔斯指挥舰 the tables translate as "Antontas Command Ship" — the English client calls it the
  **Antontas Swordbearer**. Same ship, already identified days earlier under the other name.
- **NOMA is the NOMA M470** (307), not the NOMA 330 — several ships carry the NOMA name. Its B is a
  **healer** and C is **AA**, which is 30702 M470 Support and 30703 M470 AA exactly, in id order
  behind 30701 M470 Siege.
- **Janbiya is the Saber** (120). Two fighters sit at exactly 4,050 HP, 1 CP, size 2, group 3; the
  Saber is the 3,500-speed one carrying the heavy system-damage profile (primary weapon 60%/+250%),
  against the Reason A101 at 2,800 speed with almost none. Speed and system damage both matched.

**Both accounts now resolve completely — 79 of 79 and 73 of 73 — at 1,091 and 572 TP, agreeing to the
point with the other agent's independent counts from the raw lists.**

## Settled: the lock-on is NOT in the cycle

Chris, 2026-10-12: the Saber's AS weapon shows a **single-ship DPM of 445, computed at 10 armour**.
That is decisive, because the two candidate cycles are far apart:

| cycle | formula | DPM |
|---|---|---|
| **35s** — duration + cooldown + flight, the model's | (75 − 10) × 1 × 4 × 60 / 35 | **445.7** ✓ |
| 45s — the same plus the 10s lock-on | (75 − 10) × 1 × 4 × 60 / 45 | 346.7 |

**445.7 against a displayed 445.** So the cycle the tools already use is right, the lock-on is paid on
acquiring a target rather than on every volley, and **no DPM figure or ranking in this repo moves** —
which is the good outcome, since 65% of mounts carry a lock-on and the alternative would have shifted
everything by 20–40%.

It also confirms the **10-armour display convention** on a second hull, independently of the Quaoar
Railgun in `data/upgrades.md` §7. Two hulls, two weapon types, same convention.

Worth recording that this went against the expectation — Chris's read was that "lock-on is always
counted in the cycle time for fighters, but not corvettes", and his own number says otherwise for a
fighter. The arithmetic is unambiguous.

### Still unexplained: the AA gun's 398

The Saber's cross AA gun reads **398 nominal per fighter**, with 15 damage total to aircraft — and 15
is exactly 5 damage × 3 shots, one action of one launcher. The gun is `install_num` 2, 5 damage, 3×4,
16s duration, 10s cooldown and no flight time, which gives:

| | install 1 | install 2 |
|---|---|---|
| 26s cycle (no lock-on) | 138 | **277** |
| 36s cycle (with) | 100 | 200 |

None of them is 398, and no combination of the damage, install count and the two cycles lands on it.

Two things Chris added do check out, and both are about the hit side rather than the cycle:

- **The tooltip's "60% to-hit, aircraft vs aircraft" is consistent with the tables.** The gun's own
  priority row reads **75%** against fighter classes 100/102/103 and 80% against 105, and the verified
  hit rule is `table × (1 + bonus) × (1 − evasion)`. 75 × (1 − 0.20) = 60, so the tooltip is the table
  rate against a 20%-evasion aircraft — which supports the hit model rather than contradicting it.
- **"Special armour" is special *ammo*** (Chris's correction). So the 15 is what the gun does to
  aircraft with its ammo, not a defence the target carries, and nothing needs adding to the damage
  model for it.

The 398 itself stays open. It is **not** worth fitting a constant to — that is precisely the mistake
Chris caught on the HP ladder, and anti-air is where this model has least ground truth. What would
settle it is the rest of the tooltip: whether that 398 is per launcher or for both, and whether it is
quoted for one Saber or for the three in a wing. None of it touches ship-to-ship DPM.

### Where the pools already in hand should go

Scored against the **small** pirate team, which is the right enemy for accounts at this level. The
pool is per *family*, so the question is which variant to direct each one at.

**DelA5Hades** — biggest gains from TP already held:

| direct the pool at | TP in hand | of | gain now | maxed would be |
|---|---|---|---|---|
| **Reliat Stealth** | 47 | 86 | **+266.8** | 479.1 |
| **Constantine the Great** | 34 | 136 | **+179.4** | 461.2 |
| ST59 | 16 | 152 | +114.8 | 423.9 |
| Wraith (Void Elfin) | 17 | 107 | +105.1 | 757.8 |
| Ray (Silent Assassin) | 44 | 90 | +73.8 | 314.7 |
| AT021 Attack | 19 | 64 | +71.8 | 428.5 |

**Cnc04Cavalry**:

| direct the pool at | TP in hand | of | gain now | maxed would be |
|---|---|---|---|---|
| **Constantine the Great** | 13 | 136 | **+134.4** | 461.2 |
| **Hayredin's Loyal** | 33 | 108 | **+97.6** | 757.7 |
| CV3000 | 14 | 103 | +74.5 | 279.2 |
| M011 Missile | 27 | 91 | +67.2 | 416.9 |
| ST59 | 7 | 152 | +63.1 | 423.9 |

Two patterns worth noting. **Reliat Stealth at 384 BV/CP on 47 points** is the same effect as the Void
Elfin on the mobile account — a cheap high-evasion hull is enormous against a team of torpedo frigates
and collapses against the big one, so these are small-fleet answers and should be re-scored with
`--vs large` before a 200 CP fleet uses them. And **the capitals are where the unspent capacity is**:
Constantine and ST59 have 136 and 152 point ladders against 13–34 in hand, so they will absorb
everything these accounts can feed them for a long time.

## Constraints this has to respect (told, not derived)

1. **Blueprints arrive randomly**, so TP committed to the best design you have now is stranded when a
   better one turns up.
2. **Resets exist but are expensive** — not a routine move.
3. **Some TP cannot be removed at all.** It survives a reset, so assignment there is irreversible.
   The blueprints Chris has identified as carrying fixed TP, 2026-10-09: **FG300, AC721, CAS066
   (066), KCCP, ST59, CV3K, CVM (the M011 corvettes), 11003 (II003)**. SC002 was assumed to be one
   and turns out not to be — a reset on it would free 25 of its 38 points. This list is read off the
   game, not derived, and is the hard constraint on any reallocation plan.
4. **A reset is capped at 50 points, and none is available anyway.** Chris's AC721, 2026-10-09:
   205 TP on the family, 184 committed, and a reset returns **only 50** — 27% of what is in it, with
   21 of the rest being the unremovable kind. So a reset is not a clean slate but a partial refund
   that gets worse the more a hull has absorbed. He has none and buying one is not worth it for a
   side event, so **every recommendation here is about where the NEXT points go**, never about
   recovering committed ones.
5. **A family's pool is shared and can be directed at one variant** — see the README on `tp` vs
   `tp_pool`.
6. **A full playthrough fields 10+ hulls**, plus up to 125 aircraft across ~12 types. Maxing one or
   two hulls at the expense of the rest is not a stable distribution even where it scores well.

## Still open

- **Fighter and corvette TP cannot be priced at all.** They are 25% of the supply (10% + 15%), and
  neither has a `playable_weapons` entry, so `tp_assign.py` has no mounts to work from. `craft.csv`
  and `craft_matrix.csv` have the stats; the gap is a craft-shaped `hull()`.
- **Electronic warfare is now half-decoded, and it is a small-fleet tool.** The Thassa /
  Fluorite-class (41401, 41402) jams with a zero-damage `ACTION 7` mount that lands
  `EFFECT_HIT_RATE_DEC` on what it hits, and the application rate is its priority table: **100%
  against aircraft and corvettes, 75% frigates and destroyers, 30% cruisers, 20% battlecruisers**.
  So a jammer is worth about 3.75× as much against the small pirate team as the large one. What is
  still missing is the *size* of the debuff in a battle — skill 9190 is −10 points of hit rate,
  9189 takes the default per-level curve — and whether the Balance Anderson works the same way.
  Nothing in these tools scores any of it yet, so EW hulls still carry no value here; the difference
  is that the mechanism is now known rather than guessed at. See `data/families.md`.
- **Stranding risk is not priced.** It needs a blueprint arrival rate and the reset cost, neither
  recorded, and a list of which basic hulls carry unremovable TP — a hard constraint.
- **Combat and trade value are still separate scores.** `--roi` prices routes in credits per hour; a
  cruise level and an armour level should ultimately compete in that same currency, not in BV/CP and
  warp % side by side.

## The 20-reset grant (Chris, 2026-10-14)

A balance patch changed enough that NetEase compensated every account with **20 tech-point resets**.
One reset takes up to **50 points out of one FAMILY** and returns them to that family's typed pool;
part of some pools is fixed and comes back as nothing. `tools/reset_plan.py` in the lagrange-combat
repo does both halves - which families to strip, and where the points then go.

Chris also described the other new source of points, which is NOT a reset and NOT permanent:

> season **experience** gives up to **50 temporary TP**, usable only in that season. The first **30
> are easy** and come from PvE. The last **20 can only be had from PvP, or from "upgrades"** - awards
> given for battles, also season-only.

**Corrected 2026-10-14: experience TP is PER HULL, not an account pool, and it has to be EARNED by
fielding and using that hull.** Each hull can reach 30-50 of its own, and none of it survives the
season. That changes the arithmetic completely - a season's peak is not "the permanent pool plus 50",
it is the permanent pool plus 30-50 **on every hull you actually fly**. Chris: "each hull gets their
own experience... it's nice to start with some base TP."

### Therefore: how many hulls you field beats how you allocate between them

The free 30 buys the steepest part of every ladder, so what you do with the permanent points barely
matters by comparison. Worked on Chris's cruiser pool - 69 free points across the Io A, Chimera A and
066 General, with +30 experience landing on each:

| allocation | free split | ends at | sum of BV/CP |
|---|---|---|---|
| two-way split | 35/34/0 | 65/64/30 | **5,943** |
| Io to 50, then Chimera | 20/49/0 | 50/79/30 | 5,905 |
| all free into the Io | 69/0/0 | 99/30/30 | 5,867 |
| even thirds | 23/23/23 | 53/53/53 | 5,836 |

**1.8% separates the best allocation from the worst.** Against that, fielding three hulls instead of
one harvests 90-150 experience points a season rather than 30-50 - a 60-100 point swing. The
allocation question is noise; the roster question is the whole game.

So the rule is a **bootstrapping threshold**, not a hedge: spend permanent points to get a hull over
the line where it is worth fielding, and from then on it earns its own 30-50 every season. Points
concentrated in one hull leave the others below that line, and their experience is forgone
permanently - it cannot be earned by a hull that never flies.

A new blueprint is somewhat cheaper to absorb than it looks, but **not free**: experience has to be
EARNED by flying the hull, PvE encounters stop paying at 30 points, and the last 20 come only from PvP
or battle awards (Chris, 2026-10-14). So a new hull does not start at 30 - it starts at zero and
climbs, at the cost of play time, with the top 20 much harder than the first 30. Pre-positioning
permanent points in a family therefore has real value, and arguments of the form "experience will
cover it later" are claims about grinding, not about a grant.

### Two hard numbers behind the doctrine

**The ladders are concave**, so the top of a ladder is the worst TP you can buy. BV/CP per TP by band:

| hull | 0-10 | 10-20 | 20-33 | 33-50 | 50-66 | 66-80 | 80-99 |
|---|---|---|---|---|---|---|---|
| Io A | 22.5 | 17.0 | 13.8 | 13.4 | 12.4 | 12.1 | **6.1** |
| Chimera A | 12.7 | 13.5 | 11.0 | 13.1 | 9.2 | 9.1 | **6.3** |
| 066 General | 8.6 | 8.7 | 8.0 | 6.2 | 6.7 | 4.9 | **4.5** |
| Conamara Chaos Plasma | 15.4 | 0.0 | 10.9 | 12.0 | 11.9 | 9.1 | **8.6** |

**A reset recovers up to 50 from one family, and a family can be reset AGAIN for another 50** (Chris,
2026-10-14). So nothing is ever stranded permanently and 50 is not a cliff - it is the recovery unit,
which makes it a **block size**. The useful form of the rule is Chris's: *up to 50 points can go into
a hull without creating a reset problem*, because one reset takes all of it back.

That cuts against spreading, not for it. Freeing 69 permanent points costs:

| shape | resets to free it all |
|---|---|
| 50 + 19, two families | 2 |
| 35 + 34, two families | 2 |
| 23 + 23 + 23, three families | **3** |
| 69, one family | 2 |

Each family needs its own reset and each reset recovers at most 50, so holding **less** than 50 in a
family wastes reset capacity. Reset-efficiency therefore prefers fewer families at ~50 each - the
exact opposite of the experience argument above.

**Which of the two wins depends on whether resets are free, and normally they are not.** Chris,
2026-10-14: the 20-reset grant is a one-off that turns up "maybe once a year" with a balance update -
**the normal price of a reset is expensive.** So there are two regimes:

* **During a grant (now).** Resets are not the scarce thing: only 8-16 of the 20 are worth taking on
  any of the five accounts, and each runs out of places to put recovered points long before it runs
  out of resets. Spending an extra reset to keep a third hull earning 30-50 a season is trivially
  worth it, so reset-efficiency is only a tiebreaker between otherwise equal splits.
* **The rest of the year.** Reset-efficiency is a real cost and the 50-point block is the discipline
  that avoids paying it: a family at or under 50 is undone by one reset, a family at 99 needs two.
  Points committed past 50 in a hull are a bet that it will not need unwinding before the next grant.

Conveniently the two constraints agree on the number. **~50 per hull is both the reset block and the
end of the useful part of the ladder** - the Io A returns 13.4 BV/CP per TP in its 33-50 band and 6.1
in its last 19 points. So capping a hull near 50 costs almost nothing in value and buys a cheap exit.

Experience TP is season-only and expires by itself, so none of this applies to it - only the
permanent footprint is ever reset.

### The binding constraint is the TYPE of the points, not the 20 resets

No account can use all 20, and not one of them runs out of resets - they run out of places to put
what comes back. TP is typed, so points recovered from a frigate family can only ever buy frigates.

| account | resets worth taking | TP recovered | best destination found |
|---|---|---|---|
| DelA5Hades | 14 of 20 | 324 | Nebula Pulse, 22.6 BV/CP per TP |
| Cnc04Cavalry | 11 of 20 | 176 | Wraith, 22.8 per TP |
| Countlesmoney | 16 of 20 | 323 | Nebula Pulse, 24.4 per TP |
| Count DeMonet (33) | 8 of 20 | 307 | Nebula Pulse, 25.9 per TP |
| CountDeMonet (76) | 9 of 20 | 328 | Vee B, 16.5 per TP |

### Craft are worth two to ten times what line hulls are

The strongest result, and it holds on all five accounts: recovered points are worth far more in the
**corvette and fighter** pools than in any line hull. Corvettes return **9.7-25.9 BV/CP per TP** and
fighters **9.0-17.1**, against **0.08-14.4** for frigates, destroyers and cruisers. The reason is the
wing multiplier - a craft in a 4-bay has its damage counted (n+1)/2 = 2.5 times, so a point spent on
the craft is spent 2.5 times over, while the same point in a cruiser is spent once.

The cruiser pools are also simply closer to saturation. On CountDeMonet (76) the CA queue ends with
the Conamara Chaos Plasma taking 17 points for **0.08 per TP** - a rounding error - and the fielded
Jaeger Carrier at 1.90. Points that cheap are better left unrecovered until a new cruiser blueprint
arrives, because the reset that frees them is itself the scarce thing.

### The frigate pools on the big accounts are stranded, and a reset cannot unstrand them

This is the same wall already recorded for the unspent pools. The big accounts hold large FF pools in
families no fleet fields, and their fleets field so few frigate families that there is nowhere for the
points to land:

| account | stranded, by type | held in |
|---|---|---|
| DelA5Hades | FF 223 | M470 50, Ruby Railgun 48, Mare Imbrium 48, Mare Serenitatis 47, Carilion Recon 30 |
| CountDeMonet (76) | FF 250, DD 50 | M470, Mare Nubium, Carilion Recon, FG300, Mare Imbrium, Ceres Carrier - 50 each |
| Count DeMonet (33) | FF 200, DD 100 | FG300, M470, Carilion Recon, Mare Nubium, AC721, Winged Hussar - 50 each |
| Countlesmoney | FF 184, BC 33, AUX 16 | Carilion Recon 50, Mare Imbrium 46, Ruby Railgun 44, Mare Serenitatis 44 |
| Cnc04Cavalry | BC 20, AUX 9 | Constantine 13, ST59 7, FSV830 9 |

Resetting any of these converts 50 usable points into 50 unusable ones, so the tool refuses them and
says why. The only thing that moves them is a frigate the fleet wants to field - which is a blueprint
problem, not a tech-point problem.

### A reset is not needed to fix a merely unfielded hull

Worth separating, because it looks like a reset case and is not. On CountDeMonet (76) the Winged
Hussar A already holds its full ladder (123 points, family 408) and still does not make the FF/DD
fleet - the planner passes it over on the gradient, not for want of points. Dropping 2 XenoStinger
for 3 Hussar is **+0.49%** and fills the fleet to exactly 400 CP. Free, and no reset involved.

### Two bugs this uncovered

1. `reset_plan.py` decided which families were fielded by looking for each hull's **name** in
   `fleet_plan`'s printed output. That output ends with a `craft unused:` line naming two dozen idle
   craft, so idle craft counted as fielded and their families were never offered for reset; and a
   carrier bay prints its bay label, never its roster name, so **AC721 was offered up for reset on
   accounts whose fleet was flying it**. `fleet_plan` now emits a `FIELDED_SIDS` line and
   `reset_plan` reads ids; it refuses to run if that line is missing rather than guess.
2. Demand was taken per fielded **family** rather than per fielded **variant**. Family 511 holds 19
   points on CountDeMonet (76) and flies the Jaeger Carrier, but the family's best ladder belongs to
   the Jaeger **Cannon**, so the plan put 69 points into the Cannon - stripping the bay the cruiser
   fleet is built around. Points now go only to the variant actually fielded.
