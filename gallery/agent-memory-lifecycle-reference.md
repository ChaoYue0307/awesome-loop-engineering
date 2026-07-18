# Agent Memory Lifecycle Reference Loop

## Summary

A reference design for carrying useful state across recurring agent runs without turning raw transcripts into permanent, ungoverned memory. The loop admits explicit records, recalls only task-relevant state, audits contradictions and retention rules, consolidates duplicates, and forgets or redacts records when policy requires it.

This is a design reference, not a claimed production deployment. It was adapted from [TerminallyLazy's public pattern proposal](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/7); the linked Tree Ring Memory project is an illustrative implementation, not an adoption or reliability claim.

## Runtime Or Tooling

- Runtime: any scheduled, event-driven, or manually bootstrapped agent runtime with a durable local or service-backed store.
- Agent system: operator, bounded worker, memory curator, independent verifier, and human owner.
- Illustrative tooling: [Tree Ring Memory](https://github.com/TerminallyLazy/Tree-Ring-Memory), SQLite/FTS, a project ledger, or another inspectable memory store with deletion support.
- Repository or environment: recurring coding, documentation, release, outreach, or operations work where cold starts cause repeated discovery.

## Loop Contract

- Objective: preserve useful, attributable lessons between runs while preventing stale, sensitive, contradictory, or irrelevant state from silently steering future work.
- Trigger: before and after a bounded agent run, plus a scheduled audit and consolidation pass.
- Discover / intake: the current task, project instructions, approved prior records, public receipts, and explicit operator corrections; never silent terminal or transcript capture.
- Workspace: a scoped project store separate from model context, with retention and access rules reviewed before unattended use.
- Context: task identity, source links, timestamps, confidence, access class, expiry, contradiction links, and the last audit decision.
- Delegation: the operator selects relevant records, the worker acts, the curator proposes writes or consolidation, the verifier checks receipts and policy, and the human owns sensitive or ambiguous decisions.
- Verification: schema and provenance checks, duplicate and contradiction search, retention-policy checks, deterministic project tests, and public or local receipts for consequential actions.
- State: append-only memory records plus indexes, tombstones, consolidation links, audit decisions, and the next review time.
- Budget: cap recalled records, new writes, consolidation operations, and retries per run; stop when the same contradiction or policy failure repeats.
- Escalation: credentials, private data, legal or license questions, conflicting operator decisions, deletion uncertainty, or any memory that would authorize a higher-impact action.
- Exit: the task is externally verified and the memory delta is accepted, or the run stops with an evidence-backed report and named human owner.

## Loop Instruction Or Automation

```text
Before acting, recall only approved records relevant to the current task and cite their IDs.
After acting, propose explicit memory writes with source, timestamp, confidence, retention,
and contradiction links. Run project verification and memory-policy checks independently.
Persist accepted receipts and tombstones outside the model. Never store secrets or raw
transcripts by default. Escalate ambiguous, sensitive, stale, or conflicting state.
```

## Receipts

- Pattern proposal: [issue #7](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/7).
- Inspectable implementation: [Tree Ring Memory source](https://github.com/TerminallyLazy/Tree-Ring-Memory).
- Implementation snapshot: [Tree Ring Memory v0.11.0](https://github.com/TerminallyLazy/Tree-Ring-Memory/releases/tag/v0.11.0).
- A real deployment should additionally retain task IDs, recalled record IDs, accepted and rejected writes, verifier commands, tombstones, and the human escalation decision.

No production run receipt was supplied with the proposal, so this entry does not claim measured reliability, adoption, or deployed outcomes.

## Worked Scenario

A weekly PR-maintenance loop repeatedly rediscovers that generated API files must be updated through a source schema and that one flaky integration test needs a fixed seed. Before each run, it recalls only those two source-linked records. After a verified patch, it records the PR URL and passing command but rejects a proposed transcript summary that contains an access token. When the schema workflow changes, the curator links the old instruction to a tombstone and writes a replacement instead of leaving both active.

## Lessons Learned

- Useful memory is a governed state transition, not a transcript dump.
- Recall needs a relevance and access boundary; more context can preserve stale or conflicting instructions.
- Writes need provenance, retention, and deletion semantics before an unattended loop can trust them.
- Public receipts and deterministic checks should validate consequential memories; the memory tool must not certify its own downstream result.

## Safety Notes

- Sensitive actions: storing credentials, private conversations, customer data, identity-bound decisions, or records that expand permissions.
- Human approvals: required for sensitive retention, ambiguous contradictions, destructive forgetting, and any memory used to authorize a high-impact action.
- Data or privacy constraints: default to explicit writes, least retention, scoped recall, inspectable exports, and tested redaction or deletion.
