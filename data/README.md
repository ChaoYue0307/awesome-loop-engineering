# Dataset Exports

Download deterministic tabular exports of all 555 source-audited resources.

- `resources.csv` - Tabular export for spreadsheets and ad hoc analysis.
- `resources.jsonl` - JSON Lines export and source for the Hugging Face Parquet build.
- `resources.parquet` - Native Parquet shard generated in the Hugging Face release snapshot; it powers the Dataset Viewer without relying on server-side conversion.
- `../docs/assets/resources.json` - Slim generated payload used by the website's searchable Resource Atlas.
- `first_seen.json` - Forward-only sidecar mapping resource URL to the date it was first added; the export left-joins it into the `date_added` column. Empty `date_added` means the entry predates per-entry tracking (started 2026-07-15).
- `resource_source_audit.csv` - Retrieval-time audit of every row, including URL status, source title metadata, arXiv IDs, and GitHub repository stats where available.
- `arxiv_publication_overrides.csv` - Human-verified conference, journal, and workshop records backed by official proceedings, DOI registries, OpenReview, or current author-supplied acceptance notes.
- `arxiv_publication_audit.csv` - Complete decision table for every arXiv-linked resource: published, accepted, or preprint-only.

The exports preserve each section and annotation while adding three discovery layers:

- **Task facets**: `collection`, `user_goal`, `lifecycle_stages`, and `audience` answer why a reader needs the source and where it fits in the Loop Contract.
- **Evidence facets**: `evidence_class`, `evidence_tier`, `signal_strength`, `source_status`, canonical URL, source metadata, GitHub statistics, arXiv ID, and audit timestamp separate source provenance from popularity or editorial judgment.
- **Publication facets**: `authors`, `publication_date`, `publication_year`, `publication_venue`, `publisher`, `doi`, `publication_note`, `primary_category`, and `metadata_source` provide a paper-like bibliographic row without inventing missing facts.

`key_contribution`, `novelty`, and `impact` are resource-specific. `evidence_tier` follows the public A-C source hierarchy: A for primary or official artifacts, B for implementation-grounded practice and risk analysis, and C for curated synthesis. `signal` states the evidence basis and limits; GitHub stars and forks provide point-in-time context, never proof of reliability. `signal_strength` is `high` for primary official documentation and benchmarks, `medium` for inspectable implementations, papers, patterns, and locally maintained artifacts, `contextual` for practitioner analysis and curated lists, and `unverified` only when the latest audit cannot validate availability.

## Load And Query

```python
from datasets import load_dataset

resources = load_dataset(
    "cy0307/awesome-loop-engineering",
    "resources",
    split="train",
)

verification_papers = resources.filter(
    lambda row: row["resource_type"] == "Paper"
    and "verification" in row["lifecycle_stages"].split(";")
)
```

For pandas:

```python
import pandas as pd

resources = pd.read_csv("data/resources.csv")
current_sources = resources[resources["source_status"].isin(["ok", "local_ok"])]
```

Use `url` as the durable join key. `row_id` and `source_line` are positional and may change when the README is reordered.

## Reproducibility

Render the README rows first, then regenerate all three discovery files after changing resource entries or refreshing the source audit:

```sh
python3 scripts/render_readme_tables.py
python3 scripts/export_resource_dataset.py
python3 scripts/resolve_arxiv_publications.py --check
python3 scripts/check_project_consistency.py
python3 scripts/build_hf_card.py --check
```

Every README resource-table row becomes one deterministic export row with its marker, resource type, title, link, original publishing platform or venue, annotation, section, and source line.

Run a network-backed source audit when refreshing the Hugging Face dataset:

```sh
python3 scripts/audit_resource_sources.py --timeout 20 --workers 16 --attempts 2 --github-cli
```

The audit file is a snapshot. HTTP status, redirects, page titles, publication metadata, and GitHub statistics can change over time. arXiv bibliographic fields come from the primary arXiv API, while verified conference or journal records take precedence for venue, publisher, DOI, and canonical URL. The arXiv ID and original preprint link remain available for provenance and access. GitHub dates come from the repository API; other web metadata comes from citation or Open Graph tags when available. A blank publication date means the primary source did not expose one. Rows marked `restricted` returned an access-control or rate-limit status during retrieval; they are tracked separately from broken or unreachable links.

Refresh publication decisions before applying them to a current source audit:

```sh
python3 scripts/resolve_arxiv_publications.py --refresh --cache-dir /tmp/ale-publication-cache
python3 scripts/audit_resource_sources.py --apply-publication-overlay-only
python3 scripts/render_readme_tables.py
python3 scripts/export_resource_dataset.py
```

Exact-title DBLP and Crossref matches may add new published versions automatically. Ambiguous records remain preprint-only until a primary publication record or an author-supplied acceptance note can be verified and added to `arxiv_publication_overrides.csv`.

Build the focused Hugging Face dataset card for a staging mirror with:

```sh
python3 scripts/build_hf_card.py --output /tmp/awesome-loop-engineering-hf/README.md
python3 scripts/build_hf_parquet.py --output /tmp/awesome-loop-engineering-hf/data/resources.parquet
```

The card is generated from `meta/hf_card_header.yaml`, `meta/hf_card_body.md`, the current dataset, and `CITATION.cff`. The Parquet shard is a lossless derivative of `data/resources.jsonl` and requires `pyarrow`. The YAML front matter is intentionally Hugging Face-only and must not be added to the GitHub README.
