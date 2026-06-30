# Assertions

## v1 产品断言

| ID | 断言 | 状态 | 证据 |
|---|---|---|---|
| V1-A01 | 读者侧必须是一篇主阅读稿，不修补 v0 的 5 个短页。 | pass | `reader/01_主阅读稿.md`。 |
| V1-A02 | 主稿必须覆盖材料边界、缺口、增量、不增量。 | pass | `reader/01_主阅读稿.md` 的“这本书真正补的缺口”。 |
| V1-A03 | 主稿必须写机制链，不只列目录。 | pass | `reader/01_主阅读稿.md` 的“机制链：不是‘很拼’，而是约束如何传导”。 |
| V1-A04 | 主稿必须写认知旅程。 | pass | `reader/01_主阅读稿.md` 的“读完应完成的认知旅程”。 |
| V1-A05 | 主稿必须有候选/通过/降级/拒绝链。 | pass | `reader/01_主阅读稿.md` 的“候选如何筛过”。 |
| V1-A06 | 必须说明为什么 69 法则整体、拼命工作、共情表达、多行星叙事不能直接升格。 | pass | `reader/01_主阅读稿.md` 的候选筛选表。 |
| V1-A07 | 阅读路线必须替换为正文附近问题、批注触发和误读纠偏。 | pass | `reader/01_主阅读稿.md` 的 15 个批注触发行。 |
| V1-A08 | 只保留 3-5 个可执行能力，且每个有 `trigger / input / steps / output / boundary`。 | pass | `reader/01_主阅读稿.md` 的 5 个能力。 |
| V1-A09 | 来源和审计信息必须与读者正文分离。 | pass | `audit/90_来源与审计.md`、`audit/method-absorption.md`。 |
| V1-A10 | 必须明确非 product ready，人工状态仍待复核。 | pass | `README.md`、`audit/90_来源与审计.md`。 |
| V1-A11 | 不写 LifeAtlas `300/600/800`，不改 EPUB，不新增依赖，不改 scripts。 | pass | 本目录只新增 repo 内 v1 产物。 |
| V1-A12 | 必须有独立候选证据和能力候选验证审计层。 | pass_with_caveat | `audit/candidate-evidence.v1.json`。 |

## ELON-A01 到 ELON-A13 自检

| ID | 状态 | v1 处理 |
|---|---|---|
| ELON-A01 | pass_by_reference | v1 没复制 `catalog-map.v1.json`，但 `audit/90_来源与审计.md` 引用 v0 `contracts/catalog-map.v1.json` 作为结构底座。 |
| ELON-A02 | pass_by_boundary | v1 没新增 `coverage_status=full` 的新 grounded map，也没有把 v1 主稿说成完整精选译文或人工通过。 |
| ELON-A03 | pass_by_reference | v1 审计页引用 v0 contracts；v1 自身是读者稿和审计页，不新增地图 JSON。 |
| ELON-A04 | pass | `audit/90_来源与审计.md` 保留已知局部范围；主稿把第二部分作为重点误读区域处理。 |
| ELON-A05 | pass_with_caveat | 主稿中的高价值提炼均有方法来源和适用边界；具体 source refs 仍继承 v0 contracts，需后续升级为 v1 独立契约。 |
| ELON-A06 | pass_by_replacement | v1 不再写空泛“读法顺序”，改成正文附近问题和批注触发；全书深读和来源精度边界进入审计页。 |
| ELON-A07 | pass | `README.md` 和 `audit/90_来源与审计.md` 明确人工阅读质量仍待复核。 |
| ELON-A08 | pass_by_replacement | v1 不继续使用旧 deepread card 类型，而是在主稿中覆盖候选筛选、机制、边界、术语含义和可迁移能力。 |
| ELON-A09 | pass_with_caveat | 主稿显式使用通过/降级/拒绝链；`audit/candidate-evidence.v1.json` 已为候选项补 `v1_cross_context`、`v2_predictive_power`、`v3_distinctiveness`。仍需人工抽查。 |
| ELON-A10 | partial_pass | `audit/candidate-evidence.v1.json` 已把候选和能力连接到 heading/block/char refs，但 refs 继承自 v0 location map，尚未人工抽查，也不是 fresh parse 生成的正式 v1 source-grounded contract。 |
| ELON-A11 | pass | 主阅读稿不写 validator、hash、machine status 或覆盖明细，这些只在 audit 和 assertions 中出现。 |
| ELON-A12 | pass | 主阅读稿使用“本书说明、第一部分：追寻目标、第二部分：极限硬核工作、第三部分：企业建设、第四部分：代表人类、69 项核心法则”等可追溯标题。 |
| ELON-A13 | pass | 主阅读稿开头和结尾都说明读者新增理解：从名人故事转向“目标如何压成工程、组织、制造和边界判断”。 |

## 未通过或待人工判断

- `ELON-A10` 已从纯 pending 修到 `partial_pass`：有 v1 独立审计 JSON，但缺人工抽查和正式 source-grounded contract。
- 读者体验、压缩程度、批注触发是否足够贴近真实阅读，需要主 Agent 或对抗审查 worker 再审。
- 5 个能力已有候选验证审计，但仍不是正式 Skill。
