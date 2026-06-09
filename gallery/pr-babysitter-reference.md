# PR Babysitter Reference Loop

## Summary

This is a reference gallery entry for a loop that keeps one pull request moving toward merge readiness. It is based on the repository's [`PR babysitter`](../patterns/pr-babysitter.md) pattern and [`pr-babysitter-loop.json`](../examples/pr-babysitter-loop.json) contract, not a claimed production deployment.

## Runtime Or Tooling

- Runtime: Codex, Claude Code, GitHub Agentic Workflows, or a custom GitHub Actions loop.
- Agent system: explorer, implementer, reviewer, judge.
- Integrations: GitHub pull requests, checks, comments, branch status.
- Repository or environment: open-source repository with required checks and review rules.

## Loop Contract

- Objective: keep the PR merge-ready or clearly blocked.
- Trigger: every 1-2 hours during working hours, and after requested changes or failed checks.
- Discover / intake: PR comments, review threads, check status, mergeability, linked issues.
- Workspace: dedicated branch or worktree based on the PR branch.
- Context: `AGENTS.md`, contribution rules, acceptance criteria, last checked SHA.
- Delegation: explorer classifies blockers, implementer patches mechanical issues, reviewer checks scope, judge decides next action.
- Verification: required checks pass, comments are answered or resolved, conflicts are gone, diff remains scoped.
- State: PR progress comment or `PROGRESS.md` with blockers, commands, attempts, and next action.
- Budget: 3 retries per distinct blocker or 60 minutes per run.
- Escalation: architecture decisions, force-push needs, product ambiguity, reviewer disagreement, repeated failures.
- Exit: PR is merge-ready, waiting on human review, blocked, or out of budget.

## Loop Instruction Or Automation

```text
Every 2 hours during working hours, inspect PR <number>.
Load review comments, check status, mergeability, linked issues, and project instructions.
If there is a narrow mechanical blocker, patch it in an isolated worktree and run the smallest relevant checks.
Record commands, changed files, check URLs, and remaining blockers in a PR comment.
Stop when the PR is merge-ready, waiting only on human review, blocked, or out of retry budget.
```

## Receipts

Public or anonymized receipts should include:

- PR URL or anonymized PR number;
- last checked SHA;
- failed or passed check URLs;
- commands run;
- changed files;
- unresolved comments or blocker summary.

## Lessons Learned

- What worked: narrow blockers such as formatting, docs comments, merge conflicts, and test failures are good loop candidates.
- What failed: product questions and broad review disagreements should escalate quickly.
- What changed after the first run: the progress comment became the state artifact that prevents repeated work.

## Safety Notes

- Sensitive actions: force-pushes, broad rewrites, dependency upgrades, migrations, secrets, and production changes.
- Human approvals: required for anything beyond narrow review or CI fixes.
- Data or privacy constraints: do not copy private review context into public gallery entries.
