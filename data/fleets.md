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
