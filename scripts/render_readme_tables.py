#!/usr/bin/env python3
"""Render README resources as compact, metadata-rich Markdown tables."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from export_resource_dataset import README, TYPE_MARKERS, iter_rows


TABLE_HEADERS = ("Resource", "Published at", "Key feature")
LEGACY_TABLE_HEADERS = {TABLE_HEADERS, ("Resource", "Publication / source", "Key feature")}
SUMMARY_START = "<!-- resource-type-summary:start -->"
SUMMARY_END = "<!-- resource-type-summary:end -->"
PROJECT_GITHUB_REPO = "chaoyue0307/awesome-loop-engineering"

TYPE_DESCRIPTIONS = {
    "Paper": "Academic paper, preprint, or technical report",
    "Blog": "Essay, field note, article, or practitioner write-up",
    "Docs": "Official product, API, SDK, or platform documentation",
    "Tool": "Repository, framework, SDK, runtime, or implementation",
    "Benchmark": "Benchmark, eval suite, leaderboard, or evaluation dataset",
    "Pattern": "Operational playbook or reusable workflow",
    "Template": "Template, checklist, schema, guide, or contribution artifact",
    "List": "Adjacent awesome list, ecosystem map, or curated collection",
    "Critique": "Risk analysis, limitation, caveat, or skeptical take",
}

GITHUB_OWNER_LABELS = {
    "cloudflare": "Cloudflare",
    "vercel": "Vercel",
}


def escape_cell(value: str) -> str:
    return value.replace("|", r"\|")


def author_summary(authors: str) -> str:
    names = [name.strip() for name in authors.split(";") if name.strip()]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} & {names[1]}"
    return f"{names[0]} et al."


def repository_artifact_label(url: str) -> str:
    path = url.split("#", 1)[0]
    if path.startswith("patterns/"):
        return "Pattern library"
    if path.startswith("templates/"):
        return "Template library"
    if path.startswith("schemas/"):
        return "Schema"
    if path.startswith("examples/runnable/"):
        return "Runnable example"
    if path.startswith("examples/"):
        return "Example library"
    if path.startswith("gallery/"):
        return "Community gallery"
    if path.startswith("docs/"):
        return "Project website"
    if path.startswith("scripts/"):
        return "Repository utility"
    if path.startswith("meta/"):
        return "Project operations guide"
    if path.startswith("posts/"):
        return "Project article"
    return "Project documentation"


def publication_cell(row: dict[str, str]) -> str:
    year = row["publication_year"]
    resource_type = row["resource_type"]
    details: list[str] = []

    github_repo = row["github_repo"]
    if row["url_kind"] != "external":
        source = row["publication_venue"] or row["publisher"] or "GitHub"
        details.append(repository_artifact_label(row["url"]))
    elif github_repo.lower() == PROJECT_GITHUB_REPO:
        source = row["publication_venue"] or row["publisher"] or "GitHub"
        license_id = row["github_license"]
        if license_id and license_id != "NOASSERTION":
            details.append(f"License: {license_id}")
    elif github_repo:
        source = row["publisher"] or "GitHub"
        owner, separator, repository = github_repo.partition("/")
        owner = GITHUB_OWNER_LABELS.get(owner, owner)
        details.append(f"{owner}{separator}{repository}")
        license_id = row["github_license"]
        if license_id and license_id != "NOASSERTION":
            details.append(f"License: {license_id}")
    else:
        source = row["publication_venue"] or row["publisher"] or row["domain"] or "Source not stated"
        if resource_type in {"Paper", "Benchmark", "Blog", "Critique"}:
            author = author_summary(row["authors"])
            if author:
                details.append(author)

    primary = (
        f"**{escape_cell(year)}** · {escape_cell(source)}"
        if year
        else f"**{escape_cell(source)}**"
    )
    if details:
        secondary = " · ".join(escape_cell(detail) for detail in details)
        return f"{primary}<br><sub>{secondary}</sub>"
    return primary


def resource_cells(row: dict[str, str]) -> tuple[str, str, str]:
    title = escape_cell(row["title"])
    url = escape_cell(row["url"])
    annotation = escape_cell(row["annotation"])
    marker = escape_cell(row["marker"])
    resource_type = escape_cell(row["resource_type"])
    resource = f"{marker} **[{title}]({url})**<br><sub>{resource_type}</sub>"
    return resource, publication_cell(row), annotation


def markdown_table(headers: tuple[str, ...], data: list[tuple[str, ...]]) -> list[str]:
    # Remark aligns source offsets as UTF-16 code units, matching JavaScript.
    def source_length(value: str) -> int:
        return len(value.encode("utf-16-le")) // 2

    widths = [
        max(source_length(headers[index]), *(source_length(row[index]) for row in data))
        for index in range(len(headers))
    ]

    def format_row(row: tuple[str, ...]) -> str:
        cells = (
            cell + " " * (width - source_length(cell))
            for cell, width in zip(row, widths)
        )
        return "| " + " | ".join(cells) + " |"

    separator = tuple("-" * max(3, width) for width in widths)
    return [format_row(headers), format_row(separator), *(format_row(row) for row in data)]


def is_resource_table_header(line: str) -> bool:
    if not line.startswith("|"):
        return False
    cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
    return cells in LEGACY_TABLE_HEADERS


def is_table_separator(line: str) -> bool:
    if not line.startswith("|"):
        return False
    cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
    return len(cells) == len(TABLE_HEADERS) and all(
        len(cell) >= 3 and not cell.strip("-") for cell in cells
    )


def summary_lines(rows: list[dict[str, str]]) -> list[str]:
    counts = Counter(row["resource_type"] for row in rows)
    data = []
    for resource_type, marker in TYPE_MARKERS.items():
        data.append(
            (
                f"{marker} **{resource_type}**",
                str(counts[resource_type]),
                TYPE_DESCRIPTIONS[resource_type],
            )
        )
    return [SUMMARY_START, *markdown_table(("Type", "Rows", "Includes"), data), SUMMARY_END]


def replace_summary(lines: list[str], rows: list[dict[str, str]]) -> list[str]:
    try:
        start = lines.index(SUMMARY_START)
        end = lines.index(SUMMARY_END, start + 1)
    except ValueError as error:
        raise RuntimeError("README resource-type summary markers are missing") from error
    return lines[:start] + summary_lines(rows) + lines[end + 1 :]


def render_readme(readme_path: Path = README) -> str:
    rows = iter_rows(readme_path)
    rows_by_line = {int(row["source_line"]): row for row in rows}
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if is_resource_table_header(line):
            index += 1
            if index < len(lines) and is_table_separator(lines[index]):
                index += 1
            continue

        row = rows_by_line.get(index + 1)
        if row:
            run: list[tuple[str, ...]] = []
            while index < len(lines):
                row = rows_by_line.get(index + 1)
                if not row:
                    break
                run.append(resource_cells(row))
                index += 1
            output.extend(markdown_table(TABLE_HEADERS, run))
            continue

        output.append(line)
        index += 1

    output = replace_summary(output, rows)
    return "\n".join(output) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when README tables are stale")
    args = parser.parse_args()

    rendered = render_readme()
    current = README.read_text(encoding="utf-8")
    if args.check:
        if rendered != current:
            print("README resource tables are stale; run scripts/render_readme_tables.py", file=sys.stderr)
            return 1
        return 0

    README.write_text(rendered, encoding="utf-8")
    print(f"Rendered {len(iter_rows())} resource rows in {README.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
