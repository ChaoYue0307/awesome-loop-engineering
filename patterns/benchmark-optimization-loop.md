# Benchmark Optimization Loop

## Objective

Improve a measurable system outcome through small experiments while preserving correctness and keeping every accepted change reproducible.

## Use This When

- You have a stable benchmark, eval suite, or objective metric.
- One change can be tested independently of the next.
- The system can reject regressions and restore the last accepted state.

Do not use this loop when the score is easy to game, the benchmark is still changing, or the real outcome requires human judgment that the metric does not capture.

## Trigger

- Schedule: a bounded overnight or weekly experiment window.
- Event: a new baseline, model, dataset, or optimization target is available.
- Manual bootstrap: "run up to five benchmark-backed optimization experiments."

## Intake

- Baseline artifact, benchmark command, correctness checks, and target metric.
- Prior experiment ledger, failed hypotheses, and protected files.
- Compute, token, time, and concurrency budgets.

## Agents

- Experiment designer: proposes one falsifiable change and expected effect.
- Implementer: applies only that change in an isolated candidate workspace.
- Verifier: runs correctness checks and the frozen benchmark.
- Recorder: accepts or rejects the candidate and updates the experiment ledger.

## Workspace And Permissions

- Use a disposable worktree, branch, or sandbox per candidate.
- Allow edits only to the declared optimization surface.
- Keep benchmark data, scoring code, holdout cases, and acceptance thresholds read-only.
- Disallow test deletion, scorer edits, hidden-test inspection, and concurrent candidates that exceed the budget.

## Durable State

- Baseline version and score, hypothesis, candidate diff, commands, raw results, cost, decision, and rejection reason.
- The last accepted artifact remains the parent of the next experiment.

## Loop Steps

1. Freeze the baseline, benchmark version, correctness gate, and budget.
1. Read the ledger so the next hypothesis does not repeat a failed experiment.
1. Propose one bounded change with a predicted effect.
1. Apply it in an isolated candidate workspace.
1. Run correctness checks before the benchmark.
1. Compare repeated benchmark runs against the accepted baseline.
1. Accept only a reproducible improvement that clears the minimum delta; otherwise reject and restore the baseline.
1. Record the full receipt and continue until the target or budget is reached.

## Verification Gates

- Correctness and safety checks pass unchanged.
- The benchmark, dataset split, scorer, and environment match the recorded baseline.
- Improvement clears the declared minimum delta across the required repeats.
- The candidate does not worsen protected secondary metrics beyond tolerance.
- The ledger contains enough evidence to reproduce the decision.

## Budget And Exit

- Max retries: 5 candidate experiments.
- Max runtime: 240 minutes.
- Stop on target attainment, budget exhaustion, two repeated hypotheses, benchmark instability, or a protected-metric regression.

## Escalation

Escalate when the metric conflicts with observed quality, a candidate changes the evaluator, results vary beyond tolerance, or the next experiment would broaden permissions or compute.

## Loop Instruction

```text
Optimize <artifact> against <benchmark> for at most five experiments.
Treat <correctness command> as a non-negotiable gate and <metric> as the optimization signal.
Change one declared variable per candidate in an isolated workspace. Never edit the
benchmark, scorer, holdout set, or protected tests. Accept a candidate only when repeated
runs improve the baseline by <minimum delta> without regressing <secondary metrics>.
Record every hypothesis, diff, command, score, cost, and accept/reject decision.
```

## Worked Example

A team wants to reduce an agent workflow's median latency without lowering task success. The loop starts from a frozen 78% success / 42-second baseline, tries one routing or caching change at a time, reruns the same 100-task suite three times, and accepts only candidates that keep success within one percentage point while cutting median latency by at least 5%.

## Failure Modes

- Optimizing on the same cases used to invent the change.
- Accepting a noisy single run as improvement.
- Changing multiple variables and losing causal attribution.
- Improving the headline metric while silently degrading cost, safety, or tail latency.
- Letting the agent modify the verifier that judges its own work.

## Example Contract

- [`examples/benchmark-optimization-loop.json`](../examples/benchmark-optimization-loop.json)

## References

- [A Self-Improving Coding Agent](https://arxiv.org/abs/2504.15228) - Demonstrates benchmark-gated self-modification with measurable gains.
- [Understanding the Challenges in Iterative Generative Optimization with LLMs](https://arxiv.org/abs/2603.23994) - Identifies evaluation and credit-assignment choices that make iterative optimization brittle.
