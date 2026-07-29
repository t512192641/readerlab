# ReaderLab 当前真实运行审查地图

> 冻结日期：2026-07-29
> 审查分支：`review/readerlab-current-runtime-audit`
> 目的：只记录当前仓库、当前工作区和冻结运行证据能够证明的事实，供外部 Code Review 检查产品要求与实际实现是否一致。
> 边界：本文件不补写流程，不修订方法、Prompt、schema 或代码，不把技术通过写成产品接受。

## 1. 先看结论

当前不存在一条已经接入 ReaderLab 正式入口、可由仓库代码自动运行的完整图书生产
runtime。仓库中存在：

1. 已技术激活、但明确 `not integrated / not verified` 的长期内容流合同；
2. 负责 run 创建、候选排他 promotion、冻结和确定性检查的 `tools/run.py`；
3. 一个只允许虚构材料的功能性角色隔离 Skill，不能充当真实图书生产入口；
4. T2.35 的真实 Expert、知识卡、来源审核和 P2 证据；
5. 仓库外完成的 Writer、Fidelity 与候选装配 sidecar；
6. 仓库外完成的 Discovery V0／V1′ 18 次 Scout sidecar；
7. 2026-07-29 完成的 U01／U02／U03 D 直接路线与 ABC 路线人工多会话实验。

这些对象没有被一个共同 orchestrator 串成正式生产链。当前最接近成品的两组实际证据也不是
同一条运行：

- T2.35 → Writer sidecar：同一个 U03 原文身份上的神圣价值 Reader 候选；
- U01／U02／U03 pilot：另一次 D／ABC 对照，单次生成会话同时承担搜索 C、恢复 C、写近终稿和
  标注 M 深度。

## 2. 本次工作区分类

| 类别 | 文件或目录 | 本次处理 |
|---|---|---|
| 当前真实运行所需 | `AGENTS.md`、`PRODUCT-DECISIONS.md`、`GOLD-STANDARDS.md`、`ENGINEERING-LESSONS.md`、`blueprints/PIPELINE-MAP.md`、`contracts/BOOK-CONTENT-FLOW-v2.md`、`tools/run.py`、当前 Skill、当前任务卡与 run 控制证据 | 由审查分支现有树提供 |
| 本轮相关、此前未提交 | `AGENTS.md`、`PRODUCT-DECISIONS.md`、`docs/agent-run-ledger.md`、`docs/current-task.md`、`docs/decisions.md`、`docs/dev-state.md`、`docs/research-log.md` | 原样纳入；本轮未改写其语义 |
| 本次新增审查证据 | `audit/current-runtime-snapshot/`、本文件、`docs/current-runtime-review-brief.md` | 纳入独立审查 commit |
| 无关修改 | 没有发现可由现有证据确认的无关已跟踪修改 | 不擅自制造“无关”判断 |
| 前置诊断／已被后续 U pilot 取代的临时实验 | `b-from-a-validation-output*`、`b-guided*`、`b-to-c-search-validation-output*`、仓库根 `direct/` | 保留在本地，不纳入本次 commit |
| 重复或临时封装 | `.DS_Store`、`__pycache__/`、`*.pyc`、重复 ZIP | 不纳入本次 commit |

## 3. 当前入口

| 入口 | 实际能力 | 不能证明 |
|---|---|---|
| `python3 -B tests/entry.py` | 运行当前 36 项确定性测试 | 不是产品 gate，也不运行语义生产链 |
| `python3 -B tools/run.py new/promote/freeze/check` | 创建 run 骨架、校验候选、排他写正式路径、冻结 manifest、检查 hash 与顺序 | 不调用模型，不执行 Discovery、Expert、Writer、Judge 或 Fidelity |
| `.agents/skills/readerlab-functional-role-isolation/SKILL.md` | 对首个非空行是 `FICTIONAL TEST MATERIAL` 的短材料运行 producer → judge 隔离实验 | 禁止用于真实图书材料；不是 ReaderLab 图书生产 Skill |
| `taskcards/T2.35.md` | 人工调度 T2.35 Expert 与来源审核的实际运行卡 | 只到 P2，不含 Writer、Fidelity、装配或 P3 |
| `audit/current-runtime-snapshot/writer-assembly/tools/assemble-and-verify.mjs` | 对已存在的 Writer v2 做两项获准机械小修、锚定装配与可逆验证 | 不生成 Writer v2，不调用模型，不构成生产 B2 |
| `audit/current-runtime-snapshot/pilot-contract/.../00_README.md` 及 01—08 任务文件 | 通过四个隔离会话人工组织 U01—U03 D／ABC 对照 | 不由仓库代码调度；无原始模型调用日志 |

## 4. 产品合同要求的长期步骤

现行长期合同 `contracts/BOOK-CONTENT-FLOW-v2.md` 定义：

```text
冻结范围内完整 B1
→ 控制层建立章节论证地图并选择稳定认知背景
→ Expert 完整自由阅读，提交课程入口或沉默
→ 课程入口价值门
→ 同一 Expert 形成完整内部专家课
→ 知识审计、来源核验、语义锁
→ Writer 组织 Reader 单元
→ 独立 Fidelity
→ B2 确定性就近装配
```

合同自身第 13 节明确：

- `implemented`：合同文件存在；
- `integrated`：未接入真实 runtime；
- `verified`：未运行真实图书产品链；
- `accepted`：真实产物为 `unknown`。

合同还明确各交接物精确 schema、模型、思考强度、调用次数、来源工具、Writer 拆分算法、
Fidelity 实现与最终 Judge 都是 `unknown`。因此下面只能分别还原实际 sidecar，不能把合同图
当成已执行事实。

## 5. T2.35 → Writer sidecar：实际经过的步骤

### 5.1 T2.35 Expert 与来源审核

| 步骤 | 读取文件 | 模型／工具 | 最小输入 | 输出 |
|---|---|---|---|---|
| 机械提取 B1 | `materials/T2.4-IDEA-PILOT-01/source.epub`、`taskcards/T2.35.md` | 本地机械提取、`tools/run.py promote` | EPUB、member 路径、scope bytes/hash | `locked/chapter-scope.xhtml`、`locked/chapter-readable.md` |
| Expert 完整展开 | `locked/chapter-scope.xhtml`、任务卡内 D3 方向指令 | `gpt-5.6-sol / high`；Web Search + Web Fetch；10 查询／20 页面上限 | 完整章节、临时 Expert 身份、方向指令 | `raw/D3-expert.md`、`raw/knowledge-cards.md` |
| 独立来源审核／P2 | 完整章节、正式 Expert 课、`raw/knowledge-cards.md` | `gpt-5.6-terra / high`；Web Search + Web Fetch；12 查询／24 页面上限 | Expert 课、五张卡、章节 | `raw/review-outcomes.md`、锁定卡、`locked/D3-p2-gate.md` |
| 冻结 | run 内 raw/locked/final 与 `run.json` | `tools/run.py freeze/check` | 文件身份、hash、目录顺序 | `production-freeze.json`、`acceptance-freeze.json` |

实际终局是 `P2_PASS_WORTH_WRITING`。T2.35 自身明确停止，不进入 Writer、Fidelity、装配或
P3。

### 5.2 Writer 与装配 sidecar

Writer v2 的生成调用不在当前仓库或 sidecar 的原始调用日志中；快照只保存“产品已接受的
Writer v2 原件”及其后续装配证据。其精确模型、Prompt、token 和金额均无法从当前文件恢复，
状态为 `unknown`。

Writer 装配 sidecar 的 `control/input-freeze.json` 证明实际输入清单为：

1. `BOOK-CONTENT-FLOW-v2.md`
2. `T2.35.md`
3. `run.json`
4. `production-freeze.json`
5. `chapter-scope.xhtml`
6. `chapter-readable.md`
7. `D3-expert.md`
8. `locked-knowledge-cards.md`
9. `review-outcomes.md`
10. `D3-p2-gate.md`
11. `writer-v2-accepted.md`

实际后续步骤：

| 步骤 | 模型／工具 | 输出 | 终局 |
|---|---|---|---|
| 两项获准小修与锚定装配 | `assemble-and-verify.mjs` | `reader-unit-assembly-v1.md`、`chapter-with-reader-v1.md` | candidate only |
| Assembly Boundary / Exact-Byte Check | 独立 Agent，`high`，backend model id `unknown` | `checks/assembly/result.json` | `PASS` |
| Writer Fidelity Check | 独立 Agent，`high`，backend model id `unknown` | `checks/fidelity/result.json` | `保真通过` |
| P3 审阅入口复制 | 机械复制 | `review/P3-product-review-candidate.md` | P3 `PENDING`，未 promotion |

这条 sidecar 证明候选层已装配、两道技术检查通过；不证明生产 B2 已集成，也不证明完整章节
产品接受。

## 6. U01／U02／U03：D 与 ABC 实际步骤

### 6.1 共同输入

`pilot-inputs/input-manifest.md` 证明：

| 单元 | 历史冻结输入映射 | bytes | SHA-256 |
|---|---|---:|---|
| U01 | F01 | 16368 | `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c` |
| U02 | F02 | 21297 | `27a0ef436b8d6e57ca9e6cb0cf4b43babe76f6852857edad0c2b6ae30bcf9e04` |
| U03 | F04 | 34512 | `0f4af98ac9beb82cea8d4ad708191bf28aa7758645249e0640d6c1d9d5c4f88a` |

U03 与 T2.35 的章节 scope SHA-256 相同，但两次运行的路线、任务和输出不同。

### 6.2 D 直接路线

实际任务文件：`02_DIRECT_ROUTE_TASK.md`。

```text
完整读取 U
→ 直接 Web 搜索真实外部对象 C
→ 同一会话最多保留 4 个内部候选
→ 同一会话按 R1—R8 淘汰
→ 同一会话选择 1 个或沉默
→ 同一会话恢复 C 的 M1/M2/M3
→ 同一会话按统一格式写近终稿
```

- 模型：`GPT-5（Codex）`
- 思考强度：`unknown`
- 工具：内置 Web 搜索与网页打开
- 每 U 预算：最多 10 查询、15 页面、至少 2 个来源
- 实际合计：5 查询、9 页面打开、7 个核验来源
- 输出：U01、U02、U03 均为 `status: PROPOSED`；另有候选台账和 runner manifest

### 6.3 ABC 路线

实际任务文件：`03_ABC_ROUTE_TASK.md`。

```text
完整读取 U
→ 同一会话提取最多 4 个 A
→ 为每个 A 生成最多 2 个 B-core
→ 选择最多 2 个 B
→ 用 B 做跨域 Web 搜索并生成 C 候选
→ 同一会话最多保留 4 个 C
→ 同一会话选择 1 个或沉默
→ 同一会话恢复 C 的 M1/M2/M3
→ 同一会话按统一格式写近终稿
```

- 模型：`GPT-5（Codex；本会话可见标识）`
- 思考强度：`unknown`
- 工具：内置 Web `search_query` 与 `open`
- 每 U 预算：与 D 相同
- 实际合计：18 查询、18 页面打开、15 个核验来源
- 输出：U01、U02、U03 均为 `status: PROPOSED`；另有 A/B/C 台账和 runner manifest

### 6.4 C、知识结构与 M1/M2/M3 的实际决定点

- **哪一步生成 C**：
  - D：直接搜索后，由 D 生成会话保留和选择；
  - ABC：B 搜索阶段后，由 ABC 生成会话保留和选择。
- **哪一步恢复 C 的完整知识结构**：
  - 两条路线都只在近终稿生成前写了一句“恢复 C 原本真实拥有的 M1/M2/M3 深度”；
  - 没有单独 Expert 产物、知识结构 schema、语义锁或独立恢复审核。
- **哪一步决定 M1／M2／M3**：
  - 同一个生成会话在最终稿“继续了解”中自行标注；
  - pilot 的 00—08 文件没有定义 M1、M2、M3 各自的可检验含义，也没有独立判定步骤。

六条实际标签：

| 单元 | D | ABC |
|---|---|---|
| U01 | `M1+M2+M3` | `M1+M2` |
| U02 | `M1+M2+M3` | `M1+M2` |
| U03 | `M1+M2` | `M1+M2` |

### 6.5 U01、U02、U03 各自经过的步骤

三个单元都经过同样的 D 七步和 ABC 八步；没有单元沉默，没有单元被停止：

| 单元 | D 最终 C | ABC 最终 C | 技术审核 |
|---|---|---|---|
| U01 | 社会连接责任模型 | 多手问题 | 两条均 `TECH_PASS` |
| U02 | 情境完整性 | 数据权利束 | 两条均 `TECH_PASS` |
| U03 | 公民宗教 | 身份融合 | 两条均 `TECH_PASS` |

技术审核后，v2 只机械修复盲审文件中 XHTML 的展示噪声；六条成品、路线密钥、成本比较和技术
资格均未改变。当前冻结文件没有保存已填写的产品盲审选择或产品接受判词。

## 7. Writer 实际拿到什么

### 7.1 长期合同要求

合同要求 Writer 只读：

- 已 `锁定并进入 Writer` 的完整 Expert 初稿；
- 语义锁；
- 来源核验结果；
- 为忠实组织所需的同一范围完整 B1；
- 冻结锚定关系。

### 7.2 T2.35 Writer sidecar

当前证据没有保存 Writer v2 的原始调用 Prompt、模型或逐项 read set。能够证明的是后续
装配 sidecar 收到了第 5.2 节列出的 11 个冻结文件，其中包括已生成的 Writer v2。

### 7.3 U pilot

U pilot 没有独立 Writer。D 和 ABC 的同一生成会话直接从完整原文、路线任务、
`05_PRODUCT_RULES.md` 和 `06_OUTPUT_FORMAT.md` 产出近终稿。因此不存在可独立列出的
“Writer 实际输入”；搜索、C 选择、知识恢复、写作和 M 标签在同一上下文完成。

## 8. Judge、Fidelity 与来源审核实际检查什么

### 8.1 U pilot 技术审核

独立审核按 H1—H10 检查：

1. 来源真实
2. 表达准确
3. 连接自然
4. 外部知识承重
5. 非同域专业扩展
6. 认知回报合格
7. 无表面跨域
8. 无原创伪装
9. 人类可读
10. 篇幅与阅读位置合理

资格规则主要由 H1、H2、H3、H4、H8、H9 和总 FAIL 数决定。审核只标记、不重写。它不是
Fidelity 与 Writer 的逐语义锁比较，也不是产品接受。

### 8.2 T2.35 来源审核

来源审核检查五张卡的价值、事实、重复、边界，核验神圣价值、禁忌交换、物质加码反噬、
象征性承认及 C4 删除测试。其 `P2_PASS_WORTH_WRITING` 只表示可进入后续 Writer。

### 8.3 Writer sidecar Fidelity

实际 F1—F5 检查的是：

- 相对已接受 Writer v2 是否只有两处获准修改；
- “禁忌交换”定义是否与锁定 K01/K02 一致；
- 象征性承认是否被收窄且保留空结果和实体边界；
- K01—K05 承重判断、方向交互、来源／Expert 综合区分及误用边界是否保留；
- lineage、Reader id、锚点和文件 hash 是否未漂移。

它只证明“装配 Reader 忠实于已接受 Writer v2 和锁定上游”，不重新判断这堂课是否值得、是否
讲清、是否符合最终产品体验。

### 8.4 最终 Judge

现行合同明确最终 Judge 尚未取得资格，且实现不在合同内。当前没有一个可从仓库运行的最终产品
Judge；产品接受仍只归产品负责人。

## 9. 失败、沉默与退出条件

### 长期合同

- 来源、范围、身份、读取权限或上游 gate 不明：硬阻塞；
- 背景没有稳定知识库存或控制层预先决定 Expert 看见什么：路由门阻塞；
- Expert 只交标题、结论、表面连接或原文内局部论辩：停止，不交 Writer；
- 课程入口只有新颖、没有价值：不得晋级；
- 来源或语义锁不足：退回、待补、淘汰或硬阻塞；
- Writer 必须新增知识才能可读：停止并退回内容锁；
- Fidelity 只有 `保真通过`、`退回 Writer`、`阻塞并重开内容锁`；
- B2 任一确定性检查失败：停止受影响项或装配；
- Expert 与受控偶遇允许沉默，沉默不自动表示成功或产品接受。

### T2.35

- 没有重试／返工额度；
- C4 不承重、内容不合格、来源阻塞或控制失败均停止；
- 实际在 P2 通过后按卡停止。

### U pilot

- D 或 ABC 没有合格候选时输出 `SILENCE`；
- 超预算、历史答案污染、路线交叉污染、模型／思考强度不公平等可触发
  `EXPERIMENT_INVALID`；
- 实际技术审核判为 `EXPERIMENT_VALID_WITH_LIMITATIONS`；
- 限制包括思考强度 unknown、缺少原始模型调用日志、无法日志级证明隔离、Prompt 未改和未补跑。

### Discovery sidecar

- 实际只运行 18 次 Scout，下游 Normalizer、Judge、Clusterer、Verifier 调用为 0；
- 18/18 JSON 可解析并通过 response schema，但 18/18 至少一个 exact anchor 不匹配；
- harness 将 18 次都标记 `MODEL_CONTRACT_FAILURE`；
- 当前状态只允许把原始结果作为 diagnostic evidence，不得写成产品通过。

## 10. 当前实际模型、参数、工具与成本

| 运行 | 模型 | reasoning | 工具 | 可见成本 |
|---|---|---|---|---|
| Discovery 18 次 Scout | `gpt-5.4` | `medium` | `codex-cli 0.142.5`；plugins/apps/skills instructions 关闭 | V0：449,673 input / 20,996 output；V1′：325,761 input / 25,701 output；billed cost unknown |
| T2.35 Expert | `gpt-5.6-sol` | `high` | Web Search + Web Fetch | token / 金额未记录 |
| T2.35 来源审核 | `gpt-5.6-terra` | `high` | Web Search + Web Fetch | token / 金额未记录 |
| Writer v2 生成 | `unknown` | `unknown` | `unknown` | unknown |
| Writer Assembly check | backend id `unknown` | `high` | 独立 Agent | token / 金额 unknown |
| Writer Fidelity check | backend id `unknown` | `high` | 独立 Agent | token / 金额 unknown |
| U D 路线 | `GPT-5（Codex）` | `unknown` | Web 搜索与网页打开 | 5 查询 / 9 打开 / 7 来源；token、时间、金额未记录 |
| U ABC 路线 | `GPT-5（Codex）` | `unknown` | Web `search_query` / `open` | 18 查询 / 18 打开 / 15 来源；token、时间、金额未记录 |

## 11. 当前 schema 与协议

- `tools/run.py`
  - `readerlab-run/v2`
  - `readerlab-production-freeze/v1`
  - `readerlab-acceptance-freeze/v1`
  - production 目录：`raw`、`locked`、`final`
  - promotion 检查：`artifact_type`、`fields`、`source`、`synthetic`、`version`
- Discovery sidecar
  - `seed-batch.schema.json`、`trigger-map.schema.json`
  - Scout V0／V1′ response schema
  - Normalizer、Clusterer、Judge、Verifier、product-pack 等 schema；本轮下游调用为 0
- Writer sidecar
  - `readerlab-writer-assembly-input-freeze/v1`
  - `readerlab-reader-unit-lineage/v1`
  - `readerlab-assembly-boundary-check/v1`
  - `readerlab-reader-fidelity-check/v1`
- U pilot
  - Markdown 输出格式，无 JSON schema；
  - `status: PROPOSED | SILENCE`；
  - 近终稿固定为原文锚点、标题、正文、继续了解和 M 深度标签。
- 长期 v2 内容合同
  - 功能 seam 已冻结；
  - 各语义交接物精确字段和 schema 明确保持 `unknown`。

## 12. 已知可能与产品要求不一致之处

以下是当前文件可以证明的结构差异，或产品负责人本次明确要求审查的观察；没有把它们写成已完成
根因判定：

1. 产品合同要求稳定认知背景 → 完整 Expert 课 → 内容锁 → 独立 Writer → Fidelity；U pilot
   把 C 搜索、选择、恢复、写作和 M 标签合在同一生成会话。
2. U pilot 没有独立 Expert 产物、完整知识结构 artifact、语义锁或 Writer 输入包，外部审核只能
   从最终文反推过程。
3. M1／M2／M3 在 pilot 包中没有操作性定义或独立判定器，标签由生成者自报；技术审核也没有逐层
   核验 M 标签。
4. U 技术审核 H1—H10 可以确认来源、准确、连接、承重与可读，却没有单独检查“C 的内部理论
   结构是否已经搭建完整”或“标签深度与正文展开深度是否一致”。
5. 六条 U 成品技术上全部 `TECH_PASS`，但技术审核文件本身明确声明不替代产品判断；这允许出现
   “技术通过、产品不接受”而不触发技术失败。
6. 产品负责人本次观察：C 的理论内容没有解释清楚，框架内部结构没有搭建，正文主要解释 A 如何
   连接 C，M 标签可能高于实际交付深度。这些观察应由审查者对六条实际成品逐条核对。
7. U 运行缺少原始模型调用日志，精确 reasoning、Prompt 注入、补跑和隔离只能依赖 runner
   自报；token、时长和金额缺失。
8. Writer v2 的生成模型、原始 Prompt、调用日志和精确 read set 不在当前证据中；只能验证其后续
   装配与 Fidelity。
9. 当前 `docs/current-task.md` 与 `docs/dev-state.md` 更新到 2026-07-26，仍把 T2.35 和
   Discovery sidecar 作为当前事实，没有登记 2026-07-29 U pilot。U pilot 在本次冻结前只存在
   于仓库外。
10. 当前生产 Skill 入口不存在；现有项目 Skill 只允许虚构测试材料。
11. `tools/run.py` 只保护文件身份、promotion 和冻结顺序，不编排语义角色，也不检查产品忠实性。
12. v2 合同的语义 schema、模型和失败实现仍为 unknown；当前 sidecar 的临时 schema 不能自动
   填补长期合同。

## 13. 测试与最小运行验证

| 命令 | 结果 |
|---|---|
| `python3 -B tests/entry.py` | 36 项中 35 PASS、1 FAIL |
| `python3 -B tools/run.py check runs/T2.35-CH08-D3-EXPERT-P2-01 --state-file contracts/BOOK-CONTENT-FLOW-v2.md` | PASS；8 个 production 文件，production frozen，acceptance frozen:2；不评价语义和产品接受 |
| `sha256sum` 复算 U01/U02/U03 | 3/3 与 input manifest 一致 |
| 在 `audit/current-runtime-snapshot/writer-assembly/` 执行 `sha256sum -c SHA256SUMS` | 28/28 PASS |
| `git diff --check` | 对原有 7 个已跟踪修改和两份新增审查文档为 PASS；把逐字冻结证据加入 index 后为 FAIL，见下方 |

失败项：

- `test_asset_register_exhaustively_lists_taskcards_and_runs` 失败。测试按当前工作树枚举 Markdown／run
  资产，发现此前未登记的根目录实验文件以及本次新增的只读审查快照，不等于这些文件内容测试失败。
  按本轮“不得为测试通过修改实现”的约束，没有修改资产登记或测试。
- `git diff --cached --check` 对若干逐字冻结输入和知识卡报告 trailing whitespace。Discovery
  输入保留来源的 CRLF，知识卡使用 Markdown 行尾双空格；修改这些字节会破坏现有 SHA-256 和
  冻结证据，因此本轮没有格式化它们。
- 第一次从仓库根直接执行 Writer `sha256sum -c` 时，manifest 的相对路径无法解析；切换到
  manifest 所在目录后 28/28 PASS。这是验证命令工作目录错误，不是 artifact hash 失败。

无法验证：

- U 两条路线精确 reasoning 是否相同；
- U 是否存在未记录的 Prompt 修改、补跑或跨路线读取；
- U token、墙钟时间和货币成本；
- Writer v2 生成模型、Prompt、调用顺序与 token；
- 长期内容合同的真实集成和端到端产品资格；
- 最终产品 Judge 资格；
- Obsidian / `tandem-comments` 真实集成；
- 产品负责人对 U01／U02／U03 六条成品的最终逐条判词。
