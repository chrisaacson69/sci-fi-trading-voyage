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
