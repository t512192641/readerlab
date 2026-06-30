# Method Absorption Audit

## 总判断

v1 的目标不是证明 ReaderLab 已经 product ready，而是证明这次没有继续把四种阅读方法平均混成一锅。v1 按职责分层：

- 李继刚式深读负责材料边界、缺口、增量、不增量、机制链和认知旅程。
- 仓颉式方法负责候选池、通过/降级/拒绝链和三重验证意识。
- 乔木式共读负责正文附近的读者问题、批注触发和误读纠偏。
- book-to-skill 负责判断哪些内容能成为可执行能力，哪些只能降级。
- ReaderLab 负责把上述内容组织成可读、可批注、可复核的 LifeAtlas 阅读包，并把审计信息退到附录。

本次阻断项修复后，完整候选筛选链和能力候选验证链已进入 `audit/candidate-evidence.v1.json`。主阅读稿仍保持连续可读；候选池、V1/V2/V3 证据、location refs 和能力验证状态不塞回 reader 侧。

## 吸收对照

| 方法证据 | v0 暴露的问题 | v1 吸收位置 | v1 改善点 |
|---|---|---|---|
| `ljg-deepread-only.md` | v0 有机制骨架，但缺“补什么缺口、增量是什么、不增量是什么、认知如何变化”。 | `reader/01_主阅读稿.md` 的“这本书真正补的缺口”“机制链”“认知旅程”。 | 主稿先判断材料性质和读者增量，再展开机制，不再只列目录式链条。 |
| `cangjie-only.md` | v0 只有被选中的卡，没有候选池、淘汰链和降级理由。 | `reader/01_主阅读稿.md` 的“候选如何筛过”。 | 明确通过、降级、拒绝，特别拒绝 69 法则整体、单纯拼命工作、共情表达、多行星整体升格。 |
| `qiaomu-coread-only.md` | v0 的“阅读路线”是空泛顺序，不像陪读。 | `reader/01_主阅读稿.md` 的“读到正文附近，你该问什么”。 | 用 15 个正文附近批注触发替代“先读什么再读什么”。 |
| `book-to-skill-only.md` | v0 深读卡混合概念、边界、案例和术语，没有可调用能力结构。 | `reader/01_主阅读稿.md` 的“只保留 5 个可执行能力”。 | 每个能力都有 `trigger / input / steps / output / boundary`，其余内容降级。 |
| ReaderLab 工程底座 | v0 有 source/location/contracts 和 reader/audit 分离，但读者页碎片化。 | `README.md`、`audit/90_来源与审计.md`、`assertions.md`。 | reader 侧只保留主稿，审计侧说明来源、状态、validator 和 product-ready 边界。 |

## 新增独立审计实例

`candidate-evidence.v1.json` 补上三个之前被对抗审查指出的缺口：

- `locations_used`：从 v0 `location-map.v1.json` 复制必要精简字段，包含 `location_id`、`heading_path`、`block_id`、`char_range`、`text_preview` 和 `precision_note`。
- `candidate_screen`：覆盖主稿中的通过、降级和拒绝项，并逐项写出 `primary_location_refs`、`v1_cross_context`、`v2_predictive_power`、`v3_distinctiveness`、`boundary`、`review_status`。
- `ability_candidates`：记录 5 个能力候选的 `trigger / input / steps / output / boundary / evidence_location_refs / validation_status / not_formal_skill_reason`。

这个 JSON 是 v1 的独立审计层，不是正式生成器输出，也不是人工验收记录。

## 这次没有吸收的内容

- 没有把 `yao-meta-skill` 当成读书方法。它只提供 output eval 的断言和 gate 口径。
- 没有把 CTK/MEM 写进读者输出。它们只属于协作和状态纪律。
- 没有接入 NotebookLM、Obsidian API、llm-wiki、MinerU、markitdown 或 OCR 工具。
- 没有把整本书转成正式 Skill。
- 没有把 69 项核心法则整体包装为“马斯克方法论”。

## Output eval 口径应用

Meta Skill 的 output eval 方法强调：评估应证明最终用户可见输出变好，而不是只证明路由、文件存在或固定措辞。

本 v1 对应的质量断言是：

- 读者侧必须是一篇主稿，而不是 5 个短页拼装。
- 主稿必须包含候选/降级/拒绝链，抓住 v0 没解释“为什么不选”的问题。
- 主稿必须包含缺口、增量、不增量和认知旅程，抓住 v0 像摘要的问题。
- 主稿必须包含批注触发和误读纠偏，抓住 v0 像报告、不像陪读的问题。
- 主稿必须包含 3-5 个可执行能力，且每个都有触发、输入、步骤、输出、边界。
- 审计页必须承认人工状态 pending，validator 不能替代人工阅读质量。

这些断言仍需要后续对抗审查和人工复核。当前只完成 worker 自检。

## 风险

- 主稿基于 bakeoff outputs 和 v0 contracts 重组，不是由正式 ReaderLab 生成器自动生成。
- v1 已补 `candidate-evidence.v1.json` 作为独立审计层，但其位置字段仍来自 v0 location map；还不是从 EPUB fresh parse 生成的正式 v1 source-grounded contract。
- 主稿为了连续阅读压缩了候选池细节；候选池已进入单独 audit JSON，若要进入正式产品，还需要升级为有 schema 和 validator 的正式契约。
- 5 个可执行能力仍是方法候选，不是已经安装或验证过的 Skill。
- 人工状态仍为 `pending`，需要抽查 candidate decisions、location refs 和能力边界。
