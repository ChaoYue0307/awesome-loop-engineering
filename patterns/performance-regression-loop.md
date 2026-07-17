# Performance Regression Loop

## Objective

Turn a measured latency, throughput, memory, or cost regression into a reproducible profile, a narrow candidate fix, and a verified comparison against the same workload.

## Use This When

- A stable workload and performance budget exist.
- Correctness can be gated separately from speed or resource use.
- Runs can control warmup, hardware, load, and statistical noise.

Do not use this loop when production impact cannot be reproduced safely or the benchmark environment changes faster than the code.

## Trigger

- Event: benchmark or service-level threshold regresses beyond tolerance.
- Schedule: nightly or weekly performance suite.
- Manual bootstrap: "diagnose the regression between <baseline> and <candidate>."

## Intake

- Baseline and candidate commits, benchmark workload, environment fingerprint, profiles, and recent changes.
- Correctness suite, latency/throughput/memory budgets, and protected secondary metrics.
- Production traces or sampled telemetry when permitted.

## Agents

- Reproducer: confirms the regression under controlled conditions.
- Profiler: localizes time, allocation, I/O, or contention hotspots.
- Implementer: applies one evidence-backed change.
- Verifier: reruns correctness and repeated performance measurements.

## Workspace And Permissions

- Use an isolated worktree on fixed hardware or a controlled benchmark runner.
- Allow profiling and scoped implementation changes.
- Disallow benchmark edits, reduced workloads, disabled correctness checks, or production changes.

## Durable State

- Environment fingerprint, workload version, baseline distribution, profiles, hypothesis, candidate diff, repeated measurements, and decision.

## Loop Steps

1. Freeze the workload, environment, and correctness gate.
1. Reproduce the regression over the required warmup and sample count.
1. Profile before proposing a fix.
1. Change one measured bottleneck in an isolated candidate.
1. Run correctness first, then repeat the performance workload.
1. Compare distributions and protected metrics, not only the best run.
1. Accept, reject, or escalate with a reproducible receipt.

## Verification Gates

- Correctness and safety tests pass unchanged.
- Baseline and candidate use the same workload and environment fingerprint.
- The regression or improvement exceeds the declared noise tolerance.
- Tail latency, memory, throughput, and cost stay within protected budgets.
- Profile and raw measurements are attached to the decision.

## Budget And Exit

- Max retries: 3 candidate fixes.
- Max runtime: 180 minutes.
- Stop on recovery to budget, inability to reproduce, noisy environment, budget exhaustion, or an architectural bottleneck.

## Escalation

Escalate for production-only behavior, unstable infrastructure, hardware changes, correctness/performance trade-offs, or fixes that require architecture or capacity decisions.

## Loop Instruction

```text
Diagnose the performance regression between <baseline> and <candidate> on <workload>.
Fingerprint the environment, reproduce with <sample count> runs, and profile before editing.
Make one evidence-backed change, keep the workload and correctness gates fixed, then compare
the full measurement distribution and protected metrics. Stop after three candidates or when
the target budget is restored. Record raw measurements, profile, diff, and decision.
```

## Worked Example

A retrieval service's p95 latency rises from 180 ms to 265 ms. The loop reproduces the shift on the pinned dataset, profiles an added serialization pass, removes only that duplicate conversion, reruns correctness and 30 load samples, and accepts the patch when p95 returns below 190 ms without increasing memory or error rate.

## Failure Modes

- Comparing different hardware, datasets, concurrency, or warmup states.
- Optimizing a microbenchmark that does not represent user traffic.
- Reporting the best run instead of a distribution.
- Trading correctness or tail latency for a faster median.
- Editing the benchmark to make the candidate look better.

## Example Contract

- [`examples/performance-regression-loop.json`](../examples/performance-regression-loop.json)

## References

- [PERFOPT-Bench: Evaluating Coding Agents on Software Performance Optimization](https://arxiv.org/abs/2607.07744) - Evaluates the profile-diagnose-edit-verify loop with correctness and reproducible speedups.
- [OpenTelemetry Metrics](https://opentelemetry.io/docs/concepts/signals/metrics/) - Defines portable measurements for runtime behavior and service health.
