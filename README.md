# System Tool — Rogue Trader Star-System Generator & Chart

A single-page browser tool that **generates, edits, and renders individual star
systems** for the Rogue Trader campaign. It drives the full RT14 *Stars of
Inequity* procedural world-generation pipeline (in Python) and displays each
system as an orbital chart — star glyph, solar zones, planets, and other system
elements — that the GM can inspect and hand-edit. Companion to the
**reach-map-tool** sector chart.

## Quick start

Open **`index.html`** in any modern browser (`file://` is fine). It loads
`data.js`, `options.js`, and `app.js`, and renders the system selected in the
**Library** dropdown from `window.SYSTEM_LIBRARY`. Deep-link a specific system
with `index.html#<system_id>`.

To create new systems you run the Python bridge (below) and reload the page —
generation is a Python step, not done in the browser.

## Generating systems

The generator is **`gen_system.py`** (Python 3 standard library only):

```
python gen_system.py --seed 42 --name "Solivarn"   # generate one system, fixed seed
python gen_system.py --count 3                      # generate several (random seeds)
python gen_system.py --rebuild                      # just rebuild data.js/options.js from the library
```

Each run walks the 27 canonical RT14 tables (System Features → Star → Elements →
per-planet Body/Gravity/Atmosphere/Climate/Habitability/Territories/Resources/
Inhabitants, plus derelict-station and starship-graveyard origins), appends the
new system to the canonical library, and regenerates the browser wrappers.
Reload `index.html` to see it. The **Generate** sidebar section builds the exact
command for you (seed + name) and copies it to the clipboard.

## Editing & persistence workflow

The browser app edits an in-memory copy of the library. To persist:

1. In the **Data** section, click **Export Library** — downloads `library.json`.
2. Save it over **`data/systems/library.json`**.
3. Run **`python gen_system.py --rebuild`** to regenerate `data.js` / `options.js`.
4. Reload `index.html`.

`Ctrl+Z` undoes the last edit in the browser.

## Data model

- `window.SYSTEM_LIBRARY` (`data.js`) — `{ systems: [ … ] }`. Each entry is a
  `star_system.schema.json` system plus tool-added fields (elements may carry a
  `name` and `_ui:{angle}` for chart placement).
- `window.SYSTEM_OPTIONS` (`options.js`) — enumerated category names (body
  classes, climates, gravities, orbital features, star types, zones…) extracted
  live from the generation tables, so the editor's dropdowns always match the
  corpus rather than hard-coded lists.
- Canonical store: **`data/systems/library.json`** — `gen_system.py` reads and
  writes this; `data.js`/`options.js` are derived wrappers (do not hand-edit).

## Files

| File | Role |
|------|------|
| `index.html`   | App shell, styling, sidebar UI |
| `app.js`       | Chart rendering + element editor (`window.SYSTEM_LIBRARY`-driven) |
| `data.js`      | Generated: `window.SYSTEM_LIBRARY` |
| `options.js`   | Generated: `window.SYSTEM_OPTIONS` (editor dropdown vocabularies) |
| `gen_system.py`| Generator bridge: runs the engine, maintains the library + wrappers |
| `BUILD_INFO.json` / `_GENERATED_DO_NOT_EDIT.txt` | Build provenance (generated). Rebuild via `rogue_trader/build_apps.py` |
| `rules/`       | Snapshot of the RT14 engine modules (see below) |
| `data/tables/world_generator/` | RT14 star-system generation tables (29 files) |
| `data/tables/treasure/`        | Treasure tables (xenos ruins / derelicts) |
| `data/tables/starships/`       | Starship-graveyard tables |
| `data/systems/library.json`    | Canonical system library (generated/edited) |

### Bundled engine (`rules/`)

To make the tool portable, the generation engine is snapshotted locally:

- `star_system_generation.py` — the RT14 pipeline (`generate_star_system`, `load_table`)
- `treasure_generation.py` — lazily called for xenos-ruin / derelict contents
- `starship_generation.py` — lazily called for starship-graveyard elements

`gen_system.py` puts the tool folder on `sys.path` and imports
`rules.star_system_generation`; the engine resolves its own tables relative to
this folder, so no path back into `codified-systems/` is required.

## Built from the corpus

This is a **generated bundle** — do not hand-edit (see `_GENERATED_DO_NOT_EDIT.txt`). The
hand-edited source lives in `codified-systems/rogue_trader/apps/rt2_system_map_tool/` (the UI +
`gen_system.py`); the RT14 engine (`rules/`) and tables (`data/`) bundled here are copies of the
corpus — the single source of truth.

Rebuild this bundle after editing the corpus engine, the tables, or the app source:

```
python codified-systems/rogue_trader/build_apps.py rt2_system_map_tool
```

It re-copies the declared engine + tables, runs `gen_system.py --rebuild`, and writes
`BUILD_INFO.json`. Because this is a **self-contained generator** bundle, you can still generate
new systems locally with `python gen_system.py --seed N` and they persist in this bundle's
`data/systems/library.json` (promote them into the corpus when you want them upstream). See
`docs/TOOLS_PIPELINE_PLAN.md` for the architecture.

## Integration

The `#<system_id>` deep-link contract lets the **reach-map-tool** sector chart
open a planet's detailed system view here. The editor's dropdown vocabularies
(`options.js`) are sourced from the same RT14 tables the generator uses, keeping
hand-edits consistent with generated content.
