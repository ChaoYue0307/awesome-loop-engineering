# Pattern Matrix

A side-by-side comparison of all 20 loops in the [pattern library](README.md). Use it to pick a pattern, compare trade-offs, or check that your own loop names the same parts.

## How To Read This Matrix

- **Best for** is the symptom or job the loop solves. If you know the symptom, start from [Choose Your Loop](../README.md#choose-your-loop).
- **Trigger / cadence** is what starts a run: a schedule, an event, or a manual bootstrap.
- **Intake** is where the loop finds work each run.
- **Durable state** is what survives between runs, outside the model.
- **Verification gate** is the deterministic check that decides done, not the model's opinion.
- **Budget** is the hard stop on retries or runtime.
- **Escalation** is the moment a human takes over.
- **Runtime fit** suggests where the loop tends to run well; see the [runtime selection guide](../meta/RUNTIME_SELECTION.md) for the full comparison. It is a starting point, not a constraint.

Every pattern links to its full write-up and a schema-valid contract in [`examples/`](../examples/README.md).

## Matrix

| Pattern | Best for | Trigger / cadence | Intake source | Durable state | Verification gate | Budget | Escalation | Runtime fit |
| ------- | -------- | ----------------- | ------------- | ------------- | ----------------- | ------ | ---------- | ----------- |
| [PR babysitter](pr-babysitter.md) | A PR stalls on comments, CI, or conflicts | Schedule + PR events | PR metadata, reviews, checks | PR progress comment, last SHA | Required checks pass, comments resolved | 3 retries / 60 min | Architectural or force-push decisions | Claude Code routines, Codex automations, gh-aw |
| [CI repair loop](ci-repair-loop.md) | CI keeps failing on a mechanical cause | Event: required check fails | Failing check, logs, artifacts | Failing command, attempted fixes | Original failing command passes | 3 retries / 60 min | Test-infra or out-of-scope failures | Codex automations, gh-aw, shell/cron |
| [Docs drift collector](docs-drift-collector.md) | Docs may be stale versus code | Schedule: weekly | Changed files, docs, examples, CLI help | Verified drift items, false positives | Examples run, links pass | 2 retries / 60 min | Product behavior or generated-docs calls | Claude Code routines, gh-aw |
| [Deploy verifier](deploy-verifier.md) | A rollout needs watching | Event: deploy starts; poll 5-15 min | Dashboards, logs, traces, flags | Rollout phase, anomalies, decisions | Synthetic checks and thresholds hold | 2 retries / rollout window | Threshold breach or missing telemetry | Shell/cron, custom durable runtime |
| [Feedback clusterer](feedback-clusterer.md) | Feedback is noisy and unsorted | Schedule: daily or weekly | Issues, tickets, threads, reviews | Processed IDs, cluster definitions | Clusters cite sources, frequency vs severity | 1 retry / 90 min | Security, legal, or prioritization conflicts | Claude Code routines, Codex automations |
| [Dependency triage loop](dependency-triage-loop.md) | Dependency updates pile up | Schedule: weekly + bot PRs | Update PRs, advisories, lockfile diff | Processed updates, deferral reasons | Tests, typecheck, build, audit pass | 2 retries / 60 min | Major versions, advisories, migrations | gh-aw, Codex automations, shell/cron |
| [Evaluation regression loop](evaluation-regression-loop.md) | Agent evals regressed | Schedule: nightly + score drop | Eval runs, traces, recent commits | Run IDs, hypotheses, rerun scores | Targeted tasks return to baseline | 3 retries / 120 min | Scorer bugs or overfitting risk | Custom durable runtime, shell/cron |
| [Benchmark optimization loop](benchmark-optimization-loop.md) | A stable system should improve on a metric | Bounded schedule + new baseline | Frozen benchmark, correctness suite, ledger | Accepted baseline, candidate receipts | Repeated improvement with protected metrics intact | 5 candidates / 240 min | Metric conflict, evaluator drift, more compute | Custom durable runtime, isolated worktrees |
| [Security review loop](security-review-loop.md) | Sensitive changes need review | Event: sensitive diff; weekly pass | Diffs, threat model, scan output | Reviewed SHA, findings, false positives | Findings cite concrete evidence | 2 retries / 90 min | Credentials, crypto, exploitability doubt | Claude Code routines, gh-aw |
| [Adversarial red-team loop](adversarial-red-team-loop.md) | An agent needs active adversarial testing | Pre-release campaign + capability change | Threat model, sandbox target, known findings | Campaign ledger, minimized traces | Independent reproduction and policy citation | 3 confirmations / 120 min | Critical finding, real impact, scope ambiguity | Sandboxed custom runtime |
| [Accessibility regression loop](accessibility-regression-loop.md) | A UI introduced an accessibility failure | Event: accessibility check fails | Rule, route, viewport, interaction, diff | Before/after evidence, manual review | Original rule plus required human criteria pass | 3 retries / 90 min | Ambiguous semantics or design-system change | CI, Codex automations, local browser runtime |
| [Cost-control loop](cost-control-loop.md) | Agent spend is rising | Schedule + spend threshold | Usage telemetry, traces, billing | Baseline spend, proposed changes | Quality gates hold on a comparable sample | 2 retries / 60 min | Quality tradeoffs or routing changes | Custom durable runtime, shell/cron |
| [Performance regression loop](performance-regression-loop.md) | Latency, throughput, or memory regressed | Event: metric exceeds tolerance | Baseline/candidate, workload, profile | Environment, samples, profile, decision | Correctness plus repeated performance budget | 3 candidates / 180 min | Production-only or architectural bottleneck | Controlled benchmark runner, shell/cron |
| [Bug hunting loop](bug-hunting-loop.md) | Recurring bug discovery | Schedule: weekly on active modules | Logs, flaky tests, traces, diffs | Checked areas, reproductions | Reproducible steps or failing test | 3 retries / 90 min | Production-only or security-sensitive bugs | Claude Code routines, shell/cron |
| [Enterprise approval loop](enterprise-approval-loop.md) | A change needs sign-off | Schedule + gate/approver events | Change request, gates, approvers | Approval ledger, gate status | Every gate has a recorded human decision | 3 retries / SLA window | Failed gate or unresponsive approver | Custom durable runtime, gh-aw |
| [Incident response loop](incident-response-loop.md) | An incident just paged | Event: alert; refresh 2-5 min | Alert, dashboards, traces, changes | Incident timeline, hypotheses | Severity backed by impact evidence | 2 retries / incident life | Outage, data loss, or mitigation needed | Custom durable runtime, shell/cron |
| [Data-quality loop](data-quality-loop.md) | A dataset keeps drifting | Event: refresh; or nightly | New version, schema, prior baseline | Profile metrics, accepted exceptions | Hard rules pass before promotion | 2 retries / 90 min | Schema change or regulated fields | Custom durable runtime, shell/cron |
| [Knowledge freshness loop](knowledge-freshness-loop.md) | An agent knowledge index is stale | Daily refresh + source change | Approved sources, manifest, retrieval evals | Versioned index, provenance, tombstones | Freshness, retrieval, leakage, atomic promotion | 2 retries / 120 min | Source conflict, access change, sensitive data | Custom durable runtime, scheduled task |
| [Release-note loop](release-note-loop.md) | Release notes are a chore | Event: release branch or tag | Merged PRs, issues, commits | Processed IDs, draft changelog | Every entry links to a source | 2 retries / 60 min | Security advisories or wording calls | gh-aw, Codex automations |
| [Model-routing loop](model-routing-loop.md) | Model choice is ad hoc | Schedule + model/price change | Per-task telemetry, eval results | Task-class metrics, routing log | Replays hold quality within tolerance | 2 retries / 120 min | Privacy tier or quality-cost tradeoffs | Custom durable runtime |

## Notes

- Runtime fit is advisory. Most patterns run on more than one runtime; the [runtime selection guide](../meta/RUNTIME_SELECTION.md) compares persistence, file access, isolation, and permissions so you can choose deliberately.
- Budgets are defaults from each pattern's contract. Tune them to your blast radius before running unattended.
- Read-mostly patterns (deploy verifier, incident response, feedback clusterer, model routing) keep humans on any state-changing action by design.
