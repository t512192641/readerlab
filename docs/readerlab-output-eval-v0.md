# ReaderLab Output Eval v0

## 状态

- Eval 状态：`draft-v0`
- 目的：证明 ReaderLab 是否提升最终读者产物，而不是只证明文件存在或 validate 通过。
- 方法来源：`yao-meta-skill` output eval method，已按 ReaderLab 的 source-grounded 阅读包质量改写。
- 当前执行形态：先形成 scorecard 和 worker-ready case；尚未收集 provider-backed model evidence。

## Scorecard 读法

v0 case 只有在输出诚实标明来源范围、对阅读有帮助、且可按 source refs 复核时才算通过。不能靠复述某个关键词过关。

评分字段：

- `baseline_pass_rate`：旧样张或无 ReaderLab 约束输出的预期通过率。
- `with_readerlab_expected_pass_rate`：使用 IR + contracts 后的预期通过率。
- `absolute_delta`：预期提升。
- `failed_assertion_taxonomy`：断言抓到的质量问题类型。
- `human_review_status`：`pending`、`accepted` 或 `rejected`。

本轮新增的回归重点：

- 低覆盖或 spine 级登记不得冒充精选译文正文或产品 ready。
- 全书主线不能停在目录复述；必须解释核心问题、机制链、案例和边界。
- 精华、亮点或可迁移洞察必须有 item-level source/location refs。
- 读者页不能混入完整内部审计；审计信息应在 README、report、appendix 或契约 JSON。
- `dbs-suite` 能力地图不能退化成目录清单；必须有 route/exclusion 和验收方法。

## Case 1：《埃隆之书》目录地图和局部深读

### 输入

- Source EPUB：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 当前 demo 包：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629`
- 已完整处理局部单元：`部件 II：极致艰苦工作`
- 已知来源范围：EPUB `v101-13.xhtml` 到 `v101-18.xhtml`，约 25,686 抽取字符

### Baseline

旧 `02_全书地图.md` 存在，但不是合格全书地图。它的失败模式是：低覆盖或局部处理样张看起来像“全书理解”。它只能作为负面 baseline。

### With ReaderLab 预期输出

下一版样张应产出：

- 针对 demo 包来源范围的 `source-registry.v1` 和 `location-map.v1` 实例。
- 基于 TOC/meta/已知结构的全书 `catalog-map.v1`。
- 针对 `部件 II：极致艰苦工作` 的局部深读地图，明确标记 partial coverage。
- 在完整正文覆盖前，不产出声称 full coverage 的 `grounded-global-map.v1`。
- 只对已覆盖部分产出提炼候选；每项必须有 source refs、confidence、applicability boundary 和 human review status。
- 读者 Markdown 必须说明先读什么、哪些只是路线假设、哪些仍待人工复核。
- 局部深读必须产出读者可读的深读卡，覆盖可用的框架、原则、案例、反例、术语、可迁移洞察；没有的类型必须说明为空或降级原因。
- 读者 Markdown 只保留阅读主线和必要来源提示；coverage 明细、hash、validator、worker 状态进入审计输出。

### 可机器检查断言

| ID | 断言 | 抓到的问题 |
|---|---|---|
| ELON-A01 | 只有 TOC/meta/全书结构线索时，输出应包含 `catalog-map.v1`。 | 目录冒充全书 grounded map。 |
| ELON-A02 | 除非 source registry 标记完整正文覆盖，否则不得出现 `coverage_status=full` 的 `grounded-global-map.v1`。 | 低覆盖冒充全书。 |
| ELON-A03 | 每个地图都有 `source_scope`、`coverage_status`、`coverage_note`、`confidence`、`review_items`、`machine_status`、`human_status`。 | 文件存在或 validate 替代验收边界。 |
| ELON-A04 | 局部深读必须命名 `部件 II：极致艰苦工作`，并标出 `v101-13.xhtml` 到 `v101-18.xhtml`。 | 局部判断无来源。 |
| ELON-A05 | 提炼项必须有 source refs 和适用边界；不得出现无来源的泛泛“精华”。 | 精华无证据。 |
| ELON-A06 | 读者路线必须区分全书路线假设和已覆盖部件阅读指导。 | TOC 清单冒充阅读路线。 |
| ELON-A07 | 除非有明确人工评审记录，否则 human status 必须保持 `pending`。 | 机器完成冒充人工验收。 |
| ELON-A08 | 局部深读必须包含 `deepread_cards`，并至少覆盖框架/原则、案例、反例或边界、术语、可迁移洞察中的 4 类；缺失类型必须有 review item。 | “6 个收获”太浅，缺案例/反例/术语。 |
| ELON-A09 | 高价值卡片必须有 V1/V2/V3 验证状态；未验证不得写成稳定方法论。 | 仓颉三重验证没有进入读者页。 |
| ELON-A10 | 高价值主张的 `primary_location_refs` 不能只停在包级或 spine 级；若只能 spine 级，必须写 precision exception。 | source-grounded 只落到粗 refs。 |
| ELON-A11 | 读者页不得把 `human_status=pending`、validator、未写入 LifeAtlas、hash、spine coverage 明细作为主阅读段落；这些信息必须进入审计输出。 | 读者页混入内部审计。 |
| ELON-A12 | 全书级输出必须使用书中正式标题或可追溯标题映射，不能只用“部件 I/II/III/IV”占位。 | 地图看起来像机器目录，不像读者路线。 |
| ELON-A13 | 全书主线或局部 thesis 必须包含 `reader_gain` 或等价字段，说明读者读完新增理解是什么。 | 全书主线太浅，只复述目录。 |

### 人工评审点

- 目录地图是否帮助第一次读者理解全书可能路线，同时没有假装已经深读全书？
- `部件 II` 局部深读是否保留足够一手内容，并解释这一部件为什么重要？
- 提炼项是否具体，还是退化成普通传记口号？
- 不确定性和复核边界是否清楚，同时不破坏阅读体验？

### 预期 v0 分数

- Baseline pass rate：低。除非被手工补丁修过，否则应失败 ELON-A02、ELON-A03、ELON-A05、ELON-A07、ELON-A08、ELON-A10、ELON-A11、ELON-A13。
- With ReaderLab expected pass rate：如果所有断言满足，应足以进入 worker review。
- Worker 输出后的人工状态：`pending`。

## Case 2：`dbs-suite` capability map

### 输入

- Canonical package：`/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite`
- 当前版本：`2.15.1`，upstream commit `096f726a20407901ca517cfc42509f96232fd0ea`
- 当前 LifeAtlas 试产包：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726`

### Baseline

旧 `06_能力地图.md` 存在，但不是合格能力地图。它的失败模式是目录/库存映射：列出 Skill 或分组，却没有说明触发信号、方法原子、输出、验收，以及读者如何选择能力。

### With ReaderLab 预期输出

下一版样张应产出：

- 用于 canonical package 证据文件的 `source-registry.v1` 和 `location-map.v1` 实例。
- `capability-map.v1`，而不是图书式 `global-map.v1`。
- 能力域：说明这个 suite 服务什么用户问题或任务族。
- 每个重要能力：trigger signals、near-neighbor exclusions、method atoms、required inputs、output contract、verification method、source refs、confidence、review status。
- 读者路线：第一次理解、选择能力、深读方法、排错/验收路线。
- 即使 package validate 通过，也必须保持明确的 pending human review status。
- 每个能力域必须有 route decisions：何时用、何时不用、冲突时交给哪个能力、对应证据。
- sample coverage 必须显式列出未覆盖 Skills 或未覆盖路线，不能暗示已经覆盖完整 suite。

### 可机器检查断言

| ID | 断言 | 抓到的问题 |
|---|---|---|
| DBS-A01 | 输出使用 `capability-map.v1`；不得把 `dbs-suite` 写成图书 `grounded-global-map.v1`。 | 地图类型错误。 |
| DBS-A02 | 每个能力域至少有 trigger signal、method atom、output contract、verification method。 | 目录清单冒充能力地图。 |
| DBS-A03 | 每个高层能力都指向 `SKILL.md`、package manifest、scripts、references 或 tests 中的来源证据。 | 能力判断无来源。 |
| DBS-A04 | suite 顶层和高混淆能力必须有 near-neighbor exclusions。 | 触发边界过宽或含糊。 |
| DBS-A05 | 地图包含读者路线：先读、选择能力、检查方法、验证输出。 | 平铺库存，没有读者旅程。 |
| DBS-A06 | `machine_status` 和 `human_status` 分开；不得把 `delivery_status=deliverable` 当成人工接受。 | 机器完成冒充阅读质量通过。 |
| DBS-A07 | review items 包含来源缺口、能力名歧义和跨 Skill 路由不确定性。 | 隐藏不确定性。 |
| DBS-A08 | 每个能力域必须有 `route_decisions.when_to_use`、`when_not_to_use`、`handoff_to` 或 `route_conflicts`。 | 能力地图退化成目录/库存。 |
| DBS-A09 | `coverage_plan` 必须说明 sample/full 状态、已覆盖和未覆盖 Skills；sample 不得暗示 24 Skills 全覆盖。 | 代表性样本冒充整包能力地图。 |
| DBS-A10 | 读者 Markdown 不得把 package validate、manifest 数量、内部 blocker 当作主阅读内容；审计细节进入 report/appendix。 | 读者页混入内部审计。 |
| DBS-A11 | 能力域必须说明读者选择该能力后预期产物和验收检查，不能只有技能名或文件路径。 | 能力地图无法指导真实使用。 |

### 人工评审点

- 读者是否能据此决定真实任务该用哪个 `dbs-suite` Skill？
- 地图是否解释了能力之间的差异，而不只是列文件位置？
- 输出契约和验收方式是否具体到能检查未来产物？
- 不确定和重叠路线是否被诚实暴露？

### 预期 v0 分数

- Baseline pass rate：低到中。旧样张可能通过“文件存在”，但应失败 DBS-A02、DBS-A05、DBS-A06、DBS-A08、DBS-A09、DBS-A11。
- With ReaderLab expected pass rate：如果所有断言满足，应足以进入 worker review。
- Worker 输出后的人工状态：`pending`。

## 下一轮样张避免路径

- 《埃隆之书》先生成或更新 `source-registry.v1` / `location-map.v1`，再写 `catalog-map.v1`、`local-deepread.v1` 和读者 Markdown；不要先写读者页再补来源。
- 对全书级内容，spine 36/36 只能证明登记完整；若没有 heading/block/char 级一手正文 refs 和精选正文边界，不得声明产品 ready。
- 对局部深读，优先补深读卡、案例/反例/术语和 V1/V2/V3 状态；短“收获”列表不能替代深读。
- 对 `dbs-suite`，先按任务族聚能力，再写 route/exclusion 和验收；不要从目录顺序直接生成能力地图。
- 每个样张都应同时产出 reader-facing Markdown 和 internal-audit/report；两者互相链接但不混写。

## 禁止通过条件

出现以下任一情况，output eval 必须失败：

- 输出说或暗示旧样张是合格最终交付。
- 低覆盖书籍输出被标成全书 grounded understanding。
- 目录、TOC 或 Skill 列表被标成地图，却没有关系和来源支撑解释。
- 提炼、亮点或可复用洞察没有 source refs 和适用边界。
- 深读卡没有案例/反例/术语/验证状态，却被写成可迁移洞察。
- `dbs-suite` 能力地图只列 Skill 名、路径或目录分组，没有 route/exclusion/verification。
- 读者页主体混入大段机器审计、validator 绿灯或内部 blocker。
- validate、文件存在或 `delivery_status=deliverable` 被当成人工阅读验收。
- 输出写入 LifeAtlas `300/600/800`、修改 canonical source packages、安装 Skill 或新增依赖。

## 样张重做 worker 任务

### Worker A：《埃隆之书》ReaderLab v0 样张重做

写入边界：

- 只有确认不会覆盖批注风险后，才允许写到现有 demo 包下的新试产文件，或清晰版本化的 sibling path。
- 可以在试产包内写契约实例。
- 不写 LifeAtlas `300/600/800`。
- 不把旧 `02_全书地图.md` 覆盖成“已接受”版本。

输入：

- 读取本文件、`docs/readerlab-skill-ir-v0.md`、`docs/contracts/readerlab-contracts-v0.md`。
- 按需读取 source package / demo manifest 和当前 demo 结构。
- 旧 `02_全书地图.md` 只能作为负面 baseline。

预期输出：

- `source-registry.v1` 和 `location-map.v1` 实例。
- 全书路线的 `catalog-map.v1`。
- `部件 II：极致艰苦工作` 局部深读地图。
- 从契约渲染或伴随契约生成的读者 Markdown。
- 简短 worker report，列出 ELON-A01 到 ELON-A13 的结果。

验收：

- 所有机器断言通过，或列出明确失败原因。
- human status 保持 `pending`。
- 不声称已经产出 full-book grounded map。

### Worker B：`dbs-suite` capability-map v0 样张重做

写入边界：

- 只有确认保护已有批注且不无审查覆盖旧文件时，才允许在 `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726` 写新试产产物。
- 不修改 `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite`。
- 不安装、启用或更新任何 Skill。

输入：

- 读取本文件、`docs/readerlab-skill-ir-v0.md`、`docs/contracts/readerlab-contracts-v0.md`。
- 只把 canonical `dbs-suite` package 文件作为来源证据读取。
- 旧 `06_能力地图.md` 只能作为负面 baseline。

预期输出：

- `source-registry.v1` 和 `location-map.v1` 实例。
- `capability-map.v1`。
- 读者可读的 capability map Markdown。
- 简短 worker report，列出 DBS-A01 到 DBS-A11 的结果。

验收：

- 所有机器断言通过，或列出明确失败原因。
- 地图解释能力、触发、方法原子、输出、验收和读者路线。
- human status 保持 `pending`。

## 后续执行证据

契约稳定后，后续 worker 可以补确定性 output eval 工具。第一版工具只需读取 fixture outputs 并按断言评分。Provider-backed model evidence 是可选项，且需要明确凭证；fixture 或 deterministic runner evidence 不能被描述成 model-executed evidence。
