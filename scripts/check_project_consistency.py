#!/usr/bin/env python3
"""Check cross-surface counts, release metadata, and generated discovery files."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from build_hf_card import project_context, render_card


ROOT = Path(__file__).resolve().parents[1]


def require(path: Path, snippets: list[str], failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            failures.append(f"{path.relative_to(ROOT)}: missing {snippet!r}")


def main() -> int:
    context = project_context()
    count = context["RESOURCE_COUNT"]
    version = context["VERSION"]
    failures: list[str] = []

    require(
        ROOT / "README.md",
        [
            f"resources-{count}-",
            f"**{count} curated resources**",
            f"covers all {count} rows",
        ],
        failures,
    )
    require(
        ROOT / "docs" / "index.html",
        [
            f'content="{count} audited resources',
            f">{count}</b><span>curated entries</span>",
            f"Search {count} audited works",
            f"Search {count} audited resources",
            f'"version": "{version}"',
        ],
        failures,
    )
    require(ROOT / "meta" / "social-preview.html", [f">{count}</b>"], failures)
    require(ROOT / "posts" / "launch.md", [f"# Awesome Loop Engineering v{version}", f"{count} audited resources"], failures)
    require(ROOT / "posts" / "launch.zh-CN.md", [f"# Awesome Loop Engineering v{version}", f"{count} 条"], failures)
    require(ROOT / "meta" / "DISTRIBUTION.md", [f"v{version}", f"{count} audited resources"], failures)

    for translation in sorted(ROOT.glob("README.*.md")):
        require(translation, [count], failures)

    with (ROOT / "data" / "resources.csv").open(encoding="utf-8", newline="") as handle:
        csv_count = sum(1 for _ in csv.DictReader(handle))
    if csv_count != int(count):
        failures.append(f"data/resources.csv: expected {count} rows, found {csv_count}")

    site_payload = json.loads((ROOT / "docs" / "assets" / "resources.json").read_text(encoding="utf-8"))
    if site_payload.get("count") != int(count) or len(site_payload.get("resources", [])) != int(count):
        failures.append("docs/assets/resources.json: count or resources array is stale")

    _, card_failures = render_card()
    failures.extend(card_failures)

    if failures:
        print("Project consistency check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        f"Validated {count} resources, {context['PATTERN_COUNT']} patterns, "
        f"{context['CONTRACT_COUNT']} contracts, and release v{version}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
