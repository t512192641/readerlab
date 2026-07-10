# ReaderLab V3 回归套件索引

状态：29 张逐 case 卡已独立执行并与限定预期匹配。本文件只做索引和汇总；样本、原判词、证据缺口与预期以 case 卡为准，原始判断以 `v3/eval/constraint-redesign-r2/` 为准。

## 判定纪律

- `historical`：必须有既有样本及原判词或后续真实结论；没有逐字原话就明确写无，不得补写。
- `derived-structure`：用具体最小场景检查当前规则结构，不是历史重放，也不证明发生过真实运行。
- 执行者逐卡读取明确路由的证据，不用本文件的 expected 代替实际判断。
- 正例只保护原证明范围；硬负例必须淘汰；scope-lock 不得升级。
- case 与 expected 冲突、证据无法定位或规则无法判定时记 `blocked`，不得用汇总表掩盖。

## 图书历史 cases

| id | kind | case card | expected | actual |
| --- | --- | --- | --- | --- |
| B-P01 | historical | `v3/standards/regression-cases/book/B-P01.md` | accept | accept (matched) |
| B-P02 | historical | `v3/standards/regression-cases/book/B-P02.md` | accept | accept (matched) |
| B-P03 | historical | `v3/standards/regression-cases/book/B-P03.md` | accept | accept (matched) |
| B-N01 | historical | `v3/standards/regression-cases/book/B-N01.md` | reject | reject (matched) |
| B-N02 | historical | `v3/standards/regression-cases/book/B-N02.md` | reject | reject (matched) |
| B-N03 | historical | `v3/standards/regression-cases/book/B-N03.md` | reject | reject (matched) |
| B-N04 | historical | `v3/standards/regression-cases/book/B-N04.md` | reject | reject (matched) |
| B-N05 | historical | `v3/standards/regression-cases/book/B-N05.md` | reject | reject (matched) |
| B-N06 | historical | `v3/standards/regression-cases/book/B-N06.md` | reject | reject (matched) |
| B-N07 | historical | `v3/standards/regression-cases/book/B-N07.md` | reject | reject (matched) |
| B-N08 | historical | `v3/standards/regression-cases/book/B-N08.md` | reject | reject (matched) |
| B-N09 | historical | `v3/standards/regression-cases/book/B-N09.md` | reject | reject (matched) |

原始结果：`v3/eval/constraint-redesign-r2/regression-book-raw.md`。

## Skill cases

| id | kind | case card | expected | actual |
| --- | --- | --- | --- | --- |
| S-P01 | historical | `v3/standards/regression-cases/skill/S-P01.md` | scope-lock | scope-lock (matched) |
| S-P02 | historical | `v3/standards/regression-cases/skill/S-P02.md` | scope-lock | scope-lock (matched) |
| S-N01 | derived-structure | `v3/standards/regression-cases/skill/S-N01.md` | reject | reject (matched) |
| S-N02 | derived-structure | `v3/standards/regression-cases/skill/S-N02.md` | reject | reject (matched) |
| S-N03 | derived-structure | `v3/standards/regression-cases/skill/S-N03.md` | reject | reject (matched) |
| S-N04 | derived-structure | `v3/standards/regression-cases/skill/S-N04.md` | reject | reject (matched) |
| S-N05 | derived-structure | `v3/standards/regression-cases/skill/S-N05.md` | reject | reject (matched) |
| S-N06 | derived-structure | `v3/standards/regression-cases/skill/S-N06.md` | reject | reject (matched) |
| S-N07 | historical | `v3/standards/regression-cases/skill/S-N07.md` | reject | reject (matched) |
| S-N08 | historical | `v3/standards/regression-cases/skill/S-N08.md` | scope-lock | scope-lock (matched) |

原始结果：`v3/eval/constraint-redesign-r2/regression-skill-raw.md`。

## 运行完整性派生 cases

以下全部是 `derived-structure`，`historical_run: false`。

| id | case card | expected | actual |
| --- | --- | --- | --- |
| RI-N01 | `v3/standards/regression-cases/run-integrity/RI-N01.md` | reject | reject (matched) |
| RI-N02 | `v3/standards/regression-cases/run-integrity/RI-N02.md` | reject | reject (matched) |
| RI-N03 | `v3/standards/regression-cases/run-integrity/RI-N03.md` | reject | reject (matched) |
| RI-N04 | `v3/standards/regression-cases/run-integrity/RI-N04.md` | reject | reject (matched) |
| RI-N05 | `v3/standards/regression-cases/run-integrity/RI-N05.md` | reject | reject (matched) |
| RI-N06 | `v3/standards/regression-cases/run-integrity/RI-N06.md` | reject | reject (matched) |
| RI-P01 | `v3/standards/regression-cases/run-integrity/RI-P01.md` | accept-structure-only | accept-structure-only (matched) |

最新原始结果：`v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md`。此前通过与后续暴露 schema / dispatch / fixture 缺口的失败记录均保留，不作为最新结果替代品。

## 套件通过条件

- 29 张卡均有独立 actual、匹配状态、实际证据与作用域；不得合并跳过单卡。
- B-P01—B-P03 保持原范围；B-N01—B-N09 淘汰。
- S-P01/S-P02/S-N08 保持原作用域；S-N01—S-N07 按卡预期淘汰。
- RI-N01—RI-N06 被结构门拦截；RI-P01 只证明合规结构可表达，仍为 `runtime-not-run`。
- 任一 `blocked` 或 mismatch 都使套件失败并停下，不靠新增作者禁令修补。
