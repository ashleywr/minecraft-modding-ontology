# Governance

## Maintainers

The repository has a small group of maintainers with merge rights. Maintainers review
pull requests, moderate discussions, and make final calls on disputed taxonomy decisions.

The current maintainer list is kept in [MAINTAINERS.md](MAINTAINERS.md).

Additional maintainers can be nominated by any existing maintainer via a Discussion in
the **Meta** category. Nominations are confirmed by consensus among existing maintainers.

---

## Decision making

Most contributions (adding a token, fixing a tag, translating a label) are
uncontroversial and reviewed by any available maintainer.

Larger decisions follow this path:

```
Discussion opened
      ↓
Community weighs in (no fixed time limit; discussions close when there is clear
consensus or clear deadlock, not on a schedule)
      ↓
Maintainer closes discussion with a documented decision
The closing comment becomes the canonical rationale for the record
      ↓
Issue created (links to discussion)
      ↓
PR opened and reviewed
      ↓
Merged — issue closed, discussion linked in commit message
```

When a maintainer closes a contested discussion, they document the reasoning in the
closing comment. This record serves the same role as a Wikipedia talk page closure:
a reference point for future "why does X work this way?" questions.

---

## Principles

**Decisions are documented.** Every non-trivial merge links to the issue or discussion
that motivated it. Taxonomy choices that seem obvious today may be questioned in three
years; the reasoning should survive.

**Criteria are public.** The qualification threshold for mod-specific categories, the
facet DSL format, and the contribution process are all defined in this repository.
Nothing is decided behind closed doors.

**No mod favoritism.** A PR that quietly shifts routing to benefit one specific mod
without improving general accuracy will be rejected. Reviewers should verify proposed
changes against multiple mods, not just the one the contributor cares about. When in
doubt, request examples from two or three different mods before merging.

**Stability over completeness.** A missing facet is better than a wrong one. When a
proposed facet or routing rule would help 10 items but misclassify 5 others, it should
wait until the definition is tighter. Conservative merges are the default.

**Facets and categories are separate concerns.** Facets capture properties that are
true about items regardless of how any tool displays them. Categories are one
organization scheme built on top of those properties; other tools can use the same
facets to build different trees.

---

## Mod-specific categories

Mods that are large enough and diverse enough can earn a dedicated top-level category
in `mod-categories/`. The threshold exists because scattering a very large mod's items
across many generic categories produces a worse player experience than grouping them.

### Qualification criteria

All three of the following should be present in a nomination:

**1. Item count**
At least approximately 150 unique, distinct items. Color and material variants of the
same item type don't count separately. A mod with 200 shades of the same decorative
block has one item type.

**2. Subcategory spread**
Items span at least 4 generic subcategories. A mod with 300 items all in the same
subcategory does not need its own category.

**3. Popularity**
A meaningful current install or download count on Modrinth or CurseForge, demonstrating
that the category would benefit a real number of players. There is no fixed minimum; the
Discussion evaluates this alongside the other criteria.

No single criterion is a hard gate. A mod with extraordinary diversity but moderate
downloads can qualify. A mod with enormous downloads but items that all fit one
subcategory should wait.

### Nomination process

1. Open a [Mod Category nomination issue](.github/ISSUE_TEMPLATE/new-mod-category.yml)
2. Include: mod name, mod ID, approximate item count, which generic subcategories its
   items currently land across (with examples), current download figures
3. Maintainers review the nomination against the criteria above
4. If accepted: a PR adds `mod-categories/mod-id/` with the qualification metadata
   recorded in `_index.yml`

### Removal policy

Mod-specific categories are not removed if a mod becomes less popular or unmaintained.
Removal is more disruptive to tools and users than retention. A category may be marked
deprecated in its `_index.yml` if a mod is formally abandoned and a clear successor
exists.

---

## Schema versioning

Changes to the YAML schema format itself (new required fields, renamed keys, removed
support for old syntax) are major version bumps and require a migration note in
`migrations/`. Maintainers are responsible for communicating breaking changes clearly
in the release notes and CHANGELOG.

---

## Code of conduct

This project follows the
[Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
Maintainers are responsible for enforcement.
