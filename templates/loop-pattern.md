# Loop Pattern Template

Use this to document a practical loop pattern such as PR babysitting, CI repair, bug hunting, feedback clustering, deploy verification, or docs drift collection.

## Name

Short name for the loop.

## Objective

What outcome should this loop optimize for?

What manual prompting or repeated human polling does this loop replace?

## Trigger

- Schedule:
- Event:
- Automation or hook config:
- Manual bootstrap/debug command:

## Intake

Where does the loop find work?

Examples: GitHub PRs, failed CI checks, Linear issues, Slack threads, logs, eval failures.

## Agents

- Explorer:
- Implementer:
- Reviewer:
- Judge:

## Delegation

- Which agent handles each work item:
- Handoff rules:
- When to switch from maker to checker:

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

1. Discover / intake work.
1. Load durable state and relevant context.
1. Delegate to the right agent role.
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

## Loop Instruction

```text
Describe the prompt, automation spec, hook config, or scheduled command that starts the loop.
```

## State Artifacts

- Progress file:
- Issue or PR comment:
- Trace or dashboard:

## Failure Modes

List the main ways the loop can go wrong and how to detect them.

## References

- [Title](https://example.com) - Why this reference matters.
