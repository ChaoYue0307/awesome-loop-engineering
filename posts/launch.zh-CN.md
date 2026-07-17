# Awesome Loop Engineering v0.7.0

Awesome Loop Engineering v0.7.0 把 implementation kit 整理成一条清晰路径：从真实的重复性问题出发，选择 pattern，改造经校验的 contract，再接入可运行的 runtime starter。

可浏览 545 条经审核资源，理解 prompt、context 与 harness engineering 之上的运行层：如何发现工作、分派任务、验证结果、持久化状态并决定下一步。

## 可直接使用

- 545 条链接到 canonical source 的审阅资源
- 20 个按 build、operate、optimize、govern 组织的 operational patterns
- 20 个经过 schema 校验的 loop contracts，每个 pattern 对应一个
- 8 个 runtime starters：3 个轻量级可执行程序与 5 个可复制改造的 runtime 模板
- 可按目标、生命周期、资源类型和证据类别筛选的交互式 Resource Atlas
- CSV 与 JSONL 数据导出，并同步到 Hugging Face Dataset
- 8 个语言入口

## 相比 v0.6.0 的变化

- 新增五个边界清晰的 patterns：benchmark optimization、accessibility regression、knowledge freshness、performance regression，以及经过授权的 adversarial red teaming。
- 为每个新 pattern 增加 schema-valid contract 与完整 use case。
- 将 pattern library 重组为四个运行领域，并明确每个问题对应的可验证结果，以及相似 loops 之间的选择边界。
- 将 contract catalog 改造成面向实现者的对照表：何时使用、如何触发、哪个 deterministic gate 判定完成、什么 receipt 会持久化。
- 新增四条端到端路径，覆盖 CI repair、knowledge refresh、queue processing 与只读 threshold monitoring。
- 新增两个可执行 starter：具备幂等状态的 JSONL queue worker，以及带有限轮询与证据升级的只读 threshold monitor。
- 明确 starter library 由 3 个可执行程序与 5 个 runtime 模板组成，不再把每个文档都描述成独立可执行程序。
- 同步更新网站、social preview、翻译、release metadata 与 Hugging Face Dataset。

## 为什么值得关注

只有当证据能导向可审阅的实现时，它才真正有用。

v0.7.0 的路径是：

1. 明确重复性问题。
1. 选择 operational pattern。
1. 改造对应的 validated contract。
1. 选择 runtime starter。
1. 用外部证据、持久状态、硬预算与 human escalation 管理整个 loop。

目标仍然不是无限自治，而是有边界、可审阅、由证据驱动的重复运行。

## 浏览与复用

- [浏览 Resource Atlas](https://chaoyue0307.github.io/awesome-loop-engineering/#resources)
- [选择 operational pattern](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/patterns/README.md)
- [改造 validated contract](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/examples/README.md)
- [运行 starter](https://github.com/ChaoYue0307/awesome-loop-engineering/tree/main/examples/runnable)
- [使用 Hugging Face 数据集](https://huggingface.co/datasets/cy0307/awesome-loop-engineering)
- [贡献资源或提交纠错](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/CONTRIBUTING.md)

如果某条概括不够准确，或存在更可靠的 canonical source，请使用 annotation-correction form 或提交 pull request。

## 打开 Field Guide

[github.com/ChaoYue0307/awesome-loop-engineering](https://github.com/ChaoYue0307/awesome-loop-engineering)
