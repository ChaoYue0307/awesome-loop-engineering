# Knowledge Freshness Loop

## Objective

Keep an agent's retrieval corpus aligned with authoritative sources without silently promoting stale, untrusted, or low-quality content.

## Use This When

- An agent answers from a maintained document or retrieval index.
- Source documents change independently of the agent application.
- You can test freshness, provenance, retrieval quality, and answer grounding before promotion.

Use the docs-drift loop for documentation inside one codebase. Use this pattern when the durable product is a knowledge corpus or retrieval index assembled from multiple sources.

## Trigger

- Schedule: daily or weekly source refresh.
- Event: source webhook, policy update, new release, or expired freshness window.
- Manual bootstrap: "refresh and validate the <knowledge base> index."

## Intake

- Authoritative source registry, allowed domains, owners, and freshness policy.
- Changed documents, current corpus manifest, parser/index versions, and retrieval eval set.
- Data-classification, deletion, retention, and access-control rules.

## Agents

- Source monitor: detects additions, updates, removals, and ownership changes.
- Curator: resolves duplicates, metadata, authority, and scope.
- Indexer: builds a versioned candidate corpus.
- Evaluator: tests freshness, provenance, retrieval, and grounded answers.

## Workspace And Permissions

- Build a candidate index separate from production.
- Allow reads only from the source registry and writes only to the candidate corpus and manifest.
- Disallow new domains, privilege expansion, source deletion, or production promotion without policy checks.

## Durable State

- Source manifest with canonical URL, owner, checksum, fetched time, parser version, access class, tombstones, and accepted exceptions.
- Candidate index version, eval results, promotion decision, and rollback pointer.

## Loop Steps

1. Compare the source registry with the last accepted manifest.
1. Fetch only changed or expired sources and record provenance.
1. Quarantine parse failures, unauthorized sources, and ambiguous duplicates.
1. Build a versioned candidate corpus and retrieval index.
1. Run freshness, coverage, leakage, retrieval, and grounded-answer evaluations.
1. Promote atomically only when every hard gate passes; otherwise keep production unchanged.
1. Record the receipt, tombstones, exceptions, and next refresh time.

## Verification Gates

- Every chunk maps to an allowed canonical source and current access policy.
- Required sources are within their freshness window; removals are tombstoned.
- Retrieval quality and grounded-answer scores stay above the accepted baseline.
- Sensitive or revoked content is absent from the candidate index.
- Promotion is versioned, atomic, and reversible.

## Budget And Exit

- Max retries: 2 fetch or indexing attempts per source version.
- Max runtime: 120 minutes per refresh.
- Stop on successful promotion, no changed sources, budget exhaustion, policy failure, or evaluation regression.

## Escalation

Escalate for conflicting authoritative sources, access-policy changes, parser corruption, sensitive-data detection, or quality/freshness trade-offs that require an owner decision.

## Loop Instruction

```text
Refresh <knowledge base> from the approved source registry.
Build a versioned candidate index; never write directly to production.
Record canonical source, checksum, fetch time, parser version, and access class for every item.
Run freshness, provenance, retrieval, leakage, and grounded-answer gates.
Promote atomically only if every hard gate passes; otherwise preserve production and
write an escalation receipt with the failed sources and metrics.
```

## Worked Example

A support agent uses product docs, release notes, and policy pages. The daily loop detects two changed releases and one removed policy, rebuilds a candidate index, verifies that deprecated guidance is no longer retrieved, runs 50 frozen support questions, and promotes the new index only when citation coverage and answer accuracy remain above baseline.

## Failure Modes

- Updating vectors without updating source metadata or tombstones.
- Treating a successful fetch as proof that the content is authoritative.
- Promoting an index that is fresh but retrieves worse answers.
- Retaining revoked or access-restricted content in caches.
- Rebuilding everything every run and losing change attribution.

## Example Contract

- [`examples/knowledge-freshness-loop.json`](../examples/knowledge-freshness-loop.json)

## References

- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670) - Frames agent memory as a write-manage-read loop requiring explicit maintenance and evaluation.
- [Are We Ready for an Agent-Native Memory System?](https://arxiv.org/abs/2606.24775) - Evaluates memory systems as representation, extraction, retrieval, and maintenance modules.
