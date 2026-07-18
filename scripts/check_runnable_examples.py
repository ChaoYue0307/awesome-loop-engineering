#!/usr/bin/env python3
"""Smoke-test the dependency-light runnable loop examples."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNABLE = ROOT / "examples" / "runnable"
DOCS_DRIFT = RUNNABLE / "docs-drift" / "docs-drift-loop.py"


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    expected: tuple[int, ...] = (0,),
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, check=False, timeout=30)
    if result.returncode not in expected:
        raise RuntimeError(
            f"command failed ({result.returncode}): {shlex.join(argv)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main() -> int:
    run(["bash", "-n", str(RUNNABLE / "test-repair-loop.sh"), str(RUNNABLE / "threshold-monitor-loop.sh")])
    run([sys.executable, "-m", "py_compile", str(RUNNABLE / "queue-worker-loop.py"), str(DOCS_DRIFT)])

    with tempfile.TemporaryDirectory(prefix="ale-runnable-") as temporary:
        temp = Path(temporary)
        queue = temp / "queue.jsonl"
        write(queue, '{"id":"docs-1","objective":"Check the docs"}\n')
        run([sys.executable, str(RUNNABLE / "queue-worker-loop.py"), "--queue", str(queue), "--dry-run"])

        monitor_state = temp / "monitor.md"
        monitor_env = {
            **os.environ,
            "PROBE_CMD": "printf '42\\n'",
            "THRESHOLD": "100",
            "MAX_SAMPLES": "1",
            "PROGRESS_FILE": str(monitor_state),
        }
        run(["bash", str(RUNNABLE / "threshold-monitor-loop.sh")], env=monitor_env)

        detector_clean = temp / "detector-clean.py"
        write(detector_clean, "raise SystemExit(0)\n")
        state = temp / "docs-drift.jsonl"
        run(
            [
                sys.executable,
                str(DOCS_DRIFT),
                "--discover-command",
                shlex.join([sys.executable, str(detector_clean)]),
                "--state",
                str(state),
            ]
        )
        receipt = json.loads(state.read_text(encoding="utf-8").splitlines()[-1])
        if receipt["status"] != "no_drift":
            raise RuntimeError("docs-drift no-work exit did not persist a no_drift receipt")

        detector_drift = temp / "detector-drift.py"
        write(detector_drift, "print('README output differs from current CLI help')\nraise SystemExit(1)\n")
        dry_run = run(
            [
                sys.executable,
                str(DOCS_DRIFT),
                "--discover-command",
                shlex.join([sys.executable, str(detector_drift)]),
                "--dry-run",
            ]
        )
        if json.loads(dry_run.stdout)["status"] != "drift_detected":
            raise RuntimeError("docs-drift dry run did not expose confirmed evidence")

        report_state = temp / "report-state.jsonl"
        run(
            [
                sys.executable,
                str(DOCS_DRIFT),
                "--discover-command",
                shlex.join([sys.executable, str(detector_drift)]),
                "--report-only",
                "--state",
                str(report_state),
            ],
            expected=(2,),
        )
        report_receipt = json.loads(report_state.read_text(encoding="utf-8").splitlines()[-1])
        if report_receipt["status"] != "reported":
            raise RuntimeError("docs-drift report-only mode did not persist an escalation receipt")

        repository = temp / "repo"
        repository.mkdir()
        write(repository / "README.md", "old command\n")
        run(["git", "init", "-q"], cwd=repository)
        run(["git", "add", "README.md"], cwd=repository)
        run(
            [
                "git",
                "-c",
                "user.name=Loop Smoke Test",
                "-c",
                "user.email=loop-smoke@example.com",
                "commit",
                "-qm",
                "fixture",
            ],
            cwd=repository,
        )

        agent = temp / "agent.py"
        verifier = temp / "verifier.py"
        write(agent, "from pathlib import Path\nPath('README.md').write_text('current command\\n', encoding='utf-8')\n")
        write(
            verifier,
            "from pathlib import Path\nraise SystemExit(0 if Path('README.md').read_text(encoding='utf-8') == 'current command\\n' else 1)\n",
        )
        patch_state = temp / "patch-state.jsonl"
        run(
            [
                sys.executable,
                str(DOCS_DRIFT),
                "--discover-command",
                shlex.join([sys.executable, str(detector_drift)]),
                "--agent-command",
                shlex.join([sys.executable, str(agent)]),
                "--verify-command",
                shlex.join([sys.executable, str(verifier)]),
                "--allowed-path",
                "README.md",
                "--workdir",
                str(repository),
                "--state",
                str(patch_state),
            ]
        )
        patch_receipt = json.loads(patch_state.read_text(encoding="utf-8").splitlines()[-1])
        if patch_receipt["status"] != "verified" or patch_receipt["changed_paths"] != ["README.md"]:
            raise RuntimeError("docs-drift patch mode did not persist a verified scoped change")

        run(["git", "restore", "README.md"], cwd=repository)
        unsafe_agent = temp / "unsafe-agent.py"
        write(unsafe_agent, "from pathlib import Path\nPath('outside.txt').write_text('unsafe\\n')\nraise SystemExit(1)\n")
        unsafe_state = temp / "unsafe-state.jsonl"
        run(
            [
                sys.executable,
                str(DOCS_DRIFT),
                "--discover-command",
                shlex.join([sys.executable, str(detector_drift)]),
                "--agent-command",
                shlex.join([sys.executable, str(unsafe_agent)]),
                "--verify-command",
                shlex.join([sys.executable, str(verifier)]),
                "--allowed-path",
                "README.md",
                "--workdir",
                str(repository),
                "--state",
                str(unsafe_state),
            ],
            expected=(2,),
        )
        unsafe_receipt = json.loads(unsafe_state.read_text(encoding="utf-8").splitlines()[-1])
        if unsafe_receipt["status"] != "escalated" or "out-of-scope paths" not in unsafe_receipt["reason"]:
            raise RuntimeError("docs-drift did not stop an out-of-scope edit from a failed agent command")

    print("Runnable loop smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
