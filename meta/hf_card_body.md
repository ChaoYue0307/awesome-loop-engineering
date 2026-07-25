<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="assets/awesome-loop-engineering-logo.png" alt="Visit the Awesome Loop Engineering website" width="128"></a>
</p>

<h1 align="center">Awesome Loop Engineering Dataset</h1>

<p align="center">
  A structured dataset of {{RESOURCE_COUNT}} papers, official docs, tools, benchmarks, patterns, critiques, and implementation guides for recurring AI-agent systems.
</p>

<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering: the Prompt, Context, Harness, and Loop layers" width="100%"></a>
</p>

<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">Resource Atlas</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering">GitHub field guide</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/meta/CURATION.md">Resource selection</a> ·
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml">Report a correction</a>
</p>

<p align="center">
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering"><img src="https://img.shields.io/github/stars/ChaoYue0307/awesome-loop-engineering?style=social" alt="Star Awesome Loop Engineering on GitHub"></a>
  &nbsp;
  <a href="https://github.com/ChaoYue0307/awesome-loop-engineering/fork"><img src="https://img.shields.io/github/forks/ChaoYue0307/awesome-loop-engineering?style=social" alt="Fork Awesome Loop Engineering on GitHub"></a>
</p>

## Dataset Summary

Each row connects an original source to its contribution, novelty, impact, publication details, lifecycle stages, audience, evidence type, link status, and repository context when applicable.

This dataset is generated from the [GitHub field guide](https://github.com/ChaoYue0307/awesome-loop-engineering), which grows near-daily with source-verified additions. If it is useful to you, [starring the repo](https://github.com/ChaoYue0307/awesome-loop-engineering) is the easiest way to follow new resources and helps other builders find the collection.

Current release: **v{{VERSION}}**

| Surface | Count |
| --- | ---: |
| Resources | {{RESOURCE_COUNT}} |
| Research papers | {{PAPER_COUNT}} |
| Model-layer resources | {{MODEL_COUNT}} |
| Operational patterns | {{PATTERN_COUNT}} |
| Adaptable loop contracts | {{CONTRACT_COUNT}} |
| Runtime starters | {{RUNNABLE_COUNT}} |
| Dataset fields | {{FIELD_COUNT}} |
| Language entry points | {{LANGUAGE_COUNT}} |

At the **{{AUDIT_DATE}}** source check, **{{REACHABLE_COUNT}} public links opened successfully**, **{{RESTRICTED_COUNT}} required access**, **{{LOCAL_COUNT}} pointed to repository files**, and **{{BROKEN_COUNT}} were broken or unreachable**.

## What A Loop Contract Is

A **Loop Contract** is a reviewable operating specification for one recurring agent job. It fixes what authorizes a run, which work and actions are allowed, what context and roles the run uses, which external evidence proves progress, what state survives, how much the loop may spend, and when a human takes over or the loop exits.

Recurring agents need this policy because schedules, events, queues, and goals remove live supervision. Without explicit boundaries, missing decisions become hidden defaults: the loop can select the wrong work, widen its own scope, approve itself, forget failed attempts, or retry without a stopping rule. Start with the [JSON schema](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/schemas/loop-contract.schema.json) and adapt one of the [{{CONTRACT_COUNT}} schema-checked examples](https://github.com/ChaoYue0307/awesome-loop-engineering/tree/main/examples).

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
model_recurrence = resources.filter(
    lambda row: row["loop_layer"] == "model"
    and row["scope_fit"] == "adjacent"
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
- Separate model, agent, harness, workflow, operations, evaluation, and cross-layer resources without treating adjacent model recurrence as a complete operational loop.
- Build literature maps, reading lists, dashboards, or retrieval indexes.
- Inspect contribution, novelty, impact, source, and evidence fields before following a claim.
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
| Resource analysis | `annotation`, `key_contribution`, `novelty`, `impact` | What the resource contributes to recurring agent systems. |
| Scope | `loop_layer`, `scope_fit` | Where recurrence lives and whether the source is direct, enabling, or adjacent to operational Loop Engineering. |
| Navigation | `section`, `collection`, `user_goal`, `lifecycle_stages`, `audience` | Where the resource fits and who it serves. |
| Evidence | `evidence_class`, `evidence_tier`, `signal`, `signal_strength`, `source_status`, `audited_at` | What kind of evidence or provenance is available. |
| Publication | `authors`, `publication_date`, `publication_year`, `publication_venue`, `publisher`, `doi`, `arxiv_id`, `primary_category` | Bibliographic data exposed by the original or official source. |
| Source details | `source_title`, `source_description`, `metadata_source`, `publication_note` | Where metadata came from and what caveats accompany it. |
| Repository context | `github_repo`, `github_stars`, `github_forks`, `github_license`, `github_created_at`, `github_updated_at` | Point-in-time adoption and maintenance context for GitHub projects. |
| Export trace | `source_readme`, `source_line`, `source_url`, `date_added` | How the row maps back to the full field guide. |

The complete field-by-field schema is documented in [`data/README.md`](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/data/README.md).

## How To Read The Evidence

Open the linked work before relying on a summary. Evidence labels distinguish published research, official documentation, inspectable implementations, practitioner analysis, risk analysis, and discovery indexes; they describe the kind of source, not its scientific quality.

Summaries explain each work's contribution in original language rather than copying abstracts. They do not imply author endorsement. Follow the source link to inspect methods, results, limitations, licenses, and current documentation.

The latest link-check results are available as [`data/resource_source_audit.csv`](https://huggingface.co/datasets/cy0307/awesome-loop-engineering/blob/main/data/resource_source_audit.csv).

## Limitations

- Coverage is selective rather than exhaustive, and one person currently reviews changes.
- Coverage is skewed toward English-language, publicly available material.
- A successful URL check proves that a link opened at check time, not that its claims are correct, permanent, or independently validated.
- Access-restricted rows could not be fully retrieved during the latest check and should be opened manually.
- Publication dates and authors remain blank when the primary source does not expose reliable metadata.
- Resource statistics are snapshots and will drift after the recorded `audited_at` timestamp.
- Linked third-party works retain their own licenses and terms; CC0-1.0 covers only original repository descriptions, metadata, templates, and documentation.

## Versioning And Corrections

GitHub Releases define versioned snapshots; cite a release or commit for reproducibility. Submit corrections to summaries, contribution, novelty, impact, authorship, dates, venues, identifiers, or source URLs through the [correction form](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml).

## Follow And Support

Everything here starts life in the GitHub repository — the dataset, the atlas, the patterns, and the contracts are all generated from it.

- ⭐ [Star the repo](https://github.com/ChaoYue0307/awesome-loop-engineering) to follow near-daily verified additions and help others discover the collection.
- 🍴 [Fork it](https://github.com/ChaoYue0307/awesome-loop-engineering/fork) to adapt the {{PATTERN_COUNT}} patterns, {{CONTRACT_COUNT}} loop contracts, and {{RUNNABLE_COUNT}} runtime starters to your own stack.
- 🧭 [Suggest a resource or open a PR](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/CONTRIBUTING.md) — every submission is source-verified before it lands.
- 🤗 Liking this dataset on Hugging Face also helps other practitioners find it.

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
