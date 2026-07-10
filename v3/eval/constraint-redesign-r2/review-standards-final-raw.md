# ReaderLab V3 约束重构最终 Standards 验收原始输出

## 审查身份与边界

- reviewed_at: `2026-07-10T11:58:01-04:00`
- fixed_point: `1ed34c474bd2b84a9ed164a59810506b8fa2b4aa`
- current_branch: `v3/cognitive-compounding`
- axis: `Standards`
- verdict_policy: `any blocker => fail`
- rules_or_cases_modified_by_reviewer: `false`
- real_fresh_or_revision_run_observed: `false`

本次按 `v3/current-task.md` 审查当前工作区相对 fixed point 的全部相关改动，重点核对图书类型化 request、批量事实核查、逐候选淘汰、全 0 路径与无早停 11；Skill 条件事实链；角色图、状态、schema 与 manifest；29 张回归卡和最新 RI rerun-8；引用、行数、角色裁剪、模板、document map、dirty boundary 与 `git diff --check`。本执行者没有修改规则、case 或汇总文件，只写本原始审查结果。

## 结论

```yaml
axis: Standards
verdict: fail
blockers: 3
non_blocking_issues: 0
regression_cards_present: 29
latest_ri_result_read: 7/7-derived-structure-only
runtime: not-run
```

图书与 Skill 的类型化事实链、RI-P01 rerun-8、29 张逐 case 卡和大部分机械约束已经闭合，但仍有三个 Standards blocker：manifest 与 orchestrator 的非来源事实门 schema 不是同形；全 0 路径最新 pass raw 错误跳过了仍有输入和职责的 writer / cold-reader；document map 的三类身份存在重叠。任何 blocker 必须 fail，因此不能把本轮标为 Standards 通过，也不能进入 Demo。

## 1. 图书 typed request、批量核查与逐候选淘汰

结果：`pass`。

- `cognition-candidate.md` 的每个实例输出统一 `fact_check_request`；有候选时 request / claim id 非空唯一，并列全必要的源内、外部、事实与因果断言；0 候选时有明确 `not-applicable` 与 `zero_candidate_reason`。
- `fact-checker.md` 可在一个任务中接收一份或多份 request；`request_ids` 精确等于输入 required request 集合，逐 claim 生成稳定 check id，并以集合精确相等证明每个 request 的 coverage。
- 外部事实只有本次定位核实的 high-trust 来源才可 `supported`；kind、assertion type、materiality 与原 claim 保持一致。
- `cognition-judge.md` 逐 candidate 回接 request / check / claim。任一可见事实不是 `supported` 时只淘汰受影响候选，不拖死同批其他候选，也不把 fact-checker 已完整执行误记为任务失败。
- RI-P01 的三份 request 均有 `trigger_reason`、明确外部授权边界；三条 check 均有 `minimal_correction`，批次有 `overall / blocked_reason / return_to`。最新 `regression-run-integrity-rerun-8-raw.md` 对这部分的 `accept-structure-only` 与当前合同一致。

可声称范围仅为静态 handoff 和派生 fixture 自洽；没有真实来源核实或 Agent 执行。

## 2. Skill 条件事实链

结果：`pass`。

- 标准 Skill 链有来源整合、机制候选、独立裁判、单一成文、独立冷读/冷启动/复现 5 个所有者；简单材料只能在保持生产与独立验收分离时降到 3—4。
- mechanism auditor 在没有外部事实时明确 `not-applicable`；出现可见外部事实时必须生成 required request，列全事实且提供取证边界。
- 主控只能按上游 request 派发共用 fact-checker，不能临时猜测核查范围；Skill judge 在独立裁判前逐 check id 验证完整覆盖。
- source integrator 的逐单元 schema 包含 retained / moved / merged / reordered、实际 treatment，以及重要删除的理由和 destination。
- Skill writer 保持净化正文不变；独立读者把阅读体验与冷启动/复现结果分开。

该结果只证明当前静态合同链闭合，不证明 Skill 线、`gstack/browse` 或真实复现通过。

## 3. 图书角色图、盲区和 11 任务

结果：`pass_with_blocker_B02_in_zero_path_evidence`。

- 无早停标准计划为 11：source map 1、anchor nomination 2、merge 1、candidate 3、fact-checker 1、judge 1、writer 1、cold-reader 1；主控不计入，盲区检查并入 judge。
- 锚点提名合同包含 `likely_shallow_or_wrong_reading` 与 `investigation_question`；归并保留调查问题并可定向退回。
- 三个 candidate 实例全为 0 时，fact-checker 可以 skipped；judge 仍须读取三份合法 0 报告和锚点，运行盲区检查并把 absolute value 结算为 pass / selection count 0。
- 11 是无早停计划，不是实际任务配额；skipped 不计 `actual_tasks`。

角色本体足以表达正确路径，但最新全 0 专项 raw 对 judge 之后的任务给出了错误结论，详见 B02。

## 4. Blocker B01：orchestrator 与 manifest 的 verification schema 不同形

结果：`fail`。

### 冲突

- `run-manifest.md:55-69` 只有 `source_and_fact` 是含 owner、scope、evidence、conflicts 的对象；`absolute_value`、`regression`、`cold_read`、`cold_start_or_reproduction`、`run_integrity` 和 `user_experience` 都只是状态标量。
- `orchestrator.md:29-36` 的同名六个门却全部是对象，并新增 `owner / scope / evidence / conflicts`。
- `orchestrator.md:40` 又要求整个 `verification` 与同一 manifest “完全一致，不得作为第二事实源”。当前对象无法逐字段写入 manifest 的同名标量，也没有权威的投影或派生规则。

### 影响

- 主控无法按自己的合同同时保存 gate owner、范围、证据和冲突并满足唯一 manifest 事实源。
- 除 `source_and_fact` 外，manifest 不能无损承载独立裁判、回归、冷读、复现和运行完整性的验收证据；后续执行者只能建立合同外影子记录，或丢失字段。
- RI-P01 只填写 manifest 标量，因此不能证明 orchestrator 的完整 `verification` 对象可持久化；rerun-8 没有关闭这处跨文件 schema 冲突。

### 最小解除条件

让 manifest 的所有 verification gates 与 orchestrator 同形，或把 orchestrator 明确定义为从 manifest 与证据引用确定性派生的非持久化视图，并给出逐字段投影规则；修后重新做主控冷启动。

## 5. Blocker B02：全 0 专项 pass raw 错误跳过 writer / cold-reader

结果：`fail`。

### 冲突

- `role-cold-start-book-fact-handoff-rerun-2-raw.md:61-65` 声称全 0 时 fact-checker skipped 后，“其后无输入的成文 / 冷读 dispatch”也可 skipped，并据此判 pass。
- `book-writer.md:9-16` 明确 writer 即使 0 条接受仍有 `body_artifact` 与 source map 输入，并负责编排、交付正文-only 页面；它不是无输入下游。
- `cold-reader.md:9-10,26-31` 明确接收最终读者页面，并由该角色把正文-only 页面结算为 `not-applicable`。若直接 skipped，现有合同没有保存独立 cold-read N/A 结果的主体。
- `book-engine.md:73-76` 仍要求生成正文优先的读者页，并把冷读结果留在 audit；0 个陪读单元只是合法终态，不等于省略最终页面装配和门结算。

### 影响

- 最新全 0 scoped pass 的任务图与当前角色合同互相冲突，不能作为“全 0 路径已独立通过”的有效原始证据。
- 正确路径应至少明确：fact-checker skipped；judge 实际执行并通过；writer 用正文输入实际交付 body-only 页面；cold-reader 实际结算 N/A，或由现行合同另行明确哪个独立主体可以确定性结算 N/A。
- 此问题不推翻 RI-P01 的非零 11-dispatch fixture，但会使 calibration 中“图书全 0 候选路径也已独立通过”的当前声明没有合格 raw 支撑。

### 最小解除条件

统一 book protocol、writer、cold-reader、orchestrator 对全 0 下游 dispatch 的规则，随后保存新的限定冷启动 raw；旧错误 pass raw 保留为历史失败证据，不覆盖。

## 6. Blocker B03：document map 三类身份重叠

结果：`fail`。

### 冲突

- `document-map.md:21` 把整个 `v3/skill/examples/` 列为 `current-authority`；`:37` 又把其中 `book-annotation-examples.md` 的冻结金标与反例列为 `routed-evidence`。同一文件同时有两类身份。
- `document-map.md:35` 把整个 `v3/eval/constraint-redesign-r2/` 列为 `routed-evidence`；`:48` 又把其中较早的 `*-raw.md / *-rerun-*.md` 列为 `retired-preserved`，但没有从前一目录范围排除它们或给出确定的 latest 清单。
- 分类规则宣称新索引用来区分 current / routed / retired；当前重叠让执行者无法仅凭索引确定文件身份，也与“不按文件名猜最新”相冲突。

### 默认入口

`AGENTS.md + v3/current-task.md` 的默认入口本身仍然正确，README 没有重新成为动态状态副本。阻塞发生在 current-task 路由后使用 document map 分类时，不是默认入口退化。

### 最小解除条件

将范围改成互斥的精确文件或带明确排除项的目录，并为本轮 eval 指定哪些 raw 是当前可引用结果、哪些只保留失败史；冻结 examples 只能归入一个身份。

## 7. 回归证据包

结果：`pass_except_B02_evidence_claim`。

- 卡片数量：book 12、Skill 10、run-integrity 7，共 29。
- 分类：16 historical、13 derived-structure；派生结构测试均明确不是历史重放或真实运行。
- book 12/12 与限定预期匹配；B-N07 明确用后续真实用户否定覆盖旧 audit 的 waiting，B-N09 只拒绝当前证据范围，没有扩大成永久无价值。
- Skill 10/10 与限定预期匹配；S-N01—S-N06 明确没有历史证据，S-P01/S-P02/S-N08 保持 scope-lock。
- 最新 RI rerun-8 为 7/7 derived-structure-only；RI-P01 的 request、check、coverage、11 dispatch、nested source/fact gates 和 `runtime-not-run` 声明边界自洽。
- 29 卡均有独立 actual 与 raw 路由；没有 pending、blocked 或 mismatch 状态。

但全 0 book handoff raw 不属于这 29 张卡，仍是 current-task 要求的角色冷启动证据；B02 未关闭前不能把所有角色冷启动概括为通过。

## 8. 状态、引用、行数、裁剪与模板

结果：`pass`。

- 未发现旧 `not_run`、`test_invalid` 或 underscore 状态重新进入现行规则；manifest、主控和角色可表达 `not-run / pass / fail / blocked` 及适用的 `not-applicable`。
- `v3/current-task.md` 49 行；`SKILL.md` 97 行；book/judge/skill protocols 为 77/60/76 行。
- 所有角色合同最长 48 行；每份均为 3 条核心职责 + 2 条禁令，共 5 条行为规则，不超过 7。
- 三个读者模板的生产说明均在 HTML comments 内；去掉 comments 后没有把 candidate、judge、audit、manifest 等生产词作为可见槽位。
- 29 cards、suite、协议和合同引用的直接文件路径均可定位；未发现本轮引用的显式行号超过目标文件长度。
- `git diff --check` exit 0。

## 9. Dirty worktree 与可分离边界

结果：`pass_with_caution`。

- `HEAD` 与 fixed point 一致，分支正确；工作区仍有 tracked 修改和大量 untracked 文件，没有独立提交。
- `change-set-boundary.md` 将约束返工 A 组与旧 022 R1/R2、候选 audit、版式 Demo、一次性提示和设计合同 B 组分开；本审查未 reset、checkout、删除、移动、暂存或提交任何文件。
- `calibration-log.md` 与 Phase 4 gate 包含返工前未提交 hunk；未来若形成提交仍必须逐 hunk 核对，不能整文件归因本轮。
- 当前只能声称“可分开审查”，不能声称工作区干净或已物理形成干净变更集。

## 最终 Standards verdict

```yaml
verdict: fail
blockers:
  - B01: non-source verification gates differ between orchestrator objects and manifest scalars
  - B02: latest all-zero cold-start raw incorrectly skips writer and cold-reader despite live inputs and duties
  - B03: document-map categories overlap for examples and eval raw files
runtime: not-run
```

可以声称：typed fact request、批量 coverage、逐候选淘汰、Skill 条件事实链、RI rerun-8 的 7/7 派生结构结果、29 张 case 的分类与机械完整性、角色行数、模板、引用、dirty boundary 和 diff whitespace 检查完成。

不可以声称：Standards 轴通过、双轴验收通过、所有角色冷启动通过、完整主控 manifest schema 闭合、真实图书/Skill 运行、内容质量、用户体验、Phase 4 或 ReaderLab V3 整体通过；当前不应进入 Demo。
