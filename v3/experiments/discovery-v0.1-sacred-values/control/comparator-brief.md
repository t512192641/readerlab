# 独立比较者任务

你是本轮唯一的独立比较者。你可以读取共同任务规则、完整章节原文、普通基线和 S1—S5 的全部 raw 输出；不得读取仓库其他路径、历史候选、历史 Expert、产品判词或网页，不得搜索，不得调用 Expert/Writer。

只读取：

- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/control/seed-task.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/docs/expert-teaching-v0.1.2-migration-inputs/A/source.xhtml`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/raw/baseline.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/raw/seat-1.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/raw/seat-2.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/raw/seat-3.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/raw/seat-4.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/raw/seat-5.md`

## 工作

为每条原始种子生成机制指纹：解释对象、关键变量、因果动作、新生成结果。按机制而不是理论名称聚类；名称不同但机制四元组基本相同必须合并。对每个机制簇与代表种子执行：

1. 去标签测试：删除理论名/书名/人物名后，是否只剩原文换句话说？
2. 原文盲推测试：只读原章的正常读者是否大概率能自行推出核心结论？
3. 新结果测试：是否有具体新分类、诊断、预测、反事实、判断条件或方法？
4. 第三案例潜力：离开本章后是否有望分析不同问题？

将簇分为：

- A 核心借脑候选：外部知识可独立成套、分析语法不同、承诺具体新结果、与原文连接自然且承重。
- B 高质量原文深化：外部知识真实/有价值，但核心仍沿作者轨道，生成剩余不足。
- C 淘汰：标签、类比、牵强连接、无法成套、无具体新结果或重复且无增量。

输出必须写入：

`/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/04-clusters-and-screen.md`

文件至少包含：

- 基线与各席位原始种子总数；
- 机制簇清单、成员 Seed ID、代表席位、机制指纹；
- 每簇 A/B/C 判断和四项轻筛理由；
- 基线与五席的机制多样性比较；
- 固定专家、轮换单领域、轮换跨领域、图书互引的实际贡献；
- “扣除作者贡献”是否减少原文续写的观察；
- 尚不能由本阶段证明的事项。

不要搜索、核验事实或润色 raw 输出。不要修改其他文件。
