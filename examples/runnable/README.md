# Runnable Loop Starters

Eight implementation starters connect a loop contract to a runtime. Three are dependency-light executables; five are copy/paste runtime templates with concrete prompts, schedules, permissions, state, and stop conditions.

Each starter keeps the control loop visible: permissions, verification, state, and budgets remain explicit instead of disappearing inside a framework.

## Choose A Starter

| Starter | Form | Best when | Trigger | State | External gate |
| --- | --- | --- | --- | --- | --- |
| [`test-repair-loop.sh`](test-repair-loop.sh) | **Executable** Bash | A deterministic command is failing | Manual bootstrap | Markdown progress ledger | Check-command exit code |
| [`threshold-monitor-loop.sh`](threshold-monitor-loop.sh) | **Executable** Bash | A metric must stay above or below a boundary | Bounded polling cadence | Markdown sample receipts | Numeric threshold comparison |
| [`queue-worker-loop.py`](queue-worker-loop.py) | **Executable** Python | Independent JSONL work items need bounded processing | Manual or scheduler | JSONL item receipts | Per-item verifier exit code |
| [Claude Code `/loop`](claude-loop.md) | Copy/paste template | You are present in an open coding session | Session interval | Session + progress file | Project check command |
| [Claude desktop scheduled task](claude-desktop-scheduled-task.md) | Copy/paste template | Local files need a recurring desktop task | Local schedule | Last-run marker + output | Live source checks |
| [Codex automation](codex-automation.md) | Copy/paste template | Background work belongs in an isolated worktree | Schedule | Worktree receipts + report | Declared repository checks |
| [GitHub agentic workflow](github-agentic-workflow.md) | Copy/paste template | Work starts from GitHub events or Actions schedules | Event or cron | Issue, PR, artifact, or cache | Required workflow checks |
| [Shell / cron](shell-cron-loop.md) | Copy/paste template | An existing agent CLI needs minimal OS scheduling | Cron | Lock + progress file | Script exit code |

Use the [runtime selection guide](../../meta/RUNTIME_SELECTION.md) when persistence, file access, isolation, or permissions determine the choice. Vendor templates describe a portable operating shape, not a guarantee of current product behavior; confirm commands and scheduling semantics in the linked official docs.

## Executable 1: Test Repair

This starter runs a deterministic check, sends only the failing evidence to an agent, and reruns the check until it passes, the evidence stops changing, or the budget expires.

```bash
# Claude Code
CHECK_CMD="pytest -x" AGENT_CMD="claude -p" ./test-repair-loop.sh

# Codex CLI
CHECK_CMD="npm test" AGENT_CMD="codex exec" ./test-repair-loop.sh
```

Run it inside a branch, worktree, or sandbox. The script edits nothing itself, but the delegated agent can.

| Contract part | Implementation |
| --- | --- |
| Objective | Make `CHECK_CMD` pass |
| Intake | Last `EVIDENCE_LINES` lines of failing output |
| Verification | `CHECK_CMD` exit code, judged by the script |
| State | `LOOP_PROGRESS.md` |
| Budget | `MAX_ITERATIONS`, default 5 |
| Escalation | Repeated evidence or exhausted budget returns non-zero |

## Executable 2: Threshold Monitor

This read-only starter samples a command that prints one number. It records each sample and exits on the first boundary breach. An optional agent can diagnose the evidence, but the script never remediates.

```bash
PROBE_CMD="./scripts/p95_latency_ms.sh" \
THRESHOLD=250 \
DIRECTION=max \
MAX_SAMPLES=12 \
INTERVAL_SECONDS=300 \
AGENT_CMD="codex exec" \
./threshold-monitor-loop.sh
```

Set `DIRECTION=max` when values above the threshold are bad, such as latency or spend. Set `DIRECTION=min` when values below it are bad, such as pass rate or availability.

| Contract part | Implementation |
| --- | --- |
| Objective | Keep a measured signal inside its declared boundary |
| Intake | Numeric final line from `PROBE_CMD` |
| Verification | `awk` compares the value with `THRESHOLD` |
| State | `MONITOR_PROGRESS.md` |
| Budget | `MAX_SAMPLES` and `INTERVAL_SECONDS` |
| Escalation | Probe error or first threshold breach |

## Executable 3: Queue Worker

This starter reads JSONL work items, skips IDs already marked complete, delegates one item at a time, runs an external verifier, and persists every attempt.

Minimum queue row:

```json
{"id":"docs-101","objective":"Update the CLI install example","allowed_paths":["README.md"],"verification":"python3 scripts/check_docs.py"}
```

Validate before invoking an agent:

```bash
python3 queue-worker-loop.py --queue tasks.jsonl --dry-run
```

Process a bounded batch:

```bash
python3 queue-worker-loop.py \
  --queue tasks.jsonl \
  --agent-command "codex exec" \
  --verify-command "python3 verify_item.py {id}" \
  --max-items 3 \
  --max-retries 2 \
  --command-timeout 900
```

The verifier receives the current item ID through both `{id}` substitution and the `LOOP_ITEM_ID` environment variable.

| Contract part | Implementation |
| --- | --- |
| Objective | Each queue row's `objective` |
| Intake | Pending JSONL rows after completed IDs are removed |
| Verification | `--verify-command` exit code |
| State | `QUEUE_PROGRESS.jsonl` |
| Budget | `--max-items`, `--max-retries`, and `--command-timeout` |
| Escalation | A work item exhausts its retry budget |

A timed-out agent or verifier consumes one attempt and leaves a receipt before the item retries or escalates.

## Design Choices Worth Copying

- **The maker does not check its own work.** External commands or thresholds decide completion.
- **State lives outside the model.** Markdown or JSONL receipts survive cold agent calls and reruns.
- **Completed work is idempotent.** Queue IDs and last-run markers prevent duplicate processing.
- **Evidence stops waste.** Repeated failures and threshold breaches stop or escalate instead of consuming an open-ended budget.
- **Permissions remain visible.** The starters expect a branch, worktree, sandbox, or read-only boundary rather than pretending isolation is automatic.

## Smoke Checks

Run these without an agent account:

```bash
bash -n test-repair-loop.sh threshold-monitor-loop.sh
python3 -m py_compile queue-worker-loop.py
printf '%s\n' '{"id":"demo","objective":"Validate the queue"}' > /tmp/loop-queue.jsonl
python3 queue-worker-loop.py --queue /tmp/loop-queue.jsonl --dry-run
PROBE_CMD="printf '42\\n'" THRESHOLD=100 MAX_SAMPLES=1 ./threshold-monitor-loop.sh
```

## Adapting A Starter

- Replace the verifier first; it defines what "done" means.
- Map allowed paths, tools, credentials, and network access from the chosen JSON contract.
- Keep mutable work away from the benchmark, policy, or tests that judge it.
- Choose a durable state artifact that the next cold run can read.
- Start with one item or iteration, then raise budgets only after reviewing receipts.
- Test failure, timeout, duplicate work, and human escalation before scheduling unattended runs.
