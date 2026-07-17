# Loop Engineering Taxonomy

Classify an AI-agent loop by its trigger, work intake, verification method, state model, agent topology, and operating domain.

## By Trigger

- **Scheduled loop**: runs on a cadence such as hourly, daily, weekly, or during a rollout window.
- **Event-triggered loop**: starts from a webhook, failed check, new comment, issue label, release event, or alert.
- **Goal-driven loop**: continues until a verifiable goal is met, such as passing tests or resolving all blocking comments.
- **Manual bootstrap loop**: starts from a human command, then follows a repeatable contract with state, verification, and exit rules.

## By Work Intake

- **Queue loop**: consumes work from issues, PRs, tickets, alerts, feedback streams, or triage inboxes.
- **Scan loop**: periodically searches a repository, dashboard, logs, docs, or benchmark output for new work.
- **Reactive loop**: responds to a specific failure signal such as CI, eval regression, deploy anomaly, or user report.

## By Verification

- **Deterministic loop**: uses tests, typechecks, lint, schemas, dashboards, or threshold checks as the main gate.
- **Evaluator loop**: uses a second model, rubric, reviewer, or judge agent to evaluate output.
- **Human-supervised loop**: requires human approval before sensitive actions or before completion is accepted.
- **Receipt-based loop**: records evidence such as commands, logs, trace IDs, screenshots, PR links, or issue comments.

## By State Model

- **Stateless retry loop**: feeds immediate failure evidence back into one session. Useful but fragile.
- **File-backed loop**: stores progress in `PROGRESS.md`, task files, runbooks, or generated reports.
- **Issue-backed loop**: stores progress in GitHub, Linear, Jira, Slack, or another system of record.
- **Checkpointed loop**: persists structured state in a database, workflow engine, trace store, or event log.

## By Agent Topology

- **Single-agent loop**: one agent acts, with deterministic checks or human review.
- **Maker-checker loop**: one agent changes the artifact and another verifies it.
- **Manager-worker loop**: an orchestrator decomposes work and assigns specialized agents.
- **Adversarial loop**: reviewer, critic, or security agents try to falsify the maker's output.

## By Operating Domain

- **Repository loop**: PR babysitting, CI repair, bug hunting, docs drift, dependency triage.
- **Release loop**: deploy verification, canary monitoring, rollback recommendation, incident handoff.
- **Feedback loop**: user feedback clustering, issue deduplication, community triage, roadmap signal collection.
- **Evaluation loop**: recurring benchmark runs, trace review, regression detection, prompt or harness hill-climbing.

## Maturity Path

Most teams should move in this order:

1. Manual bootstrap loop with explicit state.
1. Scheduled or event-triggered loop with deterministic gates.
1. Maker-checker loop with durable receipts.
1. Multi-agent or workflow-backed loop.
1. Production-supervised loop with observability, approvals, budgets, and rollback rules.

Higher maturity is not automatically better. The right loop is the simplest loop that can safely discover work, delegate, verify, persist state, decide the next action, and stop.
