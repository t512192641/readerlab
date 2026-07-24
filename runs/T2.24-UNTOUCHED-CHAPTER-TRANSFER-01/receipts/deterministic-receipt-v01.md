# T2.24 确定性装配收据 v01

verification-status: PASS
p3-wait-start-utc: 2026-07-23T05:59:25.902352+00:00
p3-verdict-observed-at-utc: 2026-07-23T06:12:29.610115+00:00
product-status: ACCEPTED
terminal: TRANSFER_SAMPLE_ACCEPTED
assembly-wall-ms: 1

## 冻结身份

- chapter-scope-sha256: `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`
- canonical-readable-b1-sha256: `deaf67f74d3e8c44c58a62e77e98ed724c8bddef77bfb03e8bf601e6dbd3be90`
- bounded-reader-sha256: `b9d44500efeb555c5bb919ef1a6e511aabd06c9e22131e605ef71fb51f94f5b3`
- epistemic-reader-sha256: `ee8a9b19d66173c6ef970d04c7b5888c3c2c3372f0cb6d27f10eda3f74ecdeda`
- end-to-end-review-sha256: `75282fae7adb46be10b0ac9ca9288f7b589cb54a515fd8662ace78677f151487`
- product-verdict-sha256: `2b4004aa3e8b12b89eeca58cff26991d6cc7dd0ad94e10f800ee0ebde6f717eb`

## 锚点检查

| 对象 | 冻结 XHTML 逐字匹配 | 可读 B1 block 匹配 | 装配位置 |
|---|---:|---:|---|
| 情境性知识与认识论不正义 | 1 | 1 | 唯一锚点所在原文段落之后 |
| 有限理性与行政可读性 | 1 | 1 | 唯一锚点所在原文段落之后 |

两个陪读保持为独立 callout，没有合并框架。

## 可逆性检查

- canonical B1 blocks: `27`
- assembled Reader blocks: `2`
- remove-readers-restores-b1: `PASS`
- restored-readable-b1-sha256: `deaf67f74d3e8c44c58a62e77e98ed724c8bddef77bfb03e8bf601e6dbd3be90`
- byte-equal-to-canonical-readable-b1: `true`

## 装配边界

- 装配为确定性控制层操作，没有调用模型。
- 没有改写原文、Reader、锚点或语义内容。
- 产品审阅稿不包含控制标识、候选 ID、哈希或审计台账；这些只保留在本收据。

## 最终统计冻结

- usage-ledger-sha256: `6909227bd80cc30344e60c0f110d1438887adcce857e058907f35785777defa3`
- usage-summary-sha256: `3e8349754614841e06bbcc269ccf9b4f562da1bed6665ee0562bd6c52bd004d2`
- actual-model-calls: `16`
- model-retries: `0`
- tool-invocation-retries: `3`
- provider-token-coverage: `0/16`
- visible-token-coverage: `0/16`
- token-policy: 未取得的数据保持 `unknown`，未用字符数或零值替代。
