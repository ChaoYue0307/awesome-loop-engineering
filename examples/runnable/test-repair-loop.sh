#!/usr/bin/env bash
# Minimal runnable Loop Engineering reference: a test-repair loop.
#
# Runs a deterministic check command, and while it fails, hands the evidence
# to an agent CLI for a narrow fix, then re-runs the check. Demonstrates the
# Loop Contract with no dependencies beyond bash, coreutils, and your agent CLI.
#
#   Objective    : make CHECK_CMD pass
#   Trigger      : manual bootstrap (run this script)
#   Intake       : failing check output
#   Workspace    : current directory (run it inside a branch or worktree)
#   Delegation   : AGENT_CMD receives the evidence as a prompt
#   Verification : CHECK_CMD exit code, judged by the script, not the agent
#   State        : PROGRESS_FILE survives across iterations and runs
#   Budget       : MAX_ITERATIONS
#   Escalation   : exits non-zero with a reason when evidence stops changing
#   Exit         : check passes, budget exhausted, or repeated failure
#
# Usage:
#   CHECK_CMD="pytest -x" AGENT_CMD="claude -p" ./test-repair-loop.sh
#   CHECK_CMD="npm test"  AGENT_CMD="codex exec" ./test-repair-loop.sh
#
# Exit codes: 0 check passes, 1 budget exhausted, 2 no new evidence, 3 usage.

set -u

CHECK_CMD="${CHECK_CMD:-${1:-}}"
AGENT_CMD="${AGENT_CMD:-${2:-}}"
MAX_ITERATIONS="${MAX_ITERATIONS:-5}"
PROGRESS_FILE="${PROGRESS_FILE:-LOOP_PROGRESS.md}"
EVIDENCE_LINES="${EVIDENCE_LINES:-80}"

if [ -z "$CHECK_CMD" ] || [ -z "$AGENT_CMD" ]; then
  echo "Usage: CHECK_CMD='pytest -x' AGENT_CMD='claude -p' $0" >&2
  echo "   or: $0 'pytest -x' 'claude -p'" >&2
  exit 3
fi

# AGENT_CMD is split on whitespace; the prompt is passed as one final argument.
read -r -a agent_argv <<< "$AGENT_CMD"

failure_digest() {
  # Stable fingerprint of the failure so we can tell when evidence stops changing.
  if command -v shasum >/dev/null 2>&1; then shasum | cut -d' ' -f1; else cksum | cut -d' ' -f1; fi
}

record() {
  printf '%s\n' "$1" >> "$PROGRESS_FILE"
}

if [ ! -f "$PROGRESS_FILE" ]; then
  record "# Loop progress"
  record ""
  record "- Objective: make \`$CHECK_CMD\` pass."
fi

record ""
record "## Run started $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
record ""
record "- Check command: \`$CHECK_CMD\`"
record "- Budget: $MAX_ITERATIONS iterations"

previous_digest=""
iteration=0

while [ "$iteration" -lt "$MAX_ITERATIONS" ]; do
  iteration=$((iteration + 1))
  echo "[loop] iteration $iteration/$MAX_ITERATIONS: running check..." >&2

  check_output="$(bash -c "$CHECK_CMD" 2>&1)"
  check_status=$?

  if [ "$check_status" -eq 0 ]; then
    echo "[loop] check passed." >&2
    record "- Iteration $iteration: check passed. Loop complete."
    exit 0
  fi

  evidence="$(printf '%s\n' "$check_output" | tail -n "$EVIDENCE_LINES")"
  digest="$(printf '%s' "$evidence" | failure_digest)"

  if [ "$digest" = "$previous_digest" ]; then
    echo "[loop] same failure twice with no new evidence; escalating to a human." >&2
    record "- Iteration $iteration: identical failure repeated (digest $digest). Escalated."
    exit 2
  fi
  previous_digest="$digest"

  record "- Iteration $iteration: check failed (exit $check_status, digest $digest). Delegating fix."

  prompt="You are one iteration inside an automated test-repair loop.

Objective: make this command pass: $CHECK_CMD
Read $PROGRESS_FILE for what previous iterations already tried.

Latest failing output (last $EVIDENCE_LINES lines):
---
$evidence
---

Rules:
- Fix only the cause of this failure. Do not expand scope.
- Do not modify or delete tests to make them pass unless the test itself is provably wrong.
- Do not add dependencies, change CI config, or touch unrelated files.
- After editing, append one line to $PROGRESS_FILE describing what you changed and why.
- The loop re-runs the check itself; an external gate decides completion, not you."

  "${agent_argv[@]}" "$prompt"
  agent_status=$?
  record "- Iteration $iteration: agent exited with status $agent_status."
done

echo "[loop] budget of $MAX_ITERATIONS iterations exhausted; escalating to a human." >&2
record "- Budget exhausted after $MAX_ITERATIONS iterations. Escalated."
exit 1
