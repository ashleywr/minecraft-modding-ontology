#!/usr/bin/env python3
"""
Generates a translation completeness report.
Outputs a markdown table showing coverage per locale across facet and category files.
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
FACETS_DIR = ROOT / "facets"
CATEGORIES_DIR = ROOT / "categories"


def is_translation_file(path):
    return "." in path.stem


def locale_from_path(path):
    # seed.de.yml -> "de", seed.zh_cn.yml -> "zh_cn"
    parts = path.stem.split(".")
    return parts[-1] if len(parts) > 1 else None


def collect_base_files(root_dir):
    return {
        p for p in root_dir.rglob("*.yml")
        if not is_translation_file(p) and p.name != "_index.yml"
    }


def collect_index_files(root_dir):
    return {p for p in root_dir.rglob("_index.yml")}


def collect_translations(root_dir):
    translations = defaultdict(set)
    for path in root_dir.rglob("*.yml"):
        locale = locale_from_path(path)
        if locale:
            # Normalise to base path: seed.de.yml -> seed.yml
            base = path.parent / (path.stem.rsplit(".", 1)[0] + ".yml")
            translations[locale].add(base)
    return translations


def main():
    facet_bases = collect_base_files(FACETS_DIR)
    cat_bases = collect_index_files(CATEGORIES_DIR)
    all_bases = facet_bases | cat_bases
    total = len(all_bases)

    if total == 0:
        return

    facet_translations = collect_translations(FACETS_DIR)
    cat_translations = collect_translations(CATEGORIES_DIR)

    locales = sorted(set(facet_translations) | set(cat_translations))
    if not locales:
        print("No translation files found yet.")
        return

    rows = []
    for locale in locales:
        covered = len(facet_translations[locale] | cat_translations[locale])
        pct = int(covered / total * 100)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        rows.append((locale, covered, total, pct, bar))

    print("| Locale | Coverage | |")
    print("|--------|----------|---|")
    for locale, covered, total, pct, bar in rows:
        print(f"| `{locale}` | {covered}/{total} ({pct}%) | {bar} |")


if __name__ == "__main__":
    main()
