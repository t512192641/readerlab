# ReaderLab v0.4 Cold Read Task

version: `v0.4-control-candidate`
date: `2026-07-30`
status: `control-only / not-executed`

## Purpose

本任务用全新上下文检查普通成人读者能否仅凭必要 source context 和 Writer draft 读懂并迁移使用。它不
做研究、不补解释、不读取内部合同，也不改写 Writer 文本。

## Input whitelist（fresh context）

只能读取：

1. 为理解当前原文所必需的最小 source context；
2. C5 Writer draft；
3. 本文件固定的 8 个问题。

禁止读取 contract、structured asset、candidate seed、teaching draft、expert review、product review、
Fidelity 结果、历史答案、搜索结果或其他候选材料。读者不需要研究背景、内部术语或外部资料。

## Fixed eight questions

每题只记录 `PASS | FAIL | UNCLEAR`，不得改写问题或另加问题：

1. 读完后，读者能否用自己的话说出文中所教的外部框架及其要解决的问题，而不只是复述原文？
2. 读者能否说出这个框架与作者原文表面意思或当前案例读法的差别？
3. 读者能否指出它让自己对原文产生的至少一个新判断，而不是只得到一个新名词？
4. 读者能否解释价值、分配、执行如何连在一起，以及这条关系改变了什么观察？
5. 读者能否解释为什么在成本集中、收益分散时会出现搭便车或履约问题，而不需要先查专业背景？
6. 读者能否说出这套判断在哪些条件下成立、何时不能支持更强结论？
7. 读者能否把这套结构迁移到另一个未给出的情境，而不是把当前案例的冲突结论照搬过去？
8. 从观察到机制、判断、边界再到迁移的因果链是否完整，没有必须依靠研究背景才能补上的跳步？

## Fixed output fields

```text
reader_context: <minimal source context identity>
draft_identity: <C5 Writer draft identity>
question_1: PASS | FAIL | UNCLEAR
question_2: PASS | FAIL | UNCLEAR
question_3: PASS | FAIL | UNCLEAR
question_4: PASS | FAIL | UNCLEAR
question_5: PASS | FAIL | UNCLEAR
question_6: PASS | FAIL | UNCLEAR
question_7: PASS | FAIL | UNCLEAR
question_8: PASS | FAIL | UNCLEAR
background_required: NO | YES
internal_terms_required: NO | YES
causal_chain_gap: NO | YES
barrier: <short reader-facing barrier; no rewrite>
final: COLD_READ_PASS | RETURN_WRITER
stop: PASS | STOP
```

## Final mapping and prohibitions

- 8 题全部 `PASS`，且 `background_required: NO`、`internal_terms_required: NO`、`causal_chain_gap: NO`：
  `COLD_READ_PASS`。
- 任一题为 `FAIL`／`UNCLEAR`，或需要研究背景、内部术语、补造因果链：`RETURN_WRITER`。
- Reviewer 不得替 Writer 补句、重排、解释或生成 v2；只能记录 barrier 并停止。
- 不得把“读者知道答案”混同于“读者理解结构”；不得要求读者记忆内部字段名或角色名。

## Acceptance gate

验收门是新上下文、白名单闭合、8 个问题逐项有结果、终局只能为 `COLD_READ_PASS` 或 `RETURN_WRITER`，
且没有研究、内部术语或因果链缺口。通过仍需产品负责人审阅，不自动构成产品接受。
