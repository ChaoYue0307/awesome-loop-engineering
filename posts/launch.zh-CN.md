# Awesome Loop Engineering v0.10.0

Awesome Loop Engineering v0.9.0 建立了一张从模型内部递归、Agent 执行、Harness 到外层运行系统的完整地图。

可浏览 974 篇论文、官方文档、工具、benchmark 与实践指南，同时保持清晰边界：模型内的循环提供自适应计算，但不等于具备外部验证、持久状态、预算、人类交接与退出规则的运行级 Loop。

## 可直接使用

- 974 篇论文、官方文档、工具、benchmark 与实践指南，并直接链接原始来源
- 29 个模型层资源，覆盖 Universal Transformers、Huginn、Loopie、LoopCoder、LoopWM 等方向
- 20 个按 build、operate、optimize、govern 组织的 operational patterns
- 20 个经过 schema 校验的 loop contracts，每个 pattern 对应一个
- 8 个 runtime starters：3 个轻量级可执行程序与 5 个可复制改造的 runtime 模板
- 可按目标、Loop 层级、生命周期、资源类型和证据类别筛选的交互式 Resource Atlas
- 包含 50 个字段的 CSV、JSONL 与 Parquet 数据，并同步到 Hugging Face Dataset
- 8 个语言入口

## v0.9.0 的更新

- 新增 Loopie，并补充 21 项相关工作，覆盖模型递归、Agent 工作流、验证、安全、记忆、编排、评测与运行。
- 将 Model-Level Recurrence 扩展到 29 个资源，纳入稀疏 MoE 递归、fixed-point stopping 与机理分析，并接入 Awesome Loop Models 作为更深的架构索引。
- 为每条数据新增 `loop_layer` 与 `scope_fit`，避免将模型递归误标为完整的运行级 Loop Engineering。
- 在 Resource Atlas 中新增模型到运维的层级图与 Loop 层级筛选器。
- 新增跨层评测方案，用匹配算力和成本的实验比较模型内部递归与外部证据驱动重试。
- 检查全部 669 个来源链接，并刷新所有 arXiv 论文的会议或期刊发表状态。
- 同步更新网站、social preview、翻译、release metadata 与 Hugging Face Dataset。

## 为什么值得关注

“Loop”可以发生在不同层级：模型内部可以重复隐状态计算，Agent 可以在单个任务中交替调用推理与工具，运行系统则可以跨时间重复经验证的工作。它们彼此相关，但状态、停止规则、证据与风险并不相同。

v0.9.0 将这些层级连接起来：

1. 当问题是自适应深度与隐式计算时，研究模型递归。
1. 当问题是任务内的推理、工具、上下文与验证时，研究 Agent 与 Harness。
1. 当工作需要跨事件、会话或时间重复时，使用 operational pattern 与 Loop Contract。
1. 用外部证据、持久状态、硬预算与 human escalation 管理真实世界中的重复执行。

每次运行都应留下可审查的凭证（receipts），让下一轮和 human owner 能判断发生了什么、哪些 gate 已通过，以及为什么继续、升级或停止。

目标仍然不是无限自治，而是有边界、可审阅、由证据驱动的重复运行。

## 浏览与复用

- [浏览 Resource Atlas](https://chaoyue0307.github.io/awesome-loop-engineering/#resources)
- [选择 operational pattern](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/patterns/README.md)
- [改造经 schema 校验的 contract](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/examples/README.md)
- [运行 starter](https://github.com/ChaoYue0307/awesome-loop-engineering/tree/main/examples/runnable)
- [使用 Hugging Face 数据集](https://huggingface.co/datasets/cy0307/awesome-loop-engineering)
- [贡献资源或提交纠错](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/CONTRIBUTING.md)

如果某条概括不够准确，或存在更可靠的原始或官方来源，请使用 annotation-correction form 或提交 pull request。

## 打开 Field Guide

[github.com/ChaoYue0307/awesome-loop-engineering](https://github.com/ChaoYue0307/awesome-loop-engineering)
