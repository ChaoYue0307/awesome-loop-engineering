# CI Repair Loop

## Objective

Turn a failing CI signal into a small, verified fix or a precise escalation note.

## Trigger

- Schedule: poll failing checks on active branches.
- Event: CI check fails on a PR or protected branch.
- Manual bootstrap/debug command: "repair the failing CI check for this PR."

## Intake

- Failed check name, logs, artifacts, commit SHA, changed files, and recent successful run.
- Local test commands from project docs.
- Known flaky-test list or CI status page.

## Agents

- Investigator: extracts the failing command, error, and likely affected files.
- Implementer: makes the smallest patch consistent with the failure.
- Verifier: reruns the local or CI-equivalent command.
- Reporter: summarizes evidence and residual risk.

## Workspace And Permissions

- Use a clean branch or worktree based on the failing commit.
- Allow read access to CI logs and artifacts.
- Allow local test, lint, typecheck, and build commands.
- Disallow unrelated refactors, dependency upgrades, broad formatting, or changes to protected CI config unless explicitly requested.

## Durable State

- Failing check URL, command reproduced, exact error, attempted fixes, passing evidence, and unresolved blockers.

## Loop Steps

1. Fetch the failed check and logs.
1. Identify the deterministic failing command or closest local equivalent.
1. Delegate log extraction, patching, verification, and reporting to separate roles when useful.
1. Reproduce locally when possible.
1. Patch the smallest cause.
1. Rerun the failing command first, then any adjacent cheap checks.
1. If green, summarize and push.
1. If not reproducible or blocked, write an escalation with logs and hypotheses.

## Verification Gates

- The original failing command passes locally or in rerun CI.
- The patch is limited to the failure cause.
- New tests are added when the fix changes behavior.
- Output includes exact commands and relevant log excerpts.

## Budget And Exit

- Max retries: 3 patch attempts.
- Max runtime: 45-90 minutes.
- Stop when the target check passes, the failure is proven flaky, the environment is unavailable, or the fix exceeds scope.

## Escalation

Escalate for flaky infrastructure, missing credentials, third-party outages, nondeterministic failures without reproduction, or changes requiring owner approval.

## Loop Instruction

```text
Repair the failing CI check for <PR or branch>.
Start by identifying the exact failing command and reproducing it locally if possible.
Make the smallest scoped patch, rerun the failing command, and report evidence.
Do not change unrelated files or CI configuration unless the logs prove it is necessary.
```

Example automation: trigger on failed required checks, or poll active PRs for red CI every 30-60 minutes.

## Failure Modes

- Treating a CI artifact as stale without checking commit SHA.
- Running only broad checks and missing the failing command.
- Fixing by weakening tests or deleting assertions.
- Chasing flaky failures without a retry budget.

## References

- [Stop Babysitting Your Coding Agent. Give It Backpressure.](https://generativeprogrammer.com/p/stop-babysitting-your-coding-agent) - Turns tests, linters, builds, and traces into feedback loops for coding agents.
- [GitHub Agentic Workflows](https://github.github.com/gh-aw/) - Runs coding agents from GitHub events or schedules with repository-level guardrails.
