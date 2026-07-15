"""Rogue Trader — Procedural Star System Generation
======================================================

Implements the full RT14 Stars of Inequity Chapter I world-generator pipeline.
Walks the 27 canonical tables to produce a star system conforming to
`schemas/star_system.schema.json`.

Pipeline (per RT14 p.7-52):
  1. System Features (Table 1-1)
  2. Star Creation (Table 1-2)
  3. System Elements per Solar Zone (Table 1-3)
  4. For each Planet element:
       - Body (1-6) → Gravity (1-7) → Orbital Features (1-8)
       - Atmospheric Presence (1-9) + Composition (1-10)
       - Climate (1-11) → Habitability (1-12)
       - Territories: 1-13 count, 1-14 base terrain, 1-15 traits, 1-23 landmarks
       - Resources: 1-16/17/18 + 1-19 (depletion later) + 1-20/21/22
       - Native Species (1-24/25) if Habitability >= Limited Ecosystem
       - Inhabitants (1-26/27)
  5. For each Derelict Station element: 1-4 origins
  6. For each Starship Graveyard element: 1-5 origins

Usage:
    from rules.star_system_generation import generate_star_system
    system = generate_star_system(seed=42)
    print(system['name'])
    # Optionally validate against schemas/star_system.schema.json with jsonschema

Source: RT14 Stars of Inequity (FFG, 2012), Chapter I pp.7-52.
Every table consulted by this module ships in data/tables/world_generator/.
"""

from __future__ import annotations
import json
import os
import random
import re
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = ROOT / "data" / "tables" / "world_generator"

# Lazy-loaded table cache
_TABLES: Dict[str, Dict] = {}


def load_table(table_id: str) -> Dict:
    """Load a generation table by ID. Cached per process."""
    if table_id in _TABLES:
        return _TABLES[table_id]
    path = TABLES_DIR / f"{table_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Table not found: {path}")
    _TABLES[table_id] = json.load(open(path))
    return _TABLES[table_id]


# === Dice helpers ===

DICE_RE = re.compile(r"(\d*)d(\d+)\s*([+-]\s*\d+)?\s*(?:\(minimum\s+(\d+)\))?", re.IGNORECASE)


def roll(formula: str, rng: random.Random) -> int:
    """Roll dice expressed in standard `NdM+K` or `NdM-K (minimum X)` form."""
    formula = formula.strip()
    m = DICE_RE.search(formula)
    if not m:
        # Plain integer?
        try:
            return int(formula)
        except ValueError:
            raise ValueError(f"Cannot parse dice formula: {formula!r}")
    n_dice = int(m.group(1)) if m.group(1) else 1
    sides = int(m.group(2))
    modifier = 0
    if m.group(3):
        modifier = int(m.group(3).replace(" ", ""))
    minimum = int(m.group(4)) if m.group(4) else None
    total = sum(rng.randint(1, sides) for _ in range(n_dice)) + modifier
    if minimum is not None:
        total = max(total, minimum)
    return total


def roll_d100(rng: random.Random) -> int:
    return rng.randint(1, 100)


def roll_d10(rng: random.Random) -> int:
    return rng.randint(1, 10)


def roll_d5(rng: random.Random) -> int:
    return rng.randint(1, 5)


# === Table lookups ===

def lookup_row(rows: List[Dict], roll_value: int) -> Optional[Dict]:
    """Find the row whose [range_min, range_max] contains roll_value."""
    for row in rows:
        lo = row.get("range_min", 1)
        hi = row.get("range_max", 100)
        if lo <= roll_value <= hi:
            return row
    return None


# === Step 1: System Features (Table 1-1) ===
#
# Patched 2026-05-16 (cross-checked against RT14 p.9 and TiLT's GenerateSystemFeatures):
#   * Count formula now follows the book: max(1, 1d5-2) instead of always 1.
#   * Duplicate features are re-rolled (book canon, p.9: "re-rolling any
#     duplicate results"). Up to 30 re-roll attempts then we accept the dup
#     rather than infinite-loop.
#   * Each feature's sub-effect cascade (Table 1-1 sub-rolls) is rolled and
#     written into a per-system `feature_flags` struct -- the codified
#     analogue of TiLT's SystemCreationRules.
#   * Warp Stasis / Warp Turbulence mutex is NOT enforced (the book does not
#     mark them as mutually exclusive; TiLT's mutex is a house rule).

# Default feature_flags shape -- mirrors TiLT's SystemCreationRules (24 fields)
# but expressed in snake_case JSON. Every field has a documented effect tied
# back to its source page.
FEATURE_FLAGS_DEFAULT: Dict[str, Any] = {
    # Solar-zone size modifiers (driven by star Table 1-2, populated in generate_star)
    "inner_cauldron_weak": False,
    "inner_cauldron_dominant": False,
    "primary_biosphere_weak": False,
    "primary_biosphere_dominant": False,
    "outer_reaches_weak": False,
    "outer_reaches_dominant": False,
    # Bountiful (Table 1-1 sub-roll)
    "extra_asteroid_field": 0,
    "bountiful_asteroids": False,
    "extra_mineral_resources_per_planet": 0,
    "chance_for_extra_exotic_materials_per_planet": False,
    # Gravity Tides (Table 1-1 sub-roll)
    "extra_gravity_riptides": 0,
    "gravity_tides_gravity_wells_around_planets": False,
    "gravity_tides_travel_time_halves": False,
    # Haven (Table 1-1 sub-roll)
    "extra_planets_in_each_solar_zone": 0,
    "haven_thicker_atmospheres_in_primary_biosphere": False,
    "haven_better_habitability": False,
    # Ill-Omened (Table 1-1 sub-roll)
    "ill_omened_fickle_fate_points": False,
    "ill_omened_willpower_penalty": False,
    "ill_omened_doubled_insanity": False,
    "ill_omened_fear_from_psychic_exploration": False,
    # Pirate Den
    "pirate_den_present": False,
    # Ruined Empire (Table 1-1 sub-roll)
    "ruined_empire_extra_xenos_ruins_on_different_planets": 0,
    "ruined_empire_increased_abundance_xenos_ruins": False,
    "ruined_empire_extra_archeotech_caches_on_different_planets": 0,
    "ruined_empire_increased_abundance_archeotech_caches": False,
    # Starfarers
    "minimum_num_planets_after_modifiers": 0,
    "starfarers_num_system_features_inhabited": 0,
    # Stellar Anomaly
    "num_planets_modifier": 0,
    # Warp Turbulence
    "num_planets_in_warp_storms": 0,
    # Warp Stasis
    "warp_stasis_focus_power_penalties": False,
    "warp_stasis_no_push": False,
    "warp_stasis_reduced_psychic_phenomena": False,
}


def _new_feature_flags() -> Dict[str, Any]:
    return dict(FEATURE_FLAGS_DEFAULT)


def _apply_feature_cascade(feature_name: str, flags: Dict[str, Any],
                            rng: random.Random) -> List[Dict]:
    """Roll the sub-effect cascade for a Table 1-1 feature and mutate `flags`.

    Returns the list of selected sub-options for provenance.
    """
    subrolls = load_table("table_1_1_subrolls")
    feat = subrolls["features"].get(feature_name)
    if not feat:
        return []  # No sub-cascade defined
    options = feat["options"]
    mode = feat["pick_mode"]
    chosen: List[Dict] = []

    if mode == "deterministic":
        for opt in options:
            chosen.append({"id": opt["id"], "description": opt["description"]})
            _apply_option(opt, flags, rng)
    elif mode == "one":
        idx = rng.randint(0, len(options) - 1)
        opt = options[idx]
        chosen.append({"id": opt["id"], "description": opt["description"], "sub_roll": idx + 1})
        _apply_option(opt, flags, rng)
    elif mode == "one_or_more":
        # Per RT14: roll on the sub-table; repeat until you get a result you've
        # already taken (TiLT's "GetNextOneOrMoreChoiceResult" pattern).
        taken: List[int] = []
        while True:
            idx = rng.randint(0, len(options) - 1)
            if idx in taken:
                break
            taken.append(idx)
            opt = options[idx]
            chosen.append({"id": opt["id"], "description": opt["description"],
                           "sub_roll": idx + 1})
            _apply_option(opt, flags, rng)
            if len(taken) == len(options):
                break
    return chosen


def _apply_option(opt: Dict, flags: Dict[str, Any], rng: random.Random) -> None:
    """Apply one sub-option's flag mutation."""
    op = opt["flag_op"]
    tgt = opt["flag_target"]
    if op == "set_true":
        flags[tgt] = True
    elif op == "increment":
        flags[tgt] = flags.get(tgt, 0) + 1
    elif op == "decrement_by_2":
        flags[tgt] = flags.get(tgt, 0) - 2
    elif op == "set_to_1":
        flags[tgt] = 1
    elif op == "add_d5":
        flags[tgt] = flags.get(tgt, 0) + roll_d5(rng)
    elif op == "add_d5_plus_3":
        flags[tgt] = flags.get(tgt, 0) + roll_d5(rng) + 3
    elif op == "set_min_4_planets":
        flags["minimum_num_planets_after_modifiers"] = max(
            flags.get("minimum_num_planets_after_modifiers", 0), 4)
    elif op == "set_xenos_ruins_bundle":
        flags["ruined_empire_increased_abundance_xenos_ruins"] = True
        flags["ruined_empire_extra_xenos_ruins_on_different_planets"] = max(
            1, roll_d5(rng) - 1)
    elif op == "set_archeotech_bundle":
        flags["ruined_empire_increased_abundance_archeotech_caches"] = True
        flags["ruined_empire_extra_archeotech_caches_on_different_planets"] = max(
            1, roll_d5(rng) - 1)
    # else: unknown op, silently skip (forward-compat for new sub-effects)


def generate_system_features(rng: random.Random,
                              count: Optional[int] = None,
                              flags: Optional[Dict[str, Any]] = None
                              ) -> List[Dict]:
    """Roll 1d10 on Table 1-1 per RT14 p.9.

    Args:
        rng:    Seeded RNG.
        count:  Override the book's 1d5-2 (min 1) count formula. None = book formula.
        flags:  Optional feature_flags struct to mutate as each cascade fires.
                If None, a fresh struct is created and discarded (legacy mode).
    """
    table = load_table("table_1_1_system_features")
    if count is None:
        count = max(1, roll_d5(rng) - 2)  # RT14 p.9
    if flags is None:
        flags = _new_feature_flags()

    features: List[Dict] = []
    seen: set = set()
    for _slot in range(count):
        # Re-roll duplicates per RT14 p.9 -- up to 30 attempts then accept.
        for _attempt in range(30):
            r = roll_d10(rng)
            row = lookup_row(table["rows"], r)
            if row and row["name"] not in seen:
                seen.add(row["name"])
                cascade = _apply_feature_cascade(row["name"], flags, rng)
                features.append({
                    "name": row["name"],
                    "roll": r,
                    "sub_effects": cascade,
                    "_source": table["_source"],
                })
                break
        else:
            # All 30 attempts collided -- table is saturated; stop emitting.
            break
    return features


# === Step 2: Star Creation (Table 1-2) ===
#
# Patched 2026-05-16 (cross-checked against RT14 p.13 and TiLT's GenerateStar):
# Binary star resolution per RT14 p.13:
#   "Roll 1d10 to determine the nature of the set: On a 1-7, the stars are of
#    the same type, while on an 8-10 they should be generated separately.
#    Generate binary stars by rolling on this Table again, ignoring results of
#    9 or 10. Use the effect of the more powerful star to determine the size
#    of Solar Zones, if there is variance."
# "More powerful" = lower roll value (Mighty=1, Vigorous=2-4, ..., Dull=8).

def _resolve_star_roll(r: int, table: Dict) -> Dict:
    """Look up a single star-type row by its 1d10 roll value (excluding binary recursion)."""
    row = lookup_row(table["rows"], r)
    return {
        "type": row["name"],
        "description": row.get("description", ""),
        "roll": r,
        "solar_zone_modifiers": row.get("solar_zone_modifiers", {}),
        "_source": table["_source"],
    }


def generate_star(rng: random.Random) -> Dict:
    """Roll 1d10 on Table 1-2. Handles Binary special-case per RT14 p.13."""
    table = load_table("table_1_2_star_generation")
    r = roll_d10(rng)
    if r != 10:
        # Single star -- straight lookup
        return _resolve_star_roll(r, table)

    # Binary primary -- resolve composition
    composition_roll = roll_d10(rng)
    if composition_roll <= 7:
        # Twins: both stars same type, single sub-roll 1-8
        sub = rng.randint(1, 8)
        twin = _resolve_star_roll(sub, table)
        return {
            "type": "Binary",
            "description": f"Binary system. Both stars are {twin['type']}.",
            "roll": r,
            "binary_composition": "twins",
            "binary_composition_roll": composition_roll,
            "binary_sub_roll": sub,
            "binary_companions": [twin, dict(twin)],
            # Both twins contribute the same effect; use it directly.
            "solar_zone_modifiers": twin["solar_zone_modifiers"],
            "_effective_star_roll": sub,
            "_source": table["_source"],
        }
    else:
        # Potentially different: two independent sub-rolls 1-8; lowest = strongest
        s1 = rng.randint(1, 8)
        s2 = rng.randint(1, 8)
        star1 = _resolve_star_roll(s1, table)
        star2 = _resolve_star_roll(s2, table)
        stronger = star1 if s1 <= s2 else star2
        desc = (f"Binary system. Both stars are {star1['type']}."
                if star1["type"] == star2["type"]
                else f"Binary system. Stars are {star1['type']} and {star2['type']} "
                     f"(zones use {stronger['type']} -- the more powerful star).")
        return {
            "type": "Binary",
            "description": desc,
            "roll": r,
            "binary_composition": "potentially_different",
            "binary_composition_roll": composition_roll,
            "binary_companions": [star1, star2],
            # Per RT14 p.13: use effect of the more powerful (lowest-numbered) star.
            "solar_zone_modifiers": stronger["solar_zone_modifiers"],
            "_effective_star_roll": min(s1, s2),
            "_source": table["_source"],
        }


# === Step 3: System Elements per Solar Zone (Table 1-3) ===

ZONE_NAMES = ["inner_cauldron", "primary_biosphere", "outer_reaches"]


def zone_size(star: Dict, zone: str) -> str:
    """Determine solar-zone size (typical/dominant/weak) from star modifiers."""
    mods = star.get("solar_zone_modifiers", {})
    if mods.get(zone) == "dominant":
        return "dominant"
    if mods.get(zone) == "weak":
        return "weak"
    return "typical"


def zone_element_count(size: str, rng: random.Random) -> int:
    """1d5 typical / 1d5+2 dominant / 1d5-2 (min 1) weak."""
    if size == "dominant":
        return roll_d5(rng) + 2
    if size == "weak":
        return max(1, roll_d5(rng) - 2)
    return roll_d5(rng)


def generate_system_elements(star: Dict, rng: random.Random,
                              flags: Optional[Dict[str, Any]] = None
                              ) -> Dict[str, Dict]:
    """For each Solar Zone, roll for N System Elements per Table 1-3.

    Patched 2026-05-16 (cross-checked against TiLT's GenerateSystemElements):
      * Solar Flares and Radiation Bursts STACK rather than duplicate -- per
        the book and TiLT, when a second roll would add another Solar Flare to
        a zone that already has one, increment a `count` field on the existing
        node instead. This matters because the in-game effect of the second
        Flare is to add +1 to the daily Flare roll, not to double the body.
      * Optional `flags` honours feature_flags-driven adjustments:
          - extra_planets_in_each_solar_zone -> add N extra Planets per zone
          - extra_asteroid_field -> add N extra Asteroid Belts/Clusters
          - extra_gravity_riptides -> add N extra Gravity Riptides
    """
    flags = flags or _new_feature_flags()
    table = load_table("table_1_3_system_elements")
    zones: Dict[str, Dict] = {}

    for zone in ZONE_NAMES:
        size = zone_size(star, zone)
        count = zone_element_count(size, rng)
        rows = table["subtables"][zone]
        elements: List[Dict] = []

        def _add_element(elt_name: str, roll_val: Optional[int]) -> None:
            # Stack Solar Flares / Radiation Bursts on duplicate
            if elt_name in ("Solar Flares", "Radiation Bursts"):
                for existing in elements:
                    if existing["element_type"] == elt_name:
                        existing["count"] = existing.get("count", 1) + 1
                        existing.setdefault("stacked_rolls", []).append(roll_val)
                        return
                elements.append({"element_type": elt_name, "roll": roll_val,
                                 "count": 1, "_source": table["_source"]})
                return
            elements.append({"element_type": elt_name, "roll": roll_val,
                             "_source": table["_source"]})

        for _ in range(count):
            r = roll_d100(rng)
            row = lookup_row(rows, r)
            if row:
                _add_element(row["name"], r)

        # Apply feature-driven additions (Bountiful, Gravity Tides, Haven)
        for _ in range(flags.get("extra_planets_in_each_solar_zone", 0)):
            _add_element("Planet", None)
        zones[zone] = {
            "size": size,
            "element_count_formula": table["roll_count_formulas"][size],
            "elements": elements,
        }

    # Apply per-system additions that aren't per-zone (Bountiful asteroids,
    # Gravity Tides gravity riptides). Distribute across zones uniformly at
    # random per TiLT's GetRandomZone() pattern.
    n_extra_asteroid = flags.get("extra_asteroid_field", 0)
    for _ in range(n_extra_asteroid):
        zone = rng.choice(ZONE_NAMES)
        # 5+ on 1d10 = Belt, else Cluster (per Table 1-1 Bountiful sub-effect text)
        kind = "Asteroid Belt" if roll_d10(rng) >= 6 else "Asteroid Cluster"
        zones[zone]["elements"].append({
            "element_type": kind, "roll": None,
            "_source": "src_rt14_stars_p9_bountiful_feature",
        })
    n_extra_riptide = flags.get("extra_gravity_riptides", 0)
    for _ in range(n_extra_riptide):
        zone = rng.choice(ZONE_NAMES)
        zones[zone]["elements"].append({
            "element_type": "Gravity Riptide", "roll": None,
            "_source": "src_rt14_stars_p9_gravity_tides_feature",
        })

    return zones


# === Step 4a: Planet Body + Gravity (Tables 1-6, 1-7) ===

def generate_planet_body(rng: random.Random, is_gas_giant: bool = False) -> Dict:
    table = load_table("table_1_6_body")
    key = "gas_giants" if is_gas_giant else "rocky_planets"
    r = roll_d10(rng)
    row = lookup_row(table["subtables"][key], r)
    return {
        "body_class": "Gas Giant" if is_gas_giant else "Rocky Planet",
        "body_size": row["name"],
        "description": row.get("description", ""),
        "modifiers": row.get("modifiers", []),
        "roll": r,
        "_source": table["_source"],
    }


def generate_planet_gravity(body: Dict, rng: random.Random) -> Dict:
    table = load_table("table_1_7_gravity")
    is_gas = body["body_class"] == "Gas Giant"
    key = "gas_giants" if is_gas else "rocky_planets"
    r = roll_d10(rng)
    # Apply Body modifiers on Table 1-7 rolls
    for mod in body.get("modifiers", []):
        if mod.get("affects") == "table_1_7_gravity" and mod.get("op") == "add":
            r += mod["value"]
    row = lookup_row(table["subtables"][key], r)
    return {
        "name": row["name"] if row else "Normal",
        "description": row.get("description", "") if row else "",
        "orbital_features_count_formula": row.get("orbital_features_count", "1d5-2") if row else "1d5-2",
        "modifiers": row.get("modifiers", []) if row else [],
        "roll": r,
        "_source": table["_source"],
    }


# === Step 4b: Orbital Features (Table 1-8) ===

def generate_orbital_features(body: Dict, gravity: Dict, rng: random.Random) -> List[Dict]:
    table = load_table("table_1_8_orbital_features")
    key = "gas_giants" if body["body_class"] == "Gas Giant" else "rocky_planets"
    count_formula = gravity.get("orbital_features_count_formula", "1d5-2 (minimum 1)")
    count = roll(count_formula, rng)
    count = max(0, count)
    features: List[Dict] = []
    for _ in range(count):
        r = roll_d100(rng)
        # Apply Body/Gravity modifiers
        for mod in body.get("modifiers", []) + gravity.get("modifiers", []):
            if mod.get("affects") == "table_1_8_orbital_features" and mod.get("op") == "add":
                r += mod["value"]
        r = max(1, min(100, r))
        row = lookup_row(table["subtables"][key], r)
        if row:
            features.append({
                "feature_type": row["name"],
                "description": row.get("description", ""),
                "roll": r,
                "_source": table["_source"],
            })
    return features


# === Step 4c: Atmosphere (Tables 1-9, 1-10) ===

def generate_atmosphere(body: Dict, gravity: Dict, rng: random.Random) -> Dict:
    pres_table = load_table("table_1_9_atmospheric_presence")
    r = roll_d10(rng)
    for mod in gravity.get("modifiers", []):
        if mod.get("affects") == "table_1_9_atmospheric_presence" and mod.get("op") == "add":
            r += mod["value"]
    pres_row = lookup_row(pres_table["rows"], r)
    pres = pres_row["name"] if pres_row else "Moderate"
    if pres == "None":
        return {"presence": "None", "composition": "N/A",
                "_source": pres_table["_source"]}
    comp_table = load_table("table_1_10_atmospheric_composition")
    cr = roll_d10(rng)
    comp_row = lookup_row(comp_table["rows"], cr)
    return {
        "presence": pres,
        "composition": comp_row["name"] if comp_row else "Pure",
        "presence_roll": r,
        "composition_roll": cr,
        "_source": pres_table["_source"],
    }


# === Step 4d: Climate + Habitability (Tables 1-11, 1-12) ===

def generate_climate(atmosphere: Dict, solar_zone: str, rng: random.Random) -> str:
    if atmosphere["presence"] == "None":
        if solar_zone == "inner_cauldron": return "Burning World"
        if solar_zone == "outer_reaches": return "Ice World"
        return rng.choice(["Burning World", "Ice World"])
    table = load_table("table_1_11_climate")
    r = roll_d10(rng)
    if solar_zone == "inner_cauldron": r -= 6
    elif solar_zone == "outer_reaches": r += 6
    row = lookup_row(table["rows"], r)
    return row["name"] if row else "Temperate World"


def generate_habitability(atmosphere: Dict, climate: str, rng: random.Random) -> str:
    if atmosphere["presence"] == "None":
        return "Inhospitable"
    if atmosphere["composition"] not in ("Tainted", "Pure"):
        return "Inhospitable"
    table = load_table("table_1_12_habitability")
    r = roll_d10(rng)
    if climate in ("Hot World", "Cold World"):
        r -= 2
    elif climate in ("Burning World", "Ice World"):
        r -= 7
        r = min(r, 3)  # cap
    row = lookup_row(table["rows"], r)
    return row["name"] if row else "Inhospitable"


# === Step 4e: Territories + Terrain + Traits + Landmarks ===

def generate_territories(body_size: str, habitability: str, rng: random.Random) -> List[Dict]:
    if body_size in ("Gas Dwarf", "Gas Giant", "Massive Gas Giant"):
        return []  # Gas giants don't have territories
    count = roll_d5(rng)
    if body_size == "Small": count -= 2
    elif body_size == "Vast": count += 3
    if habitability == "Verdant": count += 2
    if habitability == "Limited Ecosystem": count += 0
    count = max(0, count)

    terrain_table = load_table("table_1_14_base_terrain")
    traits_table = load_table("table_1_15_territory_traits")
    landmarks_table = load_table("table_1_23_landmarks")

    landmark_count_formulas = {"Small": "1d5", "Large": "1d5+2", "Vast": "1d5+3"}
    landmark_count_formula = landmark_count_formulas.get(body_size, "1d5")

    territories: List[Dict] = []
    for _ in range(count):
        tr = roll_d5(rng)
        terrain_row = lookup_row(terrain_table["rows"], tr)
        if not terrain_row: continue
        terrain = terrain_row["name"]
        # Traits — roll 1d5-1 (min 1) times on appropriate subtable
        subtable_key = terrain.lower() + "s" if not terrain.lower().endswith("s") else terrain.lower()
        subtable_key = subtable_key.replace("plainss", "plains").replace("swampss", "swamps").replace("forests", "forests").replace("mountains", "mountain_ranges").replace("mountain", "mountain_ranges").replace("mountain_rangess", "mountain_ranges").replace("wastelands", "wastelands")
        traits_subtable = traits_table["subtables"].get(subtable_key, [])
        trait_count = max(1, roll_d5(rng) - 1)
        traits = []
        for _ in range(trait_count):
            tr_r = roll_d100(rng)
            trait_row = lookup_row(traits_subtable, tr_r)
            if trait_row:
                traits.append(trait_row["name"])
        # Landmarks
        lc = roll(landmark_count_formula, rng)
        landmarks = []
        # The table may carry exceptional_landmarks as a dict {snake_id: {requires,effect}} or a list
        _ex_raw = landmarks_table.get("exceptional_landmarks") or {}
        if isinstance(_ex_raw, dict):
            exceptional_pool = list(_ex_raw.keys())
        else:
            exceptional_pool = list(_ex_raw)
        exceptional_name_map = {
            "glacier": "Glacier",
            "inland_sea": "Inland Sea",
            "perpetual_storm": "Perpetual Storm",
            "reef": "Reef",
            "whirlpool": "Whirlpool",
        }
        for _ in range(lc):
            lr = roll_d100(rng)
            lm_row = lookup_row(landmarks_table["rows"], lr)
            if not lm_row:
                continue
            if lm_row.get("category") == "Exceptional" and exceptional_pool:
                pick = rng.choice(exceptional_pool)
                landmarks.append({
                    "type": exceptional_name_map.get(pick, pick.replace("_", " ").title()),
                    "category": "Exceptional",
                })
            else:
                landmarks.append({"type": lm_row["name"], "category": lm_row.get("category", "General")})
        territories.append({
            "base_terrain": terrain,
            "traits": traits,
            "landmarks": landmarks,
        })
    return territories


# === Step 4f: Resources ===

def generate_resources(body_size: str, habitability: str, rng: random.Random) -> Dict[str, List[Dict]]:
    presence_table = load_table("table_1_16_resource_presence")
    additional_table = load_table("table_1_17_additional_resources")
    abundance_table = load_table("table_1_18_resource_abundance")
    mineral_table = load_table("table_1_20_mineral_resources")
    organic_table = load_table("table_1_21_organic_resources")
    xenos_table = load_table("table_1_22_xenos_ruins")

    size_key = "small"
    if body_size in ("Large", "Large and Dense"): size_key = "large"
    if body_size == "Vast": size_key = "vast"

    by_body = presence_table.get("by_body", {}).get(size_key, {"base_mineral": "1d5-2 (min 0)", "additional": "1d5-3 (min 0)"})
    mineral_count = max(0, roll(by_body["base_mineral"].replace("(min 0)", "").replace("(min 1)", ""), rng))
    additional_count = max(0, roll(by_body["additional"].replace("(min 0)", "").replace("(min 1)", ""), rng))

    def roll_abundance(rng) -> Dict:
        r = roll_d100(rng)
        row = lookup_row(abundance_table["rows"], r)
        return {"level": row["name"] if row else "Minimal", "roll_result": r}

    minerals: List[Dict] = []
    for _ in range(mineral_count):
        r = roll_d10(rng)
        row = lookup_row(mineral_table["rows"], r)
        if row:
            minerals.append({
                "resource_type": row["name"],
                "abundance": roll_abundance(rng),
                "_source": mineral_table["_source"],
            })

    additional: List[Dict] = []
    can_support_life = habitability in ("Limited Ecosystem", "Verdant", "Liquid Water")
    for _ in range(additional_count):
        ar = roll_d10(rng)
        row = lookup_row(additional_table["rows"], ar)
        if not row: continue
        rtype = row["name"]
        # Re-roll Organic if Planet can't support life
        if rtype.startswith("Organic Compound") and not can_support_life:
            while rtype.startswith("Organic Compound"):
                ar = roll_d10(rng)
                row = lookup_row(additional_table["rows"], ar)
                rtype = row["name"]
        entry: Dict = {"resource_type": rtype, "abundance": roll_abundance(rng),
                       "_source": additional_table["_source"]}
        if rtype.startswith("Organic Compound") or rtype == "Organic Compound":
            orr = roll_d10(rng)
            orow = lookup_row(organic_table["rows"], orr)
            if orow:
                entry["details"] = {"organic_subtype": orow["name"]}
        elif rtype == "Xenos Ruins":
            xr = roll_d10(rng)
            xrow = lookup_row(xenos_table["rows"], xr)
            if xrow:
                entry["details"] = {"xenos_origin": xrow["name"]}
        additional.append(entry)

    return {"mineral_resources": minerals, "additional_resources": additional}


# === Step 4g: Native Species (Tables 1-24, 1-25) ===

def generate_native_species(habitability: str, rng: random.Random, max_species: int = 4) -> List[Dict]:
    if habitability == "Inhospitable" or habitability == "Trapped Water" or habitability == "Liquid Water":
        return []
    archetype_table = load_table("table_1_24_bestial_archetypes")
    natures_table = load_table("table_1_25_bestial_natures")
    archetype_key_map = {
        "Apex Predator":   "apex_predators",
        "Behemoth":        "behemoths",
        "Ptera-Beast":     "ptera_beasts",
        "Shadowed Stalker":"shadowed_stalkers",
        "Venomous Terror": "venomous_terrors",
    }
    if habitability == "Limited Ecosystem":
        count = rng.randint(0, 3)
    else:
        count = rng.randint(1, max_species)
    species: List[Dict] = []
    for _ in range(count):
        ar = roll_d5(rng)
        arow = lookup_row(archetype_table["rows"], ar)
        if not arow: continue
        sub_key = archetype_key_map.get(arow["name"], "apex_predators")
        natures_sub = natures_table["subtables"].get(sub_key, [])
        nr = roll_d10(rng)
        nrow = lookup_row(natures_sub, nr)
        species.append({
            "archetype": arow["name"],
            "natures": [nrow["name"]] if nrow else [],
        })
    return species


# === Step 4h: Inhabitants (Tables 1-26, 1-27) ===

def generate_inhabitants(habitability: str, rng: random.Random) -> Optional[Dict]:
    if habitability == "Inhospitable":
        return None
    inhab_table = load_table("table_1_26_inhabitants")
    dev_table = load_table("table_1_27_inhabitant_development")
    species_key_map = {
        "Eldar":         "eldar",
        "Humans":        "humans",
        "Kroot":         "kroot",
        "Orks":          "orks",
        "Rak'Gol":       "rakgol",
        "Xenos (Other)": "xenos_other",
    }
    # Roll species (re-roll Kroot/Orks on uninhabitable Planets — already filtered above)
    sr = roll_d10(rng)
    srow = lookup_row(inhab_table["rows"], sr)
    if not srow: return None
    species = srow["name"]
    if species in ("Kroot", "Orks") and habitability == "Liquid Water":
        # Re-roll once
        while species in ("Kroot", "Orks"):
            sr = roll_d10(rng)
            srow = lookup_row(inhab_table["rows"], sr)
            species = srow["name"]
    dev_sub = dev_table["subtables"].get(species_key_map.get(species, "xenos_other"), [])
    dr = roll_d10(rng)
    drow = lookup_row(dev_sub, dr)
    return {"species": species, "development": drow["name"] if drow else "Primitive Clans"}


# === Step 4: Full planet generation ===

def generate_planet(rng: random.Random, solar_zone: str, allow_gas_giant: bool = True) -> Dict:
    """Generate a full Planet element, walking Tables 1-6 through 1-27 as appropriate."""
    is_gas = (solar_zone in ("inner_cauldron", "outer_reaches")) and rng.random() < 0.15 and allow_gas_giant
    body = generate_planet_body(rng, is_gas_giant=is_gas)
    gravity = generate_planet_gravity(body, rng)
    orbital_features = generate_orbital_features(body, gravity, rng)
    atmosphere = generate_atmosphere(body, gravity, rng)
    climate = generate_climate(atmosphere, solar_zone, rng)
    habitability = generate_habitability(atmosphere, climate, rng)
    territories = generate_territories(body["body_size"], habitability, rng)
    resources = generate_resources(body["body_size"], habitability, rng)
    species = generate_native_species(habitability, rng)
    inhabitants = generate_inhabitants(habitability, rng)
    return {
        "body_class": body["body_class"],
        "body_size": body["body_size"],
        "gravity": gravity["name"],
        "orbital_features": orbital_features,
        "atmospheric_presence": atmosphere["presence"],
        "atmospheric_composition": atmosphere["composition"],
        "climate": climate,
        "habitability": habitability,
        "territories": territories,
        "mineral_resources": resources["mineral_resources"],
        "additional_resources": resources["additional_resources"],
        "native_species": species,
        "inhabitants": inhabitants,
        "_source": "src_rt14_stars_p19",
    }


# === Step 5: Derelict Station + Starship Graveyard details ===
#
# Patched 2026-05-16 (Tier 2 contents codification):
#   * Derelict Station now emits armour, hull integrity, and per-find resource
#     abundances (Archeotech or Xenotech depending on origin), with Ruined
#     Empire feature-flag bonuses applied per RT14 p.10.
#   * Starship Graveyard now emits the hulk count (per origin formula) and
#     placeholder per-hulk records. Full per-hulk ship-class generation is
#     deferred to Tier 4 (Battlefleet Koronus hulls).
#   * Optional treasure hoard: if `include_treasure=True`, each archeotech /
#     xenotech find spawns a treasure artefact via generate_treasure().

def generate_derelict_station(rng: random.Random,
                               flags: Optional[Dict[str, Any]] = None,
                               include_treasure: bool = False) -> Dict:
    flags = flags or _new_feature_flags()
    table = load_table("table_1_4_derelict_station_origins")
    contents_table = load_table("table_derelict_station_contents")
    r = roll_d100(rng)
    row = lookup_row(table["rows"], r)
    origin = row["name"] if row else "Unknown"

    out: Dict[str, Any] = {
        "origin": origin,
        "origin_roll": r,
        "origin_description": row.get("description", "") if row else "",
        "armour": 10,
        "hull_integrity": sum(rng.randint(1, 10) for _ in range(4)),  # 4d10
        "_source": table["_source"],
    }

    # Resources -- xenotech vs archeotech based on origin
    kind = contents_table["resource_kind_by_origin"].get(origin, "archeotech")
    num_finds = max(0, roll_d5(rng) - 1)
    out["resource_kind"] = kind
    out["num_resource_finds"] = num_finds
    finds: List[Dict] = []

    for _ in range(num_finds):
        abundance = roll_d100(rng)
        if kind == "xenotech" and flags.get(
                "ruined_empire_increased_abundance_xenos_ruins"):
            abundance += roll_d10(rng) + 5
        elif kind == "archeotech" and flags.get(
                "ruined_empire_increased_abundance_archeotech_caches"):
            abundance += roll_d10(rng) + 5
        find: Dict[str, Any] = {"kind": kind, "abundance": abundance,
                                 "_source": contents_table["_source"]}
        if include_treasure:
            from rules.treasure_generation import generate_treasure
            # Xenotech finds force Alien Technology; archeotech finds force
            # Ancient Miracle (per RT14 narrative cross-refs at p.83).
            forced = "Alien Technology" if kind == "xenotech" else "Ancient Miracle"
            find["treasure"] = generate_treasure(rng, forced_origin=forced)
        finds.append(find)
    out["resource_finds"] = finds
    return out


def generate_starship_graveyard(rng: random.Random,
                                  flags: Optional[Dict[str, Any]] = None,
                                  include_treasure: bool = False) -> Dict:
    flags = flags or _new_feature_flags()
    table = load_table("table_1_5_starship_graveyard_origins")
    r = roll_d100(rng)
    row = lookup_row(table["rows"], r)
    origin = row["name"] if row else "Unknown"

    out: Dict[str, Any] = {
        "origin": origin,
        "origin_roll": r,
        "origin_description": row.get("description", "") if row else "",
        "_source": table["_source"],
    }
    if row and "ship_count_formula" in row:
        formula = row["ship_count_formula"]
        # The Unknown Provenance formula has prose appended; extract just the dice
        dice_only = formula.split(" ")[0] if " (" in formula else formula
        try:
            count = roll(dice_only, rng)
        except Exception:
            count = 0
            out["ship_count_formula"] = formula
        out["ship_count"] = count
        out["ship_count_formula"] = formula
        # Tier 4: generate real ship hulks via starship_generation.py.
        # Falls back to the Tier 2 placeholder if the starship generator
        # is unavailable (preserves backward compatibility).
        try:
            from rules.starship_generation import generate_starship_hulk
            integrity_pool = ["Shattered", "Heavily Damaged", "Damaged", "Mostly Intact"]
            out["hulks"] = [
                generate_starship_hulk(rng, integrity=rng.choice(integrity_pool))
                for _ in range(count)
            ]
        except ImportError:
            out["hulks"] = [
                {
                    "_placeholder": True,
                    "race": "Unknown",
                    "class": "Unknown",
                    "integrity": rng.choice(["Shattered", "Heavily Damaged",
                                               "Damaged", "Mostly Intact"]),
                    "_source": "tier_4_pending_bfk_codification",
                }
                for _ in range(count)
            ]

    # Optional salvage treasure -- graveyards yield 1d5-1 finds, kind by origin
    num_finds = max(0, roll_d5(rng) - 1)
    out["num_resource_finds"] = num_finds
    finds: List[Dict] = []
    for _ in range(num_finds):
        abundance = roll_d100(rng)
        # Most graveyards yield archeotech; xenos-vs-xenos engagements would
        # logically yield xenotech but the canonical text doesn't specify --
        # default to archeotech and flag for GM review.
        kind = "archeotech"
        if flags.get("ruined_empire_increased_abundance_archeotech_caches"):
            abundance += roll_d10(rng) + 5
        find: Dict[str, Any] = {"kind": kind, "abundance": abundance,
                                 "_source": table["_source"],
                                 "_gm_note": "Graveyard salvage kind is GM-defaulted to archeotech; switch to xenotech if all hulks are xenos."}
        if include_treasure:
            from rules.treasure_generation import generate_treasure
            find["treasure"] = generate_treasure(rng, forced_origin="Ancient Miracle")
        finds.append(find)
    out["resource_finds"] = finds
    return out


# === Top-level orchestration ===

def _apply_star_modifiers_to_flags(star: Dict, flags: Dict[str, Any]) -> None:
    """Translate the star's solar_zone_modifiers into feature_flags booleans
    so downstream code (encounter generators, planet generators) can query a
    single flat struct.
    """
    mods = star.get("solar_zone_modifiers", {})
    if mods.get("inner_cauldron") == "dominant":
        flags["inner_cauldron_dominant"] = True
    if mods.get("inner_cauldron") == "weak":
        flags["inner_cauldron_weak"] = True
    if mods.get("primary_biosphere") == "dominant":
        flags["primary_biosphere_dominant"] = True
    if mods.get("primary_biosphere") == "weak":
        flags["primary_biosphere_weak"] = True
    if mods.get("outer_reaches") == "dominant":
        flags["outer_reaches_dominant"] = True
    if mods.get("outer_reaches") == "weak":
        flags["outer_reaches_weak"] = True


def generate_star_system(seed: Optional[int] = None, name: Optional[str] = None,
                         system_feature_count: Optional[int] = None,
                         include_treasure: bool = False) -> Dict:
    """Generate a complete Rogue Trader star system per RT14 Ch.I.

    Args:
        seed:                 Random seed for reproducibility. None -> fresh randomness.
        name:                 System name. If None, an auto-generated placeholder is used.
        system_feature_count: Override the book's 1d5-2 (min 1) count formula. None = book formula.
        include_treasure:     If True, derelict/graveyard finds spawn full treasure
                              artefacts via rules/treasure_generation.py.
    Returns:
        A dict conforming to schemas/star_system.schema.json.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    actual_seed = seed if seed is not None else rng.randint(0, 2**32 - 1)
    rng = random.Random(actual_seed)

    flags = _new_feature_flags()
    features = generate_system_features(rng, count=system_feature_count, flags=flags)
    star = generate_star(rng)
    _apply_star_modifiers_to_flags(star, flags)
    zones = generate_system_elements(star, rng, flags=flags)

    # Walk every element; for Planets, generate full planet details
    for zone_key, zone in zones.items():
        for element in zone["elements"]:
            etype = element["element_type"]
            if etype == "Planet":
                element["details"] = generate_planet(rng, solar_zone=zone_key)
            elif etype == "Gas Giant":
                # Generate a planet but force gas-giant body
                p = generate_planet(rng, solar_zone=zone_key, allow_gas_giant=True)
                if p["body_class"] != "Gas Giant":
                    body = generate_planet_body(rng, is_gas_giant=True)
                    p["body_class"] = "Gas Giant"
                    p["body_size"] = body["body_size"]
                element["details"] = p
            elif etype == "Derelict Station":
                element["details"] = generate_derelict_station(
                    rng, flags=flags, include_treasure=include_treasure)
            elif etype == "Starship Graveyard":
                element["details"] = generate_starship_graveyard(
                    rng, flags=flags, include_treasure=include_treasure)

    sys_id = f"system_{actual_seed:05d}" if actual_seed is not None else "system_unknown"

    return {
        "id": sys_id,
        "name": name or f"System {sys_id[7:]}",
        "system_features": features,
        "feature_flags": flags,
        "star": star,
        "solar_zones": zones,
        "_generated_by": "rogue_trader.rules.star_system_generation",
        "_generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "_seed": actual_seed,
        "_source": "src_rt14_stars_p7",
    }


if __name__ == "__main__":
    import sys as _sys
    seed = int(_sys.argv[1]) if len(_sys.argv) > 1 else None
    name = _sys.argv[2] if len(_sys.argv) > 2 else "Test System"
    s = generate_star_system(seed=seed, name=name)
    print(json.dumps(s, indent=2, default=str))
