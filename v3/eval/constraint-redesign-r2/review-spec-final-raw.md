# 2026-07-10 约束重构返工：最终独立 Spec 验收原始输出

## 验收边界

- reviewed_at_utc: `2026-07-10T15:58:28Z`
- reviewed_at_local: `2026-07-10T11:58:28-04:00`
- axis: `Spec`
- verdict_policy: `any blocker => fail`
- baseline: `HEAD 1ed34c4`
- real_run_performed: `false`
- content_generated: `false`
- rules_or_summaries_modified_by_reviewer: `false`

本次按用户 2026-07-10 返工要求重新读取现行总则、两线协议、角色合同、manifest、29 张 case、最新回归与冷启动 raw、文档生命周期索引和 dirty 边界。此前 Spec fail 与各次 scoped rerun 均保留；本文件不覆盖旧失败，也不把专项 pass 扩大为真实运行或整条流水线通过。

## 总 verdict

```yaml
axis: spec
verdict: fail
blockers:
  - SPEC-F01: anchor merger contract uses argument-task grouping instead of the protocol's cognitive-question grouping
matched_regression_cases: 29/29
run_integrity_cases: 7/7
runtime: not-run
```

除锚点归并合同的一处可执行标准漂移外，本轮点名的其他链段均已闭合。由于执行 Agent 不读取完整图书协议，这一漂移会直接改变实际归并行为，属于 blocker；按验收纪律，本轴仍为 `fail`。

## Blocker：锚点归并合同仍可能退化为论证结构归并

- id: `SPEC-F01`
- result: `fail`
- affected_file: `v3/skill/roles/anchor-merger.md`

图书协议规定归并者按“是否在解决同一个认知问题”合并提名。这是本轮从“找论证结构”转向“定义值得展开的认知问题”的关键约束。

但真正发给执行 Agent 的短合同仍写为：

> 按同一论证任务合并重复提名。

合同虽然保存了 `investigation_question` 字段，却没有要求以该问题作为归并判据。一个只读角色合同的 Agent 可以把同一论证位置上针对不同误读、不同调查问题的提名合并为一个锚点，也可以按论证结构去重，而不按认知问题去重；这会重新出现用户此前指出的退化。

该问题不能由完整 `book-engine.md` 补救，因为四层分发明确规定执行 Agent 不读取完整线路协议。字段存在也不能替代行为规则：`investigation_question` 被保留，不等于归并决策必须以它为准。

最小解除条件：把 anchor-merger 的核心职责直接改为“按是否解决同一个认知问题归并；同一论证位置但调查问题不同不得仅因位置相同而合并”，并保持 `investigation_question`、少数派与定向补提名的现有输出。随后只需做一次锚点提名 → 归并的限定冷启动复核；不需要重开其他已通过链段。

## 逐项验收

| 用户要求 | 结果 | 实际证据与边界 |
| --- | --- | --- |
| 盲区检查并入认知裁判；无早停标准计划为 11 | `pass` | constraint、SKILL、book protocol、roles index 一致；裁判同一任务先做盲区检查，主控不计入；全 0 时 fact-checker skipped、judge 仍执行并结算绝对价值门。仅为静态合同。 |
| Skill 线 3—5 任务的生产、独立裁判、成文、冷读/复现所有权 | `pass` | 标准 5 任务分别由 source integrator、mechanism auditor、skill judge、skill writer、cold-start reproducer 拥有；简单路径不得合并生产与裁判或成文与冷读自评；外部事实扩展须预算审批。未运行真实 Skill。 |
| 锚点提名说明读浅/读偏与调查问题 | `pass` | anchor-nominator 有 `likely_shallow_or_wrong_reading` 与 `investigation_question`，实例数 2、0 提名和 links schema 均闭合。 |
| 锚点归并继续以认知问题为判断主体 | `fail` | 协议写“同一认知问题”，执行合同写“同一论证任务”；见 `SPEC-F01`。 |
| Skill source map 的保留、移动、合并、重排、整理方式、删除理由与去向 | `pass` | `clean_units.source_actions` 记录全部来源动作与 treatment；`deletions` 单列 source refs、reason、destination。 |
| 状态枚举与停止状态 | `pass` | manifest、orchestrator、生产角色、冷读、事实门和确认状态能表达 not-run/pass/fail/blocked 及适用的 not-applicable；样本确认三路与 mixed route 闭合。 |
| 历史回归与派生结构测试分开 | `pass` | 29 张卡为 16 historical + 13 derived-structure；派生卡均不冒充历史运行。 |
| B-N07 使用后来真实否定覆盖旧 waiting | `pass` | case、book raw 与 calibration 均明确旧 audit 只 waiting，后续真实结论为未过体验门；没有伪造逐字用户原话。 |
| 保存角色冷启动与回归原始结果 | `pass` | 图书、Skill、主控、事实门、图书 fact handoff 均保留首次失败和定向复跑；book 12/12、Skill 10/10、RI 最新 7/7 各有 raw。均为静态/历史复核。 |
| typed fact request、批量 handoff、逐 request coverage、坏候选隔离 | `pass` | 图书与 Skill 候选可输出非空唯一 request/claim id；fact-checker 保留 kind/assertion_type/materiality、稳定 check id、精确 coverage、停止回交；judge 逐候选淘汰，不让一个坏候选拖死整批。 |
| 图书三个候选全 0 的路径 | `pass` | 三份合法 0 报告；fact-checker skipped 且不计 actual_tasks；judge 仍做盲区检查并以 selection_count 0 结算 absolute_value pass。仅静态路径。 |
| RI-P01 自包含 request/check/coverage fixture | `pass` | 11 个实例级 dispatch、3 份 request、3 条 check、3 条精确 coverage、嵌套来源/事实子门、trigger/source boundary/return 字段闭合。 |
| RI rerun-8 与 suite | `pass` | RI 7/7、book 12/12、Skill 10/10，总计 29/29 与限定 expected 匹配；RI-P01 只为 `accept-structure-only`。 |
| 成本声明 | `pass` | 图书标准无早停 11，盲区不另计；Skill 标准 5、简单 3—4，条件事实核查超出预算需用户批准；actual_tasks 只计实际非跳过 dispatch。 |
| 文档生命周期分类 | `pass` | document-map 分为 current-authority、routed-evidence、retired-preserved，并写明读取条件、替代关系和禁止用途；未移动或删除历史文件。 |
| dirty worktree 分离 | `pass_with_caution` | change-set-boundary 以 HEAD 1ed34c4 区分本轮返工集与旧 022 R1/R2、Demo、一次性提示和设计合同；当前仍未物理暂存/提交，calibration 与 Phase 4 文件未来必须逐 hunk 处理。 |
| 声明不升级 | `pass` | suite、RI raw、calibration、document-map 与边界文件均明确 `runtime-not-run`；没有声称图书线、Skill 线、Phase 4 或 ReaderLab 流水线通过。 |

## 回归与证据核对

- 图书历史 cases：`12/12` 与限定预期匹配。
- Skill cases：`10/10` 与限定预期匹配；其中 4 historical、6 derived-structure。
- run-integrity cases：`7/7` 与限定预期匹配；全部 derived-structure、`historical_run: false`。
- 总计：`29/29` 匹配；16 historical、13 derived-structure。
- 最新 RI 证据：`regression-run-integrity-rerun-8-raw.md`，明确 `runtime-not-run`。
- `git diff --check`：通过。
- 当前分支：`v3/cognitive-compounding`；HEAD：`1ed34c4`；工作区仍 dirty，未暂存、未提交、未删除或移动旧产物。

这些通过项不能抵消 `SPEC-F01`，也不能证明真实 Agent 已执行完整调度。旧 book cold-start 全量 raw 早于 typed request 修订，但后续 book fact-handoff 与 RI rerun-8 已保存针对新链段的独立原始复核；本次把它视为可追溯的累积证据链，不冒充一次全链真实运行。

## 声明边界

当前可以声称：

- 29 张历史/派生回归卡与限定预期匹配；运行完整性结构包为 7/7。
- 除锚点归并判据外，角色调度、事实 handoff、全 0 路径、成本、生命周期分类和 dirty 边界已通过本次静态 Spec 核对。

当前不能声称：

- Spec 轴通过或整套约束返工完成验收。
- 真实 fresh/revision、真实事实核查、内容生产、图书线、Skill 线、用户体验、Phase 4 或 ReaderLab 流水线通过。
- 可以开始 Demo。

最终结论：`fail`。只需修正 anchor-merger 的归并判据并做限定冷启动复核；在该 blocker 关闭前，不应把 current-task 改为等待用户验收，也不应进入 fresh Demo。
