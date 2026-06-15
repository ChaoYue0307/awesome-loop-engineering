# Claude Code `/loop` Variant

> Template, not a guarantee of product behavior. Commands and flags change; confirm against the [Claude Code docs](https://code.claude.com/docs/en/scheduled-tasks) before relying on this unattended.

A session-scoped recurring loop. Use `/loop` when you are nearby and want Claude to repeat a bounded task each interval inside an open session, with a deterministic check deciding when it is done.

## When to use

- You are iterating actively and want hands-off repetition for a while.
- The work touches your local working tree.
- A run that stops when you close the session is acceptable. For runs that must survive a closed app, see [the desktop scheduled task variant](claude-desktop-scheduled-task.md) or [remote routines](../../meta/RUNTIME_SELECTION.md).

## Shape

```text
/loop every 15m

Objective: keep `npm test` green on the current branch.

Each iteration:
1. Run `npm test`. Treat its exit code as the only signal of done.
2. If it passes, stop and say the loop is complete.
3. If it fails, read the last 80 lines of output and fix only the cause of that failure.
4. Append one line to LOOP_PROGRESS.md describing what you changed and why.
5. Read LOOP_PROGRESS.md at the start of each iteration so you do not repeat a failed fix.

Permission boundary:
- Edit only application and test files under src/ and tests/.
- Do not change CI config, add dependencies, or touch files outside this repo.
- Do not weaken or delete tests to make them pass.

Stop conditions:
- Stop when `npm test` passes.
- Stop after 5 iterations.
- Stop if the same failure repeats twice with no new evidence.

Escalation:
- If stopped without success, write a short summary of the blocker to LOOP_PROGRESS.md
  and open an issue titled "test-repair loop blocked" instead of continuing.
```

## How it maps to the Loop Contract

| Contract part | In this template |
| ------------- | ---------------- |
| Trigger | `/loop every 15m`, session-scoped |
| Verification | `npm test` exit code, judged by the runtime, not the model |
| Durable state | `LOOP_PROGRESS.md`, read at the start of each iteration |
| Budget | 5 iterations; stop on repeated identical failure |
| Permission boundary | Explicit allowed paths and disallowed actions in the prompt |
| Escalation | Summary plus an issue when stopped without success |

## Guardrails

- Run from a [worktree](../../README.md#core-loop-primitives) or branch so the loop cannot corrupt your main checkout.
- Keep the budget small until you trust the loop; an unattended loop with no cap is an incident waiting to happen.
- The check command must be deterministic. If "done" depends on the model's opinion, the loop has no real gate.
