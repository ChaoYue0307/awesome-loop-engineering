# Loop Engineering Manifesto

Loop Engineering is the practice of designing recurring AI-agent systems whose behavior remains reviewable across runs.

Prompt engineering shapes the instruction. Context engineering shapes what the model can see. Harness engineering shapes one run's tools, permissions, isolation, and checks. Loop Engineering connects those decisions across runs: when agents start, what work enters, who acts, what evidence gates results, what state survives, and when the system repeats, reports, escalates, or stops.

## Why It Exists

Recurring agent work shifts the design problem from the next prompt to the operating system around every run. A useful loop finds work, loads bounded context, acts in isolation, verifies against explicit gates, records receipts, and resumes without relying on human memory.

This does not remove engineering judgment. It makes judgment explicit in the loop contract: objective, trigger, intake, workspace, context, delegation, verification, state, budget, escalation, and exit.

## Core Commitments

- **Design the system, not just the next prompt.** Specify the operating contract instead of steering every turn.
- **Make state external.** Progress files, issue comments, traces, checkpoints, and dashboards should outlive the model context.
- **Separate maker from checker.** The actor must not be the sole judge of completion.
- **Prefer deterministic gates.** Tests, typechecks, evals, dashboards, trace graders, and reviewer decisions are stronger than "looks good".
- **Bound autonomy.** Loops need budgets, allowed actions, disallowed actions, stop conditions, and escalation paths.
- **Keep receipts.** A loop should explain what it saw, what it changed, what it ran, what passed, what failed, and why it stopped.
- **Keep ownership human.** A loop can delegate work; quality, safety, and product judgment remain human responsibilities.

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

Visible answers make the loop reviewable, portable, and improvable.
