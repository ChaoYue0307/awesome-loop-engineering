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
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlencode, urlparse


ROOT = Path(__file__).resolve().parents[1]
RESOURCES_CSV = ROOT / "data" / "resources.csv"
AUDIT_CSV = ROOT / "data" / "resource_source_audit.csv"
ARXIV_PUBLICATION_AUDIT = ROOT / "data" / "arxiv_publication_audit.csv"
REPO_BLOB_URL = "https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main"
PROJECT_GITHUB_REPO = "chaoyue0307/awesome-loop-engineering"

ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(?P<id>\d{4}\.\d{4,5})(?:v\d+)?")
YEAR_RE = re.compile(r"(?<!\d)(?P<year>19\d{2}|20\d{2})(?!\d)")
ISO_DATE_RE = re.compile(r"(?P<year>19\d{2}|20\d{2})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})")

ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

PUBLISHER_BY_DOMAIN = {
    "adk.dev": "Google Agent Development Kit",
    "arxiv.org": "arXiv",
    "github.com": "GitHub",
    "anthropic.com": "Anthropic",
    "claude.com": "Anthropic",
    "crewai.com": "CrewAI",
    "openai.com": "OpenAI",
    "huggingface.co": "Hugging Face",
    "langchain.com": "LangChain",
    "microsoft.com": "Microsoft",
    "google.com": "Google",
    "googleblog.com": "Google",
    "aws.amazon.com": "Amazon Web Services",
    "amazon.com": "Amazon",
    "preprints.org": "Preprints.org",
    "ainowinstitute.org": "AI Now Institute",
    "medium.com": "Medium",
    "substack.com": "Substack",
    "strandsagents.com": "Strands Agents",
    "x.com": "X",
    "youtube.com": "YouTube",
}

PUBLICATION_OVERRIDES = {
    "https://www.preprints.org/manuscript/202603.1756": {
        "authors": "Chaoyue He; Xin Zhou; Di Wang; Hong Xu; Wei Liu; Chunyan Miao",
        "publication_date": "2026-04-23",
        "publication_year": "2026",
        "publication_venue": "Preprints.org",
        "publisher": "Preprints.org",
        "doi": "10.20944/preprints202603.1756.v2",
        "publication_note": "Version 2; the primary source states that this preprint is not peer-reviewed.",
        "metadata_source": "primary-page",
    },
    "https://resources.anthropic.com/hubfs/Building%20Effective%20AI%20Agents-%20Architecture%20Patterns%20and%20Implementation%20Frameworks.pdf": {
        "authors": "Anthropic",
        "publication_date": "2025-12-03",
        "publication_year": "2025",
        "publication_venue": "Anthropic eBook",
        "publisher": "Anthropic",
        "publication_note": "Date verified from the primary PDF creation metadata.",
        "metadata_source": "pdf-metadata",
    },
    "https://adk.dev/evaluate/": {
        "authors": "Google Agent Development Kit",
        "publication_venue": "Google Agent Development Kit",
        "publisher": "Google",
        "metadata_source": "primary-page",
    },
    "https://adk.dev/sessions/": {
        "authors": "Google Agent Development Kit",
        "publication_venue": "Google Agent Development Kit",
        "publisher": "Google",
        "metadata_source": "primary-page",
    },
    "https://adk.dev/graphs/": {
        "authors": "Google Agent Development Kit",
        "publication_venue": "Google Agent Development Kit",
        "publisher": "Google",
        "metadata_source": "primary-page",
    },
    "https://docs.langchain.com/oss/python/langgraph/persistence": {
        "authors": "LangChain",
        "publication_venue": "LangGraph",
        "publisher": "LangChain",
        "metadata_source": "primary-page",
    },
    "https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints": {
        "authors": "Microsoft",
        "publication_venue": "Microsoft Agent Framework",
        "publisher": "Microsoft",
        "metadata_source": "primary-page",
    },
    "https://docs.crewai.com/en/concepts/flows": {
        "authors": "CrewAI",
        "publication_venue": "CrewAI",
        "publisher": "CrewAI",
        "metadata_source": "primary-page",
    },
    "https://strandsagents.com/docs/user-guide/concepts/agents/state/": {
        "authors": "Strands Agents",
        "publication_venue": "Strands Agents",
        "publisher": "Strands Agents",
        "metadata_source": "primary-page",
    },
    "https://strandsagents.com/docs/user-guide/concepts/multi-agent/graph/": {
        "authors": "Strands Agents",
        "publication_venue": "Strands Agents",
        "publisher": "Strands Agents",
        "metadata_source": "primary-page",
    },
}

FIELDS = [
    "row_id",
    "title",
    "url",
    "url_kind",
    "domain",
    "audit_status",
    "http_status",
    "final_url",
    "canonical_url",
    "content_type",
    "source_title",
    "source_description",
    "authors",
    "publication_date",
    "publication_year",
    "publication_venue",
    "publisher",
    "doi",
    "publication_note",
    "primary_category",
    "metadata_source",
    "github_repo",
    "github_stars",
    "github_forks",
    "github_open_issues",
    "github_description",
    "github_license",
    "github_created_at",
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


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title_parts: list[str] = []
        self.description = ""
        self.description_priority = 0
        self.meta_values: dict[str, list[str]] = {}

    @property
    def title(self) -> str:
        return clean(" ".join(self.title_parts))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True
            return
        if tag.lower() != "meta":
            return

        attr_map = {key.lower(): value or "" for key, value in attrs}
        name = (attr_map.get("name") or attr_map.get("property") or attr_map.get("itemprop") or "").lower()
        candidate = clean(attr_map.get("content"))
        if name and candidate:
            self.meta_values.setdefault(name, []).append(candidate)
        priority = {
            "description": 1,
            "og:description": 1,
            "twitter:description": 1,
            "dc.description": 2,
            "citation_abstract": 3,
        }.get(name, 0)
        if candidate and priority > self.description_priority:
            self.description = candidate
            self.description_priority = priority

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    def first(self, *names: str) -> str:
        for name in names:
            values = self.meta_values.get(name.lower(), [])
            if values:
                return values[0]
        return ""

    def all(self, *names: str) -> list[str]:
        for name in names:
            values = self.meta_values.get(name.lower(), [])
            if values:
                return list(dict.fromkeys(values))
        return []


class RedirectHandler(urllib.request.HTTPRedirectHandler):
    """Teach Python 3.9's urllib opener to follow permanent HTTP 308 moves."""

    def http_error_308(self, req, fp, code, msg, headers):  # type: ignore[no-untyped-def]
        return self.http_error_302(req, fp, code, msg, headers)

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        if code == 308 and req.get_method() in {"GET", "HEAD"}:
            code = 307
        return super().redirect_request(req, fp, code, msg, headers, newurl)


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


def normalize_date(value: str) -> str:
    value = clean(value)
    if not value:
        return ""
    match = ISO_DATE_RE.search(value)
    if match:
        return f"{match.group('year')}-{int(match.group('month')):02d}-{int(match.group('day')):02d}"
    year = YEAR_RE.search(value)
    return year.group("year") if year else ""


def year_from_value(value: str) -> str:
    match = YEAR_RE.search(value or "")
    return match.group("year") if match else ""


def normalize_doi(value: str) -> str:
    value = clean(value)
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.lower().startswith(prefix):
            value = value[len(prefix) :]
            break
    return value.strip()


def publisher_for_domain(domain: str) -> str:
    normalized = domain.lower().removeprefix("www.")
    for suffix, publisher in PUBLISHER_BY_DOMAIN.items():
        if normalized == suffix or normalized.endswith(f".{suffix}"):
            return publisher
    return normalized


def project_github_venue(url: str) -> str:
    path = urlparse(url).path.lower()
    if "/releases" in path:
        return "GitHub Releases"
    if "/discussions" in path:
        return "GitHub Discussions"
    return "GitHub"


def html_metadata(body: bytes, content_type: str) -> dict[str, str]:
    if "html" not in content_type.lower():
        return {}
    text = body[:750_000].decode("utf-8", errors="ignore")
    parser = MetadataParser()
    try:
        parser.feed(text)
    except Exception:  # noqa: BLE001 - source metadata should not fail the URL audit.
        return {}

    authors = parser.all("citation_author", "dc.creator", "author")
    publication_date = normalize_date(
        parser.first(
            "citation_publication_date",
            "citation_date",
            "article:published_time",
            "datepublished",
            "dc.date.issued",
            "dc.date",
            "date",
        )
    )
    publication_venue = parser.first(
        "citation_conference_title",
        "citation_journal_title",
        "citation_technical_report_institution",
    )
    publisher = parser.first("citation_publisher", "dc.publisher", "og:site_name", "application-name")
    doi = normalize_doi(parser.first("citation_doi", "dc.identifier.doi", "doi"))
    has_publication_metadata = any((authors, publication_date, publication_venue, publisher, doi))
    return {
        "source_title": parser.title,
        "source_description": parser.description,
        "authors": "; ".join(authors),
        "publication_date": publication_date,
        "publication_year": year_from_value(publication_date),
        "publication_venue": publication_venue,
        "publisher": publisher,
        "doi": doi,
        "metadata_source": "html-meta" if has_publication_metadata else "",
    }


def fetch_url(url: str, timeout: float, attempts: int) -> dict[str, str]:
    context = ssl._create_unverified_context()
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=context),
        RedirectHandler(),
    )
    last_error = ""
    parsed_url = urlparse(url)
    request_url = url

    for attempt in range(1, attempts + 1):
        for method in ("GET", "HEAD"):
            request = urllib.request.Request(
                request_url,
                method=method,
                headers={"User-Agent": "awesome-loop-engineering-source-audit"},
            )
            try:
                with opener.open(request, timeout=timeout) as response:
                    final_url = response.geturl()
                    final_host = urlparse(final_url).netloc.lower()
                    if parsed_url.netloc.lower() == "code.claude.com" and final_host not in {
                        "",
                        "code.claude.com",
                        "docs.anthropic.com",
                    }:
                        return {
                            "audit_status": "restricted",
                            "http_status": str(response.status),
                            "final_url": request_url,
                            "content_type": response.headers.get("content-type", ""),
                            "source_title": "",
                            "source_description": "",
                            "error": f"redirected_to_unrelated_host:{final_host}",
                        }
                    content_type = response.headers.get("content-type", "")
                    body = response.read(750_000) if method == "GET" else b""
                    metadata = html_metadata(body, content_type)
                    result = {
                        "audit_status": "ok",
                        "http_status": str(response.status),
                        "final_url": final_url,
                        "content_type": content_type,
                        "error": "",
                    }
                    result.update(metadata)
                    return result
            except urllib.error.HTTPError as error:
                if method == "HEAD":
                    continue
                error_host = urlparse(error.geturl()).netloc.lower()
                if parsed_url.netloc.lower() == "code.claude.com" and error_host not in {
                    "",
                    "code.claude.com",
                    "docs.anthropic.com",
                }:
                    return {
                        "audit_status": "restricted",
                        "http_status": str(error.code),
                        "final_url": request_url,
                        "content_type": error.headers.get("content-type", "") if error.headers else "",
                        "source_title": "",
                        "source_description": "",
                        "error": f"redirected_to_unrelated_host:{error_host}",
                    }
                if error.code == 404 and parsed_url.netloc.lower() == "code.claude.com" and attempt < attempts:
                    last_error = "HTTPError:404"
                    break
                if error.code in RESTRICTED_HTTP:
                    return {
                        "audit_status": "restricted",
                        "http_status": str(error.code),
                        "final_url": request_url,
                        "content_type": error.headers.get("content-type", "") if error.headers else "",
                        "source_title": "",
                        "source_description": "",
                        "error": "restricted_or_rate_limited",
                    }
                return {
                    "audit_status": "broken",
                    "http_status": str(error.code),
                    "final_url": request_url,
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
            delay = 1.5 * attempt if parsed_url.netloc.lower() == "code.claude.com" else 0.25 * attempt
            time.sleep(min(4.0, delay))

    return {
        "audit_status": "unreachable",
        "http_status": "",
        "final_url": request_url,
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
        "canonical_url": "",
        "content_type": "",
        "source_title": "",
        "source_description": "",
        "authors": "",
        "publication_date": "",
        "publication_year": "",
        "publication_venue": "",
        "publisher": "",
        "doi": "",
        "publication_note": "",
        "primary_category": "",
        "metadata_source": "",
        "github_repo": github_repo_from_url(row["url"]),
        "github_stars": "",
        "github_forks": "",
        "github_open_issues": "",
        "github_description": "",
        "github_license": "",
        "github_created_at": "",
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
                    "final_url": f"{REPO_BLOB_URL}/{local_target}" + (f"#{fragment}" if fragment else ""),
                    "source_title": row["title"],
                    "publication_year": "2026",
                    "publication_venue": "GitHub",
                    "publisher": "GitHub",
                    "metadata_source": "repository",
                }
            )
        else:
            base.update({"audit_status": "local_missing", "error": "local_path_missing"})
        return base

    if row["url_kind"] == "local_anchor":
        base.update(
            {
                "audit_status": "local_anchor",
                "final_url": row["url"],
                "publication_year": "2026",
                "publication_venue": "GitHub",
                "publisher": "GitHub",
                "metadata_source": "repository",
            }
        )
        return base

    base.update(fetch_url(row["url"], timeout=timeout, attempts=attempts))
    return base


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
        "github_created_at": clean(str(data.get("created_at", ""))),
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


def fetch_arxiv_batch(arxiv_ids: list[str], timeout: float, attempts: int) -> dict[str, dict[str, str]]:
    query = urlencode({"id_list": ",".join(arxiv_ids), "max_results": str(len(arxiv_ids))})
    url = f"https://export.arxiv.org/api/query?{query}"
    context = ssl._create_unverified_context()
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "awesome-loop-engineering-publication-audit"},
    )

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                root = ET.fromstring(response.read())
            break
        except Exception:  # noqa: BLE001 - fallback metadata remains explicit below.
            if attempt == attempts:
                return {}
            time.sleep(min(3.0, attempt))

    records: dict[str, dict[str, str]] = {}
    for entry in root.findall(f"{ATOM_NS}entry"):
        entry_url = clean(entry.findtext(f"{ATOM_NS}id") or "")
        match = ARXIV_RE.search(entry_url)
        if not match:
            continue
        arxiv_id = match.group("id")
        authors = [
            clean(author.findtext(f"{ATOM_NS}name") or "")
            for author in entry.findall(f"{ATOM_NS}author")
        ]
        primary = entry.find(f"{ARXIV_NS}primary_category")
        published = normalize_date(entry.findtext(f"{ATOM_NS}published") or "")
        journal_reference = clean(entry.findtext(f"{ARXIV_NS}journal_ref") or "")
        records[arxiv_id] = {
            "authors": "; ".join(author for author in authors if author),
            "publication_date": published,
            "publication_year": year_from_value(published),
            "publication_venue": journal_reference or "arXiv",
            "publisher": "arXiv",
            "doi": normalize_doi(entry.findtext(f"{ARXIV_NS}doi") or ""),
            "publication_note": clean(entry.findtext(f"{ARXIV_NS}comment") or ""),
            "primary_category": clean(primary.get("term", "")) if primary is not None else "",
            "metadata_source": "arxiv-api",
        }
    return records


def arxiv_year(arxiv_id: str) -> str:
    try:
        return str(2000 + int(arxiv_id[:2]))
    except (TypeError, ValueError):
        return ""


def enrich_arxiv(rows: list[dict[str, str]], timeout: float, attempts: int) -> None:
    arxiv_ids = sorted({row["arxiv_id"] for row in rows if row["arxiv_id"]})
    records: dict[str, dict[str, str]] = {}
    batch_size = 75
    for start in range(0, len(arxiv_ids), batch_size):
        if start:
            time.sleep(3.0)
        records.update(fetch_arxiv_batch(arxiv_ids[start : start + batch_size], timeout, attempts))

    for row in rows:
        arxiv_id = row["arxiv_id"]
        if not arxiv_id:
            continue
        metadata = records.get(arxiv_id)
        if metadata:
            row.update({key: value for key, value in metadata.items() if value})
        else:
            row["publisher"] = "arXiv"
            row["publication_year"] = row["publication_year"] or arxiv_year(arxiv_id)
            row["metadata_source"] = row["metadata_source"] or "arxiv-id"


def load_arxiv_publication_decisions() -> dict[str, dict[str, str]]:
    if not ARXIV_PUBLICATION_AUDIT.exists():
        return {}
    with ARXIV_PUBLICATION_AUDIT.open(encoding="utf-8", newline="") as handle:
        return {row["arxiv_id"]: row for row in csv.DictReader(handle)}


def apply_arxiv_publication_overlay(rows: list[dict[str, str]]) -> None:
    decisions = load_arxiv_publication_decisions()
    for row in rows:
        row["canonical_url"] = row.get("canonical_url") or row.get("final_url") or row["url"]
        decision = decisions.get(row.get("arxiv_id", ""))
        if not decision or decision["status"] not in {"accepted", "published"}:
            continue

        for field in (
            "publication_date",
            "publication_year",
            "publication_venue",
            "publisher",
            "doi",
            "metadata_source",
        ):
            row[field] = decision[field]
        row["canonical_url"] = decision["published_url"] or row["canonical_url"]
        if decision["status"] == "accepted":
            row["publication_note"] = (
                f"Accepted at {decision['publication_venue']}; "
                "the linked arXiv record is the available paper version."
            )
        else:
            row["publication_note"] = (
                f"Published in {decision['publication_venue']}; "
                "the linked arXiv record remains available for open access."
            )


def year_from_url(url: str) -> str:
    parsed = urlparse(url)
    match = re.search(r"/(?:manuscript/)?(?P<year>20\d{2})(?:[/_-]|\d{2}\.)", parsed.path)
    if not match:
        return ""
    year = int(match.group("year"))
    return str(year) if year <= datetime.now(timezone.utc).year + 1 else ""


def finalize_publication_metadata(rows: list[dict[str, str]]) -> None:
    for row in rows:
        override = PUBLICATION_OVERRIDES.get(row["url"], {})
        row.update({key: value for key, value in override.items() if value})

        if row["github_repo"]:
            row["publisher"] = "GitHub"
            if row["github_repo"].lower() == PROJECT_GITHUB_REPO:
                row["publication_venue"] = project_github_venue(row["url"])
            else:
                row["publication_venue"] = row["publication_venue"] or row["github_repo"]
            if not row["publication_date"] and row["github_created_at"]:
                row["publication_date"] = normalize_date(row["github_created_at"])
                row["metadata_source"] = "github-api"

        if not row["publisher"]:
            row["publisher"] = publisher_for_domain(row["domain"]) or "Source not stated"
        if not row["publication_year"]:
            row["publication_year"] = year_from_value(row["publication_date"])
        if not row["publication_year"]:
            row["publication_year"] = year_from_url(row["url"])
            if row["publication_year"] and not row["metadata_source"]:
                row["metadata_source"] = "url-date"
        if not row["metadata_source"]:
            row["metadata_source"] = "domain-fallback"
        row["doi"] = normalize_doi(row["doi"])


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
    parser.add_argument(
        "--apply-publication-overlay-only",
        action="store_true",
        help="apply the checked-in arXiv publication decisions to the existing source audit without network access",
    )
    args = parser.parse_args()

    if args.apply_publication_overlay_only:
        with AUDIT_CSV.open(encoding="utf-8", newline="") as handle:
            audited = list(csv.DictReader(handle))
        apply_arxiv_publication_overlay(audited)
        write_audit(audited)
        resolved = sum(
            bool(row.get("arxiv_id")) and row.get("publisher") not in {"", "arXiv"}
            for row in audited
        )
        print(f"Applied {resolved} published or accepted venue records to {AUDIT_CSV.relative_to(ROOT)}")
        return 0

    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows = read_rows()
    with futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        checks = [executor.submit(audit_row, row, retrieved_at, args.timeout, args.attempts) for row in rows]
        audited = [check.result() for check in futures.as_completed(checks)]

    audited.sort(key=lambda row: row["row_id"])
    enrich_github(audited, timeout=args.timeout, use_gh_cli=args.github_cli)
    enrich_arxiv(audited, timeout=max(args.timeout, 20.0), attempts=args.attempts)
    finalize_publication_metadata(audited)
    apply_arxiv_publication_overlay(audited)
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
