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
