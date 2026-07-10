# ReaderLab V3 约束重构完整 Standards 终验复跑原始输出

## 审查身份与边界

- reviewed_at: `2026-07-10T12:08:29-04:00`
- fixed_point: `HEAD 1ed34c4`
- branch: `v3/cognitive-compounding`
- axis: `Standards`
- verdict_policy: `any blocker => fail`
- rules_cases_or_summaries_modified_by_reviewer: `false`
- real_fresh_or_revision_run_observed: `false`
- content_or_user_experience_observed: `false`

本次不是 scoped blocker 复核，而是按 `v3/current-task.md` 和用户 2026-07-10 的完整返工要求，重新审查当前工作区相对 fixed point 的全部相关改动。重点证据包括当前总则、两线协议、角色合同、manifest、29 张 case、RI rerun-9、book-routing-final、standards-blockers-rerun、Spec final rerun、document map、change-set boundary 与 git 事实。本文件只保存审查结果，不修改规则、case、suite、calibration 或 current-task。

## 总结结论

```yaml
axis: Standards
verdict: pass
blockers: 0
regression_cases: 29/29
run_integrity_cases: 7/7-derived-structure-only
runtime: not-run
```

用户最初点名的角色悬空、Skill 事实链、锚点合同、source map、状态枚举、成本、历史回归自证、原始结果缺失和 dirty 边界问题，以及后续完整终验发现的 typed fact handoff、全 0 路由、manifest gate 对象、document map 重叠和锚点归并判据问题，当前均已关闭。没有发现新的 Standards blocker。

本 verdict 只表示“约束架构与回归证据包通过当前完整 Standards 静态终验”。它不表示真实图书线、Skill 线、内容质量、用户体验、Phase 4 或 ReaderLab 流水线通过。

## 1. 总原则、分线规则与上下文分发

结果：`pass`。

- constraint architecture 保留五条总原则，图书两条专属规则、Skill 两条专属规则和固定冲突优先级；同一细则按生产、表达、淘汰或验收主责归档。
- 主控读取总则、当前线路协议、judge 与 manifest；执行 Agent 只读取本线路两条规则摘录、自己的短合同和任务输入，不加载另一线路或全套历史。
- 回归样本只由裁判 / 回归执行者按 case 路由；作者、提名、候选、成文和冷读角色不得读取历史答案。
- V3 保持纯 Prompt / Markdown；没有新增生成用 Python、依赖或旧 validator 入口。

## 2. 图书角色图、盲区与成本

结果：`pass`。

- 标准无早停计划可精确重建为 11 个实例任务：source map 1、anchor nomination 2、anchor merger 1、cognition candidate 3、fact-checker 1、cognition judge 1、book writer 1、cold-reader 1；主控不计。
- 盲区检查由 cognition-judge 在同一任务先执行，不存在悬空的第 12 个盲区角色。
- 每阶段都有唯一生产 / 判断主体、结构化输出、停止或回交路径；writer 只表达锁定包，不能重新选题或加料，cold-reader 不接触生产上下文。
- 11 是无早停计划，不是可见数量或实际计费配额；skipped dispatch 不计 actual_tasks，扩容和超预算均有触发与用户确认门。

## 3. 锚点提名与归并

结果：`pass`。

- anchor-nominator 每条提名直接给出原文位置、承重理由、容易怎样读浅 / 读偏、值得调查的认知问题、论证联系和置信度。
- anchor-merger 的短合同现直接以“是否在解决同一个认知问题”作为归并判据，与 book protocol 一致，不再退化为按论证位置或论证任务去重。
- 输出保留全部 source locators、merged-from 关系、investigation question、context links 与少数派高潜标志；单方发现不因票数自动淘汰。
- `role-cold-start-book-routing-final-raw.md` 用“同位置不同问题不得合并、不同位置同问题可以合并”的最小输入完成冷启动，Chain A 为 pass。

## 4. 图书 typed request、批量事实核查与逐候选淘汰

结果：`pass`。

- 三个 cognition-candidate 实例分别输出统一 typed `fact_check_request`；有候选时 request / claim id 非空唯一，列全必要的源内、外部、事实和因果断言，并保存 candidate、anchor、kind、assertion type、materiality、visible、已有来源与取证边界。
- 一个 fact-checker 可批量接收多份 request；输入 request id 集合、逐 claim check、per-request coverage 和 batch overall 有确定映射，non-material 可见事实也不能漏检。
- check id 稳定唯一，kind / assertion type / materiality 与原 claim 一致；外部 supported 要求本次定位的 high-trust 来源，源内事实回登记原材料。
- `conflicted / insufficient / out_of_scope` 作为逐候选淘汰证据，不把已完整执行的 fact-checker 任务误判失败，也不让一个坏候选拖死同批其他候选。
- blocked reason、return-to 与 minimal correction 能表达停止和最小回交，不需主控发明影子 request 转换。

## 5. 图书三个 candidate 全 0 路径

结果：`pass`。

- 三个 candidate 实例各自实际提交可审计的合法 0 报告、request N/A 与 zero reason；不把漏跑、失败或 blocked 冒充 0。
- required request 集合为空时，只有 fact-checker skipped；conditional fact child gate 为 N/A，request refs 为空，fact-checker 不计 actual_tasks。
- cognition-judge 仍读取三份 0 报告与锚点，实际执行盲区检查；无遗漏时结算 absolute value pass、selection count 0。
- book-writer 仍以正文和 source map 装配正文-only 页面；reader units / insertions 为空，不使用落选材料填充。
- cold-reader 仍实际检查最终 body-only 页面并返回 `not-applicable`，不是 skipped 或 not-run；输入污染时可 blocked。
- `role-cold-start-book-routing-final-raw.md` 的 Chain B 将账本重建为 11 planned、10 done、1 fact-checker skipped、actual_tasks 10，整体 pass。较早 raw 中 writer / cold-reader 可 skipped 的错误句只保留为失败演进证据。

## 6. Skill 3—5 任务角色所有权

结果：`pass`。

- 标准 5 任务依次由 source integrator、mechanism auditor、skill judge、skill writer、cold-start reproducer 拥有。
- 来源 / 候选生产与独立裁判分离，成文与独立冷读分离；简单材料降到 3—4 任务时也不能由生产者或成文者自评闭环。
- 最后一个角色先冷读最终读者页，再执行适用的冷启动或复现，两种结果分别记录；资产卡、局部机制、阅读体验和完整复现不能互相升级。
- 外部事实只在候选实际引入时追加共用 fact-checker；如果突破标准 5 任务，需说明触发原因并先获用户批准。

## 7. Skill source map、事实链与页面职责

结果：`pass`。

- source integrator 为每个可见单元保存全部来源、retained / moved / merged / reordered、实际 treatment；重要删除另存 source refs、类型、理由和 appendix / technical-lead / audit / omitted 去向。
- mechanism auditor 的可见外部事实使用统一 typed request；无外部事实明确 N/A。主控只按 request 派 fact-checker，skill judge 在裁判前逐 check id 核对完整覆盖。
- 主读页只装配可追溯净化正文；技术负责人页只讲锁定机制、取舍、失败和迁移边界。skill writer 保存 source map、rendered body、unchanged 与 verification 证据。
- 独立读者能分别表达阅读体验、冷启动和复现的 pass / fail / blocked / N/A / not-run 范围。

## 8. 状态枚举、manifest 和唯一事实源

结果：`pass`。

- 生产和裁判角色可表达 `not-run / pass / fail / blocked`；条件事实、冷读和冷启动另有适用的 `not-applicable`，输入污染统一 blocked。
- manifest 与 orchestrator 的七个 verification gates 逐字段同形。适用 gate 均有 status、owner、scope、evidence、conflicts；user experience 同形为 status、owner、scope、evidence。
- source-and-fact 另保存 source provenance 与 conditional fact check 两个子门，主控只做确定性聚合；全部字段直接写入唯一 manifest，无第二状态源。
- route 可表达 unassigned / book / skill 和 mixed parent 拆 child runs；dispatch / instance id、stages 和 actual_tasks 有确定映射。
- 样本确认的合法组合和 planned / running / awaiting-user / failed / accepted 转换均与对象 schema 一致；状态文字已读取 `verification.user_experience.status`。
- `review-standards-blockers-rerun-raw.md` 对以上三项原 Standards blocker复核为 3/3 closed；本次完整交叉检查结果一致。

## 9. 独立验收门和真实运行完整性

结果：`pass`。

- 来源事实、绝对价值、回归、冷读、冷启动 / 复现和真实运行完整性由不同证据主体结算，不能靠平均分或局部通过互相抵消。
- fresh 必须从登记原始材料开始、零生成产物复用、使用全新隔离目录；旧 URL 只能作线索，本次重新定位核实。
- revision 必须列明基线、复用、实际重跑、未重跑和不可声称范围。
- 样本影响能力结论时先经用户确认；pending / declined 或字段组合无效时不得 dispatch。
- audit 保存来源、运行、复用、候选、事实、裁判与门证据；can-claim 只能覆盖实际执行和对应独立门通过的交集。

这些条款形成了可执行的静态门，但本轮没有真实通过该运行门。

## 10. 历史回归与派生结构证据

结果：`pass`。

- case 总数 29：16 historical、13 derived-structure。
- 图书 12 张全部为 historical：B-P01—B-P03 只保护原证明范围，B-N01—B-N09 继续 reject。
- Skill 10 张为 4 historical + 6 derived-structure；S-N01—S-N06 明确无历史样本，不把当前规则写成历史证据。
- run-integrity 7 张全部为 derived-structure、historical-run false，不冒充真实运行。
- 每张 case 都有具体输入、证据路由、expected、独立 actual 和 scope；没有 pending、blocked 或 mismatch。suite 不用汇总 expected 代替逐卡判断。

## 11. B-N07 与历史判词诚实性

结果：`pass`。

- B-N07 明确旧 R1 audit 当时是 waiting，不能自证通过。
- case 与 book regression raw 路由到 calibration 中后来的真实用户否定：四段离对应原文太远、像新增阅读材料、读者仍需整理，因此未过体验门。
- 没有逐字用户原话时明确写无，不把后续摘要伪造成引号原话；B-N09 等受顺序污染或局部证据只拒绝当前证明范围，不扩大成永久无价值。

## 12. 独立原始输出与最新回归

结果：`pass`。

- 图书、Skill、主控、事实门和 fact handoff 均保留首次失败及定向复跑；最终 pass 没有覆盖失败演进。
- 锚点归并和全 0 路由由新的 `role-cold-start-book-routing-final-raw.md` 完整复核。
- 图书历史回归为 12/12，Skill 为 10/10。
- `regression-run-integrity-rerun-9-raw.md` 按当前统一 gate 对象重跑 7 张 RI：六个负例继续 reject，RI-P01 为 accept-structure-only，7/7、0 blocked。
- RI-P01 含 11 个唯一 dispatch、三份 request、三条 check、三条精确 coverage、嵌套 source/fact gate 和全部统一 gate 对象；claims 明确排除真实 run、内容、用户体验和完整能力。
- 总计 29/29 与限定预期匹配；所有 RI 仍是 `runtime-not-run`。

## 13. 默认入口和文档生命周期

结果：`pass`。

- V3 默认启动仍只有 `AGENTS.md + v3/current-task.md`；README 只提供稳定概览，不复制当前进度。
- document map 将文件放入 current-authority、routed-evidence、retired-preserved 三类，并给出读取条件、禁止扩大和替代入口。
- 当前 raw 由 regression suite、calibration 或 final review 明确引用；未被当前汇总引用的旧 raw 才进入 retired preserved，两集合互斥，不按文件名猜最新。
- examples 自身 README 进一步限制为认知裁判 / 回归 case 路由，历史答案不向普通生产角色回流。
- 022 R1/R2、audit 与历史 Skill 样本保留为 routed evidence；一次性提示、旧设计合同、旧 review prompt 和版式 Demo 已退出执行层。没有删除、移动或重命名历史文件。

## 14. 引用、行数、角色裁剪和模板

结果：`pass`。

- 当前入口、规则、协议、角色、suite 和 29 cards 的直接 `v3/` 文件引用均可定位；未发现显式行号超过目标文件长度。
- `v3/current-task.md` 49 行，不超过 60；`SKILL.md` 97 行，不超过 300。
- book / judge / skill protocols 为 77 / 60 / 76 行，保持短协议目标。
- 角色合同最长 48 行；每份均为 3 条核心职责 + 2 条禁令，共 5 条行为规则，不超过 7。
- 三个读者模板移除 HTML comments 后只剩读者标题 / 槽位，没有 candidate、judge、audit、manifest 等生产结构作为可见文本。
- 未发现活动规则中的旧 `not_run`、`test_invalid`、`28/29` 或 RI rerun-8 最新结果引用。

## 15. Dirty worktree 与可分离变更边界

结果：`pass_with_caution`。

- 当前分支为 `v3/cognitive-compounding`，HEAD 为 `1ed34c4`；工作区仍有 tracked 修改和大量基线外 untracked 文件，没有独立提交。
- `change-set-boundary.md` 将约束返工 A 组与旧 022 R1/R2、候选 audit、版式 Demo、一次性提示和旧设计合同 B 组分开。
- calibration 与 Phase 4 gate 在返工前已有未提交 hunk；未来若形成提交必须逐 hunk 暂存，不能整文件归因本轮。
- 本审查没有 reset、checkout、删除、移动、暂存、提交或覆盖旧产物。

该 caution 不阻塞当前文档级返工验收；它只说明“可分开审查”，不能声称工作区已干净或已物理形成变更集。

## 16. 机械检查

结果：`pass`。

```yaml
git_diff_check: pass
current_task_lines: 49
skill_lines: 97
book_protocol_lines: 77
judge_protocol_lines: 60
skill_protocol_lines: 76
role_behavior_rules_max: 5
case_files: 29
historical_cases: 16
derived_structure_cases: 13
latest_ri_cases_matched: 7/7
```

## 最终 Standards verdict 与声明范围

```yaml
axis: Standards
verdict: pass
blockers: 0
runtime: not-run
```

当前可以声称：

- ReaderLab V3 约束架构返工、角色合同、历史 / 派生回归证据包和真实运行完整性结构门通过完整 Standards 静态终验。
- 29 张 case 与限定预期匹配；RI 7/7 只证明 derived structure。

当前不能声称：

- 真实 fresh / revision 已发生。
- 真实事实来源、图书或 Skill 内容质量、冷读结果、用户体验、图书线、Skill 线、Phase 4 或 ReaderLab 流水线已经通过。
- 本审查本身授权开始 Demo、Phase 5 或 LifeAtlas 回写。

最终结论：`pass`，0 blocker，`runtime-not-run`。
