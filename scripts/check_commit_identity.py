#!/usr/bin/env python3
"""Guard `main` against non-owner commit identities and co-author trailers."""

from __future__ import annotations

import subprocess
import sys


OWNER_NAME = "ChaoYue0307"
OWNER_EMAIL = "hechaoyue0307@gmail.com"


def commit_records() -> list[tuple[str, str, str, str, str, str]]:
    record_format = "%H%x00%an%x00%ae%x00%cn%x00%ce%x00%B%x00"
    raw = subprocess.check_output(["git", "log", "-z", f"--format={record_format}"])
    records: list[tuple[str, str, str, str, str, str]] = []
    for raw_record in raw.split(b"\x00\x00"):
        if not raw_record:
            continue
        fields = raw_record.decode("utf-8").split("\x00", 5)
        if len(fields) != 6:
            raise ValueError("could not parse a commit identity record")
        records.append((fields[0], fields[1], fields[2], fields[3], fields[4], fields[5]))
    return records


def main() -> int:
    try:
        commits = commit_records()
    except (subprocess.CalledProcessError, UnicodeDecodeError, ValueError) as error:
        print(f"Could not inspect git history: {error}", file=sys.stderr)
        return 1

    failures: list[str] = []
    for commit, author_name, author_email, committer_name, committer_email, message in commits:
        if (author_name, author_email) != (OWNER_NAME, OWNER_EMAIL):
            failures.append(f"{commit}: unexpected author {author_name} <{author_email}>")
        if (committer_name, committer_email) != (OWNER_NAME, OWNER_EMAIL):
            failures.append(f"{commit}: unexpected committer {committer_name} <{committer_email}>")
        if any(line.lower().startswith("co-authored-by:") for line in message.splitlines()):
            failures.append(f"{commit}: contains a co-author trailer")

    if failures:
        print("Commit identity check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
