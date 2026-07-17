# Curation Standard

This repository is intentionally selective. It should help builders understand and practice Loop Engineering for AI and coding agents as the layer above prompt, context, and harness engineering, not become a general AI-agent link dump.

## Acceptance Test

A resource belongs when it passes all three checks:

1. **Scope fit**: It is about AI/coding-agent loops, or a direct foundation for designing repeated agent runs that discover work, delegate to agents, coordinate context and harnesses, verify results, persist state, decide next actions, and escalate.
1. **Builder value**: It helps someone design, run, verify, evaluate, operate, or critique recurring agent systems.
1. **Stable evidence**: It is public, specific, and stable enough that readers can inspect it later.

## Strong Signals

Prefer resources with one or more of these properties:

- Primary source from the author, project, vendor, or research team.
- Official docs for an agent runtime, SDK, workflow system, benchmark, or eval framework.
- Concrete implementation detail: commands, architecture, traces, code, loop instructions, automation configs, hooks, schedules, state files, worktrees, checks, or failure modes.
- Durable research foundation: ReAct, reflection, self-correction, planning, memory, tool use, evaluation, or state.
- Practical operational value: CI repair, PR babysitting, deploy verification, docs drift, feedback clustering, cost control, or escalation.

## Weak Signals

Usually reject resources that are mostly:

- broad AI-agent trend commentary;
- generic prompt tips with no state, tools, verification, scheduling, or retry loop;
- generic context or harness resources with no repeated-run, state, verification, trigger, or escalation angle;
- pure vendor marketing without technical substance;
- unrelated event loops, growth loops, control theory, game loops, or generic automation;
- private, unstable, paywalled, or hard-to-verify sources;
- duplicated coverage where a primary source is already listed.

## Evidence Tiers

| Tier | Meaning | Typical examples |
| --- | --- | --- |
| A | Primary or official source | Paper, official docs, project README, author write-up |
| B | Practitioner source with implementation detail | Field note, runbook, postmortem, architecture note |
| C | Curated survey or high-quality explainer | Taxonomy, comparison, tutorial |
| D | Commentary or news coverage | Useful only for origin, adoption, quotes, or debate |

Prefer the highest-tier source that explains the same idea clearly.

## Annotation Rules

Each annotation should answer: **why does this matter for Loop Engineering?**

Good:

```md
| 🔁 **[Autonomous Loops](https://example.com)**<br><sub>Pattern</sub> | **2026** · Example publisher | Shows how task files, stop hooks, hard limits, and a kill switch form a self-continuing agent loop. |
```

Weak:

```md
| 📝 **[Cool Agent Article](https://example.com)**<br><sub>Blog</sub> | **Example publisher** | Interesting article about agents. |
```

## Resource Type Labels

Every resource entry in `README.md` should use one visible type label:

- 📄 **Paper**
- 📝 **Blog**
- 📚 **Docs**
- 🧰 **Tool**
- 🧪 **Benchmark**
- 🔁 **Pattern**
- 🧾 **Template**
- 🧭 **List**
- ⚠️ **Critique**

## Pattern Quality Bar

Pattern entries should be concrete enough to adapt to a real agent runtime. A good pattern states:

- objective;
- trigger or cadence;
- intake source;
- agents and roles;
- workspace and permissions;
- durable state;
- verification gates;
- retry budget;
- exit condition;
- escalation path;
- loop instruction, automation spec, hook config, or scheduled command;
- failure modes.

## License Scope

Only original repository curation text, annotations, templates, pattern documents, and metadata are released under `CC0-1.0`. Linked third-party resources keep their own licenses and terms.
