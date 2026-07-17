EXIT_FAILURE = 1EXIT_SUCCESS = 0LINE_NUMBER_OFFSET = EXIT_FAILURE#!/usr/bin/env python3
"""Ensure README resource entries carry a visible resource type label."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from export_resource_dataset import TYPE_MARKERS, parse_entry_line


RESOURCE_SECTIONS = {
    "Canonical Definition",
    "Concept Guides",
    "Maintainer Picks",
    "Start Here",
    "Core Loop Primitives",
    "Official Runtime Guides",
    "Research Foundations",
    "Agent Workflow Patterns",
    "Coding-Agent Loop Systems",
    "Verification And Feedback Gates",
    "Securing Unattended Loops",
    "State, Memory, And Context Persistence",
    "Orchestration And Multi-Agent Delegation",
    "Benchmarks And Evaluation",
    "Operations Playbooks",
    "Templates And Patterns",
    "Examples And Schema",
    "Community Gallery",
    "Pattern Library",
    "Discovery And Distribution",
    "Roadmap And Discussion",
    "Critiques, Risks, And Limitations",
    "Adjacent Awesome Lists",
}

def check_readme(path: Path) -> list[tuple[int, str]]:
    failures: list[tuple[int, str]] = []
    current_section = ""

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), LINE_NUMBER_OFFSET):
        if line.startswith("## "):
            current_section = line.removeprefix("## ").strip()
            continue

        if current_section not in RESOURCE_SECTIONS:
            continue

        if not line.startswith(("- ", "| ")):
            continue

        if "](http" not in line and "](" not in line:
            continue

        entry = parse_entry_line(line)
        if not entry or TYPE_MARKERS.get(entry["resource_type"]) != entry["marker"]:
            failures.append((line_number, line))

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("readme", type=Path, default=Path("README.md"), nargs="?")
    args = parser.parse_args()

    failures = check_readme(args.readme)
    if not failures:
        return EXIT_SUCCESS

    print("Resource entries missing type labels:", file=sys.stderr)
    for line_number, line in failures:
        print(f"- line {line_number}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
