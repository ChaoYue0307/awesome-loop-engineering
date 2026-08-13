#!/usr/bin/env python3
"""Build production PNG variants from the transparent ChatGPT Image logo master."""

import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "assets" / "awesome-loop-engineering-logo-master.png"
OUTPUTS = {
    "awesome-loop-engineering-logo.png": 512,
    "awesome-loop-engineering-logo-192.png": 192,
    "apple-touch-icon.png": 180,
    "favicon-32.png": 32,
}


def prepare_mark(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
    if bbox is None:
        raise ValueError(f"Logo master has no visible pixels: {MASTER}")

    cropped = rgba.crop(bbox)
    padding = round(max(cropped.size) * 0.09)
    side = max(cropped.size) + 2 * padding
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    offset = ((side - cropped.width) // 2, (side - cropped.height) // 2)
    canvas.alpha_composite(cropped, offset)
    return canvas


def encode_png(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when committed brand variants differ from the generated output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prepared = prepare_mark(Image.open(MASTER))
    destinations = (ROOT / "assets", ROOT / "docs" / "assets")
    stale: list[Path] = []

    for filename, size in OUTPUTS.items():
        output = prepared.resize((size, size), Image.Resampling.LANCZOS)
        payload = encode_png(output)
        for destination in destinations:
            destination.mkdir(parents=True, exist_ok=True)
            path = destination / filename
            if args.check:
                if not path.exists():
                    stale.append(path)
                    continue
                current = Image.open(path).convert("RGBA")
                # getbbox() defaults to alpha_only=True on RGBA, so it would compare only the
                # alpha channel and report a fully recoloured mark as current. Compare colour.
                difference = ImageChops.difference(current, output)
                if current.size != output.size or difference.getbbox(alpha_only=False):
                    stale.append(path)
                continue
            path.write_bytes(payload)
            print(f"wrote {path.relative_to(ROOT)} ({size}x{size})")

    if stale:
        formatted = "\n".join(f"- {path.relative_to(ROOT)}" for path in stale)
        raise SystemExit(f"Brand assets are stale; run scripts/build_brand_assets.py:\n{formatted}")

    if args.check:
        print(f"Brand assets are current ({len(OUTPUTS) * len(destinations)} files).")


if __name__ == "__main__":
    main()
