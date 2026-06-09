# Awesome Loop Engineering v0.1.0

Loop Engineering is the layer above prompt, context, and harness engineering.

Prompt engineering improves what you ask the model. Context engineering improves what the model can see. Harness engineering improves the tools, permissions, sandboxes, checks, and feedback around one agent run. Loop Engineering asks a different question: what recurring system should discover work, delegate to agents, verify results, persist state, decide next actions, and run again?

## Why This Matters

Coding-agent work is moving from turn-by-turn prompting toward recurring operating systems for agent work. A useful loop can wake up on a schedule or event, inspect a real work source, load durable context, act in an isolated workspace, verify with explicit gates, record receipts, and decide whether to repeat, report, or escalate.

That shift is powerful, but it is also risky. Loops can burn tokens, repeat mistakes, hide state, or take unsafe actions if they are not bounded. The craft is not "let the agent run forever." The craft is designing the contract that keeps repeated agent work reviewable.

## What The Repo Adds

Awesome Loop Engineering collects and organizes:

- direct Loop Engineering explainers;
- official runtime docs for schedules, goals, worktrees, hooks, skills, plugins, subagents, and workflows;
- research foundations for ReAct, reflection, self-correction, planning, memory, and tool use;
- coding-agent systems and benchmarks;
- verification, observability, and feedback-gate resources;
- practical pattern docs for PR babysitting, CI repair, docs drift, deploy verification, and feedback clustering;
- a loop contract schema with validated examples;
- anti-patterns, taxonomy, comparison guide, manifesto, and sourced signals.

## The Core Contract

A loop should make these parts visible:

1. Objective
1. Trigger
1. Discover / intake
1. Workspace
1. Context
1. Delegation
1. Verification
1. State
1. Budget
1. Escalation
1. Exit

If those parts are missing, the loop usually becomes either a manual prompt habit or unsafe background automation.

## How To Contribute

The most valuable contributions are:

- direct sources about Loop Engineering in the AI/coding-agent sense;
- concrete loop patterns with trigger, state, verification, budget, and escalation;
- public or anonymized gallery entries from real loops;
- corrections to weak annotations, unstable links, or category placement;
- translations that preserve the narrow scope.

Repo:

[github.com/ChaoYue0307/awesome-loop-engineering](https://github.com/ChaoYue0307/awesome-loop-engineering)

Landing page:

[chaoyue0307.github.io/awesome-loop-engineering](https://chaoyue0307.github.io/awesome-loop-engineering/)

Community pattern thread:

[What loop patterns are you using?](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/1)

This is an early curated field guide, not a final standard. Corrections and stronger sources are welcome.
