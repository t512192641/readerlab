# Elon Assertions

对象：`埃隆之书 ReaderLab Demo` absorption review pack。

结论：6 pass / 1 partial / 0 fail。它仍只能作为 repo 内 review pack，不能进入 LifeAtlas 写入；当前产物是目录地图 + `部件 II：极致艰苦工作` 局部深读，不是正式样张，也不是人工验收。

| ID | 结果 | 自评 |
|---|---|---|
| ELON-A01 | pass | 已生成 `catalog-map.v1.json`，基于 demo manifest 和 `01_全书分组与章节手册.md` 给出全书结构和阅读路线假设。 |
| ELON-A02 | pass | 未生成全书 grounded map 契约；所有 coverage 都保持 `partial`，没有声称全书正文已经完整覆盖。 |
| ELON-A03 | pass | `readerlab.local-deepread.v1` 已在契约文件中补定义；四个 JSON 都包含 `source_scope`、`coverage_status`、`coverage_note`、`confidence`、`review_items`、`machine_status`、`human_status`。 |
| ELON-A04 | pass | `part2-local-deepread.v1.json` 明确命名 `部件 II：极致艰苦工作`，并列出 `v101-13.xhtml` 到 `v101-18.xhtml`。 |
| ELON-A05 | partial | 提炼候选已补 item-level `claim_refs`，主证据改为 part II reader page 的原文行段，派生提炼页只作辅助证据；但这些 refs 仍是 reader-page line range，不是精确 EPUB char span，不能算 fully pass。 |
| ELON-A06 | pass | `catalog-map.v1.json` 区分全书 route hypothesis、已覆盖 part II、未覆盖单元；`part2-local-deepread.v1.json` 只给局部阅读路线。 |
| ELON-A07 | pass | 所有 `human_status` 均为 `pending`，没有把机器状态当成人工接受。 |

## 剩余风险

- 目录地图只适合第一次阅读路线，不应被提升为全书理解。
- 局部深读的候选方法原子仍需要精确 EPUB span 和人工复核；当前只能说已从派生提炼页回退到 reader-page 原文行段。
- 当前 location map 对 markdown 使用整文件 char range + line range；后续工具化时应生成更精确的 block/char offsets。
