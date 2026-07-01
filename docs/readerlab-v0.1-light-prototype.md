# ReaderLab v0.1 轻量原型

更新时间：2026-06-29  
定位：本地 Markdown 优先的 Obsidian 陪读工具  
第一使用场景：Agent Skills / Markdown 材料陪读
状态：从 Downloads 原始构想归档到项目内；本文保留 v0.1 轻量原型边界，不是当前任务源。当前执行事实以 `docs/current-task.md` 为唯一入口；稳定路径和工具状态按需看 `docs/dev-state.md`。

---

## 1. 一句话定义

ReaderLab v0.1 不是知识图谱、不是外置大脑、不是复杂阅读系统。

它只做一件事：

> 把一个 Skills 仓库或 Markdown 材料整理成一本可在 Obsidian 里阅读、翻译、批注，并可由 Codex 读取批注后回复的 Markdown 书。

---

## 2. v0.1 要解决的问题

现在的问题是：

- Skills 仓库里文件很多，逐个打开成本高。
- 很多材料是英文，直接读阻力大。
- 只让 AI 总结全文会丢掉人的主动思考。
- 读书式学习需要“看到哪里标到哪里”，不能把批注统一堆到文末。
- 需要让 Codex 能读取人的真实标注痕迹，并围绕上下文回复。

v0.1 的目标是降低第一次阅读和二次讨论成本。

---

## 3. v0.1 的产品边界

### 做

- 有一个书架入口。
- 能添加一个材料。
- 能把材料拆成一本可读的 Markdown 书。
- 英文材料能处理成中文。
- 能生成简短导读和目录。
- 能让用户在 Obsidian 正文里就地批注。
- Codex 能读取批注、上下文和高亮，并生成回复。
- Codex 的回复尽量写回批注附近，保持原文、批注、回复之间的上下文关系。

### 不做

- 不做网页 UI。
- 不做数据库。
- 不做知识图谱。
- 不做飞书集成。
- 不做 Readwise / 微信读书同步。
- 不做 PDF / EPUB 完整导入。
- 不自动修改正式 Skills。
- 不自动升格进 Life Atlas 正式知识库。
- 不做跨材料旁征博引。
- 不做完整读书系统。
- 不做万能材料解析器。

说明：这里的“不做跨材料旁征博引”只约束 v0.1 的自动导入和初次生成流程。2026-06-29 后续讨论确认，跨材料新知、导师式旁批、行业类比和思维模型连接是 ReaderLab 的长期价值方向之一，但不应塞进当前生成器的默认页面里。它更适合后续作为独立 Skill、读后提问触发能力，或基于 LifeAtlas/思维模型库/联网搜索的单独模块来设计。

---

## 4. 推荐存放位置

由于 LifeAtlas 已有顶层结构，v0.1 不新增顶层目录。

推荐放在：

```txt
LifeAtlas/
  900_AI工作台/
    ReaderLab/
```

理由：

- 这是一个当前工作台，而不是正式知识库。
- 读过的材料、翻译、批注和讨论先保存在实验区。
- 未来确认长期有用的内容，再手动升格到 `800_Skills与流程`、`300_方法论与卡片` 或其他正式区。

---

## 5. v0.1 文件结构

```txt
ReaderLab/
  00_书架.md

  _research/
    000_资料来源与设计备忘.md

  books/
    gstack/
      00_导读.md
      01_目录.md
      chapters/
        001_spec.md
        002_review.md
        003_office-hours.md
```

说明：

- `00_书架.md`：所有已导入材料的入口。
- `_research/`：保存参考资料、后续功能、设计线索，不影响 v0.1 使用。
- `books/`：每个材料被整理成一本“书”。
- `chapters/`：每个章节是一份可阅读 Markdown。

---

## 6. 使用流程

### 第一步：添加材料

输入一个本地路径或仓库路径，例如：

```txt
把这个路径下的材料加入 ReaderLab：
/Users/tianqiang/Downloads/gstack

材料类型：skills
阅读目标：学习它怎么写 Skills
如果是英文，请翻译成中文。
```

v0.1 优先支持：

1. Skills 仓库 / 文件夹。
2. Markdown / TXT 文档集合。

暂不支持：

- PDF
- EPUB
- 网页抓取
- 飞书文档
- Readwise / 微信读书

---

### 第二步：生成书架记录

`00_书架.md` 示例：

```md
# ReaderLab 书架

## 正在读

| 材料 | 类型 | 状态 | 入口 | 最近阅读 |
|---|---|---|---|---|
| gstack | Skills 仓库 | 已拆书 | [[books/gstack/00_导读]] | spec |
| qiaomu-read-helper | Skills 仓库 | 待阅读 | [[books/qiaomu-read-helper/00_导读]] | - |

## 添加记录

- 2026-06-28：导入 gstack
- 2026-06-28：导入 qiaomu-read-helper
```

书架只承担入口作用，不做复杂统计。

---

### 第三步：生成材料导读

`books/gstack/00_导读.md` 示例：

```md
# gstack 导读

## 这是什么

这是一套 Agent Skills 工作流。

## 我为什么读

学习它如何组织 Skills、定义触发条件、写约束、拆角色、处理安全边界。

## 建议先读

1. [[chapters/001_spec]]
2. [[chapters/002_review]]
3. [[chapters/003_office-hours]]

## 阅读提醒

先看中文正文。需要核对原意时，再看原文对照。
```

导读要短，不要写成长篇分析。

---

### 第四步：生成目录

`books/gstack/01_目录.md` 示例：

```md
# gstack 目录

| 章节 | 原文件 | 中文名 | 说明 |
|---|---|---|---|
| [[chapters/001_spec]] | spec/SKILL.md | 规格生成 | 把模糊需求变成执行规格 |
| [[chapters/002_review]] | review/SKILL.md | 审查 | 检查代码或方案风险 |
| [[chapters/003_office-hours]] | office-hours/SKILL.md | 办公时间 | 执行前澄清问题 |
```

目录的目标是把文件列表变成“可阅读的书籍目录”。

---

## 7. 章节文件结构

章节文件不要设置单独“批注区”。

读书批注应当发生在正文附近。

`books/gstack/chapters/001_spec.md` 示例：

```md
---
type: readerlab-chapter
source: gstack
source_type: skills
source_file: spec/SKILL.md
language: zh-CN
status: reading
---

# spec：规格生成

## 简短导读

这个 Skill 用来把模糊需求整理成可执行规格。阅读时重点看它如何定义目标、边界和验收标准。

---

## 中文正文

这里放中文译文。

用户直接在正文附近用 Obsidian 插件或 Markdown 原生语法做批注。

例如：

==好 Skill 不只是告诉模型做什么，还要告诉模型什么时候应该停。==

%% 这个是不是和我们之前的 ctk-goal 很像？ %%

或者使用插件生成的 inline comment。

---

## 原文对照

这里放英文原文，方便必要时核对。
```

---

## 8. 批注策略

v0.1 不自己发明批注系统。

正确策略是：

> ReaderLab 生成适合阅读的 Markdown；Obsidian 插件负责批注；Codex 适配插件的真实存储格式。

优先测试顺序：

1. Reading Comments：适合 Markdown 正文 inline comments。
2. Comments：适合侧边栏和 inline callouts 形式的评论。
3. Markdown 原生语法：作为稳定兜底，例如 `==高亮==`、`%%评论%%`、inline footnote。
4. PDF++ / Annotator：后续处理 PDF / EPUB 时再测试，不进入 v0.1。

关键原则：

- 批注必须靠近原文。
- 批注必须能被 Codex 从 Markdown 文件里读到。
- 回复也尽量靠近原文或批注，不要统一放在文末。
- 具体格式以最终选定插件的真实 Markdown 存储格式为准。

---

## 9. Codex 读取批注的最小流程

用户读完某一章后，可以对 Codex 说：

```txt
请读取：
LifeAtlas/900_AI工作台/ReaderLab/books/gstack/chapters/001_spec.md

任务：
1. 只处理正文中的批注、高亮、评论、inline comment。
2. 每条批注都要结合它附近的上下文回复。
3. 不要重写全文。
4. 不要做长篇总结。
5. 把回复写回对应批注附近。
6. 如果插件格式不支持就地回复，就用最接近原文位置的 Markdown callout 追加回复。
```

示例回复格式：

```md
==好 Skill 不只是告诉模型做什么，还要告诉模型什么时候应该停。==

%% 这个是不是和我们之前的 ctk-goal 很像？ %%

> [!answer] Codex 回复
> 是，有重叠。ctk-goal 更偏目标控制，spec 更偏任务规格化。小任务可以只用 ctk-goal，中大型任务再加 spec。
```

---

## 10. Codex 预处理材料的范围

v0.1 允许 Codex 做轻量预处理：

- 生成简短导读。
- 生成中文译文。
- 生成目录。
- 用 Markdown callout 标出少量阅读提示。
- 保留原文对照。
- 保留正文附近批注和回复链路。

不允许 Codex 做：

- 大段泛泛总结。
- 自动提炼长期原则。
- 自动加入正式知识库。
- 自动改写原仓库内容。
- 自动生成新 Skill。
- 自动生成复杂图谱。
- 在初次导入时自动进行跨材料旁征博引或导师式高阶解读。

预处理的目标是“让材料更容易读”，不是替代阅读。

---

## 11. v0.1 验收标准

v0.1 只要满足以下 5 条，就算成功：

1. 能把 gstack 加入书架。
2. 能生成 gstack 的导读和目录。
3. 能点开一个 Skill 章节，看中文正文和原文对照。
4. 能在 Obsidian 里对正文就地批注。
5. Codex 能读取批注并在对应位置回复。

---

## 12. 第一批测试材料

建议第一批只测 2 个材料：

1. gstack  
   用来测试“复杂 Skills 仓库拆书”。

2. qiaomu-read-helper  
   用来测试“读书/陪读方法类 Skill 的中文理解和批注”。

不要一开始导入太多材料。

---

## 13. v0.1 成功后的下一步

v0.1 成功后，再考虑：

- 确认一个 Obsidian 批注插件作为主方案。
- 固化 Codex 读取批注的规则。
- 加一个简单的“讨论记录追加”机制。
- 再决定是否加入模式索引、跨材料比较、Life Atlas 升格等功能。

当前不进入 PRD。
