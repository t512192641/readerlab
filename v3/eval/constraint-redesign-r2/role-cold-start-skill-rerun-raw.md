# Skill 四角色合同 schema 复核原始输出

- 执行主体：上一轮五角色合同冷启动检查的同一 Agent。
- 此前上下文：本 Agent 知道首次检查指出的三项阻塞——前四角色缺整体状态、judge 无法区分合法 0 条与 blocked、writer 缺“净化正文不变”的结构化证明；保留首次失败文件未读未改。
- 本次读取范围：仅复核 `v3/skill/roles/skill-source-integrator.md`、`skill-mechanism-auditor.md`、`skill-judge.md`、`skill-writer.md` 四份修订后合同。
- 明确未读：首次 raw、完整 Skill 协议、constraint architecture、rubric、回归证据、cold-start 合同及其他任何文件。
- 执行性质：只检查修订后 schema 是否具备表达三项原阻塞所需的字段；不检查完整协议一致性，不运行真实 Skill，不修改规则。
- 执行时间：2026-07-10 07:00 EDT（UTC-04:00）。

## 复核结论摘要

三项原阻塞均已在 schema 表达能力层面消除：

1. 四角色均新增统一整体状态 `not-run | pass | fail | blocked`，并新增 `blocked_reason`、`return_to`。
2. judge 新增 `zero_accept_reason`，可与整体状态及 `selection_count` 共同区分“正常裁判后 0 条接受”和“整门 blocked / 未运行”。
3. writer 新增 `source_body_integrity`，包含 source map、实际渲染正文、`unchanged` 断言与验证证据。

本次 rerun verdict：`pass`。

存在一个非阻断提示：schema 没有把字段组合约束写成显式不变量，例如 `status: pass + selection_count: 0` 时必须填写 `zero_accept_reason: no-qualified-candidates`。当前字段已经足以无歧义表达正确结果，因此不再构成原阻塞；若后续做机器校验，再固定组合规则即可。

## 1. skill-source-integrator

- rerun verdict：`pass`。
- 实际修订：结构化输出顶部新增：
  - `status: not-run|pass|fail|blocked`
  - `blocked_reason: ""`
  - `return_to: ""`
- 整体状态阻塞是否消除：是。正常完成、未运行、失败和停止阻塞已有独立状态；缺源、来源冲突或必须实质改写时，可用 `status: blocked`、原因和退回对象表达，不再需要用空 `clean_units` 或自由形态 `gaps` 猜测状态。
- 合法空结果 / blocked 是否仍混淆：否。即使 `clean_units: []`，整体状态也能说明它是正常空结果、未运行还是 blocked。
- 对原成功 schema 的影响：未破坏。`clean_units`、`deletions`、`related_assets`、`gaps` 均保留。
- 剩余非阻断点：停止条件正文没有逐字写“触发后必须设 `status: blocked`”，但字段命名和 `blocked_reason` 已给出唯一自然表达；本次 schema 复核不把它判为阻塞。
- 可声称范围：可声称来源整合合同的整体运行状态和停止输出已结构化；不可声称任何真实来源整合已经运行或通过。

## 2. skill-mechanism-auditor

- rerun verdict：`pass`。
- 实际修订：同样新增统一 `status`、`blocked_reason`、`return_to` 三个顶层字段。
- 整体状态阻塞是否消除：是。无法回源、来源冲突或未授权运行/外部比较时，可以整体 blocked 并记录原因、退回对象。
- 合法 0 候选 / blocked 是否仍混淆：否。`mechanism_candidates: []` 不再独自承担运行状态；可由 `status: pass` 表达正常完成但没有提交候选，由 `status: blocked` 表达证据或权限阻塞，由 `status: not-run` 表达未执行。
- 对证据缺口的影响：`evidence_gaps` 继续描述缺什么；新的整体状态说明这些 gap 是否已经阻止运行，两者职责不再混淆。
- 剩余非阻断点：没有单独的 `zero_candidate_reason`，但本轮原阻塞只要求区分整体空结果与 blocked；`status` 加 `evidence_gaps` 已足够表达。若产品以后需要审计“为什么正常 0 候选”，可另加原因枚举，但不是当前阻断。
- 可声称范围：可声称候选生产合同的整体状态出口已闭合；不可声称候选质量或独立裁判结果通过。

## 3. skill-judge

- rerun verdict：`pass`。
- 实际修订：新增统一 `status`、`blocked_reason`、`return_to`，保留候选级 `accept | reject | blocked`，并在 `selection_count` 后新增：
  - `zero_accept_reason: no-qualified-candidates|not-applicable|""`
- 整体状态阻塞是否消除：是。候选级 verdict 与整门运行状态现在分层：单个候选可 blocked，整门也可因 source map、事实核查或回归冲突而 blocked。
- 合法 0 条 / blocked 是否消除：是。合同现在能表达至少三种原先混淆的情况：
  - 正常裁判、全部 reject：`status: pass`，`selection_count: 0`，`zero_accept_reason: no-qualified-candidates`。
  - 整门阻塞：`status: blocked`，填写 `blocked_reason` 和 `return_to`；不能再仅用 `selection_count: 0` 冒充合法 0 条。
  - 未执行：`status: not-run`。
- 锁定包交接：未受影响；有接受项时继续由 `locked_packets` 交 writer。
- 剩余非阻断点：上述字段组合规则是从字段语义直接恢复的，但合同没有把它们写成显式 invariant；例如没有明文禁止 `status: pass + selection_count: 0 + zero_accept_reason: ""`。这不会妨碍一个冷启动 Agent正确输出，却可能允许坏输出通过未来的宽松机器解析。属于后续校验强化项，不再是 schema 表达缺失。
- 可声称范围：可声称“合法 0 条接受”与“整门 blocked / 未运行”已可结构化区分；不可声称逐 case 回归、实际裁判或用户体验已经通过。

## 4. skill-writer

- rerun verdict：`pass`。
- 实际修订：新增统一 `status`、`blocked_reason`、`return_to`，并新增：

```yaml
source_body_integrity:
  source_map_ref: ""
  rendered_body_ref: ""
  unchanged: true
  verification: []
```

- 整体状态阻塞是否消除：是。正文/source map 不一致、锁定包缺证据/边界、需要新事实或无法不混题装配时，可明确 blocked 并退回主控，不再以空页面引用表示失败。
- writer 正文不变证明是否补齐：是。成功输出必须同时指向使用的 source map 与实际渲染正文，声明 `unchanged: true`，并提供验证证据；这比只有 `main_page_ref` 能直接审计“原样装配净化正文”的关键承诺。
- 证明边界：该字段提供的是可审计证据槽，不自动证明内容真的未改。真实 run 仍必须检查 `verification` 中的实际证据；本次只确认合同 schema 已经能承载证明。
- 剩余非阻断点：`verification` 未规定证据项子 schema，`unchanged` 只展示成功值 `true`。由于正文不一致已属于停止条件，可由整体 `blocked` 表达，当前设计足以闭合成功和阻塞两条路径；未来若需机器复核，可给 verification 定义固定字段。
- 可声称范围：可声称 writer 的整体状态和正文完整性证明出口已补齐；不可声称任何已生成页面实际保持正文不变。

## 三项原阻塞逐项终判

### A. 整体状态缺失

- source-integrator：已消除。
- mechanism-auditor：已消除。
- skill-judge：已消除。
- skill-writer：已消除。

终判：`pass`。四份 schema 使用同一整体枚举，并均带阻塞原因与退回对象。

### B. 合法 0 条与 blocked 混淆

- source / mechanism 的空数组可由整体状态区分正常完成、未运行与 blocked。
- judge 进一步用 `selection_count` 与 `zero_accept_reason` 标明正常 0 接受原因，并用整门 `status` 表示 blocked。

终判：`pass`。原来最关键的 judge `selection_count: 0` 歧义已消除。

### C. writer 缺正文不变证明

- `source_body_integrity` 已给出源映射引用、渲染正文引用、未改变断言和验证证据槽。

终判：`pass`。原 schema 缺口已补齐；实际证明强度仍须在真实 run 中据 verification 内容判断。

## 总判定与声明边界

- rerun 整体 verdict：`pass`。
- 可声称：四份修订合同已消除首次 raw 指出的三项 schema 阻塞，成功、合法空结果、未运行与 blocked 已有可区分出口，writer 也能提交正文完整性证据。
- 不可声称：完整 Skill 协议一致性通过、回归通过、真实运行通过、正文完整性实际验证通过、冷读或复现通过。
- 非阻断后续项：如要做机器强校验，应补 status/selection_count/zero_accept_reason 的组合不变量，并固定 writer `verification` 的证据项 schema；这不影响本次三项阻塞关闭。
