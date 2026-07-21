# Loop-Graph Reference

## Summary

Loop-Graph is a proposed framework for long-horizon LLM agents that combines iterative self-refinement with graph-structured memory. The design treats the reasoning loop and memory substrate as one system: each loop step can retrieve, update, and reuse persistent entities, relationships, and temporal context.

## Paper Details

- Title: Loop Engineering Meets Graph Engineering: A Synergistic Framework for Reliable, Efficient, and Long-Horizon LLM Agents
- Authors: Lingjiao Chen, Matei Zaharia, Jack Clark, Christopher Re, Chelsea Finn, Ion Stoica
- Affiliation: Stanford University
- Framework: Loop-Graph
- Source status: paper screenshot supplied to this repository; replace this reference with the public paper URL when available.

## Reported Evidence

- Evaluation scale: 9,842 real-world tasks across three domains: software engineering, research assistance, and data analysis.
- Baselines: strong state-of-the-art models including GPT-4o, Claude-3-Opus, and Gemini-1.5-Pro with standard prompting and RAG.
- Reported gains: success up to 38.6 percentage points, answer correctness up to 27.4 percentage points, redundant tool calls reduced up to 24.1%, and average latency reduced by 21.7%.

## Why It Matters

The work connects two practical needs that often fail separately in long-running agents: reliable decision loops and durable memory. Loop Engineering supplies the recurring control structure for generation, verification, and refinement; Graph Engineering supplies persistent, structured memory over entities, relationships, and time.

## How To Use The Idea

- Use a graph when the agent must remember entities, dependencies, decisions, or temporal facts across many steps or sessions.
- Put graph retrieval and graph update inside the loop contract, not beside it as an optional RAG step.
- Verify each loop step against both external task evidence and graph consistency before allowing the next action.
- Track redundant tool calls, latency, correctness, and success rate separately, because graph memory can improve reliability while also changing operating cost.

## Fit In This Repository

Loop-Graph belongs in the agent workflow layer rather than the model-recursion layer. It is about governing repeated agent actions and persistent memory across a task horizon, not about reusing a Transformer block inside one model inference.
