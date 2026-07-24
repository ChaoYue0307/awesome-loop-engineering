#!/usr/bin/env python3
"""Check cross-surface counts, release metadata, and generated discovery files."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

from build_hf_card import project_context, render_card


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RESOURCE_FIELDS = {
    "row_id",
    "title",
    "url",
    "canonical_url",
    "resource_type",
    "annotation",
    "key_contribution",
    "novelty",
    "impact",
    "signal",
    "signal_strength",
    "collection",
    "user_goal",
    "lifecycle_stages",
    "audience",
    "loop_layer",
    "scope_fit",
    "evidence_class",
    "evidence_tier",
    "source_status",
    "metadata_source",
    "audited_at",
}
ALLOWED_EVIDENCE_TIERS = {"A", "B", "C", "D"}
ALLOWED_SIGNAL_STRENGTHS = {"high", "medium", "contextual", "unverified"}
ALLOWED_SOURCE_STATUSES = {"ok", "local_ok", "restricted", "broken", "unreachable", "local_missing"}
ALLOWED_LOOP_LAYERS = {"model", "agent", "harness", "workflow", "operations", "evaluation", "cross-layer"}
ALLOWED_SCOPE_FITS = {"direct", "enabling", "adjacent"}


def require(path: Path, snippets: list[str], failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            failures.append(f"{path.relative_to(ROOT)}: missing {snippet!r}")


def validate_resource_rows(rows: list[dict[str, str]], failures: list[str]) -> None:
    if not rows:
        failures.append("data/resources.csv: no resource rows")
        return

    missing_columns = REQUIRED_RESOURCE_FIELDS - set(rows[0])
    if missing_columns:
        failures.append(f"data/resources.csv: missing columns {sorted(missing_columns)}")

    seen_urls: set[str] = set()
    seen_ids: set[str] = set()
    for index, row in enumerate(rows, 1):
        row_label = row.get("row_id") or f"row {index}"
        missing = sorted(field for field in REQUIRED_RESOURCE_FIELDS if not row.get(field, "").strip())
        if missing:
            failures.append(f"data/resources.csv: {row_label} missing required values {missing}")

        normalized_url = row.get("url", "").strip().lower().rstrip("/")
        if normalized_url in seen_urls:
            failures.append(f"data/resources.csv: duplicate URL at {row_label}: {row.get('url', '')}")
        seen_urls.add(normalized_url)

        row_id = row.get("row_id", "")
        if row_id in seen_ids:
            failures.append(f"data/resources.csv: duplicate row_id {row_id}")
        seen_ids.add(row_id)
        expected_id = f"ale-{index:04d}"
        if row_id != expected_id:
            failures.append(f"data/resources.csv: expected {expected_id}, found {row_id or '<blank>'}")

        if row.get("evidence_tier") not in ALLOWED_EVIDENCE_TIERS:
            failures.append(f"data/resources.csv: {row_label} has invalid evidence_tier {row.get('evidence_tier')!r}")
        if row.get("signal_strength") not in ALLOWED_SIGNAL_STRENGTHS:
            failures.append(f"data/resources.csv: {row_label} has invalid signal_strength {row.get('signal_strength')!r}")
        if row.get("source_status") not in ALLOWED_SOURCE_STATUSES:
            failures.append(f"data/resources.csv: {row_label} has invalid source_status {row.get('source_status')!r}")
        if row.get("loop_layer") not in ALLOWED_LOOP_LAYERS:
            failures.append(f"data/resources.csv: {row_label} has invalid loop_layer {row.get('loop_layer')!r}")
        if row.get("scope_fit") not in ALLOWED_SCOPE_FITS:
            failures.append(f"data/resources.csv: {row_label} has invalid scope_fit {row.get('scope_fit')!r}")

        year = row.get("publication_year", "")
        if year and not re.fullmatch(r"(?:19|20)\d{2}", year):
            failures.append(f"data/resources.csv: {row_label} has invalid publication_year {year!r}")
        if row.get("resource_type") == "Paper":
            for field in ("authors", "publication_year"):
                if not row.get(field, "").strip():
                    failures.append(f"data/resources.csv: {row_label} paper is missing {field}")
        if "arxiv.org" in row.get("url", "") and not row.get("arxiv_id", "").strip():
            failures.append(f"data/resources.csv: {row_label} arXiv work is missing arxiv_id")


def main() -> int:
    context = project_context()
    count = context["RESOURCE_COUNT"]
    version = context["VERSION"]
    source_summary = (
        f"{context['REACHABLE_COUNT']} public links opened successfully, "
        f"{context['RESTRICTED_COUNT']} required access, "
        f"{context['LOCAL_COUNT']} pointed to files in this repository"
    )
    failures: list[str] = []

    require(
        ROOT / "README.md",
        [
            f"resources-{count}-",
            f"patterns-{context['PATTERN_COUNT']}-",
            f"contracts-{context['CONTRACT_COUNT']}-",
            f"starters-{context['RUNNABLE_COUNT']}-",
            f"**{count} resources**",
            source_summary,
            f"**{context['RUNNABLE_COUNT']} runtime starters**",
            f"{context['EXECUTABLE_COUNT']} dependency-light executables plus {context['RUNTIME_TEMPLATE_COUNT']} copy/paste runtime templates",
            f"{context['LANGUAGE_COUNT']} language entry points",
        ],
        failures,
    )
    require(
        ROOT / "docs" / "index.html",
        [
            f'content="Explore {count} resources',
            f">{count}</b><span>resources</span>",
            f"Filter {count} resources",
            f"{context['REACHABLE_COUNT']} public links opened successfully, {context['RESTRICTED_COUNT']} required access",
            f'"version": "{version}"',
        ],
        failures,
    )
    require(ROOT / "meta" / "social-preview.html", [f">{count}</b>"], failures)
    distribution_text = (ROOT / "meta" / "DISTRIBUTION.md").read_text(encoding="utf-8")
    share_match = re.search(r"awesome-loop-engineering/(x-v\d+-\d+\.html)", distribution_text)
    if share_match is None:
        failures.append("meta/DISTRIBUTION.md: missing current x share-page link")
    else:
        require(
            ROOT / "docs" / share_match.group(1),
            [f"{count} resources", f"{count} papers"],
            failures,
        )
    require(
        ROOT / "posts" / "launch.md",
        [
            f"# Awesome Loop Engineering v{version}",
            f"{count} resources",
            f"{context['MODEL_COUNT']} model-layer resources",
            f"{context['FIELD_COUNT']}-field CSV",
            f"{context['LANGUAGE_COUNT']} language entry points",
        ],
        failures,
    )
    require(ROOT / "posts" / "launch.zh-CN.md", [f"# Awesome Loop Engineering v{version}", f"{count} 篇论文"], failures)
    require(ROOT / "meta" / "DISTRIBUTION.md", [f"v{version}", f"{count} resources"], failures)
    require(
        ROOT / "design-qa.md",
        [
            f"returns {context['MODEL_COUNT']} of {count} resources ({context['MODEL_PAPER_COUNT']} papers plus Awesome Loop Models)",
            f"{context['REACHABLE_COUNT']} public sources reachable, {context['RESTRICTED_COUNT']} access-restricted, {context['LOCAL_COUNT']} repository-native",
        ],
        failures,
    )
    require(ROOT / "data" / "README.md", [f"Download all {count} resources"], failures)

    for translation in sorted(ROOT.glob("README.*.md")):
        require(translation, [count], failures)

    with (ROOT / "data" / "resources.csv").open(encoding="utf-8", newline="") as handle:
        resource_rows = list(csv.DictReader(handle))
    csv_count = len(resource_rows)
    if csv_count != int(count):
        failures.append(f"data/resources.csv: expected {count} rows, found {csv_count}")
    validate_resource_rows(resource_rows, failures)

    with (ROOT / "data" / "resource_source_audit.csv").open(encoding="utf-8", newline="") as handle:
        audit_rows = list(csv.DictReader(handle))
    if len(audit_rows) != int(count):
        failures.append(f"data/resource_source_audit.csv: expected {count} rows, found {len(audit_rows)}")
    audit_statuses: dict[str, int] = {}
    for row in audit_rows:
        status = row.get("audit_status", "")
        audit_statuses[status] = audit_statuses.get(status, 0) + 1
    expected_statuses = {
        "ok": int(context["REACHABLE_COUNT"]),
        "restricted": int(context["RESTRICTED_COUNT"]),
        "local_ok": int(context["LOCAL_COUNT"]),
    }
    if audit_statuses != expected_statuses:
        failures.append(
            "data/resource_source_audit.csv: status counts do not match the generated resource exports "
            f"({audit_statuses!r} != {expected_statuses!r})"
        )

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
        f"Validated {count} resources, {context['MODEL_COUNT']} model-layer resources, "
        f"{context['PATTERN_COUNT']} patterns, {context['CONTRACT_COUNT']} contracts, "
        f"{context['RUNNABLE_COUNT']} runtime starters, and release v{version}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
