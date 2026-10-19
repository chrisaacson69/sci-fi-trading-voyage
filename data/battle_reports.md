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
