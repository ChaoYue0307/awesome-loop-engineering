# Agent Memory Lifecycle Loop

## Objective

Keep recurring agent work from cold-starting every run while the memory that carries between runs stays governed: explicitly written, scoped on recall, audited, consolidated, and deletable.

## Use This When

- An agent runs repeatedly against the same project, product, or user and repeats mistakes it already made.
- Prior-session state materially changes what the next run should do.
- Unbounded transcript carryover has caused stale, contradictory, or sensitive context to leak into later runs.

Use the knowledge-freshness loop when the durable product is a retrieval corpus assembled from external sources. Use this pattern when the durable product is the agent's own operational memory: lessons, decisions, preferences, warnings, and open threads.

## Trigger

- Schedule: consolidation pass daily or weekly; audit pass on a longer cadence.
- Event: session end, task completion, memory-store size or age threshold, or a policy change that affects retention.
- Manual bootstrap: "consolidate and audit the agent memory for <project>."

## Intake

- Candidate writes from recent runs: lessons, decisions, preferences, failures worth remembering.
- The current memory store with per-record provenance, timestamps, and access class.
- Retention, privacy, and escalation policy for what may be remembered at all.

## Agents

- Recorder: distills a finished run into explicit candidate records, never raw transcripts.
- Auditor: flags stale, contradictory, sensitive, or unattributed records.
- Consolidator: merges duplicates, promotes repeated lessons to principles, and prunes superseded records.
- Recall gate: scopes what each future run may read, by task and access class.

## Workspace And Permissions

- Memory writes go to a staging area; promotion to the live store is a separate gated step.
- Allow reads of run artifacts and the live store; allow writes only to staging and the audit log.
- Disallow storing raw transcripts, credentials, or personal data barred by policy, and disallow silent deletion of audited records.

## Durable State

- The memory store itself: typed records with provenance, scope, timestamps, and expiry or review dates.
- Audit log of writes, merges, prunes, redactions, and the run that caused each.
- Consolidation receipts: what was merged or promoted, and which records were retired.

## Loop Steps

1. Collect candidate records from runs since the last pass.
1. Reject candidates that violate retention or privacy policy at write time.
1. Deduplicate against the live store; merge near-duplicates with provenance preserved.
1. Audit the live store for staleness, contradiction, and scope creep; quarantine failures.
1. Consolidate repeated instance-level lessons into principle-level records.
1. Apply expiries: delete, redact, or send to review anything past its window.
1. Write the receipt and update recall scopes for the next run.

## Verification Gates

- Every record has provenance, a scope, and an expiry or review date.
- No raw transcript, credential, or policy-barred content is present in the live store.
- Contradictory records cannot coexist unresolved; the newer record must cite what it supersedes.
- Recall tests confirm the next run retrieves the intended records and nothing out of scope.
- Deletions and redactions are logged and reversible for the review window.

## Budget And Exit

- Max runtime: 30-60 minutes per consolidation pass.
- Max churn: cap the fraction of the store that one pass may merge or delete.
- Stop when candidates are exhausted, the churn cap is reached, or the audit finds policy failures that need a human.

## Escalation

Escalate for sensitive or ambiguous records, contradictions between an operator instruction and remembered preference, retention-policy questions, and any suspected memory-injection artifact: records whose provenance does not trace to a legitimate run.

## Loop Instruction

```text
Consolidate agent memory for <project>.
Distill recent runs into explicit candidate records; never store raw transcripts.
Deduplicate, audit for staleness and contradiction, consolidate repeated lessons into principles,
and apply expiries with logged, reversible deletions.
Verify recall scope with test queries before finishing.
Escalate sensitive records, unresolved contradictions, and any record whose provenance
does not trace to a legitimate run.
```

## Worked Example

A team runs a nightly PR-babysitter loop over one repository. Its weekly memory pass distills the week's runs into candidate lessons, merges three near-duplicate records about a flaky integration test into one principle with provenance, expires a remembered workaround that a merged fix made obsolete, quarantines one record whose provenance traces to no known run, and verifies with test recalls that the next babysitter run retrieves the flaky-test principle but not the retired workaround.

## Failure Modes

- Remembering transcripts instead of distilled records, so recall floods future runs with stale context.
- Treating the most recent or most assertive record as true when records contradict.
- Memory that only grows: no expiry, no consolidation, no deletion path.
- Poisoned records entering the store because writes are not gated by provenance checks.
- Recall without scoping, so unrelated tasks read each other's remembered state.

## Example Contract

- [`examples/agent-memory-lifecycle-loop.json`](../examples/agent-memory-lifecycle-loop.json)

## References

- [Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents](https://arxiv.org/abs/2606.30306) - Finds the literature over-indexes on accumulating state and under-indexes on governing, recovering, or deleting it.
- [The Compliance Trap: Diagnosing How AI Agents Consume Conflicting Memory](https://arxiv.org/abs/2607.10608) - Shows agents tend to comply with the most recent or most assertive memory record rather than the correct one.
- [When Claws Remember but Do Not Tell: Stealthy Memory Injection in Persistent Personal Agents](https://arxiv.org/abs/2607.05189) - Demonstrates why memory writes need provenance gates: one poisoned input can silently steer future unattended runs.
