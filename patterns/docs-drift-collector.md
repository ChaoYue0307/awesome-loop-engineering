# Docs Drift Collector

## Objective

Find places where documentation has drifted from code, tests, CLI behavior, API schemas, screenshots, or examples, then propose small verified patches.

## Trigger

- Schedule: weekly for active repositories.
- Event: release branch cut, public API change, CLI flag change, docs-related issue, or failed docs example.
- Manual command: "scan for docs drift around this feature."

## Intake

- Changed files since the last release.
- Public docs, README sections, examples, generated API references, CLI help, OpenAPI specs, and tutorials.
- User reports or search queries that indicate confusion.

## Agents

- Explorer: maps changed behavior to docs that mention it.
- Implementer: patches docs, examples, or comments.
- Verifier: runs docs tests, examples, link checks, or CLI help comparisons.
- Reviewer: checks tone, accuracy, and scope.

## Workspace And Permissions

- Use a docs-focused branch or worktree.
- Allow docs, examples, comments, and tests that verify examples.
- Require approval before changing product behavior, public API, or generated docs sources.

## Durable State

- Candidate drift items, checked files, accepted patches, rejected false positives, and verification commands.

## Loop Steps

1. Identify recent behavior changes or stale-doc signals.
1. Search docs for old names, flags, endpoints, screenshots, or examples.
1. Compare docs against code, schema, tests, or runtime output.
1. Patch only confirmed drift.
1. Run docs checks, examples, and link verification.
1. Record false positives so the next loop does not repeat them.

## Verification Gates

- Updated examples run or match current CLI/API output.
- Link checker passes.
- No generated file is edited manually unless that is the project convention.
- Diff is scoped to confirmed drift.

## Budget And Exit

- Max retries: 2 per drift item.
- Max runtime: 60 minutes.
- Stop when all high-confidence drift items are patched, remaining items need owner judgment, or verification cannot run.

## Escalation

Escalate when docs conflict with product decisions, generated docs are out of date, examples require credentials, or screenshots need design approval.

## Starter Prompt

```text
Scan for documentation drift related to <feature, release, or changed files>.
Confirm each drift item against code, tests, schema, or runtime output before editing.
Patch only verified mismatches, run docs/link/example checks, and record false positives.
```

## Failure Modes

- Updating docs based on guesswork instead of runtime evidence.
- Editing generated files directly.
- Changing examples without running them.
- Treating missing docs as drift when it is really a product documentation decision.
