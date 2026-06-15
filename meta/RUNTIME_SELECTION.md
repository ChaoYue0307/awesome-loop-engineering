# Runtime Selection Guide

A loop is a design; a runtime is where it runs. The same [Loop Contract](../README.md#the-loop-contract) can run as a session-scoped command, a scheduled cloud job, a CI workflow, or a cron wrapper. This guide helps you pick deliberately.

Behavior of hosted products changes; treat the vendor-specific rows as a starting point and confirm current limits, triggers, and permissions in each product's official docs before relying on them unattended.

## Quick Comparison

| Runtime | Runs where | Persistence | Local file access | Isolated workspace | Permission model | Best for | Avoid when |
| ------- | ---------- | ----------- | ----------------- | ------------------ | ---------------- | -------- | ---------- |
| Claude Code `/loop` | Your machine, inside an open session | Within the session | Yes, your working tree | Use a worktree yourself | Interactive session permissions | Active development iteration with you nearby | You need it to run while the app is closed |
| Claude Code Desktop scheduled tasks | Your machine, via the desktop app | Across runs, while the app can run | Yes, local files | Use a worktree yourself | Local app permissions | Recurring local jobs that need your filesystem | The machine or app is often closed at run time |
| Claude remote routines | Anthropic-managed cloud | Across runs, laptop closed | Cloned repo only, per run | Yes, fresh clone per run | Scoped env, connectors, branch-push limits | Unattended cloud jobs on schedules, API, or GitHub events | You need direct access to local, non-Git files |
| Codex automations | Cloud / background | Across runs | Cloned repo / worktree | Yes, worktree isolation | Automation + connector scope | Recurring background tasks and triage inboxes | You want everything on your own infrastructure |
| GitHub Agentic Workflows | GitHub Actions runner | Per run, plus repo artifacts | Checked-out repo | Yes, containerized job | Actions permissions and guardrails | Event- or schedule-triggered repo automation | The work is not tied to a GitHub repository |
| Shell/cron + agent CLI | Any machine or server you control | Whatever you write to disk | Full, by default | Only if you add it | Whatever the OS user can do | Maximum control and portability | You do not want to own isolation and secrets |
| Custom durable workflow runtime | Your infrastructure | Crash-proof, durable | Depends on your setup | Yes, you design it | Your own policy layer | Production-grade long-running loops with recovery | A small job that a simpler runtime already covers |

## Choosing By Concern

### Persistence

- Session-scoped (`/loop`) state lives only as long as the session; write a progress file if you need more.
- Desktop scheduled tasks and most cloud runtimes persist across runs, but **always keep durable state in a file, issue, or database**, never only in model memory.
- For loops that must survive crashes and resume exactly where they stopped, use a durable execution runtime.

### Local file access

- If the loop must touch files that are not in a Git repository, prefer a local runtime (`/loop`, desktop scheduled tasks, or shell/cron).
- Cloud runtimes generally operate on a cloned repository per run; work that depends on local, uncommitted files does not fit them well.

### Isolated workspace

- Cloud and CI runtimes give you a fresh, isolated workspace per run by default.
- Local runtimes do not isolate automatically: run them inside a [worktree](../README.md#core-loop-primitives), branch, or sandbox so a loop cannot corrupt your main checkout.

### Permission model

- The safest unattended loops are read-mostly with a narrow, explicit set of write actions.
- Scope network access, secrets, and branch-push rights to exactly what the loop needs. See [Securing Unattended Loops](../README.md#securing-unattended-loops).
- Prefer runtimes that let you cap permissions per job over ones that inherit your full local privileges.

### Verification strategy

- Keep the verification gate deterministic and outside the acting agent: an exit code, a passing check, a schema validation, an eval threshold.
- CI runtimes make required status checks the natural gate.
- Local and cloud runtimes should call the same check command your contract names, and judge the result by exit code, not by the agent's say-so.

### Escalation strategy

- Every runtime needs a defined human exit: a PR, an issue, a Slack or pager message, or a labeled triage inbox.
- Cloud and CI runtimes pair naturally with PR and issue escalation.
- Long-running and incident-style loops should page a human; never let a loop substitute confidence for an owner.

## Migration Path

Most teams climb the [Loop Maturity Model](../README.md#loop-maturity-model) by changing runtime, not rewriting the loop:

1. Prototype interactively with `/loop` or a [shell/cron wrapper](../examples/runnable/shell-cron-loop.md).
1. Move recurring local work to desktop scheduled tasks.
1. Promote unattended work to cloud routines, Codex automations, or GitHub Agentic Workflows.
1. Graduate production-critical, crash-sensitive loops to a durable execution runtime.

Keep the contract stable across the move; only the trigger, isolation, and permission wiring change.

## See Also

- [Runnable loop variants](../examples/runnable/README.md) - concrete templates for each runtime.
- [Core Loop Primitives](../README.md#core-loop-primitives) and [Official Runtime Guides](../README.md#official-runtime-guides) - the primary-source docs behind each runtime.
- [Pattern matrix](../patterns/MATRIX.md) - suggested runtime fit per pattern.
