# Contributing

Contribute a canonical source, an evidence-backed correction, or a loop you have run.

Contributions must address recurring AI-agent or coding-agent systems with explicit triggers, work intake, verification, durable state, budgets, escalation, and exit.

Before submitting, read the [curation standard](meta/CURATION.md). It defines scope, evidence tiers, annotation rules, and correction handling.

## Fastest Contribution (Under Five Minutes)

Use the [resource suggestion form](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=resource-suggestion.yml) to propose one source without preparing a fork. Include:

- the canonical public URL;
- the most specific README category;
- one sentence on the contribution, novelty, or practical value for recurring agent systems;
- the source type and evidence tier;
- any caveat, such as vendor bias, a paywall, early-stage status, or weak evidence.

Maintainers apply the same scope, duplication, source-quality, and annotation checks used for pull requests. Corrections are equally valuable: link the current entry and state the exact change.

For an inaccurate summary, contribution, novelty, impact, authorship, date, venue, identifier, or canonical link, use the [annotation-correction form](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml). Include primary-source evidence; omit unavailable metadata rather than guessing.

## Quick PR Flow

1. Search `README.md` for the resource title, author, project, and URL.
1. Confirm the resource is about AI/coding-agent Loop Engineering or a direct foundation for it.
1. Pick the most specific category.
1. Add one metadata-rich row with a resource type label, verified year/source context, and one specific key feature:

```md
| 📄 **[Title](https://example.com)**<br><sub>Paper</sub> | **2026** · arXiv<br><sub>First Author et al.</sub> | One sentence explaining the resource's contribution to Loop Engineering. |
```

When a source exposes no reliable publication date, omit the year and keep only the original venue or publishing platform. Do not infer a date from a search-result snippet. Maintainers regenerate the table layout and structured exports after review.

1. Open a PR using the template and explain:
   - why the resource belongs;
   - which category it updates;
   - whether it is a primary source, official documentation, paper, tool, benchmark, playbook, critique, or adjacent list;
   - the evidence quality tier and resource type label;
   - any caveat such as vendor bias, paywall, early-stage status, or weak evidence.

If automated tools assisted discovery, extraction, or drafting, say so in the PR. Check every resulting claim against the canonical source; generated text is not evidence.

## License For Contributions

By contributing to this repository, you agree that your contribution to this repository's curation text, annotations, templates, patterns, metadata, and documentation is released under [CC0-1.0](LICENSE).

Do not copy third-party articles, papers, images, documentation, code, or other content into this repository unless you have the right to do so. Prefer stable links and short original annotations. External resources keep their own licenses and terms.

## What Belongs Here

Good additions usually fit one of these groups:

- Direct explanations of Loop Engineering in the AI/coding-agent sense.
- Papers that introduce agent loops, reflection, critique, verification, planning, tool use, or memory patterns used by looped agents.
- Official docs for agent runtimes, hooks, subagents, skills, guardrails, observability, MCP, worktrees, automations, goals, or state persistence.
- Engineering blogs with concrete implementation details, failure modes, or production lessons.
- Benchmarks and eval systems for long-horizon, tool-using, or coding agents.
- Playbooks for recurring agent work such as PR babysitting, CI repair, issue triage, deploy verification, bug hunting, docs drift collection, and feedback clustering.
- Critiques that clarify when loops are risky, wasteful, or not yet justified.
- Translation improvements that make the concept accessible without changing the scope.

## What Does Not Belong Here

Please avoid submitting:

- Software event loops, UI event loops, game loops, control theory loops, growth loops, or generic feedback-loop content unless it is explicitly applied to AI agent loops.
- Generic prompt engineering resources with no loop, tool, verification, state, or scheduling angle.
- Generic context or harness engineering resources unless they directly explain how repeated agent runs are triggered, verified, persisted, or governed.
- Resources that only improve single-turn prompts belong in prompt-engineering lists unless they show scheduling, state, verification, retries, or escalation.
- Generic agent news, product launches, or listicles without technical substance.
- Private, unstable, or paywalled sources that most readers cannot inspect.
- Duplicate resources already covered by an existing entry.
- Pure marketing pages with no reusable technical insight.

## Evidence Quality

Prefer higher tiers when two resources cover the same idea.

| Tier | Source type | Examples |
| --- | --- | --- |
| A | Primary source or official docs | Tool docs, paper, project README, author write-up |
| B | Practitioner write-up with implementation detail | Field notes, playbooks, postmortems |
| C | Curated survey or high-quality explainer | Taxonomy, comparison, tutorial |
| D | Commentary or news coverage | Useful only when it documents origin, adoption, or debate |

If two links cover the same idea, prefer the more primary, stable, and implementation-specific source.

## Quality Labels

Use these labels in PR descriptions and issue suggestions when they help reviewers understand why a resource belongs:

- **Primary source**: written by the original author, project, vendor, or research team.
- **Official docs**: documentation for a runtime, SDK, API, benchmark, or platform.
- **Implementation-heavy**: includes code, architecture, commands, traces, or operational details.
- **Foundational**: explains a core loop mechanism such as ReAct, reflection, planning, state, or verification.
- **Cautionary**: clarifies limitations, risks, cost, safety, or when not to use loops.
- **Adjacent**: useful context from prompt, context, harness, eval, or agent engineering.

## Category Guidance

- Use **Start Here** only for direct Loop Engineering explainers.
- Use **The Loop Contract** and **Loop Maturity Model** only for framework-level content, not individual links.
- Use **Core Loop Primitives** for automations, goals, worktrees, hooks, skills, connectors, subagents, and state files.
- Use **Official Runtime Guides** for primary-source docs from tool builders.
- Use **Research Foundations** for papers and reference implementations that explain the mechanics behind agent loops.
- Use **Agent Workflow Patterns** for general workflow architecture, durable execution, and official guidance.
- Use **Coding-Agent Loop Systems** for systems that run agents over repositories, terminals, code, or software issues.
- Use **Verification And Feedback Gates** for tests, evals, CI, tracing, guardrails, deterministic checks, and LLM-as-judge caveats.
- Use **Securing Unattended Loops** for prompt-injection defenses, memory-poisoning attacks and mitigations, sandboxing, permission boundaries, and monitoring of agents that run without a human watching.
- Use **State, Memory, And Context Persistence** for durable state, checkpoints, context, progress files, and memory.
- Use **Orchestration And Multi-Agent Delegation** for subagents, handoffs, manager-worker loops, and workflow runtimes.
- Use **Benchmarks And Evaluation** for benchmarks that measure agent behavior over multi-step tasks.
- Use **Operations Playbooks** for recurring engineering jobs run by agents.
- Use **Templates And Patterns** for reusable pattern docs hosted in this repository.
- Use **Critiques, Risks, And Limitations** for thoughtful warnings and failure analysis.
- Use **Adjacent Awesome Lists** for neighboring maps, not individual resources.

## Annotation Style

Write for the person deciding whether to open or use the source. Lead with the concrete contribution, result, mechanism, or limitation; keep annotations short, specific, and builder-oriented.

Avoid repository-centered or self-referential openings such as "this paper explores," "this page provides," or "this list includes." Name what the work does instead. Replace praise such as "excellent," "comprehensive," or "important" with inspectable evidence, reported measurements, or a precise use case.

Use the resource type legend from `README.md`:

- 📄 **Paper**
- 📝 **Blog**
- 📚 **Docs**
- 🧰 **Tool**
- 🧪 **Benchmark**
- 🔁 **Pattern**
- 🧾 **Template**
- 🧭 **List**
- ⚠️ **Critique**

Prefer:

```md
| 🔁 **[Autonomous Loops](https://example.com)**<br><sub>Pattern</sub> | **2026** · Example publisher | Shows how to combine task files, stop hooks, limits, and kill switches into a self-continuing agent loop. |
```

Avoid:

```md
| 📝 **[Cool Agent Article](https://example.com)**<br><sub>Blog</sub> | **Example publisher** | Interesting article about AI. |
```

## Adding A Loop Pattern

For a practical loop pattern, use [`templates/loop-pattern.md`](templates/loop-pattern.md), optionally structure it with [`schemas/loop-contract.schema.json`](schemas/loop-contract.schema.json), and place the finished pattern in [`patterns/`](patterns/). A good pattern names:

- objective;
- trigger;
- intake source;
- agents and roles;
- workspace and permissions;
- verification gates;
- durable state;
- budget and exit conditions;
- escalation path;
- loop instruction, automation spec, hook config, or scheduled command;
- failure modes.

Pattern PRs should be concrete enough that a reader can adapt them to an agent runtime without guessing the loop contract. If you want feedback before writing the full pattern, open a loop pattern suggestion issue.

## Translation Contributions

See [TRANSLATIONS.md](TRANSLATIONS.md).

Translation PRs should:

- link back to the canonical English README;
- preserve the narrow AI/coding-agent scope;
- keep resource URLs unchanged;
- update language navigation if a new language file is added;
- explain who can help maintain the translation.

## Issues

If you do not want to open a PR, use the resource suggestion issue template. Please include:

- title and URL;
- suggested category;
- resource type label;
- evidence quality tier;
- why it is relevant to Loop Engineering;
- whether it is a direct Loop Engineering source, official docs, paper, engineering note, tool, benchmark, critique, or translation.

## Review Standard

Maintainers may ask for stronger relevance, a more precise category, a better annotation, or removal of promotional language. The goal is to keep the list useful for people designing real agent loops, not to collect every AI-agent link on the internet.
