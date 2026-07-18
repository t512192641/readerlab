---
status: frozen
scope: long-term
---

# M1 冻结收据

## Gate 结论

- 固定审核 HEAD：`4efa709d24c741218ed2a64982c55b3488cc5e95`
- 审核范围：`4623abce80071ca3d2de90efc7312f816aa8338e^..4efa709d24c741218ed2a64982c55b3488cc5e95`
- 审核结论：`M1 PASS`，四项均为 `PASS`
- 附加冻结条件：`C1` 已获本次明确授权；术语表与 T1.1–T1.8、T1.9 v1 一并纳入冻结集和本收据
- 哈希算法：`SHA-256`；摘要按各文件冻结后的最终字节计算，并以 64 位小写十六进制记录

## 冻结身份

| 路径 | SHA-256 |
|---|---|
| `contracts/GLOSSARY.md` | `333b3eb4840cea16b7f5049fe7a8dbba09ddedb4ecb2b37479c1c13129737844` |
| `contracts/T1.1-material-intake.md` | `00aa1cd34bed83310878bd679552b85faaa4f5c05f6cb5d34ee8c49dde7c8cc2` |
| `contracts/T1.2-b1-source.md` | `c31d27f364c02b237f3b650eda4946799bf12a2a8d960f6eadaaab0514cd4866` |
| `contracts/T1.3-discovery.md` | `c56377d70861237f39d773ba414c4080d7a2e163962d256e98a0faf388b05178` |
| `contracts/T1.4-expert-and-knowledge-card.md` | `979cf646150b4085ae36d47104261ad76e22fbce986313cbad57e89f511b8048` |
| `contracts/T1.5-independent-review.md` | `aa55e7f1136f9fa59577134c1ead5f675042a33900a8db9b78d4f7002d932de8` |
| `contracts/T1.6-writer.md` | `79a15346dea8d90bbde1f14bdb9fc7b966cd38438ed0eed357b8da4ac7190129` |
| `contracts/T1.7-b2-assembly.md` | `6bbaaae335c2737a543b791118c2dddc44afe78e861e8df956eeb96728b9b474` |
| `contracts/T1.8-independent-acceptance.md` | `7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093` |
| `lenses/T1.9-seed-lenses.md` | `cffdf3fe5d1cf104cf51d4c5a4f187ea88243391dadb616a3a57ff64fae7cd07` |

## 证据边界

本收据只证明上述冻结正文的身份与 hash，不复制、引用或替代正文，也不对本收据自身计算 hash。

本次冻结不证明 runtime `integrated`、真实材料 `verified`、资格通过、semantic／product 合格或 `accepted`。
