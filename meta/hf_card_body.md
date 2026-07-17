<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="assets/awesome-loop-engineering-logo.png" alt="Visit the Awesome Loop Engineering website" width="128"></a>
</p>

<h1 align="center">Awesome Loop Engineering Dataset</h1>

<p align="center">
  A source-audited sheet of {{RESOURCE_COUNT}} papers, official docs, tools, benchmarks, patterns, critiques, and implementation guides for recurring AI-agent systems.
</p>

<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">Resource Atlas</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering">GitHub field guide</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/meta/CURATION.md">Curation standard</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml">Report a correction</a>
</p>

## Dataset Summary

Each row represents one resource from the canonical English field guide. The export combines the maintainer's short assessment with source-level bibliographic metadata, lifecycle and audience facets, evidence classification, audit status, and current repository statistics when applicable.

Current release: **v{{VERSION}}**

| Surface | Count |
| --- | ---: |
| Curated resources | {{RESOURCE_COUNT}} |
| Operational patterns | {{PATTERN_COUNT}} |
| Validated loop contracts | {{CONTRACT_COUNT}} |
| Runnable templates | {{RUNNABLE_COUNT}} |

The source audit dated **{{AUDIT_DATE}}** found {{REACHABLE_COUNT}} reachable public sources, {{RESTRICTED_COUNT}} access-restricted sources, {{LOCAL_COUNT}} repository-native artifacts, and {{BROKEN_COUNT}} broken or unreachable sources.

## Load The Data

```python
from datasets import load_dataset

resources = load_dataset(
    "cy0307/awesome-loop-engineering",
    "resources",
    split="train",
)

papers = resources.filter(lambda row: row["resource_type"] == "Paper")
verification = resources.filter(
    lambda row: "verification" in row["lifecycle_stages"].split(";")
)
```

For pandas:

```python
import pandas as pd

resources = pd.read_csv(
    "https://huggingface.co/datasets/cy0307/awesome-loop-engineering/resolve/main/data/resources.csv"
)
```

Use `url` as the durable join key. `row_id` and `source_line` are positional and can change when the README is reordered.

## Intended Uses

- discover primary sources and implementation references for recurring agent systems;
- compare resources by lifecycle stage, audience, evidence class, source type, and publication metadata;
- build literature maps, reading lists, dashboards, or retrieval indexes;
- audit how a public field guide characterizes contribution, novelty, impact, and evidence;
- find reusable patterns, contracts, schemas, and runnable examples.

Do not use `signal_strength`, GitHub stars, forks, or inclusion in this collection as a quality label, endorsement, or automated ranking of scientific validity.

## Dataset Structure

The primary configuration is `resources`, with one `train` split backed by `data/resources.jsonl`. `data/resources.csv` contains the same rows for spreadsheet and dataframe workflows.

| Field group | Fields | What it describes |
| --- | --- | --- |
| Identity | `row_id`, `title`, `url`, `canonical_url`, `resource_type`, `domain` | What the resource is and where it lives. |
| Editorial assessment | `annotation`, `key_contribution`, `novelty`, `impact` | Why the resource matters in this collection. |
| Navigation | `section`, `collection`, `user_goal`, `lifecycle_stages`, `audience` | Where the resource fits and who it serves. |
| Evidence | `evidence_class`, `signal`, `signal_strength`, `source_status`, `audited_at` | What kind of evidence or provenance is available. |
| Publication | `authors`, `publication_date`, `publication_year`, `publication_venue`, `publisher`, `doi`, `arxiv_id`, `primary_category` | Bibliographic data exposed by the canonical source. |
| Source provenance | `source_title`, `source_description`, `metadata_source`, `publication_note` | Where metadata came from and what caveats accompany it. |
| Repository context | `github_repo`, `github_stars`, `github_forks`, `github_license`, `github_created_at`, `github_updated_at` | Point-in-time adoption and maintenance context for GitHub projects. |
| Export trace | `source_readme`, `source_line`, `source_url`, `date_added` | How the row maps back to the canonical field guide. |

The complete field-by-field schema is documented in [`data/README.md`](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/data/README.md).

## Curation And Provenance

The collection prioritizes primary papers, official documentation, project repositories, and implementation-heavy practitioner sources. Every released row must pass the public [curation standard](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/meta/CURATION.md).

Annotations are original repository syntheses, not copied abstracts and not claims of author endorsement. Automation may assist discovery, URL resolution, duplicate detection, bibliographic extraction, repository statistics, and draft normalization. The canonical source remains the evidence, and the maintainer is accountable for the released inclusion decision and text.

The full point-in-time audit is available as [`data/resource_source_audit.csv`](https://huggingface.co/datasets/cy0307/awesome-loop-engineering/blob/main/data/resource_source_audit.csv).

## Limitations

- The collection is maintained by one person and reflects editorial judgment despite a public acceptance standard.
- Coverage is skewed toward English-language, publicly available material.
- A successful URL check proves reachability at audit time, not correctness, permanence, or independent validation.
- Access-restricted rows could not be fully retrieved during the latest audit and should be checked manually.
- Publication dates and authors remain blank when the primary source does not expose reliable metadata.
- Resource statistics are snapshots and will drift after the recorded `audited_at` timestamp.
- Linked third-party works retain their own licenses and terms; CC0-1.0 covers only original repository curation, metadata, templates, and documentation.

## Versioning And Corrections

GitHub Releases define versioned snapshots. Cite a release or commit when reproducibility matters. Accuracy corrections to summaries, contribution, novelty, impact, author, date, venue, identifier, or canonical URL are accepted through the [correction form](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml).

## Citation

```bibtex
@misc{chaoyue2026awesome_loop_engineering,
  author       = {He, Chaoyue},
  title        = {Awesome Loop Engineering},
  year         = {2026},
  howpublished = {\url{https://github.com/ChaoYue0307/awesome-loop-engineering}},
  note         = {Version {{VERSION}}}
}
```
