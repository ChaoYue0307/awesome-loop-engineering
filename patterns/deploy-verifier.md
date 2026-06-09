# Deploy Verifier

## Objective

Watch a rollout after deployment, compare live signals against release expectations, and escalate quickly when anomalies appear.

## Trigger

- Event: deployment starts, canary advances, feature flag flips, migration completes, or release tag is created.
- Schedule: every 5-15 minutes during the rollout window.
- Manual bootstrap/debug command: "verify deploy <version> until stable or blocked."

## Intake

- Release notes, expected changes, dashboards, logs, traces, error budgets, synthetic checks, feature flags, and rollback instructions.
- Known risky areas and owner contacts.

## Agents

- Observer: gathers metrics, logs, traces, and check status.
- Comparator: compares observed signals against release expectations and baseline.
- Reporter: writes concise rollout status.
- Escalator: notifies humans when thresholds or unknowns are crossed.

## Workspace And Permissions

- Prefer read-only access to observability systems.
- Allow comments, status updates, and issue creation.
- Require human approval for rollback, config changes, traffic shifting, database actions, or incident declaration.

## Durable State

- Release version, rollout phase, baseline window, checked dashboards, anomalies, decisions, and timestamps.

## Loop Steps

1. Load release expectations and rollback criteria.
1. Snapshot key metrics before or at rollout start.
1. Delegate observation, comparison, reporting, and escalation to separate roles when the rollout is complex.
1. Poll signals on the defined cadence.
1. Compare against baseline and explicit thresholds.
1. Report stable, degraded, blocked, or unknown.
1. Escalate if thresholds are crossed or evidence is missing.
1. Stop when the rollout window completes or a human takes over.

## Verification Gates

- Synthetic checks pass.
- Error rate, latency, saturation, and business metrics stay within thresholds.
- Logs/traces show no new dominant failure mode.
- Feature flag or deployment status matches the expected phase.

## Budget And Exit

- Max runtime: the rollout window plus one confirmation interval.
- Max unknown intervals: 2 before escalation.
- Stop when the deploy is stable, rolled back, paused, or handed to an incident owner.

## Escalation

Escalate on threshold breach, missing telemetry, unclear ownership, migration errors, customer-impacting regressions, or rollback criteria.

## Loop Instruction

```text
Verify deploy <version>. Use the release notes and rollout checklist as the contract.
Poll the required dashboards, logs, traces, synthetic checks, and feature flag state.
Report stable/degraded/blocked with evidence. Do not roll back or change production without human approval.
```

Example automation: trigger when a deployment starts or a feature flag changes, then poll every 5-15 minutes until stable, paused, rolled back, or handed to a human.

## Failure Modes

- The loop trusts a single green dashboard while logs show a new error class.
- Baseline windows are mismatched to traffic patterns.
- Missing telemetry is treated as healthy.
- The agent takes production action without approval.

## References

- [OpenAI Agents SDK human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) - Describes approval boundaries for sensitive agent actions.
- [OpenTelemetry Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/) - Provides tracing vocabulary for model, tool, and agent workflow receipts.
