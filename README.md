# Minecraft Modding Ontology

A community-maintained vocabulary for classifying Minecraft modded items. Ideally to be able to be used by item
search overlays, recipe viewers, sorting mods, and server tools to consistently organize
the thousands of items that modpacks can contain.

No programming knowledge required to contribute. Most contributions are likely to be small edits to
human-readable text files.

---

## How it works

Every Minecraft item can be described by a set of **facets**, properties like *seed*,
*machine*, *door*, or *melee weapon*. An item can have many facets at once. A wheat seed
is `seed`, `compostable`, and `placeable` simultaneously.

The **categories** folder defines how facets map to the browsable tree that players see.
The *Seeds & Saplings* subcategory shows anything with the `seed` facet. *Tech / Machines*
shows anything with the `machine` facet.

```
Item gets decorated with all applicable facets
───────────────────────────────────────────────────────────────
create:mechanical_mixer  →  [machine] [mechanical_component]
                            [has_block_entity] [placeable]

Category routing picks the best-matching subcategory
───────────────────────────────────────────────────────────────
machine facet  →  Tech / Machines  ✓
```

Because facets and categories are separate folders, contributors can work on detection
rules without touching routing logic, and vice versa.

---

## Repository layout

```
facets/           What things ARE. Detection rules using tags, path words, data components
categories/       Where things APPEAR. Routing rules that reference facets
mod-categories/   Dedicated groupings for large, diverse mods (Create, Cobblemon, etc.)
schema/           Validation rules that CI checks on every pull request
```

Within `facets/` and `categories/` the directory structure mirrors the ontology itself.
The path `facets/natural/seed.yml` tells you the facet ID is `natural/seed`. You can
browse the folder tree on GitHub and understand the structure without reading any
documentation.

---

## How to contribute

### An item from my mod lands in the wrong place

[Open a Misclassification issue](.github/ISSUE_TEMPLATE/misclassified-items.yml) and
describe the item and where it should go. To fix it yourself:

1. Browse `facets/` to find the facet that should apply
2. Open the `.yml` file and check the `matches:` section
3. If your mod's tags or item name words are missing, add them
4. Open a pull request

### I want to add a translation

Find any `.yml` file in `facets/` or `categories/`, and create a copy with your locale
code inserted before `.yml`:

```
facets/natural/seed.yml        ← original (English)
facets/natural/seed.de.yml     ← German
facets/natural/seed.zh_cn.yml  ← Simplified Chinese
facets/natural/seed.pt_br.yml  ← Brazilian Portuguese
```

Translation files contain only `label` and `description`. Detection rules live only in
the canonical file and are not translated. Open a pull request. Missing translations
fall back to English automatically.

To add translations across the entire ontology at once, which is likely needed at first, will take some minor tooling that will ideally come in the near future, or please add it yourself!

### I think a new facet is needed

[Open a New Facet issue](.github/ISSUE_TEMPLATE/new-facet.yml) and describe what
property you want to capture, with examples of items that would have it.

### I want to debate the taxonomy

[Start a Discussion](../../discussions). Questions about where things belong, proposals
for new categories, "should X and Y be the same facet?" debates, and structural ideas
all live there. Discussions that reach a clear conclusion get converted into issues and
then pull requests.

### My mod should have its own top-level category

Large, diverse mods can earn a dedicated top-level category. See the
[qualification criteria](GOVERNANCE.md#mod-specific-categories) and open a
[Mod Category nomination](.github/ISSUE_TEMPLATE/new-mod-category.yml).

---

## Facet file format

```yaml
# facets/natural/seed.yml

label: Seed
description: >
  A plantable seed, crop seed, or sapling. Items receive this facet
  regardless of what other facets they also have.

matches:
  tags:       [c:seeds, forge:seeds, minecraft:saplings]
  block_tags: [minecraft:saplings]
  path_words: [seed, seeds, sapling, saplings]

except_when:
  path_words: [pouch, bucket, machine, maker]
  # "seed pouch" and "oil-seed press" are not seeds
```

The file path is the facet's ID: `facets/natural/seed.yml` becomes `natural/seed`.

**`matches`**: the item has at least one of these properties  
**`requires`**: the item must also satisfy all of these (additional constraints)  
**`except_when`**: if any of these match, the facet is not assigned

Available match types: `tags`, `block_tags`, `path_words`, `components`,
`creative_tab`, `has_facet`. See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## Category file format

```yaml
# categories/tech/machines/_index.yml

label: Machines
description: >
  Blocks that perform automated processing, generation, or transformation.

show_if_any:
  - tech/machine
  - tech/workstation

priority: high
```

The `show_if_any` list references facet IDs by path. `priority` is a hint for tools
when an item qualifies for multiple subcategories; a `high` subcategory takes precedence.

---

## For tool developers

The ontology is published as a versioned release on this repository. Each release tag
follows semantic versioning:

- **Patch** (1.0.x): new entries, new tokens, new tags. Safe to update without code changes.
- **Minor** (1.x.0): new facets or subcategories. May require new display strings.
- **Major** (x.0.0): renamed or removed facets, schema format changes.

Facet IDs are derived from file paths: `facets/natural/seed.yml` becomes `natural/seed`.
Translation files are excluded from IDs.

See [CHANGELOG.md](CHANGELOG.md) for a full history of changes between versions.

---

## License

[CC0 1.0 Universal](LICENSE). Public domain. No attribution required.
Usable in commercial mods and tools without restriction.
