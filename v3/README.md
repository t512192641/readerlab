# ReaderLab V3

ReaderLab V3 的目标是把一次阅读变成可复利的认知资产：材料输入可以是图书、长文、Skill 包或工程材料；输出不只是一份陪读页，而是一套能继续被下次阅读调用的工具箱、读法、问题和资产卡。

## 三层架构

### 资产层

资产层跨会话存在，住在 LifeAtlas。它只保留五个 Markdown 登记簿：工具箱清单、阅读履历、开放问题、读法卡、资产卡。会话开工先读它们，用来把新材料接到用户已有知识上；会话收工只提交沉淀候选，未经用户确认不写回正式登记簿。

### 会话层

会话层是一套纯 prompt Skill 包，不写生成用 Python。图书线使用批注席引擎：先识别原文活点，再招募有资格的读者身份产出候选批注，由裁判淘汰，最后蒸馏心法与冰山页。Skill 线使用逆向工程引擎：从机制走查、取舍解读、方法论指认、设计评审到复现配方和资产卡，让读者能看懂它为什么这样设计、照着怎么复现。

### 界面层

界面层保持 Obsidian + Markdown。读者可见页面必须是中文、正文优先、可批注。批注后的就地回复循环放到 v1.1，V3 v1 先完成标准、Skill 包、双试点和资产回写验证。

## 阶段索引

1. Phase 0：准备独立 worktree 与 `v3/` 骨架。
2. Phase 1：先写图书批注与 Skill 工艺两份评分标准，并用金标样张校准。
3. Phase 2：建立五个资产层登记簿 schema。
4. Phase 3：编写纯 prompt 会话层 Skill 包与模板。
5. Phase 4：用埃隆书 `022_丰饶时代` 和 `gstack/browse` 做完整成品阅读试点；`gstack/spec` 只保留为 Phase 1 校准与资产卡冷启动基线。
6. Phase 5：经用户确认后回写资产层，并形成 v1 可声称 / 不可声称清单。

## 当前进度（2026-07-09）

- Phase 0：完成。独立 worktree、分支和 `v3/` 骨架已建立。
- Phase 1：关闭。图书线收敛为“页边批注死刑制 + 章末延伸讲堂”；H03 讲堂体金标已入库。
- Phase 2：repo-local 骨架完成。五登记簿 schema、种子和查重协议已存在；尚未写入 LifeAtlas 正式区。
- Phase 3：repo-local 骨架完成。Skill 入口、双引擎、裁判、模板和范例库已存在；这不等于完整成品已经验证。
- Phase 4：预检修正完成，完整试点尚未运行。下一步是分别交付 `022_丰饶时代` 图书成品页和 `gstack/browse` 完整 Skill 包，并按 `v3/standards/phase4-pilot-definition.md` 验收，单线最多三轮。
- Phase 5：未开始。只有两个试点经用户确认后，才允许回写资产层并验证跨材料串联。
- Phase 6：暂缓到 v1.1，当前不做 Obsidian 批注回复循环。

当前完成的是“方法、协议和验收闸门”，尚未证明完整 ReaderLab 成品稳定成立。后续进度讨论以本节、`v3/standards/calibration-log.md` 和 `v3/standards/phase4-pilot-definition.md` 为准。

## 当前边界

- 只在本 worktree 的 `v3/` 下新增 V3 材料。
- 不修改主工作区 dirty 文件。
- 不修改 gstack 源仓库。
- 不写生成用 Python。
- 未经用户确认不写 LifeAtlas。
- 不触碰旧线 PR #23。
