# ReaderLab Next Session Prompt

```text
/goal 继续 ReaderLab。当前目标不是继续扩写样张，也不是把仿型 Skill 拼在一起，而是按“短板驱动能力学习”补 ReaderLab 的第一短板：结构化提炼。

启动：
从 `/Users/tianqiang/Documents/读书伴侣` 开始。先读最小真相层：
1. `AGENTS.md`
2. `docs/current-task.md`
3. `docs/dev-state.md`
4. `docs/progress.md`
5. 需要决策背景时读 `docs/decisions.md`，重点 D-034 到 D-037
6. 需要运行历史时读 `docs/agent-run-ledger.md` 顶部最新记录

调度方式：
- 主 Agent 负责主持工作、拆分任务、调度子 Agent、回收结果、审查证据、更新进度板和最终交付给用户。
- 具体研究、诊断、样张产出、对比评估和对抗审查都由子 Agent 执行。
- 子 Agent 的产物必须先交给主 Agent；主 Agent 对照目标、边界、文件和验证结果审查后，才能交给用户。
- 子 Agent PASS 不等于任务完成；主 Agent 必须给出最终判断。

当前判断：
- ReaderLab 的根目标仍是复杂材料陪读阅读包。
- v0/v1/fullbook/fragment/dbs 都只是 repo 内或 LifeAtlas 试产样张，不是 product ready，不是生成器能力证明。
- 旧路线“参考项目真实吸收 -> 样张反测”容易让人误以为列了仿型、写了 matrix、产了样张就算进步。这个口径已收窄。
- 新路线是：先找 ReaderLab 短板，再找该能力环节最强的仿型，学习解题逻辑，小范围重考，验证后再进入生产链。
- 当前第一短板是结构化提炼：全书地图、章节地图、重点/亮点提炼背后是同一套能力。

本轮唯一目标：
完成“结构化提炼最小闭环”的可执行样张和评估，不做全产品重写。

必须做：
1. 诊断旧输出：
   - `docs/reports/readerlab-fullbook-demo-v0`
   - `docs/reports/readerlab-elon-full-product-v1`
   - `docs/reports/readerlab-elon-fragment-capability-eval-v0`
   对照全书地图、章节/部件地图、亮点提炼三个粒度，找出共同失败原因。
2. 建立结构化提炼仿型能力矩阵：
   - 列：定性、筛选、排序、组织、边界、表达。
   - 行：仓颉、李继刚式深读、source-grounded / NotebookLM 类、ReaderLab 现有能力；乔木和 book-to-skill 只在确实相关时作为补充，不默认拼入。
   - 每格标明：立即学习、替代方案、未来储备、不吸收。
3. 引入 Meta Skill 做横向评估裁判：
   - 至少派一个 Meta Skill 评估 worker，读取并应用：
     - `/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/skill-engineering-method.md`
     - `/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/output-eval-method.md`
     - 必要时读取 `skill-ir-method.md`
   - 它的任务不是生成阅读内容，而是评估 ReaderLab 与各仿型在结构化提炼环节的能力差异。
   - 报告必须覆盖：能力边界、参考扫描是否过宽、是否只奖励字段存在、output risk、应采用的 gate、下一步最高价值改进。
   - Meta Skill 评估报告只是一个裁判视角；主 Agent 仍要结合 ReaderLab 自己的产品目标和用户判断做最终取舍。
4. 抽出一条结构化提炼生产链：
   - 输入：材料范围和来源。
   - 过程：材料定性 -> 主问题 -> 候选池 -> 通过/降级/拒绝 -> 机制传导 -> 结构表达 -> 来源/边界。
   - 输出：同一套逻辑生成全书主线、一个章节/部件地图、3-5 个亮点提炼。
5. 用《埃隆之书》做小范围重考：
   - 不写 LifeAtlas 正式区。
   - 不声称全书产品完成。
   - 必须能说明为什么这些亮点被选中，为什么其他内容降级或拒绝。
6. 对比旧输出：
   - 是否减少目录复述。
   - 是否更清楚地说明书补了什么缺口。
   - 是否能解释结构如何传导。
   - 是否能说明选点理由和不升格理由。
   - 是否保留来源范围和人工待复核边界。
7. 更新 `docs/progress.md`：
   - 本轮新增多少点。
   - 是否有旧判断被扣分。
   - 哪些模块 close / working / blocked。

明确不做：
- 不把所有仿型的所有加分项拼进页面。
- 不继续扩写《埃隆之书》总纲。
- 不把片段卡、v1 主稿、DBS capability v1 说成生成器能力。
- 不新增依赖。
- 不整体重构 `scripts/readerlab.py`。
- 不写 LifeAtlas `300/600/800`。
- 不安装或启用新 Skill。

验收标准：
- 能回答 ReaderLab 当前哪门课弱，以及为什么先补结构化提炼。
- 能指出每个被学习仿型在结构化提炼中到底强在哪里。
- 能产出一条可复用生产链，而不是字段拼装。
- 有 Meta Skill 横向评估报告，并明确哪些建议采用、哪些只做储备、哪些不吸收。
- 小范围重考比旧输出更能说明主问题、机制传导、选点和边界。
- `docs/progress.md` 已更新，且没有把样张 PASS 当产品 ready。
```
