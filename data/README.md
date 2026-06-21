# Dataset Exports

This directory contains generated tabular exports of the canonical English `README.md` resource list.

- `resources.csv` - Primary sheet for the Hugging Face Dataset Viewer.
- `resources.jsonl` - Equivalent JSON Lines export for scripts and data tooling.
- `resource_source_audit.csv` - Retrieval-time audit of every row, including URL status, source title metadata, arXiv IDs, and GitHub repository stats where available.

Regenerate both files after changing resource entries:

```sh
python3 scripts/export_resource_dataset.py
```

The export is deterministic and includes one row for every README bullet that follows the repository's curated entry format: marker, resource type, title, link, annotation, section, and source line.

Run a network-backed source audit when refreshing the Hugging Face dataset:

```sh
python3 scripts/audit_resource_sources.py --timeout 20 --workers 16 --attempts 2 --github-cli
```

The audit file is a snapshot. HTTP status, redirects, page titles, and GitHub stars/forks can change over time. Rows marked `restricted` returned an access-control or rate-limit status during retrieval; they are tracked separately from broken or unreachable links.
