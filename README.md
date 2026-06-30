# ReaderLab

ReaderLab 是一个复杂材料吸收系统：把书籍、长文、课程资料、代码文档、Skill 包和混合型资料，转成中文可读、可批注、可讨论、可学习、可沉淀的 LifeAtlas 阅读包。

它不是摘要器、翻译器或完整图书生成器。ReaderLab 的目标是让读者更容易接触一手材料，同时获得有证据、有边界、有技术判断、有误读防护的 AI 陪读。

当前默认环境仍是：

```text
Obsidian + Markdown + Codex + 现有批注插件
```

## 产品形态

ReaderLab 的正式产品形态是 **正文优先的陪读包**：

```text
一手正文轨：书籍/长文原样正文，或 Skill/工程材料净化正文
AI 陪读轨：全局讲解、高阶讲解、误读防护、候选沉淀
设计资产轨：面向产品负责人的技术负责人解剖和可复用设计卡
```

AI 不替代人的第一次阅读。它负责降低阅读阻力、讲清结构、标出边界、解释技术和设计取舍、整理候选沉淀；读者仍在正文附近阅读、批注和判断。

高阶讲解不能只是章节摘要。它应在正文之后，用全局视角、跨学科思维模型、历史 / 商业 / 组织 / 工程经验和相似经历中的同构逻辑，给读者提供新的看法，同时区分原文依据、AI 解释和待验证判断。

## 目标包结构

目标 ReaderLab 包的逻辑结构如下。当前生成器尚未完整实现该结构；这是正式开发前的产品规格。

```text
ReaderLab Package/
  00_从这里开始.md
  01_全局讲解.md

  10_一手正文/
    001_章节或模块名.md

  20_AI陪读/
    catalog-map.md
    grounded-global-map.md
    local-deepread/
    capability-map.md
    design-asset-notes.md
    misread-guards.md

  30_批注与讨论/
    comments-index.md
    codex-replies.md

  40_候选沉淀/
    distillation-candidates.md
    skill-candidates.md

  audit/
    source-registry.json
    location-map.json
    contracts/
    rejected-downgraded.md
    eval.md
```

主阅读入口必须先让读者看到材料本身、整体结构和当前章节/模块在全文中的位置。书籍和长文默认原样保留正文；除非用户明确要求整理原文，否则只做空格、空行、断行等轻量清理。Skill 包和工程材料默认提供净化正文：剥离安装命令、重复模板和机器噪音，但保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点。审计、hash、命令行、脚本、来源路径、内部 source ids 和机器执行视图属于 `audit/` 或附录，不应污染第一次阅读。

## AI 阅读方法

ReaderLab 的 AI 层采用 E-R-D-D 链：

```text
Evidence  证据边界：来源、覆盖、位置、不能下结论的范围
Route     结构定位：材料类型、阅读单元、主干/外壳/证据分层和章节位置
Deepen    深读候选：主问题、机制链、原则、案例、反例、术语、技术设计、迁移洞察
Decide    升降级决策：Promote / Keep / Downgrade / Reject
```

任何高层判断必须能回到来源范围和位置引用。覆盖不足时只能输出目录地图、局部地图或结构诊断，不能冒充完整全局理解。

## 技术材料处理

对 Skill 包、代码文档、Agent 工作流和工程资料，ReaderLab 需要额外生成“技术负责人 / 设计资产提炼层”。它面向产品负责人，不解释术语，也不做技术吹捧，而是替读者看出其不容易感知的工程和系统设计，并回答：

- 这个设计解决什么问题。
- 它为什么放在这里。
- 它约束了什么行为。
- 它防止什么失败。
- 它带来什么代价和脆弱点。
- 它能否迁移，什么时候不要迁移。
- 它能沉淀成什么设计卡，未来什么场景可以复用。

完整方法见 [`docs/technical-cofounder-method.md`](docs/technical-cofounder-method.md)。

## 当前开发阶段

当前阶段是正式开发前准备，不是继续扩写旧样张，也不是开发完整自动生成器。

已完成准备：

- 产品定义重设为正文优先陪读包。
- AI 方法层重设为 E-R-D-D。
- 深读卡、设计资产提炼层、来源契约和验收 gate 已形成开发前规格。
- 旧结构化提炼任务降级为局部能力实验，不再作为项目主线。

contract / validator 的最小闭环已经完成第一版，但 2026-06-30 的人工反馈说明 reader-facing 原型仍会走样。最新处理不是继续返工旧《埃隆之书》reader 页，而是先把正文优先陪读包落成输出契约：书籍/长文原样正文，Skill/工程材料净化正文，高阶讲解服务正文阅读，技术负责人层输出设计资产卡，audit 与读者页分离。real-source demo v1 证明正文契约方向基本成立，但《埃隆之书》讲解仍像普通总结，未达到 ReaderLab 体验要求。下一步要先重做 AI 高阶讲解口径，再用小样章验证。

## 关键文档

- [`docs/product-spec.md`](docs/product-spec.md)：产品目标、边界和正式开发前状态。
- [`docs/readerlab-package-spec.md`](docs/readerlab-package-spec.md)：目标阅读包结构。
- [`docs/ai-reading-method.md`](docs/ai-reading-method.md)：E-R-D-D AI 阅读方法。
- [`docs/technical-cofounder-method.md`](docs/technical-cofounder-method.md)：技术材料分析方法。
- [`docs/eval-gates.md`](docs/eval-gates.md)：验收 gate 和失败条件。
- [`docs/current-task.md`](docs/current-task.md)：当前唯一执行切片。
- [`docs/dev-state.md`](docs/dev-state.md)：当前事实和开发边界。
- [`docs/progress.md`](docs/progress.md)：模块化进度板。

## 当前脚本能力

当前脚本主要支持 Skill 包导入、批注读取/回复和既有阅读包校验：

```bash
python3 scripts/readerlab.py import-skills \
  /path/to/skills-package \
  --dest "/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料" \
  --book-id gstack \
  --title gstack \
  --goal "学习 gstack 的使用方式与优秀 Skill 设计"

python3 scripts/readerlab.py comments-list path/to/reading-unit.md

python3 scripts/readerlab.py comments-reply path/to/reading-unit.md COMMENT_ID \
  --text "Codex 回复内容"

python3 scripts/readerlab.py validate /path/to/ReaderLab/material
python3 scripts/readerlab.py validate /path/to/ReaderLab/material --require-complete
```

这些脚本是工具层，不代表完整 ReaderLab 产品已经实现。

## 边界

- 不自建批注系统、网页 UI、数据库或知识图谱。
- 不让 AI 替代人的第一次阅读判断。
- 不把 reader-facing Markdown 当事实层；事实层应进入 JSON contracts / audit。
- 不把 validator 通过当人工阅读质量通过。
- 不自动写入 LifeAtlas `300/600/800` 正式沉淀区。
- 不把手工样张、旧 demo 或局部链路说成 product ready。
