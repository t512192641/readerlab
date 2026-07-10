# 来源与事实门最后两项第四次复核原始输出

## 复核边界

- 时间：`2026-07-10T07:40:00-04:00`。
- 本次只复核：manifest 与 orchestrator 的 `source_and_fact` 同名对象是否逐字段一致；judge 是否要求覆盖全部可见 request facts。
- 本次读取：仅 `v3/skill/templates/run-manifest.md`、`v3/skill/roles/orchestrator.md`、`v3/skill/protocols/judge.md` 中相关段落。
- 旧事实门 raw 全部保留不改；本次不修改规则文件。
- 上下文声明：本执行者做过前三次事实门复核；本次不是零上下文，但两个 verdict 只依据三份当前文件重新判断。

## 总结结论

- scoped overall verdict：`pass`。
- 两个 rerun-3 剩余冲突均已关闭：source_and_fact 在 manifest 与 orchestrator 中现为同形嵌套对象；judge 已把覆盖范围从 material claims 改为全部可见 request facts，不论 materiality。
- 通过范围：本次只证明最后两处静态 schema 冲突修复；没有执行真实 fact-check request、聚合门或完整主控 run。

## 1. `source_and_fact` 同形持久化对象

- verdict：`pass`。
- manifest 顶层字段：
  - `status`
  - `owner`
  - `source_provenance`
  - `conditional_fact_check`
  - `scope`
  - `evidence`
  - `conflicts`
- orchestrator 顶层字段：与上述七项完全相同。
- `source_provenance` 子门：两边均为 `status + owner + evidence`，status 枚举均为 `not-run | pass | fail | blocked`。
- `conditional_fact_check` 子门：两边均为 `status + owner + request_ref + evidence`，status 枚举均为 `not-applicable | not-run | pass | fail | blocked`。
- 聚合 owner：两边均固定为 orchestrator；子门 owner 与证据各自保留。
- 占位符解释：manifest 使用 `required / required-if-run` 表示填值约束，orchestrator 使用空字符串表示实际输出待填写位置；字段类型和必需语义不冲突。
- 判断：rerun-3 指出的 manifest 缺少顶层 owner / scope / evidence / conflicts 已修复；“逐字段写入 manifest 同名对象”现在有合法落点，不再需要影子记录。
- 可声称范围：可声称静态持久化 schema 同形；不能声称真实 manifest 已填入有效 owner、证据或 request_ref。

## 2. Judge 覆盖全部可见 request facts

- verdict：`pass`。
- 当前 judge 规则：条件事实核查触发时，必须覆盖 request 中全部可见事实，明确注明“无论 materiality”，并通过后才可参与 source_and_fact 聚合。
- 与事实门上位要求一致：可见源内事实回原始材料，可见外部事实回本次核实的高可信来源。
- 判断：rerun-3 中“聚合句只写 material claims”的较弱门槛已经消失；non-material 可见外部事实不再能绕过完整覆盖要求。
- 可声称范围：可声称 judge 的覆盖范围已与严格执行链一致；不能声称任何真实可见事实已经 supported。

## 最终矩阵

| 剩余项 | verdict | 结论 |
| --- | --- | --- |
| manifest / orchestrator 同形 source_and_fact | `pass` | 七个顶层字段与两个子门结构、枚举一致。 |
| judge 全部可见 request facts | `pass` | 已明确无论 materiality 全覆盖。 |

## 最终可声称范围

- 可以声称：rerun-3 剩余的两个静态 schema blocker 已关闭。
- 不可以仅凭本文件声称：完整事实门已做真实 cold-start 执行、实际 request/check coverage 已验证，或完整 ReaderLab run 已通过。

最终 scoped overall verdict：`pass`。
