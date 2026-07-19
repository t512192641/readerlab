# ReaderLab

这是 ReaderLab 的全新、隔离项目起点。

它只带入五类已经整理并可直接阅读的资产：

1. [产品决议](PRODUCT-DECISIONS.md)
2. [工程经验](ENGINEERING-LESSONS.md)
3. [金标、反例与边缘案例](GOLD-STANDARDS.md)
4. [流水线开发蓝图](blueprints/PIPELINE-MAP.md)
5. [图书与 Skills 借鉴方法](references/BOOK-AND-SKILLS-METHODS.md)

`examples/` 保存可直接阅读的固定案例；`audit/manifest.json` 只负责证明这些文件没有被静默改动。

本项目不包含任何旧 ReaderLab 代码、Prompt、合同、runtime、run、Memory 或旧项目路径，也不允许 Agent 自动回查旧项目。缺失信息必须标为 `unknown`，等待产品负责人在新项目内决定。

## 当前项目状态（唯一交接入口）

截至 2026-07-19，本 `README.md` 是仓库唯一的项目状态与跨会话交接入口。项目已暂停继续开发；本节只记录已验证事实、当前阻塞和证据位置，不设计恢复方案。

### 1. 当前阶段与 gate

- 当前阶段：阶段 2「裁判先行校准」。
- 当前 gate：T2.2 裁判资格考试已执行但 `FAIL`，处于 M2 之前的硬阻塞。
- 本轮总控复核输入 HEAD：`378306fa804dba47fb3316932aaf8b3f839f585b`；该提交只更新上一轮状态快照与对应 manifest，T2.2 证据 HEAD 仍为 `909531c42336a0fd6f22a39f7aaba7b3c9c1e3dd`。
- M2 未建立；阶段 3 真实材料运行、生产 runtime 和产品验收均未开始。

### 2. 已经通过的内容

- T0.1—T0.3 开发基座已完成：目录、任务卡、术语表、轻量运行工具与确定性验证边界已经建立。
- T1.1—T1.9 合同与种子透镜 v1 已完成，M1 审核 `PASS`；冻结身份以 `contracts/M1-freeze-receipt.md` 为准。
- T2.1 缩句差分诊断方法卡已 `implemented` 并通过确定性验证，但尚未经过 M2 冻结。
- T2.3 失败案例诊断与种子透镜 v2 已 `implemented` 并通过确定性验证；v2 仍为 `draft`，尚未取得资格。
- T2.2 的冻结盲包、评分键、judge brief、answers、哈希链、评分和失败留痕已按任务卡落库；本轮重新核对 14 项顺序、状态头、关键哈希、payload／源片段逐字节一致性和 `FAIL` 汇总均为 `PASS`。这只证明仓库内考试证据自洽，不代表裁判通过，也不补足仓库中缺失的 raw runtime 日志。

### 3. 尚未通过的内容

- T2.2 裁判资格未通过，裁判不得上岗。
- M2 未通过且没有 receipt。
- T2.1、T2.2 baseline、T2.3 v2 与 T1.8 尚未组成 M2 冻结集。
- 图书线生产 runtime 未 `integrated`，未知材料能力和整体 semantic／product 质量未验证。
- 产品 `accepted` 尚未发生。

### 4. T2.2 当前失败结果

- 冻结 answers 记录的授权配置：`gpt-5.6-terra / high`。
- 冻结 answers 记录的调用粒度：`single fresh isolated judge turn / one 14-item batch`；既有执行记录称无追问、无第二次 judge 调用。
- 8 个 `negative`：要求 8/8 `拦截`，实际 0/8 `拦截`，全部被 `放行`。
- 3 个 `positive`：要求 3/3 `放行`，实际 0/3 `放行`，全部被判为 `边缘`。
- 3 个 `reference`：实际为 `边缘`、`放行`、`放行`，不参与硬门。
- 资格结论：`FAIL`。失败基线为 `diagnostics/T2.2-judge-baseline.md`，硬阻塞为 `taskcards/T2.2-BLOCKER.md`。

### 5. 已确认问题与仍属推测的问题

已确认：

- 14/14 源文件 hash、提取片段 hash 与 blind packet payload hash 已复算一致，源片段与 payload 逐字节相同。
- 既有执行记录确认 judge 按四文件白名单运行；仓库可独立复核 blind packet、brief 与 answers 没有 scoring key、源路径、类别标签或产品判词泄漏。仓库没有 raw runtime 日志，因此不能只靠仓库重放完整实时上下文。
- blind packet 的 14 个中性 ID 均没有 T1.8 要求的既有 `b2-item-id`、冻结生产产物可信身份／内容 hash 和固定 scope；多个 ID 实际合并了整页或多条 AI 陪读，未满足 T1.8“一对象对应一个既有冻结 B2 单元”的对象边界。
- 8/8 negative 带有正文上下文；3/3 positive 缺少同粒度、可追溯的完整原文锚点，输入证据不对称。
- judge 对 8 个 negative 系统性把原文明说关系的机制化措辞、换名或页内局部强片段判为实质增量；对 3 个 positive 的内容增量和原文关联均因证据不足判为 `unknown`。
- 冻结 T1.8 已排除复述、整理和换名，并保留删除测试；本次 judge brief 没有强制记录“最小承重主张与原文明说集合做差分”的操作过程。

仍属推测／`unknown`：

- judge 判断能力、对象合并、原文证据不对称分别造成多大比例的失败，当前没有独立对照。
- 14 项单批是否造成注意力稀释或同向偏差，当前没有证据。
- 后续是否需要修改 T1.8、judge brief、样张、对象粒度或其他合同，尚未决定。
- 当前没有获准或冻结的恢复方案、复考版本、模型变更或新通过线。

### 6. 必须保留的证据

输入：

- `contracts/M1-freeze-receipt.md`
- `contracts/T1.8-independent-acceptance.md`
- `taskcards/T2.2.md`
- `GOLD-STANDARDS.md`
- T2.2 任务卡列出的 14 个 `examples/book/` 源文件；其逐项源路径、定位与 hash 以 `diagnostics/T2.2-scoring-key.md` 为准。

输出与 blocker：

- `diagnostics/T2.2-blind-packet.md`
- `diagnostics/T2.2-scoring-key.md`
- `diagnostics/T2.2-judge-brief.md`
- `diagnostics/T2.2-judge-answers.md`
- `diagnostics/T2.2-judge-baseline.md`
- `taskcards/T2.2-BLOCKER.md`

关键 SHA-256：

| 对象 | SHA-256 |
|---|---|
| M1 receipt | `6dd5ce00a3a0c14e0c2dc8036e7543c113d885a986b6c393025d60e1e5432aa1` |
| T1.8 | `7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093` |
| blind packet | `606ff15528c3dd7150ff5dc74e9ac93976c39837e092a315fc7dee0036f85399` |
| scoring key | `14988f3b908e8e31874e9b7196efe0bbda5d9116f92052844bb43e4a786b26e3` |
| judge brief | `cbca2fbfa19e7778994ad54d9a5bdbc46077b3ec8506cc562a40257b62a36b6b` |
| judge answers | `e2508f584ccb9d696485cbc8e140e69ef32d9a27a29122495ba3590f47d876f7` |
| judge baseline | `830f0758439ee72d549efe27296a444ccb9769c92c1298399dd9b5bebce0d4af` |
| T2.2 blocker | `84c7a0dede0797c5667228398cc4be1b8a945d8a871dab7058737778bba1684b` |

执行日志索引：

- T2.2 主控准备／评分任务：`019f7746-0021-76f2-a7f9-dee14a2453dd`
- 唯一隔离 judge 任务：`019f7748-ea2c-75a3-99e0-716fe763edca`
- 仓库内没有独立 raw runtime 日志；冻结 answers、baseline、scoring key、blocker 与 Git 提交共同构成必须保留的执行证据。

上述冻结文件、hash 链、任务记录和 blocker 不得删除、覆盖、改写或当作通过证据。

### 7. 当前最后可信 commit

- 当前最后可信项目证据 commit：`909531c42336a0fd6f22a39f7aaba7b3c9c1e3dd`（忠实记录 T2.2 `FAIL`，不是资格通过；其后的本次交接提交只更新状态快照与对应 manifest）。
- 当前最后已通过 gate 的 commit：`dab61e73ef4b3cadfde2ae7d422c0023ed53a850`（M1）。
- 上一轮状态快照 commit：`378306fa804dba47fb3316932aaf8b3f839f585b`。

### 8. 当前未提交修改

- 当前未提交修改只有仓库根目录未跟踪的 `.DS_Store`；它不属于项目交付，本次不处理。

### 9. 当前唯一下一步编排

- 原路线现在不可继续：T2.2 资格为 `FAIL`，且 `diagnostics/M2-gate-receipt.md` 不存在；不得进入 M2 或阶段 3。
- 紧接着只启动一个**架构角色**，会话名称为「ReaderLab M2｜T2.2 版本化恢复架构」。
- 该会话使用 Local 环境，只设计可验证、版本化的恢复／复考路线；不得执行 judge、改写既有冻结证据、创建 M2 receipt、写生产代码或进入阶段 3。
- 为保证仓库仍是唯一记忆，该架构会话只允许新增 `diagnostics/T2.2-recovery-architecture-v1.md`，并在验证通过后形成一个独立本地 commit；不得修改其他文件。
- 架构产物必须分开已确认事实、因果假设与 `unknown`，给出后续前置审查所需的完整技术边界，但不得替产品负责人作产品决策。
- 架构 commit 完成后，产品负责人只需把 commit SHA、验证结果和是否出现产品 blocker 回报总控；总控重新读取仓库后，才决定是否启动前置审查。

### 10. 下一会话读取顺序

1. `AGENTS.md`
2. `README.md`
3. `PRODUCT-DECISIONS.md`
4. `ENGINEERING-LESSONS.md`
5. `GOLD-STANDARDS.md`
6. `blueprints/EXECUTION-ROADMAP.md`
7. `contracts/M1-freeze-receipt.md`
8. `contracts/T1.8-independent-acceptance.md`
9. `taskcards/T2.2.md`
10. `diagnostics/T2.2-blind-packet.md`
11. `diagnostics/T2.2-scoring-key.md`
12. `diagnostics/T2.2-judge-brief.md`
13. `diagnostics/T2.2-judge-answers.md`
14. `diagnostics/T2.2-judge-baseline.md`
15. `taskcards/T2.2-BLOCKER.md`

只有需要核对阶段 2 其他已完成草案时，再读取 `diagnostics/T2.1-r01-r08.md`、`diagnostics/T2.3-seed-lens-diagnostic.md` 与 `lenses/T2.3-seed-lenses-v2.md`。不得读取或依赖旧 ReaderLab 项目。

### 11. 硬停止条件

**在 T2.2 恢复并重新通过资格验证前，不得进入 M2。**

运行以下命令可验证项目边界：

```bash
python3 validate.py
```
