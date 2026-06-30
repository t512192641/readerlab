# ReaderLab 阶段复盘

## 阶段结论

ReaderLab 已经从人工样本页，推进到真实 `SKILL.md` 的分块精读闭环：

- `gstack-openclaw-ceo-review`：74 个 block，真实分块产物 completed。
- `benchmark-models`：146 个 block，长 Skill 压力测试 completed。
- `benchmark`：155 个 block，8 个 part，多子 Agent 小块拆分 completed。

当前结论不是“自动翻译已经完全可靠”，而是：

1. block manifest、source_hash、状态机和 validator 可以防止结构性漏块。
2. 小块拆分能降低长文本一次性输出时的漏译和摘要化风险。
3. 仅靠结构指标不够，必须叠加质量门和人工抽查。

## 真正解决了什么

- 未完成 Skill 不再生成占位页，减少 Obsidian 中的误读。
- Skill 正文和 ReaderLab 解读分层：正文只翻译 `SKILL.md`，导读、关联材料、重点旁批各自承担解释职责。
- 关联材料改为 inventory-first，避免 hooks、脚本、模板等机制被藏起来。
- 公共术语表前置，避免读者先读正文再补术语。
- 分块产物 schema 和质量门落地，能够发现缺块、hash mismatch、空译文、模板残留和明显英文原句残留。

## 关键决策

- D-001：Skill 正文只翻译 `SKILL.md`。
- D-002 / D-002a：关联材料单独展示，并且必须 inventory-first。
- D-009：Agent 正文译文不得摘要化。
- D-010：分块精读由 ReaderLab 掌控状态。
- D-011：分块精读必须记录时间和可得消耗。
- D-012：稳定性测试应批量覆盖不同长度和类型。

## 踩过的坑

### 1. 结构通过不等于阅读质量通过

现象：`benchmark-models` 首轮产物 block/hash 覆盖看似完整，但 94 个 block 带有“中文译文：”模板残留，并有大段英文原句残留。

根本原因：大模型在长任务中可能优先满足显性的结构要求，把“每块有输出”当成完成，而不是保证每块都被自然、完整地翻译。

防重检查点：

- validator 必须检查模板残留和英文自然语言残留。
- 主线程验收不能只看 `completed`，还要抽查正文是否可读。
- 子 Agent prompt 必须明确：不要摘要，不要原文贴回，不要用模板标签冒充译文。

### 2. 长文本会诱发摘要化和省略

现象：旧 `readerlab.skill-reading.v1` 产物曾把 `benchmark-models` 压缩成摘要式解读，不能达到 completed。

根本原因：没有外部切块协议时，Agent 会为了控制输出长度和认知负荷，把“完整翻译”退化成“概括说明”。

防重检查点：

- 3 万字符以上不要交给一个 Agent 一次完成。
- ReaderLab 负责切块、分派、合并和覆盖校验；Agent 只翻译有限 block。
- 每个 part 的输入/输出都要有 block id 和 source_hash。

### 3. Validator 也可能误判

现象：`benchmark` 首次临时 validate 时，155/155 block 覆盖完整，但 `heading_coverage_incomplete` 报错。

根本原因：标题计数把 fenced code block 中的 Bash 注释 `# ...` 误当成 Markdown 标题。

防重检查点：

- validator 规则必须理解 Markdown 结构，不能只用行级正则。
- 遇到“覆盖失败”时先定位是产物问题还是验证器误判，不要为了过验证伪造内容。
- 修 validator 时要补测试。

### 4. 机制材料容易被正文掩盖

现象：早期页面只翻译正文，hooks、脚本、模板等实际执行机制没有充分展示。

根本原因：Skill 的功能并不只存在于 `SKILL.md`；很多行为由 frontmatter、hooks、bin 脚本、模板和迁移脚本共同决定。

防重检查点：

- 关联材料必须 inventory-first。
- 正文翻译和机制讲解必须分区。
- 有 hooks 时必须展示 matcher、command 和解析到的机制文件。

## 给未来 Codex 的经验

- 不要把“JSON 结构正确”理解成“任务完成”。
- 不要把“validator 绿灯”理解成“阅读质量可靠”；validator 只能覆盖已定义的失败模式。
- 对长文本任务，要先降低单个 Agent 的工作量，再做后验质量门。
- 质量门不是为了替代人工判断，而是为了把明显坏产物挡在 completed 之外。
- 当用户质疑“你是不是藏了东西”时，通常说明产物层级设计有问题：应回到源材料结构，检查是否有模板、hooks、脚本、外部配置没有展示。

## 可升维到全局错题本的候选

以下是候选，不自动写入 `~/.codex/global-knowledge/common-mistakes.md`。根据 MEM Clean 规则，只有用户批准后才能升维。

### 候选 G-001：结构指标通过不等于内容质量通过

- 域：Agent 流程 / 状态 / 记忆
- 现象：结构化产物字段齐全、block 覆盖完整，但内容可能是摘要、模板残留或英文原句。
- 根本原因：大模型倾向优化显性验收信号，尤其在长任务中可能牺牲未被明确检测的质量维度。
- 正确做法：结构门 + 内容质量门 + 人工抽查共同验收；不要只看 schema 或 completed。
- 防重检查点：看到结构化输出通过时，抽查 3 类内容：开头、中段、末尾；检查是否有模板残留、原文残留、摘要化。
- 来源：ReaderLab / 2026-06-28 / `benchmark-models` 首轮分块产物。

### 候选 G-002：长文本任务必须外部切块，不要依赖 Agent 自觉循环

- 域：Agent 流程 / 状态 / 记忆
- 现象：要求 Agent 完整处理长文时，容易输出摘要式结果或漏段。
- 根本原因：上下文压力和输出长度压力会让模型自动压缩任务。
- 正确做法：由外部工作流生成 block manifest，按小块分派，合并后做覆盖校验。
- 防重检查点：超过中等长度的文档任务，先问“切块、覆盖清单、合并校验在哪里？”
- 来源：ReaderLab / 2026-06-28 / `benchmark-models` 与 `benchmark`。

### 候选 G-003：验证器误判时不要让产物迎合错误指标

- 域：Agent 流程 / 状态 / 记忆
- 现象：产物真实覆盖完整，但 validator 把代码块注释误算成标题，导致失败。
- 根本原因：验证器规则过于表层，没有理解语法边界。
- 正确做法：先定位失败来源；如果是验证器错，修验证器并补测试，而不是改产物去迎合指标。
- 防重检查点：覆盖失败时抽样比较 source 和 output 的真实结构，确认失败属于产物还是 validator。
- 来源：ReaderLab / 2026-06-28 / `benchmark` 标题覆盖误判。

## 后续风险

- 英文残留质量门仍是启发式，不能识别所有坏译文。
- `---` 等分隔线目前仍可能被切成独立 paragraph，切块质量还可优化。
- 当前还没有正式 token 计量工具，只能先记录耗时；token 若不可得必须显式标记 unavailable。
- 下一轮 3-4 个 Skill 并行时，需要避免多个子 Agent 写同一个最终 JSON 文件。
