# Loop Engineering Manifesto

Loop Engineering is the practice of designing recurring AI-agent systems that sit above prompt, context, and harness engineering.

Prompt engineering improves what you ask the model. Context engineering improves what the model can see. Harness engineering improves the tools, permissions, sandboxes, and checks around one agent run. Loop Engineering connects those layers over time: it defines when agents run, what work they discover, how work is delegated, how results are verified, what state survives, and when the system repeats, reports, or escalates.

## Why It Exists

The leverage point in agent work is moving from writing better one-off prompts to designing better recurring systems. A useful loop can notice work, load the right context, act in an isolated workspace, verify against explicit gates, record receipts, and continue later without relying on a human to remember every intermediate step.

This does not remove engineering judgment. It moves judgment into the loop contract: objective, trigger, intake, workspace, context, delegation, verification, state, budget, escalation, and exit.

## Core Commitments

- **Design the system, not just the next prompt.** The human should specify the operating contract, not manually steer every turn.
- **Make state external.** Progress files, issue comments, traces, checkpoints, and dashboards should outlive the model context.
- **Separate maker from checker.** The system that acts should not be the only system that decides whether the work is done.
- **Prefer deterministic gates.** Tests, typechecks, evals, dashboards, trace graders, and reviewer decisions are stronger than "looks good".
- **Bound autonomy.** Loops need budgets, allowed actions, disallowed actions, stop conditions, and escalation paths.
- **Keep receipts.** A loop should explain what it saw, what it changed, what it ran, what passed, what failed, and why it stopped.
- **Stay responsible.** A loop can delegate work, but ownership of quality, safety, and product judgment remains human.

## What It Is Not

Loop Engineering is not a new name for every agent, cron job, workflow, or feedback system. It is not software event loops, growth loops, control theory, or generic automation. It is also not prompt engineering with repetition. A loop needs a trigger, work intake, durable state, verification, budget, and exit condition.

## Success Standard

A Loop Engineering artifact is useful when another builder can answer:

1. What starts the loop?
1. How does it discover work?
1. Which agent or role does what?
1. What context and tools are available?
1. What can it change safely?
1. What verifies success or failure?
1. What state is persisted for the next run?
1. What is the retry budget?
1. When does it escalate?
1. When is it done?

If those answers are visible, the loop can be reviewed, shared, improved, and trusted.
