# GitHub Agentic Workflow Variant

> Template, not a guarantee of product behavior. GitHub Agentic Workflows are evolving; confirm syntax, permissions, and triggers in the [official docs](https://github.github.com/gh-aw/) before relying on this. The block below is an illustrative shape, not a copy-paste workflow file.

A scheduled or event-triggered loop that runs a coding agent inside GitHub Actions. Use it when the work is tied to a repository and you want CI-style guardrails, required checks, and a pull request as the escalation path.

## When to use

- The loop's intake and output are GitHub-native: issues, PRs, releases, checks.
- You want the run isolated in a container and gated by repository permissions.
- A pull request is the right place for a human to take over.

## Shape

The intent is usually written in Markdown and compiled to a locked Actions workflow. The illustrative shape:

```text
on:
  schedule: weekly
  pull_request: [opened, synchronize]   # optional event trigger
permissions: read-only by default; request the minimum the job needs
engine: a coding agent (for example Copilot CLI, Claude Code, or Codex)

job: docs-drift-check
  intake:
    - changed files since the last run
    - public docs, examples, and CLI help
  steps:
    1. For each candidate drift item, verify it against code, schema, or runtime output.
    2. Patch only verified mismatches in a new branch.
    3. Run the docs build, link check, and example checks. These are the verification gate.
  output:
    - open a pull request with the verified patches and the check results
  guardrails:
    - never edit generated files by hand
    - never push to a protected branch
    - if the checks fail, open the PR as draft and label it "needs-human"
```

## How it maps to the Loop Contract

| Contract part | In this template |
| ------------- | ---------------- |
| Trigger | `schedule: weekly`, optionally plus PR events |
| Workspace | Containerized Actions job, isolated per run |
| Verification | Docs build, link check, and example checks as required gates |
| Durable state | The branch, the PR, and run artifacts |
| Budget | The Actions job timeout |
| Escalation | A pull request, drafted and labeled when checks fail |

## Guardrails

- Default to read-only permissions and request only the minimum scopes the job needs; see [Securing Unattended Loops](../../README.md#securing-unattended-loops).
- Make the verification gate a real status check, not a model summary.
- Keep the escalation path a reviewable PR; never let the workflow merge its own changes to a protected branch.
- Start from the full [docs drift pattern and contract](../../patterns/docs-drift-collector.md) before adapting this runtime variant.
