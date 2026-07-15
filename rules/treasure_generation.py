"""Rogue Trader -- Procedural Treasure Generation
==================================================

Implements the RT14 Stars of Inequity Ch.II "Treasure Generator" cascade
(pp.83-92), independent of any GPL-licensed source -- written from the book
and cross-checked structurally against TiLT's RogueTraderGeneratorTools
TreasureNode.cs for fidelity.

Cascade:
  1. Origin (Table 2-30, 1d10): Finely Wrought / Ancient Miracle /
     Alien Technology / Cursed Artefact
  2. Type   (RT14 p.83 selector, 1d10): Melee / Ranged / Armour /
     Gear & Tools / Ship Component  -> rolls on Table 2-25..2-29
  3. Origin-specific addenda:
       Finely Wrought   -> automatic Best Craftsmanship + 1 Quirk (Table 2-35)
       Ancient Miracle  -> Craftsmanship (Table 2-34) at +3 (cap 10)
                            + Miracles of the Dark Age (Table 2-31)
                            + 2 Quirks (Table 2-35, no duplicates)
       Alien Technology -> Craftsmanship (Table 2-34) normal
                            + Xenos Construction (Table 2-32)
                            + 1 Quirk (+1 more if Ramshackle weapon)
       Cursed Artefact  -> Craftsmanship (Table 2-34) normal
                            + Mark of the Curse (Table 2-33) + 1 Quirk

Usage:
    from rules.treasure_generation import generate_treasure
    t = generate_treasure(rng=random.Random(42))
    # -> {"origin": "Ancient Miracle", "type": "Power Axe", ...}

Source: RT14 Stars of Inequity (FFG, 2012), Chapter II pp.83-92.
"""

from __future__ import annotations
import json
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = ROOT / "data" / "tables" / "treasure"

_TABLES: Dict[str, Dict] = {}


def _load(table_id: str) -> Dict:
    if table_id in _TABLES:
        return _TABLES[table_id]
    path = TABLES_DIR / f"{table_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Treasure table not found: {path}")
    _TABLES[table_id] = json.load(open(path))
    return _TABLES[table_id]


def _roll(rng: random.Random, sides: int = 10) -> int:
    return rng.randint(1, sides)


def _lookup(rows: List[Dict], r: int) -> Optional[Dict]:
    for row in rows:
        if row.get("range_min", 1) <= r <= row.get("range_max", 9999):
            return row
    return None


# ---------------------------------------------------------------------------

def _roll_origin(rng: random.Random) -> Dict:
    table = _load("table_2_30_origin")
    r = _roll(rng)
    row = _lookup(table["rows"], r)
    return {
        "name": row["name"],
        "cascade": row["cascade"],
        "roll": r,
        "_source": table["_source"],
    }


def _roll_type(rng: random.Random) -> Dict:
    table = _load("table_treasure_type")
    r = _roll(rng)
    row = _lookup(table["rows"], r)
    return {
        "name": row["name"],
        "sub_table": row["sub_table"],
        "roll": r,
        "_source": table["_source"],
    }


def _roll_item(rng: random.Random, sub_table_id: str) -> Dict:
    table = _load(sub_table_id)
    r = _roll(rng)
    row = _lookup(table["rows"], r)
    out = {
        "name": row["name"],
        "roll": r,
        "_source": table["_source"],
    }
    if "profile" in row:
        out["profile"] = row["profile"]
    if "_cross_ref" in row:
        out["_cross_ref"] = row["_cross_ref"]
    return out


def _roll_craftsmanship(rng: random.Random, bonus: int = 0) -> Dict:
    table = _load("table_2_34_craftsmanship")
    r = _roll(rng) + bonus
    capped = min(r, 10)  # per RT14 p.86 Archeotech rule: max 10
    row = _lookup(table["rows"], capped)
    return {
        "name": row["name"],
        "roll": r,
        "capped_at": capped if r > 10 else None,
        "bonus_applied": bonus,
        "_source": table["_source"],
    }


def _roll_quirk(rng: random.Random, exclude: Optional[List[str]] = None) -> Dict:
    table = _load("table_2_35_quirks")
    exclude = exclude or []
    for _attempt in range(20):
        r = _roll(rng)
        row = _lookup(table["rows"], r)
        if row["name"] not in exclude:
            return {"name": row["name"], "roll": r, "_source": table["_source"]}
    # Fallback if 20 attempts somehow collide (unreachable with d10 + ~2 exclusions)
    return {"name": row["name"], "roll": r, "_source": table["_source"]}


def _roll_miracle(rng: random.Random,
                  collected: Optional[List[Dict]] = None,
                  allow_multiple_blessings: bool = True) -> List[Dict]:
    """Roll Table 2-31. On 10 (Multiple Blessings), roll twice more
    (suppressing further 10s and rejecting duplicates)."""
    table = _load("table_2_31_miracles_of_the_dark_age")
    collected = collected if collected is not None else []
    sides = 10 if allow_multiple_blessings else 9
    r = rng.randint(1, sides)
    row = _lookup(table["rows"], r)
    if row.get("_recursive"):
        # Multiple Blessings: roll twice, no further recursion, no duplicates
        first = _roll_miracle(rng, collected, allow_multiple_blessings=False)
        second = _roll_miracle(rng, first, allow_multiple_blessings=False)
        # Dedupe within this group
        names = set()
        dedup: List[Dict] = []
        for m in first + second:
            if m["name"] not in names:
                names.add(m["name"])
                dedup.append(m)
        # If dedupe left only one, roll one more to reach 2
        while len(dedup) < 2:
            extra = _roll_miracle(rng, dedup, allow_multiple_blessings=False)
            for m in extra:
                if m["name"] not in names:
                    names.add(m["name"])
                    dedup.append(m)
                    break
        return dedup[:2]
    collected.append({
        "name": row["name"],
        "page": row.get("_page"),
        "description": row.get("description", ""),
        "roll": r,
        "_source": table["_source"],
    })
    return collected


def _roll_xenos_construction(rng: random.Random) -> Dict:
    table = _load("table_2_32_xenos_construction")
    r = _roll(rng)
    row = _lookup(table["rows"], r)
    return {
        "name": row["name"],
        "page": row.get("_page"),
        "description": row.get("description", ""),
        "roll": r,
        "_special": row.get("_special"),
        "_source": table["_source"],
    }


def _roll_mark_of_the_curse(rng: random.Random) -> Dict:
    table = _load("table_2_33_mark_of_the_curse")
    r = _roll(rng)
    row = _lookup(table["rows"], r)
    return {
        "name": row["name"],
        "page": row.get("_page"),
        "description": row.get("description", ""),
        "roll": r,
        "_source": table["_source"],
    }


# ---------------------------------------------------------------------------

def generate_treasure(rng: random.Random,
                      forced_origin: Optional[str] = None) -> Dict:
    """Generate one artefact per RT14 Ch.II.

    Args:
        rng:           Seeded RNG.
        forced_origin: Optional override (e.g. "Alien Technology" when generating
                       finds from an Eldar ruin per Table 2-3 narrative effects).
    Returns:
        Dict with keys: origin, type, item, craftsmanship, quirks, and one of
        {miracles, xenos_construction, mark_of_the_curse} depending on origin.
    """
    origin = _roll_origin(rng)
    if forced_origin:
        origin = {"name": forced_origin,
                  "cascade": {"Finely Wrought": "skilled_craftsmanship",
                              "Ancient Miracle": "archeotech",
                              "Alien Technology": "xenos_tech",
                              "Cursed Artefact": "twisted_omens"}[forced_origin],
                  "roll": None, "_source": "forced", "_forced": True}
    type_pick = _roll_type(rng)
    item = _roll_item(rng, type_pick["sub_table"])

    out: Dict[str, Any] = {
        "origin": origin,
        "type": type_pick,
        "item": item,
        "quirks": [],
    }

    if origin["cascade"] == "skilled_craftsmanship":
        # Finely Wrought: automatic Best craftsmanship + 1 Quirk
        out["craftsmanship"] = {"name": "Best", "_source": "src_rt14_stars_p85", "_automatic": True}
        out["quirks"].append(_roll_quirk(rng))
    elif origin["cascade"] == "archeotech":
        # Ancient Miracle: Miracles, craftsmanship +3 (cap 10), 2 Quirks
        out["miracles"] = _roll_miracle(rng)
        out["craftsmanship"] = _roll_craftsmanship(rng, bonus=3)
        q1 = _roll_quirk(rng)
        q2 = _roll_quirk(rng, exclude=[q1["name"]])
        out["quirks"] = [q1, q2]
    elif origin["cascade"] == "xenos_tech":
        # Alien Technology: Xenos Construction + craftsmanship + 1 Quirk
        # (+ another Quirk if Ramshackle + weapon)
        out["xenos_construction"] = _roll_xenos_construction(rng)
        out["craftsmanship"] = _roll_craftsmanship(rng)
        out["quirks"].append(_roll_quirk(rng))
        if (out["xenos_construction"].get("_special") == "weapon_extra_quirk"
                and type_pick["name"] in ("Melee Weapon", "Ranged Weapon")):
            out["quirks"].append(_roll_quirk(rng, exclude=[out["quirks"][0]["name"]]))
    elif origin["cascade"] == "twisted_omens":
        # Cursed Artefact: Mark of the Curse + craftsmanship + 1 Quirk
        out["mark_of_the_curse"] = _roll_mark_of_the_curse(rng)
        out["craftsmanship"] = _roll_craftsmanship(rng)
        out["quirks"].append(_roll_quirk(rng))

    return out


def generate_treasure_hoard(rng: random.Random, count: int) -> List[Dict]:
    return [generate_treasure(rng) for _ in range(count)]


if __name__ == "__main__":
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    rng = random.Random(seed)
    for i, t in enumerate(generate_treasure_hoard(rng, n), 1):
        print(f"=== Treasure {i} ===")
        print(json.dumps(t, indent=2, default=str))
