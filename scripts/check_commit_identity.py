#!/usr/bin/env python3
"""Guard `main` against non-owner commit identities and co-author trailers."""

from __future__ import annotations

import subprocess
import sys


OWNER_NAME = "ChaoYue0307"
OWNER_EMAIL = "hechaoyue0307@gmail.com"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def main() -> int:
    try:
        commits = git("rev-list", "HEAD").splitlines()
    except subprocess.CalledProcessError as error:
        print(f"Could not inspect git history: {error}", file=sys.stderr)
        return 1

    failures: list[str] = []
    for commit in commits:
        author_name = git("show", "-s", "--format=%an", commit)
        author_email = git("show", "-s", "--format=%ae", commit)
        committer_name = git("show", "-s", "--format=%cn", commit)
        committer_email = git("show", "-s", "--format=%ce", commit)
        message = git("show", "-s", "--format=%B", commit)

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
