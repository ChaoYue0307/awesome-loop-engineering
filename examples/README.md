# Validated Loop Contracts

Twenty JSON examples turn the operational patterns into reviewable machine-readable contracts. Every file validates against [`schemas/loop-contract.schema.json`](../schemas/loop-contract.schema.json) in CI.

A pattern explains **how a class of loop should operate**. Its contract pins down **what one implementation may read, change, verify, spend, and escalate**. A [runtime starter](runnable/README.md) then wires that contract to a session, schedule, CI job, or durable worker.

## Contract Catalog

### Build And Maintain

| Pattern and contract | Use when | Trigger | Deterministic gate | Durable receipt |
| --- | --- | --- | --- | --- |
| [PR babysitter](../patterns/pr-babysitter.md) · [`JSON`](pr-babysitter-loop.json) | A PR stalls on comments, CI, or conflicts | PR event + schedule | Required checks pass and review threads are resolved | Last SHA, check URLs, thread status, blockers |
| [CI repair](../patterns/ci-repair-loop.md) · [`JSON`](ci-repair-loop.json) | A required check fails | CI failure event | Original failing command passes | Failure excerpt, patch, commands, passing output |
| [Docs drift](../patterns/docs-drift-collector.md) · [`JSON`](docs-drift-loop.json) | Docs may disagree with code | Weekly schedule | Examples and links pass against current behavior | Verified drift items and false positives |
| [Dependency triage](../patterns/dependency-triage-loop.md) · [`JSON`](dependency-triage-loop.json) | Update PRs accumulate | Weekly + bot PR events | Tests, build, typecheck, and audit pass | Update group, risk class, commands, deferral reason |
| [Bug hunting](../patterns/bug-hunting-loop.md) · [`JSON`](bug-hunting-loop.json) | A team needs recurring bug discovery | Weekly schedule | Reproducible steps or a failing test | Checked surface, trace, minimal reproduction |
| [Release notes](../patterns/release-note-loop.md) · [`JSON`](release-note-loop.json) | A release needs evidence-backed notes | Tag or release branch | Every entry links to a merged source | Processed PRs/issues and draft changelog |

### Operate And Observe

| Pattern and contract | Use when | Trigger | Deterministic gate | Durable receipt |
| --- | --- | --- | --- | --- |
| [Deploy verifier](../patterns/deploy-verifier.md) · [`JSON`](deploy-verifier-loop.json) | A rollout needs monitoring | Deployment event + polling | Synthetic checks and thresholds hold | Rollout phase, anomalies, metric links, decision |
| [Incident response](../patterns/incident-response-loop.md) · [`JSON`](incident-response-loop.json) | An alert needs evidence and ownership | Pager or SLO event | Severity and cause cite concrete impact signals | Timeline, hypotheses, owner, handoff |
| [Data quality](../patterns/data-quality-loop.md) · [`JSON`](data-quality-loop.json) | A dataset refresh may drift | Refresh event or nightly | Hard schema and quality rules pass | Profile metrics, exceptions, quarantine decision |
| [Cost control](../patterns/cost-control-loop.md) · [`JSON`](cost-control-loop.json) | Agent spend rises | Schedule + spend threshold | Quality holds on a comparable sample | Baseline spend, traces, proposed savings |
| [Model routing](../patterns/model-routing-loop.md) · [`JSON`](model-routing-loop.json) | Model selection is inconsistent | Schedule + model/price change | Replay quality stays within tolerance | Task-class metrics and routing decision |
| [Performance regression](../patterns/performance-regression-loop.md) · [`JSON`](performance-regression-loop.json) | Latency, throughput, or memory worsens | Metric or benchmark regression | Correctness passes and repeated measurements recover | Environment, profile, samples, candidate decision |

### Learn And Optimize

| Pattern and contract | Use when | Trigger | Deterministic gate | Durable receipt |
| --- | --- | --- | --- | --- |
| [Feedback clusterer](../patterns/feedback-clusterer.md) · [`JSON`](feedback-clusterer-loop.json) | Feedback is noisy | Daily or weekly schedule | Themes cite sources and preserve frequency/severity | Processed IDs, clusters, outliers |
| [Evaluation regression](../patterns/evaluation-regression-loop.md) · [`JSON`](evaluation-regression-loop.json) | Agent evals fall below baseline | Nightly + score drop | Targeted tasks recover without scorer changes | Run IDs, traces, hypotheses, rerun scores |
| [Benchmark optimization](../patterns/benchmark-optimization-loop.md) · [`JSON`](benchmark-optimization-loop.json) | A stable system should improve | Bounded experiment window | Repeated gain with correctness and protected metrics intact | Hypothesis, diff, raw scores, cost, decision |
| [Knowledge freshness](../patterns/knowledge-freshness-loop.md) · [`JSON`](knowledge-freshness-loop.json) | An agent retrieval corpus is stale | Daily refresh + source change | Provenance, freshness, retrieval, and leakage gates pass | Manifest diff, checksums, evals, promotion pointer |

### Govern And Protect

| Pattern and contract | Use when | Trigger | Deterministic gate | Durable receipt |
| --- | --- | --- | --- | --- |
| [Security review](../patterns/security-review-loop.md) · [`JSON`](security-review-loop.json) | A sensitive diff needs review | Sensitive change + weekly sweep | Findings cite reproducible evidence | Reviewed SHA, findings, false positives |
| [Enterprise approval](../patterns/enterprise-approval-loop.md) · [`JSON`](enterprise-approval-loop.json) | A change needs formal sign-off | Gate or approver event | Every required gate has a human decision | Approval ledger, status, SLA, owner |
| [Accessibility regression](../patterns/accessibility-regression-loop.md) · [`JSON`](accessibility-regression-loop.json) | A UI accessibility check fails | PR or preview failure | Exact rule plus required human criteria pass | Before/after scan, interaction trace, reviewer decision |
| [Adversarial red team](../patterns/adversarial-red-team-loop.md) · [`JSON`](adversarial-red-team-loop.json) | An agent needs active security testing | Pre-release campaign | Independent reproduction and policy citation | Seed, full/minimized trace, severity, disclosure status |

## Read And Validate A Contract

Preview a contract as a compact human-readable checklist:

```bash
python3 scripts/preview_loop_contract.py examples/ci-repair-loop.json
```

Validate the complete contract library with the dependency-free CI validator:

```bash
python3 scripts/check_loop_contract_examples.py
```

## Four Worked Paths

### 1. Repair A Failing Check

**Symptom:** a pull request's `pytest -x` job is red.

1. Choose the [CI repair pattern](../patterns/ci-repair-loop.md).
1. Adapt [`ci-repair-loop.json`](ci-repair-loop.json): set the event trigger, protected files, three-retry budget, and escalation owner.
1. Run the [test-repair starter](runnable/test-repair-loop.sh) in an isolated worktree:

```bash
CHECK_CMD="pytest -x" AGENT_CMD="codex exec" ./examples/runnable/test-repair-loop.sh
```

**Done means:** the original command passes. The agent's claim is not the gate.

### 2. Refresh A Support Knowledge Base

**Symptom:** answers cite policies and release notes that may be stale.

1. Choose the [knowledge freshness pattern](../patterns/knowledge-freshness-loop.md).
1. Adapt [`knowledge-freshness-loop.json`](knowledge-freshness-loop.json): name approved sources, freshness windows, retrieval evals, leakage checks, and atomic promotion.
1. Schedule it with the [Codex automation](runnable/codex-automation.md), [desktop task](runnable/claude-desktop-scheduled-task.md), or your durable worker.

**Done means:** a versioned candidate passes provenance, freshness, retrieval, and sensitive-data gates before promotion. A successful fetch alone is not enough.

### 3. Process A Bounded Work Queue

**Symptom:** a set of narrow, independently verifiable tasks needs unattended handling.

Create `tasks.jsonl`:

```json
{"id":"docs-101","objective":"Update the CLI install example","context":["README.md","src/cli.ts"],"allowed_paths":["README.md"],"verification":"python3 scripts/check_docs.py"}
{"id":"schema-204","objective":"Add the missing status enum test","context":["schemas/status.json","tests/test_status.py"],"allowed_paths":["tests/test_status.py"],"verification":"pytest tests/test_status.py -q"}
```

Validate the queue first, then run a bounded batch:

```bash
python3 examples/runnable/queue-worker-loop.py --queue tasks.jsonl --dry-run
python3 examples/runnable/queue-worker-loop.py \
  --queue tasks.jsonl \
  --agent-command "codex exec" \
  --verify-command "python3 verify_item.py {id}" \
  --max-items 2 \
  --max-retries 2 \
  --command-timeout 900
```

**Done means:** the external verifier exits successfully and the item ID is persisted in `QUEUE_PROGRESS.jsonl`; reruns skip completed work.

### 4. Watch A Threshold Without Auto-Remediation

**Symptom:** a rollout, latency metric, pass rate, or spend metric needs bounded monitoring and evidence-backed escalation.

```bash
PROBE_CMD="./scripts/p95_latency_ms.sh" \
THRESHOLD=250 \
DIRECTION=max \
MAX_SAMPLES=12 \
INTERVAL_SECONDS=300 \
AGENT_CMD="codex exec" \
./examples/runnable/threshold-monitor-loop.sh
```

**Done means:** all samples stay within policy, or the first breach produces a durable receipt and read-only diagnosis. The starter never changes production.

## Adaptation Checklist

Before running any contract unattended:

- replace every generic source, command, file, and destination with a real one;
- keep the acting agent away from tests, scorers, policies, or thresholds that judge its work;
- narrow allowed paths, tools, credentials, and network access;
- make receipts reviewable and safe to retain;
- set time, retry, token, cost, and concurrency budgets;
- test the escalation path before trusting the success path;
- run first in a branch, worktree, sandbox, synthetic target, or read-only mode.
