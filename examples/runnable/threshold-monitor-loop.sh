#!/usr/bin/env bash
# Read-only threshold monitor for deploy, performance, cost, and data-quality loops.
#
# PROBE_CMD must print one numeric value on its final output line. The script
# samples it on a bounded cadence, records receipts, and optionally asks an
# agent for diagnosis when the threshold is breached. It never remediates.
#
# Examples:
#   PROBE_CMD="./scripts/p95_latency_ms.sh" THRESHOLD=250 DIRECTION=max ./threshold-monitor-loop.sh
#   PROBE_CMD="./scripts/pass_rate.sh" THRESHOLD=0.95 DIRECTION=min AGENT_CMD="codex exec" ./threshold-monitor-loop.sh
#
# Exit codes: 0 all samples healthy, 2 threshold breached, 3 usage/probe error.

set -u

PROBE_CMD="${PROBE_CMD:-${1:-}}"
THRESHOLD="${THRESHOLD:-${2:-}}"
DIRECTION="${DIRECTION:-${3:-max}}"
AGENT_CMD="${AGENT_CMD:-}"
MAX_SAMPLES="${MAX_SAMPLES:-5}"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-60}"
PROGRESS_FILE="${PROGRESS_FILE:-MONITOR_PROGRESS.md}"

usage() {
  echo "Usage: PROBE_CMD='./probe.sh' THRESHOLD=250 DIRECTION=max $0" >&2
  echo "DIRECTION=max breaches above the threshold; min breaches below it." >&2
  exit 3
}

is_number() {
  printf '%s\n' "$1" | awk 'BEGIN { ok = 0 } /^[[:space:]]*-?([0-9]+([.][0-9]*)?|[.][0-9]+)[[:space:]]*$/ { ok = 1 } END { exit ok ? 0 : 1 }'
}

if [ -z "$PROBE_CMD" ] || [ -z "$THRESHOLD" ]; then
  usage
fi

if [ "$DIRECTION" != "max" ] && [ "$DIRECTION" != "min" ]; then
  usage
fi

if ! is_number "$THRESHOLD"; then
  echo "[monitor] THRESHOLD must be numeric: $THRESHOLD" >&2
  exit 3
fi

if ! printf '%s\n' "$MAX_SAMPLES" | awk '/^[1-9][0-9]*$/ { ok = 1 } END { exit ok ? 0 : 1 }'; then
  echo "[monitor] MAX_SAMPLES must be a positive integer." >&2
  exit 3
fi

record() {
  printf '%s\n' "$1" >> "$PROGRESS_FILE"
}

if [ ! -f "$PROGRESS_FILE" ]; then
  record "# Threshold monitor receipts"
fi

record ""
record "## Run started $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
record ""
record "- Probe: \`$PROBE_CMD\`"
record "- Boundary: $DIRECTION threshold $THRESHOLD"
record "- Budget: $MAX_SAMPLES samples, ${INTERVAL_SECONDS}s interval"

sample=0
while [ "$sample" -lt "$MAX_SAMPLES" ]; do
  sample=$((sample + 1))
  echo "[monitor] sample $sample/$MAX_SAMPLES" >&2

  probe_output="$(bash -c "$PROBE_CMD" 2>&1)"
  probe_status=$?
  value="$(printf '%s\n' "$probe_output" | tail -n 1 | tr -d '[:space:]')"

  if [ "$probe_status" -ne 0 ] || ! is_number "$value"; then
    echo "[monitor] probe failed or did not end with a numeric value." >&2
    record "- Sample $sample: probe error (exit $probe_status); escalated."
    record ""
    record "  \`\`\`text"
    printf '%s\n' "$probe_output" | tail -n 20 | sed 's/^/  /' >> "$PROGRESS_FILE"
    record "  \`\`\`"
    exit 3
  fi

  breached="$(awk -v value="$value" -v threshold="$THRESHOLD" -v direction="$DIRECTION" 'BEGIN { if (direction == "max") print (value > threshold ? "yes" : "no"); else print (value < threshold ? "yes" : "no") }')"
  record "- Sample $sample: value $value; status $([ "$breached" = "yes" ] && printf 'breached' || printf 'healthy')."

  if [ "$breached" = "yes" ]; then
    echo "[monitor] threshold breached: value=$value, $DIRECTION threshold=$THRESHOLD" >&2

    if [ -n "$AGENT_CMD" ]; then
      read -r -a agent_argv <<< "$AGENT_CMD"
      prompt="You are the read-only diagnosis role in a threshold-monitor loop.

Probe command: $PROBE_CMD
Observed value: $value
Boundary: $DIRECTION threshold $THRESHOLD
Sample: $sample of $MAX_SAMPLES

Recent probe output:
---
$(printf '%s\n' "$probe_output" | tail -n 40)
---

Diagnose likely causes and name the next evidence a human should inspect.
Do not modify files, services, configuration, deployments, or alert state.
Append a concise diagnosis to $PROGRESS_FILE if your runtime permits it."
      "${agent_argv[@]}" "$prompt"
      agent_status=$?
      record "- Diagnosis agent exited with status $agent_status."
    fi

    record "- Threshold breach escalated; no remediation attempted."
    exit 2
  fi

  if [ "$sample" -lt "$MAX_SAMPLES" ]; then
    sleep "$INTERVAL_SECONDS"
  fi
done

echo "[monitor] all $MAX_SAMPLES samples remained within the boundary." >&2
record "- All samples healthy. Loop complete."
exit 0

