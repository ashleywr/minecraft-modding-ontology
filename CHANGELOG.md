# Changelog

All notable changes to the ontology are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [semantic versioning](https://semver.org/):

- **Patch** (1.0.x) — new entries, tokens, tags. Safe to update without tool changes.
- **Minor** (1.x.0) — new facets or subcategories. Tools may need new display strings.
- **Major** (x.0.0) — renamed or removed facets, schema format changes. See `migrations/`.

---

## [1.0.0] — 2026-06-04

Initial release. Ontology bootstrapped from the AMI mod's classification system,
covering approximately 60 facets across 12 domains and 25 top-level categories.

### Facets added
- All facets from `facets/natural/`, `facets/tech/`, `facets/building/`,
  `facets/decoration/`, `facets/food/`, `facets/tools/`, `facets/armor/`,
  `facets/magic/`, `facets/ingredients/`, `facets/redstone/`,
  `facets/transport/`, `facets/utility/`

### Categories added
- `nature`, `tech`, `building`, `decoration`, `tools`, `armor`, `magic`,
  `ingredients`, `utility`

### Mod-specific categories added
- `create`, `cobblemon`, `ae2`, `mekanism`, `gregtech`, `apotheosis`,
  `botania`, `sophisticated`, `minecolonies`
