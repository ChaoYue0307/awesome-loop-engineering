# PR Babysitter

## Objective

Keep an open pull request moving toward merge readiness without requiring a human to repeatedly poll comments, CI, conflicts, and stale review threads.

## Trigger

- Schedule: every 30-120 minutes during working hours.
- Event: new review comment, failed check, requested changes, merge conflict, or stale PR label.
- Manual command: "babysit PR #123 until it is merge-ready or blocked."

## Intake

- GitHub PR metadata, review state, comments, requested changes, checks, branch status, and mergeability.
- Linked issues or acceptance criteria.
- Existing runbook, `AGENTS.md`, and project contribution rules.

## Agents

- Explorer: summarizes PR state, blockers, comments, and check failures.
- Implementer: applies only narrow fixes required by the latest evidence.
- Reviewer: inspects the diff and verifies that comments were addressed.
- Judge: decides whether to push, open a follow-up issue, or escalate.

## Workspace And Permissions

- Use a dedicated branch or worktree for fixes.
- Allow reading PR metadata, comments, checks, and changed files.
- Allow narrow code/doc edits tied to explicit review feedback.
- Require human approval for force pushes, broad rewrites, dependency upgrades, migrations, secrets, or production changes.

## Durable State

- Progress comment on the PR or a local `PROGRESS.md`.
- Last checked commit SHA, unresolved comments, attempted fixes, commands run, and known blockers.

## Loop Steps

1. Fetch the latest PR state.
1. Classify blockers: comments, CI, conflicts, missing review, product decision, or no work.
1. If the blocker is mechanical and scoped, patch it in the isolated workspace.
1. Run the smallest relevant checks.
1. Push the patch or prepare a clear summary.
1. Update durable state with evidence and next action.
1. Stop when merge-ready, blocked on a human, or budget is exhausted.

## Verification Gates

- Required GitHub checks pass.
- Review comments are resolved or explicitly answered.
- Merge conflicts are gone.
- Diff is limited to the stated blocker.
- Summary names commands run and remaining risk.

## Budget And Exit

- Max retries: 3 per distinct blocker.
- Max runtime: 30-60 minutes per loop run.
- Stop when the PR is merge-ready, waiting on human review, blocked on product judgment, or the same failure repeats twice.

## Escalation

Escalate when the fix requires architectural judgment, large refactors, test infrastructure repair, credentials, unavailable services, or reviewer disagreement.

## Starter Prompt

```text
Babysit PR <number>. Inspect review comments, CI checks, conflicts, and merge readiness.
Only make narrow changes tied to explicit blockers.
Use an isolated workspace, run the smallest relevant verification commands, and keep a progress record.
Stop and escalate if the blocker requires human judgment, broad rewrites, secrets, or force-push decisions.
```

## Failure Modes

- The loop keeps patching symptoms instead of identifying the root failing check.
- The agent expands scope beyond review feedback.
- CI is flaky and the loop burns retries without new evidence.
- The PR needs human product judgment, not more code.
