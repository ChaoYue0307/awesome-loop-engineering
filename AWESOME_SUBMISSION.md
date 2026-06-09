# Awesome List Submission Checklist

Use this before submitting `awesome-loop-engineering` to [`sindresorhus/awesome`](https://github.com/sindresorhus/awesome).

## Current Status

- Repository name: `awesome-loop-engineering`.
- Default branch: `main`.
- License: `CC0-1.0`.
- Topics include: `awesome` and `awesome-list`.
- Cover image: present in `assets/awesome-loop-engineering-cover.png`.
- Contribution guidelines: `CONTRIBUTING.md`.
- Code of conduct: `CODE_OF_CONDUCT.md`.
- Quality workflow: enabled, but the README does not show a CI badge.

## Submission Timing

The upstream Awesome guidelines require the list to be around for at least 30 days after the first real commit or open-source publication, whichever is most recent.

The first clean public commit for this repository was created on 2026-06-10. Submit no earlier than 2026-07-10 unless the upstream maintainer explicitly says otherwise.

Until then, use the incubation issue mentioned in the upstream PR template for visibility instead of opening a draft PR.

## Required Preflight

Run:

```sh
npx --yes awesome-lint
npx --yes markdownlint-cli2 "**/*.md"
python3 scripts/check_license.py
python3 scripts/check_resource_labels.py README.md
python3 scripts/check_loop_contract_examples.py
python3 scripts/check_pages_metadata.py
python3 scripts/check_internal_links.py
python3 scripts/verify_urls.py . --timeout 12 --workers 20
python3 scripts/check_commit_identity.py
git diff --check
```

Fix all actionable findings before submitting. If `awesome-lint` reports a false positive, document it in the submission PR instead of hiding it.

If `awesome-lint` reports `Awesome list must reside in a valid git repository` from a local clone, check whether the local `origin` uses SSH without an available key. Run the linter from an HTTPS clone or against the public GitHub URL after pushing before treating that as a README failure.

## Upstream PR Requirements

Before opening the PR:

- Read the upstream contribution guidelines and list creation instructions again.
- Search existing open and closed PRs for duplicate Loop Engineering or agent-loop submissions.
- Review at least 4 other open PRs in `sindresorhus/awesome` with substantive comments.
- Prepare the PR title in the exact format `Add Loop Engineering`.
- Add the entry at the bottom of the appropriate category.
- Use a URL ending in `#readme`.
- Comment `unicorn` on the PR to confirm the guidelines were read.

Suggested entry:

```md
- [Loop Engineering](https://github.com/ChaoYue0307/awesome-loop-engineering#readme) - Designing recurring AI-agent systems that discover work, delegate to agents, verify results, persist state, and decide next actions.
```

## Suggested PR Body

```md
https://github.com/ChaoYue0307/awesome-loop-engineering

Loop Engineering is the practice of designing recurring AI-agent systems that discover work, delegate to agents, verify results, persist state, and decide next actions. The list curates papers, official docs, tools, benchmarks, critiques, and operational patterns for this emerging AI/coding-agent layer above prompt, context, and harness engineering.

I reviewed these PRs:

- #...
- #...
- #...
- #...
```
