# ReaderLab

ReaderLab 的终极交付是两条独立、成熟、可复用的 Skill 能力：

- 图书解读：保留作者完整原文，在真正值得停下的位置提供高质量认知增量；
- Skills 包解读：把 Skills 包转换为产品负责人能看懂、无背景 Agent 能复用的中文资料。

两条线只共享材料身份、范围、冻结、证据、成本与故障恢复等薄工程骨架，不共用错误的
语义标准。

## 当前从哪里开始

1. 项目边界与工作规则：[`AGENTS.md`](AGENTS.md)
2. 产品目标与固定责任：[`PRODUCT-DECISIONS.md`](PRODUCT-DECISIONS.md)
3. 已确认的工程教训：[`ENGINEERING-LESSONS.md`](ENGINEERING-LESSONS.md)
4. 两条产品线的长期地图：[`blueprints/PIPELINE-MAP.md`](blueprints/PIPELINE-MAP.md)
5. 当前任务、停止点与允许动作：[`CURRENT-STATE.md`](CURRENT-STATE.md)

`CURRENT-STATE.md` 是唯一当前执行状态 owner。若它与真实任务卡、run、产品判词或 Git
现场冲突，应停止派发下一阶段并先由执行现场同步状态。

## 工程与审计入口

- 当前确定性测试：`python3 -B tests/entry.py`
- run 创建、promotion、冻结与复核：`python3 -B tools/run.py --help`
- 审计运行机制：[`audit/AUDIT-OPERATING-MODEL.md`](audit/AUDIT-OPERATING-MODEL.md)
- 开放问题与行动门：[`audit/FINDINGS-REGISTER.md`](audit/FINDINGS-REGISTER.md)
- 资产生命周期与保留清单：[`audit/ASSET-LIFECYCLE-REGISTER.md`](audit/ASSET-LIFECYCLE-REGISTER.md)
- 工程事故与防复发状态：[`audit/INCIDENT-GUARDRAILS.md`](audit/INCIDENT-GUARDRAILS.md)

早期 clean-seed validator 和已经失效的 T2.26 历史脚本／测试均已从当前工作树删除；
需要取证时可从本地 Git 提交 `c13ea5a` 恢复。

## 历史内容

原 README 的 2026-07-22 历史交接正文仍可从本地 Git 提交
`b39a284c10e09ad03b9af8b4899aea34f9b64dc1` 完整恢复。历史任务卡、run、旧合同和路线文档
只用于追溯，不能授权当前执行；它们的生命周期与保留规则见资产清单。

本项目与任何旧 ReaderLab 项目隔离。缺失事实标为 `unknown`，不得回旧项目补取。
