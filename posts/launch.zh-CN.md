# Awesome Loop Engineering v0.6.0

Awesome Loop Engineering v0.6.0 进一步把项目升级为面向循环式 AI-agent 系统的领域指南和可验证数据产品。

当前集合包含 540 条资源，覆盖 prompt、context 与 harness engineering 之上的运行层：负责发现工作、分派任务、验证结果、持久化状态并决定下一步的系统。

## 本次版本包含

- 540 条链接到 canonical source 的审阅资源
- 15 个可操作的 loop patterns 与按问题选择的对比矩阵
- 15 个经过 schema 校验的 loop contracts
- 6 个适用于本地、定时、CI 与托管环境的可运行模板
- 可按目标、生命周期阶段、资源类型和证据类别筛选的交互式 Resource Atlas
- CSV 与 JSONL 数据导出，并同步到 Hugging Face Dataset
- 8 个语言入口

## 相比 v0.5.0 的变化

- 审阅资源数量从 509 条增加到 540 条。
- 逐条重新核对 canonical source：在 2026-07-17 的审计中，493 个公开来源可访问，4 个来源受访问限制，43 个为仓库原生材料，没有 broken 或 unreachable 来源。
- 新增明确的 trust 与 provenance 说明，覆盖编辑责任、自动化辅助、来源元数据、纠错、许可证和版本管理。
- 将 Hugging Face 上完整复制的 540 行超长 README 改为专门的数据集卡片，补充加载示例、适用场景、来源说明和局限，同时保留完整仓库与数据文件。
- 新增一致性检查，避免 README、网站、翻译、发布文案、social preview 源文件、release metadata 与生成数据集之间的数量漂移。
- Resource Atlas 的约 1 MB 索引改为接近该区域时再加载，并移除依赖滚动才显示的隐藏内容，让 deep link、打印、截图和辅助工具获得稳定页面。
- 修正 pull request 模板，要求填写作品原始发布平台和 primary-source metadata，而不是本仓库名称。
- 新增专门的 annotation correction 流程与明确的 review ownership。

## 为什么值得关注

Prompt engineering 改善你对模型说什么。Context engineering 改善模型能看到什么。Harness engineering 改善单次运行周围的工具、权限、沙箱和检查。

Loop Engineering 继续追问：什么系统应该定期或按事件启动，发现工作，加载持久上下文，在安全环境中执行，通过明确的 gate 验证，记录 receipts，并决定重复、报告、升级给人或停止？

目标不是无限自治，而是有边界、可审阅、由证据驱动的重复运行。

## 浏览与复用

- [浏览 Resource Atlas](https://chaoyue0307.github.io/awesome-loop-engineering/#resources)
- [使用 Hugging Face 数据集](https://huggingface.co/datasets/cy0307/awesome-loop-engineering)
- [查看 patterns 与 contracts](https://github.com/ChaoYue0307/awesome-loop-engineering#pattern-library)
- [运行模板](https://github.com/ChaoYue0307/awesome-loop-engineering/tree/main/examples/runnable)
- [查看 curation standard](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/meta/CURATION.md)
- [贡献资源或提交纠错](https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/CONTRIBUTING.md)

如果仓库对某篇引用工作的概括不够准确，或存在更可靠的 canonical source，请使用 annotation-correction form 或提交 pull request。

## 仓库

[github.com/ChaoYue0307/awesome-loop-engineering](https://github.com/ChaoYue0307/awesome-loop-engineering)
