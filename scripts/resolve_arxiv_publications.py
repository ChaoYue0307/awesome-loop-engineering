#!/usr/bin/env python3
"""Resolve arXiv resources to verified conference or journal versions."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import ssl
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote, urlencode, urlparse


ROOT = Path(__file__).resolve().parents[1]
SOURCE_AUDIT = ROOT / "data" / "resource_source_audit.csv"
OUTPUT = ROOT / "data" / "arxiv_publication_audit.csv"
VERIFIED_OVERRIDES = ROOT / "data" / "arxiv_publication_overrides.csv"
USER_AGENT = "awesome-loop-engineering-publication-resolver/1.0 (https://github.com/ChaoYue0307/awesome-loop-engineering)"
DBLP_API = "https://dblp.uni-trier.de/search/publ/api"

FIELDS = [
    "row_id",
    "arxiv_id",
    "resource_title",
    "arxiv_title",
    "arxiv_year",
    "status",
    "published_title",
    "publication_date",
    "publication_year",
    "publication_venue",
    "publisher",
    "doi",
    "published_url",
    "record_url",
    "metadata_source",
    "match_score",
    "checked_on",
]

PUBLISHED_DBLP_TYPES = {
    "Conference and Workshop Papers",
    "Journal Articles",
    "Parts in Books or Collections",
}
PUBLISHED_CROSSREF_TYPES = {
    "book-chapter",
    "journal-article",
    "proceedings-article",
    "reference-entry",
}
PREPRINT_VENUES = {"", "corr", "arxiv"}

VENUE_NAMES = {
    "AAAI": "AAAI Conference on Artificial Intelligence",
    "ACL": "Annual Meeting of the Association for Computational Linguistics (ACL)",
    "CHI": "ACM CHI Conference on Human Factors in Computing Systems",
    "COLM": "Conference on Language Modeling (COLM)",
    "EACL": "Conference of the European Chapter of the Association for Computational Linguistics (EACL)",
    "EMNLP": "Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    "ICLR": "International Conference on Learning Representations (ICLR)",
    "ICML": "International Conference on Machine Learning (ICML)",
    "IJCAI": "International Joint Conference on Artificial Intelligence (IJCAI)",
    "NAACL": "Conference of the North American Chapter of the Association for Computational Linguistics (NAACL)",
    "NeurIPS": "Advances in Neural Information Processing Systems (NeurIPS)",
    "TMLR": "Transactions on Machine Learning Research",
}

PUBLISHER_BY_HOST = {
    "aclanthology.org": "Association for Computational Linguistics",
    "dl.acm.org": "Association for Computing Machinery",
    "ieeexplore.ieee.org": "IEEE",
    "jmlr.org": "JMLR.org",
    "openreview.net": "OpenReview",
    "ojs.aaai.org": "AAAI Press",
    "papers.nips.cc": "Neural Information Processing Systems Foundation",
    "proceedings.mlr.press": "PMLR",
    "link.springer.com": "Springer",
    "usenix.org": "USENIX Association",
}


def clean(value: object) -> str:
    if value is None:
        return ""
    return " ".join(html.unescape(str(value)).strip().split())


def normalize_doi(value: object) -> str:
    doi = clean(value)
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix) :]
            break
    if doi.lower().startswith("10.48550/arxiv."):
        return ""
    return doi


def normalize_title(value: object) -> str:
    title = re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", clean(value))
    title = re.sub(r"<[^>]+>", " ", title)
    title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def title_match(left: str, right: str) -> tuple[float, float]:
    left_norm = normalize_title(left)
    right_norm = normalize_title(right)
    ratio = SequenceMatcher(None, left_norm, right_norm).ratio()
    left_tokens = set(left_norm.split())
    right_tokens = set(right_norm.split())
    union = left_tokens | right_tokens
    jaccard = len(left_tokens & right_tokens) / len(union) if union else 0.0
    return ratio, jaccard


def surname(value: str) -> str:
    parts = re.findall(r"[a-z]+", unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower())
    while parts and parts[-1].isdigit():
        parts.pop()
    return parts[-1] if parts else ""


def author_overlap(source_authors: str, candidate_authors: list[str]) -> bool:
    source = {surname(author) for author in source_authors.split(";") if surname(author)}
    candidate = {surname(author) for author in candidate_authors if surname(author)}
    return bool(source & candidate)


def json_request(
    url: str,
    timeout: float,
    attempts: int = 3,
    cache_path: Path | None = None,
    offline: bool = False,
) -> dict[str, object]:
    if cache_path and cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    if offline:
        return {}
    context = ssl._create_unverified_context()
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            if attempt == attempts:
                return {}
            time.sleep(attempt)
    return {}


def list_value(value: object) -> list[object]:
    if value in (None, ""):
        return []
    return value if isinstance(value, list) else [value]


def dblp_authors(info: dict[str, object]) -> list[str]:
    authors = info.get("authors") or {}
    if not isinstance(authors, dict):
        return []
    values = list_value(authors.get("author"))
    result = []
    for value in values:
        if isinstance(value, dict):
            result.append(clean(value.get("text")))
        else:
            result.append(clean(value))
    return [value for value in result if value]


def choose_official_url(info: dict[str, object], doi: str) -> str:
    if doi:
        return f"https://doi.org/{doi}"
    electronic_editions = [clean(value) for value in list_value(info.get("ee"))]
    electronic_editions = [
        value
        for value in electronic_editions
        if value and "arxiv.org" not in value.lower() and "10.48550/arxiv" not in value.lower()
    ]
    preferred_hosts = tuple(PUBLISHER_BY_HOST)
    for value in electronic_editions:
        if urlparse(value).netloc.lower() in preferred_hosts:
            return value
    return electronic_editions[0] if electronic_editions else clean(info.get("url"))


def publication_year_from_crossref(message: dict[str, object]) -> str:
    for field in ("published-print", "published-online", "published", "issued"):
        value = message.get(field)
        if not isinstance(value, dict):
            continue
        parts = value.get("date-parts")
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            return str(parts[0][0])
    return ""


def publication_date_from_crossref(message: dict[str, object]) -> str:
    for field in ("published-print", "published-online", "published", "issued"):
        value = message.get(field)
        if not isinstance(value, dict):
            continue
        parts = value.get("date-parts")
        if not isinstance(parts, list) or not parts or not isinstance(parts[0], list) or not parts[0]:
            continue
        date_parts = parts[0]
        if len(date_parts) >= 3:
            return f"{int(date_parts[0]):04d}-{int(date_parts[1]):02d}-{int(date_parts[2]):02d}"
        return str(date_parts[0])
    return ""


def crossref_message_for_doi(
    doi: str,
    timeout: float,
    cache_path: Path | None = None,
    offline: bool = False,
) -> dict[str, object]:
    if not doi:
        return {}
    payload = json_request(
        f"https://api.crossref.org/works/{quote(doi, safe='')}",
        timeout,
        cache_path=cache_path,
        offline=offline,
    )
    message = payload.get("message")
    return message if isinstance(message, dict) else {}


def display_venue(venue: str, year: str, crossref: dict[str, object]) -> str:
    crossref_type = clean(crossref.get("type"))
    container = next((clean(value) for value in list_value(crossref.get("container-title")) if clean(value)), "")
    event = crossref.get("event") or {}
    event_name = clean(event.get("name")) if isinstance(event, dict) else ""
    if crossref_type == "journal-article" and container:
        base = container
    elif event_name:
        base = event_name
    else:
        base = VENUE_NAMES.get(venue, venue)
    if year and year not in base:
        return f"{base} {year}"
    return base


def publisher_for(url: str, venue: str, crossref: dict[str, object]) -> str:
    publisher = clean(crossref.get("publisher"))
    if publisher:
        return publisher
    host = urlparse(url).netloc.lower().removeprefix("www.")
    for domain, name in PUBLISHER_BY_HOST.items():
        if host == domain or host.endswith(f".{domain}"):
            return name
    if venue in {"ACL", "EACL", "EMNLP", "NAACL"}:
        return "Association for Computational Linguistics"
    if venue == "AAAI":
        return "AAAI Press"
    if venue == "NeurIPS":
        return "Neural Information Processing Systems Foundation"
    if venue in {"ICML"}:
        return "PMLR"
    if venue in {"ICLR", "TMLR", "COLM"}:
        return "OpenReview"
    return venue


def published_dblp_candidate(
    row: dict[str, str],
    timeout: float,
    cache_dir: Path | None = None,
    offline: bool = False,
) -> dict[str, str] | None:
    query_title = re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", row["source_title"]) or row["title"]
    params = urlencode({"q": query_title, "format": "json", "h": "30"})
    cache_path = cache_dir / "dblp" / f"{row['arxiv_id']}.json" if cache_dir else None
    payload = json_request(
        f"{DBLP_API}?{params}",
        timeout,
        cache_path=cache_path,
        offline=offline,
    )
    result = payload.get("result") or {}
    hits = result.get("hits") or {} if isinstance(result, dict) else {}
    values = list_value(hits.get("hit")) if isinstance(hits, dict) else []
    candidates: list[tuple[tuple[float, ...], dict[str, object], float]] = []

    for value in values:
        if not isinstance(value, dict) or not isinstance(value.get("info"), dict):
            continue
        info = value["info"]
        venue = clean(info.get("venue"))
        kind = clean(info.get("type"))
        if venue.lower() in PREPRINT_VENUES or kind not in PUBLISHED_DBLP_TYPES:
            continue
        candidate_title = clean(info.get("title")).rstrip(".")
        ratio, jaccard = title_match(query_title, candidate_title)
        authors_match = author_overlap(row["authors"], dblp_authors(info))
        exact = normalize_title(query_title) == normalize_title(candidate_title)
        accepted = exact or (ratio >= 0.94 and jaccard >= 0.82 and authors_match)
        if not accepted:
            continue
        doi = normalize_doi(info.get("doi"))
        score = (float(exact), ratio, jaccard, float(authors_match), float(bool(doi)))
        candidates.append((score, info, ratio))

    if not candidates:
        return None

    _, info, score = max(candidates, key=lambda candidate: candidate[0])
    venue = clean(info.get("venue"))
    year = clean(info.get("year"))
    doi = normalize_doi(info.get("doi"))
    crossref_path = cache_dir / "crossref-doi" / f"{row['arxiv_id']}.json" if cache_dir else None
    crossref = crossref_message_for_doi(doi, timeout, crossref_path, offline)
    if crossref:
        published_title = next((clean(value) for value in list_value(crossref.get("title")) if clean(value)), "")
        if published_title and title_match(query_title, published_title)[0] < 0.90:
            crossref = {}
    official_url = choose_official_url(info, doi)
    crossref_year = publication_year_from_crossref(crossref)
    year = crossref_year or year
    return {
        "published_title": clean(info.get("title")).rstrip("."),
        "publication_date": publication_date_from_crossref(crossref) or year,
        "publication_year": year,
        "publication_venue": display_venue(venue, year, crossref),
        "publisher": publisher_for(official_url, venue, crossref),
        "doi": doi,
        "published_url": official_url,
        "record_url": clean(info.get("url")),
        "metadata_source": "DBLP API + primary publication record",
        "match_score": f"{score:.3f}",
    }


def crossref_authors(message: dict[str, object]) -> list[str]:
    values = list_value(message.get("author"))
    result = []
    for value in values:
        if not isinstance(value, dict):
            continue
        result.append(clean(f"{clean(value.get('given'))} {clean(value.get('family'))}"))
    return [value for value in result if value]


def published_crossref_candidate(
    row: dict[str, str],
    timeout: float,
    cache_dir: Path | None = None,
    offline: bool = False,
) -> dict[str, str] | None:
    query_title = re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", row["source_title"]) or row["title"]
    params = urlencode({"query.title": query_title, "rows": "8"})
    cache_path = cache_dir / "crossref-search" / f"{row['arxiv_id']}.json" if cache_dir else None
    payload = json_request(
        f"https://api.crossref.org/works?{params}",
        timeout,
        cache_path=cache_path,
        offline=offline,
    )
    message = payload.get("message") or {}
    items = list_value(message.get("items")) if isinstance(message, dict) else []
    candidates: list[tuple[tuple[float, ...], dict[str, object], float]] = []
    for item in items:
        if not isinstance(item, dict) or clean(item.get("type")) not in PUBLISHED_CROSSREF_TYPES:
            continue
        candidate_title = next((clean(value) for value in list_value(item.get("title")) if clean(value)), "")
        ratio, jaccard = title_match(query_title, candidate_title)
        authors_match = author_overlap(row["authors"], crossref_authors(item))
        exact = normalize_title(query_title) == normalize_title(candidate_title)
        if not (exact or (ratio >= 0.97 and jaccard >= 0.90 and authors_match)):
            continue
        doi = normalize_doi(item.get("DOI"))
        if not doi:
            continue
        candidates.append(((float(exact), ratio, jaccard, float(authors_match)), item, ratio))

    if not candidates:
        return None
    _, item, score = max(candidates, key=lambda candidate: candidate[0])
    year = publication_year_from_crossref(item)
    container = next((clean(value) for value in list_value(item.get("container-title")) if clean(value)), "")
    event = item.get("event") or {}
    event_name = clean(event.get("name")) if isinstance(event, dict) else ""
    venue = event_name or container
    if year and year not in venue:
        venue = f"{venue} {year}"
    doi = normalize_doi(item.get("DOI"))
    official_url = f"https://doi.org/{doi}"
    return {
        "published_title": next((clean(value) for value in list_value(item.get("title")) if clean(value)), ""),
        "publication_date": publication_date_from_crossref(item) or year,
        "publication_year": year,
        "publication_venue": venue,
        "publisher": publisher_for(official_url, "", item),
        "doi": doi,
        "published_url": official_url,
        "record_url": official_url,
        "metadata_source": "Crossref API + DOI record",
        "match_score": f"{score:.3f}",
    }


def existing_publication_candidate(
    row: dict[str, str],
    timeout: float,
    cache_dir: Path | None = None,
    offline: bool = False,
) -> dict[str, str] | None:
    venue = clean(row.get("publication_venue"))
    if venue.lower() in PREPRINT_VENUES:
        return None
    doi = normalize_doi(row.get("doi"))
    crossref_path = cache_dir / "crossref-doi" / f"{row['arxiv_id']}.json" if cache_dir else None
    crossref = crossref_message_for_doi(doi, timeout, crossref_path, offline)
    year = publication_year_from_crossref(crossref) or clean(row.get("publication_year"))
    published_url = f"https://doi.org/{doi}" if doi else clean(row.get("url"))
    return {
        "published_title": re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", clean(row.get("source_title"))) or clean(row.get("title")),
        "publication_date": publication_date_from_crossref(crossref) or year,
        "publication_year": year,
        "publication_venue": display_venue(venue, year, crossref),
        "publisher": publisher_for(published_url, venue, crossref),
        "doi": doi,
        "published_url": published_url,
        "record_url": clean(row.get("url")),
        "metadata_source": "arXiv journal reference" + (" + DOI record" if crossref else ""),
        "match_score": "1.000",
    }


def base_output(row: dict[str, str], checked_on: str) -> dict[str, str]:
    arxiv_title = re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", clean(row.get("source_title"))) or clean(row.get("title"))
    return {
        "row_id": clean(row.get("row_id")),
        "arxiv_id": clean(row.get("arxiv_id")),
        "resource_title": clean(row.get("title")),
        "arxiv_title": arxiv_title,
        "arxiv_year": clean(row.get("publication_year")),
        "status": "preprint-only",
        "published_title": "",
        "publication_date": "",
        "publication_year": "",
        "publication_venue": "",
        "publisher": "",
        "doi": "",
        "published_url": "",
        "record_url": "",
        "metadata_source": "DBLP and Crossref exact-title audit",
        "match_score": "",
        "checked_on": checked_on,
    }


def read_source_rows() -> list[dict[str, str]]:
    with SOURCE_AUDIT.open(encoding="utf-8", newline="") as handle:
        return [row for row in csv.DictReader(handle) if row.get("arxiv_id")]


def read_existing() -> dict[str, dict[str, str]]:
    if not OUTPUT.exists():
        return {}
    with OUTPUT.open(encoding="utf-8", newline="") as handle:
        return {row["arxiv_id"]: row for row in csv.DictReader(handle)}


def read_verified_overrides() -> dict[str, dict[str, str]]:
    if not VERIFIED_OVERRIDES.exists():
        return {}
    with VERIFIED_OVERRIDES.open(encoding="utf-8", newline="") as handle:
        return {row["arxiv_id"]: row for row in csv.DictReader(handle)}


def verified_candidate(row: dict[str, str], overrides: dict[str, dict[str, str]]) -> dict[str, str] | None:
    override = overrides.get(row["arxiv_id"])
    if not override:
        return None
    return {
        "status": override["status"],
        "published_title": re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", clean(row.get("source_title"))) or clean(row.get("title")),
        "publication_date": override["publication_date"],
        "publication_year": override["publication_year"],
        "publication_venue": override["publication_venue"],
        "publisher": override["publisher"],
        "doi": normalize_doi(override["doi"]),
        "published_url": override["published_url"],
        "record_url": override["record_url"],
        "metadata_source": override["metadata_source"],
        "match_score": "1.000",
    }


def resolve_row(
    row: dict[str, str],
    timeout: float,
    delay: float,
    cache_dir: Path | None,
    offline: bool,
    overrides: dict[str, dict[str, str]],
) -> dict[str, str] | None:
    candidate = verified_candidate(row, overrides)
    if candidate:
        return candidate
    candidate = published_dblp_candidate(row, timeout, cache_dir, offline)
    if delay:
        time.sleep(delay)
    if candidate:
        return candidate
    candidate = published_crossref_candidate(row, timeout, cache_dir, offline)
    if delay:
        time.sleep(delay)
    return candidate or existing_publication_candidate(row, timeout, cache_dir, offline)


def dblp_query(row: dict[str, str]) -> str:
    query_title = re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", row["source_title"]) or row["title"]
    return f"{DBLP_API}?{urlencode({'q': query_title, 'format': 'json', 'h': '30'})}"


def crossref_search_query(row: dict[str, str]) -> str:
    query_title = re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", row["source_title"]) or row["title"]
    return f"https://api.crossref.org/works?{urlencode({'query.title': query_title, 'rows': '8'})}"


def write_curl_config(path: Path, requests: list[tuple[str, Path]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "location",
        "silent",
        "show-error",
        "retry = 2",
        "connect-timeout = 15",
        "max-time = 45",
    ]
    for url, output in requests:
        output.parent.mkdir(parents=True, exist_ok=True)
        lines.extend(
            [
                f'output = "{output}"',
                f'url = "{url}"',
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_dblp_curl_config(path: Path, cache_dir: Path, rows: list[dict[str, str]]) -> None:
    requests = [(dblp_query(row), cache_dir / "dblp" / f"{row['arxiv_id']}.json") for row in rows]
    write_curl_config(path, requests)
    print(f"Wrote {len(requests)} DBLP requests to {path}.")


def write_crossref_curl_config(path: Path, cache_dir: Path, rows: list[dict[str, str]], timeout: float) -> None:
    requests: list[tuple[str, Path]] = []
    for row in rows:
        dblp_candidate = published_dblp_candidate(row, timeout, cache_dir, offline=True)
        doi = normalize_doi(dblp_candidate.get("doi")) if dblp_candidate else ""
        if not doi:
            doi = normalize_doi(row.get("doi"))
        if doi:
            requests.append(
                (
                    f"https://api.crossref.org/works/{quote(doi, safe='')}",
                    cache_dir / "crossref-doi" / f"{row['arxiv_id']}.json",
                )
            )
        if not dblp_candidate:
            requests.append(
                (
                    crossref_search_query(row),
                    cache_dir / "crossref-search" / f"{row['arxiv_id']}.json",
                )
            )
    write_curl_config(path, requests)
    print(f"Wrote {len(requests)} Crossref requests to {path}.")


def validate_snapshot(
    rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    overrides: dict[str, dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    expected = {row["arxiv_id"] for row in source_rows}
    actual = {row["arxiv_id"] for row in rows}
    by_id = {row["arxiv_id"]: row for row in rows}
    if expected != actual:
        failures.append(f"snapshot IDs differ: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    unknown_overrides = set(overrides) - expected
    if unknown_overrides:
        failures.append(f"verified overrides are not present in the source audit: {sorted(unknown_overrides)}")
    for row in rows:
        if row["status"] not in {"preprint-only", "accepted", "published"}:
            failures.append(f"{row['arxiv_id']}: invalid status {row['status']!r}")
        if row["status"] in {"accepted", "published"}:
            required = ("publication_year", "publication_venue", "publisher", "published_url", "metadata_source")
            missing = [field for field in required if not row.get(field)]
            if missing:
                failures.append(f"{row['arxiv_id']}: resolved row missing {', '.join(missing)}")
            if row.get("publication_venue", "").lower() in PREPRINT_VENUES:
                failures.append(f"{row['arxiv_id']}: resolved row still names a preprint venue")
    for arxiv_id, override in overrides.items():
        row = by_id.get(arxiv_id)
        if not row:
            continue
        for field in (
            "status",
            "publication_date",
            "publication_year",
            "publication_venue",
            "publisher",
            "doi",
            "published_url",
            "record_url",
            "metadata_source",
        ):
            expected_value = normalize_doi(override[field]) if field == "doi" else override[field]
            if row.get(field, "") != expected_value:
                failures.append(
                    f"{arxiv_id}: {field} differs from verified override "
                    f"({row.get(field, '')!r} != {expected_value!r})"
                )
    return failures


def write_rows(rows: list[dict[str, str]]) -> None:
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the checked-in snapshot without network access")
    parser.add_argument("--refresh", action="store_true", help="refresh every arXiv record instead of only new entries")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--delay", type=float, default=0.15, help="polite delay between API requests")
    parser.add_argument("--limit", type=int, default=0, help="resolve only the first N rows (development only)")
    parser.add_argument("--cache-dir", type=Path, help="read API responses from a reusable local cache")
    parser.add_argument("--offline", action="store_true", help="do not make network requests; requires --cache-dir")
    parser.add_argument("--write-dblp-curl-config", type=Path, help="write a curl config for caching DBLP responses")
    parser.add_argument("--write-crossref-curl-config", type=Path, help="write a curl config after DBLP responses are cached")
    args = parser.parse_args()

    source_rows = read_source_rows()
    existing = read_existing()
    overrides = read_verified_overrides()
    if args.write_dblp_curl_config:
        if not args.cache_dir:
            parser.error("--write-dblp-curl-config requires --cache-dir")
        write_dblp_curl_config(args.write_dblp_curl_config, args.cache_dir, source_rows)
        return 0
    if args.write_crossref_curl_config:
        if not args.cache_dir:
            parser.error("--write-crossref-curl-config requires --cache-dir")
        write_crossref_curl_config(args.write_crossref_curl_config, args.cache_dir, source_rows, args.timeout)
        return 0
    if args.offline and not args.cache_dir:
        parser.error("--offline requires --cache-dir")
    if args.check:
        failures = validate_snapshot(list(existing.values()), source_rows, overrides)
        if failures:
            print("arXiv publication audit check failed:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
            return 1
        resolved = sum(row["status"] in {"accepted", "published"} for row in existing.values())
        accepted = sum(row["status"] == "accepted" for row in existing.values())
        print(
            f"Validated {len(existing)} arXiv publication decisions "
            f"({resolved} venue-resolved; {accepted} accepted and awaiting archival publication)."
        )
        return 0

    checked_on = datetime.now(timezone.utc).date().isoformat()
    output_rows: list[dict[str, str]] = []
    refresh_rows = source_rows[: args.limit or None]
    refresh_ids = {row["arxiv_id"] for row in refresh_rows}
    for index, row in enumerate(source_rows, 1):
        old = existing.get(row["arxiv_id"])
        if row["arxiv_id"] not in refresh_ids or (old and not args.refresh and old.get("arxiv_title") == base_output(row, checked_on)["arxiv_title"]):
            output_rows.append(old or base_output(row, checked_on))
            continue
        print(f"[{index}/{len(source_rows)}] {row['arxiv_id']} {row['title']}", flush=True)
        output = base_output(row, checked_on)
        candidate = resolve_row(
            row,
            timeout=args.timeout,
            delay=args.delay,
            cache_dir=args.cache_dir,
            offline=args.offline,
            overrides=overrides,
        )
        if candidate:
            output.update({key: value for key, value in candidate.items() if key != "status"})
            output["status"] = candidate.get("status", "published")
        output_rows.append(output)

    failures = validate_snapshot(output_rows, source_rows, overrides)
    if failures:
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    write_rows(output_rows)
    resolved = sum(row["status"] in {"accepted", "published"} for row in output_rows)
    accepted = sum(row["status"] == "accepted" for row in output_rows)
    print(
        f"Wrote {len(output_rows)} decisions to {OUTPUT.relative_to(ROOT)} "
        f"({resolved} venue-resolved; {accepted} accepted and awaiting archival publication)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
