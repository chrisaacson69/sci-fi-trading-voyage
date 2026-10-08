# System damage

Some weapons damage a ship's **systems** instead of its HP. Systems have their own HP pools;
when one is destroyed it deals "explosion" damage to the ship's HP and stops working until it
repairs on a timer. Decoded from the game tables plus a battle report, 2026-10-08.

## Where it lives

| field | meaning |
|---|---|
| `Tb_cfg_ship_blueprint.FEATURE` contains **139** | the blueprint keyword "attack against systems". 33 blueprints carry it, mostly fighters. |
| `Tb_cfg_weapon.SYSTEM_BURST_PRIORITY` | target systems as **GROUP ids**, in priority order. |
| `Tb_cfg_weapon.SYSTEM_BURST_DECAY_RATIO` | step-down multiplier per entry down that list. |
| `Tb_cfg_weapon.SYSTEM_BURST_MODE` | 2 on every system-damage weapon. |
| `Tb_cfg_ship_system.HP` | the separate HP pool for each system. |
| `EFFECT_AUTO_SYSTEM_REPAIR`, `EFFECT_DO_DAMAGE_WHEN_REMOVE` | repair timer and explosion, as module/adjustment effects. |

Group ids seen so far: **1 = primary weapon, 3 = command, 5 = propulsion**.

## Worked example - Stingray torpedo vs AC721 Amphibious

Stingray's torpedo is module 11191: ballistic base 400, weapon type 6, `MODE 2`,
`PRIORITY 1,3,5`, `DECAY 80`. In game the blueprint reads "attack against systems",
priority 1 primary weapon medium, 2 command low, 3 propulsion low - which is the
1 -> 0.8 -> 0.64 decay rendered as tiers.

AC721 Amphibious system pools: group 1 = 7,650, group 2 = 6,500, group 3 = 6,300,
group 4 = 6,750, group 5 = 5,950, group 6 = 6,500, group 7 = 5,950 (ship HP 30,730).

Observed in one battle, four Stingrays against five AC721 Amphibious:
destroyed 4x group 1 and 1x group 3, zero group 5 - exactly a decaying 1,3,5 list.
Their combined pools are 4x7,650 + 6,300 = **36,900** against **37,050** system damage
reported, so only 150 spilled into systems that survived.

Bomber damage that fight: 108,522 total, **48.5% of it into system pools**, and 74% of it
aimed at the five AC721. Four 1-CP craft at +90 evasion, against a fleet with no AA.

## Explosion, repair and permanent loss - SOLVED

From the AC721 blueprint text: **each disable deals 5% of the ship's max HP**, the system
**repairs in 25 seconds**, and it **repairs twice - the third disable is permanent**. Chris
confirms the explosions are all the same size, which rules out the system-HP formula.

Both halves show up in the tables:

| effect | id | param |
|---|---|---|
| `EFFECT_DO_DAMAGE_WHEN_REMOVE` | 12270 | **5** (= the 5% of max HP). A param-10 variant exists, so some hulls take 10%. |
| `EFFECT_AUTO_SYSTEM_REPAIR` | 12250 | **4025** - the `25` is the 25-second repair; the leading `40` is not yet decoded. |

Arithmetic check: 5% of the AC721 Amphibious' 30,730 max HP is 1,536 per explosion, so five
should be 7,682 against the 6,768 observed - 88%. The likely cause is that two of those five
ships died, and an explosion on a dying ship is capped by its remaining HP. Not confirmed.

The repair rule matters tactically: a disabled primary weapon is a ship that stops shooting for
25 seconds and comes back, twice. That is a concrete mechanism for the gap between predicted and
realised DPM that this project has been covering with a hand-waved factor.

Also unmodelled: the engine tracks HP only, so none of its DPM figures account for the system
half of a bomber's output.
