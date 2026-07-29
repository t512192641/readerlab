# ReaderLab 当前执行切片

> owner：当前任务、run、停止点、允许动作、禁止动作与下一生产授权
> 更新日期：2026-07-29
> current-task: `taskcards/T2.40.md`
> current-run: `runs/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01`
> execution-status: `STOPPED_AFTER_SKILL_BOUNDARY_HARDENING`
> product-verdict: `unknown`
> product-verdict-source: `taskcards/T2.40.md`
> next-production-authorization: `none`
> governance-status: `DIAGNOSTIC_EXPERT_TEACHING_SKILL_HARDENING`

## 当前目标

根据外部 Code Review，把已经验证的 Expert Teaching 控制能力修正为可复验的
`readerlab-book-expert-teaching` Skill v0.1.1 候选：保留不可变的 0.1.0 根实现，增加明确版本共存入口、
结构化来源允许列表、稳定中文表达合同、精确内容泄露门和全 hash mechanical replay。T2.38 只作机械回放
fixture，不产生新语义结果；0.1.0 与 0.1.1 结果不得静默混算。

`current-run` 仅指向该只读 fixture，以保持项目状态入口的 canonical target；本轮没有创建新的语义 run。

## 当前允许

- 只执行 `taskcards/T2.40.md` 预注册的版本化 Skill 实现、Skill-local tests、T2.38 mechanical replay、
  repository active tests、确定性验证、文档状态同步、提交与推送。

## 当前禁止

- 不修改 `PRODUCT-DECISIONS.md`、`contracts/BOOK-CONTENT-FLOW-v2.md`、历史判词或 T2.36/T2.37/T2.38/T2.39 冻结产物。
- 不搜索替换 C、不比较 D／ABC、不生成 B、不发明 M1/M2/M3、不增加 Judge／知识库／生产架构。
- 不启动语义 Agent、Writer、ABC、Discovery、迁移样本或完整 orchestrator；不调用真实语义模型；不把 Skill
  候选声明为 integrated 或 accepted 的生产能力。
- Skill 只允许固定输入、结构化来源白名单、隔离任务生成、双门停止、产品包、全 hash replay 和 archive
  的确定性控制。

## 停止点

- 已完成 Skill v0.1.1 边界 hardening；0.1.0 根实现保持不可变，0.1.1 只在独立目录中修改。
- 按本卡停止，不运行迁移样本；`integrated`: `not_integrated`；`accepted`: `unknown`；下一生产授权保持
  `none`。
