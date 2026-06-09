# CI Repair Reference Loop

## Summary

This is a reference gallery entry for a loop that turns failing CI into a small verified patch or an escalation note. It is based on the repository's [`CI repair loop`](../patterns/ci-repair-loop.md) pattern and [`ci-repair-loop.json`](../examples/ci-repair-loop.json) contract, not a claimed production deployment.

## Runtime Or Tooling

- Runtime: Codex, Claude Code, GitHub Agentic Workflows, or a custom CI-triggered agent workflow.
- Agent system: investigator, implementer, verifier, reporter.
- Integrations: CI logs, artifacts, test runner, GitHub PR comments.
- Repository or environment: repository with reproducible local checks or CI-equivalent commands.

## Loop Contract

- Objective: convert a failing check into a narrow fix or useful escalation.
- Trigger: required CI check fails on an active PR.
- Discover / intake: failed check name, logs, artifacts, changed files, recent successful run.
- Workspace: clean worktree based on the failing commit.
- Context: project instructions, test docs, failing command, relevant artifacts.
- Delegation: investigator extracts evidence, implementer patches, verifier reruns checks, reporter records outcome.
- Verification: original failing command passes, patch matches root cause, new behavior has focused tests when needed.
- State: CI repair note with log excerpt, hypothesis, attempted fixes, passing output, unresolved blockers.
- Budget: 3 patch attempts or 90 minutes.
- Escalation: missing credentials, flaky infrastructure, third-party outage, nondeterminism, broad CI config change.
- Exit: target check passes, failure is proven flaky, environment blocks reproduction, or fix exceeds scope.

## Loop Instruction Or Automation

```text
When a required CI check fails, inspect the failing check, logs, artifacts, changed files, and recent successful run.
Identify the exact failing command or closest local equivalent.
Patch only the smallest log-backed cause, rerun the failing command first, and summarize evidence.
Escalate instead of changing tests, broad CI config, dependencies, or unrelated files without proof.
```

## Receipts

Public or anonymized receipts should include:

- CI run URL;
- failing log excerpt;
- local command and output;
- patch summary;
- passing rerun evidence;
- escalation note if unresolved.

## Lessons Learned

- What worked: starting from the exact failing command prevents broad speculative fixes.
- What failed: weakening tests or deleting assertions creates false green signals.
- What changed after the first run: repeated flaky failures are now a stop condition, not an invitation to keep retrying.

## Safety Notes

- Sensitive actions: CI config edits, dependency updates, secrets, deploy keys, and test weakening.
- Human approvals: required for protected workflow changes and non-local infrastructure changes.
- Data or privacy constraints: redact logs that contain secrets, tokens, customer data, or private paths.
