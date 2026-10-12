#!/usr/bin/env python3
"""Parse an account's blueprint list into data/blueprints/<account>.csv.

Input: data/blueprints/<account>_raw.txt, Chris's in-game list, kept verbatim. One entry per line,
fields separated by two or more spaces (or tabs):

    <name>   <value>   [<class>]        or        <class>   <name>   <value>

  * <name> is the family plus a variant letter, A-D (KCCPA, IO A). A is the base hull, B-D the
    variants, in ship-id order (Taurus A = id 40501). No letter = a single-variant family.
  * <value>, a whole number: the family's available TP; the variant is owned (1 BP).
    Variants of a family share one TP pool, so count it once per family.
  * <value>, a decimal: the variant is NOT owned yet; the decimal is the unlock progress (0 BP).
  * <value>, TP/modules (capital ships): TP awarded, then modules owned. Repeat picks give modules,
    so BP = 1 + modules beyond the base set (3 for the Solar Whale and Thunderbolt, 2 for the rest).
  * <class>, optional, first or last: FF, DD, CA, BC, CV, AUX, or F/Fighter and C/Corvette for craft.
    Without it, the type comes from KNOWN_TYPES (families already recorded in this repo).

Usage:  py -3 blueprints.py dela5hades
"""
from __future__ import annotations

import csv
import io
import re
import sys
from collections import OrderedDict
from pathlib import Path

DIR = Path(__file__).resolve().parent / "data" / "blueprints"
CAPITAL_BASE_MODULES = {"Solar Whale": 3, "Thunderbolt": 3}  # every other capital starts with 2
SPELLING = {"Mere": "Mare"}                                # MereSeren/MereTranq are the Mare families
CLASS_ALIASES = {"FIGHTER": "FT", "F": "FT", "CORVETTE": "CO", "C": "CO"}
CLASSES = {"FF", "DD", "CA", "BC", "CV", "AUX", "FT", "CO", *CLASS_ALIASES}
# hull type by family (variants never change type): the mobile account's roster, data/craft.csv,
# and Chris's answers 2026-10-12. FT fighter, CO corvette.
KNOWN_TYPES = {
    "Solar Whale": "CV", "FSV830": "AUX", "Swordbearer": "BC", "SpearOUranus": "BC", "CtG": "BC", "ST59": "BC",
    "Predator": "CA", "IO": "CA", "CAS066": "CA", "Ranger": "CA", "Jaeger": "CA", "KCCP": "CA",
    "Taurus": "DD", "Guardian": "DD", "AC721": "DD", "Eris1": "DD", "WingHuss": "DD", "Aladabra": "DD",
    "Ceres": "DD", "Quaoar": "DD",
    "NOMA": "FF", "MareImb": "FF", "MareSeren": "FF", "MareNubium": "FF", "MareTranq": "FF", "Ruby": "FF",
    "Reliat": "FF", "Carilion": "FF", "FG300": "FF", "Zircon": "FF", "Xeno": "FF", "Inoscrancevia": "FF",
    "CVT800": "CO", "CVM011": "CO", "VoidElfin": "CO", "NebChase": "CO", "CellDefender": "CO", "RedBeast": "CO",
    "SilentAss": "CO", "CV110033": "CO",
    "AT021": "FT", "Vitas A021": "FT", "Strix": "FT", "SC002": "FT", "BalAnder": "FT", "Bullfrog": "FT",
    "Janbiya": "FT", "Sandrake": "FT", "Mistral": "FT", "Hayreddon L": "FT",
}
CRAFT = {"FT", "CO"}
NOTES = {
    "CtG": "Constantine the Great (ConstTGreat on the mobile account)",
    "CV110033": "CV-11003 (II003) in data/craft.csv",
    "BalAnder": "Balance Anderson in data/craft.csv", "SilentAss": "Silent Assassin (the Ray) in data/craft.csv",
    "NebChase": "NebulaChaser in data/craft.csv", "CellDefender": "Cellular Defender in data/craft.csv",
    "VoidElfin": "Void Elfin in data/craft.csv", "Void Elfin": "Void Elfin in data/craft.csv",
    "Levy9": "SLevi9 in data/craft.csv", "NebChaser": "NebulaChaser in data/craft.csv",
    "CV11003": "CV-11003 (II003) in data/craft.csv", "Tempel": "Tempel (Intf/Alert) in data/craft.csv",
    "HaleBopp": "HaleBopp (MR/Dock) in data/craft.csv",
}


def parse(lines):
    rows, family_tp = [], OrderedDict()
    for line in lines:
        if not line.strip():
            continue
        fields = [f.strip() for f in re.split(r"\s{2,}|\t", line.strip())]
        if len(fields) >= 3 and fields[0].upper() in CLASSES:      # class first
            given_class, name, value = fields[0].upper(), fields[1], fields[2]
        else:                                                      # class last, or none
            name, value = fields[0], fields[1]
            given_class = fields[2].upper() if len(fields) > 2 else ""
        fixed = name
        for wrong, right in SPELLING.items():
            if fixed.startswith(wrong):
                fixed = right + fixed[len(wrong):]
        m = re.match(r"^(.*?)\s?([A-D])$", fixed)
        family, variant = (m.group(1), m.group(2)) if m else (fixed, "")
        hull_type = CLASS_ALIASES.get(given_class, given_class) or KNOWN_TYPES.get(family, "")
        r = {"family": family, "variant": variant, "name_as_given": name,
             "kind": "craft" if hull_type in CRAFT else "hull", "type": hull_type, "owned": "", "unlock_pct": "",
             "tp": "", "modules": "", "base_modules": "", "modules_earned": "", "bp_earned": "",
             "notes": NOTES.get(family, "")}
        if name != fixed:
            r["notes"] = (r["notes"] + "; " if r["notes"] else "") + f"spelled '{name}' in the list"
        if "/" in value:
            tp, mods = map(int, value.split("/"))
            base = CAPITAL_BASE_MODULES.get(family, 2)
            r.update(kind="capital", owned="y", tp=tp, modules=mods, base_modules=base,
                     modules_earned=mods - base, bp_earned=1 + mods - base)
            family_tp[family] = tp
        elif "." in value:
            r.update(owned="n", unlock_pct=round(float(value) * 100), bp_earned=0)
        else:
            tp = int(value)
            r.update(owned="y", tp=tp, bp_earned=1)
            if family_tp.setdefault(family, tp) != tp:
                raise ValueError(f"{family}: variants disagree on TP ({family_tp[family]} vs {tp})")
        rows.append(r)
    return rows, family_tp


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__)
        return 2
    account = argv[0]
    rows, family_tp = parse((DIR / f"{account}_raw.txt").read_text(encoding="utf-8").splitlines())
    buf = io.StringIO()
    w = csv.DictWriter(buf, list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    (DIR / f"{account}.csv").write_text(buf.getvalue(), encoding="utf-8")
    untyped = sorted({r["family"] for r in rows if not r["type"]})
    print(f"{account}: {len(rows)} entries, {sum(r['owned'] == 'y' for r in rows)} owned, "
          f"{sum(r['owned'] == 'n' for r in rows)} in progress; {sum(r['bp_earned'] for r in rows)} BP; "
          f"{sum(family_tp.values()):,} TP over {len(family_tp)} families")
    if untyped:
        print("no type for:", ", ".join(untyped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
