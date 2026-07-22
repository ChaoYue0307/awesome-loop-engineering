# Fleet Coordination Loop

## Objective

Run many coding agents in parallel against one codebase or backlog without merge collisions, duplicated work, or unreviewed changes reaching the integration branch.

## Use This When

- More than a handful of agents work the same repository or task queue concurrently.
- Agent throughput is limited by coordination, not generation: collisions, rework, and review pile-ups.
- You can define a deterministic landing gate that every parallel change must pass before integration.

Use the PR-babysitter loop to shepherd a single change. Use this pattern when the unit of work is the fleet: assigning, isolating, verifying, and landing many parallel changes.

## Trigger

- Schedule: continuous while the backlog is non-empty, or in timed waves.
- Event: backlog growth past a threshold, a milestone branch opening, or a batch of verified tasks becoming ready.
- Manual bootstrap: "work this backlog with <N> parallel agents until the queue is empty or budget is spent."

## Intake

- The task backlog with priorities, dependencies, and claim status.
- Repository state: protected branches, required checks, and the landing gate definition.
- Fleet policy: max concurrency, per-agent budgets, and which task classes may run unattended.

## Agents

- Dispatcher: claims tasks, assigns them to workers, and prevents duplicate claims.
- Workers: implement one bounded task each inside an isolated workspace.
- Verifier: runs the landing gate on each candidate change independently of the worker that produced it.
- Integrator: serializes landings through a merge queue and resolves ordering.

## Workspace And Permissions

- One isolated worktree, branch, or container per worker; no shared mutable checkout.
- Allow workers to read the repository and write only to their own workspace and claim record.
- Disallow direct pushes to the integration branch, cross-worker file claims, and landing without the gate.

## Durable State

- The claim ledger: which agent owns which task, started when, with what budget remaining.
- Merge-queue state: ordered candidates, gate results, and landing receipts.
- Fleet telemetry: per-task cost, retry counts, collision events, and gate failures for tuning concurrency.

## Loop Steps

1. Refresh the backlog and reconcile stale claims from dead or expired workers.
1. Dispatch unclaimed ready tasks to idle workers up to the concurrency cap.
1. Each worker implements its task in isolation and submits a candidate change.
1. Verify each candidate with the landing gate: build, tests, lint, and scoped-diff checks.
1. Queue passing candidates; land them serially, rebasing or re-verifying on conflict.
1. Return failed candidates to their worker with evidence, up to the retry budget.
1. Record receipts and telemetry; adjust concurrency if collisions or costs trend up.

## Verification Gates

- Every landed change passed the full landing gate after its final rebase, not before.
- Each change's diff stays inside its claimed task scope.
- No two live claims cover the same task or the same protected files.
- The integration branch stays green: a failed landing halts the queue, not just the one change.
- Every landing has a receipt linking task, worker, gate results, and commit.

## Budget And Exit

- Per-task: bounded retries and runtime before the task returns to the backlog for a human.
- Per-fleet: max concurrent workers, total token or cost ceiling, and a wall-clock window.
- Stop when the backlog is empty, the budget is spent, or the integration branch cannot be kept green.

## Escalation

Escalate when the same task fails its gate repeatedly, two tasks genuinely require the same files, gate infrastructure itself breaks, or landing order forces a product decision no worker owns.

## Loop Instruction

```text
Work the backlog at <repo> with up to <N> parallel workers.
One isolated workspace per worker; claim tasks through the ledger, never work an unclaimed task.
Every candidate change must pass the landing gate after final rebase; land serially through the queue.
Return gate failures to the owning worker with evidence, within retry budget.
Halt the queue and escalate if the integration branch goes red or claims conflict.
```

## Worked Example

A migration backlog of 140 mechanical refactor tasks runs with twelve workers. The dispatcher hands out tasks by dependency order; each worker edits in its own worktree and submits a branch. The verifier runs build, tests, and a scoped-diff check per candidate; the merge queue lands nine changes per hour serially, bounces two candidates back with failing-test evidence, and reconciles one stale claim after a worker times out. The fleet exits with 137 landed, 3 escalated as genuinely entangled, and per-task receipts for review.

## Failure Modes

- Shared checkouts, so parallel edits trample each other before verification.
- Verifying before the final rebase and landing changes that break the branch anyway.
- Two workers silently duplicating one task because claims are advisory.
- Per-agent monitors missing fleet-level effects: correlated failures and coordinated drift.
- Scaling concurrency past what the merge queue and reviewers can absorb, converting throughput into backlog.

## Example Contract

- [`examples/fleet-coordination-loop.json`](../examples/fleet-coordination-loop.json)

## References

- [Scaling Long-Running Autonomous Coding](https://cursor.com/blog/scaling-agents) - Cursor's coordination designs, from flat agents with locking to a planner, worker, and judge hierarchy pushing to a single branch.
- [Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors](https://arxiv.org/abs/2607.07368) - Shows per-agent monitors weaken as more agents coordinate, motivating fleet-level gates and telemetry.
- [claude-code-merge-queue](https://github.com/funador/claude-code-merge-queue) - A minimal landing gate: serialize parallel agents through a FIFO queue that blocks integration until a check command passes.
