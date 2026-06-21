#!/usr/bin/env python3
"""Audit exported resource rows against local files and external source metadata."""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import csv
import html
import json
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urldefrag, urlparse


ROOT = Path(__file__).resolve().parents[1]
RESOURCES_CSV = ROOT / "data" / "resources.csv"
AUDIT_CSV = ROOT / "data" / "resource_source_audit.csv"

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(
    r"<meta[^>]+(?:name|property)=[\"'](?:description|og:description)[\"'][^>]+content=[\"'](.*?)[\"'][^>]*>",
    re.IGNORECASE | re.DOTALL,
)
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(?P<id>\d{4}\.\d{4,5})(?:v\d+)?")

FIELDS = [
    "row_id",
    "title",
    "url",
    "url_kind",
    "domain",
    "audit_status",
    "http_status",
    "final_url",
    "content_type",
    "source_title",
    "source_description",
    "github_repo",
    "github_stars",
    "github_forks",
    "github_open_issues",
    "github_description",
    "github_license",
    "github_updated_at",
    "arxiv_id",
    "error",
    "retrieved_at",
]

RESTRICTED_HTTP = {401, 403, 405, 406, 418, 429, 999}


def clean(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(html.unescape(value).strip().split())


def read_rows() -> list[dict[str, str]]:
    with RESOURCES_CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def github_repo_from_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc.lower() != "github.com":
        return ""
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2 or parts[0] in {"topics", "marketplace", "features"}:
        return ""
    return f"{parts[0]}/{parts[1]}"


def arxiv_id_from_url(url: str) -> str:
    match = ARXIV_RE.search(url)
    return match.group("id") if match else ""


def html_metadata(body: bytes, content_type: str) -> tuple[str, str]:
    if "html" not in content_type.lower():
        return "", ""
    text = body[:750_000].decode("utf-8", errors="ignore")
    title_match = TITLE_RE.search(text)
    desc_match = META_DESC_RE.search(text)
    return clean(title_match.group(1) if title_match else ""), clean(desc_match.group(1) if desc_match else "")


def fetch_url(url: str, timeout: float, attempts: int) -> dict[str, str]:
    context = ssl._create_unverified_context()
    last_error = ""

    for attempt in range(1, attempts + 1):
        for method in ("HEAD", "GET"):
            request = urllib.request.Request(
                url,
                method=method,
                headers={"User-Agent": "awesome-loop-engineering-source-audit"},
            )
            try:
                with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                    body = b""
                    content_type = response.headers.get("content-type", "")
                    if method == "GET":
                        body = response.read(750_000)
                    else:
                        body = b""
                    title, description = html_metadata(body, content_type)
                    return {
                        "audit_status": "ok",
                        "http_status": str(response.status),
                        "final_url": response.geturl(),
                        "content_type": content_type,
                        "source_title": title,
                        "source_description": description,
                        "error": "",
                    }
            except urllib.error.HTTPError as error:
                if method == "HEAD":
                    continue
                if error.code in RESTRICTED_HTTP:
                    return {
                        "audit_status": "restricted",
                        "http_status": str(error.code),
                        "final_url": url,
                        "content_type": error.headers.get("content-type", "") if error.headers else "",
                        "source_title": "",
                        "source_description": "",
                        "error": "restricted_or_rate_limited",
                    }
                return {
                    "audit_status": "broken",
                    "http_status": str(error.code),
                    "final_url": url,
                    "content_type": error.headers.get("content-type", "") if error.headers else "",
                    "source_title": "",
                    "source_description": "",
                    "error": f"HTTPError:{error.code}",
                }
            except Exception as error:  # noqa: BLE001 - audit output should capture exact failure class.
                last_error = error.__class__.__name__
                if method == "HEAD":
                    continue

        if attempt < attempts:
            time.sleep(min(1.5, 0.25 * attempt))

    return {
        "audit_status": "unreachable",
        "http_status": "",
        "final_url": url,
        "content_type": "",
        "source_title": "",
        "source_description": "",
        "error": last_error or "unknown",
    }


def audit_row(row: dict[str, str], retrieved_at: str, timeout: float, attempts: int) -> dict[str, str]:
    base = {
        "row_id": row["row_id"],
        "title": row["title"],
        "url": row["url"],
        "url_kind": row["url_kind"],
        "domain": row["domain"],
        "audit_status": "",
        "http_status": "",
        "final_url": "",
        "content_type": "",
        "source_title": "",
        "source_description": "",
        "github_repo": github_repo_from_url(row["url"]),
        "github_stars": "",
        "github_forks": "",
        "github_open_issues": "",
        "github_description": "",
        "github_license": "",
        "github_updated_at": "",
        "arxiv_id": arxiv_id_from_url(row["url"]),
        "error": "",
        "retrieved_at": retrieved_at,
    }

    if row["url_kind"] == "local_path":
        local_target, fragment = urldefrag(row["url"])
        path = (ROOT / local_target).resolve()
        if path.exists():
            base.update(
                {
                    "audit_status": "local_ok",
                    "final_url": str(path) + (f"#{fragment}" if fragment else ""),
                    "source_title": local_title(path),
                }
            )
        else:
            base.update({"audit_status": "local_missing", "error": "local_path_missing"})
        return base

    if row["url_kind"] == "local_anchor":
        base.update({"audit_status": "local_anchor", "final_url": row["url"]})
        return base

    base.update(fetch_url(row["url"], timeout=timeout, attempts=attempts))
    return base


def local_title(path: Path) -> str:
    if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".html", ".xml", ".txt"}:
        return ""
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return clean(stripped.removeprefix("# "))
        if stripped:
            return clean(stripped)[:160]
    return ""


def github_stats_via_gh(repo: str, timeout: float) -> dict[str, str]:
    if not repo:
        return {}
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}"],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except Exception:  # noqa: BLE001 - stats are best-effort.
        return {}
    if result.returncode != 0:
        return {}
    try:
        return github_stats_from_payload(json.loads(result.stdout))
    except json.JSONDecodeError:
        return {}


def github_stats_from_payload(data: dict[str, object]) -> dict[str, str]:
    license_data = data.get("license") or {}
    if not isinstance(license_data, dict):
        license_data = {}
    description = data.get("description") or ""
    return {
        "github_stars": str(data.get("stargazers_count", "")),
        "github_forks": str(data.get("forks_count", "")),
        "github_open_issues": str(data.get("open_issues_count", "")),
        "github_description": clean(str(description)),
        "github_license": clean(str(license_data.get("spdx_id", ""))),
        "github_updated_at": clean(str(data.get("updated_at", ""))),
    }


def github_stats(repo: str, timeout: float, use_gh_cli: bool) -> dict[str, str]:
    if not repo:
        return {}
    if use_gh_cli:
        stats = github_stats_via_gh(repo, timeout=timeout)
        if stats:
            return stats

    context = ssl._create_unverified_context()
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"User-Agent": "awesome-loop-engineering-source-audit"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception:  # noqa: BLE001 - stats are best-effort; URL audit carries primary status.
        return {}

    return github_stats_from_payload(data)


def enrich_github(rows: list[dict[str, str]], timeout: float, use_gh_cli: bool) -> None:
    repos = sorted({row["github_repo"] for row in rows if row["github_repo"]})
    stats = {repo: github_stats(repo, timeout=timeout, use_gh_cli=use_gh_cli) for repo in repos}
    for row in rows:
        row.update(stats.get(row["github_repo"], {}))


def write_audit(rows: list[dict[str, str]], out_path: Path = AUDIT_CSV) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--github-cli", action="store_true", help="use authenticated gh api calls for GitHub repo stats")
    parser.add_argument("--fail-on-broken", action="store_true")
    args = parser.parse_args()

    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows = read_rows()
    with futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        checks = [executor.submit(audit_row, row, retrieved_at, args.timeout, args.attempts) for row in rows]
        audited = [check.result() for check in futures.as_completed(checks)]

    audited.sort(key=lambda row: row["row_id"])
    enrich_github(audited, timeout=args.timeout, use_gh_cli=args.github_cli)
    write_audit(audited)

    broken = [row for row in audited if row["audit_status"] in {"broken", "unreachable", "local_missing"}]
    print(f"Wrote {len(audited)} rows to {AUDIT_CSV.relative_to(ROOT)}")
    print(f"Broken or unreachable rows: {len(broken)}")
    for row in broken[:20]:
        print(f"- {row['row_id']} {row['audit_status']} {row['url']} {row['error']}", file=sys.stderr)

    if broken and args.fail_on_broken:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
