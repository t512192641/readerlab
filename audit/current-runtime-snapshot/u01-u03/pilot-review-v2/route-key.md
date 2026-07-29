# 匿名路线密钥

## 可复验机械随机方法

对每个单元计算：

```text
SHA256("readerlab-abc-pilot-v1|" + U_ID + "|" + 该单元冻结输入的 SHA-256)
```

读取结果的第一个字节：奇数时 D 直接路线置左，偶数时 ABC 路线置左。右边为另一条路线。字符串按 UTF-8 编码，不含换行。

| 单元 | 冻结输入 SHA-256 | 随机摘要 | 第一个字节 | 左边 | 右边 |
|---|---|---|---:|---|---|
| U01 | `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c` | `17a73f1bbb15435265c4cf8463bb40ed1dcafb0e169ede0116e2d91b4a512590` | `0x17`（奇） | D 直接路线 | ABC 路线 |
| U02 | `27a0ef436b8d6e57ca9e6cb0cf4b43babe76f6852857edad0c2b6ae30bcf9e04` | `518c58c6a7a9d06f8d9a7e67a7cf6138b178996f2daa1f313480191f72df7f08` | `0x51`（奇） | D 直接路线 | ABC 路线 |
| U03 | `0f4af98ac9beb82cea8d4ad708191bf28aa7758645249e0640d6c1d9d5c4f88a` | `506b46cd7d91816b7d3232ebf9a3a5831f8c72fc9130fced33aa4daeced30f2e` | `0x50`（偶） | ABC 路线 | D 直接路线 |

