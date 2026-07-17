# Codex Automation Variant

> Template, not a guarantee of product behavior. Confirm triggers, worktree behavior, and scopes in the [scheduled tasks docs](https://learn.chatgpt.com/docs/automations?surface=app) before relying on this unattended.

A Codex automation runs a saved task on a cadence or in response to events, in an isolated workspace. Use it for recurring background work such as triage, repair, or digest loops that should run without you starting each one.

## When to use

- The work recurs and should run unattended in the background.
- It fits an isolated, per-run [worktree](https://learn.chatgpt.com/docs/environments/git-worktrees).
- You want it on the Codex runtime rather than your own infrastructure.

## Shape

```text
Automation: CI repair triage
Trigger: when a required check fails on an open PR (and a nightly sweep as backup).
Workspace: isolated worktree off the PR branch.

Task:
1. Reproduce the failing check. Identify the exact failing command or the closest local equivalent.
2. Read the failing logs and the changed files. Form one hypothesis about the cause.
3. If the cause is mechanical and in scope, patch only that cause in the worktree.
4. Rerun the failing command first. Treat its exit code as the only signal of success.
5. Record the failing log excerpt, the patch, and the passing output in a PR comment.

Permission boundary:
- Edit only the files implicated by the failure.
- Do not change CI config, upgrade dependencies, or edit unrelated files.
- Do not merge, force-push, or alter required checks.

Stop conditions:
- Stop when the failing command passes and the diff is scoped to the cause.
- Stop after 3 repair attempts.
- Stop if the failure is outside scope (flaky infra, test design, missing service).

Escalation:
- If stopped without success, post a PR comment summarizing the failing command,
  what was tried, and why it is out of scope, then request a human reviewer.
```

## How it maps to the Loop Contract

| Contract part | In this template |
| ------------- | ---------------- |
| Trigger | Check-failure event, with a nightly backup sweep |
| Workspace | Isolated worktree per run |
| Verification | The original failing command passes, judged by exit code |
| Durable state | PR comment with logs, patch, and passing output |
| Budget | 3 repair attempts |
| Escalation | PR comment plus a requested human reviewer |

## Guardrails

- Keep the patch scoped to the failure cause; scope creep is the most common way these loops go wrong.
- Pair the event trigger with a periodic sweep so a missed event does not leave work undone.
- Start from the full [CI repair pattern and contract](../../patterns/ci-repair-loop.md) before adapting this runtime variant.
