# Loop Gallery

The gallery is for real-world or realistic loop examples contributed by the community.

Use it to show how a loop works in practice, not just what resources describe it. A good gallery entry should be concrete enough that another builder can adapt the pattern without guessing the trigger, state, verification, or escalation rules.

## Contribution Format

Create one file per loop:

```text
gallery/<short-loop-name>.md
```

Use [`gallery/template.md`](template.md) as the starting point.

## Reference Entries

These entries are reference examples, not claimed production deployments. They show the level of specificity expected from future real or anonymized gallery contributions.

- [PR babysitter reference loop](pr-babysitter-reference.md)
- [CI repair reference loop](ci-repair-reference.md)
- [Docs drift reference loop](docs-drift-reference.md)

## Quality Bar

Gallery entries should include:

- the runtime or tool used;
- trigger or cadence;
- work intake source;
- agent roles or delegation pattern;
- workspace and permissions;
- verification gates;
- durable state artifact;
- retry budget and stop condition;
- escalation path;
- screenshots, PR links, issue links, trace IDs, or anonymized receipts when available;
- lessons learned.

Do not include secrets, private customer data, proprietary code, or internal links that readers cannot inspect. If a real example cannot be public, write an anonymized version and say which details were generalized.

## Minimum Useful Case Study

An entry is worth publishing once it answers all of these. If you cannot fill one in, say so explicitly rather than inventing it.

- [ ] **Objective**: the single outcome the loop optimizes for.
- [ ] **Trigger**: schedule, event, or manual bootstrap.
- [ ] **Intake**: where the loop finds work each run.
- [ ] **Runtime / tool**: which runtime and agent system ran it.
- [ ] **Agent roles**: who explores, acts, checks, and decides.
- [ ] **Verification**: the deterministic gate that decided done.
- [ ] **State**: what survived between runs, and where.
- [ ] **Budget**: the retry or runtime cap.
- [ ] **Escalation**: when and how a human took over.
- [ ] **Receipts**: public or anonymized evidence (PR, issue, trace, dashboard, commands).
- [ ] **Lesson learned**: what changed after the loop met reality.

## Safe Anonymization Checklist

Run this before publishing a real-world entry:

- [ ] Remove secrets, tokens, keys, and credentials.
- [ ] Remove private customer data and any PII.
- [ ] Remove internal URLs, hostnames, and dashboards readers cannot reach.
- [ ] Replace personal names with roles (for example "the on-call engineer", "the reviewer").
- [ ] Include only public or anonymized receipts; redact anything in a screenshot you would not paste in plain text.
- [ ] State which details were generalized so readers know what was changed.

## Suggested First Gallery Entries

- PR babysitter loop for a small open-source repository.
- CI repair loop that turns failed checks into small verified patches.
- Docs drift loop that compares CLI output with README examples.
- Deploy verifier loop that watches dashboards and escalates on threshold breaches.
- Feedback clusterer loop that groups issues or support tickets into themes.
