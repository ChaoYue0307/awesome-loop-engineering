# Roadmap

Prioritize stronger evidence, runnable implementations, and measured operating results.

Use the role-based [Future Directions agenda](FUTURE-DIRECTIONS.md) to choose research questions, infrastructure priorities, application opportunities, measurable outputs, and starter projects.

## Near Term

- Collect more direct Loop Engineering sources as the term stabilizes.
- Add real or anonymized gallery entries from practitioners running recurring agent loops.
- Turn more validated contracts into runtime-specific executables with crash recovery, timeouts, replayable receipts, and failure-injection tests.
- Add more translations for the introduction, mental model, Loop Contract, and contribution guide.
- Audit contextual sources in small batches; replace weak summaries and secondary links with canonical evidence.
- Replace unstable links with primary sources, official docs, papers, or implementation-heavy write-ups.

## Pattern Library

The library now contains 20 reference patterns: PR babysitting, CI repair, docs drift, deploy verification, feedback clustering, dependency triage, evaluation regression, security review, cost control, bug hunting, enterprise approval, incident response, data quality, release notes, model routing, benchmark optimization, knowledge freshness, performance regression, accessibility regression, and adversarial red teaming. Every pattern ships a schema-validated loop contract in `examples/`.

Next pattern-library work should prioritize variants backed by operational evidence rather than adding names for coverage. Useful additions include runtime-specific implementations, before/after receipts, measured retry and cost budgets, failure cases, and human-escalation outcomes.

## Community And Adoption

- Publish a concise monthly Discussions digest with corrected annotations, new primary sources, and open contributor tasks.
- Keep several narrowly scoped `good first issue` and `help wanted` tasks available for source audits, translations, runnable examples, and gallery case studies.
- Ask cited authors to review their annotations; request corrections, not promotion or stars.
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
- Describe Awesome Loop Engineering as an early field guide, not a finished standard.
- Preserve clean owner-only commit identity for `main`.

## Open Questions

- Which Loop Contract fields preserve their semantics across session, CI, scheduled, and durable runtimes?
- How should benchmarks separate model, harness, verifier, and outer-loop effects under matched budgets?
- Which verification gates remain calibrated under distribution shift and adversarial pressure?
- Which receipt format is sufficient for replay, incident review, and human escalation without retaining sensitive data?
- How should maintainers evaluate real-world loop examples without exposing private inputs, state, or traces?
