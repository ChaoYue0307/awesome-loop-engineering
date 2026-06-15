# Data-Quality Loop

## Objective

Keep a recurring dataset or knowledge base trustworthy by validating each refresh against explicit quality rules before it is published, instead of discovering bad data downstream.

## Trigger

- Schedule: after each dataset or knowledge-base refresh, or nightly.
- Event: upstream load completes, source schema changes, or a freshness SLA is breached.
- Manual bootstrap/debug command: "validate the latest <dataset> refresh and quarantine on failure."

## Intake

- The new dataset version, its schema, row counts, and the prior accepted version.
- Quality rules: schema constraints, null thresholds, range checks, uniqueness, referential integrity, and freshness.
- Known accepted exceptions and prior false positives.

## Context

- Required files: data contract or schema, quality-rule definitions, ownership map.
- Runtime sources: current load metrics, profiling output, diff against the last accepted version.

## Agents

- Profiler: computes row counts, distributions, null rates, and freshness for the new version.
- Validator: checks the profile against quality rules and the prior accepted baseline.
- Investigator: classifies each failure as a real defect, an accepted shift, or a rule bug.
- Reporter: records pass/fail, quarantines bad versions, and proposes rule fixes.

## Workspace And Permissions

- Read access to the dataset, schema, profiling tools, and prior versions.
- Allowed to run validation queries, write a quality report, and quarantine a failing version.
- Disallowed from editing source data, publishing to production, or relaxing rules without review.
- Promoting a version to production is a human or policy-gated decision.

## Durable State

- Dataset version, profile metrics, rule results, quarantine status, and accepted exceptions.
- A quality ledger so recurring shifts are recognized rather than re-investigated every run.

## Loop Steps

1. Load the new version, its schema, and the last accepted baseline.
1. Profile the data: counts, distributions, nulls, ranges, uniqueness, and freshness.
1. Run quality rules and diff the profile against the baseline.
1. Classify each failure as a defect, an accepted shift, or a rule bug.
1. Quarantine the version if a hard rule fails; otherwise mark it ready for promotion.
1. Persist the profile, results, and any new accepted exception.
1. Stop when the version is validated and ready, quarantined, or blocked on owner judgment.

## Verification Gates

- Hard rules (schema, referential integrity, freshness) pass before a version is promotable.
- Distribution shifts beyond threshold are flagged with the metric and the delta.
- Every quarantine cites the failing rule and the offending sample.
- Accepted exceptions are recorded so the same shift is not re-flagged forever.

## Budget And Exit

- Max retries: 2 re-profiling attempts per failing rule before escalation.
- Max runtime: 30-90 minutes depending on dataset size.
- Stop when the version is validated, quarantined with evidence, or needs owner judgment.

## Escalation

Escalate for ambiguous distribution shifts, schema changes that need a data-contract update, repeated upstream failures, regulated or PII-bearing fields, or a rule that may itself be wrong.

## Loop Instruction

```text
Validate the latest <dataset> refresh against its data contract and quality rules.
Profile counts, distributions, nulls, ranges, uniqueness, and freshness, then diff against the last accepted version.
Quarantine on any hard-rule failure and cite the failing rule and a sample.
Record accepted shifts so they are not re-flagged, and never publish to production yourself.
Escalate ambiguous shifts, schema changes, or anything touching regulated fields.
```

Example automation: run after each upstream load or nightly, and quarantine failing versions before any downstream job consumes them.

## Failure Modes

- Validating against a moving baseline so real regressions look normal.
- Treating every distribution shift as a defect and drowning owners in false positives.
- Passing a version on row count alone while a key column silently went null.
- Editing or "cleaning" source data instead of quarantining and escalating.

## Safety Notes

- Never copy raw PII or regulated values into reports; reference row keys or hashes instead.
- Quarantine is reversible; publishing bad data downstream often is not, so fail closed.
- Keep the prior accepted version immutable as the comparison baseline.

## Example Contract

- [`examples/data-quality-loop.json`](../examples/data-quality-loop.json)

## References

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Treating durable data and state as managed runtime inputs rather than ad hoc dumps.
- [Durable Execution for Agentic Workflows](https://arizenai.com/durable-execution/) - Checkpointing and replay patterns for recurring data jobs.
