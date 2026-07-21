#!/usr/bin/env python3
"""Render README resources as compact, metadata-rich Markdown tables."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from export_resource_dataset import README, TYPE_MARKERS, iter_rows


TABLE_HEADERS = ("Resource", "Published at", "Contribution", "Evidence")
LEGACY_TABLE_HEADERS = {
    TABLE_HEADERS,
    ("Resource", "Published at", "Key feature"),
    ("Resource", "Publication / source", "Key feature"),
}
SUMMARY_START = "<!-- resource-type-summary:start -->"
SUMMARY_END = "<!-- resource-type-summary:end -->"
PROJECT_GITHUB_REPO = "chaoyue0307/awesome-loop-engineering"
README_RENDER_BUDGET_BYTES = 480 * 1024

TYPE_DESCRIPTIONS = {
    "Paper": "Academic paper, preprint, or technical report",
    "Blog": "Essay, field note, article, or practitioner write-up",
    "Docs": "Official product, API, SDK, or platform documentation",
    "Tool": "Repository, framework, SDK, runtime, or implementation",
    "Benchmark": "Benchmark, eval suite, leaderboard, or evaluation dataset",
    "Pattern": "Operational playbook or reusable workflow",
    "Template": "Template, checklist, schema, guide, or contribution artifact",
    "List": "Adjacent directory, ecosystem map, or reading list",
    "Critique": "Risk analysis, limitation, caveat, or skeptical take",
}

GITHUB_OWNER_LABELS = {
    "cloudflare": "Cloudflare",
    "vercel": "Vercel",
}

EVIDENCE_LABELS = {
    "research-paper": "Research paper",
    "research-preprint": "Research preprint",
    "official-documentation": "Official documentation",
    "technical-documentation": "Technical documentation",
    "source-implementation": "Source implementation",
    "implementation": "Implementation",
    "benchmark": "Benchmark or evaluation",
    "repository-native": "Project artifact",
    "reusable-artifact": "Reusable artifact",
    "operational-pattern": "Operational pattern",
    "practitioner-analysis": "Practitioner analysis",
    "risk-analysis": "Risk analysis",
    "curated-index": "Discovery index",
    "curated-source": "Background source",
}

EVIDENCE_NOTES = {
    "research-paper": "Published or accepted research record",
    "research-preprint": "Preprint; inspect methods and evaluation",
    "official-documentation": "Primary product or standard behavior",
    "technical-documentation": "Technical reference from the source",
    "source-implementation": "Inspectable source and runtime behavior",
    "implementation": "Working implementation or runtime",
    "benchmark": "Repeatable tasks, scores, or evaluation data",
    "repository-native": "Schema, example, guide, or repository documentation",
    "reusable-artifact": "Adaptable template, schema, or guide",
    "operational-pattern": "Transferable operating practice",
    "practitioner-analysis": "Experience-backed implementation context",
    "risk-analysis": "Failure modes, limits, or adoption cautions",
    "curated-index": "Broader ecosystem coverage for finding related work",
    "curated-source": "Background context for comparison",
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
        if resource_type == "Paper" and row["authors"]:
            details.append(author_summary(row["authors"]))
        else:
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


def evidence_cell(row: dict[str, str]) -> str:
    evidence = row["evidence_class"]
    label = EVIDENCE_LABELS.get(evidence, evidence.replace("-", " ").title())
    note = EVIDENCE_NOTES.get(evidence, "Inspect the linked source")
    if row["source_status"] == "restricted":
        note = "The linked source required access at the latest check"
    elif row["source_status"] not in {"ok", "local_ok"}:
        note = "The linked source was unavailable at the latest check"
    return f"**{escape_cell(label)}**<br><sub>{escape_cell(note)}</sub>"


def resource_cells(row: dict[str, str]) -> tuple[str, str, str, str]:
    title = escape_cell(row["title"])
    url = escape_cell(row["url"])
    annotation = escape_cell(row["annotation"])
    marker = escape_cell(row["marker"])
    resource_type = escape_cell(row["resource_type"])
    subtype = resource_type
    if row.get("section") == "Model-Level Recurrence":
        subtype = f"{resource_type} · Model layer · Adjacent foundation"
    resource = f"{marker} **[{title}]({url})**<br><sub>{escape_cell(subtype)}</sub>"
    return resource, publication_cell(row), annotation, evidence_cell(row)


def markdown_table(headers: tuple[str, ...], data: list[tuple[str, ...]]) -> list[str]:
    # Aligned padding added over 200 KB and caused GitHub to truncate the README.
    def format_row(row: tuple[str, ...]) -> str:
        return "| " + " | ".join(row) + " |"

    separator = tuple("---" for _ in headers)
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
    valid_lengths = {len(headers) for headers in LEGACY_TABLE_HEADERS}
    return len(cells) in valid_lengths and all(
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
    rendered_bytes = len(rendered.encode("utf-8"))
    if rendered_bytes > README_RENDER_BUDGET_BYTES:
        print(
            f"README is {rendered_bytes:,} bytes; keep it below the "
            f"{README_RENDER_BUDGET_BYTES:,}-byte GitHub render budget",
            file=sys.stderr,
        )
        return 1

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
