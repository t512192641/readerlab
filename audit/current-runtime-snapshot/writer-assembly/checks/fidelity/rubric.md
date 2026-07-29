# 装配前 Reader 单元 Fidelity 独立检查

只允许读取：

- `inputs/writer-v2-accepted.md`
- `inputs/D3-expert.md`
- `inputs/locked-knowledge-cards.md`
- `inputs/review-outcomes.md`
- `inputs/D3-p2-gate.md`
- `control/assembly-protocol.md`
- `control/reader-unit-lineage.json`
- `candidates/reader-unit-assembly-v1.md`
- `evidence/writer-v2-to-assembly.diff`

只允许写 `checks/fidelity/result.json`；不得搜索、列目录或读取其他路径。

独立检查：

1. Reader 相对已接受 Writer v2 是否只有两处获准小修。
2. “禁忌交换”定义是否自然且与 K01/K02 的锁定含义一致，没有新增机制或扩大范围。
3. 象征性承认是否精确收窄为“部分愤怒和暴力反对指标”，并保持 K04 的较弱证据、
   实施信心空结果及实体问题边界。
4. K01—K05 的承重判断、方向交互、来源/Expert 综合区分、误用边界是否仍完整。
5. lineage、Reader id 与锚点是否未漂移；未锁定内容是否没有进入。

合同终局只允许 `保真通过`、`退回 Writer`、`阻塞并重开内容锁`；不得宣称 P3 产品接受。

只输出：

```json
{
  "schema": "readerlab-reader-fidelity-check/v1",
  "verdict": "保真通过",
  "checks": [{"id": "F1", "status": "PASS", "evidence": "简短证据"}],
  "unauthorized_change": false,
  "semantic_damage": [],
  "blocking_findings": [],
  "notes": ["技术终局不构成 P3 产品判词"]
}
```
