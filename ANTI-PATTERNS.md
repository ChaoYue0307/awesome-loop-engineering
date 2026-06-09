# Loop Engineering Anti-Patterns

Use this page to reject unsafe, vague, or misleading loop designs.

## Prompt Loop With No Contract

**Symptom:** A script repeatedly asks an agent to "keep improving" without a named objective, intake, state, verification, or exit condition.

**Why it fails:** The loop becomes a manual prompting habit disguised as automation.

**Better:** Define the loop contract before running: objective, trigger, intake, workspace, context, delegation, verification, state, budget, escalation, and exit.

## Infinite Retry Loop

**Symptom:** The loop keeps feeding failures back to the agent indefinitely.

**Why it fails:** Cost grows, context degrades, and the loop may repeatedly damage the same files.

**Better:** Set retry budgets per blocker, stop on repeated failures, and escalate with evidence.

## Model Self-Approval

**Symptom:** The same agent that made the change decides that the work is complete.

**Why it fails:** Models can rationalize their own mistakes and miss regressions they introduced.

**Better:** Use deterministic checks, a separate verifier agent, or human review for completion gates.

## Hidden State

**Symptom:** The only memory is inside the conversation.

**Why it fails:** The next run cannot reliably know what was tried, what passed, what failed, or what remains.

**Better:** Persist state in files, issues, comments, checkpoints, traces, or workflow state.

## Unsafe Production Autonomy

**Symptom:** A loop can deploy, roll back, change config, rotate secrets, or modify data without explicit approval boundaries.

**Why it fails:** A small model error can become an operational incident.

**Better:** Make sensitive actions approval-gated and document rollback, escalation, and owner rules.

## Generic Automation Rebranded As Loop Engineering

**Symptom:** A cron job or workflow runs without agentic reasoning, context loading, verification, or stateful next-action decisions.

**Why it fails:** It blurs Loop Engineering with ordinary automation.

**Better:** Call ordinary automation ordinary automation. Use Loop Engineering when repeated agent work is actually being triggered, bounded, verified, persisted, and rerun.

## Context Dump Loop

**Symptom:** Each run gives the agent a huge context bundle instead of a curated state contract.

**Why it fails:** The loop becomes slow, expensive, and hard to debug.

**Better:** Separate durable state from supporting context. Load only the state, docs, examples, and receipts needed for the current objective.

## No Escalation Path

**Symptom:** The loop keeps acting even when it lacks credentials, sees ambiguous product requirements, hits flaky infrastructure, or needs architectural judgment.

**Why it fails:** The agent spends budget where a human decision is required.

**Better:** Define escalation triggers and include the evidence a human needs to take over.

## No Receipts

**Symptom:** The loop says it is done without commands, logs, changed files, trace IDs, dashboard snapshots, reviewer decisions, or links.

**Why it fails:** Maintainers cannot audit the loop or trust its result.

**Better:** Require receipts as part of the exit gate.
