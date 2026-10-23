# Tech-point upgrades: what they actually buy

> **Scope: the speed findings here are EVENT-ONLY.** Chris, 2026-10-09: fleet speed is the mean of
> every ship's cruise *in this trading event*, which ends in under a week. **In the normal game a
> fleet travels at its slowest hull**, as physics would have it, and speed does not affect combat at
> all. So everything that follows about cruise upgrades, speed ballast and fleet mean speed is a
> temporary exploit of this event's rules, not general advice. In the normal game a cruise upgrade is
> worth having but cannot be laundered into damage, and adding a fast cheap frigate to a slow fleet
> does nothing.


Read from `Tb_cfg_ship_system` / `Tb_cfg_system_enhance` / `Tb_cfg_system_effect` in the client tables
(`lagrange-combat/tools/maxout.py`, `dpm_curve.py`). Every figure below is computed from config, not
from a battle report, except where an anchor is named.

## 1. Warp speed is a +30% cap, and it is NOT the same stat as curvature

Four prefixes sit in a hull's propulsion system and all four read "+15% speed" in the UI, but they are
two different effects:

| prefix | effect id | effect | what moves |
|---|---|---|---|
| 2101, 2105 | 1 | `EFFECT_SPEED` | **warp / cruise** — the stat trade travel time uses |
| 2102, 2104 | 2 | `EFFECT_CURVATURE_SPEED` | the jump stat |
| 2103 | 1 + 2 | both, at +7% | |
| 2106 | 10001 | `EFFECT_BATTLE_SHIP_SPEED_INC` +75% | in-combat movement only |

**Anchors, and they separate the two stats cleanly:**

- The Io A reads **650 → 845** in game: its `SPEED` stat, +30%, exactly two `EFFECT_SPEED` rows.
- Chris's maxed Quaoar Railgun, 2026-10-10, shows **both numbers at once** — speed **850 → 1105**
  (×1.3000, two `EFFECT_SPEED` rows) and warp **4,250 → 4,887** (×1.1499, **one**
  `EFFECT_CURVATURE_SPEED` row). Its propulsion limit is 3, and 2 + 1 = 3. Every digit fits.

So the in-game **"speed" figure is the `SPEED` stat that `EFFECT_SPEED` raises, and the separate
"warp" figure is the curvature stat** — they are only equal (warp = 5 × speed) on a stock hull, and an
upgrade splits them. +30% is the ceiling on `SPEED`; there is no third row to buy. Trade travel
follows `SPEED`, which the Io stopwatch test established independently.

An earlier version of this file called the `EFFECT_SPEED` gain a "warp" gain and tabulated the Quaoar
as 4,250 → 5,525. That was the two stats conflated: the hull's *speed* goes 850 → 1,105 and its
*displayed warp* only 4,250 → 4,887, because the three propulsion slots cannot hold two of each.

The propulsion system has an `ENHANCEMENTS_LIMIT`, so the two stats compete for the same slots, and a
hull that lists only ONE `EFFECT_SPEED` row is hard-capped at +15% however much TP you throw at it.

### What each hull can reach

Reachable `EFFECT_SPEED` gain (the *speed* stat, not the displayed warp):

| reachable | TP | hulls |
|---|---|---|
| +30% | **6** | 37 — every 16–20 CP cruiser and carrier: Io A/B/Siege, Callisto A/Heavy/Drone, Chimera A/B/Defense, Conamara Railgun/Plasma, Light Cone Attack C / Composite A / Area AA, 066 (all four), KCPV (all four), Jaeger Cannon/Carrier, Predator, Alioth, Arctos, Cretaceous, Ranger |
| +30% | 12 | 79 — destroyers and the rest: Quaoar Railgun/Torpedo, Eris (all), AC721 (all), Taurus Pulse, Constantine, Marshal Crux, FG300 Armored |
| **+15% only** | 6 | 40 — the cheap screen: FG300 Multipurpose/Recon/SP, **Carilion (all three)**, Reliat A/Energy, Trader Transport/Support, Mare Tranquillitatis/Serenitatis/Imbrium, Ruby, Rager, Zircon, XT 8, NOMA 330, Holy Spirit |
| +22% | 16 | Reliat Stealth |
| +45% | 24 | one hull |

**Consequence for fleet speed (EVENT ONLY — the normal game uses the slowest hull).** In this event
fleet speed is the *mean* of every ship's cruise, not the slowest
(measured, see README), so a warp upgrade lifts the fleet only by its share — which means warp TP pays
off when bought **fleet-wide**, and then +30% warp is +30% credits/hr. The counter-intuitive part: the
**cruisers are the cheap speed buys (6 TP) and the cheap frigates are the ones that cannot go past
+15%**. A 10-ship Io fleet buys its full +30% for 60 TP. A 10-ship Carilion/Reliat screen can only
ever reach +15%, at the same 60 TP, and it drags the mean down for whatever it escorts.

## 2. Engines before weapons, by a factor of 10–20

Full weapon max is 106–150 TP per hull for a 1.4–3.6× DPM gain. Warp max is 6–12 TP per hull for +30%
credits/hr. Both come out of the same TP pool but they sit in *different systems*, so they do not
compete for slots — only for order. Buy warp on every ship in a trade fleet first, then weapons on the
escorts only.

## 3. Q-torp vs Q-rail — the A/B

Both 6 CP, 8,500 cargo, 4,250 warp, row 1, limit 10, both +30% warp for 12 TP. Effective DPM against a
target at the armour shown, stock vs fully maxed:

| vs (armour) | Railgun stock | Railgun maxed | Torpedo stock | Torpedo maxed | winner |
|---|---|---|---|---|---|
| FF (20) | 3,098 | **11,262** (3.64×) | 3,552 | 9,210 (2.59×) | railgun +22% |
| DD (30) | 2,835 | **10,764** (3.80×) | 3,263 | 8,705 (2.67×) | railgun +24% |
| CA (80) | 2,216 | 7,858 (3.55×) | 2,561 | **8,366** (3.27×) | torpedo +6% |
| BC (120) | 1,991 | 7,221 (3.63×) | 2,206 | **7,461** (3.38×) | torpedo +3% |
| BB (200) | 1,541 | **5,946** (3.86×) | 1,494 | 5,650 (3.78×) | railgun +5% |

Weapon max: railgun 106 TP, torpedo 116 TP. Both land near 1,200 DPM/CP against the 98 CP pirate BC
fleet, which is the top of the destroyer class.

**Where each one's TP goes.** The railgun's weapon module holds a third cooldown row — prefix 115
"full firepower", CD −40% / hit −15% — so it stacks to **−70% cooldown** (115 + 301 + 302) and takes
its gain as rate of fire. The torpedo has only −30% (305 + 306) and takes its gain as **crit**: its
module already crits 15% / +170% at stock, and prefixes 161 (`EFFECT_BURST_DAMAGE` 30050) and 163
(`EFFECT_BURST_DAMAGE_INC` 40) buy more of it.

Not in the DPM figures, and both favour the torpedo:
- torpedoes are `SPECIAL_TARGET_LOGIC` 0 — unblockable by a front row, and they hunt the rear
- prefix 213 is `EFFECT_INTERCEPT_DEC` 30, which cuts the defender's torpedo interception

So: **railgun for a screen-killer, torpedo for the pirate BC fleets**, and the torpedo is the better
pick on a route that gets attacked, by more than the 3% the table shows.

### Two unverified combination rules behind those numbers

`EFFECT_BURST_DAMAGE` from a *system upgrade* onto a weapon that *already* crits, and
`EFFECT_BURST_DAMAGE_INC`, are both taken as **additive** — the engine-wide convention Chris verified
for damage and cooldown. Additive is the only reading that is not absurd (replacement would make the
Q Torpedo's 10 TP prefix 161 a *downgrade*: 30%/+50% is E[×]=0.15 against the module's native
15%/+170% at E[×]=0.255), but it has not been measured. A battle report from a crit-upgraded torpedo
boat would settle it. `EFFECT_INTERCEPT_DEC` is read from config but **not applied** — relative vs
absolute differ by ~10× at the 3–5% interception values that exist.

## 4. How wild the Io gets (and the Carilion does not)

| hull | CP | wpn TP | BC dpm stock | maxed | ×  | maxed/CP | armour | HP |
|---|---|---|---|---|---|---|---|---|
| Io A | 18 | 122 | 20,844 | **35,735** | 1.71× | **1,985** | 50 → 80 | 62k → 78k |
| Io B | 18 | 142 | 20,437 | 27,693 | 1.36× | 1,539 | 50 → 80 | 62k → 85k |
| Io Siege | 18 | 122 | 17,376 | 27,983 | 1.61× | 1,555 | 50 → 80 | 62k → 78k |
| Conamara Plasma | 20 | 132 | 21,027 | 38,002 | 1.81× | 1,900 | | |
| Constantine | 35 | 269 | 24,139 | 42,300 | 1.75× | 1,209 | | |
| Carilion Heavy Cannon | 5 | 135 | 1,165 | 2,350 | 2.02× | 470 | 5 → 8 | 10k → 14k |
| Carilion Recon | 4 | 117 | 122 | 192 | 1.57× | 48 | 5 → 8 | 8k → 10k |
| Carilion Special | 5 | 125 | 123 | 149 | 1.22× | 30 | 5 → 8 | 10k → 12k |

**Io A is the headline hull of the account** — 1,985 DPM/CP against a battlecruiser, flat across
CA/BC/BB because its guns are energy and so armour-insensitive, with armour 50 → 80 and 78k HP, for
122 TP. Nothing else in the roster is close per CP at that HP. Io B trades 1.71× for 1.36× (it is the
anti-screen variant: it beats Io A vs FF/DD and loses vs everything heavier).

**The Carilion is not a damage hull and maxing it does not change that** — 192 DPM against anything
above a destroyer, and it is one of the 40 hulls hard-capped at +15% warp. It is a screen and an
evasion body (35 → 43% evasion on the Recon, 55% on the Special) and should be costed as HP, not DPM.

## 5. Engine-model corrections this came from

Two bugs in `lagrange-combat/tools/`, both of which understated torpedo and missile hulls:

1. `matrix.system_mods` had no case for `EFFECT_BURST_DAMAGE` / `_INC` / `EFFECT_INTERCEPT_DEC`, so a
   crit-granting upgrade read as "does nothing". Fixed; the burst override now rides on the mount
   (`matrix.mount_burst`) and `dpm_curve` reads it.
2. `maxout.score` therefore priced crit at zero, so the Q Torpedo spent 2 of its 7 weapon slots on an
   early-warning row and a bare `BURST_DAMAGE_INC` and read **1.88×** maxed against the railgun's
   3.45×. `score` now prices crit **marginally** against the module's native crit
   (`maxout.native_burst`), which is what puts the two variants within a few percent of each other
   where they belong.

## 6. The Carilion Special tank, and why battle time beats it in this event

Chris: *"it's not about DPS with the Carilion — you max out the Special and put healers with it and they
can tank forever. It dumps a lot of points into defense, but you can't be hurt. OTOH time is $$ in this
variant, so 30 minute battles are also costly."*

Both halves check out, and the second one wins.

### The tank is real: two systems no other Carilion has

The Special carries **two dedicated evasion systems** (groups 6 and 7, limit 2 each) that the Recon and
the Heavy Cannon do not. They buy `EFFECT_AVOID_INC_BY_WEAPON_TYPE`, whose param is `TPPP` — the lead
digit is the **attacker's** `WEAPON_TYPE`, not a ship class:

| prefix | group | TP | buys |
|---|---|---|---|
| 4104 | 6 | 6 | +25 vs ion (3) and railgun (2) |
| 4203 | 6 | 6 | +15 vs artillery (1), pulse (4), ion (3) |
| 4201 | 7 | 8 | +20 vs missile (5) and torpedo (6) |
| 4202 | 7 | 8 | +15 vs artillery (1), pulse (4), ion (3) |

Weapon types: 1 artillery (`WEAPON_TYPE` blank, the 207-module default), 2 railgun, 3 ion, 4 pulse,
5 missile, 6 torpedo — corroborated by `intercept_pct`'s already-verified 5/6 and by which hulls mount
each type. Both groups fill completely (4 rows, 28 TP) and nothing is given up, because evasion lives in
its own systems and competes with nothing else.

Full defence build — those 4 rows, plus +HP/+HP/energy-resistance in group 3 and its +15% warp — is
**68 TP**, against 125 TP for maxout's combat build, and gives HP 9,770 → 11,724, energy def 0 → 10%:

| incoming | evasion | hit chance |
|---|---|---|
| ion | 55% → **110%** | **unhittable** |
| artillery | 55% → 85% | ×0.33 |
| pulse | 55% → 85% | ×0.33 |
| railgun | 55% → 80% | ×0.44 |
| missile | 55% → 75% | ×0.56 |
| torpedo | 55% → 75% | ×0.56 |

### But the pirates don't fire ion, so it halves the damage, it doesn't null it

The Special's single biggest bonus is +55 against ion — and **neither pirate template fires ion.** Ion
is a *player* weapon (Io, Constantine, Marshal Crux, Ruby Ion), so the unhittable build is a PvP build.
Incoming DPM on one Carilion Special, stock vs defence-maxed:

| team | | stock | tank | |
|---|---|---|---|---|
| 1010801 (98 CP) | railgun 49%, missile 41%, artillery 10% | 16,927 | 8,113 | ×0.48 |
| 1010501 (30 CP) | torpedo 61%, artillery 23%, missile 16% | 9,820 | 4,952 | ×0.50 |

Time to kill one 5 CP Carilion Special goes from **35 s to 87 s** against the big team. Long, not
infinite. (Whether evasion is capped at all is **UNMEASURED** — 110% computes to literally unhittable,
and the engine now clamps the hit chance at zero rather than going negative. If the game caps evasion
the ion row is worth less than it looks; nothing else in the table changes.)

### Time is the real cost, and it is the bigger number

ArbreCAP ↔ EpsiCentauri, 95 CP fleet, 48.5 min round trip at 2,177,621/hr. **Each battle minute costs
~36,300** — 2% of the hourly rate per minute:

| fight | effective rate | | lost per fight |
|---|---|---|---|
| 1 min | 2,133,628/hr | −2% | 36,293 |
| 5 min | 1,974,105/hr | −9% | 181,468 |
| 10 min | 1,805,378/hr | −17% | 362,936 |
| 30 min | 1,345,409/hr | **−38%** | 1,088,810 |

Now the fleets, all weapon-maxed, against team 1010801's 402,762 HP:

| fleet | CP | DPM | battle | effective rate |
|---|---|---|---|---|
| 5× Io A | 90 | 161,778 | **2.5 min** | 95% |
| 10× Quaoar Torpedo + 5× Eris Cannon | 95 | 93,385 | 4.3 min | 92% |
| 10× Carilion Special + 10× Quaoar Torpedo | 110 | 83,342 | 4.8 min | 91% |
| 10× Taurus Pulse | 110 | 61,081 | 6.6 min | 88% |
| **20× Carilion Special (pure tank)** | 100 | 2,985 | **134.9 min** | 26% |

A pure tank fleet cannot finish the fight — 135 minutes against a 48.5 minute round trip — and the 26%
is generous, because 20 Carilion Specials carry only 24,000 cargo, so the 2.18M/hr it is scored against
was never available to them. **In this event the tank is not a defence, it is a stall**, and the
dominant play is to end the fight: 5× Io A keeps 95% of the rate at 2.5 minutes.

The tank earns its place as a *mixed-in* screen (the 10+10 row costs 4% against the all-Quaoar fleet
while soaking the hits), not as the fleet.

### The healers are not yet sized

In-battle repair is a **`deploy_bay`** — repair drones — and only three hulls in the whole table carry
one: **Alioth-class Type A and Type C** (20 CP, and both are +30%-warp-for-6-TP hulls) and **Dubhe**,
all at `EFFECT_SHIP_REPAIR_ARMOR_ADD` 300. Whether 300 per tick out-heals the 8,113 DPM a tank still
takes depends on a tick rate that is not in the config, so the "tank forever" claim cannot be confirmed
or refuted from tables. A battle report with an Alioth in the fleet would settle it. Even if it holds,
the time arithmetic above is unaffected — an unkillable fleet that does 2,985 DPM still loses the hour.

### Engine gaps closed to get these numbers

`matrix.system_mods` had no case for `EFFECT_AVOID_INC_BY_WEAPON_TYPE` (so the Special's two evasion
systems scored zero and `maxout` left them unbought — they are its entire purpose) or for
`EFFECT_ENERGY_INJURY_DEC` (so no hull could buy energy resistance, the only defence that exists against
plasma and ion, armour being bypassed). `per_shot` now takes evasion per **attacking weapon type**.
`EFFECT_BALLISTIC_INJURY_SUB` needed nothing — it is id 10033, which the model already reads as armour.

## 7. The model reconstructed against a real maxed hull

Chris's maxed Quaoar Railgun, 2026-10-10, with the build he actually bought — 2× damage, 3× frequency
(the third being prefix 115 "full firepower"), the target-count row, and his two free adjustments:

| | model | in game |
|---|---|---|
| railgun damage | 450 × (1 + 0.20 + 0.05) = **562.5** | 562 |
| turret damage | 60 × (1 + 0.20 + 0.05) = **75.0** | 75 |
| railgun cycle | 16.0s × (1 − 0.70) = **4.80s** | 4.8s |
| HP | 30,540 × (1 + 0.12 + 0.12 + 0.05) + 40/TP × 111 = **43,836** | 43,836 |
| railgun DPM | (562.5 − 10) × 2 × 60 / 4.8 = **13,812.5** | 13,812 |

Every figure. Getting there took four corrections and produced one new convention:

1. **The per-level values are in the table and must be read, not assumed.** `EFFECT_PARAM_LEVEL`
   carries an explicit ladder — the Quaoar's HP rows are `1,200;2,400;3,600;4,900;5,1200;`, i.e.
   level/value pairs ending at 1200 = **12%**. **The steps are not uniform**: 2, 2, 2, 3, 3, exactly
   as Chris described. 1,014 effect rows ship one.

   This is the correction that matters most, and it is his catch. My first pass fitted a constant of
   2.4%/level to this one hull and was about to generalise it across every hull in the model — a
   number that is right nowhere except here. `matrix.ladder_at()` now reads the row's own ladder and
   only falls back to a constant when a row has neither ladder nor parameter.

   Worth noting against his recollection that "most HP increases are +10%": across the playable
   hulls the HP ladders run **5% ×106 rows, 7.5% ×3, 12% ×265, 14% ×46, 15% ×2** — no 10% at all, and
   12% is the commonest. The 5% rows look like the free adjustments. The 10% figure fits the
   **damage** rows instead, which carry no ladder and do use 2%/level over five levels.
2. **Damage rows have no ladder and stay at 2.0%/level.** The earlier Hussar measurement (5/5 =
   +10%, 3/5 = +6%) was right, and the apparent conflict — 562 against a predicted 540 — was the free
   **gun adjustment** at +5%, which Chris has and which the hand-built comparison had left out.
3. **`EFFECT_ID` 1010 is `EFFECT_SHIP_SYSTEM_HP`, not ship HP.** The model was adding it to the hull's
   hit points. It is the *per-system* pool from `data/system_damage.md`, which is why the Quaoar's
   prefix 401 (+35%) contributes nothing to Chris's HP decomposition.
4. **Prefix 115 counts as one of the three frequency upgrades**, which is what makes the stack −70%
   and takes a 16.0s cycle to exactly 4.8s.

**The in-game DPM display subtracts 10 points of armour** — confirmed twice, here and independently on
the Saber's AS weapon, whose 445 is `(75 − 10) × 4 × 60 / 35` to a tenth (`data/tp.md`). That second
check also settled whether a weapon's lock-on belongs in its cycle: it does not. `(damage − 10) × shots × 60 / cycle`
reproduces 13,812 from 13,812.5. So every DPM the game shows is quoted against a 10-armour target —
which flatters low-damage, high-rate weapons and understates big single shots, and is a different
convention again from the "full firepower" accuracy problem in section 4. Chris also reports roughly
2% shield in the display; the railgun line fits without it, so it is not pinned down.

**Still open: 5 tech points.** His total is 111, the tools compute 106 for the same six weapon rows,
and the gap is exactly explained if the target-count row (prefix 401) costs **15 TP rather than 10**.
`Tb_cfg_system_enhance` gives it `ENHANCE_COST (2, 2, 2, 2, 2)` = 10, so either that field is not the
whole price for this row or the row is not the one being read. Worth one look at the upgrade screen.

## Carrier and craft model faults, found against Chris's in-game readings (2026-10-14)

Chris checked the model's carrier numbers against the game and three of the four disagreements were
the model's fault. The readings that found them: stock Solar Whale 9,648 DPM; Constantine the Great
34k+; Wraith 5,200 HP with 120/60 mounts; RB7 5,200 HP with a 220 ballistic; T800 carrying the 120
pulse. Everything below is anchored to those.

### FIXED - weapon systems are one-per-GROUP, exactly like hangars

`carriers_csv` already knew that a carrier fields ONE system per `Tb_cfg_ship_system.GROUP` and that
summing every hangar module counts alternatives that cannot coexist. The same rule governs WEAPON
systems and `matrix.hull` was not applying it. It filtered mounts by module id against
`STOCK_MODULES`, and a module that appears in both the stock system and its alternatives passes that
test once per system. The Solar Whale's group 102 is the worked example:

```
8010103  grp 102  STOCK    [18011, 18012]     <- the stock M1/A1/B1 fit
8010104  grp 102  add-on   [18014, 18012]
8010105  grp 102  add-on   [18016, 18012]
```

Module 18012 is in all three, so the hull mounted it three times - the stock copy at slot 0304 plus
the optional systems' copies at 0406 and 0508. On top of that the Whale carried module 11032, a
4 x 900-damage **UAV ST-1 drone wing hosted on an optional system**, straight into the hull's gun DPM.

Result: the model read **21,074 DPM where Chris measured 9,648** - 2.2x, and worse once the drone
wing is understood as a third thing that is neither gun nor corvette bay.

`matrix.hull` now drops any weapon mount whose `system_group` is in `OPTIONAL_SYS[sid]` on the stock
path, and the same test gates drone bays. The Whale is left with slots 0303 (320 dmg x2) and 0304
(220 dmg x2), which reproduces the measurement exactly:

| | model | Chris |
|---|---|---|
| nominal | 10,032 | |
| display convention, (dmg - 10) | **9,648** | **9,648** |
| hit-adjusted | 7,513 | |

**15 of 164 hulls had an inflated stock loadout, every one of them a capital.** Solar Whale and Spear
of Uranus lost weapon mounts (2 each); Shield of Plutus, CV3000 and Dubhe lost 3 drone bays each;
Eternal Storm, Antontas Command Ship and Ediacaran 2 each; ST59, Constantine, Megrez, FSV830,
Ganymede, Marshal Crux and Eternal Heavens 1 each. No frigate, destroyer or cruiser moved, so the
line-hull work and the ceiling table's FF/DD/CA sections are unaffected.

### The in-game display is NOMINAL; the model is hit-adjusted

Not a fault, but the conversion has to be applied before the two are compared, and forgetting it
manufactured a fault that did not exist. The display applies the -10 armour convention and nothing
else; `tp_assign._mount_dpm` multiplies by the hit-table probability.

| hull | nominal | display | hit-adjusted | Chris reads |
|---|---|---|---|---|
| Solar Whale, stock | 10,032 | 9,648 | 7,513 | 9,648 |
| Constantine the Great | 33,000 | 32,493 | 26,850 | 34k+ |

The Whale's two guns hit 70% and 80% against a cruiser, which is the whole of the gap between 9,648
and 7,513. The Constantine was **never wrong** - its 34k is nominal and the model's 28,232 was the
same gun after hit rates. Its tech points go to non-damage upgrades, so its nominal DPM is flat at
33,000 from 0 to 31 TP.

Flight time is **zero** on both Whale guns, so the cycle rule (duration + cooldown + flight, lock-on
excluded) reproduces the display unchanged and needs no revision.

### OPEN - `AIRCRAFT_COEF` and `AIRCRAFT_RANGE` are never read

Every `Tb_cfg_weapon` row carries both and the model ignores them. Across 601 weapon rows
`AIRCRAFT_COEF` is 100 on 288, blank on 271, and scattered at 5, 15, 25, 30, 33, 40, 44 and 66 with a
couple at 200 and 307; `AIRCRAFT_RANGE` is 99 on 223 rows, 11 on 161, blank on 125, 3 on 40, 0 on 34
and 2 on 18.

**Whether blank means "full damage" or "cannot engage aircraft" decides how much a wing is worth.**
Chris: most of the meta is aircraft killing aircraft, with a heavy focus on killing carriers, and
aircraft are hard for ships to hurt. If blank is "cannot engage", 45% of ship weapons cannot touch a
wing and craft effective HP is several times what the model computes. Measured today, craft EHP comes
out at only 0.7-1.5x raw HP, which is far too flat to match what Chris describes - so the model is
missing this and the gap is most likely here. Two cheap in-game tests settle it: a wing taking fire
from a ship whose weapons are blank-coef, and the same against a coef 5-15 weapon.

### OPEN - craft hit tables carry 1xx target classes the lookup never reads

`matrix.per_shot` finds the hit rate with `table.get(defender["type"] * 100)`, so it only ever reads
the 300/400/500/600 ship entries. The Wraith's table also carries classes 100, 101, 102, 103 and 105
alongside 200, 1000, 2100-2300, 3100, 4100 and 4300. Those are where aircraft-versus-aircraft lives,
and none of them are reachable through a `type * 100` key. Any answer about wings fighting wings is
currently outside the model.

### Corrected for the record - energy weapons are NOT wrongly armour-immune

An earlier note in this session claimed the armour model was broken for energy weapons, on the
strength of the Wraith showing flat damage against armour. That was a label swap in a scratch script,
not a model fault: the flat curve belonged to the **T800**, whose weapon genuinely is a 120-damage
Energy/pulse mount. The ids are right in `data/ships/*.csv` and were right all along:

| sid | craft | base HP | mounts |
|---|---|---|---|
| 20701 | RB7 | 5,200 | 220 Ballistic |
| 21001 | Wraith | 5,200 | 120 Ballistic x2 + 65 |
| 21301 | T800 | 7,500 | 120 Energy (pulse) |

Corvette damage retention from armour 0 to 300, corrected:

| corvette | DPM @0 | @300 | keeps | |
|---|---|---|---|---|
| T800 (120 pulse, energy) | 2,280 | 2,280 | **100%** | armour-proof |
| S Levi 9 (1,180 torpedo x3) | 2,579 | 1,949 | **76%** | few big shots resist |
| Wraith (120 x2 + 65) | 3,958 | 372 | 9% | floors at armour 108 |
| M011 Missile | 3,285 | 328 | 10% | |
| RB7 (220 ballistic) | 2,508 | 251 | 10% | floors at armour 198 |

Chris called the Wraith and the M011 correctly and his "flattens to 10% just over 100" is the model's
own prediction for a 120-damage ballistic mount. The RB7 collapses too. Its reputation for hitting
cruisers is a HIT TABLE, not a damage bonus - 85% against FF/DD, 95% CA, 100% BC, **70% CV** - so it
holds up against battlecruisers and gets worse against carriers, the wrong direction for a
carrier-focused meta.

### What this changes in the plans

The reinforcement comparison reverses. With the Whale's anti-ship damage corrected from 21,074 to
7,513 hit-adjusted, against the Constantine's 26,850, **5x Constantine the Great beats 5x Solar
Whale** on Cnc04Cavalry, and the 11 free BC points stop being dead. The earlier claim that a Whale
package was 86% hull and 14% wing was an artifact of the same bug: part of what was counted as hull
was a drone wing, and the carrier's damage was tripled.

The FF/DD and CA allocations for Cnc04Cavalry are untouched - they are line hulls, and no FF, DD or
CA hull changed.

### Chimera A over Light Cone Composite A, at 53 TP each (2026-10-14)

Chris asked for both at equal investment. The Light Cone is 20 CP and the Chimera A 18 - the 20 CP
Chimera is the HC variant, which he does not hold.

| | Light Cone Composite A | Chimera A |
|---|---|---|
| HP at 53 TP | 78,614 | 107,268 |
| EHP | 113,672 | **168,452** |
| mounts | 336x2, 192x2, 25x4, 25x4 | 385x3, 280x1, 27.5x4 |
| full ladder | 89 TP | 100 TP |

| target armour | 0 | 80 | 160 | 240 | 300 | keeps |
|---|---|---|---|---|---|---|
| Light Cone DPM | **25,467** | 16,025 | 10,034 | 5,575 | 2,517 | 10% |
| Chimera DPM | 19,636 | 13,065 | 9,215 | 5,364 | **3,314** | **17%** |
| Light Cone BV | 53,804 | 42,681 | 33,772 | 25,173 | 16,916 | |
| Chimera BV | **57,513** | **46,914** | **39,399** | **30,061** | **23,628** | |

**The Chimera leads on BV at every armour value and there is no crossover** - 7% ahead at zero, 40%
ahead at 300. The Light Cone leads only on raw DPM and only below about armour 205, opening 30% ahead
and finishing 24% behind.

The reason is the same pattern the corvettes showed: **fewer, bigger shots resist armour**. Eight of
the Light Cone's twelve barrels are 25-damage mounts that floor at armour 22, and its main guns are
336 and 192 against the Chimera's 385 and 280. Third independent sighting of the rule, after the
S Levi 9's 1,180-damage torpedoes holding 76% and the Wraith's 120s collapsing to 9%. It is now a
reliable way to read a loadout before running anything.

This confirms rather than changes the Cnc04Cavalry plan, where the Light Cone was already one of the
four families being reset to fund the Io A, and the Chimera A is kept and fielded. Worth noting the
Chimera's ladder is 100 TP and it holds 97 there - three points from maxed.

### Mounting a module costs 10 TP (Chris, 2026-10-14)

A mechanic the model does not have at all. Fitting a module into a new system slot costs **10 tech
points**, and for that you get the module's own effect immediately; its upgrade ladder is extra on
top. Chris on the Constantine the Great: "according to the blueprint, the module alone gives +10% dam
to energy weapons and it costs 10 to mount a new module. (slots C and D are new). it also then gives
a damage and cooldown upgrade for extra."

**This invalidates every "best (every module unlocked)" ceiling figure in this repo**, which treats
optional systems as free. Each one costs 10 TP to reach before any of its upgrades are bought.

The correction that matters: the Solar Whale's spare bays were costed at zero. Group 103's `48015`
(+3 corvettes) and group 201's `48013` (+5 fighters) are optional systems, so reaching the 9C+5F
configuration costs **20 TP**, not nothing. The earlier claim that it was "+31% wing value for no
tech points at all" was wrong - and on Cnc04Cavalry it is also unaffordable, since the account holds
7 free CV points against the 20 needed.

### The planner is blind to blank adjustment upgrades

`matrix.apply_upgrades` ignores enhancement prefixes that carry `EFFECT_TYPE=3`,
`ADJUST_ENHANCE_INDEX=1` and no `EFFECT_ID`, and `tp_assign.plan` never schedules them. These are the
flat percentage upgrades - cost `(2,2,2,2,2)` for five levels of 2%, so **10 TP for +10% damage on one
gun**. Two sit on the Constantine alone: prefix `6040110` on system `6040101` (its ion gun) and
`6040112` on `6040103` (its missiles). Applying either through the model produces no change at all.

So every ladder figure in this repo is missing them, every "full ladder" total is understated, and
gain-per-TP rankings are mis-ordered wherever an adjustment row would have competed. The arithmetic
has to be done by hand until this is fixed.

### Worked example: the Constantine's +10% energy module is low priority

The Constantine is **not** mostly energy, which is what makes the answer clear. Its 33,000 nominal:

| gun | action | nominal | share |
|---|---|---|---|
| `16041`, 400 dmg ion | **Energy** | 9,000 | 27% |
| `16941` x2, 850 dmg | **Ballistic** (missile) | 24,000 | **73%** |

So +10% to energy weapons is +900 nominal, +2.7% of the ship. The same flat upgrade on the missile
gun is +2,400, or +7.3%.

| target armour | +10% energy | +10% ballistic |
|---|---|---|
| 0 | +900 | **+2,400** (2.7x) |
| 240 | +900 | **+1,728** (1.9x) |
| 540 | +900 | +875 (crossover) |

The ion gun ignores armour, so its relative worth climbs as armour rises, but the crossover is near
**armour 540** - far past the 300 ceiling of any sweep taken so far. The missiles are the better buy
at every armour level that occurs in practice. Chris: "the big weapons on the CtG are actually the
missiles.. and while this module is helpful, it is probably down the list."

Also resolved, and not a fault: the Constantine's ladder reads 145 TP against the 29 on Chris's ship
because **29 is what it currently holds**, not its ceiling.

### FIXED: system_mods handled 19 of 285 upgrade effects (2026-10-14)

The "blank adjustment" rows were never blank. Prefix `6040110` on the Constantine's ion gun carries
**`EFFECT_ID` 12350 = `EFFECT_WEAPON_BASIC_ATTACK_ADD`** with a real ladder (`1,14;...;5,70`), and
`6040112` on its missiles carries `1,25;...;5,125`. `system_mods` took the named-effect branch, found
no case for 12350, and dropped it silently.

Auditing it: **`system_mods` had branches for 19 of the 285 effect names that appear in upgrade rows.**
The unhandled ones by frequency:

| effect | rows | |
|---|---|---|
| `EFFECT_WEAPON_BASIC_ATTACK_ADD` | 149 | **flat** damage add - now handled |
| `EFFECT_SHIP_HP_ADD` | 92 | flat HP add - now handled |
| `EFFECT_WEAPON_DURATION_INC0` / `DEC0` | 80 | cycle length - still unhandled |
| `EFFECT_FLIGHT_TIME_DEC` | 39 | cycle length - still unhandled |
| `EFFECT_WEAPON_REPEAT_TIMES_ADD0` | 30 | volleys per cycle - now handled |
| `EFFECT_TARGET_PRIORITY_TOP` | 85 | targeting, not a stat |
| `EFFECT_SPEED_ADD` / `CURVATURE_SPEED_ADD` | 118 | movement, out of scope here |
| `EFFECT_REPAIR_INC` | 43 | healing, known unmodelled |

Three are now implemented - the flat damage add, the flat HP add and the repeat-times add. The cycle
effects (119 rows) are left, and they raise DPM where they appear, so DPM remains a floor.

### FIXED: ship-level hit points were never applied

`maxout.level_hp` has held the measured per-class rates since they were taken - destroyer 40 per TP,
cruiser 60, corvette 5, fighter 1, capitals 0 - and **nothing in the repo ever called it.** So every
HP figure was short by the whole term: 4,440 on a 111-TP destroyer, 12% of the hull.
`fleet_build.stats` now adds it.

### Both fixes validated against Chris's Quaoar Railgun at 111 TP

| | model | Chris | |
|---|---|---|---|
| display DPM | **16,112** | **16,106** | **0.04%** |
| raw HP | 42,310 | 43,836 | short 1,526 |

The DPM match is as close as the readings can resolve. The HP shortfall is exactly the **+5% chip
adjustment** this file already documents at 1,527 on a 30,540 base, so the remaining gap is a single
known, unimplemented term rather than an unexplained one. Composition: 30,540 base x 1.24 from two
+12% structure upgrades, plus 40 x 111 ship-level. Chris's own breakdown of the same hull was
base x (1 + .12 + .12 + .05) + 40 x TP = 43,837.

### Consequence: the Conamara Chaos Plasma beats the Chimera A at any armour

With the fixes in, the cruiser comparison Chris asked for, at 70-80 TP:

| hull | CP | TP | BV/CP @0 | @80 | @160 | @240 | @300 |
|---|---|---|---|---|---|---|---|
| Io A | 18 | 75 | **4,346** | **4,092** | **4,072** | **4,072** | **4,072** |
| Chimera A | 18 | 75 | 3,577 | 2,932 | 2,501 | 1,979 | 1,634 |
| Conamara Chaos Plasma | 20 | 75 | 3,481 | 3,435 | 3,435 | 3,435 | 3,435 |

The Conamara is **armour-immune** - 27,480 DPM flat from armour 80 to 300 - so the Chimera's 2.8%
lead against bare targets becomes a 74% deficit at armour 240. The Io A is largely energy too and
beats both everywhere. This does not contradict the earlier Chimera-over-Light-Cone result: those are
both ballistic hulls, and against a plasma hull the ordering inverts.

**Corrected: the three-way split IS the right hedge.** Two things were wrong in the first version of
this note (Chris, 2026-10-14).

Experience is **earned, not granted**. A new hull does not arrive with 30 points - it has to be flown,
PvE encounters stop paying at 30, and the last 20 need PvP or battle awards. So "experience will cover
a new hull" is a claim about grinding, not about a free grant, and pre-positioning permanent TP has
real value.

And the Conamara Chaos **Railgun** and **Plasma** are the SAME family - 51201 and 51202 are both 512 -
and Chris already owns and flies the Railgun. So points placed in the Conamara family are not
speculative: they work today in a fielded hull, and one reset moves the whole position to the Plasma
if it lands, as long as the family stays at or under 50.

That is what makes the hedge cheap. Chris measured the three-way split at about **2% below** the
Io/Chimera split today, and that 2% reverses the moment the Plasma arrives, because the Conamara
family's points carry over while the Chimera's cannot - family 506 has no path to 512.

The Chimera should still be capped at **50 permanent**, and Chris's reason is the better one: "it is
possible the Chimera gets dropped in an advanced account, so I don't want to take this past 50
anyway." Io A first and heavily, Chimera to 50, and the Conamara family funded as the hedge.

## Repair, modelled at last (Chris, 2026-10-14)

Chris: *"repair is a UAV that has stats like a weapon, except that it is +HP instead of -HP. The
upgrades on the ship are similar to any other weapon upgrade, so you can increase damage or reduce
cooldown or duration."* That is exactly how the tables hold it, and it is why repair was invisible.

A repair drone's module has **`ACTION = 4`** in `Tb_cfg_weapon_action`, and its `ACTION_PARAM` is the
heal amount. `matrix.ACTION_NAMES` mapped only 1 (Energy) and 2 (Ballistic), so `per_shot` returned
zero on its first line and the whole system vanished. There are **17 repair modules** in the game.
`ACTION_NAMES` now maps 4 to "Repair", and `matrix.repair_pm(hull)` reads them with the same cycle
arithmetic as a gun - duration + cooldown + flight, lock-on excluded. Every DAMAGE path in the repo
already gated on `action in ("Ballistic", "Energy")`, so repair mounts are skipped there untouched.

`WEAPON_TYPE = 7` is the repair type, and the Alioth's RT-2 carries
`EFFECT_WEAPON_SELECT_TARGET_REPAIR_SELF_OR_CARRIER` - the drone aims its "weapon" at its own ship.

### The three support cruisers on the new account

| hull | CP | repair drones | module | heal | reps | cycle | repair/min | per CP |
|---|---|---|---|---|---|---|---|---|
| **XT 20 Support** | **14** | 3x ST-10 | `11034` | 500 | 4 | 44,000 | 8,182 | **584** |
| 066 Support | 18 | 3x AT-2 维修 | `11034` | 500 | 4 | 44,000 | 8,182 | 455 |
| Alioth A | 20 | 2x RT-2 | `27414` | 350 | 1 | 6,000 | 7,000 | 350 |

**The XT 20 Support and the 066 Support carry the identical repair module**, three each, so their
healing is the same and the XT 20 delivers it for 4 fewer CP plus two armed ST-9s. It is strictly the
better healer, which settles whether the XT 20s are worth chasing: they are.

The Alioth's RT-2 is a different design - a third of the heal on a 6-second cycle instead of 44 - so
it is higher per drone (3,500 against 2,727) and only loses by carrying two. It is also the only one
of the three with **`EFFECT_SHIP_REPAIR_ARMOR_ADD = 300`**, which, if it lands on each repair action,
would take it to 13,000/min. Whether that bonus is per-action, per-second or something else is
**unmeasured**, and it is the one number that decides Alioth against 066.

### Repair scales with tech points, but the planner cannot see it

| hull | 0 TP | 50 TP | 80 TP |
|---|---|---|---|
| Alioth A | 7,000 | 8,750 | **11,667** |
| 066 Support | 8,182 | 8,182 | 8,182 |
| XT 20 Support | 8,182 | 8,182 | 8,182 |

The flat lines WERE the planner not looking, and it is fixed. `tp_assign.seconds_alive` now
subtracts `repair_pm` from incoming damage - which is Chris's breakpoint directly, a hull healing as
fast as it is hit cannot be killed - so `value_of` prices a repair upgrade and `plan` buys it. The net
is floored at 5% of incoming rather than allowed to reach zero, because a hull that out-heals one
pirate template is not immortal and an infinity would make every repair rung look priceless.

With that in, all three scale and Chris's description is reproduced:

| hull | CP | 0 TP | 50 TP | 80 TP | ladder | repair/CP at 80 |
|---|---|---|---|---|---|---|
| Alioth A | 20 | 7,000 | 9,211 | **11,667** | 74 | 583 |
| **XT 20 Support** | **14** | 8,182 | 8,182 | 9,491 | 64 -> **94** | **678** |
| 066 Support | 18 | 8,182 | 8,182 | 9,184 | 58 -> **78** | 510 |

Chris: *"the base healers only differ in the amount of UAV they have. it is the upgrades that start to
differentiate them... the ships differentiate as more and more TP are applied."* That is the table:
identical 8,182 at zero points, diverging only once fed. The ladders lengthen too - the 066 from 58 to
78 TP and the XT 20 from 64 to 94 - because repair upgrades are now purchasable at all.

He also notes the XT 20 ships with specific upgrades already applied, which is what the `-TE` trial
variants are, so an upgraded player model overtakes a TE one given enough points. Two XT 20 lines
exist in the tables with different costs - 573xx at 18/18/14 CP and 582xx at 14/14 - and which is the
TE line is not yet established.

### Corrected again: the XT 20s are TE ships and cannot be fed

Chris, 2026-10-14: **the XT 20s are TE ships with fixed upgrades.** So the 94 TP ladder computed for
the XT 20 Support above is meaningless - there is no way to spend points on it - and the conclusion
that it is "the best healer per CP at every investment level" was wrong twice over. A TE hull is
compared at its frozen state against a hull that can be invested in.

| hull | CP | TP | HP | repair/min | DPM | rep/CP | DPM/CP |
|---|---|---|---|---|---|---|---|
| XT 20 Support (TE, frozen) | 14 | - | 57,510 | 8,182 | 3,714 | **584** | 265 |
| 066 Support | 18 | 0 | 66,400 | 8,182 | 3,728 | 455 | 207 |
| 066 Support fed | 18 | 78 | **82,336** | 9,184 | **6,390** | 510 | **355** |
| Alioth A fed | 20 | 74 | **101,618** | **11,667** | **7,842** | 583 | **392** |

**The XT 20 wins only on repair-per-CP in isolation**, and that is the wrong yardstick: healing a hull
that dies anyway is wasted, so repair has to be read alongside the HP it is protecting and the damage
the platform contributes. A fed 066 Support carries 43% more hit points and 72% more damage. Chris:
*"a 78 TP CAS is prolly gonna outperform an XT20 even at a per/CP level.. not to mention the CAS has
guns and more HP."* It does.

**A fed Alioth A beats both outright** - most HP, most repair, most damage, best DPM/CP. So among
these three the Alioth is the investment target, the 066 the solid buildable healer, and the XT 20
free filler that cannot be improved.

**Note the tables do not mark TE status for these hulls.** `TEST_NAME` is plain for all of them -
XT-20护航, XT-20载机, XT-20支援 - with no `-TE` suffix, which is the only TE marker the tooling knows.
Two XT 20 lines exist, 573xx at 18/18/14 CP and 582xx at 14/14, and which is the trial line is not
established. So TE status currently has to come from Chris, and any ranking that silently feeds a TE
hull tech points is wrong in the way this section was.

### Known-bad number to distrust

`Alioth-class Type C` computes to **16,000 repair/min**, which would make it the best healer found.
Its module `27401` has a **blank `CD_TIME`**, so the code substitutes `CD_DEFAULT_MS = 3000` - an
assumption covering the 20 weapon rows with no cooldown. If the true cooldown is 30 seconds the real
figure is 1,600. Do not use it until the cooldown is measured.

The game's repair ceiling is far above any of these in any case: `13058` heals 1,120 x 4 on a 52s
cycle, and `27407` 800 on 30s. Whatever carries those out-heals all three of these hulls.

### Sizing it against Chris's breakpoint

Chris's rule is that a hull healing at least as fast as it is being hit cannot be killed, so
`repair_pm` is directly comparable to incoming DPM. At ~8,000/min these cruisers each absorb roughly
one upgraded corvette's worth of fire, so a 400 CP fleet needs several before healing changes an
outcome. That sizing question is now answerable, which it was not this morning.

## Weapon strategies: the 9xxx prefixes (Chris, 2026-10-17)

Chris asked whether the Reliat A's **"high-speed dense munitions"** had been priced. It had not, and
nor had any other strategy - `tp_assign.options` discarded every `9xxx` enhancement prefix outright.

A `9xxx` prefix is a **skill**, not a permanent buff: each has a row in `Tb_cfg_system_skill` with a
`TRIGGER_TYPE`, a `TRIGGER_PARAM` and an `EFFECT_ROUND`. "High-speed dense munitions" is prefix
**`9216`, 15 TP, a single rung**, granting `WEAPON_REPEAT_TIMES_ADD0 = 2` (+2 volleys on a 4-volley
launcher) and `HIT_RATE_INC = 30`, with `TRIGGER_TYPE=13 TRIGGER_PARAM=3 EFFECT_ROUND=1
SKILL_PROB=100`. While it runs it is worth **+63% DPM** against +9% for the best permanent option on
the same system - so discarding these hid the largest single upgrade on some hulls.

**Uptime is inferred, not measured.** Across the 22 `TRIGGER_TYPE=13` skills, `EFFECT_ROUND` is 1 (one
is 2) and `TRIGGER_PARAM` is 2, 3 or 4, which reads as "fires every `TRIGGER_PARAM` rounds, lasts
`EFFECT_ROUND`" - so `uptime = EFFECT_ROUND / TRIGGER_PARAM`, one third for `9216`. The semantics of
trigger type 13 are unconfirmed; a strategy that really fires on a player action or a kill would have
quite different uptime. **Any ranking that turns on a strategy is provisional until the cadence is
measured in game.**

### Two things this got wrong before it got right

**Scaling a strategy's parameters by uptime is invalid.** It is only correct where DPM is linear in
the parameter. The Quaoar Railgun proved it: strategy `9101` cuts cooldown 80%, and a "uptime-scaled"
26.7% stacked onto its permanent cut produced a 533ms cycle and **2,326 -> 6,955 BV/CP**. Having 80%
off for a third of a fight is not 27% off always. `tp_assign._mount_dpm` now blends the **rates** -
`(1-u) * rate_off + u * rate_on` - which is exact for every effect type.

**But rate-blending alone was not enough, because the stacking rule is unknown.** With the strategy's
cooldown applied at full strength in the on-state, `9101`'s -80% stacks additively onto the Quaoar's
permanent reduction to give **-99%, a 160ms cycle and 285,525 DPM**. Additive stacking is confirmed
for ordinary upgrades (Chris: two 15% cuts = 30%) but nothing establishes it for a strategy, and the
result is plainly degenerate. So **a strategy is credited only with the effects DPM is LINEAR in** -
flat and percentage damage, extra volleys, hit rate - and its cooldown and duration effects are
ignored. A strategy whose only modelled effect is a cooldown cut therefore contributes nothing and is
never bought. That is the honest answer until the stacking rule is measured, and it means **DPM
remains a floor** for hulls carrying such a strategy.

### What moves, with strategies wired in

| hull | with strategies | without | strategies bought |
|---|---|---|---|
| **Reliat A** | **800** | 673 | **+19%** - `9216` + `9119` |
| Taurus Defense | 1,539 | 1,530 | +1% - `9119` |
| Quaoar Railgun | 2,326 | 2,326 | none: `9101` is cooldown-only |
| Eris Heavy Cannon | 1,906 | 1,906 | none |
| Quaoar Torpedo | 2,406 | 2,406 | none |
| Reliat Stealth | 3,048 | 3,048 | none |

So the practical effect is small today and concentrated on hulls with volley or hit-rate strategies.
That is a consequence of the conservative choice above, not evidence that strategies are minor.

### The layer that is still missing

All 22 trigger-13 skills are now offered to the planner, but several grant effects the model has no
handler for, so they still price at zero: `9232` armour penetration +100 (`WEAPON_ARMOR_PENETRATION_INC`),
`9180` and `9137` burst damage, `9131`/`9132` extra attack targets (`EXTRA_ATTACK_TARGET`), `9260`
target priority. **Armour penetration is the one to worry about**: armour has been the dominant
variable in every comparison this week, so a strategy granting +100 penetration could reorder the
cruiser and corvette rankings outright. Until `WEAPON_ARMOR_PENETRATION_INC` is implemented, any
armour-curve conclusion for a hull carrying `9232` is understated.

## A stock module can grant hull HP, and it was never counted (Chris, 2026-10-17)

Chris checked the Taurus against the game and found both the Assault and the Defense showing **48,036
HP where the tables say 40,030** - with no upgrades applied, and his own tool agreeing with the game.
He traced it himself: "both of them have 2 armor modules. the base armor system with
structure/resistance upgrades shows base 40030 HP, and the Reinforced Armor system (anti crit/system
structure upgrades) lists 8006 additional HP."

That is exactly +20%, and it is in the data: systems `4050203` and `4050303` field module **`36032`,
carrying `EFFECT_SHIP_HP_INC = 2000`**. `matrix.hull` read `playable_weapons.json`'s `hp` and never
added module HP at all, so it was short by the whole term.

**The Taurus Pulse is the control.** It has no such system and reads its base 36,040, which is what
Chris sees - so the discrepancy appears on exactly the two variants that carry the module.

`EFFECT_SHIP_HP_INC` is in **hundredths of a percent**, which Chris's own Quaoar reading confirms
independently: he described that ladder as "2+2+2+3+3" against params 200, 400, 600, 900, 1200. So
2000 is +20%, not +2000.

`hull()` now applies `stock_stat(sid, "10")`. **Only three hulls in the game carry a stock HP module**,
and two of them now match Chris's readings to the digit:

| hull | table HP | module | corrected | Chris sees |
|---|---|---|---|---|
| Taurus Assault (40502) | 40,030 | +20% | **48,036** | **48,036** |
| Taurus Defense (40503) | 40,030 | +20% | **48,036** | **48,036** |
| Aldabra B (41202) | 37,090 | +10% | 40,799 | - |

The Quaoar Railgun carries none, so the 42,310 HP validation of the ship-level-HP fix is unaffected.

### What it changes for the build decision

| hull | CP | @0 | @30 TP | @40 TP |
|---|---|---|---|---|
| **Taurus Defense** (C) | 8 | 1,212 | **1,519** | **1,598** |
| Taurus 攻坚 (48701) | 8 | 1,122 | 1,386 | 1,455 |
| **Eris Heavy Cannon** | 9 | 780 | 1,245 | 1,434 |
| Taurus Assault (B) | 11 | 980 | 1,235 | 1,315 |
| Taurus Pulse (A) | 11 | 825 | 1,057 | 1,119 |

On the limited account the only Taurus held is the **Pulse**, the one variant with no HP module, so
**the Eris Heavy Cannon wins there by 18% at 30 TP and 28% at 40** and the HP fix does not disturb
that. Where the Defense IS held, it leads until about **60-72 TP** (the fix pushed that crossover out
from ~45) after which the Eris overtakes and keeps climbing to 1,906 against the Defense's 1,687.

### Also settled: families 405 and 487 are different ships, not variants

`48701` is **斗牛攻坚** (storming/siege) while `40502` is **斗牛-突击** (assault). Two distinct hulls
this repo had mistranslated to the same English name, "Taurus Assault", which is why the two families
looked like duplicates. They are separate families with separate TP pools: 487 is 8 CP with an 85 TP
ladder reaching 1,715, against the 405 Assault's 11 CP and 1,315 at 40 TP.

## Strategy uptime is in the tables after all, and the event stream proves it (2026-10-17)

Preparing to capture a Reliat battle for the `9216` trigger cadence, the existing captures turned out
to answer most of the question already.

### Skill activations are logged in the battle event stream, by skill id

`NOTIFY_WORLD_BATTLE_DATA` (cmd 2010) carries per-event rows of `[type, actor, code, 0, target]`, and
**some of those codes are skill ids**: `battle4.jsonl` contains 68 events with code `9227` and 18 with
`9901`, both real `Tb_cfg_system_skill` rows. So a strategy's firing is directly observable with
microsecond timestamps - no need to infer it from volley counts, and no need for a single-hull fleet,
since the events carry the actor.

### And the cadence matches the table to the millisecond

Skill `9227` has `PREPARE_TIME = 45000` and `EFFECT_TIME = 35000`. Its inter-arrival gaps per actor in
battle4, for five separate ships, are **exactly `0.0, 35.0, 0.0, 45.0, 0.0, 35.0, 0.0, 45.0`** -
paired events marking each transition, then 35 seconds active and 45 seconds preparing. So for a
timed skill:

    uptime = EFFECT_TIME / (PREPARE_TIME + EFFECT_TIME)

which for `9227` is 43.75%. **155 of 709 skills carry both fields** (152 of them `TRIGGER_TYPE=1`),
and **45 of those are buyable `9xxx` prefixes** on playable hulls. Median uptime among the timed
skills is **95%**, so most are nearly permanent rather than occasional.

`matrix.strategy_uptime` now uses that formula where the fields exist and falls back to the
round-based inference only where they do not.

### What this changed

24 of 160 hulls moved, and the two that matter most moved DOWN, because the measured uptimes are
lower than the 1/3 default they had been getting:

| hull | with the 1/3 guess | measured | |
|---|---|---|---|
| Conamara Chaos Plasma | 3,215 | **2,961** | -254 |
| Io A | 3,485 | **3,403** | -82 |

So part of yesterday's "+20% to the Conamara" was the guess rather than the data. The
Conamara-over-Chimera case survives at **+25%** (2,961 against 2,363) rather than +36%.

### What still needs the capture

`9216` - the Reliat A's "high-speed dense munitions" - is `TRIGGER_TYPE=13` with **no timing fields at
all**: just `TRIGGER_PARAM=3`, `EFFECT_ROUND=1`, `SKILL_PROB=100`. Round-based, not clock-based. **No
existing capture contains any of the 22 type-13 skills firing**, so its cadence is still the inferred
one-third and the Reliat recommendation still rests on it. Break-even remains ~22% uptime.

The capture to take is a live battle with Reliats carrying `9216`; the fleet can be mixed, since the
events are attributed per actor. Count `9216` events and read the gaps the way `9227`'s were read.

### Also found, also unmodelled

Several buyable strategies grant **`EFFECT_SHIP_ADD_TEMP_SKILL`**, which chains to a further skill id
(`9541` -> 954200 and 954300, `9170` -> 917100/917200, and so on). That is a second layer the model
does not follow at all: a strategy that grants a skill that grants an effect currently prices as
nothing. Worth mapping before trusting any ranking that turns on one of those 45 prefixes.

## MEASURED: the Reliat's "high-speed dense munitions" trigger (battle7, 2026-10-17)

Chris captured a live battle with ten Reliat A carrying `9216`, in Wireshark, across two waves (a
second pirate joined mid-fight). `battle7.pcapng`, 508 MB, 322.9 seconds. **64 `9216` events.** Both
halves of the model's treatment are now observed rather than assumed.

### The effect: +2 volleys, exactly as modelled

The event stream's type-2 rows carry the shot count in field 6 and `[hits, misses]` in field 8, which
sum exactly. Each Reliat fires two weapons - code `101` at 8 shots per volley (duration 15000) and
code `202` at 6 shots. **The shot count never changes all battle** (52 volleys of `202` at 6, 30 of
`101` at 8).

What changes is the number of VOLLEYS per firing cycle. Every Reliat fires exactly **4** volleys of
the `101` weapon in its first cycle, with no activation. Cycles containing a `9216` activation run to
**6**. That is `EFFECT_WEAPON_REPEAT_TIMES_ADD0 = 2` - more repeats, not bigger volleys - which is how
`matrix.system_mods` applies it.

### The cadence: 31%, against the inferred 33%

| | complete cycles | mean volleys |
|---|---|---|
| no activation | 48 | 3.23 (29 of them exactly 4) |
| activation | 22 | 4.09 (7 at five, one at six, two at ten) |
| **activation rate** | **22 / 70 = 31%** | |

`EFFECT_ROUND / TRIGGER_PARAM` = 1/3 = 33%. **The inference was right.** So the Reliat A figures stand:
+5.8% at 52 TP, +8.4% at 60, break-even around 22% uptime.

Two cautions on the statistic. Estimating uptime from EXTRA VOLLEYS instead gives 25%, because many
cycles were cut short when targets died - the means above are depressed by truncation on both sides,
so the activation RATE is the sounder number. And the final cycle per ship is dropped for the same
reason.

### Read as "every third cycle", and do not over-fit it

Chris's reading, and the right one: **it fires on the 3rd cycle**, which is exactly
`TRIGGER_PARAM = 3` with `EFFECT_ROUND = 1`. The 31% rate is corroboration, not a precise constant.

The wall-clock gaps are ragged - 23, 25, 26, 26, 28, 28, 30, 30, 30, 38, 38, 38, 65, 65, 69, 82, 82,
82, 85, 85, 85, 86 seconds - but that is what a cycle COUNTER looks like when the cycles themselves
are irregular. A ship that switches targets or has nothing in range does not complete a cycle, so
wall-clock spacing drifts even though the count does not. Chris: *"it is possible they are missing
cycles or the timing is off because they switched targets... I wouldn't try to get too accurate here
as the test conditions were not clean."*

Two artefacts of the measurement rather than the mechanic: the apparent absence of activations in the
first four cycles, and the two cycles that read as **10 volleys**, are both most likely the 20-second
gap threshold used to segment cycles merging or splitting them around target changes. A clean read
would need a single-wave fight against one target type, which this was not - a second pirate joined
mid-battle and the fleet had to be sized to win rather than to measure.

So: **uptime 1/3 for a round-based strategy, from the table and consistent with observation.** Not a
figure to refine further without a staged fight.

### Bug found: ilcap.py ignored nanosecond timestamps

`_read_pcapng` returned raw EPB timestamps without reading the interface's **`if_tsresol`** option.
pktmon's `etl2pcap` writes the pcapng default of microseconds and omits the option; **Wireshark and
dumpcap write nanoseconds**. So battle7 first read as a 322,861-second fight with 38,000-second gaps
between skill firings. The parser now reads option 9 per interface and normalises to microseconds, so
`ts_us` means what it says whichever tool wrote the file. Every earlier capture was pktmon, which is
why this never showed up before - and why the first cadence numbers out of this capture were nonsense
by a factor of 1,000.

## Battle rows: the model scored every hull as if it were front-line (2026-10-17)

Chris, explaining why his Reliat build has no defensive upgrades at all: *"I skipped the evasion
because the reliats are mid-row, and are mostly shielded by all of the frontline ships."*

`battle7`'s own damage table settles it:

| ship | n | damage dealt | damage **taken** | taken/ship | ROW_INDEX |
|---|---|---|---|---|---|
| Quaoar Railgun | 10 | 48,457 | 8,526 | 853 | 1 |
| **Reliat A** | 10 | **47,012** | **0** | **0** | 1 |
| Eris Heavy Cannon | 8 | 40,181 | 12,344 | **1,543** | **0** |
| Carilion Recon | 10 | 6,007 | 11,132 | 1,113 | **0** |
| FG300 Multipurpose | 1 | 697 | 0 | 0 | 1 |

**The Reliats took zero damage all fight while dealing the second-most in the fleet.** Evasion on them
would have been entirely wasted. And `Tb_cfg_ship.ROW_INDEX` has carried this all along - 36 playable
hulls in row 0, **77 in row 1, 51 in row 2** - so 128 of 164 hulls are not front-line and every BV/CP
figure in this repo scored them as if they absorbed full incoming fire.

The table also prices the Carilion exactly: **6,007 dealt for 11,132 taken**, the only hull in the
fleet that absorbs more than it contributes. Chris: *"Carilions are probably temporary, but I needed
them for the frontline when I could not build destroyers."*

### Scaling exposure does not fix it; capping survival does

The obvious fix - multiply incoming damage by a row factor - **changes nothing**, because it enters
`sqrt(DPM x seconds_alive)` multiplicatively. Exposure x1, x5 and x100 all produce an identical buy
order on the Reliat A. What makes survivability stop paying is a **cap**: once a hull outlives the
fight, more hit points buy nothing. `seconds_alive` is now capped at `FIGHT_SECONDS = 320` (battle7's
length) and takes a `ROW_EXPOSURE` multiplier.

With the cap in place the behaviour matches Chris's reasoning. At exposure 0.05 - what the Reliats
actually experienced - the model buys **17 damage rungs and no defensive ones**, starting
`9216, 305, 305, 305, 305`. That is his real 51 TP build (`9216`, `305` x5, `306` x3, `103` x5,
`104` x5). At 0.10 and above it still buys evasion first, so the threshold is sharp.

### But no default discount is applied, and here is why

Within row 1 the measured spread was **0 (Reliat), 0 (FG300), 853 (Quaoar)**. Exposure is a function
of targeting and fleet composition, not of row alone - a thin front line exposes the mid row, a deep
one hides it completely. A constant would quietly rewrite every ranking on one battle's composition,
so `ROW_EXPOSURE` defaults to 1.0 for all rows and is a knob to set when a hull is known to be
shielded.

### What the cap alone changed: capitals were overstated

19 of 160 hulls moved, every one of them a capital, because they are tanky enough to survive a whole
fight and were being credited for survivability they cannot use:

| | before | after |
|---|---|---|
| Ediacaran (AUX) | 2,078 | 1,257 |
| Eternal Storm (BC) | 3,160 | 2,382 |
| Marshal Crux (CV) | 2,400 | 1,668 |
| Constantine the Great (BC) | 2,929 | 2,286 |
| Thunderous Radiance (CV) | 2,070 | 1,376 |

Orderings: FF, DD, CA and AUX unchanged; **BC swaps at rank 3** (Spear of Uranus now ahead of the
Antontas) and **CV at rank 3** (Solar Whale now ahead of Eternal Heavens). No frigate, destroyer or
cruiser moved, so the line-hull work stands.

---

## Measured against real battles (2026-10-19)

The model has now been scored against two captured battle reports rather than against itself. See
**[data/battle_reports.md](battle_reports.md)** for the wire format, the enemy resolution and the
full comparison. The short version:

* Damage attribution must come from the **battle report** (cmd 2402), not the live event stream —
  stream weapon codes are per-slot and reused by both fleets. The earlier "this fleet is armour
  floored" reading, including the claim that the Reliat Energy floored at 108, came from that
  mistake and is withdrawn.
* **UAV and repair-drone mounts fly as their own ship instances.** The XenoStinger's `install=4`
  type-8 mount is 4 craft per ship, logged separately; counting it as hull DPM reads 20x over.
  The mount's `uav` field names the craft, and the report logs the craft under the parent's module id.
* Per-hull error, consistent across both battles and duration-free: **Quaoar Railgun 1.8x too high**,
  **Taurus Pulse ~0.6x too low**, Reliat Energy and M470 Support accurate. Cooldown stacking and the
  prefix-`115` accuracy penalty are both ruled out as the Quaoar's cause.
* `repair_pm` checked empirically for the first time: model capacity 30,612/min against 20,378 and
  17,382 measured, with the fleet ending at 89-100% HP — a floor under capacity, so consistent.

---

## The client holds 348 config tables, not 85 (2026-10-22)

`lagrange-combat/tables/` is a **curated subset**. The decrypted client carries **348** tables in
`decrypted/common/config/db/` (271 of them `_Tb_cfg_*` data tables), so nothing was ever missing from
the game - only from the extract. That is why the whole base/facility side looked absent.

### Reading them: constants yes, rows no

The files are marshalled Python modules whose rows are built by their own bytecode. **That bytecode
cannot be executed** - NeoX ships a modified Python, so `exec` on the code object segfaults 3.14 and
hard-exits even the bundled matching `tools/py311/python.exe` with no traceback. `marshal.loads`
itself works under 3.11 (it does not validate bytecode), so every **constant** is recoverable.

One trap cost an hour: **code objects nest inside TUPLES in `co_consts`**, so a walker that only
recurses on `CodeType` misses most of the data. It reported the facility costs as absent until a raw
byte grep contradicted it. `tools/load_table.py` now deep-walks properly.

Constants come out in emission order - which is row order - but **without column attribution**, so
this recovers values, not tables. Finishing the job needs whatever produced the existing 85 CSVs, or
a NeoX-aware disassembler.

### Facility costs: found, and the resource ids are pinned

`_Tb_cfg_facility_level_ex` (plus `_ex_3`, `_ex_4`, `_ex_7`, `_ex_8`, `_ex_62`) holds 728
resource-cost strings in the form `type,amount;type,amount;...`:

    1,120000;2,300;3,120;4,0
    1,0;2,18600;3,7440;4,0

**Type 2 is metal**, confirmed twice against Chris's in-game reading of Generic Port 1 - level 1 at
**300** and level 2 at **18,600**. Type 1 and 3 are unidentified; on the rows where they co-vary the
ratio is type1 = 400 x type2 and type3 = 0.4 x type2, and by Chris's resource values (metal 1,
crystal 40, deuterium 100) a 120,000 / 300 / 120 split lands at 83% / 8% / 8% by value - close to the
90/5/5 he recalls, which is consistent with type 1 being a bulk resource.

The same table also carries effect strings in a different id space (`152,3000;153,90;154,90;` and
`141,1200000;142,30000;143,15000;`), so costs and effects are co-located - good news for a planner
once rows can be attributed.

### Facility tree, from the subset we already had

75 root facilities; 257 enhancement nodes in chains up to 6 deep; **exactly 4 choice points**
(`1008014`, `1039013`, `1042011`, `1043013`), matching Chris's "only 4 real choices". `1006` is
Generic Port 1 - lowest root, legacy id 11, two-node chain. Unlike the ship trees, the facility tree
**does** carry explicit `PARENT_ENHANCE_ID` links, so prerequisites are available here.

Correction to an earlier note: the root's second field is `2` on **all 75** roots, so it is a
node-type marker, not a level count.

### Base build scheduling is a FLOW problem, not a budget one

Chris's actual constraint: **529.2k metal/hr mined, 2 build slots, don't run dry.** A build is not a
lump sum - it drains for its whole duration - so the only number that matters is

    burn rate = metal cost / build time

You are solvent while the active burns sum to under income. That gives a cost ceiling to check any
upgrade against before starting it, at 529.2k/hr:

| build length | ceiling, both slots busy | ceiling, sole build |
|---|---|---|
| 1 h | 264,600 | 529,200 |
| 12 h | 3,175,200 | 6,350,400 |
| 24 h | 6,350,400 | 12,700,800 |
| **36 h** | **9,525,600** | **19,051,200** |
| 50 h | 13,230,000 | 26,460,000 |

`tools/base_plan.py` computes this, plus which builds are co-runnable and how long to bank for one
that is not. Costs and times are entered by hand, since they cannot yet be attributed to rows.

**Correction (2026-10-22).** An earlier version of this section said build times top out at 5 h and
concluded that "any single upgrade over ~1.32M metal cannot be run two-at-a-time". **Both were
wrong.** The 18,000 s maximum came from `_Tb_cfg_facility`, which holds only the short/early times;
per-level times live in `_Tb_cfg_facility_level_ex`, whose half-hour-aligned ladder runs **0.5 h to
50 h** (24 h, 30 h, 34.5 h, 37.5 h, 40 h, 45 h, 50 h at the top, plus outliers near 85-92 h). Chris
called this out from play experience - he expected 36 h at high levels, and the ladder brackets it.

The correction inverts the conclusion: **long builds are EASIER to sustain, not harder**, because burn
is cost divided by time and duration is the denominator. A 36 h upgrade can cost 9.5M and still share
a slot pair. What breaks the budget is a high cost-to-TIME ratio, not a high cost - 20M over 50 h
burns 400k/hr and is fine, while the same 20M over 5 h would need 4M/hr and is impossible.

Enhancement costs are ignored by design - Chris reports them as trivial against the level upgrades.

### 79 facility names recovered

The names are readable after all: `_Tb_cfg_facility` carries them as `img_<name>` asset keys, so
`data/facilities.csv` now lists all 79 in emission order (`trading_center`,
`small_integrated_plant`, ..., `generic_port_1` at #7, ..., `advanced_habitat_46`) with blank cost and
time columns to fill in. **The mapping from emission order to the tree's facility ids (1006-1083) is
NOT verified** - 79 names against 75 tree roots - so treat the order as a name list, not an id map.
