# Dataset Exports

This directory contains generated tabular exports of the canonical English `README.md` resource list.

- `resources.csv` - Tabular export for spreadsheets and ad hoc analysis.
- `resources.jsonl` - JSON Lines export; this file backs the Hugging Face Dataset Viewer (the dataset card's configs point at it).
- `../docs/assets/resources.json` - Slim generated payload used by the website's searchable Resource Atlas.
- `first_seen.json` - Forward-only sidecar mapping resource URL to the date it was first added; the export left-joins it into the `date_added` column. Empty `date_added` means the entry predates per-entry tracking (started 2026-07-15).
- `resource_source_audit.csv` - Retrieval-time audit of every row, including URL status, source title metadata, arXiv IDs, and GitHub repository stats where available.

The main exports preserve the original section and annotation while adding three complementary discovery layers:

- **Task facets**: `collection`, `user_goal`, `lifecycle_stages`, and `audience` answer why a reader needs the source and where it fits in the Loop Contract.
- **Evidence facets**: `evidence_class`, `signal_strength`, `source_status`, canonical URL, source metadata, GitHub statistics, arXiv ID, and audit timestamp separate source provenance from popularity or editorial judgment.
- **Publication facets**: `authors`, `publication_date`, `publication_year`, `publication_venue`, `publisher`, `doi`, `publication_note`, `primary_category`, and `metadata_source` provide a paper-like bibliographic row without inventing missing facts.

`key_contribution`, `novelty`, and `impact` are resource-specific. `signal` states the evidence basis and its limits; GitHub stars and forks are reported as current context, never as proof of reliability. Signal strength is calibrated as `high` for primary official documentation and benchmarks, `medium` for inspectable implementations, papers, patterns, and repository-native artifacts, `contextual` for practitioner analysis and curated lists, and `unverified` only when the latest source audit cannot validate availability.

Regenerate all three generated discovery files after changing resource entries or refreshing the source audit:

```sh
python3 scripts/export_resource_dataset.py
```

The export is deterministic and includes one row for every README bullet that follows the repository's curated entry format: marker, resource type, title, link, annotation, section, and source line.

Run a network-backed source audit when refreshing the Hugging Face dataset:

```sh
python3 scripts/audit_resource_sources.py --timeout 20 --workers 16 --attempts 2 --github-cli
```

The audit file is a snapshot. HTTP status, redirects, page titles, publication metadata, and GitHub statistics can change over time. arXiv bibliographic fields come from the primary arXiv API; GitHub dates come from the repository API; other web metadata comes from citation or Open Graph tags when available. A blank publication date means the primary source did not expose one. Rows marked `restricted` returned an access-control or rate-limit status during retrieval; they are tracked separately from broken or unreachable links.
