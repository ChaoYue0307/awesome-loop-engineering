# Distribution And Discovery Checklist

Use this checklist after major updates or releases. The goal is accurate discovery, not hype.

## Indexing Basics

- Confirm the repository is public.
- Confirm GitHub Pages is enabled and points to `docs/` on `main`.
- Confirm the Pages homepage is set as the repository website.
- Confirm `docs/sitemap.xml` and `docs/robots.txt` are reachable.
- Share the GitHub repository URL and Pages URL from public pages that search engines can crawl.

Search engines may still take days or longer to index a new repository. Backlinks and real activity help discovery.

## Hugging Face Dataset Mirror

The repository is mirrored to the Hugging Face Hub dataset repo [`datasets/cy0307/awesome-loop-engineering`](https://huggingface.co/datasets/cy0307/awesome-loop-engineering) for discovery within the AI/ML community. The daily maintenance routine syncs it after each GitHub push.

- The mirror tracks the full GitHub tree (docs, patterns, examples, schema, scripts).
- The dataset mirror includes generated resource sheets at `data/resources.csv` and `data/resources.jsonl`, refreshed from the canonical English `README.md` by `scripts/export_resource_dataset.py`.
- The HF copy of `README.md` carries a dataset-card YAML header (`license`, `language`, `size_categories`, `task_categories`, `tags`, `pretty_name`, and `configs`); the canonical header lives in meta/hf_card_header.yaml. This header is **HF-only**: it must never be added to the GitHub `README.md`, because the YAML list items break `awesome-lint`.
- Sync uses the `hf upload --type dataset` CLI against a staging copy with the header prepended, so the GitHub working tree stays header-free. The token lives in the local Hugging Face cache; no token is committed.

## GitHub-Native Promotion

Discoverability levers that live on GitHub itself, in priority order.

- **Topic page (`github/explore`).** There is no curated page for the [`loop-engineering` topic](https://github.com/topics/loop-engineering) yet. A page is prepared on the fork branch `ChaoYue0307:add-loop-engineering-topic` (file `topics/loop-engineering/index.md`); open a PR from that branch to `github/explore`. This describes the topic, not this repo specifically, so it promotes the concept and helps the whole ecosystem.
- **sindresorhus/awesome submission.** The canonical awesome-list promotion; opens after the 30-day age rule (~2026-07-09). Use [`AWESOME_SUBMISSION.md`](AWESOME_SUBMISSION.md).
- **Reciprocal entries on adjacent lists** this repo already cites (harness, context, agent-papers lists). Ready-to-paste entry:

  ```md
  - [Awesome Loop Engineering](https://github.com/ChaoYue0307/awesome-loop-engineering#readme) - Recurring AI/coding-agent systems above prompt, context, and harness engineering: patterns, contracts, runnable loops, and curated resources.
  ```

- **Pin the repository** on your profile, and add it to your profile README (profile-level promotion).
- **Custom social preview** (repo Settings, Social preview) so shared links render with the cover image. This is UI-only; it cannot be set through the API.
- **Releases** notify watchers and appear on the repo; the latest is the cleanest moment to share.

## Launch Copy

Use the canonical [English launch article](../posts/launch.md) or [Chinese launch article](../posts/launch.zh-CN.md) for long-form distribution.

### Short Post

```text
Awesome Loop Engineering v0.5.0 is live.

509 audited resources for designing recurring AI-agent systems above prompt, context, and harness engineering, plus an interactive Resource Atlas, 15 patterns, 15 validated loop contracts, runnable templates, and a structured Hugging Face dataset.

Explore the atlas:
https://chaoyue0307.github.io/awesome-loop-engineering/
```

### Longer Post

```text
Awesome Loop Engineering v0.5.0 is live.

Loop Engineering is the operating layer above prompt, context, and harness engineering: the recurring system that discovers work, delegates it, verifies results, persists state, and decides what happens next.

The release includes:

- 509 audited resources
- an interactive Resource Atlas
- 15 operational patterns and 15 validated loop contracts
- 6 runnable templates
- CSV and JSONL exports mirrored to Hugging Face

Explore, reuse, or correct the map:
https://github.com/ChaoYue0307/awesome-loop-engineering
```

### Hacker News

Use a regular submission, not Show HN.

```text
Title: Awesome Loop Engineering: 509 resources for recurring AI-agent systems

I have been mapping the layer above prompt, context, and harness engineering: recurring systems that discover work, delegate it, verify results, persist state, and decide whether to retry, escalate, or exit.

The repository now includes 509 audited sources, 15 operational patterns, validated loop contracts, runnable templates, an interactive Resource Atlas, and a structured Hugging Face dataset. Corrections to the taxonomy and source annotations are especially welcome.

https://github.com/ChaoYue0307/awesome-loop-engineering
```

Do not ask anyone to upvote the submission.

## Coordinated Release Sequence

1. Publish the GitHub release and confirm Pages, dataset, and CI are current.
1. Publish the English article and a concise LinkedIn or X post using the stack or lifecycle visual.
1. Publish the native Chinese article rather than translating a social post mechanically.
1. Submit the regular Hacker News post after the release page is stable.
1. Contact cited authors with accuracy requests, then approach adjacent list maintainers and newsletters.
1. Record each channel and its referral result in the 14-day traffic snapshot.

## Where To Share

- X/Twitter thread with the cover image and canonical definition.
- LinkedIn post focused on the prompt/context/harness/loop stack.
- Hacker News or Reddit only if framed as a useful field guide, not a launch announcement.
- Relevant GitHub issues or discussions where Loop Engineering, coding agents, or agent workflows are already being discussed.
- Authors and maintainers cited in the repo, asking for corrections or stronger canonical links.
- The repository's own Discussions, using [`DISCUSSIONS.md`](DISCUSSIONS.md) for starter prompts and scope guidance.

## Outreach Targets

Use [`OUTREACH.md`](OUTREACH.md) for wording.

- Direct Loop Engineering article authors.
- Agent runtime maintainers with scheduling, goals, hooks, worktrees, skills, plugins, or subagents.
- Benchmark maintainers for long-horizon coding agents.
- Builders who can contribute real PR babysitting, CI repair, docs drift, deploy verification, or feedback clustering loops.

## Awesome List Submission

Use [`AWESOME_SUBMISSION.md`](AWESOME_SUBMISSION.md) for the upstream checklist, timing rule, suggested entry, and PR body.

Before submitting to any awesome list:

1. Verify all links pass.
1. Confirm the README has a narrow scope and contribution guidelines.
1. Confirm the license is visible and correct.
1. Confirm the repo has a release and working CI.
1. Submit only where the maintainers accept related awesome-list entries.

Candidate places:

- [sindresorhus/awesome](https://github.com/sindresorhus/awesome)
- adjacent prompt, context, harness, and agent engineering lists that accept PRs for related resources

## Accuracy Rules

- Do not claim that Loop Engineering is a finished standard.
- Do not imply cited authors endorse this repository unless they explicitly do.
- Prefer "early field guide" or "curated map" over "definitive source".
- Keep all claims linked to public, inspectable sources.
