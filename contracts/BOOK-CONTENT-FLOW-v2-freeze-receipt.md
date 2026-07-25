---
status: frozen
scope: long-term
---

# 图书内容流合同 v2 冻结收据

## 技术激活结论

- 技术激活状态：`TECHNICALLY_ACTIVE`
- 独立工程审查结论：`PASS`
- 哈希算法：`SHA-256`；摘要按合同冻结后的最终字节计算，并以 64 位小写十六进制记录

| 合同路径 | SHA-256 | bytes |
|---|---|---:|
| `contracts/BOOK-CONTENT-FLOW-v2.md` | `daf2e546ec84715481746056abb7ed58110468ec64d424c440600139cca67e91` | `21930` |

## 历史身份边界

`contracts/T1.3-discovery.md`、`contracts/T1.4-expert-and-knowledge-card.md`、
`contracts/T1.5-independent-review.md`、`contracts/T1.6-writer.md`、
`contracts/T1.7-b2-assembly.md` 及 `contracts/M1-freeze-receipt.md` 原样保留为 M1 历史证据。
本收据不修改、不重新绑定或替代这些历史字节与身份。

## 证据边界

本收据只绑定上述 v2 合同的路径、冻结字节数、SHA-256 与独立工程审查 `PASS` 结论。它不绑定
本收据自身或任何 commit hash，也不复制、引用或替代合同正文。

技术激活只证明现行长期合同身份已经冻结并取得工程侧启用资格；不证明内容生产 runtime 已
`integrated`，不证明真实链路已经 `verified`，也不构成产品负责人 `accepted`。本收据不授权
Writer、不授权创建新 run，也不改变 `CURRENT-STATE.md` 的当前停止点或唯一产品前进行动。
