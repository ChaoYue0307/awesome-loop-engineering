#!/usr/bin/env python3
"""Lightweight URL checker for Markdown files.

This script intentionally uses only the Python standard library so contributors
can run it without installing project dependencies.
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


URL_RE = re.compile(r'https?://[^\s)\]}>"]+')
CLAUDE_DOC_HOSTS = {"code.claude.com", "docs.anthropic.com"}


class RedirectHandler(urllib.request.HTTPRedirectHandler):
    """Follow permanent HTTP 308 redirects on Python versions that omit them."""

    def http_error_308(self, req, fp, code, msg, headers):  # type: ignore[no-untyped-def]
        return self.http_error_302(req, fp, code, msg, headers)

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        if code == 308 and req.get_method() in {"GET", "HEAD"}:
            code = 307
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def iter_urls(paths: list[Path]) -> list[str]:
    urls: set[str] = set()
    for path in paths:
        if path.is_dir():
            markdown_files = path.rglob("*.md")
        else:
            markdown_files = [path]

        for markdown_file in markdown_files:
            if ".git" in markdown_file.parts:
                continue
            text = markdown_file.read_text(encoding="utf-8")
            urls.update(match.group(0).rstrip(".,;") for match in URL_RE.finditer(text))
    return sorted(urls)


def check_url(url: str, timeout: float, attempts: int) -> tuple[bool, str]:
    context = ssl._create_unverified_context()
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=context),
        RedirectHandler(),
    )
    last_error = "unknown"
    source_host = urlparse(url).netloc.lower()

    for attempt in range(1, attempts + 1):
        for method in ("HEAD", "GET"):
            request = urllib.request.Request(
                url,
                method=method,
                headers={"User-Agent": "awesome-loop-engineering-url-checker"},
            )
            try:
                with opener.open(request, timeout=timeout) as response:
                    final_host = urlparse(response.geturl()).netloc.lower()
                    if source_host == "code.claude.com" and final_host not in CLAUDE_DOC_HOSTS:
                        return True, f"{response.status} restricted redirect"
                    return response.status < 400, f"{response.status} {method}"
            except urllib.error.HTTPError as error:
                final_host = urlparse(error.geturl()).netloc.lower()
                if source_host == "code.claude.com" and final_host not in CLAUDE_DOC_HOSTS:
                    return True, f"{error.code} restricted redirect"
                if error.code in {401, 403, 405, 406, 418, 429, 999}:
                    return True, f"{error.code} restricted"
                if method == "HEAD":
                    continue
                return False, f"{error.code} {method}"
            except Exception as error:  # noqa: BLE001 - report URL checker failures plainly.
                last_error = error.__class__.__name__
                if method == "HEAD":
                    continue

        if attempt < attempts:
            time.sleep(min(1.5, 0.25 * attempt))

    return False, last_error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, default=[Path(".")])
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--attempts", type=int, default=3)
    args = parser.parse_args()

    failures: list[tuple[str, str]] = []
    urls = iter_urls(args.paths)
    with futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        checks = {executor.submit(check_url, url, args.timeout, args.attempts): url for url in urls}
        for check in futures.as_completed(checks):
            url = checks[check]
            ok, detail = check.result()
            status = "ok" if ok else "fail"
            print(f"{status:4} {detail:14} {url}", flush=True)
            if not ok:
                failures.append((url, detail))

    if failures:
        print("\nFailed URLs:", file=sys.stderr)
        for url, detail in failures:
            print(f"- {url} ({detail})", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
