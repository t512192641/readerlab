# 图书事实 Handoff 三个 Blocker 修订后复核原始输出

## 复核边界

- 时间：`2026-07-10T07:55:12-04:00`。
- 本次复核上一份 raw 的三个 blocker：单实例 0 候选与三实例总 0 skipped；批量 overall 与逐候选淘汰分离；kind / assertion_type / materiality 逐字段无损。
- 本次读取：`cognition-candidate.md`、`fact-checker.md`、`cognition-judge.md`、`orchestrator.md`、`run-manifest.md`、`book-engine.md`，以及补充指定的 `constraint-architecture.md`、`roles/README.md` 中无早停 11 / skipped / actual_tasks 条款。
- 上一份失败 raw 保留不改；本次不修改规则文件。
- 上下文声明：本执行者做过上一轮图书事实 handoff；本次不是零上下文，但 verdict 只依据当前指定条款重新判断。

## 总结结论

- overall verdict：`fail`。
- 已修复两项：批量 fact-checker overall 现在只表示核查任务完整性，坏事实交给 judge 逐候选淘汰；kind、assertion_type、materiality 也明确逐字段相等。
- 0 候选生产与 dispatch 规则大部分已修复：单实例 0 用 request n/a，主控只收 required requests；三实例全 0 才把无输入下游 skipped；actual_tasks 不凑 11。
- 仍有一个 gate blocker：补充条款明确三实例全 0 时无输入下游 dispatch skipped，包含没有输入的认知裁判；但 manifest `absolute_value` 没有 `not-applicable`，只有 `not-run | pass | fail | blocked`。accepted 又要求不适用门明确 not-applicable。全 0 路径无法同时表达 judge skipped、absolute_value 合法状态与 run accepted。
- 按“任何缺口 fail”，本次仍不能通过。

## 1. 单实例 0 candidate request

- 当前 schema：`request_id: none | nonempty-unique-id`，`status: not-applicable | required`。
- 当前规则：
  - 有候选：required，列全必要证据；
  - 单实例 0：none + not-applicable；
  - 主控只汇集 required requests。
- verdict：`pass`。
- 判断：上轮“request 永远 required，0 候选无合法结构化输出”的冲突已关闭。一个实例为 0 不会阻断其他两个实例的 requests，也不会伪造空 request。

## 2. 三实例总 0 才 skipped

- 当前角色规则：三个实例全为 0 才把 fact-checker skipped。
- book-engine：至少一份 required request 时才运行单一批量 fact-checker。
- constraint / README：11 是无早停标准计划；合法 0 候选时，无输入下游 dispatch 记 skipped，actual_tasks 只计实际执行，不能为凑 11 伪造空任务。
- verdict：`partial`。
- dispatch 与预算已闭合：
  - 一零两非零：fact-checker 运行，request_refs 只含两份 required request；
  - 三实例全零：fact-checker 及其他无输入下游 skipped，写入 stages.skipped；
  - skipped 不计 actual_tasks，实际任务数可小于 11。
- gate 仍未闭合：
  - conditional_fact_check 可合法写 `not-applicable + request_refs: []`；
  - cold_read 也有 not-applicable；
  - 但 absolute_value 只有 `not-run | pass | fail | blocked`，没有 not-applicable。
- 直接冲突：全 0 时 cognition-judge 无输入按补充条款 skipped，不能把未执行 judge 写成 pass；若写 not-run，manifest accepted 又要求所有不适用门明确 not-applicable。当前没有合法值。
- 最小剩余修复：为 `absolute_value` 增加 not-applicable，并明确仅在“三实例总候选 0、认知裁判无输入 skipped”时使用；或者规定即使总候选 0，cognition-judge 仍必须运行盲区检查并以 pass + selection_count 0 结算，不能同时说它是无输入下游 skipped。两种路径必须只留一种。

## 3. Batch overall 表示任务完整性

- 当前 fact-checker pass 条件：
  - 输入 required request 集合精确匹配；
  - 每个 request coverage 完整；
  - 每项得到合法 verdict；
  - 未把不合格证据误标 supported。
- conflicted / insufficient / out_of_scope：作为逐候选淘汰证据，不拖死同批其他候选。
- cognition-judge：任一候选可见事实非 supported，只淘汰该候选，不让其他候选或核查任务一起失败。
- book-engine：事实核查任务完整执行可 pass，坏候选由裁判淘汰。
- verdict：`pass`。
- 判断：上轮“一个坏候选 -> fact-checker overall fail -> source_and_fact fail -> 整 run 失败”的冲突已关闭。overall 现在表示批处理执行质量，不再冒充候选内容全通过。
- 与主控映射：overall pass 可映射 conditional_fact_check pass；候选级事实 verdict 仍由 judge 决定 accept / reject / blocked。
- 边界：来源不可访问到无法判定仍可让任务 blocked；coverage / schema 不完整仍可 fail。这些是执行失败，不是候选质量失败，区分合理。

## 4. Kind / assertion_type / materiality 无损

- request 与 check 均使用：
  - `kind: source-internal | external`
  - `assertion_type: factual | causal`
  - `materiality: material | non-material`
- fact-checker 明确规定三字段必须与原 claim 相同。
- verdict：`pass`。
- 判断：上轮 materiality 改名 conclusion_impact 的问题已关闭；事实核查者不能静默改变因果类型、来源类型或结论重要性。
- judge 通过 request_id + check_id + claim_id 引用完整 check，因此三字段无需在 verdict 中重复也可无损追溯。

## 5. 0 候选与 0 接受的区分

- 生产总候选 0：按 constraint / README 走无输入下游 skipped，actual_tasks 减少。
- 有候选但 judge 最终 0 接受：fact-checker 与 judge 正常执行；judge 用 `selection_count: 0 + zero_accept_reason: no-qualified-candidates`，读者页只交正文。
- verdict：语义区分 `pass`；gate 状态 `fail`。
- 判断：两个“0”不再混淆，前者是早停，后者是合法淘汰结果。但前者的 absolute_value 状态仍无合法 not-applicable 表达，因此完整 run 状态未闭合。

## 三项修复矩阵

| 上轮 blocker | rerun verdict | 结论 |
| --- | --- | --- |
| 单实例 0 n/a；三实例总 0 才 skipped | `partial` | request / dispatch / actual_tasks 已闭合；absolute_value gate 缺 N/A。 |
| batch overall 与逐候选淘汰分离 | `pass` | 执行完整性与候选事实质量已分层。 |
| kind / assertion_type / materiality 相等 | `pass` | 三字段同名同枚举，并有相等不变量。 |

## 最终可声称范围

- 可以声称：0 request 的实例级表达、required requests 汇集、三实例总 0 早停、actual_tasks 不凑数、批量任务与候选淘汰分离、三类字段无损均已实质修复。
- 不可以声称：三实例总 0 的完整 verification / accepted 路径闭合，或图书事实 handoff 已通过冷启动。

最终 overall verdict：`fail`。
