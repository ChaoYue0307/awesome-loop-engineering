# Canonical Definition

Use this page when you need a short, stable definition of Loop Engineering.

## Short Definition

**Loop Engineering** is the AI and coding-agent practice of designing recurring systems that discover work, delegate it to agents, verify results, persist state, decide next actions, and run again on a cadence, event, or until a verifiable goal is reached.

## One-Sentence Positioning

Prompt engineering improves what you ask the model, context engineering improves what the model can see, harness engineering improves the environment around one agent run, and Loop Engineering governs repeated agent work over time.

## Longer Definition

Loop Engineering sits above prompt, context, and harness engineering. It turns agent work from turn-by-turn human prompting into a reviewable operating contract: what starts the loop, where work comes from, which agents act, what context and tools they receive, how results are verified, what state survives, when retry is allowed, and when a human takes over.

## Minimal Loop Test

A system is probably practicing Loop Engineering when it can answer:

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

If you cite this repository, use the BibTeX entry in [`README.md`](README.md#citation) or [`CITATION.bib`](CITATION.bib). If you quote the concept definition, prefer linking to this page so readers can see the scope boundary.
