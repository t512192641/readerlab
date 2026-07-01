# AGENTS.md

## 项目目的

ReaderLab 把复杂材料转成中文可读、可批注、可讨论、可沉淀的 LifeAtlas 双轨陪读包。材料可以是电子书、长文、Markdown 文档、课程资料、访谈稿、代码文档、Skill 包或混合型资料。

当前默认前提是：Obsidian + Markdown + Codex + 现有批注插件。gstack 是第一组复杂压力样本，但项目目标不是 gstack 专项，也不是 Skill 专项。所有规则都应优先服务“复杂材料陪读 / 吸收”：先提供可信的一手正文或净化正文，再提供全局讲解、高阶讲解、设计资产提炼、误读防护、批注讨论入口和候选沉淀；读者在 Obsidian 正文附近批注后，Codex 能读取批注和上下文并就地回复。

正式开发前的产品骨架是：

```text
一手正文轨 + AI 陪读轨 + audit/contracts/eval 事实层
```

AI 方法层采用 E-R-D-D：Evidence -> Route -> Deepen -> Decide。旧结构化提炼和 Combo-B 相关任务只作为局部能力证据，不再作为项目主线。

## 启动顺序

每个新会话先读两个入口文件：

1. `AGENTS.md`
2. `docs/current-task.md`

`docs/current-task.md` 是当前执行事实的唯一入口。它会列出本轮真正需要继续读取的队列、方法和验收文件；不要在启动阶段自行扩大到旧报告、旧 prompt 或长历史。

按需扩展读取：

- 需要产品边界时读 `docs/product-spec.md`。
- 需要包结构时读 `docs/readerlab-package-spec.md`。
- 需要稳定路径和工具状态时读 `docs/dev-state.md`。
- 需要耐久决策时读 `docs/decisions.md`。
- 需要运行历史或验证证据时只读 `docs/agent-run-ledger.md` 顶部最新两条。
- 需要外部研究或 baseline 线索时读 `docs/research-log.md`。

不要从旧聊天、旧 prompt、旧报告或 Obsidian 当前画面倒推项目事实。当前事实以仓库文件、LifeAtlas 输出和验证命令为准。

## 关键入口

- 生成脚本：`scripts/readerlab.py`
- 单元测试：`tests/test_readerlab.py`
- 项目说明：`README.md`
- 产品规格：`docs/product-spec.md`
- 包结构规格：`docs/readerlab-package-spec.md`
- AI 阅读方法：`docs/ai-reading-method.md`
- 高阶讲解方法：`docs/high-order-explanation-method.md`
- 技术负责人 / 设计资产提炼方法：`docs/technical-cofounder-method.md`
- 验收 gate：`docs/eval-gates.md`
- 当前 repo-local Skill：`.agents/skills/readerlab/SKILL.md`
- 最小验证 fixtures：`tests/fixtures/readerlab/`
- 当前埃隆书整书解读：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629/10_中文精读/03_ReaderLab整书章节解读/`
- gstack 原始 Skills 学习材料：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack`

## Memory Map

- `docs/current-task.md`：唯一当前执行事实源；如果它和其他状态、prompt、进度文件冲突，以它为准。
- `docs/dev-state.md`：稳定路径、工具状态和验证命令；不记录当前任务进度，不作为启动必读。
- `docs/product-spec.md`：产品目标、边界和阶段路线。
- `docs/readerlab-package-spec.md`：目标阅读包结构。
- `docs/ai-reading-method.md`：E-R-D-D 方法。
- `docs/high-order-explanation-method.md`：认知升级讲解的内部生产协议。
- `docs/contracts/high-order-explanation-v1.md`：高阶讲解 audit contract。
- `docs/technical-cofounder-method.md`：技术材料的设计原子分析。
- `docs/eval-gates.md`：功能、阅读质量、深读质量、技术洞察和失败条件。
- `docs/decisions.md`：耐久决策，只记录之后会继续约束实现的判断。
- `docs/agent-run-ledger.md`：压缩后的运行历史、改动摘要、验证命令和结果。
- `docs/research-log.md`：外部研究和可复用候选结论；只在产生新的可复用研究结论时更新。

## 项目边界

- 不新建第二个 LifeAtlas `270_电子书与书籍资料` 目录。
- 不移动、软链或改写 gstack 源仓库。
- 不新增依赖，除非用户明确批准。
- 不自动写入 LifeAtlas 的 `300/600/800` 正式沉淀区。
- 不自己发明批注系统；优先适配 Obsidian 现有批注插件或 Markdown 原生批注格式。
- 不让 AI 替代人的第一次阅读判断；AI 预处理只负责降低阅读门槛，Codex 回复围绕人的批注和附近上下文。
- 未完成 Skill 不生成占位阅读页，只在主控清单和 manifest 中保留目标路径。
- 不把当前样本包的特殊结构写成 ReaderLab 的通用规则；gstack 只用于暴露和验证复杂材料阅读化问题。
- 面向读者的正文必须服务理解主线；完整原文、执行外壳、代码块、脚本细节和审计证据可以放入附录或包级机制页，不能反复污染每个模块的主阅读页。
- AI 生成的全局讲解、高阶讲解、设计资产提炼和误读防护是阅读辅助；它们不能替代一手主体内容。
- 书籍和长文默认原样保留正文；除非用户明确要求整理原文，否则只做空格、空行、断行等轻量清理，不能压缩、改写或用导读替代正文。
- Skill 包和工程材料默认生成净化正文：剥离命令行、重复执行协议和机器细节，但必须保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点；被剥离内容进入附录、技术解析或 audit。
- 关联模板、脚本、参考资料必须单独展示，不能冒充材料主体。
- Markdown 是展示层；source registry、location map、contracts、eval 和人工状态才是事实层。

## 验证命令

```bash
python3 tests/test_readerlab.py
python3 tests/test_readerlab_trace_validator.py
python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures
```

当前阶段不删除或移动 gstack 原始 Skills 源仓库；LifeAtlas 270 下旧 gstack ReaderLab 生成解读包已清理。
