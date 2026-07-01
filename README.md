# ReaderLab

ReaderLab 是复杂材料陪读系统：把书籍、长文、课程资料、代码文档、Skill 包和混合型资料，转成中文可读、可批注、可讨论、可沉淀的 LifeAtlas 阅读包。

当前默认环境：

```text
Obsidian + Markdown + Codex + 现有批注插件
```

## 核心结构

```text
一手正文轨：书籍/长文原样正文，或 Skill/工程材料净化正文
AI 陪读轨：全局讲解、高阶讲解、误读防护、候选沉淀
audit/contracts/eval：来源、位置、claim、candidate、gate、机器验收
```

AI 不替代人的第一次阅读。它负责降低阅读阻力、讲清结构、标出边界、解释技术和设计取舍；读者仍在正文附近阅读、批注和判断。

## 当前状态

- repo-local Skill 已激活：`.agents/skills/readerlab/SKILL.md`
- trace validator 已实现 reader paragraph trace 检查。
- 最小验证 fixtures 在 `tests/fixtures/readerlab/`。
- 《埃隆之书》整书 ReaderLab 章节解读已放到 LifeAtlas：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629/10_中文精读/03_ReaderLab整书章节解读/`

不能宣称：

- production ready
- global Skill installed
- public external validation pass
- `transferable_method_kernel_pass`
- real Obsidian body-prose annotation full pass

## 核心入口

- `AGENTS.md`：项目规则和启动顺序。
- `docs/current-task.md`：当前唯一执行事实源。
- `docs/dev-state.md`：稳定路径和命令。
- `docs/decisions.md`：耐久决策。
- `.agents/skills/readerlab/SKILL.md`：repo-local ReaderLab Skill。
- `docs/contracts/`：事实层 contract。

## 验证

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
```
