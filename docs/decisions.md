# ReaderLab 持久决定索引

## D-MEM-001 · 采用标准 MEM 分层

- 状态：`active`
- 日期：2026-07-25
- 决定：`docs/current-task.md` 唯一拥有当前执行切片；`docs/dev-state.md` 唯一拥有当前已验证
  工程事实与缺口；`CURRENT-STATE.md` 只作为兼容入口，不再拥有动态字段。
- 原因：避免把同一状态平行复制到自定义状态页和标准 MEM 层，重新制造双 owner。
- 后果：新会话从 `AGENTS.md`、`docs/current-task.md`、`docs/dev-state.md` 冷启动；运行历史、
  持久决定和外部研究分别按 MEM 固定层维护。
- 替代关系：取代“`CURRENT-STATE.md` 直接拥有全部当前状态”的项目内历史约定；历史报告和
  审计事实保留原表述，不反向改写。

## 既有权威入口

- 产品目标与长期责任仍只由 `PRODUCT-DECISIONS.md` 拥有。
- 历史工程观察与失败边界仍只由 `ENGINEERING-LESSONS.md` 拥有。
- 长期派生架构仍由 `blueprints/PIPELINE-MAP.md` 呈现。
- 审计节奏与问题状态分别由 `audit/AUDIT-OPERATING-MODEL.md` 和
  `audit/FINDINGS-REGISTER.md` 拥有。

## D-MEM-002 · 完整审阅包默认本地保留

- 状态：`active`
- 日期：2026-07-25
- 决定：完整原文、Expert、知识卡、来源审核和完整审阅包默认由 Git 忽略；主仓库只保存
  manifest、freeze、gate、产品判词等小型控制证据。
- 云端例外：确需云端模型审核时，由产品负责人按任务单独授权准确材料、外部目的地与保留
  边界；该授权不得恢复通用文件名放行，也不自动授权 push 或其他外部写入。
- 原因：早期 `acceptance-report.md` 多为小型结论报告，T2.35 首次用同名文件承载完整原文
  审阅包；按文件名永久放行无法表达数据边界。
- 验证：`.gitignore` 与 `tests/test_run_promotion.py` 的 Git policy 回归。

## D-ENG-001 · 网络能力与本地读取闭集分开治理

- 状态：`active`
- 日期：2026-07-25
- 决定：生产 Expert 默认可以使用 `Web Search + Web Fetch`；只有闭卷资格考试、因果实验或
  任务卡另有明确理由时才禁网。本地 read set 是角色合同和上下文层的功能性闭集，禁止越界读取并
  在发生时记控制失败，但不得宣称拥有 OS 级“物理上读不到”保证。
- 工具边界：Chrome remote debugging、浏览器自动化与已卸载的 `web-access` 继续默认禁止；
  这是稳定性和可审计性边界，不是默认断网政策。
- 原因：T2.33 的 46 分钟 Chrome 死锁证明了工具路线不稳定；T2.34 preflight 又证明把特定实验的
  断网要求外推为长期生产政策，会把不存在的物理隔离能力写成执行前置，并与最终 Skill 的宿主能力
  冲突。
- 证据与现行实现：`taskcards/TEMPLATE.md` 的工具政策、`taskcards/T2.34.md` 第 13—14 节的
  历史控制失败与政策校正记录。

## D-ENG-002 · 原始证据优先与总控执行熔断

- 状态：`active`
- 日期：2026-07-26
- 决定：独立 Writer／Discovery 线使用独立小组长、队列和执行优先级；每轮只以一页运行卡中
  不超过三个 blocker 阻止原始调用。授权后 30 分钟仍无一对可保存、可解析的真实 smoke
  evidence 时，停止新增前置工程并执行最小 pair，或提交可复现 blocker。
- 责任边界：可以预先冻结假设、产品判据与解盲规则；Normalizer、模型 Judge、Clusterer、
  Verifier、成本系统、schema 套件或 promotion gate 的实现完成度不得成为 Scout 原始证据的
  默认启动条件。总控只在启动、smoke、完成包三个检查点管理小组长和独立验收，不直接承担组内
  语义创作或实现微调。
- 原因：2026-07-26 Discovery treatment-isolation 运行在约一小时前置扩建后仍无正式 Scout；
  产品负责人收缩到三项 blocker 后，18 次真实调用约 20 分 38 秒完成。独立审计确认原始证据可
  进入内容审阅，并确认“共享队列相互干扰、前置实现膨胀、总控角色下沉”的主诊断；包内不能证明
  Writer 单向阻塞 Discovery，后续只能按并发日志认定实际方向。
- 证据：`/Users/tianqiang/Downloads/ReaderLab_Discovery_Execution_Controller_Independent_Audit_20260726.md`；
  原始 sidecar 报告位于
  `/private/tmp/readerlab-new-route-20260726/discovery-isolation/checkpoint-b/evidence/`。
- 后果：未列 blocker 只能记 limitation／backlog；冻结后修改 Prompt、schema、harness 或语义
  内容必须新版本并形成 change receipt，受影响结果不得与旧版本静默混算。

本索引不复制其他 owner 的正文；只有新的持久工程决定才在此追加编号。
