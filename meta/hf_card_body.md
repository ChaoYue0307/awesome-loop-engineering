<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="assets/awesome-loop-engineering-logo.png" alt="Visit the Awesome Loop Engineering website" width="128"></a>
</p>

<h1 align="center">Awesome Loop Engineering Dataset</h1>

<p align="center">
  A source-audited dataset of {{RESOURCE_COUNT}} papers, official docs, tools, benchmarks, patterns, critiques, and implementation guides for recurring AI-agent systems.
</p>

<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">Resource Atlas</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering">GitHub field guide</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/meta/CURATION.md">Curation standard</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml">Report a correction</a>
</p>

## Dataset Summary

Each row pairs one source with a concise editorial assessment, bibliographic metadata, lifecycle and audience facets, evidence classification, audit status, and point-in-time repository statistics when applicable.

Current release: **v{{VERSION}}**

| Surface | Count |
| --- | ---: |
| Source-audited resources | {{RESOURCE_COUNT}} |
| Operational patterns | {{PATTERN_COUNT}} |
| Validated loop contracts | {{CONTRACT_COUNT}} |
| Runtime starters | {{RUNNABLE_COUNT}} |

The source audit dated **{{AUDIT_DATE}}** reports these row statuses: **{{REACHABLE_COUNT}} reachable public**, **{{RESTRICTED_COUNT}} access restricted**, **{{LOCAL_COUNT}} repository-native**, and **{{BROKEN_COUNT}} broken or unreachable**.

## What A Loop Contract Is

A **Loop Contract** is a reviewable operating specification for one recurring agent job. It fixes what authorizes a run, which work and actions are allowed, what context and roles the run uses, which external evidence proves progress, what state survives, how much the loop may spend, and when a human takes over or the loop exits.

Recurring agents need this policy because schedules, events, queues, and goals remove live supervision. Without explicit boundaries, missing decisions become hidden defaults: the loop can select the wrong work, widen its own scope, approve itself, forget failed attempts, or retry without a stopping rule. Start with the [JSON schema](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/schemas/loop-contract.schema.json) and adapt one of the [{{CONTRACT_COUNT}} validated examples](https://github.com/ChaoYue0307/awesome-loop-engineering/tree/main/examples).

## Loop Maturity Model

The maturity model helps teams choose the smallest operating model that can perform one recurring job reliably. Levels describe how a workflow is triggered, remembered, verified, divided, and supervised; they do not score model intelligence or product quality.

| Level | Added capability | Example |
| --- | --- | --- |
| 0 · Manual prompting | A person holds state and judges each next action. | One supervised test repair. |
| 1 · Scripted retry | A bounded wrapper returns external failure to one agent. | Three `pytest` repair attempts. |
| 2 · Scheduled loop | A schedule or event starts bounded intake and reporting. | Nightly docs-drift scan. |
| 3 · Stateful loop | Checkpoints and receipts survive across runs. | Feedback clustering with processed IDs. |
| 4 · Self-verifying loop | External checks or independent evaluation gate completion. | CI repair exits only when the original check passes. |
| 5 · Multi-agent loop | Specialists use explicit handoffs and shared state. | Explorer, reproducer, and reviewer for security findings. |
| 6 · Production-supervised loop | Telemetry, least privilege, budgets, approvals, rollback, and escalation govern production work. | Deploy verification with threshold-based pause and human rollback approval. |

Move up only when the current level cannot meet a recurring continuity, evidence, or risk requirement. Durable state should precede longer unattended runs, external verification should precede more agents, and production controls should precede production impact. The [full field guide](https://github.com/ChaoYue0307/awesome-loop-engineering#loop-maturity-model) explains why each level exists and the signal for advancing.

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

- Find primary sources and implementation references for recurring agent systems.
- Compare works by lifecycle, audience, evidence class, source type, and publication metadata.
- Build literature maps, reading lists, dashboards, or retrieval indexes.
- Audit contribution, novelty, impact, provenance, and evidence claims.
- Find reusable patterns, contracts, schemas, executable examples, and copy/paste runtime templates.

Do not use `signal_strength`, GitHub stars, forks, or inclusion in this collection as a quality label, endorsement, or automated ranking of scientific validity.

## Future Directions

The agenda organizes fifteen measurable workstreams in dependency order:

| Tier | Prove next | First artifacts |
| --- | --- | --- |
| Foundation | Verification, state, recovery, receipts, and security remain trustworthy under failure | Challenge sets, fault injection, replay, receipt schemas, and enforced permissions |
| Scale | Gains survive ablation, long horizons, matched budgets, runtime changes, and cost accounting | Factorized benchmarks, control-policy replays, contract adapters, and economic frontiers |
| Adoption | Operators can deploy, understand, interrupt, hand off, update, and retire a useful loop | Domain pilots, promotion gates, handoff studies, incident drills, and lifecycle controls |

The complete [Future Directions agenda](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/FUTURE-DIRECTIONS.md) provides a shared evaluation protocol, operational metric definitions, starter slices and completion gates for every workstream, 90-day role plans, field milestones, and a proposal template.

## Dataset Structure

The primary configuration is `resources`, with one `train` split backed by the native `data/resources.parquet` shard. `data/resources.jsonl` and `data/resources.csv` contain the same rows for streaming, spreadsheet, and dataframe workflows.

| Field group | Fields | What it describes |
| --- | --- | --- |
| Identity | `row_id`, `title`, `url`, `canonical_url`, `resource_type`, `domain` | What the resource is and where it lives. |
| Editorial assessment | `annotation`, `key_contribution`, `novelty`, `impact` | What the resource contributes to recurring agent systems. |
| Navigation | `section`, `collection`, `user_goal`, `lifecycle_stages`, `audience` | Where the resource fits and who it serves. |
| Evidence | `evidence_class`, `evidence_tier`, `signal`, `signal_strength`, `source_status`, `audited_at` | What kind of evidence or provenance is available. |
| Publication | `authors`, `publication_date`, `publication_year`, `publication_venue`, `publisher`, `doi`, `arxiv_id`, `primary_category` | Bibliographic data exposed by the canonical source. |
| Source provenance | `source_title`, `source_description`, `metadata_source`, `publication_note` | Where metadata came from and what caveats accompany it. |
| Repository context | `github_repo`, `github_stars`, `github_forks`, `github_license`, `github_created_at`, `github_updated_at` | Point-in-time adoption and maintenance context for GitHub projects. |
| Export trace | `source_readme`, `source_line`, `source_url`, `date_added` | How the row maps back to the canonical field guide. |

The complete field-by-field schema is documented in [`data/README.md`](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/data/README.md).

## Curation And Provenance

Start with primary papers, official documentation, project repositories, and implementation-heavy practitioner sources. Every released row must pass the public [curation standard](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/meta/CURATION.md).

Annotations are original syntheses, not copied abstracts or claims of author endorsement. Automation may assist discovery, URL resolution, duplicate detection, bibliographic extraction, repository statistics, and draft normalization. The canonical source remains the evidence; the maintainer owns each released inclusion decision and annotation.

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

GitHub Releases define versioned snapshots; cite a release or commit for reproducibility. Submit corrections to summaries, contribution, novelty, impact, authorship, dates, venues, identifiers, or canonical URLs through the [correction form](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml).

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
