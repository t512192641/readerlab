# Assertions

## 本轮片段评测断言

| ID | 断言 | 状态 | 证据 |
|---|---|---|---|
| FRAG-A01 | 必须产出 6 到 8 个高价值片段。 | pass | `reader/01_片段能力评测.md` 产出 8 个片段。 |
| FRAG-A02 | 片段必须覆盖不同阅读难点，不能只选同一类方法片段。 | pass | 覆盖材料边界、价值选择、推理方法、危机误迁移、组织机制、流程能力、交付系统、宏大叙事。 |
| FRAG-A03 | 必须区分核心字段和条件字段，不能把 7 字段齐全当作质量断言。 | pass | `reader/01_片段能力评测.md` 写明必填核心与条件字段；`audit/90_维度价值审计.md` 写明正式化时条件触发。 |
| FRAG-A04 | 每个片段必须有 heading/path 或 location_id 支撑。 | pass_with_caveat | 每张卡含 `location_id`、heading、EPUB xhtml path；refs 继承 v0/v1。 |
| FRAG-A05 | 必须说明没有 fresh source-grounded contract。 | pass | `README.md` 和 `reader/01_片段能力评测.md` 均声明。 |
| FRAG-A06 | 必须评估维度本身价值。 | pass | `audit/90_维度价值审计.md`。 |
| FRAG-A07 | 必须明确这是手工片段评测样张，不是 product ready 或生成器能力证明。 | pass | `README.md`、`reader/01_片段能力评测.md`。 |
| FRAG-A08 | 不写 LifeAtlas `300/600/800`，不新增依赖，不修改 canonical packages。 | pass | 本轮只写 `docs/reports/readerlab-elon-fragment-capability-eval-v0/`。 |
| FRAG-A09 | Meta Skill 方法只用于 output eval / Skill IR 口径，不冒充读书模板。 | pass | `audit/90_维度价值审计.md` 只引用 output eval 判断逻辑。 |
| FRAG-A10 | 不继续写全书总纲。 | pass | 读者文件只做片段卡，不新增全书地图或主阅读稿。 |
| FRAG-A11 | 断言必须检查误读防护、过度迁移或来源误用，而不是只查字段存在。 | pass | 每张卡的 `审查标准` 都定义了 fail 条件；F01/F04/F08 分别针对来源误用、疲惫美化和宏大叙事免检。 |
| FRAG-A12 | 高风险片段必须标出额外复核要求。 | pass | F04 标 `inherited refs only` 和正式 eval 人工复核要求；F08 标跨片段综合卡、外部核验要求。 |

## ELON-A01 到 ELON-A13 范围化自检

| ID | 状态 | 片段评测处理 |
|---|---|---|
| ELON-A01 | pass_by_reference | 本目录不生成 catalog map；片段来源继承 v0 contracts 和 v1 evidence。 |
| ELON-A02 | pass_by_boundary | 没有新增 `coverage_status=full`，没有把片段样张说成精选译文正文。 |
| ELON-A03 | pass_by_boundary | 没有新增 grounded global map 或 source registry。 |
| ELON-A04 | pass | 使用多个具体局部锚点，不把第二部分或全书混成单一片段。 |
| ELON-A05 | pass_with_caveat | 片段均有高价值阅读判断和 source refs；但 refs 不是 fresh contract。 |
| ELON-A06 | pass_by_replacement | 不写空泛阅读路线，改为片段附近阅读动作。 |
| ELON-A07 | pass | 人工状态和 product-ready 边界明确保留。 |
| ELON-A08 | pass_by_scope | 本轮不是 deepread card 全量重做；片段卡覆盖机制、边界、反例，并按需要使用迁移题或核验题。 |
| ELON-A09 | partial_pass | 使用 v1 的通过/降级/拒绝思路，但本轮没有重建完整候选池。 |
| ELON-A10 | partial_pass | 有 heading/path/location_id；缺 fresh source-grounded contract 和人工抽查。 |
| ELON-A11 | pass | reader 侧没有塞 validator、hash、machine status 或覆盖明细。 |
| ELON-A12 | pass | 每张片段卡使用正式 heading 或既有 location_id。 |
| ELON-A13 | pass | 输出明确读者新增能力：识别误读、执行阅读动作、判断迁移边界。 |

## 未解决风险

- 位置引用继承 v0/v1，尚未 fresh parse EPUB，也没有人工逐段抽查。
- 片段卡是手工样张，不代表生成器稳定能力。
- 没有真实用户批注输入，无法证明这些片段能在 Obsidian 附近触发更好讨论。
- 维度价值判断已经过一次对抗式审查和修订，但尚未经过 blind A/B。
