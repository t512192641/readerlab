# Writer v2 → 完整章节候选装配协议

状态：`CANDIDATE_ONLY`

## 输入身份

- 完整 B1：`inputs/chapter-readable.md`，来自 T2.35 合法当前 run 的冻结
  `locked/chapter-readable.md`。
- Writer Reader 单元：`inputs/writer-v2-accepted.md`，产品负责人已经给出 Writer `PASS`
  并停止 Writer 迭代。
- 锚点 owner：`inputs/D3-expert.md` 中
  `### 实际触发本课的完整段落（逐字）`。该段是上游 Expert 已经选择并记录的实际触发段，
  不是装配阶段新选锚点。
- lineage 与边界：`inputs/locked-knowledge-cards.md`、`inputs/review-outcomes.md` 和
  `inputs/D3-p2-gate.md`。

## 唯一允许的小修

1. 在 Reader 首次承担论证的“禁忌交换”处补入一句：
   `所谓“禁忌交换”，就是拿金钱、便利等世俗利益去交换被视为身份义务的东西。`
2. 将唯一的
   `象征性承认降低了部分极端反应`
   替换为
   `象征性承认降低了部分愤怒和暴力反对指标`。

除这两处外，Reader 单元必须逐字保持已接受 Writer v2。

## 装配关系

1. 从 Expert 的“实际触发本课的完整段落（逐字）”机械提取锚点正文。
2. 要求完整 B1 中该段逐字出现且只出现一次。
3. Reader 单元固定插入该完整段落之后、下一原文段落之前。
4. Reader 单元身份固定为 `T235-D3-READER-V2-A1`，不得拆分、合并或重选位置。
5. 使用两条 candidate-only HTML comment 作为可逆审计边界；它们不是
   `tandem-comments` 字段，也不声明目标环境兼容：
   - `<!-- readerlab-candidate-only:reader-unit-start id="T235-D3-READER-V2-A1" -->`
   - `<!-- readerlab-candidate-only:reader-unit-end id="T235-D3-READER-V2-A1" -->`
6. 删除完整插入块后必须逐字恢复原始 B1；提取两个 marker 之间正文后必须逐字得到小修后的
   Reader 单元。

## 输出与停止点

- `candidates/reader-unit-assembly-v1.md`：只含两处获准小修的 Reader 单元。
- `candidates/chapter-with-reader-v1.md`：保留完整 B1 的可逆装配候选。
- `review/P3-product-review-candidate.md`：与完整章节候选逐字相同的唯一产品审阅入口。
- 独立检查只能给出技术结论，不能宣布 P3 `PASS`。
- 本轮不得 promotion、不得写正式生产路径、不得声称已集成 `tandem-comments`。
