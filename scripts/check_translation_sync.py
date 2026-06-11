#!/usr/bin/env python3
"""Ensure translated READMEs declare a recent sync date with the canonical README.

Each translation must contain a marker like `<!-- last-synced: 2026-06-11 -->`.
The check fails when a marker is missing, malformed, or older than MAX_AGE_DAYS,
so translations are reviewed against the English README at least twice a year.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path


MARKER_RE = re.compile(r"<!-- last-synced: (\d{4}-\d{2}-\d{2}) -->")
MAX_AGE_DAYS = 180


def main() -> int:
    translations = sorted(Path(".").glob("README.*.md"))
    if not translations:
        print("No translated README files found", file=sys.stderr)
        return 1

    today = dt.date.today()
    failures: list[str] = []

    for translation in translations:
        match = MARKER_RE.search(translation.read_text(encoding="utf-8"))
        if not match:
            failures.append(f"{translation}: missing '<!-- last-synced: YYYY-MM-DD -->' marker")
            continue

        try:
            synced = dt.date.fromisoformat(match.group(1))
        except ValueError:
            failures.append(f"{translation}: invalid sync date {match.group(1)!r}")
            continue

        age_days = (today - synced).days
        if age_days < 0:
            failures.append(f"{translation}: sync date {synced} is in the future")
        elif age_days > MAX_AGE_DAYS:
            failures.append(
                f"{translation}: last synced {age_days} days ago (max {MAX_AGE_DAYS}); "
                "review it against README.md and bump the marker"
            )

    if failures:
        print("Translation sync check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
