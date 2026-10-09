# Tech-point upgrades: what they actually buy

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

**Anchor:** the Io A reads 650 → 845 warp in game = +30% = exactly two `EFFECT_SPEED` rows at +15%.
So warp responds to effect id 1 only, and +30% is the ceiling — there is no third row to buy.

The propulsion system has an `ENHANCEMENTS_LIMIT`, so the two stats compete for the same slots, and a
hull that lists only ONE `EFFECT_SPEED` row is hard-capped at +15% however much TP you throw at it.

### What each hull can reach

| reachable | TP | hulls |
|---|---|---|
| +30% | **6** | 37 — every 16–20 CP cruiser and carrier: Io A/B/Siege, Callisto A/Heavy/Drone, Chimera A/B/Defense, Conamara Railgun/Plasma, Light Cone Attack C / Composite A / Area AA, 066 (all four), KCPV (all four), Jaeger Cannon/Carrier, Predator, Alioth, Arctos, Cretaceous, Ranger |
| +30% | 12 | 79 — destroyers and the rest: Quaoar Railgun/Torpedo, Eris (all), AC721 (all), Taurus Pulse, Constantine, Marshal Crux, FG300 Armored |
| **+15% only** | 6 | 40 — the cheap screen: FG300 Multipurpose/Recon/SP, **Carilion (all three)**, Reliat A/Energy, Trader Transport/Support, Mare Tranquillitatis/Serenitatis/Imbrium, Ruby, Rager, Zircon, XT 8, NOMA 330, Holy Spirit |
| +22% | 16 | Reliat Stealth |
| +45% | 24 | one hull |

**Consequence for fleet speed.** Fleet speed is the *mean* of every ship's cruise, not the slowest
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
