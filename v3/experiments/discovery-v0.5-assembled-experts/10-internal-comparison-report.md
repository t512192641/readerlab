status: executed
model: gpt-5.6-terra
reasoning_effort: high
started_at: 2026-07-30T06:49:08Z
finished_at: 2026-07-30T06:50:42Z
input_files:
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/01-run-manifest.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/03-expert-packs/freeze-manifest.json
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E1-thin.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E1-assembled.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E2-thin.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E2-assembled.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E3-thin.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E3-assembled.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/06-identity-audit.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/07-blind-collision-audit.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/08-clusters-and-comparison.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/09-USER-CANDIDATE-CARDS.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/control/anonymization-map.json
output_files:
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/10-internal-comparison-report.md
agent_context: independent
retry: no-retry
---

# ReaderLab v0.5｜组装专家与薄卡内部比较报告

## 本轮创建或修改过的全部 run 和文件清单

### 项目内正式文件

- `v3/experiments/discovery-v0.5-assembled-experts/10-internal-comparison-report.md`：本轮新建的独立内部比较报告。

### 项目外工作文件

无（0 个）：本轮未创建或修改项目外工作文件。

## 结论

本批配对材料支持有限的方向判断：`ASSEMBLY_DIRECTION_SUPPORTED`。组装条件产生了唯一一个通过身份与盲碰撞审核、进入用户候选卡的借脑候选；薄卡的两次原始激活则是同一真实资产的重复，并都因当前阅读材料缺少关键机制连接而停在 `HOLD_CONNECTION`。这只是本次三个配对专家、一个阅读材料范围内的方向性支持，不是统计显著性，也不能推出组装对一般任务有普遍因果优势。

用户产品接受：`unknown`；CORE：`0`。运行按清单在用户候选卡后停止；未生成新的候选、Expert、Writer 或任何生产授权。

## 计数口径与结果

身份通过率的分母是进入身份审核的原始候选，不把零激活阅读组误记为身份失败。AI 综合资产、邻近深化、强行类比和借脑候选均按聚类报告的定义计数；同一资产的重复原始记录仍保留在激活数中，但不重复计为独立供给。

| 指标 | thin | assembled |
|---|---:|---:|
| 原始激活 | 2 | 1 |
| 身份通过率 | 2/2（100%） | 1/1（100%） |
| AI 综合资产 | 0 | 0 |
| 邻近深化 | 2 | 0 |
| 强行类比 | 0 | 0 |
| 借脑候选 | 0 | 1 |
| 无候选的专家行 | 1/3 | 2/3 |

三个 full 专家包各冻结 6 项已核验资产：E1 为 6、E2 为 6、E3 为 6，合计 18。薄卡本身各为 0 项具体资产，符合冻结清单的设计。

薄卡的两次原始激活均指向同一 Hobsbawm 资产，故去重后只形成一个 `HOLD_CONNECTION` 资产簇；组装条件的唯一激活是 E3 的 Williams 资产，也是唯一独特资产和唯一借脑候选。两组已输出候选的身份通过率相同，不能把方向判断误写成“组装身份更准确”。

## raw 证据与归因

E1-thin 与 E3-thin 各产生一条 Hobsbawm 的“被发明的传统”记录。身份审核确认二者均是同一真实、可定位资产，且没有临时拼接；盲碰撞审核却认为本次材料没有直接给出重复实践、连续性主张或稳定仪式运行这几个必要连接要件。两条因此均为 `HOLD_CONNECTION`，并被标为邻近深化：它们的主要解释效果紧贴材料已给出的国家重塑、筛选和官方化说明。

E3-assembled 产生一条 Williams 的“主导／残余／新兴”记录。raw 记录明确锚定材料中的官方制度化、压制地方传统与选择性纳入；盲审认定三位置及其吸纳、边缘化、压制关系构成非作者等价的新增观察方式，连接真实，最终为 `BORROWED_BRAIN_CANDIDATE`。这正是唯一进入用户候选卡的对象。

其余三条 raw 记录是审慎沉默，而非失败候选：E1-assembled 未见其六项长期机制链所需证据；E2-thin 拒绝以生态／复杂系统领域词作装饰；E2-assembled 拒绝把生态位、内共生、选择、韧性、灾变或复杂适应系统硬套到材料。由此两组强行类比计数均为 0；该零值表示没有产出被审核判定为强行类比的候选，不表示该风险已被一般性消除。

### 问题分别来自哪里

- **专家包**：E1 full 包的六项冻结资产要求材料提供更长的跨政体、资源动员、人口—财政、差异化统治、气候中介或路径依赖机制链，因此本次材料不触发，产生零候选。E2 thin 没有可核验的具体资产；E2 full 的具体资产又要求生态与复杂系统的相应证据，这共同导致 E2 两组审慎停止。相反，E3 full 的 Williams 资产提供了与材料中制度化、压制、选择性纳入可逐项对接的关系结构。
- **阅读任务／材料**：它充分支持国家重造、压制与选择性吸纳，却不充分支持 Hobsbawm 所需的重复仪式、过去连续性主张和稳定运行；这是两条薄卡候选连接不足的直接原因。相同材料同时足以支撑 Williams 的位置与权力关系，说明问题不是材料一概不可用，而是资产—材料匹配不同。
- **审核门槛**：身份审核只确认资产真实、归属和机制来源，因此三条候选均通过；盲碰撞审核另要求外部增量、非作者等价、资产完整性及真实连接，故两条 Hobsbawm 记录被挡在 `HOLD_CONNECTION`。去重门将它们合为一个资产簇，用户卡门只允许盲审通过的 Williams 记录进入用户入口。

## 方向判断、调用与隔离边界

组装显示方向性改善的依据很窄但明确：它没有产生连接不足或强行类比候选；E1、E2 在条件不成立时停止；E3 产出了本批唯一独特、具明确认知位移的借脑候选。反向限制也同样成立：只有三位专家，组装组原始激活更少（1 对 2），两组候选身份通过率同为 100%，所以不能声称统计显著性、一般准确率提升或普遍因果关系。

运行清单记录首轮**计划** 12 次外部上下文调用（3 个专家构建、1 个专家核验、6 个阅读、1 个身份审计、1 个碰撞审计）。本报告允许输入中可直接核验 10 份 `executed` 运行记录：6 份 raw、身份审计、盲碰撞审计、聚类比较、用户候选卡；其中聚类与用户卡是后续控制步骤，专家包构建／核验的实际调用记录不在允许输入内。因此，计划调用数为 12，而最终实际总调用数在本报告的证据边界内为 `unknown`，不得把计划数冒充完成数。

隔离边界如下：冻结前不读测试原文或旧实验；生产端在用户卡冻结前不读 GOLD-STANDARDS、旧 examples、旧候选、旧 raw seed、C1—C9、K1—K10 或旧判词；full 只用本 run 的 `VERIFIED` 资产，thin 不含具体资产身份；盲审收到匿名 A01—A03，不接收原候选 ID、阅读组、传统、raw 结论或内部建议。内部比较报告获准使用匿名映射，但不以匿名映射绕开上述生产隔离。

另有必须保留的运行限制：聚类上下文曾误读治理文件；其说明称该文件未用于分析，且 `08` 的正式 `input_files` 未列该治理文件。即便没有证据表明它改变了聚类结论，这仍是一次上下文隔离偏差，不能掩盖，也不能据此把本轮结论升级为更强证明。

## 用户卡停止点与下一轮最小动作

用户卡只保留候选 A（Williams），并要求产品负责人判定其是否真实独立、是否带来原文之外的观察、是否只是专业化改写，以及是否愿意进入 Expert。当前停止点已经达到：用户候选卡生成后立即停止；产品接受仍为 `unknown`。

下一轮最小动作是只收集产品负责人对候选 A 的早期判词。若未获明确“进入 Expert”的接受，不创建 Expert、Writer 或生产授权；若获接受，后续工作须另立任务和授权，不能由本报告自动触发。
