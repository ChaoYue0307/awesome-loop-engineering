# Distribution And Discovery Checklist

Use this checklist after major updates or releases. The goal is accurate discovery, not hype.

## Indexing Basics

- Confirm the repository is public.
- Confirm GitHub Pages is enabled and points to `docs/` on `main`.
- Confirm the Pages homepage is set as the repository website.
- Confirm `docs/sitemap.xml` and `docs/robots.txt` are reachable.
- Share the GitHub repository URL and Pages URL from public pages that search engines can crawl.

Search engines may still take days or longer to index a new repository. Backlinks and real activity help discovery.

## Launch Copy

Use [`posts/launch.md`](posts/launch.md) when you want a longer article-style launch post.

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
