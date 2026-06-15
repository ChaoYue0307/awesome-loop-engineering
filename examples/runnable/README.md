# Runnable Loops

Most of this repository describes loops. This directory contains loops you can run.

The scripts are intentionally minimal: bash, coreutils, and whatever agent CLI you already use. They exist to make the [Loop Contract](../../README.md#the-loop-contract) concrete, not to be a framework.

## Runtime variants

The same loop shape runs on different runtimes. These templates show the wiring for each; the [runtime selection guide](../../meta/RUNTIME_SELECTION.md) compares persistence, file access, isolation, and permissions so you can choose deliberately.

- [Claude Code `/loop`](claude-loop.md) - session-scoped recurring task while you are nearby.
- [Claude Code desktop scheduled task](claude-desktop-scheduled-task.md) - local scheduled runs with file access and missed-run guardrails.
- [Codex automation](codex-automation.md) - unattended background task in an isolated worktree.
- [GitHub agentic workflow](github-agentic-workflow.md) - scheduled or event-triggered loop in GitHub Actions.
- [Shell / cron loop](shell-cron-loop.md) - minimal cron wrapper that delegates to an agent CLI and records receipts.

Each variant is a portable template, not a guarantee of vendor behavior; confirm product specifics in the linked official docs.

## test-repair-loop.sh

A manual-bootstrap loop that keeps handing failing check output to an agent until the check passes, the budget runs out, or the failure stops changing.

```sh
# Claude Code
CHECK_CMD="pytest -x" AGENT_CMD="claude -p" ./test-repair-loop.sh

# Codex CLI
CHECK_CMD="npm test" AGENT_CMD="codex exec" ./test-repair-loop.sh
```

Run it from inside a branch, worktree, or sandbox - the script edits nothing itself, but the agent it delegates to will.

### How the script maps to the Loop Contract

| Contract part | Where it lives in the script                                              |
| ------------- | ------------------------------------------------------------------------- |
| Objective     | Make `CHECK_CMD` pass                                                      |
| Trigger       | Manual bootstrap: you run the script                                       |
| Intake        | Captured check output, trimmed to the last `EVIDENCE_LINES` lines          |
| Workspace     | The directory you run it in; isolation is your responsibility              |
| Delegation    | `AGENT_CMD` receives the evidence and rules as a single prompt             |
| Verification  | The check command's exit code, judged by the script, never by the agent    |
| State         | `LOOP_PROGRESS.md` receipts survive iterations and reruns                  |
| Budget        | `MAX_ITERATIONS` (default 5)                                               |
| Escalation    | Non-zero exit with a recorded reason                                       |
| Exit          | Check passes, budget exhausted, or identical failure repeats               |

### Design choices worth copying

- **The maker does not check its own work.** The agent never decides the loop is done; the deterministic check command does. This is the separation of maker and checker from the [Loop Design Checklist](../../README.md#loop-design-checklist).
- **Stop when evidence stops changing.** Hashing the failure output and exiting when two consecutive iterations look identical prevents the most common waste mode: burning budget re-attempting the same dead end.
- **State lives outside the model.** Each iteration appends receipts to a progress file, and the prompt tells the agent to read it, so iteration 4 knows what iterations 1-3 tried even though each agent call starts cold.
- **Budgets are not optional.** An unattended loop without a hard iteration cap is an incident waiting to happen.

### Adapting it

- Swap `CHECK_CMD` for any deterministic gate: a typecheck, a linter, a schema validator, an eval suite with a threshold.
- Swap the manual trigger for a scheduler (cron, CI schedule, Claude Code scheduled tasks, Codex automations) to climb from Level 1 to Level 2 on the [Loop Maturity Model](../../README.md#loop-maturity-model).
- Tighten the agent's permissions with your runtime's flags (allowed tools, sandbox mode, read-only paths) before running it unattended - see [Securing Unattended Loops](../../README.md#securing-unattended-loops).
