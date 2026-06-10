# Security Review Loop

## Objective

Continuously review scoped code changes for security risks, validate findings with evidence, and escalate sensitive decisions to humans.

## Trigger

- Schedule: before release or weekly on active branches.
- Event: security-sensitive files change, dependency advisories appear, authentication/authorization code changes, or infrastructure config changes.
- Manual bootstrap/debug command: "run a security review loop for this PR."

## Intake

- Changed files, diff, threat model, sensitive paths, dependency advisories, secrets scan output, prior security issues, and relevant policy docs.
- Repository permission boundaries and disallowed actions.
- CI security checks, static analysis, dependency audit, and test results.

## Agents

- Explorer: maps attack surfaces and sensitive changes.
- Reviewer: checks for vulnerability classes and missing controls.
- Validator: distinguishes exploitable findings from speculative concerns.
- Reporter: writes concise findings with impact, evidence, and remediation.
- Judge: decides whether to open a PR, file an issue, or escalate.

## Workspace And Permissions

- Prefer read-only mode for exploration and finding validation.
- Allow static analysis, tests, dependency audit, and local proof-of-concept only against safe fixtures.
- Disallow secret exfiltration, production access, destructive testing, public disclosure, or broad rewrites without approval.

## Durable State

- Reviewed commit SHA, sensitive paths checked, commands run, findings, false positives, unresolved questions, and human decisions.

## Loop Steps

1. Discover security-relevant diffs or scheduled review targets.
1. Load security policy, threat model, and prior findings.
1. Delegate surface mapping, review, validation, reporting, and judgment.
1. Run allowed static checks and dependency/security scans.
1. Validate each finding against code paths and realistic inputs.
1. Record evidence, severity, and remediation options.
1. Open a narrow PR for mechanical safe fixes or escalate sensitive decisions.

## Verification Gates

- Findings cite concrete files, paths, inputs, commands, or traces.
- Static analysis or tests support the claim when possible.
- Suggested fixes do not weaken security controls or broaden permissions.
- Sensitive actions are human-approved or explicitly out of scope.

## Budget And Exit

- Max retries: 2 validation attempts per finding.
- Max runtime: 90 minutes per review target.
- Stop when high-confidence findings are reported, safe fixes are proposed, no evidence-backed issues remain, or human approval is required.

## Escalation

Escalate for production credentials, exploitability uncertainty, public disclosure, authentication/authorization design, cryptography, data retention, compliance, or severity disagreements.

## Loop Instruction

```text
Run a security review loop for <PR, branch, or release>.
Stay read-only unless a narrow mechanical fix is explicitly safe.
Map the changed attack surface, run allowed checks, validate each finding with evidence, and avoid speculative claims.
Report impact, evidence, recommended fix, residual risk, and escalation needs.
Do not access production secrets or perform destructive testing.
```

Example automation: trigger on PRs touching auth, permissions, infra, dependency manifests, cryptography, logging, or data-handling code.

## Failure Modes

- Producing generic vulnerability lists without repository-specific evidence.
- Treating scanner output as truth without validation.
- Attempting unsafe proof-of-concept tests.
- Fixing security issues by silently changing product behavior or permissions.

## References

- [OpenAI Agents SDK human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) - Human approval boundaries for sensitive operations.
- [Engineering Agentic Systems for Reliability](https://pruningmypothos.com/systems/engineering-agentic-systems-for-reliability/) - Cautions about permissions, traceability, and escalation.
