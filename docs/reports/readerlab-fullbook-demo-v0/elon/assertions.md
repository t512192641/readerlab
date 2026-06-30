# 《埃隆之书》Fullbook Demo Assertions

| ID | 状态 | 说明 |
|---|---|---|
| FULLBOOK-A01 | pass | 新增 `grounded-global-map.v1.json` 和 `fullbook-reader-demo.md`，不是复制旧 `catalog-map` 或旧局部 demo。 |
| FULLBOOK-A02 | pass | `source-registry` 登记 OPF spine count 36，`location-map` 登记 36/36 个 `elon-spine-*` location，未列出缺失 spine。 |
| FULLBOOK-A03 | pass | `fullbook-reader-demo.md` 包含总收获和亮点，每条均带 `elon-spine-*` refs。 |
| FULLBOOK-A04 | pass | `grounded-global-map.v1.json` 使用 `coverage_status=full` 的依据是完整 EPUB spine 登记；说明它不是精选译文完整阅读页。 |
| FULLBOOK-A05 | pass | 所有 JSON 顶层 `human_status` 均为 `pending`，没有声明人工验收通过。 |
| FULLBOOK-A06 | pass | README 和读者 demo 明确缺口：没有精选译文正文、不是 LifeAtlas 正式写入、未完成人工验收。 |

总体判断：机器断言 pass；人工阅读质量验收仍为 `pending`。
