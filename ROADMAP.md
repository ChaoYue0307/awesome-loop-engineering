# Roadmap

This roadmap keeps Awesome Loop Engineering focused on useful, verifiable work for an emerging practice.

## Near Term

- Collect more direct Loop Engineering sources as the term stabilizes.
- Add real or anonymized gallery entries from practitioners running recurring agent loops.
- Grow the runnable loop directory beyond the test-repair reference loop, including scheduled-trigger variants per runtime.
- Add more translations for the introduction, mental model, Loop Contract, and contribution guide.
- Audit contextual sources in small batches and replace weak summaries or secondary links with stronger canonical evidence.
- Continue replacing weak or unstable links with primary sources, official docs, papers, and implementation-heavy write-ups.

## Pattern Library

The library now contains 15 reference patterns: PR babysitting, CI repair, docs drift, deploy verification, feedback clustering, dependency triage, evaluation regression, security review, cost control, bug hunting, enterprise approval, incident response, data quality, release notes, and model routing. Every pattern ships a schema-validated loop contract in `examples/`.

Next pattern-library work should prioritize variants backed by operational evidence rather than adding names for coverage. Useful additions include runtime-specific implementations, before/after receipts, measured retry and cost budgets, failure cases, and human-escalation outcomes.

## Community And Adoption

- Publish a concise monthly Discussions digest with corrected annotations, new primary sources, and open contributor tasks.
- Keep several narrowly scoped `good first issue` and `help wanted` tasks available for source audits, translations, runnable examples, and gallery case studies.
- Ask cited authors to review the repository's characterization of their work; request corrections, not promotion or stars.
- Track qualified traffic, forks, watchers, and external contributions after each launch channel while GitHub traffic data is still available.

## Gallery

The gallery should grow from reference examples into public or anonymized case studies. Good entries should include:

- the runtime or agent tool used;
- trigger and intake source;
- verification gates;
- durable state artifact;
- budget and escalation rules;
- receipts or anonymized evidence;
- lessons learned after real use.

## Quality And Governance

- Keep CI dependency-light and easy for contributors to run locally.
- Keep all resource annotations tied to recurring agent systems, not generic AI-agent interest.
- Keep public claims conservative: this repository is an early curated field guide, not a finished standard.
- Preserve clean owner-only commit identity for `main`.

## Open Questions

- Which loop primitives become common across Codex, Claude Code, GitHub Agentic Workflows, and custom runtimes?
- What is the right schema shape for portable loop contracts?
- Which verification gates are strong enough for unattended or semi-attended loops?
- How should maintainers evaluate submitted real-world loop examples without exposing private data?
