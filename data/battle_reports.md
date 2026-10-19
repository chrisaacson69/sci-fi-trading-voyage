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

### The event stream reports damage at 2x

Summing the stream's damage field per hull and comparing against the report's kind 0 gives **exactly
2.00 for all seven hulls** (1.98 for the Quaoar, partial capture). Shot counts are *not* doubled, so
this is a half-unit encoding in the damage field, not duplicated events. **Halve stream damage
before using it.** The report is the authority: it matches the in-game numbers to the digit.

### Recalibrated per-weapon truth

Ownership in the stream was never actually ambiguous — field 1 is the attacker **instance id**, which
resolves it completely. The earlier "codes are reused by both fleets" caveat applies only to the
code, and keying on it alone was the mistake.

| weapon | real dmg/hit | model base | real cycle | model cycle |
|---|---|---|---|---|
| Quaoar rail | 229 | 540 | 4,526 ms | 4,800 ms |
| Taurus main | 235 | 420 | **1,243 ms** | 3,500 ms |
| Mare Imbrium main | 250 | 378 | 2,079 ms | 4,200 ms |
| Reliat main | 76 | 120 | 1,424 ms | 17,600 ms / 5 repeats |

### The two outliers have different causes

* **Quaoar (model 2x high): `shots_per_action` double-counts damage.** In-game shows the rail at
  **562 damage, 4,800 ms, 2 shots**, and 562/2 = 281 less ~50 armour = 231 against **229 measured** —
  so the table damage is **per volley**, and the model applies it per shot and then multiplies by the
  shot count. The cycle was never wrong: 4,800 in-game, 4,526 measured, 4,800 modelled.
* **Taurus (model 0.6x low): the cycle is 2.8x too long.** Damage is close; the model has 3,500 ms
  against 1,243 ms measured.
* **Quaoar's tiny railgun (model 5x high): armour flooring plus a short cycle.** Real 4.25 damage per
  hit against a modelled 72, and the in-game cycle is 6 s duration + 4.2 s cooldown = **10.2 s**
  against the modelled 7,800 ms.

Cooldown stacking is **not** implicated in any of these, and neither is the prefix-115 accuracy
penalty. Both earlier hypotheses are dead.

### Still open

* Whether the per-volley reading of damage generalises beyond the two-shot railgun. The Mare Imbrium's
  secondary also has `shots_per_action = 2` and reads 0.97, which is noise at 10 damage.
* Why the model's cycle is long for the Taurus and Mare Imbrium but right for the Quaoar.
* sid 57101 is named **Omni Ion Cannon** here but **StarSweep** in-game — a name-mapping discrepancy.
* Chris notes a small real loss from lock-on timing when targets switch; minor at 5 ships.
