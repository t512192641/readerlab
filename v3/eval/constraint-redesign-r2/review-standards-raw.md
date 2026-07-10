# 约束重构返工 Standards 独立验收原始输出

## 审查身份与边界

- fixed point：`1ed34c474bd2b84a9ed164a59810506b8fa2b4aa`；当前 `HEAD` 与该提交相同，因此本次审查对象是该基线上的 tracked 工作区 diff 与 untracked 文件，不是提交间 diff。
- 审查时间：2026-07-10 07:26 EDT（UTC-04:00）。
- 审查轴：只做 Standards，不代替并行的 Spec 审查，不把两轴结果合并。
- 独立性披露：本 Agent 未实施任何规则、协议、合同、manifest、case 或总结文件修改；此前参与过图书 12 case 回归原始判断，也做过 Skill 角色合同首次检查与 schema 复核，因此不是零历史上下文。当前 verdict 重新依据现行工作区证据得出，不用本人旧 raw 代替 Standards 判断。
- 路由：先读 `v3/current-task.md`，再按其权威输入、待修对象和验证项读取约束架构、Skill、两线/裁判协议、角色合同、manifest、29 case、必要 raw、变更边界、模板和 calibration 末尾更正。
- 明确未做：不生成陪读、不运行 fresh/revision、不重跑 022 或 gstack、不修改规则/总结、不暂存/提交/移动旧文件。

## 结论先行

- blockers：`0`。
- non-blocking issues：`4`。
- Standards verdict：`pass`。
- 通过含义：当前约束重构在静态标准层闭合了角色图、任务计数、最小上下文、schema / gate / manifest 状态、29 case 证据包、模板可见边界和 dirty worktree 分离；没有发现必须令 Standards 失败的冲突。
- 不代表：Spec 轴通过、真实角色 dispatch、真实 fresh/revision run、内容质量、用户体验、Phase 4、ReaderLab V3 整体通过。

## 1. 角色图与任务数

### 图书线

- `v3/skill/roles/README.md:8-15,22` 给出 8 类执行合同及实例数：`source-map 1 + anchor-nominator 2 + anchor-merger 1 + cognition-candidate 3 + fact-checker 1 + cognition-judge 1 + book-writer 1 + cold-reader 1 = 11`，主控不计入。
- `v3/skill/protocols/book-engine.md` 的执行链按同一顺序覆盖正文/source map、双提名、归并、三候选、事实核查、含盲区检查的独立裁判、锁定、单一成文和冷读。观点锁定由主控完成，不另冒充 Agent 任务。
- `v3/standards/constraint-architecture.md:83-85` 的后续精确规则、`v3/skill/SKILL.md` 调度段、角色索引和 book 冷启动复跑均收敛到标准 11，盲区检查不另增任务。
- 每阶段都有生产、输出、停止/退回主体：source-map 处理一手正文；提名与归并只定锚点；candidate 只生产；fact-checker 独立核事实；judge 先查盲区再绝对判定；writer 不改题；cold-reader 不读生产背景。
- 0 提名、0 候选、0 接受和正文-only 冷读 `not-applicable` 均有结构化出口。
- verdict：`pass`。

### Skill 线

- `v3/skill/protocols/skill-engine.md:41-51` 与角色索引逐项一致：来源整合、机制候选、独立裁判、单一成文、独立冷读/冷启动/复现，共 5 个任务。
- 简单材料 3—4 个任务的合并边界明确禁止生产者自评；外部事实触发共用 fact-checker 时必须说明并按预算审批。
- source integrator 只建净化正文/source map；mechanism auditor 是候选生产者；skill judge 独立验收并允许 0 条；writer 只写锁定包并证明正文未变；cold-start-reproducer 分开记录冷读与冷启动/复现。
- verdict：`pass`。

### 非阻断问题 1：概览措辞仍有轻微双口径

- `constraint-architecture.md:83` 仍写“标准图书章约 10—11 个任务”，紧接的 `:84` 又明确“标准链为 11 个任务”。`current-task.md` 也保留“10—11”，而 Skill、角色索引和返工更正采用固定 11。
- 判断：不阻断。精确执行句、角色算式、协议和合同均唯一落到 11，未发现实际 10 任务图；但下次文字清理可把概览统一成“标准 11”，避免执行者误把 10 当成同等标准值。

## 2. 协议、角色合同与最小上下文

- `constraint-architecture.md` 四层分发明确：完整总则只给主控/架构审查；线路协议只给主控/编排；执行者只拿线路两条规则摘录、自身短合同和任务输入；回归病例只给裁判/回归执行者。
- `v3/skill/SKILL.md` 的“路由与最小上下文”逐字采用同一边界，普通作者、成文者和冷读者不得读取另一线路、历史病历或完整生产日志。
- 每份角色合同均包含任务、允许输入、3 条核心职责、2 条禁令、结构化输出和停止条件；执行输入没有要求完整线路协议。
- 图书角色合同冷启动复跑在不读完整 book protocol 的限定下重建 11 任务图；Skill 角色合同复核在不读完整 Skill protocol 的限定下重建 5 任务图并关闭首次 schema 阻塞。
- verdict：`pass`。

### 非阻断问题 2：Skill judge 的事实核查输入缺“如适用”字样

- `skill-engine.md:51` 只在引入外部事实时追加 fact-checker；`skill-judge.md:10,37` 却把“已完成事实核查结果 / 事实核查不完整”写成无条件输入和停止项。
- 判断：不阻断。judge 自身负责来源核对，没有外部事实时可将事实核查理解为不适用，现有五任务图仍可执行；但增加“如适用”会消除冷启动执行者把标准 Skill run 错判为必须第六任务的余量。

## 3. Schema、状态枚举与 manifest 转换

- 主控 `run_ref.status` 与 manifest 顶层完全一致：`planned | running | failed | awaiting-user | accepted`。
- 主控与 manifest 的六个技术 gate key 及枚举一致；cold-read / cold-start 允许 `not-applicable`，user experience 使用 `not-requested | pending | pass | fail`。
- 角色生产合同统一提供 `not-run | pass | fail | blocked`、`blocked_reason` 与 `return_to`；事实门和冷读门只省略角色执行时不需要输出的 `not-run`，正文-only 冷读单独使用 `not-applicable`，语义没有冲突。
- orchestrator dispatch 使用唯一 `dispatch_id + instance_id`，两个提名与三个候选可分别审计；`done/skipped/failed/reused` 到 manifest stages 的四项映射逐字一致，actual_tasks 只统计实际执行且计费的 dispatch。
- manifest 路由能表达 mixed 父 run 的 `unassigned` 以及 child runs；样本组合不变量和 `planned -> running / awaiting-user / failed` 三路互斥；运行后用户体验/claim 等待有返回 running 或 failed 的路径；accepted 受适用门、pending/blocked、预算和 claim 交集共同约束。
- Skill 四合同复核确认整体状态、合法 0 与 blocked、writer `source_body_integrity` 三项原阻塞已关闭。
- verdict：`pass`。

### 非阻断问题 3：两个组合不变量仍靠文字而非 schema 强制

- skill judge 能用 `status + selection_count + zero_accept_reason` 区分合法 0 与 blocked，但没有明文禁止 `status: pass + selection_count: 0 + zero_accept_reason: ""`。
- orchestrator dispatch 枚举包含中间态 `blocked`，stages 只记录四类终态；当前可理解为 blocked 恢复后转 done、不可恢复后转 failed，但 dispatch 自身转换没有逐条冻结。
- 判断：不阻断。现有字段已能无歧义表达正确状态，manifest 的 accepted/failed 保护也能拦截未清 blocked；若未来加入机器 validator，应把这两处组合/转换写成显式 invariant。

## 4. 29 张 case 与独立 raw

- 文件计数：book `12`，Skill `10`，run-integrity `7`，总计 `29`。
- 分类计数与 calibration 末尾更正一致：historical `16`，derived-structure `13`；run-integrity 全部明确 `historical_run: false`。
- 元数据检查：29/29 有 id、kind、expected、独立执行结果和 raw 路由；没有 pending 或 blocked case。
- raw 标题检查：book raw 有 12 个逐 case 标题，Skill raw 有 10 个，最新 run-integrity rerun-2 raw 有 7 个；没有 mismatch 或 blocked 汇总。
- 结果：book 12/12、Skill 10/10、run-integrity 7/7 与限定 expected 匹配；RI-P01 只为 `accept-structure-only / runtime-not-run`。
- 引用检查：从 case 与 suite 中提取 100 个唯一直接本地引用；没有缺失路径或超出文件总行数的显式定位。raw 文件及 case 指向的 Markdown anchor 均存在。
- 历史卡保存真实样本及原判词或后续结论；没有逐字原话处明确写无。派生卡明确声明没有历史运行/原判词，不冒充历史重放。
- 首次失败 raw 与后续 rerun raw 均保留；suite 明确最新 run-integrity raw，不用最新通过覆盖首次失败。
- verdict：`pass`。

### 非阻断问题 4：六张 RI 负例卡仍指首次 raw

- RI-N01—RI-N06 的卡内 `future_raw_result_path` 仍指向 `regression-run-integrity-raw.md`，suite 的最新整组结果则指向 `regression-run-integrity-rerun-2-raw.md`；RI-P01 已指向最新 rerun-2。
- 判断：不阻断。六个负例在首次 raw 与最新 rerun-2 中 verdict 相同，旧 raw 被要求保留且路径可定位，suite 也明确了最新结果；若希望每卡“一跳到最新”，可额外增加 latest raw 引用，但不能覆盖首次 raw 历史。

## 5. 引用、行数与模板生产词

- `v3/skill/SKILL.md` 当前 97 行，满足架构的 `<= 300`；book / judge / skill 三协议分别 77 / 60 / 74 行，未继续堆成长万能 prompt；角色文件最长 46 行。
- 三个读者模板剥离 HTML 注释后，禁用生产词扫描无命中。`audit`、锚点、候选、裁判、评分、路径、生产过程等只出现在不可见注释内，用于指导成文，不会成为模板默认可见内容。
- book 页面允许 0 个陪读并删除空槽位；Skill 主读页不预演机制，技术负责人页不复述正文；模板与协议职责一致。
- verdict：`pass`。

## 6. Dirty worktree 分离边界

- 当前 `HEAD == 1ed34c4`；工作区非干净，tracked 修改和 untracked 文件均通过 `git status --short` 审查。
- `change-set-boundary.md:5-12` 的 A 组覆盖入口、架构、Skill、协议、角色、manifest、模板/范例/rubric、Phase 4 闸门、calibration 更正、29 case 与 eval raw。
- B 组明确列出并原样保留旧 022 R1/R2 成品、五份 audit/候选、版式 Demo、一次性提示和历史设计合同；当前 status 中没有删除或移动记录。
- `calibration-log.md` 与 `phase4-pilot-definition.md` 的既有未提交 hunks 被明确标成需逐 hunk 分离，未把整文件错误归因给返工。
- `calibration-log.md:251-259` 的最新更正明确覆盖旧“12 角色/三组均通过”宽泛声明，改为图书 11、Skill 5、首次失败与复跑 raw 分存、29 case 分类及双轴验收中；当前状态没有提前升级。
- verdict：`pass`。可声称“逻辑上可分离审查”，不可声称 worktree clean 或已经物理形成可提交变更集。

## 7. 机械检查

- `git rev-parse 1ed34c4` 与 `git rev-parse HEAD` 相同。
- `git diff --check`：exit 0，无空白错误。
- case 计数、raw 标题、pending/blocked/mismatch、引用存在性与行号上界检查均通过。
- 模板去注释后的生产词扫描无命中。
- verdict：`pass`。

## 最终 verdict 与可声称范围

- blocker 数：`0`。
- non-blocker 数：`4`。
- final Standards verdict：`pass`。

可以声称：

- 当前静态约束架构与合同能重建图书标准 11 任务、Skill 标准 5 任务，并保持生产、独立裁判、成文、冷读/复现分离。
- 协议、角色 schema、manifest gate 与状态转换在当前静态文本下可一致执行；执行角色无需读取完整协议。
- 29 张 case 和三组最新 raw 齐备、可追溯且与限定 expected 匹配；历史与派生证据没有混写。
- 返工集可与旧 022/Demo 证据逻辑分开，机械检查通过。

不能声称：

- Spec 轴已经通过，或当前任务已经进入“等待用户复审”终态。
- 真实 run、真实 11/5 任务 dispatch、内容质量、用户体验、Phase 4、gstack/browse、LifeAtlas 回写或 V3 全链路通过。
- worktree 已干净、已暂存、已提交，或 A/B 边界已经物理执行。
