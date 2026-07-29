# 完整 B1、锚点与装配边界独立检查

只允许读取：

- `inputs/chapter-readable.md`
- `inputs/D3-expert.md`
- `control/assembly-protocol.md`
- `control/reader-unit-lineage.json`
- `candidates/reader-unit-assembly-v1.md`
- `candidates/chapter-with-reader-v1.md`
- `evidence/mechanical-receipt.json`

只允许写 `checks/assembly/result.json`；不得搜索、列目录或读取其他路径。

独立检查：

1. 完整 B1 来源 hash 是否为 `c936cde2…`，装配候选删除唯一完整插入块后是否 exact-byte
   恢复 B1，原文段落顺序是否不变。
2. 锚点是否确实来自 Expert 明示的“实际触发本课的完整段落（逐字）”，是否在 B1 中唯一，
   插入是否紧接完整锚点之后。
3. marker 之间是否 exact-byte 包含 `reader-unit-assembly-v1.md`，装配器是否没有改写、
   拆分、合并 Reader。
4. candidate-only marker 是否明确不是 `tandem-comments` 接口，没有恢复旧 callout、猜字段、
   promotion 或声称 P3 `PASS`。
5. lineage、Reader id、anchor hash、章节 hash 是否一致。

只输出：

```json
{
  "schema": "readerlab-assembly-boundary-check/v1",
  "verdict": "PASS",
  "checks": [{"id": "B1", "status": "PASS", "evidence": "简短证据"}],
  "exact_b1_recovery": true,
  "exact_reader_recovery": true,
  "anchor_unique": true,
  "boundary_violation": false,
  "blocking_findings": [],
  "notes": ["技术 PASS 不构成 P3 产品判词"]
}
```
