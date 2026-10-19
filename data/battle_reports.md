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
