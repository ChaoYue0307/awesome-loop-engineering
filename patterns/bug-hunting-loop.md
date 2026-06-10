# Bug Hunting Loop

## Objective

Find, validate, and report likely bugs with reproducible evidence instead of filing speculative agent-generated issues.

## Trigger

- Schedule: weekly on active modules.
- Event: error logs spike, flaky tests cluster, user reports mention the same behavior, or a release branch opens.
- Manual bootstrap/debug command: "hunt for reproducible bugs in this module."

## Intake

- Recent errors, flaky tests, issue labels, support snippets, changed files, code ownership, logs, traces, and module documentation.
- Existing bug reports and duplicate issue search.
- Safe reproduction commands and test fixtures.

## Agents

- Scout: discovers suspicious signals and likely affected code paths.
- Reproducer: attempts minimal reproduction in a safe environment.
- Minimizer: reduces the reproduction to the smallest failing case.
- Fix suggester: proposes a patch only when the cause is clear.
- Reporter: files evidence-backed issues or PRs.

## Workspace And Permissions

- Use a branch, worktree, sandbox, or read-only mode depending on the target.
- Allow tests, local fixtures, logs, static search, and non-production reproduction.
- Disallow production data access, destructive fuzzing, speculative mass issue creation, or broad refactors.

## Durable State

- Checked modules, signals inspected, duplicate issue search, reproduction steps, commands, expected/actual behavior, traces, screenshots, and final disposition.

## Loop Steps

1. Discover candidate bug signals from tests, logs, issues, traces, or recent diffs.
1. Load ownership docs, existing issues, and prior bug-hunt state.
1. Delegate signal discovery, reproduction, minimization, patch proposal, and reporting.
1. Search for duplicates before filing anything.
1. Reproduce in the smallest safe environment.
1. If root cause is obvious and patch is small, propose a PR with tests.
1. Otherwise file a precise issue with evidence and stop.
1. Persist false positives and checked areas.

## Verification Gates

- A bug report includes reproducible steps or a clear trace/log link.
- A patch includes a failing test or deterministic reproduction when feasible.
- Duplicate issue search is recorded.
- Expected vs actual behavior is grounded in docs, tests, or product requirements.

## Budget And Exit

- Max retries: 3 reproduction attempts per candidate.
- Max runtime: 90 minutes per module or signal cluster.
- Stop when a bug is reproduced and reported, a small verified patch is opened, the signal is classified as non-bug, or owner judgment is needed.

## Escalation

Escalate for production-only bugs, privacy-sensitive logs, ambiguous product behavior, security-sensitive findings, data loss, or broad architectural fixes.

## Loop Instruction

```text
Hunt for reproducible bugs in <module, release, or signal cluster>.
Start from concrete signals: failing tests, logs, traces, issues, or recent changes.
Search for duplicates before filing.
Reproduce safely, minimize the case, and report expected vs actual behavior.
Open a patch only when the cause is clear and verification is available.
```

Example automation: run weekly against modules with recent churn, flaky tests, or repeated user reports.

## Failure Modes

- Filing issues from code smell without reproduction.
- Creating duplicate bug reports.
- Using private logs or customer data as public evidence.
- Patching symptoms while leaving the reproduced cause unexplained.

## References

- [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) - Practical plan-edit-test-observe-repair-document-repeat runbook.
- [SWE-bench](https://www.swebench.com/) - Benchmark framing around real repository issues and tests.
- [Terminal-Bench](https://www.tbench.ai/) - Evaluation context for hard terminal tasks and reproducibility.
