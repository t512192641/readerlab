# 主控合同独立输入 / Schema 审查原始输出

## 审查身份与读取边界

- 时间：`2026-07-10T07:04:59-04:00`。
- 审查对象：`v3/skill/roles/orchestrator.md`、`v3/skill/roles/README.md`、`v3/skill/templates/run-manifest.md`。
- 本切片实际读取：仅上述三个文件。
- 本切片明确未读：线路协议、其他角色合同、约束架构、回归 case、回归 suite、旧主控审查结果和真实 run 产物。
- 此前上下文如实声明：本执行者在同一会话的前一个切片做过 Skill 回归 case 审查，曾读取 `AGENTS.md`、`v3/current-task.md`、Skill 回归卡、Skill 裁判 / rubric / engine 和 case 路由的历史 evidence。因此这不是严格意义上的“从未接触过仓库的零上下文 Agent”。为避免污染，本次所有判断和证据只引用本节列出的三个审查对象；此前内容不作为本次合同通过依据。
- 审查性质：静态输入 / schema 冷审查，不是 run 执行，不生成内容，不调用角色，不验证真实 dispatch。

## 总结论

- overall verdict：`fail`。
- 不是 `blocked`：三个指定文件足以判断 schema 是否闭合。
- 通过部分：主控任务、边界保护和禁止自评的方向清楚；run 顶层 `status` 与 `mode` 枚举一致；角色索引在静态计数上列齐图书 11 个标准执行实例和 Skill 5 个标准执行实例。
- 失败部分：主控输出与 manifest 之间没有可执行的一一映射；线路、dispatch、gate、claim 和 run 状态转换存在缺字段或枚举缺口。当前合同能描述“主控应该做什么”，但不能仅凭其结构化输出证明“每个实例已正确分发、每个必需门已结算、manifest 与主控状态未漂移”。
- 可声称范围：可声称“静态角色清单覆盖 11 / 5，部分顶层枚举一致”；不可声称“主控合同 schema 已闭合”“能够无歧义驱动或审计完整 run”“角色图已通过冷启动执行验证”。

## 1. 主控任务与权责边界

- verdict：`pass_with_gap`。
- 实际证据：`orchestrator.md` 把任务定义为按线路、模式和预算分发最小上下文，保护运行边界并汇总独立验收；核心职责要求先锁线路、fresh/revision、来源、隔离输出、复用、任务上限和声明范围；禁令阻止主控生产内容或把局部通过升级为整线通过。
- 正面判断：方向与所有权基本闭合。主控负责调度与汇总，生产和独立判定留给专门角色；停止条件覆盖未声明来源 / 模式、样本影响结论、超预算、工作区冲突和未经确认的真实生成 / 重跑。
- 主要缺口：合同没有定义“哪些 gate 对哪条线路 / 模式是必需的”，也没有定义主控把独立结果转换成 `accepted`、`failed` 或 `awaiting-user` 的状态转换规则。因此职责文字清楚，但最终裁决算法没有闭合。
- 影响：两个主控可基于同一组 dispatch 与 gate，给出不同 run status，仍都能声称遵守合同。

## 2. 输入闭合性

- verdict：`partial`。
- 实际证据：允许输入包含当前任务、约束架构、当前线路协议、run manifest、各角色结构化交付、独立验收结果和当前运行证据。
- 正面判断：主控所需的主要信息类别已经被点名，且 run manifest 具备来源、样本、复用、输出、预算、阶段、验证和声明字段。
- 主要缺口：主控的结构化输出没有 `manifest_id` / `manifest_path` / `run_id` 引用，`run.source` 和 `run.output` 又被压成字符串。无法从主控输出证明它汇总的是哪一份 manifest，也无法防止来源、输出目录或状态在两份记录间漂移。
- 次要缺口：主控职责要求先锁定“允许复用项、样本确认和声明范围”，但结构化输出没有对应的 `reuse`、`sample` 或完整 `claims` 字段；它只能依赖未被显式关联的外部 manifest。
- 可声称范围：可以说“允许输入列表足以让人工主控开始工作”；不能说“主控输出自带完整、可追溯的输入快照”。

## 3. 线路与 material type 映射

- verdict：`fail`。
- 实际证据：主控输出的 `run.line` 只允许 `book | skill`；manifest 没有 `line` 字段，只有 `source.material_type: book | longform | skill | engineering | mixed`。
- 主要理由：这两个字段不是同一枚举，也没有在三个文件中定义映射。`book` 与 `skill` 看似可直接映射，但 `longform`、`engineering` 和 `mixed` 如何选择线路、是否拆分、由谁停止或确认均没有 schema 规则。
- 风险：同一份 `mixed` manifest 可被主控静默写成 `book` 或 `skill`；审计者无法仅凭结构判断这是正确路由还是跨线。
- 最小闭合要求：manifest 显式记录 `line: book | skill`，或合同冻结 `material_type -> line` 映射与 `mixed` 的分拆 / 停止规则；主控输出同时引用同一 run manifest。

## 4. Run 顶层枚举一致性

- verdict：`partial`。
- 一致项：
  - `mode`：主控与 manifest 都是 `fresh | revision`。
  - `status`：主控与 manifest 都是 `planned | running | failed | awaiting-user | accepted`。
- 未闭合项：
  - 主控 `task_cap` 对应 manifest `budget.task_limit`，但没有声明这是同一字段的别名。
  - 主控 `source: ""` 对应 manifest 的结构化 `source` 对象；主控 `output: ""` 对应 manifest 的结构化 `output` 对象；压平后丢失 fingerprint、actual read scope、隔离目录与防回写字段。
  - 主控 `claim_scope: []` 不能无损表达 manifest 的 `can_claim`、`cannot_claim`、`reused_results_only`、`awaiting_user_acceptance` 四种不同状态。
- 状态转换缺口：三个文件没有规定从 `planned` 到 `running`、`awaiting-user`、`failed`、`accepted` 的必要条件，也没有规定 dispatch `blocked`、gate `blocked`、用户体验 `pending` 分别映射到哪个 run status。
- 影响：虽然字符串枚举相同，语义仍可能不一致；尤其 `accepted` 没有机器可审计的进入条件。

## 5. Dispatch schema 闭合性

- verdict：`fail`。
- 当前 schema：`dispatches: [{role, inputs, expected_output, status}]`，status 为 `pending | running | done | blocked | failed`。
- 正面判断：它至少记录角色、输入、预期输出和任务状态，能表达一次最小分发。
- 关键缺口：
  1. 没有 `dispatch_id` 或 `instance_id`。图书线有 2 个 `anchor-nominator` 和 3 个 `cognition-candidate` 实例，仅靠重复 `role` 无法稳定区分、引用或证明实例数。
  2. 没有 `line`、`stage`、依赖 / 前置 dispatch、实际输出位置或实际证据字段。`expected_output` 不等于真实交付，`done` 也无法证明产物在哪里。
  3. 没有 gate owner / next gate 绑定，无法从 dispatch 判断该交付应由哪个独立角色验收。
  4. dispatch status 与 manifest `stages.executed / skipped / failed / reused_without_rerun` 没有映射。`done` 是否进入 `executed`、`blocked` 是否进入 `failed`、被复用任务是否建立 dispatch，均未定义。
  5. 没有任务计数规则，无法证明 `budget.actual_tasks` 与 dispatch 数量、重复实例或合并任务一致。
- 影响：静态索引虽然列出了标准实例数，实际 run 仍可能少发一个提名者 / 候选者、重复计数、把复用写成执行，主控输出本身无法发现。
- 最小闭合要求：给每次分发增加唯一实例标识、线路 / 阶段、输入边界、实际输出 / 证据、依赖、验收门，并定义 dispatch 到 `stages` 和预算计数的映射。

## 6. Gate schema 与 manifest 枚举一致性

- verdict：`fail`。
- 当前主控 gate：`gates: [{name, evidence, verdict}]`，verdict 只允许 `not-run | pass | fail | blocked`。
- manifest gate：
  - `source_and_fact`、`absolute_value`、`regression`、`run_integrity` 使用 `not-run | pass | fail | blocked`；与主控枚举一致。
  - `cold_read`、`cold_start_or_reproduction` 额外允许 `not-applicable`；主控无法表示。
  - `user_experience` 使用 `not-requested | pending | pass | fail`；主控无法表示 `not-requested` 或 `pending`，也无法区分它们与 `not-run` / `blocked`。
- 名称缺口：主控 `name` 是任意字符串，没有冻结成 manifest 的七个 verification key，也没有要求每个适用 key 恰好出现一次。因此漏门、重名门或同义词漂移都不会被 schema 拦住。
- 证据缺口：gate 只有 `evidence` 与 verdict，没有 `required | optional | not-applicable`、验收角色、覆盖对象 / 链段和冲突字段；无法计算哪些门是 `accepted` 的必要条件。
- 影响：合法 manifest 可能无法无损转换成主控 gate 输出；主控也可能遗漏 manifest gate 却仍把 run 标为 `accepted`。
- 最小闭合要求：gate 名称冻结为 manifest verification keys；各 key 使用与 manifest 相同的专属枚举，或定义无损总枚举及转换表；同时记录适用性、验收主体和覆盖链段。

## 7. 角色索引：图书 11 个实例

- verdict：静态覆盖 `pass`；可执行实例化 `fail`。
- 静态计数：
  - 一手主体 1
  - 锚点搜索 2
  - 锚点归并 1
  - 候选生产 3
  - 共用事实复核 1
  - 绝对裁判 1
  - 成文与最终页面装配 1
  - 无上下文冷读 1
  - 合计：`1 + 2 + 1 + 3 + 1 + 1 + 1 + 1 = 11`
- 所有阶段都有索引条目，且 README 末段分别指明事实可靠、认知价值、成文与好读的责任主体。
- 缺口：主控 dispatch 没有实例 id，无法证明 2 个锚点提名者和 3 个候选生产者是五个独立实例；也没有 stage / gate 映射，无法仅凭主控输出证明 11 个实例全部完成且各自被正确验收。
- 边界：共用 `orchestrator` 不计入图书 11；计入后是 12 个运行角色实例。README 中 `fact-checker` 标为“共用”，但最终责任说明明确把图书事实可靠交给它；三个文件没有进一步说明它在 Skill 标准五任务中何时追加。

## 8. 角色索引：Skill 5 个实例

- verdict：静态覆盖 `pass`；可执行实例化 `partial`。
- 静态计数：
  - 一手主体 1
  - 机制候选 1
  - 独立裁判 1
  - 读者成文 1
  - 独立冷读 / 冷启动 / 复现 1
  - 合计：`5`
- README 末段给出责任链：source integrator 证明来源、skill judge 判机制价值、skill writer 成文、cold-start reproducer 分门验证好读与可复用范围。
- 缺口：最后一个角色合同索引把冷读、冷启动、复现合在一个实例，但 manifest 将 `cold_read` 与 `cold_start_or_reproduction` 分成两个 gate；主控 schema 没有子任务 / 子门字段，无法证明同一实例分别产出两份独立结果，也无法表示其中一门 `not-applicable`。
- 额外歧义：`fact-checker` 被索引为“共用”，但标准 Skill 计数只列五个 Skill 实例；三个指定文件没有说明 Skill 出现外部事实时它是五任务内复用、条件追加还是由 source integrator 承担。静态五实例仍成立，但扩展时的预算和 dispatch 规则未闭合。
- 边界：共用 `orchestrator` 不计入 Skill 5；计入后标准运行至少有 6 个角色实例。

## 9. Run 接受与停止闭环

- verdict：`fail`。
- 已有保护：停止条件覆盖来源 / 模式未声明、样本会影响结论、预算突破、工作区冲突和未经确认的真实生成 / 重跑；manifest 也要求样本确认、隔离目录、实际阶段与 claim 交集。
- 未闭合点：
  1. 未定义 `accepted` 的必需 gate 集合和例外口径。
  2. 未定义 `awaiting-user` 与 manifest `sample.user_confirmation: pending`、`claims.awaiting_user_acceptance`、`verification.user_experience: pending` 的联动。
  3. 未定义 dispatch / gate 失败后 run 必须是 `failed`，还是允许 `awaiting-user` 修复。
  4. 未定义 revision 的复用阶段如何进入 dispatch、gate 和 accepted 计算。
  5. 未定义混合材料如何拆线、何时关闸，以及拆线后是一份还是多份 run manifest。
- 结论：停止原则存在，但没有形成确定性状态机；无法证明 run 状态与角色、gate、manifest 始终同步。

## 10. 最小修复清单（本次不修改）

1. 在 manifest 与主控输出之间建立唯一 run 引用，并冻结 `material_type -> line` 映射；单独处理 `mixed`。
2. 让主控输出引用或无损表达 manifest 的 source、sample、reuse、output、budget、stages、verification 与 claims，避免字符串摘要成为第二事实源。
3. 为 dispatch 增加唯一实例、线路 / 阶段、实际输出 / 证据、依赖、验收门和任务计数映射。
4. 将 gate 名与 manifest verification keys 对齐，并消除 `not-applicable`、`not-requested`、`pending` 的枚举缺口。
5. 冻结 run 状态转换表：各线路 / 模式的必需门、用户等待条件、失败处理、revision 复用和 `accepted` 进入条件。
6. 明确 Skill 第五实例如何分别输出 cold-read 与 cold-start / reproduction 两门结果，以及共用 fact-checker 在 Skill 扩展中的预算与调度规则。

## 最终可复核结论

- 主控任务：方向闭合，最终裁决规则未闭合。
- 允许输入：足以人工启动，但主控输出缺少 manifest 身份与无损引用。
- dispatch：不闭合。
- gate：不闭合，且与 manifest 存在直接枚举不一致。
- run status：字符串枚举一致，状态转换不闭合。
- 图书 11 实例：索引静态覆盖；主控 schema 不能证明独立实例化完成。
- Skill 5 实例：索引静态覆盖；第五实例的双门输出与条件 fact-checker 未闭合。
- overall：`fail`，需先修 schema 再声称主控合同通过冷启动输入审查。
