# Adversarial Red-Team Loop

## Objective

Continuously discover, reproduce, minimize, and report agent-system failures under a bounded threat model without turning speculative attacks into unsupported findings.

## Use This When

- A deployed or pre-release agent has explicit tools, permissions, and safety boundaries.
- Tests can run in a sandbox or synthetic target with no real users or secrets.
- Findings require reproducible evidence and a human-owned disclosure path.

Use the security review loop for reviewing a known code change. Use this pattern when the work is active adversarial discovery against the behavior of an agent system.

## Trigger

- Schedule: bounded weekly or pre-release campaign.
- Event: new tool, model, permission, policy, or attack class.
- Manual bootstrap: "probe <target> against <threat model> for <budget>."

## Intake

- Target version, threat model, allowed attack classes, synthetic accounts, and prohibited actions.
- Policy, tool permissions, known findings, regression corpus, and disclosure contacts.
- Token, request, time, concurrency, and data budgets.

## Agents

- Attacker: generates and adapts probes within the allowed threat model.
- Reproducer: confirms candidate failures in a clean environment.
- Minimizer: reduces the trace to the smallest reliable test case.
- Judge: separates confirmed findings from policy-compliant or non-reproducible behavior.

## Workspace And Permissions

- Use a sandboxed target with synthetic data, fake credentials, and rate limits.
- Keep attack generation separate from confirmation and severity judgment.
- Disallow production exploitation, persistence, destructive actions, real-user data, external exfiltration, and testing outside written scope.

## Durable State

- Target version, seed, probe, full trace, tool calls, expected policy, reproduction count, severity rationale, duplicate link, and disclosure status.

## Loop Steps

1. Freeze target version, threat model, scope, and stop conditions.
1. Select an uncovered attack class or failed regression case.
1. Generate a bounded probe and run it against the sandboxed target.
1. Reproduce promising behavior independently and minimize the trace.
1. Judge against the written policy and classify confirmed, duplicate, expected, or inconclusive.
1. Add confirmed cases to the regression corpus and prepare a private evidence packet.
1. Stop on budget, risk threshold, scope ambiguity, or human intervention.

## Verification Gates

- The behavior reproduces on the recorded target version and environment.
- The finding cites the exact policy or security boundary it violates.
- A separate judge confirms the result; the attacking agent does not grade itself.
- The minimized test contains no real secrets, user data, or harmful payload beyond the sandbox.
- Duplicate and severity checks are complete before reporting.

## Budget And Exit

- Max retries: 3 confirmation attempts per candidate finding.
- Max runtime: 120 minutes per campaign.
- Stop on budget exhaustion, confirmed critical behavior, scope ambiguity, unstable target, or rate-limit breach.

## Escalation

Escalate immediately for possible real-world impact, production data exposure, out-of-scope behavior, unsafe containment, or any critical finding. Keep disclosure private until the owner responds.

## Loop Instruction

```text
Red-team <sandboxed target version> against <written threat model> for at most <budget>.
Use only synthetic data and the allowed attack classes. Generate bounded probes, but require
a separate reproducer and judge before calling anything a finding. Record the full trace,
minimized test, violated policy, reproduction count, and severity rationale. Never test
production, exfiltrate data, persist access, or continue when scope is unclear.
```

## Worked Example

A tool-using support agent gains a new URL-fetch tool. The campaign probes indirect prompt injection in synthetic pages, confirms that one payload can trigger an unauthorized internal lookup, minimizes it to a small HTML fixture, records the exact tool trace, and privately escalates the finding while adding the fixture to the release regression suite.

## Failure Modes

- Letting the attacker grade its own success.
- Calling an interesting response a vulnerability without reproduction or a violated boundary.
- Testing production or using real credentials and customer data.
- Optimizing for attack count instead of distinct, actionable failure classes.
- Publishing sensitive details before remediation and disclosure approval.

## Safety Notes

- Run only with written authorization and an explicit target scope.
- Prefer synthetic fixtures, local sandboxes, and private disclosure.
- Stop rather than improvise when containment or ownership is uncertain.

## Example Contract

- [`examples/adversarial-red-team-loop.json`](../examples/adversarial-red-team-loop.json)

## References

- [Agent Hacks Agent: Autoresearch for Production-Agent Red-Teaming](https://arxiv.org/abs/2607.11698) - Applies an autonomous research loop to attack discovery and reproducible agent failures.
- [Designing AI agents to resist prompt injection](https://openai.com/index/designing-agents-to-resist-prompt-injection/) - Official defense-in-depth guidance for permissions, isolation, and approval boundaries.
