# Awesome Loop Engineering

<!-- last-synced: 2026-07-20 -->

<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering cover" width="100%"></a>
</p>

<p align="center">
  <sub>如果这个项目对你有帮助，可以 Star 以便再次找到它，<a href="https://github.com/ChaoYue0307/awesome-loop-engineering/fork">Fork loop contracts 与数据 schema</a>，或<a href="https://github.com/ChaoYue0307/awesome-loop-engineering/subscription">订阅 Releases 与 Discussions</a> 获取精选更新。</sub>
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
  <a href="TRANSLATIONS.md">帮助翻译</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">落地页</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Hugging Face 镜像</a>
</p>

> 设计可重复运行的 AI-agent 系统：明确触发条件、外部验证、持久状态、资源预算和人类接管机制。

Prompt engineering 改进你对模型说什么。Context engineering 改进模型能看到什么。Harness engineering 改进单次 agent 运行周围的工具、权限、沙箱和检查。**Loop Engineering 位于三者之上**：人不再逐轮手动提示 agent，而是设计一个循环系统，让它负责提示、监督、验证、更新状态并再次触发 agents。

一个 loop 会发现工作、分派给一个或多个 agents、检查结果、留下可审查的运行凭证（receipts）、更新状态并决定下一步；它按既定节奏重复运行，或在达到可验证目标后停止。

Loop Engineering 专指具备明确触发、外部验证和持久状态的可重复 AI-agent 与 coding-agent 系统，不包括软件事件循环、控制论、增长循环、通用 workflow automation 或非 AI feedback loop。

可直接从 730 篇论文、官方文档、工具、benchmark 与实践指南，22 个操作模式、22 个经 schema 校验的 loop contracts 和 8 个 runtime starters（3 个可直接执行，5 个可复制改造）开始，并通过社区 gallery 和 8 种语言入口继续探索。

## 一句话定位

- Prompt engineering 关注：我应该对模型说什么？
- Context engineering 关注：模型应该看到什么状态和知识？
- Harness engineering 关注：agent 周围应该有什么工具、权限、测试、沙箱和反馈？
- Loop engineering 关注：当人不在内循环里时，什么系统负责发现工作、分派给 agents、验证结果、持久化状态、决定下一步并重新运行？

Prompt、context 和 harness engineering 让单次 agent 运行更好。Loop Engineering 让 agent 工作能跨时间重复、观察和治理。

## Loop Contract

一个有效的 loop 通常需要这些部分：

| 部分                | 设计问题           | 常见产物                                                  |
| ----------------- | -------------- | ----------------------------------------------------- |
| Objective         | loop 要优化什么？    | goal、issue、PRD、runbook                                |
| Trigger           | 什么时候运行？        | schedule、webhook、`/loop`、`/goal`、automation           |
| Discover / Intake | 如何发现工作？        | GitHub query、Linear filter、CI failure、feedback stream |
| Workspace         | agent 在哪里安全行动？ | worktree、sandbox、branch、container                     |
| Context           | 哪些知识应该长期存在？    | `AGENTS.md`、`CLAUDE.md`、`SKILL.md`、docs               |
| Delegation        | 哪个 agent 负责什么？ | explorer、implementer、reviewer、judge                   |
| Verification      | 什么机制判断通过或失败？   | tests、typecheck、lint、evals、trace graders              |
| State             | 下一轮需要保留什么？     | progress file、checkpoint、trace、运行凭证（receipt）        |
| Budget            | 何时停止消耗？        | max turns、max retries、token budget、time box           |
| Escalation        | 何时交给人？         | PR、issue、Slack alert、triage inbox                     |
| Exit              | loop 如何知道完成？   | acceptance criteria、passing checks、no work found      |

## 成熟度模型

Loop Maturity Model 用来判断**一个具体的 recurring agent workflow**需要哪些运行能力。它衡量 workflow 如何启动、记忆、验证、分工和接受监督，而不是给模型智能、团队水平或产品质量打分。

使用时，先从任务的结果、证据、风险和 human owner 出发，再选择最低但足够可靠的等级。每一级都会增加实现、观测、权限和维护成本；只有当前等级反复出现明确限制时才向上升级。能力应按顺序建立：先保存状态，再延长无人值守运行；先建立外部验证，再增加 agents；能影响用户或基础设施之前，先补齐 production controls。

| 等级 | 运行方式 | 为什么需要 | 具体示例 | 升级信号 |
| --- | --- | --- | --- | --- |
| **0 · Manual prompting** | 人保存上下文、写下一条指令并判断结果。 | 让一次性、模糊或高度依赖判断的工作保持人工监督。 | 开发者让 agent 修复一个失败测试，检查 diff 后再决定是否继续。 | 相同任务和反馈步骤频繁重复，已经可以编码。 |
| **1 · Scripted retry** | 有界脚本重复调用一个 agent，并把外部失败结果反馈给它。 | 省去重复 reprompt，同时保持单一目标和单一反馈信号。 | 运行 `pytest`，最多把失败输出反馈给 agent 三次。 | 任务应该按时间或事件自动启动，不再依赖人工发起。 |
| **2 · Scheduled loop** | schedule 或 event 触发新的 intake、一次有界运行以及 report 或 artifact。 | 去掉人工启动，并明确 cadence、idempotence 和 no-work exit。 | 每晚检查 docs drift，仅在代码与文档不一致时生成报告。 | 工作跨越多次运行、重复处理条目或在调用之间丢失上下文。 |
| **3 · Stateful loop** | 在模型之外持久化已完成工作、blocker、证据和 next action。 | 让 workflow 能在重启后继续，避免重复工作，并支持审计。 | feedback clusterer 保存已处理 ID、历史主题和最近成功 checkpoint。 | 稳定的外部证据已经可以判断状态转换或完成是否有效。 |
| **4 · Self-verifying loop** | tests、evals、policy checks、traces 或独立 evaluator 决定能否继续和退出。 | 用可检查的证据取代 agent 对成功的自我判断。 | CI repair loop 只有在原失败命令通过且 diff 未越界时才退出。 | 单一角色成为瓶颈，需要职责分离或独立 review。 |
| **5 · Multi-agent loop** | 专门角色通过明确 handoff 和共享状态分担 discovery、action、review 与 judgment。 | 引入职责分离和并行专业能力，同时避免 acting agent 自我批准。 | security loop 由 explorer 找候选问题、reproducer 复现、reviewer 判断严重性和范围。 | workflow 将影响 production、用户、资金、凭证或其他高影响系统。 |
| **6 · Production-supervised loop** | telemetry、least privilege、budgets、approvals、rollback、incident ownership 和 human escalation 共同约束每次运行。 | 控制 blast radius，让无人值守的 production work 可观察、可中断、可追责。 | deploy verifier 监控 rollout metrics，阈值被突破时暂停并把 rollback approval 交给 release owner。 | 随 workflow 演进持续强化 service objectives、replay、权限审查、failure drills 和成本控制。 |

等级代表能力，不代表目标越高越好。很多有价值的 workflow 停在 Level 2 或 3 就足够；拥有 durable state 的可靠 Level 3，优于目标模糊、检查薄弱或只有形式化角色的 Level 5。

## 必读入口

完整资源列表以英文 README 为准：[README.md](README.md)。

建议从这些直接讨论 Loop Engineering 的资料开始：

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - Addy Osmani 对 Loop Engineering 的核心定义和 Codex / Claude Code primitives 对照。
- [Loop Engineering](https://addyo.substack.com/p/loop-engineering) - 同文 Substack 版本，包含 Peter Steinberger 和 Boris Cherny 的相关引用。
- [Loop Engineering](https://cobusgreyling.substack.com/p/loop-engineering) - 简明解释从 prompt agents 到 design loops 的转变。
- [Stop Prompting. Design the Loop.](https://www.pulumi.com/blog/stop-prompting-design-the-loop/) - 拆解 loop 的构建模块（automations、worktrees、skills、connectors、subagents），并强调外部记忆与以 tests/builds 为 oracle 的验证。
- [The Anthropic leader who built Claude Code ditched prompting](https://thenewstack.io/loop-engineering/) - 报道 Boris Cherny 从手动 prompting 转向编写 loops 来处理 PR、CI、deploy 等重复性 agent 工作。

## 如何贡献内容

欢迎提交 PR。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

最快流程：

1. 确认资源属于 AI/coding-agent 语境的 Loop Engineering，或是它的直接基础。
1. 在 README 中搜索，避免重复。
1. 选择最具体的分类。
1. 按这个格式添加一行：

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

1. 在 PR 中说明：为什么相关、属于哪个分类、资源类型是什么、为什么对 builders 有用。

## 翻译

如果你想维护新的语言版本，请阅读 [TRANSLATIONS.md](TRANSLATIONS.md)。翻译应该保留概念边界：不要把 event loop、growth loop 或普通 automation 翻译进来。

## 许可证

本仓库中的原创整理文字、注释、模板、模式文档和仓库元数据使用 [CC0-1.0](LICENSE) 发布。

本仓库链接到的第三方论文、博客、文档、工具、benchmark、图片和其他外部资源仍遵循其原作者或发布方各自的许可证和使用条款。本仓库只是索引和链接它们，并不重新授权这些外部内容。
