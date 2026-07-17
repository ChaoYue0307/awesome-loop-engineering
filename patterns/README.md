# Loop Pattern Library

Twenty operational patterns turn the Loop Contract into repeatable ways of working. Every pattern names the problem, trigger, intake, permissions, roles, deterministic gate, durable state, budget, escalation path, and a matching schema-valid contract.

## Use The Library In Three Steps

1. Start from the symptom in the coverage map below.
1. Open the pattern to understand the operating model and worked example.
1. Adapt its linked JSON contract, then choose a [runtime starter](../examples/runnable/README.md).

The layers have different jobs:

| Layer | Question it answers | Artifact |
| --- | --- | --- |
| **Pattern** | How should this class of recurring work operate? | Human-readable operating playbook |
| **Contract** | What exactly may this loop read, change, verify, spend, and escalate? | Schema-valid JSON in [`examples/`](../examples/README.md) |
| **Runtime starter** | Where and how does the contract execute? | Copy/paste and executable starters in [`examples/runnable/`](../examples/runnable/README.md) |

## Coverage Map

### Build And Maintain

| Symptom | Pattern | Verified outcome |
| --- | --- | --- |
| A pull request is stalled | [PR babysitter](pr-babysitter.md) | Required checks pass, review threads are resolved, and merge state is current |
| CI keeps failing | [CI repair loop](ci-repair-loop.md) | The original failing command passes with a scoped patch |
| Documentation may be stale | [Docs drift collector](docs-drift-collector.md) | Verified code/docs mismatches are patched and examples still run |
| Dependency updates pile up | [Dependency triage loop](dependency-triage-loop.md) | Safe updates pass tests and risky upgrades have an owner-backed escalation |
| Bugs need systematic discovery | [Bug hunting loop](bug-hunting-loop.md) | Each accepted finding has reproducible steps or a failing test |
| Release notes are incomplete | [Release-note loop](release-note-loop.md) | Every shipped change maps to a merged source and audience-facing note |

### Operate And Observe

| Symptom | Pattern | Verified outcome |
| --- | --- | --- |
| A rollout needs watching | [Deploy verifier](deploy-verifier.md) | Synthetic checks and rollout thresholds remain within policy |
| An incident just paged | [Incident response loop](incident-response-loop.md) | Impact, evidence, timeline, and accountable owner are recorded |
| A dataset keeps drifting | [Data-quality loop](data-quality-loop.md) | Hard quality rules pass before a new version is promoted |
| Agent spend is rising | [Cost-control loop](cost-control-loop.md) | Spend falls on a comparable workload without quality regression |
| Model choice is ad hoc | [Model-routing loop](model-routing-loop.md) | Routing decisions meet quality, latency, privacy, and cost tolerances |
| Latency, throughput, or memory regressed | [Performance regression loop](performance-regression-loop.md) | A controlled benchmark confirms recovery with correctness intact |

### Learn And Optimize

| Symptom | Pattern | Verified outcome |
| --- | --- | --- |
| Feedback is noisy and unsorted | [Feedback clusterer](feedback-clusterer.md) | Themes cite source items and separate frequency from severity |
| Agent evaluations regressed | [Evaluation regression loop](evaluation-regression-loop.md) | Targeted evals return to the accepted baseline without scorer changes |
| A system should improve against a metric | [Benchmark optimization loop](benchmark-optimization-loop.md) | Repeated measurements confirm an improvement with protected metrics intact |
| An agent's knowledge is stale | [Knowledge freshness loop](knowledge-freshness-loop.md) | A versioned corpus passes provenance, freshness, retrieval, and leakage gates |

### Govern And Protect

| Symptom | Pattern | Verified outcome |
| --- | --- | --- |
| A sensitive change needs review | [Security review loop](security-review-loop.md) | Findings cite concrete evidence and approval boundaries stay intact |
| A change needs formal sign-off | [Enterprise approval loop](enterprise-approval-loop.md) | Every required gate has a recorded decision and audit trail |
| A UI introduced an accessibility failure | [Accessibility regression loop](accessibility-regression-loop.md) | The exact regression is fixed and required human criteria are approved |
| An agent system needs adversarial testing | [Adversarial red-team loop](adversarial-red-team-loop.md) | Confirmed findings are reproduced, minimized, privately reported, and regression-tested |

## Choosing Between Similar Patterns

| If the work sounds like... | Choose | Not |
| --- | --- | --- |
| "A known code change may be unsafe" | Security review | Adversarial red team, which actively discovers behavior failures |
| "Find new failures in a sandboxed agent" | Adversarial red team | Bug hunting, which is broader and not threat-model driven |
| "Our eval score dropped" | Evaluation regression | Benchmark optimization, which seeks new improvement from a stable baseline |
| "Make this system measurably better" | Benchmark optimization | Performance regression, unless the target is specifically latency, throughput, memory, or cost |
| "Our repo docs no longer match code" | Docs drift | Knowledge freshness, which maintains a multi-source retrieval corpus |
| "The retrieval corpus is stale" | Knowledge freshness | Data quality, unless the artifact is a general dataset rather than an agent knowledge index |
| "A scanner found an accessibility issue" | Accessibility regression | General CI repair, because automated checks do not cover all human accessibility criteria |

Compare trigger, state, gate, budget, escalation, and runtime across every pattern in the [full matrix](MATRIX.md).

## Pattern Quality Bar

A pattern qualifies for this library only when it:

- solves a recurring job that is materially distinct from an existing pattern;
- has an external feedback signal stronger than the acting model's opinion;
- names durable state, a hard budget, and a human handoff;
- states what the loop must not do;
- includes a worked scenario and a schema-valid contract;
- can map to at least one practical runtime without assuming unlimited permissions.

Reject patterns whose only gate is "the agent says it looks good." Prefer exit codes, score distributions, changed files, source manifests, trace IDs, dashboard thresholds, screenshots, or named reviewer decisions.
