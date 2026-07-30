# ReaderLab v0.4 Expert Asset Audit Task

version: `v0.4-control-candidate`
date: `2026-07-30`
status: `control-only / not-executed`

## Purpose

本任务只审计 C5 已冻结资产是否足以交给 Writer。它不执行 Expert，不生成新课，不生成 C5 最终内容，
也不替 Expert 补写结构化资产。

## Input whitelist（fresh context）

运行时只能读取以下 5 个 C5 冻结输入，名称和角色不得扩展：

1. C5 frozen v0.1 candidate seed；
2. C5 teaching draft；
3. C5 source map；
4. C5 expert review；
5. C5 product review。

除执行本任务所需的控制指令外，不得读取任何合同文件（包括 `contract-task.md`）、K10/C1 材料、其他
run、source context、搜索结果、金标、反例、Writer 草稿、Fidelity 或 cold-read 结果；不得联网或创建新 seed。

## Fixed output fields

```text
candidate_id: C5
input_set: <the five allowlisted inputs, by frozen identity>
field_coverage: <PASS | FAIL for each required contract field>
source_map_closure: PASS | FAIL
expert_review_presence: PASS | FAIL
product_review_presence: PASS | FAIL
asset_status: ASSET_SUFFICIENT | ASSET_NEEDS_TARGETED_SUPPLEMENT | ASSET_UNUSABLE
missing_or_blocking_fields: <field names only>
targeted_supplement_scope: NONE | <one bounded missing field and its frozen-input location>
writer_handoff: ALLOW | HOLD
stop_reason: <required when writer_handoff is HOLD>
```

## Status rules

- `ASSET_SUFFICIENT`：五个输入身份完整，固定字段和来源映射闭合，资产足以让 Writer 只做组织表达；
  只允许交接到 C5 Writer，不代表 Writer 已执行或已通过。
- `ASSET_NEEDS_TARGETED_SUPPLEMENT`：只允许指出一个可定位、有限、与现有 source map 相容的缺口；
  不得开放搜索、增加 seed、另找对象或自行补写语义。补充未冻结前必须 `writer_handoff: HOLD`。
- `ASSET_UNUSABLE`：身份、来源、外部对象结构或核心合同无法恢复；立即停止，不得启动 Expert、Writer、
  Fidelity 或 cold-read。

## Prohibited boundary crossings

- 不得把 audit 变成 Expert 重写、来源研究、候选比较或产品判词。
- 不得把 `expert review` 或 `product review` 的结论扩写成新的语义资产。
- 不得把字段完整、文件存在或模型自述当作内容真实或产品接受的证明。
- 不得为继续 Writer 而静默修改冻结输入、合同、路由或版本。

## Stop and acceptance gate

任何白名单外读取、无法定位的缺口、需要新知识来源的补充、或三种状态之外的判断，立即停止。验收门：
输出字段齐全、状态为三者之一、缺口只写字段和定位、`ASSET_UNUSABLE` 不越过 Writer 门；审计通过不等于
产品负责人接受。
