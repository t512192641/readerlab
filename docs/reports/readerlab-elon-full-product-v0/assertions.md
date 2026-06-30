# ELON Assertions

| ID | 结果 | 证据 | 未解决项 |
|---|---|---|---|
| ELON-A01 | pass | `contracts/catalog-map.v1.json` 存在，并以正式标题/可追溯标题映射组织全书结构。 | 无。 |
| ELON-A02 | pass | `grounded-global-map.v1.json` 使用 `coverage_status=full`，且 `source-registry.v1.json` 标记 EPUB OPF spine 36/36 已抽取。 | full 只代表来源覆盖，不代表精选译文正文完成。 |
| ELON-A03 | pass | catalog、grounded global、local deepread 均含 `source_scope`、`coverage_status`、`coverage_note`、`confidence`、`review_items`、`machine_status`、`human_status`。 | 无。 |
| ELON-A04 | pass | `local-deepread.v1.json` 命名“部件 II：极致艰苦工作”旧映射，并列出 `v101-13.xhtml` 到 `v101-18.xhtml`。 | 正式标题是“第二部分：极限硬核工作”，需主 Agent 确认显示名。 |
| ELON-A05 | pass | distillation candidates 和 claim_refs 都有 source refs、primary location refs、适用边界和 pending human status。 | 人工仍需抽查引用准确度。 |
| ELON-A06 | pass | `reader/01_全书阅读路线.md` 区分全书路线、第二部分深读和未完成精选译文正文。 | 无。 |
| ELON-A07 | pass | 所有契约 JSON 的 `human_status` 都是 `pending`。 | 无。 |
| ELON-A08 | pass | `local-deepread.v1.json` 含 6 张 deepread_cards，覆盖 framework、principle、case、counterexample、term、transfer_insight。 | 卡片质量需人工评审。 |
| ELON-A09 | pass | 每张 deepread_card 均含 V1/V2/V3，状态均为 `pending`，未写成稳定方法论。 | 需要后续新材料反测。 |
| ELON-A10 | pass | 高价值主张的 `primary_location_refs` 指向 heading/block/cleaned-char refs；结构性 spine/title 例外写在 precision exception。 | char_range 是清洗文本偏移，不是纸书页码。 |
| ELON-A11 | pass | 读者页没有把 hash、validator、spine coverage 明细作为主阅读段落；这些在 README、audit、contracts。 | 无。 |
| ELON-A12 | pass | 全书结构使用“本书说明/第一部分：追寻目标/第二部分：极限硬核工作/第三部分：企业建设/第四部分：代表人类/附录”等正式或可追溯标题。 | 无。 |
| ELON-A13 | pass | `grounded-global-map.v1.json` 和 `reader/02_全书地图.md` 均含 reader_gain 等价内容。 | 仍需主 Agent 判断是否足够有阅读增量。 |

## 总体判断

机器断言自检为 13/13 pass。人工状态保持 pending；本结果只进入主 Agent 和对抗审查 worker 审核，不称为 product ready。
