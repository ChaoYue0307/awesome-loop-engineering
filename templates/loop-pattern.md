# Loop Pattern Template

Use this to document a practical loop pattern such as PR babysitting, CI repair, bug hunting, feedback clustering, deploy verification, or docs drift collection.

## Name

Short name for the loop.

## Objective

What outcome should this loop optimize for?

## Trigger

- Schedule:
- Event:
- Manual command:

## Intake

Where does the loop find work?

Examples: GitHub PRs, failed CI checks, Linear issues, Slack threads, logs, eval failures.

## Agents

- Explorer:
- Implementer:
- Reviewer:
- Judge:

## Workspace And Permissions

- Worktree, sandbox, branch, or container:
- Allowed tools:
- Disallowed actions:
- Human approval boundaries:

## Verification Gates

- Deterministic checks:
- LLM or human review:
- Required evidence:

## State

What survives across iterations?

Examples: progress file, issue comment, database checkpoint, trace, status report.

## Loop Steps

1. Intake work.
1. Decide whether the loop can act safely.
1. Act in an isolated workspace.
1. Verify with the defined gates.
1. Persist evidence and state.
1. Repeat, report, open a PR, or escalate.

## Budget And Exit

- Max retries:
- Max runtime:
- Stop condition:
- Escalation condition:

## Escalation

When should a human take over?

## Starter Prompt

```text
Describe the starter prompt or automation instruction here.
```

## Failure Modes

List the main ways the loop can go wrong and how to detect them.

## References

- [Title](https://example.com) - Why this reference matters.
