#!/usr/bin/env python3
"""Fetch GitHub stargazer timestamps and build branded star-history charts."""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPOSITORY = "ChaoYue0307/awesome-loop-engineering"
DATA_PATH = ROOT / "data" / "star-history.json"
OUTPUT_PATHS = {
    "light": (
        ROOT / "assets" / "star-history.svg",
        ROOT / "docs" / "assets" / "star-history.svg",
    ),
    "dark": (
        ROOT / "assets" / "star-history-dark.svg",
        ROOT / "docs" / "assets" / "star-history-dark.svg",
    ),
    "light-mobile": (
        ROOT / "assets" / "star-history-mobile.svg",
        ROOT / "docs" / "assets" / "star-history-mobile.svg",
    ),
    "dark-mobile": (
        ROOT / "assets" / "star-history-mobile-dark.svg",
        ROOT / "docs" / "assets" / "star-history-mobile-dark.svg",
    ),
}


@dataclass(frozen=True)
class Theme:
    background: str
    border: str
    grid: str
    text: str
    muted: str
    line: str
    area: str
    point: str
    badge: str
    brand: str
    shadow: str


THEMES = {
    "light": Theme(
        background="#FFFDFC",
        border="#DCE2ED",
        grid="#D9E0EB",
        text="#172033",
        muted="#647089",
        line="#F25F5C",
        area="#FDE3E1",
        point="#F5BE3D",
        badge="#FFFFFF",
        brand="#2457D6",
        shadow="#E9EDF5",
    ),
    "dark": Theme(
        background="#111827",
        border="#344158",
        grid="#354158",
        text="#F8FAFC",
        muted="#AAB6CA",
        line="#FF8582",
        area="#572F38",
        point="#FFD166",
        badge="#172033",
        brand="#73A7FF",
        shadow="#0B1220",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPOSITORY),
        help="GitHub repository in owner/name form.",
    )
    parser.add_argument(
        "--gh-cli",
        action="store_true",
        help="Fetch through the authenticated GitHub CLI instead of Python's REST client.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify committed charts against committed timestamp data without network access.",
    )
    parser.add_argument(
        "--from-data",
        action="store_true",
        help="Regenerate charts from committed timestamp data without network access.",
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Append the public repository star count when it differs from the latest observation.",
    )
    return parser.parse_args()


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_timestamps(values: list[str]) -> list[str]:
    return [format_timestamp(value) for value in sorted(parse_timestamp(item) for item in values)]


def fetch_with_gh(repository: str) -> list[str]:
    command = [
        "gh",
        "api",
        "--paginate",
        "-H",
        "Accept: application/vnd.github.star+json",
        f"repos/{repository}/stargazers",
        "--jq",
        ".[].starred_at",
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return normalize_timestamps([line for line in result.stdout.splitlines() if line.strip()])


def fetch_with_api(repository: str, token: str) -> list[str]:
    timestamps: list[str] = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repository}/stargazers?per_page=100&page={page}"
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github.star+json",
                "Authorization": f"Bearer {token}",
                "User-Agent": "awesome-loop-engineering-star-history",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                items = json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API returned {error.code}: {detail}") from error

        if not isinstance(items, list):
            raise RuntimeError("GitHub stargazer response was not a list")
        timestamps.extend(str(item["starred_at"]) for item in items if item.get("starred_at"))
        if len(items) < 100:
            break
        page += 1

    return normalize_timestamps(timestamps)


def fetch_repository_star_count(repository: str, token: Optional[str]) -> int:
    url = f"https://api.github.com/repos/{repository}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-loop-engineering-star-history",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub repository API returned {error.code}: {detail}") from error

    count = payload.get("stargazers_count") if isinstance(payload, dict) else None
    if not isinstance(count, int) or count < 0:
        raise RuntimeError("GitHub repository response did not include a valid stargazers_count")
    return count


def fetch_repository_star_count_with_gh(repository: str) -> int:
    command = ["gh", "api", f"repos/{repository}", "--jq", ".stargazers_count"]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    try:
        count = int(result.stdout.strip())
    except ValueError as error:
        raise RuntimeError("GitHub CLI did not return a valid stargazers_count") from error
    if count < 0:
        raise RuntimeError("GitHub CLI returned a negative stargazers_count")
    return count


def normalize_snapshots(values: list[object], after: Optional[datetime] = None) -> list[dict[str, object]]:
    snapshots: list[dict[str, object]] = []
    for value in values:
        if not isinstance(value, dict):
            raise ValueError("Star-count snapshots must be objects")
        observed_at = parse_timestamp(str(value.get("observed_at", "")))
        stars = value.get("stars")
        if not isinstance(stars, int) or stars < 0:
            raise ValueError("Star-count snapshots require a non-negative integer stars value")
        if after is not None and observed_at <= after:
            continue
        snapshots.append({"observed_at": format_timestamp(observed_at), "stars": stars})
    return sorted(snapshots, key=lambda item: str(item["observed_at"]))


def canonical_payload(payload: dict[str, object]) -> dict[str, object]:
    repository = str(payload.get("repository", DEFAULT_REPOSITORY))
    normalized = normalize_timestamps([str(value) for value in payload.get("starred_at", [])])
    latest_exact = parse_timestamp(normalized[-1]) if normalized else None
    snapshots = normalize_snapshots(list(payload.get("count_snapshots", [])), after=latest_exact)
    latest_total = int(snapshots[-1]["stars"]) if snapshots else len(normalized)
    latest_observed = str(snapshots[-1]["observed_at"]) if snapshots else (normalized[-1] if normalized else None)
    return {
        "repository": repository,
        "source": "GitHub stargazer timestamps followed by repository star-count snapshots",
        "total_stars": latest_total,
        "first_starred_at": normalized[0] if normalized else None,
        "latest_starred_at": normalized[-1] if normalized else None,
        "latest_observed_at": latest_observed,
        "starred_at": normalized,
        "count_snapshots": snapshots,
    }


def source_payload(repository: str, timestamps: list[str]) -> dict[str, object]:
    return canonical_payload(
        {
            "repository": repository,
            "starred_at": timestamps,
            "count_snapshots": [],
        }
    )


def snapshot_payload(payload: dict[str, object], stars: int, observed_at: datetime) -> dict[str, object]:
    canonical = canonical_payload(payload)
    if stars == canonical["total_stars"]:
        return canonical
    snapshots = list(canonical["count_snapshots"])
    snapshots.append({"observed_at": format_timestamp(observed_at), "stars": stars})
    canonical["count_snapshots"] = snapshots
    return canonical_payload(canonical)


def history_points(payload: dict[str, object]) -> list[tuple[datetime, int]]:
    canonical = canonical_payload(payload)
    points = [
        (parse_timestamp(str(value)), count)
        for count, value in enumerate(canonical["starred_at"], start=1)
    ]
    points.extend(
        (parse_timestamp(str(item["observed_at"])), int(item["stars"]))
        for item in canonical["count_snapshots"]
    )
    return sorted(points, key=lambda point: point[0])


def serialize_payload(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def nice_step(value: int) -> int:
    if value <= 4:
        return 1
    rough = value / 4
    magnitude = 10 ** math.floor(math.log10(rough))
    normalized = rough / magnitude
    for candidate in (1, 2, 5, 10):
        if normalized <= candidate:
            return max(1, int(candidate * magnitude))
    return max(1, int(10 * magnitude))


def date_label(value: datetime, include_year: bool = False) -> str:
    label = f"{value.strftime('%b')} {value.day}"
    return f"{label}, {value.year}" if include_year else label


def fmt(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def star_path(cx: float, cy: float, outer: float, inner: float) -> str:
    points: list[str] = []
    for index in range(10):
        radius = outer if index % 2 == 0 else inner
        angle = -math.pi / 2 + index * math.pi / 5
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        command = "M" if index == 0 else "L"
        points.append(f"{command} {fmt(x)} {fmt(y)}")
    return " ".join(points) + " Z"


def chart_svg(repository: str, payload: dict[str, object], theme_name: str, compact: bool = False) -> bytes:
    points = history_points(payload)
    if not points:
        raise ValueError("At least one star-history observation is required")

    theme = THEMES[theme_name]
    total = points[-1][1]
    peak = max(point[1] for point in points)
    first = points[0][0]
    latest = points[-1][0]
    start = first.replace(hour=0, minute=0, second=0, microsecond=0)
    end = latest.replace(hour=23, minute=59, second=59, microsecond=0)
    end = max(end, start + timedelta(days=1))
    duration = (end - start).total_seconds()
    history_days = (latest.date() - first.date()).days + 1

    if compact:
        width, height = 720, 680
        frame_x, frame_y, frame_width, frame_height = 16, 16, 688, 648
        header_x = 48
        eyebrow_y, title_y = 62, 108
        subtitle_y, subtitle_gap = 143, 27
        eyebrow_size, title_size, subtitle_size = 17, 40, 20
        meta_y = 211
        plot_left, plot_right, plot_top, plot_bottom = 74, 670, 252, 535
        y_label_x, x_label_y = 58, 570
        axis_font, line_width = 17, 5
        callout_width, callout_height, callout_font = 142, 40, 18
        footer_line_y, footer_text_y, footer_range_y = 603, 630, 653
        footer_left, footer_right, footer_font = 48, 672, 16
        x_tick_count = 3
    else:
        width, height = 1200, 560
        frame_x, frame_y, frame_width, frame_height = 24, 24, 1152, 512
        header_x = 78
        eyebrow_y, title_y = 72, 113
        subtitle_y, subtitle_gap = 143, 0
        eyebrow_size, title_size, subtitle_size = 14, 34, 16
        meta_y = 91
        plot_left, plot_right, plot_top, plot_bottom = 102, 1122, 184, 442
        y_label_x, x_label_y = 82, 474
        axis_font, line_width = 13, 4
        callout_width, callout_height, callout_font = 118, 34, 14
        footer_line_y, footer_text_y, footer_range_y = 500, 525, 525
        footer_left, footer_right, footer_font = 78, 1122, 13
        x_tick_count = 5

    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    y_step = nice_step(peak)
    y_max = max(y_step, math.ceil(peak / y_step) * y_step)

    def x_position(value: datetime) -> float:
        ratio = (value - start).total_seconds() / duration
        return plot_left + ratio * plot_width

    def y_position(count: int) -> float:
        return plot_bottom - (count / y_max) * plot_height

    release_x = x_position(latest)
    endpoint_y = y_position(total)
    path_parts = [f"M {fmt(plot_left)} {fmt(y_position(0))}"]
    event_points: list[tuple[float, float, int]] = []
    for event, count in points:
        x = x_position(event)
        y = y_position(count)
        path_parts.append(f"L {fmt(x)} {fmt(y)}")
        event_points.append((x, y, count))
    path_parts.append(f"L {fmt(plot_right)} {fmt(endpoint_y)}")
    line_path = " ".join(path_parts)
    area_path = f"{line_path} V {plot_bottom} H {plot_left} Z"

    y_ticks = list(range(0, y_max + 1, y_step))
    x_ticks = [start + (end - start) * (index / (x_tick_count - 1)) for index in range(x_tick_count)]
    if endpoint_y - callout_height - 12 >= plot_top:
        callout_y = endpoint_y - callout_height - 12
    else:
        callout_y = endpoint_y + 14
    milestone_points = [
        point for point in event_points
        if point[2] == 1 or point[2] % 10 == 0 or point[2] == total
    ]

    title = f"GitHub star growth for {repository}"
    description = (
        f"GitHub star history from {date_label(first, True)} to "
        f"{date_label(latest, True)}, ending at {total} stars."
    )
    rows: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"  <title id=\"title\">{escape(title)}</title>",
        f"  <desc id=\"desc\">{escape(description)}</desc>",
        "  <style>",
        "    text { font-family: ui-rounded, 'SF Pro Rounded', 'Nunito Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; letter-spacing: 0; }",
        "  </style>",
        "  <defs>",
        "    <filter id=\"rough-line\" x=\"-3%\" y=\"-6%\" width=\"106%\" height=\"112%\">",
        "      <feTurbulence type=\"fractalNoise\" baseFrequency=\"0.008 0.12\" numOctaves=\"1\" seed=\"17\" result=\"noise\"/>",
        "      <feDisplacementMap in=\"SourceGraphic\" in2=\"noise\" scale=\"1.2\" xChannelSelector=\"R\" yChannelSelector=\"G\"/>",
        "    </filter>",
        f'    <clipPath id="plot-clip"><rect x="{plot_left - 3}" y="{plot_top - 5}" width="{plot_width + 6}" height="{plot_height + 10}"/></clipPath>',
        "  </defs>",
        f'  <rect x="{frame_x + 5}" y="{frame_y + 7}" width="{frame_width}" height="{frame_height}" rx="8" fill="{theme.shadow}" opacity="0.58"/>',
        f'  <rect x="{frame_x}" y="{frame_y}" width="{frame_width}" height="{frame_height}" rx="8" fill="{theme.background}" stroke="{theme.border}" stroke-width="2"/>',
        f'  <path d="{star_path(header_x + 7, eyebrow_y - 5, 8 if compact else 7, 3.5 if compact else 3)}" fill="{theme.point}" stroke="{theme.text}" stroke-width="1"/>',
        f'  <text x="{header_x + (24 if compact else 21)}" y="{eyebrow_y}" fill="{theme.brand}" font-size="{eyebrow_size}" font-weight="800">STAR HISTORY</text>',
        f'  <text x="{header_x}" y="{title_y}" fill="{theme.text}" font-size="{title_size}" font-weight="760">{total} stars and counting</text>',
    ]

    if compact:
        rows.extend(
            [
                f'  <text x="{header_x}" y="{subtitle_y}" fill="{theme.muted}" font-size="{subtitle_size}">Every star helps more builders discover</text>',
                f'  <text x="{header_x}" y="{subtitle_y + subtitle_gap}" fill="{theme.muted}" font-size="{subtitle_size}">loop engineering.</text>',
                f'  <text x="{header_x}" y="{meta_y}" fill="{theme.brand}" font-size="{eyebrow_size}" font-weight="700">{history_days} days of growth</text>',
                f'  <text x="{footer_right}" y="{meta_y}" fill="{theme.muted}" font-size="{eyebrow_size}" text-anchor="end">Updated {escape(date_label(latest))}</text>',
            ]
        )
    else:
        rows.extend(
            [
                f'  <text x="{header_x}" y="{subtitle_y}" fill="{theme.muted}" font-size="{subtitle_size}">Every star helps more builders discover loop engineering.</text>',
                f'  <text x="{footer_right}" y="{meta_y}" fill="{theme.text}" font-size="28" font-weight="760" text-anchor="end">{history_days}</text>',
                f'  <text x="{footer_right}" y="{meta_y + 25}" fill="{theme.muted}" font-size="12" font-weight="750" text-anchor="end">DAYS OF GROWTH</text>',
            ]
        )

    for tick in y_ticks:
        y = y_position(tick)
        rows.extend(
            [
                f'  <line x1="{plot_left}" y1="{fmt(y)}" x2="{plot_right}" y2="{fmt(y)}" stroke="{theme.grid}" stroke-width="1" stroke-dasharray="3 9" stroke-linecap="round"/>',
                f'  <text x="{y_label_x}" y="{fmt(y + axis_font * 0.38)}" fill="{theme.muted}" font-size="{axis_font}" text-anchor="end">{tick}</text>',
            ]
        )

    for index, tick in enumerate(x_ticks):
        x = x_position(tick)
        anchor = "start" if index == 0 else "end" if index == x_tick_count - 1 else "middle"
        rows.append(
            f'  <text x="{fmt(x)}" y="{x_label_y}" fill="{theme.muted}" font-size="{axis_font}" text-anchor="{anchor}">{escape(date_label(tick))}</text>'
        )

    rows.extend(
        [
            '  <g clip-path="url(#plot-clip)">',
            f'    <path d="{area_path}" fill="{theme.area}" opacity="0.6"/>',
            f'    <path d="{line_path}" fill="none" stroke="{theme.line}" stroke-width="{line_width + 3}" stroke-linejoin="round" stroke-linecap="round" opacity="0.13" transform="translate(0 2)"/>',
            f'    <path d="{line_path}" fill="none" stroke="{theme.line}" stroke-width="{line_width}" stroke-linejoin="round" stroke-linecap="round" filter="url(#rough-line)"/>',
            "  </g>",
        ]
    )

    for x, y, count in milestone_points:
        outer = (12 if compact else 10) if count == total else (8 if compact else 6)
        inner = outer * 0.46
        rows.append(
            f'  <path d="{star_path(x, y, outer, inner)}" fill="{theme.point}" stroke="{theme.text}" stroke-width="{1.6 if count == total else 1}" stroke-linejoin="round"/>'
        )

    callout_gap = 28 if compact else 24
    callout_x = min(plot_right - callout_width - 16, max(plot_left + 8, release_x - callout_width - callout_gap))
    rows.extend(
        [
            f'  <path d="M {fmt(callout_x + callout_width)} {fmt(callout_y + callout_height / 2)} L {fmt(release_x - (13 if compact else 11))} {fmt(endpoint_y)}" fill="none" stroke="{theme.line}" stroke-width="1.5" stroke-dasharray="3 5" stroke-linecap="round"/>',
            f'  <rect x="{fmt(callout_x)}" y="{fmt(callout_y)}" width="{callout_width}" height="{callout_height}" rx="8" fill="{theme.badge}" stroke="{theme.line}"/>',
            f'  <text x="{fmt(callout_x + callout_width / 2)}" y="{fmt(callout_y + callout_height * 0.68)}" fill="{theme.text}" font-size="{callout_font}" font-weight="700" text-anchor="middle">{total} stars</text>',
            f'  <line x1="{footer_left}" y1="{footer_line_y}" x2="{footer_right}" y2="{footer_line_y}" stroke="{theme.border}"/>',
            f'  <path d="{star_path(footer_left + 7, footer_text_y - 5, 6 if compact else 5, 2.7 if compact else 2.2)}" fill="{theme.point}" stroke="{theme.text}" stroke-width="0.8"/>',
            f'  <text x="{footer_left + 22}" y="{footer_text_y}" fill="{theme.muted}" font-size="{footer_font}">{escape(repository)}</text>',
            f'  <text x="{footer_right}" y="{footer_range_y}" fill="{theme.muted}" font-size="{footer_font}" text-anchor="end">{escape(date_label(first, True))} to {escape(date_label(latest, True))}</text>',
            "</svg>",
            "",
        ]
    )
    return "\n".join(rows).encode("utf-8")


def expected_files(payload: dict[str, object]) -> dict[Path, bytes]:
    canonical = canonical_payload(payload)
    repository = str(canonical["repository"])
    expected = {DATA_PATH: serialize_payload(canonical)}
    for variant, paths in OUTPUT_PATHS.items():
        theme_name = "dark" if variant.startswith("dark") else "light"
        svg = chart_svg(repository, canonical, theme_name, compact=variant.endswith("mobile"))
        for path in paths:
            expected[path] = svg
    return expected


def main() -> None:
    args = parse_args()
    if sum((args.check, args.from_data, args.snapshot)) > 1:
        raise SystemExit("Choose only one of --check, --from-data, or --snapshot")

    if args.check or args.from_data or args.snapshot:
        if not DATA_PATH.exists():
            raise SystemExit(f"Missing {DATA_PATH.relative_to(ROOT)}")
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    if args.snapshot:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if args.gh_cli:
            star_count = fetch_repository_star_count_with_gh(args.repo)
        else:
            star_count = fetch_repository_star_count(args.repo, token)
        payload = snapshot_payload(payload, star_count, datetime.now(timezone.utc))
    elif not (args.check or args.from_data):
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if args.gh_cli or not token:
            timestamps = fetch_with_gh(args.repo)
        else:
            timestamps = fetch_with_api(args.repo, token)
        payload = source_payload(args.repo, timestamps)

    expected = expected_files(payload)
    stale: list[Path] = []
    for path, content in expected.items():
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                stale.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != content:
            path.write_bytes(content)
            print(f"wrote {path.relative_to(ROOT)}")

    if stale:
        formatted = "\n".join(f"- {path.relative_to(ROOT)}" for path in stale)
        raise SystemExit(f"Star-history artifacts are stale; run scripts/build_star_history.py:\n{formatted}")
    if args.check:
        print(f"Star-history assets are current ({payload['total_stars']} stars).")


if __name__ == "__main__":
    main()
