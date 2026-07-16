#!/usr/bin/env python3
"""Validate bibliographic metadata in the generated resource dataset."""

from __future__ import annotations

import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "data" / "resources.csv"
YEAR_RE = re.compile(r"^(19|20)\d{2}$")
REQUIRED_COLUMNS = {
    "authors",
    "publication_date",
    "publication_year",
    "publication_venue",
    "publisher",
    "doi",
    "publication_note",
    "primary_category",
    "metadata_source",
}


def main() -> int:
    with RESOURCES.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            print(f"Missing publication columns: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1
        rows = list(reader)

    failures: list[str] = []
    maximum_year = datetime.now(timezone.utc).year + 1
    for row in rows:
        row_id = row["row_id"]
        year = row["publication_year"]
        date = row["publication_date"]

        if not row["publisher"]:
            failures.append(f"{row_id}: publisher/source platform is missing")
        if not row["metadata_source"]:
            failures.append(f"{row_id}: metadata provenance is missing")
        if year:
            if not YEAR_RE.fullmatch(year) or not 1900 <= int(year) <= maximum_year:
                failures.append(f"{row_id}: invalid publication year {year!r}")
            if date and not date.startswith(year):
                failures.append(f"{row_id}: publication date {date!r} disagrees with year {year!r}")
        if row["resource_type"] == "Paper":
            if not row["authors"]:
                failures.append(f"{row_id}: paper authors are missing")
            if not year:
                failures.append(f"{row_id}: paper publication year is missing")
        if row["arxiv_id"]:
            if row["publisher"] != "arXiv":
                failures.append(f"{row_id}: arXiv row has publisher {row['publisher']!r}")
            if not row["authors"]:
                failures.append(f"{row_id}: arXiv authors are missing")
            if not date:
                failures.append(f"{row_id}: arXiv publication date is missing")
            if row["metadata_source"] != "arxiv-api":
                failures.append(f"{row_id}: arXiv metadata is not API-backed")
        doi = row["doi"].lower()
        if doi.startswith(("http://", "https://", "doi:")):
            failures.append(f"{row_id}: DOI is not normalized")

    if failures:
        print("Publication metadata check failed:", file=sys.stderr)
        for failure in failures[:50]:
            print(f"- {failure}", file=sys.stderr)
        if len(failures) > 50:
            print(f"- ... and {len(failures) - 50} more", file=sys.stderr)
        return 1

    print(f"Validated publication metadata for {len(rows)} resources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
