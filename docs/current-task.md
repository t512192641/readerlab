# ReaderLab 当前执行切片

> owner：当前任务、run、停止点、允许动作、禁止动作与下一生产授权
> 更新日期：2026-07-29
> current-task: `taskcards/T2.41.md`
> current-run: `runs/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01`
> execution-status: `STOPPED_AFTER_012_VERIFICATION`
> product-verdict: `unknown`
> product-verdict-source: `taskcards/T2.41.md`
> next-production-authorization: `none`
> governance-status: `DIAGNOSTIC_EXPERT_TEACHING_SKILL_HARDENING`

## 当前目标

完成 0.1.2 的迁移前工程边界修正：保留不可变的 0.1.0 根实现和独立 0.1.1，新增独立 0.1.2、根目录
current dispatcher、source-access 回执和 source-map／allowlist 闭合摘要。T2.38 只作带显式访问回执的机械
回放 fixture，不产生新语义结果；0.1.0、0.1.1 与 0.1.2 结果不得静默混算。

`current-run` 仅指向该只读 fixture，以保持项目状态入口的 canonical target；本轮没有创建新的语义 run。

## 当前允许

- 只执行 `taskcards/T2.41.md` 预注册的版本化 Skill 实现、Skill-local tests、T2.38 mechanical replay、
  repository active tests、确定性验证、文档状态同步、提交与推送。

## 当前禁止

- 不修改 `PRODUCT-DECISIONS.md`、`contracts/BOOK-CONTENT-FLOW-v2.md`、历史判词或 T2.36/T2.37/T2.38/T2.39 冻结产物。
- 不搜索替换 C、不比较 D／ABC、不生成 B、不发明 M1/M2/M3、不增加 Judge／知识库／生产架构。
- 不启动语义 Agent、Writer、ABC、Discovery、迁移样本或完整 orchestrator；不调用真实语义模型；不把 Skill
  候选声明为 integrated 或 accepted 的生产能力。
- Skill 只允许固定输入、结构化来源白名单、闭合 source boundary、隔离任务生成、双门停止、访问回执、产品包、全 hash replay 和 archive
  的确定性控制。

## 停止点

- 已完成 Skill v0.1.2 边界 hardening、发布基线 0.1.0 历史入口版本隔离测试、quick／Skill-local／replay／diff／敏感信息检查；repository active tests
  35/36 通过，唯一失败为本轮开始前已存在且未登记的 Markdown 影子文件穷举项。提交与推送后停止。
- 按本卡停止，不运行迁移样本；`integrated`: `not_integrated`；`accepted`: `unknown`；下一生产授权保持
  `none`。
