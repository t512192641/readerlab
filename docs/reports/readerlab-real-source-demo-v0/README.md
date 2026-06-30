# ReaderLab real-source demo v0

这个目录用于纠正上一轮误用 ReaderLab proof 样本的问题。本轮只使用两个真实来源：

- DB Skills 场景：完整真实 Skill 文件 `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-good-question/SKILL.md`。
- 埃隆之书场景：本地 EPUB `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub` 中的完整章节 `OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-14.xhtml`，TOC 标题为“成功之道”。

## 边界

- 这是手工真实来源 demo，不是自动生成器输出。
- 这是 reader-facing 契约样张，不是 product ready。
- DB demo 的 reader 主体是净化正文，audit 保留来源路径、frontmatter 和状态说明。
- 埃隆之书 demo 只做 repo 内版权安全预览：确认完整章节边界，展示章节结构、极短摘录和讲解位置；不在仓库报告中保存完整版权正文。完整正文应留在本地私有 EPUB 或私有阅读包中。
- source refs、location refs、claim trace、machine/human 状态、降级/拒绝说明只放 audit。

## 文件

- `dbs-good-question/reader/01_dbs-good-question_阅读页.md`
- `dbs-good-question/audit/source-notes.md`
- `elon-success/reader/01_成功之道_阅读页.md`
- `elon-success/audit/source-notes.md`
