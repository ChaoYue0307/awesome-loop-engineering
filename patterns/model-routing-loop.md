# Model-Routing Loop

## Objective

Keep agent work on the right model for each task by routing on measured quality, latency, privacy, and cost, instead of pinning everything to one model and hoping.

## Trigger

- Schedule: daily or weekly review of routing decisions against outcomes.
- Event: a new model ships, a price or latency change lands, or a quality or cost threshold is crossed.
- Manual bootstrap/debug command: "review model routing for <workflow> and propose a safer or cheaper split."

## Intake

- Per-task telemetry: model used, success rate, latency, token cost, and retries.
- The routing policy: task classes, model options, privacy tiers, and fallbacks.
- Eval results and known-sensitive task types that must stay on approved models.

## Context

- Required files: routing policy, privacy and data-residency rules, eval baselines.
- Runtime sources: recent traces, cost and latency dashboards, model availability and pricing.

## Agents

- Analyst: clusters tasks by class and measures quality, latency, and cost per model.
- Proposer: suggests routing changes such as cheaper models for easy classes or fallbacks for hard ones.
- Verifier: replays a representative sample on the proposed routing to confirm quality holds.
- Reporter: records the proposed policy, the evidence, and the privacy constraints checked.

## Workspace And Permissions

- Read access to telemetry, eval results, pricing, and the current routing policy.
- Allowed to run offline replays and open a routing-policy change proposal.
- Disallowed from changing production routing, moving a task to a non-approved model, or crossing a privacy tier without review.
- Production routing changes and any privacy-tier change require human approval.

## Durable State

- Task-class definitions, per-model metrics, proposed routes, replay results, and privacy checks.
- A routing decision log so changes are auditable and reversible.

## Loop Steps

1. Load telemetry, the routing policy, and eval baselines.
1. Cluster tasks by class and compute quality, latency, and cost per model.
1. Identify classes that are over-served (too expensive) or under-served (too weak).
1. Propose the smallest routing change that preserves quality and privacy.
1. Replay a representative sample on the proposed routing and compare against baseline.
1. Persist the proposal, evidence, and privacy checks; open a change proposal.
1. Stop when a safe proposal is ready, no change is warranted, or a tradeoff needs an owner.

## Verification Gates

- Proposed routes are replayed on a representative sample, not argued from price alone.
- Quality on each affected class stays within the agreed tolerance of baseline.
- Privacy and data-residency constraints are checked for every rerouted class.
- Cost and latency deltas are reported with sample size and variance.

## Budget And Exit

- Max retries: 2 replay-and-adjust passes per task class.
- Max runtime: 60-120 minutes per routing review.
- Stop when a safe proposal is ready, the current routing is already optimal, or a tradeoff needs owner approval.

## Escalation

Escalate for quality-versus-cost tradeoffs, privacy-tier changes, data-residency questions, a model deprecation that forces migration, or customer-impacting latency changes.

## Loop Instruction

```text
Review model routing for <workflow>.
Cluster tasks by class and measure quality, latency, and cost per model.
Propose the smallest routing change that preserves quality and privacy, then replay a representative sample to confirm.
Report cost and latency deltas with sample size; check privacy and residency for every rerouted class.
Do not change production routing or cross a privacy tier without human approval.
```

Example automation: run weekly, or trigger when a new model ships or a cost or latency threshold is crossed, then open a routing-policy proposal for review.

## Failure Modes

- Routing on price alone and quietly degrading quality on hard task classes.
- Optimizing on an unrepresentative sample that misses the long tail.
- Moving a sensitive task to a cheaper model that violates a privacy tier.
- Flapping between models as short-term metrics wobble.

## Safety Notes

- Privacy tier and data residency are hard constraints, never traded for cost.
- Keep a fast rollback to the prior routing if a change regresses in production.
- Verify quality with replays and evals before any production routing change.

## Example Contract

- [`examples/model-routing-loop.json`](../examples/model-routing-loop.json)

## References

- [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability) - Traces as the basis for measuring and routing agent work.
- [Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals) - Using evals as the signal for changing how agents run.
