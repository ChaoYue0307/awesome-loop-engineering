# Incident Response Loop

## Objective

Turn a fresh alert into a triaged, evidence-backed incident with a clear owner and a postmortem trail, without an engineer doing the mechanical correlation work by hand.

## Trigger

- Event: pager alert fires, error budget burn crosses a threshold, or a synthetic check fails.
- Schedule: every 2-5 minutes while an incident is open, to refresh signals.
- Manual bootstrap/debug command: "triage incident <id> until owned or resolved."

## Intake

- The alert payload, affected service, severity, and recent deploys or config changes.
- Dashboards, logs, traces, recent incidents, and the service runbook.
- On-call rotation, ownership map, and escalation policy.

## Context

- Required files: incident runbook, service ownership map, severity policy.
- Runtime sources: live metrics, log queries, trace samples, recent change log, pager state.

## Agents

- Observer: gathers metrics, logs, traces, and the recent change timeline.
- Correlator: links the alert to likely causes such as a deploy, dependency, or saturation.
- Reporter: writes a concise incident summary with severity, impact, and current hypothesis.
- Escalator: pages the right owner and hands off when human judgment is required.

## Workspace And Permissions

- Read-only access to observability systems, change logs, and pager state.
- Allowed to open or update an incident record, post status, and page the on-call owner.
- Disallowed from rolling back, restarting services, changing config, or running remediation.
- Any mitigation action is a human decision; the loop prepares it but does not execute it.

## Durable State

- Incident ID, severity, affected service, timeline of signals, hypotheses, and handoffs.
- A running incident log that becomes the seed for the postmortem.

## Loop Steps

1. Ingest the alert and load the service runbook and ownership map.
1. Snapshot metrics, logs, traces, and the recent deploy or config timeline.
1. Correlate the alert with likely causes and assign a working severity.
1. Write or update the incident record with impact and current hypothesis.
1. Page the owning team if severity or staleness thresholds are crossed.
1. Persist the timeline and hand off to a human for any mitigation.
1. Stop when an owner accepts the incident or it auto-resolves with evidence.

## Verification Gates

- Severity is backed by concrete impact evidence, not the raw alert text alone.
- The correlated cause cites specific deploys, logs, traces, or metric changes.
- Missing or stale telemetry is reported as unknown, never as healthy.
- The handoff names an owner and includes a reproducible timeline.

## Budget And Exit

- Max retries: 2 correlation attempts per distinct signal before paging a human.
- Max runtime: the incident lifetime, refreshed each interval until ownership transfers.
- Stop when a human owner accepts the incident, it is mitigated, or it auto-resolves with evidence.

## Escalation

Escalate immediately for customer-facing outages, data loss risk, security signals, missing telemetry, or any case where mitigation requires production action.

## Loop Instruction

```text
Triage incident <id>. Use the runbook and ownership map as the contract.
Snapshot metrics, logs, traces, and recent changes; correlate the alert with likely causes.
Write the incident record with severity, impact, and hypothesis backed by evidence.
Page the owning team on threshold or staleness; never roll back or change production yourself.
Keep a timeline that can seed the postmortem, and hand off to a human for any mitigation.
```

Example automation: trigger on a pager alert or error-budget breach, then refresh every 2-5 minutes until an owner accepts the incident.

## Failure Modes

- The loop declares a cause from a single correlated signal without corroboration.
- Alert storms create duplicate incidents instead of one correlated record.
- Missing telemetry is silently treated as a healthy system.
- The agent drifts toward remediation instead of staying in triage and handoff.

## Safety Notes

- Mitigation is a human action: the loop assembles evidence and pages, it does not act on production.
- Never include secrets, tokens, or customer PII in the incident record or postmortem seed.
- Prefer paging a human early over a confident but unverified auto-diagnosis.

## Example Contract

- [`examples/incident-response-loop.json`](../examples/incident-response-loop.json)

## References

- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) - Approval boundaries for sensitive operations such as production mitigation.
- [OpenTelemetry Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/) - Portable tracing vocabulary for the signals an incident loop correlates.
