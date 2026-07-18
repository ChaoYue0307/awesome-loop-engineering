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
ARXIV_PUBLICATIONS = ROOT / "data" / "arxiv_publication_audit.csv"
YEAR_RE = re.compile(r"^(19|20)\d{2}$")
PROJECT_GITHUB_REPO = "chaoyue0307/awesome-loop-engineering"
PROJECT_PUBLICATION_SURFACES = {"GitHub", "GitHub Releases", "GitHub Discussions"}
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
    "github_repo",
    "url_kind",
    "canonical_url",
    "evidence_class",
}


def main() -> int:
    with RESOURCES.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            print(f"Missing publication columns: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1
        rows = list(reader)

    if not ARXIV_PUBLICATIONS.exists():
        print("Missing data/arxiv_publication_audit.csv", file=sys.stderr)
        return 1
    with ARXIV_PUBLICATIONS.open(encoding="utf-8", newline="") as handle:
        publication_rows = list(csv.DictReader(handle))
    publications = {row["arxiv_id"]: row for row in publication_rows}

    failures: list[str] = []
    maximum_year = datetime.now(timezone.utc).year + 1
    for row in rows:
        row_id = row["row_id"]
        year = row["publication_year"]
        date = row["publication_date"]

        if not row["publisher"]:
            failures.append(f"{row_id}: publisher/source platform is missing")
        if row["publisher"].strip().lower() == "awesome loop engineering":
            failures.append(f"{row_id}: project name is exposed as a publisher")
        if row["url_kind"] != "external" and (
            row["publication_venue"] != "GitHub" or row["publisher"] != "GitHub"
        ):
            failures.append(f"{row_id}: repository-native artifact must use GitHub as its publishing platform")
        if row["github_repo"].lower() == PROJECT_GITHUB_REPO and (
            row["publication_venue"] not in PROJECT_PUBLICATION_SURFACES or row["publisher"] != "GitHub"
        ):
            failures.append(f"{row_id}: project surface must identify GitHub, not the repository name, as its venue")
        if PROJECT_GITHUB_REPO in row["publication_venue"].lower():
            failures.append(f"{row_id}: project repository slug is exposed as a publication venue")
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
            decision = publications.get(row["arxiv_id"])
            if not decision:
                failures.append(f"{row_id}: arXiv publication decision is missing")
                continue
            if not row["authors"]:
                failures.append(f"{row_id}: arXiv authors are missing")
            if not date:
                failures.append(f"{row_id}: arXiv publication date is missing")
            if decision["status"] == "preprint-only":
                if row["publisher"] != "arXiv":
                    failures.append(f"{row_id}: preprint-only row has publisher {row['publisher']!r}")
                if row["metadata_source"] not in {"arxiv-api", "arxiv-html-meta"}:
                    failures.append(f"{row_id}: preprint metadata is not backed by a primary arXiv source")
                expected_evidence = "benchmark" if row["resource_type"] == "Benchmark" else "research-preprint"
                if row["evidence_class"] != expected_evidence:
                    failures.append(f"{row_id}: preprint-only row has evidence class {row['evidence_class']!r}")
            else:
                expected = {
                    "publication_date": decision["publication_date"],
                    "publication_year": decision["publication_year"],
                    "publication_venue": decision["publication_venue"],
                    "publisher": decision["publisher"],
                    "doi": decision["doi"],
                    "canonical_url": decision["published_url"],
                    "metadata_source": decision["metadata_source"],
                }
                for field, expected_value in expected.items():
                    if row[field] != expected_value:
                        failures.append(
                            f"{row_id}: {field} differs from the verified publication record "
                            f"({row[field]!r} != {expected_value!r})"
                        )
                if row["publisher"] == "arXiv":
                    failures.append(f"{row_id}: resolved publication still uses arXiv as publisher")
                expected_evidence = "benchmark" if row["resource_type"] == "Benchmark" else "research-paper"
                if row["evidence_class"] != expected_evidence:
                    failures.append(f"{row_id}: resolved publication has evidence class {row['evidence_class']!r}")
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

    resource_arxiv_ids = {row["arxiv_id"] for row in rows if row["arxiv_id"]}
    if resource_arxiv_ids != set(publications):
        print("Publication metadata check failed:", file=sys.stderr)
        print("- arXiv decision IDs do not match exported resource IDs", file=sys.stderr)
        return 1

    resolved = sum(row["status"] in {"accepted", "published"} for row in publication_rows)
    print(f"Validated publication metadata for {len(rows)} resources ({resolved} arXiv venue upgrades).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
