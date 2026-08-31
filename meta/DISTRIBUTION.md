# Distribution And Discovery Checklist

Use this checklist after major updates or releases. Optimize for qualified discovery, accurate claims, and useful follow-through.

## Current Launch Status

Status as of 2026-07-20:

| Surface | Status | Evidence / next action |
| --- | --- | --- |
| GitHub release | Complete | [`v0.9.0`](https://github.com/ChaoYue0307/awesome-loop-engineering/releases/tag/v0.9.0) packages 989 resources, 22 patterns and contracts, 8 runtime starters, and explicit model-to-operations scope facets. |
| Release announcement | Ready | Publish the v0.9.0 summary from [`posts/launch.md`](../posts/launch.md); [Discussion #9](https://github.com/ChaoYue0307/awesome-loop-engineering/discussions/9) is the low-noise release and contributor feed. |
| GitHub Explore topic | Complete | [`github/explore#5209`](https://github.com/github/explore/pull/5209) merged the `loop-engineering` topic page. |
| Canonical Awesome directory | Policy objection | [`sindresorhus/awesome#4339`](https://github.com/sindresorhus/awesome/pull/4339) is open and lint passes, but the owner stated that AI-generated lists are not accepted. Do not treat further visual polish as a path around that policy or misrepresent automated assistance. |
| Adjacent harness directory | In review | [`ai-boost/awesome-harness-engineering#131`](https://github.com/ai-boost/awesome-harness-engineering/pull/131) transparently proposes the project for the list's Related Awesome Lists section. |
| Hugging Face dataset | Complete | [`datasets/cy0307/awesome-loop-engineering`](https://huggingface.co/datasets/cy0307/awesome-loop-engineering) carries the structured resource sheet and full project mirror. |
| English and Chinese launch articles | Ready | Publish [`posts/launch.md`](../posts/launch.md) and [`posts/launch.zh-CN.md`](../posts/launch.zh-CN.md) natively on suitable channels. |
| Profile pin and social posting | Owner action | Pin the repository, then publish from identity-bound LinkedIn, X, Hacker News, and Chinese-language accounts. |

## Indexing Basics

- Confirm the repository is public.
- Confirm GitHub Pages is enabled and points to `docs/` on `main`.
- Confirm the Pages homepage is set as the repository website.
- Confirm `docs/sitemap.xml` and `docs/robots.txt` are reachable.
- Share the GitHub repository URL and Pages URL from public pages that search engines can crawl.

Search engines may still take days or longer to index a new repository. Backlinks and real activity help discovery.

## Hugging Face Dataset Mirror

The Hugging Face dataset [`datasets/cy0307/awesome-loop-engineering`](https://huggingface.co/datasets/cy0307/awesome-loop-engineering) exposes the collection to AI/ML users and tabular workflows. Sync it after each GitHub release or data change.

- The mirror tracks the full GitHub tree (docs, patterns, examples, schema, scripts).
- The dataset mirror includes generated resource sheets at `data/resources.csv` and `data/resources.jsonl`, refreshed from the full English `README.md` by `scripts/export_resource_dataset.py`.
- The HF copy of `README.md` is a focused dataset card generated from `meta/hf_card_header.yaml` and `meta/hf_card_body.md` by `scripts/build_hf_card.py`. It documents intended uses, evidence fields, limitations, loading examples, and the latest link status without duplicating the 989-row GitHub README.
- The YAML header is **HF-only**: it must never be added to the GitHub `README.md`, because the metadata list items break `awesome-lint`.
- Sync uses `python3 scripts/build_hf_card.py --output <staging>/README.md` followed by `hf upload --type dataset` against a staging copy. The token lives in the local Hugging Face cache; no token is committed.
- **Upload from a clean checkout, and exclude local artifacts.** `hf upload` mirrors the working directory as it is on disk, so a sync run from a working copy that holds untracked build or QA output publishes that output too, and later syncs never remove it because the CLI does not delete. A July 2026 sync pushed 79 browser-automation files (`.playwright-cli/` console logs and element captures, `output/playwright/` screenshots) that were never part of the GitHub tree; they were removed with `hf repos delete-files`. Sync from a fresh clone, and pass `--exclude ".playwright-cli/*" --exclude "output/*"` alongside the existing exclusions.
- **Always pass `--exclude "README.md"` to the full-tree upload.** The GitHub `README.md` carries no YAML header, so uploading it to the dataset repository overwrites the card and removes the `configs` block. The dataset is then briefly configured with no explicit data file while `data/resources.csv`, `data/resources.jsonl`, and `data/resources.parquet` all sit in `data/`, which queues a dataset-viewer job that cannot resolve a split and leaves the viewer stuck on "should be available soon" even after the card is restored. Upload the generated card and `data/resources.parquet` in the same pass so the repository never holds a card and a shard that disagree.

## GitHub-Native Promotion

Use GitHub-native discovery in this order.

- **Topic page (`github/explore`).** The [`loop-engineering` topic](https://github.com/topics/loop-engineering) now has a curated page through merged PR [`github/explore#5209`](https://github.com/github/explore/pull/5209). Keep the topic description ecosystem-wide rather than repository-specific.
- **sindresorhus/awesome submission.** The open PR at [`sindresorhus/awesome#4339`](https://github.com/sindresorhus/awesome/pull/4339) has a passing lint check and an explicit owner policy objection to AI-generated lists. Keep the curation process transparent and wait for maintainer clarification; do not present the PR as ordinary pending review. See [`AWESOME_SUBMISSION.md`](AWESOME_SUBMISSION.md).
- **Editorial submissions to adjacent lists** this repo already cites (harness, context, and agent-paper lists). Submit only where the maintainers explicitly accept related resources. Ready-to-paste entry:

  ```md
  - [Awesome Loop Engineering](https://github.com/ChaoYue0307/awesome-loop-engineering#readme) - Practical resources, reusable patterns, adaptable contracts, and runtime starters for recurring AI-agent systems.
  ```

- **Pin the repository** on your profile, and add it to your profile README (profile-level promotion).
- **About description.** Keep this concise value statement aligned with the README and project site: `🔁 Build reliable recurring AI-agent systems: 989 resources, 22 operational patterns, 22 loop contracts, 8 runtime starters, an interactive atlas, and a structured dataset.`
- **Custom social preview** (repo Settings, Social preview) so shared links lead with the same four durable proof points. This is UI-only; it cannot be set through the API.
- **Releases and Discussions** provide a lower-noise subscription path. Recommend `Watch -> Custom -> Releases and Discussions`; do not ask readers to watch every repository event.

Do not use reciprocal-star requests, broad promotional pull requests, or unrelated issue comments. Every directory or newsletter submission should satisfy its normal editorial policy on its own merits.

## Measurement Baseline

GitHub retains repository traffic details for only 14 days. Record a snapshot weekly, using the same definitions each time.

Snapshot captured on 2026-07-20 for the API window ending 2026-07-19:

| Metric | Baseline |
| --- | ---: |
| Repository views | 637 |
| Unique visitors | 157 |
| Clones | 720 |
| Unique cloners | 199 |
| Stars | 35 |
| Forks | 7 |
| Watchers | 1 |

The repository overview reached 126 unique visitors. The Chinese README remained the second-most visited content path with 20 unique visitors. The largest identifiable referrers were GitHub and Google (22 unique visitors each), Bing (11), and the project site (8); X contributed two identifiable visitors. Clone traffic remains unusually high and may include automated clients, so do not treat clone counts as human adoption without corroborating forks or contributions.

Since the previous snapshot, stars increased from 31 to 35 and forks from 6 to 7 while watchers remained at 1. Qualified discovery is improving, but release and discussion subscriptions remain the clearest gap; the next campaign should keep prioritizing useful external reach and the low-noise release/digest path.

Working 30-day campaign targets:

- 1,000-1,500 unique visitors;
- 75-100 total stars;
- 8-12 forks;
- 5-8 watchers;
- at least 5 external contributors.

Treat these as measurement targets, not promises. Log the publication date and canonical URL for each channel, then compare referral traffic and qualified contributions rather than optimizing for raw impressions.

## Launch Copy

Use the [English launch article](../posts/launch.md) or [Chinese launch article](../posts/launch.zh-CN.md) for long-form distribution.

### Short Post

```text
🔁 Awesome Loop Engineering maps how recurring AI agents should act, verify, remember, retry, and stop.

989 resources · 22 patterns · 22 contracts · 8 starters

Explore and build:
https://github.com/ChaoYue0307/awesome-loop-engineering

#AIAgents #AgentEngineering
```

Attach [`assets/social-preview.png`](../assets/social-preview.png) directly when the platform permits it. The post is 264 characters before platform-specific URL shortening.

For a fresh link card on X or LinkedIn, share <https://chaoyue0307.github.io/awesome-loop-engineering/x-v10-989.html>. The versioned URL points to the current preview image, records the `v0.10.0` campaign, and redirects readers to the interactive site.

### Chinese Short Post

```text
🔁 Awesome Loop Engineering 把反复运行的 AI 智能体变成可设计、可验证、可停止的工程系统。

669 个资源 · 20 个运行模式 · 20 份循环契约 · 8 个启动模板

浏览并开始构建：
https://github.com/ChaoYue0307/awesome-loop-engineering

#AIAgents #智能体工程
```

### Longer Post

```text
Awesome Loop Engineering v0.9.0 is live.

"Loop" can mean recurrent computation inside a model, reasoning and tools inside one task, or verified work repeated across time. v0.9.0 maps all three without confusing their guarantees.

The release includes:

- 989 papers, docs, tools, benchmarks, and guides
- 29 model-layer resources, including Loopie, labeled as adjacent foundations
- an interactive Resource Atlas
- 22 operational patterns and 22 adaptable loop contracts
- 8 runtime starters: 3 executables and 5 copy/paste templates
- 50-field CSV, JSONL, and Parquet exports mirrored to Hugging Face
- source and evidence fields, with point-in-time link-check results

Explore, reuse, or correct the map:
https://github.com/ChaoYue0307/awesome-loop-engineering
```

### Hacker News

Use a regular submission, not Show HN.

```text
Title: Awesome Loop Engineering: 989 resources from looped models to agent operations

I have been mapping recurring AI-agent systems: how work enters, agents act, evidence gates results, state survives, and the system retries, escalates, or exits.

The repository connects 989 papers, docs, tools, benchmarks, and guides across model, agent, harness, workflow, operations, and evaluation layers with 22 operational patterns, 22 adaptable contracts, 8 runtime starters, an interactive Resource Atlas, and a structured Hugging Face dataset. Model-level recurrence is labeled as an adjacent foundation rather than a complete operational loop. Corrections to source links, taxonomy, and summaries are especially welcome.

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

- X/Twitter thread with the cover image and working definition.
- LinkedIn post focused on the prompt/context/harness/loop stack.
- Hacker News or Reddit only if framed as a useful field guide, not a launch announcement.
- Relevant GitHub issues or discussions where Loop Engineering, coding agents, or agent workflows are already being discussed.
- Authors and maintainers cited in the repo, asking for corrections or better original source links.
- The repository's own Discussions, using [`DISCUSSIONS.md`](DISCUSSIONS.md) for starter prompts and scope guidance.

## Outreach Targets

Use [`OUTREACH.md`](OUTREACH.md) for wording.

- Direct Loop Engineering article authors.
- Agent runtime maintainers with scheduling, goals, hooks, worktrees, skills, plugins, or subagents.
- Benchmark maintainers for long-horizon coding agents.
- Builders who can contribute real PR babysitting, CI repair, docs drift, deploy verification, benchmark optimization, knowledge freshness, or feedback clustering loops.

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
- Describe what readers can explore, compare, or build instead of claiming authority or completeness.
- Keep all claims linked to public, inspectable sources.
