#!/usr/bin/env python3
"""Reject self-evaluative marketing phrases on reader-facing surfaces."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "DEFINITION.md",
    ROOT / "CITATION.cff",
    ROOT / "CITATION.bib",
    ROOT / "TRANSLATIONS.md",
    ROOT / "data" / "README.md",
    ROOT / "docs" / "index.html",
    ROOT / "docs" / "llms.txt",
    ROOT / "meta" / "DISTRIBUTION.md",
    ROOT / "meta" / "CURATION.md",
    ROOT / "meta" / "OUTREACH.md",
    ROOT / "meta" / "hf_card_body.md",
    ROOT / "meta" / "social-preview.html",
    ROOT / "posts" / "launch.md",
    ROOT / "posts" / "launch.zh-CN.md",
    ROOT / ".github" / "pull_request_template.md",
}
PUBLIC_FILES.update(ROOT.glob("README.*.md"))
PUBLIC_FILES.update((ROOT / "docs").glob("x-v*.html"))

BANNED_PHRASES = {
    "source-audited": re.compile(r"source[ -]audited", re.IGNORECASE),
    "audited resources": re.compile(r"audited (?:resources|works)", re.IGNORECASE),
    "canonical source": re.compile(r"canonical source", re.IGNORECASE),
    "canonical README": re.compile(r"canonical README", re.IGNORECASE),
    "curated marketing claim": re.compile(
        r"curated (?:field guide|map|resources|order|lists)", re.IGNORECASE
    ),
    "process-first heading": re.compile(
        r"(?:maintainer picks|trust and provenance|audit snapshot)", re.IGNORECASE
    ),
}


def main() -> int:
    failures: list[str] = []
    for path in sorted(PUBLIC_FILES):
        if not path.exists():
            failures.append(f"missing public surface: {path.relative_to(ROOT)}")
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for label, pattern in BANNED_PHRASES.items():
                if pattern.search(line):
                    failures.append(
                        f"{path.relative_to(ROOT)}:{line_number}: {label}: {line.strip()}"
                    )

    if failures:
        print("Reader-facing copy uses process-first language:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Reader-facing copy check passed across {len(PUBLIC_FILES)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
