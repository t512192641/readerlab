# 来源与事实门修订后第二次 Schema 冷启动复核原始输出

## 复核身份与边界

- 时间：`2026-07-10T07:34:30-04:00`。
- 本次读取：`v3/skill/roles/skill-mechanism-auditor.md`、`fact-checker.md`、`skill-judge.md`、`orchestrator.md`、`v3/skill/templates/run-manifest.md`、`v3/skill/protocols/skill-engine.md`、`judge.md`。
- 本次按上一份失败 raw 的六项最小修复逐项复核：typed request / 触发主体、request/check id 与覆盖、结果回交、overall 映射与整门聚合、未触发状态、高可信 supported 与 owner。
- 本次未读：其他角色、回归 case / suite、真实 run 和旧事实门结果。
- 上下文声明：本执行者写过上一份事实门失败 raw；本次不是零历史上下文，但 verdict 只依据上述七份当前文件重新判断。
- 保留规则：上一份失败 raw 保留不改；本次不修改规则文件。

## 总结论

- overall verdict：`fail`。
- 实质修复：typed request、触发主体、material claim coverage、check_id 回交、高可信 supported、overall 映射、条件未触发、双子门聚合和最终 owner 均已写入合同。
- 剩余冲突一：request_id 与 check_id 虽新增字段，但没有冻结“required request 必须是非空唯一 id”“每个 request 内 check_id 唯一”，仍无法保证稳定引用。
- 剩余冲突二：orchestrator 定义了嵌套 `source_provenance / conditional_fact_check` 记录，manifest YAML 仍只有标量 `verification.source_and_fact`；manifest 文字要求子门状态与证据保存在“同一 manifest 的主控验收记录”，但模板中没有该记录字段。两个 schema 形状不能无损一致。
- 剩余冲突三：fact-checker 的 pass 只要求所有 material claims supported；judge 协议却要求所有可见外部事实回到高可信来源。non-material 外部事实若 insufficient / conflicted，当前仍可能 overall pass，且 Skill judge 不改写候选，可能把未支持的可见事实带入接受项。
- 按“仍有冲突必须 fail”的要求，本次不能判通过。

## 1. Typed request 与触发主体

- 当前生产者：`skill-mechanism-auditor`。
- request 字段：`request_id`、`status`、`requested_by`、`trigger_reason`、claims 的 `claim_id / candidate_id / text / kind / materiality / existing_source_refs`，以及 `allowed_external_source_boundary`。
- 触发规则：无外部事实时 `request_id: none + status: not-applicable`；有会影响结论的外部事实时列全 material claims、标 required，由主控在独立裁判前派 fact-checker。
- verdict：`pass`。
- 判断：请求对象、生产主体、触发时机、允许取证边界均已明确；主控不再临时猜测范围。skill-engine 与角色合同的顺序一致。
- 边界：本 verdict 只评价字段存在与职责闭合，不代表某次真实 request 已覆盖正确。

## 2. Request id / check id 与 material coverage

- 当前结果：fact-checker 回填 request_id；每条 check 有 check_id、claim_id、candidate_id、kind；coverage 保存 material_claim_ids、checked_material_claim_ids 与 complete。
- Skill judge：source_checks 以 `{check_id, claim_id}` 引用，另存 missing_material_claim_ids；coverage 不完整即停止。
- verdict：`partial`。
- 已修复：上一轮“只有 candidate_id、无逐项 check 引用和覆盖证明”的问题已实质补齐。
- 剩余唯一性缺口：
  - required request 的 schema 仍写 `request_id: none|""`，没有“非空、run 内唯一”约束；
  - `check_id: ""` 没有“request 内唯一”约束；
  - coverage.complete 没有明文要求 `material_claim_ids` 必须精确等于 request 中全部 material claim ids，且 `checked_material_claim_ids` 与其集合相等。
- 影响：重复 check_id、空 request_id 或遗漏 request claim 后自报 complete，在当前 schema 下没有被明确判无效；skill-judge 的引用可能歧义。
- 最小剩余修复：冻结 request_id / check_id 唯一性和非空条件，并把 coverage.complete 定义为两个集合与 request material claims 的精确相等关系。

## 3. High-trust supported

- 当前规则：外部事实只有至少一个“本次定位核实”的 high 来源才可 supported；源内事实必须回到登记原始材料可定位位置。
- source schema：每个来源记录 trust 与 verified_this_run。
- verdict：`pass`。
- 判断：上一轮 medium / low 来源也可能推动 supported 的缺口已关闭；字段与聚合条件能同时验证可信度和本次核实。
- 可声称范围：只证明规则硬约束存在，不证明真实外部事实已核实。

## 4. Fact-checker overall 到条件子门映射

- orchestrator 规则：fact-checker `overall` 无损映射到 `conditional_fact_check.status`。
- 状态范围：条件子门支持 `not-applicable | not-run | pass | fail | blocked`；fact-checker 完成后使用 pass / fail / blocked。
- verdict：`pass`。
- 判断：字段名不同但转换已被显式冻结，不再由主控自行解释。未触发和未运行也各有独立状态。

## 5. Source provenance + conditional fact 聚合

- 当前聚合规则：来源证明必须 pass；条件事实未触发必须 not-applicable，触发必须 pass；两者满足才 source_and_fact pass。任一子门 fail 则整体 fail，任一 blocked 则整体 blocked，其余为 not-run。
- 最终 owner：orchestrator；两个子门各自保留 owner 与证据。
- judge 与 manifest 文字：均重复该聚合边界。
- verdict：`fail`。
- 规则层正面判断：聚合真值表、not-applicable 和 owner 已经闭合。
- 持久化 schema 冲突：
  - orchestrator 的 `verification.source_and_fact` 是包含 status、owner、source_provenance、conditional_fact_check、scope、evidence、conflicts 的嵌套对象；
  - manifest YAML 的 `verification.source_and_fact` 仍只是 `not-run | pass | fail | blocked` 标量；
  - manifest 文字说子门状态与证据保存在“同一 manifest 的主控验收记录”，但 YAML 中没有 `orchestrator_acceptance`、子门对象或其他引用字段。
- 影响：按 orchestrator 输出无法写入 manifest 的现有字段；按 manifest 只能保存聚合标量，无法保存 request_ref、子门 owner / evidence，也无法复核聚合。`run_ref / verification 必须与同一 manifest 完全一致` 无法在形状上成立。
- 最小剩余修复：在 manifest 模板中增加与 orchestrator 同形的来源与事实门验收记录，或明确一个 manifest 内可定位的记录引用；聚合标量与嵌套记录必须各有唯一字段，不能共用同名 key 的不同类型。

## 6. 未触发条件事实核查

- 当前规则：无外部事实时 request 为 none / not-applicable；主控 conditional_fact_check 必须 not-applicable；来源证明 pass 后可聚合 source_and_fact pass。
- verdict：`pass`。
- 判断：not-run 不再冒充 not-applicable，未触发也不再被误判为缺门。

## 7. Fact-checker 到 Skill-judge 的结果回交

- 当前链路：主控在裁判前按 request 派发 fact-checker；结果带 request_id、check_id、claim_id、candidate_id 与 coverage；skill-judge 接收 request 和完整结果，以 check_id + claim_id 引用，并报告 missing material claims。
- verdict：`partial`。
- 已闭合：顺序、输入内容和逐项引用位置明确，blocked 时能通过 missing_material_claim_ids 给出缺失全集。
- 剩余依赖：由于 request/check id 唯一性和 coverage 集合相等规则未冻结，回交对象仍可能出现重复 id 或伪 complete；因此不能判无冲突 pass。

## 8. Non-material 可见外部事实

- judge 协议要求“可见判断中的外部事实”回到本次核实的高可信来源，没有只限 material。
- fact-checker overall 规则只要求所有 material claims supported；non-material claim 为 conflicted / insufficient / out_of_scope 时没有阻止 overall pass。
- skill-judge 禁止补事实或改写候选；其停止条件只点名 material claim 覆盖不完整，没有要求非 material 不支持事实先删除或退回。
- verdict：`fail`。
- 影响：一个候选可含不会改变核心结论、但仍会呈现给读者的错误或无证据外部事实；fact-checker overall 仍可 pass，主控条件子门也随之 pass，最终违反 judge 的可见事实要求。
- 最小剩余修复：所有将保留为可见内容的外部事实都必须 supported；非 material 若非 supported，必须有结构化 `remove_or_revise` 处置并在 Skill judge 前完成，不能直接随 overall pass 留在候选中。

## 六项修复矩阵

| 上一份最小修复 | rerun verdict | 结论 |
| --- | --- | --- |
| typed request + 触发主体 | `pass` | 机制候选生产 request，主控按 request 派发。 |
| request/check id + 完整覆盖 | `partial` | 字段已补；唯一性与 coverage 集合等式未冻结。 |
| result 引用到 skill-judge | `partial` | check_id + claim_id 已补；仍受唯一性 / complete 规则影响。 |
| overall 映射 + 条件未触发 | `pass` | overall 映射明确，not-applicable 与 not-run 分离。 |
| source provenance + conditional fact 聚合 | `fail` | 真值表已补，但 manifest 标量与主控嵌套记录形状冲突。 |
| high-trust supported + owner | `pass` | high 本次核实已硬化，主控聚合 owner 与子 owner 已明确。 |

## 最终可声称范围

- 可以声称：请求生产与触发责任、逐项结果字段、高可信 supported、overall 转换、未触发状态及聚合真值表已实质建立。
- 不可以声称：request/check 引用已经唯一可复核、manifest 能无损持久化子门证据、所有可见外部事实都受 pass 门约束，或事实门 handoff 已无冲突。

最终 overall verdict：`fail`。
