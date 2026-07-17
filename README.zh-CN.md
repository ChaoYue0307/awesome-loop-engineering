# Awesome Loop Engineering

<!-- last-synced: 2026-07-17 -->

<p align="center">
  <img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering cover" width="100%">
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

一个 loop 会发现工作、分派给一个或多个 agents、检查结果、记录状态、决定下一步，并按照节奏或直到满足可验证目标为止持续运行。

Loop Engineering 专指具备明确触发、外部验证和持久状态的可重复 AI-agent 与 coding-agent 系统，不包括软件事件循环、控制论、增长循环、通用 workflow automation 或非 AI feedback loop。

可直接从 545 条经审核资源、20 个操作模式、20 个经 schema 校验的 loop contracts 和 8 个 runtime starters（3 个可直接执行，5 个可复制改造）开始，并通过社区 gallery 和 8 种语言入口继续探索。

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
| State             | 下一轮需要保留什么？     | progress file、checkpoint、trace、issue comment          |
| Budget            | 何时停止消耗？        | max turns、max retries、token budget、time box           |
| Escalation        | 何时交给人？         | PR、issue、Slack alert、triage inbox                     |
| Exit              | loop 如何知道完成？   | acceptance criteria、passing checks、no work found      |

## 成熟度模型

| 等级  | 名称                         | 描述                                                              |
| --- | -------------------------- | --------------------------------------------------------------- |
| 0   | Manual prompting           | 人读取状态并写下一条 prompt。                                              |
| 1   | Scripted retry             | 脚本把错误反馈给 agent。                                                 |
| 2   | Scheduled loop             | agent 按固定节奏运行并报告结果。                                             |
| 3   | Stateful loop              | 通过文件、issue、checkpoint 或 trace 保留进度。                             |
| 4   | Self-verifying loop        | 用确定性检查或 evaluator agent 阻止错误完成。                                 |
| 5   | Multi-agent loop           | discovery、implementation、review、judgment 由不同 agents 分工。         |
| 6   | Production-supervised loop | observability、budget、approval、rollback、human escalation 都是一等公民。 |

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
