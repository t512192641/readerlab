# T2.12 组装与计时收据

experiment-id: T2.12-NON-BERGER-INLINE-READING-PROTOTYPE-01
active-version: v01
result: READY
production-started-at: 2026-07-22T08:06:07Z
production-finished-at: 2026-07-22T08:10:27Z
total-wall-seconds: 260
product-wait-included: false

## 分段计时

| stage | started_at | finished_at | wall_seconds | retries | result |
|---|---|---|---:|---:|---|
| preflight | 2026-07-22T08:06:07Z | 2026-07-22T08:06:54Z | 47 | 0 | READY |
| object-01-anchor-and-assembly | 2026-07-22T08:06:54Z | 2026-07-22T08:07:40Z | 46 | 0 | READY |
| object-02-anchor-and-assembly | 2026-07-22T08:07:20Z | 2026-07-22T08:08:34Z | 74 | 0 | READY |
| aggregate-and-check | 2026-07-22T08:08:34Z | 2026-07-22T08:10:27Z | 113 | 0 | READY |

两个对象线有 20 秒重叠；总墙钟按统一起止时间计算，不把分段秒数机械相加。整轮 260 秒，低于本卡 5—8 分钟目标区间的上限，也未触发 10 分钟报警线。

## 输入身份

- EPUB SHA-256：`3baf9932c92412f0e7d0ccae993182f55f62e2fab5ec46a3882d675476288664`
- `text/part0019.html` member SHA-256：`c72b2e794266b7eb0d2589045328ea98c9511d8a56aa4037d924e036d1fac891`
- 完整 scope：`13337` bytes；SHA-256：`216f3a01176e10084ee7a011da7f85cd8bb6e6f1558546db6414f9a285b05dad`
- object-01 冻结讲义 SHA-256：`1fbcb1335a8fa4e9906daf9a24eb288715535adc997609e40013fb5eff45118f`
- object-02 冻结讲义 SHA-256：`a57120f6ea82088c0edc02c84acf5d9cc29957a6a40f586df2a47038b614b670`

## 交付身份

- `raw/object-01-anchor.md` SHA-256：`c3fd9666e6aad51ec7d933b851326f0d29f22cc10f52ebd2d0b0919287fa26e7`
- `raw/object-02-anchor.md` SHA-256：`24dbb729d0a291527a33f41e508bcc7741b137989d406cee83fe3ec90e63b8b0`
- `review/inline-reading-v01.md` SHA-256：`d87a48a513a58787cee7351412c136650ec1554984788e32d1faa42f52b97c1a`

## 最小核验

- 两个对象均为 `READY`，各自只有一个实质锚点，返工次数均为 `0`。
- 去除 Obsidian callout 并忽略空白后，v01 原文与已核验的完整章节 Markdown 原文逐字一致：`4210 / 4210` 非空白字符。
- 阅读页只有宗派化与诺斯两个陪读 callout；未保留伯格内容，未包含远程 URL。
- 本轮未联网、未重做来源研究、未读取来源审计、金标、examples、其他未授权 run 或旧 ReaderLab。
- 未新增或修改共享 validator、schema、manifest、README、长期 owner 或自动化入口。

## 停止点

技术交付达到 `implemented / integrated / verified`，产品阅读体验仍为 `unknown`。下一步只能由产品负责人阅读 `review/inline-reading-v01.md`，分别判断两处连接和整章阅读体验；判词前不得继续未见章节生产。

