"""Rogue Trader -- Procedural Starship Generation
=====================================================

Implements per-race hull selection for ship hulks, drawing on:
  * RT01 Core Rulebook       -- Human ships (pp.194-209)
  * RT04 Into the Storm      -- Human ships (pp.151-153)
  * RT09 Battlefleet Koronus -- Human, Ork, Eldar, Rak'Gol, Chaos Reaver hulls
  * RT12 The Soul Reaver     -- Dark Eldar hulls

Scope: hull selection only (race + hull name + ship class + book/page +
upgrades). Full per-ship component / weapon / power-and-space build-out is
intentionally left out -- it's a separate codification project that touches
RT01 Ch.IX (the starship construction rules) end-to-end and would multiply
this file's size 5-10x. For Starship Graveyard hulks this hull-level data
is sufficient (a derelict's components are usually long gone anyway).

Generator surface:
  * generate_starship_hulk(rng, race=None, integrity=None) -- one hulk
  * generate_pirate_fleet(rng, count=8)   -- a Pirate Den fleet per RT14 p.10
  * pick_random_species(rng)              -- the d14 race selector

Cross-checked structurally against TiLT's StarshipTools.cs.

Used by rules/star_system_generation.py:generate_starship_graveyard() to
populate the `hulks` array (replacing the Tier 2 _placeholder records).
"""

from __future__ import annotations
import json
import random
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = ROOT / "data" / "tables" / "starships"

_TABLES: Dict[str, Dict] = {}

INTEGRITY_LEVELS = ["Shattered", "Heavily Damaged", "Damaged", "Mostly Intact"]


def _load(table_id: str) -> Dict:
    if table_id in _TABLES:
        return _TABLES[table_id]
    p = TABLES_DIR / f"{table_id}.json"
    if not p.exists():
        raise FileNotFoundError(f"Starship table not found: {p}")
    _TABLES[table_id] = json.load(open(p))
    return _TABLES[table_id]


def _d100(rng): return rng.randint(1, 100)
def _d10(rng):  return rng.randint(1, 10)


def _lookup(rows, r):
    for row in rows:
        if row.get("range_min", 1) <= r <= row.get("range_max", 9999):
            return row
    return None


def _lowest_of_two_d100(rng):
    """Per TiLT and BFK: many ship rolls take lowest of two d100 to bias
    toward smaller / earlier-listed ships."""
    a = _d100(rng); b = _d100(rng)
    return min(a, b)


# ----------------------------------------------------------------------------

def pick_random_species(rng) -> str:
    table = _load("table_ship_race_selector")
    r = rng.randint(table["rows"][0]["range_min"], table["rows"][-1]["range_max"])
    row = _lookup(table["rows"], r)
    return row["species"]


def _roll_ork_upgrade(rng, sub_key: str, exclude: List[str]) -> str:
    table = _load("table_ship_ork_upgrades")["subtables"][sub_key]
    for _attempt in range(20):
        r = _d10(rng)
        row = _lookup(table, r)
        if row["name"] not in exclude:
            return row["name"]
    return row["name"]  # fallback


def _apply_upgrades(rng, upgrades_spec: List[str]) -> List[str]:
    """upgrades_spec is a list of `sub_key:count` strings (e.g.
    'ork_small_ship_upgrades:1'). Returns a flat list of upgrade names."""
    out: List[str] = []
    for spec in upgrades_spec:
        sub_key, _, count = spec.partition(":")
        count = int(count) if count else 1
        for _ in range(count):
            out.append(_roll_ork_upgrade(rng, sub_key, out))
    return out


def _gen_human(rng, integrity: Optional[str], with_its: bool = True) -> Dict:
    """Human ship per TiLT's GenerateRandomHumanShip: 30% chance to redirect to
    Into the Storm sub-table if ItS is enabled; otherwise main table."""
    use_its = with_its and (_d100(rng) <= 30)
    if use_its:
        table = _load("table_ship_hulls_human_into_the_storm")
        chose_its = True
    else:
        table = _load("table_ship_hulls_human")
        chose_its = False
    r = _lowest_of_two_d100(rng)
    row = _lookup(table["rows"], r)
    return {
        "race": "Human",
        "ship_name": row["name"],
        "ship_class": row["class"],
        "book": row["_book"],
        "page": row["_page"],
        "upgrades": [],
        "integrity": integrity,
        "_roll": r,
        "_book_source_chosen_by_random_30pct_into_the_storm": chose_its,
        "_source": table["_source"],
    }


def _gen_simple(rng, race: str, table_id: str, integrity: Optional[str]) -> Dict:
    """For races whose hull table is a simple d100 lookup with no upgrades."""
    table = _load(table_id)
    r = _lowest_of_two_d100(rng)
    row = _lookup(table["rows"], r)
    return {
        "race": race,
        "ship_name": row["name"],
        "ship_class": row["class"],
        "book": row["_book"],
        "page": row["_page"],
        "upgrades": [],
        "integrity": integrity,
        "_roll": r,
        "_source": table["_source"],
    }


def _gen_ork(rng, integrity: Optional[str]) -> Dict:
    table = _load("table_ship_hulls_ork")
    r = _lowest_of_two_d100(rng)
    row = _lookup(table["rows"], r)
    # Resolve secondary roll for sibling-pair hulls
    name = row["name"]; secondary_roll: Optional[int] = None
    if "secondary_roll" in row:
        sr = _d10(rng)
        secondary_roll = sr
        sec = row["secondary_roll"]
        name = sec["le_5"] if sr <= 5 else sec["ge_6"]
    upgrades = _apply_upgrades(rng, row.get("upgrades", []))
    return {
        "race": "Ork",
        "ship_name": name,
        "ship_class": row["class"],
        "book": row["_book"],
        "page": row["_page"],
        "upgrades": upgrades,
        "integrity": integrity,
        "_roll": r,
        "_secondary_roll": secondary_roll,
        "_source": table["_source"],
    }


def _gen_stryxis_or_kroot_or_other(rng, race: str, integrity: Optional[str]) -> Dict:
    """Stryxis, Kroot, and 'Other' xenos don't have codified hull catalogues in
    BFK -- generate a generic placeholder. Kroot/Stryxis stacks are heavily
    capped per TiLT (numMajority /= 5) because they appear less often."""
    return {
        "race": race,
        "ship_name": f"Unknown {race} Vessel",
        "ship_class": "Frigate",
        "book": "RT09_BFK",
        "page": 0,
        "upgrades": [],
        "integrity": integrity,
        "_roll": None,
        "_source": f"src_codifier_placeholder_for_{race.lower()}",
        "_note": f"BFK does not catalogue {race} hulls in detail. Replace with custom NPC ship as needed."
    }


# ----------------------------------------------------------------------------

def generate_starship_hulk(rng: random.Random,
                            race: Optional[str] = None,
                            integrity: Optional[str] = None,
                            with_into_the_storm: bool = True) -> Dict:
    """Generate one ship hulk. If race is None, picks via d14 selector."""
    if race is None:
        race = pick_random_species(rng)
    if integrity is None:
        integrity = rng.choice(INTEGRITY_LEVELS)
    if race == "Human":
        out = _gen_human(rng, integrity, with_its=with_into_the_storm)
    elif race == "Ork":
        out = _gen_ork(rng, integrity)
    elif race == "Eldar":
        out = _gen_simple(rng, "Eldar", "table_ship_hulls_eldar", integrity)
    elif race == "DarkEldar":
        out = _gen_simple(rng, "DarkEldar", "table_ship_hulls_dark_eldar", integrity)
    elif race == "RakGol":
        out = _gen_simple(rng, "RakGol", "table_ship_hulls_rakgol", integrity)
    elif race == "ChaosReaver":
        out = _gen_simple(rng, "ChaosReaver", "table_ship_hulls_chaos_reaver", integrity)
    elif race in ("Stryxis", "Kroot", "Other"):
        out = _gen_stryxis_or_kroot_or_other(rng, race, integrity)
    else:
        raise ValueError(f"Unknown race: {race!r}")
    return out


def generate_pirate_fleet(rng: random.Random, count: Optional[int] = None,
                           dominant_race: Optional[str] = None) -> List[Dict]:
    """Per RT14 p.10 Pirate Den: 1d5+4 Wolfpack Raiders led by a stronger
    flagship (usually a Frigate, occasionally a Cruiser). Never <5, rarely >8.
    Alternative fleets can be all Ork/Eldar/Rak'Gol/Chaos -- pass dominant_race.
    """
    if count is None:
        count = max(5, min(8, rng.randint(1, 5) + 4))
    if dominant_race is None:
        dominant_race = "Human"
    fleet: List[Dict] = []
    # Flagship: 1d10 — 7+ = Cruiser-ish (use higher d100 roll), else Frigate
    flagship_class_pref = "Cruiser" if _d10(rng) >= 9 else "Frigate"
    flagship = generate_starship_hulk(rng, race=dominant_race, integrity="Mostly Intact")
    flagship["_role"] = "flagship"
    flagship["_target_class_pref"] = flagship_class_pref
    fleet.append(flagship)
    # Raiders: Wolfpack Raiders (or race-equivalent Raider)
    for _ in range(count - 1):
        raider = generate_starship_hulk(rng, race=dominant_race, integrity="Mostly Intact")
        raider["_role"] = "raider"
        fleet.append(raider)
    return fleet


if __name__ == "__main__":
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    rng = random.Random(seed)
    print("=== Random ship picks ===")
    for _ in range(8):
        h = generate_starship_hulk(rng)
        print(f"  {h['race']:<12} {h['ship_class']:<14} {h['ship_name']:<40} [{h['book']} p.{h['page']}] upgrades={h['upgrades']}")
    print()
    print("=== Pirate Den fleet (Human) ===")
    rng = random.Random(seed)
    for h in generate_pirate_fleet(rng, dominant_race="Human"):
        role = h.get("_role", "ship")
        print(f"  [{role:<10}] {h['race']:<12} {h['ship_class']:<14} {h['ship_name']:<40} [{h['book']} p.{h['page']}]")
