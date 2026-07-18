# Comparison Guide

Loop Engineering is easiest to understand by separating it from nearby practices.

## Model-Level Recurrence vs Loop Engineering

**Model-level recurrence** repeats a learned layer, block, module, or latent-state update inside one model inference. It can provide adaptive depth, latent reasoning, parameter sharing, or iterative world-state refinement.

**Loop Engineering** governs repeated agent work outside the model: what triggers a run, which work enters, what tools and permissions apply, what external evidence gates progress, what state survives, and when the system retries, escalates, or stops.

A looped Transformer, recurrent-depth language model, or LoopWM can be the model inside an agent loop. It does not replace the Loop Contract because hidden-state iteration alone does not provide durable receipts, independent verification, permission boundaries, or accountable human handoff.

## Prompt Engineering vs Loop Engineering

**Prompt Engineering** asks: what should I say to the model now?

**Loop Engineering** asks: what system should discover work, delegate to agents, verify results, persist state, decide next actions, and rerun?

Prompt engineering can be part of a loop instruction, but a good prompt alone is not a loop.

## Context Engineering vs Loop Engineering

**Context Engineering** asks: what state, memory, documents, examples, and tool results should the model see?

**Loop Engineering** asks: when should context be loaded, what state should survive across runs, and how should that state affect the next run?

Context engineering improves the input to an agent. Loop Engineering governs recurring agent work over time.

## Harness Engineering vs Loop Engineering

**Harness Engineering** asks: what tools, permissions, sandboxes, tests, traces, and feedback surround one agent run?

**Loop Engineering** asks: how should repeated agent runs use those harnesses to act, verify, record receipts, retry, and escalate?

Harness engineering makes a run safer and more observable. Loop Engineering decides when and why that run happens again.

## Workflow Automation vs Loop Engineering

**Workflow automation** executes predefined steps.

**Loop Engineering** coordinates agentic work that may require discovery, delegation, tool use, verification, state updates, and next-action decisions.

Many loops use workflow automation. Not every workflow automation is Loop Engineering.

## Agent Workflow vs Loop Engineering

**Agent workflows** describe how models, tools, and agents solve a task.

**Loop Engineering** describes how work recurs: what triggers it, what state persists, what gates completion, when retry is allowed, and when humans take over.

An agent workflow can be the inner mechanism. The loop is the operating system around repeated work.

## Evaluation Loop vs Operational Loop

**Evaluation loops** repeatedly measure and improve prompts, tools, models, or harnesses.

**Operational loops** repeatedly perform engineering work such as PR babysitting, CI repair, docs drift collection, feedback clustering, or deploy verification.

Both are valid Loop Engineering patterns when they have a clear trigger, state, verification, budget, and exit.

## Quick Test

Ask these questions before calling something Loop Engineering:

1. Does it run more than once by design?
1. Does it discover or receive work from a real source?
1. Does it delegate work to one or more agents?
1. Does it verify results with explicit gates?
1. Does it persist state or receipts outside the model context?
1. Does it decide whether to repeat, report, escalate, or stop?

If the answer is mostly no, it may be prompt engineering, context engineering, harness engineering, or automation, but it is probably not Loop Engineering.
