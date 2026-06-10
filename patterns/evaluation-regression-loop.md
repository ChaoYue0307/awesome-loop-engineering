# Evaluation Regression Loop

## Objective

Detect regressions in agent behavior, connect them to recent prompt/context/harness changes, and produce a verified repair proposal.

## Trigger

- Schedule: nightly or before release.
- Event: benchmark score drops, trace grader fails, evaluation suite changes, or agent prompt/harness changes land.
- Manual bootstrap/debug command: "investigate the latest agent evaluation regression."

## Intake

- Eval run ID, failing tasks, trace samples, baseline score, recent commits, prompt changes, harness changes, and model/runtime configuration.
- Known flaky evals and accepted score variance.
- Evaluation rubric, scorers, and task fixtures.

## Agents

- Investigator: compares failing traces against passing baseline traces.
- Hypothesis writer: identifies likely prompt, context, tool, scorer, or harness causes.
- Implementer: proposes the smallest prompt, context, harness, or test fixture patch.
- Verifier: reruns targeted evals and checks for new regressions.
- Judge: decides whether the evidence supports merging, deferring, or escalating.

## Workspace And Permissions

- Use a branch or sandbox with read access to traces and eval artifacts.
- Allow targeted eval reruns, scorer inspection, prompt/harness edits, and report generation.
- Disallow leaderboard claims, benchmark cherry-picking, or broad prompt rewrites without review.

## Durable State

- Eval run IDs, baseline comparison, failing task IDs, trace excerpts, hypotheses, patch attempts, rerun scores, and final decision.

## Loop Steps

1. Discover failed or degraded eval runs.
1. Load baseline traces, current traces, rubric, and prior regression notes.
1. Delegate trace comparison, hypothesis writing, patching, verification, and judgment.
1. Identify whether the failure is model behavior, context missingness, tool failure, scorer drift, fixture drift, or harness regression.
1. Patch the smallest plausible cause.
1. Rerun targeted evals first, then a broader smoke suite if the targeted rerun passes.
1. Persist evidence and either open a PR, report no-action, or escalate.

## Verification Gates

- Targeted failing tasks improve or return to baseline.
- No known sentinel tasks regress.
- Trace evidence supports the claimed cause.
- Score changes are reported with sample size, variance caveat, and run IDs.

## Budget And Exit

- Max retries: 3 patch attempts per regression cluster.
- Max runtime: 2 hours per run.
- Stop when the regression is repaired, classified as flaky or scorer drift, blocked by missing artifacts, or requires product judgment.

## Escalation

Escalate for ambiguous product-quality tradeoffs, benchmark methodology changes, scorer bugs, missing private traces, model-provider incidents, or changes that would overfit to a benchmark.

## Loop Instruction

```text
Investigate evaluation regression <run id>.
Compare failing traces against the last known good baseline.
Classify the likely cause before editing.
Patch only the smallest prompt, context, harness, scorer, or fixture issue supported by trace evidence.
Rerun targeted evals, record run IDs and score deltas, and escalate if the fix risks overfitting.
```

Example automation: run nightly after eval completion and open an issue or PR only when a regression cluster has reproducible evidence.

## Failure Modes

- Optimizing for one failing task and reducing general behavior.
- Treating flaky evals as real regressions without repeated runs.
- Changing scorers to make failures disappear.
- Reporting score deltas without run IDs or variance context.

## References

- [OpenAI agent evals](https://developers.openai.com/api/docs/guides/agent-evals) - Guidance for evaluating agent workflows from traces.
- [Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals) - Uses evals as the learning signal for harness improvement.
- [OpenTelemetry Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/) - Portable tracing conventions for model and tool calls.
