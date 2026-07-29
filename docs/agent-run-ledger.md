# ReaderLab Agent 运行账本

### Run: 2026-07-25 - governance-closeout

- Task / Type / Tool：治理一致性收口 / verification / active tests + independent re-audit
- Context source / Boundary：`/private/tmp/readerlab-audit-handoff-2026-07-25.md`；不修改 T2.35
  任务卡或 run，不启动 Writer。
- Files read / changed：治理文档、任务卡模板与 active tests；完整清单见本轮 Git diff。
- Commands / checks：`python3 -B tests/entry.py`、全部当前 run 的 `tools/run.py check`、
  `git diff --check`、冻结身份 SHA-256。
- Artifacts / reports：`audit/FINDINGS-REGISTER.md`、`audit/INCIDENT-GUARDRAILS.md`、
  `CURRENT-STATE.md` 的迁移前快照内容由 Git diff 保留。
- Result / Evidence type：独立全新上下文最终 `GREEN`；Standards／Spec 均 `PASS`。
- Canonical status：`historical`
- Failures / detours：首次复核发现 blocker 权限只有文字约束；后续 adversarial 复核继续发现
  重复字段、路径穿越、symlink、blocker 归属与下一授权生命周期等 fail-open 边界，均在
  active tests 中收口。
- Repeat-error check：状态 owner 过期属于 AUD-001 已记录问题；当前机制已补，等待下一次真实
  状态变化验证持续性。
- Reusable lesson / rule candidate：治理字段必须由真实入口 fail closed；测试内部自测正则不能
  代替解析真实当前对象。
- Follow-up：下一次真实业务状态变化后复核 AUD-001；审计节奏见
  `audit/AUDIT-OPERATING-MODEL.md`。

### Run: 2026-07-25 - mem-initialization

- Task / Type / Tool：标准 MEM 初始化与自定义状态 owner 迁移 / cleanup / mem-init + mem-clean
- Context source / Boundary：产品负责人明确批准；不修改 T2.35、当前 run、冻结合同或产品事实。
- Files read / changed：五个固定 MEM 层、兼容入口、当前控制面引用与 active tests。
- Commands / checks：`python3 -B tests/entry.py`、全部当前 run check、`git diff --check`、关键
  冻结身份 SHA-256。
- Artifacts / reports：`docs/current-task.md`、`docs/dev-state.md`、`docs/decisions.md`、
  `docs/agent-run-ledger.md`、`docs/research-log.md`。
- Result / Evidence type：标准 MEM 五层已建立并完成 owner 迁移；active tests 35/35、当前 run
  11/11、`git diff --check` 与 T2.35／GLOSSARY／v2／receipt 冻结身份全部通过。
- Canonical status：`canonical`
- Failures / detours：无。
- Repeat-error check：通过迁移而非平行复制，避免再次形成两个动态状态 owner。
- Reusable lesson / rule candidate：该规则已经由 MEM Skill contract 覆盖，不重复提升到全局
  错误簿。
- Follow-up：完成验证后从 `docs/current-task.md` 和 `docs/dev-state.md` 冷启动下一会话。

### Run: 2026-07-25 - git-evidence-closeout

- Task / Type / Tool：T2.35 Git 证据边界与治理提交收口 / implementation / implement + mem-save
- Context source / Boundary：产品负责人批准本地收口；不上传 GitHub、不启动 Writer、不修改
  旧 T1.6、不把完整审阅包加入 Git。
- Files read / changed：`.gitignore`、active tests、T2.35 小型控制证据、治理投影与固定 MEM
  层；T2.35 完整语义 payload 保持本地 ignored。
- Commits：Git policy `3748b1dc829055ca757e11b4f948283f4ad6c88c`；T2.35 evidence
  `bcb052e4dcaeac53a273a36608a632b98a98d94b`。
- Commands / checks：`python3 -B tests/entry.py`、全部当前 run check、Git ignored inventory、
  `git diff --check` 与 T2.35／GLOSSARY／v2／receipt／两个 freeze 身份复核。
- Result / Evidence type：active tests 36/36、当前 run 11/11、diff 与冻结身份全部通过；完整
  审阅包、Expert 和知识卡确认 ignored，run 内无 `.DS_Store`；`READY_FOR_REAUDIT`。
- Canonical status：`canonical`
- Failures / detours：首次直接模块名运行专项 unittest 因 `tests` 不是 package 而失败；改用
  discover 后 12/12 PASS，不涉及实现失败。
- Repeat-error check：按文件名放行会随审阅包语义变化复发；已改为默认忽略并由自动测试锁定。
- Reusable lesson / rule candidate：D-MEM-002；云端审核逐任务显式授权，不建立主仓库永久例外。
- Follow-up：全新上下文复核三笔提交、忽略边界、当前 run 与 MEM 一致性；复核前保持 Writer
  未授权。

### Run: 2026-07-25 - book-line-realignment-memory-closeout

- Task / Type / Tool：图书线第一性原理复盘、owner 归位与下一会话交接 / cleanup /
  mem-save + mem-clean + handoff
- Context source / Boundary：产品负责人的长轮次产品与工程复盘；只维护产品／工程 owner、固定 MEM
  层和仓库外 handoff，不修改 T2.35 taskcard、run、合同、Writer 指南或生产证据，不启动实验。
- Files read / changed：`PRODUCT-DECISIONS.md`、`ENGINEERING-LESSONS.md`、
  `blueprints/PIPELINE-MAP.md`、`docs/current-task.md`、`docs/dev-state.md`、
  `docs/decisions.md`、本账本；仓库外两个 handoff／执行设计文件。
- Commands / checks：`git diff --check`、`python3 -B tests/entry.py`、11 个当前 run 的
  `python3 -B tools/run.py check <run-path>`。
- Artifacts / reports：`/private/tmp/readerlab-book-line-handoff-20260725.md`、
  `/private/tmp/readerlab-next-session-execution-design-20260725.md`。
- Result / Evidence type：产品对象、成熟外部知识边界、分级核验、自动 Judge 暂缓、C4／Discovery
  边界、候选期成本结构和 Writer A/B 未知项已归回各自 owner；active tests 36/36、当前 run
  11/11、diff check 全部 PASS。诊断方案已认可但未派发，生产授权仍为 `none`。
- Canonical status：`canonical`
- Failures / detours：首次把 `docs/current-task.md` 的 `current-task` 写成自由标签，active tests
  将其按任务卡路径解析并出现 1 ERROR／1 FAIL；随后保留 T2.35 为最后一个正式任务对象，以独立
  诊断字段记录已批准未派发状态，复验通过。没有为交接伪造新 taskcard。
- Repeat-error check：再次确认 handoff 不能成为产品或当前状态的平行 owner；当前事实只引用
  `PRODUCT-DECISIONS.md`、`ENGINEERING-LESSONS.md` 与固定 MEM 层。
- Reusable lesson / rule candidate：`docs/current-task.md` 的控制字段是可执行协议，不是自由
  文案；新会话准备状态应使用已有字段语义或独立非生产字段，不能破坏任务卡／run／判词的 fail-closed
  关系。
- Follow-up：产品负责人手动把最终 handoff 交给干净总控；总控只运行仓库外 Discovery Lab 与
  Writer Lab，完成后停止并等待产品盲审或新授权。

### Run: 2026-07-26 - discovery-treatment-isolation-and-controller-correction

- Task / Type / Tool：Writer 收敛、Discovery treatment-isolation、独立审计与总控纠偏 /
  diagnostic + cleanup / 真实模型运行 + GPT Pro 独立审计 + mem-clean + handoff
- Context source / Boundary：产品负责人批准两条仓库外 sidecar 验证线；随后明确把 Discovery
  第一目标收缩为 18 次真实 Scout，只允许输入不一致、输出合同不一致或结果无法保存阻塞。
  不改变生产任务、生产合同或 promotion；Writer 线在产品 `PASS` 后停止。
- Files read / changed：本轮正式维护 `AGENTS.md`、`docs/current-task.md`、
  `docs/dev-state.md`、`docs/decisions.md` 与本账本；语义产物、运行证据、独立审核包和最终
  handoff 均在仓库外。
- Commands / checks：三份冻结材料 × V0／V1′ × 三次重复共 18 次真实 Scout；18/18
  parse/save、9/9 paired input／`seed_batch` 合同核对；GPT Pro 两阶段独立审计；阶段收尾
  执行 active tests、当前 run check、`git diff --check` 与 MEM owner 去重检查。
- Artifacts / reports：
  `/private/tmp/readerlab-new-route-20260726/discovery-isolation/checkpoint-b/`、
  `/Users/tianqiang/Downloads/ReaderLab_Discovery_Execution_Controller_Independent_Audit_20260726.md`、
  `/private/tmp/ReaderLab_Discovery_Execution_Controller_Audit_20260726.zip`、
  `/private/tmp/readerlab-new-route-20260726/writer-assembly/review/P3-product-review-candidate.md`。
- Result / Evidence type：Writer 修订稿获产品 `PASS`，完整章节 Assembly／Fidelity 技术通过但
  P3 产品体验待验；Discovery 原始证据获 `RAW_EVIDENCE_USABLE_FOR_CONTENT_REVIEW`，可进入
  匿名人工比较，但 V0／V1′ 胜负仍为 `unknown`。总控纠偏固化为 `D-ENG-002` 与自动加载规则。
- Canonical status：`diagnostic-only`
- Failures / detours：两条独立工作线共用执行队列，总控下沉到组内实现，并在真实证据前追加
  多余协议、schema、harness 与 gate；产品负责人介入收缩 blocker 前，约一小时仍未启动正式
  Scout。收缩后 18 次调用约 20 分 38 秒完成。审核包只支持“共享队列相互干扰”，不能证明
  Writer 单向阻塞 Discovery。
- Repeat-error check：与全局错题 `M002`“验收／前置工程吞掉产品闭环”同类，构成复发候选；
  是否把 `M002` 从复发 x1 更新为 x2，须产品负责人另行批准，本轮未写全局文件。
- Incident classification：`actual-loss` / `significant`；实际损失为约一小时没有可审阅的真实
  Scout 证据、产品负责人被迫中途纠偏；潜在损失为继续扩建下游系统并污染两条线的优先级。
  Failure signature：冻结实验已经具备最小输入和输出合同，但总控把未授权风险转成新启动门，
  且没有证据启动时限。
- Confirmed / unconfirmed：确认 18 次正式调用在收缩后完成、独立审计认可原始证据可用于人工
  内容审阅、共享队列／前置膨胀／角色下沉成立；未确认全部前置工作的精确耗时因果，也未确认
  Writer 对 Discovery 的单向阻塞关系。
- Fix verification：项目自动加载规则新增独立队列、一页运行卡、最多三个 blocker、30 分钟
  evidence-start fuse 与总控三检查点；`D-ENG-002` 保存决定与证据边界。下一干净会话必须只
  生成 9 个匿名 A/B 产品审阅 block，交包即停止。
- Reusable lesson / rule candidate：项目内已升级为强规则；跨项目候选是更新全局 `M002` 的复发
  次数和来源，不新建重复条目。
- Follow-up：按最终 handoff 启动干净总控，只组织一个 Discovery 小组长机械制作盲审包；产品
  负责人完成 71 个 seed 与 9 个 pair 的内容判断前，不启动核验、解盲、Writer 或下一实验。

### Run: 2026-07-26 - discovery-blind-review-rejection-and-root-cause

- Task / Type / Tool：18 次冻结 Scout 的匿名内容审阅包、两版中文 smoke、产品失败复盘与上游
  目标回溯 / diagnostic / Discovery 小组长机械装配 + 总控独立核验 + 产品负责人 smoke 审阅
- Context source / Boundary：本会话直接任务只允许把既有 18 次原始结果机械整理成 9 组匿名
  A/B，不重跑模型、不改 Prompt、不启动 Writer。产品负责人先后要求中文、正常阅读界面和材料
  语境；两版 smoke 仍失败后，授权只读回查产品 owner、现行蓝图、实验协议、冻结 Prompt/schema
  与 71 个 raw seed。未读取 Gold、examples、archive 或旧 ReaderLab。
- Files read / changed：仓库外生成机械匿名包与两版中文 smoke；本次收口维护
  `PRODUCT-DECISIONS.md`、`docs/current-task.md`、`docs/dev-state.md` 与本账本。没有修改冻结
  原始证据、实验 Prompt/schema、生产 taskcard、run 或 Writer 正文。
- Commands / checks：9/9 pair 材料与 repeat 对齐；71/71 seed；284 项原始语义字段字节一致；
  anchor 为 1 个 exact substring、52 个 normalized contiguous、18 个 ordered-spans（共 102 个
  exact source spans）；54 个 raw/request/receipt hash、21 个冻结文件 hash、9/9 随机映射和
  匿名泄漏检查通过。随后对全部 71 个 seed 按材料与主题族做只读语义审计。
- Artifacts / reports：
  `/private/tmp/readerlab-discovery-blind-review-20260726/final/`、
  `/private/tmp/readerlab-discovery-blind-review-zh-20260726/candidate-smoke/`、
  `/private/tmp/readerlab-discovery-blind-review-zh-20260726/candidate-smoke-v0.2/`。
- Result / Evidence type：机械匿名包达到 `verified`，但两版中文 smoke 均未获产品
  `accepted`；产品负责人确认产物只是把简单材料接到更深、更专业、更晦涩的知识，没有交付一套
  解析和理解世界的可迁移框架。完整 71 项盲审停止，V0／V1′ 胜负未回答。
- Canonical status：`diagnostic-only`
- Failures / detours：第一版直接展示孤立工程原句和 seed 字段，第二版补材料定性、上下文与中文
  解释，但都把“展示不清”误当主要问题；真正失败在上游共同合同。产品原始目标是让具有不同稳定
  认知背景的专家自由阅读完整材料并自然提出成熟外部框架，实验却把它编译为“找到局部关系缺少的
  解释变量并输出短机制 seed”。通用 Scout、短字段 schema、技术 Judge 与压缩式产品包共同
  放大了这一缩窄；V1′ trigger map 不是独立根因。
- Repeat-error check：与 `ENGINEERING-LESSONS.md` 已记录的“模型准确执行错误编译目标、通用无
  背景生产者收敛到局部分析”同类，再次在 Discovery 控制实验中复现；本轮不新增平行工程教训
  owner。
- Incident class: actual-loss
- Loss severity: significant
- Loss dimensions: progress / user-attention / artifact
- Actual loss：18 次调用和 71 个 seed 虽保留诊断价值，但不能用于原计划的产品 A/B；产品负责人
  连续阅读两版不合格 smoke 后才暴露共同目标错误。
- Potential impact：若继续逐卡、解盲或优化展示，会把产品注意力消耗在错误题目上，并可能错误
  宣布某种触发方式胜出。
- Failure signature：机械证据、匿名性和格式全部通过，但真实读者仍无法说清“这是一套什么知识、
  为什么值得借它重读原文”；对照材料两变体 6/6 非零并收敛到相同的局部技术主题。
- Evidence pointers：本 run 的三个仓库外目录；冻结
  `treatment-isolation-v0.1.md`、`scout-v0.md`、`scout-v1-prime.md` 与共同
  `seed-batch.schema.json`；`PRODUCT-DECISIONS.md` 的“核心交付对象”“透镜系统原始目标”和
  “完整阅读单元”。
- Confirmed facts：共同 Prompt 要求外部解释机制，V1′ 只增加缺失变量 trigger；共同 schema
  没有稳定专家背景、框架内核、边界或完整课字段；静态对照 6/6 运行共 23 个 seed；两变体主题
  收敛；产品负责人明确拒绝当前 smoke。
- Unconfirmed hypotheses：正确角色和 Prompt 能否稳定召回成熟外部框架、哪一种触发方法更好、
  目标档模型是否具备所需能力，均为 `unknown`。
- Fix and verification：本轮只完成根因定位，没有修复或新模型运行。产品负责人把 Discovery
  范围收回“可迁移外部认知框架”，暂不另开仿生学趣闻等具体新知入口；未来如修复，必须以新版本
  和 change receipt 运行一个最小正例加负向控制，并先交自然可读产物。
- Cross-project candidate: no
- Follow-up：以后单独讨论原始问题——怎样触发具有稳定认知背景的专家，从完整原文自然召回
  可迁移外部认知框架；没有新方案与明确授权前，不改 Prompt、不重跑、不启动下游。

### Run: 2026-07-29 - T2.36 U01 social-connection depth seam

- Task / Type / Tool：固定 C 的 Expert → 内容锁 → Writer → Fidelity／Depth 独立链 / diagnostic / 四个功能隔离 Codex Agent + Web Search/Web Fetch（仅 Expert）+ SHA-256 freeze。
- Context source / Boundary：产品负责人明确冻结 U01 与 Iris Marion Young 的 Social Connection Model，并禁止新路线、ABC、候选搜索、B、M1/M2/M3、长期合同与生产入口改动。四个语义角色按白名单文件交接；旧稿只在双门通过后才可由控制层读取，实际从未读取。
- Files read / changed：新任务卡 `taskcards/T2.36.md`、当前状态／开发状态／本账本、审计资产投影，以及 `runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/` 全部实际 evidence；完整本地包为 `artifacts/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01.tar.gz`。
- Commands / checks：U01 输入 hash／字节数、5 份 Prompt hash、Stage 0—4 hash 全部 `shasum -c` 通过；Phase 2/4 终局标记、UTF-8、包内条目和 `git diff --check` 复核。初次 active tests 因新任务卡／run 未登记到资产投影和 current-state control 字段而失败，机械同步后重跑。
- Artifacts / reports：`raw/expert-course.md`、`raw/source-map.md`、`locked/content-review.md`、`locked/content-lock.md`、`final/reader-v1.md`、`acceptance/fidelity-depth-review.md`、run manifest／ledger 与本地压缩包。
- Result / Evidence type：Phase 2 `LOCK_FOR_WRITER`；Fidelity `RETURN_WRITER`；Depth `DEPTH_PASS`。按任务卡立即停止，未生成产品审阅包／版本密钥；产品接受为 `unknown`。
- Canonical status：`diagnostic-only`
- Failures / detours：初始 Expert 上下文 `/root/u01_expert` 因外部 worktree 写入策略未能落盘，未产生任何 raw artifact；同一未改 Prompt、未改输入由新的 `/root/u01_expert_recovery` 技术重派完成。归档首次因目标目录缺失失败，创建空目录后成功；两次均记录在 run ledger，未作为结果质量补跑。
- Repeat-error check：未发现与既有语义／产品失败相同的已确认机制；两项均为本地路径／归档机械恢复，未升级全局候选。
- Reusable lesson / rule candidate：无；功能性 Agent 隔离、失败重派与 artifact freeze 的适用边界已由当前项目规则拥有，不新增平行规则。
- Follow-up：停止。若产品负责人希望修订 Reader，必须在新任务中重新冻结 Writer 输入、版本和验收边界；不得覆盖本 run 的冻结文件。

### Run: 2026-07-29 - T2.37 U01 social-connection Writer return

- Task / Type / Tool：T2.36 `RETURN_WRITER` 的两处归属修正、来源说明、独立 Fidelity／Depth v2 与条件性产品匿名包 / diagnostic / 两个全新功能隔离 Codex Agent + SHA-256 freeze。
- Context source / Boundary：产品负责人明确只修复 Writer 保真问题；分支先按要求推送到 `origin`，随后从 T2.36 逐字复制六个冻结输入。不得重开 Expert、内容审核或来源研究，不得读取旧稿直到双门通过；不修改长期合同、Skill、产品标准或生产入口。
- Files read / changed：`taskcards/T2.37.md`、当前／开发状态、资产生命周期投影、本 run 六个输入副本、return brief、两份阶段任务、Reader v2、Fidelity／Depth v2、条件性产品包、run manifest／ledger 与本地 archive。旧直接路线 `audit/current-runtime-snapshot/u01-u03/direct-output/U01.md` 只在双门通过后由控制层机械读取；Reader v1 未进入产品包。T2.36 六个源文件未修改。
- Agent contexts：Writer return `/root/u01_writer_return`；Fidelity／Depth v2 `/root/u01_fidelity_depth_v2`。模型、reasoning、token、成本均 `unavailable`；两个 Agent 均 `fork_turns="none"`，精确 read set 见各自阶段任务；两阶段均 `network: no`、`retry: no`、`Prompt modified: no`。
- 时间记录：run 启动 `2026-07-29T05:20:53-0400`；Writer 输出文件落盘 `2026-07-29T05:23:09-0400`；Fidelity／Depth v2 报告落盘 `2026-07-29T05:25:46-0400`；产品包／归档机械步骤结束 `2026-07-29T05:30:51-0400`。两个 Agent 的精确开始时间不可取得，记 `unavailable`，不倒推墙钟。
- Input SHA-256：U01 `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`；Expert `86540f040d9002ffd5e6bff581a5455c24fdc197e2bfaec712a3d8944df8b65b`；source map `f89b357700f05eb8ab9ee12602ddc81a736d28443fa10b4cb53fc0e825d33f0a`；content lock `2f0c8ec0b4e06c5957010dec5a68aa8dcd957cdb7344c6acf3553430a969ed47`；Reader v1 `49fe703f2e578a477390d621d6d82f566a4d1342baa70ab761f1aac0cee1e71a`；T2.36 Fidelity／Depth `d801a153a2f948d43ed508c4f2dc27919cc189ddf59a724abada04ccbcdeecfc`。
- Prompt／control freeze：return brief `00a1629d58a8793e5ef9d6809dc28e230bdd8b92fcaaf1477e12411ade865b66`；Writer task `5d661471002bd8e82ace65681c6ea3159f3ce76bc97e776ef06ce982e1e9b3cc`；Fidelity／Depth task `17a99eaa72754ac0b8567af204d3e19e13295c5bf3c5aaeaa2fcff20ea1e2156`；product task `702aa3163586d9569cc075182341fbd334bbe9ffb4915f94283cf52bbdad8218`。六个输入与阶段冻结记录分别在 `control/freeze-stage-0.sha256` 至 `freeze-stage-3.sha256`。
- Result / Evidence type：Writer v2 只改两处教学／案例归属并添加指定来源说明，SHA-256 `a329df15d0162ea16479a56554970aba6a29d03ea993bdc9c959834682102a02`；Fidelity／Depth v2 报告 SHA-256 `8751f9719cddf0972248f5d98c18a2c73c0ab0da26f41a211abe958414522862`，终局 `FIDELITY_PASS` + `DEPTH_PASS`。产品匿名包最终冻结 SHA-256 `0a462fe1c17f049ba3a486c7828ebe9e30fc71416b71933567d075ae3f88bc05`（仅做 EOF 与行尾空白规范化，不改变可见内容）；版本密钥 SHA-256 `acb0ac703f9ea78fd73bd94069423815e9f10680efc4e23c731b7701ac8fb748`，产品审阅前不得打开。
- Archive：`artifacts/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01.tar.gz`，最终 SHA-256 `d30f248dd8ae5d89921ca9d19bf81284f740ee86d7017760e4b5751ce0f03a6e`，29 个条目；不把自引用 archive hash 写入 archive 内部。
- Checks：六个 T2.36→T2.37 `cmp`、所有 stage freeze `shasum -c`、Reader v1 未覆盖、T2.36 路径无 diff、`git diff --cached --check`（排除必须逐字节保留、原文既有行尾空白的 `inputs/u01-frozen.md`）通过。`python3 -B tests/entry.py` 35/36 通过；唯一失败是审计基线在本轮开始前已有的未跟踪 Markdown 未列入资产登记的全树穷举项，未修改或纳入提交。
- Stop / Acceptance：`STOPPED_AFTER_PRODUCT_PACK_WAITING_FOR_PRODUCT_REVIEW`；产品负责人判词 `unknown`，下一生产授权 `none`。完成后停止，不修改 ReaderLab 长期合同、Skill、生产路线或产品标准。

### Run: 2026-07-29 - T2.39 ReaderLab Book Expert Teaching Skill v0.1

- Task / Type / Tool：从 T2.38 已验证控制能力建立 `readerlab-book-expert-teaching` Skill v0.1.0 候选；确定性实现、Skill-local tests 与 T2.38 mechanical replay，不启动任何新语义实验。
- Baseline / Branch：基线 `4f9c62529d3ef55ead9ccf6a5e33a3b402e663cb`；分支 `feature/readerlab-book-expert-teaching-skill-v0.1`。T2.36/T2.37/T2.38 冻结文件保持只读，未创建新的语义 run。
- Contexts：语义 Agent contexts `none`；本轮由主执行上下文完成控制层实现与确定性测试。模型、reasoning、token、成本与墙钟均 `unavailable`；network `no`；retry `no`；Prompt modified `no`（没有语义 Prompt 调用）。
- Exact read set：`AGENTS.md`、`docs/current-task.md`、`docs/dev-state.md`、`docs/agent-run-ledger.md`、`PRODUCT-DECISIONS.md`、`ENGINEERING-LESSONS.md`、`blueprints/PIPELINE-MAP.md`、`tools/run.py`、`tests/entry.py`、`tests/test_run_promotion.py`、`taskcards/T2.39.md`、T2.38 `run-manifest.md`／`run-ledger.md`／`control/*`／`raw/*`／`acceptance/*`、T2.36 固定输入、既有 functional-role-isolation Skill，以及 Skill Creator 的 `SKILL.md` 与 `references/openai_yaml.md`。未读取其他语义路线或产品判词。
- Source / search：没有外部来源打开、没有搜索、没有语义模型调用；T2.38 fixture 只按已登记仓库路径注入冻结字节。
- Created / changed：Skill 目录、T2.39 taskcard、阶段实现状态、Skill review map／brief、blueprint pointer、current/dev state、asset register 与本条 ledger；未修改产品决议、现行内容合同、历史判词或 T2.36/T2.37/T2.38 冻结产物。
- Verification：`quick_validate.py` 通过；Skill-local `unittest` 13/13 通过（含 init、覆盖拒绝、漂移、输出完整性、Agent ID 隔离、非法状态、双门产品包、可读 Markdown、泄漏门、archive、fingerprint 与 T2.38 replay）；T2.38 replay 使用临时 run 注入既有 Expert／review 输出，`init → seal-expert → seal-review → build-product-pack → verify → archive` 全部通过，无新语义结果或产品判词。仓库 active tests 的资产穷举失败属于本任务开始前已存在的 118 个未登记 Markdown 影子文件；其余断言已通过，未纳入或改写这些文件。
- Freeze / hash：每个 Skill run 以 `SKILL.md`、`VERSION`、`agents/openai.yaml`、contracts、templates、scripts 的 aggregate fingerprint 防漂移；T2.38 机械 replay 的临时 run 与 archive 随测试清理，不冒充正式 run。最终提交前再执行 `git diff --check`、敏感信息检查和状态／冻结核对。
- Result / Stop：`implemented` 为 Skill v0.1.0 文件与入口存在；`integrated: not integrated`；`verified` 仅限上述确定性检查与机械 replay；`accepted: unknown`；停止在 Skill scaffold 与 replay，不运行两个迁移样本，不启动 Writer、ABC、Discovery 或完整 orchestrator。

### Run: 2026-07-29 - T2.38 U01 social-connection Expert teaching

- Task / Type / Tool：固定 U01、固定 Iris Marion Young Social Connection Model 与 T2.36 冻结来源范围下的 Expert
  teaching diagnostic sidecar / 两个全新功能隔离 Codex Agent + allowlist Web Fetch + SHA-256 freeze；不启动
  Writer、Reader、ABC、Discovery 或产品装配。
- Context source / Boundary：`taskcards/T2.38.md`、T2.36 U01 与 source map 的逐字副本；不修改长期合同、
  Skill、生产入口、产品标准、T2.36/T2.37 或任何历史 run。Expert 不读 T2.36 Expert 正文、Reader、Writer、
  content lock、判词或其他 Agent 对话；审核者不读旧 Expert、Reader、Writer、产品判词或隐藏推理。
- Agent contexts：Expert teaching `/root/u01_expert_teaching`；独立来源／教学审核
  `/root/u01_expert_teaching_review`；均 `fork_turns="none"`、各一次语义执行。模型、reasoning、token、成本与
  精确 Agent 墙钟时间未暴露，记录为 `unavailable`；retry `no`；Prompt modified `no`。
- Exact read sets：Expert 读取 `runs/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01/inputs/u01-frozen.md`、
  `inputs/frozen-source-map.md`、`control/expert-teaching-task.md`，以及 source map allowlist 页面；审核者读取
  同一 run 的上述 U01、source map、`raw/expert-teaching-draft.md`、`raw/expert-teaching-source-map.md`、
  `control/expert-teaching-review-task.md`，以及同一 allowlist 页面。除此之外未读取其他本地路径或 Agent 对话。
- Source pages opened (Expert)：Cambridge 2006、Paperzz 2006、MIT 2004 PDF、Oxford 2011、SEP、Springer Zheng
  2018 均成功；Cambridge Gunnemyr 2020 初次成功但后续行定位 timeout（未重试）；OUP24 原 URL 成功并重定向至
  登记允许的 `https://oup.silverchair-cdn.com/book-minimal/58181/chapter-minimal/480373479`；UGR PDF Internal
  Error（未采用、未重试）。仅直接打开 allowlist URL，无开放式搜索、无新增来源。
- Source pages opened (review)：Cambridge 2006、Paperzz 2006、MIT 2004 PDF、Oxford 2011、SEP、Springer Zheng
  2018 成功；Gunnemyr、OUP24 原 URL、登记 OUP CDN 与 UGR 本次 Internal Error，未以失败页面扩展结论，未重试；
  无开放式搜索、无新增来源。
- Input SHA-256：U01 `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`（16368 bytes）；固定
  source map `f89b357700f05eb8ab9ee12602ddc81a736d28443fa10b4cb53fc0e825d33f0a`（T2.36 原始副本一致）。
- Prompt／control freeze：Expert task `8545d270156bfd3f783d479ee81a2b11efa99ad40e4da69eb383f9054402e9a5`；
  review task `3135f342aaf30a5e706736f58dd970719d869822482e046826c0a20422b69049`；product task
  `bcf8a03dcab59a922fcd63a6f6448556869fced9287ebc2a511b0f7e94256861`；input-freeze
  `884f4fa4abd02c54171e21b8e49ed092933832dc900a1cf61441fd1a1cc529b3`。阶段 0、Prompt、阶段 1、阶段 2、阶段 3
  的 `shasum -c` 全部通过。
- Result / Evidence type：Expert teaching `raw/expert-teaching-draft.md` SHA-256
  `13d5cd6ae520fda515cc2a3a6c105ddd564d88d50d5232feea9ac399789053b2`；来源归属表 SHA-256
  `1b518fc97a5bf0abe2d2c664ed049294ee7b42079c7401aa2e5ed3e4d71043f8`；独立审核报告 SHA-256
  `9c9f7c64cce0bd17cbc9747775b00ca938bb4b5962b69821a1b4583eab87846f`。终局为
  `SOURCE_FIDELITY_PASS` + `TEACHING_PASS`。正文无 M1/M2/M3 标签，教学整理与 U01 推论在来源表和正文中
  分开标注。
- Product pack：双门通过后由控制层机械复制冻结 U01 与完整教学课生成
  `runs/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01/acceptance/expert-product-review.md`，SHA-256
  `fe194eea4666ffd55bf25a4a33c11f2062b28e7fdffe26de41a994e73b9dde33`；不含来源表、技术评分、Writer、旧稿、
  路线或版本密钥；产品负责人判词仍为 `unknown`。
- Archive：`artifacts/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01.tar.gz`，22 个条目，最终 SHA-256
  `30ee088275a68a8fccd852fa8147b1906343aad0dab48c49d3aefb8537047a3e`；archive hash 不写入 archive 自身，
  由本账本记录。
- Checks：T2.36 U01 与 source map `cmp`、所有 freeze、首两行终局、无 M1/M2/M3、产品包内容限制、archive
  条目／完整性均通过。`python3 -B tests/entry.py` 共 36 项，35 项通过；资产计数项已同步通过，唯一失败是
  审计基线在本轮开始前已有的未跟踪 Markdown 未列入资产登记全树穷举
  （`test_asset_register_exhaustively_lists_taskcards_and_runs`），未修改或纳入提交。
  `git diff --check` 需在 staging 后复核；冻结 U01 的既有行尾空白若出现，按逐字节输入保留并单独说明。
- Stop / Acceptance：`STOPPED_AFTER_EXPERT_TEACHING_REVIEW`；双门通过后停止在产品负责人审阅前，产品接受
  `unknown`、下一生产授权 `none`。完成后不根据结果启动 Writer 或修改 ReaderLab 长期合同、Skill、生产路线或
  产品标准。

### Run: 2026-07-29 - T2.40 Expert Teaching Skill v0.1.1 boundary hardening

- Task / Type / Tool：外部 Code Review 后的版本共存、结构化来源 allowlist、中文表达合同、内容泄露门、T2.38
  mechanical replay 和运行元数据 hardening / diagnostic implementation / 本主执行上下文 + 本地确定性工具。
- Baseline / Branch：基线 `66eeaa1d8a068df3e73848717ee20b0c87b105918`；
  `feature/readerlab-book-expert-teaching-skill-v0.1`；保留不可变的 0.1.0 根实现，新实现位于独立
  `versions/0.1.1/`，current dispatcher 由 `CURRENT_VERSION` 明确选择。
- Contexts：语义 Agent `none`；本轮没有启动模型。模型、reasoning、token、成本、精确墙钟和外部执行
  receipt 均 `unavailable`；Skill 自身语义调用 `none`；外部语义上下文 `controller_declared`；network
  `no`；retry `no`；Prompt modified `no`。运行字段在 manifest／ledger 中均标为 `controller_declared`。
- Exact read set：`AGENTS.md`、`docs/current-task.md`、`docs/dev-state.md`、`docs/agent-run-ledger.md`、
  `PRODUCT-DECISIONS.md`、`ENGINEERING-LESSONS.md`、`blueprints/PIPELINE-MAP.md`、
  `audit/ASSET-LIFECYCLE-REGISTER.md`、`tools/run.py`、`tests/entry.py`、
  `tests/test_repository_audit_guardrails.py`、`taskcards/T2.39.md`、0.1.0 Skill 文件、T2.38 fixture 登记的
  source／source map／Expert／review／产品包及 `/Users/tianqiang/.codex/skills/.system/skill-creator/SKILL.md`。
  没有读取或修改 T2.36—T2.39 冻结语义内容以外的路线结果。
- Source / search：无外部来源打开、无搜索、无 redirect 自动扩展、无网络、无语义调用；T2.38 replay 只按
  fixture 登记路径注入冻结字节。
- Created / changed：T2.40 taskcard、0.1.1 版本目录、current dispatcher、allowlist fixture、Skill-local
  tests、change receipt、阶段状态、review map／brief、蓝图 pointer、current／dev state、asset register 和本条
  ledger；0.1.0 根文件、PRODUCT-DECISIONS、`contracts/BOOK-CONTENT-FLOW-v2.md`、T2.36—T2.39 冻结产物和历史
  判词未改。
- Fixture identities：T2.36 source `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`；
  source map `f89b357700f05eb8ab9ee12602ddc81a736d28443fa10b4cb53fc0e825d33f0a`；allowlist
  `5eca499c6e8c899e5d44e97d91eb78884c76169f0638fab0e747fc2f334817ab`；Expert draft
  `13d5cd6ae520fda515cc2a3a6c105ddd564d88d50d5232feea9ac399789053b2`；Expert source map
  `1b518fc97a5bf0abe2d2c664ed049294ee7b42079c7401aa2e5ed3e4d71043f8`；review
  `9c9f7c64cce0bd17cbc9747775b00ca938bb4b5962b69821a1b4583eab87846f`；0.1.0 frozen product
  `fe194eea4666ffd55bf25a4a33c11f2062b28e7fdffe26de41a994e73b9dde33`；0.1.1 replay product
  `859b72105a9ad1858dde720fc1c4ed2af7810b29da09efaaf8fa2696e9c8df1e`。
- Verification：Skill-local deterministic tests `24/24` 通过；quick validation 通过；T2.38 mechanical replay
  通过（含 source、source map、allowlist、Expert draft、Expert source map、review、产品包和 archive 成员
  hash）；`git diff --cached --check` 与敏感信息检查通过。repository active tests `35/36` 通过，唯一失败是
  本轮开始前已存在的 118 个未登记 Markdown 资产穷举项；未修改或纳入这些文件。不运行迁移样本，不启动
  Writer、Discovery、ABC 或 orchestrator。
- Stop / Acceptance：完成指定提交和推送后停止；`implemented` 为 0.1.1 版本化实现，`verified` 仅指确定性
  checks 与 mechanical replay，`integrated: not_integrated`，`accepted: unknown`，下一生产授权 `none`。
