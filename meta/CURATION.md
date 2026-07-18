# Curation Standard

Include only recurring AI-agent and coding-agent systems with explicit triggers, verification, durable state, budgets, escalation, and exit. General agent links belong elsewhere.

## Acceptance Test

A resource belongs when it passes all three checks:

1. **Scope fit**: It covers AI/coding-agent loops or a direct foundation for repeated runs that discover work, delegate, verify, persist state, decide next actions, and escalate.
1. **Builder value**: It helps someone design, run, verify, evaluate, operate, or critique recurring agent systems.
1. **Inspectable evidence**: It is public, specific, and stable enough for readers to verify.

## Strong Signals

Prefer resources with one or more of these properties:

- Primary source from the author, project, vendor, or research team.
- Official docs for an agent runtime, SDK, workflow system, benchmark, or eval framework.
- Concrete implementation detail: commands, architecture, traces, code, loop instructions, automation configs, hooks, schedules, state files, worktrees, checks, or failure modes.
- Durable research foundation: ReAct, reflection, self-correction, planning, memory, tool use, evaluation, or state.
- Operational value: CI repair, PR babysitting, deploy verification, docs drift, feedback clustering, cost control, or escalation.

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

## Editorial Responsibility And Assistance

The maintainer owns every released inclusion decision, category, annotation, and project-level claim. Automation may assist discovery, URL resolution, duplicate detection, bibliographic extraction, repository statistics, and draft normalization. Automated output is not evidence; canonical sources, primary metadata, and stated limitations control the final entry.

The public dataset keeps those layers separate:

- `annotation`, `key_contribution`, `novelty`, and `impact` are original editorial syntheses;
- `source_title`, `source_description`, authorship, date, venue, DOI, and repository statistics come from the source audit and record their metadata provenance;
- `evidence_tier` records whether the row is a primary source, implementation-grounded practitioner source, or curated synthesis;
- `loop_layer` records whether recurrence lives inside the model, agent, harness, workflow, operations, evaluation, or spans layers;
- `scope_fit` records whether a resource directly describes operational Loop Engineering, enables it, or is an explicitly adjacent foundation;
- `signal_strength` describes the kind of evidence available, not whether the maintainer agrees with the work;
- `source_status` records reachability at one point in time and is not a guarantee of future availability.

No author, company, venue, star count, or citation count can buy or guarantee placement. Vendor inclusion does not imply endorsement, and inclusion of a critique does not imply that every claim in it is accepted.

## Corrections And Disputes

Accuracy corrections take priority over expansion. Authors and readers can submit the [annotation-correction form](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=annotation-correction.yml) or a pull request with the current entry, the disputed text, the proposed correction, and primary-source evidence.

When evidence conflicts:

1. prefer the original publishing venue, official documentation, paper record, or repository over secondary coverage;
1. distinguish a verified fact from editorial interpretation;
1. preserve material caveats, negative results, and stated evaluation limits;
1. omit a date, venue, author, or metric rather than infer it from an unreliable source;
1. record the correction in the next release notes when it changes the meaning of an entry.

## Audit And Versioning

`data/resource_source_audit.csv` is the inspectable point-in-time audit log. `data/resources.csv` and `data/resources.jsonl` are deterministic exports of the canonical English README enriched with that audit. GitHub Releases identify versioned snapshots; downstream users should cite a release or commit when reproducibility matters.

## Annotation Rules

Each annotation should answer: **why does this matter for Loop Engineering?** Lead with the mechanism, result, use case, or limitation. Avoid self-referential openings such as "this paper explores" or "this page provides."

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
