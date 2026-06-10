# Cost-Control Loop

## Objective

Keep long-running agent workflows within budget by measuring usage, identifying waste, and proposing scoped efficiency improvements.

## Trigger

- Schedule: daily or weekly usage review.
- Event: spend threshold exceeded, token or tool-call spike, long-running loop budget exceeded, or abnormal retry volume.
- Manual bootstrap/debug command: "investigate agent cost increase for this workflow."

## Intake

- Token usage, model calls, tool calls, retries, runtime, trace IDs, workflow IDs, success rates, and recent prompt/context/harness changes.
- Budget policy and cost thresholds.
- Known expensive tasks and accepted exceptions.

## Agents

- Analyst: clusters usage by workflow, task type, model, tool, and retry cause.
- Investigator: inspects traces for waste patterns and repeated failures.
- Optimizer: proposes smaller context, cheaper model routing, caching, batching, or early-exit changes.
- Verifier: reruns sample tasks or evals to confirm quality is preserved.
- Reporter: records savings estimate, quality risk, and rollout plan.

## Workspace And Permissions

- Use read-only access to traces, billing exports, dashboards, and workflow configs by default.
- Allow small config or prompt changes only when verified against representative tasks.
- Disallow silent quality-reducing changes, disabling verification gates, or changing production routing without approval.

## Durable State

- Baseline spend, usage clusters, trace samples, suspected waste causes, proposed changes, verification results, and accepted exceptions.

## Loop Steps

1. Discover spend, token, retry, or runtime anomalies.
1. Load budget policy, prior exceptions, and recent workflow changes.
1. Delegate usage clustering, trace inspection, optimization proposals, verification, and reporting.
1. Identify whether cost comes from context bloat, retries, tool latency, model choice, poor batching, or missing stop conditions.
1. Propose the smallest cost-control change.
1. Verify quality with tests, evals, or representative trace replay.
1. Persist before/after evidence and escalate risky routing changes.

## Verification Gates

- Before/after usage is measured with the same task mix or an explicitly comparable sample.
- Quality gates, evals, or reviewer checks still pass.
- Savings estimates include uncertainty and sample size.
- The loop keeps verification and escalation intact.

## Budget And Exit

- Max retries: 2 optimization attempts per workflow.
- Max runtime: 60 minutes per usage review.
- Stop when spend returns below threshold, the cause is explained, a safe optimization is proposed, or quality tradeoffs require owner approval.

## Escalation

Escalate for product-quality tradeoffs, model-routing policy changes, production rollout, customer impact, budget policy changes, or unknown spend sources.

## Loop Instruction

```text
Investigate agent workflow cost for <workflow or period>.
Cluster usage by workflow, task type, model, tool calls, retries, and runtime.
Inspect traces for repeated failures, context bloat, expensive tools, or missing stop conditions.
Suggest only scoped changes that preserve quality gates.
Report before/after metrics, quality evidence, and any escalation needs.
```

Example automation: trigger when spend, tokens, retries, or runtime exceed thresholds for a workflow over a rolling window.

## Failure Modes

- Reducing cost by removing verification.
- Optimizing on an unrepresentative sample.
- Confusing one-off backfills with steady-state cost.
- Hiding quality regressions behind aggregate spend improvements.

## References

- [OpenAI Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability) - Traces and observability for agent workflows.
- [AgentOps](https://github.com/AgentOps-AI/agentops) - Monitoring, replay, cost tracking, benchmarking, and tracing for agent sessions.
- [Engineering Agentic Systems for Reliability](https://pruningmypothos.com/systems/engineering-agentic-systems-for-reliability/) - Reliability framing for observability and boundary failures.
