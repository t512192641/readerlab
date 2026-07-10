# 来源与事实门 Schema 冷启动复核原始输出

## 复核身份与边界

- 时间：`2026-07-10T07:30:10-04:00`。
- 本次读取：`v3/skill/protocols/judge.md`、`v3/skill/roles/fact-checker.md`、`v3/skill/roles/skill-judge.md`、`v3/skill/roles/orchestrator.md`、`v3/skill/templates/run-manifest.md`。
- 本次只检查：来源与事实门的逐项 verdict、整门 status，以及 Skill 条件事实核查从请求、执行、回交到主控 / manifest 的 schema 是否无冲突。
- 本次未读：其他角色合同、线路协议、回归 case / suite、真实 run 或旧事实门结果。
- 上下文声明：本执行者此前审过主控 schema 与 Skill 回归；本次不是零历史上下文，但所有 verdict 只引用本节五个指定文件。
- 本次不修改规则，只新增该 raw。

## 总结论

- overall verdict：`fail`。
- 已一致：事实逐项 verdict 的四值枚举完全一致；整门最终值的三值枚举也一致；来源不可访问 / 身份不明只进入整门 `blocked`，没有另造逐项 blocked，边界清楚。
- 仍冲突：Skill 条件事实核查没有完整请求 envelope 和触发主体；fact-checker 的 `overall` 到主控 `source_and_fact.status` 没有显式无损映射；合并“来源证明 + 条件外部事实核查”为单一 gate 的聚合规则缺失；`supported` 也未在 schema 上强制至少有高可信来源。
- 按任务要求，只要 handoff 仍有冲突必须 fail，因此不能以枚举一致替代整条交接闭合。
- 可声称范围：可声称“逐项与整门枚举对齐”；不可声称“Skill 条件事实核查可无冲突 handoff”或“来源与事实门 schema 已通过”。

## 1. 逐项 verdict 一致性

- judge 协议：`supported | conflicted | insufficient | out_of_scope`。
- fact-checker：`supported | conflicted | insufficient | out_of_scope`。
- verdict：`pass`。
- 判断：名称、拼写和语义顺序一致；事实核查角色可以直接产出 judge 协议要求的逐项值，不需要翻译枚举。
- blocked 边界：judge 明确来源不可访问 / 身份不明造成无法判断时，blocked 写在整门状态；fact-checker 也没有逐项 blocked，而使用 `overall: blocked + blocked_reason`。该设计一致。

## 2. 整门 status 一致性

- judge 协议整门：`pass | fail | blocked`。
- fact-checker：字段名为 `overall`，值为 `pass | fail | blocked`。
- orchestrator：`verification.source_and_fact.status: not-run | pass | fail | blocked`。
- manifest：`verification.source_and_fact: not-run | pass | fail | blocked`。
- verdict：`partial`。
- 已一致：执行完成后的三种终态完全一致；主控 / manifest 额外的 `not-run` 合理表达尚未执行。
- 未闭合：没有一条合同明确规定 `fact-checker.overall -> orchestrator.verification.source_and_fact.status -> manifest.verification.source_and_fact` 的字段映射。值可以对齐，但 `overall` 与 `status` 是不同字段名，且 source_and_fact 还包含来源证明，不一定等同于 fact-checker 单项输出。
- 影响：主控可以把 fact-checker `overall: pass` 直接写成整门 pass，也可以先与其他来源结果合并；两个行为在当前五文件中都没有被禁止或规定。

## 3. Fact-checker 内部聚合

- 当前规则：所有 material claim 均 supported 才 pass；任一 material claim 为 conflicted / insufficient / out_of_scope 则 fail；来源不可访问或身份不明到无法判定则 blocked。
- verdict：`partial`。
- 已闭合：material 事实的 pass / fail / blocked 聚合规则清楚，非 material 缺口不会自动推翻整门。
- 高可信冲突：judge 要求外部事实回到“本次核实的高可信来源”；fact-checker 的 source `trust` 允许 `high | medium | low`，但聚合规则没有要求 `supported` 的外部事实至少含一个 `high` 来源。按 schema，只有 medium / low 来源的 check 仍可被标成 supported 并推动 overall pass。
- 最小修复：冻结 `supported` 条件，至少区分源内事实与外部事实；外部事实没有可定位 high-trust 来源时只能是 insufficient / out_of_scope，不能 supported。

## 4. Skill 条件事实核查的请求输入

- fact-checker 允许输入：主控提供的来源 / 事实要求摘录、待核事实清单、原始来源、source map，以及获授权的高可信外部来源。
- skill-judge 允许输入：如触发外部事实核查，读取“已完成的事实核查结果”。
- verdict：`fail`。
- 缺失请求对象：五个文件中没有结构化 `fact_check_request`，至少缺少 `triggered`、请求主体、触发原因、claim_id、candidate_id、待核事实文本、源内 / 外部类型、materiality、已有 source refs 和允许外部来源边界。
- 缺失触发主体：skill-judge 的输入假定事实核查已经完成；它自身的输出也没有待核事实请求字段。fact-checker 又要求主控提供待核清单，但 orchestrator 没有规则说明谁在 skill-judge 之前识别并提交该清单。
- 当前无法补救：orchestrator 的通用 `input_refs` 只能引用某个对象，不能定义对象必须含什么；fact-checker 的自由文本 `return_to` 也不能弥补请求端缺 schema。
- 影响：同一机制候选是否“触发外部事实核查”、核查哪些 claim、哪些 claim 会改变结论，可能由不同主控临时决定；skill-judge 无法验证收到的结果是否覆盖原请求全集。

## 5. Fact-checker 到 Skill-judge 的结果回交

- 可用连接：fact-checker 每项含 `claim_id`、`candidate_id`、`anchor_id`；skill-judge 每项含 `candidate_id` 与 `source_checks`；orchestrator dispatch 也有 actual_output_refs / evidence_refs / depends_on。
- verdict：`partial`。
- 正面判断：candidate_id 提供了最小关联键，主控可以把事实核查产物作为 skill-judge input ref；skill-judge 的 source_checks 也有容纳引用的位置。
- 剩余冲突：`skill-judge.verdicts[].source_checks` 没有定义应存 check id、claim id、完整 check 还是 output ref；fact-checker 的 check 又没有独立 `check_id`。因此一条 candidate 下多项事实核查无法稳定逐项引用，也无法证明 source_checks 覆盖 fact-check request 的全部 material claims。
- blocked 回交：skill-judge 在“事实核查不完整”时停止并退回上游，但没有字段记录缺失的 claim ids；只能使用自由文本 blocked_reason / return_to，仍不能形成可审计补跑列表。

## 6. `source_and_fact` 整门聚合

- judge 的来源与事实门同时要求：正文 / source map 可定位、AI 解读不冒充主体、源内事实可回原材料、外部事实可回高可信来源。
- manifest / orchestrator 只有一个 `source_and_fact` 状态；orchestrator owner 是单一字符串。
- verdict：`fail`。
- 缺失子门：没有 schema 区分 `source_provenance` 与 `conditional_external_fact_check` 的状态和证据。
- 缺失条件聚合：
  - 未触发外部事实核查时，fact-checker 应是 not-run，但来源证明仍可能让整门 pass；当前没有明文规则。
  - 触发时，整门应如何合并来源结果与 fact-checker overall 没有规则；任一子结果 fail / blocked 是否支配整门也未冻结。
- owner 冲突：来源证明与条件事实核查可能由不同角色完成，但 `owner` 是单值；没有最终聚合 owner 或 owners 列表规则。
- 影响：fact-checker pass 可能错误覆盖 source map 失败，或 source integrator pass 可能掩盖外部事实核查未跑 / 失败。

## 7. 无冲突 handoff 判定

| 链段 | verdict | 原因 |
| --- | --- | --- |
| judge 逐项枚举 -> fact-checker checks | `pass` | 四值完全一致。 |
| fact-checker overall -> 主控 / manifest status | `partial` | 终态值一致，字段与聚合关系未定义。 |
| Skill 条件触发 -> fact-checker 请求 | `fail` | 无请求 envelope、触发主体和覆盖清单。 |
| fact-checker checks -> skill-judge source_checks | `partial` | 有 candidate_id，但无 check_id 与引用类型。 |
| 来源证明 + 条件事实 -> source_and_fact 整门 | `fail` | 无子门与确定性聚合规则。 |
| 外部事实 supported -> 高可信来源 | `fail` | trust 可为 medium/low，supported 未强制 high。 |

## 最小修复清单（本次不修改）

1. 定义条件事实核查请求 envelope 和唯一 request / check id，明确触发主体与 material claims 全集。
2. 定义 fact-checker 结果引用方式：skill-judge.source_checks 只能引用 check ids，并能验证 material request 全覆盖。
3. 冻结 `fact-checker.overall` 到主控 / manifest 的映射，以及 `source_provenance + conditional_fact_check -> source_and_fact` 聚合表。
4. 明确未触发外部事实核查时的状态与证据口径，避免 not-run 被误判为缺门。
5. 强制外部事实 `supported` 至少包含本次核实、可定位的 high-trust 来源。
6. 处理 gate owner：指定一个最终聚合 owner，或将 owner 改为可列多个子门 owner。

## 最终可声称范围

- 可以声称：逐项 verdict 与完成后的整门枚举已对齐，blocked 的逐项 / 整门边界一致。
- 不可以声称：Skill 条件事实核查已经具有无冲突请求、完整回交和确定性整门聚合；也不能声称事实门或主控 schema 通过本次冷启动复核。

最终 overall verdict：`fail`。
