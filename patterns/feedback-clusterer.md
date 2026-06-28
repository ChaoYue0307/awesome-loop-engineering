# Feedback Clusterer

## Objective

Turn noisy feedback streams into a small set of actionable themes with evidence, owners, and suggested next steps.

## Trigger

- Schedule: daily or weekly.
- Event: launch, incident, release, community spike, support backlog growth, or high-volume issue labels.
- Manual bootstrap/debug command: "cluster feedback from the last week."

## Intake

- GitHub issues, PR comments, Linear tickets, Slack threads, support tickets, app reviews, forum posts, social posts, and survey responses.
- Existing product areas, labels, owners, roadmap themes, and known duplicates.

## Agents

- Collector: gathers feedback and preserves source links.
- Clusterer: groups items by user problem, not by surface wording.
- Skeptic: checks whether clusters are overgeneralized or missing counterexamples.
- Reporter: produces themes, examples, confidence, and next actions.

## Workspace And Permissions

- Prefer read-only access to feedback systems.
- Allow creating summary docs, issues, or labels when permitted.
- Require human approval for closing user reports, changing priorities, or sending customer-facing replies.

## Durable State

- Query windows, source filters, processed item IDs, cluster names, representative links, confidence, and follow-up owners.

## Loop Steps

1. Define the time window and source filters.
1. Collect raw items with stable links.
1. Delegate collection, clustering, skepticism, and reporting to separate roles when source volume is high.
1. Deduplicate exact repeats and known duplicates.
1. Cluster by underlying user need, failure mode, or request.
1. Attach representative examples and counterexamples.
1. Rank by frequency, severity, strategic relevance, and confidence.
1. Produce action items or escalate ambiguous themes.

## Verification Gates

- Every cluster has source links.
- High-impact claims include representative examples.
- The report distinguishes frequency from severity.
- The loop records processed IDs to avoid double counting.

## Budget And Exit

- Max runtime: 30-90 minutes depending on source volume.
- Max items: set a sampling cap before the run.
- Stop when clusters are stable, source rate limits block collection, or themes require product judgment.

## Escalation

Escalate when feedback includes security issues, legal concerns, customer-specific commitments, sensitive data, or prioritization conflicts.

## Loop Instruction

```text
Cluster feedback from <sources> for <time window>.
Group by underlying user problem, keep source links, separate frequency from severity, and record processed IDs.
Produce the top themes with representative examples, confidence, suggested owners, and next actions.
Do not close issues or send external replies without approval.
```

Example automation: run daily or weekly, or trigger after a launch, incident, release, support backlog spike, or high-volume issue label.

## Failure Modes

- The loop clusters by keywords instead of user problems.
- High-volume low-severity noise hides rare severe issues.
- The report loses links back to evidence.
- The same item is counted repeatedly across mirrored systems.

## References

- [The Anthropic leader who built Claude Code ditched prompting - now he writes loops](https://thenewstack.io/loop-engineering/) - Reports Boris Cherny's loop-writing workflow for recurring agent work, including handling streams of feedback.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) - Shows orchestrator-worker patterns for collecting, checking, and reporting evidence.
