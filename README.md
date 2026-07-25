# ReaderLab

这是 ReaderLab 的全新、隔离项目起点。

它只带入五类已经整理并可直接阅读的资产：

1. [产品决议](PRODUCT-DECISIONS.md)
2. [工程经验](ENGINEERING-LESSONS.md)
3. [金标、反例与边缘案例](GOLD-STANDARDS.md)
4. [流水线开发蓝图](blueprints/PIPELINE-MAP.md)
5. [图书与 Skills 借鉴方法](references/BOOK-AND-SKILLS-METHODS.md)

`examples/` 保存可直接阅读的固定案例；`audit/manifest.json` 是早期 clean-seed 文件集合的
历史快照，只能回放当时边界，不证明当前仓库文件没有变化。

本项目不包含任何旧 ReaderLab 代码、Prompt、合同、runtime、run、Memory 或旧项目路径，也不允许 Agent 自动回查旧项目。缺失信息必须标为 `unknown`，等待产品负责人在新项目内决定。

## 当前状态入口

仓库当前任务、run、业务证据基线、dirty 快照、停止点、唯一产品前进行动、禁止动作与
`unknown` 只由 [`CURRENT-STATE.md`](CURRENT-STATE.md) 拥有。长期产品责任仍由
[`PRODUCT-DECISIONS.md`](PRODUCT-DECISIONS.md) 拥有，两条产品线的派生架构仍由
[`blueprints/PIPELINE-MAP.md`](blueprints/PIPELINE-MAP.md) 呈现。

以下内容是截至 2026-07-22 的历史交接快照，只用于追溯当时事实，已经失去“当前状态”和
执行授权效力；其中的 T2.12 等“下一步”措辞不得用于派发新任务。

历史快照正文（原样保留）：

截至 2026-07-22，本 `README.md` 是仓库项目状态入口；长期产品责任由 `PRODUCT-DECISIONS.md` 拥有，两条产品线的派生架构由 `blueprints/PIPELINE-MAP.md` 呈现。T2.5 已完成且整包不通过；`taskcards/T2.6.md` 状态为 `COMPLETE`，`taskcards/T2.7.md` 状态为 `COMPLETE`，两轮产品均未接受；`taskcards/T2.8.md` 状态为 `COMPLETE`，三个知识核心卡获准进入单样张打磨；`taskcards/T2.9.md` 状态为 `COMPLETE`，active version 为 `v03`，伯格内容与 T2.10 原文融合 v02 已先后获得产品接受。`taskcards/T2.11.md` 状态为 `COMPLETE`，宗派化与诺斯意识形态—执行成本机制 v01 已分别获得产品接受并准许进入原文融合；`taskcards/T2.12.md` 已冻结为下一轮唯一图书线切片。历史 T2.2 恢复架构继续保留，但不构成当前执行许可。

### 1. 2026-07-22 历史阶段与 gate（已失效）

- 当时阶段：T2.12 两个非伯格知识对象的原文融合迁移实验已冻结，尚未开始生产。
- 当时 gate：`taskcards/T2.12.md` 状态为 `READY`，active version 为 `v01`。当时只允许在同一完整章节中融合两份已接受讲义并记录最小分段墙钟，停在产品负责人阅读判词；不得进入未见章节、自动化、Judge、M2 或 T3。
- C0 输入 HEAD：`fc7b6c01daaee8a7814e26e8d3b8ff8c1fb198d7`；T2.2 失败证据 commit 仍为 `909531c42336a0fd6f22a39f7aaba7b3c9c1e3dd`。
- 当前控制状态：`A1_ARCHITECTURE_RELEASED`。C0 读取隔离修复已 `implemented / integrated / verified`，但尚未经过总控基于真实提交的复核，不能认定 `A2_CONTROL_PLANE_INTEGRATED`；恢复卡数量：`0`。
- T2.2 资格仍为 `FAIL`，但它不是当前正例生产的前置 gate；M2 receipt 仍不存在，模型 Judge 不得上岗。

### 2. 已经通过的内容

- T0.1—T0.3 开发基座已完成：目录、任务卡、术语表、轻量运行工具与确定性验证边界已经建立。
- T1.1—T1.9 合同与种子透镜 v1 已完成，M1 审核 `PASS`；冻结身份以 `contracts/M1-freeze-receipt.md` 为准。
- T2.1 缩句差分诊断方法卡已 `implemented` 并通过确定性验证，但尚未经过 M2 冻结。
- T2.3 失败案例诊断与种子透镜 v2 已 `implemented` 并通过确定性验证；v2 仍为 `draft`，尚未取得资格。
- T2.2 的冻结盲包、评分键、judge brief、answers、哈希链、评分和失败留痕已按任务卡落库；本轮重新核对 14 项顺序、状态头、关键哈希、payload／源片段逐字节一致性和 `FAIL` 汇总均为 `PASS`。这只证明仓库内考试证据自洽，不代表裁判通过，也不补足仓库中缺失的 raw runtime 日志。
- v3 architecture/review/quality audit 的固定身份分别通过 `PASS`／`CONFIRMED_PASS`，A1 `A1_ARCHITECTURE_RELEASED` 已成立。
- C0 读取隔离修复保留已通过的 M2 receipt 26 字段精确 schema、R01 product-request blocker 合法关闭、`BLOCKED` selector 拒绝与完整 M2 hash 链；进一步把 21 卡 read whitelist 从控制面 hash 依赖中解耦，按单一发布责任机械锁定逐卡业务闭集。R05 业务输入由旧 55 路径收窄为 28 blobs、byte manifest、admission 与 R04 byte review 共 31 路径；加四份治理文件与自身任务卡后，完整 read-path 由旧 60 路径收窄为 36。census/gap、selector/resolution、authorization、adapter、历史证据、架构正文和 prior blocker 均已移除。R09/R14/R19 每个 fresh judge 也被单独锁定为五文件白名单。

### 3. 尚未通过的内容

- T2.2 裁判资格未通过，裁判不得上岗。
- M2 未通过且没有 receipt。
- C0 读取隔离修复尚未经过总控基于真实提交的复核，A2 尚未成立；不得启动独立后置审查或注册 21 张恢复卡。
- 21 张恢复卡尚未注册，R01—R21 均未执行；v2 active attempt/baseline/postflight 均不存在。
- T2.1、未来 v2 active baseline/postflight、T2.3 v2 与 T1.8 尚未组成 M2 冻结集。
- 图书线生产 runtime 未 `integrated`，未知材料能力和整体 semantic／product 质量未验证。
- T2.9 伯格 v03 内容与 T2.10 原文融合 v02 均已获得产品接受；另外两个知识对象的平行样张与自动化仍未验证。
- `taskcards/T2.10.md` 状态为 `COMPLETE`；该历史状态只证明伯格融合样张已收口，不为 T2.11 或后续阶段授予权限。
- T2.11 两份内容已分别获得产品接受；T2.12 只继承冻结讲义与判词，不继承来源研究或 T2.11 专属自动化。

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
- v3 恢复架构已通过独立前置审查和质量复核，并已编译进控制面；这只建立可验证的恢复合同，不是恢复执行授权。
- 对照诊断是否足以区分输入、对象边界、操作程序与 judge 能力的影响，尚未经过真实运行证明。
- 当前没有获准执行的复考版本、模型／调用授权、新通过线或产品材料补充。

### 6. 恢复架构状态

- `diagnostics/T2.2-recovery-architecture-v1.md` 已由架构会话新增并提交于 `dc2e21d67ba8b5eb7c7f48048c670901d089d7a8`，SHA-256 为 `b67e28b0f12d46c4c90b2c9064e975eb3ffe296ba16c043f89ceebed57e97648`。
- 该文件状态为 `draft / long-term`：已 `implemented`，尚未 `integrated`；独立前置审查结论为 `FAIL`，产品 `accepted` 为 `unknown`。
- 架构草案提出 Route D：永久保留 v1 `FAIL` 证据与冻结 T1.8，以版本化适配合同、v2 原子夹具、对称来源上下文、明确处置映射、最小对照诊断和独立复考形成恢复链；不得把该建议当作现行任务授权。
- 草案确认三个执行前 blocker：3 个 positive 缺少完整来源锚点；多对象样张缺少原子候选级产品判词边界；模型、调用次数与预算未获授权。产品负责人现在不需要补材料或作决定，须先完成技术前置审查。
- 前置审查报告 `diagnostics/T2.2-recovery-architecture-v1-preflight-review.md` 已提交于 `575b317dec64a78054ab4bbb0e6b04b1a0f2cbb3`，SHA-256 为 `84d70747f0db290cd16d2d60d2745aa5d4c5f51a35f1cc27870c64235cd55acc`，结论为 `FAIL`。
- 审查确认五项必须由技术架构修正的问题：
  1. 四张建议任务卡会被现行验证器拒绝，16 个鲜会话对照也缺少合法路线入口；
  2. v2 活动 baseline 尚未接入 M2，成功证据无法进入正式 gate；
  3. adapter、brief、独立审查和对照结果的写 owner、冻结点与 hash 时序不闭合；
  4. 当前最小对照不能支持其声称的单变量、16 次可复算因果结论；
  5. 产品材料与原子判词缺口尚未通过先行技术 census 变成逐对象、可回答的最小请求。
- 审查确认这些都是技术架构问题，当前不需要产品负责人补材料、补判词或授权模型调用；因此没有当前产品 blocker。
- `diagnostics/T2.2-recovery-architecture-v2.md` 已提交于 `037f33b0893208a232efa4aaeb23866885ec5fd0`，SHA-256 为 `1154110c3a3bff65e4dc2ceb8244e724f0da60924c4e32ba4afa413600a2043a`。
- v2 文件当前状态头为 `frozen / run-only`，正文声明只允许下一步进行独立 v2 前置审查。该状态头及正文均只是被审输入事实，不表示总控已经判断 v2 正确。
- v2 已 `implemented`；独立前置审查结论为 `FAIL`，尚未 `integrated`，恢复路线未 `verified`，产品 `accepted` 仍为 `unknown`。
- v2 独立前置审查报告 `diagnostics/T2.2-recovery-architecture-v2-preflight-review.md` 已提交于 `4bc9feca20f41e9c41158885cad41683f4d227b2`，SHA-256 为 `9d2c80e23e30018c4dc4283c56315ab2df2198344b98dda91cebae6755f92e13`。
- 审查结果为 P01—P20 中 18/20 `PASS`：F-02、F-04、F-05 已关闭；F-01、F-03 未关闭。DAG、M14、M2 active/history 接线与 v2 自身状态头均通过本轮审查。
- v2 独立前置审查当时确认的三个技术 blocker：
  1. P0：R03 没有冻结供 R05 逐字复制的完整 `SOURCE-CONTEXT` bytes，R05 又无权重读样张；
  2. P0：21 张卡必须在 R03 前静态原子注册，但 R06 白名单要求只列 R05 后才知道的实际 material slots；
  3. P1：未来 stateful artifacts 缺少逐路径 `scope: long-term|run-only` 决议，会把生命周期选择留给执行者或触发验证器失败。
- 这三个架构 blocker 已由 v3 关闭；当时及当前均没有产品 blocker，也不需要产品负责人补材料、补判词或授权模型调用。
- `diagnostics/T2.2-recovery-architecture-v3.md` 已提交于 `a67f011d112e1e06022867cb3577110816064bd9`，SHA-256 为 `38025c0b2ebb26171e7f6ad8bef69b97bfeb2d88597a78e67b3dcdc48110d1e1`。
- v3 状态头为 `frozen / run-only`，正文声明 supersede v2，成为唯一活动架构候选；v1、v2 与两轮失败审查继续作为历史证据。
- v3 已 `implemented`；独立前置审查报告给出 `PASS`，C0 已把其静态合同 `integrated` 到现行控制面。恢复路线尚未执行，产品 `accepted` 仍为 `unknown`。
- v3 独立前置审查报告 `diagnostics/T2.2-recovery-architecture-v3-preflight-review.md` 已提交于 `626562fa3fa6487200e953ca0b804a275ec3ef33`，SHA-256 为 `e5d450f019685fba6eed679e06ccedee10255591e9a4a65359ac6cfb918e06ec`。
- 报告完整记录三项 blocker `CLOSED`、V01—V32 `32/32 PASS`、不回退 `14/14 PASS`，共 446 行；身份、提交范围、hash、V 项编号完整性、`python3 validate.py` 和 diff check 均由本轮总控复核通过，没有发现截断、占位或条件式 `PASS`。
- 产品负责人报告该审查会话曾因模型调用问题中断。原会话过程仍无法由仓库证明，因此其“未调用模型”声明保持 `unknown`；该过程未知不再作为技术 `PASS` 的唯一依据。
- 独立质量复核报告 `diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md` 已提交于 `e74221b85a8c750827c534e14d6df4079cb85c06`，SHA-256 为 `a81ded57546981d40b7c95d0d206ca0b627008fe509c32dfff1fb09abb415342`，结论为 `CONFIRMED_PASS`。
- 质量复核重新执行三个 blocker、V01—V32、不回退、packet parser 反例及数字展开，确认 14 candidate、14 context、28 raw blobs、14 material slots、21 DAG nodes、3 composite tasks、11 direct reviews、105 stateful paths 与 M14 `C4/B4/E4/G2`。其 105 路径算法为 `1 preflight + 82 正常卡输出 + 21 blockers + 1 M2 receipt`。
- 质量复核发现三个 P2：原报告未写 105 路径展开算法、不回退 14 项计数口径不透明、原会话“未调用模型”不可审计。三者均不形成架构死路、权限冲突或 C0 blocker。
- 本轮总控接受 v3 架构级技术 `PASS`：三个 blocker 已关闭，F-02/F-04/F-05 与不回退项成立，A1「架构已释放」成立。
- C0 候选 commit `17b7feec50262e5447cd216a02e7f6dd83f4151f` 只修改 `README.md`、`blueprints/EXECUTION-ROADMAP.md`、`validate.py`、`taskcards/T3.6.md`、`taskcards/T4.1.md` 和 `audit/manifest.json`。当前 `python3 validate.py`、`python3 -m py_compile validate.py`、提交范围与 diff check 均通过，恢复卡为 0，M2 receipt 不存在。
- 总控按 v3 固定规格复核后判定首版 C0 候选未达到 A2，存在两个 P0 和一个 P1：
  1. P0：`selector-result: BLOCKED` 没有成为 M2 receipt 的硬拒绝条件，与 v3 §13.3“仍有 blocker 即禁止 M2”冲突；
  2. P0：M2 gate 没有重算完整 attempt/package/byte hash 链，只深验少量最终产物；中间 packet、key、manifest 或 review 被改动时仍可能错误放行；
  3. P1：任务卡注册投影只要求 R03 列出 14 个 material slots，未强制 v3 §7 要求的 R03、R04、R05、R06 四卡都静态列全。
- 首轮 C0 修复 commit `dd3f7c60cb6f5a350edd59dcbdb672603c70a9e0` 修改 `validate.py`、`README.md`、`blueprints/EXECUTION-ROADMAP.md` 和 `audit/manifest.json`。`python3 -B validate.py --self-test-recovery`、`python3 -B validate.py`、编译检查和 diff check 均通过；这证明实现自洽，不自动证明符合 v3。
- 总控的 Standards 轴为 `PASS`，仅发现一个非阻断 P2：恢复图以大量路径字符串、元组和正则分组集中在 `validate.py`，存在 Primitive Obsession、Data Clumps 与未来 Shotgun Surgery 风险。v3 Spec 轴为 `FAIL`，最高 P0：
  1. P0：v3 §13.2 声明 M2 receipt 的精确 key 集；验证器却把 architecture/review commit、review result、quality-audit 四字段及 v2 commit 等九个额外字段设为必填，自测正例也按该私有 schema 生成，导致符合 v3 的精确 receipt 被拒绝；
  2. P0：R03—R06 只检查任意位置的 `material-slot-policy` 标记行，不检查六节任务卡中的实际“允许读取清单”。独立反例在 R05 允许读取清单加入 `materials/T2.2-v2/*.md` 和“打开全部材料”后仍得到零错误，R05 的运行时零材料读取没有机械闭合；
  3. P1：M2 当前拒绝任何 recovery blocker；v3 §6.5、§11.2、§13.3 明确允许 R01 product-request blocker 在 R03 resolution 逐 request-id 关闭后永久留档。当前合法需产品答复路径会因此永久无法进入 M2，自测没有覆盖该必经历史 blocker。
- 二次修复 commit `cf8262587ce22453114954e7bd8546cdd1cb7a6d` 只修改 C0 六文件；`python3 -B validate.py --self-test-recovery`、`python3 -B validate.py`、编译检查和 diff check 均通过。总控独立确认 receipt 文档/实现均为 26 字段且集合相等，R05 material glob 注入被拒绝，R01 blocker 合法关闭与反例回归存在。
- Standards 轴为 `PASS`，仅保留静态图大量路径字符串和长分支造成的非阻断 P2 维护风险。v3 Spec 轴仍为 `FAIL`，最高 P0：v3 §8.8 明确规定 R05 copy-only 只能读取 R03 的 28 blobs、byte manifest/admission 并核验 R04 review；当前 `_expected_card_read_paths("T2.2-R05")` 却从完整 attempt dependency 生成 60 个允许路径，额外包含 census/gap/selector/resolution、authorization、adapter/review、v1/v2/v3 历史证据和先前 blocker。路线图又把该扩权写成现行合同，自测只证明 raw slot/glob 等注入失败，没有证明 R05 的冻结最小允许集合。
- 本次读取隔离修复不再从 `_recovery_chain_dependencies` 反推执行角色权限，而是建立 21 卡显式业务读取投影。R05 的 §8.8 业务闭集精确相等、31 项合法输入逐项缺失反例、census/gap/selector/resolution/authorization/adapter/历史 key/answers/baseline/prior blocker 逐项越权反例、14 slots 静态登记与运行时 `forbidden`、21 卡逐卡越权注入，以及 R09/R14/R19 每个 fresh judge 五文件闭集均通过确定性回归。
- 这只建立 C0 读取隔离修复的技术 `verified`，不替代总控复核或 A2 判定。当前仍为 A1，T2.2 资格仍为 `FAIL`，M2 receipt 不存在，21 张恢复卡为 0。
- C0 不授权恢复卡、材料、模型调用、M2 receipt 或恢复执行；它也不创建任何恢复产物或阶段 3 入口。

### 7. 必须保留的证据

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

恢复设计：

- `diagnostics/T2.2-recovery-architecture-v1.md`
- `diagnostics/T2.2-recovery-architecture-v1-preflight-review.md`
- `diagnostics/T2.2-recovery-architecture-v2.md`
- `diagnostics/T2.2-recovery-architecture-v2-preflight-review.md`
- `diagnostics/T2.2-recovery-architecture-v3.md`
- `diagnostics/T2.2-recovery-architecture-v3-preflight-review.md`
- `diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md`

### 8. 当前最后可信 commit

- 当前最后可信 T2.2 考试证据 commit：`909531c42336a0fd6f22a39f7aaba7b3c9c1e3dd`（忠实记录 T2.2 `FAIL`，不是资格通过）。
- 当前最后已通过 gate 的 commit：`dab61e73ef4b3cadfde2ae7d422c0023ed53a850`（M1）。
- 恢复架构草案 commit：`dc2e21d67ba8b5eb7c7f48048c670901d089d7a8`（只证明设计文件存在，不证明已集成、已验证或已接受）。
- 恢复架构前置审查 commit：`575b317dec64a78054ab4bbb0e6b04b1a0f2cbb3`（结论 `FAIL`，不授权执行）。
- 恢复架构 v2 commit：`037f33b0893208a232efa4aaeb23866885ec5fd0`（只证明 v2 文件存在和身份稳定，不证明审查通过）。
- 恢复架构 v2 独立前置审查 commit：`4bc9feca20f41e9c41158885cad41683f4d227b2`（结论 `FAIL`，不授权 C0 或执行）。
- 恢复架构 v3 commit：`a67f011d112e1e06022867cb3577110816064bd9`（只证明 v3 文件存在和身份稳定，不证明审查通过）。
- 恢复架构 v3 独立前置审查 commit：`626562fa3fa6487200e953ca0b804a275ec3ef33`（报告结论 `PASS`，已由质量复核确认并作为 C0 固定输入）。
- 恢复架构 v3 前置审查质量复核 commit：`e74221b85a8c750827c534e14d6df4079cb85c06`（`CONFIRMED_PASS`）。
- C0 控制面集成基准 commit：`fc7b6c01daaee8a7814e26e8d3b8ff8c1fb198d7`。
- C0 控制面候选 commit：`17b7feec50262e5447cd216a02e7f6dd83f4151f`（总控复核未通过，不授权 A2 或 21 卡注册）。
- 首轮 C0 修复 commit：`dd3f7c60cb6f5a350edd59dcbdb672603c70a9e0`（自身回归通过，但总控 v3 Spec 复核 `FAIL`，不授权 A2、后置审查或 21 卡注册）。
- C0 二次修复 commit：`cf8262587ce22453114954e7bd8546cdd1cb7a6d`（receipt 与 R01 blocker 部分通过总控复核，但 R05 read isolation 为 P0 `FAIL`）。
- 上一轮总控状态 commit：`4fe26a4106855bd0ae1a76f4584fb4c5c402b05b`。

### 9. 非交付工作树项

- 仓库根目录未跟踪的 `.DS_Store` 不属于项目交付，本次不处理。

### 10. 2026-07-22 历史下一步编排（已失效）

- 当时唯一切片是 T2.12：把宗派化与诺斯意识形态—执行成本机制两份已接受讲义放回同一完整原章节，验证真实锚点、连续阅读体验和激进时间预算，经过最小确定性检查后停在产品负责人阅读判词。
- 当时的 T2.12 只做同章融合迁移；不重做来源核验、不改讲义承重语义、不提炼共享 Meta Prompt，也不进入未见章节、Writer runtime、Assembler runtime、Judge、M2、T3 或自动化。
- 该编排已经失效，不构成当前下一步；现行状态只见 [`CURRENT-STATE.md`](CURRENT-STATE.md)。

### 11. 2026-07-22 历史读取顺序（已失效）

下列清单只保留当时交接证据，不能作为新会话的现行读取指令。新会话按 `AGENTS.md` 的读取
规则进入，并从 [`CURRENT-STATE.md`](CURRENT-STATE.md) 恢复当前状态。

1. `AGENTS.md`
2. `README.md`
3. `PRODUCT-DECISIONS.md`
4. `ENGINEERING-LESSONS.md`
5. `blueprints/EXECUTION-ROADMAP.md`
6. `validate.py`
7. `taskcards/T0.1.md`
8. `contracts/M1-freeze-receipt.md`
9. `contracts/T1.8-independent-acceptance.md`
10. `taskcards/T2.2.md`
11. `diagnostics/T2.2-blind-packet.md`
12. `diagnostics/T2.2-scoring-key.md`
13. `diagnostics/T2.2-judge-brief.md`
14. `diagnostics/T2.2-judge-answers.md`
15. `diagnostics/T2.2-judge-baseline.md`
16. `taskcards/T2.2-BLOCKER.md`
17. `diagnostics/T2.2-recovery-architecture-v1.md`
18. `diagnostics/T2.2-recovery-architecture-v1-preflight-review.md`
19. `diagnostics/T2.2-recovery-architecture-v2.md`
20. `taskcards/T3.6.md`
21. `taskcards/T4.1.md`
22. `diagnostics/T2.1-r01-r08.md`
23. `lenses/T2.3-seed-lenses-v2.md`
24. `diagnostics/T2.2-recovery-architecture-v2-preflight-review.md`
25. `diagnostics/T2.2-recovery-architecture-v3.md`
26. `diagnostics/T2.2-recovery-architecture-v3-preflight-review.md`
27. `diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md`
28. `taskcards/TEMPLATE.md`
29. `materials/.gitignore`
30. `audit/manifest.json`

本 C0 集成不继承透镜开发、诊断端或裁判端对 `GOLD-STANDARDS.md` 与 `examples/` 的读取授权；不得读取或依赖旧 ReaderLab 项目。

### 12. 硬停止条件

**在 T2.2 恢复并重新通过资格验证前，不得进入 M2。**

当前 active deterministic tests 入口是：

```bash
python3 -B tests/entry.py
```

`python3 -B validate.py` 只用于历史 clean-seed 回放。当前新增状态 owner、后续任务卡与历史
artifact 均不属于其早期清单，因此它预期报告历史差异，不作为 active gate。
