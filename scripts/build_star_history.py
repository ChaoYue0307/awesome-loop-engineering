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


THEMES = {
    "light": Theme(
        background="#F7F9FC",
        border="#D7E0EC",
        grid="#DCE4EF",
        text="#121722",
        muted="#5B667A",
        line="#155EEF",
        area="#DCE8FF",
        point="#0C9B68",
        badge="#FFFFFF",
    ),
    "dark": Theme(
        background="#0B1220",
        border="#28364D",
        grid="#25334A",
        text="#F8FAFC",
        muted="#A6B4C8",
        line="#38BDF8",
        area="#163A70",
        point="#34D399",
        badge="#111C2E",
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
        help="Fetch through the authenticated GitHub CLI instead of the REST API.",
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


def source_payload(repository: str, timestamps: list[str]) -> dict[str, object]:
    normalized = normalize_timestamps(timestamps)
    return {
        "repository": repository,
        "source": "GitHub stargazers API",
        "total_stars": len(normalized),
        "first_starred_at": normalized[0] if normalized else None,
        "latest_starred_at": normalized[-1] if normalized else None,
        "starred_at": normalized,
    }


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


def chart_svg(repository: str, timestamps: list[str], theme_name: str, compact: bool = False) -> bytes:
    if not timestamps:
        raise ValueError("At least one stargazer timestamp is required")

    theme = THEMES[theme_name]
    events = [parse_timestamp(value) for value in timestamps]
    total = len(events)
    first = events[0]
    latest = events[-1]
    start = first.replace(hour=0, minute=0, second=0, microsecond=0)
    end = latest.replace(hour=23, minute=59, second=59, microsecond=0)
    end = max(end, start + timedelta(days=1))
    duration = (end - start).total_seconds()
    history_days = (latest.date() - first.date()).days + 1

    if compact:
        width, height = 720, 680
        frame_x, frame_y, frame_width, frame_height = 16, 16, 688, 648
        header_x = 48
        eyebrow_y, title_y, subtitle_y = 58, 104, 138
        eyebrow_size, title_size, subtitle_size = 17, 42, 21
        metric_a_x, metric_b_x, metric_value_y, metric_label_y = 330, 672, 194, 220
        divider_x, divider_top, divider_bottom = 360, 166, 226
        plot_left, plot_right, plot_top, plot_bottom = 72, 672, 258, 550
        y_label_x, x_label_y = 58, 584
        axis_font, line_width = 18, 5
        callout_width, callout_height, callout_font = 116, 38, 18
        footer_line_y, footer_dot_y, footer_text_y = 616, 640, 647
        footer_left, footer_right, footer_font = 48, 672, 17
        x_tick_count = 3
    else:
        width, height = 1200, 560
        frame_x, frame_y, frame_width, frame_height = 24, 24, 1152, 512
        header_x = 80
        eyebrow_y, title_y, subtitle_y = 76, 116, 148
        eyebrow_size, title_size, subtitle_size = 14, 34, 16
        metric_a_x, metric_b_x, metric_value_y, metric_label_y = 938, 1120, 90, 116
        divider_x, divider_top, divider_bottom = 966, 68, 126
        plot_left, plot_right, plot_top, plot_bottom = 104, 1120, 190, 454
        y_label_x, x_label_y = 84, 482
        axis_font, line_width = 13, 4
        callout_width, callout_height, callout_font = 96, 30, 14
        footer_line_y, footer_dot_y, footer_text_y = 510, 522, 527
        footer_left, footer_right, footer_font = 80, 1120, 13
        x_tick_count = 5

    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    y_step = nice_step(total)
    y_max = max(y_step, math.ceil(total / y_step) * y_step)

    def x_position(value: datetime) -> float:
        ratio = (value - start).total_seconds() / duration
        return plot_left + ratio * plot_width

    def y_position(count: int) -> float:
        return plot_bottom - (count / y_max) * plot_height

    path_parts = [f"M {fmt(plot_left)} {fmt(y_position(0))}"]
    event_points: list[tuple[float, float, int]] = []
    for count, event in enumerate(events, start=1):
        x = x_position(event)
        path_parts.append(f"H {fmt(x)} V {fmt(y_position(count))}")
        event_points.append((x, y_position(count), count))
    path_parts.append(f"H {fmt(plot_right)}")
    line_path = " ".join(path_parts)
    area_path = f"{line_path} V {plot_bottom} H {plot_left} Z"

    y_ticks = list(range(0, y_max + 1, y_step))
    x_ticks = [start + (end - start) * (index / (x_tick_count - 1)) for index in range(x_tick_count)]
    release_x = x_position(latest)
    endpoint_y = y_position(total)
    if endpoint_y - callout_height - 12 >= plot_top:
        callout_y = endpoint_y - callout_height - 12
    else:
        callout_y = endpoint_y + 12
    milestone_points = [point for point in event_points if point[2] % 5 == 0 or point[2] == total]

    title = f"GitHub star growth for {repository}"
    description = (
        f"Cumulative star history from {date_label(first, True)} to "
        f"{date_label(latest, True)}, ending at {total} stars."
    )
    rows: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"  <title id=\"title\">{escape(title)}</title>",
        f"  <desc id=\"desc\">{escape(description)}</desc>",
        "  <style>",
        "    text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; letter-spacing: 0; }",
        "  </style>",
        f'  <rect x="{frame_x}" y="{frame_y}" width="{frame_width}" height="{frame_height}" rx="8" fill="{theme.background}" stroke="{theme.border}" stroke-width="2"/>',
        f'  <text x="{header_x}" y="{eyebrow_y}" fill="{theme.line}" font-size="{eyebrow_size}" font-weight="700">COMMUNITY MOMENTUM</text>',
        f'  <text x="{header_x}" y="{title_y}" fill="{theme.text}" font-size="{title_size}" font-weight="750">Star Growth</text>',
        f'  <text x="{header_x}" y="{subtitle_y}" fill="{theme.muted}" font-size="{subtitle_size}">Cumulative GitHub stars since the first save.</text>',
        f'  <text x="{metric_a_x}" y="{metric_value_y}" fill="{theme.text}" font-size="{title_size}" font-weight="750" text-anchor="end">{history_days}</text>',
        f'  <text x="{metric_a_x}" y="{metric_label_y}" fill="{theme.muted}" font-size="{eyebrow_size - 2}" font-weight="650" text-anchor="end">DAYS OF GROWTH</text>',
        f'  <line x1="{divider_x}" y1="{divider_top}" x2="{divider_x}" y2="{divider_bottom}" stroke="{theme.border}"/>',
        f'  <text x="{metric_b_x}" y="{metric_value_y}" fill="{theme.text}" font-size="{title_size}" font-weight="750" text-anchor="end">{total}</text>',
        f'  <text x="{metric_b_x}" y="{metric_label_y}" fill="{theme.muted}" font-size="{eyebrow_size - 2}" font-weight="650" text-anchor="end">GITHUB STARS</text>',
    ]

    for tick in y_ticks:
        y = y_position(tick)
        rows.extend(
            [
                f'  <line x1="{plot_left}" y1="{fmt(y)}" x2="{plot_right}" y2="{fmt(y)}" stroke="{theme.grid}" stroke-width="1"/>',
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
            f'  <path d="{area_path}" fill="{theme.area}" opacity="0.72"/>',
            f'  <path d="{line_path}" fill="none" stroke="{theme.line}" stroke-width="{line_width}" stroke-linejoin="round" stroke-linecap="round"/>',
        ]
    )

    for x, y, count in milestone_points:
        radius = (8 if compact else 6) if count == total else (5 if compact else 3.5)
        fill = theme.point if count == total else theme.badge
        rows.append(
            f'  <circle cx="{fmt(x)}" cy="{fmt(y)}" r="{radius}" fill="{fill}" stroke="{theme.line}" stroke-width="{2 if count == total else 1.5}"/>'
        )

    callout_gap = 100 if compact else 80
    callout_x = min(plot_right - callout_width, max(plot_left, release_x - callout_width - callout_gap))
    rows.extend(
        [
            f'  <rect x="{fmt(callout_x)}" y="{fmt(callout_y)}" width="{callout_width}" height="{callout_height}" rx="8" fill="{theme.badge}" stroke="{theme.point}"/>',
            f'  <text x="{fmt(callout_x + callout_width / 2)}" y="{fmt(callout_y + callout_height * 0.68)}" fill="{theme.text}" font-size="{callout_font}" font-weight="700" text-anchor="middle">{total} stars</text>',
            f'  <line x1="{footer_left}" y1="{footer_line_y}" x2="{footer_right}" y2="{footer_line_y}" stroke="{theme.border}"/>',
            f'  <circle cx="{footer_left + 8}" cy="{footer_dot_y}" r="{5 if compact else 4}" fill="{theme.line}"/>',
            f'  <text x="{footer_left + 22}" y="{footer_text_y}" fill="{theme.muted}" font-size="{footer_font}">Cumulative stars</text>',
            f'  <text x="{footer_right}" y="{footer_text_y}" fill="{theme.muted}" font-size="{footer_font}" text-anchor="end">{escape(date_label(first, True))} to {escape(date_label(latest, True))}</text>',
            "</svg>",
            "",
        ]
    )
    return "\n".join(rows).encode("utf-8")


def expected_files(payload: dict[str, object]) -> dict[Path, bytes]:
    repository = str(payload["repository"])
    timestamps = [str(value) for value in payload["starred_at"]]
    expected = {DATA_PATH: serialize_payload(source_payload(repository, timestamps))}
    for variant, paths in OUTPUT_PATHS.items():
        theme_name = "dark" if variant.startswith("dark") else "light"
        svg = chart_svg(repository, timestamps, theme_name, compact=variant.endswith("mobile"))
        for path in paths:
            expected[path] = svg
    return expected


def main() -> None:
    args = parse_args()
    if args.check or args.from_data:
        if not DATA_PATH.exists():
            raise SystemExit(f"Missing {DATA_PATH.relative_to(ROOT)}")
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    else:
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
