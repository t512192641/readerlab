# ReaderLab 图书线重建执行路线图

> 派生执行路线，不拥有产品决议，与 owner 文档冲突时停止并报告

## 问题、现状与边界

本路线在干净种子上把图书线逐步落成可运行流水线，目标是达到 80 分交付，并正面处理低质量复述、成品样式差与裁判识别不出问题三个历史痛点。执行／语义／产品三层验收必须分开；生产端不得偷看金标；旧项目完全隔离。

当前仓库只有产品、架构与证据基线：`PRODUCT-DECISIONS.md`、`ENGINEERING-LESSONS.md`、`GOLD-STANDARDS.md`、`examples/`、`blueprints/PIPELINE-MAP.md` 与种子完整性验证器。没有内容生产 runtime。产品事实只由产品 owner 拥有，派生架构只负责呈现两条长期产品线；候选数量、模型强度、考试门槛、反馈数量、组织方式和节奏都是任务卡拥有的阶段性参数，不是长期产品标准。

## 当前产品时序校正

`PRODUCT-DECISIONS.md` 拥有本阶段产品事实，`blueprints/PIPELINE-MAP.md` 呈现两条长期产品线；一次性实验组织、阶段交接和停止条件只由当前任务卡拥有。本路线不复制 owner 正文，只把它们编译成当前执行顺序。

当前执行顺序仍以取得产品接受的正例目标包为第一目标。T2.4—T2.7 均已完成并被产品负责人整包否决；T2.8 的三个既存知识对象核心卡获准进入单样张打磨。T2.9 的伯格 v03 内容与 T2.10 原文融合 v02 已经产品接受；T2.11 的宗派化与诺斯意识形态—执行成本机制 v01 也已分别获准进入原文融合。下一轮 T2.12 先在同一完整章节验证两种不同知识结构的融合迁移，并以任务卡内的激进墙钟预算暴露浪费；通过后立即停止打磨已见材料，转向未见完整章节的 Expert 开放发现与完整授课。已见章节融合不能证明未知材料能力，未见章节试跑也不能跳过当前融合迁移。

Expert 日常生产资格按三个不同证据层顺序取得：第一，跨知识结构的内容与融合正例获产品接受；第二，在未见完整章节中完成开放发现、允许沉默、价值选择和同一 Expert 完整授课；第三，在流程冻结后用另一未见材料和目标档模型复验，不靠改 Prompt、加专属 schema 或最强模型救场。具体章节数、模型、调用量、预算和停止线由对应任务卡逐轮冻结；当前只能确认至少还需要一次可诊断的未见章节试跑和一次冻结后的未见复验，不能提前宣称 Expert 已通过。

Expert 资格成立后，才从跨样本稳定部分建立新版内容审核、Writer、只装配不改文和最小 harness；随后以目标档模型跑完整 B1→发现→课程→来源核验→Writer→B2 路径，再用已接受正例重新校准独立 Judge 并取得所需 gate，最后扩大到多章节去重、成本与 B3，形成整本书生产。历史 T2.2 恢复设计只作条件式资料，不得机械恢复成当前必经的 21 卡工程。

Skills 线产品上独立，可在产品负责人明确调整优先级并提供一份获授权 Skill 材料后，与图书线以隔离任务卡并行启动一个人工端到端样张：E1 必交，E2／E3／E4 分别生产或合法归零并分别验收。两线只共享材料身份、scope、hash、读取隔离、receipt 与验收分层等薄骨架，绝不共享 B2／E2-E4 语义标准、Expert／Writer 合同、Judge、金标或通过证据。

下文关于 T2.2 恢复控制面、M2 与后续阶段的内容继续保留为历史和未来条件式设计，但本次时序校正不授权注册恢复卡、执行恢复链、创建 M2 receipt、调用旧 judge 或进入阶段 3。凡与本节时序冲突的旧“裁判先上岗”描述，不再构成当前执行许可。

## 总体架构：轻骨架、合同与执行 Agent

- **确定性骨架**：Python 标准库的小脚本只负责 run 目录与材料身份哈希、`raw`／`locked`／`final` 目录隔离、冻结清单、以及 preflight／postflight。它不做状态机、数据库或调度。
- **产品 owner、架构地图与节点合同**：`PRODUCT-DECISIONS.md` 定义长期产品责任，`blueprints/PIPELINE-MAP.md` 呈现派生架构；每个节点再用 Markdown 合同说明输入、输出、硬阻塞、允许读取清单和终局状态。任务卡和节点合同不得覆盖 owner，也不得把一次性实验组织复制成长期默认。
- **执行 Agent**：Codex 会话按合同完成语义工作。历史 T2.2 原始资格考试是主控准备／评分侧加鲜会话 judge 的已完成／失败隔离复合任务；恢复链只允许 T2.2-R09、T2.2-R14、T2.2-R19 为复合任务，其余十八张恢复卡和既有普通任务均为单会话。所有跨会话状态必须写入任务卡列出的仓库文件，禁止口头传递。每项模型调用与调用粒度必须在当前任务明确获授权；“一次调用一张完整知识卡”只是可调整的起点参数。

生产／验收隔离由目录和合同共同实现。生产任务合同列出白名单，`GOLD-STANDARDS.md` 与 `examples/` 仅在裁判、透镜开发、诊断或回归任务被逐项授权时开放。

当前实验组织、角色输入白名单和停止条件只由对应任务卡拥有；本路线不另写一套责任正文。`implemented`、`integrated`、`verified` 与产品检查点分开，技术完成不得自动晋级。

## 会话护栏

- **任务卡制**：派发前写自包含任务卡，逐项列出目标、读取白名单、交付路径、具体约束引用和完成判据。会话无状态，仓库是唯一记忆；会话间不得口头传递状态。历史 T2.2 的隔离复合任务只允许主控准备／评分侧与鲜会话 judge 通过 frozen packet、brief、answers、key 与 baseline 文件交接；恢复链的三个复合任务也只能通过各自任务卡列出的冻结文件交接。
- **状态头分层**：未来合同、透镜和执行方法卡应带 `status: draft|frozen` 与 `scope: long-term|run-only`。T0.3 术语表、T1 合同和种子透镜先以 `draft` 提交；M1 通过后，主控只在语义不变时改为 `frozen`，并创建 `contracts/M1-freeze-receipt.md` 的独立 gate commit。M1 receipt 必须逐文件绑定 `contracts/GLOSSARY.md`、所有冻结 T1 合同和 `lenses/T1.9-seed-lenses.md` v1 的 SHA-256；需语义修改则先返工；无 receipt 不得进入 T2。T2.2 恢复后，M2 只能按下文精确 active/history schema 创建 `diagnostics/M2-gate-receipt.md`，不得继续引用失败的 v1 baseline 作为 active。阶段 3 每张卡先核对 M2 所记 M1 receipt SHA-256 与实际 M1 receipt 一致，再用实际 M1 receipt 核对本卡所读 T1 合同 hash；T3.3／T3.6 再用 M2 receipt 核对所读 T2 正文 hash，最后才读取正文。receipt 只证明身份与 hash，不复制、引用或替代正文。只有产品事实变化才修改 `PRODUCT-DECISIONS.md`，并由产品负责人决定。一次性参数只能活在对应任务卡及该次 run 中，并按任务卡声明失效。
- **一任务一提交**：每任务恰好一次本地提交；验收查看 diff。
- **决议一致性检查**：主控对每项交付逐条核对相关产品决议。

并行任务必须拥有不相交写入范围。T0.2 先完成运行脚本与验证器，再执行同样写验证器的 T0.3。T0.3 完成后，T1.1—T1.8 可独立并行；T1.9 读取 T1.4，因此只在 T1.4 后执行。组装一致性由验收侧审查。

## T2.2 v3 恢复控制面

### 当前状态与授权边界

- 历史原始 T2.2 是已经完成且资格 `FAIL` 的复合任务；其 v1 baseline 与 blocker 永久保留为失败历史。
- 活动恢复架构固定为 `diagnostics/T2.2-recovery-architecture-v3.md`，commit `a67f011d112e1e06022867cb3577110816064bd9`，SHA-256 `38025c0b2ebb26171e7f6ad8bef69b97bfeb2d88597a78e67b3dcdc48110d1e1`。
- 活动架构审查固定为 `diagnostics/T2.2-recovery-architecture-v3-preflight-review.md`，commit `626562fa3fa6487200e953ca0b804a275ec3ef33`，SHA-256 `e5d450f019685fba6eed679e06ccedee10255591e9a4a65359ac6cfb918e06ec`，结果 `PASS`。
- 独立质量复核固定为 `diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md`，commit `e74221b85a8c750827c534e14d6df4079cb85c06`，SHA-256 `a81ded57546981d40b7c95d0d206ca0b627008fe509c32dfff1fb09abb415342`，结果 `CONFIRMED_PASS`。
- A1 `A1_ARCHITECTURE_RELEASED` 已通过；C0 是只修改控制面的 `controller-only bootstrap seam`。C0 修复已完成实现与确定性回归，但 `A2_CONTROL_PLANE_INTEGRATED` 只能由后续总控和独立后置审查认定，当前仍为 A1。
- C0 不注册恢复卡、不读取材料、不调用模型、不创建 M2 receipt、不执行 R01，也不进入阶段 3。当前恢复卡数量仍为 0，T2.2 资格仍为 `FAIL`，M2 仍未建立。
- 下一状态只能由总控重新读取并另行授权：21 张恢复卡从 0 一次性原子注册为 21。不得部分注册、额外注册或借 C0 自动创建 R01。

### 恢复任务闭集与会话粒度

recovery-registration-cardinality: 0|21

恢复 ID 字面闭集恰为：

`T2.2-R01`、`T2.2-R02`、`T2.2-R03`、`T2.2-R04`、`T2.2-R05`、`T2.2-R06`、`T2.2-R07`、`T2.2-R08`、`T2.2-R09`、`T2.2-R10`、`T2.2-R11`、`T2.2-R12`、`T2.2-R13`、`T2.2-R14`、`T2.2-R15`、`T2.2-R16`、`T2.2-R17`、`T2.2-R18`、`T2.2-R19`、`T2.2-R20`、`T2.2-R21`。

recovery-composite-task-ids: T2.2-R09,T2.2-R14,T2.2-R19

这三张卡是仅有的恢复复合任务；其余十八张必须声明 `single-session`。未注册 ID、不同大小写或补零、R22、额外 `T2.2-R*` 路径及任意 1—20 张部分集合都必须由验证器拒绝。

每张未来卡必须沿用六节模板，在 `## 3. 允许读取清单` 逐行内嵌验证器按 v3 单一发布责任编译出的完整 `read-path` 投影，并在 `## 4. 交付文件清单` 逐行内嵌完整 artifact-policy 写投影。两侧均执行字面集合相等检查；少路径、多路径、重复、范围、glob、前缀、大小写变化或放错章节均禁止派发。读取章节出现的任何路径字面量都纳入完整白名单比较，不能用去掉反引号、改写为自然语言或省略 `read-path` 前缀绕过机械闭集。

读取投影严格分成两层：

1. 所有卡都可读取四份项目治理文件与自身任务卡；
2. 恢复业务输入只按本卡单一发布责任、direct subject 和完成独立复核所需的已发布证据逐路径授予。

控制面验证器的完整 hash 重算权限不等于任务执行者的读取权限。验证器可以在派发前、写后和 M2 gate 独立重算完整仓库身份、历史链和 blocker 状态，但不得把这份全局可见性转授给 R01—R21。上游文件要求下游记录的固定身份、commit/hash 或历史坐标，必须从冻结任务合同、允许读取的 manifest/review 或已发布证明忠实传递；不能仅因 `_recovery_chain_dependencies` 最终会重算该文件，就把正文加入执行角色 `read-path`。prior blocker gate 由控制面先判断，也不自动给业务角色增加 blocker 或 blocker 之外的历史正文读取权。

recovery-r05-previous-business-read-count: 55

recovery-r05-business-read-count: 31

二次 C0 的旧实现中，R05 业务读取为 55 路径；加四份治理文件与自身任务卡后，完整 `read-path` 为 60 路径。修复后的业务读取闭集严格等于 v3 §8.8：28 个 R03 raw blobs、`diagnostics/T2.2-fixture-byte-manifest-v2.md`、`diagnostics/T2.2-fixture-admission-v2.md`、`diagnostics/T2.2-fixture-byte-review-v2.md`，共 31 路径；加上四份治理文件和自身任务卡后，完整 `read-path` 投影为 36 路径。R05 不读取 authorization、census/gap、selector/resolution、adapter、历史 packet/key/brief/answers/baseline、prior blocker、v1/v2/v3 架构或审查正文；attempt 中的固定身份只从固定任务合同或允许的上游证明传递。R05 不重读历史正文或材料准备过程。

全部 21 卡的业务读取投影审计如下；括号内为展开后的业务路径数，不含四份治理文件和自身任务卡：

| 卡 | 最小业务读取闭集 |
|---|---|
| R01（17） | M1 receipt、T1.8、GOLD 与 14 个固定 source groups |
| R02（20） | R01 三个 subjects，加 R01 的上述证据 |
| R03（21） | R01/R02 已发布 subjects/reviews、GOLD 与 14 source groups、条件式 authorization 控制文件 |
| R04（53） | R01—R03 已发布 subjects/reviews、GOLD 与 14 source groups、28 blobs |
| R05（31） | 28 blobs、byte manifest、admission、R04 byte review |
| R06（83） | R05 package direct subjects，以及完成端到端 package 独立复核所需的 R01—R04 已发布证明、28 blobs、M1/T1.8、GOLD 与 14 source groups |
| R07（6） | adapter、package manifest/review、full brief、control packets 01—02 |
| R08（7） | R07 call manifest 及 R07 的六项已发布输入 |
| R09（11） | control call/review、answers 01—04、T1.8、adapter、full brief、packets 01—02 |
| R10（8） | answers 01—04、control index、contrast key、control call/review |
| R11（9） | control result 作为 direct subject，加 R10 的八项复算证据 |
| R12（13） | adapter、package manifest/review、control result/postflight、full/variant briefs、packets 01—06 |
| R13（14） | diagnostic call manifest 作为 direct subject，加 R12 的十三项证据 |
| R14（22） | diagnostic call/review、answers 05—14、T1.8、adapter、full/variant briefs、packets 01—06 |
| R15（20） | control/diagnostic answers、control result/postflight、diagnostic call/review/index、contrast key |
| R16（21） | contrast result 作为 direct subject，加 R15 的二十项证据 |
| R17（20） | adapter、package manifest/review、contrast result/postflight、full brief、14 formal packets |
| R18（21） | retest call manifest 作为 direct subject，加 R17 的二十项证据 |
| R19（33） | retest call/review、14 formal answers、T1.8、adapter、full brief、14 formal packets |
| R20（19） | attempt manifest、scoring key、14 formal answers、formal index、retest call/review |
| R21（145） | baseline direct subject与完整 attempt 复算证据：固定 v1/v2/v3 身份、R01—R20 已发布产物、28 blobs、先前 blockers、T2.1/T2.3；明确排除 GOLD、examples、authorization 与 14 material slots |

读投影只给 R01/R02/R03/R04/R06 金标与十四份样张权限；R07—R21 不得继承金标、样张或 material slot 权限。reviewer 只读明确 direct subject 与完成独立复核所需的已发布证据；write owner 不因此自动成为其他角色的 read consumer。

fresh-judge-read-count: 5

R09/R14/R19 的控制会话读投影包含同卡 fresh judges 写出的答案，供主控冻结 index；它不扩大 fresh judge 的权限。验证器必须为每个独立 call 在任务卡同一读取章节机械锁定恰好五个 `fresh-judge-read-path`：`AGENTS.md`、冻结 T1.8、冻结 adapter、该 call 的一个 frozen brief、该 call 的一个 frozen packet。缺一项、多一项、重复、换成 call manifest/review/key/其他答案或把父控制会话权限继承给 judge，均禁止派发。

R03、R04、R05、R06 还必须在 `## 3. 允许读取清单` 各自逐行内嵌完整 material-slot-policy 投影：R03/R04/R06 为 `runtime-open: selected-only`，R05 为 `runtime-open: forbidden`。这十四行对 R05 只登记静态路径宇宙，不构成 `read-path` 或打开权限。十四个 slot 的缺失、重复、额外路径、范围、glob、前缀、大小写变化或章节错位都失败；R05 同节不得另行授权打开任一 slot、材料目录、glob 或全部材料。恢复 blocker 只允许使用已注册 ID 的 `taskcards/T2.2-RNN-BLOCKER.md`，精确为 `blocked/run-only`。

R01 精确产品请求 blocker 的最小机器格式为唯一 `blocker-type: product-request`，并对每个非空、唯一 request ID 逐行记录 `- product-request-id: <id>`。R03 resolution 对同一闭集逐行记录 `- product-request-resolution: <id> | status: resolved|rejected|unresolved`。只有两边 request ID 集严格相等、均无重复且全部为 `resolved` 时，R01 blocker 才在 M2 gate 判断中视为已关闭；文件永久保留且必须与实际 resolution 一同进入 attempt hash 链。R01 blocker 不存在是合法无产品请求路径。R01 其他类型、任一未关闭状态或 R02—R21 任一 blocker 都禁止 M2。

### Artifact 生命周期与直接审查

recovery-normal-markdown-output-count: 82

recovery-stateful-path-universe-count: 105

105 的静态路径宇宙由 `1` 份 v3 preflight review、`82` 份正常 Markdown 输出、`21` 份可能的逐卡 blocker 和 `1` 份 M2 receipt 构成。`validate.py` 的字面 artifact-policy map 对每个未来路径固定 owner、是否需要 header、status、scope、direct review、M2 关系与 attempt-local 关系。R01 的 adapter 为 `frozen/long-term`，census/gap 为 `frozen/run-only`；R02 分别写同 scope 的两份 review；R03 的 authorization/selector/resolution/admission/byte manifest 为 `frozen/run-only`；R04—R19 的 Markdown 输出均为 `frozen/run-only`；R20 baseline 与 R21 postflight 均为 `frozen/long-term`。28 个 blobs 和 14 个 raw slots 不带 Markdown header。

recovery-direct-review-count: 11

直接审查闭集恰为：

1. v3 preflight review → v3 architecture，`run-only`；
2. historical adapter review → adapter，`long-term`；
3. fixture census review → census + gap list，`run-only`；
4. fixture byte review → 按固定存在规则的 authorization + selector + resolution + admission + byte manifest + 28 blobs，`run-only`；
5. package preflight review → R05 的 attempt manifest + package 闭集 + package manifest，`run-only`；
6. control input review → control call manifest，`run-only`；
7. control postflight review → control results，`run-only`；
8. diagnostic input review → diagnostic call manifest，`run-only`；
9. contrast postflight review → contrast results，`run-only`；
10. retest input review → retest call manifest，`run-only`；
11. postflight review → v2 baseline，`long-term`。

每一行都要求 review scope 等于 subject scope。R02 的 mixed scope 必须拆成两份 review；R21 与 baseline 都必须是 long-term；除此闭集外不得临时增加 direct reviewer。

### 14 个材料 slot 与 selector

recovery-material-slot-count: 14

材料最大允许宇宙是以下静态字面路径，不表示全部必需：

```text
materials/T2.2-v2/source-01-full.md
materials/T2.2-v2/source-02-full.md
materials/T2.2-v2/source-03-full.md
materials/T2.2-v2/source-04-full.md
materials/T2.2-v2/source-05-full.md
materials/T2.2-v2/source-06-full.md
materials/T2.2-v2/source-07-full.md
materials/T2.2-v2/source-08-full.md
materials/T2.2-v2/source-09-full.md
materials/T2.2-v2/source-10-full.md
materials/T2.2-v2/source-11-full.md
materials/T2.2-v2/source-12-full.md
materials/T2.2-v2/source-13-full.md
materials/T2.2-v2/source-14-full.md
```

唯一 selector 是 `diagnostics/T2.2-material-gap-manifest-v2.md`。它必须逐行记录固定 `slot-set-id: T2.2-V2-SOURCE-SLOTS-01-14`、十四行 `slot-member`、`selected-slot-count`、选中行 `selected-slot: <literal> | source-group: <id> | request-id: <id>`、未选中行 `unselected-slot: <literal>`、`selection-reason` 与 `selector-result: NO_SLOTS|SLOTS_REQUIRED|BLOCKED`。selector 不存在时，对十四个 raw slot 的恢复专用检查为零 filesystem 操作；存在时只允许对 selected 字面成员执行 `lstat/open/hash`。selected/unselected 必须是不相交补集；selected 缺失只报告该字面路径；unselected 不得被探测、列目录、读取或 hash。`materials/T2.2-v2/authorization.md` 是固定 control file，不是 raw slot。所有通用树扫描必须在该 raw 目录入口剪枝。

### 28 个 raw blobs

recovery-raw-blob-count: 28

R03 达到 byte gate 时只能原子发布下列 regular、非 symlink、无 Markdown header 的字面闭集，不接受部分集合或第 29 个 `.bin`：

```text
diagnostics/T2.2-fixture-bytes-v2/candidate-01.bin
diagnostics/T2.2-fixture-bytes-v2/context-01.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-02.bin
diagnostics/T2.2-fixture-bytes-v2/context-02.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-03.bin
diagnostics/T2.2-fixture-bytes-v2/context-03.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-04.bin
diagnostics/T2.2-fixture-bytes-v2/context-04.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-05.bin
diagnostics/T2.2-fixture-bytes-v2/context-05.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-06.bin
diagnostics/T2.2-fixture-bytes-v2/context-06.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-07.bin
diagnostics/T2.2-fixture-bytes-v2/context-07.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-08.bin
diagnostics/T2.2-fixture-bytes-v2/context-08.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-09.bin
diagnostics/T2.2-fixture-bytes-v2/context-09.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-10.bin
diagnostics/T2.2-fixture-bytes-v2/context-10.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-11.bin
diagnostics/T2.2-fixture-bytes-v2/context-11.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-12.bin
diagnostics/T2.2-fixture-bytes-v2/context-12.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-13.bin
diagnostics/T2.2-fixture-bytes-v2/context-13.bin
diagnostics/T2.2-fixture-bytes-v2/candidate-14.bin
diagnostics/T2.2-fixture-bytes-v2/context-14.bin
```

这些 bytes 的唯一 writer 是 R03，并必须与 byte manifest、owner、R03/R04/R05/R06 的 copy/review 责任一致。

### M2 完整 hash 链的机器投影

以下行格式只把 v3 已冻结的 path/hash/commit/length 责任编译成确定性输入，不新增产品判词或恢复路线：

- 每个消费者对其冻结直接输入逐行记录 ``- input-binding: `<literal-path>` | byte-length: <base-10> | sha256: <64-lowercase-hex>``；验证器对每个消费节点执行闭集相等、实际长度和实际 hash 检查，不接受 future hash、自引用、漏项或额外输入。
- 每份 direct review 记录唯一 `review-result: PASS`、`subjects-unchanged-since-commit: yes`，并对全部 subject 逐行记录 ``- subject-binding: `<literal-path>` | owner-task: <T2.2-RNN> | commit: <40-lowercase-hex> | sha256: <64-lowercase-hex>``。验证器同时核对当前 bytes、subject commit blob 与 HEAD 祖先关系。
- byte manifest 对 01—14 每组各有一行 `candidate-byte-proof` 和 `context-byte-proof`，固定 selected candidate ID、verdict scope、source path/hash、半开 range 或 ordered spans、fragment/span hash、blob path/length/hash、尾随 LF、raw-slot foreign key、context extraction evidence 与 `copy-ready: yes`。验证器从 source raw bytes 重建 28 个非空 strict UTF-8 blobs；若 selector 为某组选择了 material slot，该组 source 必须是同编号 selected slot，不能回退 example source。
- attempt manifest 以十四行 `qualification-item` 把 byte manifest candidate ID、Q ID、candidate/context blob 与 formal packet 一一连接，以两行 `sentinel` 固定 P/N1 source group，以十四行 `m14-call` 固定 C4/B4/E4/G2 的 packet/brief/object-order，以 `attempt-salt-hex` 固定 32-byte salt，以 `fixed-identity` 固定 v3/v2/v1 历史身份，并以 `future-path` 逐项登记全部未来 package/call/baseline/postflight/M2 字面路径。attempt 不写自身 hash 或未来文件 hash。
- package manifest 对 package 闭集逐行记录 `package-binding`，对每个非空 byte block 记录 `payload-copy-proof` 的 input/embedded length/hash 与 `copy-equality: PASS`；E 臂空 context 只允许以 `payload-omission-proof` 绑定 canonical context hash。验证器按第 9 节 length-driven grammar 重新解析实际 packet bytes，并核对 blind/formal/contrast 与 attempt mapping。

M2 receipt 出现时，验证器必须沿 `source → blobs → byte manifest/review → attempt → package/review → 三段 call/input-review → answers/index/results/reviews → baseline/postflight → receipt` 重算整条链。修改任一中间文件后，只更新 baseline 或 receipt 不得掩盖失配。`selector-result: BLOCKED`、selector 缺失或非法、任一 direct review 非 PASS、control result 非 PASS、baseline 非 PASS、R01 product-request blocker 未按本节精确关闭、R02—R21 任一 blocker、路径越界、symlink 或非 regular file 都禁止 M2。

### M2 active/history 精确 schema

活动资格候选固定为 v2 attempt；v1 baseline/blocker 是固定 `FAIL` 历史，v2 architecture/review 是固定失败架构历史。M1 receipt、T1.8、T2.1 与 T2.3 继续承担原有 gate 身份。没有 `diagnostics/M2-gate-receipt.md` 时，未来 active 文件均不因此被要求存在，阶段 3 仍被硬阻塞；receipt 一旦存在，验证器必须重算所有实际 hash、结果、路径与历史身份，禁止别名、版本扫描、路径回退或软链接替代。

未来 M2 receipt 的 T2.2 机器字段必须恰好一次，并与下列 schema 一致：

```text
m1-freeze-receipt-sha256: <actual hash>
t1.8-independent-acceptance-sha256: <actual hash>
t2.1-r01-r08-sha256: <actual hash>
t2.3-seed-lenses-v2-sha256: <actual hash>
t2.2-active-architecture-path: diagnostics/T2.2-recovery-architecture-v3.md
t2.2-active-architecture-sha256: 38025c0b2ebb26171e7f6ad8bef69b97bfeb2d88597a78e67b3dcdc48110d1e1
t2.2-active-architecture-review-path: diagnostics/T2.2-recovery-architecture-v3-preflight-review.md
t2.2-active-architecture-review-sha256: e5d450f019685fba6eed679e06ccedee10255591e9a4a65359ac6cfb918e06ec
t2.2-active-attempt-id: T2.2-QV2-A01
t2.2-active-attempt-manifest-path: diagnostics/T2.2-qualification-attempt-manifest-v2.md
t2.2-active-attempt-manifest-sha256: <actual hash>
t2.2-active-baseline-path: diagnostics/T2.2-judge-baseline-v2.md
t2.2-active-baseline-sha256: <actual hash>
t2.2-active-postflight-review-path: diagnostics/T2.2-postflight-review-v2.md
t2.2-active-postflight-review-sha256: <actual hash>
t2.2-active-result: PASS
t2.2-history-v1-baseline-path: diagnostics/T2.2-judge-baseline.md
t2.2-history-v1-baseline-sha256: 830f0758439ee72d549efe27296a444ccb9769c92c1298399dd9b5bebce0d4af
t2.2-history-v1-baseline-result: FAIL
t2.2-history-v1-blocker-path: taskcards/T2.2-BLOCKER.md
t2.2-history-v1-blocker-sha256: 84c7a0dede0797c5667228398cc4be1b8a945d8a871dab7058737778bba1684b
t2.2-history-v2-architecture-path: diagnostics/T2.2-recovery-architecture-v2.md
t2.2-history-v2-architecture-sha256: 1154110c3a3bff65e4dc2ceb8244e724f0da60924c4e32ba4afa413600a2043a
t2.2-history-v2-review-path: diagnostics/T2.2-recovery-architecture-v2-preflight-review.md
t2.2-history-v2-review-sha256: 9d2c80e23e30018c4dc4283c56315ab2df2198344b98dda91cebae6755f92e13
t2.2-history-v2-review-result: FAIL
```

以上代码块与 v3 §13.2 相同，恰为 26 个字段；缺字段、重复字段或任意额外字段都禁止 M2 receipt。架构、审查和质量复核的 commit 身份仍由 C0 固定前置检查负责，不写入 receipt 私有字段。

v2 baseline 必须机器记录唯一 `qualification-result: PASS`；R21 postflight 必须按上一节 direct-review 格式记录唯一 `review-result: PASS`、`subjects-unchanged-since-commit: yes` 和 R20 baseline 的精确 subject-binding。缺一项、hash 改变、R01 product-request blocker 未精确关闭、R02—R21 任一 blocker、21 卡未完整注册或 28 blobs 未完整发布，都禁止 M2 receipt。

## 三个痛点的针对性设计

### 低质量复述：知识卡承重主张制

每张知识卡先写一句最小承重主张，并归类为机制、模型、方法、预测、权衡、可迁移关系、高手指点或跨行业视角之一，不得写“点评”。

缩句差分探针（R01–R08）拦截原文直述、后文透支、明显推论和术语换名；它不得把上述八类合法增量收窄为只有“新机制／新关系”。探针只是诊断与预筛，不替代删除测试、整体判断或产品判词。删除测试仍要求回答：删掉这条，读者会失去哪个具体判断能力；答不出时，该候选不得扩写并从候选中剔除。独立审核此时尚未开始，不能提前把候选写成“淘汰”终局。

专家合同的正向基准是紧扣原文承诺推出原文未明说但必需的内容，或把人物、书与概念组织成改变理解的一条解释线。每个锚点先廉价生成 N 条一句话候选，经探针、删除测试与去重筛选后，幸存者才扩写成完整知识卡；候选数量是当前任务冻结的参数。

### 呈现质量：Writer 单焦点合同

Writer 只接收锁定卡。一张卡只交付一条定稿标题和一份定稿正文，二者只能统一同一焦点、同一解释线的表达，不得拼贴多主题或添加事实、主张；表达仍以两篇正例样张的成段讲课体为阶段性基准，不堆字段。实际读取样张仍须由当前任务逐文件授权，该阶段基准不是长期产品 gate。同时原样携带来源锚点／位置关系绑定、`knowledge-card-id` 与 producer lineage，Writer 不选择插入位置。T1.7 只消费这一绑定，把定稿标题与正文按 `> [!note] AI 陪读｜标题` 的 Obsidian callout 就近组装到原文，不得补造标题、正文或锚点。`tandem-comments` 的精确锚点字段为 `unknown`，在得到真实样例前不得猜测或冻结。呈现质量独立于内容增量验收。

### 裁判无能：先考试、后上岗

生产前，裁判按 T1.8 合同盲测固定案例，做绝对判断；当前路线参数是拦住全部 8 个反例、放行全部 3 个正例，参考件可判边缘。不及格则修订裁判合同并复考，记录模型、合同版本和成绩。裁判校准通过是阶段 3 的前置；生产端不读取金标目录。

资格考试只使用冻结 T1.8 合同与 blind packet，不输入 T2.1。资格通过后，裁判才可把缩句差分、删除测试和重复检测作为诊断工具，再对幸存者做五项定性绝对判断。固定案例可能过拟合；T4.1 用产品判词回填扩充考卷。产品判词永远是最终 gate，裁判只是预筛。

## 专家、透镜与持续改进

透镜是一套可检查的思维程序，必须有适用触发器、强制提问序列、输出类型限定和懒惰应用反例。种子透镜只从三个正例的逆向工程和本轮阶段候选起点编译：激励、演化选择、系统反馈、生产力史观、博弈论。该候选起点不是永久透镜清单；真实缺口可由临时专家按同一格式即席编译。透镜是问题而非答案；临时专家的检索上限受执行模型知识约束。

正式透镜是战绩缓存而不是能力边界。每轮产品判词按透镜归账，系统可提出升降、调整或退役建议，但不得自动覆盖、删除、降级或退役。每个版本保留使用结果、合格／质疑／失败及原因；人工定期复盘才可作出决定。日常技术冻结不得转嫁为产品负责人审批，只有产品事实变化才修改 `PRODUCT-DECISIONS.md`。

产品负责人无需预设洞见内容：透镜是问题而非答案，内容层面的未知来自已知框架与未知材料的结合；框架层面的未知由临时专家检索“哪个学科会把这段当教科书案例”。这不保证超出执行模型知识，只追求超过文本与读者已有认知。

裁判的持续改进依赖分歧挖掘：裁判先对真实运行陪读冻结逐条预测，后收产品判词；“裁判放行而产品废弃”与“裁判拦截而产品惊艳”的分歧加入新考题。四级判词为惊艳／有用／平庸／废弃；平庸和废弃附死因，有用可补“差哪一步到惊艳”。收敛不预设数量，而看新章节上的分歧率趋势。

已揭晓失败案例只可用于透镜与探针调试，不构成资格；真正的资格检验在未知章节由产品判词给出。

## 任务分解

历史 T2.2 原始资格考试已按隔离复合任务完成并失败；恢复链仅 R09、R14、R19 为复合任务，其余任务保持单会话粒度，并分别报告 `implemented`、`integrated`、`verified`、`accepted`。

### 阶段 0：开发基座

- **T0.1 目录骨架、边界附则与任务卡落库**：建立 `contracts/`、`runs/`、`materials/`、`tools/`、`diagnostics/`、`lenses/` 与 `taskcards/`；补充读取隔离；把本方案纳管为本路线图；为全部任务写卡；扩展验证器。
- **T0.2 轻量运行脚本 `tools/run.py`**：实现 `new`、`freeze`、`check` 三个子命令，负责 run、身份哈希、冻结清单、preflight／postflight 与状态头检查；纯标准库、单文件。
- **T0.3 任务卡模板与术语表**：建立任务卡模板和术语表，统一知识卡、承重主张、锚点、终局四态与八类增量等词汇。

### 阶段 1：图书线节点合同

- **T1.1 材料进入与范围冻结合同**：来源确认、版权／授权、本次范围与材料哈希；无法确认即硬阻塞。
- **T1.2 B1 原文合同**：只承接同一已准入且可信的图书材料身份与冻结 scope，按作者结构呈现一手正文，禁止 Skills 材料、替换正文或总结替代；定义章节命名与段落锚点约定，锚点细节为 `unknown`。
- **T1.3 发现合同**：从 B1 产出透视需求的最小结构（位置锚点、为何停下、期望增量类型），“为何停下”必须承载一个清楚、单一、值得深入的问题；每次强制完成一次受控偶遇探索，探索后允许零发现，禁止凑数。
- **T1.4 专家与知识卡合同**：承接三字段透视需求，先按正式透镜优先／真实缺口才创建临时专家完成路由并建立稳定 `producer kind/id/version`，再让两类 producer 进入同一探索合同；候选主张经诊断筛选后扩写，且候选与知识卡持续绑定原需求；知识卡最小字段为稳定 `knowledge-card-id`、承重主张、增量类型、来源锚点、失效边界、证据状态，以及稳定 producer lineage。
- **T1.5 独立审核合同**：七项知识卡责任完整才可开始审核；审核价值、事实、重复、边界，终局四态为锁定／淘汰／退回／待补证据；locked 集逐字复制整张原卡及 lineage，淘汰项不得被 Writer 捞回。
- **T1.6 Writer 合同（历史 M1 冻结接口）**：该合同的字节与 M1 收据保留为历史证据，不原位改写；其“仅输入锁定卡、每卡一稿、单焦点单解释线”不再是当前人工正例流程入口。Writer 的稳定编辑责任由 `PRODUCT-DECISIONS.md` 拥有，未来实现必须另建版本化合同，不能把历史冻结身份伪装成现行接口。
- **T1.7 B2 组装合同**：只消费 Writer 定稿及原样绑定并就近组装 callout，不补造标题、正文或锚点；逐条有稳定 `b2-item-id`，并绑定 `knowledge-card-id`／producer；有惊艳／有用／平庸／废弃价值标签位，数量和长度不设配额。
- **T1.8 独立验收合同**：每个实际验收对象与一个既有冻结 B2 单元一一对应，execution／semantic／product 共用其 `b2-item-id`、冻结生产产物可信身份及内容 hash、固定 scope；五项语义标准与三层报告不预设阈值，产品判词记录的长期通用路径、schema 和编码保持 `unknown`。
- **T1.9 种子透镜编译**：逆向工程三个正例与经典框架，编译 4–6 个包含四件套的种子透镜；仅透镜开发期可读取金标。

### 阶段 2：裁判先行校准

- **T2.1 缩句差分诊断探针**：将 R01–R08 写成 `diagnostics/` 方法卡和操作步骤，供生产自检及资格通过后的裁判诊断使用；它不是资格考试输入或产品 gate。
- **T2.2 裁判资格考试（历史已完成／失败）**：原始隔离复合任务已写 frozen blind packet、scoring key、judge brief、answers、draft baseline 与 blocker，资格结果固定为 `FAIL`。这些 v1 字节永久保留为历史，不能原位改写或作为 active 通过证据。恢复控制面以本路线的 v3 恢复闭集另行推进；当前仍为 A1，C0 修复等待总控与独立后置审查，不授权 21 卡注册、R01、材料、模型调用、M2 receipt 或恢复执行。
- **T2.3 种子透镜试射（诊断）**：读取 T1.9 v1，在已揭晓失败章节试射并创建精确 v2 路径，避免已否决复述模式；旧版保留，失败回填为新版本的懒惰反例；不读取 T2.1，不作资格证明。
- **T2.4 首次 Idea 对照实验（已完成、整包不通过）**：冻结产物、匿名判词、配置揭示和终局报告由任务卡与对应 run 保留；一次性参数已经失效。
- **T2.5 Expert 工作合同知识课 Demo 实验（已完成、整包不通过）**：四份隔离 Demo 收敛为同一类局部论证分析；冻结产物、匿名判词、配置揭示和终局报告由任务卡与对应 run 保留，一次性参数已经失效。
- **T2.6 学科专长最小激活实验（已完成、整包不通过）**：学科知识被激活，但三份内容都没有教出可由读者重建的完整概念框架；判词和诊断由任务卡及 run 保留，参数已失效。
- **T2.7 有边界知识框架 Prompt 对照实验（`COMPLETE`）**：三份输出具有条理，但产品负责人无法确认它们是既存理论／框架还是针对原文现场生成的议论文结构，并认为篇幅过长；整包不通过，v2 参数已经失效。
- **T2.8 既存知识对象核心卡实验（`COMPLETE`）**：三个对象的核心卡形态获准进入下一步；来源身份未核验，因此该接受不等于事实接受，一次性参数已经失效。
- **T2.9 伯格原理论考点式讲义单样张（`COMPLETE`，`v03`）**：来源核验、七点结构和分层表达已冻结；产品负责人认为内容基本合格，并授权进入原文融合。
- **T2.10 伯格知识讲义原文融合单样张（`COMPLETE`，`v02`）**：完整原文与单锚点连续讲义已组合为 Obsidian 单文件 Markdown并获产品接受；v01 HTML 只保留为设计试验。本任务参数失效，后续对象与自动化须重新建卡。
- **T2.11 两个非伯格知识对象考点式讲义平行样张（`COMPLETE`，`v01`）**：宗派化与诺斯意识形态—执行成本机制的轻量来源核验和人工讲义已冻结；产品负责人分别确认信息足够并准许进入原文融合。该判词不把讲义认定为原著逐字摘录，也不证明融合体验或日常生产资格。
- **T2.12 两个非伯格知识对象原文融合迁移实验（`READY`，`v01`）**：只读取同一完整原文章节、两份已接受讲义和判词，分别寻找实质锚点并统一生成 Obsidian 阅读页；不重做来源研究、不改承重语义、不新增专属 schema／validator，以任务卡冻结的墙钟预算区分必要融合与流程浪费，停在产品阅读判词。

### 阶段 3：首次真实运行（《今日简史》新章节）

- **T3.1 材料授权与冻结**：派发前产品负责人把获授权输入置于 `materials/T3.1/source.epub`（不纳入提交），确认来源与范围并选择未被历史判词覆盖的章节；技术侧写 `materials/T3.1/authorization.md` 与 `runs/T3.1/freeze-receipt.md`。
- **T3.2 B1 生产**：在 `runs/T3.1/raw/b1.md` 呈现该章节原文，并写 `runs/T3.1/raw/T3.2-postflight.md`。
- **T3.3 发现到知识卡**：先核验 M2→M1 链中 T1.2／T1.3／T1.4、T2.1 与 v2 的 hash，再读取对应冻结正文；随后在 `runs/T3.1/raw/knowledge-cards.md` 产卡、以 `runs/T3.1/raw/knowledge-card-self-check.md` 自检，卡携带稳定 `knowledge-card-id` 与 producer lineage。
- **T3.4 独立审核**：写 `runs/T3.1/raw/review-outcomes.md`，将锁定卡隔离到 `runs/T3.1/locked/knowledge-cards.md`。
- **T3.5 Writer 到 B2 组装（历史条件式设计）**：原 T1.6／T1.7 接口只随历史路线保留，不是当前执行许可。若未来重启阶段 3，必须依据 `PRODUCT-DECISIONS.md` 的稳定编辑责任重建版本化 Writer 与只装配不改文接口，再冻结新的路径和 lineage；不得直接消费历史合同。
- **T3.6 冻结、独立验收与产品判词**：无有效 M2 receipt 立即硬阻塞。先按 M2→M1 链核验冻结 T1.8、T2.1，并只从 receipt 的字面 active 字段核验 `diagnostics/T2.2-judge-baseline-v2.md` 与 `diagnostics/T2.2-postflight-review-v2.md` 的实际 hash 和 `PASS`；v1 baseline/blocker 只核验为固定 `FAIL` 历史，不得回退为 active。随后才读取对应正文。派生执行时序固定为 `runs/T3.1/freeze-receipt.md` → 写入并绑定它的 `runs/T3.1/final/freeze-receipt.md` → production freeze → 以既有冻结 B2 单元为一一验收对象，并让 judge predictions／acceptance report 共用其 `b2-item-id`、冻结生产产物可信身份及内容 hash、固定 scope → acceptance freeze → M3 → 产品负责人四级判词与 `runs/T3.1/acceptance/product-verdicts.md`。该 run-specific 记录绑定同一固定对象身份，不得写回生产 B2 的 `unknown` 标签位；其路径不外推为长期通用路径，长期 schema 与编码仍保持 `unknown`。这是 80 分交付验收点。

### 阶段 4：复盘与最小治理件

- **T4.1 判词回填与分歧挖掘**：按对象、scope、判断权威和哈希写 `runs/T3.1/acceptance/gold-candidates.md`，只作候选而不修改金标 owner；将分歧加入考卷，利用 `b2-item-id`、knowledge-card 与 producer lineage 按透镜／专家归账。无有效 M2 receipt 立即硬阻塞；构建 ledger 前按 M2→M1 链核验 T1.8、v1 lens、v2 lens，并只从 receipt 的字面 active 字段核验 `diagnostics/T2.2-judge-baseline-v2.md` 与 `diagnostics/T2.2-postflight-review-v2.md` 的实际 hash 和 `PASS`；v1 T2.2 baseline/blocker 只作固定 `FAIL` 历史。ledger 为每个 lens 逐字列出未来 registry 相对路径、source lens 相对路径及可信 source lens SHA-256。主控技术核验后冻结 ledger，并写 `diagnostics/T4.1-freeze-receipt.md` 绑定 ledger hash。
- **T4.2 透镜登记册最小实现**：读取冻结 ledger 与 receipt，只写唯一根 `lenses/registry/index.md` 及 ledger 逐字枚举的版本文件；创建前逐项核对 source lens 相对路径和 SHA-256。禁止 glob 推断、额外文件或原位覆盖。记录结果与合格／质疑／失败原因，只提出建议。
- **T4.3 复盘决定下一轮**：选择继续本书、换新书或启动 Skills 线复用骨架。

## 里程碑、波次与卡壳协议

- **M1 基座与合同组装**：阶段 0、1 提交后，核验术语、合同衔接和决议一致性。通过时主控仅冻结语义未变的 `contracts/GLOSSARY.md`、T1 合同与种子透镜，写 `contracts/M1-freeze-receipt.md` 并逐文件记录 `contracts/GLOSSARY.md`、所有 T1 合同及 T1.9 v1 的 SHA-256，然后独立提交；需语义改动先返工。无 receipt 不得进阶段 2。
- **M2 裁判上岗**：当前未建立。只有 21 卡原子注册、完整恢复 DAG、v2 active baseline `PASS`、R21 postflight `PASS`、R01 product-request blocker 不存在或已被 R03 逐 request-id 精确关闭、R02—R21 blocker 均不存在且现行验证器通过后，总控才能在新的明确授权下按 v3 §13.2 的 26 字段精确 schema 写 `diagnostics/M2-gate-receipt.md`。receipt 绑定 M1、T1.8、T2.1、T2.3、v3 architecture/review、v2 active attempt/baseline/postflight 及 v1/v2 固定失败历史；架构/review/quality audit 的 commit 身份继续由 C0 前置检查，不扩写 receipt。无 receipt 不得进阶段 3。
- **M3 首次真实运行冻结**：T3.6 报告后、产品判词前，核验 execution／semantic；随后产品负责人判词。
- **M4 复盘**：T4.1 receipt 冻结 ledger 后，核验 registry 与回填，并与产品负责人决定下一轮。

波次依次为：T0.1；T0.2→T0.3；T1.1—T1.8 并行，随后 T1.9（在 T1.4 后）→M1；T2.1、历史 T2.2 `FAIL` 与 T2.3 后停在 M2 前；v3 A1 → C0/A2 → 总控另行决定是否原子注册 21 卡/A3 → R01 至 R21 严格按 DAG → 总控另行创建 M2 receipt/A12；其后才允许 T3.1→T3.6 严格串行，其中 T3.6 从 T3.1 根 receipt 开始，依次写 final receipt、冻结 production、写预测和报告、冻结 acceptance、通过 M3，再收产品判词；T4.1→冻结 ledger receipt→T4.2→T4.3，由产品负责人与主控共同完成后 M4。

默认只允许读取 `AGENTS.md`、`PRODUCT-DECISIONS.md`、`ENGINEERING-LESSONS.md`、涉及流程或任务卡时的 `blueprints/PIPELINE-MAP.md`、本路线图和自己的任务卡；`GOLD-STANDARDS.md`、`examples/`、合同、receipt、run 与其他交付物都必须由当前任务卡逐文件列出。金标与样张的读取例外不得跨任务继承；生产任务永远不得获得该例外。

如果发现决议冲突、信息缺失、需要产品判断或合同打架，唯一合法动作是立即停止，在对应 `taskcards/T-X-Y-BLOCKER.md` 写明问题与 `unknown`，然后结束会话；不得自行取舍或先做后报。

## 关键决定与理由

- **正例坐标先于裁判恢复**：当前裁判尚不能可靠判断 Expert、Writer 与最终产品质量；先由产品负责人建立分层正例坐标，再讨论 Judge 校准和上岗，历史 T2.2 恢复设计不构成当前执行许可。
- **质量关卡先于 Writer**：当前人工正例流程先判断自然可读 Idea，再判断同一 Expert 的完整专家稿；知识卡只可作为内部审计投影，不能重新成为现行产品价值关口。Writer 不能挽救浅稿。
- **骨架刻意做薄**：身份哈希、目录隔离与冻结清单覆盖防覆盖、防混读和防伪 lineage 的核心收益；不让状态机和依赖反噬生成质量。
- **阈值一律后置**：先用五项标准的定性绝对判断跑通首轮，等真实判词积累后再讨论数值阈值，避免复活旧实验参数。

## Unknown

- `tandem-comments` 的实际批注锚点格式；需真实使用样例。
- 《今日简史》EPUB 文件和具体章节；由 T3.1 授权并冻结。
- 执行 Agent 的模型代号；每任务冻结实际可用型号。
- B3 读薄；待 B2 通过验收后另开，Skills 线同理。
