# Dependency Triage Loop

## Objective

Classify dependency updates into safe patches, deferred upgrades, or human-review items with reproducible evidence.

## Trigger

- Schedule: weekly or after dependency bot activity.
- Event: Dependabot, Renovate, package manager advisory, or lockfile update PR.
- Manual bootstrap/debug command: "triage dependency updates for this repository."

## Intake

- Dependency update PRs, release notes, changelogs, advisories, lockfile diff, package manager audit output, and affected package usage.
- Repository compatibility policy and supported runtime versions.
- Recent CI status and known flaky tests.

## Agents

- Classifier: groups updates by risk, security relevance, semantic version change, and blast radius.
- Implementer: applies low-risk updates or patches lockfile conflicts.
- Verifier: runs targeted tests, typechecks, builds, and package manager audits.
- Reporter: records accepted updates, deferred updates, and human-review reasons.

## Workspace And Permissions

- Use a clean branch or worktree per update group.
- Allow package manager commands, tests, typechecks, and build commands.
- Disallow broad dependency upgrades, runtime-version changes, migration rewrites, or security-policy changes without human approval.

## Durable State

- Processed update IDs, package versions, changelog links, commands run, verification output, deferred reasons, and reviewer questions.

## Loop Steps

1. Discover dependency PRs, advisories, or stale dependency groups.
1. Load repository compatibility rules and prior triage state.
1. Delegate risk classification, patching, verification, and reporting.
1. Split updates into safe patch, minor feature, major migration, security, and blocked groups.
1. Apply only the safe group automatically.
1. Run targeted tests, typechecks, build, and audit commands.
1. Persist evidence and open or update PR comments.
1. Repeat for the next safe group or escalate.

## Verification Gates

- Lockfile and package manifest are consistent.
- Relevant tests, typecheck, build, and package audit pass.
- Release notes or changelogs do not indicate required migration steps that were skipped.
- Diff is limited to the intended dependency group.

## Budget And Exit

- Max retries: 2 patch attempts per dependency group.
- Max runtime: 60 minutes per scheduled run.
- Stop when safe updates are merged or ready for review, risky updates are deferred with reasons, or verification fails repeatedly.

## Escalation

Escalate for major version upgrades, runtime requirement changes, security advisories with product impact, migration code, licensing concerns, or repeated verification failures.

## Loop Instruction

```text
Triage dependency updates for <repository>.
Group updates by risk and apply only narrow, low-risk changes automatically.
Run the smallest relevant verification commands and package audit.
Record changelog links, commands, passing evidence, deferred updates, and escalation reasons.
Do not perform major migrations or runtime changes without human approval.
```

Example automation: run weekly and on dependency bot PR creation, then comment with accepted, deferred, and escalated update groups.

## Failure Modes

- Bundling unrelated upgrades into one large diff.
- Ignoring runtime or peer dependency constraints.
- Treating a security advisory as fixed without verifying the vulnerable path.
- Updating generated lockfiles without a reproducible package manager command.

## References

- [GitHub Agentic Workflows](https://github.github.com/gh-aw/) - Event or schedule triggered repository automation with guardrails.
- [OpenAI Agents SDK human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) - Approval boundaries for sensitive tool actions.
