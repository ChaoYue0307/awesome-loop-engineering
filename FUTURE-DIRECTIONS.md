# Future Directions

Loop Engineering will mature when recurring agent systems can show not only that a task finished, but **why an action was allowed, which evidence accepted it, what state survived, how failure was contained, what the run cost, and when control returned to a person**.

This agenda turns those gaps into fifteen research and engineering workstreams. Each workstream names the decision it should unlock, the smallest useful artifact, the measures that matter, and a completion gate. Use it to scope a paper, benchmark, runtime feature, product pilot, standards proposal, or public case study.

## From Idea To Evidence

1. **Choose one recurring task.** Name its operator, trigger, intake source, external definition of done, and consequence of a wrong action.
2. **Freeze the Loop Contract.** Record permissions, verifier ownership, durable state, budgets, escalation, and exit before comparing systems.
3. **Keep a meaningful baseline.** Compare with the current human workflow, a single agent run, and a bounded fixed-retry policy. Multi-agent work also needs a cost-matched single-agent baseline.
4. **Test the failure path.** Inject interruption, stale state, unavailable tools, ambiguous requests, verifier disagreement, and exhausted budgets.
5. **Publish the whole result.** Release unsuccessful runs, configuration versions, receipts, costs, human interventions, and the condition that would reject the approach.

| If you are a... | Start with | Produce first |
| --- | --- | --- |
| **Researcher or evaluator** | A falsifiable comparison in workstreams 1-5 | Preregistered protocol, benchmark slice, ablation table, traces, and negative results |
| **Runtime or reliability engineer** | A missing guarantee in workstreams 6-10 | Reference implementation, fault-injection suite, conformance fixtures, and recovery report |
| **Application or product developer** | A repeated job in workstreams 11-15 | Baseline, bounded vertical slice, domain verifier, handoff flow, and rollout report |
| **Security or governance lead** | Permissions, adversarial cases, and ownership across workstreams 3, 8, 9, 14, and 15 | Threat model, enforceable policy, abuse tests, incident runbook, and audit evidence |

## Shared Evaluation Protocol

Results are comparable only when the unit under test is the **full loop configuration**: model, instructions, context, tools, permissions, runtime, verifier, state policy, retry policy, and budget.

### Required Baselines

- **Current operation:** the human or automated process the loop would replace or assist.
- **Single pass:** one agent run with the same model, tools, context, and task.
- **Fixed retry:** the same run repeated to a declared limit with unchanged policy.
- **Candidate loop:** the proposed state, verification, control, or delegation change.
- **Cost-matched alternative:** required whenever the candidate uses more models, agents, judges, tools, tokens, or human review.

### Core Measures

| Measure | Operational definition | Why it matters |
| --- | --- | --- |
| **Verified completion rate** | Eligible runs accepted by an independent evidence gate | Separates completed work from persuasive final messages |
| **False-completion rate** | Runs declared complete that fail an independent audit, divided by all declared-complete runs | Exposes unsafe optimism hidden by pass rate alone |
| **Cold-resume fidelity** | Restart trials that continue from the correct objective, state, and next action | Tests whether persistence works after the conversation disappears |
| **Recovery rate** | Injected failures followed by a valid state and bounded continuation or escalation | Measures resilience rather than happy-path success |
| **Duplicate-side-effect rate** | Repeated external actions caused by retries, replay, or worker recovery | Detects unsafe execution semantics |
| **Budget adherence** | Runs that stay inside declared token, cost, time, step, and concurrency limits | Makes autonomy governable and comparisons fair |
| **Escalation precision and recall** | Necessary handoffs raised and unnecessary handoffs avoided against adjudicated cases | Measures both missed danger and review fatigue |
| **Cost per verified outcome** | Total model, tool, compute, and review cost divided by independently accepted outcomes | Prevents quality gains from hiding uneconomic operation |
| **Human correction load** | Review time and corrective actions per accepted outcome | Shows whether automation reduces work or merely moves it |

Do not collapse these measures into one leaderboard score. Report distributions, uncertainty, every budget breach, and results by failure class. A higher task-success rate is not an improvement if false completion, unsafe action, human correction, or cost rises beyond the declared acceptance threshold.

### Minimum Reproducibility Bundle

Every study or operating report should include:

- a versioned [Loop Contract](schemas/loop-contract.schema.json) and resolved runtime configuration;
- task IDs, environment versions, model identifiers, harness versions, and seeds where supported;
- baseline and candidate budgets measured on the same accounting boundary;
- verifier code or rubric, verifier ownership, and a statement of what the acting agent can modify;
- event receipts, state snapshots or diffs, and redacted traces sufficient to reconstruct each decision;
- success, failure, escalation, and no-work cases rather than selected demonstrations;
- raw per-run outcomes plus the script that produces aggregate tables;
- privacy, licensing, and redaction decisions for data that cannot be public.

## Priority Map

The tiers describe dependency order, not prestige. Establish trustworthy state transitions before optimizing complex delegation.

| Tier | Workstreams | Shared proof point |
| --- | --- | --- |
| **Foundation** | 3. Verification, 6. State and provenance, 7. Durable execution, 8. Receipts and replay, 9. Security | A loop can be interrupted, audited, attacked, recovered, and stopped without losing control of evidence or side effects |
| **Scale** | 1. Factorized evaluation, 2. Long-horizon reliability, 4. Control policies, 10. Portability, 11. Economics | Improvements survive matched budgets, multiple runtimes, adverse conditions, and cost accounting |
| **Adoption** | 5. Human oversight, 12. Multi-agent delegation, 13. Domain loops, 14. Rollout and handoff, 15. Lifecycle governance | A real operator can deploy, understand, interrupt, update, and retire the system using measured promotion gates |

## Research And Evaluation Workstreams

### 1. Factorized System Evaluation

- **Decision unlocked:** whether an observed gain came from the model, context, harness, verifier, outer-loop policy, or extra compute.
- **Build:** a factorial runner that changes one component at a time while holding tasks, model access, budgets, and acceptance policy fixed.
- **Measure:** verified completion, false completion, effect size with uncertainty, latency, cost, recovery, and human review.
- **Starter slice:** replay at least 25 public tasks through single pass, fixed retry, and evidence-aware retry using one model and two harness configurations.
- **Completion gate:** another team can reproduce the comparison and attribute each reported gain to a declared component rather than an untracked configuration change.

### 2. Long-Horizon Reliability And Recovery

- **Decision unlocked:** whether a loop can preserve correct progress across sessions, interruptions, changing constraints, and partial failure.
- **Build:** multi-stage tasks with graded checkpoints and controlled injections for process death, stale state, changed objectives, tool outages, and rollback.
- **Measure:** milestone coverage, time to first irrecoverable error, cold-resume fidelity, rollback precision, recovery time, and cost by stage.
- **Starter slice:** convert ten short tasks into five-stage sequences that must resume across three fresh sessions with no conversation history.
- **Completion gate:** the benchmark distinguishes reasoning failure, state divergence, premature exit, timeout, and recovery failure instead of reporting only final pass or fail.

### 3. Verification Science And False Completion

- **Decision unlocked:** which evidence gates are trustworthy enough to advance state or declare completion.
- **Build:** paired accepted and rejected outputs with hard negatives, verifier disagreement, tampering attempts, and underspecified intent; compare deterministic checks, learned judges, ensembles, and human adjudication.
- **Measure:** false-accept and false-reject rates, calibration, inter-rater agreement, leakage sensitivity, tamper resistance, latency, and review cost.
- **Starter slice:** collect 100 adjudicated receipts from coding or research tasks, freeze the acceptance policy, and evaluate four verifier designs without letting the actor edit its checker.
- **Completion gate:** held-out results include confidence intervals and challenge cases, and no acceptance claim depends only on the acting model judging itself.

### 4. Control Policies, Stopping, And Abstention

- **Decision unlocked:** when the loop should retry, change strategy, ask for help, abstain before acting, or stop.
- **Build:** a replay environment that applies alternative next-action policies to the same state and evidence under identical budgets.
- **Measure:** marginal retry yield, decision regret, unnecessary escalation, missed escalation, post-action abstention, budget breaches, and cost-quality frontiers.
- **Starter slice:** take 50 completed traces and compare fixed retries, evidence-aware rules, and a learned policy without rerunning the underlying task.
- **Completion gate:** the proposed policy improves verified value per cost over fixed retry without increasing false completion or irreversible unsafe action.

### 5. Human Oversight And Decision Quality

- **Decision unlocked:** what evidence and interaction design help people intervene correctly without automation bias or review fatigue.
- **Build:** a preregistered study comparing raw traces, narrative summaries, and structured receipts for the same approve, retry, rollback, and escalate decisions.
- **Measure:** decision accuracy, missed failures, time to decision, override quality, confidence calibration, interruption burden, and retention after handoff.
- **Starter slice:** anonymize 20 mixed-success cases, recruit participants who match the intended operator role, and keep the underlying evidence identical across interfaces.
- **Completion gate:** the interface improves decision quality or time on held-out cases and reports where summaries hide evidence, induce over-trust, or add no value.

## Runtime And Infrastructure Workstreams

### 6. Durable State, Memory, And Provenance

- **Decision unlocked:** which information may safely influence the next run and how it can be corrected, expired, compacted, or rolled back.
- **Build:** an event-sourced state model with stable item IDs, schema versions, source lineage, confidence or authority, retention rules, checkpoints, and reversible compaction.
- **Measure:** cold-resume fidelity, stale-read rate, contamination rate, state divergence, rollback precision, storage growth, and maintenance cost.
- **Starter slice:** implement file, database, and object-store adapters for one contract, then inject missing, stale, conflicting, and poisoned state.
- **Completion gate:** every derived state value points to its source event, corruption is detected before action, and a fresh worker reconstructs the same next action from persisted evidence.

### 7. Crash-Safe Execution And Idempotency

- **Decision unlocked:** whether work can survive worker death, retries, deploys, rate limits, and partial side effects without duplication or loss.
- **Build:** leased work intake, stable idempotency keys, checkpointed state transitions, retry-safe tool adapters, dead-letter handling, and bounded recovery.
- **Measure:** duplicate-side-effect rate, lost-work rate, recovery time, lease contention, poison-item isolation, and state consistency after restart.
- **Starter slice:** run one reference worker while killing it before and after every external action, verifier call, state write, and acknowledgment.
- **Completion gate:** repeated fault injection produces one accepted effect or a visible escalation, never silent loss, uncontrolled replay, or an unbounded retry storm.

### 8. Receipts, Observability, And Causal Debugging

- **Decision unlocked:** whether an operator can reconstruct why the loop acted, retried, escalated, or exited.
- **Build:** a receipt envelope for trigger, objective version, input identity, action, tool result, verifier result, state transition, budget delta, next action, and redaction policy, mapped where practical to [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai).
- **Measure:** receipt coverage, missing causal links, replay agreement, trace overhead, redaction failures, and time to diagnose seeded incidents.
- **Starter slice:** instrument one validated contract end to end and build a replay view that derives the decision timeline from receipts rather than model narration.
- **Completion gate:** an independent reviewer can identify the cause of a seeded failure and reproduce the control decision without access to the original chat session.

### 9. Security, Permissions, And Containment

- **Decision unlocked:** whether a compromised instruction, tool result, memory entry, dependency, or agent can exceed the authority granted to one run.
- **Build:** machine-enforced capability manifests, short-lived credentials, egress controls, data boundaries, approval gates for irreversible actions, signed state transitions, and revocation.
- **Measure:** unauthorized-action block rate, exfiltration success, privilege persistence, memory-poisoning survival, containment time, blast radius, and human-override auditability.
- **Starter slice:** map one production-shaped loop to the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), then automate at least one abuse case per applicable risk.
- **Completion gate:** forbidden actions fail at the policy or sandbox boundary, not because the prompt politely requested restraint, and every override leaves an attributable receipt.

### 10. Contract Portability And Interoperability

- **Decision unlocked:** whether the same operating intent survives movement between a session tool, CI, scheduler, and durable worker.
- **Build:** a portable Loop Contract profile, runtime adapters, capability negotiation, conformance fixtures, and explicit extension points for runtime-specific behavior.
- **Measure:** semantic conformance, adapter effort, unsupported-field rate, equivalent state transitions, receipt compatibility, and migration defects.
- **Starter slice:** execute the same contract locally, in GitHub Actions, and in a recoverable worker using one shared fixture set.
- **Completion gate:** all runtimes agree on trigger, permission, verification, budget, escalation, and exit decisions, while unavoidable differences are machine-readable rather than hidden in prompts.

## Application And Operations Workstreams

### 11. Reliability Economics And Resource Allocation

- **Decision unlocked:** which model, verifier, retry, tool, and reviewer allocation maximizes verified value inside a real operating budget.
- **Build:** budget-aware routing with per-stage accounting, marginal-value stopping, queue priorities, and policy simulation over historical traces.
- **Measure:** cost per verified outcome, marginal retry yield, latency percentiles, review cost, queue age, budget variance, and quality-cost Pareto frontiers.
- **Starter slice:** replay 100 tasks across two model tiers, three retry limits, and two verification policies while preserving the same acceptance gate.
- **Completion gate:** the policy identifies a stable Pareto improvement and publishes the workloads where a cheaper single pass or human process remains better.

### 12. Multi-Agent Delegation And Coordination

- **Decision unlocked:** when specialized roles, parallelism, or independent review justify coordination cost and new failure modes.
- **Build:** tasks with explicit decomposition opportunities, role and handoff manifests, shared-state rules, attribution receipts, and single-agent ablations.
- **Measure:** cost-matched verified completion, parallel speedup, coordination overhead, redundant work, handoff loss, disagreement resolution, and blame localization.
- **Starter slice:** compare one expert-designed topology with a single agent using equivalent tools, total tokens, and wall-clock budget on separable and non-separable tasks.
- **Completion gate:** the advantage survives role ablation and a cost-matched single-agent baseline; otherwise publish the negative result and simplify the topology.

### 13. Domain-Grade Loop Use Cases

- **Decision unlocked:** which recurring jobs are verifiable, reversible, frequent, and valuable enough to deserve a loop.
- **Build:** a complete vertical slice for one bounded queue, such as PR checks, documentation drift, support triage, experiment monitoring, data-quality alerts, or evidence collection.
- **Measure:** recurrence, verifier coverage, exception rate, avoided rework, operator time, false completion, rollback rate, and verified value per cycle.
- **Starter slice:** baseline the current process for two weeks, run the candidate in read-only shadow mode, and adjudicate every disagreement.
- **Completion gate:** repeated operating cycles show a measurable benefit over the baseline, and all unsupported or high-impact cases reach a named owner rather than disappearing.

### 14. Progressive Rollout, Handoff, And Incident Response

- **Decision unlocked:** when a loop may move from observation to recommendation, approval-required action, and bounded autonomy.
- **Build:** promotion gates, a live evidence view, pause and kill controls, rollback, escalation routing, on-call ownership, and an incident runbook.
- **Measure:** shadow precision, approval and override rates, missed escalations, time to understand, rollback success, time to containment, and notification burden.
- **Starter slice:** define one acceptance threshold and rollback rule for each rollout stage, then rehearse ambiguous input, verifier failure, budget exhaustion, and operator unavailability.
- **Completion gate:** each stage has objective promotion and demotion criteria, and an operator can pause, inspect, resume, or retire the loop without editing its prompt or state by hand.

### 15. Lifecycle Governance And Maintainable Adoption

- **Decision unlocked:** how loop behavior remains reviewable as models, prompts, tools, verifiers, data, policies, and owners change.
- **Build:** versioned contracts beside code, ownership metadata, change review, regression suites, dependency and permission inventories, service objectives, deprecation, and retirement procedures.
- **Measure:** configuration drift, change-failure rate, expired permissions, regression escape rate, review time, owner coverage, incident recurrence, and rollback readiness.
- **Starter slice:** make contract changes visible in CI, require evidence for permission or verifier changes, and run one model upgrade through the same replay suite before promotion.
- **Completion gate:** every active loop has an accountable owner, tested rollback, current permissions, declared service objectives, and a retirement path aligned with the [NIST Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) where applicable.

## Ninety-Day Execution Plans

| Owner | Days 1-30 | Days 31-60 | Days 61-90 | Publish |
| --- | --- | --- | --- | --- |
| **Researcher or evaluator** | Select one workstream, freeze tasks and baselines, define rejection criteria | Run a pilot, repair protocol flaws, add adversarial and failure cases | Run the held-out study and one independent reproduction | Contract, task set, configs, per-run results, analysis, traces, and negative findings |
| **Runtime or reliability engineer** | Instrument one contract and establish state plus receipt schemas | Add fault injection, idempotency tests, replay, and policy enforcement | Port to a second runtime and run conformance plus recovery tests | Reference worker, fixtures, SLOs, recovery table, and known limitations |
| **Application or product developer** | Measure the current workflow and define the domain evidence gate | Run read-only shadowing and adjudicate every disagreement | Pilot approval-required actions with rollback and handoff drills | Before/after metrics, verifier coverage, escalation UX, costs, and rollout decision |
| **Security or governance lead** | Map permissions, data, identities, side effects, and applicable threats | Turn threats into executable abuse cases and enforce runtime boundaries | Exercise containment, revocation, incident response, and audit reconstruction | Threat model, policy manifest, attack results, exceptions, and remediation owners |

## Milestones Worth Coordinating

| Field milestone | Evidence that it exists |
| --- | --- |
| **Portable contract profile** | Three runtime classes execute one contract against shared fixtures with declared semantic differences |
| **Receipt and replay standard** | A third party reconstructs state transitions and control decisions from redacted receipts |
| **Verifier reliability benchmark** | Deterministic, learned, ensemble, and human gates are compared on held-out hard negatives with calibration and cost |
| **Long-horizon recovery suite** | Multi-session tasks include crashes, stale state, changed objectives, rollback, and dense intermediate grading |
| **Agent security challenge set** | Applicable OWASP risks become executable tests with measured containment and recovery |
| **Economic benchmark** | Model, verifier, retry, and review policies are compared under one accounting boundary and acceptance gate |
| **Human handoff study** | Intended operators make blinded intervention decisions using alternative evidence interfaces |
| **Case-study commons** | Public or safely anonymized reports include contracts, receipts, budgets, incidents, and before/after outcomes |

## Proposal Template

Use this structure before opening an implementation or study:

```text
Title:
Workstream and intended operator:
Recurring task and trigger:
Decision this project should unlock:
Falsifiable claim:
Current-operation baseline:
Single-pass and fixed-retry baselines:
Loop Contract and runtime:
Independent evidence gate:
State and receipt format:
Budgets and accounting boundary:
Failure injections and abuse cases:
Primary and guardrail measures:
Human escalation and rollback:
Artifacts to publish:
Result that would reject the approach:
```

## Qualification Checklist

Before calling a direction complete, confirm:

- [ ] The recurring task, intended operator, and consequence of error are explicit.
- [ ] The baseline and falsifiable claim were fixed before the held-out result.
- [ ] The external evidence gate and its owner are independent of the acting agent where practical.
- [ ] State, receipts, budgets, escalation, rollback, and exit are part of the tested contract.
- [ ] At least one interruption, stale-state, verifier, permission, and budget failure was exercised or marked not applicable with a reason.
- [ ] Quality, reliability, safety, economics, and human effort are reported separately.
- [ ] Unsuccessful runs and negative findings are included.
- [ ] Reproduction, privacy, licensing, and redaction constraints are stated.
- [ ] The result that would block deployment or reject the hypothesis is visible.
- [ ] A maintainer, operator, or research owner is named for the next decision.

Open a [direction proposal](https://github.com/ChaoYue0307/awesome-loop-engineering/issues/new?template=direction-proposal.yml) with the template above, discuss cross-project questions in [GitHub Discussions](https://github.com/ChaoYue0307/awesome-loop-engineering/discussions), or publish a run using the [minimum useful case-study checklist](gallery/README.md#minimum-useful-case-study).
