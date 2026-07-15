<p align="center">
  <img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering cover" width="100%">
</p>

<h1 align="center">Awesome Loop Engineering</h1>

<p align="center">
  Curated resources and practical patterns for designing recurring, stateful, verified AI-agent and coding-agent loops.
</p>

<!-- Keep the resources badge count in sync with data/resources.csv, Repository Highlights, and the landing-page stats on every sweep. -->
<p align="center">
  <a href="https://github.com/sindresorhus/awesome"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="https://img.shields.io/badge/project-site-38bdf8" alt="project site"></a>
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering"><img src="https://img.shields.io/badge/HF-dataset-ffcc4d" alt="Hugging Face dataset"></a>
  <img src="https://img.shields.io/badge/resources-509-a78bfa" alt="resources">
  <img src="https://img.shields.io/badge/patterns-15-38bdf8" alt="patterns">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC0--1.0-64748b" alt="license"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-22c55e" alt="PRs welcome"></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">中文</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.pt-BR.md">Português</a> |
  <a href="TRANSLATIONS.md">Help translate</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">Landing page</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Hugging Face dataset</a>
</p>

Awesome Loop Engineering is a curated, implementation-oriented field guide to **Loop Engineering**: the layer above prompt, context, and harness engineering for designing recurring AI-agent systems.

Prompt engineering improves what you ask the model. Context engineering improves what the model can see. Harness engineering improves the tools, permissions, sandboxes, and checks around one agent run. **Loop Engineering sits above all three**: it is the emerging AI and coding-agent practice of moving from manually prompting agents turn by turn to designing loops that do the prompting, supervision, verification, state updates, and re-triggering for you.

A loop discovers work, hands it to one or more agents, checks the result, records state, decides what should happen next, and runs again on a cadence or until a verifiable goal is reached.

This repository is about the new AI-agent meaning of Loop Engineering. It is **not** about software event loops, control theory, growth loops, generic workflow automation, or non-AI feedback systems.

**Quick orientation for first-time visitors:**

- **What it is:** the layer that governs how agent work is discovered, delegated, verified, retried, and escalated over time, not just for a single run.
- **Why it matters now:** As coding agents move from one-off prompts to background automation, the design challenge shifts from "what do I ask?" to "how does the system keep working reliably?" This list exists because no existing collection focused on that layer.
- **Who this is for:** builders of AI agents, coding agents, and orchestration systems; reliability and eval engineers; teams adding recurring agent loops to production infrastructure.
- **Where to start:** Canonical Definition, Loop Contract, Start Here, then Pattern Library.

## Contents

- [Why This Repo Exists](#why-this-repo-exists)
- [Mental Model](#mental-model)
- [How To Use This List](#how-to-use-this-list)
- [Reading Paths](#reading-paths)
- [Choose Your Loop](#choose-your-loop)
- [Canonical Definition](#canonical-definition)
- [Concept Guides](#concept-guides)
- [Maintainer Picks](#maintainer-picks)
- [Repository Highlights](#repository-highlights)
- [Resource Type Legend](#resource-type-legend)
- [Start Here](#start-here)
- [Scope Boundary](#scope-boundary)
- [The Loop Contract](#the-loop-contract)
- [Loop Design Checklist](#loop-design-checklist)
- [Loop Maturity Model](#loop-maturity-model)
- [Pattern Library](#pattern-library)
- [Core Loop Primitives](#core-loop-primitives)
- [Official Runtime Guides](#official-runtime-guides)
- [Research Foundations](#research-foundations)
- [Agent Workflow Patterns](#agent-workflow-patterns)
- [Coding-Agent Loop Systems](#coding-agent-loop-systems)
- [Verification And Feedback Gates](#verification-and-feedback-gates)
- [Securing Unattended Loops](#securing-unattended-loops)
- [State, Memory, And Context Persistence](#state-memory-and-context-persistence)
- [Orchestration And Multi-Agent Delegation](#orchestration-and-multi-agent-delegation)
- [Benchmarks And Evaluation](#benchmarks-and-evaluation)
- [Operations Playbooks](#operations-playbooks)
- [Templates And Patterns](#templates-and-patterns)
- [Examples And Schema](#examples-and-schema)
- [Community Gallery](#community-gallery)
- [Critiques, Risks, And Limitations](#critiques-risks-and-limitations)
- [Adjacent Awesome Lists](#adjacent-awesome-lists)
- [Discovery And Distribution](#discovery-and-distribution)
- [Roadmap And Discussion](#roadmap-and-discussion)
- [Citation](#citation)

## Why This Repo Exists

Loop Engineering is becoming a distinct craft because the leverage point is moving from better single prompts, richer context, and stronger harnesses to recurring systems that decide when and how agents should run. Mature agent workflows now combine goals, state, work isolation, tool permissions, feedback gates, retries, escalation, and receipts. This list exists to make that craft easier to learn, compare, and practice without mixing it with unrelated loop concepts or generic AI-agent hype.

## Mental Model

Prompt engineering asks: **what should I say to the model?**

Context engineering asks: **what state and knowledge should the model see?**

Harness engineering asks: **what tools, permissions, tests, sandboxes, and feedback should surround the agent?**

Loop engineering asks: **what recurring system should discover work, delegate to agents, verify results, persist state, decide next actions, and re-run when the human is no longer in the inner loop?**

Prompt, context, and harness engineering make one agent run better. Loop Engineering makes agent work repeatable, observable, and governable over time.

<p align="center">
  <img src="assets/loop-engineering-stack.svg" alt="Diagram of the engineering stack: Prompt, Context, and Harness Engineering improve one run; Loop Engineering governs recurring agent work over time" width="100%">
</p>

Loop shape:

```text
Objective
  -> Trigger / cadence
  -> Discover / intake work
  -> Delegate to agents
  -> Act in an isolated workspace
  -> Verify with tests, evals, traces, or reviewers
       -> if failed: feed back the evidence and retry
       -> if passed: persist state and decide what happens next
  -> Repeat, report, open a PR, or escalate to a human
```

<p align="center">
  <img src="assets/loop-lifecycle.svg" alt="Loop Engineering lifecycle: Intake, Delegate, Act, Verify, Persist, Decide; Decide retries by feeding evidence back, escalates to a human, or exits when the goal is met" width="100%">
</p>

## How To Use This List

Start with the first-read resources and the Loop Contract if the term is new. For implementation work, move through core primitives, runtime guides, templates, and patterns. For reliability work, focus on verification gates, securing unattended loops, state persistence, critiques, and limitations. Contributions should prefer primary sources, official docs, papers, and implementation-heavy write-ups.

## Reading Paths

Choose a path based on your intent.

- Learn the concept: canonical definition, mental model, comparison guide, and the Loop Contract.
- Implement a loop: core primitives, official runtime guides, the pattern library, and examples.
- Improve reliability or evals: verification gates, securing unattended loops, benchmarks, critiques, and limitations.
- Contribute: the community gallery, templates, and contribution guide.

## Choose Your Loop

Start from the problem you have, not the pattern you want. Find the pattern name below, then open its full write-up in the Pattern Library section, or compare every pattern in the [pattern matrix](patterns/MATRIX.md), which also links each one by symptom.

| When you say...                  | Reach for the loop         |
| -------------------------------- | -------------------------- |
| "My PR is stuck"                 | PR babysitter              |
| "CI keeps failing"               | CI repair loop             |
| "The docs may be stale"          | Docs drift collector       |
| "A deploy needs monitoring"      | Deploy verifier            |
| "Feedback is noisy"              | Feedback clusterer         |
| "Dependency updates pile up"     | Dependency triage loop     |
| "Agent evals regressed"          | Evaluation regression loop |
| "Sensitive changes need review"  | Security review loop       |
| "Agent spend is rising"          | Cost-control loop          |
| "I need recurring bug discovery" | Bug hunting loop           |
| "A change needs sign-off"        | Enterprise approval loop   |
| "An incident just paged"         | Incident response loop     |
| "A dataset keeps drifting"       | Data-quality loop          |
| "Release notes are a chore"      | Release-note loop          |
| "Model choice is ad hoc"         | Model-routing loop         |

Not sure which runtime should run it? See the [runtime selection guide](meta/RUNTIME_SELECTION.md).

## Canonical Definition

**Loop Engineering** is the AI and coding-agent practice of designing recurring systems that discover work, delegate it to agents, verify results, persist state, decide next actions, and run again on a cadence, event, or until a verifiable goal is reached.

## Concept Guides

These repository-native guides define the concept, boundaries, and practical artifacts without relying on vendor-specific terminology.

- 🧾 **Template** [Canonical Definition](DEFINITION.md) - Short definition, positioning, minimal loop test, and citation note.
- 🧾 **Template** [Loop Engineering Manifesto](MANIFESTO.md) - Concise statement of the concept, commitments, non-goals, and success standard.
- 🧾 **Template** [Loop Engineering Taxonomy](TAXONOMY.md) - Classification by trigger, intake, verification, state model, topology, and operating domain.
- ⚠️ **Critique** [Loop Engineering Anti-Patterns](ANTI-PATTERNS.md) - Common failure modes such as prompt loops with no contract, infinite retries, model self-approval, hidden state, and unsafe autonomy.
- 🧾 **Template** [Comparison Guide](COMPARISON.md) - Distinguishes Loop Engineering from prompt engineering, context engineering, harness engineering, workflow automation, agent workflows, and evaluation loops.
- 🧾 **Template** [Sourced Signals And Quotes](QUOTES.md) - Short sourced signals from linked public materials that anchor the emerging concept.
- 🧾 **Template** [Outreach Kit](meta/OUTREACH.md) - Conservative messages for inviting corrections, sources, and real-world loop patterns.

## Maintainer Picks

A compact path through the repository. Each resource is linked in full in the section named in parentheses.

- Concept: Addy Osmani's Loop Engineering essay frames the practice (Start Here), and the Canonical Definition and Manifesto fix the scope and principles (Concept Guides).
- Foundations: the harness-layer taxonomy decomposes control, agency, and runtime beneath the loop and proposes a HarnessCard so reported agent gains can be separated from harness effects (Agent Workflow Patterns).
- Practice: the Codex long-horizon runbook (Official Runtime Guides) and Claude's scheduled-task docs (Core Loop Primitives) cover the core mechanics, then the PR babysitter and CI repair patterns turn the contract into operating models (Pattern Library).
- Reliability: "Give It Backpressure" (Verification And Feedback Gates) and "Building Effective Agents" (Agent Workflow Patterns) make verification the learning signal, with the Anti-Patterns guide listing failure modes to avoid (Concept Guides).
- Reusable artifacts: the loop contract schema and validated example specs make the contract concrete (Examples And Schema), and the Loop Gallery is the format for sharing real or anonymized loops (Community Gallery).

## Repository Highlights

Beyond the curated list, this repository also maintains:

- 509 curated resource rows with tabular exports
- 15 operational loop patterns with a comparison matrix
- 15 schema-validated loop contracts
- 6 runnable loop templates
- A community gallery for real or anonymized loops
- 8 language entry points
- A standalone landing page and a Hugging Face dataset mirror
- An active discussion thread for Loop Engineering patterns

## Resource Type Legend

- 📄 **Paper**: academic paper, preprint, or technical report.
- 📝 **Blog**: essay, field note, article, or practitioner write-up.
- 📚 **Docs**: official product, API, SDK, or platform documentation.
- 🧰 **Tool**: repository, framework, SDK, runtime, or implementation.
- 🧪 **Benchmark**: benchmark, eval suite, leaderboard, or evaluation dataset.
- 🔁 **Pattern**: real-world loop pattern, operational playbook, or reusable workflow.
- 🧾 **Template**: template, checklist, schema, repository guide, or contribution artifact.
- 🧭 **List**: adjacent awesome list, ecosystem map, or curated collection.
- ⚠️ **Critique**: risk analysis, limitation, caveat, or skeptical take.

## Start Here

Direct resources about the new AI/coding-agent meaning of Loop Engineering.

- 📝 **Blog** [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - Addy Osmani's framing of loop engineering as the layer above manually prompting coding agents, with concrete primitives across Codex and Claude Code; also on [Substack](https://addyo.substack.com/p/loop-engineering) with the original discussion trail and Steinberger and Cherny quotations.
- 📝 **Blog** [Peter Steinberger on designing loops](https://x.com/steipete/status/2063697162748260627) - The June 2026 post - "you shouldn't be prompting coding agents anymore, you should be designing loops that prompt your agents" - that catalyzed the current discussion.
- 📝 **Blog** [Boris Cherny: five tips for running Opus autonomously for hours or days](https://x.com/bcherny/status/2063792263067754658) - The Claude Code creator's compact loop recipe: auto-mode permissions, dynamic workflows, `/goal` or `/loop`, the cloud runner, and end-to-end self-verification.
- 📝 **Blog** [Loop Engineering](https://cobusgreyling.substack.com/p/loop-engineering) - Concise explanation of the shift from prompting agents to designing loops that discover work, delegate, verify, persist, and continue.
- 📝 **Blog** [Stop Prompting. Design the Loop.](https://www.pulumi.com/blog/stop-prompting-design-the-loop/) - Practical breakdown of loop building blocks - automations, worktrees, skills, connectors, subagents - plus external memory and verification through oracles such as tests and builds.
- 📝 **Blog** [Writing Loops, Not Prompts, Explained](https://rico.codes/loops-not-prompts) - Rico Kahler's break-even model for when a recurring task justifies building a loop instead of prompting, with stop conditions, evidence collection, and an execution-horizon framing for moving from execution-bound to judgment-bound work.
- 📝 **Blog** [Loop Engineering: A Guide for Engineers and Practitioners](https://medium.com/@adnanmasood/loop-engineering-a-guide-for-engineers-and-practitioners-893bb65ea943) - Adnan Masood's practitioner guide that organizes loop design into triggers, topologies, verifiers, and termination rules, with coverage of failure modes, cost control, and observability for production agent loops.
- 📝 **Blog** [Loop Engineering: When Generation Gets Cheap, Judgment Gets Expensive](https://sderosiaux.substack.com/p/loop-engineering-cheap-generation) - Stephane Derosiaux's essay on the economics of the loop layer (generation becomes abundant while judgment becomes the bottleneck), proposing evaluator agents that must act rather than merely review, and cataloging failure modes such as unverified merges and quota depletion.
- 📝 **Blog** [Andrew Ng on Loop Engineering and the Three Loops of AI-Native Product Development](https://x.com/AndrewYNg/status/2071988145667928442) - Andrew Ng's letter laying out three product-development loops (agentic coding in minutes, developer feedback in hours, external feedback in days) and arguing that human-in-the-loop persists wherever the human knows something the AI does not.
- 📝 **Blog** [From Prompting Agents to Loop Engineering](https://x.com/omarsar0/status/2068008743153832264) - DAIR.AI founder Elvis Saravia's X article examining the claim that you should stop prompting coding agents and start designing loops that prompt them for you.
- 📝 **Blog** [My Lord! AI Programming Undergoes Another Major Shift](https://eu.36kr.com/en/p/3844224911346184) - Broad coverage of the Boris Cherny and Peter Steinberger discussion, including the distinction between cold-start scripts and persistent agent loops.
- 📝 **Blog** [The Anthropic leader who built Claude Code ditched prompting - now he writes loops](https://thenewstack.io/loop-engineering/) - The New Stack's report on Boris Cherny's shift from prompting to loop writing and what it changes about developer workflow.
- 📝 **Blog** [Engineering for Agents That Never Sleep](https://nader.substack.com/p/engineering-for-agents-that-never) - Cognition's Nader Dabit predicts the human-initiated share of Devin sessions will invert from 70/30 to 10/90 within a year as signals like alerts and failing tests trigger agents directly, recasting the engineer's job as designing triggers, constraints, and quality gates.
- 📝 **Blog** [Loop Engineering Orange Book](https://github.com/alchaincyf/loop-engineering-orange-book) - Plain-language bilingual (Chinese and English) field guide to loop engineering by HuaShu, framing the discipline as one floor above harness engineering: the outer system that decides when and why agents run.
- 📝 **Blog** [How I AI: How to Write AI Agent Loops in Claude Code and Codex](https://www.lennysnewsletter.com/p/how-i-ai-how-to-write-ai-agent-loops) - Mozilla distinguished engineer Brian Grinstead demonstrates goal-based and scheduled loops, including a daily PR-review loop with per-PR subagents, on Lenny's Newsletter.

## Scope Boundary

| In scope                                                                                                            | Out of scope                                                    |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| AI/coding-agent loops that coordinate prompts, context, harnesses, verification, and state over repeated agent runs | Software event loops, UI/game loops, or control theory loops    |
| Scheduled, goal-driven, or event-triggered agent work                                                               | Generic cron jobs with no agentic reasoning or verification     |
| Agent loops with durable state, worktrees, checkpoints, traces, or progress files                                   | One-off prompt examples with no loop, state, or feedback signal |
| Verification loops using tests, CI, evals, reviewers, or deterministic gates                                        | Pure AI news, generic product pages, or marketing copy          |
| Multi-agent maker/checker/delegation patterns                                                                       | Broad agent lists without specific loop-design relevance        |

## The Loop Contract

A useful loop has a contract. If one of these is missing, the loop usually becomes either a manual prompt habit or an unsafe background automation. Prompt, context, and harness choices are ingredients; the loop contract is the operating layer that connects them over time.

<p align="center">
  <img src="assets/loop-contract-cards.svg" alt="Loop Contract cards: objective, trigger, intake, workspace, context, delegation, verification, state, budget, escalation, and exit" width="100%">
</p>

| Part              | Design question                        | Common artifact                                              |
| ----------------- | -------------------------------------- | ------------------------------------------------------------ |
| Objective         | What should the loop optimize for?     | Goal, issue, PRD, runbook                                    |
| Trigger           | When does the loop run?                | Schedule, webhook, `/loop`, `/goal`, automation              |
| Discover / Intake | How does the loop find work?           | GitHub queries, Linear filters, CI failures, feedback stream |
| Workspace         | Where can the agent act safely?        | Worktree, sandbox, branch, container                         |
| Context           | What durable knowledge should it load? | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, docs                   |
| Delegation        | Which agent does which job?            | Explorer, implementer, reviewer, judge                       |
| Verification      | What says "yes" or "no"?               | Tests, typecheck, lint, evals, trace graders                 |
| State             | What survives the next run?            | Progress file, database checkpoint, trace, issue comment     |
| Budget            | When should it stop spending?          | Max turns, max retries, token budget, time box               |
| Escalation        | When does a human take over?           | PR, issue, Slack alert, triage inbox                         |
| Exit              | How does the loop know it is done?     | Acceptance criteria, passing checks, no work found           |

Good loop documentation should make the contract visible. A reader should be able to tell what triggers the loop, what state it reads, what it is allowed to change, how it verifies progress, and when it stops.

## Loop Design Checklist

| Check                           | Question                                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Name one objective              | Does the loop optimize for a specific outcome instead of a vague goal such as "improve the repo"?    |
| Define the intake               | Where does work enter: PR comments, CI failures, issues, logs, eval failures, feedback, or schedule? |
| Isolate execution               | Does the agent act in a worktree, sandbox, branch, container, or read-only mode?                     |
| Write the feedback signal first | Do tests, typechecks, lint, evals, policy checks, or trace graders exist before retries begin?       |
| Persist state outside the model | Does progress survive in files, issue comments, checkpoints, traces, or a database?                  |
| Separate maker and checker      | Does something other than the acting agent decide whether the work is done?                          |
| Put a budget on autonomy        | Are runtime, turns, retries, token spend, and concurrent workers capped?                             |
| Design escalation               | Is it clear when the loop should open a PR, file an issue, ask a human, or stop?                     |
| Keep receipts                   | Are commands, evidence, changed files, and stop reasons recorded?                                    |

## Loop Maturity Model

| Level | Name                       | Description                                                                        |
| ----- | -------------------------- | ---------------------------------------------------------------------------------- |
| 0     | Manual prompting           | A human reads state and writes the next prompt.                                    |
| 1     | Scripted retry             | A shell/script loop feeds errors back to an agent.                                 |
| 2     | Scheduled loop             | The agent runs on a cadence and reports findings.                                  |
| 3     | Stateful loop              | Progress survives across sessions through files, issues, checkpoints, or traces.   |
| 4     | Self-verifying loop        | Deterministic checks or evaluator agents gate completion.                          |
| 5     | Multi-agent loop           | Specialized agents split discovery, implementation, review, and judgment.          |
| 6     | Production-supervised loop | Observability, budgets, approvals, rollback, and human escalation are first-class. |

Most teams should climb this model slowly. A reliable Level 3 loop with clear state and deterministic checks is usually more valuable than a flashy Level 5 loop with vague goals.

## Pattern Library

Practical loop patterns translate the abstract contract into runnable operating models. Each pattern documents the trigger, discover/intake step, agents, workspace, state, verification gates, retry budget, escalation path, and loop instruction.

- 🔁 **Pattern** [PR babysitter](patterns/pr-babysitter.md) - Repeatedly checks review comments, CI, merge conflicts, stale threads, and readiness to merge.
- 🔁 **Pattern** [CI repair loop](patterns/ci-repair-loop.md) - Reproduces failing checks, patches narrowly, reruns evidence, and escalates when failures are outside scope.
- 🔁 **Pattern** [Docs drift collector](patterns/docs-drift-collector.md) - Finds mismatches between docs and code, proposes small patches, and verifies examples.
- 🔁 **Pattern** [Deploy verifier](patterns/deploy-verifier.md) - Watches rollout signals, compares them with release expectations, and stops on anomalies.
- 🔁 **Pattern** [Feedback clusterer](patterns/feedback-clusterer.md) - Periodically groups GitHub, Linear, Slack, support, or social feedback into actionable themes.
- 🔁 **Pattern** [Dependency triage loop](patterns/dependency-triage-loop.md) - Classifies dependency updates, applies safe groups, verifies them, and escalates risky upgrades.
- 🔁 **Pattern** [Evaluation regression loop](patterns/evaluation-regression-loop.md) - Investigates degraded agent evals with baseline traces, targeted reruns, and repair proposals.
- 🔁 **Pattern** [Security review loop](patterns/security-review-loop.md) - Reviews sensitive diffs with evidence-backed findings, safe permissions, and human approval boundaries.
- 🔁 **Pattern** [Cost-control loop](patterns/cost-control-loop.md) - Monitors agent workflow spend, identifies waste, proposes scoped savings, and preserves quality gates.
- 🔁 **Pattern** [Bug hunting loop](patterns/bug-hunting-loop.md) - Discovers, reproduces, minimizes, and reports bugs with concrete evidence.
- 🔁 **Pattern** [Enterprise approval loop](patterns/enterprise-approval-loop.md) - Drives a permissioned change through required gates and approvers with a full audit trail.
- 🔁 **Pattern** [Incident response loop](patterns/incident-response-loop.md) - Triages an alert into an owned, evidence-backed incident with a postmortem seed.
- 🔁 **Pattern** [Data-quality loop](patterns/data-quality-loop.md) - Validates each dataset refresh against quality rules and quarantines bad versions.
- 🔁 **Pattern** [Release-note loop](patterns/release-note-loop.md) - Drafts release notes from merged commits, issues, and PRs with linked evidence.
- 🔁 **Pattern** [Model-routing loop](patterns/model-routing-loop.md) - Routes tasks across models on measured quality, latency, privacy, and cost.

## Core Loop Primitives

Feature-level building blocks you assemble a loop from: schedulers, goals, worktrees, hooks, skills, plugins, and protocols.

- 📚 **Docs** [Automations - Codex app](https://developers.openai.com/codex/app/automations) - Codex background automations for recurring tasks, triage inboxes, skills, and worktree isolation.
- 📚 **Docs** [Follow a goal - Codex use cases](https://developers.openai.com/codex/use-cases/follow-goals) - Official guidance for durable objectives with stopping conditions, validation commands, checkpoints, and progress logs.
- 📚 **Docs** [Worktrees - Codex app](https://developers.openai.com/codex/app/worktrees) - Codex worktree model for isolated parallel tasks and handoffs between local and background workspaces.
- 📚 **Docs** [Prompting - Codex](https://developers.openai.com/codex/prompting) - Explains the Codex loop, threads, context, and `/goal` mode.
- 📚 **Docs** [Customization - Codex](https://developers.openai.com/codex/concepts/customization) - Maps `AGENTS.md`, memories, skills, MCP, and subagents into a coherent customization stack.
- 📚 **Docs** [Agent Skills - Codex](https://developers.openai.com/codex/skills) - Official skill format for reusable workflows, scripts, MCP dependencies, invocation policy, and plugin packaging.
- 📚 **Docs** [Plugins - Codex](https://developers.openai.com/codex/plugins) - Bundles skills, app integrations, and MCP servers into reusable loop capabilities.
- 🧰 **Tool** [dotskills](https://github.com/vincentkoc/dotskills) - A `.skills` registry of curated Codex and OpenClaw skills, framed as an "ADE Loop" (Agent Development Environment to registry to Skills Gym) where reusable skills are developed, shared, and evaluated across runs.
- 📚 **Docs** [Slash commands in Codex CLI](https://developers.openai.com/codex/cli/slash-commands) - CLI commands for switching agent threads, browsing skills, inspecting MCP tools, and using subagent workflows.
- 🔁 **Pattern** [Autonomous Loops](https://claudecodeguide.dev/docs/patterns/autonomous-loops) - Claude Code pattern using task files, stop hooks, restart behavior, hard limits, and a kill switch.
- 📚 **Docs** [Claude Code Glossary](https://code.claude.com/docs/en/glossary.md) - Defines the agentic loop, hooks, subagents, skills, MCP, and related primitives in Claude Code terminology.
- 📚 **Docs** [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal) - `/goal` runs turn after turn until a completion condition is met by a verifier.
- 📚 **Docs** [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) - `/loop`, scheduled tasks, reminders, monitor tools, and session-scoped recurring prompts.
- 📚 **Docs** [Automate work with routines](https://code.claude.com/docs/en/routines) - Claude Code routines: persistent cloud automations triggered by schedules, API calls, or GitHub events, with connectors, scoped environments, and branch-push limits.
- 📚 **Docs** [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) - Local recurring runs on your own machine, with the persistence, file-access, permission, worktree, and missed-run trade-offs that distinguish them from `/loop` and cloud routines.
- 📚 **Docs** [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees) - Worktree isolation for parallel sessions and subagents so concurrent edits do not collide.
- 📚 **Docs** [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) - Claude Code hooks guide for deterministic lifecycle control around model actions.
- 📚 **Docs** [Hooks reference](https://code.claude.com/docs/en/hooks.md) - Event-level reference for session, turn, tool-call, and subagent hooks.
- 📚 **Docs** [Common workflows - Claude Code](https://code.claude.com/docs/en/common-workflows) - Practical workflows for worktrees, subagents, CI, batch processing, planning, and resuming prior work.
- 📚 **Docs** [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view.md) - Dashboard for dispatching, monitoring, and attaching to background agent sessions.
- 📚 **Docs** [Run agents in parallel](https://code.claude.com/docs/en/agents.md) - Compares agent view, subagents, agent teams, worktrees, tasks, and workflows for parallel work.
- 📚 **Docs** [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows) - Moves loop state and branching into workflow scripts so large tasks do not overload the conversation context.
- 📚 **Docs** [Create plugins](https://code.claude.com/docs/en/plugins) - Packaging model-invoked skills, agents, hooks, MCP servers, monitors, and settings as shareable loop components.
- 📚 **Docs** [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) - Standard protocol for exposing tools and data sources to agent loops.
- 📚 **Docs** [Allowing GitHub Copilot CLI to work autonomously](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot) - Copilot CLI autopilot mode plus `/every` and `/after` scheduling, turning the CLI into an unattended loop that runs steps until a task is complete.
- 🧰 **Tool** [opencode-scheduler](https://github.com/different-ai/opencode-scheduler) - OpenCode plugin that runs recurring agent jobs through OS-native schedulers (launchd on macOS, systemd on Linux), with workdir-scoped jobs, timeouts, and skipped ticks when the previous run is still active.
- 🧰 **Tool** [Agent-Loop-Skills](https://github.com/gaasher/Agent-Loop-Skills) - Reusable verification-gated loops (autoresearch, scientific writing, data analysis, code and prompt optimization, red-teaming) packaged as open-standard Agent Skills, each with a feedback signal, run ledger, and termination conditions.
- 🧰 **Tool** [launch-your-agent](https://github.com/anthropics/launch-your-agent) - Anthropic's official Claude Code skill set that operationalizes an interview, launch, grade-against-definition-of-done, iterate, and schedule loop for Claude Managed Agents, leaving a live recurring scheduled agent plus an eval scaffold and roadmap.

## Official Runtime Guides

End-to-end operating guides and release notes from the runtime vendors themselves: how each platform expects you to run recurring agent work.

<!-- OpenAI and Codex -->
- 📚 **Docs** [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) - OpenAI's runbook for plan-edit-test-observe-repair-document-repeat work, including specs, plans, status logs, and validation gates.
- 📚 **Docs** [Best practices - Codex](https://developers.openai.com/codex/learn/best-practices) - Official best practices for context, `AGENTS.md`, MCP, skills, subagents, and automations.
- 📚 **Docs** [Agents SDK](https://developers.openai.com/api/docs/guides/agents) - OpenAI guide for agent orchestration, tool execution, approvals, state, guardrails, and observability.
- 📚 **Docs** [Agents - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/agents/) - SDK primitives for agents, tools, handoffs, guardrails, and runner-managed loops.
- 📚 **Docs** [Running agents](https://developers.openai.com/api/docs/guides/agents/running-agents) - OpenAI guide to turns, state, approvals, sessions, and continuation in the SDK runtime loop.
- 📚 **Docs** [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability) - OpenAI guide to MCP wiring and traces as the basis for debugging and evaluation loops.
- 📚 **Docs** [Sandbox Agents](https://developers.openai.com/api/docs/guides/agents/sandboxes) - Splits the harness control plane from the sandbox execution plane for long-running file and command work.
- 📚 **Docs** [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) - Approval and validation boundaries for sensitive agent actions.
- 📝 **Blog** [ChatGPT Work and the Codex Desktop App](https://openai.com/index/chatgpt-for-your-most-ambitious-work/) - OpenAI's July 9, 2026 launch of ChatGPT Work, a GPT-5.6-powered agent that stays with a project for hours by breaking a goal into smaller steps and completing them independently across apps and files, alongside Codex merging into the ChatGPT desktop app with in-sidebar PR review and cross-repository projects, extending the long-horizon coding-agent loop pattern to general knowledge work.

<!-- Anthropic and Claude Code -->
- 📚 **Docs** [Building agents with the Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview.md) - Claude SDK overview for tool-using agents, subagents, state, permissions, and streaming.
- 📚 **Docs** [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) - Official walkthrough of the inner agent loop that outer recurring loops build on.
- 📚 **Docs** [Extend Claude with skills](https://code.claude.com/docs/en/skills) - Claude Code skill system for reusable loop instructions and assets.
- 📚 **Docs** [Create custom subagents](https://code.claude.com/docs/en/sub-agents) - Claude Code custom subagents with isolated context, model choice, and tool permissions.
- 📚 **Docs** [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) - Anthropic's guidance on evaluating and improving tool specs using agentic loops and realistic tasks.
- 📚 **Docs** [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use?e45d281a_page=3) - Tool search, programmatic tool calling, and tool-use examples for scaling large tool libraries without flooding context.
- 📚 **Docs** [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - Anthropic's guidance for agents that work across many context windows: durable progress artifacts, environment setup, and self-verification.
- 📚 **Docs** [Claude Code best practices](https://code.claude.com/docs/en/best-practices) - Widely cited workflow guidance that underlies many recurring Claude Code loops.
- 📚 **Docs** [Claude Managed Agents: Scheduled Deployments and Vaults](https://claude.com/blog/whats-new-in-claude-managed-agents) - Scheduled deployments for Claude Managed Agents, where each cron firing starts a fresh session to complete the task, plus environment-variable vaults that let sandboxed agents authenticate tools while the real secret attaches only at the network boundary.
- 📝 **Blog** [Getting Started with Loops](https://claude.com/blog/getting-started-with-loops) - Official Claude Code team guide by Delba de Oliveira and Michael Segner (June 30, 2026) that defines loops as agents repeating cycles of work until a stop condition is met, categorizes turn-based, goal-based (/goal), time-based (/loop, /schedule), and proactive loops by trigger and stop criteria, and recommends encoding verification as skills with quantitative success criteria alongside token-spend management.
- 📚 **Docs** [Claude Code What's New, Week 28](https://code.claude.com/docs/en/whats-new/2026-w28) - Weekly digest whose loop-integrity features include auto mode blocking tampering with session transcript files and confirmation prompts before destructive operations in unattended runs.

<!-- GitHub and Copilot -->
- 📚 **Docs** [GitHub Agentic Workflows](https://github.github.com/gh-aw/) - Repository automation that runs coding agents in GitHub Actions on events or schedules with guardrails.
- 📚 **Docs** [Continuous AI](https://githubnext.com/projects/continuous-ai/) - GitHub Next's umbrella framing for CI/CD-style AI automation across the software lifecycle, the category that agentic workflows demonstrate.
- 📝 **Blog** [Automate repository tasks with GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/) - Official walkthrough of writing Markdown-defined agentic workflows with guardrails for triage, QA, and docs chores, announced in the [technical preview changelog](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/).
- 📝 **Blog** [Continuous AI in practice: What developers can automate today with agentic CI](https://github.blog/ai-and-ml/generative-ai/continuous-ai-in-practice-what-developers-can-automate-today-with-agentic-ci/) - Concrete agentic-CI automations available today, with recurring patterns for triage, review, and documentation upkeep.
- 📚 **Docs** [About GitHub Copilot coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent) - GitHub's autonomous coding agent: assign an issue, the agent works in an isolated Actions-powered workspace, and a reviewable pull request comes back.
- 📝 **Blog** [GitHub Copilot: Meet the new coding agent](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/) - Launch overview of the issue-to-PR delegation loop, including iteration on review feedback.
- 📚 **Docs** [GitHub Copilot for Jira Is Now Generally Available](https://github.blog/changelog/2026-06-25-github-copilot-for-jira-is-now-generally-available/) - General availability of Copilot for Jira: delegate a Jira issue to the Copilot coding agent, monitor session progress inside the issue, and send follow-up instructions that continue the same draft pull request instead of starting a new one.
- 📚 **Docs** [Copilot Agent Session Streaming (Public Preview)](https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview/) - Public preview that streams Copilot agent session activity, including prompts, responses, and tool calls, from cloud agents, the CLI, and IDEs to SIEM-compatible endpoints and a REST API, giving enterprises an audit trail for delegated agent work.
- 📚 **Docs** [Security Reviews in the GitHub Copilot App](https://github.blog/changelog/2026-07-14-security-reviews-now-available-in-the-github-copilot-app) - Changelog adding on-demand security reviews inside the Copilot app, so an agent's proposed changes can be scanned for vulnerabilities before they are merged.

<!-- Cursor -->
- 📚 **Docs** [Cursor cloud agents](https://cursor.com/docs/cloud-agent) - Remote agents that work asynchronously in isolated environments and hand results back for review.
- 📚 **Docs** [Cursor 3.8: Improvements to Cursor Automations](https://cursor.com/changelog/06-18-26) - Cursor 3.8 changelog introducing an /automate skill that configures an automation's triggers, instructions, and tools from a plain-language description, plus Slack emoji-reaction and five new GitHub event triggers for dispatching cloud agents.
- 📝 **Blog** [Expanding Our Long-Running Agents Research Preview](https://cursor.com/blog/long-running-agents) - Cursor's research preview of days-long autonomous agents gated by an upfront human-approved plan and cross-checked by multiple agents, reporting merge rates comparable to standard agents on runs as large as 52 hours and 151k lines.
- 📚 **Docs** [Cursor 3.11: Side Chats, Transcript Search, and Cloud Agent Hooks](https://cursor.com/changelog/side-chat) - Cursor changelog adding cloud-agent hooks (before-submit, after-response, after-thought, stop, and subagent-start) that the platform pitches for gating and observing background agent runs.

<!-- Other runtimes -->
- 📚 **Docs** [Jules](https://jules.google/docs) - Google's asynchronous coding agent that plans, executes tasks in isolated cloud VMs, and returns reviewable diffs.
- 📚 **Docs** [Devin Docs](https://docs.devin.ai/get-started/devin-intro) - Documentation for a long-running autonomous software engineer with sessions, playbooks, knowledge, and review boundaries.
- 📝 **Blog** [Amp: Agents, Anywhere](https://ampcode.com/news/agents-anywhere) - Amp launches remote agent creation on any machine with shell access plus a headless runner mode that lets multiple agents run concurrently without a terminal UI.

## Research Foundations

Loop Engineering is new as a practice name, but it builds on years of agent-loop, feedback, planning, and self-correction research.

- 📄 **Paper** [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) - Foundational reason-act-observe loop for tool-using language agents.
- 📄 **Paper** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) - Converts environment feedback into written reflections stored in memory for future attempts.
- 📄 **Paper** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) - Generate-feedback-refine loop where a model improves outputs over repeated passes.
- 📄 **Paper** [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing](https://arxiv.org/abs/2305.11738) - Uses tools to ground critique and correction rather than relying only on introspection.
- 📄 **Paper** [Tree of Thoughts](https://arxiv.org/abs/2305.10601) - Search over multiple reasoning branches; relevant when loop design needs exploration before committing.
- 📄 **Paper** [Graph of Thoughts](https://arxiv.org/abs/2308.09687) - Generalizes thought structures beyond chains and trees, useful for complex loop planning and aggregation.
- 📄 **Paper** [Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models](https://arxiv.org/abs/2310.04406) - Combines search, action, and environment feedback for language agents.
- 📄 **Paper** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) - Demonstrates lifelong skill acquisition through iterative exploration, feedback, and a skill library.
- 📄 **Paper** [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) - Introduces reflection and memory mechanisms for long-running agent behavior.
- 📄 **Paper** [Measuring AI Ability to Complete Long Software Tasks](https://arxiv.org/abs/2503.14499) - METR's task-length time horizon metric; grounds why loop budgets, checkpoints, and escalation matter as autonomous work gets longer.
- 📝 **Blog** [Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) - Accessible summary of the 50% task-completion time horizon and its doubling trend.
- 📄 **Paper** [Reflection-Driven Control for Trustworthy Code Agents](https://arxiv.org/abs/2512.21354) - Elevates reflection from an external pass to an internal control loop that monitors the agent's decision path during generation and constrains risky steps with low overhead.
- 📄 **Paper** [Hyperagents](https://arxiv.org/abs/2603.19461) - Self-referential agents that fold task-solving and self-modification into editable programs, extending the Darwin Godel Machine toward open-ended self-improvement, the loop where an agent rewrites its own improvement mechanism across runs.
- 📄 **Paper** [PARC: An Autonomous Self-Reflective Coding Agent for Robust Execution of Long-Horizon Tasks](https://arxiv.org/abs/2512.03549) - Hierarchical plan-execute-assess loops that detect and correct strategic errors during multi-hour autonomous runs.
- 📄 **Paper** [When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents](https://arxiv.org/abs/2603.17104) - Measures how agents drift from intent when specifications arrive incrementally across a long loop, and proposes a mitigation that recovers most of the loss.
- 🧰 **Tool** [Reflexion code](https://github.com/noahshinn/reflexion) - Reference implementation and experiments for verbal reinforcement loops.
- 📄 **Paper** [Stop Hand-Holding Your Coding Agent: Engineering the Loops that Replace Step-by-Step Prompting](https://arxiv.org/abs/2607.00038) - Position paper that formalizes the loop specification (trigger, goal, verification step, stopping rule, memory) as a reusable artifact handed to an agent harness, with a taxonomy, a five-level verification ladder, and a hand-coded analysis of fifty real-world loops.
- 📄 **Paper** [From Question Answering to Task Completion: A Survey on Agent System and Harness Design](https://arxiv.org/abs/2606.20683) - Survey that decomposes the agent execution harness into six runtime responsibilities (observation, context, control, action, state, verification) and argues task performance emerges from the interaction of model, runtime, task structure, and evaluation rather than the model alone.
- 📄 **Paper** [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](https://arxiv.org/abs/2605.22794) - Self-evolution loop where the agent rewrites its own source code, with each change anchored to a production failure and accepted only after deterministic replay verification with rollback, lifting a four-task mean grader score from 0.25 to 0.61 without human intervention.
- 📝 **Blog** [METR Time Horizon 1.1](https://metr.org/blog/2026-1-29-time-horizon-1-1/) - Update to METR's time-horizon methodology, expanding the task suite to 228 tasks (31 at 8+ hours), migrating to the open-source Inspect framework, and revising the post-2023 capability doubling time to roughly 131 days.
- 📄 **Paper** [MetaSkill-Evolve: Recursive Self-Improvement via Two-Timescale Meta-Skill Evolution](https://arxiv.org/abs/2607.05297) - Two-timescale recursive self-improvement where a fast loop rewrites task skills from execution traces while a slow loop evolves the meta-skill governing improvement itself, gaining up to 23.5 points on OfficeQA, SealQA, and ALFWorld.
- 📄 **Paper** [SkillOpt-Lite: Better and Faster Agent Self-Evolution via One Line of Vibe](https://arxiv.org/abs/2607.03451) - Formalizes agent skill self-evolution as zeroth-order optimization and distills it into a minimal pipeline of file-system trajectory exploration, consensus attribute mining, and independent validation gating, letting a smaller model surpass larger ones on LiveMath and SpreadsheetBench.
- 📄 **Paper** [Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops](https://arxiv.org/abs/2607.07663) - Survey of 1,250 arXiv papers from 2024-2026 organized along two axes, what a self-improvement loop improves and its degree of loop closure, separating bounded evaluable self-refinement from open-ended recursive self-improvement.
- 📄 **Paper** [From Atomic Actions to Standard Operating Procedures: Iterative Tool Optimization for Self-Evolving LLM Agents](https://arxiv.org/abs/2607.07321) - EvoSOP has agents distill recurring execution trajectories into reusable standard operating procedures and iteratively optimize the toolset through a construction, merging, evaluation, and pruning lifecycle.
- 📄 **Paper** [TTHE: Test-Time Harness Evolution](https://arxiv.org/abs/2607.08124) - Adapts LLM agents at test time by evolving a population of candidate harnesses (the executable control program around the model) from execution traces, using a label-free agentic proposer and judge to sustain improvements on text-to-SQL and competitive programming while flagging execution-derived proxy reliability as the key open challenge.
- 📄 **Paper** [DeepSearch-World: Self-Distillation for Deep Search Agents in a Verifiable Environment](https://arxiv.org/abs/2607.07820) - Introduces DeepSearch-Evolve, where a deep search agent improves by self-distilling its own trajectories inside a deterministic 420K-task verifiable environment, progress verification, grounded reflection, and failure recovery replace teacher trajectories and sparse RL reward, lifting a 9B model to 31.2% BrowseComp and 61.5% GAIA.
- 📄 **Paper** [What Makes a Good Bug Report for an AI Agent?](https://arxiv.org/abs/2607.07593) - Statistical analysis of 433 issues plus controlled multi-model experiments showing LLM repair agents succeed more when bug reports carry reproduction scripts, fix suggestions, and fault-localization cues, while longer natural-language reports correlate with lower success, directly informing how a loop's work-discovery step should specify tasks before dispatching agents.
- 📄 **Paper** [AutoPersonas: A Multi-Timescale Loop Engine for Open-Ended Persona Evolution](https://arxiv.org/abs/2607.08252) - Names self-locking as a runtime failure mode of continuing agent loops, where accumulated state and history pull generation toward stale repetition (over 95% rolling action-repetition across an eight-model 40-day stress test), and proposes a multi-timescale loop that admits divergent material only through evidence-governed absorption, cutting macro-theme repetition from 61.8% to 36.3%.
- 📄 **Paper** [Agentic Data Environments](https://arxiv.org/abs/2607.07397) - Vision paper from the IEEE Data Engineering Bulletin reframing data systems as the active execution environment agents operate in, spanning files, APIs, applications, and system state, arguing the substrate under recurring agent loops should both amplify agent capability and enforce safety guarantees that bound the cost of failure.
- 📄 **Paper** [Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation](https://arxiv.org/abs/2607.08938) - Meta agent maps observed failure modes to harness adaptation strategies, letting small-model agents recover ~90% of frontier-LLM performance at ~4% of the cost, the harness itself becomes the optimization target.
- 📄 **Paper** [Inside the Skill Market: From Software Engineering Activities to Reusable Agent Skills](https://arxiv.org/abs/2607.09065) - First large-scale empirical study of public agent-skill repositories and marketplaces, characterizing which software-engineering activities get packaged as reusable skills, their coverage across the development lifecycle, how they evolve, and how they are evaluated - an activity-centric map of the skills layer that agent loops compose (Cao, Cheung, et al., HKUST).
- 📝 **Blog** [Harness Engineering for Self-Improvement](https://lilianweng.github.io/posts/2026-07-04-harness/) - Lilian Weng's deep-dive arguing the harness, the system surrounding a base model that orchestrates execution, matters as much as raw intelligence for recursive self-improvement, with a taxonomy of harness components and failure modes.
- 📄 **Paper** [Compile, Then Page: Executable SOP Programs and a Capability-Gated Runtime](https://arxiv.org/abs/2607.11346) - Compiles safety-critical standard operating procedures into executable pseudo-code run by a program-guided stack machine that pages the active frame while the LLM does semantic execution, finding runtime guidance is capability-gated (it helps strong models and harms weak ones) across a six-model, seven-domain SOPBench study.
- 📄 **Paper** [Mako: A Self-Evolving Agentic Operating System for Autonomous Web Exploitation](https://arxiv.org/abs/2607.11288) - Industrial self-evolving agentic OS that treats exploit capability as a mutable, versioned kernel: the agent observes its own failures, synthesizes new capabilities, proves them against a live target, and hot-loads them back, a self-improvement loop with in-loop verification.
- 📄 **Paper** [How Do Practitioners Build SE Agents? Insights from a Mixed-Methods Study](https://arxiv.org/abs/2607.10856) - Mixed-methods study of how practitioners actually design software-engineering agents, surfacing the recurring loop, harness, and verification decisions teams make and where their mental models diverge from benchmark assumptions.
- 📄 **Paper** [Dynamic Agent Skills: A Lifecycle Survey and Taxonomy of Evolving Skill Libraries](https://arxiv.org/abs/2607.10113) - Survey and taxonomy of how agent skill libraries are created, evaluated, retired, and reused over time, organizing the fast-growing self-evolving-skills literature into a lifecycle framework.

## Agent Workflow Patterns

These resources are included when they help design the higher-level loop around agents, not merely because they describe agents in general.

- 📚 **Docs** [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's canonical guide to workflows and agents, including evaluator-optimizer and orchestrator-workers patterns.
- 📄 **Paper** [Harness Engineering for Language Agents: The Harness Layer as Control, Agency, and Runtime](https://www.preprints.org/manuscript/202603.1756) - Decomposes the harness layer that loops build on into control, agency, and runtime, audits 63 harness works, and proposes a HarnessCard so reported agent gains can be separated from harness effects.
- 📝 **Blog** [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) - Detailed orchestrator-worker system with planning, memory, subagents, citation passes, and iterative research loops.
- 📄 **Paper** [Building Effective AI Agents: Architecture Patterns and Implementation Frameworks](https://resources.anthropic.com/hubfs/Building%20Effective%20AI%20Agents-%20Architecture%20Patterns%20and%20Implementation%20Frameworks.pdf) - PDF overview of agent architecture patterns, including generator-evaluator loops.
- 📝 **Blog** [AI Agent Architectures](https://hld.handbook.academy/curriculum/ai-ml-system-design/ai-agent-architectures/) - System-design overview of ReAct, reflection, planning, tool use, memory, and control strategies.
- 📝 **Blog** [What Are Agentic Workflows?](https://weaviate.io/blog/what-are-agentic-workflows) - Accessible taxonomy of planning, tool use, reflection, and memory patterns.
- 📝 **Blog** [Agent Planning & Reflection Patterns](https://learnaivisually.com/tracks/ai-agents/planning-reflection) - Visual explanation of plan-execute, observe, reflect, retry, and stop patterns.
- 📝 **Blog** [Agentic Design Patterns](https://addyosmani.com/agents/04-agentic-design-patterns/) - Practical overview of ReAct, reflection, tool use, planning, and how to combine them in real-world agents.
- 🔁 **Pattern** [12 Factor Agents](https://github.com/humanlayer/12-factor-agents) - Operating principles for production agents, including explicit prompts, state ownership, and pause-resume behavior.
- 🔁 **Pattern** [Durable Execution for Agentic Workflows](https://arizenai.com/durable-execution/) - Explains checkpointing, event-sourced journals, replay, and recovery for long-running agent workflows.
- 📄 **Paper** [Code as Agent Harness](https://arxiv.org/abs/2605.18747) - Organizes agent infrastructure into harness interface, feedback-driven control, and multi-agent scaling for executable, verifiable, stateful systems; maps the harness layer that loops build on.
- 📄 **Paper** [Agentic Agile-V: From Vibe Coding to Verified Engineering](https://arxiv.org/abs/2605.20456) - Proposes a task-level SCOPE-V loop (Specify, Constrain, Orchestrate, Prove, Evolve, Verify) with human approval gates, arguing agentic coding needs process control and independent verification, not better prompts.
- 📄 **Paper** [Agentic Software Engineering: Foundational Pillars and a Research Roadmap](https://arxiv.org/abs/2509.06216) - Splits agentic SE into an Agent Command Environment for human orchestration and an Agent Execution Environment for agent task execution, a research roadmap for the layers recurring loops run inside.
- 📝 **Blog** [The Art of Loop Engineering](https://www.langchain.com/blog/the-art-of-loop-engineering) - LangChain's account of four stacked loops around agents (core execution, rubric-based verification, event-driven triggers, and trace-driven self-improvement) using a documentation-writing agent as the running example.
- 🧰 **Tool** [Loopy](https://github.com/Forward-Future/loopy) - Library of reusable AI-agent loops with verification checks and stopping conditions, plus an installable skill for finding, adapting, and designing repeatable agent workflows.
- 📝 **Blog** [The Factory Model: How Coding Agents Changed Software Engineering](https://addyosmani.com/blog/factory-model/) - Addy Osmani's February 2026 essay recasting engineers as operators of parallel agent workstreams, with agents running "thirty minutes, an hour, several hours and increasingly days" and verification, not generation, as the new bottleneck; the fleet-level framing that precedes his June Loop Engineering essay.
- 📚 **Docs** [2026 Agentic Coding Trends Report](https://resources.anthropic.com/2026-agentic-coding-trends-report) - Anthropic's official 2026 trends report on the shift from single coding assistants to coordinated agent teams running autonomously for hours or days, with case studies from Rakuten, TELUS, and Zapier (landing page is registration-gated; the direct PDF is public).
- 🧰 **Tool** [HomeRail](https://github.com/xiaotianfotos/homerail) - TypeScript runtime that turns one-off agent chats into auditable, reusable DAG workflows on self-hosted hardware, with a DAG engine, CLI, and voice front end.
- 📝 **Blog** [Old and New Apps, via Modern Coding Agents](https://terrytao.wordpress.com/2026/07/11/old-and-new-apps-via-modern-coding-agents/) - Terence Tao's July 11, 2026 account of porting roughly two dozen Java 1.0 applets to JavaScript and resurrecting long-abandoned projects through iterative agent sessions, concluding that domain expertise remains the human verification layer: high-level design decisions stay with the author while implementation is automated away, and the exchange was "a net wash" on code quality, he caught one minor bug in the agent's output while the agent found two bugs in his original code. Named-practitioner post; loop content is iterative-refinement rather than unattended loops, so it fits the practitioner-workflow section rather than core loop patterns.

## Coding-Agent Loop Systems

End-to-end systems and field reports of coding agents running in loops, from single-repo Ralph runners to production agent fleets.

<!-- Research agent frameworks -->
- 🧰 **Tool** [SWE-agent](https://github.com/SWE-agent/SWE-agent) - Agent-computer interface and autonomous software engineering agent for repository tasks.
- 📄 **Paper** [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) - Paper behind SWE-agent and its interface design.
- 🧰 **Tool** [mini-SWE-agent](https://mini-swe-agent.com/latest/) - Minimal coding agent that is useful for understanding the core loop without a large framework.
- 🧰 **Tool** [OpenHands](https://github.com/All-Hands-AI/OpenHands) - Open platform for AI software developers as generalist agents.
- 📄 **Paper** [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741) - Paper describing OpenHands, CodeActAgent, benchmarks, and generalist agent evaluation.
- 🧰 **Tool** [Agentless](https://github.com/OpenAutoCoder/Agentless) - Workflow-based approach for software issue resolution using localization, repair, and patch validation.
- 📄 **Paper** [Agentless: Demystifying LLM-based Software Engineering Agents](https://arxiv.org/abs/2407.01489) - Useful contrast case: strong results through structured workflow rather than a fully open-ended agent.
- 🧰 **Tool** [AutoCodeRover](https://github.com/AutoCodeRoverSG/auto-code-rover) - Autonomous program improvement system for issue localization, patch generation, and validation.
- 📄 **Paper** [AutoCodeRover: Autonomous Program Improvement](https://arxiv.org/abs/2404.05427) - Paper on autonomous code repair loops over real repositories.
- 🧭 **List** [SWE-bench reading list](https://github.com/SWE-bench/reading-list) - Maintained map of software engineering agent systems and related papers.
- 📄 **Paper** [TraceCoder: A Trace-Driven Multi-Agent Framework for Automated Debugging of LLM-Generated Code](https://arxiv.org/abs/2602.06875) - ICSE'26 observe-analyze-repair loop with instrumentation, analysis, and repair agents, a history-learning mechanism, and a rollback to the last good state; iteration alone drives most of the gain.
- 📄 **Paper** [The Kitchen Loop: User-Spec-Driven Development for a Self-Evolving Codebase](https://arxiv.org/abs/2603.25697) - Production loop where an agent exercises a spec surface as a synthetic power user behind ground-truth tests and quality gates, reporting 285+ self-correcting iterations and 1,000+ merged PRs with zero detected regressions.
- 📄 **Paper** [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](https://arxiv.org/abs/2604.03515) - Dissects 13 open-source coding-agent scaffolds and identifies five composable loop primitives (ReAct, generate-test-repair, plan-execute, retry, tree search) that real agents layer, mapping how control loop, tools, and state combine.
- 📄 **Paper** [A Self-Improving Coding Agent](https://arxiv.org/abs/2504.15228) - An agent that edits its own code and tools and re-runs against a benchmark, lifting itself from 17% to 53% on a SWE-bench Verified subset, a concrete self-modifying improvement loop.
- 📄 **Paper** [Don't Blame the Large Language Model: How Scaffolding Evolution Shapes Coding Agent Quality](https://arxiv.org/abs/2607.03691) - Longitudinal study of 35 Qwen Code CLI releases with the model held constant, tracing coding-agent shifts to specific scaffolding changes in system prompts, tools, context management, and reasoning loops, and separating scaffolding regressions from model regressions.
- 📄 **Paper** [ToFu: A White-Box, Token-Efficient Agent Harness for Researchers](https://arxiv.org/abs/2607.11423) - MIT-licensed white-box agent harness built on the thesis that agent behavior is set by the orchestration code around the model as much as the model itself, letting researchers inspect, modify, and evaluate its orchestration logic with reported token-efficiency gains over existing harnesses.
- 📄 **Paper** [When Does Restricting a Coding Agent to execute_code Help?](https://arxiv.org/abs/2607.10569) - Regime-by-design ablation measuring when constraining a coding agent to a single execute_code action helps or hurts, separating task regime from agent design so harness choices can be made from evidence rather than intuition.

<!-- The Ralph technique and its runners -->
- 🔁 **Pattern** [Ralph](https://ghuntley.com/ralph/) - Geoffrey Huntley's original Ralph technique: run one agent in a bare loop with fresh context per iteration and the filesystem plus specs as memory.
- 🔁 **Pattern** [everything is a ralph loop](https://ghuntley.com/loop/) - Follow-up essay arguing the loop, not the agent, is the durable engineering unit: one task per iteration, deterministic context, and verification inside the loop.
- 🧰 **Tool** [how-to-ralph-wiggum](https://github.com/ghuntley/how-to-ralph-wiggum) - Reference repository documenting the Ralph Wiggum technique end to end, from the bare loop script to guardrails and conventions.
- 📝 **Blog** [A Brief History of Ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph) - Traces how the bare-loop technique spread from a provocation to a production practice among early adopters.
- 🔁 **Pattern** [Ralph Copilot](https://github.com/giocaizzi/ralph-copilot/tree/e5b2813cc876c73a8c9d3398c0115da0d15f63cf) - Language-agnostic Ralph loop implementation using fresh context, filesystem memory, `PRD.md`, and `PROGRESS.md`.
- 🧰 **Tool** [Ralph (snarktank)](https://github.com/snarktank/ralph) - Ryan Carson's PRD-driven Ralph implementation that re-runs Amp or Claude Code with a fresh instance per iteration, gates each story on typecheck and tests, and persists state in prd.json, progress.txt, and Git history until every story passes.
- 🧰 **Tool** [ralph-claude-code](https://github.com/frankbria/ralph-claude-code) - Loop runner that repeatedly re-executes Claude Code against project requirements, using dual-condition exit detection, rate limiting, and a circuit breaker to decide when the loop should stop.
- 🧰 **Tool** [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) - Multi-backend implementation of the Ralph Wiggum technique that keeps a coding agent looping until task completion, using role-scoped hat personas that coordinate through events, with human-in-the-loop controls and a monitoring dashboard.
- 🧰 **Tool** [ralphex](https://github.com/umputun/ralphex) - Extended Ralph loop runner that creates a Git branch per plan, executes tasks in fresh sessions with a commit after each, runs a multi-phase review pipeline with parallel review agents, and archives the completed plan.
- 🧰 **Tool** [ralph (iannuttall)](https://github.com/iannuttall/ralph) - File-based Ralph-style agent loop that executes one JSON PRD story per iteration with fresh model context, using Git and on-disk state as memory across Claude, Codex, Droid, and OpenCode backends.
- 🧰 **Tool** [ralph-loop-agent](https://github.com/vercel-labs/ralph-loop-agent) - Vercel Labs implementation of the Ralph loop for the AI SDK: an outer loop re-runs the agent with verifier feedback until a verifyCompletion check passes or iteration, token, or cost stop conditions trigger.
- 🧰 **Tool** [Open Ralph Wiggum](https://github.com/Th0rgal/open-ralph-wiggum) - Agent-agnostic CLI that runs the Ralph Wiggum loop by feeding the same prompt to a fresh agent instance each iteration, with task tracking, live status monitoring, and mid-loop context injection across six coding-agent backends.

<!-- Loop runners and delivery harnesses -->
- 🔁 **Pattern** [Compound Engineering](https://every.to/guides/compound-engineering) - Every's named plan-work-review-compound loop, where each run feeds lessons back into `AGENTS.md`-style memory so the next loop is easier; the self-improving counterpart to Ralph.
- 🧰 **Tool** [Gas Town](https://github.com/steveyegge/gastown) - Steve Yegge's multi-agent orchestrator that runs 20-30 parallel coding agents with coordinator, worker, and merge-queue roles; the structured-orchestration end of the spectrum that Ralph anchors with bare iteration.
- 🧰 **Tool** [Amp](https://ampcode.com/) - Agentic coding tool built around threads, subagents, and an opinionated harness, with an owner's manual that documents loop-style operating practices.
- 🧰 **Tool** [karl](https://github.com/kayoslab/karl) - Autonomous multi-agent development loop with planner, reviewer, architect, tester, developer, deployment, and retry phases.
- 🔁 **Pattern** [joelclaw agent-loop skill](https://github.com/joelhooks/joelclaw/blob/main/skills/agent-loop/SKILL.md) - Durable Planner-Implementor-Reviewer-Judge coding loops via Inngest events and progress files.
- 🧰 **Tool** [ARIS (Auto-Research-In-Sleep)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) - Markdown-only skills that run autonomous overnight ML research loops on Claude Code, Codex, or other LLM agents, iterating idea discovery and experiments with cross-model review as the verification gate.
- 🧰 **Tool** [AutoAgent](https://github.com/kevinrgu/autoagent) - Meta-agent that autonomously edits its own harness (system prompt, tools, orchestration), re-runs the benchmark, and keeps or discards each change by score, with an author-reported top SpreadsheetBench result from a 24-hour unattended run.
- 🧰 **Tool** [zeroshot](https://github.com/the-open-engine/zeroshot) - CLI that runs a planner, an implementer, and independent validators in isolated environments, looping until a change is verified or rejected with reproducible failures.
- 🧰 **Tool** [Loki Mode](https://github.com/asklokesh/loki-mode) - Autonomous spec-to-app loop that runs Reason-Act-Reflect-Verify cycles behind quality gates, with completion gated by a blind three-reviewer council and a deterministic evidence receipt that rejects empty diffs and failing tests.
- 🧰 **Tool** [Looper](https://github.com/ksimback/looper) - Claude Code skill for designing review-gated agent loops before running them, coaching the user into a portable loop.yaml spec with explicit goals, typed verification, iteration caps, and budget limits, then emitting artifacts runnable in-session or via an external Python runner.
- 🧰 **Tool** [Agent Apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship) - Multi-backend ecosystem where apprentice agents complete tasks through workflow loops, mentors or humans verify results, and execution traces are compiled into a published dataset that feeds future agent improvement.
- 🧰 **Tool** [Scholar Loop](https://github.com/renee-jia/scholar-loop) - Autonomous multi-agent research loop from literature to hypothesis to real ML experiments to write-up, scoring every checkable agent claim against frozen ground-truth metrics and shipping an adversarial cheater engine that probes the loop for reward-hacking gaps.
- 🧰 **Tool** [loop-engineering (Cobus Greyling)](https://github.com/cobusgreyling/loop-engineering) - Patterns-and-tooling repo shipping seven npm CLIs (loop-init, loop-audit, loop-cost, loop-sync, loop-context, loop-mcp-server, loop-worktree), starter kits, and production loop patterns; scaffolds skills/state/budget files, scores a repo's "Loop Ready" readiness, detects state drift, and estimates token spend per cadence for Claude Code, Codex, OpenCode, and Grok loops.
- 🧰 **Tool** [AutoCVE](https://github.com/larlarua/AutoCVE) - Open-source agent-driven CVE discovery platform whose orchestrator coordinates Recon, Scan, Triage, Finding, and Verification agents through ReAct loops with correction nudges and structured FinalizeFinding termination, running the full discover, source-audit, dynamic-verify, dedup, and report loop on a self-hosted FastAPI/React/PostgreSQL stack with agent-tree observability.
- 🧰 **Tool** [LoongFlow (Baidu)](https://github.com/baidu-baige/LoongFlow) - Baidu's open-source agent framework built explicitly for Loop Engineering: a Plan-Execute-Summary loop with structured experiential memory lets agents plan, execute, reflect, and evolve across software-engineering, math, and ML tasks (Apache-2.0, on PyPI, paper: arXiv 2512.24077).
- 🧰 **Tool** [cc10x](https://github.com/romiluz13/cc10x) - Claude Code plugin that routes work through one router, nine specialist agents, sixteen skills, and four workflows, enforcing fail-closed verification and test-honesty gates and writing each workflow's intent, evidence, and verdicts to durable .cc10x/ disk artifacts so resume and review survive context compaction.
- 🧰 **Tool** [RigorLoop](https://github.com/ronikobrosly/RigorLoop) - Statistically-grounded loop-engineering framework in which a strategy agent directs concurrent executor agents that iteratively build and refine a solution against gold-standard examples.
- 🧰 **Tool** [Open-Inspect](https://github.com/ColeMurray/background-agents) - Open-source background coding-agent system inspired by Ramp's Inspect: hosted agents in full dev-environment sandboxes, reachable from a web UI, Slack, GitHub PRs, Linear, or webhooks.
- 🧰 **Tool** [T3MP3ST](https://github.com/elder-plinius/T3MP3ST) - Multi-agent offensive-security meta-harness that turns an existing coding agent into an autonomous vulnerability-research loop, with a verify-claims receipt step that separates confirmed findings from speculation.
- 🧰 **Tool** [Loom](https://github.com/valkor-ai/loom) - Open-source delivery harness for existing coding agents that treats delivery as a durable loop: route, execute, verify, record evidence, repair, and continue from saved state.
- 🧰 **Tool** [Inferoa](https://github.com/agentic-in/inferoa) - Inference-native agent harness for loop engineering that treats every loop as an inference workload, shaping each turn to preserve cacheable prefixes and bound stale evidence.
- 🧰 **Tool** [PlanWeave](https://github.com/GaosCode/PlanWeave) - File-backed loop-engineering system for long-running coding agents that turns fuzzy plans into a claimable task graph of nodes and block documents routed through implementation and review.
- 🧰 **Tool** [loop.js](https://github.com/loop-js/loop.js) - TypeScript loop-engineering framework that runs an agent in rounds against a stated goal until a skeptical, read-only verifier agent accepts the result or a budget is exhausted.
- 🧰 **Tool** [ai-trains-ai](https://github.com/Danau5tin/ai-trains-ai) - Recursive training loop where a trainer agent autonomously writes complete reinforcement-learning jobs (environments, rewards, configs), runs them, and iterates on the results.

<!-- Production systems and field reports -->
- 📝 **Blog** [Factory 2.0: From Coding Agents to Software Factories](https://factory.ai/news/software-factory) - Factory's software-factory pattern, where Automations coordinate recurring workflows with shared objectives and memory, Missions run multi-agent execution over hours or days, and Droid Computers give agents persistent remote execution across the SDLC.
- 📝 **Blog** [Superpowers 6](https://blog.fsck.com/2026/06/15/Superpowers-6/) - Release notes doubling as a case study of an unattended overnight autoresearch loop that ran 25 harness experiments against the project's own eval suite, roughly halving orchestration runtime and cutting token spend about 60%.
- 📝 **Blog** [Introducing Devin Security Swarm](https://cognition.com/blog/introducing-devin-security-swarm) - Cognition's agent swarm runs a continuous discover-verify-fix security loop: parallel agents hunt vulnerabilities, reproduce each in an isolated sandbox to confirm exploitability before reporting, and open remediation PRs, re-running on a schedule after the backlog clears.
- 📝 **Blog** [Towards Self-Driving Codebases](https://cursor.com/blog/self-driving-codebases) - Cursor research on running thousands of coding agents as a recursive planner-subplanner-worker hierarchy sustaining roughly 1,000 commits per hour, finding that tolerating small error rates that peer agents later fix beats enforcing per-step correctness.
- 📝 **Blog** [Factory: Incident Response Automation](https://factory.ai/news/incident-response) - Factory's July 10, 2026 launch where a Droid triggered by Slack alerts (Sentry, Datadog, Rootly, Axiom) autonomously investigates each incident on a dedicated computer, triages, prepares fixes, and reports back in the thread, recording what it learns in a persistent runbook that Factory says improves its incident response over time.
- 📝 **Blog** [A Week-Long Autonomous Voxel Manhattan Build](https://x.com/mattshumer_/status/2075268746315268138) - Matt Shumer's demonstration of a single-prompt run in which a frontier model worked autonomously for almost a week with subagent fan-out to build a navigable voxel Manhattan.

## Verification And Feedback Gates

These resources include harness and observability mechanisms that loops compose into exit gates, receipts, and retry signals.

<!-- Practice: verification-first workflows -->
- 📝 **Blog** [Why Agentic Systems Must Produce Deterministic Outputs to Scale](https://streamzero.com/blog/posts/deep-dives-tools-technologies-architectures/agentic-patterns/why-agentic-systems-must-produce-deterministic-outputs-to-scale) - Argues for deterministic boundaries, contracts, and execution gates around probabilistic agent reasoning.
- 🔁 **Pattern** [Stop Babysitting Your Coding Agent. Give It Backpressure.](https://generativeprogrammer.com/p/stop-babysitting-your-coding-agent) - Explains how to turn tests, linters, builds, traces, and other signals into feedback loops for coding agents.
- 🔁 **Pattern** [How to Build a Self-Verification Loop in Claude Code](https://dev.to/shipwithaiio/how-to-build-a-self-verification-loop-in-claude-code-3-layers-20-minutes-m1p) - Uses hooks to enforce syntax, intent, and regression checks before an agent can finish.
- 📝 **Blog** [Agentic Code Review](https://addyosmani.com/blog/agentic-code-review/) - Addy Osmani argues that review, not code generation, is the bottleneck in agentic workflows, proposing risk-tiered verification depth, heterogeneous AI reviewers, and hard CI gates while warning against closed loops of models with correlated blind spots.
- 📝 **Blog** [Using DSPy to Evaluate and Improve Datasette Agent's SQL System Prompts](https://simonwillison.net/2026/Jul/2/dspy-datasette-agent-prompts/) - Simon Willison wires a DSPy evaluation harness to a live Datasette instance with real tool calls and gold-standard metrics, then uses the eval traces to find and fix weaknesses in the agent's SQL system prompt.
- 📝 **Blog** [Agentic coding notes](https://danluu.com/ai-coding/) - Dan Luu's first-hand benchmarks and workflows arguing that systematic test infrastructure such as fuzzing and randomized testing, not human review, is what lets agent-generated code ship, and documenting why a self-contained agentic quality loop has so far eluded him.
- 📝 **Blog** [Understanding Is the New Bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html) - Geoffrey Litt argues that human understanding, not verification, is the real bottleneck in agent loops, warning that cognitive debt accrues when iterations outpace comprehension and proposing literate diffs, quizzes, and interactive micro-worlds as speed regulators.
- 📝 **Blog** [Verifying Agentic Development at Scale](https://cognition.com/blog/testing-development) - Cognition details the verification stack behind Devin sessions going majority-async: source-grounded test plans, deterministic reusable testing skills, and annotated video artifacts with pass/fail assertions so unattended runs return merge-ready results.
- 📝 **Blog** [Loop Engineering Without Verification Is Just Automation](https://www.sonarsource.com/blog/loop-engineering-without-verification-is-just-automation/) - Sonar formalizes a two-tier verification gate for agent loops, pairing a probabilistic LLM verifier sub-agent for intent with a deterministic analysis gate as the hard halt, arguing that LLM-only verification amounts to two optimists agreeing.
- 📝 **Blog** [Closing the Verification Loop: Observability-Driven Harnesses](https://www.datadoghq.com/blog/ai/harness-first-agents/) - Datadog engineers' case for harness-first engineering once agents write code faster than humans can review, using deterministic simulation testing across millions of seeds as the verification gate.

<!-- Harness hill-climbing with traces and evals -->
- 📝 **Blog** [How to build a better agent harness with traces and evals](https://arize.com/blog/improve-ai-agents-traces-evals-harness/) - Trace-evaluate-debug-refine loop for improving agent behavior from real runs.
- 📝 **Blog** [Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals) - LangChain's recipe for using evals as the learning signal for harness improvement.
- 📝 **Blog** [Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) - Practical discussion of self-verification, traces, middleware, and loop detection for coding agents.
- 📄 **Paper** [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](https://arxiv.org/abs/2604.25850) - Closed loop that turns each harness edit into a falsifiable contract verified against trajectory outcomes, so the harness evolves from observability rather than trial and error.
- 📄 **Paper** [Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/abs/2603.28052) - Optimizes the surrounding harness (tools, prompts, control flow) end to end against task outcomes, turning harness tuning into a measurable improvement loop instead of manual trial and error.
- 🧰 **Tool** [HALO (Hierarchical Agent Loop Optimizer)](https://github.com/context-labs/halo) - Analyzes production agent traces to find harness-level failure modes, hands its report to a coding agent to apply fixes, and repeats the collect-analyze-fix-redeploy cycle, reporting AppWorld gains from harness changes alone.
- 📄 **Paper** [Harness-Aware Self-Evolving: Co-Evolving Model Weights, Harness, and Task Solutions](https://arxiv.org/abs/2607.03935) - Agentic RL framework in which one model both solves tasks and edits its own harness, including repairing faulty evaluation code, co-evolving weights, harness, and solutions so a trained Qwen3-8B matches a much larger baseline.
- 🧰 **Tool** [auto-harness](https://github.com/neosigmaai/auto-harness) - Bring-your-own-agent framework for self-improving agentic systems that mines failures from runs, optimizes the harness in response, and gates every change behind regression checks.

<!-- Observability and eval tooling -->
- 📚 **Docs** [OpenAI agent evals](https://developers.openai.com/api/docs/guides/agent-evals) - Evaluation guidance for moving from traces to repeatable grading of agent workflows.
- 🧰 **Tool** [Promptfoo OpenAI Agents provider](https://www.promptfoo.dev/docs/providers/openai-agents/) - Testing and assertions for multi-turn agent workflows, tools, state, handoffs, sandboxes, and traces.
- 🧰 **Tool** [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) - UK AISI evaluation framework with solvers, scorers, sandboxing, tool use, MCP, and log viewing.
- 📚 **Docs** [OpenTelemetry Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/) - Portable tracing conventions for model calls, tool calls, and agent workflows.
- 🧰 **Tool** [AgentOps](https://github.com/AgentOps-AI/agentops) - Monitoring, replay, cost tracking, benchmarking, and tracing for agent sessions.
- 🧰 **Tool** [Langfuse](https://github.com/langfuse/langfuse) - Open-source LLM engineering platform with tracing, evaluations, and metrics that loops can read back as feedback signals.
- 🧰 **Tool** [LangSmith](https://www.langchain.com/langsmith) - Tracing, evaluation, and monitoring platform for inspecting and grading agent runs across iterations.
- 🧰 **Tool** [Arize Phoenix](https://github.com/Arize-ai/phoenix) - Open-source AI observability for tracing, evaluating, and debugging agent behavior from real runs.
- 🧰 **Tool** [Braintrust](https://www.braintrust.dev/) - Evaluation and observability platform with experiments, datasets, and CI integration for gating agent changes.
- 🧰 **Tool** [Weave](https://docs.wandb.ai/weave) - Weights & Biases toolkit for tracing, evaluating, and monitoring agent applications over time.
- 🧰 **Tool** [agentops (boshu2)](https://github.com/boshu2/agentops) - Independent verification layer for coding agents where a change only counts as done after a different model or a real test checks it, with the verdict recorded in the repo via a tamper-evident ledger.
- 🧰 **Tool** [SkillSpec](https://github.com/modiqo/skillspec) - CLI that makes agent skills followable, testable, and provable by converting prose skills into structured contracts, scoring follow-through risk, and generating execution traces of which steps ran, were skipped, and what evidence exists.
- 🧰 **Tool** [Shepherd](https://github.com/shepherd-agents/shepherd) - Python runtime that records agent execution as reversible, Git-like traces so meta-agents or humans can observe, fork, replay, and revert any run before results touch files, with copy-on-write forking, roughly 95% cache reuse on replay, and syscall-level permission enforcement.
- 🧰 **Tool** [grill-for-unknowns](https://github.com/nicobailon/grill-for-unknowns) - Portable SKILL.md agent skill that gates long-running subagent and coding-agent launches behind plan interrogation: it inspects the real territory (docs, source, tests, config) first, sorts what's known into facts, decisions, domain language, and unknowns across known/unknown quadrants, then emits a launch packet with assumptions, verification steps, and rollback risks before dispatch.
- 🧰 **Tool** [Fable Harness](https://github.com/Miguok/fable-harness) - Drop-in behavior protocol kit (hooks, a skill, and sub-agents auto-injected into every Claude Code session) enforcing a verify-first process: gather evidence before answering and verify changes before declaring done.
- 🧰 **Tool** [Mindwalk](https://github.com/cosmtrek/mindwalk) - Local visualization tool that replays Claude Code and Codex session logs as light moving across a 3D map of the repository, making long agent runs inspectable after the fact.
- 🧰 **Tool** [Waggle](https://github.com/modiqo/waggle) - MCP-native reference layer for agent handoffs: instead of pasting full context between agents, it passes a compact attributed, resolvable reference token that the receiving agent expands on demand.
- 🧰 **Tool** [Jacquard](https://github.com/jbwinters/jacquard-lang) - Research language designed around the machine-writes, human-verifies contract, using effect-typed signatures so an agent's generated code carries checkable declarations of what it is allowed to touch.

<!-- Research: gates, judges, and repair loops -->
- 📄 **Paper** [Agentic Verification of Software Systems](https://arxiv.org/abs/2511.17330) - Pairs a coding agent with a theorem prover (AutoRocq) in a generate-and-validate loop, turning formal proof into the exit gate for trusted automatic programming.
- 📄 **Paper** [A Trace-Based Assurance Framework for Agentic AI Orchestration: Contracts, Testing, and Governance](https://arxiv.org/abs/2603.18096) - Treats execution traces as the assurance substrate, pairing machine-checkable contracts, testing, and governance so recurring agent orchestration stays verifiable and auditable.
- 📄 **Paper** [Self-Evolving Agents with Anytime-Valid Certificates](https://arxiv.org/abs/2607.00871) - Confines self-modification to a small steering adapter around a frozen base model and gates each change with anytime-valid statistical tests that emit auditable certificates, reporting solve-count gains and logged regression prevention on a SWE-bench Verified subset.
- 📄 **Paper** [Delayed Verification Destabilizes Multi-Agent LLM Belief](https://arxiv.org/abs/2606.27409) - Models verifier-corrector loops in multi-agent LLM systems as delayed consensus, deriving a stability threshold where verification that is too strong or too late turns factual consensus into oscillation, plus a greedy corrector-placement algorithm validated on five open models.
- 📄 **Paper** [Lean4Agent: Formal Modeling and Verification for Agent Workflow and Trajectory](https://arxiv.org/abs/2606.06523) - Models agent workflows and trajectories in Lean 4 dependent types so semantic consistency is machine-checked rather than judged by an LLM, with verification-passing workflows outperforming failing ones by about 12% on software-engineering benchmarks.
- 📄 **Paper** [Regimes: An Auditable, Held-Out-Gated Improvement Loop](https://arxiv.org/abs/2606.10241) - Event-sourced agent runtime whose self-improvement loop gates every proposed repair behind static checks, sandbox execution, and held-out evaluation before adoption, keeping the full decision trail replayable.
- 📄 **Paper** [Agentic CLEAR: Automating Multi-Level Evaluation of LLM Agents](https://arxiv.org/abs/2605.22608) - Automated evaluation framework from IBM Research that grades agent behavior at system, trace, and node granularity without predefined error taxonomies, producing feedback aligned with human-annotated errors and predictive of task success.
- 📄 **Paper** [Diagnosis-Driven Automatic Repair for Agentic Workflow via Symbolic Inference](https://arxiv.org/abs/2607.02882) - FlowFixer converts runs of platform-built agentic workflows (Dify, Coze, n8n) into symbolic traces, infers correctness specs and node dependencies to localize root-cause failures, and generates targeted repairs at a 71.3% success rate.
- 📄 **Paper** [SkillCoach: Self-Evolving Rubrics for Evaluating and Enhancing Agentic Skill-Use](https://arxiv.org/abs/2607.01874) - Self-evolving rubric framework that scores agent trajectories on skill selection, following, composition, and reflection, exposing failures that pass/fail outcome checks miss and beating outcome-only filtering as a training signal.
- 📄 **Paper** [SWE-Doctor: Guiding Software Engineering Agents with Runtime Diagnosis from Bug Reproduction Tests](https://arxiv.org/abs/2607.00990) - Shows that naively feeding bug-reproduction tests to software-engineering agents can mislead them, and instead pipes runtime diagnosis from multi-faceted reproduction tests into patch generation, reaching 75.7% on SWE-bench Verified.
- 📄 **Paper** [AgentTether: Graph-Guided Diagnosis and Runtime Intervention for Reliable LLM Agent Operation](https://arxiv.org/abs/2607.06273) - Runtime repair layer that abstracts agent runs into a dependency-aware critical-transition graph, localizes failure-critical subtrajectories after a run, and guides recovery on re-execution without modifying the underlying agent.
- 📄 **Paper** [SWE-Review: Closing the Loop on Issue Resolution with Agentic Code Review](https://arxiv.org/abs/2607.06065) - Replaces one-shot PR generation with a generate-review-revise loop in which a reviewer agent explores the repository, accepts or rejects the PR, and feeds structured feedback into revision, with an accompanying benchmark and trajectory dataset.
- 📄 **Paper** [Reason Less, Verify More: Deterministic Gates Recover a Silent Policy-Violation Failure Mode](https://arxiv.org/abs/2607.07405) - Finds that 78% of observed agent failures in a tau^2-bench domain are silent wrong-state failures invisible to both the tool and the agent's self-report, and that deterministic read-only pre-execution gates in the loop recover them.
- 📄 **Paper** [Harnessing Code Agents for Automatic Software Verification](https://arxiv.org/abs/2607.06341) - Wraps a general code agent in a verification harness and lets it run until every targeted Coq lemma is proved, beating fixed human-designed proof strategies and reaching full lemma coverage with no expert intervention.
- 📄 **Paper** [LLM-as-a-Verifier: A General-Purpose Verification Framework](https://arxiv.org/abs/2607.05391) - Treats verification as a scaling axis and builds a training-free framework that computes continuous scores from token logits for fine-grained agentic feedback, scaled via score granularity, repeated evaluation, and criteria decomposition.
- 📄 **Paper** [From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents](https://arxiv.org/abs/2607.08028) - Moves deterministic agent behavior out of prompts into code, schemas, and behavior contracts, wrapping validation around a replaceable model boundary so enterprise agents remain auditable and safe across model substitutions.
- 📄 **Paper** [From Noisy Traces to Root Causes: Structural Trajectory Analysis and Causal Extraction for Agent Optimization](https://arxiv.org/abs/2607.07702) - STRACE structures redundant, heterogeneous agent execution traces by mining batch-level failure patterns and performing causal localization over a textual dependency graph, handing root causes rather than noisy trajectories to the reflection-based optimizer and lifting success on a formal verification task from 42.5% to 58.5%.
- 📄 **Paper** [Who Broke the System? Failure Localization in LLM-Based Multi-Agent Systems](https://arxiv.org/abs/2607.07989) - AgentLocate attributes failures in LLM multi-agent trajectories to both the responsible agent and the earliest decisive step, pairing LLM-based evaluation with independent assessor verification and confidence-weighted aggregation to outperform prior attribution methods on two benchmarks, the diagnose side of the verify step for dispatched-agent loops.
- 📄 **Paper** [3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse](https://arxiv.org/abs/2607.07980) - Builds a causal theory of 26 constructs and 67 relationships from 3,100 coded practitioner documents on how AI-authored pull requests reshape code review, arguing review is the control point through which a coding agent's effect on software is decided and that outcomes hinge on team expertise and review process structure rather than AI itself.
- 📄 **Paper** [Persuasion Attacks Can Decrease Effectiveness of CoT Monitoring](https://arxiv.org/abs/2607.08066) - Stress-tests chain-of-thought monitoring as an in-loop safety gate: adversarial agents arguing for policy-violating proposals turn the scratchpad into a persuasion channel, with monitor access to the agent's reasoning increasing approval of harmful actions by 9.5% on average, while pairing monitor and fact-checker from different model families cuts violating approvals by up to 45%.
- 📄 **Paper** [Physics-Audited Agentic Discovery in Scientific Machine Learning](https://arxiv.org/abs/2607.07379) - Verification-first workflow (PA-SciML) for agentic model discovery in scientific ML: fixes the scoring evaluator before search, derives machine-checkable physics requirements (boundary conditions, superposition, stiffness scaling, causality), audits every trained candidate's predicted fields against them, and separately searches prescribed input ranges for high-violation cases, reporting a surrogate as verified only under the stated checks; a domain-specific case of verification-gated agentic search.
- 📄 **Paper** [Bug Report Specification Refinement with Trajectory Guidance for Automated Program Repair](https://arxiv.org/abs/2607.07882) - TrajSpec runs a trajectory-collection agent over the pre-fix repository and mines the unverified trajectory for specification evidence, refining vague bug reports into structured specifications that guide automated program-repair loops.
- 📄 **Paper** [Failure as a Process: An Anatomy of CLI Coding Agent Trajectories](https://arxiv.org/abs/2607.09510) - Empirical anatomy of 3,843 CLI coding-agent trajectories across seven models and three scaffolds (OpenHands, MiniSWE, Terminus2), with 1,794 fully annotated over 63,000+ manually reviewed steps; models failure as a temporal process of onset, evolution, and recovery and finds failures dominated by epistemic errors that begin within the first few steps yet stay undetected until recovery is impossible, arguing for in-loop validation and intervention over final-outcome evaluation.
- 📄 **Paper** [Agentic Proof and Property-Based Testing via Property-Templates](https://arxiv.org/abs/2607.09072) - Dual-track verification-in-the-loop for AI-generated code: shared property templates drive both formal proof in Lean 4 and executable property-based tests for PySpark, raising agentic proof success up to 2.6x and cutting proof hallucinations by 59%.
- 📄 **Paper** [AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP](https://arxiv.org/abs/2607.11098) - Workbench that reproduces an agent failure, intervenes at the point it went wrong, and tests mitigations, turning one-off agent bugs into a repeatable diagnose-and-fix loop over MCP tool use.
- 📄 **Paper** [Latent Programming Horizons in Coding Agents](https://arxiv.org/abs/2607.05188) - Shows a coding agent's hidden states linearly encode program properties like correctness and test outcomes and predict future edits up to 25 steps ahead, a latent signal that could gate or steer verification loops before edits materialize.

## Securing Unattended Loops

A loop that runs while nobody watches needs stronger boundaries than an interactive session. These resources cover the main risks: untrusted intake content, over-broad permissions, and unsandboxed execution.

- ⚠️ **Critique** [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) - Simon Willison's rule of thumb: private data, untrusted content, and an exfiltration channel must never meet inside one unattended agent.
- ⚠️ **Critique** [Prompt injection series](https://simonwillison.net/series/prompt-injection/) - Ongoing series on the core unsolved vulnerability for loops whose intake includes content written by strangers.
- 📚 **Docs** [Agentic AI - Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) - OWASP threat model for agentic systems, useful when reviewing intake, memory, tool, and delegation boundaries.
- 📚 **Docs** [Designing AI agents to resist prompt injection](https://openai.com/index/designing-agents-to-resist-prompt-injection/) - OpenAI's official defense-in-depth guidance: least privilege, sandboxed tools, output verification, and human confirmation for the high-impact actions an unattended loop might take.
- 🧰 **Tool** [sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime) - Anthropic's OS-level filesystem and network sandboxing for arbitrary processes without requiring a container.
- 🧰 **Tool** [E2B](https://github.com/e2b-dev/E2B) - Open-source isolated cloud sandboxes for running untrusted, AI-generated code inside agent loops.
- 📚 **Docs** [Modal Sandboxes](https://modal.com/docs/guide/sandboxes) - Secure sandboxed execution for agent-driven code with resource limits and network controls.
- 🧰 **Tool** [Daytona](https://www.daytona.io/) - Infrastructure for running AI-generated code in fast, isolated sandboxes.
- 🧰 **Tool** [peerd](https://github.com/NotASithLord/peerd) - Browser-extension harness that runs the agent loop entirely client-side with user-supplied keys, sandboxed compute, and per-environment actor agents that hold only their tools and no API keys, isolating the orchestrator from untrusted content as a prompt-injection boundary.
- 📄 **Paper** [When Claws Remember but Do Not Tell: Stealthy Memory Injection in Persistent Personal Agents](https://arxiv.org/abs/2607.05189) - Shows one poisoned email can write hidden entries into a persistent personal agent's long-term memory that silently alter future unattended runs, introducing the 108-case WhisperBench evaluation and the MemGhost attack that reaches 87.5% success.
- 📄 **Paper** [Your Agent's Memories Are Not Its Own: Forged Reasoning Attacks on LLM Agent Memory and Defenses](https://arxiv.org/abs/2607.05029) - Introduces FARMA, an attack that plants forged reasoning traces in an agent's persistent memory so poisoned rationales carry into future runs, and SENTINEL, a reasoning-guard defense that cut attack success from up to 100% to zero in evaluation.
- 📄 **Paper** [Distributed Attacks in Persistent-State AI Control](https://arxiv.org/abs/2607.02514) - Extends AI-control evaluation to coding agents shipping code that persists across sessions, showing a misaligned agent can spread an attack across successive PRs to evade per-transcript monitors, and adds a stateful link-tracker monitor that cuts evasion from 93% to 47%.
- 📄 **Paper** [ElephantAgent: Contextual State Continuity in Agentic Systems](https://arxiv.org/abs/2607.01919) - Verification protocol that recomputes state digests before each query and logs authorized changes to a trusted-hardware ledger, so an agent's persistent memory and tool descriptions cannot be covertly poisoned between runs and can be rolled back to the last verified state.
- 🧰 **Tool** [Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill) - Cloudflare's open-sourced six-phase audit pipeline in which separate validation agents try to disprove each finding and fresh agents independently verify every claim against source code, emitting schema-validated findings that accumulate across repeated runs.
- 📄 **Paper** [The Balkanization of Execution-Security Research for AI Coding Agents](https://arxiv.org/abs/2607.05743) - Systematizes 39 papers on the execution layer around coding agents, spanning sandbox isolation, capability control, TOCTOU races, MCP threats, and egress control, surfacing five cross-cutting gaps and four verified CVEs in production agent harnesses.
- 📄 **Paper** [Context-to-Execution Integrity for LLM Agents](https://arxiv.org/abs/2607.06000) - Execution-boundary system where a deterministic gate admits a tool call only after field authority, exact-effect authorization, and invocation authority all bind to the same action manifest, protecting loops that read attacker-writable context.
- 📄 **Paper** [When Agents Remember Too Much: Memory Poisoning Attacks on Large Language Model Agents](https://arxiv.org/abs/2607.06595) - GhostWriter is a two-phase attack that poisons the long-term memory store of tool-using personal agents so injected content persists across runs and activates in later tasks.
- 📄 **Paper** [Token-Flow Firewall: Semantic Runtime Auditing for Persistent AI Agents](https://arxiv.org/abs/2607.08395) - Proposes TokenWall, a runtime firewall that audits a long-lived agent's semantic flows (memory updates, tool arguments, inter-component messages) before they reach privileged sinks, reporting attack success reduced to 12.5% with a 97.4% benign pass rate and 0.69s added latency.
- 📄 **Paper** [Prismata: Confining Cross-Site Prompt Injection in Web Agents](https://arxiv.org/abs/2607.08147) - Applies contextual least privilege to web agents by dynamically labeling page content with trust levels and mechanically confining what the agent can see and do, cutting cross-site prompt-injection attack success on benign pages without requiring developer annotations.
- 📄 **Paper** [TRACE: A Two-Channel Robust Attribution Watermark via Complementary Embeddings for LLM-Agent Trajectories](https://arxiv.org/abs/2607.08400) - Embeds a two-channel attribution watermark in LLM-agent trajectory logs (one channel keyed on content for deletion resistance, one on log structure for rewrite resistance) so provenance survives an adversary with full read/write access, reporting detection scores near z = 100 on long-horizon ToolBench and ALFWorld trajectories with no loss of agent performance.
- 📄 **Paper** [Beyond Attack-Success Rate: Action-Graded Severity Scale for Tool-Using AI Agents](https://arxiv.org/abs/2607.07474) - Replaces binary attack-success red-teaming metrics with a seven-level ordinal severity rubric (L0-L6) that grades harm along the agent's tool-call trajectory by action reversibility, scope expansion, and privilege escalation, validated with deterministic analysis and frontier-model judges across multiple victim models and defenses.
- 📄 **Paper** [Beware of Agentic Botnets: Scalable Untargeted Promptware Attacks via Universal and Transferable Adversarial HalluSquatting](https://arxiv.org/abs/2607.07433) - Introduces adversarial hallucination squatting, in which attackers pre-register resource names LLMs predictably hallucinate (at rates up to 85-100%) and plant universal, cross-model-transferable promptware payloads on the open web, reaching agent loops that autonomously ingest internet content with no direct injection channel.
- 📝 **Blog** [GitLost: How We Tricked GitHub's AI Agent into Leaking Private Repos](https://noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos/) - Noma Labs researcher Sasi Levi shows how hidden plain-English instructions in a malicious GitHub Issue make an issue-triggered GitHub Agentic Workflows agent exfiltrate private-repo contents into public comments, bypassing GitHub's data-leak guardrails with a one-word reframe, disclosed responsibly to GitHub.
- 🧪 **Benchmark** [ScopeJudge: Cost-Aware Pre-Execution Gating for Offensive Security Agents](https://arxiv.org/abs/2607.07774) - Benchmark of 4,897 tool calls from offensive-security agent trajectories, labeled by professional penetration testers, for studying pre-execution gating where a cheap trusted LLM judge accepts or rejects each proposed call before it runs and the engagement boundary must be inferred from the request rather than a fixed policy.
- 📄 **Paper** [Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors](https://arxiv.org/abs/2607.07368) - Studies AI control when several agents operating jointly on shared infrastructure pursue a malicious goal, evaluated on FakeLab (synthetic AI-lab codebase: 9 services, 86 benign tasks, 4 attack scenarios); finds a fragmentation effect (the more agents coordinate an attack, the less likely per-agent monitors catch any single attacker) and that explicit planners amplify attack success, directly relevant to monitoring fleets of background agents.
- 📄 **Paper** [Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions](https://arxiv.org/abs/2607.07461) - Finds taint-style flaws make up a substantial fraction of MCP-server vulnerabilities and normally demand context-specific code fixes, then proposes SPELLSMITH, which hardens tool descriptions with security-aware behavioral guidance so the agent's own self-reflection steers it away from triggering the vulnerable flows, mitigating multiple vulnerability classes at the tool-protocol layer without code-level patches.
- 📝 **Blog** [Factory Droid Shield 2.0: Learned Secret Detection for Autonomous Commits](https://factory.ai/news/droid-shield-2-0) - Factory upgrades the verification gate on every autonomous Droid commit with a two-model pipeline flanking the deterministic secret scanner, pairing a high-recall risk model with a precision referee.
- 🧰 **Tool** [destructive_command_guard](https://github.com/Dicklesworthstone/destructive_command_guard) - Rust safety hook that intercepts and blocks destructive Git and shell commands (hard resets, recursive deletes, database drops) before AI coding agents execute them, across Claude Code and other harnesses.
- 📄 **Paper** [Friendly Fire: Hijacking Defensive Cyber AI Agents for Remote Code Execution](https://ainowinstitute.org/publications/friendly-fire-exploit-brief) - Proof-of-concept showing prompt injections spread across ordinary repository files can hijack defensive security agents into remote code execution, demonstrating that even security-focused agent loops inherit the untrusted-content attack surface.
- 📝 **Blog** [How We Contain Claude Across Products](https://www.anthropic.com/engineering/how-we-contain-claude) - Anthropic engineering on capping agent blast radius with three containment architectures matched to threat models, including ephemeral sandbox containers for untrusted code execution.
- 📄 **Paper** [Rethinking MCP Security: A Large-Scale Study of Runtime MCP Servers and Scanner Reliability](https://arxiv.org/abs/2607.11086) - Large-scale study of live MCP servers finding widespread security weaknesses and that existing MCP security scanners miss or misreport many of them, a gap for anyone gating agent tool access on scanner output.
- 📄 **Paper** [Agent Hacks Agent: Autoresearch for Production-Agent Red-Teaming](https://arxiv.org/abs/2607.11698) - Uses an autonomous research loop to red-team production agents, having one agent iteratively discover, reproduce, and refine attacks against another, turning red-teaming itself into a recurring verified loop.
- 📄 **Paper** [Temporary Authority, Permanent Effects: Commit-Time Authorization for LLM Agents](https://arxiv.org/abs/2607.10487) - Proposes binding an agent's authority to the moment of commit rather than the moment of request, so a permission granted mid-run cannot be replayed later to cause irreversible effects in unattended execution.
- 📄 **Paper** [ANCHOR: Automated Alignment Auditing for CLI Agents on Real-World Harm](https://arxiv.org/abs/2607.10455) - Automated auditing framework that probes CLI coding agents for real-world harmful behavior and grades alignment, giving unattended-agent operators a repeatable safety check rather than manual spot review.
- 🧰 **Tool** [Clawk](https://github.com/clawkwork/clawk) - Runs coding agents inside disposable, network-restricted Linux VMs so an unattended or untrusted agent's blast radius is confined to a throwaway sandbox.
- 📝 **Blog** [Auto-Review of Agent Actions Without Synchronous Human Oversight](https://alignment.openai.com/auto-review/) - OpenAI's alignment team on reviewing agent actions asynchronously with automated reviewers when a human cannot watch every step, so oversight scales with agent throughput instead of gating it.

## State, Memory, And Context Persistence

This section focuses on durable loop state and cross-run context. For context-window design as its own lower layer, see the adjacent Context Engineering lists.

- 📚 **Docs** [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic guide to context as managed runtime state rather than a prompt dump.
- 📝 **Blog** [Agent Harnesses: the Infrastructure Layer Your LLM Agent Actually Needs](https://ninadpathak.com/blog/agent-harnesses/) - Covers execution loops, state, checkpointing, observers, and replayability.
- 📝 **Blog** [The Agent Loop Is the New OS](https://www.harness.io/blog/agent-loop-new-os) - Frames the agent loop as an OS-like boundary with context as RAM and tools as I/O.
- 📝 **Blog** [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) - Martin Fowler article on feedforward, feedback, and outer harnesses for coding agents.
- 📝 **Blog** [Context Engineering](https://simonwillison.net/2025/Jun/27/context-engineering/) - Simon Willison's framing of context engineering, useful for distinguishing context state from loop orchestration.
- 📝 **Blog** [Agentic Coding in 2026](https://sourcegraph.com/blog/agentic-coding) - Sourcegraph on supplying deterministic, large-codebase context and code intelligence so recurring agent runs reuse durable repository state instead of rediscovering it each time.
- 📝 **Blog** [Agentic AI State Management with ScyllaDB and LangGraph](https://www.scylladb.com/2026/04/08/agentic-ai-state-management-with-scylladb-and-langgraph/) - Durable agent state with checkpointers, write-ahead logs, and time-travel branching.
- 🧰 **Tool** [Mem0](https://github.com/mem0ai/mem0) - Open-source memory layer for retaining user, session, and agent state across repeated agent sessions.
- 🧰 **Tool** [Letta](https://github.com/letta-ai/letta) - Stateful agent framework from the MemGPT line with persistent, self-editing memory across runs.
- 🧰 **Tool** [Zep](https://github.com/getzep/zep) - Temporal knowledge graph memory that tracks how facts about users and systems change across sessions.
- 🧰 **Tool** [LangMem](https://github.com/langchain-ai/langmem) - SDK for extracting, consolidating, and retrieving long-term agent memory between loop runs.
- 🧰 **Tool** [Beads](https://github.com/steveyegge/beads) - Git-plus-SQLite issue and memory store that agents read and write with a `bd` CLI, giving recurring loops durable task state and progress that survives context resets.
- 📄 **Paper** [ARC: Active and Reflection-driven Context Management for Long-Horizon Agents](https://arxiv.org/abs/2601.12030) - Treats context as a managed runtime artifact, reorganizing the working context when degradation or context rot is detected across a long run.
- 📄 **Paper** [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670) - Formalizes agent memory as a write-manage-read loop and surveys compression, retrieval, reflective self-improvement, and policy-learned management across recurring runs.
- 📄 **Paper** [Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering](https://arxiv.org/abs/2604.08224) - Reviews how durable state, reusable skills, protocols, and the harness move out of model weights into external infrastructure, the substrate that lets loops persist progress and reuse capability across runs.
- 📄 **Paper** [Meta Context Engineering via Agentic Skill Evolution](https://arxiv.org/abs/2601.21557) - A bi-level loop where a meta-agent evolves reusable skills while a base-agent optimizes context, co-evolving the harness and context artifacts across runs (ICML 2026).
- 📄 **Paper** [Are We Ready for an Agent-Native Memory System?](https://arxiv.org/abs/2606.24775) - Evaluates twelve agent memory systems across five workloads from a data-management perspective, decomposing memory into representation, extraction, retrieval, and maintenance modules and finding localized maintenance more cost-efficient than global reorganization.
- 📄 **Paper** [Self-Evolving World Models for LLM Agent Planning](https://arxiv.org/abs/2606.30639) - Evolves a deployment-time world model while the agent and model weights stay frozen, retrieving observed transitions, distilling rules from prediction-observation mismatches, and filtering low-confidence forecasts so each run's errors improve later planning.
- 📄 **Paper** [Rethinking Continual Experience Internalization for Self-Evolving LLM Agents](https://arxiv.org/abs/2606.04703) - Finds that naively re-internalizing accumulated experience causes progressive capability collapse across self-improvement iterations, and identifies what keeps the loop stable: principle-level abstractions, step-wise injection for tool use, and off-policy distillation from stronger teacher trajectories.
- 🧰 **Tool** [GenericAgent](https://github.com/lsdefine/GenericAgent) - Self-evolving agent that grows a skill tree from a small seed, crystallizing completed runs into layered memory and reusable skills, with a master-worker mode for long-horizon goals.
- 📄 **Paper** [Self-GC: Self-Governing Context for Long-Horizon LLM Agents](https://arxiv.org/abs/2607.00692) - Governs long-horizon agent context as indexed lifecycle objects in an explicit nod to garbage collection, with a side-channel planner proposing fold, mask, and prune actions under harness-enforced recoverable sidecars, cutting production input tokens by 10-15%.
- 📄 **Paper** [CompactionRL: Reinforcement Learning with Context Compaction for Long-Horizon Agents](https://arxiv.org/abs/2607.05378) - Reinforcement-learning method that jointly optimizes task execution and compaction-summary generation so long-horizon agents can continue past finite context windows, lifting GLM-4.5-Air to 66.8% on SWE-bench Verified and shipping in the GLM-5.2 pipeline.
- 📄 **Paper** [SelfMem: Self-Optimizing Memory for AI Agents](https://arxiv.org/abs/2607.03726) - Memory framework in which the agent autonomously optimizes its own storage, retrieval, and summarization strategies per task instead of a fixed pipeline, reporting 40-49% gains over baselines on the BEAM benchmark at 100K-1M token contexts.
- 📄 **Paper** [Memory-Orchestrated Semantic System (MOSS): An Auditable Agentic Memory Architecture](https://arxiv.org/abs/2607.04391) - Model-, storage-, and API-agnostic agent memory architecture where the agent drives symbolic retrieval over a structured relational database, making long-term memory auditable and reproducible instead of opaque embedding search, validated in a year-long deployment.
- 📄 **Paper** [The Log Is the Agent: Event-Sourced Reactive Graphs for Auditable, Forkable Agentic Systems](https://arxiv.org/abs/2605.21997) - BabyAGI creator Yohei Nakajima makes an append-only event log the source of truth and the working graph a deterministic projection, giving long-running loops deterministic replay, cheap forking at any event, and end-to-end causal lineage from goal to model call.
- 📝 **Blog** [Agentics: Memorizing Session Transcripts Isn't Useful](https://12gramsofcarbon.com/p/agentics-memorizing-session-transcripts) - From thousands of agent sessions at Nori, reports zero coding-task benefit from giving agents search over prior session transcripts and argues loop state belongs in distilled artifacts like commits and docs because agents never prune stale context.
- 📝 **Blog** [Long-Running Agents](https://addyo.substack.com/p/long-running-agents) - Addy Osmani's essay on the infrastructure behind agents that run for hours or days, naming three walls (finite context, missing persistent state, unreliable self-verification) and the patterns that address them: durable event logs, checkpoint-and-resume, external state, and a planner/worker/judge split.
- 📄 **Paper** [StateFuse: Deterministic Conflict-Preserving Memory for Multi-Agent Systems](https://arxiv.org/abs/2607.05844) - Conflict-aware replicated memory contract with immutable history, explicit conflict objects, and projection-time resolution, so agent systems that accumulate contradictory observations across branches, retries, and replicas record state auditably instead of silently overwriting it.
- 📄 **Paper** [Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents](https://arxiv.org/abs/2607.08716) - Names the failure mode "behavioral state decay" (decision-relevant state such as prior attempts, diagnoses, and open subgoals gets buried or evicted as trajectories grow) and pairs the action agent with a proactive memory agent that maintains a structured memory bank and injects memory-grounded reminders only when needed, gaining +8.3 points on Terminal-Bench 2.0 and +6.8 on τ²-Bench.
- 📄 **Paper** [What to Keep, What to Forget: A Rate-Distortion View of Memory Compaction](https://arxiv.org/abs/2607.08032) - Rate-distortion framing that unifies KV-cache eviction, prompt compression, recurrent state, and cross-session agent memory compaction under a single objective with a layer-agnostic lower bound, showing why attention- and recency-based eviction discards information before future queries reveal what mattered.
- 📄 **Paper** [A Hierarchical Memory Architecture Overcomes Context Limits in Long-Horizon Multi-Agent Modeling](https://arxiv.org/abs/2607.07666) - Three-layer hierarchical memory keeps injected context bounded and roughly constant across multi-session, long-horizon multi-agent workflows, demonstrated by the Ensemble QSP framework autonomously selecting pharmacokinetic-pharmacodynamic models across 104 runs with overseer agents handling verification and troubleshooting.
- 📄 **Paper** [SkillCenter: A Large-Scale Source-Grounded Skill Library for Autonomous AI Agents](https://arxiv.org/abs/2607.07676) - Claims the largest open skill library for agents (216,938 structured skills across 24 domain bundles), built with an LLM quality gate (SkillGate) and iterative source-grounding that maps each retained claim to an exact source quotation, and shipped as offline-searchable SQLite FTS5 bundles, infrastructure for skills-as-persistent-state that agent loops accumulate and reuse.
- 📝 **Blog** [How version control will evolve for the agent boom](https://entire.io/blog/how-version-control-will-evolve-for-the-agent-boom) - Thomas Dohmke (former GitHub CEO, now founder of Entire) argues that agent session logs (prompts, tool calls, and decision checkpoints) are becoming the most important artifact in software development and should be versioned alongside code so agent fleets stop repeating mistakes, and that Git hosting must re-decentralize for agent-scale parallelism.
- 🧰 **Tool** [self-learning-skills](https://github.com/Kulaxyz/self-learning-skills) - Meta-skill for Claude Code, Cursor, and AGENTS.md-compatible agents that recognizes when a session has earned a hard-won golden path (or hit a dead-end worth remembering), distills the procedure including failed approaches, and persists it as a skill or rule auto-loaded next run, turning each session's discoveries into durable cross-session loop state.
- 📄 **Paper** [GitLake: Git-for-data for the agentic lakehouse](https://arxiv.org/abs/2607.08319) - Git-for-data design for an agent-first lakehouse that lifts single-table Iceberg snapshots into lakehouse-wide commits, branches, and merges, so agents work on isolated branches while humans review and publish, and pipeline outputs become visible atomically or not at all, with production lessons and correctness insights from a preliminary Alloy model of the core abstractions.
- 📄 **Paper** [Shared Selective Persistent Memory for Agentic LLM Systems](https://arxiv.org/abs/2607.09493) - Architecture that selectively persists four categories of reusable context (task specifications, data schemas, tool configurations, output constraints) across agent sessions while discarding session-specific reasoning traces, with cross-user sharing under access controls and a zero-token refresh path for recurring data updates, reporting 96% task completion vs 79% without memory and 71% with full-history carryover.
- 📄 **Paper** [Scoped Verification for Reliable Long-Horizon Agentic Context Evolution](https://arxiv.org/abs/2607.09175) - GRACE represents an agent's persistent instructions as a typed semantic graph and runs scoped verification over the local neighborhood of each proposed edit before committing it, so accumulated context evolves reliably across long-horizon deployment under distribution shift instead of drifting as flat text; evaluated on telecom agent tasks.
- 🧰 **Tool** [AgentMemory](https://github.com/rohitg00/agentmemory) - Persistent cross-session memory for coding agents: auto-capture lifecycle hooks, an MCP server, and a REST API so progress, decisions, and context survive across runs and tools.
- 🧰 **Tool** [TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) - Tencent Cloud's open-source local-first long-term memory for AI agents: a four-tier progressive pipeline from capture through consolidation with zero external API dependencies.
- 🧰 **Tool** [agent-memory (Neo4j Labs)](https://github.com/neo4j-labs/agent-memory) - Official Neo4j Labs graph-native memory system that stores conversations, builds knowledge graphs from agent interactions, and lets agents learn from their own reasoning traces.
- 🧰 **Tool** [re_gent](https://github.com/regent-vcs/re_gent) - Agent-native version control layered on top of Git that records agent activity at the prompt level, so you can answer why the agent did something and undo agent work without losing your own.
- 📄 **Paper** [StructAgent: Harness Long-Horizon Digital Agents with Unified Causal Structure](https://arxiv.org/abs/2607.11388) - State-centered framework that structures a long-horizon computer-use agent's state around a unified causal representation of task progress, regulating every update through verifier-backed state transitions with checkpointing and targeted failure recovery, lifting Qwen3.5-27B from 31.6% to 62.2% on OSWorld-Verified.
- 📄 **Paper** [The Compliance Trap: Diagnosing How AI Agents Consume Conflicting Memory](https://arxiv.org/abs/2607.10608) - Diagnoses how agents resolve contradictions in their own persistent memory, finding they tend to comply with the most recent or most assertive entry rather than the correct one, a failure mode for any loop that accumulates state across runs.

## Orchestration And Multi-Agent Delegation

Coordinating multiple agents inside one loop: planners, workers, judges, worktree isolation, and merge gates.

- 🧰 **Tool** [AutoGen](https://github.com/microsoft/autogen) - Multi-agent programming framework for conversations, tool use, and orchestration; active development has moved to the Microsoft Agent Framework.
- 🧰 **Tool** [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) - Microsoft's successor to AutoGen and Semantic Kernel for building and orchestrating multi-agent workflows in Python and .NET.
- 🧰 **Tool** [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based framework for controllable agent workflows, persistence, and human-in-the-loop steps.
- 🧰 **Tool** [CrewAI](https://github.com/crewAIInc/crewAI) - Framework for multi-agent workflows organized around roles, tasks, and crews.
- 📚 **Docs** [LlamaIndex Workflows](https://developers.llamaindex.ai/python/llamaagents/workflows/) - Event-driven workflow abstraction for agentic applications.
- 📚 **Docs** [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-python/handoffs/) - First-class delegation between specialized agents.
- 📚 **Docs** [Agent Protocol](https://agentprotocol.ai/) - API protocol for agent interaction, useful for separating loop managers from agent runtimes.
- 🧰 **Tool** [AgentKit](https://github.com/inngest/agent-kit) - TypeScript toolkit for durable, event-driven agents on workflow infrastructure.
- 🧰 **Tool** [deepagents](https://github.com/langchain-ai/deepagents) - LangChain project for deeper, longer-running agents with middleware and harness patterns.
- 📚 **Docs** [Temporal for AI](https://temporal.io/solutions/ai) - Durable execution for long-running agent workflows: crash-proof state, automatic retries, and human-in-the-loop signals.
- 🧰 **Tool** [Restate](https://restate.dev/) - Durable execution runtime for building resilient, stateful agents and workflows that survive failures mid-loop.
- 🧰 **Tool** [DBOS](https://www.dbos.dev/) - Lightweight PostgreSQL-backed durable execution library for crash-proof agent workflows, queues, and scheduled triggers.
- 🧰 **Tool** [Composio Agent Orchestrator](https://github.com/ComposioHQ/agent-orchestrator) - Orchestrates parallel coding agents in isolated worktrees that plan tasks, fix CI failures, respond to reviews, and manage their own PR lifecycle.
- 🧰 **Tool** [Omnigent](https://github.com/omnigent-ai/omnigent) - Databricks' open-source meta-harness and control plane that runs Claude Code, Codex, Cursor, and Pi under shared policies, with budget caps and human-approval gates enforced at the harness layer rather than in prompts.
- 📄 **Paper** [From Agent Loops to Structured Graphs: A Scheduler-Theoretic Framework for LLM Agent Execution](https://arxiv.org/abs/2604.11378) - Replaces opaque agent loops with immutable plan-version DAGs and a planning-execution-recovery split, giving inspectable scheduling, deterministic recovery, escalation, and termination guarantees.
- 🧰 **Tool** [Eve](https://github.com/vercel/eve) - Vercel's TypeScript-native agent framework with durable execution, sandboxed compute, and OpenTelemetry tracing built in, so recurring agent work persists, replays, and is observable across runs by default.
- 📄 **Paper** [Verified Multi-Agent Orchestration: A Plan-Execute-Verify-Replan Framework](https://arxiv.org/abs/2603.11445) - Decomposes work into a dependency-aware DAG, runs domain agents in parallel, and uses an LLM verifier to drive adaptive replanning with configurable stop conditions, the verify-and-replan core of a reliable loop.
- 📄 **Paper** [From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents](https://arxiv.org/abs/2603.22386) - Organizes how agent workflows are fixed ahead of time or generated and revised per run, and which evaluation signals drive that choice, a map of the design space for recurring loops.
- 🧰 **Tool** [Agent-as-a-Router](https://github.com/LanceZPF/agent-as-a-router) - Agentic model routing for coding agents reframed as a context-action-feedback loop (ACRouter: orchestrator, verifier, memory) that learns which LLM to route each task to from execution feedback rather than frozen priors, with the CodeRouterBench benchmark across 8 frontier models.
- 📝 **Blog** [Amp: Custom Agents](https://ampcode.com/news/custom-agents) - Amp's plugin-defined custom agents that run as the main agent or as subagents, spawn parallel workers, join tool pipelines, and use thread actions to build background review threads that report results back to a parent thread.
- 🧰 **Tool** [AgentsMesh](https://github.com/AgentsMesh/AgentsMesh) - Self-hosted control plane for running fleets of coding agents across your own machines, with scheduling, per-pod Git worktree isolation, Kanban work tracking, and merge-request integration.
- 🧰 **Tool** [Bernstein](https://github.com/sipyourdrink-ltd/bernstein) - Deterministic Python orchestrator that runs parallel CLI coding agents in isolated Git worktrees, gates merges on tests, lint, and type checks, and records every scheduling decision in a tamper-evident audit log.
- 🧰 **Tool** [Aeon](https://github.com/aaronjmars/aeon) - Autonomous agent framework that runs Claude Code unattended on GitHub Actions, dispatching skills on cron or reactive triggers with per-run quality scoring, persistent memory, and self-healing skill repair.
- 🧰 **Tool** [h5i](https://github.com/h5i-dev/h5i) - Gives each coding agent an isolated sandboxed Git worktree, dispatches one task to a team that peer-reviews each other's candidates, then replays and tests each candidate with a neutral verifier before merging the winner.
- 📄 **Paper** [SwarmResearch: Orchestrating Coding Agents for Open-Ended Discovery](https://arxiv.org/abs/2607.02807) - A shepherd agent with global context steers a population of search agents that each work in their own Git branch with local context, countering the context accumulation of solo long-running agents and matching or beating baselines on 13 of 15 open-ended discovery tasks.
- 📝 **Blog** [Scaling Long-Running Autonomous Coding](https://cursor.com/blog/scaling-agents) - Cursor traces the coordination designs behind week-long autonomous coding runs, from flat agents with locking to optimistic concurrency to a planner/worker/judge hierarchy, letting hundreds of concurrent workers push to one branch on projects exceeding a million lines.
- 🧰 **Tool** [babysitter](https://github.com/a5c-ai/babysitter) - Harness-agnostic orchestration framework that runs agent workflows as process-as-code with mandatory enforcement stops after every step, quality-convergence loops that re-run verify-and-refine until thresholds pass, human-approval breakpoints, and an immutable event-sourced journal for deterministic replay across 12 coding harnesses.
- 🧰 **Tool** [claude-code-merge-queue](https://github.com/funador/claude-code-merge-queue) - Local FIFO merge queue that serializes parallel Claude Code agents landing on a shared codebase, with a machine-wide build lock and a landing gate that blocks the integration branch until a configured check command passes, wired into the WorktreeCreate hook.
- 📝 **Blog** [Devin can now manage Devins](https://cognition.com/blog/devin-can-now-manage-devins) - Cognition's multi-Devin architecture where a coordinator Devin scopes a task into pieces, delegates each to a managed Devin running in its own isolated VM with terminal, browser, and dev environment, monitors progress, resolves conflicts, compiles the results, and reads workers' full trajectories to learn what worked and where they got stuck.
- 🧰 **Tool** [pilotfish](https://github.com/Nanako0129/pilotfish) - Multi-model orchestration layer for Claude Code where the frontier model plans, decides, and reviews while cheaper models execute volume work through six global subagent roles, with quality guarded by fresh-context verifier subagents rather than expensive models everywhere and graceful degradation when the frontier model is unavailable, shipped as three config files with no runtime code.
- 🧰 **Tool** [fable-advisor](https://github.com/DannyMac180/fable-advisor) - Claude Code plugin implementing an architect pattern where Fable 5 owns specs, decomposition, and verification while routing implementation to cheaper lanes (Grok 4.5 by default, GPT-5.6 via Codex CLI, or Sonnet/Opus fallback), with cross-vendor review and optional racing of two implementers on the same spec.
- 🧰 **Tool** [agent-chief](https://github.com/SmileLikeYe/agent-chief) - Local-first chief-of-staff layer that guards human attention across a fleet of agents and alerts: hard rules kill noise fast while a cache-stable LLM judge batches, blocks, or escalates what remains.
- 🧰 **Tool** [OpenTag](https://github.com/amplifthq/opentag) - Turns an existing work thread into a governed agent work loop: @-mention a coding agent from Slack, GitHub, GitLab, Linear, Lark, Telegram, or Discord, and OpenTag curates the context and manages the run.
- 🧰 **Tool** [herdr](https://github.com/ogulcancelik/herdr) - Single-binary terminal multiplexer purpose-built for running fleets of coding agents (Claude Code, Codex, Copilot CLI, Cursor Agent, and 15+ others) with per-agent state tracking.
- 🧰 **Tool** [Orca](https://github.com/stablyai/orca) - Open-source agent development environment for orchestrating a fleet of parallel coding agents (20+ backends) on your own subscriptions, with per-agent workspaces and review flow.
- 📄 **Paper** [Agentic Routing: The Harness-Native Data Flywheel](https://arxiv.org/abs/2607.11399) - Argues model routing must live inside the execution harness rather than in single-turn cost-quality tradeoffs, making step-level model selections from execution state and logging each decision as structured telemetry that feeds back to improve both routers and models.
- 📄 **Paper** [A Formal Hierarchical Architecture for Agentic Orchestration with Stack-Based Execution](https://arxiv.org/abs/2607.11138) - Formal orchestration architecture that runs agent workflows on a call stack with lazy capability discovery, giving multi-agent loops explicit, inspectable control flow instead of implicit prompt-driven handoffs.

## Benchmarks And Evaluation

How to measure loops rather than single runs: long-horizon, multi-session, reliability, and verifier-quality benchmarks.

- 🧪 **Benchmark** [SWE-bench](https://www.swebench.com/) - Benchmark for resolving real GitHub issues through code editing and tests.
- 📄 **Paper** [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) - Original SWE-bench paper.
- 📄 **Paper** [SWE-bench Goes Live](https://arxiv.org/abs/2505.23419) - Dynamic benchmark designed to reduce overfitting to static issue sets.
- 🧪 **Benchmark** [Terminal-Bench](https://www.tbench.ai/) - Benchmark for agents operating in terminal environments.
- 🧰 **Tool** [Terminal-Bench repository](https://github.com/harbor-framework/terminal-bench) - Open-source benchmark and harness for hard terminal tasks.
- 📄 **Paper** [AgentBench](https://arxiv.org/abs/2308.03688) - Multi-environment benchmark for evaluating LLMs as agents.
- 📄 **Paper** [WebArena](https://arxiv.org/abs/2307.13854) - Realistic web environment for autonomous agents.
- 📄 **Paper** [OSWorld](https://arxiv.org/abs/2404.07972) - Benchmark for multimodal agents operating full computer environments.
- 📄 **Paper** [ToolBench](https://arxiv.org/abs/2307.16789) - Tool-use benchmark and dataset for tool-augmented agents.
- 📄 **Paper** [GAIA](https://arxiv.org/abs/2311.12983) - Benchmark for general AI assistants requiring reasoning, tool use, and multi-step work.
- 📄 **Paper** [Tau-bench](https://arxiv.org/abs/2406.12045) - Benchmark for tool-agent-user interactions in realistic domains.
- 📄 **Paper** [VisualWebArena](https://arxiv.org/abs/2401.13649) - Visually grounded web-agent benchmark extending WebArena.
- 📄 **Paper** [AppWorld](https://arxiv.org/abs/2407.18901) - Benchmark of interactive app tasks with state-based and execution-based evaluation.
- 📄 **Paper** [Vending-Bench](https://arxiv.org/abs/2502.15840) - Benchmark for long-term coherence of autonomous agents; documents how small errors compound over very long loop horizons.
- 🧪 **Benchmark** [Vending-Bench leaderboard](https://andonlabs.com/evals/vending-bench) - Live long-horizon coherence results from Andon Labs.
- 🧪 **Benchmark** [SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios](https://arxiv.org/abs/2512.18470) - Release-note-derived evolution tasks where agents score far below isolated-issue benchmarks, quantifying the long-horizon gap loops must manage.
- 📄 **Paper** [EvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification](https://arxiv.org/abs/2604.01687) - A skill generator and a co-evolving surrogate verifier improve multi-file skill packages over iterations, evaluated on the SkillsBench benchmark of structured skill bundles.
- 🧪 **Benchmark** [SaaSBench: Coding Agents in Long-Horizon Enterprise SaaS Engineering](https://arxiv.org/abs/2605.17526) - Benchmark for agents on multi-dependency, interactive enterprise tasks, with automated evaluation that probes where long-horizon loops break down.
- 🧪 **Benchmark** [RoadmapBench: Evaluating Long-Horizon Agentic Software Development Across Version Upgrades](https://arxiv.org/abs/2605.15846) - 115 real version-upgrade tasks across 17 repositories requiring multi-file changes (median ~3,700 lines), stressing how far agent loops sustain coherent, large-scale work.
- 🧪 **Benchmark** [RefactorBench: Evaluating Stateful Reasoning in Language Agents Through Code](https://arxiv.org/abs/2503.07832) - Multi-file refactoring tasks that require tracking and carrying state across many steps, isolating the durable-state weakness that breaks long agent loops.
- 🧪 **Benchmark** [RigorBench: Benchmarking Engineering Process Discipline in Autonomous AI Coding Agents](https://arxiv.org/abs/2606.22678) - Scores planning, verification coverage, recovery, abstention, and atomic transitions (not just whether code passes), measuring the loop discipline that separates reliable agents from reckless trial-and-error.
- 🧪 **Benchmark** [SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks](https://arxiv.org/abs/2603.24755) - Quantifies structural erosion and verbosity creep across iteration checkpoints in native harnesses like Claude Code and Codex, evidence for why loops need verification and budgets.
- 🧪 **Benchmark** [LongCLI-Bench: A Preliminary Benchmark for Long-horizon Agentic Programming in Command-Line Interfaces](https://arxiv.org/abs/2602.14337) - Long-horizon CLI tasks where most runs stall below 30% completion, mapping where unattended loops break down.
- 🧪 **Benchmark** [Can LLM-as-a-Judge Reliably Verify Rubrics in Agentic Scenarios?](https://arxiv.org/abs/2606.29920) - Benchmark of 2,458 instances across research and coding domains measuring how reliably LLM judges verify rubrics on agent outputs, finding substantial noise even in strong models and quantifying the trade-offs of prompt design, batched evaluation, and majority voting.
- 🧪 **Benchmark** [SentinelBench: A Benchmark for Long-Running Monitoring Agents](https://arxiv.org/abs/2606.05342) - Microsoft Research benchmark of 100 tasks across 10 synthetic web environments that evaluates long-running monitoring agents on whether they wait or act appropriately, scoring task completion, response speed, and resource efficiency.
- 🧪 **Benchmark** [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](https://arxiv.org/abs/2606.29957) - Multi-session coding benchmark of 109 repository-level tasks reconstructed from 11,260 recorded user-agent sessions, replayed with an LLM user simulator and scored on final correctness and the number of corrective feedback turns.
- 🧪 **Benchmark** [The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break](https://arxiv.org/abs/2604.11978) - Cross-domain diagnostic benchmark that scales task horizon through depth and breadth extension, then attributes failures across 3,100+ agent trajectories to a seven-category taxonomy via a trajectory-grounded LLM judge validated against human annotation.
- 📄 **Paper** [Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents](https://arxiv.org/abs/2603.29231) - Reliability metrics for long-horizon agents (reliability decay, variance amplification, graceful degradation, meltdown onset) measured over roughly 24,000 episodes across 10 models, showing capability and reliability rankings diverge as tasks lengthen.
- 🧪 **Benchmark** [SEAGym: An Evaluation Environment for Self-Evolving LLM Agents](https://arxiv.org/abs/2606.17546) - Evaluation environment that measures whether a self-evolving agent's modifications to prompts, memory, and tools generalize to held-out tasks, using train, validation, and test splits and cost metrics on Terminal-Bench 2.0 and HLE.
- 🧪 **Benchmark** [EvoCode-Bench: Evaluating Coding Agents in Multi-Turn Iterative Interactions](https://arxiv.org/abs/2605.24110) - Benchmark of 26 evolving coding tasks across 227 evaluation rounds using cumulative executable tests to check that agents keep prior requirements working as specifications change, with top agents reaching only about 50% on multi-turn success metrics.
- 📄 **Paper** [On the Reliability of Computer Use Agents](https://arxiv.org/abs/2604.17849) - Repeated-execution study on OSWorld decomposing why computer-use agents fail tasks they previously completed, separating execution stochasticity, task-specification ambiguity, and behavioral variability as distinct causes of unreliability.
- 📄 **Paper** [AgentLens: Revealing the Lucky Pass Problem in SWE-Agent Evaluation](https://arxiv.org/abs/2605.12925) - Grades over 2,600 SWE-agent trajectories across eight models to show that a meaningful share of passes are lucky trial-and-error successes, replacing binary pass/fail with process-quality tiers that shift model rankings.
- 🧪 **Benchmark** [ORLoopBench: Solver-in-the-Loop Benchmarks for Self-Correction](https://arxiv.org/abs/2601.21008) - Formalizes infeasible-model debugging as a solver-in-the-loop process where each action triggers solver re-execution and infeasibility recomputation, giving deterministic verification for iterative repair in operations research.
- 🧪 **Benchmark** [LongDS-Bench: On the Failure of Long-Horizon Agentic Data Analysis](https://arxiv.org/abs/2605.30434) - Benchmark of 68 real-world data-analysis tasks built from Kaggle notebooks spanning 2,225 interactive turns, finding that long-horizon errors account for 52-69% of agent failures and that maintaining a correct analytical state is the core bottleneck.
- 🧪 **Benchmark** [MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks](https://arxiv.org/abs/2602.16313) - Multi-session benchmark of interdependent agentic tasks where agents must distill earlier sessions into memory and use it to guide later actions, showing that near-saturated scores on long-context memory benchmarks fail to transfer.
- 🧪 **Benchmark** [Momento: Evaluating Persistent Memory and Reasoning with Multi-Session Agentic Conversations](https://arxiv.org/abs/2606.00832) - Benchmark for persistent, tool-mediated task completion across multiple sessions, finding that agents fail by treating prior-session history as current context instead of stale state that needs re-validation.
- 🧪 **Benchmark** [π-Bench: Evaluating Proactive Personal Assistant Agents in Long-Horizon Workflows](https://arxiv.org/abs/2605.14678) - Benchmark of 100 multi-turn tasks across 5 user personas with hidden intents, inter-task dependencies, and cross-session continuity, measuring agent proactivity separately from task completion in long-horizon trajectories.
- 🧪 **Benchmark** [Can LLM Agents Be CFOs? Benchmarking Long-Horizon Resource Allocation](https://arxiv.org/abs/2603.23638) - A 132-month CFO simulation where agents repeat a monthly cycle of liquidity management, financial closings, and financing decisions with compounding state, and only 15.4% of trials survive the full horizon.
- 🧪 **Benchmark** [EvoAgentBench: Benchmarking Agent Self-Evolution via Ability Transfer](https://arxiv.org/abs/2607.05202) - Benchmark isolating whether agents transfer reusable procedures such as searching, debugging, and verification across episodes in four long-horizon domains linked by ability graphs, finding curated experience transfers but no automatic method yields consistent gains.
- 🧪 **Benchmark** [AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents](https://arxiv.org/abs/2607.02255) - Bounded-memory testbed built on Slay the Spire 2 where every agent decision is made from a fresh prompt assembled by typed retrieval over recorded state, keeping prompt size bounded across runs of any length, with 298 documented trajectories released.
- 📄 **Paper** [Is Three the Magic Number? An Empirical Evaluation of LLM-Based Repair Loops](https://arxiv.org/abs/2607.05197) - Empirical evaluation of iteration budgets for generate-validate-repair loops across code generation, test generation, and translation, finding the first three to four iterations capture most gains and that orchestration and feedback design matter more than the model.
- 🧪 **Benchmark** [DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks](https://arxiv.org/abs/2607.07946) - 113 from-scratch, contamination-free long-horizon software-engineering tasks with custom verifiers that accept any correct implementation, built to sidestep SWE-bench-style pretraining recall and better differentiate frontier coding agents.
- 🧪 **Benchmark** [PERFOPT-Bench: Evaluating Coding Agents on Software Performance Optimization](https://arxiv.org/abs/2607.07744) - Benchmarks the profile-diagnose-edit-verify loop where the verifier is a profiler rather than a test suite: agents must deliver measured, reproducible speedups without breaking correctness, and across seven agent configurations the framework choice shifts results even with identical models.
- 🧪 **Benchmark** [Benchmarking coding agents on Databricks' multi-million line codebase](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) - Databricks engineering post (July 8, 2026, authors including Matei Zaharia and Patrick Wendell) on an internal benchmark built from real merged PRs with test-suite verification, finding that models cluster into three capability tiers, token price is a poor proxy for end-to-end task cost, and harness choice matters, with their Pi harness sending about 3x less context per turn at equal quality.
- 🧪 **Benchmark** [UniClawBench: A Universal Benchmark for Proactive Agents on Real-World Tasks](https://arxiv.org/abs/2607.08768) - Capability-driven benchmark of 400 bilingual tasks for proactive agents operating everyday tools in live Docker environments with step-level checkpoints, decomposed into five foundational capabilities, skill usage, exploration, long-context reasoning, multimodal understanding, and cross-platform coordination, so failures localize to a root-cause capability instead of mixing capabilities per task, with closed-loop evaluation using multiple agent roles to simulate human feedback without leaking grading criteria.
- 🧪 **Benchmark** [SLBench: Evaluating How LLM Agents Follow Logical Relations in Skills](https://arxiv.org/abs/2607.09016) - Benchmark for whether agent loops respect the logical relations inside skill files (preconditions, constraints, fallbacks): 70% of 5,000+ public skills contain at least one such relation, and on 86 executable cases leading coding agents show unsafe-behavior rates up to 70%, with an inference-time scaffold cutting violations by 63%.
- 🧪 **Benchmark** [SWE-Milestone: Evaluating AI Agents on Continuous Software Evolution](https://arxiv.org/abs/2603.13428) - Commit-history-derived milestone task streams where agents must preserve system integrity across successive runs - frontier-model scores collapse from >80% on isolated tasks to at most 38% in continuous settings, quantifying the error-accumulation gap loop engineering targets.
- 🧪 **Benchmark** [AgentAbstain: Do LLM Agents Know When Not to Act?](https://arxiv.org/abs/2607.10059) - Benchmark measuring whether agents correctly abstain from acting when a task is underspecified, unsafe, or impossible, rather than proceeding anyway, a capability every unattended loop depends on for safe exits.
- 🧪 **Benchmark** [Agents Don't Just Agree, They Remember: Benchmarking Persistent Sycophancy](https://arxiv.org/abs/2607.10526) - Benchmark showing that once a stateful personal agent is nudged into a sycophantic stance, it persists across later sessions through memory, so single-turn sycophancy tests understate the risk in long-running agents.

## Operations Playbooks

Running loops in production: cost control, incident handling, and promoting validated agent behavior into cheaper deterministic paths.

- 📝 **Blog** [Agentic Engineering: The Agent Loop](https://junpingyi.com/books/agentic-engineering/agent-loop/) - Minimal mental model for the loop underlying agent operation.
- 📝 **Blog** [The agent loop: ReAct, plan-and-execute, reflection](https://www.kunwar.page/chapter/067-the-agent-loop-react-plan-and-execute-reflection) - Practical walkthrough of the base loop and common variants.
- 📝 **Blog** [How to Build an Agent](https://ampcode.com/how-to-build-an-agent) - Thorsten Ball's demystification of the inner agent loop: a model, a loop, and enough tokens.
- 📝 **Blog** [Agentic Coding Recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/) - Armin Ronacher's field notes on which practices hold up when agents do most of the work.
- 📝 **Blog** [Coding Agents 101: The Art of Actually Getting Things Done](https://devin.ai/agents101) - Practical delegation guidance from the Devin team on scoping tasks agents can actually finish.
- 📝 **Blog** [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code) - Cross-team field report of real recurring agent workflows in engineering, security, and data science.
- 📝 **Blog** [How Boris Uses Claude Code](https://howborisusesclaudecode.com/) - Unofficial but concrete compilation of Boris Cherny's autonomous setups: parallel worktrees, auto mode, `/loop`, `/schedule`, dynamic workflows, and `/goal` completion conditions.
- 📝 **Blog** [Agent of the Day: Copilot Agent PR Analysis](https://github.github.com/gh-aw/blog/2026-05-26-agent-of-the-day/) - Official walkthrough of a daily scheduled agentic workflow that ingests PR data, analyzes it, and publishes findings to a Discussion, a concrete recurring loop with trigger, intake, analysis, and output.
- 📄 **Paper** [Progressive Crystallization: Turning Agent Exploration into Deterministic, Lower-Cost Workflows](https://arxiv.org/abs/2607.07052) - Production lifecycle in which repeatedly validated agent-loop behaviors are promoted into deterministic workflows and demoted on regression, cutting per-incident agent cost by over 70% across eight months of a cloud AIOps system.
- 📄 **Paper** [Tool-Making and Self-Evolving LLM Agents in Low-Latency Systems](https://arxiv.org/abs/2607.08010) - Production tool-making pipeline that mines live execution traces to compile recurring SOP steps into validated, versioned tools agents call instead of regenerating code, cutting median latency 42% and errors up to 53% in a fulfillment-center alarm-triage deployment.
- 📝 **Blog** [AI Loop Engineering: Build Autonomous Agents with Claude Code /goal and Routines](https://www.sabrina.dev/p/loop-engineering-claude-code-goal-routines) - Sabrina Ramonov's practitioner walkthrough of building verified loops with Claude Code `/goal` and cloud routines: a six-part loop-engineering framework, five worked examples each with a verifiable end state, and a production daily support-ticket cleanup routine whose independent checker agents illustrate why the checker is the hard part.
- 📄 **Paper** [Agent Delivery Engineering Predictive Reliability Framework](https://arxiv.org/abs/2607.07689) - Proactive health-trajectory prediction for long-horizon multi-agent systems, aggregating 20 heterogeneous signals across five layers into a trust-margin metric with 8-hour forecasts at 76.8% direction accuracy, detecting degradation concealed by normal surface metrics across 15 days of production traffic.
- 🧰 **Tool** [rocketplaneIO](https://github.com/olemeyer/rocketplaneIO) - Self-hosted AI SRE for Kubernetes whose copilot investigates autonomously via eBPF traces, logs, and live service maps, but can only act through named, reversible, risk-graded operations.
- 📝 **Blog** [Migrating a Production AI Agent to GPT-5.6](https://ploy.ai/blog/migrating-a-production-ai-agent-to-gpt-5-6) - Lorenzo Gentile's July 2026 case study of swapping the model inside Ploy's production website-building agent (plans pages, writes components, screenshots its own work, decides when done): roughly a third of initial cross-model eval failures traced to Opus-specific harness assumptions rather than the new model, GPT-5.6 invented placeholder values for optional tool parameters (fixed via required-but-nullable schemas, after 52-64% of file reads silently returned empty), cache keys needed workspace scoping (0% to 83.7% first-call hits), and reasoning state moved to self-contained encrypted blobs, concrete evidence that eval harnesses and regression gates are the load-bearing layer when changing the model inside a production loop.

## Templates And Patterns

Reusable patterns that contributors can turn into future examples, templates, or playbooks.

- 🧾 **Template** [Resource entry template](templates/resource-entry.md) - Format for adding a single resource with evidence quality and category fit.
- 🧾 **Template** [Loop pattern template](templates/loop-pattern.md) - Template for documenting an operational loop such as PR babysitting, CI repair, or feedback clustering.
- 🧾 **Template** [Loop contract schema](schemas/loop-contract.schema.json) - Machine-readable schema for portable loop specs.
- 🧾 **Template** [Loop contract preview script](scripts/preview_loop_contract.py) - Dependency-free demo that validates and renders a loop contract JSON file.
- 🧾 **Template** [Translation guide](TRANSLATIONS.md) - How to add or maintain a language translation without drifting from the canonical English list.
- 🧾 **Template** [Pattern library index](patterns/README.md) - Practical loop patterns with triggers, state, verification gates, budgets, and escalation paths.

All fifteen documented patterns, including PR babysitting, CI repair, feedback clustering, deploy verification, and docs drift collection, live in the Pattern Library section with a full write-up each. Proposals for new patterns are welcome via issues or PRs.

## Examples And Schema

Concrete examples make the loop contract easier to adapt to real repositories.

- 🔁 **Pattern** [Example loop specs](examples/README.md) - Human-readable walkthroughs for PR babysitting, CI repair, and docs drift collection.
- 🧾 **Template** [Loop contract library](examples/README.md#contract-library) - Schema-validated loop contracts for every pattern-library loop, from PR babysitting to model routing.
- 🧾 **Template** [Runnable test-repair loop](examples/runnable/test-repair-loop.sh) - Dependency-light reference loop script with a verification gate, retry budget, durable progress log, repeat-failure detection, and escalation exit.
- 🧾 **Template** [Runnable loop guide](examples/runnable/README.md) - Maps the script line by line to the Loop Contract and shows how to drive it with Claude Code, Codex CLI, or any agent CLI.

Preview an example locally:

```sh
python3 scripts/preview_loop_contract.py examples/pr-babysitter-loop.json
```

## Community Gallery

The gallery is for real-world or realistic loop examples contributed by the community.

**Running a real loop?** Share it, real or anonymized, in the patterns discussion linked under Roadmap And Discussion below. Use the [minimum useful case study](gallery/README.md#minimum-useful-case-study) and [anonymization](gallery/README.md#safe-anonymization-checklist) checklists so others can learn from it safely.

- 🧾 **Template** [Loop gallery guide](gallery/README.md) - Quality bar for contributed loop examples with receipts and lessons learned.
- 🧾 **Template** [Loop gallery template](gallery/template.md) - Markdown template for sharing a loop's trigger, intake, state, verification, escalation, and safety notes.
- 🔁 **Pattern** [PR babysitter reference loop](gallery/pr-babysitter-reference.md) - Reference gallery entry for keeping a pull request moving.
- 🔁 **Pattern** [CI repair reference loop](gallery/ci-repair-reference.md) - Reference gallery entry for turning failing CI into a verified patch or escalation.
- 🔁 **Pattern** [Docs drift reference loop](gallery/docs-drift-reference.md) - Reference gallery entry for recurring docs/code consistency checks.

## Critiques, Risks, And Limitations

Skeptical takes and measured failure modes, because a loop that cannot fail safely should not run unattended.

- ⚠️ **Critique** [Most Developers Do Not Need Agent Loops Yet](https://alphasignalai.substack.com/p/most-developers-do-not-need-agent) - Useful caution against adopting loops before the task, signal, and economics justify them.
- ⚠️ **Critique** [Engineering Agentic Systems for Reliability](https://pruningmypothos.com/systems/engineering-agentic-systems-for-reliability/) - Cautions that agentic systems fail at boundaries when permissions, verification, traceability, and escalation are weak.
- ⚠️ **Critique** [Self-Correcting Agents: Reflexion, CRITIC, and ReAct Loops Compared](https://callsphere.ai/blog/self-correcting-agents-reflexion-critic-react-loops-compared-2026) - Compares self-correction patterns and their cost/failure tradeoffs.
- ⚠️ **Critique** [How to Build an AI Agent Harness: A 2026 Complete Guide](https://atlan.com/know/how-to-build-ai-agent-harness/) - Broad guide with useful warnings on data readiness, permissions, context management, and evaluation.
- ⚠️ **Critique** [Harness Engineering vs Prompt Engineering vs Context Engineering Explained](https://medium.com/@visrow/harness-engineering-vs-prompt-engineering-vs-context-engineering-explained-0423b692c87d) - Adjacent framing that helps avoid confusing loop engineering with the surrounding harness discipline.
- 📄 **Paper** [Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering](https://arxiv.org/abs/2606.17799) - Argues benchmark scores conflate the model with the harness and penalize valid alternatives, so headline numbers hide which loop and harness choices actually move performance.
- 📄 **Paper** [Understanding the Challenges in Iterative Generative Optimization with LLMs](https://arxiv.org/abs/2603.23994) - Empirically isolates three hidden design choices that make self-improving agent loops succeed or fail - starting artifacts, credit horizons over execution traces, and batching strategy - explaining why iterative refinement loops stay brittle in production.
- 📄 **Paper** [The Illusion of Multi-Agent Advantage](https://arxiv.org/abs/2606.13003) - Systematic evaluation showing automatically generated multi-agent systems consistently underperform chain-of-thought self-consistency while costing up to 10x more, cautioning that auto-designed orchestration adds complexity without functional benefit.
- ⚠️ **Critique** [The Coming Loop](https://lucumr.pocoo.org/2026/6/23/the-coming-loop/) - Flask creator Armin Ronacher's skeptical essay on harness loops, examining what continuously re-driving agents past their natural stopping points does to code quality, review capacity, and human understanding of the resulting systems.
- ⚠️ **Critique** [Loop Engineering, the Latest AI Buzzword, Still Needs Humans in the Loop](https://www.theregister.com/ai-and-ml/2026/06/24/loop-engineering-latest-ai-buzzword-still-needs-humans-in-the-loop/5261735) - The Register's report on the June 2026 loop-engineering discussion, collecting the Steinberger, Osmani, and Cherny quotes while arguing that vendor token-consumption incentives and model non-determinism keep humans in the loop.
- 📄 **Paper** [When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents](https://arxiv.org/abs/2607.01641) - Characterizes infinite agentic loops, a failure class where unbounded feedback paths make agents repeat calls, tools, or handoffs forever, and ships IAL-Scan, a static analyzer that confirmed 68 real cases across 47 of 6,549 scanned agent projects at 91.9% precision.
- 📄 **Paper** [The Blind Curator: How a Biased Judge Silently Disables Skill Retirement in Self-Evolving Agents](https://arxiv.org/abs/2607.07436) - Shows via corrupted-reward analysis that false-pass bias in an LLM judge silently disables the skill-retirement mechanism that keeps a self-evolving agent's growing skill library from drifting below the no-skill baseline.
- 📄 **Paper** [Do LLM-Generated Skills Make Better AI Data Scientists? A Component Ablation Across Data-Science Workflows](https://arxiv.org/abs/2607.07504) - Negative result for low-curation skill libraries: across four data-science lifecycle stages (56 tasks), fully LLM-generated skill files show no reliable improvement over plain task prompting, and component ablations find no skill part that helps either (all p > 0.396). Useful counterweight to the skill-generation enthusiasm in self-evolving agent stacks, curation still matters.
- 📄 **Paper** [The Verification Horizon: No Silver Bullet for Coding Agent Rewards](https://arxiv.org/abs/2606.26300) - Position paper arguing verification has become harder than generation for coding agents: every verifier is only a proxy for underspecified human intent, so reward design faces a horizon that no single verification mechanism crosses.
- ⚠️ **Critique** [Write Code Like a Human Will Maintain It](https://unstack.io/write-code-like-a-human-will-maintain-it) - Argues that agent-driven codebases create a compounding feedback loop where every merged shortcut becomes training signal for the next generation of changes, so code quality standards matter more, not less, under automation.
- 📝 **Blog** [Claude Code Sends 33k Tokens Before Reading the Prompt](https://systima.ai/blog/claude-code-vs-opencode-token-overhead) - July 12, 2026 proxy-interception study of per-turn harness overhead: Claude Code sends ~33k tokens of scaffolding before user input versus OpenCode's ~7k (a 4.7x gap that narrows to 3.3x on newer models), mid-session cache-block rewrites produce up to 54x more cache-write tokens on identical tasks, a 72KB instruction file adds ~20k tokens per request, five MCP servers add 5-7k more, and subagent delegation alone multiplied total cost 4.2x. Directly quantifies the per-iteration economics that compound across recurring loops, with transparent methodology of identical-outcome tasks and a logging proxy capturing exact request payloads.

## Adjacent Awesome Lists

Neighboring curated lists for the layers around loop engineering.

- 🧭 **List** [Awesome Harness Engineering](https://github.com/ai-boost/awesome-harness-engineering) - Comprehensive list for the agent harness layer that Loop Engineering builds on.
- 🧭 **List** [Awesome Harness Engineering](https://github.com/walkinglabs/awesome-harness-engineering) - High-signal harness list with strong categories for context, guardrails, specs, evals, runtimes, and benchmarks.
- 🧭 **List** [Awesome Agent Harness](https://github.com/AutoJunjie/awesome-agent-harness) - Curated tools and resources for environments, constraints, and feedback around coding agents.
- 🧭 **List** [Awesome Context Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) - Survey-style list for context engineering across LLMs and agents.
- 🧭 **List** [Awesome Prompt Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering) - Classic adjacent list for prompt techniques and prompting resources.
- 🧭 **List** [Awesome LLM Agents](https://github.com/kaushikb11/awesome-llm-agents) - General list of LLM agent papers, frameworks, and applications.
- 🧭 **List** [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents) - Broad AI agent ecosystem map.
- 🧭 **List** [Awesome CLI Coding Agents](https://github.com/bradAGI/awesome-cli-coding-agents) - Directory of terminal-native coding agents, parallel runners, autonomous loops, and the harnesses that orchestrate them.
- 🧭 **List** [Awesome Self-Evolving Agents](https://github.com/XMUDeepLIT/Awesome-Self-Evolving-Agents) - Survey-style list of agents that improve themselves over repeated runs, an adjacent angle on long-running loops with memory and verification.
- 🧭 **List** [Awesome AI Agent Papers](https://github.com/VoltAgent/awesome-ai-agent-papers) - Curated 2026 research collection across agent engineering, memory, evaluation, workflows, and autonomous systems, a paper-level feeder for loop-design foundations.
- 🧭 **List** [awesome-ralph](https://github.com/snwfdhmp/awesome-ralph) - Curated directory for the Ralph technique, collecting official resources, implementations, playbooks, tutorials, and community channels for running coding agents in automated loops until specifications are fulfilled.
- 🧭 **List** [Awesome Agent Loops](https://github.com/serenakeyitan/awesome-agent-loops) - Curated collection of /loop, /goal, and /schedule commands for Claude Code and Codex sourced from practitioner posts, organized around trigger, condition, and skill structure.

## Discovery And Distribution

Prefer this list as a website or as structured data?

- 🧾 **Template** [Landing page](https://chaoyue0307.github.io/awesome-loop-engineering/) - SEO-friendly entry point for the repository.
- 🧭 **List** [Hugging Face dataset mirror](https://huggingface.co/datasets/cy0307/awesome-loop-engineering) - Synced dataset repo with the full project plus generated `data/resources.csv` and `data/resources.jsonl` resource sheets.
- 🧾 **Template** [Landing page source](docs/index.html) - Source for the static landing page.
- 🧾 **Template** [Sitemap](docs/sitemap.xml) - Crawl hints for the landing page and core repository pages.
- 🧾 **Template** [Robots file](docs/robots.txt) - Allows indexing and points crawlers to the sitemap.

Load the curated resources directly from the Hugging Face dataset mirror:

```python
from datasets import load_dataset
resources = load_dataset("cy0307/awesome-loop-engineering", "resources", split="train")
```

For launch copy and backlink strategy, use the [distribution checklist](meta/DISTRIBUTION.md).

## Roadmap And Discussion

Where this project is going and where to talk about it.

- 🧾 **Template** [Release notes](https://github.com/ChaoYue0307/awesome-loop-engineering/releases) - Versioned changelog of new resources, patterns, and repository changes.
- 🧾 **Template** [Roadmap](ROADMAP.md) - Near-term work, pattern priorities, gallery goals, and open questions.
- 🧾 **Template** [Launch article](posts/launch.md) - Shareable explanation of the concept and repository.
- 🧾 **Template** [Discussion guide](meta/DISCUSSIONS.md) - Suggested discussion categories, starter prompts, and moderation standard.
- 🔁 **Pattern** [Show your Loop Engineering patterns](https://github.com/ChaoYue0307/awesome-loop-engineering/discussions/2) - Community discussion for real or anonymized loop examples.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

This repository uses a strict [curation standard](meta/CURATION.md) to keep the list focused, verifiable, and useful for builders. Maintainers can use the [maintenance guide](meta/MAINTENANCE.md) for link checks, identity checks, and periodic refreshes.

For community expectations and support channels, see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [SUPPORT.md](SUPPORT.md), and [SECURITY.md](SECURITY.md).

Fast path for adding a resource:

- Check that it is about AI/coding-agent Loop Engineering or a direct foundation for it.
- Search the README to avoid duplicates.
- Pick the most specific category.
- Add one entry using this format:

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

- Open a pull request and explain the category fit, source type, and why builders should care.

Fast path for contributing a loop pattern: start from the loop pattern template or loop contract schema, include trigger, discover/intake, delegation, workspace, context, verification, durable state, budget, escalation, and exit, then open a pattern suggestion issue if you want feedback before writing the full pattern.

Good submissions should answer three questions:

1. Is this about the new AI/coding-agent meaning of Loop Engineering or a direct foundation for it?
2. Does it help someone design, run, verify, evaluate, or critique recurring agent systems that coordinate prompting, context, harnesses, verification, and state?
3. Is the source stable, public, and specific enough to be useful?

## Citation

If this repository is useful in your work, please cite it with:

```bibtex
@misc{chaoyue2026awesome_loop_engineering,
  author       = {He, Chaoyue},
  title        = {Awesome Loop Engineering},
  year         = {2026},
  howpublished = {\url{https://github.com/ChaoYue0307/awesome-loop-engineering}},
  note         = {Curated resources for Loop Engineering}
}
```

**Reusable blurb** (for blog posts, talks, internal docs, or community posts):

> Loop Engineering is the practice of designing recurring AI-agent and coding-agent systems that discover work, delegate to agents, verify results, persist state, and retry or escalate on a cadence or until a goal is reached. *Awesome Loop Engineering* is a curated, implementation-focused resource collection for this practice: [github.com/ChaoYue0307/awesome-loop-engineering](https://github.com/ChaoYue0307/awesome-loop-engineering)
