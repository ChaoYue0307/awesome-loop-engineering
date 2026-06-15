# Release-Note Loop

## Objective

Assemble accurate, human-readable release notes from the merged commits, issues, and PRs in a release, so the changelog is drafted from evidence rather than memory.

## Trigger

- Event: a release branch is cut, a tag is created, or a release milestone closes.
- Schedule: weekly draft for the next release during active development.
- Manual bootstrap/debug command: "draft release notes for <version> from the merged changes."

## Intake

- Merged PRs, closed issues, and commits since the last release tag.
- Labels, conventional-commit types, linked issues, and breaking-change markers.
- The prior changelog format and any release-note style guide.

## Context

- Required files: changelog, release-note style guide, label-to-section mapping.
- Runtime sources: commit range, PR metadata, issue links, and migration notes.

## Agents

- Collector: gathers the merged PRs, issues, and commits in the release range with links.
- Classifier: groups changes into sections such as features, fixes, breaking changes, and docs.
- Writer: drafts user-facing notes that explain impact, not just commit titles.
- Reviewer: checks each note against its source and flags anything user-affecting for a human.

## Workspace And Permissions

- Read access to git history, PR and issue metadata, and the existing changelog.
- Allowed to open a draft changelog PR and link each entry to its source.
- Disallowed from publishing the release, editing tags, or rewording security advisories unreviewed.
- Publishing the release and finalizing breaking-change wording are human decisions.

## Durable State

- The release range, processed PR and issue IDs, the section mapping, and the current draft.
- A record of which entries were human-reviewed versus auto-drafted.

## Loop Steps

1. Determine the commit range since the last release and load the changelog format.
1. Collect merged PRs, closed issues, and commits with stable links.
1. Classify each change into a section and drop noise such as chores and merge commits.
1. Draft user-facing notes, calling out breaking changes and migration steps.
1. Open or update a draft changelog PR with one source link per entry.
1. Persist processed IDs so the next run does not duplicate entries.
1. Stop when the draft is review-ready or blocked on a product wording decision.

## Verification Gates

- Every release-note entry links to a merged PR, issue, or commit.
- Breaking changes and migrations are called out explicitly, not buried.
- The draft excludes noise (chores, reverts that cancel out, merge commits).
- Processed IDs are recorded so re-runs do not double-count.

## Budget And Exit

- Max retries: 2 redraft passes per section before escalation.
- Max runtime: 30-60 minutes per release draft.
- Stop when the draft is review-ready, or blocked on product wording or a security advisory.

## Escalation

Escalate for security advisories, ambiguous breaking changes, customer-commitment wording, license-relevant changes, or release scope that needs product judgment.

## Loop Instruction

```text
Draft release notes for <version>.
Collect merged PRs, issues, and commits since the last release, each with a link.
Classify into features, fixes, breaking changes, and docs; drop chores and merge noise.
Write user-facing notes that explain impact, call out migrations, and link every entry to its source.
Open a draft changelog PR. Do not publish the release or finalize security wording without a human.
```

Example automation: trigger when a release branch or tag is created, then open a draft changelog PR for human review before publication.

## Failure Modes

- Notes copy raw commit titles instead of explaining user impact.
- A breaking change is filed under features and missed by readers.
- Duplicate entries appear because processed IDs were not tracked.
- The loop publishes or tags a release instead of stopping at a reviewed draft.

## Safety Notes

- Treat security-relevant changes as escalation items; do not auto-publish their wording.
- Link to sources rather than pasting internal discussion that should stay private.
- Keep the human as the publisher of record for the release.

## Example Contract

- [`examples/release-note-loop.json`](../examples/release-note-loop.json)

## References

- [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) - Plan-edit-test-observe-document-repeat work with status logs and validation gates.
- [GitHub Agentic Workflows](https://github.github.com/gh-aw/) - Event or schedule triggered repository automation with guardrails.
