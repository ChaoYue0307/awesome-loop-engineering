# Claude Code Desktop Scheduled Task Variant

> Template, not a guarantee of product behavior. Confirm scheduling, file access, and missed-run handling in the [Claude Code desktop scheduled tasks docs](https://code.claude.com/docs/en/desktop-scheduled-tasks) before relying on this unattended.

A desktop scheduled task runs a saved prompt on a cadence on your own machine, with access to local files. Use it when a [session-scoped `/loop`](claude-loop.md) is too tied to an open session, but the work still needs your local filesystem and does not belong in the cloud.

## When to use a desktop scheduled task instead of `/loop`

- The job should run on a schedule even when you are not actively in a session.
- It needs local files that are not in a cloned Git repository.
- You want it on your machine, not Anthropic-managed cloud infrastructure. For cloud, prefer [remote routines](../../meta/RUNTIME_SELECTION.md).

Choose `/loop` instead when you are present and iterating; choose a remote routine when the work should run with your laptop closed and only needs a cloned repo.

## Shape

```text
Schedule: weekdays at 08:30 local time.

Prompt:
Objective: produce a morning status digest for this repository.

Each run:
1. In a fresh worktree off the default branch, collect: open PRs needing review,
   failing checks on main, and issues labeled "urgent" opened since the last run.
2. Verify each item against live GitHub state before including it.
3. Write the digest to reports/morning-digest-<date>.md with one source link per item.
4. Record the last-run timestamp in reports/.digest-state so the next run only adds new items.

Permission boundary:
- Read GitHub state and write only under reports/.
- Do not modify code, comment on PRs, or change issue state.

Stop conditions:
- Stop when the digest is written, or after 15 minutes.

Escalation:
- If GitHub is unreachable, write a short "digest skipped: <reason>" note and exit
  rather than producing an empty or stale digest.
```

## Worktree guidance

- Run the task inside a dedicated [worktree](../../README.md#core-loop-primitives) or branch so a scheduled run never collides with whatever you are doing in your main checkout.
- Keep writes scoped to an output directory the task owns (here, `reports/`).

## Missed-run guardrails

Scheduled tasks on a local machine only fire when the app can run them. Design for misses:

- **Make runs idempotent.** Use a last-run marker (here, `reports/.digest-state`) so a run that fires late or twice does not duplicate or skip work.
- **Drive intake from state, not from "since I last looked".** Select work by a recorded timestamp or processed-ID set, not by assuming every interval ran.
- **Fail visibly, not silently.** If the run cannot do its job, write a short reason and exit; do not emit an empty artifact that looks like success.
- **Do not assume catch-up semantics.** If you need guaranteed execution with recovery, use a [durable execution runtime](../../meta/RUNTIME_SELECTION.md).

## How it maps to the Loop Contract

| Contract part | In this template |
| ------------- | ---------------- |
| Trigger | Local schedule (weekdays 08:30) |
| Workspace | Fresh worktree per run, writes scoped to `reports/` |
| Verification | Each item checked against live GitHub state |
| Durable state | `reports/.digest-state` last-run marker |
| Budget | 15-minute stop |
| Escalation | Skip-with-reason instead of a stale digest |
