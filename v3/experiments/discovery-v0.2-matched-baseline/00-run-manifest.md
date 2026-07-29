# ReaderLab Discovery v0.2｜运行卡与清单

状态：运行卡已冻结；本文件先于第一次真实语义调用写入。它只组织本次实验，不构成长期产品合同。

## 根目标

在同一章节、同一模型与推理配置、同一输出预算下，比较五次普通独立采样与五席专业入口是否产生不同的 `A_CORE` 召回；同时用事先封存的新观测承载门槛重筛 v0.1 的九个机制簇，并在揭盲后检查它对 C1/C5/C8 Expert 终局的预测有效性。

## 唯一处理差异

普通组只有共同任务与完整章节；专业组额外获得一个固定席位的知识方向卡。两组均最多输出 0—2 条种子，字段、预算、章节和当前默认模型／推理配置完全相同。不得读取其他运行、v0.1 Expert 输出或比较结果。

## Exact inputs

- 章节：`docs/expert-teaching-v0.1.2-migration-inputs/A/source.xhtml`；所有十次调用读取同一 SHA-256 字节。
- 普通组：共同任务 `control/plain-task.md`。
- 专业组：共同任务 `control/professional-task.md` + 对应唯一席位卡 `control/professional-seat-01.md`—`05.md`。
- 不提供作者观点摘要，不搜索，不提供 v0.1 候选、Expert 或最终报告。

## 共同输出合同

每条种子必须按任务中冻结的字段输出：Seed ID、组内运行编号、原文锚点、作者已提供的解释、外部知识对象、独立分析语法、预计生成剩余、连接依据、框架潜力、完成本章应用需要的关键观测、原文已经提供的观测、原文缺失的观测、当前可承诺的结果等级、记忆缺口。结果等级只能是：明确诊断／有依据的条件化判断／待核查假设／仅知识联想。Agent 不自评 A/B/C。

## 调用数与证据路径

- 固定真实语义调用：普通 5 次 + 专业 5 次 = 10 次；失败可重试同一次但必须保留失败证据。
- 原始候选区：`/private/tmp/readerlab-v0.2-matched-baseline-candidate/raw/`。
- 运行控制区：`/private/tmp/readerlab-v0.2-matched-baseline-candidate/control/`。
- 最终正式目录：`v3/experiments/discovery-v0.2-matched-baseline/`，完成字节／字段／来源／匿名化检查后排他 promotion。

## 停止点

完成 A 类重筛封存、十份 raw 可解析保存、匿名化、盲审聚类筛选、揭盲比较、预测有效性检查和用户验收索引后停止。禁止 Expert、Writer、Reader、外部搜索、生产流程修改、补跑任意额外样本。

## Blockers（最多三个）

1. v0.1 精确模型名、推理强度和运行配置未在可读控制材料中恢复，因此采用路径 B，不把新普通组与旧专业组写成严格匹配对照。
2. 当前 sub-agent API 不提供可证明的 OS 级隔离；通过 fresh context、最小白名单和禁止读取声明实现功能性输入隔离，不能声称安全沙箱。
3. 当前模型／推理的部署别名由宿主继承且未向主控暴露；十次调用统一继承同一当前默认配置，并在方法文件中标记精确别名为 unknown。

## 启动状态

- 原仓库：`/Users/tianqiang/GitHub/t512192641/readerlab`
- 独立 worktree：`/Users/tianqiang/GitHub/t512192641/readerlab-v0.2-matched-baseline`
- 分支：`review/discovery-v0.2-matched-baseline`
- 起始 HEAD：`d7f8e8cc404995e2e83d194155d7dd0e387768c6`
- 原工作区：存在大量既有未跟踪文件；未读取、未移动、未暂存。
- 当前调用配置：模型别名 `unknown`（继承当前默认）；推理强度 `unknown`（继承当前默认）；十次调用一致。
