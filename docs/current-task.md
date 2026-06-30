# Current Task

## 当前唯一执行切片

本轮已完成 ReaderLab **结构化提炼同题多路线对照 v0**：仓颉-only、李继刚-only、ReaderLab-current、Combo-A、Combo-B 均按同一任务处理《埃隆之书》，并由独立评估 worker 做横评。

主 Agent 最终判断：**Combo-B 暂时胜出，进入下一轮候选主链验证，但不是生产通过，也不是生成器能力**。

Combo-B 的候选顺序是：

1. source-grounded 前置：先限定原文能说什么、不能说什么。
2. 仓颉候选筛选：再判断候选通过、降级或拒绝。
3. 李继刚式受控表达：最后把已通过或降级的判断组织成机制传导和读者可理解结构。

## 已完成

1. `docs/reports/readerlab-structured-extraction-min-loop-v0/`：结构化提炼最小手工闭环。
2. `docs/reports/readerlab-structured-extraction-bakeoff-v0/`：同题多路线对照和组合增益审查。
3. D-038 / D-039 已将用户护栏固化：不能默认抽取仿型局部环节可靠，组合增益必须用同题对照证明。
4. `docs/progress.md` 已更新：当前总进度 48/100，结构化提炼 12/18。

## 下一轮唯一执行切片

下一轮做 **Combo-B 轻量模板和迁移前验证**，不是继续扩写《埃隆之书》。

必须做：

1. 把 Combo-B 抽成轻量验证模板：材料范围 -> 来源断言 -> 候选筛选 -> 受控机制表达 -> 拒绝/降级清单 -> 读者页风险检查。
2. 用 5-8 个候选跑完整 gate，不扩写整书内容。
3. 做 blind A/B 或等价盲评包，对比 Li-only、Cangjie-only、ReaderLab-current 和 Combo-B；不能只看字段是否齐全。
4. 选第二类材料做小范围迁移测试，证明 Combo-B 不是《埃隆之书》特化解法。
5. 明确哪些步骤可以沉入工具，哪些必须保留 Agent 判断。

## 当前能力模块

ReaderLab 生产能力暂按 4 门主课管理：

1. **结构化提炼**：全书地图、章节地图、重点/亮点提炼。当前第一短板，已完成手工闭环和同题对照，仍未机制化。
2. **片段深读与误读防护**：局部机制、反例、边界、批注触发，已有片段样张但未形成稳定生产链。
3. **能力化判断**：判断哪些内容能转成方法/流程/Skill，哪些只能保留为案例或边界。
4. **来源审计与产品组织**：source/location、人工状态、读者页/审计页分离、Obsidian 可读包装。

## 明确不做

- 不把 Combo-B 说成 product ready。
- 不把同题对照 PASS 说成生成器能力。
- 不继续扩写《埃隆之书》总纲或阅读正文。
- 不把所有仿型的所有优点拼进页面。
- 不新增依赖，不改 `scripts/readerlab.py`，不写 LifeAtlas `300/600/800`，不安装或启用新 Skill。

## 必须更新

每轮大迭代后必须更新：

- `docs/progress.md`：总进度、模块状态、本轮新增/扣减点、close/working/blocker。
- `docs/current-task.md`：唯一下一步切片。
- `docs/dev-state.md`：当前事实和边界，不放流水账。
- `docs/agent-run-ledger.md`：运行记录和验证证据。
