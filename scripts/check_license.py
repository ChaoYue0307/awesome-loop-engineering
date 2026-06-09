#!/usr/bin/env python3
"""Verify that LICENSE stays on the canonical CC0-1.0 text used by GitHub."""

from __future__ import annotations

import hashlib
from pathlib import Path


EXPECTED_SHA256 = "a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499"


def main() -> int:
    text = Path("LICENSE").read_text(encoding="utf-8").replace("\r\n", "\n").strip() + "\n"
    digest = hashlib.sha256(text.encode()).hexdigest()
    if digest != EXPECTED_SHA256:
        print("LICENSE does not match the expected canonical CC0-1.0 text.")
        print(f"Expected: {EXPECTED_SHA256}")
        print(f"Actual:   {digest}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
