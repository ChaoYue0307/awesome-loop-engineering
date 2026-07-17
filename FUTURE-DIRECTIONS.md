# Future Directions

Loop Engineering is still an emerging practice. This agenda turns its largest open gaps into falsifiable research questions, buildable infrastructure, and testable product work. It is a guide to useful next contributions, not a prediction that every direction will succeed.

Prioritize work that makes at least one recurring agent loop **more measurable, portable, recoverable, economical, or governable**. A credible result should expose the trigger, permissions, external verification gate, durable state, budget, escalation path, and failure evidence.

## For Researchers

| Category | High-value question | Evidence of progress | Concrete starting point |
| --- | --- | --- | --- |
| **Factorized evaluation** | How much performance comes from the model, harness, verifier, and outer loop separately? | Matched model and token budgets, controlled component ablations, confidence intervals, and held-out tasks | Run one fixed model across several harness and loop policies while scoring outcome, recovery, abstention, and resource use |
| **Verification science** | Which combinations of deterministic checks, learned judges, independent agents, and humans prevent false completion? | False-accept and false-reject rates, calibration, tamper resistance, inter-rater agreement, and adversarial challenge sets | Compare a test suite, single judge, judge ensemble, and human review on the same traces with a frozen acceptance policy |
| **State and learning across runs** | Which state representations support cold resume and improvement without stale-memory drift or compaction errors? | Longitudinal replay, state corruption tests, retention curves, recovery accuracy, state size, and maintenance cost | Build tasks that inject missing, stale, conflicting, or poisoned state between runs and measure recovery |
| **Control, stopping, and budgets** | When should a loop retry, change strategy, escalate, abstain, or stop under uncertainty? | Quality-cost-latency Pareto curves, regret, budget adherence, failure containment, and sensitivity analysis | Compare fixed retries, evidence-aware stopping, and learned escalation under identical budgets |
| **Human oversight** | Which handoff designs help people intervene accurately without review fatigue or automation bias? | Preregistered user studies, intervention precision, time to decision, missed failures, workload, and trust calibration | Compare raw traces, concise summaries, and structured evidence receipts on the same review decisions |

Research reports should publish negative results and separate task success from process discipline. A loop that reaches the answer through uncontrolled retries, hidden state, or verifier leakage is not equivalent to one that succeeds within its declared contract.

## For Infrastructure And Reliability Engineers

| Category | Engineering objective | Evidence of progress | Concrete starting point |
| --- | --- | --- | --- |
| **Durable execution** | Resume safely after crashes, rate limits, deploys, and partial work | Idempotency tests, deterministic replay, duplicate-work rate, recovery time, and chaos results | Implement checkpointed queue processing with stable item IDs, bounded leases, and externally verified completion |
| **Receipts and observability** | Make every decision reconstructable from evidence rather than model narration | Correlated traces, immutable receipts, state diffs, cost attribution, and replay tooling | Define a receipt envelope for trigger, input version, action, verifier result, state transition, budget, and next action |
| **Permissions and isolation** | Enforce least privilege across tools, files, networks, credentials, and approval boundaries | Denied-action tests, capability manifests, sandbox escape tests, secret-exposure checks, and audited human overrides | Translate each Loop Contract permission into runtime policy and test both allowed and forbidden actions |
| **Portability and interoperability** | Move one contract between session, CI, scheduled, and durable runtimes without changing its semantics | Conformance tests, adapter compatibility, migration fixtures, and equivalent receipts across runtimes | Build adapters for one contract on a local schedule, GitHub Actions, and a recoverable worker |
| **Reliability economics** | Allocate models, tools, retries, and reviewers to maximize verified value within budget | Cost per verified outcome, latency percentiles, retry amplification, queue stability, and quality-budget frontiers | Add policy-based routing and compare it with fixed-model baselines on a replayable workload |

Operational maturity should be demonstrated with failure injection, not only happy-path demos. Useful artifacts include runbooks, service-level objectives, incident reviews, migration notes, and conformance suites.

## For Application And Product Developers

| Category | Product objective | Evidence of progress | Concrete starting point |
| --- | --- | --- | --- |
| **Loop-worthy use cases** | Select recurring work with stable intake and a defensible external definition of done | Baseline human effort, recurrence rate, verifier coverage, exception rate, and avoided rework | Start with a narrow queue such as failing checks, stale documents, support triage, or threshold monitoring |
| **Domain verification** | Encode completion in domain evidence rather than a generic model confidence score | Golden cases, contract tests, reviewer agreement, regression suites, and unresolved-edge-case logs | Pair every action path with a domain-specific checker and keep the agent unable to edit that checker |
| **Human handoff experience** | Show progress, uncertainty, evidence, and safe next actions at the moment judgment is needed | Time to understand, correct intervention rate, override quality, notification burden, and user-reported clarity | Design one escalation view around objective, attempted actions, receipts, remaining budget, and recommended choices |
| **Progressive rollout** | Move from observation to bounded production use without hiding risk | Shadow-mode precision, canary outcomes, rollback rate, budget breaches, and post-launch incidents | Roll out through read-only, suggestion, approval-required, and bounded-autonomy stages with explicit promotion gates |
| **Maintainable adoption** | Keep loop behavior understandable as models, tools, policies, and teams change | Contract review time, configuration drift, ownership coverage, change failure rate, and onboarding success | Store versioned contracts beside code, assign an owner, and test them whenever prompts, tools, or verifiers change |

Strong developer contributions are complete vertical slices: a real trigger, bounded permissions, independent gate, durable receipts, escalation UX, and a before/after operating result.

## Shared Infrastructure Priorities

| Priority | Shared asset | Minimum useful outcome |
| --- | --- | --- |
| **Portable Loop Contract profile** | A small interoperable subset of objective, trigger, permissions, verification, state, budget, escalation, and exit fields | Two runtimes execute the same contract and produce semantically equivalent decisions |
| **Receipt and replay format** | A stable event envelope for reconstructing each state transition and verifier decision | A third party can replay one run and identify why it retried, escalated, or exited |
| **Factorized benchmark harness** | Evaluation that varies model, harness, verifier, and loop policy independently | Results attribute gains and costs to the component that caused them |
| **Failure and safety challenge set** | Reusable cases for infinite retries, stale state, judge bias, prompt injection, permission escape, and budget exhaustion | Implementations report comparable containment and recovery metrics |
| **Case-study commons** | Public or safely anonymized operating reports with contracts, receipts, budgets, and lessons | Builders can compare real failure modes and operating economics across domains |

## Three Starter Projects

1. **Research:** create a matched-budget benchmark that compares fixed retry, evidence-aware retry, and human escalation while publishing every trace and negative result.
2. **Engineering:** implement the same validated contract in a local scheduler, CI workflow, and durable worker, then publish a conformance and crash-recovery report.
3. **Development:** ship one read-only production loop with a measurable baseline, independent checker, evidence-rich handoff, and staged rollout report.

## Qualification Checklist

Before proposing a new direction, record:

- the recurring task and user or operator it serves;
- the baseline and falsifiable claim;
- the external evidence gate and who controls it;
- the durable state and receipt format;
- the time, cost, retry, and concurrency budgets;
- the failure injection or adversarial cases;
- the human escalation and rollback path;
- the reproducibility, privacy, and licensing constraints;
- the negative result that would cause the approach to be rejected.

Use [GitHub Discussions](https://github.com/ChaoYue0307/awesome-loop-engineering/discussions) to propose a study, reference implementation, or case study. Use the [gallery checklist](gallery/README.md#minimum-useful-case-study) when reporting a loop that has actually run.
