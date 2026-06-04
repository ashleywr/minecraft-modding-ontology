# Contributing to Minecraft Modding Ontology

Thank you for helping improve item classification for the whole Minecraft modding
community. This guide covers every type of contribution, from fixing a single wrong
token to proposing a new category.

No programming experience is required for most contributions.

---

## Understanding the two files you'll touch most

### Facet files (`facets/**/*.yml`)

A facet file describes a property that items can have. It answers: *"what signals tell
us an item has this property?"*

```yaml
label: Seed
description: >
  A plantable seed, crop seed, or sapling.

matches:
  tags:       [c:seeds, forge:seeds]
  path_words: [seed, seeds, sapling]

except_when:
  path_words: [pouch, bucket]
  # seed pouches are containers, not seeds
```

The `matches` section lists signals that identify an item as having this facet. If *any*
signal matches, the facet is assigned. The `except_when` section overrides matches. If
any of those signals match, the facet is not assigned regardless of what `matches` found.

### Category index files (`categories/**/_index.yml`)

A category index file describes a browsable bucket in the tree. It answers: *"which
facets should cause an item to appear here?"*

```yaml
label: Seeds & Saplings
description: Plantable seeds, crop seeds, and saplings.

show_if_any:
  - natural/seed
  - natural/crop

priority: high
```

If an item has *any* of the listed facets, it can appear in this subcategory. `priority`
hints to tools which subcategory should win when an item qualifies for multiple.

---

## Contribution types

### 1. Fix a misclassified item

**Symptom:** Items from a mod appear in the wrong place (e.g., a rail item landing in
*Tech / Machines* instead of *Tech / Transport*).

**Fix:** The item is probably missing a facet, or has the wrong one.

1. Find the correct facet file by browsing `facets/` (e.g., `facets/transport/rail.yml`)
2. Look at the `matches:` section
3. Check your item's registry ID (e.g., `traincraft:iron_rail`). Does any word in the
   path appear in `path_words`? Does the item have any of the listed tags?
4. If not, add the missing word or tag to the appropriate list
5. Leave a comment (lines starting with `#`) explaining why if it isn't obvious
6. Open a pull request

**Tip:** If you're not sure which facet file is relevant, open an issue and describe the
problem. A maintainer will point you in the right direction.

---

### 2. Add a missing match signal

**Symptom:** You know which facet file is right, but your mod's items don't match it
because the mod uses different tag names or unusual item names.

1. Open the facet file
2. Add your tag to `tags:` or `block_tags:`, or add your path word to `path_words:`
3. If you're adding a word that might accidentally match unrelated items, add those
   unrelated words to `except_when: path_words:` with a comment explaining why
4. Open a pull request

```yaml
# Before
matches:
  tags: [c:seeds, forge:seeds]

# After — added mythicbotany's tag
matches:
  tags: [c:seeds, forge:seeds, mythicbotany:seeds]
```

---

### 3. Add a translation

Translation files sit alongside the originals with a locale code inserted before `.yml`.

| Locale | Code | Example filename |
|--------|------|-----------------|
| German | `de` | `seed.de.yml` |
| Simplified Chinese | `zh_cn` | `seed.zh_cn.yml` |
| Brazilian Portuguese | `pt_br` | `seed.pt_br.yml` |
| French | `fr` | `seed.fr.yml` |
| Japanese | `ja` | `seed.ja.yml` |

Translation files contain **only** `label` and `description`. Do not copy detection
rules; they are language-independent and ignored in translation files.

```yaml
# facets/natural/seed.de.yml
label: Samen
description: >
  Ein pflanzlicher Samen, Erntesamen oder Setzling.
```

You can translate any file in `facets/` or `categories/`. Translate as many or as few
as you like. Partial translations are welcome. Missing translations always fall back to
English automatically.

---

### 4. Propose a new facet

If items exist that genuinely cannot be described by any current facet, open a
[New Facet issue](.github/ISSUE_TEMPLATE/new-facet.yml).

Include:
- What property you're trying to capture
- 3 to 5 example items that should have this facet
- Whether any existing facet is close but not quite right

If the discussion confirms the facet is needed, either you or a maintainer will create
the facet file in the appropriate `facets/` subfolder.

---

### 5. Propose a new subcategory or category

Open a Discussion in the **Taxonomy** category rather than an issue directly. These
decisions affect many items and need broader input before becoming PRs.

Good discussion prompts:
- "Should *decoration/furniture* be split into *seating* and *tables*? Here's why..."
- "I think we need a new *geology* category separate from *building* — here are the
  items that don't fit well today..."

Once a Discussion reaches consensus, a maintainer will convert it to an issue and the
PR process begins.

---

### 6. Nominate a mod for its own top-level category

Large, diverse mods can earn a dedicated top-level category in `mod-categories/`. See
[GOVERNANCE.md](GOVERNANCE.md#mod-specific-categories) for the qualification criteria.

Open a [Mod Category nomination](.github/ISSUE_TEMPLATE/new-mod-category.yml) rather
than a Discussion. Nominations use a standard format for evaluating the criteria.

---

## Match signal reference

| Key | What it checks |
|-----|----------------|
| `tags` | Item has this tag (e.g., `c:seeds`, `minecraft:saplings`) |
| `block_tags` | The placed block has this tag |
| `path_words` | Any word in the item's registry path (split on `_`, `-`, `/`, spaces) |
| `components` | Item has this data component (e.g., `minecraft:food`) |
| `creative_tab` | Creative tab ID or label contains this word |
| `has_facet` | Item already matched this other facet (use path-style ID like `natural/seed`) |

**Tag namespace conventions:**

| Prefix | Meaning |
|--------|---------|
| `minecraft:` | Vanilla, works on all loaders |
| `c:` | Cross-loader (Fabric + NeoForge unified) |
| `forge:` | NeoForge / legacy Forge only |
| `fabric:` | Fabric only |

When both `c:` and `forge:` versions of a tag exist, include both.

---

## Complex match logic

For the rare case where simple `matches`/`requires`/`except_when` isn't expressive
enough, you can use explicit logic combinators:

```yaml
matches:
  any:
    - tags: [c:seeds]
    - all:
        - path_words: [seed]
        - tags: [c:crops]
  not:
    path_words: [oil, press]
```

Use the simple form first. Reach for `any`/`all`/`not` only when you genuinely need it.
Complex logic is harder for reviewers to verify.

---

## Running validation locally

To check your changes before opening a PR:

```bash
pip install pyyaml jsonschema
python .github/scripts/validate.py
```

CI runs the same script automatically on every PR. Results appear in the checks panel
on your pull request.

---

## Pull request guidelines

- Keep PRs focused. One issue per PR is easier to review and revert if needed.
- If your change is non-obvious, add a `#` comment to the YAML explaining why.
- Reference the issue or discussion your PR addresses in the PR description.
- Translation-only PRs don't need issue references.
