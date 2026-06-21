#!/usr/bin/env python3
"""Export README resource entries as tabular dataset files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CSV_PATH = ROOT / "data" / "resources.csv"
JSONL_PATH = ROOT / "data" / "resources.jsonl"
SOURCE_URL = "https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/README.md"

ENTRY_RE = re.compile(
    r"^- (?P<marker>\S+) \*\*(?P<resource_type>[^*]+)\*\* "
    r"\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\) - (?P<annotation>.+)$"
)
HEADING_RE = re.compile(r"^(?P<level>#{2,3}) (?P<title>.+)$")
NON_SLUG_RE = re.compile(r"[^a-z0-9]+")

FIELDS = [
    "row_id",
    "section",
    "section_slug",
    "resource_type",
    "marker",
    "title",
    "url",
    "url_kind",
    "domain",
    "annotation",
    "source_readme",
    "source_line",
    "source_url",
]


def slugify(value: str) -> str:
    slug = NON_SLUG_RE.sub("-", value.lower()).strip("-")
    return slug or "section"


def clean(value: str) -> str:
    return " ".join(value.strip().split())


def classify_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return "external", parsed.netloc.lower()
    if url.startswith("#"):
        return "local_anchor", ""
    return "local_path", ""


def iter_rows(readme_path: Path = README) -> list[dict[str, str]]:
    section = ""
    section_slug = ""
    rows: list[dict[str, str]] = []

    for line_number, raw_line in enumerate(readme_path.read_text(encoding="utf-8").splitlines(), 1):
        heading = HEADING_RE.match(raw_line)
        if heading:
            section = clean(heading.group("title"))
            section_slug = slugify(section)
            continue

        match = ENTRY_RE.match(raw_line)
        if not match:
            continue

        url = clean(match.group("url"))
        if "example.com" in url:
            continue

        url_kind, domain = classify_url(url)
        row_number = len(rows) + 1
        rows.append(
            {
                "row_id": f"ale-{row_number:04d}",
                "section": section,
                "section_slug": section_slug,
                "resource_type": clean(match.group("resource_type")),
                "marker": clean(match.group("marker")),
                "title": clean(match.group("title")),
                "url": url,
                "url_kind": url_kind,
                "domain": domain,
                "annotation": clean(match.group("annotation")),
                "source_readme": "README.md",
                "source_line": str(line_number),
                "source_url": f"{SOURCE_URL}#L{line_number}",
            }
        )

    if not rows:
        raise RuntimeError(f"No resource entries found in {readme_path}")

    return rows


def write_outputs(rows: list[dict[str, str]], csv_path: Path, jsonl_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=False))
            handle.write("\n")


def check_outputs(rows: list[dict[str, str]]) -> int:
    with TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        expected_csv = temp / "resources.csv"
        expected_jsonl = temp / "resources.jsonl"
        write_outputs(rows, expected_csv, expected_jsonl)

        failures = []
        for expected, actual in [(expected_csv, CSV_PATH), (expected_jsonl, JSONL_PATH)]:
            if not actual.exists():
                failures.append(f"{actual.relative_to(ROOT)} is missing")
                continue
            if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
                failures.append(f"{actual.relative_to(ROOT)} is stale; run scripts/export_resource_dataset.py")

        if failures:
            for failure in failures:
                print(failure, file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated dataset files are stale")
    args = parser.parse_args()

    rows = iter_rows()
    if args.check:
        return check_outputs(rows)

    write_outputs(rows, CSV_PATH, JSONL_PATH)
    print(f"Wrote {len(rows)} rows to {CSV_PATH.relative_to(ROOT)} and {JSONL_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
