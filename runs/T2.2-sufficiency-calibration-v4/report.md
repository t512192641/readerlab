# T2.2 v4 负向先行双角色校准报告

## 结论

- 执行状态：`COMPLETE`
- 校准成绩：`FAIL`
- positive：`0/2` 命中
- hard negative：`5/5` 命中
- non-pass borderline：`3/3` 命中
- reference：`CASE-B9Q5J=block`、`CASE-L3E7W=block`，只记录

两个 fresh 功能隔离角色按固定顺序各调用一次，全部 12 题的 objection、final judgment 与机械复算一致。失败原因是规则过度拦截：两个必须放行对象 `CASE-K7M2Q`、`CASE-V8H3L` 都被判为 `block`。本次没有修改冻结输入、补跑角色或创建第三角色，也没有生成 v5 Prompt。

同题校准不证明未知材料泛化。本次 `FAIL` 不能作为未知材料裁判资格、M2、T3 或真实图书生产许可。

## Git 与路径闭集

- branch：`codex/readerlab-book-t2-2-negative-first-calibration-v4`
- starting commit：`8df2c7966c2006acab956fb5b9a9aa52d0a68985`
- starting parent：`e8bd46c166531aa291dd83e89450a1b300f3cb4b`
- v3 standard parent：`0891ecf3366573c2142fb3ce36120dcd0614ebf6`
- main merge-base：`c9988591b97ed472d2341f0747316d4ea650c9b7`
- commit message：`T2.2-v4: run negative-first judge calibration`
- commit：由提交后的 `git rev-parse HEAD` 作为 Git 外部证据解析，避免报告自含所属 commit hash 的循环引用
- 未 push

changed paths 恰为：

1. `taskcards/T2.2.md`
2. `runs/T2.2-sufficiency-calibration-v4/run-manifest.json`
3. `runs/T2.2-sufficiency-calibration-v4/packet.md`
4. `runs/T2.2-sufficiency-calibration-v4/product-standard-excerpt.md`
5. `runs/T2.2-sufficiency-calibration-v4/v4-calibration-contract.md`
6. `runs/T2.2-sufficiency-calibration-v4/skeptical-reader-brief.md`
7. `runs/T2.2-sufficiency-calibration-v4/skeptical-reader-input-manifest.json`
8. `runs/T2.2-sufficiency-calibration-v4/objection-sheet.json`
9. `runs/T2.2-sufficiency-calibration-v4/final-judge-brief.md`
10. `runs/T2.2-sufficiency-calibration-v4/final-judge-input-manifest.json`
11. `runs/T2.2-sufficiency-calibration-v4/final-judgment.json`
12. `runs/T2.2-sufficiency-calibration-v4/scoring-key.json`
13. `runs/T2.2-sufficiency-calibration-v4/verify.py`
14. `runs/T2.2-sufficiency-calibration-v4/receipt.json`
15. `runs/T2.2-sufficiency-calibration-v4/report.md`

## 同字节输入与冻结哈希

`cmp`、固定 SHA-256 与 v4 verifier 共同证明：

- v3/v4 packet 字节完全相同：`e09ce22554cfc693b358348ab85eca794023a9b6df9e6f6e5b339c31668869d0`
- v3/v4 product excerpt 字节完全相同：`0e199ad969a4e2e6ae2916d638a38ade45c891c94f0d1c5c47f90427b1b3fb27`
- T1.8：`7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093`
- architecture report：`f5d2be8285285860057d9c9b69bf4f723749dd98ef68ba2e4a7e90a1d197ec16`

本次关键产物：

| 产物 | SHA-256 |
| --- | --- |
| `v4-calibration-contract.md` | `9c3437f6cac789ab5f9305a5c4f7844acc9725a4d2a63fffc62b165c5d50cf3f` |
| `skeptical-reader-brief.md` | `d2bb9a5138ddf90c57b8adb8370fd3e99b23e6ca4b2ffec5de41a881352e300a` |
| `skeptical-reader-input-manifest.json` | `303a4f3463dfa08bac2690f65ef1b2bd106c78a456979f054965cdc61ad66e3c` |
| `objection-sheet.json` | `9396542948f682ffa31c9a784ddaba76fe20b2b8a3eee203b92c48c1d53889b0` |
| `final-judge-brief.md` | `3354416dcec2ba4f7efca1667bff7d39e48d308d8201dfc4b19305b75883311b` |
| `final-judge-input-manifest.json` | `6a035be302be2edaa840dfaa0f85dabd673d48d0b92f15f1f261e04bc02240ea` |
| `final-judgment.json` | `6631998651e400f5571624a98399417189096e71264750a83f9715f8d1459eea` |
| `scoring-key.json` | `246ebbedcc50bb3e7e15bd3ea8abf68463af050e303acfd6428dc64c4a475ba9` |
| `run-manifest.json` | `cafdaae05913b075e1652a94165a0dced16aa0facae8cd8989bd59fd8336e8ef` |
| `verify.py` | `85016e3dd89e0805ddf1e6f607e3eaaa3397fc31c7006a74d0da17c971d886fc` |
| `receipt.json` | `12e1a7aeedcd1adf2dcdaeb1f48d9c2730248c911f6f9c120d62542ced9b7d87` |

## 两个 fresh 角色与隔离

### skeptical reader

- Agent ID：`/root/t2_2_v4_skeptical_reader`
- model：`gpt-5.6-terra`
- reasoning：`high`
- `fork_turns="none"`
- 调用次数：`1`
- 单次对象数：`12`
- 完成时间：`2026-07-20T16:01:05Z`（冻结输出文件 creation evidence）
- 唯一读取闭集：`AGENTS.md`、T1.8、v4 packet、v4 product excerpt、v4 contract、skeptical brief
- 唯一写入：v4 `objection-sheet.json`

### final judge

- Agent ID：`/root/t2_2_v4_final_judge`
- model：`gpt-5.6-terra`
- reasoning：`high`
- `fork_turns="none"`
- 调用次数：`1`
- 单次对象数：`12`
- 完成时间：`2026-07-20T16:10:37Z`（冻结输出文件 creation evidence）
- 唯一读取闭集：`AGENTS.md`、T1.8、v4 packet、v4 product excerpt、v4 contract、final brief、冻结 objection sheet
- 唯一写入：v4 `final-judgment.json`

两个角色总调用次数恰为 `2`。final judge 没有读取 skeptical reader 对话，只读取冻结 objection sheet。这里建立的是功能性输入隔离，不声称构成 OS／容器安全边界。

两个角色在 JSON 内自报的 `completed_at_utc` 均为 `2026-07-20T00:00:00Z`；这些原始字段已随输出冻结，没有事后修改。时序验证不信任该自报值，而使用当前原始 Worktree 的文件 creation evidence：skeptical manifest `1784562932` < objection `1784563265` < final manifest `1784563350` < final judgment `1784563837` < scoring key `1784563939`。

## 逐题 objection、处置与聚合一致性

| ID | strongest objection | final | verifier 复算 |
| --- | --- | --- | --- |
| `CASE-K7M2Q` | 候选把“真正的自动驾驶”改写成需要乘员接手的前提，角色认为该前提不在原文 | `block` | `block` |
| `CASE-C2F6P` | 将原文已明说的激励、惩罚、薪酬与风险回报重组为组织设计，没有额外承重认识 | `block` | `block` |
| `CASE-J9W4D` | 指标不等同真实安全性的提醒被判为正常读者可直接想到的小步 | `block` | `block` |
| `CASE-B9Q5J` | 为自由主义补入具体叙事并推出历史方向判断，承重内容不在原文 | `block` | `block` |
| `CASE-M5A8S` | 臭鼬工厂外部案例承担机制，却未说明为何能证明原文比喻 | `block` | `block` |
| `CASE-V8H3L` | 需求池化依赖总体需求稳定，但角色认为 candidate 未说明稳定性成立条件 | `block` | `block` |
| `CASE-Q3L7X` | 声称原文强调“迅速且完整”，但给定原文没有该句，外部细节承担核心解释 | `block` | `block` |
| `CASE-H6N2B` | 从运营隧道搭建逐级验证链，但给定原文未说明运营表现 | `block` | `block` |
| `CASE-L3E7W` | 海军核动力体系例子替代招聘判断解释，并把品性改写为规则下可靠运行 | `block` | `block` |
| `CASE-T8C5R` | 简单故事协调行动并排除事实的承重关系未在 candidate 中展开 | `block` | `block` |
| `CASE-D4V9K` | 并列多个外部权威，但没有逐一闭合它们与劳动力瓶颈论证的关系 | `block` | `block` |
| `CASE-P7G3M` | 用食物案例推出所有商品服务与贫困结论，但未说明案例如何承载更宽结论 | `block` | `block` |

每题的 `final_disposition`、`aggregation_trace.derived_disposition`、hard veto、minor limitation 与 verifier 复算一致，没有用碰巧命中 scoring key 代替规则一致性。

## 机械成绩

| ID | 类别 | 允许处置 | 实际处置 | 命中 |
| --- | --- | --- | --- | --- |
| `CASE-K7M2Q` | positive | `allow` | `block` | 否 |
| `CASE-C2F6P` | hard negative | `block` | `block` | 是 |
| `CASE-J9W4D` | hard negative | `block` | `block` | 是 |
| `CASE-B9Q5J` | reference | 只记录 | `block` | 不适用 |
| `CASE-M5A8S` | non-pass borderline | `borderline` 或 `block` | `block` | 是 |
| `CASE-V8H3L` | positive | `allow` | `block` | 否 |
| `CASE-Q3L7X` | hard negative | `block` | `block` | 是 |
| `CASE-H6N2B` | hard negative | `block` | `block` | 是 |
| `CASE-L3E7W` | reference | 只记录 | `block` | 不适用 |
| `CASE-T8C5R` | hard negative | `block` | `block` | 是 |
| `CASE-D4V9K` | non-pass borderline | `borderline` 或 `block` | `block` | 是 |
| `CASE-P7G3M` | non-pass borderline | `borderline` 或 `block` | `block` | 是 |

三类硬门没有全部满足，所以 calibration 为 `FAIL`。scoring key 在 final judgment 冻结后才首次创建并绑定其 SHA-256。

## 验证与禁止范围

- v4 verifier：`PASS`
- root `python3 -B validate.py`：`PASS`
- `git diff --check`：`PASS`
- path check：`PASS`
- Worktree 提交后干净：`PASS`
- 未运行 v2/v3 历史 verifier
- 未使用 archive、复制品或新 checkout 冒充历史原始现场
- owner、T1.8、examples、v2/v3 run、其他 taskcard、root validator：未修改
- T2.2-R01—R21：未注册、未读取正文
- `materials/`、其他 run、其他 Worktree、Skills 线、旧 ReaderLab、真实生产材料：未读取
- 新依赖、联网、M2 receipt、T3、push：均未发生

## 技术状态与接受边界

- implemented：taskcard 与规定的 14 个 v4 run 文件存在
- integrated：packet/excerpt、合同、两个 brief、两个 manifest、objection、final、后置 key、机械 verifier、receipt 与 report 形成一条真实证据链
- verified：v4 verifier、根验证器、diff/path 检查与提交后 clean check 全部通过
- accepted：产品负责人的既有判词只用于后置计分；本次校准不是新的产品判词，也没有新的产品接受

remaining risk：同题校准不证明未知材料泛化。由于本次为 `FAIL`，后续边界只能是由产品负责人提供仍失败边界的最小 pass/non-pass 对照对取证，再决定是否采用确定性预门加模型判断；本次不直接生成 v5 Prompt。
