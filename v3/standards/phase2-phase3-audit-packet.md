# Phase 2/3 骨架军师审计包

## 审计范围

本包只提交 repo-local 骨架，不写入 LifeAtlas 正式沉淀区。

## Phase 2：五登记簿 + 种子 + 查重

| 项目 | 文件 | DoD 自检 |
| --- | --- | --- |
| 五登记簿 schema | `v3/asset-layer/schemas.md` | 5 类登记簿，文件 49 行；包含读写协议；未写入 LifeAtlas。 |
| 种子条目 | `v3/asset-layer/ledger-seeds.md` | 工具箱种子 2 条：`多学科思维模型`、`第一性原理`；使用 Obsidian wikilink 形式。 |
| 查重协议 | `v3/asset-layer/dedup-protocol.md` | 包含名称键、来源键、做法键、边界键、关系键；写回前分新建、更新、放弃。 |

五登记簿清单：

1. 工具箱清单：`toolbox.md`
2. 阅读履历：`reading-ledger.md`
3. 开放问题：`open-questions.md`
4. 读法卡：`reading-moves.md`
5. 资产卡：`asset-cards.md`

Phase 2 结论：骨架满足“登记簿数量正好 5、schema 有读写协议、种子条目合规、查重协议存在”。正式 LifeAtlas 写回仍需用户确认。

## Phase 3：Skill 骨架

| 项目 | 文件 | DoD 自检 |
| --- | --- | --- |
| Skill 入口 | `v3/skill/SKILL.md` | 98 行；包含触发、路由、工作流、读者页输出限制、停止条件。 |
| 图书引擎 | `v3/skill/protocols/book-engine.md` | 145 行；包含死刑制、讲堂体、全读者可见产物自检。 |
| Skill 引擎 | `v3/skill/protocols/skill-engine.md` | 47 行；包含净化正文、产品解读、技术负责人讲解、资产卡标准。 |
| Judge 协议 | `v3/skill/protocols/judge.md` | 43 行；覆盖图书线和 Skill 线，声明用户判定不被机器替代。 |
| 模板 | `v3/skill/templates/` | 7 个模板：图书章节页、冰山页、读法卡、Skill 主读页、技术负责人页、资产卡、沉淀候选区。 |
| 范例库 | `v3/skill/examples/` | 包含图书批注金标、反例、讲堂体金标缺文本记录；用于生成与裁判 prompt。 |

模板清单：

- `book-chapter-page.md`
- `iceberg-page.md`
- `reading-move-card.md`
- `skill-main-page.md`
- `technical-lead-page.md`
- `asset-card.md`
- `distillation-candidates.md`

## 干跑结果

干跑文件：`v3/pilots/phase3-dry-run.md`

结果：

- 中文读者页：通过。
- 无模板残留：通过。
- 未把候选写入正式登记簿：通过。
- 未把裁判记录写入读者页：通过。

## 行数 / 预算检查

当前行数：

- `v3/skill/SKILL.md`：98 行。
- `v3/skill/protocols/book-engine.md`：145 行。
- `v3/skill/protocols/skill-engine.md`：47 行。
- `v3/skill/protocols/judge.md`：43 行。
- `v3/asset-layer/schemas.md`：49 行。

结论：入口 Skill 和协议文件保持在骨架预算内；book-engine 因 Phase 1 收档追加讲堂体与自检规则，略厚但仍可人工审计。

## 本轮验证

- `git diff --check`：通过。
- `python3 tests/test_readerlab.py`：通过，30 个测试。
- `python3 tests/test_fullbook_demo_validate.py`：通过，6 个测试。
- `python3 tests/test_review_pack_validate.py`：通过，15 个测试。
- `python3 tests/test_readerlab_trace_validator.py`：未运行，当前仓库没有该文件；现有测试文件为 `tests/test_fullbook_demo_validate.py`、`tests/test_readerlab.py`、`tests/test_review_pack_validate.py`。
- 模板数量：7。
- 登记簿 schema 数量：5。
- `gstack/browse` 重写页术语检查：`cookie`、`token`、`ARIA` 均在正文内解释；未出现用户反馈中的 `AIRA` 或未解释的 `eval`。

## 已知缺口

- 军师 H03 示范段原文未入库，范例库已记为缺文本状态；不能宣称讲堂体金标已完整内嵌。
- Phase 2 登记簿只完成 repo-local schema 与种子，不写入 LifeAtlas 正式区。
- Phase 3 是骨架，不是完整自动生成器。
