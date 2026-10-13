# Fleets for the small accounts

Goal (Chris, 2026-10-12): two fleets per account, **400 CP each — one FF/DD, one CA**, both wanting
**5 carried craft**. These are in-game fleets, so cargo and the trading event's speed rules do not
apply; `data/upgrades.md` is scoped to the event and none of it is relevant here.

Built by `lagrange-combat/tools/fleet_build.py` from the resolved rosters, scored on
**sqrt(fleet DPM × fleet HP)** — the strength metric `data/npc_teams.csv` already uses to call a
fight — against the 98 CP pirate team, with each variant's build limit enforced.

```
python tools/fleet_build.py dela5hades --cp 400 --types FF,DD --vs large --tp
```

## Two things the first version got wrong

Chris, 2026-10-12, on the first pass: *"the comps do not look right, not even against high armor."*
Two rules were missing and both change the answer:

1. **TP goes to ONE variant of a family, exclusively.** Fielding a second variant means fielding it at
   **zero points**, so a 60 TP Taurus Assault beats a 0 TP Taurus Defense. The builder now assigns each
   family's pool deliberately — to the variant worth most per CP while holding it — and values every
   other variant of that family at 0 TP, marked `0*` in the tables below.
2. **Rank on BV/CP, not total fleet strength.** The cap is CP, so value per point is what maximises.
   This is what promoted the Ruby Railgun and Mare Serenitatis on DelA5Hades, which Chris had already
   picked out by eye as good BV/CP, and demoted the Eris Armor, which was only ever in the fleet as a
   second Eris variant sharing one pool.

## Build limits bind, not CP

Six of the nine hulls in DelA5Hades' FF/DD fleet are **at their build limit** and the fleet still
scrapes to fill 400 CP with single ships. "What should I build" has a blunt answer on these accounts:
**build the cap of the good hulls**, because you run out of permitted hulls before you run out of
points. Chris: *"the smaller account will have troubles with # of hulls — I found this account
difficult."*

## DelA5Hades

**FF/DD, 400 CP** — 63 ships, 149,674 DPM, 1,459,790 HP

| hull | n | CP | BV/CP | DPM | HP | pool |
|---|---|---|---|---|---|---|
| Reliat Energy | 10 *(limit)* | 40 | **1214** | 20,000 | 117,940 | 47 |
| Eris Heavy Cannon | 10 *(limit)* | 90 | 1209 | 36,575 | 323,720 | 68 |
| Winged Hussar A | 10 *(limit)* | 60 | 1195 | 18,705 | 274,790 | 57 |
| Guardian Pulse | 10 *(limit)* | 90 | 1168 | 34,725 | 318,060 | 46 |
| **Ruby Railgun** | 10 *(limit)* | 50 | 1099 | 15,108 | 199,890 | 48 |
| **Mare Serenitatis A** | 10 *(limit)* | 50 | 1083 | 18,828 | 155,690 | 47 |
| Taurus Pulse | 1 | 11 | 1074 | 3,120 | 44,690 | 62 |
| Mare Imbrium Basic | 1 | 5 | 1020 | 1,794 | 14,480 | 48 |
| Reliat Stealth | 1 | 4 | 733 | 815 | 10,530 | 0* |

**CA, 400 CP** — 22 ships, 177,637 DPM, 1,515,846 HP, **21.0×** the 98 CP team

| hull | n | CP | BV/CP | DPM | HP | pool |
|---|---|---|---|---|---|---|
| Io A | 8 *(limit)* | 144 | **1563** | 94,422 | 536,720 | 30 |
| 066 Bombardment | 12 *(limit)* | 216 | 1153 | 75,558 | 820,884 | 30 |
| Ranger Composite | 2 | 32 | 1088 | 7,655 | 158,242 | 30 |

## Cnc04Cavalry

**FF/DD, 400 CP** — 55 ships, 131,976 DPM, 1,661,930 HP, **17.1×**

| hull | n | CP | BV/CP | DPM | HP | pool |
|---|---|---|---|---|---|---|
| Quaoar Railgun | 10 *(limit)* | 60 | **1706** | 34,305 | 305,400 | 33 |
| Taurus Defense | 10 *(limit)* | 80 | 1363 | 23,952 | 496,370 | 47 |
| Winged Hussar A | 10 *(limit)* | 60 | 1115 | 17,598 | 254,350 | 42 |
| Mare Serenitatis A | 10 *(limit)* | 50 | 971 | 15,731 | 149,700 | 26 |
| Taurus Assault | 10 *(limit)* | 110 | 832 | 20,924 | 400,300 | **0\*** |
| XenoStinger Tactical | 5 | 40 | 824 | 19,463 | 55,810 | 30 |

**CA, 400 CP** — 21 ships, 156,498 DPM, 1,706,376 HP, **20.8×**

| hull | n | CP | BV/CP | DPM | HP | pool |
|---|---|---|---|---|---|---|
| Io A | 8 *(limit)* | 144 | **1481** | 84,739 | 536,720 | 14 |
| Chimera A | 8 *(limit)* | 144 | 1239 | 39,750 | 800,936 | 15 |
| Light Cone Composite A | 5 | 100 | 1086 | 32,008 | 368,720 | 13 |

## The 5 reinforcements are SHIPS, not CP

Corrected by Chris, 2026-10-12: the five reinforcements sit **outside the 400 CP cap** — they cost
nothing against it, so the only question is which five hulls go there. And **"CV" means an actual
40+ CP carrier**, not anything with a hangar, which is what an earlier version of this page had wrong.

| account | CV-class owned | CP | limit | stock | unlocked | **×5 reinforcements** |
|---|---|---|---|---|---|---|
| Cnc04Cavalry | **CV3000** | 40 | 5 | 5F + 3C | 8F + 3C | **25F + 15C** (40F + 15C unlocked) |
| both | Solar Whale | 55 | 5 | 0F + 6C | 13F + 3C | 30C (**65F + 15C** unlocked) |
| DelA5Hades | Solar Whale only | | | | | |

So **Cnc04 fields 5× CV3000** for 25 fighters and 15 corvettes with no CP cost at all, and
**DelA5Hades fields 5× Solar Whale** — 30 corvettes as it stands, but **unlocking the Whale's
8-fighter module turns that into 65 fighters + 15 corvettes**, which is comfortably the largest single
upgrade available to that account and costs a module rather than TP.

To add craft *beyond* the five, cheap carriers go in the main fleet and do cost CP: the **8 CP Ceres
Carrier** (2 fighters, size ≤ 2) in the FF/DD fleet, and the **18 CP Predator Carrier** (4 fighters) or
**20 CP Jaeger Carrier** (4 corvettes) in the CA fleet. At 2–3% of line strength each that is cheap,
and the craft themselves are not in the strength index at all.

The battlecruisers are *not* the craft platform — Constantine carries 1 fighter at best and 0 stock,
ST59 2 and 0 stock. They earn their place by fighting, not by carrying.

### Which craft

Both accounts' best fighters are **size 2** — Follower and Hayredin's Loyal, ~250–300 now against
~400 maxed — so a size-2 bay is enough and there is no case for paying up for size 3.

| | best fighters | size | now | maxed | pool |
|---|---|---|---|---|---|
| DelA5Hades | Follower | 2 | 253.9 | 395.2 | **0** |
| | Hayredin's Loyal | 2 | 246.0 | 400.9 | **0** |
| Cnc04Cavalry | Hayredin's Loyal | 2 | 298.5 | 400.9 | 33 |
| | Follower | 2 | 253.9 | 395.2 | **0** |

**Both accounts' two best fighters have empty or near-empty pools** against 81- and 108-point ladders.
Clearest craft-TP opportunity either account has.

## Caveats

- Scored against the **large** team. These accounts will meet the small one more often, and
  `data/tp.md` shows that reverses rankings for cheap high-evasion hulls — rerun with `--vs small`
  before committing to a build if the fleet is for low-tier content.
- Whether a fleet has a **ship-count cap** is still unknown, and the FF/DD fleets run 52–60 hulls.
  If a cap exists these compositions break and the answer shifts toward fewer, bigger ships.
- The craft are not in the strength index at all, so a fleet's real value with 6–8 fighters aboard is
  higher than the numbers here.

## DelA5Hades: the capitals' modules, and 160 unspent points

### The capitals own drone bays, not fighter bays

Chris's module list, 2026-10-12, mapped against `Tb_cfg_ship_system` — M/A/B/C are the group letters
`maxout.build` documents (M = group 101, A = 102, B = 201, C = 202, in system-id order):

| hull | owns | what those are | **does not own** |
|---|---|---|---|
| **ST59** | M2, A3, B1, B3, C1, C2, C3 | three more weapons (M2 16036, A3 16038, B1 16035), a **drone bay** (B3), three C utility modules | **B2 — its 2-fighter carrier bay** |
| **Constantine** | C3 | a **drone bay** (6040110) | C2 — its 1-fighter bay |
| **FSV830** | A3, C2 | one module, a **drone bay** (C2) | C1 — its 2-fighter bay |

So all three capitals carry **drones** and none carries fighters. That settles the earlier question from
the other direction: the battlecruisers are not the craft platform on this account because **the
modules that would make them one are not owned**, not merely because they are small. It also means
`EFFECT_DRONE` matters here and nothing in these tools scores drones at all.

The seven ST59 modules also match the blueprint list's `16/9` exactly — 2 base plus 7 earned — which
is an independent check on the other agent's capital-module reading.

### Where the 160 unspent points go

TP sits in a **typed account pool** before it is assigned, which the per-family numbers in the
blueprint list do not show. DelA5Hades holds: DD 38, FF 33, CV 30, Aux 17, FT 15, CA 13, CO 11, BC 3.

| type | pts | best use | gain | note |
|---|---|---|---|---|
| **FT** | 15 | **Follower** (pool 0 of 81) | **+31.3** | biggest gain of any type, and the account's best fighter |
| **DD** | 38 | **Quaoar Railgun** (pool 0 of 78) | **+29.1** | not currently in the fleet — see below |
| **FF** | 33 | Mare Serenitatis A (47 of 83) | +8.3 | *in* the fleet |
| **CO** | 11 | Wraith (17 of 107) | +17.3 | |
| **CA** | 13 | **Io A** (30 of 100) | +5.7 | *in* the fleet |
| CV | 30 | Solar Whale (0 of 98) | +13.0 | Chris is holding these for a CV3000 |
| BC | 3 | anything | +0.6 to +2.5 | negligible |
| **Aux** | 17 | FSV830 (0 of 65) | **+1.3** | Chris's instinct to save these is right — it is the worst return on the account |

Two things to watch:

- **Reliat Stealth shows the biggest FF gain (+17.9) but shares family 316 with Reliat Energy**, which
  holds the pool and is in the fleet. Spending there is *moving* the pool, not adding to it, so the
  real FF pick is Mare Serenitatis A.
- **The Quaoar Railgun is the best DD buy and is not in the fleet.** It is the highest BV/CP hull on
  Cnc04Cavalry (1706) and sits at 0 TP here; 38 points may well promote it into the composition, so
  the fleet is worth re-running after that spend rather than before.

## DelA5Hades, after the DD spend

**38 DD points on the Quaoar Railgun promote it from absent to the best hull in the fleet**, and the
whole composition improves by **+19%**:

| | ships | strength | top hull |
|---|---|---|---|
| Quaoar at 0 TP | 63 | 2.18e11 | Reliat Energy, BV/CP 1214 |
| **Quaoar at 38 TP** | 62 | **2.60e11** | **Quaoar Railgun, BV/CP 1765** |

Final FF/DD fleet: **10× Quaoar Railgun** (1765), 10× Reliat Energy (1214), 10× Eris Heavy Cannon
(1209), 10× Winged Hussar A (1195), 10× Guardian Pulse (1168), 10× Ruby Railgun (1099), 2× Mare
Serenitatis A — six hulls at their build limit.

## Filling the Solar Whales: 30 corvette seats, 3 blueprints

5× Solar Whale is **30 corvette seats**, and corvette build limits are 10–15, so Chris is right that it
takes **three good corvette blueprints**. DelA5Hades has exactly three:

| corvette | limit | pool | now | maxed | of |
|---|---|---|---|---|---|
| **Hive** | 10 | 19 | **183.2** | 261.3 | 103 |
| **Nebula Pulse** | 10 | 23 | 156.7 | 215.0 | 79 |
| **T800** | 15 | 14 | 150.0 | 202.0 | 80 |

**10 + 10 + 10 = exactly 30.** The next one down, the Wraith at 117.0, is not needed — though it has
the highest ceiling of the four at 210.5 from a 107-point ladder, so it is the better long-term
target if a seat opens.

## Fighters: size 2 only, and two of them are free

With only a Solar Whale, every fighter bay on the account comes from a **Predator Carrier (4F, limit 8)**
or a **Ceres Carrier (2F, limit 10)** placed in a fleet — and **both are size ≤ 2**:

| fighter | size | limit | pool | now | maxed |
|---|---|---|---|---|---|
| **Follower** | 2 | 10 | **0** | 253.9 | 395.2 |
| **Hayredin's Loyal** | 2 | 8 | **0** | 246.0 | 400.9 |
| Bullfrog | **3** | 10 | 0 | 154.2 | 233.8 |

**The Bullfrog cannot fly from either bay.** It is the account's third-best fighter on paper and
unusable in practice until a size-3 bay exists — which on this account means unlocking the Solar
Whale's 8-fighter module.

The two that *can* fly are the two best, and both sit at **zero TP** against 81- and 108-point ladders.
The 15 FT points go to the Follower (+31.3).

## Reset candidates — corrected

A reset moves up to 50 TP out of **one class** back into its typed pool. **It is a class reset, not a
variant reset** (Chris): there is no "Mare Imbrium Pulse" reset, only a "Mare Imbrium" one, so a
candidate has to be a family the account does not want *at all*.

Part of a pool is **fixed** and cannot be recovered. Chris's figures for DelA5Hades, 2026-10-12:

| family | type | pool | **fixed** | scavengeable | per reset |
|---|---|---|---|---|---|
| **FG300** | FF | 79 | 19 | **60** | 50 |
| **AC721** | DD | 76 | 21 | **55** | 50 |

**~100 TP in one reset each**, against the 38 that just bought +19%. (The AC721's 21 fixed points are
the same number as the 205-point AC721 on the oldest account — so the fixed share looks like a
property of the family, not of how much has been poured in.)

Two of my earlier candidates are **withdrawn**, both because the metric cannot see what the hull is
for:

- **Mare Imbrium** — a good hull by reputation, and it was only flagged because the composition
  dropped it to a single ship after the Quaoar spend.
- **M470** — *the healer*, and a first build for a small fleet so ships do not have to be replaced.
  See below.

## The metric does not model healing, and healing is a PvE mechanic

Chris, 2026-10-12, correcting an earlier version of this section that had the mechanism wrong:

> *"Healers heal **during** battle, and don't explicitly heal between battles. A hull that is damaged
> before battle starts cannot be healed above starting value during. Healing is actually better as a
> PvE mechanism — with PvP damage rates are so high, healers don't get to heal long enough to be worth
> it. During PvE, once you reach a certain level, you can take on almost infinite enemies."*

So healing is **hit points restored mid-fight, capped at the HP the ship entered with**. It is not
between-battle repair, and it cannot recover damage taken before the engagement. That makes its value
a function of two things:

- **how long the fight lasts** — healing is a rate, so it compounds over time while HP is a stock
- **incoming damage per second relative to the heal rate**

Which gives a sharp breakpoint rather than a gradual benefit: **once a fleet's heal rate meets the
damage it is taking, it stops losing ships at all** — Chris's "almost infinite enemies". Below that
line a healer buys some time; above it, it buys the engagement outright. PvP sits far below the line
because damage rates are high and fights are short, so the slot is better spent on damage; PvE wave
content sits near or above it, which is why the M470 is a first build for a small fleet.

`sqrt(DPM × HP) / CP` scores a single engagement at a single instant and has no term for a rate, so it
cannot express any of this. Every healer in these tables — M470 Support, Guardian Support, Ceres
Support, Tundra Support, CAS066 Support — scores near its family's floor and reads as a reset candidate
when it is nothing of the sort.

**So the BV rankings in this file are PvP rankings.** For the PvE content these accounts actually run
they are the damage half of the answer, and a healer belongs in the fleet regardless of what the number
says. Making this quantitative needs the repair effects sized — `EFFECT_SHIP_REPAIR_ARMOR_ADD` and the
rest are still unmeasured in `data/upgrades.md` §6 — after which the useful output is not a BV score
but **the incoming DPM at which a given fleet's healing breaks even**.

## Zircon B is worth getting — it beats the XenoStinger

Chris: *"I was curious about the Zircon. The B variant is probably worthwhile and I don't have it yet
here, but upgraded this is supposed to be like the Xeno."* Better than that:

| hull | CP | HP | BV/CP stock | **maxed** | ladder |
|---|---|---|---|---|---|
| **Zircon B** (31902) | 8 | **13,400** | 27.8 | **43.4** | 118 TP |
| XenoStinger Tactical (30401) | 8 | 10,530 | 25.1 | 37.5 | 90 TP |
| Zircon A (31901) | 8 | 13,400 | 19.3 | 29.5 | 118 TP |

**Zircon B ends 16% above the XenoStinger** at the same 8 CP, with 27% more hit points — but it is a
118-point ladder against the Xeno's 90, so it is a long-term target rather than a quick win. Zircon A
is *below* the Xeno and not worth chasing.

DelA5Hades owns the XenoStinger Tactical at **zero TP** and no Zircon at all.

## The Alkaid: no

Chris got 10 of them with 20 TP from the event run. Against the 43 owned FF/DD hulls on DelA5Hades it
ranks **21st and 22nd** (General and Special are the same hull to two significant figures):

| hull | CP | DPM | HP | BV/CP |
|---|---|---|---|---|
| Quaoar Railgun *(fleet #1)* | 6 | 3,672 | 30,540 | **1,765** |
| Mare Serenitatis A *(fleet cutoff)* | 5 | 1,883 | 15,569 | 1,083 |
| **Alkaid-class Special** | 6 | **473** | 18,050 | **487** |
| **Alkaid-class General** | 6 | 473 | 17,940 | 485 |

**Less than half the value of the worst hull already in the fleet**, and it is dominated outright by a
hull the account already fields: the **Ruby Railgun at 5 CP does 1,511 DPM — 3.2× — with *more* hit
points (19,989)**. Cheaper, tougher and three times the damage.

The cause is its armament: a single 240-damage gun, one shot, one install. 17,940 HP sounds like a
body, but at 2,990 HP per CP it is not even good at that — the Winged Hussar A is 4,580 and the Ruby
Railgun 3,998.

And it will not back into the fleet at a larger cap either. Twenty owned hulls rank above it, almost
all at build limit 10, which is roughly 1,200 CP of better options before the Alkaid is reached.

**Caveat:** the tables hold no `-TE` Alkaid, only the two base variants, so this is an evaluation of
the base hull. If the event's TE version has different stats, none of the above applies to it — worth
checking its damage figure on the blueprint screen, since one 240-damage gun is the whole problem.

The 20 TP that came with them is FF-class and should go where the FF points were already headed.

## Pricing the fighter bays properly: they beat the line

The earlier section costed 3 Ceres or 2 Predators for 5–6 craft. The real question is the **18
fighters** DelA5Hades can actually field — the Follower's build limit of 10 plus Hayredin's Loyal's 8 —
and those were never priced.

Costed as **carrier + its wing as one package**, with the wing multiplier T(n)/n on the craft's damage
(a 4-bay gives each fighter 2.5×, a 2-bay 1.5×):

| package | CP | craft | pkg DPM | pkg HP | **BV/CP** |
|---|---|---|---|---|---|
| **Predator + 4 Follower, maxed** | 18 | 4 | 13,757 | 113,890 | **2,199** |
| **Ceres + 2 Follower, maxed** | 8 | 2 | 4,157 | 51,160 | **1,823** |
| Predator + 4 Hayredin's, maxed | 18 | 4 | 9,271 | 108,330 | 1,761 |
| **Predator + 4 Follower, today** | 18 | 4 | 8,474 | 103,910 | **1,649** |
| Ceres + 2 Hayredin's, maxed | 8 | 2 | 2,812 | 48,380 | 1,458 |
| Predator + 4 Hayredin's, today | 18 | 4 | 6,431 | 102,110 | 1,424 |
| Ceres + 2 Follower, today | 8 | 2 | 2,572 | 46,170 | 1,362 |
| Ceres + 2 Hayredin's, today | 8 | 2 | 1,960 | 45,270 | 1,177 |

Line hulls for comparison: **Quaoar Railgun 1,765** (best in the fleet), Reliat Energy 1,214, Eris
Heavy Cannon 1,209, Ruby Railgun 1,099, **Mare Serenitatis A 1,083 (the cutoff)**.

**Every one of the eight packages beats the cutoff, and the best beats the best line hull.** A maxed
Predator-plus-Followers at 2,199 is 25% above the Quaoar. So carriers are not a tax on the fleet —
**they are being under-fielded**, and should displace line hulls rather than be squeezed in after them.

### Predators first, not Ceres

Per CP the Ceres looks cheaper — 4.0 CP a fighter against 4.5 — but that ignores the wing. A 4-bay
multiplies each fighter's damage by **2.5×** against a 2-bay's **1.5×**, so the Predator package is
worth more per CP at every TP level. Chris's "4× Ceres + 2× Predator if we only want the best F" is
the right instinct applied the wrong way round: put the **best fighters in the biggest wings**.

| filling all 18 | CP | fighters | per fighter |
|---|---|---|---|
| **4× Predator + 1× Ceres** | **80** | **18** | 4.4 |
| 9× Ceres | 72 | 18 | 4.0 |
| 4× Predator | 72 | 16 | 4.5 |
| 4× Ceres + 2× Predator | 68 | 16 | 4.2 |

**4× Predator + 1× Ceres, 80 CP, all 18 fighters.** Put the 10 Followers in two Predators and the
Ceres, and Hayredin's 8 in the other two Predators.

One constraint from the hull classes: the **Predator is a CA** and the **Ceres a DD**, so the Predators
come out of the CA fleet's 400 CP and the Ceres out of the FF/DD fleet's. 72 CP of the CA fleet is a
real bite — but at 1,649 BV/CP today it displaces Ranger Composite (1,088) and sits just under Io A.

### And this is where the FT points go

Maxing the Follower takes its package from **1,649 to 2,199, +33%**, across four Predators. Its ladder
is 81 TP and its pool is **zero**; the 15 FT points in hand are the start of that, and it is the
highest-leverage craft spend on the account.

## Correction: reinforcements are capital CV, and the C-carriers were never priced

Chris: *"capital ship CV, not ALL carriers. Why? Because 5×55 CP isn't good to squeeze into a 400 CP
plight, while 400 CP + 5×55 CP = 675 CP. The point was that capital ships go in the reinforce slots
— not that we can't add aircraft to standard hulls."*

So the five reinforcement slots are for **capital CVs specifically**, and the reason is arithmetic:
5× Solar Whale is **275 CP** that would never fit inside 400, and in the free slots it makes the fleet
**effectively 675 CP**. Putting cheap carriers there would waste the slots. Adding Predators and Ceres
to the main fleet is a separate and still-valid move — which is what the section above prices.

### What survives the Whales

Ranked on the fleet metric, `sqrt(DPM × HP)` per unit, the 30 Whale seats take **10 Hive + 15 T800 +
5 Nebula Pulse**. (An earlier version of this page said 10/10/10 using the `tp_assign` scoring instead;
the T800's limit of 15 and its 8,400 HP put it second here.)

That leaves **5 Nebula Pulse, 10 RB7, 10 Wraith, 10 Nebula A, 15 M011 Missile, 15 M011 High-Speed** —
so yes, there is plenty left for corvette carriers in the main fleet, which had not been checked.

### The Jaeger is the best package on the account

| package | CP | pkg DPM | pkg HP | **BV/CP** |
|---|---|---|---|---|
| **Jaeger Carrier + 4 Nebula Pulse** | 20 | 16,516 | 100,382 | **2,036** |
| **Jaeger Carrier + 4 RB7** | 20 | 11,340 | 99,486 | **1,679** |
| Jaeger Carrier + 4 Wraith | 20 | 6,779 | 99,694 | 1,300 |
| AC721 Amphibious + 2 Nebula Pulse | 12 | 4,961 | 42,826 | 1,215 |
| AC721 Amphibious + 2 RB7 | 12 | 3,409 | 42,378 | 1,002 |

**Jaeger + 4 Nebula Pulse at 2,036 beats every line hull on the account** — the Quaoar Railgun is
1,765 and the Io A 1,563 — and beats the best fighter package too. The AC721 Amphibious is a DD, so it
belongs in the FF/DD fleet, and at 1,215 it clears that fleet's 1,083 cutoff.

### The CA fleet, rebuilt with carriers competing

| | CP | BV/CP |
|---|---|---|
| Jaeger Carrier + 4 Nebula Pulse | 20 | 2,036 |
| Jaeger Carrier + 4 RB7 | 2× = 40 | 1,679 |
| Predator Carrier + 4 Follower | 2× = 36 | 1,649 |
| Io A | 8× = 144 | 1,563 |
| Predator Carrier + 4 Hayredin's Loyal | 2× = 36 | 1,424 |
| Jaeger Carrier + 4 Wraith | 2× = 40 | 1,300 |
| 066 Bombardment | 4× = 72 | 1,153 |
| **TOTAL** | **388** | **strength 3.48e11** |

Against **2.69e11** for the carrier-free version — **+29%**. Nine carriers, 176 of the 388 CP, carrying
**20 corvettes and 16 fighters**, and the Ranger Composite drops out entirely.

So the CA fleet is close to half carriers, and that is before the five Solar Whales in the
reinforcement slots. The thing that was missing from every earlier version of this page is that a
carrier is not a tax on the line — **with a wing aboard it is the line.**

## Both DelA5Hades fleets, one shared craft pool

The craft pool is shared, so the fleets cannot be optimised separately. Allocating jointly — packages
and line hulls competing in one pool per fleet, craft drawn once — gives:

### Reinforcements, 10 free ships across the two fleets

| group | ships | CP (free) |
|---|---|---|
| **1** | **5× Solar Whale** — 30 corvette seats: 10 Hive, 15 T800, 5 Nebula Pulse | 275 |
| **2** | **5× Constantine the Great** — BV/CP 1,387, the best capital left | 175 |

That is **450 CP of ships at no cost to either cap**, and it is where the battlecruisers finally earn
their place: not as carriers, but as free bodies in the second reinforcement group.

### CA fleet — 388 CP, strength 3.48e11

**Reading the rows:** `2× Jaeger Carrier + 4 RB7` means **two separate Jaegers, each with a full wing
of four** — eight RB7 in total, not four shared between them. Every bay is filled to its own capacity.


| | CP | BV/CP |
|---|---|---|
| 1× Jaeger Carrier + 4 Nebula Pulse | 20 | **2,036** |
| 2× Jaeger Carrier + 4 RB7 | 40 | 1,679 |
| 2× Predator Carrier + 4 Follower | 36 | 1,649 |
| 8× Io A | 144 | 1,563 |
| 2× Predator Carrier + 4 Hayredin's Loyal | 36 | 1,424 |
| 2× Jaeger Carrier + 4 Wraith | 40 | 1,300 |
| 4× 066 Bombardment | 72 | 1,153 |

### FF/DD fleet — 398 CP, strength 2.61e11

| | CP | BV/CP |
|---|---|---|
| 10× Quaoar Railgun | 60 | **1,765** |
| 1× Ceres Carrier + 2 Follower | 8 | 1,362 |
| 10× Reliat Energy | 40 | 1,214 |
| 10× Eris Heavy Cannon | 90 | 1,209 |
| 10× Winged Hussar A | 60 | 1,195 |
| 10× Guardian Pulse | 90 | 1,168 |
| 10× Ruby Railgun | 50 | 1,099 |

### The CA fleet wins the craft, which is the opposite of the guess

Chris expected that isolating the FF/DD fleet would fill it with AC721s and Ceres. Sharing the pool
does the reverse: **a 4-bay multiplies each craft's damage by 2.5× where a 2-bay gives 1.5×**, so every
Jaeger and Predator outbids every AC721 and Ceres for the same craft. The FF/DD fleet ends up with a
single Ceres and is otherwise pure line, while the CA fleet is **seven carriers carrying 20 corvettes
and 16 fighters**.

The AC721 Amphibious never appears. At 1,215 with Nebula Pulse it clears the FF/DD cutoff on its own,
but the corvettes it would carry are worth more in a Jaeger, and the shared pool is what decides it.

### Craft accounting, checked

| craft | limit | to Whales | to carriers | to the Ceres | left |
|---|---|---|---|---|---|
| Nebula Pulse | 10 | 5 | 4 (1 Jaeger) | — | 1 |
| RB7 | 10 | — | 8 (2 Jaegers) | — | 2 |
| Wraith | 10 | — | 8 (2 Jaegers) | — | 2 |
| Follower | 10 | — | 8 (2 Predators) | 2 | **0** |
| Hayredin's Loyal | 8 | — | 8 (2 Predators) | — | **0** |

Both good fighters are fully committed; the corvettes have a handful spare.

### The spare CP is stranded

The CA fleet uses **388 of 400** and the FF/DD fleet **398 of 400** — and neither remainder can be
spent. The **cheapest CA hull on the account is 16 CP** (KCCPV2.0 Carrier, KCPV ×3), so 12 CP buys
nothing; the cheapest FF/DD is a 3 CP FG300 against 2 CP left. Trading down does not help either:
dropping an 18 CP 066 Bombardment (BV/CP 1,153) to afford a fifth Jaeger at 20 CP would have to carry
Nebula A at 868, which is worse.

So the answer to "do we have more CP here?" is **no — 12 and 2 CP are genuinely unusable**, and the
way to grow these fleets is more bays, not more points.

### 10 Bullfrogs are stranded

With the size gate enforced — Predator and Ceres are **size ≤ 2** — the size-3 Bullfrog has nowhere to
fly, and 10 of them sit unused. (An earlier pass of this allocation put them in Predators, which is
simply illegal.) That is a third argument for the **Solar Whale's 8-fighter module**: it is the
account's only route to a size-3 bay.

Craft still unused after both fleets and the Whales: 10 Bullfrog, 15 AT021 Attack, 10 Wood Owl,
15 AT021 Pulse, 10 Vee A, and the rest of the low tail. **The binding constraint is bays, not craft.**

## Yes — swapping out weaker ships to spend the stranded CP is worth +5.3%

Chris's suggestion, tested by local search from the greedy solution: try every (drop n of X, add m of
Y) that fits the cap and the build limits, keep anything that raises `total DPM × total HP`.

**CA fleet: +5.26%, and it is exactly the swap he proposed.**

| | change | CP |
|---|---|---|
| 066 Bombardment | 4 → **2** | −36 |
| **Ranger Composite** | 0 → **3** | +48 |
| | | **400 CP used, nothing stranded** |

Strength **3.48e11 → 3.66e11**. The 066 has the higher BV/CP (1,153 against the Ranger's 1,088), which
is why the greedy preferred it — but the greedy maximises value per point one ship at a time, and the
fleet is scored on the *product* of its totals. The Ranger Composite carries 632,968 HP across 8 hulls
against the 066's narrower profile, and shifting the balance toward hit points raises the product even
at slightly lower BV/CP. **BV/CP ranking is a good heuristic, not the optimum.**

**FF/DD fleet: the +1.3% the search found is an artefact — ignore it.** It proposed dropping 7 Winged
Hussar A for 6 Eris Armor, having given the Eris Armor the family pool that the Eris Heavy Cannon
already holds. Under the real rule, with the pool committed to the Heavy Cannon:

| | BV/CP with the pool | **at 0 TP** |
|---|---|---|
| Eris Heavy Cannon (9 CP) | 1,209 | 644 |
| Eris Armor (7 CP) | 1,060 | **564** |
| Winged Hussar A (6 CP) | — | **1,195** |

Eris Armor at 564 against the Winged Hussar's 1,195: the swap is less than half as good, not better.
The greedy FF/DD fleet stands as it is.

That is the same trap as the original composition, and it is worth stating as a rule: **any candidate
sharing a family with a hull already in the fleet must be valued at zero TP**, and a search that
forgets it will keep proposing the same bad swap.

## Armour sweep: the swap inverts, and it bites the corvettes harder

Chris: *"the Ranger is kind of a small ship killer, so losing the alpha of the CAS might mean it does
worse vs high armour… this might bite the corvettes too."* Both correct. Ballistic damage is
`floor(max(atk − armour, 10% of table damage))`, so a hull firing many small shots loses a far larger
share to armour than one firing few big ones, and BV/CP was computed against a single enemy template.

### The 066 → Ranger swap

DPM against a cruiser, at the TP each holds:

| hull | CP | arm 0 | 40 | **80** | 120 | 200 | 240 |
|---|---|---|---|---|---|---|---|
| 066 Bombardment | 18 | 13,177 | 11,518 | 11,235 | 10,953 | 10,388 | 10,106 |
| Ranger Composite | 16 | **13,759** | 10,115 | 6,941 | 5,637 | 3,822 | 3,056 |
| **net fleet DPM, −2× 066 +3× Ranger** | | **+14,922** | **+7,310** | **−1,647** | **−4,995** | **−9,312** | **−11,044** |

**The swap crosses over at roughly armour 65–70.** The 066 loses only 23% of its damage from armour 0
to 240; the Ranger loses **78%**. The +5.26% the search found is real on the product metric — the
Ranger brings enough hull to make up for it — but it is **bought against soft targets and it reverses
against hard ones**. The pirate cruisers in the large team sit at armour 80, i.e. right at the
crossover, so this swap is a coin-flip against the enemy it was scored on and a clear loss against
anything tougher.

**Verdict: keep the 4× 066 Bombardment unless the content is known-soft.** The 12 stranded CP is
cheaper than the alpha.

### And the corvettes flip harder

| corvette | arm 0 | 40 | **80** | 120 | 200 | 240 |
|---|---|---|---|---|---|---|
| Hive | 5,243 | 4,204 | 3,504 | 3,021 | 2,055 | 1,572 |
| **Nebula Pulse** | 3,172 | **3,172** | **3,172** | **3,172** | **3,172** | **3,172** |
| **T800** | 2,478 | **2,478** | **2,478** | **2,478** | **2,478** | **2,478** |
| RB7 | 2,907 | 2,451 | 1,995 | 1,539 | 627 | **251** |
| Wraith | 4,009 | 2,540 | 1,310 | 372 | 372 | **372** |

**The Nebula Pulse and the T800 are completely flat** — energy weapons, which the armour term does not
touch at all. Everything else falls off a cliff: the **RB7 loses 91%** and the **Wraith 91%, flooring
out by armour 120**.

Ranked per unit, the order inverts:

| at armour… | best four |
|---|---|
| 0 | Hive, Nebula A, Wraith, T800 |
| 80 | Hive, **T800**, **Nebula Pulse**, RB7 |
| 200 | **T800**, **Nebula Pulse**, Hive, RB7 |

So the Whale fill — 10 Hive, 15 T800, 5 Nebula Pulse — holds up well by luck, since the T800 is
armour-immune. But **the Jaeger wings do not**: 8 RB7 and 8 Wraith are the two worst corvettes against
armour, and at 200 they are doing 627 and 372 against the Nebula Pulse's 3,172.

**The 1 spare Nebula Pulse should be in a Jaeger before any Wraith is**, and against hard targets the
right Jaeger wings are Nebula Pulse and T800, not RB7 and Wraith — which means trading seats with the
Whales rather than taking what they left.

### The lesson for every figure above

Every BV and BV/CP number in this file is computed against **one** enemy template. Where two hulls
differ in shot size — a few big hits against many small ones — their ranking is a function of target
armour and can invert inside the range that actually occurs. The flat-DPM energy hulls (Nebula Pulse,
T800, Io A) are the ones whose ranking is stable.

## Correction: curving only against a cruiser was unfair to the corvettes

The sweep above ran the corvettes against **a cruiser out to armour 240**, which is battleship armour
and not a target a corvette meets. Per target class, at the armour each class actually carries:

| corvette | FF (arm 20) | DD (arm 30) | CA (arm 80) | BC (arm 120) |
|---|---|---|---|---|
| **Hive** | 3,321 | **3,562** | **3,504** | 3,194 |
| **Nebula Pulse** | 2,838 | 2,838 | 3,172 | **3,339** |
| **Wraith** | **2,930** | 2,601 | 1,310 | 392 |
| RB7 | 2,397 | 2,295 | 1,995 | 1,620 |
| T800 | 2,217 | 2,217 | 2,478 | 2,609 |

**Chris on both, and both hold:**

- *"the Wraith is an anti-FF/DD ship"* — 2,930 and 2,601 against frigates and destroyers, collapsing
  to 1,310 and 392 against cruisers and battlecruisers. It is a specialist, and judging it on a
  cruiser curve was judging it at the wrong job. Its kit says the same thing: +20 evasion vs missiles,
  **+30 vs torpedoes**, +35 flat evasion — built to survive the small-hull weapons that frigates and
  destroyers carry.
- *"the RB7 has unique abilities vs CA, of all things, so it isn't so bad"* — right, and my "loses
  91%" was an artefact of sweeping to armour 240. Across the classes it is the **flattest ballistic
  corvette on the account**: 2,397 → 1,620 from frigate to battlecruiser, where the Wraith goes
  2,930 → 392. Against a cruiser at 80 it still does 1,995. Its priority row also carries a **95% hit
  rate against cruisers** (class 500), the highest in its table, against rank-1 priority on frigates
  and destroyers — so it shoots small things first but hits big things hard when it does.

So the corvette picks are **role picks, not a ranking**: Hive and Nebula Pulse are the generalists,
the T800 is armour-proof filler, the Wraith is for small-hull content and the RB7 for mixed.

## The builds agree

Chris: *"the fleets you came up with are close to my builds. I did not try to squeeze 1 Ceres into the
fleet to absorb all the fighters, and I used Taurus instead of the Guardians, and I don't think I was
using the Q."*

Three differences, and the model's case for each:

| | model | Chris's build |
|---|---|---|
| **Quaoar Railgun** | 10×, BV/CP **1,765**, the best hull in the fleet | not used |
| **Guardian Pulse** | 10×, 1,168 | Taurus instead |
| **1× Ceres + 2 Follower** | 8 CP, 1,362 | not used |

The Quaoar is the one that matters — it is worth 38 DD points and **+19% fleet strength**, and it was
absent from the composition until those points were spent. The Ceres is 8 CP for a package above the
fleet's own cutoff. The Taurus-versus-Guardian call is close enough to be taste: Taurus Pulse is 1,074
against Guardian Pulse's 1,168, within 9%.

And on armour, Chris's own framing settles the 066 question: *"it isn't bad making extra CAS066 to
substitute when going up against higher armour — the small fleet is pretty anti-armour by design."*
So the 066s are a **swap-in against hard targets** rather than a permanent fixture, and the Ranger swap
is the soft-target configuration.

# Cnc04Cavalry

Same treatment, and the account behaves completely differently — Chris: *"this one is short on hulls."*
Built with `lagrange-combat/tools/fleet_plan.py`, which now does the whole pass in one go.

## Reinforcements swallow every good craft

It owns **both** capital CVs, so the ten free slots are 5× Solar Whale and 5× CV3000:

| | ships | CP (free) | carries |
|---|---|---|---|
| Solar Whale | 5 | 275 | 30 corvettes |
| CV3000 | 5 | 200 | **25 fighters + 15 corvettes** |
| | | **475 CP** | **25F + 45C** |

Seventy craft seats, and the account's best craft fill them **exactly**: 10 Follower, 8 Hayredin's
Loyal, 7 Stingray for the fighters; 15 T800, 10 S Levi 9, 10 RB7, 10 Wraith for the corvettes.

**So no carrier package appears in either fleet** — there is nothing left to put in a Jaeger or a
Predator. That is the exact opposite of DelA5Hades, where the reinforcements took 30 corvettes and the
CA fleet became half carriers. The difference is the CV3000: it carries fighters where the Whale does
not, and five of them absorb every fighter worth flying.

## CA fleet — 388 of 400 CP, strength 2.67e11

| | CP | BV/CP |
|---|---|---|
| 8× Io A | 144 | **1,481** |
| 8× Chimera A | 144 | 1,239 |
| 5× Light Cone Composite A | 100 | 1,086 |

## FF/DD fleet — 400 of 400 CP, strength 2.19e11

| | CP | BV/CP |
|---|---|---|
| 10× Quaoar Railgun | 60 | **1,706** |
| 10× Taurus Defense | 80 | 1,363 |
| 10× Winged Hussar A | 60 | 1,115 |
| 10× Mare Serenitatis A | 50 | 971 |
| 10× Taurus Assault | 110 | 832 **(0 TP — Defense holds the family pool)** |
| 5× XenoStinger Tactical | 40 | 824 |

## Where "short on hulls" actually bites: the CA fleet

**12 CA hulls against 31 FF/DD hulls**, and the CA list falls off a cliff after the top five:

| CA hull | CP | BV/CP |
|---|---|---|
| Io A | 18 | 1,481 |
| Chimera A | 18 | 1,239 |
| Light Cone Composite A | 20 | 1,086 |
| Conamara Chaos Railgun | 16 | 1,074 |
| Ranger Composite | 16 | 1,044 |
| **066 General** | 18 | **893** |
| KCPV-A | 16 | 690 |

Only three types make the fleet, 12 CP strands again, and the sixth-best CA is already 40% below the
first. On DelA5Hades the equivalent fleet had seven entries including five carrier packages.

## And the CA fleet is badly armour-exposed

DPM against a cruiser as its armour rises:

| hull | arm 0 | 80 | 160 | **240** | loss |
|---|---|---|---|---|---|
| **Io A** | 25,099 | 21,136 | 20,844 | **20,844** | **−17%** |
| Chimera A | 12,350 | 8,080 | 5,375 | 2,670 | −78% |
| Light Cone Composite A | 17,032 | 10,953 | 6,633 | 2,313 | −86% |
| Ranger Composite | 11,569 | 5,223 | 3,535 | 2,350 | −80% |

**Only the Io A holds**, because it is energy and the armour term does not touch it. The other three
lose 78–86%, so against hard targets this fleet is **eight Io A and some hulls**. That is a much
sharper exposure than DelA5Hades, whose CA fleet kept the 066 Bombardment at −23%.

The practical conclusion for this account: **the 066 General is the armour answer it already owns**
(limit 12, pool 4) even at 893 BV/CP, exactly as Chris described building extra 066s to substitute.
Here it is not a refinement, it is the only ballistic alternative with a flat profile.

## The Taurus pool costs more here than anywhere

Taurus Defense holds the family's 47 points at **1,363**; Taurus Assault is fielded alongside it at
**832 instead of 1,145** — the sibling penalty is 27% of that hull's value across ten ships, and it is
the fifth entry in a six-entry fleet. On an account this short of hulls there is no third Taurus-tier
option to replace it with, so the penalty simply has to be paid.

## Chris was right about the Xeno, and it exposed a flaw in the builder

*"Surprised the Taurus Assault got in. I would think 10× Xeno would be better."*

Checked, and it is — **+1.60%** on Cnc04Cavalry's FF/DD fleet, for 4 CP less:

| | CP | strength |
|---|---|---|
| as built: 10× Taurus Assault + 5× Xeno | 400 | 2.193e11 |
| **10× Xeno + 6× Taurus Assault** | **396** | **2.228e11** |
| 10× Xeno + 6× Taurus Pulse | 396 | 2.193e11 |
| 10× Xeno + 10× Ruby Railgun | 380 | 2.087e11 |

The builder had been ranking hulls by **standalone BV/CP** — Taurus Assault 832 against the Xeno's
824 — which is the wrong comparison. The fleet is scored on `sqrt(D × H)`, so a hull's worth depends
on the D and H **already in the fleet**. The marginal value of one more ship is `d/D + h/H`:

| hull | CP | d/D | h/H | sum | **per CP** |
|---|---|---|---|---|---|
| **XenoStinger Tactical** | 8 | 0.0295 | 0.0067 | 0.0362 | **0.00453** |
| Taurus Pulse | 11 | 0.0220 | 0.0247 | 0.0468 | 0.00425 |
| Taurus Assault | 11 | 0.0159 | 0.0241 | 0.0399 | 0.00363 |

The fleet runs **1 DPM : 12.6 HP**; the Xeno is 1 : 2.9 and the Taurus Assault 1 : 19.1. So the Xeno
is the DPM the fleet is short of, and it is worth 25% more per CP at the margin than its standalone
number says.

`fleet_plan.py` now scores **marginally** — the gain in `sqrt((D+d)(H+h))` per CP, re-priced at every
pick — while still printing BV/CP, which is the number read off a hull. Results across both accounts:

| fleet | standalone BV/CP | **marginal** | |
|---|---|---|---|
| Cnc04 CA | 2.67e11 (388 CP) | **2.82e11 (400 CP)** | **+5.6%** |
| Cnc04 FF/DD | 2.19e11 | **2.29e11** | **+4.6%** |
| DelA5Hades CA | 3.48e11 | **3.53e11** | +1.4% |
| DelA5Hades FF/DD | 2.61e11 | 2.61e11 | — |

### The revised fleets

**Cnc04 CA** — 400 CP, 2.82e11: 8× Io A, 8× Chimera A, **6× Ranger Composite**, 1× Conamara Chaos
Railgun. The stranded 12 CP is gone.

**Cnc04 FF/DD** — 400 CP, 2.29e11: 10× Quaoar Railgun, 10× Taurus Defense, 10× Winged Hussar A,
10× Mare Serenitatis A, **10× XenoStinger Tactical**, 1× Taurus Assault, 7× Ceres + 2 AT021 Pulse,
1× FG300. Chris's composition, reached from the gradient.

**DelA5Hades** is unchanged, because its fleets were already balanced enough that the two rankings
agree. Its roster now records the **38 DD points spent on the Quaoar** (`data/ships/dela5hades.csv`),
so the 1,765 BV/CP is the account's real state rather than a hypothetical.

### Why this kept happening

Three times now a composition has been wrong for the same reason: **a per-ship number cannot see the
fleet.** Standalone BV/CP ignores the fleet's DPM/HP balance; the family-pool rule ignores what the
rest of the fleet already holds; the single-enemy score ignores target armour. The gradient fixes the
first, the claim table the second, and the armour sweep is the check for the third.

## The Mizar — a TP sink that pays, **if it is permanent**

`-TE` means **temporary**, not a duplicate (Chris, 2026-10-12). That is a correction to how these
tools read the tables — every `-TE` row was being filtered as a copy — and it also means the earlier
Alkaid evaluation was of the right hull after all.

The Mizar (开阳) is a **12 CP destroyer** and the tables hold three rows: **42001** and **42002**, the
permanent A and B, and **49601**, the temporary one.

| | CP | HP | armour | edef | weapon | DPM |
|---|---|---|---|---|---|---|
| Mizar A | 12 | **46,930** | **45** | 3 | one 450 torpedo | 1,834 |
| Mizar B | 12 | 42,600 | **45** | 3 | one **550** torpedo | 2,034 |

Armour 45 on a destroyer is very high — the Taurus Assault has 30, the Quaoar Railgun 20 — and the
weapon is `WEAPON_TYPE` 6, a torpedo, so it is a projectile a screen cannot block.

### At zero points it does not make the fleet; maxed it is second best

Marginal value in Cnc04Cavalry's FF/DD fleet (which runs 1 DPM : 10.2 HP):

| hull | CP | BV/CP | marginal per CP |
|---|---|---|---|
| **Mizar B, maxed (114 TP)** | 12 | **1,397** | **0.00662** |
| XenoStinger Tactical | 8 | 824 | 0.00470 |
| Taurus Assault (0 TP) | 11 | 832 | 0.00412 |
| **Mizar A, 0 TP** | 12 | 773 | 0.00403 |
| **Mizar B, 0 TP** | 12 | 776 | 0.00389 |

**Untouched it is below the fleet's cutoff** — 0.00389 against the Xeno's 0.00470 — because it is even
more hit-point-heavy than a fleet that is already HP-rich. **Maxed it is 41% above the Xeno** and
second only to the Quaoar Railgun, at 1,397 BV/CP.

So it is the sharpest TP sink on either account: **a 114-point ladder that takes it from unplayable to
the number two hull.** Its armour profile is mid — 4,290 → 2,418 DPM from armour 0 to 240, a 44% loss,
better than the Quaoar's 66% but nothing like the flat Xeno or Taurus Assault.

### The decision rests entirely on whether this one is temporary

**If the bonus Mizar is the `-TE` temporary hull, do not put a point into it.** 114 TP is more than
the entire unspent DD pool on DelA5Hades, and it would expire with the hull. If it is the permanent
42001/42002, it is the best destroyer-class target either account has.

Worth checking which it is before anything else, because the two answers are opposite.

### Does the free +20 TP change it? Almost, but no

Chris: *"they are giving tryouts of these types of ships, so I am not putting real TP into anything."*
Right call, and the numbers say the tryout TP is deliberately just short.

Marginal value per CP in Cnc04Cavalry's FF/DD fleet, against the XenoStinger cutoff of **0.00470**:

| | 0 TP | **+20 (the tryout)** | 40 TP | maxed, 114 |
|---|---|---|---|---|
| Mizar A | 0.00403 | **0.00458** | 0.00484 | 0.00666 |
| Mizar B | 0.00389 | **0.00433** | 0.00476 | 0.00662 |
| | below | **just below** | **in fleet** | second-best hull |

**+20 TP lands it at 0.00458 against a 0.00470 cutoff** — a near miss. It crosses at **40**.

And the free points are spent on the wrong axis. The first 20 buy **evasion at 1 TP, evasion vs weapon
type at 3, HP at 5**, with the first damage-side upgrade (hit vs type) not arriving until 12. The Mizar
is already 1 DPM : 21 HP in a fleet running 1 : 10.2 — **more hit points is the one thing it does not
need**, and that is exactly what the cheap end of its ladder sells.

So the tryout shows you the hull and stops one rung short of making it fieldable, which is a
reasonable thing for a trial to do. **Try it, do not invest**: 20 more points would get it in, but on
a temporary hull those are 20 points that leave with it.

## Roster separation, checked

The two rosters are built independently from each account's own blueprint list, and the CA lists
differ exactly as Chris describes:

| | DelA5Hades | Cnc04Cavalry |
|---|---|---|
| **066 family** | **A → 066 General, B → 066 Bombardment** | **A → 066 General only** |
| Chimera | — | **A (50601)** |
| Conamara | — | **Chaos Railgun (51201)** |
| Light Cone | — | Composite A (50501) |
| Predator | A only | **A, B and C** (Carrier, Tactical, AA) |
| KCCP | A, B, C, D | A and D only |
| Io / Ranger / Jaeger | both | both |

**Cnc04 has no 066 Bombardment**, which is why its armour answer is the **General at 893 BV/CP** while
DelA5Hades gets the **Bombardment at 1,153**. The fleets above use the right one in each case — the
Bombardment appears only in DelA5Hades' CA fleet, and the cnc04 recommendation names the General.

Chris's two details also **confirm the variant-letter mapping from the other direction**: cnc04's
blueprint list carries "Conamara" with no letter, which `bp_roster.py` resolves to the family's base
hull 51201 — and Chris says it is the Conamara **Rail**, which 51201 is. Same for the Chimera at A.
That is the ship-id-order rule holding on two families it was not derived from.

One caveat worth stating: **the letter mapping is an inference**, that A/B/C/D follow ship-id order.
It is now confirmed on the Taurus, the Conamara, the Chimera and the NOMA/M470, but if any family's
in-game letters are ordered differently then that family's row is wrong. The 066 is the one that would
matter most here, since A and B are 893 and 1,153 — worth a glance at whether DelA5Hades' "CAS066 B"
really is the Bombardment.
