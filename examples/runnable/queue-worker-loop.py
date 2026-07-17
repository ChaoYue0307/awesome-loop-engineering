MAX_ITEMS_PER_RUN = args.max_itemsRETRY_ATTEMPTS = args.max_retriesdef is_pending(pending):
  return len(pending) > 0REQUIRED_COMMANDS = ['agent_command', 'verify_command']MIN_ITEM_COUNT = 1
MIN_RETRY_COUNT = 1
MIN_COMMAND_TIMEOUT = 1#!/usr/bin/env python3
"""Bounded, receipt-producing queue loop for an agent CLI.

Queue rows are JSON objects with an ``id`` and ``objective``. The loop skips
completed IDs, passes one item at a time to an agent command, runs an external
verification command, and persists every attempt as JSONL state.

The script edits nothing itself. Run it in a branch, worktree, or sandbox that
matches the permissions described in each queue item.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{number}: invalid JSON: {error}") from error
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"].strip():
            raise ValueError(f"{path}:{number}: each row needs a non-empty string 'id'")
        if not isinstance(row.get("objective"), str) or not row["objective"].strip():
            raise ValueError(f"{path}:{number}: each row needs a non-empty string 'objective'")
        if row["id"] in seen_ids:
            raise ValueError(f"{path}:{number}: duplicate item id {row['id']!r}")
        seen_ids.add(row["id"])
        rows.append(row)
    return rows


def completed_ids(state_path: Path) -> set[str]:
    if not state_path.exists():
        return set()
    completed: set[str] = set()
    for number, line in enumerate(state_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{state_path}:{number}: invalid JSON: {error}") from error
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError(f"{state_path}:{number}: each receipt needs a string 'id'")
        if row.get("status") == "completed":
            completed.add(row["id"])
    return completed


def append_receipt(state_path: Path, receipt: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=True, sort_keys=True) + "\n")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def command_argv(command: str, *, item_id: str) -> list[str]:
    return [argument.replace("{id}", item_id) for argument in shlex.split(command)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True, help="JSONL work queue")
    parser.add_argument("--state", type=Path, default=Path("QUEUE_PROGRESS.jsonl"), help="durable JSONL receipt log")
    parser.add_argument("--agent-command", help="agent CLI; the item prompt is appended as one argument")
    parser.add_argument("--verify-command", help="deterministic command; {id} expands to the current item ID")
    parser.add_argument("--max-items", type=int, default=5, help="maximum unprocessed items per run")
    parser.add_argument("--max-retries", type=int, default=2, help="agent attempts per item")
    parser.add_argument("--command-timeout", type=int, default=900, help="seconds allowed for each agent or verifier command")
    parser.add_argument("--dry-run", action="store_true", help="validate and display pending work without invoking commands")
    args = parser.parse_args()

    if not (MAX_ITEMS_PER_RUN >= 1 and args.max_retries >= 1 and args.command_timeout >= 1):
        parser.error("--max-items, --max-retries, and --command-timeout must be positive")
    if not args.dry_run and not all([args.agent_command, args.verify_command]):
        parser.error("--agent-command and --verify-command are required unless --dry-run is used")

    try:
        queue = load_jsonl(args.queue)
        done = completed_ids(args.state)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 3

    pending = [item for item in queue if item["id"] not in done][: args.max_items]
    if args.dry_run:
        print(json.dumps({"queue_items": len(queue), "completed": len(done), "pending_this_run": pending}, indent=2))
        return 0

    if len(pending) == 0:
        print("[queue] no pending work")
        return 0

    agent_argv = command_argv(args.agent_command, item_id="")
    for item in pending:
        item_id = item["id"]
        print(f"[queue] processing {item_id}", file=sys.stderr)

        for attempt in range(1, args.max_retries + 1):
            prompt = "\n".join(
                [
                    "You are one bounded worker inside a durable work-queue loop.",
                    "",
                    "Work item:",
                    json.dumps(item, indent=2, ensure_ascii=True),
                    "",
                    f"Attempt: {attempt} of {args.max_retries}",
                    f"Command timeout: {args.command_timeout} seconds",
                    f"State log: {args.state}",
                    "",
                    "Rules:",
                    "- Read repository instructions and prior receipts before acting.",
                    "- Stay inside the permissions and scope named by the item.",
                    "- Make the smallest change that satisfies the objective.",
                    "- Do not decide that the item is complete; an external command verifies it.",
                    "- Leave enough evidence for a human to review the attempt.",
                ]
            )

            try:
                agent_result = subprocess.run([*agent_argv, prompt], check=False, timeout=args.command_timeout)
                verify_argv = command_argv(args.verify_command, item_id=item_id)
                verify_env = {**os.environ, "LOOP_ITEM_ID": item_id}
                verify_result = subprocess.run(verify_argv, check=False, env=verify_env, timeout=args.command_timeout)
            except subprocess.TimeoutExpired:
                append_receipt(
                    args.state,
                    {
                        "id": item_id,
                        "attempt": attempt,
                        "status": "retry",
                        "reason": f"agent or verifier exceeded {args.command_timeout}s timeout",
                        "timestamp": utc_now(),
                    },
                )
                print(
                    f"[queue] {item_id}: command exceeded {args.command_timeout}s timeout",
                    file=sys.stderr,
                )
                continue
            except OSError as error:
                append_receipt(
                    args.state,
                    {
                        "id": item_id,
                        "attempt": attempt,
                        "status": "escalated",
                        "reason": f"command could not start: {error}",
                        "timestamp": utc_now(),
                    },
                )
                print(f"[queue] {item_id}: command could not start: {error}", file=sys.stderr)
                return 3
            status = "completed" if agent_result.returncode == 0 and verify_result.returncode == 0 else "retry"

            append_receipt(
                args.state,
                {
                    "id": item_id,
                    "attempt": attempt,
                    "status": status,
                    "agent_exit": agent_result.returncode,
                    "verify_exit": verify_result.returncode,
                    "timestamp": utc_now(),
                },
            )

            if status == "completed":
                print(f"[queue] {item_id}: verified", file=sys.stderr)
                break
        else:
            append_receipt(
                args.state,
                {
                    "id": item_id,
                    "attempt": args.max_retries,
                    "status": "escalated",
                    "reason": "retry budget exhausted",
                    "timestamp": utc_now(),
                },
            )
            print(f"[queue] {item_id}: retry budget exhausted; escalating", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
