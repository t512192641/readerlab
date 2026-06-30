# DB Skill 阅读化测试报告

## 测试目的

用本地已有的 `dbs-suite` 作为非 gstack 压力样本，验证 ReaderLab 的复杂材料阅读化 SOP 是否能迁移到另一套复杂 Skill 包。

本次测试最终写入 LifeAtlas 200 阅读材料区，不改 DB Skill 源包，不新增依赖，不写入 LifeAtlas `300/600/800`。

## 样本来源

- 源包：`/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite`
- 包来源：`https://github.com/dontbesilent2025/dbskill.git`
- 本地版本：`2.12.0+local`
- Skill 数：23
- 早期机器试跑输出：`/private/tmp/readerlab-dbskill-test/dbs-suite`
- 当前 Obsidian 验收输出：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite`

## 机器验证

### 早期临时导入

命令：

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /private/tmp/readerlab-dbskill-test --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件" --force
```

结果：

- files_scanned：25
- skills：23
- reading_units：1
- delivery_status：`in_progress`

### 临时 validate

命令：

```bash
python3 scripts/readerlab.py validate /private/tmp/readerlab-dbskill-test/dbs-suite
```

结果：

- passed：true
- total_skills：23
- completed_skills：0
- needs_review_skills：0
- not_started_skills：23
- total_source_blocks：1864
- delivery_status：`in_progress`

首轮结果符合预期：当时 ReaderLab 生成器能导入和建 manifest，但没有 DB Skill 的精读产物，所以不会生成 completed 阅读页。

补做精读产物后，重新导入 LifeAtlas 200 结果为：

- files_scanned：25
- skills：23
- reading_units：6
- delivery_status：`in_progress`

LifeAtlas 200 validate 结果为：

- passed：true
- total_skills：23
- completed_skills：5
- needs_review_skills：0
- not_started_skills：18
- total_source_blocks：1864
- delivery_status：`in_progress`

LifeAtlas 200 路径：

```text
/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
```

## 样本 1：dbs-save

### 材料类型

`dbs-save` 是状态/流程型复杂材料。它定义“诊断存档”这个动作，包括判断是否可存、标题提取、路径拼接、文件格式、回执、列表模式、状态字段、下一步字段和边界情况。

### 内容分层

| 内容类别 | 判断 |
|---|---|
| 一手主体内容 | 为什么需要存档；何时触发；项目隔离；五步工作流；frontmatter 与 body 结构；list 模式；status/next_skill 字段规则；敏感信息提示。 |
| AI 导读和 highlight | 应提醒读者：它不是诊断工具，而是把诊断结果固化成可恢复状态；重点应标“不要存空文件”“固定 6 段结构”“本地纯文本未加密”。 |
| 关联说明 | `slug`、`snapshot`、`session` 的用户话术映射；`~/.dbs/sessions/{slug}/` 的目录意义；与 `dbs-restore` 的关系。 |
| 运行/机器细节 | `mkdir -p`、时间戳生成、文件名去重、路径拼接细节；这些应放机制说明，不抢主线。 |
| 完整追溯材料 | 完整 YAML 模板、完整回执模板、完整 list 输出模板、block manifest 和 hash。 |

### 预览验收判断

PASS。SOP 能清楚处理这个材料：主阅读页应围绕“把诊断从单次对话变成可恢复状态”展开；完整模板和路径规则放机制说明或附录。

当前生成器已能读取 `data/skill-readings/dbs-suite/dbs-save.json` 并生成 completed 主阅读页。页面位置：

- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/05_状态记忆与报告/dbs-save.md`

## 样本 2：dbs-report

### 材料类型

`dbs-report` 是报告/证据汇总型复杂材料。它定义如何从多份 `dbs-save` 存档生成可交付 Markdown 报告。

### 内容分层

| 内容类别 | 判断 |
|---|---|
| 一手主体内容 | 报告只读存档，不从对话凭空总结；确认数据量；解析 frontmatter 和 6 段 body；按 6 段报告结构合并；永不覆盖；冲突结论保留并标注修正关系。 |
| AI 导读和 highlight | 应提醒读者：可信度来自存档文件，不来自 AI 二次发挥；重点应标“不凭空总结”“永不覆盖”“冲突结论新旧都列”。 |
| 关联说明 | 与 `dbs-save` 的数据依赖；`~/.dbs/reports/{项目名}/` 的输出位置；`--since` 和 `--slug` 如何改变输入范围。 |
| 运行/机器细节 | 文件排序、路径拼接、目录创建、状态中文映射；放机制说明。 |
| 完整追溯材料 | 完整报告模板、完整边界情况、完整回执模板、block manifest 和 hash。 |

### 预览验收判断

PASS。SOP 能清楚处理这个材料：主阅读页要突出“可信来源、合并规则、报告结构、冲突处理”，不是把完整模板直接塞进正文。

当前生成器已能读取 `data/skill-readings/dbs-suite/dbs-report.json` 并生成 completed 主阅读页。页面位置：

- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/05_状态记忆与报告/dbs-report.md`

## 横向验收

| 验收项 | 结果 | 说明 |
|---|---|---|
| 本地 DB Skill 是否存在 | PASS | `dbs-suite` 存在，含 23 个 Skill。 |
| 是否足够复杂 | PASS | `dbs-save`、`dbs-report` 都有流程、模板、状态、路径、边界情况和输出契约。 |
| ReaderLab 是否能导入 | PASS | 临时导入成功，manifest 生成。 |
| ReaderLab validate 是否通过 | PASS | 临时输出 validate 通过。 |
| SOP 是否适用 | PASS | 两个样本都能按五类内容分层。 |
| 当前生成器是否已自动产生成品页 | PASS/PARTIAL | `dbs-save`、`dbs-report`、`dbs-diagnosis`、`dbs-good-question`、`dbs-xhs-title` 已生成 completed 预览页；整包仍有 18 个 Skill 未完成。 |
| 复杂核心样本是否覆盖 | PASS | 已补做 `dbs-diagnosis`（商业诊断核心框架）、`dbs-good-question`（问题说明书 / Agent 可解性）、`dbs-xhs-title`（75 公式长库型材料）。 |
| 分组是否改善 | PASS/PARTIAL | 已改为结构优先的阅读路线规划；`dbs-good-question` 进入 `03_问题决策与行动系统`，`dbs-xhs-title` 进入 `04_内容表达与素材模板`。当前 DB Skill 无项目进入 `90_材料结构诊断`。 |
| 插件批注闭环是否在 DB 生成页上跑通 | PASS | LifeAtlas 200 中 `dbs-save.md` 的 `tandem-comments` anchor 定位成功，Codex 回复追加后 thread_count 从 1 变 2。 |
| 插件批注闭环是否在复杂核心页跑通 | PASS | LifeAtlas 200 中 `dbs-diagnosis.md` 的 `tandem-comments` anchor 定位成功，Codex 回复追加后 thread_count 从 1 变 2。 |

## 结论

DB Skill 测试已经从“只验证 SOP 和导入”推进到“5 个真实 DB Skill completed 预览页已生成并通过机器验收”，其中包含 3 个更复杂的核心样本。

当前仍不能声称整个 `dbs-suite` 已完成，因为 23 个 Skill 中只有 5 个 completed，18 个仍是 `not_started`。

分组机制已从 gstack 固定组 + 关键词兜底推进到结构优先的阅读路线规划。它已经能处理当前 DB Skill 样本，并在 manifest 中输出用途、判断理由、判断依据、把握程度和结构状态。

下一步应优先做两件事：

1. 把“主阅读页 / 机制说明 / 证据附录”进一步结构化到生成页面。
2. 结构不清时输出材料结构诊断，不能硬塞进旧组，也不让用户替机器分组。

## 已验证命令

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /private/tmp/readerlab-dbskill-test --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件" --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-dbskill-test/dbs-suite
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件，并在 Obsidian/LifeAtlas 200 区完成预览审阅与批注闭环"
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py block-manifest /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-save/SKILL.md --skill dbs-save --source-file dbs-save/SKILL.md
python3 scripts/readerlab.py block-manifest /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-report/SKILL.md --skill dbs-report --source-file dbs-report/SKILL.md
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/05_状态记忆与报告/dbs-save.md
python3 scripts/readerlab.py comments-reply /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/05_状态记忆与报告/dbs-save.md rl-dbs-lifeatlas-001 --author Codex --text "是。这里的关键不是文件有没有写出来，而是不能把没有诊断内容的对话写成可恢复状态；否则后续 dbs-restore 和 dbs-report 会把空状态当成事实来源。"
```
