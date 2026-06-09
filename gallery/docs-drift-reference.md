# Docs Drift Reference Loop

## Summary

This is a reference gallery entry for a loop that finds and patches documentation drift. It is based on the repository's [`Docs drift collector`](../patterns/docs-drift-collector.md) pattern and [`docs-drift-loop.json`](../examples/docs-drift-loop.json) contract, not a claimed production deployment.

## Runtime Or Tooling

- Runtime: Codex, Claude Code, GitHub Agentic Workflows, or a scheduled docs-check workflow.
- Agent system: explorer, implementer, verifier, reviewer.
- Integrations: repository search, docs tests, link checker, CLI help, API schema.
- Repository or environment: project with public docs, examples, and code-derived behavior.

## Loop Contract

- Objective: find docs that no longer match code, CLI behavior, API schemas, screenshots, or examples.
- Trigger: weekly, after release branches, after public API changes, or after docs-related issues.
- Discover / intake: changed files, README sections, docs pages, examples, generated references, CLI help, user reports.
- Workspace: docs-focused branch or worktree.
- Context: docs contribution rules, current CLI/API output, schema, docs test commands.
- Delegation: explorer maps behavior to docs, implementer patches confirmed drift, verifier runs checks, reviewer checks tone and scope.
- Verification: examples run or match output, link checker passes, generated files are not edited manually, diff is scoped to confirmed drift.
- State: drift report with checked files, accepted patches, rejected false positives, commands run.
- Budget: 2 retries per drift item or 60 minutes.
- Escalation: product documentation decisions, credentials, generated docs pipeline, screenshot/design approval.
- Exit: high-confidence drift is patched and verified, or remaining items need owner judgment.

## Loop Instruction Or Automation

```text
Weekly, scan changed files, public docs, examples, generated API references, CLI help, and docs-related issues.
Confirm each possible drift item against code, schema, tests, or runtime output before editing.
Patch only verified mismatches, run docs/link/example checks, and record false positives so future runs do not repeat them.
Escalate when product behavior, generated docs, credentials, or screenshots need owner judgment.
```

## Receipts

Public or anonymized receipts should include:

- changed docs;
- command output or schema evidence;
- link checker output;
- examples run;
- false positive list;
- unresolved owner questions.

## Lessons Learned

- What worked: verifying against runtime output before editing prevents plausible but wrong docs changes.
- What failed: treating missing docs as drift can create product decisions disguised as maintenance.
- What changed after the first run: false positives are persisted so the next scheduled run does not re-open them.

## Safety Notes

- Sensitive actions: product behavior changes, public API changes, generated file edits, screenshots needing approval.
- Human approvals: required when docs conflict with intended product behavior.
- Data or privacy constraints: remove private endpoints, customer data, internal URLs, and credentials from examples.
