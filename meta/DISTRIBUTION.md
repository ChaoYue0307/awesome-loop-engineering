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

Use [`posts/launch.md`](../posts/launch.md) when you want a longer article-style launch post.

### Short Post

```text
Awesome Loop Engineering v0.1.0 is live.

Loop Engineering is the layer above prompt, context, and harness engineering: designing recurring AI-agent systems that discover work, delegate to agents, verify results, persist state, decide next actions, and run again.

Repo:
https://github.com/ChaoYue0307/awesome-loop-engineering
```

### Longer Post

```text
Awesome Loop Engineering v0.1.0 is live.

The repo curates resources and practical patterns for an emerging AI/coding-agent practice: moving from turn-by-turn prompting to recurring systems that prompt, supervise, verify, persist state, and rerun agents.

It includes:

- curated papers, blogs, docs, tools, benchmarks, and patterns
- manifesto, taxonomy, comparison guide, anti-patterns, and sourced signals
- loop contract schema with validated examples
- pattern library for PR babysitting, CI repair, docs drift, deploy verification, and feedback clustering
- community gallery for real-world loop examples

Contributions and corrections are welcome:
https://github.com/ChaoYue0307/awesome-loop-engineering
```

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
