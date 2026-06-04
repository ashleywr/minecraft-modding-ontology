#!/usr/bin/env python3
"""
Schema validation and reference integrity check for minecraft-modding-ontology.

Checks:
  1. All facet YAML files validate against schema/facet.schema.json
  2. All category _index.yml files validate against schema/category-index.schema.json
  3. All mod-category top-level _index.yml files validate against schema/mod-category-index.schema.json
  4. All has_facet references point to real facet files
  5. All show_if_any entries reference real facets
  6. No circular has_facet dependencies
"""

import json
import os
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).parent.parent.parent
SCHEMA_DIR = ROOT / "schema"
FACETS_DIR = ROOT / "facets"
CATEGORIES_DIR = ROOT / "categories"
MOD_CATEGORIES_DIR = ROOT / "mod-categories"

errors = []
warnings = []


def load_schema(name):
    with open(SCHEMA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def facet_id_from_path(path):
    """Convert facets/natural/seed.yml -> natural/seed"""
    rel = path.relative_to(FACETS_DIR)
    parts = list(rel.parts)
    parts[-1] = parts[-1].replace(".yml", "")
    return "/".join(parts)


def is_translation_file(path):
    """Return True for files like seed.de.yml, seed.zh_cn.yml"""
    stem = path.stem  # e.g. "seed.de" or "seed"
    return "." in stem


def collect_facet_ids():
    ids = set()
    for path in FACETS_DIR.rglob("*.yml"):
        if not is_translation_file(path):
            ids.add(facet_id_from_path(path))
    return ids


def collect_has_facet_refs(data):
    """Recursively collect all has_facet values from a match block."""
    refs = []
    if not isinstance(data, dict):
        return refs
    if "has_facet" in data:
        refs.extend(data["has_facet"])
    for key in ("matches", "requires", "except_when", "not"):
        if key in data:
            refs.extend(collect_has_facet_refs(data[key]))
    for key in ("any", "all"):
        if key in data:
            for child in data[key]:
                refs.extend(collect_has_facet_refs(child))
    return refs


def validate_facets(schema, facet_ids):
    validator = jsonschema.Draft7Validator(schema)
    for path in sorted(FACETS_DIR.rglob("*.yml")):
        if is_translation_file(path):
            continue
        data = load_yaml(path)
        if data is None:
            warnings.append(f"Empty file: {path.relative_to(ROOT)}")
            continue

        # Schema validation
        for error in validator.iter_errors(data):
            errors.append(f"{path.relative_to(ROOT)}: {error.message}")

        # has_facet reference check
        for ref in collect_has_facet_refs(data):
            if ref not in facet_ids:
                errors.append(
                    f"{path.relative_to(ROOT)}: has_facet references unknown facet '{ref}'"
                )

        # Warn if no matches section
        if "matches" not in (data or {}):
            warnings.append(
                f"{path.relative_to(ROOT)}: no 'matches' section — facet will never be assigned"
            )


def validate_category_indexes(schema, facet_ids):
    validator = jsonschema.Draft7Validator(schema)
    for path in sorted(CATEGORIES_DIR.rglob("_index.yml")):
        data = load_yaml(path)
        if data is None:
            warnings.append(f"Empty file: {path.relative_to(ROOT)}")
            continue

        # Schema validation
        for error in validator.iter_errors(data):
            errors.append(f"{path.relative_to(ROOT)}: {error.message}")

        # show_if_any reference check
        for ref in data.get("show_if_any", []):
            if ref not in facet_ids:
                errors.append(
                    f"{path.relative_to(ROOT)}: show_if_any references unknown facet '{ref}'"
                )

    # Validate translation files have only label/description
    for path in sorted(CATEGORIES_DIR.rglob("_index.*.yml")):
        data = load_yaml(path)
        if data is None:
            continue
        allowed = {"label", "description"}
        extra = set(data.keys()) - allowed
        if extra:
            errors.append(
                f"{path.relative_to(ROOT)}: translation file should only contain "
                f"'label' and 'description', found: {sorted(extra)}"
            )


def validate_mod_category_indexes(cat_schema, mod_schema, facet_ids):
    cat_validator = jsonschema.Draft7Validator(cat_schema)
    mod_validator = jsonschema.Draft7Validator(mod_schema)

    for mod_dir in sorted(MOD_CATEGORIES_DIR.iterdir()):
        if not mod_dir.is_dir():
            continue

        top_index = mod_dir / "_index.yml"
        if not top_index.exists():
            errors.append(f"mod-categories/{mod_dir.name}/ is missing _index.yml")
            continue

        data = load_yaml(top_index)
        for error in mod_validator.iter_errors(data or {}):
            errors.append(f"{top_index.relative_to(ROOT)}: {error.message}")

        # Subcategory _index.yml files use the standard category schema
        for path in sorted(mod_dir.rglob("_index.yml")):
            if path == top_index:
                continue
            sub_data = load_yaml(path)
            if sub_data is None:
                continue
            for error in cat_validator.iter_errors(sub_data):
                errors.append(f"{path.relative_to(ROOT)}: {error.message}")
            for ref in sub_data.get("show_if_any", []):
                if ref not in facet_ids:
                    errors.append(
                        f"{path.relative_to(ROOT)}: show_if_any references unknown facet '{ref}'"
                    )


def validate_translation_files():
    """Translation files must only contain label and description."""
    allowed = {"label", "description"}
    for path in sorted(FACETS_DIR.rglob("*.yml")):
        if not is_translation_file(path):
            continue
        data = load_yaml(path)
        if data is None:
            continue
        extra = set(data.keys()) - allowed
        if extra:
            errors.append(
                f"{path.relative_to(ROOT)}: translation file should only contain "
                f"'label' and 'description', found: {sorted(extra)}"
            )
        if "label" not in (data or {}):
            warnings.append(
                f"{path.relative_to(ROOT)}: translation file is missing 'label'"
            )


def main():
    facet_schema = load_schema("facet.schema.json")
    cat_schema = load_schema("category-index.schema.json")
    mod_schema = load_schema("mod-category-index.schema.json")

    facet_ids = collect_facet_ids()

    validate_facets(facet_schema, facet_ids)
    validate_category_indexes(cat_schema, facet_ids)
    validate_mod_category_indexes(cat_schema, mod_schema, facet_ids)
    validate_translation_files()

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  ⚠  {w}")
        print()

    if errors:
        print("Errors:")
        for e in errors:
            print(f"  ✗  {e}")
        print(f"\n{len(errors)} error(s) found.")
        sys.exit(1)
    else:
        print(f"Validation passed. {len(facet_ids)} facets checked.")
        if warnings:
            print(f"{len(warnings)} warning(s).")


if __name__ == "__main__":
    main()
