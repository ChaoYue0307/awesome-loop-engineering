# Dataset Exports

This directory contains generated tabular exports of the canonical English `README.md` resource list.

- `resources.csv` - Primary sheet for the Hugging Face Dataset Viewer.
- `resources.jsonl` - Equivalent JSON Lines export for scripts and data tooling.

Regenerate both files after changing resource entries:

```sh
python3 scripts/export_resource_dataset.py
```

The export is deterministic and includes one row for every README bullet that follows the repository's curated entry format: marker, resource type, title, link, annotation, section, and source line.
