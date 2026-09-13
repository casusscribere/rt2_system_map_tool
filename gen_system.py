#!/usr/bin/env python3
"""System-tool generator bridge.

Runs the RT14 procedural generator (rules/star_system_generation.py) and maintains
the system tool's library + browser data files:

    python gen_system.py --seed 42 --name "Solivarn"     # generate one system
    python gen_system.py --count 3                       # generate several (random seeds)
    python gen_system.py --rebuild                       # just regenerate data.js/options.js

Self-contained: the RT14 generation engine and every table it consults are
snapshotted under this tool's own folder, so it runs anywhere without a path
back into codified-systems/.

    rules/                       snapshot of the RT14 engine modules
    data/tables/world_generator/ generation tables (star systems)
    data/tables/treasure/        treasure tables (xenos ruins / derelicts)
    data/tables/starships/       starship-graveyard tables
    data/systems/library.json    canonical store (generated/edited via this tool)
    data.js, options.js          file://-safe browser wrappers

options.js carries the enumerated category names (body classes, climates, etc.)
pulled from the snapshotted world_generator tables, so the editor's dropdowns
always match the corpus rather than hard-coded lists.

To refresh the snapshot from the corpus, see README.md ("Updating the snapshot").
"""
import argparse, json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE                       # snapshot lives under this tool's own folder
sys.path.insert(0, str(ROOT))
from rules.star_system_generation import generate_star_system, load_table  # noqa: E402

LIB = ROOT / "data" / "systems" / "library.json"


def load_library():
    if LIB.exists():
        return json.load(open(LIB, encoding="utf-8"))
    return {"_doc": "System-tool library. Each entry is a star_system.schema.json "
                    "system, plus tool-added fields: elements may carry name and "
                    "_ui:{angle}. Generated/edited via the system-tool.",
            "systems": []}


def table_names(table_id, *paths):
    """Extract the short result names from a generation table.
    paths: keys into the table dict leading to row lists (subtables handled)."""
    t = load_table(table_id)
    rows = t
    for p in paths:
        rows = rows[p]
    return [r["name"] for r in rows if isinstance(r, dict) and r.get("name")]


def build_options():
    elements = set()
    for zone_rows in load_table("table_1_3_system_elements")["subtables"].values():
        elements |= {r["name"] for r in zone_rows if r.get("name")}
    opts = {
        "_doc": "Enumerated category names extracted from data/tables/world_generator/ "
                "for the system-tool editor dropdowns.",
        "element_types": sorted(elements),
        "star_types": [r["name"] for r in load_table("table_1_2_star_generation")["rows"] if r.get("name")],
        "body_rocky": table_names("table_1_6_body", "subtables", "rocky_planets"),
        "body_gas": table_names("table_1_6_body", "subtables", "gas_giants"),
        "gravity": table_names("table_1_7_gravity", "subtables", "rocky_planets"),
        "gravity_gas": table_names("table_1_7_gravity", "subtables", "gas_giants"),
        "orbital_features": sorted({n for sub in ("rocky_planets", "gas_giants")
                                    for n in table_names("table_1_8_orbital_features", "subtables", sub)}),
        "atmospheric_presence": table_names("table_1_9_atmospheric_presence", "rows"),
        "atmospheric_composition": table_names("table_1_10_atmospheric_composition", "rows"),
        "climate": table_names("table_1_11_climate", "rows"),
        "habitability": table_names("table_1_12_habitability", "rows"),
        "zones": ["inner_cauldron", "primary_biosphere", "outer_reaches"],
    }
    # de-noise: drop placeholder rows
    for k, v in opts.items():
        if isinstance(v, list):
            opts[k] = [x for x in v if x and x.lower() not in ("no feature", "none")] \
                if k == "orbital_features" else v
    return opts


def write_wrappers(lib):
    (HERE / "data.js").write_text(
        "window.SYSTEM_LIBRARY = " + json.dumps(lib, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    (HERE / "options.js").write_text(
        "window.SYSTEM_OPTIONS = " + json.dumps(build_options(), ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int)
    ap.add_argument("--name")
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--rebuild", action="store_true", help="only regenerate data.js/options.js")
    args = ap.parse_args()

    lib = load_library()
    if not args.rebuild:
        for i in range(args.count):
            # Derive per-item seeds so a seeded BATCH is reproducible. Until
            # 2026-07-31 both --seed and --name were discarded whenever
            # --count != 1, so `--seed 42 --count 3` drew three random seeds
            # and told the user nothing — the generator is fully deterministic,
            # so the CLI was throwing that guarantee away.
            if args.seed is not None:
                seed = args.seed + i
            else:
                seed = random.randrange(1, 10 ** 6)
            if args.name is None:
                name = None
            elif args.count == 1:
                name = args.name
            else:
                name = f"{args.name} {i + 1}"      # distinguishable within the batch
            s = generate_star_system(seed=seed, name=name)
            # uniquify id
            base = s["id"]; n = 2
            while any(x["id"] == s["id"] for x in lib["systems"]):
                s["id"] = f"{base}_{n}"; n += 1
            lib["systems"].append(s)
            print(f"generated {s['id']}  ({s['name']}, seed {seed})")
    LIB.parent.mkdir(parents=True, exist_ok=True)
    json.dump(lib, open(LIB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write_wrappers(lib)
    print(f"library: {len(lib['systems'])} system(s) -> {LIB}")
    print("wrappers regenerated: data.js, options.js")


if __name__ == "__main__":
    main()
