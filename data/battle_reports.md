# Battle reports: the ground truth the model gets tuned against

Decoded 2026-10-19 from two captured battles. This supersedes damage figures taken from the live
event stream, which cannot say who fired what.

## Why the event stream was not enough

`NOTIFY_WORLD_BATTLE_DATA` (cmd 2010) carries weapon **codes that are per-slot and reused by both
fleets**. Attributing damage by code therefore mixes the two sides together. An earlier pass did
exactly that and concluded this fleet was armour-floored — including the claim that the Reliat
Energy was floored at 108 damage. That was wrong twice over: the Reliat's 120-damage main gun is
**Energy**, which ignores armour, and the model had never applied a floor to it. The measurement
below puts the Reliat at roughly 1,000 real DPM/CP, which is what was reported from in-game.

`USER_GET_BATTLE_REPORT_DETAIL2` (cmd 2402) has no such ambiguity: every damage row is already
attributed to one of our own ship instances.

## Wire format

`team_battle_data` is base64 of a 4-byte length header followed by zlib, decompressing to three
blocks:

| block | one row per | contents |
|---|---|---|
| 0 | owned hull | `[team, sid, owned, …, weapon_codes, upgrade_string, …]` |
| 1 | fielded ship instance | `[sid, instance, hp, team, …, 9:row, 10:CP, …, 14:hp_max, 15:hp_left]` |
| 2 | fielded ship instance | `[instance, sid, [], [[kind, [[target, b, c], …]], …]]` |

`enemy_battle_data` is only a list of fleet ids; the enemy composition comes from
`detail_info["39"]`, which names a `cfg_npc_team` whose `SHIP_INFO` lists the hulls. NPC ship ids
are a 5-digit sid plus 4 variant digits, so `671010401` resolves to sid `67101`, the Indomitable
Missile. **The enemy armour the model is scored against is therefore read, not assumed.**

## The `kind` field — the part that bites

Block 2's rows are grouped by a category, and summing them blind produces damage in the billions:

| kind | meaning |
|---|---|
| **0** | **direct weapon damage.** `b` is the weapon slot, coded `"1" + family + slot index` (sid `40501` → `14051`, `14052`), so damage is attributable to an individual gun. |
| **2** | further damage onto enemy ships. `b` here is a **unix timestamp in seconds**, not a slot. Its fleet total is echoed in `detail_info["103"]`. |
| 3 / 4 | **healing.** Identical totals: kind 3 sits on the ship healed and points at the repair drone, kind 4 sits on the drone and points at the ship. Counting both double-counts. |
| **5** | **kill marker** — both `b` and `c` are timestamps. Any row whose damage exceeds 1e6 is one of these and must be dropped. |
| 8 / 9 / 10 / 12 | breakdown rows already inside kind 2 (8 + 9 = 2 exactly, in both battles). |

`detail_info["103"]` is **not** the battle duration — it is the kind-2 total. The only timing in the
report is the span of the embedded kill timestamps, which is a lower bound.

### Craft fly as their own ships

A UAV or repair drone is logged as its **own ship instance**, not as its launcher's gun. The
XenoStinger Tactical's `install=4` type-8 mount appears as 40 separate `12101` instances. The model
prices that mount as hull DPM, so without folding craft back into the parent the Xeno reads **20×
over**. The link is grounded at both ends: the mount carries the craft's sid in its `uav` field, and
the report logs the craft's damage under the **parent's** module id (`11211` for the Xeno).

Same for the M470 Support: `install=1` type-7 repair drone → 10 × `10306` instances.

## What the two battles measure

Both are 1 BC + 4 CA, from `cfg_npc_team` 31010802 and 31010801. Account Count DeMonet, 375 CP
fielded, all hulls maxed.

| hull | CP | row | own gun | craft | obs DPM/CP | model DPM/CP | model/obs |
|---|---|---|---|---|---|---|---|
| Quaoar Railgun | 6 | 1 | 72,199 | — | 662 / 411 | 1,357 | **1.78 – 1.90** |
| XenoStinger Tactical | 8 | 2 | 764 | 114,033 | 790 / 467 | 1,040 | 1.20 – 1.22 |
| Reliat Energy | 4 | 1 | 84,835 | — | 1,167 / 613 | 1,058 | 0.84 – 0.93 |
| Mare Imbrium Basic | 5 | 0 | 40,522 | — | 892 / 659 | 687 | 0.56 – 0.71 |
| Taurus Pulse | 11 | 0 | 163,877 | — | 820 / 452 | 533 | **0.60 – 0.64** |
| M470 Support | 6 | 2 | 624 | — | 6 / 6 | 6 | 0.97 |

Ratios are given for both battles. The share-of-fleet comparison the tool prints is **duration-free**,
so these ratios hold whatever the true battle length turns out to be.

### What needs tuning

* **Quaoar Railgun is the model's worst hull: 1.8× too high, consistently.** Multiplicative rather
  than additive cooldown stacking would scale it by 0.69, which is close to the inverse of the
  error — but it would also cut the Reliat Energy by 23%, and the Reliat is already accurate. So
  cooldown stacking is **not** the explanation. Accuracy is not it either: the Quaoar is the only
  one of these hulls carrying prefix `115` (CD −40, hit −15), and that penalty **is** already
  applied.
* **Taurus Pulse is ~0.6× too low**, the opposite sign, and it is the hull whose error grows against
  armour. Its small gun (20 damage × install 3) delivered 13% of its damage, which suggests the
  model is underrating low-damage high-rate mounts against armour.
* **Reliat Energy and M470 Support are accurate.** The Reliat is the cleanest check in the set: pure
  energy, no craft, no kind-2 damage at all, so its number depends on nothing but the duration.

### Repair, checked for the first time

Measured healing by 10 M470 Support: **20,378/min** and **17,382/min**. Model capacity is
**30,612/min**. These are consistent rather than contradictory — the fleet ended both fights at
89–100% HP, so the healers were idle much of the time and measured healing is a floor under
capacity, not a rate. This is the first empirical check on `repair_pm` at all, and it lands within
1.5× on the correct side.

## Open question the capture cannot settle

Whether the in-game report counts **kind 2** toward a hull's damage. In battle 100119530 kind 0
lands only on that battle's own NPC team while kind 2 spans **both** concurrently-engaged teams; in
100119553 kind 2 adds exactly the two enemy **craft** that kind 0 never touches. Including it moves
every hull's DPM/CP by 20–50%, but it does **not** change the error pattern above — the Quaoar is
too high and the Taurus too low either way.

The battle length is the other missing anchor: only the kill-timestamp span is recoverable
(109 s and 201 s, both lower bounds).

## Tooling

`tools/battle_report.py` in the private analysis repo:

```
python tools/battle_report.py battle8.jsonl
python tools/battle_report.py battle8.jsonl --secs 130 --kind2 out --slots
```

Captures stay local — the raw `.etl`/`.pcapng` carry the session token in clear at offset 8 of every
client message, since port 8001 has no TLS. Only derived analysis like this page is shareable.

---

## Follow-up 2026-10-19: the stream is in half-units, and `shots_per_action` double-counts

Chris supplied the in-game per-hull damage with the battle times at the top, which pinned every
remaining free variable. Battle lengths are **1:49 and 1:56** — the two were fought back to back and
the game treats them as one 3:45 engagement, which is why the embedded kill-timestamp span ran them
together and gave 201 s for the second.

**The in-game totals match kind 0 exactly**, so three things are now settled rather than assumed:

| hull | in-game (summed per type) | decoded kind 0 |
|---|---|---|
| Taurus | 48,882 + 114,995 = 163,877 | 163,877 |
| Xeno | 67,057 + 47,740 = 114,797 | 764 own + 114,033 craft |
| Quaoar | 37,518 + 34,681 = 72,199 | 72,199 |
| Reliat | 19,634 + 65,201 = 84,835 | 84,835 |

* **kind 2 does not count** toward in-game damage.
* **craft damage is credited to the parent hull** — the Xeno line only reconciles that way.
* battle 1 was exactly **109 s**, matching the kill-timestamp span.

### The event stream emits every damage row TWICE - dedupe it

Summing the stream's damage field per hull gives exactly **2.00x** the report's kind 0, for all
seven hulls. The cause is not a half-unit encoding: **6,288 of 6,382 distinct type-2 rows appear
exactly twice, and 6,368 of those pairs occur inside a single message.** Each damage row is emitted
twice per message, so damage, shots and hits are all doubled together. Deduplicate by row identity
before using any stream figure.

> **Retracted.** An earlier version of this section read the 2.00x as a half-unit damage encoding and
> concluded from the halved figures that table damage is **per volley**, with `shots_per_action`
> double-counting it. That is wrong, and it contradicted evidence already in this repo: the model's
> nominal DPM for the Quaoar is 16,823 against 16,106 displayed in-game, and that figure is built
> from 540 x **2 shots**. Damage is per shot. The ratio dmg/hit is unaffected by duplication, so the
> real per-hit numbers were the unhalved ones all along.

Ownership in the stream was never actually ambiguous either - field 1 is the attacker **instance
id**, which resolves it completely. The original "codes are reused by both fleets" caveat applies
only to the code, and keying on it alone was the mistake.

### Per-weapon truth, after deduplication

`dmg/hit` is measured after armour; `firing` is observed shots per minute against the model's
nominal rate, so 100% means the modelled cycle is right.

| weapon | dmg/hit | model base | firing vs nominal | hit rate |
|---|---|---|---|---|
| Quaoar rail | 458 | 540 (562 in-game) | **79%** | **65.9%** |
| Quaoar secondary | 8.5 | 72 | **64%** | 74.2% |
| Taurus main | 470 | 420 | **171%** | 73.5% |
| Mare Imbrium main | 499 | 378 | 124% | 72.4% |
| Reliat main | 153 | 120 | 155% | 80.6% |

Two independent error sources, and the two outliers sit at opposite ends of both:

* **Model base damage runs 10-25% LOW** on the Taurus, Mare Imbrium and Reliat - each deals more per
  hit than its modelled base even before armour. The Quaoar is the exception at 4% low (540 against
  562 in-game).
* **Model cycles are too LONG** for the Taurus (fires 1.71x the modelled rate), Reliat (1.55x) and
  Mare Imbrium (1.24x), and slightly too SHORT for the Quaoar (0.79x).
* **The Quaoar has the worst hit rate in the fleet at 65.9%**, against 73-89% for everything else,
  which is consistent with the railgun evasion finding already recorded in roles.md.

So the Quaoar reads high because it fires less often than modelled AND hits least often, while the
Taurus reads low because its modelled cycle is nearly twice too long. Cooldown stacking and the
prefix-115 accuracy penalty remain ruled out for both.

### Still open

* A residual ~1.5x for the Quaoar: 19.7 shots/min x 65.9% x 458 predicts ~5,900 DPM/ship against
  ~3,990 measured across both battles. Either the per-ship clock span overstates active time or
  shots are still over-counted.
* Why modelled cycles are long for three hulls but short for the Quaoar.
* sid 57101 is named **Omni Ion Cannon** here but **StarSweep** in-game - a name-mapping discrepancy.
* Chris notes a real loss from lock-on timing when targets switch; minor at 5 ships.

---

## Follow-up 2: two named assumption bugs, found by auditing against in-game tooltips

Chris, on method: *"instead of trying to error correct the model, we need to go after the assumptions
and make sure it matches."* Right call, and auditing the model's weapon parameters against the
in-game tooltips found two concrete bugs rather than a fudge factor.

The battle report's per-weapon-type split confirms the slot decode exactly: Quaoar Rail
37,128 + 33,085 = **70,213** and Turret 390 + 1,596 = **1,986**, matching slots `14111` and `14112`
to the digit.

| weapon | | damage | cooldown |
|---|---|---|---|
| Taurus main | stock -> model | 350 -> 420 (+20%) | 5,000 -> 3,500 (30%) |
| | stock -> **in-game** | 350 -> **525 (+50%)** | 5,000 -> **2,700 (46%)** |
| Quaoar rail | model | 450 -> 540 (+20%) | 16,000 -> 4,800 (70%) |
| | **in-game** | 450 -> **562 (+24.9%)** | 16,000 -> **4,800** (exact) |
| Quaoar turret | model | 60 -> 72 | 6,000 -> 1,800 |
| | **in-game** | 60 -> **75** | 6,000 -> **4,200** |

### Bug 1: cross-system cooldown upgrades are not applied

The model scopes upgrades to the weapon's own system. But the Taurus carries **`4050104`,
`SYSTEM_TYPE 6`** (an auxiliary system, not `MAIN_SYSTEM`), whose prefix **`4105` is
`EFFECT_CD_TIME_DEC 15`** and applies ship-wide. The weapon's own system `4050101` has `303`+`304` =
30%, which is exactly what the model uses; adding the auxiliary 15% gives 45%, so
5,000 x 0.55 = **2,750 against the 2,700 shown in-game**.

This single miss accounts for the Taurus's entire shortfall:
`(525/2700) / (420/3500) = 1.62`, and `1/1.62 = 0.617` against the **0.61** measured.

The Quaoar has no `4110104`, which is why its rail cooldown matches in-game exactly - and that is the
confirmation that additive stacking is correct, since 40+15+15 = 70% reproduces 4,800 ms.

### Bug 2: weapon damage upgrades are a flat +20% guess

Prefixes `105`/`106` (Taurus) and `109`/`110` (Quaoar) are the weapon damage upgrades. In
`Tb_cfg_system_effect` they carry **no numeric `EFFECT_PARAM`** - instead they set
**`TARGET_MODULE_TYPE`** (204 and 202), i.e. they upgrade the weapon module's tier rather than
applying a percentage. The model does not implement that mechanism and substitutes a flat **+20% for
every hull**, which is why both hulls read exactly +20.0% while the game gives the Taurus **+50%**
and the Quaoar **+24.9%**.

### Lock-on is read but never charged

`aim_ms` is `INIT_PERPARE_TIME`, and the model holds **4,000 ms for the Taurus**, matching the 4 s
lock-on shown in-game. It is excluded from the DPM cycle, which is correct **if** it is paid once at
engagement. Whether firing at aircraft resets it is open and would be a real DPM loss.

### Target selection is RNG and single-battle ratios have wide error bars

Chris: the Quaoar's turret did **390** damage to the Indomitable in battle 1 but **1,080** in battle
2, over near-equal battle times - a 2.8x swing from target selection alone. The report lists weapons
but not who each shot was aimed at over time, so per-hull ratios from one battle cannot be read as
model error. **The Quaoar's own parameters are nearly exact** (540 vs 562, cycle exact), so its 2x
gap is realisation - hit rate 65.9%, the worst in the fleet - and not something to tune out of the
parameters.

---

## Follow-up 3: the per-ship target split

The enemy instance -> hull mapping is now grounded, not guessed: NPC instances are allocated in
`SHIP_INFO` order from the team's lead instance, and that reproduces **all ten** of Chris's in-game
per-weapon-type cells exactly (Rail 37,128 / 33,085 and Turret 390 / 1,596 in battle 1; Rail
43,316 / 27,768 / 8,374 and Turret 1,080 / 1,875 / 120 in battle 2). The only residual is 75 damage
into enemy craft, which the in-game columns omit.

### No ship specialises on a target

In battle 1, 7 of 10 Quaoar engaged 2 distinct enemies and 3 engaged 1; in battle 2, 9 of 10 engaged
3. Every hull spreads. So "did 5 Quaoar take the Indomitable and 5 the StarSweepers" has a clean
answer: **no, they share targets**.

### Armour faced varies by hull, and that is a weapon-priority effect

| hull | armour faced (b1 / b2) | share into the Indomitable (armour 120) |
|---|---|---|
| Quaoar Railgun | **86.4 / 87.6** | **52% / 54%** |
| Mare Imbrium | 64.3 / 78.3 | 20% / 40% |
| Taurus Pulse | 70.9 / 70.3 | 30% / 31% |
| Reliat Energy | **66.2 / 59.6** | **23% / 15%** |

The model averages uniformly over the enemy composition: (120 + 4x50)/5 = **64**. That is almost
exactly what the Reliat faces, which is **why the Reliat is the accurate hull**. The Quaoar faces 87
because its railgun puts half its fire into the battleship while the Reliat's torpedoes chew the
escorts - weapon-type target priority, which the model does not weight by.

It is a small effect though: (562-87)/(562-64) = **0.954**, so focus-fire explains ~5% of the
Quaoar's 2x, not the bulk.

### Bug 3: lock-on is charged in the duel path but not in the DPM path

`matrix.py:596` builds `t0 = ENGAGE_MS + aim_ms` - but only inside `timeline()`, which only the duel
simulation uses. `dpm_out()`, which every fleet, TP and ranking tool goes through, never charges it.
This is exactly the "does the matrix stay current as mechanics are added" problem, in reverse: the
duel grid has a mechanic the DPM path lacks.

For the Quaoar that is 3,000 + 10,000 = **13 s of a 109 s battle, about 12%**, and more if lock-on
re-pays on target switches. Implied firing uptime tracks `aim_ms` across the fleet:

| weapon | `aim_ms` | implied uptime |
|---|---|---|
| Quaoar rail | **10,000** | **49%** |
| Taurus main | 4,000 | 118% |
| Mare Imbrium main | 5,000 | 135% |
| Reliat main | 0 | 128% |

The >100% figures are the signature of bug 1 (modelled cooldowns too long), not real
over-performance.

### Unresolved: the Quaoar's residual

Full accounting leaves **1.78x** unexplained: nominal 14,050 -> 9,259 at 65.9% hit -> 7,834 at 0.846
armour retention -> 6,894 charging lock-on once, against **3,865 measured**.

Worse, two measurements of its firing rate disagree: **19.7 shots/min** from the deduplicated event
stream against **12.4** from the report's damage divided by damage-per-hit. The report figure is
suspiciously close to exactly half the nominal 25/min, which would mean the 2-shot volley costs two
cooldowns rather than one. **Do not tune anything on the Quaoar until that is settled** - it is the
difference between a data bug and a game mechanic.

---

## Follow-up 4: every shot traced - the 1v1 validation

`tools/shot_trace.py`. Conditioning on the target removes selection, so what is left is per-shot
mechanics, which the model predicts directly. Chris's framing was right: ballistic weapons cannot
separate mechanics from target choice (562 into armour 120 is 442, into armour 50 it is 512, and
which it got is RNG), while energy weapons ignore armour - which is why the Reliat matched first.

### Hit rates are validated

Across 38 (attacker, slot, target) cells the model's predicted hit rate lands at **0.82-1.16** of
observed, mostly inside 5%. The Quaoar is **63.7% predicted against 63.8-67.9% observed** - its poor
accuracy is correctly modelled and is not the error.

### Damage per hit inverts to the TRUE enemy armour - and the table is wrong

Observed damage per hit is exactly base-minus-armour, so it can be inverted. Two independent weapons
agree:

| target | Quaoar (base 562) | implied | Mare Imbrium (base ~598) | model table |
|---|---|---|---|---|
| Indomitable Missile | 442 | **120** | 478 -> 120 | 120 ok |
| 066 Bombardment | 512 | **50** | 548 -> 50 | 50 ok |
| Omni Ion / StarSweep | 452 | **110** | 488 -> 110 | **50 WRONG** |
| KCCPV2.0 Carrier | - | - | 518 -> **80** | **50 WRONG** |

**Bug 4: NPC stats are read off the base hull, ignoring the variant suffix.** NPC ship ids are a
5-digit sid plus 4 variant digits (`571010401`), and the model resolves only the sid. Two of four
enemy armour values are wrong as a result, which inflates predicted ballistic damage. This also
confirms Chris's naming flag - sid 57101 is not the Omni Ion Cannon the table names.

### The other two outliers are fully explained as parameter bugs

* **Mare Imbrium** deals 478-548 per hit, implying base **~598** against the model's 378 - a 1.58x
  gap matching its 0.77/0.56 over-performance.
* **Taurus**: base 525 vs 420 (1.25x) times cooldown 2,700 vs 3,500 (1.30x) = **1.62x**, against
  0.61 measured.

### The Quaoar's 2x is firing cadence, confirmed twice

Its hit rate is exact and its damage per hit is exact, so nothing per-shot is wrong. Two independent
estimates of cadence agree:

| method | independent of | cadence vs nominal |
|---|---|---|
| report damage / damage-per-hit / hit rate | stream completeness | **53%** |
| stream volley count / elapsed | damage decoding | **51%** |

This retires the earlier 19.7-vs-12.4 shots/min disagreement: the 19.7 was wrong, built on a bad
per-ship clock denominator. **The Quaoar fires at ~52% of its 4,800 ms nominal cadence.**

Lock-on at `ENGAGE_MS 3000 + aim_ms 10000` = 13 s per acquisition covers 24-36% of the ~48% idle
(each Quaoar engaged 2-3 distinct targets). The remainder implies it re-acquires **more often than
once per distinct target**, i.e. it switches back and forth - target-selection RNG appearing a second
time, as retargeting cost rather than as armour. Charging `aim_ms` every cycle would give 32%
cadence, so it is not per-cycle either.

### Fix order

1. **Bug 1** cross-system cooldown (`SYSTEM_TYPE 6` auxiliary systems apply ship-wide) - well
   determined, explains the Taurus.
2. **Bug 4** NPC variant stats - well determined, cross-validated by two weapons.
3. **Bug 2** `TARGET_MODULE_TYPE` damage tiering - needs the module-tier table located.
4. **Bug 3** charge lock-on in `dpm_out`, not only in `timeline()` - needs the retargeting rate,
   and whether firing at aircraft resets it.

---

## Follow-up 5: bug 1 fixed and measured, and a per-hull bonus audit

### Retraction: field 10 of a stream row is the target's REMAINING HP, not a clock

Verified: it decreases monotonically per target (the non-monotonic cases are our own healed ships).
Anything built from it as a millisecond clock is void, which retires two tables published above - the
measured "median cycle" figures (Taurus 1,243 ms, Quaoar 4,526 ms) and the "implied firing uptime"
column (49% / 118% / 135% / 128%). **The Quaoar's ~52% cadence survives**, because both estimates of
it used report damage and packet `ts_us`, never field 10.

The upside: max field 10 per enemy instance gives true NPC max HP, and every NPC hull exceeds its
base hull by 30-41% (Indomitable 181,556 against 136,510; KCCPV2.0 73,488 against 52,040; 066
89,226 against 63,340; StarSweep 73,822 against 56,320). So NPC entries really are upgraded variants.
The 4-digit suffix does **not** decode safely, though - `571010401` is equally valid as a
`Tb_cfg_system_enhance` id (system `5710104` + index `01`), and no hull in `Tb_cfg_ship` carries the
measured HP. Bug 2's fix should therefore use the **measured** armour and HP, which are ground truth,
rather than a guessed suffix rule.

### Bug 1 fixed, and it moved the number it was predicted to move

Two defects, not one. `apply_upgrades` looped per system and, for each, **assigned** `base_damage`
from `table_damage` and **multiplied** `cd_ms`. Both are wrong once a system can reach a mount
outside its own group:

* assigning meant the last system to touch a mount discarded every earlier system's damage bonus;
* multiplying compounded cooldown across systems (5,000 x 0.70 x 0.85 = 2,975) where the measured
  rule is additive within one pool.

Rewritten to accumulate every applicable system's mods per mount and apply them once. A system whose
group hosts no weapon mount is treated as auxiliary and applies ship-wide - scoped deliberately to
EMPTY groups, since an auxiliary system that does host a weapon gives no evidence either way.

| | before | after | in-game |
|---|---|---|---|
| Taurus main cooldown | 3,500 | **2,750** | 2,700 |
| Taurus main damage | 420 | **455** | 525 |
| Quaoar rail | 4,800 / 540 | 4,800 / 540 | 4,800 / 562 |

Scored against the battle reports, the Taurus moves **0.61 -> 0.86** and **0.68 -> 0.90** with every
other hull unchanged. The residual is bug 3 (damage 455 against 525).

Also fixed: `tp_assign.plan` divided by a zero-cost upgrade rung. A free rung is simply worth taking,
so it now ranks as unbounded value per point. It only surfaced once auxiliary systems began yielding
value, because before then no free rung ever cleared `v > cur` to reach that line.

### `effect_audit.py --hull` - what one hull is leaving on the table

The fleet-wide survey answers "which effects does the engine model". It cannot answer "what is THIS
hull missing", which is where synergies live. The new per-hull mode walks every system, every
enhancement prefix and every effect, and flags two things nothing else did:

* **which system carries a bonus, and whether that system hosts a weapon** - a bonus on a weaponless
  system applies ship-wide. This is how the Taurus's `4050104` was found.
* **prefixes with no numeric effect row.** The Taurus has **6**, the Quaoar **3**. These are not
  harmless: `105`, `106`, `4050111`, `4050112` all carry `TARGET_MODULE_TYPE=204` and are the weapon
  damage ladders. The engine cannot read them, so it substitutes a flat +20% - bug 3, now enumerable
  per hull instead of inferred from one tooltip.

It also surfaced `EFFECT_WEAPON_DURATION_DEC0` param 50 on the Taurus's strategy prefix 9201 - a 50%
duration cut, unclassified and unmodelled, and duration is inside the cycle.

### Bug 5 (new): upgrades need per-MOUNT scoping, not per-group

Both the Taurus's mounts are group 01 (`14051`, `14052`), and both the Quaoar's are too (`14111`,
`14112`). Group scoping therefore cannot tell them apart - which is why the model gives the Quaoar's
turret the rail's 70% cooldown where the game gives it 30%. The upgrade string's first number in each
triple is an enhancement INDEX, and that is the likely discriminator.

Correction to follow-up 4: the Quaoar **does** have a `4110104` (type 6, group 4). It carries no
enhancement prefixes, which is the real reason its rail is unaffected - the earlier claim that the
system was absent was wrong, though the conclusion was right.

---

## Follow-up 6: the Mare Imbrium closed, and damage percentages are ADDITIVE

Chris supplied the fully-upgraded in-game readout: **519 damage, 1x1 shots, 5,400 ms cooldown, 5 s
lock-on**, built from Additional Charge (+40% damage, +20% cooldown, an extra shot), both damage
upgrades (+20%), both cooldown upgrades (-30%), Projectile Adjustment (+5%), and Firepower Assault
(first 120 s: +25% damage, -35% cooldown).

Stock from the tables: **315 damage, 6,000 ms cooldown, aim 5,000 ms** - the lock-on matches exactly.

### Percentages are additive on the stock value, confirmed twice

    315 x (1 + 0.40 + 0.20 + 0.05)        = 519.75   vs 519 displayed
    6,000 x (1 - 0.30 + 0.20)             = 5,400    vs 5,400 displayed

Multiplicative would give 555.7, which the display rules out. Adding Firepower Assault's +25% into
the **same additive pool** gives 315 x 1.90 = **598.5**, and that reproduces every measured
damage-per-hit exactly:

| target | armour | 598.5 - armour | measured |
|---|---|---|---|
| Indomitable Missile | 120 | 478.5 | **478** |
| Omni Ion / StarSweep | 110 | 488.5 | **488** |
| KCCPV2.0 Carrier | 80 | 518.5 | **518** |
| 066 Bombardment | 50 | 548.5 | **548** |

Both battles ran 109 s and 116 s, inside the 120 s window, so the strategy was up the whole fight.
This also re-confirms the inverted enemy armours from a second, independent direction.

### Fixed: a strategy with PREPARE_TIME 0 never recharges

Skill `9135` is `EFFECT_TIME 120000, PREPARE_TIME 0` - Chris's "first 120s". `strategy_uptime` tested
`if et and pt`, so a zero PREPARE_TIME read as *absent* and fell through to the 1/3 default. Such a
buff is not a duty cycle: it runs once from the opening, so its uptime is `min(1, EFFECT_TIME /
fight)`. Now 1.0 at the measured 109 s and 0.375 at the 320 s reference. `battle_report.py` sets
`M.FIGHT_MS` from each battle's real length so validation is apples-to-apples.

This fix is correct but did **not** move the hull, because the strategy's damage half is also
unreadable (below). Reported as such rather than claimed as a win.

### Why the engine still reads 378 / 4,200 instead of 519 / 5,400

| Chris's upgrade | prefix | what the engine sees |
|---|---|---|
| Additional Charge (+40% dmg, +20% cd, +1 shot) | `113` | **only** `CD_TIME_INC 20` |
| both damage upgrades (+20%) | `109`, `110` | `TARGET_MODULE_TYPE=202`, no numeric effect |
| both cooldown upgrades (-30%) | `301`, `302` | `CD_TIME_DEC 15` x2 - applied correctly |
| Projectile Adjustment (+5%) | `3130111` | `WEAPON_BASIC_ATTACK_ADD` **param 0** |
| Firepower Assault (+25% dmg) | `191350` | no numeric effect |

`CD_TIME_INC` **is** implemented. The reason the model shows -30% rather than -10% is subtler and
worse: **the TP planner refuses to buy Additional Charge at all**, because the only effect it can see
is a cooldown PENALTY. A greedy planner correctly rejects a pure downside. So the model is not
mis-computing Chris's build - it is choosing a different, worse build because one upgrade's upside is
invisible.

Three invisible magnitudes, one root cause: **the percentage is stored outside `EFFECT_PARAM`**, as
`TARGET_MODULE_TYPE` or as a param of 0. Closing that one gap fixes the Mare Imbrium, the Taurus's
residual, and the planner's refusal together.

Arithmetic check: model 378/4,200 = 5,400 nominal DPM; real in-battle 598.5/5,400 = 6,650, a factor
**1.23** against the measured shortfall of 1/0.77 = 1.30.

### Open: did Firepower Assault's cooldown apply?

Its damage demonstrably did. If its -35% cooldown also applied, the required firing cadence is
**57%**; if only the damage applied, **94%**. The 94% reading fits far better - the Mare Imbrium's
lock-on is 5 s against the Quaoar's 10 s, and the Quaoar measured ~52% cadence, so a hull with half
the lock-on sitting at 57% would be odd.

**The discriminating experiment is a battle longer than 120 s.** The strategy would lapse partway, so
average damage per hit would fall between 519 and 598.5 by a measurable amount. Both captures are
under the window, so they cannot separate the two readings.

---

## Follow-up 7: cmd 135 is the client's own battle log - durations and kills, free

Measuring the cooldown turned out to be possible after all, and it overturned the lean in follow-up 6.

### Weapon cycles, measured from PACKET timestamps

`ts_us` on each `NOTIFY_WORLD_BATTLE_DATA` message gives a 1,000 ms median clock - coarse, but ample
to separate 5,400 ms from 3,300. (The earlier attempt failed because it used field 10, which is
remaining HP.) Per attacker instance, gaps between that instance's deduplicated volleys:

| weapon | min gap | modal gaps | nominal | reading |
|---|---|---|---|---|
| Mare Imbrium main | 2,982 | **3 s x107, 4 s x109**, ~0 at 5-6 s | 5,400 | cycle ~3,500 |
| Quaoar rail | 4,008 | **5 s x174**, tail at 11-15 s | 4,800 | on cycle, then idle |

**So Firepower Assault's -35% cooldown DID apply, and it is MULTIPLICATIVE:**

    permanent, additive:        6,000 x (1 - 0.30 + 0.20) = 5,400
    strategy, multiplicative:            5,400 x 0.65     = 3,510   <- measured ~3,500

Additive into one pool would give 3,300 and a 70/30 split of 3s/4s gaps; the observed 50/50 fits
3,510. **This closes a question the repo has carried open** - whether a strategy's cut stacks like a
permanent one. It does not.

The caution about degenerate stacking was right to exist but aimed at the wrong thing: the Quaoar's
`9101` is `EFFECT_TIME 8000 / PREPARE_TIME 90000`, an **8.2% uptime**, which is exactly why it never
appears in the Quaoar's 5 s gaps. Strategy cooldown can now be priced, gated on real uptime.

The Quaoar's modal 5 s gap against a 4,800 nominal also confirms it fires **on cycle when it fires** -
its ~52% cadence is idle time, not a longer cycle.

### Mare Imbrium, re-ranked with the measured stats

DPM/CP at 5 CP:

| armour | 0 | 50 | 100 | 180 | 240 |
|---|---|---|---|---|---|
| model today (378 / 4,200) | 868 | 667 | 567 | 407 | 287 |
| in-game display (519 / 5,400) | 919 | 741 | 663 | 539 | 445 |
| **in battle, strategy up (598.5 / 3,510)** | **1,543** | **1,323** | **1,203** | **1,012** | **868** |

The model understates it **1.8x at armour 0 and 3.0x at armour 240**, and the shape is as important
as the level: 598.5 is large relative to armour, so it loses only 44% from armour 0 to 240 where the
Reliat A loses 91% by armour 100. It is a **two-phase hull** - 1,543 DPM/CP for 120 s, then 919.

Chris's framing of the strategy is the right one: it is worth a **fixed damage budget** per battle,
not a multiplier. 624 DPM/CP x 5 CP x 10 ships x 2 min = 62.4K damage at armour 0, and that figure
does not grow with fight length, so it matters more the shorter the fight. At the 5 Mare Imbrium
actually fielded, and at the measured ~61% cadence, the realised figure is nearer 19K.

### cmd 135: battle start, end and every kill, with timestamps

This is the workflow unlock. `cmd 135` is the client's own battle log:

* `event 8` / `event 10` - a battle opens against a named `cfg_npc_team`
* `event 9` - it closes; `36` enemy destroyed, `37` exp, `18` reward
* **`event 12` - a KILL**, `param` = `[killer_sid, victim_sid, count]`

On battle8 it yields **109 s and 116 s**, Chris's 1:49 and 1:56 exactly, totalling his 3:45. Two
battles can be open at once, so starts and ends must be walked in sequence rather than matched
nearest-first. `battle_report.py` now derives `--secs` from this automatically; passing it by hand is
only an override.

The kills also date every **forced retarget** - an enemy death costs its attackers their lock. Battle
1 had five, at t+60, 62, 81, 98 and 109 s. Each Quaoar engaged 2-3 distinct targets, so 2-3 forced
re-acquisitions at 13 s each is 26-39 s of a 109 s fight, against the ~48% idle measured. That is the
right magnitude and matches Chris's prediction that retargeting happens more than it looks because
ships move and die.

---

## Follow-up 8: the battle REPLAY is a separate fetch, and it is far richer

Captured 2026-10-20 as `report18.pcapng` (21.9 MB; only 153 KB of it on port 8001 - the bulk is
unrelated traffic). Two reports with replays.

### It is its own request, fetched on demand

Downloading the battle report is **not** enough. Opening a replay issues two new commands:

| cmd | request | response |
|---|---|---|
| **5852** | `[battle_id]` | replay index: `[1, duration_ms, 1, [...], [events]]` |
| **5853** | `[battle_id, 0]` | **the full replay**, ~262 KB |

Both are plain `zlib3` bodies on port 8001, so `ilcap.py` already decodes them. Because they are
fetched **on demand rather than streamed live, a battle no longer has to be captured while it
happens** - start the capture, open the replay, done. That removes the hardest part of the workflow.

### What cmd 5853 contains

`[0, 0, duration_ms, teams, events, samples, kills]`

* **`b[2]`** - duration in ms, authoritative (162,200 and 166,100 in this capture).
* **`b[3]`** - per-team, per-ship INITIAL state: each ship's modules as
  `[module_id, slot_code, current_target, ..., cooldown_ms, ...]` plus its strategy list, e.g.
  `[[9216, 0, 3160101]]`. So cooldowns and the fitted strategies are readable directly.
* **`b[4]`** - **3,592 events at 100 ms resolution.** This is the sub-second shot timing the packet
  clock could only quantise to 1,000 ms.
* **`b[5]`** - **cumulative damage per hull, sampled every 5 s** (33-34 samples). A damage-RATE curve
  per hull for the whole battle.
* **`b[6]`** - the kill log, same `[killer_sid, victim_sid, n]` shape as cmd 135 event 12.

**Cross-validated:** `b[5]`'s final cumulative damage equals the report's kind-0 totals exactly -
Quaoar 122,406 vs 122,406, Winged Hussar 83,060 vs 83,060, Reliat A 28,253 vs 28,253, Eris 0.99.

### Both battles run past 120 s, but carry no Mare Imbrium

162 s and 166 s, so the Firepower Assault phase change is testable in principle - but the roster is
Taurus Pulse x10, **Reliat A x9**, **Zircon x2**, Eris Heavy Cannon x10, Winged Hussar A x10, Quaoar
Railgun x10, plus 4 escort craft. No Mare Imbrium, so that specific test still needs a capture with
one fielded.

### The Reliat A's 36 s cycle is visible in the rate curve

Its per-5s damage goes 0, 24k, 24k, 30k, 1k, 1k, 1k, 1k, 10k, 26k, 24k, 12k, 1k... - bursts roughly
every 36 s with near-zero between, which is exactly its 16-shot / 36 s torpedo cycle. The rate curve
is therefore good enough to read a weapon's cycle straight off.

### Actionable: the 2 Zircons contributed almost nothing

**310 damage across a 162 s battle**, confirmed independently by replay and report. Its escort boats
(`11001`, 4 of them) added 9,329. So the whole Zircon system delivered 9,639 for 2 ships over 162 s -
**about 223 DPM/CP**, against 1,489 damage/CP for the Taurus Pulse.

This is the right caveat on the armour curves from 2026-10-19, which projected ~860 DPM/CP for a
Zircon A at 53 TP: that is a **ceiling at full investment**, and the hull actually fielded is the base
Zircon at essentially no tech. Nearly all of its real output is the escort boats, not the hull.

---

## Follow-up 9: the Zircon A's tech tree, and why the planner cannot read it

Chris described the tree from in-game: 2 points into "lockon frequency" opens the two cooldown
upgrades, or 18 points into the "mobile firepower" strategy opens **both** the cooldown and the damage
upgrades; the main hull cannon is a separate module that will not see points at this level; and the
main weapon is **anti-aircraft at base**, which cleared the enemy air before it could turn on the
ships. Every part of that is in the tables, and it exposes more than it fixes.

### The tree, grounded

**System `3190201`** - the escort boats (module `11252`, uav `11002`):

| Chris's name | prefix | effect | cost | engine |
|---|---|---|---|---|
| lockon frequency | `3101` | `INIT_PREPARE_TIME_DEC 70` | 2 | applied to `aim_ms`, **worth 0** |
| the 2x cooldown upgrades | `3109`, `3102` | `CD_TIME_DEC 20` + `FLIGHT_TIME_DEC 20` | 2 | cooldown yes, **flight no** |
| the damage upgrades | `3111`, `3107` | **no numeric effect** | 2 | **invisible** |
| (accuracy) | `3116`, `3103` | `HIT_RATE_INC 20` | 2 | modelled |
| mobile firepower | `9253` | `AVOID_PROB_INC 25` + `CD_TIME_DEC 25`, 60 s window | **18** | strategy cd not applied |

**System `3190202`** - the main cannon (module `11254`, 500 dmg ballistic), a separate branch:
`109` damage (no numeric effect), `205` hit-rate-by-type (modelled), `301`/`306` `CD_TIME_DEC 15`
(modelled), `8307` crit via **effect 12031 `EFFECT_SYSTEM_BURST_DAMAGE`** - which is **not** the 12030
the engine models, so unmodelled.

### What the model cannot see on this one hull

The lock-on fix, every damage upgrade on both branches, the crit, half of each cooldown upgrade
(`FLIGHT_TIME_DEC` has **zero** references in matrix.py although `flight_before_ms`/`flight_after_ms`
are inside the cycle), and the strategy's cooldown. That is most of the tree.

**The lock-on case is the sharpest.** `INIT_PREPARE_TIME_DEC` is correctly applied to `aim_ms` - and
`aim_ms` never reaches `dpm_out`, so a 70% cut to lock-on for **2 points** prices at exactly zero. It
is the same root cause as the Quaoar mystery: lock-on is the dominant cadence loss (10 s of lock-on
costs the Quaoar ~48% of its output), and the model charges it only in the duel path. So the engine
cannot see the problem **or** the cheapest fix for it.

### Prerequisite gates are not in the data

`Tb_cfg_system_enhance` has `UNLOCK_TYPE`, `UNLOCK_COST_RARITY`, `ENHANCE_LIMIT_TAG` and
`ADJUST_ENHANCE_INDEX`, but none of them encode "prefix X requires prefix Y" - on the Zircon A they
appear only on free rows and adjust entries. So the planner treats every prefix as independently
purchasable, which is wrong in two directions at once:

* **optimistic** - it buys cheap upgrades that are actually gated behind something unbought;
* **pessimistic** - an 18-point unlock with no immediate marginal return is invisible to a greedy
  value-per-point search, so the planner will never find the branch that opens both upgrade lines.

### The AA role, and why the Zircon read as 310 damage

The replay settles it. The **first kill of the battle is at t+25.5 s: the Zircon's escort boat killing
an enemy aircraft**, before any ship dies. The Taurus clears three more at t+40.6, 52.0 and 70.7, so
all enemy air is gone inside 71 s, and the Quaoar only starts on ships at t+82.6. That value never
appears in a DPM/CP ranking - enemy craft are 5,200 HP, so removing them costs almost no damage.

The 310 damage is also narrower than it looked. Splitting the two mounts at stock cycle over 162 s
with 2 ships:

| mount | stock cycle | potential | measured |
|---|---|---|---|
| escort boats `11252` -> craft `11001` | 8,000 + 3,000 dur, aim 5,000 | ~5,600 | **9,329** |
| main cannon `11254` | 20,000, aim 0 | ~7,960 | **310** |

So the boats **beat** their stock potential, and the anomaly is entirely the main cannon, which
delivered about 4% of its - roughly a single hit in 162 seconds. Chris's note that the cannon is a
separate module with no points explains why it is weak, not why it barely fired; range or target
gating is the open question.

---

## Follow-up 10: the Quaoar closed - retargeting costs 5.8 s, measured

### Correction: the lock-on ladder is 14%/level, not 70% for 2 points

Chris: *"I show only 14% lockon reduction for each upgrade so 5 of them is a total of 70%."* Correct,
and follow-up 9's "70% for 2 points" was wrong by 6x - the full 70% costs 2+2+2+3+3 = **12 points**.
`3101` carries `EFFECT_PARAM 70` with no per-level ladder, and the rule is that **the param is the
level-5 total**: `system_mods` already scales it `level / max_level`, so level 1 gives exactly 14%.
The rule cross-checks on two other rows - `301`/`306` are `CD_TIME_DEC 15` -> 3%/level, matching
Chris's "-3% cooldown", and the blank damage rows are the 2%/level measured earlier on his Hussar.

The prerequisite rule is also now specified rather than hunted for: **at least one level in a
prerequisite opens everything behind it**, and a strategy is a single level, which is why the Zircon
A's mobile firepower needs all 18 points at once. That is implementable in the planner directly.

### Relocks, counted

From the replay's type-36 shot log (`[time_ms, 36, attacker, slot, target, shots, hits, ...]` at
100 ms resolution): **7.6 target switches per ship over 162 s**, with ~10 type-1 acquisitions.
Chris's "maybe 10 relocks" was well calibrated.

### What a relock actually costs, measured

Comparing shot-to-shot gaps that follow a target switch against those that do not:

| slot | gap, no switch | gap after switch | extra |
|---|---|---|---|
| 101 | 6,007 ms | 11,784 ms | **+5,777** |
| 102 | 5,256 ms | 5,319 ms | **+63** |
| 202 | 7,341 ms | 13,243 ms | **+5,903** |

Slot 102 pays **nothing**, which is the absorbed case - its lock (6,000) is shorter than its cycle
(7,800), so the re-lock runs under the cooldown. Slot 101's predicted cost of `aim - cycle` =
10,000 - 4,800 = 5,200 ms lands against **5,777 measured**. So the overlap rule holds: a relock costs
roughly `max(0, aim_ms - cycle_ms)`, not the whole lock.

### This closes the Quaoar's 2x

7.6 switches x 5.8 s = 44 s lost to retargeting, plus 13 s for the opening `ENGAGE_MS + aim_ms`, over
a 109 s battle = **52% idle**, against the **~48% measured**. The Quaoar's entire cadence gap is
forced retargeting - which is what Chris predicted ("retargeting happens more often than it might
appear.. ships move around or die"), now with a number on it.

Every component of that hull is therefore accounted for: hit rate exact, damage per hit exact,
cooldown exact, and the 2x is idle time from relocking.

### Is a lock-on level worth buying? Only on one weapon in seven

Chris takes it last, and he is right almost everywhere. One 14% level recovers 14% of the blocked
time, against +2% damage or -3% cooldown per level:

| weapon | aim | cycle | ratio | blocked over the fight | lock L1 | verdict |
|---|---|---|---|---|---|---|
| **Quaoar rail** | 10,000 | 4,800 | **2.08** | **52 s** | **4.5%** | **beats +2% damage** |
| Quaoar turret | 6,000 | 7,800 | 0.77 | 0 | 0% | take it last |
| Taurus main | 4,000 | 2,750 | 1.45 | 12.5 s | 1.1% | take it last |
| Mare Imbrium main | 5,000 | 4,200 | 1.19 | 8 s | 0.7% | take it last |
| Reliat A torpedo | 0 | 36,000 | - | 0 | 0% | take it last |
| Zircon escort boats | 5,000 | 7,800 | 0.64 | 0 | 0% | take it last |

**The rule: lock-on only pays where `aim_ms` exceeds the cycle.** That is one weapon on this account -
the Quaoar railgun, where retargeting burns 27% of the battle. Everywhere else the re-lock hides
inside the cooldown and the 2% damage is the better buy, exactly as Chris plays it.
