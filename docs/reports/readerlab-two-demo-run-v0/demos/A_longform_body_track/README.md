# Demo A: Longform Body Track

本 demo 只验证 repo-owned longform material 的正文轨与陪读包形态，不验证外部书籍泛化能力。

## Source

- 源文件：`docs/product-spec.md`
- source_type：`longform_owned_material`
- 材料类型：`book_longform`
- 覆盖范围：完整文件正文

## Artifacts

- `source-registry.json`
- `10_一手正文/001_正文.md`
- `20_AI陪读/001_reader-facing.md`
- `audit/contracts/body-track-gate.json`
- `audit/contracts/material-profile.json`
- `audit/contracts/claim-ledger.json`
- `audit/contracts/candidate-tournament.json`
- `audit/contracts/skillization-gate.json`
- `audit/contracts/annotation-trigger.json`
- `audit/contracts/high-order-explanation.v1.json`
- `audit/location-map.json`
- `audit/trace-to-reader.md`
- `audit/eval.md`

## Writer Status

`writer_ready_for_reader_eval`

Writer 未给最终通过结论；需要独立 reader evaluation 后才能判断是否内部通过。

## Review Hardening

- `location-map.json` 给正文段落、读者页段落、claim、candidate 和批注触发建立稳定锚点。
- `trace-to-reader.md` 说明 reader-facing 每段如何消费正文、claim 和候选决策。
- 批注插件本身不是本 demo 的风险；本 demo 补的是批注回读时如何从评论位置回到 ReaderLab 证据链。
