# Loop Pattern Library

This directory turns Loop Engineering principles into practical operating patterns. Each pattern sits above prompt, context, and harness choices: it decides when to trigger agents, what context and tools they get, how work is verified, what state survives, and when the loop repeats or escalates. Each pattern is intentionally small enough to adapt to Codex, Claude Code, GitHub Agentic Workflows, shell scripts, or custom agent runtimes.

Use a pattern when you can name:

- the objective;
- the trigger or cadence;
- the work intake;
- the agent roles;
- the workspace and permission boundary;
- the deterministic verification gate;
- the durable state;
- the retry budget;
- the exit condition;
- the escalation path.
- the loop instruction or automation artifact.

## Patterns

- [PR babysitter](pr-babysitter.md) - Watch PR comments, CI, conflicts, and readiness.
- [CI repair loop](ci-repair-loop.md) - Reproduce failing checks, patch narrowly, and rerun evidence.
- [Docs drift collector](docs-drift-collector.md) - Detect and patch code/docs mismatch.
- [Deploy verifier](deploy-verifier.md) - Watch rollout signals and stop on anomalies.
- [Feedback clusterer](feedback-clusterer.md) - Turn raw feedback streams into actionable themes.

## Pattern Quality Bar

A good loop pattern should be boring in the right places. The goal, allowed actions, deterministic verification gate, retry budget, and stop condition should be explicit before the agent starts doing work.

Avoid patterns that depend only on the model saying "looks good". Prefer checks with exit codes, changed files, issue links, trace IDs, dashboards, screenshots, or reviewer decisions.
