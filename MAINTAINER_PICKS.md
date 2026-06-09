# Maintainer Picks

Start here if you want a compact path through the repository.

## Concept

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - Direct framing of Loop Engineering as the layer above manual prompting and one floor above harness engineering.
- [Canonical Definition](DEFINITION.md) - Stable definition and scope test for quoting or explaining the concept.
- [Loop Engineering Manifesto](MANIFESTO.md) - Short statement of principles, non-goals, and success criteria.

## Practice

- [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) - Practical plan-edit-test-observe-repair-document-repeat runbook.
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) - Scheduled loop mechanics for recurring prompts, monitors, reminders, and `/loop`.
- [PR babysitter pattern](patterns/pr-babysitter.md) - Concrete operational pattern for PR comments, CI, conflicts, and merge readiness.
- [CI repair loop pattern](patterns/ci-repair-loop.md) - Concrete operational pattern for turning failing checks into narrow verified patches.

## Reliability

- [Stop Babysitting Your Coding Agent. Give It Backpressure.](https://generativeprogrammer.com/p/stop-babysitting-your-coding-agent) - Turns tests, linters, builds, traces, and other signals into feedback loops.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) - Canonical workflow patterns and caution against unnecessary complexity.
- [Loop Engineering Anti-Patterns](ANTI-PATTERNS.md) - Failure modes to avoid before running agents repeatedly.

## Reusable Artifacts

- [Loop contract schema](schemas/loop-contract.schema.json) - Machine-readable contract for recurring agent loops.
- [Example loop specs](examples/README.md) - Validated PR babysitter, CI repair, and docs drift loop examples.
- [Loop Gallery](gallery/README.md) - Community format for sharing real or anonymized loop examples.
