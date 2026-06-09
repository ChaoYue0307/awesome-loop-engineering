#!/usr/bin/env python3
"""Check GitHub Pages metadata needed for search and social previews."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


LANDING_PAGE = Path("docs/index.html")
SITEMAP = Path("docs/sitemap.xml")
ROBOTS = Path("docs/robots.txt")
CANONICAL_URL = "https://chaoyue0307.github.io/awesome-loop-engineering/"
REQUIRED_HTML_SNIPPETS = [
    "<title>Awesome Loop Engineering</title>",
    'name="description"',
    f'href="{CANONICAL_URL}"',
    'property="og:title"',
    'property="og:image"',
    'name="twitter:card"',
    "application/ld+json",
]


def main() -> int:
    failures: list[str] = []

    html = LANDING_PAGE.read_text(encoding="utf-8")
    for snippet in REQUIRED_HTML_SNIPPETS:
        if snippet not in html:
            failures.append(f"{LANDING_PAGE}: missing {snippet}")

    sitemap_text = SITEMAP.read_text(encoding="utf-8")
    if CANONICAL_URL not in sitemap_text:
        failures.append(f"{SITEMAP}: missing canonical URL")
    try:
        ET.fromstring(sitemap_text)
    except ET.ParseError as error:
        failures.append(f"{SITEMAP}: invalid XML: {error}")

    robots = ROBOTS.read_text(encoding="utf-8")
    if "Allow: /" not in robots:
        failures.append(f"{ROBOTS}: missing Allow rule")
    if f"Sitemap: {CANONICAL_URL}sitemap.xml" not in robots:
        failures.append(f"{ROBOTS}: missing sitemap URL")

    if failures:
        print("Pages metadata check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
