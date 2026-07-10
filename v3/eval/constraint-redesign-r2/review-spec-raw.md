# 2026-07-10 约束重构返工：独立 Spec 验收原始输出

## 审查身份、上下文与边界

- reviewed_at_utc: `2026-07-10T11:24:00Z`
- reviewed_at_local: `2026-07-10T07:24:00-04:00`
- axis: `Spec`
- verdict_policy: `any blocker => fail`
- real_run_performed: `false`
- content_generated: `false`
- rules_or_cases_modified_by_reviewer: `false`

本审查者此前未参与约束规则、case 或汇总的实施修改；此前执行的是验收类工作：run-integrity 派生结构回归，以及同一证据链中的图书角色合同冷启动 raw。此前没有生产陪读、运行 fresh/revision、修改规则、修改 case 或更新汇总结论。本次只新增本 Spec raw。

这不是零上下文审查。当前 verdict 以本轮重新读取的现行仓库文件、git 状态、diff 检查和既有独立 raw 为证据；先前个人判断不作为通过依据。

## 读取与检查范围

按 `v3/current-task.md` 路由，实际检查了：

- `v3/current-task.md`
- `v3/standards/constraint-architecture.md`
- `v3/skill/SKILL.md`
- `v3/skill/protocols/book-engine.md`
- `v3/skill/protocols/skill-engine.md`
- `v3/skill/protocols/judge.md`
- `v3/skill/templates/run-manifest.md`
- `v3/skill/roles/README.md`、orchestrator 与图书 / Skill 角色合同
- `v3/standards/regression-suite.md`
- 29 张 book / skill / run-integrity case
- `v3/standards/calibration-log.md`，包括文件末尾 `2026-07-10 约束重构返工更正`
- 图书、Skill、run-integrity 回归 raw
- 图书、Skill、主控角色冷启动首次及复跑 raw
- `v3/eval/constraint-redesign-r2/change-set-boundary.md`
- 相对 `HEAD 1ed34c4` 的 `git status --short`、`git diff --name-status` 和 `git diff --check`

未读取或执行真实 022 / gstack 运行，不打开 LifeAtlas，不生成内容，不运行 fresh/revision，不修改规则、case、回归汇总或 current-task。

## 总结论

- final_verdict: `fail`
- blockers: `2`
- non_blocking_findings: `3`
- passed_requirement_groups: `9`

失败不是因为缺少大量产物。大部分返工要求已经闭合；但存在两个直接违反当前 Spec 的阻塞：

1. 来源事实逐项状态在 `judge.md` 与 `fact-checker.md` 之间仍是两套不兼容枚举。
2. RI-P01 最新结构正例把一个整章 book run 压成 9 个聚合 stage，违反当前固定 11 任务与 instance-level dispatch 账本；因此 `accept-structure-only` 以及回归套件 29/29 全匹配声明目前不能成立。

按照“任何 blocker 必须 fail”，最终 Spec verdict 为 `fail`。

---

## Blocker 1：来源事实逐项 verdict 枚举仍不一致

- id: `SPEC-B01`
- severity: `blocker`
- requirement: `schema 字段与协议、manifest 状态完全一致；所有状态枚举闭合`
- actual: `fail`

### 证据

`v3/skill/protocols/judge.md` 的来源与事实门要求逐项输出：

```text
supported | unsupported | blocked
```

`v3/skill/roles/fact-checker.md` 的实际角色 schema 则输出：

```text
supported | conflicted | insufficient | out_of_scope
```

两者只有 `supported` 相同；协议的 `unsupported` 和 `blocked` 不能无损对应角色的 `conflicted / insufficient / out_of_scope`，角色的 item schema 也没有逐项 `blocked`。两边整门 `pass | fail | blocked` 虽一致，但这不能修复逐项证据 schema 的不兼容。

### 影响

- 独立验收门无法直接消费 fact-checker 输出而不做合同外映射。
- `conflicted`、`insufficient`、`out_of_scope` 是否都映射为 `unsupported`，以及来源不可达时逐项是 blocked 还是只把 overall 设为 blocked，当前没有权威规则。
- 两个执行者可对同一核查结果给出不同的 judge item 状态，仍各自声称遵守文件。
- 这直接违反 current-task 的“schema 字段与协议、manifest 状态完全一致”，不能降为未来机器校验优化。

### 最小解除条件

选择一个权威 item schema，并在另一文件逐字对齐；若保留细粒度 fact-checker 枚举，则在 judge 协议写出确定性映射和逐项 blocked 的表达方式。修后需做一次限定的事实门 schema 冷启动复核。

### 声称边界

可以声称整门三态一致；不能声称来源事实门的逐项 schema 已闭合或角色 / 协议完全一致。

---

## Blocker 2：RI-P01 不满足当前成本与 dispatch 结构

- id: `SPEC-B02`
- severity: `blocker`
- requirement: `图书标准链 11；实例级 dispatch；actual_tasks 与真实 dispatch 账本一致；逐 case actual 证据成立`
- actual: `fail`

### 权威成本与 dispatch 证据

当前文件一致规定：

- `constraint-architecture.md`：图书标准链固定为 11；正文 1、提名 2、归并 1、候选 3、事实 1、裁判 1、成文 1、冷读 1。
- `SKILL.md`：图书标准章固定 11 个 Agent 任务。
- `roles/README.md`：逐角色实例相加为 11，主控不计入。
- `orchestrator.md`：两个提名实例和三个候选实例必须分别记录，每个 dispatch 有唯一 `dispatch_id` / `instance_id`。
- `run-manifest.md`：stages 只记录 orchestrator dispatch id，`budget.actual_tasks` 等于实际计费的非复用、非跳过 dispatch 数。
- `current-task.md`：盲区并入裁判并保持标准链 10—11；当前稳定文件已进一步固定为 11。

### RI-P01 当前结构

RI-P01 是 `route.line: book`，读取固定全章 `/fixtures/source/chapter-01.md:1-120`，没有声明 shortform 或其他降档 profile。它记录：

```text
actual_tasks: 9
executed entries: 9
```

其中只有一个 `anchor-identification` 和一个 `candidate-production`。这两个名称是阶段类别，不是角色索引要求的两个独立 anchor-nominator dispatch、一个 anchor-merger dispatch和三个独立 cognition-candidate dispatch。case 也没有 `dispatch_id` / `instance_id` 能证明重复实例分别执行。

### 最新 raw 的问题

`regression-run-integrity-rerun-2-raw.md` 将 RI-P01 判为 `accept-structure-only`，理由之一是本次限定读取没有 roles index，且 case 没有声明自己是标准 11 任务运行。

这在窄切片内可以解释为什么审查者没有使用 11，但不能在跨文件 Spec 验收中覆盖当前权威成本合同：

- case 明确是 book 的完整章范围，而不是 5—7 任务短文。
- 9 不属于当前声明的标准 11、短文 5—7或深读 15—18 任一档。
- manifest 没有 run profile 字段可以证明这是获准的非标准 9 任务路径。
- stage 列表没有 instance-level dispatch，不能仅因数量自洽就满足 dispatch 账本要求。

### 影响

- RI-P01 目前不能作为“合规 fresh 结构可表达”的正例接受。
- 最新 run-integrity actual 应为 `reject` 或至少 `blocked`，而不是 `accept-structure-only`。
- 因此当前 `regression-suite.md` 的 RI 7/7 和总计 29/29 匹配声明不成立。
- 这不意味着真实 run 失败；它意味着派生正向 fixture 与最新成本 / dispatch Spec 漂移。

### 最小解除条件

二选一：

1. 把 RI-P01 改成标准 11 个唯一实例 dispatch，并使 actual_tasks 与 11 个实际执行 dispatch 一致；或
2. 在权威合同和 manifest 中定义可审计的非标准 profile，明确 9 任务为何合法、哪些角色实例被合并，以及生产与独立验收不被合并，然后让 case 显式选择该 profile。

修后必须重新独立执行 RI-P01，并据 actual 更新 suite；不能只改 Expected。

### 声称边界

六张 RI 负例仍可声称按预期拒绝；不能声称 RI-P01 当前结构接受，也不能声称 run-integrity 7/7 或全部 29 卡已匹配。

---

## 逐项 Spec 核查

### 1. 盲区并入裁判且图书链为 11

- result: `pass`
- evidence:
  - `book-engine.md` 第 6 步把整批盲区检查与绝对裁判放在同一个 cognition-judge 任务；发现关键遗漏只定向退回，不自行补候选。
  - `cognition-judge.md` 的任务和 `batch_gap_check` 同时承载盲区检查与裁判。
  - `constraint-architecture.md`、`SKILL.md`、`roles/README.md` 一致给出图书标准链 11，主控不计入。
  - 图书 cold-start rerun 重建 11 任务图，8/8 角色合同通过。
- boundary: 只证明静态调度图；没有真实调度 11 个 Agent。

### 2. Skill 3—5 任务角色所有权

- result: `pass`
- evidence:
  - `skill-engine.md` 标准链明确 5 个独立任务：source integrator 生产净化正文/source map；mechanism auditor 生产机制候选；skill judge 独立裁判；skill writer 单一成文；cold-start reproducer 独立冷读与适用冷启动/复现。
  - 简单材料仅可在生产与独立裁判、成文与独立冷读不合并自评的前提下降到 3—4。
  - 外部事实才追加共用 fact-checker；突破 5 个任务需先说明触发并取得用户批准。
  - 五份角色合同的输入、输出、禁令和停止主体与上述所有权一致。
- boundary: 不证明 gstack/browse 已真实运行或复现。

### 3. 锚点调查问题

- result: `pass`
- evidence:
  - anchor-nominator 每个提名包含 `likely_shallow_or_wrong_reading` 和 `investigation_question`。
  - `links` 有 target locator 与 relation。
  - anchor-merger 保留 `investigation_question`、context links，并为定向补提名提供 target locators、question 与 return_to。
- boundary: 只证明 schema 可承载，不证明真实锚点质量。

### 4. Skill source map actions 与 deletion destination

- result: `pass`
- evidence:
  - skill-source-integrator 的可见单元记录全部 source actions：`retained | moved | merged | reordered` 与 treatment。
  - deletions 单独记录 source refs、reason 和 destination：`appendix | technical-lead | audit | omitted`。
  - skill-engine 明确逐单元 source map 与重要删除去向必须留在 audit。
- boundary: 只证明合同表达能力，不证明任何真实净化正文已保持源含义。

### 5. 状态枚举

- result: `fail`
- evidence:
  - run manifest、orchestrator、生产角色整体 status、冷读 not-applicable 和确认状态已大体闭合；连续主控 raw 也逐步关闭 route、dispatch、计数和确认状态机。
  - 但来源事实逐项 verdict 仍存在 `judge.md` 与 fact-checker 的直接枚举冲突，见 `SPEC-B01`。
- boundary: 不能据“主控最后一个 scoped blocker 关闭”扩大为所有角色 / 协议状态完全一致。

### 6. 历史卡与派生卡分类、逐 case actual

- result: `pass_with_blocker_in_run_integrity_positive`
- evidence:
  - case 总数 29：16 historical，13 derived-structure。
  - 图书 12 卡均有实际历史对象与原判词或后续真实结论；没有逐字原话时明确写无并收窄范围。
  - Skill 4 张 historical 有真实迷你页 / 资产卡与归档结论；6 张 derived 明确无历史样本和真实运行。
  - 7 张 RI 全部标 derived-structure、historical_run false、runtime-not-run。
  - 图书 raw 逐卡 12/12，Skill raw 逐卡 10/10，RI raw 逐卡记录 actual/match。
- blocker:
  - 分类本身通过；RI-P01 的 actual 证据不满足跨文件成本 / dispatch Spec，故不能接受总计 29/29，见 `SPEC-B02`。

### 7. B-N07 后续用户否定

- result: `pass`
- evidence:
  - B-N07 卡区分 audit 当时 waiting 与后续真实结论。
  - calibration log 明确 022 R1 未过体验门：四段离原文太远、像新增阅读材料、仍需读者整理。
  - regression-book raw 实际读取集中讲堂和 audit，并以该后续否定覆盖旧 waiting，actual reject 与 expected 匹配。
- boundary: 无逐字用户评价，只能使用后续真实结论摘要；raw 已明确该证据缺口。

### 8. 角色冷启动原始结果

- result: `pass_with_non_blocking_evidence_shape`
- evidence:
  - 图书首次失败 raw 保留；完整 rerun 读取 8 合同 + roles README，8/8 通过并重建 11 任务图。
  - Skill 首次 5 合同 raw 保留；首次指出 4 个角色的状态/0 条/正文不变 schema 阻塞，四合同 rerun 逐项关闭；cold-start-reproducer 在首次 raw 已通过且当前合同仍具备独立状态输出。
  - 主控首次失败与连续 4 次 scoped rerun 均保留；route、dispatch/stages、gate、claims、计数、awaiting 路径和确认组合逐项关闭，最后 raw 明确只 scoped pass。
- non_blocking:
  - Skill 和主控没有一份“所有当前合同一次性完整重跑”的最终 raw，而是首次全量 + 定向复跑的累积证据链。它仍可追溯，且本次 Spec 审查直接读取当前合同交叉核对，因此不单独定 blocker。
- boundary: 这些都是静态冷启动；不能声称真实 Agent 调度、正文完整性实际证明或内容运行通过。

### 9. RI-P01 最新复跑

- result: `fail`
- evidence:
  - 最新 raw 正确限制为 `accept-structure-only / runtime-not-run`，没有升级到真实运行，这是正面边界。
  - 但其 9 个聚合 stage 不满足当前固定 11 实例 dispatch，见 `SPEC-B02`。
- boundary: runtime-not-run 声称诚实；结构 accept 不成立。

### 10. 成本

- result: `pass_except_RI-P01_fixture`
- evidence:
  - 图书标准 11、短文 5—7、深读 15—18；盲区不另计。
  - Skill 标准 5、简单 3—4；外部事实追加 fact-checker 并受预算审批。
  - `SKILL.md` 97 行，低于 300 行；book / skill 协议分别 77 / 74 行，保持短协议目标。
  - roles README 和 orchestrator 明确主控不计任务，实际 dispatch 计费进入唯一 manifest。
- blocker_link: RI-P01 9 任务未落入任何已声明档位，导致正例不合规。

### 11. 可分离变更集

- result: `pass_with_caution`
- evidence:
  - `change-set-boundary.md` 以 `HEAD 1ed34c4` 为基线，A 组列约束返工，B 组明确排除旧 022 R1/R2、候选 audit、版式 Demo、已消费提示和旧设计合同。
  - git status 仍显示较大 dirty worktree；文档没有声称干净、暂存或提交。
  - 文档要求未来按 A 组逐文件/逐 hunk 暂存，并在提交前重新检查 status。
- caution:
  - calibration-log 与 Phase 4 gate 同文件含返工前未提交内容，物理提交时必须按 hunk 分离；当前只有审查边界，没有真实 staging 证明。
- boundary: 当前只可声称“可分开审查”，不可声称工作区已物理分离或提交边界已经验证。

### 12. 声明不升级

- result: `pass`
- evidence:
  - calibration-log 末尾 `2026-07-10 约束重构返工更正` 明确覆盖旧“12 角色无悬空 / 三组均通过 / 静态回归完成”的宽泛声明。
  - 更正节明确所有角色结果是合同静态冷启动，不是实际调度或内容运行。
  - RI 最新 raw 明确 runtime-not-run；回归 raw 分别限制历史证明范围、派生结构、scope-lock 与真实运行。
  - change-set boundary 不声称真实运行、内容质量或流水线通过。
  - current-task 仍为“约束重构返工中；暂不验收，不得开始 Demo”。
- boundary: 声称边界本身合格；但不能因为声明诚实而忽略 `SPEC-B01/B02`。

---

## 验证结果

- `git diff --check`: `pass`，无空白错误输出。
- case 文件数: `29`。
- 分类: `16 historical + 13 derived-structure`。
- `SKILL.md`: `97` 行，满足不超过 300 行。
- book / skill protocol: `77 / 74` 行。
- git boundary: dirty worktree 存在；未暂存、未提交、未移动、未删除。

## 非阻塞项

1. Skill judge 的 `status / selection_count / zero_accept_reason` 组合不变量尚未写成显式机器校验规则；当前 schema 已可无歧义表达，属于未来 validator 强化，不是本轮 blocker。
2. writer 的 verification item、部分 return_to 仍是自由结构；停止与成功路径已有结构化出口，不阻断静态 handoff。
3. 主控 / Skill 冷启动证据采用“首次全量失败 + 定向 scoped rerun”的累积链，而不是最终一次全量重跑；证据保留真实失败并可追溯，本次不定为 blocker。

## 最终 verdict

```yaml
axis: spec
verdict: fail
blockers:
  - SPEC-B01: source/fact item verdict enum mismatch
  - SPEC-B02: RI-P01 violates 11-task instance dispatch contract
can_claim:
  - 大部分角色调度、锚点、Skill source map、历史分类、B-N07、冷启动证据、边界与声明收窄已闭合
  - 六张 run-integrity 负例仍按预期拒绝
cannot_claim:
  - Spec 轴通过
  - 所有状态枚举完全一致
  - RI-P01 结构正例通过
  - run-integrity 7/7 或全部 29 case 匹配
  - 可以开始 Demo 或真实 fresh/revision run
```

最小下一步是先修正 `SPEC-B01` 的事实 item schema 对齐，并修正 / 重建 RI-P01 的 11 实例 dispatch 结构后独立复跑。两项未关闭前，Spec 轴必须保持 `fail`，不得更新为等待用户复审或进入 Demo。
