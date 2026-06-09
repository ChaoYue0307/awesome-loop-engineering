#!/usr/bin/env python3
"""Validate local Markdown links and anchors."""

from __future__ import annotations

import re
import sys
import urllib.parse
from collections import Counter
from pathlib import Path


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SKIP_SCHEMES = {"http", "https", "mailto"}


def slugify(heading: str, seen: Counter[str]) -> str:
    text = re.sub(r"<[^>]+>", "", heading)
    text = re.sub(r"[`*_]", "", text).strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff -]", "", text)
    text = re.sub(r"\s+", "-", text)
    base = text.strip("-")
    seen[base] += 1
    if seen[base] == 1:
        return base
    return f"{base}-{seen[base] - 1}"


def anchors_for(path: Path) -> set[str]:
    seen: Counter[str] = Counter()
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if match:
            anchors.add(slugify(match.group(2), seen))
    return anchors


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)


def normalize_link(raw_link: str) -> tuple[str, str]:
    link = raw_link.split()[0].strip("<>")
    parsed = urllib.parse.urlsplit(link)
    path = urllib.parse.unquote(parsed.path)
    fragment = urllib.parse.unquote(parsed.fragment)
    return path, fragment


def main() -> int:
    root = Path(".")
    anchor_cache: dict[Path, set[str]] = {}
    failures: list[str] = []

    for source in markdown_files(root):
        text = source.read_text(encoding="utf-8")
        for raw_link in LINK_RE.findall(text):
            parsed = urllib.parse.urlsplit(raw_link.strip("<>"))
            if parsed.scheme in SKIP_SCHEMES:
                continue

            if raw_link.startswith("#"):
                target_path = source
                fragment = urllib.parse.unquote(parsed.fragment or raw_link.lstrip("#"))
            elif parsed.scheme:
                continue
            else:
                path_part, fragment = normalize_link(raw_link)
                if not path_part:
                    target_path = source
                else:
                    target_path = (source.parent / path_part).resolve().relative_to(root.resolve())

            if not target_path.exists():
                failures.append(f"{source}: missing linked file {raw_link}")
                continue

            if fragment and target_path.suffix.lower() == ".md":
                anchors = anchor_cache.setdefault(target_path, anchors_for(target_path))
                if fragment not in anchors:
                    failures.append(f"{source}: missing anchor #{fragment} in {target_path}")

    if failures:
        print("Internal link check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
