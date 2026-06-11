# Loop Examples

These examples show how to turn the abstract loop contract into concrete operating specs.

## Contract Library

Every loop in the [pattern library](../patterns/README.md) has a matching contract. Each JSON file follows [`schemas/loop-contract.schema.json`](../schemas/loop-contract.schema.json) and is validated in CI:

- [`pr-babysitter-loop.json`](pr-babysitter-loop.json)
- [`ci-repair-loop.json`](ci-repair-loop.json)
- [`docs-drift-loop.json`](docs-drift-loop.json)
- [`deploy-verifier-loop.json`](deploy-verifier-loop.json)
- [`feedback-clusterer-loop.json`](feedback-clusterer-loop.json)
- [`dependency-triage-loop.json`](dependency-triage-loop.json)
- [`evaluation-regression-loop.json`](evaluation-regression-loop.json)
- [`security-review-loop.json`](security-review-loop.json)
- [`cost-control-loop.json`](cost-control-loop.json)
- [`bug-hunting-loop.json`](bug-hunting-loop.json)

Use them as starting points. Adapt triggers, tools, checks, state artifacts, and escalation rules to your repository and runtime.

## Runnable Loops

The [runnable directory](runnable/README.md) contains working loop scripts, starting with a dependency-light test-repair loop you can drive with Claude Code, Codex CLI, or any agent CLI.

## PR Babysitter

Use when a PR needs recurring attention but should not require a human to poll comments, checks, conflicts, and stale review state.

Example loop instruction:

```text
Every 2 hours during working hours, inspect PR <number>.
Load review comments, check status, mergeability, linked issues, and project instructions.
If there is a narrow mechanical blocker, patch it in an isolated worktree and run the smallest relevant checks.
Record commands, changed files, check URLs, and remaining blockers in a PR comment.
Stop when the PR is merge-ready, waiting only on human review, blocked, or out of retry budget.
```

Good gates:

- required checks pass;
- unresolved comments are answered or resolved;
- merge conflicts are gone;
- diff is limited to the stated blocker.

## CI Repair Loop

Use when failing CI should be turned into either a small verified patch or an escalation note.

Example loop instruction:

```text
When a required CI check fails, inspect the failing check, logs, artifacts, changed files, and recent successful run.
Identify the exact failing command or closest local equivalent.
Patch only the smallest log-backed cause, rerun the failing command first, and summarize evidence.
Escalate instead of changing tests, broad CI config, dependencies, or unrelated files without proof.
```

Good gates:

- the original failing command passes locally or in rerun CI;
- the patch is limited to the failure cause;
- behavior changes include focused tests;
- the report includes the failing log excerpt and passing output.

## Docs Drift Collector

Use when docs need periodic alignment with code, CLI behavior, schemas, or examples.

Example loop instruction:

```text
Weekly, scan changed files, public docs, examples, generated API references, CLI help, and docs-related issues.
Confirm each possible drift item against code, schema, tests, or runtime output before editing.
Patch only verified mismatches, run docs/link/example checks, and record false positives so future runs do not repeat them.
Escalate when product behavior, generated docs, credentials, or screenshots need owner judgment.
```

Good gates:

- examples run or match current output;
- link checker passes;
- generated files are not edited manually unless that is the project convention;
- false positives are recorded as loop state.
