# Enterprise Approval Loop

## Objective

Move a permissioned change through required approvals without a human chasing reviewers, while keeping every gate, approver, and decision on the record.

## Trigger

- Schedule: every 1-4 hours during business hours while an approval is open.
- Event: change request opened, policy check completes, approver assigned, or an approval expires.
- Manual bootstrap/debug command: "drive change request <id> to a decision or a clear blocker."

## Intake

- The change request, its linked diff or runbook, required approver list, and policy checklist.
- Status of each required gate: security scan, compliance check, cost review, owner sign-off.
- Prior decisions, comments, and any conditions attached to earlier approvals.

## Context

- Required files: approval policy, `AGENTS.md`, change-management runbook.
- Runtime sources: current approval state, gate results, approver availability, SLA timers.

## Agents

- Explorer: summarizes what the change does and which gates and approvers still block it.
- Coordinator: routes the request to the next required gate or approver and tracks SLAs.
- Reviewer: checks that attached evidence actually satisfies each named policy gate.
- Judge: decides whether to advance, request changes, or escalate to a human owner.

## Workspace And Permissions

- Read approval metadata, gate results, diffs, and policy documents.
- Allowed to comment, request reviews, attach evidence links, and update status fields.
- Disallowed from self-approving, bypassing a gate, editing policy, or merging the change.
- Any state transition that grants access or ships the change requires a named human approver.

## Durable State

- Change request ID, required gates, gate status, approver decisions, conditions, and timestamps.
- An approval ledger entry per run recording what advanced, what blocked, and why.

## Loop Steps

1. Load the change request, required gates, and prior decisions.
1. Classify the current blocker: missing evidence, pending gate, pending approver, or rejection.
1. If evidence is missing and mechanical, attach it from the linked sources.
1. Route the request to the next required gate or approver and record the SLA.
1. Re-check gate and approver status on the next run.
1. Persist the decision trail and notify owners on state changes.
1. Stop when fully approved, rejected, or blocked on a human decision.

## Verification Gates

- Every required gate has a recorded pass, fail, or waiver with an evidence link.
- Each approver decision is attributable to a named human, not the loop.
- The change does not advance while any required gate is unmet.
- The audit trail reconstructs who approved what, when, and under which conditions.

## Budget And Exit

- Max retries: 3 routing attempts per stuck gate before escalation.
- Max runtime: the approval SLA window plus one confirmation interval.
- Stop when the change is fully approved, rejected, or waiting on a human decision.

## Escalation

Escalate when an approver is unresponsive past SLA, a gate fails, a policy is ambiguous, a waiver is requested, or the change touches regulated data or production access.

## Loop Instruction

```text
Drive change request <id> toward a decision.
Read the required gates, approver list, and policy checklist.
Attach only mechanical, sourced evidence; never self-approve or bypass a gate.
Route to the next required gate or approver, record SLAs, and keep an audit trail.
Stop and escalate on gate failure, unresponsive approver, policy ambiguity, or any production or regulated-data step.
```

Example automation: run hourly during business hours while an approval is open, and trigger when a gate completes or an approver is assigned.

## Failure Modes

- The loop treats a stale or cached gate result as current.
- The agent nudges approvers so often it becomes noise.
- An approval condition is recorded but not enforced on the final state.
- The loop advances a change because no gate explicitly said "no" rather than because every gate said "yes".

## Safety Notes

- Approval is a human act: the loop coordinates and documents, it never decides access.
- Keep gate evidence immutable; link to it rather than copying mutable values into the ledger.
- Treat any access grant, production change, or regulated-data step as a hard human-approval boundary.

## Example Contract

- [`examples/enterprise-approval-loop.json`](../examples/enterprise-approval-loop.json)

## References

- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) - Approval and validation boundaries for sensitive agent actions.
- [12 Factor Agents](https://github.com/humanlayer/12-factor-agents) - Operating principles for production agents, including explicit state ownership and human contact points.
