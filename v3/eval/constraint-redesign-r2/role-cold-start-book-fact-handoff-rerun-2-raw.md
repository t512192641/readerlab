# 图书事实 Handoff 全 0 候选路径专项复核原始输出

## 复核边界

- 时间：`2026-07-10T07:57:27-04:00`。
- 本次只复核：三个 cognition-candidate 实例全为 0 时，fact-checker skipped、cognition-judge 继续运行并以合法 0 报告结算 absolute_value pass / selection_count 0 的路径。
- 本次读取：`cognition-candidate.md`、`cognition-judge.md`、`orchestrator.md`、`run-manifest.md`、`book-engine.md`，以及 constraint / roles README 的无早停 11、skipped、actual_tasks 条款。
- 有候选路径不重新验收，只确认本次修订未改其合同入口。
- 旧 book handoff raw 全部保留不改；本次不修改规则文件。
- 上下文声明：本执行者做过前两轮图书事实 handoff；本次不是零上下文，但 verdict 只依据当前全 0 路径条款。

## 总结结论

- scoped overall verdict：`pass`。
- 全 0 路径现已闭合：三个候选实例各自提交合法 0 报告和 request n/a；fact-checker 因无 required requests skipped；cognition-judge 仍接收三份 0 报告、锚点证据并执行盲区检查；无盲区时以 status pass、selection_count 0 结算 absolute_value pass。
- 11 是无早停计划，不是实际任务配额；fact-checker skipped 不计 actual_tasks，judge 因有 0 报告与锚点输入仍是实际执行任务。
- 本次只证明静态路径闭合，不证明真实三实例 0 run 已执行。

## 1. 三个实例的合法 0 报告

- 每个 cognition-candidate 实例仍独立运行并保留 instance_id 1 / 2 / 3。
- 每个实例 candidates 为空时：
  - `request_id: none`
  - `status: not-applicable`
  - `zero_candidate_reason: no-defensible-cognition`
- verdict：`pass`。
- 判断：0 候选不是缺失输出，而是三个可审计的合法 0 报告；主控可以证明三实例都实际完成判断，而非漏跑。

## 2. Fact-checker skipped

- 触发条件：主控只汇集 required requests；三个实例全为 0 时 required request 集合为空。
- dispatch：fact-checker 标 `skipped`，写入 `stages.skipped`，不生成空核查结果。
- verification：`conditional_fact_check.status: not-applicable`，`request_refs: []`。
- budget：skipped dispatch 不计 `actual_tasks`，不能为凑无早停计划 11 伪造空任务。
- verdict：`pass`。
- 判断：fact-checker 的 skipped、manifest stages、条件子门和预算计数一致。

## 3. Cognition-judge 仍运行

- 输入：三个实例的合法 0 候选报告、各自 zero_candidate_reason、归并后的锚点证据；事实核查 requests / results 在本路径不适用。
- cognition-judge 明确要求：即使三实例全 0，也必须运行，核对三份 0 报告、锚点和盲区，确认没有漏掉可形成完整认知的关键问题。
- 输出：
  - `batch_gap_check.status: pass`
  - `status: pass`
  - `selection_count: 0`
  - `zero_accept_reason: no-qualified-candidates`
- verdict：`pass`。
- 判断：judge 不是“无输入下游”。它有三份 0 报告与锚点证据，承担独立盲区检查，因此必须执行而不能 skipped。
- 若发现关键遗漏：batch_gap_check blocked 并定向退回 cognition-candidate；不能用合法 0 绕过盲区。

## 4. Absolute value 与整门状态

- cognition-judge 实际运行且 status pass，因此 manifest `verification.absolute_value: pass` 有真实角色证据，不需要新增 not-applicable。
- source_and_fact：source provenance 仍须 pass；conditional fact check 因无 requests 为 not-applicable；聚合门可 pass。
- run accepted：absolute_value 不再停留 not-run；只要其他适用门、预算和 claims 也满足，0 陪读单元不阻止 accepted。
- verdict：`pass`。
- 判断：上一轮唯一 blocker 已关闭；0 候选是合法产品结果，不等于绝对价值门未执行。

## 5. 无早停计划与实际任务数

- 图书 11：仅表示无早停标准计划。
- 全 0 本路径：三个 candidate 任务与 cognition-judge 实际执行；fact-checker skipped；其后无输入的成文 / 冷读 dispatch 可按各自输入条件 skipped。
- `actual_tasks`：只计实际执行，允许少于 11；skipped 不计。
- verdict：`pass`。
- 判断：计划实例数、事实核查跳过和裁判必跑不再冲突，也不会为了展示“11 个任务完成”制造空核查。

## 6. 有候选路径未受破坏

- 至少一份 required request 时，fact-checker 仍执行批量核查；cognition-judge 仍按 request / check / claim 逐候选判断。
- 本轮新增的全 0 judge 输入分支没有改变非空路径的字段、枚举或顺序。
- verdict：`pass`（兼容性确认，不是重新完整验收）。

## 路径摘要

```text
3 x cognition-candidate executed
  -> 3 x legal zero report
  -> 0 required fact requests
  -> fact-checker skipped / conditional fact N/A
  -> cognition-judge executed with zero reports + anchors
  -> blind-spot check pass
  -> absolute_value pass / selection_count 0
  -> body-only delivery remains eligible for later gates
```

## 最终可声称范围

- 可以声称：三实例全 0 的 fact-checker skipped、judge 必跑、absolute_value pass、selection_count 0 和 actual_tasks 减计路径已静态闭合。
- 不可以仅凭本文件声称：真实三实例已返回 0、盲区检查已实际通过、完整图书 run 或 ReaderLab 流水线已 accepted。

最终 scoped overall verdict：`pass`。
