#!/usr/bin/env python3
"""Build the Hugging Face dataset card from repository metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "meta" / "hf_card_header.yaml"
BODY = ROOT / "meta" / "hf_card_body.md"
RESOURCES = ROOT / "data" / "resources.jsonl"
CITATION = ROOT / "CITATION.cff"
REQUIRED_METADATA = (
    "license",
    "language",
    "pretty_name",
    "size_categories",
    "task_categories",
    "tags",
    "configs",
)
TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def load_rows() -> list[dict[str, str]]:
    return [json.loads(line) for line in RESOURCES.read_text(encoding="utf-8").splitlines() if line.strip()]


def project_context() -> dict[str, str]:
    rows = load_rows()
    statuses = Counter(row.get("source_status", "") for row in rows)
    audit_dates = sorted({row.get("audited_at", "")[:10] for row in rows if row.get("audited_at")})
    version_match = re.search(r"^version:\s*([^\s]+)\s*$", CITATION.read_text(encoding="utf-8"), re.MULTILINE)

    patterns = [path for path in (ROOT / "patterns").glob("*.md") if path.name not in {"README.md", "MATRIX.md"}]
    contracts = list((ROOT / "examples").glob("*-loop.json"))
    runnable = [path for path in (ROOT / "examples" / "runnable").iterdir() if path.is_file() and path.name != "README.md"]

    return {
        "RESOURCE_COUNT": str(len(rows)),
        "REACHABLE_COUNT": str(statuses["ok"]),
        "RESTRICTED_COUNT": str(statuses["restricted"]),
        "LOCAL_COUNT": str(statuses["local_ok"]),
        "BROKEN_COUNT": str(sum(statuses[key] for key in ("broken", "unreachable", "local_missing"))),
        "AUDIT_DATE": audit_dates[-1] if audit_dates else "not recorded",
        "PATTERN_COUNT": str(len(patterns)),
        "CONTRACT_COUNT": str(len(contracts)),
        "RUNNABLE_COUNT": str(len(runnable)),
        "VERSION": version_match.group(1) if version_match else "unversioned",
    }


def validate_header(header: str) -> list[str]:
    failures: list[str] = []
    lines = header.strip().splitlines()
    if len(lines) < 3 or lines[0] != "---" or lines[-1] != "---":
        failures.append("meta/hf_card_header.yaml must be wrapped in YAML front matter delimiters")
    for key in REQUIRED_METADATA:
        if not re.search(rf"^{re.escape(key)}:\s*", header, re.MULTILINE):
            failures.append(f"meta/hf_card_header.yaml is missing {key}")
    return failures


def render_card() -> tuple[str, list[str]]:
    header = HEADER.read_text(encoding="utf-8").strip()
    body = BODY.read_text(encoding="utf-8")
    context = project_context()
    failures = validate_header(header)

    rendered = TOKEN_RE.sub(lambda match: context.get(match.group(1), match.group(0)), body)
    unresolved = sorted(set(TOKEN_RE.findall(rendered)))
    if unresolved:
        failures.append("unresolved dataset-card tokens: " + ", ".join(unresolved))

    return f"{header}\n\n{rendered.lstrip()}", failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the card template without writing it")
    parser.add_argument("--output", type=Path, help="write the rendered card to this path")
    args = parser.parse_args()

    card, failures = render_card()
    if failures:
        print("Hugging Face dataset card check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    if args.check:
        return 0
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(card, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        sys.stdout.write(card)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
