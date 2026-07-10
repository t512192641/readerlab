# 2026-07-10 约束重构返工：完整 Spec 终验复跑原始输出

## 审查身份与边界

- reviewed_at_utc: `2026-07-10T16:04:42Z`
- reviewed_at_local: `2026-07-10T12:04:42-04:00`
- axis: `Spec`
- verdict_policy: `any blocker => fail`
- fixed_point: `HEAD 1ed34c4`
- branch: `v3/cognitive-compounding`
- real_run_performed: `false`
- content_generated: `false`
- rules_cases_or_summaries_modified_by_reviewer: `false`

本次不是 scoped blocker 检查，而是按用户 2026-07-10 的整份返工要求重新做完整 Spec 终验。本审查者做过前次 Spec 验收和锚点 / 全 0 路由限定冷启动，因此不是零上下文；当前 verdict 只依据重新读取的现行规则、case、最新 raw、文档分类和 git 证据，不用旧个人结论替代检查。本文件只保存审查结果，不修改规则、case、suite、calibration 或 current-task。

## 总 verdict

```yaml
axis: spec
verdict: pass
blockers: 0
requirement_groups_passed: 15
matched_regression_cases: 29/29
run_integrity_cases: 7/7
runtime: not-run
```

用户点名的角色调度、锚点问题、Skill source map、状态、历史证据、独立原始输出、事实 handoff、全 0 路径、RI 正反例、成本、文档分类、dirty 边界和声明范围现均闭合。此前 Spec 终验发现的锚点归并 blocker 已由当前角色合同与新冷启动关闭；没有发现新的 blocker。

本结论只表示“约束架构与回归证据包通过当前完整 Spec 静态终验”。`runtime-not-run`：它不表示图书线、Skill 线、Phase 4、用户体验或 ReaderLab 流水线真实通过。

## 1. 图书角色图、盲区与成本

- 盲区检查归入 cognition-judge 的同一任务：先检查会改变结论的遗漏，再做绝对裁判；不新增第 12 个任务。
- 标准无早停计划可从 roles index 无损重建为 11 个实例级任务：source map 1、nominator 2、merger 1、candidate 3、fact-checker 1、judge 1、writer 1、cold-reader 1；主控不计入。
- 11 是无早停计划，不是可见内容或实际计费配额。skipped dispatch 不计 `actual_tasks`，不得为凑数制造空核查。
- 短文 5—7、深读 15—18 与 manifest 预算上限有明确位置；扩容需要已声明触发，超预算须用户同意。

结果：`pass`。这只证明静态调度与成本合同，不证明 11 个 Agent 已真实运行。

## 2. 锚点提名与按认知问题归并

- anchor-nominator 的每条提名直接包含原文定位、`likely_shallow_or_wrong_reading` 和 `investigation_question`，不再只找论证结构。
- anchor-merger 当前短合同已直接写“按是否在解决同一个认知问题”归并，与 book protocol 逐字一致；不依赖执行 Agent 读取完整协议。
- merger 输出保留 `investigation_question`、全部 source locators、`merged_from`、context links 与少数派高潜标记；单方发现不因票数淘汰。
- `role-cold-start-book-routing-final-raw.md` 用“同位置不同问题不得误合并、不同位置同问题允许合并”的最小场景复核，Chain A 为 pass。

结果：`pass`。前次 `SPEC-F01` 已关闭。

## 3. 图书 typed fact request 与完整 handoff

- 三个 candidate 实例各有独立 instance id；有候选时直接提交 required typed request，request / claim id 非空唯一。
- 每条 claim 保存 candidate、anchor、kind、assertion type、materiality、visible、已有来源与允许外部取证边界；因果与来源类型不靠主控临时映射。
- 单一 fact-checker 批量接收一份或多份 request，request id 集合精确相等；每条 check 有稳定唯一 id，并保留 request/claim/candidate/anchor 关系。
- 每个 request 独立记录 request claims、checked claims、material claims 与 complete；所有可见事实均覆盖，不因 non-material 跳过。
- batch overall 只结算核查任务的 schema / coverage /证据质量；`conflicted | insufficient | out_of_scope` 交给 judge 逐候选淘汰，一个坏候选不拖死其他候选。
- fact-checker 的 `blocked_reason / return_to / minimal_correction` 能表达停止与最小回交；外部 supported 要求本次定位的 high-trust 来源，源内事实回登记原始材料。

结果：`pass`。request → check → per-request coverage → batch overall → conditional fact subgate → judge 的链段不再需要主控发明影子转换。

## 4. 图书三个 candidate 全 0 路径

- 三个 candidate 实例各自实际运行并提交合法 0 报告：`candidates: []`、request N/A、`zero_candidate_reason`，不把漏跑冒充 0。
- required request 集合为空时，只有 fact-checker skipped；条件事实子门为 N/A、request refs 为空，且 skipped 不计任务。
- cognition-judge 仍收到三份 0 报告与锚点证据，实际执行盲区检查；无盲区时以 status pass、selection count 0 结算 absolute value pass。
- book-writer 仍实际装配正文-only 页面，reader units 和 insertions 为空，正文完整性有验证槽；不得以落选材料填充。
- cold-reader 仍实际检查最终正文-only 页面，结果为 `not-applicable`，不是 skipped 或 not-run；页面污染时应 blocked。
- `role-cold-start-book-routing-final-raw.md` 的 Chain B 重建 11 planned、10 done、1 fact-checker skipped、`actual_tasks: 10`，整体 pass。

结果：`pass`。较早 raw 中关于 writer / cold-reader 可 skipped 的句子已被当前合同和最终冷启动取代，只保留为失败演进证据。

## 5. Skill 3—5 任务角色所有权

- 标准 5 任务所有权明确：source integrator 生产净化正文/source map；mechanism auditor 生产机制候选；skill judge 独立裁判；skill writer 成文；cold-start reproducer 独立冷读并执行适用冷启动/复现。
- 简单材料可合并为 3—4 个任务，但生产者不得自评裁判通过，成文者不得自评冷读通过；任务合并不消除独立验收主体。
- 外部事实只有候选实际引入时追加共用 fact-checker；突破 5 个任务必须解释触发并取得用户批准。
- reader cold read 与 cold-start/reproduction 在同一独立角色内仍分开记录，局部通过不能升级为完整复现或真实运行。

结果：`pass`。不存在用图书 cold-reader 或 cold-start reproducer 互相冒充的悬空职责。

## 6. Skill source map 与页面职责

- 每个可见单元记录全部来源、retained/moved/merged/reordered 动作和 treatment。
- 删除记录独立包含 source refs、类型、理由与 appendix / technical-lead / audit / omitted 去向。
- 关联模板、脚本和参考资料有独立身份，不冒充正文。
- 主读页只承载净化正文；技术负责人页承载机制、取舍、失败与迁移边界；writer 有 source map、rendered body 和 unchanged verification 出口。

结果：`pass`。schema 能承载协议强制证据；没有据此声称真实净化正文已经生产或验证。

## 7. 状态枚举、manifest 与主控唯一事实源

- 生产 / 裁判整体状态可表达 `not-run | pass | fail | blocked`；冷读、冷启动和条件事实门另有语义明确的 `not-applicable`。
- manifest 与 orchestrator 的七个 verification gates 当前逐字段同形：适用 gate 有 status、owner、scope、evidence、conflicts；user experience 同形为 status、owner、scope、evidence。
- source_and_fact 另保存来源证明与条件事实核查两个子门，主控只做确定性聚合；没有第二份影子状态源。
- route 能表达 unassigned/book/skill 与 mixed parent 拆 child runs；dispatch id / instance id、stages、actual_tasks 有确定映射。
- 样本确认合法组合、planned/running/awaiting/failed/accepted 转换以及 `.status` 读取均与对象 schema 一致。
- `review-standards-blockers-rerun-raw.md` 对 gate 同形和状态文字复核为 pass；本次直接交叉检查未发现新冲突。

结果：`pass`。

## 8. 历史回归与派生结构分类

- case 总数 29：16 historical、13 derived-structure。
- 图书 12 张均为 historical；三张正例只保护原证明范围，九张负例继续淘汰。
- Skill 10 张中 4 historical、6 derived-structure；派生 S-N01—S-N06 明确没有历史样本，不冒充历史重放。
- run-integrity 7 张全部为 derived-structure、`historical_run: false`；只检查当前合同可表达性。
- suite 要求逐卡 actual、证据与 scope，任一 blocked / mismatch 即整门失败；没有用汇总 expected 代替实际执行。

结果：`pass`。

## 9. B-N07 与历史证据诚实性

- B-N07 case 明确区分旧 audit 的 `waiting` 与后来真实用户否定。
- 后续结论定位到 calibration：四段离原文太远、像新增阅读材料、读者仍需整理，因此未过体验门。
- book regression raw 实际使用该后续否定覆盖旧 waiting，并明确无逐字用户评价，不能补写伪原话或把内容事实判错。
- 其他历史卡同样保留证据缺口：批次级结论、缺逐字返回、重复曝光或受顺序污染时均收窄可声称范围。

结果：`pass`。历史证据不是本轮新规则的循环自证。

## 10. 独立角色冷启动与回归原始结果

- 图书、Skill、主控、事实门与图书 fact handoff 都保存首次失败和连续定向复跑；没有用最终 pass 覆盖旧失败。
- 最新锚点与全 0 角色路由有独立 `role-cold-start-book-routing-final-raw.md`。
- 图书历史回归原始结果为 12/12；Skill 为 10/10；run-integrity 最新 rerun-9 为 7/7。
- 专项 raw 都明确静态 / derived / historical replay 的边界；旧 scoped pass 不被单独当作整链通过，本次完整 Spec 直接复核其组合结果。

结果：`pass`。

## 11. RI-P01、RI rerun-9 与 29/29

RI-P01 当前自包含 fixture 具备：

- 合法 book route、原始路径 / 指纹 /读取范围、样本组合、生成产物零复用和隔离输出。
- 11 个唯一实例级 executed dispatch、`actual_tasks: 11`、上限 12。
- 三份 typed request、三条 check、三条 per-request coverage、batch status 与停止回交字段。
- source provenance 与 conditional fact check 嵌套子门，以及所有验收 gate 的统一对象形状。
- can-claim 只接受合成 manifest 的 structure-only；cannot-claim 明确排除真实 fresh、内容、用户体验和 ReaderLab 全部能力。

`regression-run-integrity-rerun-9-raw.md` 重新按当前统一 gate schema逐卡判断：六张负例继续 reject，RI-P01 为 accept-structure-only，7/7 匹配、0 blocked。加上 book 12/12、Skill 10/10，总计 29/29。

结果：`pass`。所有 RI 仍为 `runtime-not-run`；fixture 内的 pass / evidence 引用不证明背后真实文件或 Agent 执行。

## 12. 文档生命周期分类与默认入口

- default startup 仍只有 `AGENTS.md + v3/current-task.md`；README 是稳定概览，不维护动态状态副本。
- document-map 将文件分为 current-authority、routed-evidence、retired-preserved，并写明读取条件、禁止扩大与替代入口。
- 当前 raw 由 suite、calibration 或 final review 明确引用；未被当前汇总引用的旧 raw 才进入 retired-preserved，两类不再重叠。
- 022 R1/R2、audit、历史 Skill 样本继续是 routed evidence；一次性提示、旧设计合同、旧 review prompt 和版式 Demo 已退出执行层。
- examples 只在角色 / case 明确路由时读取，不向普通生产角色泄漏历史答案。

结果：`pass`。分类是身份与路由整理，不是物理移动或删除。

## 13. Dirty worktree 与可分离变更集

- 分支为 `v3/cognitive-compounding`，HEAD 为 `1ed34c4`；当前仍有 tracked 修改与基线外未跟踪文件，工作区不干净。
- `change-set-boundary.md` 将本轮约束返工 A 组与旧 022 R1/R2、候选 audit、版式 Demo、一次性提示和旧设计合同 B 组分开。
- 文档没有声称已经暂存、提交或物理归档；calibration 与 Phase 4 gate 未来仍须按具体 hunk 分离。
- 本轮没有 reset、checkout、删除、移动、暂存、提交或覆盖旧产物。

结果：`pass_with_caution`。可声称“可分开审查”，不可声称“工作区已干净分组”。该 caution 不阻塞本轮文档级返工验收。

## 14. 声明范围与真实运行完整性门

- fresh 必须从登记原始材料开始、零生成产物复用、全新隔离目录；旧 URL 只能作线索并重新定位核实。
- revision 必须列复用、实际重跑、未重跑和不可声称范围。
- 样本影响能力结论时必须先经用户确认；pending 时不得 dispatch。
- audit 保存运行、复用、事实、门结果和证据；声明只能覆盖实际执行与对应独立验收的交集。
- suite、calibration、新 raw、document map 与 change boundary 均明确没有真实 fresh/revision、内容生产、用户体验、Phase 4 或完整流水线。

结果：`pass`。真实运行完整性门已经可执行地写入合同与反例，但本轮没有实际通过该运行门。

## 15. 机械检查

- `git diff --check`: `pass`。
- case files: `29`。
- classification: `16 historical + 13 derived-structure`。
- `SKILL.md`: `97` 行，不超过 300。
- book / skill protocol: `77 / 76` 行，保持短协议目标。
- current-task: `49` 行，不超过 60；当前仍正确写“返工中、不得 Demo”，尚未提前升级。
- 未发现活动规则中的 `not_run`、`test_invalid`、旧 `28/29` 或旧 RI rerun-8 汇总引用。

结果：`pass`。

## 非阻断余量

1. dirty worktree 尚未物理形成独立提交；这正是当前边界文件明确保留的后续 staging 风险，不属于本轮要求的写操作。
2. 部分较早 raw 含已被后续合同修正的结论；document-map 已要求只使用当前汇总明确引用的 raw，旧文件保留失败演进，不可按文件名猜最新。
3. 本次通过不授权 Demo。current-task 只有在另一 Standards 完整终验也通过后，才能由主控更新为“等待用户复审”。

## 最终声明

可以声称：

- 约束重构返工满足用户当前 Spec；角色图、历史 / 派生回归证据和运行完整性结构包通过完整静态终验。
- 29 张 case 与限定预期匹配，其中 RI 7/7 仅为 derived structure。

不能声称：

- 真实 fresh/revision 已发生。
- 图书内容、Skill 内容、事实来源、用户阅读体验、图书线、Skill 线、Phase 4 或 ReaderLab 流水线已通过。
- 仅凭本 Spec pass 即可开始 Demo。

最终 verdict：`pass`，0 blocker，`runtime-not-run`。
