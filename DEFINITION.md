# Canonical Definition

Use this definition to scope a system, review a design, or cite the concept consistently.

## Short Definition

**Loop Engineering** is the AI and coding-agent practice of designing recurring systems that discover work, delegate it to agents, verify results, persist state, decide next actions, and run again on a cadence, event, or until a verifiable goal is reached.

## One-Sentence Positioning

Prompt engineering improves what you ask the model, context engineering improves what the model can see, harness engineering improves the environment around one agent run, and Loop Engineering governs repeated agent work over time.

Model-level recurrence is a complementary architecture choice: shared learned computation may repeat inside one inference, while Loop Engineering governs how that model participates in recurring work across runs.

## Longer Definition

Loop Engineering connects prompt, context, and harness decisions across runs. It replaces turn-by-turn human steering with a reviewable operating contract: what starts the loop, where work comes from, which agents act, what they can access, how evidence gates results, what state survives, how retries are bounded, and when a human takes over.

## Minimal Loop Test

A system qualifies when it can answer:

1. What triggers the loop?
1. How does it discover or receive work?
1. What context and tools does it give the agent?
1. What is the workspace and permission boundary?
1. What verifies success or failure?
1. What state persists across runs?
1. What budget limits retries, time, or cost?
1. What causes escalation?
1. What condition ends the loop?

## Citation Note

Use the BibTeX entry in [`README.md`](README.md#citation) or [`CITATION.bib`](CITATION.bib). Link to this page when quoting the definition so readers can inspect the scope boundary.
