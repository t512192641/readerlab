# ReaderLab 盲审装配 v2 变更收据

## 原因

v1 `blind-review.md` 的三个“完整原文上下文”直接嵌入冻结 XHTML，HTML 标签、属性与图片引用噪声妨碍正常阅读。此次修复只处理匿名盲审材料的机械呈现层。

## 允许变化

- 将每个原文区的冻结 XHTML 机械渲染为可读 Markdown。
- HTML 标题转为 Markdown 标题。
- 段落分行并留空行。
- HTML entity 解码。
- 删除纯标签以及 `class`、`id`、`href`、`img` 等展示噪声。
- 数字脚注引用统一为 `[n]`。
- 在 `technical-audit.md` 末尾追加本次呈现修复与验证记录。

## 禁止变化

- 不摘要、不改写、不删句、不改变原文可见文字顺序。
- 不重新搜索、不重新审核、不重新随机。
- 不改变三组顺序、左右配对、左右成品或产品判断表。
- 不改变技术资格、实验有效性判定或成本比较内容。
- 不改变 `route-key.md`。
- 不宣布路线身份或胜负。

## v1 / v2 SHA-256

| 文件 | v1 SHA-256 | v2 SHA-256 | 结果 |
|---|---|---|---|
| `technical-audit.md` | `7733c312d4c6bffc54c4b01b930430098e160760f4a7a63c6bc34381797623d9` | `00c41f38a967b541993b3bffa2306b672ee2c962e981de50af2236bb427cb9f4` | 仅追加 v2 修复记录 |
| `blind-review.md` | `87ad18e6ef9210f86dc7a1ae498e6da04285a44c0412d68b8ccc482f21ea77a9` | `0d7840d915c3e80a35e86c5726deee3a83dd189628958988c1ac2d062faff3b1` | 仅原文呈现层变化 |
| `route-key.md` | `c0d8d07631c4072ded080e7ec27fb7a7509c7f36d7023525bffc57990e52fbd3` | `c0d8d07631c4072ded080e7ec27fb7a7509c7f36d7023525bffc57990e52fbd3` | 完全一致 |
| `cost-comparison.md` | `378883ed99536ead0e05b307903241ee7bdf8fb812d045e6276f75208cd537c3` | `378883ed99536ead0e05b307903241ee7bdf8fb812d045e6276f75208cd537c3` | 完全一致 |
| 正式 ZIP | `5b9e5b4b85458523d8b194d907eb43cb67c3c4dc637602ddad58915fb1936e6f` | `e61bdd09a752a1692b8820a6e5811e4fa5c2f60756d0430321930285578b0079` | v2 正式树 |

## 确定性验证结果

| 验证 | 结果 |
|---|---|
| U01 原 XHTML 可见文本序列与 v2 原文区规范化后相同 | PASS |
| U02 原 XHTML 可见文本序列与 v2 原文区规范化后相同 | PASS |
| U03 原 XHTML 可见文本序列与 v2 原文区规范化后相同 | PASS |
| 三组左右成品区与 v1 逐字一致 | PASS |
| 三组顺序与左右配对不变 | PASS |
| `route-key.md` hash 与 v1 完全一致 | PASS |
| `cost-comparison.md` hash 与 v1 完全一致 | PASS |
| v2 盲审匿名泄漏扫描 | PASS |
| v2 原文 XHTML 标签残留扫描 | PASS |
| 正式 ZIP 完整性 | PASS |
| 正式 ZIP 成员数与既定树 | PASS |
| 正式 ZIP 未包含自身 | PASS |
| 正式 ZIP 未包含 `change-receipt.md` | PASS |

`change-receipt.md` 是修复收据，按合同保留在 `pilot-review-v2/`，不收入正式 ZIP 树。

