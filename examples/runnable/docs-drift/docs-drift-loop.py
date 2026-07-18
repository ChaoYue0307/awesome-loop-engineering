#!/usr/bin/env python3
"""Run a bounded documentation-drift loop with external verification.

The discovery command owns the drift decision: exit 0 means no confirmed drift,
exit 1 means confirmed drift and its output is evidence, and any other exit code
is a detector error. The script can write a report only or delegate a patch to
an agent CLI, enforce a path and file-count boundary, run an independent
verifier, and persist every outcome as JSONL outside the model context.

Run this only in a clean branch or worktree. The script never commits, pushes,
merges, edits generated files itself, or weakens a verifier.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


EXIT_OK = 0
EXIT_ESCALATED = 2
EXIT_ERROR = 3


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def command_argv(command: str) -> list[str]:
    argv = shlex.split(command)
    if not argv:
        raise ValueError("command cannot be empty")
    return argv


def run_command(
    command: str,
    *,
    workdir: Path,
    timeout: int,
    final_argument: str | None = None,
) -> subprocess.CompletedProcess[str]:
    argv = command_argv(command)
    if final_argument is not None:
        argv.append(final_argument)
    return subprocess.run(
        argv,
        cwd=workdir,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def combined_output(result: subprocess.CompletedProcess[str], *, max_lines: int) -> str:
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    return "\n".join(output.splitlines()[-max_lines:])


def append_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=True, sort_keys=True) + "\n")


def evidence_digest(evidence: str) -> str:
    return hashlib.sha256(evidence.encode("utf-8")).hexdigest()[:16]


def git_paths(workdir: Path) -> set[str]:
    commands = (
        ["git", "diff", "--name-only", "--relative"],
        ["git", "diff", "--cached", "--name-only", "--relative"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    )
    paths: set[str] = set()
    for argv in commands:
        result = subprocess.run(argv, cwd=workdir, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "workdir is not a Git repository")
        paths.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return paths


def path_matches(path: str, boundary: str) -> bool:
    normalized_path = Path(path).as_posix().removeprefix("./")
    normalized_boundary = Path(boundary).as_posix().removeprefix("./").rstrip("/")
    if any(character in normalized_boundary for character in "*?["):
        return fnmatch.fnmatch(normalized_path, normalized_boundary)
    return normalized_path == normalized_boundary or normalized_path.startswith(normalized_boundary + "/")


def receipt_base(run_id: str, status: str, evidence: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "status": status,
        "timestamp": utc_now(),
        "evidence_digest": evidence_digest(evidence),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover-command", required=True, help="exit 0 for no drift, 1 for confirmed drift")
    parser.add_argument("--agent-command", help="agent CLI; the bounded patch prompt is appended as one argument")
    parser.add_argument("--verify-command", help="deterministic command that must pass after an agent edit")
    parser.add_argument("--workdir", type=Path, default=Path.cwd(), help="clean Git branch or worktree")
    parser.add_argument(
        "--state",
        type=Path,
        default=Path(".loop-state/docs-drift.jsonl"),
        help="durable JSONL receipt log",
    )
    parser.add_argument("--allowed-path", action="append", default=[], help="allowed file or directory; repeat as needed")
    parser.add_argument(
        "--generated-path",
        action="append",
        default=[],
        help="generated path requiring owner review; repeat as needed",
    )
    parser.add_argument("--max-attempts", type=int, default=2, help="maximum agent attempts")
    parser.add_argument("--max-changed-files", type=int, default=8, help="hard file-count boundary")
    parser.add_argument("--command-timeout", type=int, default=900, help="seconds allowed per command")
    parser.add_argument("--evidence-lines", type=int, default=120, help="maximum detector/verifier lines in a prompt")
    parser.add_argument("--report-only", action="store_true", help="persist drift evidence and escalate without an agent")
    parser.add_argument("--dry-run", action="store_true", help="run discovery and print the decision without writing state")
    args = parser.parse_args()

    if min(args.max_attempts, args.max_changed_files, args.command_timeout, args.evidence_lines) < 1:
        parser.error("budgets and evidence-lines must be positive")

    workdir = args.workdir.resolve()
    state = args.state if args.state.is_absolute() else workdir / args.state
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    try:
        discovery = run_command(args.discover_command, workdir=workdir, timeout=args.command_timeout)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        evidence = f"discovery could not complete: {error}"
        if not args.dry_run:
            append_receipt(state, {**receipt_base(run_id, "escalated", evidence), "reason": evidence})
        print(f"[docs-drift] {evidence}", file=sys.stderr)
        return EXIT_ERROR

    evidence = combined_output(discovery, max_lines=args.evidence_lines)
    if discovery.returncode == 0:
        decision = {"run_id": run_id, "status": "no_drift", "detector_exit": 0}
        if args.dry_run:
            print(json.dumps(decision, indent=2))
        else:
            append_receipt(state, {**receipt_base(run_id, "no_drift", evidence), "detector_exit": 0})
            print("[docs-drift] no confirmed drift")
        return EXIT_OK

    if discovery.returncode != 1 or not evidence:
        reason = (
            f"detector exited {discovery.returncode}; expected 0 (clean) or 1 (drift)"
            if discovery.returncode != 1
            else "detector reported drift without evidence"
        )
        if not args.dry_run:
            append_receipt(
                state,
                {
                    **receipt_base(run_id, "escalated", evidence or reason),
                    "detector_exit": discovery.returncode,
                    "reason": reason,
                },
            )
        print(f"[docs-drift] {reason}", file=sys.stderr)
        return EXIT_ERROR

    if args.dry_run:
        print(
            json.dumps(
                {
                    "run_id": run_id,
                    "status": "drift_detected",
                    "detector_exit": discovery.returncode,
                    "evidence": evidence,
                },
                indent=2,
            )
        )
        return EXIT_OK

    if args.report_only:
        append_receipt(
            state,
            {
                **receipt_base(run_id, "reported", evidence),
                "detector_exit": discovery.returncode,
                "evidence": evidence,
                "reason": "confirmed drift requires a patch or owner decision",
            },
        )
        print(evidence)
        print("[docs-drift] report persisted; escalating", file=sys.stderr)
        return EXIT_ESCALATED

    if not args.agent_command or not args.verify_command or not args.allowed_path:
        parser.error("patch mode requires --agent-command, --verify-command, and at least one --allowed-path")

    try:
        dirty_before = git_paths(workdir)
    except RuntimeError as error:
        append_receipt(state, {**receipt_base(run_id, "escalated", evidence), "reason": str(error)})
        print(f"[docs-drift] {error}", file=sys.stderr)
        return EXIT_ERROR

    if dirty_before:
        reason = "workdir must be clean before patch mode: " + ", ".join(sorted(dirty_before))
        append_receipt(state, {**receipt_base(run_id, "escalated", evidence), "reason": reason})
        print(f"[docs-drift] {reason}", file=sys.stderr)
        return EXIT_ESCALATED

    try:
        state_relative = state.resolve().relative_to(workdir)
    except ValueError:
        state_relative = None
    if state_relative is not None:
        ignored = subprocess.run(
            ["git", "check-ignore", "--quiet", state_relative.as_posix()],
            cwd=workdir,
            check=False,
        )
        if ignored.returncode != 0:
            reason = "state path must be outside the worktree or ignored by Git: " + state_relative.as_posix()
            print(f"[docs-drift] {reason}", file=sys.stderr)
            return EXIT_ERROR

    previous_verify_digest = ""
    for attempt in range(1, args.max_attempts + 1):
        prompt = "\n".join(
            [
                "You are the implementer inside a bounded documentation-drift loop.",
                "",
                "Confirmed detector evidence:",
                "---",
                evidence,
                "---",
                "",
                f"Attempt: {attempt} of {args.max_attempts}",
                "Allowed paths: " + ", ".join(args.allowed_path),
                "Generated or owner-controlled paths: " + (", ".join(args.generated_path) or "none declared"),
                "",
                "Rules:",
                "- Confirm the mismatch against code, tests, schema, or runtime output before editing.",
                "- Make the smallest source-document change that resolves the confirmed mismatch.",
                "- Do not edit generated or owner-controlled paths; report the source that must be regenerated.",
                "- Do not change product behavior, public APIs, tests, policies, or verification commands.",
                "- Do not commit, push, merge, expose credentials, or expand permissions.",
                "- Do not decide completion; the loop runs an independent verifier.",
            ]
        )

        try:
            agent = run_command(
                args.agent_command,
                workdir=workdir,
                timeout=args.command_timeout,
                final_argument=prompt,
            )
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            append_receipt(
                state,
                {
                    **receipt_base(run_id, "retry", evidence),
                    "attempt": attempt,
                    "reason": f"agent could not complete: {error}",
                },
            )
            continue

        try:
            changed = sorted(git_paths(workdir))
        except RuntimeError as error:
            append_receipt(state, {**receipt_base(run_id, "escalated", evidence), "reason": str(error)})
            return EXIT_ERROR

        outside = [path for path in changed if not any(path_matches(path, item) for item in args.allowed_path)]
        generated = [path for path in changed if any(path_matches(path, item) for item in args.generated_path)]
        if len(changed) > args.max_changed_files or outside or generated:
            reasons: list[str] = []
            if len(changed) > args.max_changed_files:
                reasons.append(f"{len(changed)} files exceed the {args.max_changed_files}-file budget")
            if outside:
                reasons.append("out-of-scope paths: " + ", ".join(outside))
            if generated:
                reasons.append("generated or owner-controlled paths: " + ", ".join(generated))
            reason = "; ".join(reasons)
            append_receipt(
                state,
                {
                    **receipt_base(run_id, "escalated", evidence),
                    "attempt": attempt,
                    "changed_paths": changed,
                    "reason": reason,
                },
            )
            print(f"[docs-drift] {reason}; inspect the worktree", file=sys.stderr)
            return EXIT_ESCALATED

        if agent.returncode != 0:
            agent_evidence = combined_output(agent, max_lines=args.evidence_lines)
            append_receipt(
                state,
                {
                    **receipt_base(run_id, "retry", agent_evidence or evidence),
                    "attempt": attempt,
                    "agent_exit": agent.returncode,
                    "changed_paths": changed,
                    "reason": "agent command failed",
                },
            )
            evidence = agent_evidence or evidence
            continue

        if not changed:
            append_receipt(
                state,
                {
                    **receipt_base(run_id, "retry", evidence),
                    "attempt": attempt,
                    "agent_exit": agent.returncode,
                    "changed_paths": [],
                    "reason": "agent produced no file change",
                },
            )
            continue

        try:
            verification = run_command(args.verify_command, workdir=workdir, timeout=args.command_timeout)
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            verify_evidence = f"verifier could not complete: {error}"
            verify_exit = None
        else:
            verify_evidence = combined_output(verification, max_lines=args.evidence_lines)
            verify_exit = verification.returncode

        receipt = {
            **receipt_base(run_id, "verified" if verify_exit == 0 else "retry", verify_evidence or evidence),
            "attempt": attempt,
            "agent_exit": agent.returncode,
            "verify_exit": verify_exit,
            "changed_paths": changed,
            "verification": verify_evidence,
        }
        append_receipt(state, receipt)

        if verify_exit == 0:
            print("[docs-drift] patch passed the external verifier")
            return EXIT_OK

        current_digest = evidence_digest(verify_evidence)
        if current_digest == previous_verify_digest:
            evidence = verify_evidence or evidence
            break
        previous_verify_digest = current_digest
        evidence = verify_evidence or evidence

    reason = "retry budget exhausted or verifier evidence repeated"
    append_receipt(state, {**receipt_base(run_id, "escalated", evidence), "reason": reason})
    print(f"[docs-drift] {reason}; inspect the worktree", file=sys.stderr)
    return EXIT_ESCALATED


if __name__ == "__main__":
    raise SystemExit(main())
