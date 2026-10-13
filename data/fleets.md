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

## The headline: build limits bind, not CP

Five of the seven hulls in DelA5Hades' FF/DD fleet are **at their build limit**, and the fleet still
has CP to spare it cannot use. So "what should I build" has a blunt answer on these accounts: **build
the cap of the good hulls**, because you will run out of permitted hulls before you run out of CP.

## DelA5Hades

**FF/DD, 400 CP** — 60 ships, 139,864 DPM, 1,666,400 HP, **18.2×** the 98 CP team's strength

| hull | n | CP | DPM | HP | pool |
|---|---|---|---|---|---|
| Eris Heavy Cannon | 10 *(limit)* | 90 | 36,575 | 323,720 | 68 |
| Guardian Pulse | 10 *(limit)* | 90 | 34,725 | 318,060 | 46 |
| Eris Armor | 10 *(limit)* | 70 | 11,773 | 467,360 | 68 |
| Winged Hussar A | 10 *(limit)* | 60 | 18,705 | 274,790 | 57 |
| Reliat Energy | 10 *(limit)* | 40 | 20,000 | 117,940 | 47 |
| Mare Serenitatis A | 8 | 40 | 15,062 | 124,552 | 47 |
| Ruby Railgun | 2 | 10 | 3,021 | 39,978 | 48 |

**CA, 400 CP** — 23 ships, 169,121 DPM, 1,648,537 HP, **21.8×**

| hull | n | CP | DPM | HP | pool |
|---|---|---|---|---|---|
| Io A | 8 *(limit)* | 144 | 94,422 | 536,720 | 30 |
| Ranger Composite | 8 *(limit)* | 128 | 30,623 | 632,968 | 30 |
| 066 Bombardment | 7 | 126 | 44,075 | 478,849 | 30 |

## Cnc04Cavalry

**FF/DD, 400 CP** — 52 ships, 151,495 DPM, 1,670,030 HP, **19.8×**

| hull | n | CP | DPM | HP | pool |
|---|---|---|---|---|---|
| Taurus Assault | 10 *(limit)* | 110 | 33,565 | 472,350 | 47 |
| Taurus Defense | 10 *(limit)* | 80 | 23,952 | 496,370 | 47 |
| XenoStinger Tactical | 10 *(limit)* | 80 | 38,926 | 111,620 | 30 |
| Quaoar Railgun | 10 *(limit)* | 60 | 34,305 | 305,400 | 33 |
| Winged Hussar A | 10 *(limit)* | 60 | 17,598 | 254,350 | 42 |
| Mare Serenitatis A | 2 | 10 | 3,146 | 29,940 | 26 |

**CA, 400 CP** — 23 ships, 149,760 DPM, 1,883,982 HP, **22.0×**

| hull | n | CP | DPM | HP | pool |
|---|---|---|---|---|---|
| Io A | 8 *(limit)* | 144 | 84,739 | 536,720 | 14 |
| Chimera A | 8 *(limit)* | 144 | 39,750 | 800,936 | 15 |
| Ranger Composite | 6 | 96 | 21,146 | 474,726 | 23 |
| Conamara Chaos Railgun | 1 | 16 | 4,124 | 71,600 | 0 |

## The craft: not the battlecruisers

Chris expected the CV and BC to carry the reinforcements. **The battlecruisers barely carry anything** —
Constantine is 1 fighter at best and 0 stock, ST59 2 and 0 stock, Spear of Uranus and Antontas 3
corvettes and 0 stock. The cheap destroyer and cruiser carriers do the whole job:

| carrier | class | CP | stock | accepts |
|---|---|---|---|---|
| **Ceres Carrier** | DD | **8** | 2 fighters | size ≤ 2 |
| AC721 Amphibious | DD | 12 | 2 corvettes | — |
| **Predator Carrier** | CA | **18** | **4 fighters** | size ≤ 2 |
| KCCPV2.0 Carrier | CA | 16 | 2 fighters | **size ≤ 3** |
| Jaeger Carrier | CA | 20 | 4 corvettes | — |
| CV3000 *(Cnc04 only)* | CV | 40 | 5 fighters + 3 corvettes | size ≤ 3 |

What 5+ craft costs the line, as a share of fleet strength:

| fleet | pick | CP | carries | line cost |
|---|---|---|---|---|
| DelA5Hades FF/DD | **3× Ceres Carrier** | 24 | 6 fighters | −2.8% |
| DelA5Hades CA | **2× Predator Carrier** | 36 | 8 fighters | −3.0% |
| Cnc04 FF/DD | **3× Ceres Carrier** | 24 | 6 fighters | −2.3% |
| Cnc04 CA | **2× Predator Carrier** | 36 | 8 fighters | −5.7% |
| Cnc04 CA | 1× CV3000 | 40 | 5F + 3C | −1.7% |

Those percentages are the **carrier hull** being weaker per CP than the line hull it displaces, and
they do **not** count what the craft themselves contribute — the craft are carried, not line ships, so
they are outside the index. The true cost is lower than shown and probably negative.

**Size ≤ 2 is enough.** The best fighters on both accounts are size 2 — Follower and Hayredin's Loyal,
both around 250–300 now and ~400 maxed — so there is no reason to pay for a size-3 bay. That settles
the Cnc04 CA choice for the Predators over the CV3000 on craft count, 8 against 5.

| | best fighters | size | now | maxed | pool |
|---|---|---|---|---|---|
| DelA5Hades | Follower | 2 | 253.9 | 395.2 | **0** |
| | Hayredin's Loyal | 2 | 246.0 | 400.9 | **0** |
| Cnc04Cavalry | Hayredin's Loyal | 2 | 298.5 | 400.9 | 33 |
| | Follower | 2 | 253.9 | 395.2 | **0** |

**Both accounts' two best fighters have empty or near-empty pools** against 81 and 108 point ladders.
That is the clearest craft-TP opportunity on either account.

## Caveats

- Scored against the **large** team. These accounts will meet the small one more often, and
  `data/tp.md` shows that reverses rankings for cheap high-evasion hulls — rerun with `--vs small`
  before committing to a build if the fleet is for low-tier content.
- Whether a fleet has a **ship-count cap** is still unknown, and the FF/DD fleets run 52–60 hulls.
  If a cap exists these compositions break and the answer shifts toward fewer, bigger ships.
- The craft are not in the strength index at all, so a fleet's real value with 6–8 fighters aboard is
  higher than the numbers here.
