# ReaderLab v0.4 Writer Task

version: `v0.4-control-candidate`
date: `2026-07-30`
status: `control-only / not-executed`

## Purpose

本文件只定义 C5 Writer 的输入闭集、读者文本合同、保真边界和停止门。本轮不执行 Writer，不代写任何
Writer 草稿。

## Input whitelist（fresh context）

Writer 只能读取以下 4 类已冻结输入：

1. needed source context；
2. C5 contract；
3. structured asset；
4. C5 packet。

禁止读取 K10/C1、C5 candidate seed、teaching draft、expert review、product review、其他 Writer 版本、
Fidelity／cold-read 结果、历史 run、金标、搜索结果或任何新材料。不得联网、检索或补充事实。

## Fixed output fields

```text
candidate_id: C5
reader_text: <600–1000 Chinese characters; no internal terms>
framework: <plain-language statement of the external framework>
difference: <difference from the article's surface/current-case reading>
new_judgment: <the new judgment enabled by the framework>
claim_limit: <conditions and highest allowed claim>
transfer: <one transferable use outside the current case>
preservation_check: <all locked relations listed below: PASS | FAIL>
source_trace: <anchors inherited from the contract/asset; no new sources>
stop: PASS | STOP
```

`reader_text` 是未来 Writer 的输出字段名称，不是本文件中的草稿；控制文件不填入其内容。

## Reader and teaching requirements

- 面向正常成人读者；不要求研究背景、专业训练或另行查资料。
- 必须让读者读懂：框架是什么、它与原文表面意思有何不同、它带来什么新判断、主张在哪些条件下
  成立、离开当前案例后如何使用。
- 正文不得出现内部角色名、任务名、候选 ID、schema 名、审计标签、`source anchors`、`cognitive turn`
  或其他内部术语。
- 可以使用当前原文作为观察锚点，但不能把文本写成只关于当前案例的冲突断言。

## Locked relations Writer must preserve

Writer 必须忠实保留 structured asset 中已有的以下关系，不得删成口号、换成相反方向或提高断言强度：

- `value-distribution-execution`；
- `costs concentrated / benefits dispersed`；
- `free riding / fulfillment`；
- `source identity vs external structure`。

同时必须保留 `native problem`、独立语法、条件式判断、最高允许主张、new result、usage 和 boundary。
`source identity` 与 `external structure` 必须分开：来源身份不是结构本身，当前案例也不能冒充外部结构。

## Prohibited actions

- 不得选题、替 Expert 发现对象、添事实、补造机制、引入新来源、改变结论或捞回被禁止主张。
- 不得把 `value-distribution-execution` 改写成当前案例特有的“双方冲突”或单一责任归因。
- 不得用“这个案例证明……”取代条件式、可迁移的外部结构判断。
- 不得输出第二版本、备选稿、解释信或审计报告；一次只允许一个候选文本字段。

## Stop and acceptance gate

若四类输入不齐、结构化资产未达到 `ASSET_SUFFICIENT`、任一锁定关系缺失、字符范围不满足、需要外部
研究或文本只能成立为当前案例冲突，立即 `STOP`，不自行返工。只有读者文本和固定字段都齐全，才可交
Fidelity；Writer 通过不等于 Fidelity 或 cold-read 通过，也不等于产品接受。
