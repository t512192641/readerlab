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
