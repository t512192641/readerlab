# 约束重构 Standards 最终复验原始输出

## 身份、范围与方法

- fixed point：`1ed34c474bd2b84a9ed164a59810506b8fa2b4aa`；当前 `HEAD` 仍为该提交，本次复验 tracked 工作区 diff 与 untracked 返工文件。
- 时间：2026-07-10 07:45 EDT（UTC-04:00）。
- 上下文：本 Agent 写过首次 Standards pass，也参与过 book regression 与 Skill 合同 schema 复核；没有实施任何规则、协议、合同、manifest、case 或汇总修改。本次保留首次 Standards 文件不读不改，按当前文件重新检查首次报告后修订。
- 本次重点：图书精确 11 任务；Skill 条件事实核查；`judge / fact-checker / mechanism / skill-judge / orchestrator / manifest` 的嵌套事实门；29 case 与最新 raw；引用、行数、角色规则数量、模板可见词、dirty worktree 边界和 `git diff --check`。
- 规则：任何 blocker 使最终 verdict 为 `fail`；静态 schema 通过不升级为真实运行通过。

## 结论先行

- blockers：`1`。
- non-blocking issues：`0`。
- final Standards verdict：`fail`。

阻塞点不在新补的 Skill 条件事实链；该链本身已经闭合。阻塞发生在共享 `fact-checker` 被改成强制接收类型化 `fact_check_request` 后，图书候选合同仍只输出旧 `facts_to_check` 数组，导致固定 11 任务图中的 book fact-checker 没有合法输入。最新 RI-P01 又把这个无法按合同执行的 fact-checker dispatch 记为已执行，因此最新 7/7 回归汇总不能作为当前 Standards 通过证据。

## 1. 精确图书 11 任务

- `v3/current-task.md:32` 当前已同步为“标准链固定为 11 个任务（主控不计入）”。
- `v3/standards/constraint-architecture.md:83-84`、`v3/skill/SKILL.md:62`、`v3/skill/roles/README.md:22` 和 calibration 返工更正均使用精确 11。
- 实例算式保持：source-map 1、anchor nominator 2、merger 1、cognition candidate 3、fact-checker 1、cognition judge 1、writer 1、cold-reader 1，共 11；盲区检查并入 judge。
- 此项 verdict：`pass`。首次 Standards 的“10—11 / 11 双措辞”非阻断余量已关闭。

## 2. Skill 条件事实核查链

### 触发与 request

- `skill-engine.md:51-53` 明确：只有外部事实时追加 fact-checker；mechanism 角色提交类型化 request；无外部事实为 `not-applicable`；有可见外部事实时列全 request claims，不论 materiality。
- `skill-mechanism-auditor.md:31,35` 提供 `request_id / status / requested_by / trigger_reason / claims / allowed_external_source_boundary`；required request 与 claim id 必须非空唯一。

### fact-checker 输出

- `fact-checker.md:26-35` 精确回填 request id，逐 check 提供唯一 check id、claim/candidate/anchor、kind、verdict、sources 与本次核实标志，并用 request/checked claim id 集合精确相等证明 coverage。
- 所有可见 request facts 均 supported 才可 pass；外部事实至少有一个本次定位的 high-trust 来源。

### judge 与持久化

- `skill-judge.md:10,29,37` 只在触发时要求完整事实结果，以 check/claim id 回交；任一 request claim 覆盖不完整即停止。
- `judge.md:13` 要求全部可见 request facts，不论 materiality；来源证明与条件事实核查分为两个子门。
- `orchestrator.md:30,42` 与 `run-manifest.md:56-63,84` 的 `source_and_fact` 七个顶层字段和两个子门同形；聚合 owner、状态、source provenance、conditional fact request、scope、evidence、conflicts 都有唯一 manifest 落点。
- `role-cold-start-fact-gate-rerun-4-raw.md` 的 scoped pass 与当前文本一致；此前失败 raw 保留。
- 此项 verdict：`pass`。首次 Standards 的“Skill fact-check 如适用”与嵌套 schema 问题已经关闭。

## 3. Blocker：共享 fact-checker 与图书候选仍是两套输入 schema

### 当前冲突

- 图书标准链固定包含一个 fact-checker；`book-engine.md:47-49` 要求它逐条检查候选外部事实、引文和因果断言。
- 图书候选合同 `cognition-candidate.md:29-32` 仍只输出每个 candidate 内嵌的 `facts_to_check`，字段为 `claim_id / candidate_id / anchor_id / claim_text / claim_type / conclusion_impact`；没有 `fact_check_request`、request id、request status、visible、allowed boundary 或 request-level claim 集合。
- 共享 `fact-checker.md:9` 的允许输入已经改为“上游角色提交的类型化 `fact_check_request`”；其输出又强制 `request_id: nonempty-request-id`，并要求输出 request id 精确引用输入 request。
- orchestrator 没有获权把 book 的三个实例 `facts_to_check` 临时合并并发明 request id；反而要求最小路由、唯一事实源和可追溯 handoff。当前也没有独立“book request assembler”角色或 schema。

### 直接影响

1. 有待核事实的 book candidate：fact-checker 收不到合同要求的 request wrapper，不能产生合规 request_id/coverage 输出。
2. 没有外部事实的 book candidate：fact-checker 合同仍要求非空 request id；标准 11 任务又固定包含 fact-checker，无法同时表达合法空/不适用执行。
3. cognition judge 的事实结果输入因此没有稳定上游，图书 11 任务数据流在事实门处重新悬空。

### 对 RI-P01 与 29/29 声明的影响

- 最新 `RI-P01.md:57-69` 把 `book-fact-checker-1` 记入 11 个已执行 dispatch；同一 manifest `:74-81` 又声明没有外部 fact request，条件事实门为 `not-applicable`。
- 最新 `regression-run-integrity-rerun-5-raw.md:181` 直接断言“标准 fact-checker dispatch 的存在不等于条件外部事实门一定被触发”，但没有解释该 dispatch 如何满足 fact-checker 强制 typed request 与 nonempty request id 的合同。
- 因此 RI-P01 不是当前所有合同同时成立时的合规正例；其 `accept-structure-only` 至少应为 `blocked`，直到 book candidate 与 fact-checker handoff 统一，或明确 book 无 request 时 fact-checker 的合法 no-op / not-applicable schema。
- 这使 suite 当前“RI 7/7、全套 29/29”汇总不能在 Standards 轴继续视为已验证。文件数量与 raw 齐备仍成立，但最新正例 verdict 的合同依据不成立。

### 严重度

- severity：`blocker`。
- 理由：用户验收要求“角色图无悬空角色、schema 与协议/manifest 完全一致、29 case 最新 raw 有效”。当前同时违反前三项，且问题发生在标准图书固定任务，而不是可选边缘路径。
- 最小修复方向仅作定位，不在本次执行：让 book candidate 也输出统一 typed request（含多实例归并规则），或为 fact-checker 定义兼容 book facts_to_check 的明确输入与无 request 状态；随后重做 book 合同冷启动和 RI-P01 / RI 7 case 最新 raw。

## 4. 29 case 与最新 raw 的机械完整性

- case 数量：book 12、Skill 10、run-integrity 7，总计 29。
- 29/29 有独立结果与 raw 路由；最新 raw 标题数分别为 12、10、7。
- suite 和七张 RI 卡均指向 `regression-run-integrity-rerun-5-raw.md`；旧 raw 保留，没有覆盖失败历史。
- 最新 raw 文本中 mismatch/blocked 计数为 0；但这是文件内部声明，不抵消上节发现的跨合同 blocker。
- verdict：`fail`（语法/数量齐备，语义有效性因 RI-P01 blocker 失败）。

## 5. 引用、行数、角色规则、模板

- 从 29 cards 与 suite 提取 100 个唯一直接本地引用：无缺失路径，无显式行号超过文件总行数。
- `SKILL.md` 97 行；book/judge/skill protocols 为 77/60/76 行；角色文件最长 48 行。
- 角色 numbered behavior rules 检查无文件超过 7；职责/禁令仍保持裁剪合同规模。
- 三个读者模板移除 HTML 注释后，生产词扫描无可见命中。
- verdict：`pass`。

## 6. Dirty worktree 边界与机械检查

- `HEAD` 仍为 `1ed34c4`；工作区非干净，未发现本轮删除或移动旧 022/Demo 文件。
- tracked 修改、当前返工 untracked 文件与 B 组旧产物仍可按 `change-set-boundary.md` 分开；新事实门 raw、RI rerun-3/4/5、Spec raw 与本 rerun raw均落在 A 组 `v3/eval/constraint-redesign-r2/`。
- calibration 末尾已更新为 RI-P01 11 实例、嵌套事实门及最终 rerun-5 的限定说明，没有声称真实运行。
- `git diff --check`：exit 0。
- verdict：`pass`。

## 最终 verdict 与可声称范围

- blocker count：`1`。
- final Standards verdict：`fail`。

可以声称：

- 精确图书 11、Skill 条件 fact request、ID/coverage/high-trust、Skill judge 回交以及 orchestrator/manifest 嵌套持久化各自已补齐。
- 29 cards、raw 文件、引用、行数、合同裁剪、模板、dirty 边界和 diff whitespace 的机械检查通过。

不可以声称：

- 当前图书 11 任务事实门已形成可执行 handoff。
- RI-P01 是所有现行合同同时成立时的合规结构正例。
- run-integrity 7/7 或全套 29/29 已获得最终 Standards 有效通过。
- Standards 轴通过、双轴验收通过、真实 run/内容/用户体验/Phase 4/V3 通过。
