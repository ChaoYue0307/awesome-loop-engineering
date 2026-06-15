# Shell / Cron Loop Variant

> Portable template. It depends only on a POSIX shell, coreutils, `cron`, and an agent CLI you already have. Use it when you want full control and no vendor runtime.

A minimal cron wrapper that delegates one bounded task to an agent CLI, gates the result on a deterministic check, and records receipts. This is the Level 2 step on the [Loop Maturity Model](../../README.md#loop-maturity-model): a scheduled loop that reports, with state outside the model.

## When to use

- You want the loop on your own machine or server, owning isolation and secrets yourself.
- The runtime should be boring and inspectable: a script you can read end to end.
- You are prototyping a loop before promoting it to a managed runtime.

## The wrapper

```sh
#!/usr/bin/env bash
# loop-wrapper.sh - run one bounded agent task, gate on a check, record receipts.
set -u

REPO="${REPO:-$PWD}"
CHECK_CMD="${CHECK_CMD:-npm test}"
AGENT_CMD="${AGENT_CMD:-claude -p}"          # any non-interactive agent CLI
RECEIPTS="${RECEIPTS:-$REPO/loop-receipts.log}"
LOCK="${LOCK:-$REPO/.loop.lock}"

# One run at a time: skip if a previous run is still going (missed-run guardrail).
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "$(date -u +%FT%TZ) skip: previous run still holds the lock" >> "$RECEIPTS"
  exit 0
fi
trap 'rmdir "$LOCK"' EXIT

cd "$REPO" || exit 1

# Gate first: if the check already passes, there is no work to do.
if bash -c "$CHECK_CMD" >/tmp/loop-check.out 2>&1; then
  echo "$(date -u +%FT%TZ) ok: check already green, no action" >> "$RECEIPTS"
  exit 0
fi

# Delegate exactly one bounded attempt to the agent.
prompt="The check '$CHECK_CMD' is failing. Latest output:
$(tail -n 80 /tmp/loop-check.out)

Fix only the cause of this failure. Do not change CI config, add dependencies,
or edit unrelated files. Append one line to loop-receipts.log describing the change."

$AGENT_CMD "$prompt"

# Re-gate: the deterministic check, not the agent, decides success.
if bash -c "$CHECK_CMD" >/tmp/loop-check.out 2>&1; then
  echo "$(date -u +%FT%TZ) fixed: check green after agent run" >> "$RECEIPTS"
else
  echo "$(date -u +%FT%TZ) blocked: still failing, escalating" >> "$RECEIPTS"
  # Escalation: open an issue, ping a channel, or just leave a receipt for a human.
  # gh issue create --title "loop blocked: $CHECK_CMD" --body-file /tmp/loop-check.out
fi
```

Schedule it with cron (here, every weekday at 09:00):

```cron
0 9 * * 1-5 cd /path/to/repo && CHECK_CMD="npm test" AGENT_CMD="claude -p" ./loop-wrapper.sh
```

## How it maps to the Loop Contract

| Contract part | In this template |
| ------------- | ---------------- |
| Trigger | The cron schedule |
| Intake | The failing check output, trimmed to the last 80 lines |
| Verification | `CHECK_CMD` exit code, re-run after the agent, never the agent's opinion |
| Durable state | `loop-receipts.log` |
| Budget | One bounded attempt per run; the lock prevents overlap |
| Escalation | A blocked receipt, optionally an issue or alert |

## Guardrails

- Run against a dedicated branch, worktree, or a checkout you are willing to lose; the agent edits real files.
- The lock directory is the missed-run guardrail: a slow run will not stack on top of the next scheduled one.
- Scope the agent CLI's permissions (allowed tools, sandbox, read-only paths) before running unattended; see [Securing Unattended Loops](../../README.md#securing-unattended-loops).
- For crash-proof state and guaranteed recovery, graduate to a [durable execution runtime](../../meta/RUNTIME_SELECTION.md).
- The richer, multi-iteration version of this idea is [`test-repair-loop.sh`](test-repair-loop.sh).
