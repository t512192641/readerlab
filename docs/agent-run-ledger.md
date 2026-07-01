# 2026-07-01 私有材料本地验证通过

## 摘要

- 用户从本地扫描候选中选择 B2：`Feel-Good Productivity 全书完整中译.pdf`，并明确这是本地验证材料，后续会把 GitHub 项目改为 private。
- 用户选择 C1：`planning-with-files/SKILL.md` 作为 Skill / 工程材料验证源。
- 本轮新建 `docs/reports/readerlab-private-material-validation-v0/`，作为 private validation，不覆盖已有 two-demo 产物。
- 后续用户确认 GitHub visibility 已改为 private；主控通过 GitHub app 核验 `t512192641/readerlab` 的 `visibility: private`，允许纳入 private checkpoint。

## 结果

- Demo A：`A_feel_good_productivity`，由 99 页 PDF 用 `pdftotext -layout` 抽取完整正文到 `10_一手正文/001_正文.md`，本地正文规模约 4,705 行 / 360KB。reader evaluation：`pass`，`10/12`，P0/P1 为空。
- Demo B：`B_planning_with_files`，从 local Skill 源生成净化正文、设计资产、source-cleaning-map、location-map、trace-to-reader 和 contracts。reader evaluation：`pass`，`11/12`，P0/P1 为空。
- Demo A 批注触发 6 个，candidate decisions 包含 2 个 reject。
- Demo B 批注触发 5 个，candidate decisions 包含 2 个 downgrade 和 1 个 reject。

## 边界

- 这是 `private_material_validation_local_pass: 2/2`，不是 public external validation。
- Demo A 包含 copyrighted/private full body text，只能保留在 private repository / local 环境中。
- 不启动正式 ReaderLab Skill 草案；`planning-with-files` 只作为阅读材料，不安装、不同步、不启用。

## 验证

- `find docs/reports/readerlab-private-material-validation-v0/demos -name '*.json' -print -exec python3 -m json.tool {} /tmp/readerlab-private-json.out \;`：PASS。
- `rg -n "source refs|claim trace|lens score|machine_status|human_status|Body Track Gate|Claim Ledger|Candidate Tournament|Skillization Gate|Annotation Trigger" docs/reports/readerlab-private-material-validation-v0/demos/*/20_AI陪读`：PASS，无命中。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 two-demo review hardening patch

## 摘要

- 用户提交 GPT Pro 对 two-demo checkpoint 的审核结果；结论是 `two_demo_internal_pass: 2/2` 可以成立，但不能升级为 `transferable_method_kernel_pass`，也不能启动正式 ReaderLab Skill 草案。
- 本轮按 Pro 指出的最小缺口补 review hardening，不扩大到外部材料验证，不重跑 demo，不写正式 Skill。
- 明确批注层口径：Obsidian 批注插件本身不是主要风险；当前要补的是批注回读时从评论位置稳定回到正文 anchor、claim、candidate 和 gate 决策的证据链。

## 改动

- Demo A / B 均新增 `audit/location-map.json`，把正文段落、reader-facing 段落、claim、candidate 和 annotation trigger 接到稳定 anchor。
- Demo A / B 均新增 `audit/trace-to-reader.md`，说明 reader-facing 每段如何消费正文、claim ledger、candidate tournament 和 gate 决策。
- Demo B 新增 `audit/source-cleaning-map.md`，说明 `gstack/spec` 内容如何被保留、压缩、移入设计资产、移入 audit 或拒绝进入 reader-facing。
- `body-track-gate.v1` 新增 `skill_engineering_cleaned_body_pass`，Demo B 的 body-track gate 不再使用容易误解的 `audit_only`。
- GPT Pro review brief、copy prompt、required / optional attachments 已指向新增 hardening 证据。

## 验证

- `python3 -m json.tool` 检查 two-demo 所有 JSON：PASS。
- reader-facing 内部字段残留检查：PASS，无命中。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 双 demo 内部方法核验证通过

## 摘要

- 按 `docs/reports/readerlab-two-demo-run-v0/README.md` 执行两个内部 demo，没有准备 GPT Pro 审核 prompt。
- Demo A 使用 `docs/product-spec.md` 作为 repo-owned longform，完整正文轨落地到 `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/10_一手正文/001_正文.md`。
- Demo B 使用 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md` 作为 Skill / 工程阅读源，只阅读，不安装、不同步、不启用。
- 两个 demo 均由 writer agent 产出、reader evaluation agent 独立评价、主控回收验证。

## 结果

- Demo A：reader evaluation `pass`，`11/12`，P0/P1 为空。边界：证明 repo-owned longform reader package 最小形态，不证明外部书泛化。
- Demo B：reader evaluation `pass`，`11/12`，P0/P1 为空。边界：净化正文相对 2359 行源材料压缩较强，未来做 canonical benchmark 时可补 runtime 剥离类别 audit map。
- 本轮状态口径：`two_demo_internal_pass: 2/2`。
- 下一步不能自动进入正式 Skill 草案、外部书验证或 GPT Pro 审核；是否准备 GPT Pro review packet 需用户明确启动。

## 验证

- `find docs/reports/readerlab-two-demo-run-v0/demos -name '*.json' -print -exec python3 -m json.tool {} /tmp/readerlab-demo-json.out \;`：PASS。
- `rg -n "source refs|claim trace|lens score|machine_status|human_status|Body Track Gate|Claim Ledger|Candidate Tournament|Skillization Gate|Annotation Trigger" docs/reports/readerlab-two-demo-run-v0/demos/*/20_AI陪读`：PASS，无命中。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 双 demo 内部执行合同准备

## 摘要

- 用户纠正：现在不是写 GPT Pro 审核 prompt，而是先安排下一会话跑两个新 demo；只有 demo 内部 writer/reader 双门槛通过后，才值得提交 GPT Pro 审核。
- 新增 `docs/reports/readerlab-two-demo-run-v0/README.md`，作为下一会话双 demo 执行合同。
- 新增 `docs/reports/readerlab-two-demo-run-v0/01_NEXT_SESSION_PROMPT.md`，作为可直接复制的下一会话执行 prompt。
- 已同步 `docs/current-task.md` 和 `docs/next-session-prompt.md`，把下一步从“复核 method-kernel-v0 / GPT Pro 审核”改为“先跑两个内部 demo”。

## 关键约束

- Demo A 必须有合规完整正文轨；没有可提交的公版、用户自有或 repo-owned 长文源就停止。
- Demo B 默认使用 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md` 作为 Skill/工程材料源；如果下一会话判断 `spec` 过重或机器协议噪音过多，可改用 `gstack/design-review`。DB Skills 备选为 `dbs-suite/dbs-xhs-title` 或 `dbs-suite/dbs-diagnosis`。只阅读，不安装、不同步、不启用。
- 每个 demo 必须由 writer agent 产出、reader evaluation agent 独立评价、主控回收；主控不能自写自评后标 pass。
- 两个 demo 都内部通过后，才允许准备 GPT Pro review packet。

## 当前状态

- 双 demo 尚未执行。
- 尚未新增 `demos/` 产物。
- 尚未准备 GPT Pro 审核包。

## 验证

- 当前入口 / prompt 扫描：`docs/current-task.md`、`docs/next-session-prompt.md` 和 `readerlab-two-demo-run-v0` 均指向双 demo 内部执行，不再把下一步写成 GPT Pro 审核 prompt。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 GPT Pro 方法核纠偏与 mem-clean 状态压缩

## 摘要

- 用户要求读取 GPT Pro 方案 `~/Downloads/chatgpt-selected-2026-07-01T02-41-22.md`，严格执行第八部分行动，并调用 `mem-clean` 处理状态文档。
- 本轮按 GPT Pro 纠偏：15 章产物只能称为 `chapter_high_order_explanation_pass`，不能称为完整 ReaderLab 阅读包通过。
- 新增六个方法核 contract：Body Track Gate、Material Profile、Claim Ledger、Candidate Tournament、Skillization Gate、Annotation Trigger。
- 新增 `docs/reports/readerlab-method-kernel-v0/`，用 `组织设计 / v101-16` 和 `打造特斯拉 / v101-21` 做两章最小方法核探针。
- 探针结论：`method_kernel_probe_pass`；完整阅读包仍为 `reader_package_not_verified`，正式 Skill 和外部材料验证仍未启动。
- 已同步 `docs/current-task.md`、`docs/product-spec.md`、`docs/readerlab-package-spec.md`、`docs/eval-gates.md`、`docs/dev-state.md`、`docs/progress.md`、`docs/decisions.md`、`docs/next-session-prompt.md`。

## 关键纠偏

- 高阶讲解通过不等于阅读包通过。
- “讲解贴合正文锚点”不能替代“一手正文存在”。
- 候选池必须产生真实 `promote / keep / downgrade / reject`，否则只是字段吸收。
- Skill 化必须满足 trigger / input / steps / output / boundary / evidence 六项；危机、过劳、强控制和英雄化不能升格为 Skill。
- 下一步只能复核 `readerlab-method-kernel-v0`，不能自动进入正式 Skill 草案或外部书验证。

## 验证

- `python3 -m json.tool` 检查新增 14 个方法核 JSON：PASS。
- reader-facing 内部字段残留检查：PASS，无 `source refs`、`claim trace`、`lens score`、`machine_status`、`human_status` 或 gate 名称残留。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 根层文档权威边界清理

## 摘要

- 用户要求现在执行一次文档清理，解决 docs 下历史文档积压导致新会话误读多事实源的问题。
- 本轮不删除历史报告、不移动目录，只给容易被误读的根层规格/方法/研究/草案/报告文件补权威边界。
- 新增 `docs/reports/README.md`，声明 `docs/reports/**` 是证据库和历史实验区，不是当前任务源。
- `docs/decisions.md` 新增 D-051：当前事实唯一入口与动作触发读取。
- 收窄 D-036：`docs/progress.md` 已降级为历史进度快照，当前事实只能回到 `docs/current-task.md`。
- 已补边界的根层文件包括：`product-spec`、`readerlab-package-spec`、`high-order-explanation-method`、`research-log`、`readerlab-v0.1-light-prototype`、`agent-workflow`、`readerlab-output-eval-v0`、`readerlab-skill-ir-v0`、`dbskill-readerlab-test-report`、`adversarial-review`、`complex-material-reading-sop`、`readerlab-future-roadmap-and-references`。

## 验证

- `rg` 高风险启动/事实源污染搜索：仅剩 D-051 自身的清理验收规则，未发现旧启动层污染。
- `git diff --check`：PASS。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。

# 2026-07-01 文档真相层单独清理

## 摘要

- 用户指出本地十几个文档已经严重影响信息源真实唯一性，要求作为单独清理任务执行。
- 本轮将启动入口从 7 个文件进一步压缩为 2 个文件：`AGENTS.md` 和 `docs/current-task.md`。
- `docs/current-task.md` 被设为当前执行事实唯一入口；如与 `dev-state`、`progress`、`next-session-prompt`、旧报告或旧 handoff 冲突，以 `current-task.md` 为准。
- `docs/dev-state.md` 降级为稳定路径、工具状态和验证命令索引。
- `docs/progress.md` 降级为历史进度快照。
- `docs/next-session-prompt.md` 降级为从 `current-task.md` 派生的短启动提示。
- `README.md` 和 `docs/project-retrospective.md` 已同步新的文档权威边界。

## 验证

- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 MEMCLN 复盘与状态压缩

## 摘要

- 用户要求调用 MEMCLN 工具包，整理当前遇到的全部问题，包括项目开发问题和使用侧问题。
- 已按 `mem-clean` 规则把 `docs/dev-state.md` 压回当前事实层，移除阶段流水账和历史细节。
- 已重写 `docs/project-retrospective.md`，把本次问题拆成项目开发问题、使用侧问题、项目内规则候选、全局错题本候选和后续风险。
- 已在 `docs/decisions.md` 新增 D-050：多阶段闭环必须以完整链路定义完成。
- 未写入全局错题本；只提出候选 G-004 到 G-007，等待用户批准后才能升维。

## 关键纠偏

- 当前不是“全书跑过后只有两章通过”，而是“只真正跑了两章，且两章通过”。
- 当前覆盖事实是 `2 pass / 13 not_started`。
- 正确初步交付必须包含章节全部 pass、ReaderLab 全书总结 pass、baseline 横向对比和可迁移方法论 / Skill 草案。
- 本轮当时先把 15 个启动文件压到 7 个；随后 2026-07-01 文档真相层单独清理已进一步压成 2 个启动入口，见本账本顶部记录。
- baseline 已补具体路径和可用状态，不能再只写“几个 Skills”。

## 验证

- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 ReaderLab 《埃隆之书》完整闭环标准修正

## 摘要

- 用户再次纠正：本任务不能以“所有章节有结果”或“章节阶段完成”为结束标准。
- 正确初步交付标准是：15 个正文级章节全部 pass，ReaderLab 自己的全书总结 pass，仓颉 / 李继刚 / book-to-skill / 乔木等基线总结完成或纳入，读者评价 agent 完成横向对比，主控输出可迁移方法论 / Skill 草案，并通过验证。
- 本轮已重写 `docs/next-session-prompt.md`，将下一会话 prompt 改成完整执行合同，而不是旧的小样章 prompt。
- 已同步 `docs/current-task.md`、`docs/reports/readerlab-elon-chapter-loop-v0/README.md`、`docs/dev-state.md`、`docs/progress.md`。

## 关键约束

- 每章必须由两个 agent 分工：写作 agent 写，读者评价 agent 按 12 分 rubric 和硬门槛评。
- 主控 agent 回收结果并验收；通过才进入下一章。
- 每章最多五轮；五轮仍未 pass 时停止向后推进并记录 failure report，不能进入全书总结。
- 所有方法调整必须防过拟合：通用 method rule、book observation、rejected one-off fix 必须分开。
- final boss 只能在章节全部 pass 且 ReaderLab 全书总结 pass 后启动。

## 验证

- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

# 2026-07-01 ReaderLab 《埃隆之书》章节循环重启

## 摘要

- 用户打断指出：新方法只循环通过了一个章节，不能进入最终挑战池。
- 本轮收回阶段边界：当前只做《埃隆之书》章节级高阶讲解循环；全书总结和 final boss baseline 暂不启动。
- 旧 `readerlab-elon-method-bakeoff-v0/*` 和 `readerlab-elon-full-product-v1/*` 保留为未来证据库，但已在章节循环阶段被明确屏蔽，不能作为写作 agent 输入。

## 改动

- 新增 `docs/reports/readerlab-elon-chapter-loop-v0/README.md`
  - 定义章节循环当前阶段、baseline shield、章节循环契约、12 分读者 rubric、分数分层和 final boss gate。
- 新增 `docs/reports/readerlab-elon-chapter-loop-v0/rounds.md`
  - 记录《成功之道》和《打造卓越团队》的章节循环状态。
- 更新 `docs/eval-gates.md`
  - 补齐读者 12 分验收：重新理解、正文贴合、机制清晰、镜头有效、边界锋利、表达穿透。
  - 明确 Lens Auction 的 `>=7` 是内部镜头筛选分，读者 12 分是最终阅读验收分。
- 更新 `docs/current-task.md`
  - 明确当前只做章节循环，不提前进入全书总结或 baseline final boss。
- 更新 `docs/dev-state.md`、`docs/progress.md`
  - 记录阶段校正和当前两章通过事实。
- 更新《打造卓越团队》：
  - `docs/reports/readerlab-real-source-demo-v1/elon-team/reader/01_打造卓越团队_阅读页.md`
  - `docs/reports/readerlab-real-source-demo-v1/elon-team/audit/contracts/high-order-explanation.v1.json`
  - `docs/reports/readerlab-real-source-demo-v1/elon-team/audit/high-order-explanation.eval.md`

## 子 agent 结果

- 写作 agent 只允许读取本章正文和通用方法文档，不允许读取 final boss baseline。
- 写作候选标题：`团队不是人才名单，而是现实校正系统`。
- 读者评价 agent 结果：`pass`，`11/12`。
- P0/P1：none。
- P2：现实校正系统镜头有效，但未来可更具体反照原型、坏消息、总工程师思维和特种部队式团队之间的关系。

## 验证

- `rg` 检查《成功之道》《打造卓越团队》reader 页内部字段残留：PASS，无命中。
- `python3 -m json.tool docs/reports/readerlab-real-source-demo-v1/elon-team/audit/contracts/high-order-explanation.v1.json`：PASS。
- `python3 -m json.tool docs/reports/readerlab-real-source-demo-v1/elon-success/audit/contracts/high-order-explanation.v1.json`：PASS。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

## 当前结论

- 章节级方法探针：2 章通过，13 个正文级章节尚未开始。
- 新增 `docs/reports/readerlab-elon-chapter-loop-v0/chapter-queue.md` 作为后续唯一章节队列。
- 停在两章后是错误的阶段停止；正确下一步是 `组织设计 / v101-16`。
- 章节全部 pass 也不是任务结束，只是进入 ReaderLab 全书总结阶段。
- ReaderLab 全书总结 pass 后，还要进入其他 Skills / 方法基线全书总结、横向对比，以及最终方法论 / Skill 草案提炼。
- 全书总结：未启动。
- final boss baseline：未启动。
- 方法论 / Skill 草案：未启动。
- 生成器能力：未证明。
- product ready：未证明。

# 2026-06-30 ReaderLab 高阶讲解口径校准

## ChatGPT Pro 方案固化为 high-order-explanation.v1

- 用户要求先把 ChatGPT 导出方案整理进现有文档，避免上下文压缩丢失，再调整 PRD、方案和计划。
- 已读取 `~/Downloads/chatgpt-selected-2026-06-30T16-10-45.md` 并提炼为 ReaderLab 高阶讲解方法。
- 新增 `docs/high-order-explanation-method.md`：定义“认知升级讲解”的内部生产协议，包含 Source Anchor、Baseline Summary Trap、Upgrade Question、Mechanism Graph、Lens Auction、Judgment Gate、Natural Explanation 和 Delta Eval。
- 新增 `docs/contracts/high-order-explanation-v1.md`：定义高阶讲解 audit contract，记录正文锚点、普通总结陷阱、升维问题、机制图、镜头候选、吸收/降级/拒绝、reader-facing 自然讲解和 delta eval。
- 已同步 `AGENTS.md`、`README.md`、`docs/product-spec.md`、`docs/readerlab-package-spec.md`、`docs/ai-reading-method.md`、`docs/eval-gates.md`、`docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md`、`docs/decisions.md` 和 `docs/next-session-prompt.md`。
- 新增决策 D-049：`high-order-explanation.v1` 是下一轮样章执行协议，但尚未样章验证，不能视为产品能力成立。
- 范围控制：未改 reader 样张，未开发生成器，未写 LifeAtlas，未新增依赖。
- 追加修正：用户指出 `docs/next-session-prompt.md` 只写了框架名称和链路，不足以从 prompt 本身看出 GPT Pro 新框架；已将 Source Anchor、Baseline Summary Trap、Upgrade Question、Mechanism Graph、Lens Auction、Judgment Gate、Natural Explanation 和 Delta Eval 的操作细节、评分、镜头触发和失败条件直接补入 next-session prompt。

## 验证

- `rg -n "high-order-explanation|认知升级讲解|Source Anchor|Baseline Summary Trap|Upgrade Question|Mechanism Graph|Lens Auction|Judgment Gate|Delta Eval|吸收 / 降级 / 拒绝" ...`：PASS，活跃规格、方法、contract、状态和下一会话提示均已覆盖。
- `rg -n "尽量保留|正文选读导读|READY FOR HUMAN REVIEW|技术合伙人层|阅读路线|主题线索|处理过的一手正文" ...`：REVIEWED，命中均为历史账本、旧决策背景或当前失败条件，不作为活跃规格中的当前结论。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS，无输出。

## 摘要

- 用户明确：当前 real-source demo v1 的《埃隆之书》讲解不够通透，仍像普通书籍总结，不能体现 ReaderLab 的高阶陪读价值。
- 用户补充产品要求：AI 高阶讲解应高屋建瓴、有全局视角、能旁征博引，引入跨学科思维模型、历史观、产品/组织/工程经验和既往经历中的相似结构，把看似不同领域的底层逻辑串起来。
- 本轮结论：正文优先契约方向基本成立，但 AI 高阶讲解体验未通过；下一步先重做讲解口径和小样章，不继续加样本或开发生成器。

## 文档改动

- `docs/product-spec.md`
  - 将高阶讲解从“讲清楚材料”升级为“提供非摘要型认知增量”。
  - 增加跨学科模型、历史观、旁征博引、同构逻辑和来源边界要求。
- `docs/readerlab-package-spec.md`
  - 同步高阶讲解的 reader-facing 输出契约。
- `docs/ai-reading-method.md`
  - 在 Deepen / Reader Gain Gate 中加入 `cross_domain_lens`、`historical_pattern`、`reader_prior_connection` 等候选类型和判定要求。
- `docs/eval-gates.md`
  - 增加高阶讲解验收：必须有非摘要型认知增量，不能堆模型/堆名人/堆历史例子。
- `docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md`
  - 同步当前事实：real-source demo v1 不能标为 ReaderLab 体验通过，高阶讲解需要重做。
- `docs/decisions.md`
  - 新增 D-048：高阶讲解必须提供非摘要型认知增量。
- `docs/next-session-prompt.md`
  - 更新下一会话目标为重做 AI 高阶讲解口径和小样章。
- `README.md`
  - 在产品形态说明中加入高阶讲解的跨学科 / 全局视角要求。

## 当前结论

- 产品口径：UPDATED。
- 输出契约：仍成立，但只解决正文硬边界。
- 高阶讲解体验：当前 demo FAIL，不能视为 ReaderLab 体验通过。
- 下一步：在保留正文主体的前提下，重做小样章 AI 陪读层，验证它是否明显优于普通总结。

## 追加校准

- 用户补充：前述“查理芒格式跨学科模型、历史观、旁征博引、既往经历连接”等只是其当下能表达出的需求和意向，不是全部要求。
- 已同步到 `docs/product-spec.md`、`docs/decisions.md`、`docs/dev-state.md`、`docs/next-session-prompt.md`：高阶讲解仍必须讲清重点和要点，同时提供更大价值观和体系；具体知识结构不应被上述例子限制。

# 2026-06-30 ReaderLab 输出契约确认与落地

## 摘要

- 用户确认正文优先陪读包输出契约方向。
- 本轮不继续返工旧《埃隆之书》reader 页，不开发完整生成器，不写 LifeAtlas，不新增依赖。
- 输出契约落地范围：书籍/长文原样正文、Skill/工程净化正文、高阶讲解成段服务正文、技术负责人层输出设计资产卡、audit 与 reader-facing 分离。

## 文档改动

- `README.md`
  - 清理“下一轮返工《埃隆之书》第二部分读者页”的旧方向，改为先按输出契约选择小样本重做。
- `docs/product-spec.md`
  - 新增输出契约，覆盖书籍/长文、Skill/工程材料、高阶讲解、设计资产提炼和 audit 分离。
- `docs/readerlab-package-spec.md`
  - 新增包级输出契约，明确 `10_一手正文/`、`20_AI陪读/` 和 `audit/` 的分工。
- `docs/technical-cofounder-method.md`
  - 增加设计资产卡输出契约，强调面向产品负责人而非术语解释。
- `docs/eval-gates.md`
  - 增加输出契约验收，重命名旧技术合伙人口径为技术负责人 / 设计资产验收。
- `docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md`
  - 同步当前事实：输出契约已确认，下一步按契约选择小样本重做 reader-facing 样张。
- `docs/decisions.md`
  - 新增 D-047：正文优先陪读包采用输出契约作为样张前置门。
- `docs/next-session-prompt.md`
  - 更新下一会话目标为按已确认输出契约做最小样张。

## 当前结论

- 产品口径：CONFIRMED。
- 输出契约：DOCUMENTED。
- 旧《埃隆之书》reader experience：FAIL，仍不作为 product ready。
- 下一步：按输出契约选择一个小样本重做 reader-facing 样张，并通过人工 reader experience 审查。

# 2026-06-30 ReaderLab 产品规格收口：正文硬边界与设计资产提炼

## 摘要

- 用户明确：书籍/长文默认原样保留正文，不压缩、不改写、不用导读替代正文；除非明确要求整理原文，只做空格、空行、断行等轻量清理。
- 用户明确：Skill/工程材料需要净化正文，剥离安装命令、重复模板、执行外壳和机器噪音，但保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点。
- 用户明确：技术负责人层应面向产品负责人，替用户识别其不容易感知的工程和系统设计，并沉淀成可复用设计资产卡。
- 《埃隆之书》第二部分样张的 reader experience 撤回为 FAIL；source alignment 仍可作为 audit 证据。

## 文档改动

- `AGENTS.md`
  - 更新项目目的和边界：正文优先、书籍/长文原样正文、Skill/工程净化正文、设计资产提炼。
- `README.md`
  - 将产品形态从双轨陪读包细化为正文优先陪读包：一手正文轨、AI 陪读轨、设计资产轨。
  - 将 `technical-cofounder-notes.md` 口径改为 `design-asset-notes.md`。
- `docs/product-spec.md`
  - 写入书籍/长文默认原样保留正文的硬规则。
  - 写入 Skill/工程材料净化正文规则。
  - 将技术合伙人层重定义为技术负责人 / 设计资产提炼层。
- `docs/readerlab-package-spec.md`
  - 将 `01_材料方位图.md` 改为 `01_全局讲解.md`。
  - 将正文页主体改成 `正文 / 净化正文`，并明确 AI 讲解不能替代正文。
  - 将 `technical-cofounder-notes.md` 改为 `design-asset-notes.md`。
- `docs/technical-cofounder-method.md`
  - 重写为面向产品负责人的技术负责人 / 设计资产提炼方法。
- `docs/eval-gates.md`
  - 增加失败条件：书籍/长文正文被 AI 压缩、改写或导读替代；Skill/工程材料没有净化正文；技术负责人层没有设计资产提炼。
- `docs/decisions.md`
  - 新增 D-046：书籍正文原样保留，Skill 正文净化，技术负责人层沉淀设计资产。
- `docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md`、`docs/next-session-prompt.md`
  - 同步当前唯一切片：输出契约收口，而不是继续返工旧《埃隆之书》reader 页。
- `docs/reports/readerlab-elon-source-aligned-demo-v0/README.md`
- `docs/reports/readerlab-elon-source-aligned-demo-v0/audit/eval.md`
  - 将 reader experience 状态改为 FAIL；保留 source alignment PASS。

## 当前结论

- source alignment：PASS，只说明 audit 层可追溯。
- reader experience：FAIL，旧样张没有原样正文的一手轨。
- product capability：NOT ESTABLISHED。
- 下一步：设计新输出契约，再基于契约重做最小样张。

# 2026-06-30 ReaderLab reader-facing 原型返工：埃隆之书第二部分

## 摘要

- 本轮按用户 `/goal` 只返工《埃隆之书》第二部分 reader-facing 原型样张。
- 未进入第二类真实材料迁移测试，未开发完整生成器，未写 LifeAtlas，未新增依赖，未安装或启用新 Skill。
- source alignment 仍保留在 `audit/source-alignment.md`；reader 页已从审计报告式页面改成材料方位图和章节/单元陪读。

## 改动

- `docs/reports/readerlab-elon-source-aligned-demo-v0/reader/00_全书地图.md`
  - 改成自然读者语言的材料方位图。
  - 回答这本书讲什么、全书怎样组织、第二部分在全书中的位置和当前样张覆盖边界。
  - 移除主阅读页里的内部 source refs、状态字段和审计表达。
- `docs/reports/readerlab-elon-source-aligned-demo-v0/reader/01_大单元深读.md`
  - 改成第二部分章节/单元陪读页。
  - 每节使用“正文选读导读 / AI 旁批 / 误读提醒”，并明确导读不替代原书原文。
  - 移除“原文对应 / 降级拒绝理由”作为主内容的审计式结构。
- `docs/reports/readerlab-elon-source-aligned-demo-v0/audit/eval.md`
  - 改成三层评估：source alignment PASS，reader experience READY FOR HUMAN REVIEW，product capability NOT ESTABLISHED。
- `docs/reports/readerlab-elon-source-aligned-demo-v0/README.md`
  - 同步目录口径，说明当前是 reader-facing 原型样张，不是 product ready。
- `docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md`
  - 同步当前状态和下一步：先做人工读者体验复核，再决定是否进入第二类真实材料迁移测试。

## 验证

- `rg -n "source ref|source refs|claim trace|machine_status|human_status|heading path|降级|拒绝|Route|阅读路线|主题线索|处理过的一手正文" docs/reports/readerlab-elon-source-aligned-demo-v0/reader`：PASS，无命中。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS，无输出。

## 当前结论

- source alignment：PASS，审计层可追溯。
- reader experience：READY FOR HUMAN REVIEW，已完成第一轮返工，但仍需用户人工判断。
- product capability：NOT ESTABLISHED，本轮只证明手工 reader-facing 原型方向，不证明生成器能力。

## 下一步

- 用户人工审查返工后的 reader 页，重点判断 3 分钟方位感、正文/旁批边界、误读提醒是否自然，以及页面是否像正常 ReaderLab 输出。
- 人工审查通过后，再进入第二类真实材料迁移测试；不直接进入完整生成器或 LifeAtlas 正式沉淀。

# 2026-06-30 ReaderLab 读者原型校准：source alignment 通过但 reader experience 未通过

## 摘要

- 用户人工反馈指出：当前《埃隆之书》source-aligned 长样张虽然通过来源追溯对抗审查，但读者页不像未来正常使用 ReaderLab Skill 时会看到的东西。
- 主要偏差：读者页暴露 `source refs`、机器状态、审计字段和降级/拒绝理由；“阅读路线 / 主题线索 / 处理过的一手正文”等概念既不像给机器看的 contract，也不像给人看的读书介绍。
- 校准结论：`Route` / 阅读路由保留为内部结构定位方法；reader-facing 页面改用“材料方位图 / 章节位置说明 / 正文选读 / AI 旁批 / 误读提醒”的自然读者语言。
- 进度已从 68/100 下调到 64/100；产品形态与方向治理从 close 退回 working。

## 文档改动

- `docs/decisions.md`：新增 D-045，明确读者页必须提供方位感，不暴露内部路线和审计结构。
- `docs/product-spec.md`、`docs/readerlab-package-spec.md`、`docs/ai-reading-method.md`、`docs/eval-gates.md`、`README.md`：把产品原型口径从“阅读路线/主题线索”校准为材料方位图、章节位置说明和审计后置。
- `docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md`、`docs/next-session-prompt.md`：下一阶段任务改为返工《埃隆之书》第二部分 reader-facing 原型样张；暂不进入第二类材料迁移测试或完整生成器。

## 当前结论

- source alignment：PASS。
- reader experience：FAIL / needs_redesign。
- product ready：NO。
- 生成器能力：NO。

# 2026-06-30 ReaderLab 样本质量闭环：埃隆之书 source-aligned 长样张 v0

## 对抗审查修复

- 修正 `readerlab-elon-source-aligned-demo-v0` 的 source alignment：组织壁垒、短路径沟通、速度/紧迫性、并行推进和制造 heading path 按旧 `location-map.v1.json` 拆回对应 refs。
- 样张仍保持 repo 内、第 2 闭环、`human_status=pending`；未写 LifeAtlas，未声称 product ready。
- 对抗审查复审：PASS；剩余风险是旧 `location-map.v1.json` 质量、短摘录不能替代人工读 EPUB、读者收益仍需用户判断。

## 摘要

- 本轮按固定 7 个闭环推进 `2. 样本质量闭环：书籍局部样本 + Skill/工程局部样本`。
- 用户指出上一轮 toy sample 信息量不足、原文对应弱，不能展示 ReaderLab 水平。
- 本轮交付 repo 内《埃隆之书》source-aligned 长样张 v0；已通过对抗审查复审。后续人工反馈判定 reader experience 未通过，见本文件顶部最新记录。
- 未写 LifeAtlas，未新增依赖，未声称 product ready，未声称半自动生成器能力。

## 产物

- `docs/reports/readerlab-elon-source-aligned-demo-v0/README.md`
- `docs/reports/readerlab-elon-source-aligned-demo-v0/reader/00_全书地图.md`
- `docs/reports/readerlab-elon-source-aligned-demo-v0/reader/01_大单元深读.md`
- `docs/reports/readerlab-elon-source-aligned-demo-v0/audit/source-alignment.md`
- `docs/reports/readerlab-elon-source-aligned-demo-v0/audit/eval.md`

## 来源边界

- 原 EPUB：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 复用位置索引：`docs/reports/readerlab-elon-full-product-v0/contracts/location-map.v1.json`
- 复用全书/局部 contract 候选作为 refs 背景；本轮新产物是 reader-facing 长样张，不把旧样张说成合格产品。

## 内容范围

- 全书地图：主问题、结构地图、主题线索、pending 结论。
- 大单元深读：第二部分“极限硬核工作”，覆盖责任归属、深度理解、团队密度、短路径沟通、算法之道、速度与并行、制造系统。
- 每个关键段落包含 source ref、EPUB spine、短摘录、处理后的一手正文、AI 深读、降级/拒绝理由。

## 验证

- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS，无输出。

## 剩余风险

- 尚未人工审查。
- 只覆盖一个大单元，不是整本书最终产品包。
- 本轮没有重新生成 JSON contract，只复用旧 location-map 和 EPUB 抽取边界。

# 2026-06-30 ReaderLab Agent workflow / report-md 前置切片

## 摘要

- 本轮完成 Agent workflow / 半自动生成器前置切片的机器侧第一版。
- 仍然不开发完整生成器，不写 LifeAtlas，不新增依赖，不证明人工阅读质量通过。
- human gate 仍为 pending。

## 文档改动

- `docs/agent-workflow.md`
  - 明确 script / Agent / human 三者边界。
  - 定义输入准备、语义建模、确定性渲染、机器评估与报告、人工审查五阶段。
  - 明确失败路径：缺来源、空来源、缺 refs、reader/audit 混淆、一手正文缺失、output-eval gate 缺失、机器冒充 accepted 等都不能继续。

## 代码改动

- `scripts/readerlab.py`
  - `eval-rendered-package <path>` 新增 `--report-md <path>`。
  - 成功和失败都可写 Markdown 报告。
  - 报告包含 target、`validate_contract_passed`、contract count、schemas、5 个 runner gate、failures、machine / human 边界。
  - 报告默认拒绝覆盖已有文件；只有显式 `--overwrite-report` 才替换。
  - 报告拒绝写入 `/Users/tianqiang/LifeAtlas`。
- `tests/test_readerlab.py`
  - 增加成功报告测试：确认报告包含 5 个 runner gate 和 `human_status pending` 边界。
  - 增加失败报告测试：确认非零退出时仍写报告，并包含失败 gate 和失败原因。
  - 增加报告路径安全测试：已有报告默认不覆盖，`--overwrite-report` 才覆盖，LifeAtlas 路径拒写。

## 验证

- `python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py`：PASS。
- `python3 tests/test_readerlab.py`：30 tests OK。
- `python3 scripts/readerlab.py render-contract-package docs/reports/readerlab-contract-validator-proof-v0/book-longform-sample /private/tmp/readerlab-workflow-book-20260630-codex`：PASS，生成 1 个 reader 页。
- `python3 scripts/readerlab.py render-contract-package docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample /private/tmp/readerlab-workflow-skill-20260630-codex`：PASS，生成 2 个 reader 页。
- `python3 scripts/readerlab.py eval-rendered-package /private/tmp/readerlab-workflow-book-20260630-codex --report-md /private/tmp/readerlab-workflow-book-report-20260630-codex.md`：PASS，5 个 runner gate 全部通过。
- `python3 scripts/readerlab.py eval-rendered-package /private/tmp/readerlab-workflow-skill-20260630-codex --report-md /private/tmp/readerlab-workflow-skill-report-20260630-codex.md`：PASS，5 个 runner gate 全部通过。
- 已存在 report 路径退化测试：默认返回非零退出码，并保留原文件内容；显式 `--overwrite-report` 才覆盖。
- LifeAtlas report 路径退化测试：返回非零退出码，并报告 `refusing to write eval report under LifeAtlas`。
- 对抗子 Agent 复查过程：
  - 首轮：NO PASS，指出 `--report-md` 默认覆盖已有文件且可误写 LifeAtlas。
  - 二轮：PASS；确认默认不覆盖、`--overwrite-report` 才覆盖、LifeAtlas 路径拒写，且没有发现新的高优先级 false pass。

## 剩余风险

- `docs/agent-workflow.md` 是半自动生成器前置 workflow，不是完整生成器实现。
- report-md 是机器评估报告，不是人工验收结论。
- 当前两个报告证明 proof 样本链路可运行，不证明真实材料迁移稳定。
- 人工读者收益、页面品味、字段负担和是否进入 LifeAtlas 正式沉淀仍需用户判断。

## 下一步

- 选项 A：用户先人工审查两个 `/private/tmp` renderer 输出和 Markdown eval 报告，判断读者收益与字段负担。
- 选项 B：选择一个非 proof、非 gstack 的小型真实材料做第二类迁移测试，仍只写 `/private/tmp`，不写 LifeAtlas。

# 2026-06-30 ReaderLab renderer / eval runner 最小工程闭环

## 摘要

- 本轮完成 Markdown renderer / output-eval runner 最小工程切片。
- 仍然不开发完整生成器，不写 LifeAtlas，不新增依赖，不证明人工阅读质量通过。

## 代码改动

- `scripts/readerlab.py`
  - 新增 `render-contract-package <sample_dir> <output_dir>`。
  - renderer 从 proof 样本的 contract JSON 和 `audit/source-excerpts` 生成 reader-facing markdown，不复制既有 reader 页。
  - renderer 对缺失或空的 source excerpt 硬失败，避免生成没有一手正文的空壳 reader 页。
  - renderer 复制 audit 层到输出包，保留 source-registry、location-map、contracts、source-excerpts 和 rejected/downgraded。
  - 长文样本生成 `reader/01_局部长文阅读页.md`。
  - Skill/工程样本生成 `reader/01_工程材料阅读页.md` 和 `reader/02_技术合伙人旁批.md`。
  - 新增 `eval-rendered-package <path>`，复用 `validate-contract`，并额外检查 reader markdown、reader/audit 分离、一手正文段回链 source excerpts、output-eval 9 gate 和 `human_status` 不冒充 accepted。
- `tests/test_readerlab.py`
  - 增加 renderer 两样本正向测试。
  - 增加 renderer 输出通过 `validate-contract` 的回归测试。
  - 增加 eval runner 两样本正向测试。
  - 增加删除 source excerpt、删除 reader 页、删除一手正文段、删除 eval gate、把 `human_status` 改成 `accepted` 的失败测试。

## 验证

- `python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py`：PASS。
- `python3 tests/test_readerlab.py`：26 tests OK。
- `python3 scripts/readerlab.py render-contract-package docs/reports/readerlab-contract-validator-proof-v0/book-longform-sample /private/tmp/readerlab-render-book-20260630-codex`：PASS，生成 1 个 reader 页。
- `python3 scripts/readerlab.py render-contract-package docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample /private/tmp/readerlab-render-skill-20260630-codex`：PASS，生成 2 个 reader 页。
- `python3 scripts/readerlab.py validate-contract /private/tmp/readerlab-render-book-20260630-codex`：PASS，5 contracts。
- `python3 scripts/readerlab.py validate-contract /private/tmp/readerlab-render-skill-20260630-codex`：PASS，4 contracts。
- `python3 scripts/readerlab.py eval-rendered-package /private/tmp/readerlab-render-book-019f17fa-fix`：PASS，5 个 runner gate 全部通过。
- `python3 scripts/readerlab.py eval-rendered-package /private/tmp/readerlab-render-skill-019f17fa-fix`：PASS，5 个 runner gate 全部通过。
- 缺失 `audit/source-excerpts/longform-fragment.md` 的退化样本：`render-contract-package` 返回非零退出码，并报告 `source excerpt not found`。
- 只保留 source path、删除实际一手正文的退化样本：`eval-rendered-package` 返回非零退出码，并报告 `reader markdown missing actual first-hand body from source excerpts`。
- 对抗子 Agent 复查过程：
  - 首轮：NO PASS，指出缺 source excerpt false-pass。
  - 二轮：NO PASS，指出只保留 source path、没有实际一手正文仍 false-pass。
  - 三轮：PASS；确认缺 source excerpt、空 source excerpt、source-path-only reader 页都会失败。

## 剩余风险

- renderer 只支持当前两个 proof 样本形态：catalog-map 长文局部样本和 capability-map 工程样本。
- renderer 不是 provider-backed 生成器，也不做真实材料解析。
- eval runner 是最小机器 gate，不是 blind A/B、provider-backed eval 或人工验收。

## 下一步

- 进入 Agent workflow / 半自动生成器前置切片。
- 明确脚本、Agent 判断、人工验收三者边界。
- 用当前 renderer 输出做人工读者收益审查，再决定是否进入第二类真实材料迁移测试。

# 2026-06-30 ReaderLab contract validator 对抗修复收口

## 摘要

- 对抗子 Agent 初审发现一个阻塞 false-pass：删除 Skill/工程样本的第三个 capability domain 后，`validate-contract` 仍会通过。
- 主 Agent 修复后，对抗子 Agent 二次复查 PASS。
- 本轮仍然只证明 contract / validator / two-sample proof 的最小工程闭环，不证明完整生成器能力，也不证明人工阅读质量通过。

## 修复内容

- `scripts/readerlab.py`
  - `source-registry` 要求来源不能是空壳对象：必须有 `source_path` 或 `title`。
  - `location-map` 要求位置必须挂回 `source_id`，并有 `path` 或 `range`。
  - `output-eval.v1` 必须覆盖 9 个最小必检项。
  - refs 必须回链到 package 内 source/location known ids。
  - `capability-map.v1` 新增包级 primary module 覆盖检查：`source_role=primary_module` 的来源必须通过 location-map 映射到 location refs，并被 capability domains 覆盖。
- `tests/test_readerlab.py`
  - 增加缺失 eval gate、未知 refs、空壳 source/location、reader/audit 混淆、reader-facing 正文退化、capability-map 模块漏覆盖等负向测试。
- proof 样本
  - 长文样本和 Skill/工程样本的 reader-facing 正文不再只是摘要。
  - Skill/工程样本 capability-map 覆盖入口路由、证据读取、输出评估三个模块。

## 验证

- `python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py`：PASS。
- `python3 tests/test_readerlab.py`：22 tests OK。
- `python3 scripts/readerlab.py validate-contract docs/reports/readerlab-contract-validator-proof-v0/book-longform-sample`：PASS，5 contracts。
- `python3 scripts/readerlab.py validate-contract docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample`：PASS，4 contracts。
- 对抗子 Agent 复查：PASS；删除 `output-eval-gate` 后包级校验会失败，并报告 `capability-map 未覆盖 primary_module location refs：loc-output-eval-status`。

## 下一步

- 下一轮进入 Markdown renderer / output-eval runner 最小工程切片。
- 不直接开发完整生成器，不把当前 proof 样本说成 product ready。

# 2026-06-30 ReaderLab contract validator 最小闭环

## 摘要

- 本轮按唯一执行切片完成 contract / validator / two-sample proof 最小开发闭环。
- 未开发完整生成器，未写 LifeAtlas，未新增依赖，未安装或启用新 Skill。

## 代码改动

- `scripts/readerlab.py`：新增 `validate-contract <path>` CLI，支持样本目录和单个 contract JSON 文件。
- validator 最小检查覆盖：
  - high-level claim 必须有 source refs。
  - coverage 不足时不能生成 `grounded-global-map`。
  - `machine_status` 和 `human_status` 必须分开。
  - reader-facing 与 internal audit 必须分开。
  - `local-deepread` 必须有 `reader_gain`、`primary_refs`、`boundary`、`confidence`。
  - `capability-map` 必须包含 trigger signals、near-neighbor exclusions、method atoms、required inputs、output contract、verification、route decisions。
  - `output-eval` 必须表达检查项和状态。

## 样本产物

- `docs/reports/readerlab-contract-validator-proof-v0/book-longform-sample/`
  - 书籍/长文局部样本。
  - 包含 `source-registry.v1`、`location-map.v1`、`catalog-map.v1`、`local-deepread.v1`、`output-eval.v1`、`rejected-downgraded.md` 和 reader-facing markdown。
- `docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample/`
  - Skill/工程材料 2-3 模块样本。
  - 包含 `source-registry.v1`、`location-map.v1`、`capability-map.v1`、`output-eval.v1`、`rejected-downgraded.md`、reader-facing markdown 和技术合伙人旁批。

## 测试与验证

- `python3 tests/test_readerlab.py`：20 tests OK。
- `python3 scripts/readerlab.py validate-contract docs/reports/readerlab-contract-validator-proof-v0/book-longform-sample`：PASS，5 contracts。
- `python3 scripts/readerlab.py validate-contract docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample`：PASS，4 contracts。
- `python3 scripts/readerlab.py validate-contract docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample/audit/contracts/capability-map.v1.json`：PASS，单文件 contract 校验可用。

## 剩余风险

- validator 是最小规则检查，不是完整 JSON schema 系统。
- 两个样本是 repo 内 proof，不是生成器自动产物。
- 人工阅读质量仍为 `pending`，validator 通过不能说成 human accepted。
- 没有验证真实复杂材料全量生产，也没有进入 Markdown renderer。

# 2026-06-30 ReaderLab 产品方案重设与正式开发前准备

## 摘要

- 用户引入外部强模型建议后，要求不要继续被旧 `current-task.md` 和 Combo-B 局部任务牵引。
- 本轮按用户确认，完成正式开发前文档和任务入口重置。
- 本轮不改代码，不写 LifeAtlas，不新增依赖，不开发完整生成器。

## 产物

- `README.md`：改为复杂材料吸收系统 / 双轨陪读包产品入口。
- `docs/product-spec.md`：新增产品规格。
- `docs/readerlab-package-spec.md`：新增目标阅读包结构。
- `docs/ai-reading-method.md`：新增 E-R-D-D AI 阅读方法。
- `docs/technical-cofounder-method.md`：新增技术合伙人 / Design Atom Analysis 方法。
- `docs/eval-gates.md`：新增正式开发前验收 gate。
- `docs/current-task.md`：下一轮改为 contract / validator / two-sample proof。
- `docs/dev-state.md`：同步新产品目标、方法骨架和实现事实。
- `docs/progress.md`：按新产品范围重设进度口径，当前估算 45/100。
- `docs/next-session-prompt.md`：重写下一会话启动提示。
- `AGENTS.md`：更新启动顺序、关键入口和项目边界。
- `docs/decisions.md`：新增 D-040 到 D-044，约束方向重估、双轨陪读包、E-R-D-D、技术合伙人层和 contract-first 路线。

## 结论

- 旧结构化提炼和 Combo-B 相关产物保留为局部能力证据，不再作为项目主线。
- ReaderLab 正式产品方案是：一手正文轨 + AI 陪读轨 + audit/contracts/eval 事实层。
- 下一轮正式开发从 contract / validator / two-sample proof 的最小闭环开始。

## 验证

- 本轮为文档和任务入口调整，没有代码改动。
- 已执行文档一致性搜索和关键文件读取。
- 已运行 `python3 tests/test_readerlab.py`，18 tests OK。

# 2026-06-30 ReaderLab 结构化提炼同题多路线对照 v0

## 摘要

- 按用户要求和 D-039，主 Agent 开多 Agent 做同题对照，检验“只抽取某个仿型的一环是否可靠”和“组合后是否真有 1+1>2”。
- 本轮不继续扩写《埃隆之书》，不改生成器，不写 LifeAtlas，不新增依赖。
- 新增 repo 内报告：`docs/reports/readerlab-structured-extraction-bakeoff-v0/`。

## 路线与结果

- Cangjie-only：候选生成、筛选和通过/降级/拒绝最强；但读者体验和 source-grounded 弱，不适合作独立主链。
- Li Jigang-only：材料定性、缺口判断、机制传导最强；但候选筛选和来源复核不够工程化，不适合作独立主链。
- ReaderLab-current-chain：字段和链路齐，但主要复现已有手工判断，作为 baseline 和契约雏形，不作为胜出路线。
- Combo-A：李继刚定性 -> 仓颉筛选 -> source-grounded 后置，有组合增益但后置来源审计容易变成事后补证。
- Combo-B：source-grounded 前置 -> 仓颉筛选 -> 李继刚受控表达，暂时胜出，作为下一轮候选主链。

## 源文抽查

- `v101-16.xhtml`：算法之道顺序明确，删除在优化、加速、自动化之前。
- `v101-14.xhtml`：睡工厂是紧急状态边界，不可常态化。
- `v101-18.xhtml`：工厂即产品，制造系统本身是产品能力。
- `v101-11.xhtml`：第一性原理和成本拆解。
- `v101-27.xhtml`：多行星叙事需外部核验。
- `v101-29.xhtml`：69 法则是混合索引，不能整体升格。

## 产物

- `docs/reports/readerlab-structured-extraction-bakeoff-v0/README.md`
- `docs/reports/readerlab-structured-extraction-bakeoff-v0/routes/01_同题路线摘要.md`
- `docs/reports/readerlab-structured-extraction-bakeoff-v0/audit/90_同题多路线评估.md`
- `docs/reports/readerlab-structured-extraction-bakeoff-v0/assertions.md`
- `docs/progress.md`：总进度从 44/100 更新为 48/100；结构化提炼从 8/18 更新为 12/18。
- `docs/current-task.md`、`docs/dev-state.md`：下一轮切片改为 Combo-B 轻量模板、blind A/B 和第二类材料迁移测试。

## 结论

- 单抽某一仿型环节不天然可靠：仓颉筛选需要主问题和来源边界，李继刚表达需要候选筛选和反升格边界，source-grounded 需要 fresh parse 和人工 spot-check。
- 多个好环节拼在一起也不天然胜出；Combo-B 暂时胜出是因为三个环节形成阻断关系，而不是字段更多。
- Combo-B 只进入下一轮验证，不是 product ready、不是生成器能力、不是正式生产链。

## 剩余风险

- 未做 blind A/B。
- 未做第二类材料迁移测试。
- 未形成完整 fresh source-grounded contract。
- 未做人工验收，也未机制化到 `scripts/readerlab.py`。

## 验证

- 主 Agent 复核五条路线 worker 输出和独立评估 worker 输出。
- 主 Agent 做关键 EPUB 片段抽查。
- 本轮是文档侧评估产出，没有代码改动；未运行代码测试。

# 2026-06-30 ReaderLab 结构化提炼最小闭环

## 用户补充护栏

- 用户指出：只学习某个 Skill 或仿型的一个环节不一定可靠，因为该环节可能服务于下一环，脱离原方法链路后质量会下降。
- 用户进一步指出：不只是不能破坏上下游依赖，还必须证明抽出的几个部分组合后有 1+1>2 的效果；否则优秀环节拼在一起也可能不能工作。
- 用户建议下一轮应开多个 Agent 做同题对比：仓颉-only、李继刚-only、多种组合路线分别产出，再比较哪种效果更好。
- 主 Agent 接受该风险判断，并把它升级为耐久护栏：新增 D-038，要求抽取仿型局部环节前必须做上下游依赖与组合增益审查。
- 主 Agent 进一步新增 D-039：组合增益必须用同题多路线对照证明；组合不胜出时必须给出倾向性处理方案，而不是继续拼接。
- 已同步更新 `docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md` 和 `docs/reports/readerlab-structured-extraction-min-loop-v0/`。
- 当前结论被收窄：本轮“李继刚定性 + 仓颉筛选 + source-grounded 边界”只是在手工重考中方向成立，不能直接视为稳定模块化拼接方案；下一轮必须证明组合后优于单一路线和旧 ReaderLab 输出。

## 摘要

- 本轮按用户 `/goal` 继续 ReaderLab，但不扩写《埃隆之书》样张，不拼接所有仿型能力，而是补第一短板：结构化提炼。
- 主 Agent 调度四个子 Agent：旧输出诊断、仿型能力矩阵、Meta Skill 横向裁判、《埃隆之书》小范围重考。子 Agent 结果由主 Agent 复核后收口。
- 新增 repo 内报告：`docs/reports/readerlab-structured-extraction-min-loop-v0/`。
- 本轮未改 `scripts/readerlab.py`，未新增依赖，未写 LifeAtlas `300/600/800`，未安装或启用 Skill。

## 产物

- `README.md`：本轮结论、输入证据、主 Agent 取舍和边界。
- `reader/01_结构化提炼小范围重考.md`：材料定性、主问题、候选池、通过/降级/拒绝、全书主线、部件 II 地图和 5 个亮点提炼。
- `audit/90_结构化提炼评估.md`：旧输出诊断、三个粒度共同问题、仿型能力矩阵、Meta Skill 裁判、output risk、新旧对比和最终判断。
- `assertions.md`：SE-A01 到 SE-A12 全部 pass，明确剩余风险。
- `docs/progress.md`：总进度从 39/100 更新为 44/100；结构化提炼从 working-low 更新为 working。
- `docs/current-task.md`、`docs/dev-state.md`：同步下一轮切片为结构化提炼机制化前验证。

## 结论

- ReaderLab 当前哪门课弱：结构化提炼。全书地图、章节/部件地图、亮点提炼不是三套功能，而是一套主干判断能力。
- 旧输出共同失败：没有把主问题、部件功能、亮点选择、降级边界和来源范围串成同一条可验证链。
- 本轮立即学习：李继刚式深读的定性和机制传导、仓颉的候选池和通过/降级/拒绝、source-grounded 的来源边界。
- 本轮储备：乔木共读、book-to-skill、blind A/B、provider-backed eval、多材料扩测。
- 本轮不吸收：候选池页面外观、长篇论文形态、工具链扩展、把 Meta Skill 当阅读输出模板。

## 剩余风险

- 新报告仍是手工闭环，不是 product ready。
- 没有 fresh source-grounded contract。
- 没有人工逐段 spot-check。
- 没有 blind A/B 或 provider-backed output eval。
- 没有生成器机制化，也没有正式 Skill。

## 验证

- 主 Agent 检查了旧输出、method bakeoff、candidate evidence、Meta Skill 方法文件和四个子 Agent 报告。
- 本轮是文档侧样张和评估产出，没有代码改动；未运行代码测试。

# 2026-06-30 ReaderLab 路线收束与进度治理

## 摘要

- 用户指出当前体验像“永远马上完工但永远没完工”，要求把旧的、错的上下文删掉或压下去，建立可执行方案和模块化进度管理。
- 用户随后补充两条下一轮 prompt 要求：明确主 Agent / 子 Agent 调度方式；在横向环评中引入 Meta Skill 作为评估裁判并产出报告建议。
- 本轮不继续产样张，不改 `scripts/readerlab.py`，不写 LifeAtlas，不新增依赖。
- 核心路线修正：ReaderLab 不再从仿型功能出发拼装，而是从自身短板出发学习对应仿型的解题逻辑。
- 当前第一短板定为“结构化提炼”：全书地图、章节地图、重点/亮点提炼背后是同一套能力。

## 文档更新

- `AGENTS.md`：Memory Map 加入 `docs/progress.md`。
- `docs/current-task.md`：重写为当前唯一切片，下一轮只做结构化提炼最小闭环。
- `docs/dev-state.md`：压缩为当前事实、作废旧口径、模块状态和下一步。
- `docs/progress.md`：新增进度板，当前估算 39/100；记录本轮新增 +2、扣减 -4、净 -2。
- `docs/decisions.md`：新增 D-034 到 D-037，分别约束短板驱动吸收、结构化提炼统一能力、每轮大迭代必须更新进度板、Meta Skill 横向能力评估裁判。
- `docs/next-session-prompt.md`：重写为结构化提炼最小闭环目标。

## 当前进度结论

- 当前项目不是马上 product ready。更准确状态是：基础工程闭环可用，样张探索产生证据，但核心阅读智能仍处在 working-low。
- 历史判断：当时曾把 `docs/progress.md` 设为后续大迭代进度层；该口径已被 2026-07-01 D-051 收窄，`docs/progress.md` 现在只保留历史快照，不是当前事实源。

## 下一步

- 做结构化提炼最小闭环：旧输出缺陷诊断 -> 仿型能力矩阵 -> 生产链抽取 -> 《埃隆之书》小范围重考 -> 对比旧输出 -> 更新进度板。

# 2026-06-30 ReaderLab DBS capability v1

## 摘要

- 按当前目标继续做 `dbs-suite` 样张反测：实施 worker 创建 `docs/reports/readerlab-dbs-suite-capability-v1/`，主 Agent 初审并跑覆盖/引用检查，对抗审查 worker 复审。
- v1 修正旧 demo 的核心问题：不再用 7 个代表样本冒充整包能力地图，而是覆盖 canonical package 当前 24 个 upstream `SKILL.md`，并按 `capability-map.v1` 组织能力域、触发、边界、方法原子、输出契约、验收、跨 Skill 路由和读者路线。
- 对抗复审结论：PASS，但限定为“repo 内手工试产样张可交付”；不是 product ready、不是生成器稳定能力、不是安装或启用 `dbs-suite`。

## 产物

- `README.md`：v1 状态、覆盖、文件清单和验证命令。
- `reader/01_能力地图.md`：读者可读能力地图，按真实任务选择和输出验收组织，不混入 hash、validator、machine status 等审计噪音。
- `contracts/source-registry.v1.json`：25 个来源，其中 24 个是 upstream `SKILL.md`，另有 package metadata。
- `contracts/location-map.v1.json`：24 个 Skill location，每个 Skill 至少一个可回链位置。
- `contracts/capability-map.v1.json`：8 个能力域、7 条 cross-skill routes、3 条 reader routes、24/24 covered units。
- `audit/90_来源与审计.md`：人工 pending、未写 LifeAtlas、未改 canonical package、辅助资产未深审等边界。
- `audit/method-absorption.md`：capability-map、source/location、reader/audit、Meta Skill output eval 等方法如何落到 v1。
- `assertions.md`：DBS-A01 到 DBS-A11，全部 pass。

## 验证和审查

- 主 Agent 复跑：
  `python3 tests/test_readerlab.py`
  `jq empty docs/reports/readerlab-dbs-suite-capability-v1/contracts/source-registry.v1.json docs/reports/readerlab-dbs-suite-capability-v1/contracts/location-map.v1.json docs/reports/readerlab-dbs-suite-capability-v1/contracts/capability-map.v1.json`
  `comm -3 <(canonical 24 SKILL.md dirs) <(capability-map covered_units)`
  source/location/capability refs 悬空检查脚本。
- 结果：18 tests OK；三个 JSON 语法 OK；24 个 canonical Skill 目录与 `covered_units` 完全一致；source/location/capability 引用 0 悬空；读者稿未命中 `hash|validator|machine_status|delivery_status|content_hash`。
- 对抗审查 worker 复审：PASS（按 v1 手工试产样张口径）。

## 剩余风险

- 人工阅读质量仍为 `pending`。
- 没有真实用户任务路由反测，尤其 `dbs-diagnosis` / `dbs-good-question` / `dbs-goal` / `dbs-action` 和内容链路之间的优先级。
- `dbs-content-system/tools`、templates、scaffold、docs 和 `dbs-wechat-html/templates/styles.md` 只做存在性登记，未做执行完整性审计。
- 这仍是手工试产包，不证明 ReaderLab 生成器稳定能力。

# 2026-06-30 ReaderLab Elon full product v1

## 摘要

- 基于 method bakeoff 结论，实施 worker 重做《埃隆之书》v1，写入 `docs/reports/readerlab-elon-full-product-v1/`。
- v1 不修补 v0 的 5 个短 reader 页，而是收敛为一篇主阅读稿，并把来源、方法吸收和候选证据放到审计附录。
- 对抗审查第一轮判定 PARTIAL：v1 明显回应了 v0 的碎片化、type 标签、空泛路线等问题，但 `ELON-A10`、仓颉候选证据链和能力候选验证仍不足。
- 实施 worker 随后补 `audit/candidate-evidence.v1.json`，把候选筛选、V1/V2/V3、5 个能力候选和 heading/block/char refs 审计链放入 v1 审计层。
- 对抗复审结论：PASS，但限定为“v1 手工试产样张可交付”；不是 product ready、不是生成器能力、不是正式 Skill。

## 产物

- `README.md`：打开顺序、v1 相对 v0 的主要变化、非 product ready 边界。
- `reader/01_主阅读稿.md`：唯一读者主稿，覆盖材料边界、缺口/增量/不增量、机制链、候选筛选、正文附近批注触发、认知旅程和 5 个候选能力。
- `audit/90_来源与审计.md`：来源、状态、验证边界和后续人工复核点。
- `audit/method-absorption.md`：仓颉、李继刚式深读、乔木共读、book-to-skill 和 ReaderLab 的职责分层。
- `audit/candidate-evidence.v1.json`：35 个精简 location refs、11 个候选筛选项、5 个能力候选和未解决边界。
- `assertions.md`：V1-A01 到 V1-A12、ELON-A01 到 ELON-A13 自检；`ELON-A10=partial_pass`。

## 验证和审查

- 主 Agent 复跑：
  `python3 tests/test_readerlab.py`
  `python3 scripts/readerlab_fullbook_demo_validate.py`
  `jq empty docs/reports/readerlab-elon-full-product-v1/audit/candidate-evidence.v1.json`
- 结果：18 tests OK；旧 fullbook demo validator PASS；candidate evidence JSON 语法 OK。
- 对抗审查 worker 复审：PASS（按 v1 手工试产样张口径）。

## 剩余风险

- 人工阅读质量仍为 `pending`。
- `candidate-evidence.v1.json` 继承 v0 location map，不是 fresh parse 生成的正式 v1 source-grounded contract。
- 5 个能力仍是候选能力，没有 `SKILL.md`、trigger eval、output eval、测试或误用审查。
- 文明风险、AI、监管、人口、多行星等判断仍需外部验证，不能凭本书直接固化为事实。

# 2026-06-30 ReaderLab Elon method bakeoff v0

## 摘要

- 用户质疑 ReaderLab v0 只是把多个参考方法字段化拼接，像“顶级食材炒成糊饭”，要求不要把用户判断当结论，而要用独立方法输出和证据验证是否真正吸收。
- 主 Agent 派发四个独立 worker：Cangjie-only、李继刚式深读、乔木共读、book-to-skill-only。
- 四份方法输出均写入 `docs/reports/readerlab-elon-method-bakeoff-v0/`，没有改 LifeAtlas、scripts 或既有 ReaderLab 产品。

## 产物

- `cangjie-only.md`：Stage 0 整书理解、五类候选池、9 个候选的 V1/V2/V3、通过/降级/拒绝判断。
- `ljg-deepread-only.md`：缺口、增量、机制、7 步认知旅程、可复核结论分层、对 ReaderLab v0 的批评。
- `qiaomu-coread-only.md`：章节共读路线、15 个批注触发点、误读纠偏、读者行动、对 ReaderLab v0 的批评。
- `book-to-skill-only.md`：5 个可执行能力、淘汰列表、能力关系、对 ReaderLab v0 深读卡的批评。
- `README.md`：综合对照结论。

## 结论

- ReaderLab v0 不是完全失败，source/location/contracts、reader-facing/audit 分离和全书结构有价值。
- 但阅读/拆书方法没有真正吸收好：缺候选池和淘汰机制，缺缺口/增量/认知旅程，缺批注触发点，缺 trigger/input/steps/output/boundary 的能力结构。
- 下一步应重做 `readerlab-elon-full-product-v1`，不是继续修补 v0。

# 2026-06-30 ReaderLab Elon full product v0

## 摘要

- 用户要求先拿《埃隆之书》做实验，针对整本书做一套完整产品，由主 Agent 集中调度，一个实施 worker 负责产出，一个对抗 worker 负责审查。
- 本轮新增仓库内实验产品：`docs/reports/readerlab-elon-full-product-v0/`。
- 未写 LifeAtlas `300/600/800`，未覆盖旧 LifeAtlas demo 包，未改原 EPUB，未改 `scripts/readerlab.py`，未新增依赖，未联网，未安装或启用 Skill。
- 人工状态保持 `pending`；本产物可交付为整书实验产品 v0，不是 product ready。

## 产物

- `README.md`：打开顺序、边界、产品形态。
- `reader/00_阅读入口.md`、`01_全书阅读路线.md`、`02_全书地图.md`、`03_深读卡组.md`、`04_案例_反例_术语.md`：读者可打开阅读的 Markdown。
- `audit/90_来源与审计.md`：来源、抽取方式、状态和精度说明。
- `contracts/source-registry.v1.json`、`location-map.v1.json`、`catalog-map.v1.json`、`grounded-global-map.v1.json`、`local-deepread.v1.json`：可复核事实层。
- `assertions.md`：ELON-A01 到 ELON-A13 自检。

## 验证和审查

- 实施 worker 自检：13 个必需文件、5 个 JSON、77 个 locations、6 张 deepread cards，errors=0。
- 主 Agent 复跑：
  `python3 tests/test_readerlab.py`
  `python3 scripts/readerlab_fullbook_demo_validate.py`
- 结果：18 tests OK；旧 fullbook demo validator PASS。
- 对抗审查 worker 最终结论：PASS。非阻断意见是 `reader/01_全书阅读路线.md` 原有一句实验覆盖说明有轻微 A11 风险；主 Agent 已改成更读者化表达。

## 剩余风险

- 不是 product ready，人工验收仍为 pending。
- 没有生成全书精选译文正文。
- `char_range` 是清洗后 XHTML 文本偏移，不是 EPUB 原始字节或纸书页码。
- 深读卡 V1/V2/V3 都是 pending，未做跨材料验证。

# 2026-06-30 ReaderLab reference-to-implementation matrix 和能力补强落地

## 摘要

- 本轮按 research/dev worker 边界，把参考项目从研究清单转成 ReaderLab 具体能力改动。
- 未改 `scripts/readerlab.py`，未新增依赖，未联网，未写 LifeAtlas `300/600/800`，未修改 gstack、dbs-suite 或任何 canonical source package。
- 所有人工状态仍为 `pending`；本轮只完成文档侧能力补强，不代表样张通过或产品 ready。

## 已读输入

- 项目真相层：`AGENTS.md`、`docs/current-task.md`、`docs/dev-state.md`、`docs/decisions.md` D-025 到 D-033、`docs/research-log.md`。
- Meta Skill 方法：`skill-ir-method.md`、`output-eval-method.md`、`skill-engineering-method.md`。
- 只读候选：`cangjie-skill` 方法文件、`qiaomu-anything-to-notebooklm`、`anything-to-notebooklm`、Obsidian Markdown Skill、本地 GitHub 能力库 / research log 里关于 `lijigang`、book-to-skill、markitdown、MinerU、NotebookLM、Obsidian、llm-wiki、Agent Skills 形态项目的记录。

## 文档更新

- `docs/readerlab-skill-ir-v0.md`：新增 reference-to-implementation matrix，逐项覆盖参考来源、借什么、不借什么、ReaderLab 落点、预期改善、Elon/DBS 反测、采用/放弃状态和原因；新增最高杠杆 5 个吸收点。
- `docs/contracts/readerlab-contracts-v0.md`：补 `local-deepread.v1.deepread_cards`、V1/V2/V3、source/location 精度门、reader-facing/internal-audit 分离、`capability-map.v1.route_decisions`、`coverage_plan` 和 validate 意图。
- `docs/readerlab-output-eval-v0.md`：补 ELON-A08 到 ELON-A13、DBS-A08 到 DBS-A11，以及下一轮样张避免路径。
- `docs/research-log.md`：记录只读候选复查、现有资产足够、不采用强相关候选的原因。
- `docs/current-task.md`、`docs/dev-state.md`：同步当前事实，下一步是主 Agent 验收和样张反测。

## 验证建议

- 主 Agent 已完成验证：
  `rg -n "reference-to-implementation|deepread_cards|route_decisions|ELON-A13|DBS-A11|reader-facing|product-ready" docs`
  `python3 tests/test_readerlab.py`
  `python3 scripts/readerlab_review_pack_validate.py docs/reports/readerlab-demo-run-v0`
  `python3 scripts/readerlab_fullbook_demo_validate.py`

以上命令均通过。对抗审查 worker 最终结论：PASS，但只通过“文档侧能力补强 / 进入样张反测”的 gate；Skill capability 仍待样张证据，product-ready 仍为 NOT READY。

## 剩余风险

- 测试和既有 validator 已由主 Agent 复跑通过；但本轮改动仍是文档和契约语义更新。
- 旧 demo JSON 仍未包含新增字段，下一轮样张 worker 需要按新契约重做或补齐。
- `--require-complete` 仍应按项目规则失败；不能把任何 repo demo 或 validator 通过说成产品 ready。

# 2026-06-30 ReaderLab 候选范围补查与开放边界修正

## 摘要

- 用户指出下一阶段不能把方案来源圈死：可以用已收集 GitHub 项目、本地 GitHub 收藏整理、项目 prompt，也可以在不足时继续搜索 GitHub。
- 本轮启动本地 GitHub capability recommend 服务做三组补查，均返回 `health_status=ok`；查询后已停止服务。
- 关键修正：李继刚相关 Skill 不能被弱化或丢掉；下一轮 matrix 必须覆盖强相关候选，并写明采用或放弃原因。

## 本地能力库补查结果

- 复杂材料陪读 / 深读：`lijigang/ljg-skill-paper` 返回 fit 0.65，确认其“缺口/增量/机制/认知旅程”应进入 ReaderLab 深读质量 gate；`mli/paper-reading` fit 0.55，暂作弱参考；`joeseesun/qiaomu-anything-to-notebooklm` fit 0.50，适合作多源素材整理参考。
- source-grounded reading package：`opendatalab/MinerU` fit 0.78，作为复杂 PDF / Office 解析设计参考；`microsoft/markitdown` fit 0.55，作为轻量转换参考；`win4r/book-to-skill` fit 0.55，作为书籍到 Skill 路线参考。
- Skill engineering：`muratcankoylan/Agent-Skills-for-Context-Engineering`、`warpdotdev/oz-skills`、`agentskills/agentskills` 均 fit 0.72；`joeseesun/qiaomu-meta-skill` fit 0.62；`affaan-m/ECC` fit 0.55。

## 文档更新

- `docs/next-session-prompt.md`：改为“不限定方法和来源”，要求先用现有资产，不足再扩展本地能力库或直接搜索 GitHub；显式列入 `lijigang/ljg-skill-paper`、`lijigang/ljg-skill-fetch`、乔木、NotebookLM、Obsidian、llm-wiki 等必须检查候选。
- `docs/current-task.md`：更新 reference-to-implementation matrix 要求，加入“若放弃则为什么放弃”。
- `docs/dev-state.md`：记录用户纠偏和开放检索边界。
- `docs/decisions.md`：D-033 补充候选来源不预先封死、必须记录被放弃强相关候选及原因。
- `docs/research-log.md`：新增本地 GitHub 能力库补查记录。

## 验证

- `python3 ~/.codex/skills/github-capability-recommend/scripts/query.py --json ...` 三组查询均返回 `health_status=ok`。
- 用 `rg` 检查下一会话 prompt 和状态文档，确认已出现“不限定方法和来源”、李继刚、乔木、NotebookLM、Obsidian、llm-wiki、直接搜索 GitHub、放弃原因等边界词。
- 本轮未改代码，未运行测试。

# 2026-06-30 ReaderLab 参考分类修正

## 摘要

- 用户指出 Meta Skill、CTK、MEM 不是 ReaderLab 阅读输出的仿型参考：Meta Skill 是处理 Skill 的工程方法，CTK/MEM 是维护开发项目和多 Agent 协作的方法。
- 本轮修正文档分类：保留 Meta Skill 作为 Skill 级审查口径，保留 CTK/MEM 作为调度、状态和收尾纪律；但把它们从阅读输出仿型参考和内容能力吸收清单中移除。
- 未改代码、未写 LifeAtlas、未安装或启用任何 Skill、未新增依赖。

## 文档更新

- `docs/current-task.md`：明确真正仿型参考是仓颉、book-to-skill、source-grounded、Agent Skills 工程化等；Meta Skill、CTK、MEM 只作为工程审查和协作方法。
- `docs/dev-state.md`：把 `yao-meta-skill`、CTK/MEM 的定位改为工程方法，不再描述为阅读输出仿型参考。
- `docs/decisions.md`：在 D-033 中补充边界，明确 Meta Skill、CTK、MEM 不进入内容能力吸收清单。
- `docs/research-log.md`：补充反测结论里的分类边界。
- `docs/next-session-prompt.md`：更新下一会话 prompt，避免 worker 把 `yao-meta-skill`、CTK/MEM 当作阅读输出参考去吸收。

## 验证

- 用 `rg` 检查相关文档中的 Meta Skill、CTK/MEM、仿型参考表述，确认下一会话 prompt 已区分工程方法和内容/来源/Skill 形态参考。
- 本轮为文档分类修正，未运行测试。

# 2026-06-30 ReaderLab 能力补强阶段文档收束

## 摘要

- 用户要求先总结进度、整理文档，并把下一阶段改为“参考项目真实吸收 -> ReaderLab 能力补强 -> 样张反测”。
- 本轮只更新项目状态和下一会话 prompt，没有改代码、没有写 LifeAtlas、没有安装或启用任何 Skill、没有新增依赖。
- 关键判断：已有 GitHub/Skill 参考已经进入研究日志和 IR，但 fullbook demo 的 Meta Skill / 仓颉补审证明吸收还不够深；下一轮必须用实际输出质量反测吸收程度。

## 文档更新

- `docs/current-task.md`：把当前唯一执行切片改为能力补强闭环，明确参考吸收必须落到流程、契约、输出、gate 或 worker 任务。
- `docs/dev-state.md`：补充当前阶段主线、D-033、已知缺口和“参考项目不能只列名”的执行含义。
- `docs/decisions.md`：新增 D-033，规定参考项目必须转成可验收的 ReaderLab 能力改动。
- `docs/research-log.md`：新增“参考吸收不足的反测结论”，记录 fullbook demo 暴露出的吸收缺口和下一轮 matrix 要求。
- `docs/next-session-prompt.md`：重写为下一会话可直接使用的 `/goal`，要求主会话调度验收、子 Agent 执行、Meta Skill 介入、reference-to-implementation matrix 和对抗审查。

## 验证

- 本轮为文档维护和下一阶段任务收束，未运行测试。
- 未改 `scripts/readerlab.py` 或任何 validator；现有测试状态沿用上一轮记录，不能因此声明产品 ready。

# 2026-06-30 Fullbook demo Meta Skill / 仓颉方法补审

## 摘要

- 用户指出 fullbook demo 未经过 Meta Skill 审核，且《埃隆之书》内容质量偏浅。本轮补做两个只读对抗审查：一个按 `yao-meta-skill` 的 Skill IR / output eval / skill engineering 方法，一个按本地 `cangjie-skill` 的 RIA-TV++ 拆书方法。
- 未改 demo 文件、未写 LifeAtlas、未改 `scripts/readerlab.py`、未改 canonical package、未安装或启用任何 Skill。

## 审查结论

- Meta Skill Verdict：PARTIAL。fullbook demo 通过 demo gate，但没有完成 baseline vs with-ReaderLab 的 output eval，validator 主要验证结构和边界，不验证阅读质量；Skill capability gate 仍为 PARTIAL，product-ready 为 NOT READY。
- Cangjie-style Verdict：PARTIAL。fullbook demo 可算“全书导览地图”样张，但不是合格仓颉式深读；按正式读者阅读包判断偏 FAIL。

## 主要问题

- 读者页使用“部件 I/II/III/IV”，应改为书中正式标题，例如 `第一部分：追寻目标`、`第二部分：极限硬核工作`、`第三部分：企业建设`、`第四部分：代表人类`。
- “6 个收获”太短，缺作者特定用法、案例、反例、边界、应用场景和 V1/V2/V3 验证。
- 第一性原理、类比推理、算法之道、工厂即产品、多行星物种等术语缺 glossary。
- Zip2、PayPal、Tesla、SpaceX 等案例只被点名，没有写清“问题 -> 方法 -> 结果”。
- refs 仍是 spine 级，不能支撑正式亮点评审；高价值主张应收窄到 heading / block / char refs。
- 主阅读页混入 demo 状态、pending、spine refs、未写 LifeAtlas 等内部审计信息；正式读者页应把这些移到 README/报告/附录。

## 下一步

- 用 Meta Skill output eval 补 fullbook baseline vs with-ReaderLab 评估记录。
- 用仓颉 RIA-TV++ 修复 fullbook reader demo：正式标题、深读卡、案例/反例/术语、三重验证和更细 refs。
- 保留当前 fullbook demo 的 36/36 spine registry 和 `grounded-global-map.v1` 结构作为事实底座，但不能继续把它说成 Skill capability ready。

# 2026-06-30 Skill 级迭代引入 Meta Skill 审查规则

## 摘要

- 用户明确要求：具体 Skill 级别的迭代和功能审查必须使用 Meta Skills 介入。
- 本轮只更新项目状态和决策文档，未改代码，未写 LifeAtlas，未改 canonical package，未安装或启用任何 Skill。

## 文档更新

- `docs/decisions.md`：新增 D-032，规定 Skill 级功能迭代和功能审查必须引入 `yao-meta-skill` 的 `skill-ir-method`、`output-eval-method` 或 `skill-engineering-method`。
- `docs/current-task.md`：在 worker 边界中加入 Meta Skill 方法输入要求。
- `docs/dev-state.md`：同步 D-032 和执行含义，明确这不是安装新 Skill，也不改变全局 Skill 状态。

## 验证

- 本轮为治理文档更新，未运行测试；后续涉及代码或 validator 改动时必须重新运行对应验证命令。

# 2026-06-30 ReaderLab repo demo run v0

## 摘要

- 本轮按 Demo Worker 边界产出仓库内可打开查看的 ReaderLab demo run：`docs/reports/readerlab-demo-run-v0`。
- 未写 LifeAtlas，未改 canonical package，未改 `scripts/readerlab.py`，未新增依赖，也未把旧样张或本 demo 说成人工验收通过。
- demo 同时包含可验证契约 JSON、assertions、`README.md` 和两份新增读者 Markdown 样张，证明新流程已能产生实际输出，而不是只停留在逻辑骨架。

## 改动

- 新增 `docs/reports/readerlab-demo-run-v0/`，从已通过 gate 的 absorption review pack 复制契约事实层与 assertions。
- 新增 `docs/reports/readerlab-demo-run-v0/elon/reader-demo.md`：只做 `部件 II：极致艰苦工作` 局部深读，明确来源范围、读者路线、核心判断、source/location refs 和 pending 边界。
- 新增 `docs/reports/readerlab-demo-run-v0/dbs/reader-demo.md`：解释 sample-level 能力域、触发信号、方法原子、输出契约、验收方式和跨 Skill 路由，明确不代表 24 Skills full coverage。
- 更新 demo `README.md`，说明验收方式、pass/partial 汇总、blockers 和非 LifeAtlas/非人工验收边界。
- 更新 demo JSON 的 `display.markdown_path` 指向 reader demo 展示页。
- 更新 `docs/current-task.md` 和 `docs/dev-state.md`，记录 demo run 当前事实。

## 验证

- `python3 scripts/readerlab_review_pack_validate.py docs/reports/readerlab-demo-run-v0`：PASS。
- `python3 tests/test_review_pack_validate.py`：15 tests OK。
- `python3 tests/test_readerlab.py`：18 tests OK。

## 断言状态

- Elon：6 pass / 1 partial / 0 fail。A05 仍是 partial，因为局部提炼 refs 还不是精确 EPUB char span。
- DBS：3 pass / 4 partial / 0 fail。DBS 仍是 representative sample，不代表 24 Skills exhaustive coverage。

## 剩余风险

- 本 demo 是 repo 内 demo，不是 LifeAtlas 正式写入。
- 所有 `human_status` 仍为 `pending`，不能把 validator 通过当人工阅读质量通过。
- LifeAtlas 写入前仍需处理 Elon 精确 EPUB span、DBS 24 Skills / cross_skill_routes 真实证据，以及旧 LifeAtlas `dbs-suite` global-map/distillation full 冲突。

# 2026-06-30 ReaderLab repo review gate 对抗循环通过

## 摘要

- 本轮按用户要求采用开发 worker + 对抗审查 worker 的循环：先修复 validator false pass，再由主 Agent 和对抗 Agent 复核，直到 repo 内 review gate PASS。
- 未修改 `scripts/readerlab.py`，未新增依赖，未写 LifeAtlas，未修改 canonical source package，也未改 review pack JSON 规避校验。
- 结论仅限 repo 内 `docs/reports/readerlab-absorption-review-pack-v0` 的确定性 review gate 通过；不代表 LifeAtlas 写入通过，也不代表人工阅读质量通过。

## 改动

- `scripts/readerlab_review_pack_validate.py`：补强 Elon A05 逐 `claim_ref_id` 对齐；DBS `cross_skill_routes` 结构化非空、`route_id` 唯一、`from/to` 回链 capability domains；DBS `review_items` 必须结构化记录 24 Skills、cross_skill_routes 和旧 LifeAtlas global-map conflict blocker。
- `tests/test_review_pack_validate.py`：增加 A05 错配、空 cross_skill_routes、空 review_items、route domain 断链和重复 route_id 负例。
- `docs/reports/readerlab-absorption-review-pack-v0/README.md`：同步 validator 的实际机器边界说明。
- `docs/current-task.md`、`docs/dev-state.md`：更新为 repo review gate 已通过，下一步转入 LifeAtlas 写入前 blocker 或样张重做。

## 验证

- `python3 tests/test_review_pack_validate.py`：15 tests OK。
- `python3 scripts/readerlab_review_pack_validate.py`：PASS。
- `python3 tests/test_readerlab.py`：18 tests OK。
- 主 Agent 临时篡改负例：A05 不存在 claim_ref_id、清空 DBS cross_skill_routes、清空 DBS review_items、route 指向不存在 domain、重复 route_id 均被 validator 拒绝。
- 对抗 Agent 最终结论：PASS，仅作为 repo 内 validator gate。

## 剩余风险

- Elon A05 仍是 partial：还缺精确 EPUB char span。
- DBS 仍是 representative sample：未补全 24 Skills 全覆盖和真实跨 Skill 路由证据。
- LifeAtlas 写入前仍需处理旧 `dbs-suite` global-map/distillation full 冲突，并保持人工状态 pending。

# 2026-06-30 ReaderLab absorption review pack 确定性验证器

## 摘要

- 本轮把 `docs/reports/readerlab-absorption-review-pack-v0` 的人工验收规则沉成独立 helper，没有修改 `scripts/readerlab.py`，没有新增依赖，没有写 LifeAtlas，没有修改 canonical source package。
- 新增验证器只证明 repo 内 review pack 的主要机器边界可复核；它不把 `human_status` 改成 accepted，也不把 Elon/DBS 的 partial/blocker 说成人工通过。

## 改动

- 新增 `scripts/readerlab_review_pack_validate.py`：默认验证 absorption review pack，也支持传入目录参数；失败时输出 `FAIL` 和失败列表并以非 0 退出。
- 新增 `tests/test_review_pack_validate.py`：覆盖当前 pack pass、`human_status=accepted` 负例、`coverage_status=full` 负例。
- 更新 `docs/reports/readerlab-absorption-review-pack-v0/README.md`：补充确定性验证命令和机器通过含义。
- 更新 `docs/current-task.md`、`docs/dev-state.md`、`docs/agent-run-ledger.md`：记录当前状态和验证证据。

## 验证

- `python3 tests/test_readerlab.py`：18 tests passed。
- `python3 tests/test_review_pack_validate.py`：3 tests passed。
- `python3 scripts/readerlab_review_pack_validate.py`：PASS。

## 剩余风险

- Elon 仍保留 A05 partial：局部提炼项不是精确 EPUB char span。
- DBS 仍是 sample-level：未补全 24 Skills，`cross_skill_routes` 仍需真实证据。
- LifeAtlas 写入前仍需处理旧 `dbs-suite` global-map/distillation full 冲突。

# 2026-06-30 ReaderLab Skill IR / output eval / 契约薄骨架

## 摘要

- 本轮完成 ReaderLab Skill 化换轨的薄骨架设计，未修改 `scripts/readerlab.py`，未新增依赖，未写 LifeAtlas `300/600/800`，未改 canonical source packages，未安装或启用任何 Skill。
- 旧《埃隆之书》`02_全书地图.md` 和旧 `dbs-suite` `06_能力地图.md` 继续只作为负面 baseline，不作为合格样张。
- 下一步可以派发 worker 按新 IR/eval/契约重做两个高质量样张。

## 文档更新

- 新增 `docs/readerlab-skill-ir-v0.md`：定义 recurring job、触发/不触发、near-neighbor、工作流、Agent/脚本边界、资源/脚本/报告关系、参考基准逐项转译、output risk 和 reviewer gate。
- 新增 `docs/readerlab-output-eval-v0.md`：定义《埃隆之书》和 `dbs-suite` 两个 output eval case，包含 baseline、with-ReaderLab 预期、机器断言、人工评审点和 worker 任务说明。
- 新增 `docs/contracts/readerlab-contracts-v0.md`：定义 `source-registry.v1` / `location-map.v1`、`catalog-map.v1` / `grounded-global-map.v1`、`capability-map.v1` 的最小字段和 Agent/脚本边界。
- 更新 `docs/current-task.md`：把当前切片推进为“按骨架分派 worker 重做样张”。
- 更新 `docs/dev-state.md`：记录三份薄骨架是草案，不是正式生成器机制。
- 更新 `docs/decisions.md`：新增 D-031，确定 IR/eval/契约薄骨架先于样张重做。
- 更新 `docs/research-log.md`：记录参考基准已经逐项转译进 IR。

## 验证

- 已读取 `AGENTS.md`、`docs/current-task.md`、`docs/dev-state.md`、`docs/decisions.md`、`docs/research-log.md` 和 `docs/agent-run-ledger.md` 顶部记录。
- 已读取 `yao-meta-skill` 的 `skill-ir-method.md`、`output-eval-method.md`、`skill-engineering-method.md`。
- 本轮为 docs/contract-design only，未运行 Python tests；代码没有改，测试不能证明设计质量。
- 后续应以 `docs/readerlab-output-eval-v0.md` 的 ELON-A01 到 ELON-A07、DBS-A01 到 DBS-A07 验收新版样张。

## 边界与剩余风险

- 还没有重做《埃隆之书》和 `dbs-suite` 样张。
- 还没有实现新契约 JSON Schema 或 validate 检查。
- 还没有 provider-backed output eval 或 blind review evidence。
- 人工阅读验收仍是后续动作；不能把本轮设计完成说成样张质量通过。

# 2026-06-30 GitHub 能力库复查结果写入 ReaderLab 状态文档

## 摘要

- 本轮按文档 worker 边界只更新 ReaderLab 项目状态文档，没有改代码、没有运行测试、没有写 LifeAtlas、没有安装或启用任何 Skill / GitHub 资产。
- 主 Agent 已确认 GitHub 能力库 `/api/recommend` 在 2026-06-30 复查后恢复；三类正式查询均 `health_status=ok`。
- 结果类别：拆书/深读 5 个 formal 推荐，Skill 工程化 5 个 formal 推荐，材料解析 5 个 formal 推荐。
- NotebookLM、Obsidian、llm-wiki 相关项目仅是 SQLite pending 线索，不是正式推荐链路强结果，只能参考设计，不能自动启用。

## 文档更新

- `docs/next-session-prompt.md`：移除过时的 GitHub 查询故障表述；新增“参考基准（必须进入设计）”，按拆书/深读/提炼、材料解析/source-grounded、Skill 工程化列出具体候选和借鉴点；新增硬性验收“借什么 / 不借什么 / 翻译成 ReaderLab 的设计是什么”。
- `docs/research-log.md`：把“GitHub 能力库查询故障”改为复查恢复结果，记录三类正式推荐和 SQLite pending 线索边界。
- `docs/dev-state.md`：更新参考调研结论和当前已知缺口，明确下一步 IR/eval 必须把候选借鉴点转成 ReaderLab 设计。
- `docs/agent-run-ledger.md`：新增本条运行记录。

## 边界

- 未改 `scripts/readerlab.py`、测试、schema 或任何 LifeAtlas 输出。
- 未安装、启用、克隆或修改候选项目；本轮只把已确认查询结果写入 ReaderLab 文档。

# 2026-06-30 ReaderLab Skill 化换轨文档整理

## 摘要

- 用户确认：当前方向应使用 `yao-meta-skill` 完善 ReaderLab 的 Skill 开发，而不是继续把 ReaderLab 当大脚本。
- 本轮按 MEM 分层整理项目上下文：删除/改写旧样张“已交付”带来的误导，把旧《埃隆之书》全书地图和旧 dbs 能力地图标为质量未通过的负面基线。
- 新当前主线改为：ReaderLab Skill IR v0、output eval v0、契约薄骨架，然后重做样张。

## 文档更新

- `docs/current-task.md`：改为单一当前切片“ReaderLab Skill 化薄骨架与质量评估”；明确不整体重构、不继续扩写 `scripts/readerlab.py`。
- `docs/dev-state.md`：压缩为当前事实；补充旧样张未通过、`yao-meta-skill` 定位、GitHub收藏整理查询故障、下一批缺口。
- `docs/decisions.md`：新增 D-029、D-030。
  - D-029：采用薄骨架换轨，不整体重构。
  - D-030：用 `yao-meta-skill` 完善 ReaderLab Skill 工程化。
- `docs/research-log.md`：新增参考调研结论，归档仓颉/book-to-skill/ljg-paper、MarkItDown/MinerU/NotebookLM、Anthropic/CTK/MEM/Superpowers、`yao-meta-skill` 和 GitHub 能力库查询故障。
- `docs/next-session-prompt.md`：替换旧“双轨交付旧样张” prompt，改为 ReaderLab Skill IR v0 + output eval v0 + 契约薄骨架的新会话目标。

## 当前结论

- ReaderLab 是复杂材料陪读 Skill / Agent 工作流；`scripts/readerlab.py` 只应逐步降级为工具箱。
- 旧《埃隆之书》`02_全书地图.md` 不能作为合格全书地图；低覆盖时只能做 `catalog_map` 或局部地图。
- 旧 `dbs-suite` `06_能力地图.md` 不能作为合格能力地图；Skill 包需要 `capability-map.v1`。
- `yao-meta-skill` 不用于读书，而用于产出 ReaderLab Skill IR、output eval、output-risk 和 gate。

## 验证与边界

- 本轮为 docs-only 状态维护，未修改代码、未运行测试、未写 LifeAtlas 产物、未改 Skill 源包。
- 未新增依赖，未启用或安装 `yao-meta-skill`。
- GitHub收藏整理服务故障仅写入 debug 交接文档和 research-log；本轮未修该项目。

# 2026-06-30 decisions 分层压缩

## 摘要

- 用户指出 `docs/decisions.md` 过长，且不是所有旧决策都是当前必须遵守的规则。
- 本轮将 D-001 到 D-013 从主决策文件迁出，保留为历史归档，避免普通启动时被旧 Skill 包翻译/旧四段式规则拖偏。

## 文档更新

- `docs/decisions.md`：新增读取规则和状态索引；主文件只保留 D-014 到 D-030 的当前有效决策全文。
- `docs/decision-archive.md`：新增 D-001 到 D-013 的历史决策全文。仅在处理旧 Skill 包页面生成、旧翻译/精读产物、旧四段式页面或旧质量门兼容时按需读取。

## 状态结论

- D-014 到 D-030 是当前 ReaderLab 路线的 active 决策。
- D-001 到 D-013 分为 `legacy-narrow`、`superseded`、`historical`，不再作为普通启动必读内容。

## 边界

- 本轮只改文档，不改代码、不跑测试、不写 LifeAtlas、不改 Skill 源包。

# 2026-06-29 v0.4/v0.5 收尾状态文档更新

## 摘要

- 本轮按 worker F 边界只更新项目 truth layer 状态文档，没有修改代码、测试、LifeAtlas 产物或 Skill 源包。
- 主 Agent 审计指出 `docs/current-task.md` / `docs/dev-state.md` 仍把已完成的 v0.4/v0.5 双轨交付描述成“下一步要做”，容易误导下一会话。
- 本次将当前状态改为：样张、schema、契约实例和 validate 检查入口已形成；人工验收仍 pending；生成器还未正式自动生成全书地图、能力地图或契约实例。

## 文档更新

- `docs/current-task.md`：改为真实下一步切片：人工验收两个样张，决定是否把契约实例生成纳入正式生成器，后续按材料类型拆清洗、正文保留、地图生成和契约生成边界。
- `docs/dev-state.md`：把 v0.4/v0.5 状态从“尚未形成机制化产物”更新为已有样张、schema、契约实例和检查入口；保留人工验收 pending、生成器未自动化、`readerlab.py` 单体、样本硬编码和页面清洗边界风险。
- `docs/agent-run-ledger.md`：新增本条运行记录；旧历史记录保留。

## 产物核对

- 《埃隆之书》全书地图样张存在：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629/02_全书地图.md`
- `dbs-suite` 能力地图样张存在：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726/06_能力地图.md`
- 契约 schema 存在：
  `docs/contracts/global-map.v1.schema.json`
  `docs/contracts/distillation.v1.schema.json`
- 技术债边界文档存在：
  `docs/technical-debt-boundary.md`
- `rg` 核对显示两个包的 manifest 已挂载 `contract_artifacts`，并指向各自的 `40_全局理解/global-map.json` 与 `40_全局理解/distillation.json`。

## 验证证据

- 已只读核对 AGENTS、当前任务、开发状态、D-025/D-026/D-027 和账本顶部最新记录。
- 已用 `test -f` 核对上述样张、schema 和技术债边界文档存在。
- 已用 `rg -n "global-map|distillation|全书地图|能力地图|contract" ...` 核对样张、schema、契约实例和 manifest 挂载线索。
- 本次为 docs-only 收尾，未运行 Python tests；代码和测试未改，运行测试不能证明人工样张质量。

## 边界与剩余风险

- 人工验收尚未通过；不能把 validator 通过或文件存在说成人工阅读质量通过。
- 全书地图、能力地图和契约实例当前仍是样张/事实层验证结果；不能说 ReaderLab 生成器已经机制化自动生成。
- `scripts/readerlab.py` 单体、dbs/gstack 样本硬编码、页面清洗按材料类型拆分仍是后续技术风险。
- 是否把契约实例生成纳入正式生成器，需要在两个样张人工验收后再决策。

# 2026-06-29 下一阶段双轨并行：产品样张与技术收口同时推进

## 摘要

- 用户进一步澄清：之前调研出的技术问题也应得到解决，不应被完全抛掉；同时也不能放弃 v0.4/v0.5 的产品推进。
- 主 Agent 将下一阶段调整为双轨并行：产品轨交付《埃隆之书》全书地图样张和 `dbs-suite` 能力地图样张；技术轨同步解决支撑样张机制化的最小技术问题。
- 技术轨不再只是只读护栏，而是允许子 Agent / worker 在窄范围内改项目文档、schema、测试和 validate 相关代码；但不做大重构，不把样本特殊结构写死为通用规则。

## 文档更新

- `docs/current-task.md`：将下一步改为“双轨并行”，分别列出产品轨和技术轨交付目标。
- `docs/dev-state.md`：补充技术收口轨，说明它与 v0.4/v0.5 并行推进，而不是替代产品样张。
- `docs/next-session-prompt.md`：重写交付物和分派方式，新增契约与 validate worker、技术债 worker。

## 当前分配

- 子 Agent A：产出《埃隆之书》全书地图样张。
- 子 Agent B：产出 `dbs-suite__v2.15.1_096f726` 能力地图样张。
- 子 Agent C：收敛 `global-map.v1` / `distillation.v1` 契约并实现最小 validate 检查。
- 子 Agent D：处理状态语义、硬编码边界、页面清洗风险等本轮直接相关的技术问题，能小补丁就小补丁，不能安全处理则列后续清单。

# 2026-06-29 下一步任务澄清：技术问题是护栏，v0.4/v0.5 样张是主交付

## 摘要

- 用户指出上一版下一会话规划看起来像继续调研技术问题，没有清晰推进刚讨论的 v0.4 / v0.5 需求。
- 主 Agent 确认该反馈成立：技术评估应作为防过拟合和写入边界护栏，不应成为下一步主线。
- 文档已调整为：下一步主交付是《埃隆之书》全书地图样张、`dbs-suite` 能力地图样张，以及支撑这两个样张的 `global-map.v1` / `distillation.v1` 最小契约。

## 文档更新

- `docs/current-task.md`：将“下一步目标”改为“下一步交付目标”，明确不是继续技术调研，而是交付两个可读产品样张。
- `docs/next-session-prompt.md`：重写分派顺序，让产品样张子 Agent A/B 在前，技术子 Agent C 只作为只读护栏。

## 当前结论

- v0.4 = 全局理解层：图书全书地图、Skill 包能力地图。
- v0.5 = 精华提炼层：框架、原则、案例、反例、术语、可迁移洞察和候选沉淀方向。
- 技术问题用于约束实现方式：不继续堆 `readerlab.py`，不把样本结构写死成通用规则，不把 schema 当成读者可见产品。

# 2026-06-29 调度型主 Agent 模式与下一会话 prompt 更新

## 摘要

- 用户要求维护文档，把当前结论全部写入项目真相层，并撰写新会话 prompt。
- 新会话协作方式明确为：主 Agent 只负责分派、收回、验收任务以及和用户沟通；代码修改、执行、测试由子 Agent 完成。
- 主 Agent 按 MEM 分层规则维护文档：协作模式作为耐久决策进入 `docs/decisions.md`，当前执行切片进入 `docs/current-task.md`，当前事实进入 `docs/dev-state.md`，新会话启动文本进入 `docs/next-session-prompt.md`。

## 文档更新

- `docs/decisions.md`：新增 D-027，定义调度型主 Agent 与子 Agent 执行边界。
- `docs/current-task.md`：补充下一会话协作方式，明确 v0.4/v0.5 仍以 `global-map.v1` / `distillation.v1` 契约和样张为下一切片。
- `docs/dev-state.md`：补充 D-027 索引和当前协作边界。
- `docs/next-session-prompt.md`：替换旧 `dbs-suite` 试产 prompt，改为当前 v0.4/v0.5 阶段的新会话 prompt。

## 当前结论

- v0.1 基础闭环基本通过，v0.2/v0.3 后移或够用，当前主线是 v0.4 全局理解层和 v0.5 精华提炼层。
- 下一步不直接堆 `scripts/readerlab.py` 模板，而是先定义 `global-map.v1` / `distillation.v1` 数据契约，并用《埃隆之书》和 `dbs-suite__v2.15.1_096f726` 做包级样张。
- 下一会话主 Agent 必须保持调度和验收角色；具体实现、执行和测试都由子 Agent / worker 完成。

# 2026-06-29 M1M/MEM 文档压缩与技术侧独立评估

## 摘要

- 用户要求调用 M1M 工具包整理现有文档，清理过时内容，降低上下文冗余，并调用子 Agent 从技术侧独立评估当前方案。
- 当前会话未发现名为 `M1M` 的可调用工具；按项目 memory 规则改用 MEM 清理方法，读取 `mem-clean` 和 `mem-contract` 后执行文档压缩。
- 主 Agent 将 `docs/current-task.md` 压缩为单一当前执行切片，将 `docs/dev-state.md` 压缩为当前事实和技术风险，保留 `docs/decisions.md` 作为耐久决策层，保留本账本作为运行历史层。
- 检查确认项目内没有 `CLAUDE.md`，无需清理 Claude Code 兼容文件。

## 文档整理结果

- `docs/current-task.md`：压缩到 46 行，只保留当前 v0.4/v0.5 主线、下一步样张、关键路径和必须避免事项。
- `docs/dev-state.md`：压缩到 90 行，只保留产品阶段、当前实现事实、样本事实、已知缺口和约束。
- `docs/decisions.md`：新增 D-026，明确 v0.4/v0.5 必须先做 `global-map.v1` / `distillation.v1` 数据契约，不先继续堆生成器模板。
- `docs/agent-run-ledger.md`：继续承担运行历史和验证证据，不把流水账放回 `current-task` 或 `dev-state`。

## 技术侧独立评估结论

子 Agent 只读评估后认为：ReaderLab v0.1 能跑通，但当前代码还是压力样本驱动的单体原型，不适合直接承载 v0.4/v0.5 的继续堆叠。

主要风险：

- `scripts/readerlab.py` 同时承载 Skill 导入、样本分组、页面生成、清洗规则、状态写入、validate 和批注处理，后续需要拆边界。
- 代码中已有 dbs/gstack/试点样本相关硬编码，包括阅读单元分类、dbs 路由、试点 Skill 描述和完成翻译映射；这些可保留为 v0.1 历史过渡，但不应继续扩展。
- `delivery_status=deliverable` 是机器交付状态，不等于人工阅读通过；后续应考虑更清晰的状态命名或新增人工验收检查。
- 页面清洗依赖正则/黑名单，适合当前 Skill 执行壳清理，但不适合作为书籍、代码文档和混合材料的统一正文规则。
- 《埃隆之书》当前是手工 Demo，不是正式图书导入器；如果 v0.4/v0.5 继续以手工 Markdown 产物推进，必须同步沉淀数据契约，否则无法稳定复制。

## 采纳决策

- 下一步不直接修改生成器，也不先生成更多页面模板。
- 先定义 `global-map.v1` 和 `distillation.v1` 的事实层样张，再分别用于《埃隆之书》全书地图和 `dbs-suite` 能力地图。
- validate 后续应从“页面结构检查”扩展到“来源范围、置信度、待复核项、人工状态”检查。

# 2026-06-29 ReaderLab v0.1 后路线重排：转入全局理解与精华提炼

## 摘要

- 用户确认：v0.1 的基础能力已经基本实现，当前更重要的问题不是继续扩大量清洗、翻译和切段，而是补齐全局视角、精华提炼和高附加值产物。
- 主 Agent 回读最初两个产品文档：
  - `docs/readerlab-v0.1-light-prototype.md`
  - `docs/readerlab-future-roadmap-and-references.md`
- 结论：当前讨论正好对应原始路线中的 `Distill`、book-to-skill、旁通视角、BookReader/PaperReader 和 LifeAtlas 升格前置能力。
- 用户进一步确认路线重排：v0.2 批注插件增强后移；v0.3 轻量 registry 当前基本够用；现在主要讨论和建设 v0.4/v0.5；v0.6 必须建立在 v0.4/v0.5 基础上。

## 文档更新

- `docs/readerlab-future-roadmap-and-references.md`
  - 改为 v0.1 之后路线文档。
  - 明确 v0.1 产品闭环基本通过。
  - 新增工作分层：原料处理层、全局理解层、精华提炼层、升格层。
  - 新增 v0.4 全局理解层：全书地图、能力地图、主线、概念关系、章节/Skill 功能关系。
  - 新增 v0.5 精华提炼层：框架、原则、案例、反例、术语、可迁移洞察、候选 Skill 化方向。
  - 将 v0.2 批注插件增强后移，将 v0.3 轻量 registry 标为基本够用。
- `docs/decisions.md`
  - 新增 D-025：v0.1 基础闭环后，优先建设全局理解层和精华提炼层。
- `docs/current-task.md`
  - 更新当前唯一执行切片：下一步建议做《埃隆之书》全书地图样张和 `dbs-suite` 能力地图样张，不先改生成器。
- `docs/dev-state.md`
  - 新增当前产品阶段：v0.1 基本通过，v0.4/v0.5 为当前主线，v0.6 后置。

## 当前结论

- ReaderLab v0.1 已从“能否把材料做成可读 Markdown 阅读包”进入“如何提供全局理解和精华提炼”的产品升级阶段。
- 下一步最小样张不应是更多页面翻译，而是：
  - 《埃隆之书》：包级全书地图。
  - `dbs-suite__v2.15.1_096f726`：包级能力地图。
- 仓颉 `book2skill` 继续作为方法参考，不全局启用，不直接生成正式 Skill 仓库。

# 2026-06-29 埃隆之书 ReaderLab Demo 与仓颉方法局部接入

## 摘要

- 按用户确认的下一阶段方向，处理两个问题：仓颉 Skill 不全局启用，但借鉴/局部调用其拆书蒸馏方法；《埃隆之书》先做全书分组与章节手册，再完整处理一个有厚度的单元。
- `skillsctl show cangjie-skill` 确认本地 canonical package 已存在，当前为 `library-only / explicit-only / active=false`；本轮未启用为默认运行时。
- 子 Agent 只读对抗建议后，主 Agent 采纳其判断：完整处理单元从原先候选 `物理学家式思考组` 升级为完整 `部件 II：极致艰苦工作`，避免只处理小章节。
- 新增 LifeAtlas 200 独立 Demo 包：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629`
- 原 EPUB 保留在原位，未移动、未覆盖；未写入 LifeAtlas `300/600/800`。

## 涉及文件和目录

- 输入 EPUB：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 输出 Demo 包：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629`
- 临时解析/构建脚本：
  `/private/tmp/readerlab_elon_extract.py`
  `/private/tmp/readerlab_elon_build_part2_package.py`
- 项目状态文档：
  `docs/current-task.md`
  `docs/dev-state.md`
  `docs/agent-run-ledger.md`

## 关键结果

- 全书 TOC 已拆入 `01_全书分组与章节手册.md`，覆盖前置材料、部件 I、部件 II、部件 III、部件 IV、附录与工具材料。
- 完整处理单元：`部件 II：极致艰苦工作`。
- 来源文件：EPUB 内 `OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-13.xhtml` 到 `...-18.xhtml`。
- 完整处理页：`10_中文精读/02_极致艰苦工作/部件II_极致艰苦工作.md`。
- 仓颉式局部提炼样张：`20_读后提炼/仓颉式提炼样张_部件II_极致艰苦工作.md`。
- 本页生成 `内容解读` 是按需例外：该部件长、跨责任/团队/组织/速度/制造五条链路，且容易被误读成“努力鸡血”；解读只讲结构判断和误读边界。

## 已验证

```bash
python3 /Users/tianqiang/技能项目/技能管理器/scripts/skillsctl.py show cangjie-skill
python3 /private/tmp/readerlab_elon_extract.py /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-13.xhtml OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-14.xhtml OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-15.xhtml OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-16.xhtml OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-17.xhtml OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-18.xhtml
python3 /private/tmp/readerlab_elon_build_part2_package.py
python3 scripts/readerlab.py validate /private/tmp/elon-book__readerlab-demo_20260629
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629
rg -n "source_block|source_blocks|sha256|后台验收|raw frontmatter|^---$|页面分层|原 Skill|Skill 正文|本段说明" /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629 --glob '*.md'
```

结果：

- 正式 Demo 包 validate 通过：25 total / 5 completed / 0 needs_review / 20 not_started / human pending 25 / total_source_blocks 2 / `delivery_status=demo_partial`。
- `demo_partial` 符合本轮边界：全书已分组，一个完整部件已处理，不代表全书完成。
- 硬伤扫描无命中；未发现 source block、hash、raw frontmatter、旧 Skill 标题、后台验收污染。

## 剩余风险

- 这是手工构建的书籍 Demo 包；正式图书导入命令和生成器机制尚未实现。
- `内容解读` 的按需触发规则仍需回写到机制层和 SOP；本轮只在《埃隆之书》Demo 里落地验证。
- 仓颉式提炼只是读后样张，未经过仓颉三重验证，也未进入正式 Skill 仓库。

# 2026-06-29 dbs-suite 01/02 内容解读 Demo

## 摘要

- 按用户确认的方案，只处理新版 `dbs-suite__v2.15.1_096f726` 的 01/02 两个阅读单元作为 Demo。
- 子 Agent 手工改写 5 个 LifeAtlas 当前笔记；主 Agent 亲自复核标题树、`内容解读` 段落、旧结构残留和 validate 结果。
- Demo 目标是验证 `内容解读` 与 `原文` 分层是否改善阅读体验，不是全包重刷，也不是生成器机制修复。

## 修改范围

- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726/10_中文精读/01_核心入口与总览/dbs.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726/10_中文精读/02_诊断审查与质量判断/dbs-benchmark.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726/10_中文精读/02_诊断审查与质量判断/dbs-deconstruct.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726/10_中文精读/02_诊断审查与质量判断/dbs-slowisfast.md`

未修改 `scripts/readerlab.py`、`data/skill-readings`、旧版 `dbs-suite`、`gstack` 或 LifeAtlas `300/600/800`。

## 验收结论

- 5 页主结构均为：`短导读 / 阅读地图 / 内容解读 / 原文 / 关联说明`。
- 5 页均不再出现 `## Skill 正文`、`原 Skill 正文结构校读版`、重复的 `### dbs-*` Skill 标题。
- `内容解读` 与 `原文` 长度比约为：
  - `dbs`：0.15
  - `dbs-benchmark`：0.23
  - `dbs-deconstruct`：0.22
  - `dbs-diagnosis`：0.10
  - `dbs-slowisfast`：0.16
- 主 Agent 抽读确认：`benchmark/deconstruct/diagnosis/slowisfast` 的 `内容解读` 已从流程复述变成读法解释；完整表格、模板、场景库留在 `原文`。

## 已验证

```bash
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726 --require-complete
```

结果：passed true，24 completed / 0 needs_review / 0 not_started / human pending 24 / source blocks 2195 / `delivery_status=deliverable`。

## 剩余风险

- 这是 5 页 LifeAtlas 当前笔记的手工 Demo，不是生成器和 `data/skill-readings` 的耐久机制修复。
- 后续重新 `import-skills --force` 会覆盖这 5 页手工结果，除非先把规则回写到生成机制和精读 JSON。

# 2026-06-29 dbs 页人工抽读反馈与手工页修正

## 摘要

- 用户人工抽读新版 `dbs-suite__v2.15.1_096f726` 的 `dbs` 页后指出：当前页面把“中文解读正文”和“原 Skill 正文结构校读版”做成了上下两遍正文，尤其是任务后导航地图在前半散文复述、后半表格原文重复出现，信息冗余明显。
- 主 Agent 复读页面后确认问题成立：这不是用户误读，而是当前“完整覆盖 + 原结构校读”策略在入口路由型 Skill 上的副作用。
- 已记录为后续统一机制修正项：前半解读正文应讲读法、机制、抽象分组和使用边界；完整路由表/完整导航地图只在校读版出现。
- 同时确认标题层级缺陷：`原 Skill 正文结构校读版` 被统一降级成 `####`，低于其内部原文标题，造成结构倒挂。后续生成器应把校读版设为清晰区块，并把原文标题作为其子层级。

## 本次边界

- 本次只手动调整当前 LifeAtlas 笔记 `dbs.md`，不在此刻统一改生成机制。
- 用户将继续抽读其他笔记，后续统一整理问题后再调整机制层。
- 不覆盖旧 `dbs-suite` 阅读包，不写入 LifeAtlas `300/600/800`。

## 本次手工调整

- 已手动调整 `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726/10_中文精读/01_核心入口与总览/dbs.md`。
- 调整后前半 `Skill 正文` 只解释：`dbs` 的入口职责、双模式判断、任务前路由读法、任务后导航读法和边界失败条件。
- 完整路由表和完整任务后导航地图只保留在 `### 原 Skill 正文结构校读版` 下。
- 修正校读版标题层级：校读版为 `###`，原文主要小节为其下级，不再出现校读版标题低于原文标题的倒挂。

## 已验证

```bash
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726 --require-complete
```

结果：passed true，24 completed / 0 needs_review / 0 not_started / human pending 24 / source blocks 2195 / `delivery_status=deliverable`。

# 2026-06-29 dbs-suite 对抗审查后的不过拟合优化

## 摘要

- 按用户要求单独启动只读子 Agent 做对抗式产品审查；主 Agent 复核后确认三类问题成立：句子截断、顶层任务路线不足、部分 Skill 分组过粗。
- 原因判断：这些不是单页内容问题，而是生成器规则问题。
  - `reader_skill_role` 使用硬截断，导致组导读和单页职责出现半句。
  - `build_reading_map` 按组内顺序生成“上游/下游”，容易把浏览顺序误写成业务流程。
  - 分类器把 chatroom 和 content-system 吃进泛“内容表达”组，导致讨论工具和内容工程被误读成文案模板。
  - 机制盘点只按文件类型说明，工程型工具链的具体职责被稀释。
- 已做不过拟合优化：句子感知截断；阅读地图改为组内相邻页 + 常见进入/后续；按任务读路线自动生成；chatroom/content-system 拆成更细语义单元；artifact 角色按常见工具名识别职责。
- 新版正式 LifeAtlas 包已重刷，当前 24 个 Skill / 8 个 reading unit / `delivery_status=deliverable`。

## 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite__v2.15.1_096f726 --title 'dbs-suite v2.15.1' --goal 'ReaderLab v0.1 对 dbs-suite upstream v2.15.1 的版本化试产：验证新版 DBS Skill 套件能否形成可连续阅读、可批注、可复核的 LifeAtlas 阅读包，并保留旧 dbs-suite 阅读包与旧批注。' --readings-dir data/skill-readings --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726 --require-complete
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md
```

结果：

- 单元测试：17 tests OK。
- py_compile：通过。
- `--require-complete`：passed true，24 completed / 0 needs_review / 0 not_started / human pending 24 / source blocks 2195 / `delivery_status=deliverable`。
- 硬伤扫描：主阅读页未命中截断半句、伪“上游/下游”、占位正文、raw frontmatter、source block、hash、后台验收等问题。
- 旧版批注：`rl-dbs-complex-001` found=true，thread_count=2。

# 2026-06-29 dbs-suite v2.15.1 真实精读交付纠偏

## 摘要

- 前一轮仅完成 canonical package 更新、版本化包生成和机器覆盖试产，但 24 个新版精读 JSON 的主体正文仍含大量“本段说明”式占位，不能算真正完成全技能包解读。
- 本轮已将 `data/skill-readings/dbs-suite__v2.15.1_096f726/*.json` 全部重写为真实中文解读主线，并追加去 frontmatter 污染的原 Skill 正文结构校读版。
- 重新刷新正式 LifeAtlas 200 新版包：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726`。
- 修正阅读路线：`dbs` 独立进入 `01_核心入口与总览`；`dbs-report` 进入 `05_状态记忆与报告`；后续对抗审查优化后新版共 8 个 reading unit。
- 旧版 `dbs-suite` 保留，旧真实批注 `rl-dbs-complex-001` 仍可定位。

## 涉及文件和目录

- `scripts/readerlab.py`
- `data/skill-readings/dbs-suite__v2.15.1_096f726/*.json`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/agent-run-ledger.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726`

## 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite__v2.15.1_096f726 --title 'dbs-suite v2.15.1' --goal 'ReaderLab v0.1 对 dbs-suite upstream v2.15.1 的版本化试产：验证新版 DBS Skill 套件能否形成可连续阅读、可批注、可复核的 LifeAtlas 阅读包，并保留旧 dbs-suite 阅读包与旧批注。' --readings-dir data/skill-readings --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726 --require-complete
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md
rg -n "本段说明（第|这里处理|第 N 段|raw frontmatter|source block|source_block|后台验收|结构保留|占位段落|页面分层|Codex 吸收后的设计提炼|^---$|^name: dbs|^name: |^description:|\bhash\b|source_hash|sha256" /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726 --glob '*.md' --glob '!source.md'
```

结果：

- `--require-complete`：passed true，24 completed / 0 needs_review / 0 not_started / human pending 24 / source blocks 2195 / `delivery_status=deliverable`。
- 单元测试：17 tests OK。
- py_compile：通过。
- 主阅读页污染扫描：无命中；`source.md` 仍保留审计用 `sha256` 表，属于追溯层。
- 旧版批注：`rl-dbs-complex-001` found=true，thread_count=2。

## 剩余风险

- 新版所有 Skill 的人工状态仍为 `pending`，不代表人工阅读质量最终通过。
- 当前交付已完成机器覆盖、真实精读替换和主路线抽查；下一步应做人工抽读验收，尤其是新增 Skill 和变化较大的 Skill。

# 2026-06-29 dbs-suite v2.15.1 版本化试产交付

## 摘要

- 只交付 `dbs-suite` 新版版本化试产，未处理 `gstack`。
- 重新只读确认 upstream `v2.15.1` 和 `main` 均为 commit `096f726a20407901ca517cfc42509f96232fd0ea`。
- 按 D-024 先更新本地 canonical package，再基于本地新版生产 ReaderLab 阅读包。
- 本地 canonical package `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite` 已更新到 `2.15.1`。
- 旧本地非 upstream Skill `chatroom-austrian`、`dbskill-upgrade`、`evaluating-candidates` 未进入新版输入。
- 新版 LifeAtlas book id：`dbs-suite__v2.15.1_096f726`。
- 旧版 LifeAtlas `dbs-suite` 保留，真实批注 `rl-dbs-complex-001` 仍可定位。

## 涉及文件和目录

- `scripts/readerlab.py`
- `data/skill-readings/dbs-suite__v2.15.1_096f726/*.json`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/agent-run-ledger.md`
- `docs/dbs-suite-v2.15.1-version-diff.md`
- `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726`

## 关键结果

- canonical package 当前 24 个 upstream Skill，`PACKAGE.json` 为 `local_version=2.15.1`、`upstream_version=2.15.1`。
- 新版阅读包：55 个文件扫描 / 24 个 Skill / 8 个 reading unit / `delivery_status=deliverable`。该数字以本文件顶部“对抗审查后的不过拟合优化”最终重刷为准。
- 新版 validate 和 `--require-complete` 通过：24 total / 24 completed / 0 needs_review / 0 not_started / human accepted 0 / human pending 24 / 2195 source blocks。
- 新版 `material_structure.status=clear`，没有 `90_材料结构诊断`。
- 版本差异说明已写入项目 docs 和新版 LifeAtlas 包。
- `skillsctl show dbs-suite` 的实际 Skill 列表正确为 24 个；旧 local-only 名称仍作为历史 alias 出现在注册层展示中，但 ReaderLab 生产不读取 alias。

## 已验证

```bash
git ls-remote --tags --refs https://github.com/dontbesilent2025/dbskill.git 'v*'
git ls-remote https://github.com/dontbesilent2025/dbskill.git HEAD refs/heads/main
python3 /Users/tianqiang/技能项目/技能管理器/scripts/skillsctl.py update-package dbs-suite
python3 /Users/tianqiang/技能项目/技能管理器/scripts/skillsctl.py sync-package-metadata
python3 /Users/tianqiang/技能项目/技能管理器/scripts/skillsctl.py show dbs-suite
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite__v2.15.1_096f726 --title 'dbs-suite v2.15.1' --goal 'ReaderLab v0.1 对 dbs-suite upstream v2.15.1 的版本化试产：验证新版 DBS Skill 套件能否形成可连续阅读、可批注、可复核的 LifeAtlas 阅读包，并保留旧 dbs-suite 阅读包与旧批注。' --readings-dir data/skill-readings --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726 --require-complete
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md
```

结果：

- `--require-complete`：passed true。
- 单元测试：17 tests OK。
- py_compile：通过。
- 旧版批注：`rl-dbs-complex-001` found=true，thread_count=2。
- LifeAtlas 200 下同时存在 `dbs-suite` 和 `dbs-suite__v2.15.1_096f726`。

## 剩余风险

- 新版人工状态全部为 `pending`。validator 通过只说明结构、覆盖和机器底线通过，不能代表人工阅读质量通过。
- 24 个新版精读页为结构保留型中文阅读页，适合试产和人工抽读；后续如果要作为长期主版本，应人工抽读新增 Skill 和变化较大 Skill 后再决定是否提升。
- `skillsctl` 注册层仍保留旧 local-only 名称作为历史 alias，后续可在技能管理器任务中单独清理 alias 策略；本轮未把它作为 ReaderLab 输入。

# 2026-06-29 dbs-suite 版本预检与 M3 可用性检查

## 摘要

- 按用户要求，在全量生产前只读检查 `dbs-suite` 和 `gstack` upstream 状态。
- 最初讨论过用 upstream 快照 + local-only overlay 试产；随后用户调整策略：先更新本地 canonical package 到最新版，再基于本地新版生产。
- 当前最终策略：本地 `dbs-suite` canonical package 先更新到 upstream v2.15.1，并以上游最新版为准；旧本地非 upstream Skill 不默认保留，除非确认是我们自己单独开发且用户批准保留。LifeAtlas 仍采用独立新版 book id，不覆盖旧阅读包。
- 确认 MiniMax M3 在 Codex CLI 层可用，但当前内置 `multi_agent_v1.spawn_agent` 的模型列表不暴露 M3。

## 版本检查结果

`dbs-suite`：

- 本地路径：`/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite`
- 本地目录不是 Git 仓库。
- 本地 `PACKAGE.json` source：`https://github.com/dontbesilent2025/dbskill.git`，subdir=`skills`。
- 本地版本：`2.12.0+local`。
- upstream 最新版本：`2.15.1`。
- upstream 最新 commit：`096f726a20407901ca517cfc42509f96232fd0ea`。
- upstream 新增 Skill：`dbs-content-system`、`dbs-resonate`、`dbs-spread`、`dbs-wechat-html`。
- 本地旧包中的非 upstream Skill：`chatroom-austrian`、`dbskill-upgrade`、`evaluating-candidates`。按最新策略，它们不是默认保留项，只能作为“本地扩展候选”经用户批准后保留。
- 公共 upstream Skill 中 20 个 `SKILL.md` 均有变化；变化较大的包括 `dbs`、`dbs-agent-migration`、`dbs-chatroom`。

`gstack`：

- 本地路径：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack`
- 本地 HEAD：`11de390be1be6849eb9a15f91ff4922dd16c589a`
- upstream main HEAD：`11de390be1be6849eb9a15f91ff4922dd16c589a`
- 本地存在未跟踪文件 `.skillsctl-package.json`，但 upstream 版本本身无落后。

## M3 检查结果

- `~/.codex/config.toml` 已配置 `[model_providers.minimax]`。
- `MINIMAX_API_KEY` 环境变量存在。
- `~/.codex/minimax-executor.config.toml` 配置了 `model = "MiniMax-M3"`、`model_provider = "minimax"`。
- `codex exec --profile minimax-executor --skip-git-repo-check --ephemeral -s read-only ...` smoke 通过，模型输出 `M3_OK`。
- 当前 `multi_agent_v1.spawn_agent` 暴露的可选模型只有 GPT 系列，不含 MiniMax；因此 M3 不能直接作为内置子 agent model override 使用。
- 可用方式：主会话通过 CLI worker 调用 M3 做批量差异初筛、摘要、表格整理等体力活；最终判断和交付仍由主 Codex 审核。

## 下一步

新会话按 `docs/next-session-prompt.md` 执行：先更新本地 canonical package，再只交付 `dbs-suite__v2.15.1_096f726` 版本化试产，不覆盖旧 `dbs-suite`。

M3 暂不进入 ReaderLab 生产主线；已另开调研会话检查 Codex App 内是否能直接把 M3 作为子 agent 使用。

# 2026-06-29 ReaderLab v0.1 页面体验收口与正式刷新

## 摘要

- 下线当前 `重点与亮点` 默认功能：主阅读页不再输出 `## 重点与亮点`，机器状态和 validate 不再依赖 `highlights_chars`，测试不再断言 highlights。
- 主阅读页改为 `短导读 / 阅读地图 / Skill 正文 / 必要关联说明`。
- 移除读者页中的模板化 `Codex 吸收后的设计提炼`；相关追溯信息保留在 manifest 的 `codex_absorption`。
- `04_主控清单.md` 收敛为读者入口，只展示阅读单元、Skill、机器状态、人工状态和入口链接。
- 结构诊断页保持诊断语义，`setup-browser-cookies` 不伪装成普通完整页。
- 正式 LifeAtlas 200 的 `dbs-suite` 和 `gstack` 已用 `--force --preserve-comments` 重刷。
- 删除正式包中的指定虚拟测试批注，保留真实批注。

## 涉及文件

- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/decisions.md`
- `docs/complex-material-reading-sop.md`
- `docs/agent-run-ledger.md`
- `docs/next-session-prompt.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

## 已验证

```bash
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件，并在 Obsidian/LifeAtlas 200 区完成预览审阅与批注闭环" --readings-dir data/skill-readings --force --preserve-comments
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "把 gstack 作为复杂 Skill 包压力样本，生成可读、可批注、可讨论的 ReaderLab v0.1 阅读包" --readings-dir data/skill-readings --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md
```

结果：

- 单元测试：17 tests OK。
- `dbs-suite` validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 0 / human pending 23 / 1864 source blocks / `in_progress`。
- `gstack` validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59 / 14397 source blocks / `in_progress`。
- 正式包没有恢复 `11_机制说明` / `12_证据附录`。
- 正式包未发现旧读者页标题：`## 重点与亮点`、`## Codex 吸收后的设计提炼`、`## 当前位置`。
- 已删除虚拟批注：
  - `rl-virtual-dbs-xhs-title-001`
  - `rl-virtual-gstack-freeze-001`
  - `rl-virtual-gstack-setup-cookies-001` 当前未发现实际批注块
- 当前唯一保留真实批注：`rl-dbs-complex-001`，`comments-list` 显示 anchor found=true、thread_count=2。

## 下一步

下一轮进入正式页面人工抽读验收，不要重复本轮已完成的 highlights 下线和虚拟批注清理。优先检查 `dbs-diagnosis`、`dbs-xhs-title`、`dbs-save`、`dbs-report`、`benchmark-models`、`make-pdf`、`setup-browser-cookies` 和 `04_主控清单.md`。

# 2026-06-29 下一轮执行 Prompt 维护

## 摘要

- 按用户最新确认，维护 `docs/next-session-prompt.md`，下一轮目标改为：移除当前 `重点与亮点`、批量收口阅读地图/关联说明/Codex 吸收说明/主控清单/结构诊断语义，并直接刷新正式 LifeAtlas 200。
- 明确下一轮不走 `/private/tmp` 预览包；代码和测试通过后用 `--force --preserve-comments` 刷正式 `dbs-suite` 和 `gstack`。
- 明确旁通视角不在下一轮实现，后续单独设计。
- 同步 `docs/current-task.md` 和 `docs/dev-state.md`，避免下一轮被旧“先讨论样张、不刷新 LifeAtlas”的状态带偏。

## 验证

- 本轮只做项目文档维护，没有改代码，没有刷新 LifeAtlas。
- 已检查 `docs/next-session-prompt.md` 包含正式刷新命令、验证命令、抽查清单和协作方式。

---

# 2026-06-29 产品文档归档与旁通视角方向

## 摘要

- 将 Downloads 中两份 ReaderLab 原始产品文档复制到项目 `docs/` 下，作为项目内维护版。
- 明确“重点与亮点”当前定义不足：它混合了金句、价值提炼和外部启发，不能稳定服务复杂材料陪读。
- 将“旁通视角 / 跨材料新知”记录为长期方向候选，但不进入当前 v0.1 默认生成器。
- 旁通视角后续更适合独立 Skill、读后批注/提问触发，或基于 LifeAtlas/思维模型库/外部搜索的单独模块。

## 文件

- 新增/归档：`docs/readerlab-v0.1-light-prototype.md`
- 新增/归档：`docs/readerlab-future-roadmap-and-references.md`
- 更新：`docs/current-task.md`
- 更新：`docs/dev-state.md`
- 更新：`docs/decisions.md`
- 更新：`docs/complex-material-reading-sop.md`

## 验证

- 本轮只做文档维护，没有改代码，没有刷新 LifeAtlas。
- Downloads 原件未删除。

---

# Agent Run Ledger

## 2026-06-29 正式 LifeAtlas 200 状态字段重刷

### 已完成

- 按用户确认，用 `--force --preserve-comments` 重刷正式 LifeAtlas 200 的 `gstack` 和 `dbs-suite`。
- 正式包现在写入了 `machine_status`、`human_status`、可选 `human_review`，主控清单和组导读也显示“机器完成 / 人工验收”。
- 未改 gstack 或 DB Skill 源包；未写入 LifeAtlas `300/600/800`。

### 已验证

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --readings-dir data/skill-readings --force --preserve-comments
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite --title dbs-suite --goal "阅读 DB Skill 的设计方法、诊断框架和可迁移工作流" --readings-dir data/skill-readings --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
```

结果：

- `gstack` validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59 / in_progress。
- `dbs-suite` validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20 / in_progress。
- `dbs-suite` 批注迁移：found 1 / restored 1 / unresolved 0。
- `gstack` 批注迁移：found 1 / restored 0 / unresolved 1。未归位的是讨论区测试页 `benchmark-models-tandem插件闭环实测.md` 的测试批注，已保存在 `20_批注与讨论/批注迁移待处理.md`。
- `dbs-diagnosis`、`dbs-good-question`、`dbs-xhs-title` 在正式 `dbs-suite` manifest 中均为 `machine_status=completed`、`human_status=accepted`。

### 下一步

- 进入阅读单元规划升级：用更白话的说法，就是先让 ReaderLab 学会“这包材料应该分成哪几组读、为什么这么分、哪些分组不确定要人确认”，而不是继续把材料硬塞进现有目录。

## 2026-06-29 ReaderLab 机器完成 / 人工验收状态拆分

### 已完成

- `scripts/readerlab.py` 在 Skill manifest 记录中保留旧 `status`，新增 `machine_status`、`human_status` 和可选 `human_review`。
- `human_status` 默认 `pending`；已知人工认可的 DB 核心页 `dbs-diagnosis`、`dbs-good-question`、`dbs-xhs-title` 通过小型 `HUMAN_REVIEW_REGISTRY` 标记为 `accepted`。
- `validate` 继续只按机器状态判断通过/失败；旧 manifest 没有 `machine_status` / `human_status` 时分别兼容读取旧 `status` 和默认 `pending`。
- `validate` summary 新增 `human_accepted_skills`、`human_pending_skills`、`human_not_required_skills`。
- 主控清单、组导读和试跑记录现在同时展示机器完成进度和人工验收进度，避免把 validator 绿灯误说成阅读质量通过。
- 新增单元测试覆盖默认 pending、registry accepted、validate 不因人工 pending 失败、主控清单和组导读展示拆分状态。
- `docs/adversarial-review.md` 已同步当前状态，不再把“状态拆分”列为未完成风险。
- 未做主阅读页 / 机制说明 / 证据附录结构化；未重刷 LifeAtlas 200；未改 gstack 或 DB Skill 源包。

### 涉及文件

- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/adversarial-review.md`
- `docs/agent-run-ledger.md`
- `docs/next-session-prompt.md`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /private/tmp/readerlab-human-status-audit-20260629 --book-id dbs-suite --title dbs-suite --goal "验证机器完成与人工验收状态拆分" --readings-dir data/skill-readings --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-human-status-audit-20260629/dbs-suite
```

结果：

- 单元测试 16 tests OK；py_compile 通过。
- 真实 LifeAtlas `dbs-suite` 只读 validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human pending 23 / in_progress。
- 真实 LifeAtlas `gstack` 只读 validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human pending 59 / in_progress。
- 临时 DB 导入 validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20 / in_progress。
- 临时 DB manifest 中三页均为 `status=completed`、`machine_status=completed`、`human_status=accepted`。

### 下一步

- 回到阅读单元规划：让 `reading_units` 输出 reason、confidence、needs_human_review，并允许低置信内容进入 `90_待人工分组`。
- 后续用户已确认重刷，正式 LifeAtlas 200 的 `gstack` 和 `dbs-suite` 已在上一条运行记录中完成刷新。

## 2026-06-28 ReaderLab inventory-first 机制盘点修正

### 已完成

- 回应用户指出的“不能靠反复追问才发现隐藏机制”问题，把关联材料从人工枚举改为 inventory-first。
- `scripts/readerlab.py` 新增 Skill 构成发现层：扫描 `SKILL.md.tmpl`、`bin/`、`scripts/`、`sections/`、`templates/`、`docs/`、`src/`、测试参考和 hook command 引用。
- 已完成 Skill 页的关联材料区自动生成“机制盘点”和“执行机制”。
- hooks 现在会展示 matcher、command、解析到的机制文件，以及如何接入工具调用。
- `.tmpl` 纳入扫描范围；真实 gstack 扫描文件数从 1039 增至 1111。
- `manifest.json` 的 Skill 记录新增 `related_artifacts`，coverage 新增 `related_artifacts_count`、`has_execution_mechanism`、`hook_references_resolved` 等指标。
- 组导读不再把 ReaderLab 的状态汇总规则放进“重点与亮点”，改成阅读注意。
- 更新测试，断言 `freeze` 页必须展示 `### 机制盘点`、`### 执行机制`、`freeze/bin/check-freeze.sh`、`Edit`/`Write`，并在 manifest 中解析到 hook 机制文件。

### 涉及文件

- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/decisions.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill freeze
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：单元测试通过；普通 validate 通过；`freeze` 单项通过且 `related_artifacts_count=2`、`has_execution_mechanism=true`、`hook_references_resolved=true`；`--require-complete` 按预期失败，仍有 54 个 Skill 未完成。

## 2026-06-28 ReaderLab v0.1 代表性样本集扩展

### 已完成

- 按用户新方向，把四段式打样从 `freeze + unfreeze` 扩展为 5 个代表性 Skill：`unfreeze`、`freeze`、`careful`、`guard`、`gstack-upgrade`。
- 更新 `scripts/readerlab.py`，让已完成 Skill 页固定输出“导读 / Skill 正文 / 关联材料 / 重点与亮点”。
- 新增 `related_chars` 覆盖指标，确保关联材料不计入 Skill 正文译文覆盖。
- 为 `freeze`、`careful`、`guard`、`gstack-upgrade` 补充完整中文正文、关联材料说明和来源标注重点。
- 更新 `tests/test_readerlab.py`，测试 5 个完成样本、未完成 Skill 不生成占位页、关联材料区存在、`gstack-upgrade` 可单独验证。
- 重新生成 LifeAtlas gstack 输出。
- 同步 `docs/current-task.md`、`docs/dev-state.md` 和 `docs/decisions.md`。

### 涉及文件

- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/decisions.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill freeze
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill unfreeze
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill careful
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill guard
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill gstack-upgrade
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：单元测试通过；普通 validate 和 5 个 Skill 级 validate 均通过；`--require-complete` 按预期失败，报告整包仍为 `in_progress`，还有 54 个 Skill 未完成。

### 当前结果

- gstack 总 Skill：59。
- 已完成：5，`unfreeze`、`freeze`、`careful`、`guard`、`gstack-upgrade`。
- 未完成：54。
- 整包状态：`in_progress`。
- `02_审查与质量控制`：`2/12 已完成`。
- `05_发布交付与运维`：`3/9 已完成`。
- 未完成 Skill 仍不生成占位阅读页。

## 2026-06-28 ReaderLab 公共术语表与 Agent 精读边界确认

### 已完成

- 根据用户反馈，修正术语阅读顺序：术语解释不再放在正文之后的关联材料中。
- 新增公共术语页 `02_Skill阅读术语表.md`，集中解释 `frontmatter`、`hooks`、`PreToolUse`、`matcher`、`command`、`Bash`、`Edit`、`Write`、`bin/scripts`、`migrations`、`template/.tmpl`、`sections`、`src/lib`。
- 单页导读末尾前置术语表链接和本页重点术语，例如 `[[02_Skill阅读术语表]]`。
- 移除单页关联材料中的重复 `### 术语速读`，保留“机制盘点 / 执行机制”。
- 修正 `unfreeze` 旧样本中 `[!important] 高亮` 残留，统一为 `[!important] 重点`。
- 修正 `gstack-upgrade/migrations/*.sh` 分类，识别为“迁移脚本”，并在执行机制中说明它没有 hooks 但有迁移机制材料。
- 明确产品边界：当前 5 个完成页是人工精读打样页，不证明自动精读能力已经完成；下一阶段应设计 ReaderLab 专用 Agent/Skill 精读工作流。

### 涉及文件

- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/decisions.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill freeze
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill gstack-upgrade
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：单元测试和 py_compile 通过；普通 validate、`freeze`、`gstack-upgrade` 单页 validate 通过；`--require-complete` 按预期失败，仍有 54 个 Skill 未完成。

### 下一步

- 不继续靠手写 `COMPLETED_SKILL_TRANSLATIONS` 扩大完成页。
- 设计单 Skill 精读产物契约，由 Agent/Skill 产出导读、正文译文、关联材料解释、重点旁批和证据，ReaderLab 负责生成页面和验证。

## 2026-06-28 ReaderLab Agent 精读产物最小闭环

### 已完成

- 新增 Agent 精读 JSON 契约 `readerlab.skill-reading.v1`。
- `import-skills` 默认读取 `data/skill-readings/<book-id>/<skill>.json`，也支持 `--readings-dir` 指定目录。
- Agent 精读产物优先于旧的 `COMPLETED_SKILL_TRANSLATIONS`；旧 5 页人工样本仍作为兼容和打样保留。
- 新增 `data/skill-readings/gstack/benchmark-models.json`，作为跨模型评测 Skill 的试跑产物。
- ReaderLab 会把 Agent 产物的 `skill_body_translation` 放入 Skill 正文，把 `related_materials_explanation` 和 `evidence` 放入关联材料，自动机制盘点仍由源包扫描生成。
- 修复 `needs_review` 状态展示：
  - 有需复核页面时，组导读和主控清单必须链接页面。
  - `needs_review` 不计入已完成数。
  - 页面标题显示“需复核中文阅读页”。
  - 主控清单显示“需复核：路径”，不显示“待生成”。

### 当前结果

- gstack 总 Skill：59。
- 已完成：5，`unfreeze`、`freeze`、`careful`、`guard`、`gstack-upgrade`。
- 需复核：1，`benchmark-models`。
- 未完成：53。
- 整包状态：`in_progress`。
- `02_审查与质量控制`：`2/12 已完成`，另有 `1` 个需复核。
- `05_发布交付与运维`：`3/9 已完成`。

### 涉及文件

- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `data/skill-readings/gstack/benchmark-models.json`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/decisions.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill benchmark-models
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：单元测试和 py_compile 通过；普通 validate 通过；`benchmark-models` 单页 validate 通过但状态为 `needs_review`，覆盖 flags 为 `heading_coverage_incomplete`、`paragraph_coverage_low`、`code_blocks_not_preserved`；`--require-complete` 按预期失败，整包仍为 `in_progress`。

### 下一步

- 决定是把 `benchmark-models` 补到完整完成页，还是选择一个更小的中等 Skill 证明 Agent 产物可以达到 completed。
- 完善 Agent 产物生成流程，重点是完整正文翻译覆盖，而不是只产出摘要式需复核页。
- 失败诊断：`benchmark-models` 没有完成不是 ReaderLab JSON 读取失败，也不是页面生成失败；问题是 Agent 产物把 `SKILL.md` 做成压缩解读，未完整保留标题、段落和代码块。
- 修复方向：强化 Agent 产物任务契约，要求 `skill_body_translation` 逐标题、逐段落、逐代码块翻译；长 Skill 采用分块翻译和覆盖清单。

## 2026-06-28 下一阶段目标：分块精读流水线

### 结论

- 长 Skill 不能依赖 Agent 自己“for 循环”完整翻译；没有硬性分块协议和覆盖检查时，Agent 会倾向生成摘要式解读。
- 下一步目标是建设 ReaderLab 可控的分块精读流水线。

### 目标能力

- 从 `SKILL.md` 生成 block manifest：frontmatter、标题段、普通段落、代码块，包含 block id、行号、字符数、hash。
- 支持 block translation 产物：按 block id 保存译文和状态。
- 合并 block translation 为 Agent JSON 的 `skill_body_translation`。
- validator 能检查缺块、hash 不匹配、标题/段落/代码块覆盖不足。
- 缺块或覆盖不足时保持 `needs_review`，不误报 `completed`。

### 下一轮验收

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

## 2026-06-28 分块精读最小闭环实现

- 子 Agent 实现了 `block-manifest` CLI、`readerlab.skill-block-reading.v1` 分块产物读取、分块合并和 block 级校验。
- 改动范围：`scripts/readerlab.py`、`tests/test_readerlab.py`。
- 测试 fixture 证明：完整 block reading 可合并并标记 completed；缺块/hash 不匹配会产生 `block_issues`，状态保持 `needs_review`。
- 主线程验收：
  - `python3 tests/test_readerlab.py` 通过，3 tests OK。
  - `python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py` 通过。
  - 真实 `benchmark-models/SKILL.md` 可生成 146 个 block：frontmatter 1、heading 21、paragraph 107、code_block 17。
  - 真实 gstack 临时导入到 `/private/tmp/readerlab-verify/gstack` 成功，59 个 Skill，状态 `in_progress`。
  - 普通 validate 通过；`benchmark-models` 仍因旧 Agent 译文覆盖不足保持 `needs_review`；`--require-complete` 按预期失败。
- 已知问题：真实长 Skill 的切块里会出现少量仅为分隔线的 `---` 段落，后续应优化 block 过滤或归并策略。
- 下一步：调用 Agent 以 block manifest 为输入，为一个真实中等长度 Skill 生成 `readerlab.skill-block-reading.v1` 分块翻译产物，再跑 import 和 validate，争取让第一个真实 Agent 分块页达到 completed。

## 2026-06-28 第一份真实分块精读产物

- 子 Agent 为 `gstack-openclaw-ceo-review` 生成了 `data/skill-readings/gstack/gstack-openclaw-ceo-review.json`。
- 产物 schema：`readerlab.skill-block-reading.v1`。
- 源文件：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack/openclaw/skills/gstack-openclaw-ceo-review/SKILL.md`。
- block 覆盖：74/74，全部 `translated`，无空译文、无缺块、无 extra block、无 hash mismatch。
- 主线程抽查生成页：正文是完整中文译文，不是摘要；导读、关联材料和重点与亮点分层清楚。
- 正式 LifeAtlas 输出已刷新到 `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`。
- 验证结果：
  - `python3 tests/test_readerlab.py` 通过。
  - `python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py` 通过。
  - `python3 scripts/readerlab.py validate .../gstack --skill gstack-openclaw-ceo-review` 通过，status 为 `completed`，`reading_source=agent_block_reading`，`block_coverage=true`。
  - 普通整包 validate 通过：59 个 Skill，6 completed，1 needs_review，52 not_started，delivery_status 为 `in_progress`。
  - `--require-complete` 按预期失败，说明整包仍未误报完成。
- 当前组进度：
  - `02_审查与质量控制`：2/12 completed，1 needs_review。
  - `05_发布交付与运维`：3/9 completed。
  - `08_补充Skills索引`：1/6 completed。
- 下一步：再选 1-2 个真实中等长度 Skill 跑分块产物，确认这不是单例成功；同时继续优化 `---` 分隔线等无意义小 block 的切分策略。

## 2026-06-28 长 Skill 分块压力测试：benchmark-models

- 子 Agent 将 `data/skill-readings/gstack/benchmark-models.json` 从旧的摘要式 `readerlab.skill-reading.v1` 替换为 `readerlab.skill-block-reading.v1` 分块产物。
- 源文件：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack/benchmark-models/SKILL.md`。
- block 覆盖：146/146，全部 `translated`，无空译文、无缺块、无 extra block、无 hash mismatch。
- 首轮产物问题：结构 coverage 通过，但 94 个 block 带“中文译文：”前缀，并残留英文自然语言；主线程未接受，退回子 Agent 重修。
- 修复后抽查：
  - “中文译文：”残留数量：0。
  - `0047` 首次激活提示、`0075` artifacts sync 隐私门、`0080` telemetry 前置句、`0105` Plan Status Footer、`0115` prompt 选择、`0146` Important Rules 均已中文化。
  - 仍保留命令、路径、变量名、flag、状态值、工具名和 code block 原文，这是允许的技术标识保留。
- 正式 LifeAtlas 输出已刷新到 `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`。
- 验证结果：
  - `python3 tests/test_readerlab.py` 通过。
  - `python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py` 通过。
  - `python3 scripts/readerlab.py validate .../gstack --skill benchmark-models` 通过，status 为 `completed`，`reading_source=agent_block_reading`，`block_coverage=true`。
  - 普通整包 validate 通过：59 个 Skill，7 completed，0 needs_review，52 not_started，delivery_status 为 `in_progress`。
  - `--require-complete` 按预期失败，说明整包仍未误报完成。
- 当前组进度：
  - `02_审查与质量控制`：3/12 completed。
  - `05_发布交付与运维`：3/9 completed。
  - `08_补充Skills索引`：1/6 completed。
- 下一步：继续选择 1-2 个真实长 Skill 或中等长度 Skill 跑分块产物，并把“不能用英文原句冒充译文”纳入 Agent 产物质量验收。

## 2026-06-28 分块译文质量门机制化

- 新增 ReaderLab block 级译文质量门：
  - `translation_marker_residue:<block_id>`：译文中残留“中文译文：”等占位痕迹。
  - `english_sentence_residue:<block_id>`：非代码/非 frontmatter block 中英文自然语言残留异常高。
- 这些 issue 进入 `block_issues`，触发 `block_translation_incomplete`，页面保持 `needs_review`，不能进入 `completed`。
- 允许保留的英文范围：命令、路径、变量、flag、状态值、工具名、模型名、配置值、code block、必要专有名词。
- 测试已覆盖坏产物：构造“中文译文：+ 英文原句”的 block，验证它会被标为 `needs_review`，并在 validate 中产生 `block_reading` issue。
- 新质量门回扫发现 `gstack-openclaw-ceo-review-0070-paragraph` 的输出模板标签仍有英文残留；已把 `Mode`、`Strongest challenges`、`Recommended path` 等标签补成中英对照。
- 验证结果：
  - `python3 tests/test_readerlab.py` 通过。
  - `python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py` 通过。
  - 正式 `benchmark-models` validate 通过，status 为 `completed`，无 block issues。
  - 正式 `gstack-openclaw-ceo-review` validate 通过，status 为 `completed`，无 block issues。
  - 普通整包 validate 通过：59 个 Skill，7 completed，0 needs_review，52 not_started。
  - `--require-complete` 按预期失败。

## 2026-06-28 ReaderLab v0.1 标准修正与 gstack 样例清理

### 已完成

- 修正 ReaderLab 单个 Skill 阅读页边界：Skill 正文只做 `SKILL.md` 翻译，导读和重点不能替代正文。
- 修正 `unfreeze` 样例：承认源文很短，正文译文也应短；功能解释放在导读和重点区。
- 清理 LifeAtlas gstack 输出中的未验收占位页。
- 保留组导读和已验收 Skill 页；未完成 Skill 只留在主控清单和 manifest。
- 更新脚本和测试，避免用导读或重点补正文覆盖率。

### 涉及文件

- `README.md`
- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `docs/next-session-prompt.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill unfreeze
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

前三条通过。`--require-complete` 失败是当前预期结果，因为 gstack 仍有 58 个 Skill 未完成。

### 当前结果

- gstack 总 Skill：59
- 已完成：1，`unfreeze`
- 未完成：58
- 整包状态：`in_progress`
- 下一阶段目标：新增 `freeze`，让 `05_发布交付与运维` 变为 `2/9 已完成`，但整组和整包仍保持未完成。

## 2026-06-28 项目 MEM 初始化

### 已完成

- 新建 `AGENTS.md`，声明项目目的、启动顺序、memory map、边界和验证命令。
- 新建 `docs/current-task.md`，记录下一阶段唯一执行切片：`freeze + unfreeze` 四段式打样。
- 新建 `docs/dev-state.md`，记录当前事实和缺口。
- 新建 `docs/decisions.md`，记录耐久决策。
- 继续使用 `docs/agent-run-ledger.md` 记录运行历史。

### 本轮验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill unfreeze
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：前三条通过；最后一条按预期失败，报告整包仍为 `in_progress`，且仍有 58 个 Skill 未完成。

### 未创建

- `docs/research-log.md` 暂不创建，因为本阶段没有产生可复用外部研究结论。


## 2026-06-28 多子 Agent 小块拆分测试：benchmark

### 已完成

- 选择 `benchmark` 作为第二个真实长 Skill 压力样本：155 个 block，约 3.6 万字符，属于长 Skill 但低于 `qa/review` 的超大规模。
- 生成 block manifest，并按约 20 个 block 拆成 8 个 part：`data/skill-readings-work/gstack/benchmark/part-01..08-manifest.json`。
- 调用多个子 Agent 分别翻译 8 个互不重叠 part，输出 `readerlab.skill-block-reading-part.v1`：`part-01..08-reading.json`。
- 主线程合并 8 个 part 为正式 `data/skill-readings/gstack/benchmark.json`，schema 为 `readerlab.skill-block-reading.v1`。
- 正式 LifeAtlas 输出已刷新，新增 `10_中文精读/02_审查与质量控制/benchmark.md`。
- `02_审查与质量控制` 组导读已更新为 `4/12 已完成`。

### 过程发现

- 首次临时 validate 时，`benchmark` block 覆盖 155/155、hash 无误、无 block issues，但仍因 `heading_coverage_incomplete` 进入 `needs_review`。
- 主线程定位后确认：validator 的 `count_markdown_headings` 把 fenced code block 中的 Bash 注释 `# ...` 误计为 Markdown 标题。
- 已修复标题计数逻辑：跳过 fenced code block 内的内容。
- 新增单元测试 `test_markdown_heading_count_ignores_fenced_code_comments`，避免以后为了过验证去伪造标题。

### 涉及文件

- `scripts/readerlab.py`
- `tests/test_readerlab.py`
- `data/skill-readings/gstack/benchmark.json`
- `data/skill-readings-work/gstack/benchmark/part-*-manifest.json`
- `data/skill-readings-work/gstack/benchmark/part-*-reading.json`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/next-session-prompt.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /private/tmp/readerlab-benchmark-verify --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-benchmark-verify/gstack --skill benchmark
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "学习 gstack 的使用方式与优秀 Skill 设计" --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill benchmark
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：

- 单元测试通过：4 tests OK。
- `py_compile` 通过。
- 临时目录 `benchmark` validate 通过，status 为 `completed`，标题覆盖为 27/27，block 覆盖为 155/155。
- 正式 `benchmark` validate 通过，status 为 `completed`，无 validation issues。
- 正式整包 validate 通过：59 个 Skill，8 completed，0 needs_review，51 not_started，delivery_status 为 `in_progress`。
- `--require-complete` 按预期失败，说明整包仍未误报完成。

### 当前结果

- gstack 总 Skill：59。
- 已完成：8。
- 需复核：0。
- 未完成：51。
- `02_审查与质量控制`：4/12 completed。
- `05_发布交付与运维`：3/9 completed。
- `08_补充Skills索引`：1/6 completed。

### 下一步

- 继续选择一个不同类型的真实中等或较长 Skill，例如 `setup-browser-cookies`、`canary`、`devex-review`、`design-review`，重复小块拆分流程。
- 主线程继续负责合并、validate 和人工抽查；子 Agent 只负责互不重叠的 part 翻译。


## 2026-06-29 MEM Clean 阶段复盘与下一轮任务调整

### 已完成

- 按 MEM Clean 规则读取 `mem-clean` 和 `mem-contract`，确认项目复盘可以写入项目文档；可迁移到其他项目的经验只能先列候选，不能静默写入全局错题本。
- 读取 `~/.codex/global-knowledge/common-mistakes.md`，当前没有已存在条目，因此本轮候选都是新候选，不是复发 bump。
- 压缩 `docs/current-task.md`：移除阶段历史，改为下一轮唯一执行切片。
- 更新 `docs/dev-state.md`：加入下一轮 3-4 个 Skill 批量验证、耗时/消耗记录规则和候选 Skill。
- 更新 `docs/decisions.md`：新增 D-011 分块精读必须记录时间和可得消耗；D-012 稳定性测试应批量覆盖不同长度和类型。
- 更新 `docs/next-session-prompt.md`：新会话直接按 3-4 个 Skill、主会话验收、子 Agent 执行、记录耗时/token 可得性推进。
- 新建 `docs/project-retrospective.md`：盘点结构指标不等于质量、长文本摘要化、validator 误判、机制材料被正文掩盖等问题。

### 全局错题本候选

未写入全局错题本，等待用户批准后再由 MEM Clean 升维：

1. G-001：结构指标通过不等于内容质量通过。
2. G-002：长文本任务必须外部切块，不要依赖 Agent 自觉循环。
3. G-003：验证器误判时不要让产物迎合错误指标。

### 下一步

- 新会话使用 `docs/next-session-prompt.md` 启动。
- 优先选 3-4 个不同类型、不同长度的 Skill，例如 `setup-browser-cookies`、`canary`、`devex-review`、`design-review`。
- 每个 Skill 记录 `run-metrics.json`，包含耗时和 token 可得性。


## 2026-06-29 三个真实 Skill 分块闭环：setup-browser-cookies / make-pdf / canary

### 已完成

- 统计未完成 gstack Skill block 数，实际选择 3 个不同类型样本：
  - `setup-browser-cookies`：浏览器 / 登录态流程类，132 blocks，29,541 source chars，7 parts。
  - `make-pdf`：文档 / PDF 产出类，159 blocks，36,471 source chars，8 parts。
  - `canary`：发布后监控类，242 blocks，55,678 source chars，13 parts。
- 为每个 Skill 生成 `block-manifest.json` 和 `part-*-manifest.json`，位置在 `data/skill-readings-work/gstack/<skill>/`。
- 调用 3 个子 Agent 分别产出 `readerlab.skill-block-reading-part.v1` part 文件。
- 主线程合并为正式 `readerlab.skill-block-reading.v1`：
  - `data/skill-readings/gstack/setup-browser-cookies.json`
  - `data/skill-readings/gstack/make-pdf.json`
  - `data/skill-readings/gstack/canary.json`
- 正式 LifeAtlas 输出已刷新到 `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`。

### 质量门发现

- 首轮临时 validate 时，三页 block/hash 覆盖都完整，但都被 `english_sentence_residue` 拦下并保持 `needs_review`，没有误报 completed。
- `setup-browser-cookies` 首轮 1 个 block 命中英文残留：`setup-browser-cookies-0132-paragraph`；主线程修复后通过。
- `make-pdf` 首轮 1 个 block 命中英文残留：`make-pdf-0115-paragraph`；主线程修复后通过。
- `canary` 首轮 34 个 block 命中英文残留；退回原子 Agent 定点重译后通过。
- 这轮证明：质量门能拦住结构合格但正文未充分中文化的产物；长一点的流程型 Skill 仍需要返修。

### 运行指标

- `setup-browser-cookies`：132 blocks，7 parts，worker 总耗时记录 15.12 分钟，token usage 不可得。
- `make-pdf`：159 blocks，8 parts，worker 总耗时记录 2.38 分钟，token usage 不可得。
- `canary`：242 blocks，13 parts，worker 首轮总耗时记录 30.01 分钟；34-block 定点修复记录 0.73 分钟；token usage 不可得。
- part 级真实开始/结束时间未由工具稳定提供，已在 metrics 中使用 `part_time_unavailable` / `part_duration_unavailable` 记录，不做假估。

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /private/tmp/readerlab-gstack-validate --book-id gstack --title gstack --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-gstack-validate/gstack
python3 scripts/readerlab.py validate /private/tmp/readerlab-gstack-validate/gstack --skill setup-browser-cookies
python3 scripts/readerlab.py validate /private/tmp/readerlab-gstack-validate/gstack --skill make-pdf
python3 scripts/readerlab.py validate /private/tmp/readerlab-gstack-validate/gstack --skill canary
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill setup-browser-cookies
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill make-pdf
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill canary
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill benchmark
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：

- 单元测试通过：4 tests OK。
- `py_compile` 通过。
- 临时目录最终 validate 通过：59 total，11 completed，0 needs_review，48 not_started，delivery_status 为 `in_progress`。
- 正式目录 validate 通过：59 total，11 completed，0 needs_review，48 not_started，delivery_status 为 `in_progress`，validation_issues 为空。
- 三个新 Skill 单页 validate 均通过，status 为 `completed`。
- `benchmark` 回归 validate 通过，status 为 `completed`。
- `--require-complete` 按预期失败：整包仍为 `in_progress`，48 个 Skill 未完成。

### 当前结果

- gstack 总 Skill：59。
- 已完成：11。
- 需复核：0。
- 未完成：48。
- `02_审查与质量控制`：5/12 completed。
- `03_浏览器与设计工作流`：1/8 completed。
- `05_发布交付与运维`：3/9 completed。
- `06_Skill自进化与工具化`：1/4 completed。
- `08_补充Skills索引`：1/6 completed。

### 下一步

- 先抽查 `setup-browser-cookies`、`make-pdf`、`canary` 三页正文可读性，确认没有摘要化、夹带解释、英文自然语言残留或命令破坏。
- 如继续扩样本，优先选 `devex-review`（306 blocks）或 `design-shotgun`（311 blocks）；`design-review`（474 blocks）更适合单独长压测。


## 2026-06-29 质量返修与 validator 补强

### 已完成

- 按用户要求再迭代一轮，由子 Agent 执行、主线程验收。
- 子 Agent 1 返修阅读产物，只改允许范围内的 JSON：
  - `data/skill-readings/gstack/setup-browser-cookies.json`
  - `data/skill-readings/gstack/make-pdf.json`
  - `data/skill-readings/gstack/canary.json`
  - 对应 `data/skill-readings-work/gstack/<skill>/part-*-reading.json`
  - 对应 `run-metrics.json`
- 子 Agent 2 补强 validator，只改：
  - `scripts/readerlab.py`
  - `tests/test_readerlab.py`
- 主线程验收时发现新质量门还拦下旧完成页 `benchmark-models` 的 3 处英文代码注释残留，以及 `canary-0189` / `canary-0054` 两个漏点；已由主线程定点修复。

### 质量门新增

- `short_english_residue:<block_id>`：抓短英文指令句 / 提示句残留，例如以 `If`、`Only`、`Append`、`Ask`、`Check`、`Offer`、`Show`、`Print`、`Run`、`Use`、`Do not`、`Don't`、`Sure` 开头的自然英文说明。
- `code_comment_english_residue:<block_id>`：抓代码块中 `# ` 开头的英文自然语言说明注释。
- 保留豁免：命令、路径、flag、变量、状态值、工具名、模型名、CLI 输出字符串、code span 和明确标注的原始英文触发示例。
- 新 issue 继续走现有 `block_issues -> needs_review` 路径，没有另建状态分支。

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /private/tmp/readerlab-quality-repair --book-id gstack --title gstack --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-quality-repair/gstack
python3 scripts/readerlab.py validate /private/tmp/readerlab-quality-repair/gstack --skill setup-browser-cookies
python3 scripts/readerlab.py validate /private/tmp/readerlab-quality-repair/gstack --skill make-pdf
python3 scripts/readerlab.py validate /private/tmp/readerlab-quality-repair/gstack --skill canary
python3 scripts/readerlab.py validate /private/tmp/readerlab-quality-repair/gstack --skill benchmark-models
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --force
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill setup-browser-cookies
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill make-pdf
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill canary
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill benchmark-models
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill benchmark
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

结果：

- 单元测试通过：10 tests OK。
- `py_compile` 通过。
- 临时目录和正式目录 validate 均通过：59 total，11 completed，0 needs_review，48 not_started，delivery_status 为 `in_progress`，validation_issues 为空。
- `setup-browser-cookies`、`make-pdf`、`canary`、`benchmark-models`、`benchmark` 单页 validate 均为 `completed`。
- `--require-complete` 按预期失败，说明整包仍未误报完成。

### 当前结果

- gstack 总 Skill：59。
- 已完成：11。
- 需复核：0。
- 未完成：48。
- 整包状态：`in_progress`。

### 剩余风险

- 新质量门比旧门更严格，后续可能拦下旧完成页或新产物中的真实英文触发示例；如果是合理保留，应在译文中明确标注“原始英文触发示例”，或把英文放在 code span 中。
- 这轮仍不能用 `git status` 做边界核对，因为当前目录不是 Git 仓库；边界证明依赖写入路径、JSON 覆盖检查和 validate 输出。

## 2026-06-29 ReaderLab 根目标校正：从 Skill/gstack 过拟合回到复杂材料阅读化

### 背景

- 用户指出当前讨论和项目文档明显过拟合到 gstack / Skill 包。
- ReaderLab 最初目标不是只读 Skill，而是把电子书、长文、Markdown 文档、课程资料、访谈稿、代码文档、Skill 包和混合型资料转成 LifeAtlas 阅读包。
- gstack 只是第一组复杂压力样本，用来暴露“执行视图机械翻译不等于阅读理解”的问题。

### 调整

- 更新 `AGENTS.md`：项目目的改为“复杂材料阅读化”，gstack 改称当前压力样本。
- 重写 `README.md`：新增“内容分层”总纲，明确主阅读页负责理解、证据附录负责追溯。
- 重写 `docs/current-task.md`：当前唯一切片改为目标校正和通用分层验证，暂停惯性扩 gstack 样本。
- 重写 `docs/dev-state.md`：分离产品目标、当前实现事实、gstack 样本事实和已知缺口。
- 更新 `docs/decisions.md`：
  - D-001 收窄为旧 Skill 包实现约束。
  - D-009 收窄为证据覆盖约束。
  - 新增 D-014：ReaderLab 面向复杂材料阅读化，不是 Skill 专项。
  - 新增 D-015：主阅读页和证据附录分工。
  - 新增 D-016：不为单个样本包设专用通用规则。
- 重写 `docs/next-session-prompt.md`：下一会话先验证通用内容分层，不继续把 gstack 特征写成通用规则。

### 当前判断

- 旧的“Skill 正文完整翻译”仍可用于当前实现的证据覆盖，但不能再控制主阅读页形态。
- 后续 SOP 应命名和组织为复杂材料阅读化 SOP，而不是 Skill/gstack SOP。
- gstack 样本仍有价值，但只作为压力测试材料，不是方案的一等公民。

## 2026-06-29 对照初始材料补回 v0.1 陪读闭环

### 参考材料

- `/Users/tianqiang/Downloads/ReaderLab_v0.1_轻量原型.md`
- `/Users/tianqiang/Downloads/ReaderLab_后续功能与参考资料备忘.md`

### 关键校正

- 初始定位不是单纯“材料转换器”，而是本地 Markdown 优先的 Obsidian 陪读工具。
- v0.1 默认前提：Obsidian + Markdown + Codex + 现有批注插件。
- 最小闭环是：导入材料 -> 拆成 Markdown 书 -> 中文化 -> Obsidian 就地批注 -> Codex 读取批注和上下文并回复。
- 人类标注是核心；AI 预处理只降低阅读门槛，不能替代人的第一次阅读判断。
- v0.1 不自建批注系统，不做网页 UI、数据库、知识图谱、PDF/EPUB 完整导入、自动升格或自动生成 Skill。

### 文档更新

- `AGENTS.md`：补回“中文可读、可批注、可讨论、可沉淀”和 Obsidian/Markdown/Codex 批注闭环。
- `README.md`：新增 v0.1 默认前提、批注策略、Codex 围绕批注回复的验收要求。
- `docs/current-task.md`：当前切片改为校正根目标、阅读标准和陪读闭环。
- `docs/dev-state.md`：记录批注解析和就地回复尚未稳定实现，是 v0.1 缺口。
- `docs/decisions.md`：新增 D-017，明确 v0.1 不自建批注系统。
- `docs/next-session-prompt.md`：下一会话必须补测至少一种就地批注格式。

## 2026-06-29 上下文压缩前维护下一步计划

### 调整

- 更新 `docs/current-task.md`：把下一步拆成 A/B/C/D 四段：
  - A：先做样本内容分层表，不写生成器。
  - B：人工确认后只在 `20_批注与讨论/` 做 1-2 个预览样张。
  - C：实测 Markdown 原生或 Obsidian 插件批注链路。
  - D：通过人工判断后再 SOP 化或自动化。
- 更新 `docs/next-session-prompt.md`：固定下一轮优先样本为 `benchmark-models`、`make-pdf`、`gstack-openclaw-ceo-review`、`guard`/`unfreeze`，并明确每个样本只按五类内容分层。

### 边界

- 未改生成器。
- 未覆盖正式 LifeAtlas `completed` 页。
- 未改 gstack 源仓库。
- 下一轮仍应先验证阅读质量和批注闭环，再讨论 SOP 和自动化。

### 验证

```bash
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：通过。正式输出仍为 59 total / 11 completed / 0 needs_review / 48 not_started / `in_progress`，`validation_issues` 为空。

## 2026-06-29 ReaderLab A/B/C 预览验证与批注闭环实测

### 已完成

- 完成四类 gstack 压力样本的内容分层判断：
  - `benchmark-models`：外壳膨胀型，主线是模型横评，通用外壳和完整译文进入附录。
  - `make-pdf`：执行流程型，setup、核心命令、输出契约和退出码进入主阅读线，源码和测试 fixture 进入追溯材料。
  - `gstack-openclaw-ceo-review`：判断框架型，主体原则和 11 个审查章节不能摘要化失真。
  - `guard`：短护栏型，保持短，只讲组合关系、hook 生效点和生命周期。
- 在 `20_批注与讨论/` 新增预览样张：
  - `make-pdf-阅读分层预览.md`
  - `guard-阅读分层预览.md`
- 在 `20_批注与讨论/` 新增 Markdown 原生批注闭环实测：
  - `benchmark-models-批注闭环实测.md`
- 批注实测使用 `==高亮==`、`%%读者批注%%` 和紧邻原文的 callout 回复；Codex 回复只围绕附近上下文解释，不重写全文，不堆到文末。
- 更新 `docs/current-task.md`、`docs/dev-state.md` 和 `docs/next-session-prompt.md`，把下一步从“继续做 A/B/C”改为“人工验收当前预览，确认后再 SOP / 自动化”。

### 涉及文件

- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/next-session-prompt.md`
- `docs/agent-run-ledger.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/20_批注与讨论/benchmark-models-批注闭环实测.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/20_批注与讨论/make-pdf-阅读分层预览.md`
- `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/20_批注与讨论/guard-阅读分层预览.md`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：10 tests OK。
- 普通 validate 通过：59 total，11 completed，0 needs_review，48 not_started，delivery_status 为 `in_progress`，validation_issues 为空。
- 正式 completed 页未覆盖；新增内容只在 `20_批注与讨论/`。
- 未改 gstack 源仓库，未新增依赖，未写入 LifeAtlas `300/600/800`。

### 下一步

- 等用户人工检查 `benchmark-models-手工样张.md`、`make-pdf-阅读分层预览.md`、`guard-阅读分层预览.md`。
- 如果方向确认，再进入复杂材料阅读化 SOP 或生成器双层输出设计。
- 如果方向不稳，优先用非 Skill 材料再做小样本验证，而不是继续扩大 gstack。

## 2026-06-29 批注闭环方向纠偏：不能用手搓 Markdown 替代 Obsidian 插件

### 用户反馈

- 用户认可一、二、三类阅读分层预览方向“还可以”。
- 用户指出第四项批注闭环方向有误：项目已明确应通过 Obsidian 里的插件实现，不能越过插件手动搓 `==高亮==`、`%%评论%%`、callout 回复格式来冒充插件闭环。

### 调整

- `benchmark-models-批注闭环实测.md` 降级为 Markdown 原生兜底格式探索，不再作为 v0.1 插件批注闭环通过证据。
- 更新 `docs/current-task.md`：C 阶段改为“先补真实 Obsidian 插件批注链路”。
- 更新 `docs/dev-state.md`：记录 Obsidian 插件真实存储格式仍是缺口。
- 更新 `docs/next-session-prompt.md`：下一步先确认 LifeAtlas 当前启用的 Obsidian 批注插件及其真实 Markdown 存储格式。

### 下一步

- 只读检查 LifeAtlas `.obsidian` 插件配置，确认启用的是 Reading Comments、Comments，还是其他插件。
- 找到插件真实写入格式，或请用户在 Obsidian 里做一个最小批注样本后再读取文件。
- 用真实插件格式验证 Codex 能读取批注附近上下文，并把回复写回对应位置附近。
- 只有插件格式不支持就地回复时，才允许使用最接近原文位置的 Markdown callout 作为 fallback。

## 2026-06-29 tandem-comments 真实插件闭环实测

### 已完成

- 只读检查 LifeAtlas `.obsidian/community-plugins.json`，当前启用插件包括 `tandem-comments`。
- 读取 `/Users/tianqiang/LifeAtlas/.obsidian/plugins/tandem-comments/manifest.json`，确认插件描述为 quote-anchored threads，存储在文件末尾 fenced block，正文保持不变。
- 读取插件实现，确认真实存储格式：
  - fenced block：` ```tandem-comments `
  - JSON 顶层对象按 comment id 存储。
  - 每条 comment 包含 `anchor.exact`、`prefix`、`suffix`、`pos`、`status`、`thread`。
- 新增真实插件格式实测文件：
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/20_批注与讨论/benchmark-models-tandem插件闭环实测.md`
- 用 `comments-list` 读取该文件，anchor 定位成功，`actual_pos` 与 `stored_pos` 一致，prefix/suffix 均匹配。
- 用 `comments-reply` 追加 Codex 回复到同一个 `rl-plugin-001` thread。
- 再次 `comments-list`，thread_count 从 1 变为 2，latest 为 Codex 回复。

### 结论

- 之前的 `benchmark-models-批注闭环实测.md` 只能作为 Markdown 原生兜底探索。
- v0.1 的插件批注闭环应以 `tandem-comments` 真实格式为当前目标。
- ReaderLab 现有 `comments-list` / `comments-reply` 与当前启用插件格式一致，可以作为最小闭环基础。

### 已验证

```bash
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/20_批注与讨论/benchmark-models-tandem插件闭环实测.md
python3 scripts/readerlab.py comments-reply /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/20_批注与讨论/benchmark-models-tandem插件闭环实测.md rl-plugin-001 --author Codex --text '不只是省钱。结合附近上下文，dry-run 先确认 Claude、GPT/Codex、Gemini 哪些服务已经登录并可调用；不可用模型会被跳过。如果直接跑正式评测，可能花了时间和调用成本后才发现结果不可比。'
python3 tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- `comments-list` 定位成功，回复后 thread_count=2。
- 单元测试通过：10 tests OK。
- 普通 validate 通过：59 total，11 completed，0 needs_review，48 not_started，delivery_status 为 `in_progress`，validation_issues 为空。

## 2026-06-29 复杂材料阅读化 SOP 与 DB Skill 非 gstack 测试

### 已完成

- 新增 `docs/complex-material-reading-sop.md`，固化复杂材料阅读化流程：
  - 先判断材料类型。
  - 再做五类内容分层。
  - 输出主阅读页、机制说明、证据附录和 `tandem-comments` 批注线程。
  - 明确 Markdown 原生批注只能作为 fallback 探索，不能替代插件格式。
- 确认本地存在 DB Skill 包：
  - 路径：`/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite`
  - 来源：`https://github.com/dontbesilent2025/dbskill.git`
  - 本地版本：`2.12.0+local`
  - Skill 数：23
- 用 `dbs-suite` 做非 gstack 样本测试，新增 `docs/dbskill-readerlab-test-report.md`。
- 临时导入 DB Skill 到 `/private/tmp/readerlab-dbskill-test/dbs-suite`，未写入 LifeAtlas。
- 选择 `dbs-save` 和 `dbs-report` 做人工分层验收：
  - `dbs-save`：状态/流程型材料。
  - `dbs-report`：报告/证据汇总型材料。

### 测试结论

- SOP 层面：PASS。DB Skill 能按同一套五类内容分层，不依赖 gstack 特征。
- ReaderLab 导入层面：PASS。`import-skills` 和 validate 都能处理 `dbs-suite`。
- 当前生成器成品页能力：PARTIAL。没有 DB Skill 精读产物，所以 23 个 Skill 全部为 `not_started`。
- 新暴露问题：未知 Skill 包被整体放入 `08_补充Skills索引`，说明分组策略仍有 gstack/Skill 包时代残留。

### 已验证

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /private/tmp/readerlab-dbskill-test --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件" --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-dbskill-test/dbs-suite
python3 scripts/readerlab.py block-manifest /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-save/SKILL.md --skill dbs-save --source-file dbs-save/SKILL.md
python3 scripts/readerlab.py block-manifest /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-report/SKILL.md --skill dbs-report --source-file dbs-report/SKILL.md
```

结果：

- DB Skill 临时导入：25 files scanned / 23 skills / 1 reading unit / `in_progress`。
- DB Skill validate：通过，23 total / 0 completed / 0 needs_review / 23 not_started / 1864 source blocks。
- `dbs-save` 与 `dbs-report` block manifest 均可生成。

### 下一步

- 把 SOP 转成生成器数据结构：主阅读页、机制说明、证据附录、批注线程。
- 修正非 gstack Skill 包分组策略。
- 以 `dbs-save` 和 `dbs-report` 为第一组 DB Skill completed 预览样本，而不是直接扩大到整个 `dbs-suite`。

## 2026-06-29 DB Skill completed 预览与批注闭环补测

### 背景

用户指出前一阶段只完成了 SOP 和材料确认，没有完成最关键的真实精读样张。复核后确认无外部阻碍，主要缺口是没有 DB Skill 精读产物，也没有让生成器实际产出 completed 页面。

### 已完成

- 修改 `scripts/readerlab.py`：
  - 增加 `GENERIC_GROUP_KEYWORDS`，用通用关键词把 `save`、`report`、`restore` 等状态/报告型 Skill 归入 `04_上下文记忆与知识沉淀`。
  - 新增 `text_field()`，允许精读 JSON 的 `guide`、`skill_body_translation`、`related_materials_explanation` 使用字符串或段落数组，方便维护复杂材料精读正文。
- 新增 DB Skill 精读产物：
  - `data/skill-readings/dbs-suite/dbs-save.json`
  - `data/skill-readings/dbs-suite/dbs-report.json`
- 重新临时导入 `dbs-suite` 到 `/private/tmp/readerlab-dbskill-test/dbs-suite`。
- 生成 completed 预览页：
  - `/private/tmp/readerlab-dbskill-test/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-save.md`
  - `/private/tmp/readerlab-dbskill-test/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-report.md`
- 在 `dbs-save.md` 上补测真实 `tandem-comments` 批注闭环：
  - 初始 comment id：`rl-dbskill-001`
  - anchor exact：`不要存空文件。`
  - `comments-list` 定位成功，`actual_pos=stored_pos=1749`，prefix/suffix 均匹配。
  - `comments-reply` 追加 Codex 回复成功。
  - 再次 `comments-list`，thread_count 从 1 变 2。
- 更新项目状态文档：
  - `docs/current-task.md`
  - `docs/dev-state.md`
  - `docs/dbskill-readerlab-test-report.md`
  - `docs/next-session-prompt.md`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /private/tmp/readerlab-dbskill-test --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件" --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-dbskill-test/dbs-suite
python3 scripts/readerlab.py comments-list /private/tmp/readerlab-dbskill-test/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-save.md
python3 scripts/readerlab.py comments-reply /private/tmp/readerlab-dbskill-test/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-save.md rl-dbskill-001 --author Codex --text "是。这里的关键不是文件有没有写出来，而是不能把没有诊断内容的对话写成可恢复状态；否则后续 dbs-restore 和 dbs-report 会把空状态当成事实来源。"
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：10 tests OK。
- DB Skill 临时导入：25 files scanned / 23 skills / 6 reading units / `in_progress`。
- DB Skill validate：通过，23 total / 2 completed / 0 needs_review / 21 not_started / 1864 source blocks。
- `dbs-save` coverage：flags 为空，heading 18/18，paragraph 48/58，code 4/4。
- `dbs-report` coverage：flags 为空，heading 15/15，paragraph 57/65，code 3/3。
- DB 批注闭环：回复后 thread_count=2，anchor 仍定位成功。
- gstack validate：通过，59 total / 11 completed / 0 needs_review / 48 not_started / 14397 source blocks / `in_progress`。

### 剩余边界

- 这次只证明 `dbs-save` 和 `dbs-report` 两个 DB Skill completed 预览可生成并通过机器验收，不能声称整个 `dbs-suite` 已完成。
- validator 仍不能替代人工阅读质量判断；用户需要审阅两个 DB 预览页是否真的符合“复杂材料陪读”。
- 分组策略已改善但未完全解决，仍有 15 个 DB Skill 暂归 `08_补充Skills索引`。

## 2026-06-29 DB Skill 落到 LifeAtlas 200 与 Obsidian 路径纠偏

### 背景

用户指出“不写 LifeAtlas `300/600/800`”不能解释为什么没有写 LifeAtlas `200`。这是 A/B 规则混淆：ReaderLab 阅读包应该进入 `200_原始资料/270_电子书与书籍资料/`；禁止写入的是 `300/600/800` 正式沉淀区。

### 已完成

- 确认 `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/` 下原本没有 `dbs-suite`。
- 将 DB Skill 阅读包生成到 LifeAtlas 200：
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite`
- 生成的 completed 预览页：
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-save.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-report.md`
- 在 LifeAtlas 200 的 `dbs-save.md` 中写入真实 `tandem-comments` comment block：
  - comment id：`rl-dbs-lifeatlas-001`
  - anchor exact：`不要存空文件。`
  - `comments-list` 定位成功，`actual_pos=stored_pos=1749`，prefix/suffix 均匹配。
  - `comments-reply` 追加 Codex 回复成功。
  - 再次 `comments-list`，thread_count 从 1 变 2。
- 更新项目状态文档，去掉“只在 `/private/tmp` 验收”的当前事实表述：
  - `docs/current-task.md`
  - `docs/dev-state.md`
  - `docs/dbskill-readerlab-test-report.md`
  - `docs/next-session-prompt.md`

### 已验证

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件，并在 Obsidian/LifeAtlas 200 区完成预览审阅与批注闭环"
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-save.md
python3 scripts/readerlab.py comments-reply /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/04_上下文记忆与知识沉淀/dbs-save.md rl-dbs-lifeatlas-001 --author Codex --text "是。这里的关键不是文件有没有写出来，而是不能把没有诊断内容的对话写成可恢复状态；否则后续 dbs-restore 和 dbs-report 会把空状态当成事实来源。"
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 tests/test_readerlab.py
```

结果：

- DB Skill LifeAtlas 200 validate：通过，23 total / 2 completed / 0 needs_review / 21 not_started / 1864 source blocks / `in_progress`。
- DB 批注闭环：回复后 thread_count=2，anchor 仍定位成功。
- gstack validate：通过，59 total / 11 completed / 0 needs_review / 48 not_started / 14397 source blocks / `in_progress`。
- 单元测试通过：10 tests OK。

## 2026-06-29 DB Skill 复杂核心样本补测与分组机制结论

### 背景

用户指出两个问题：

- 当前 Skill 分组看起来沿用了 gstack 固定组，是否写死、是否适用于所有 Skill 包不清楚。
- DB Skill 抽样只选了 `dbs-save`、`dbs-report`，这两个是状态/报告边缘功能，不能证明 ReaderLab 对 DB Skill 核心复杂材料有效。

### 已确认

- 当前分组机制确实不是通用语义分组，而是：
  - gstack 时代的固定 `GROUP_RULES`；
  - 外加 `GENERIC_GROUP_KEYWORDS` 关键词兜底。
- 它不适用于所有 Skill。遇到不适配的 Skill，当前会落入 `08_补充Skills索引`，这只能作为待分组索引，不应被当成成品阅读单元。
- DB Skill 中更复杂的样本包括：
  - `dbs-xhs-title`：13716 chars / 109 headings / 75 个公式的长库型材料。
  - `dbs-diagnosis`：9353 chars / 61 headings / 商业模式诊断核心框架。
  - `dbs-good-question`：7038 chars / 67 headings / 问题说明书与 Agent 可解性框架。
  - `dbs-decision`：5923 chars / 41 headings / 个人决策系统。

### 已完成

- 新增复杂核心样本精读产物：
  - `data/skill-readings/dbs-suite/dbs-diagnosis.json`
  - `data/skill-readings/dbs-suite/dbs-good-question.json`
  - `data/skill-readings/dbs-suite/dbs-xhs-title.json`
- 重建 LifeAtlas 200 的 `dbs-suite` 阅读包。
- 新增 completed 预览页：
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/07_专门场景与问题调查/dbs-diagnosis.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/08_补充Skills索引/dbs-good-question.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/08_补充Skills索引/dbs-xhs-title.md`
- 在复杂核心页 `dbs-diagnosis.md` 上补测真实 `tandem-comments`：
  - comment id：`rl-dbs-complex-001`
  - anchor exact：`你的核心工作不是回答问题，是消解问题。`
  - `comments-list` 定位成功，`actual_pos=stored_pos=721`，prefix/suffix 均匹配。
  - `comments-reply` 追加 Codex 回复成功。
  - 再次 `comments-list`，thread_count 从 1 变 2。

### 已验证

```bash
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/07_专门场景与问题调查/dbs-diagnosis.md
python3 scripts/readerlab.py comments-reply /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/07_专门场景与问题调查/dbs-diagnosis.md rl-dbs-complex-001 --author Codex --text "是。附近上下文把它和 6 条商业公理、问诊/体检双路径连在一起：这个 Skill 不是先顺着用户的问题回答，而是先判断问题在语言、假设、逻辑、事实或信息充分性层面是否成立。"
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 tests/test_readerlab.py
```

结果：

- DB Skill LifeAtlas 200 validate：通过，23 total / 5 completed / 0 needs_review / 18 not_started / 1864 source blocks / `in_progress`。
- 复杂核心页批注闭环：回复后 thread_count=2，anchor 仍定位成功。
- gstack validate：通过，59 total / 11 completed / 0 needs_review / 48 not_started / 14397 source blocks / `in_progress`。
- 单元测试通过：10 tests OK。

### 结论

- 复杂样本生成链路通过：ReaderLab 可以把 DB Skill 中更复杂的核心样本生成 Obsidian 可见 completed 预览页，并完成插件批注回复闭环。
- 分组机制没有通过产品验收：`dbs-good-question` 和 `dbs-xhs-title` 作为复杂核心样本仍落入 `08_补充Skills索引`。下一步应把分组改成材料包级阅读单元规划，而不是继续扩关键词或硬套 gstack 七组。

## 2026-06-29 阅读角色分组调整与 DB Skill 重刷

### 背景

用户要求直接执行两件事：

- 调整分组方法，不再沿用 gstack 固定组或简单关键词兜底。
- 重刷 DB Skill 阅读包。

同时用户要求把其他高概率流程问题整理出来，先展示问题和解决思路，不执行。

### 已完成

- 修改 `scripts/readerlab.py`：
  - 删除 gstack 固定 `GROUP_RULES` 的通用地位。
  - 引入通用阅读角色分类：
    - `01_核心入口与总览`
    - `02_诊断审查与质量判断`
    - `03_问题决策与行动系统`
    - `04_内容表达与素材模板`
    - `05_状态记忆与报告`
    - `06_Agent工具与迁移工作台`
    - `07_流程执行与交付运维`
    - `90_待人工分组`
  - 分类使用 Skill 名称、标题和 description 评分；低置信或并列冲突进入 `90_待人工分组`。
  - 去掉把 `dbs` 包名前缀当作“入口”的规则，避免所有 DB Skill 与入口组打平。
- 更新 `tests/test_readerlab.py` 中旧分组路径断言。
- 重刷 LifeAtlas 200 的 `dbs-suite` 阅读包。
- 新分组结果：
  - `01_核心入口与总览`：`dbs`
  - `02_诊断审查与质量判断`：`dbs-ai-check`、`dbs-benchmark`、`dbs-deconstruct`、`dbs-diagnosis`、`evaluating-candidates`
  - `03_问题决策与行动系统`：`dbs-action`、`dbs-decision`、`dbs-goal`、`dbs-good-question`、`dbs-learning`、`dbs-slowisfast`
  - `04_内容表达与素材模板`：`chatroom-austrian`、`dbs-chatroom`、`dbs-chatroom-austrian`、`dbs-content`、`dbs-hook`、`dbs-xhs-title`
  - `05_状态记忆与报告`：`dbs-report`、`dbs-restore`、`dbs-save`
  - `06_Agent工具与迁移工作台`：`dbs-agent-migration`、`dbskill-upgrade`
  - 当前无 DB Skill 进入 `90_待人工分组`。
- 重刷后重新在 `dbs-diagnosis.md` 写入 `tandem-comments` 并追加 Codex 回复：
  - 新路径：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md`
  - comment id：`rl-dbs-complex-001`
  - 回复后 thread_count=2，anchor 定位成功。
- 新增 `docs/adversarial-review.md`，整理高概率流程问题和解决思路，暂不执行。
- 更新状态文档：
  - `docs/current-task.md`
  - `docs/dev-state.md`
  - `docs/dbskill-readerlab-test-report.md`
  - `docs/next-session-prompt.md`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py comments-list /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：10 tests OK。
- DB Skill LifeAtlas 200 validate：通过，23 total / 5 completed / 0 needs_review / 18 not_started / 1864 source blocks / `in_progress`。
- DB 复杂核心页批注闭环：thread_count=2，anchor 仍定位成功。
- gstack validate：通过，59 total / 11 completed / 0 needs_review / 48 not_started / 14397 source blocks / `in_progress`。

### 剩余边界

- 当前分组已经不再硬套 gstack 七组，但仍是规则分类器，还不是完整的材料包级规划产物。
- 下一步应为 reading_units 增加 reason、confidence、needs_human_review。
- `import-skills --force` 会覆盖已有页面和批注，这是 `docs/adversarial-review.md` 中的最高优先级问题。

## 2026-06-29 核心风险归纳与当前决策补回

### 背景

用户要求重新从已有项目文档归纳真正要警惕的核心问题，而不是只根据口头讨论补几条；同时要求把当前已经明确的决策纳入文档，并说明下一步 Codex 和用户各自要做什么。

### 已完成

- 重写 `docs/adversarial-review.md`，从 `AGENTS.md`、`README.md`、`docs/decisions.md`、`docs/project-retrospective.md`、`docs/current-task.md`、`docs/dev-state.md` 和运行账本中归纳核心问题：
  - 结构通过不等于阅读质量通过。
  - 长材料容易被摘要化、漏译或贴回原文。
  - 样本结构会污染通用规则。
  - Obsidian 批注是核心数据，重建阅读包可能破坏闭环。
  - 源材料里的指令不能污染当前 Codex 行为。
  - 厚页不是错误，过早拆分和过早摘要才是错误。
  - 临时目录验证不能替代 Obsidian 真实路径验证。
  - 当前实现仍偏 Skill 包，非 Skill 材料尚未验证。
- 更新 `docs/decisions.md`，新增：
  - D-018：阅读单元不是固定书架。
  - D-019：厚页可接受，摘要化不可接受。
  - D-020：重建阅读包必须保护批注。
  - D-021：机器完成不等于人工验收。
- 更新 `docs/current-task.md`、`docs/dev-state.md`、`docs/next-session-prompt.md`，把下一步顺序调整为：
  1. 批注保护。
  2. 可人工确认的 reading_units 规划。
  3. 机器完成 / 人工验收状态拆分。
  4. 主阅读页 / 机制说明 / 证据附录结构化。
- 更新 `README.md`，把批注插件方向从旧的候选插件表述纠正为当前已验证的 `tandem-comments`。
- 更新 `docs/dbskill-readerlab-test-report.md` 和 `docs/next-session-prompt.md` 中 DB Skill completed 页路径，修正分组调整前的旧目录名。

### 已验证

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：10 tests OK。
- DB Skill LifeAtlas 200 validate：通过，23 total / 5 completed / 0 needs_review / 18 not_started / 1864 source blocks / `in_progress`。
- gstack validate：通过，59 total / 11 completed / 0 needs_review / 48 not_started / 14397 source blocks / `in_progress`。

### 下一步分工

- Codex 下一步先实现重建前批注保护，不继续批量扩 gstack 或 DB Skill。
- 用户下一步人工审阅 DB Skill 5 个 completed 预览页，重点判断 `dbs-diagnosis`、`dbs-good-question`、`dbs-xhs-title` 是否真的适合阅读；尤其确认 `dbs-xhs-title` 这种厚页第一版是否可接受，是否需要人工二次拆解。

## 2026-06-29 重建前 Obsidian 批注保护实现

### 背景

用户确认 DB Skill 三个核心样本内容完整性基本合格，要求继续推进。下一步按既定计划实现“重建阅读包前保护 Obsidian 批注”。

### 已完成

- 修改 `scripts/readerlab.py`：
  - 新增 `tandem-comments` 扫描：重建前扫描目标阅读包内所有 `.md` 文件末尾的 fenced block。
  - `import-skills --force` 遇到已有 `tandem-comments` 时默认失败，且不执行 `shutil.rmtree(book_dir)`。
  - 新增 `--preserve-comments`：显式启用后允许重建，并迁移或保存批注。
  - 批注迁移优先写回同一相对路径；如果分组导致页面路径变化，则通过旧/新 manifest 的 skill name 映射到新 reading page。
  - 能定位 anchor 的批注写回目标页；不能定位或目标页不存在的批注写入 `20_批注与讨论/批注迁移待处理.md`。
  - 处理过批注时写入 `20_批注与讨论/批注迁移记录.md`。
  - `manifest.json` 新增 `comment_preservation` 摘要：found / restored / unresolved / source_pages 等。
- 修改 `tests/test_readerlab.py`，新增 5 个批注保护单元测试：
  - 目标无批注时 `--force` 仍可重建。
  - 目标有批注时仅 `--force` 必须失败，原文件保留。
  - `--force --preserve-comments` 可恢复可定位批注。
  - anchor 失效时批注进入待处理页，原 thread 和 anchor 保留。
  - 页面分组路径变化时，通过 manifest 映射迁移到新路径。
- 更新状态文档：
  - `docs/current-task.md`
  - `docs/dev-state.md`
  - `docs/adversarial-review.md`
  - `docs/next-session-prompt.md`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：15 tests OK。
- py_compile 通过。
- DB Skill LifeAtlas 200 validate：通过，23 total / 5 completed / 0 needs_review / 18 not_started / 1864 source blocks / `in_progress`。
- gstack validate：通过，59 total / 11 completed / 0 needs_review / 48 not_started / 14397 source blocks / `in_progress`。

### 剩余边界

- 批注保护当前只覆盖 `tandem-comments`，不覆盖 Markdown 原生 `==高亮==`、`%%评论%%`、callout。
- 本轮只用临时目录测试迁移逻辑，没有重刷 LifeAtlas 200 的 gstack 或 dbs-suite。
- 下一步优先级变为：可人工确认的 `reading_units` 规划，其次是机器 completed / 人工 accepted 状态拆分。

## 2026-06-29 阅读路线规划合并与结构优先实现

### 背景

用户指出“阅读路线规划”不是新路线，早期原型和现有 README/SOP/D-018 已有同一方向；本轮目标是合并重复文档，并把代码从文件名/关键词分组改成先读整体结构。

### 已完成

- 更新 `docs/complex-material-reading-sop.md`，新增“阅读路线规划”作为唯一主规则：
  - Skill 包先读包入口、路由关系、`SKILL.md` 正文职责、脚本/模板职责。
  - 图书/长文后续按书名、前言、目录和章节结构规划。
  - 结构不清时输出材料结构诊断，不让用户替机器分组。
- 更新 D-018：
  - `reading_units` 规划记录用途、判断理由、判断依据和把握程度。
  - “待人工分组”不再是正常出口。
- 修改 `scripts/readerlab.py`：
  - manifest 的 Skill 记录新增 `route_reason`、`route_basis`、`route_confidence`、`structure_status`。
  - `reading_units` 新增 `purpose`、`reason`、`basis`、`confidence`、`structure_status`。
  - 新增 `material_structure` 诊断摘要。
  - 文件名和关键词降级为辅助线索；入口、正文职责和支持文件职责优先。
  - 结构不清的材料进入 `90_材料结构诊断`，不再使用旧 `90_待人工分组`。
- 更新 `tests/test_readerlab.py`：
  - 覆盖路线字段写入。
  - 覆盖结构不清测试包输出材料结构诊断。
  - 保持 DB 三个已人工认可核心页的 human accepted 逻辑。
- 更新活跃文档：
  - `docs/current-task.md`
  - `docs/dev-state.md`
  - `docs/adversarial-review.md`
  - `docs/dbskill-readerlab-test-report.md`
  - `docs/next-session-prompt.md`

### 临时输出验证

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /private/tmp/readerlab-route-plan-audit --book-id dbs-suite --title dbs-suite --goal "验证结构优先阅读路线规划" --force
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /private/tmp/readerlab-route-plan-audit --book-id gstack --title gstack --goal "验证结构优先阅读路线规划" --force
python3 scripts/readerlab.py validate /private/tmp/readerlab-route-plan-audit/dbs-suite
python3 scripts/readerlab.py validate /private/tmp/readerlab-route-plan-audit/gstack
```

结果：

- 临时 `dbs-suite` 导入通过：23 skills / 6 reading units / `in_progress`。
- 临时 `dbs-suite` validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20。
- `dbs` 被识别为 `01_核心入口与总览`。
- `dbs-diagnosis`、`dbs-good-question`、`dbs-xhs-title` 仍为 human accepted。
- 临时 `gstack` 导入通过：59 skills / 7 reading units / `in_progress`。
- 临时 `gstack` validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59。
- 临时 `gstack` 未恢复 gstack 专用旧目录；结构不清项进入 `90_材料结构诊断`。

### 正式输出验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：17 tests OK。
- py_compile 通过。
- 正式 `dbs-suite` validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20 / `in_progress`。
- 正式 `gstack` validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59 / `in_progress`。

### 剩余边界

- 本条记录产生时没有重刷正式 LifeAtlas 200 的 `gstack` 或 `dbs-suite`，只做了临时导入和正式 validate；后续用户已确认重刷，见下一条记录。
- 下一步优先级调整为：把 SOP 的“主阅读页 / 机制说明 / 证据附录”结构落到生成页面；图书/长文导入仍未实现。

## 2026-06-29 阅读路线字段正式重刷

### 背景

用户确认正式重刷 LifeAtlas 200，让 `dbs-suite` 和 `gstack` 的正式 manifest、主控清单和组导读带上结构优先阅读路线字段。

### 已执行

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件，并在 Obsidian/LifeAtlas 200 区完成预览审阅与批注闭环" --force --preserve-comments
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "把 gstack 作为复杂 Skill 包压力样本，生成可读、可批注、可讨论的 ReaderLab v0.1 阅读包" --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

### 结果

- 正式 `dbs-suite` 重刷成功：25 files scanned / 23 skills / 6 reading units / `in_progress`。
- 正式 `dbs-suite` validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20。
- 正式 `dbs-suite` `material_structure.status=clear`，无结构诊断项。
- 正式 `dbs-suite` 批注迁移：found 1 / restored 1 / unresolved 0。
- `dbs` 仍为 `01_核心入口与总览`；`dbs-diagnosis`、`dbs-good-question`、`dbs-xhs-title` 仍为 human accepted。
- 正式 `gstack` 重刷成功：1111 files scanned / 59 skills / 7 reading units / `in_progress`。
- 正式 `gstack` validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59。
- 正式 `gstack` `material_structure.status=diagnostic`，7 个 Skill 进入 `90_材料结构诊断`：`autoplan`、`codex`、`design-consultation`、`design-html`、`ios-qa`、`plan-tune`、`setup-browser-cookies`。
- 正式 `gstack` 批注迁移：found 0 / restored 0 / unresolved 0。

### 剩余边界

- 结构优先路线规划已经进入正式包；这仍只是机器路线规划，不等于人工阅读质量验收。
- `gstack` 的 7 个结构诊断项需要后续结合页面结构化或更细的路由理解处理，不能简单按名字塞回旧分组。
- 下一阶段仍是把“主阅读页 / 机制说明 / 证据附录”结构落到生成页面；不是继续扩 gstack 或 DB Skill 样本。

## 2026-06-29 主阅读页三层结构 demo

### 背景

用户指出“主阅读页 / 机制说明 / 证据附录”已经讨论过，要求快速用真实案例做出 demo。

### 已完成

- 修改 `scripts/readerlab.py`：
  - 已完成/需复核页现在生成三层页面：
    - `10_中文精读/<group>/<skill>.md`：主阅读页，只保留导读、正文和重点。
    - `11_机制说明/<group>/<skill>-机制说明.md`：脚本、模板、hook、执行机制和关联材料。
    - `12_证据附录/<group>/<skill>-证据附录.md`：源文件、hash、覆盖指标、关联文件清单和源块统计。
  - manifest 中每个有阅读页的 Skill 新增 `mechanism_page` 和 `evidence_page`。
  - validator 会检查 completed / needs_review Skill 的机制说明页和证据附录页是否存在。
- 修改 `tests/test_readerlab.py`：
  - 主阅读页不再要求 `## 关联材料`。
  - 机制盘点、执行机制和脚本/模板说明应出现在 `11_机制说明`。
  - 证据附录页必须存在，并包含原始 `SKILL.md`。

### Demo 输出

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /private/tmp/readerlab-page-structure-demo --book-id dbs-suite --title dbs-suite --goal "演示主阅读页、机制说明、证据附录三层页面结构" --force
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /private/tmp/readerlab-page-structure-demo --book-id gstack --title gstack --goal "演示主阅读页、机制说明、证据附录三层页面结构" --force
```

重点样例：

- DB 主阅读页：`/private/tmp/readerlab-page-structure-demo/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md`
- DB 机制说明：`/private/tmp/readerlab-page-structure-demo/dbs-suite/11_机制说明/02_诊断审查与质量判断/dbs-diagnosis-机制说明.md`
- DB 证据附录：`/private/tmp/readerlab-page-structure-demo/dbs-suite/12_证据附录/02_诊断审查与质量判断/dbs-diagnosis-证据附录.md`
- gstack 主阅读页：`/private/tmp/readerlab-page-structure-demo/gstack/10_中文精读/07_流程执行与交付运维/freeze.md`
- gstack 机制说明：`/private/tmp/readerlab-page-structure-demo/gstack/11_机制说明/07_流程执行与交付运维/freeze-机制说明.md`
- gstack 证据附录：`/private/tmp/readerlab-page-structure-demo/gstack/12_证据附录/07_流程执行与交付运维/freeze-证据附录.md`

### 已验证

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py validate /private/tmp/readerlab-page-structure-demo/dbs-suite
python3 scripts/readerlab.py validate /private/tmp/readerlab-page-structure-demo/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：17 tests OK。
- py_compile 通过。
- 临时 demo `dbs-suite` validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20。
- 临时 demo `gstack` validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59。
- 正式 LifeAtlas 200 旧包 validate 仍通过，说明新 validator 兼容尚未重刷为三层结构的正式包。

### 剩余边界

- 本条记录产生时只生成临时 demo；后续用户明确要求直接更新 LifeAtlas，见下一条记录。

## 2026-06-29 主阅读页三层结构正式重刷

### 背景

用户指出临时目录不便查看，要求直接更新到 LifeAtlas。

### 已执行

```bash
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件，并在 Obsidian/LifeAtlas 200 区完成预览审阅与批注闭环" --force --preserve-comments
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "把 gstack 作为复杂 Skill 包压力样本，生成可读、可批注、可讨论的 ReaderLab v0.1 阅读包" --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

### 结果

- 正式 `dbs-suite` 已重刷为三层页面结构：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20，validate 通过。
- 正式 `gstack` 已重刷为三层页面结构：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59，validate 通过。
- 抽查以下正式页面均存在：
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/10_中文精读/02_诊断审查与质量判断/dbs-diagnosis.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/11_机制说明/02_诊断审查与质量判断/dbs-diagnosis-机制说明.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite/12_证据附录/02_诊断审查与质量判断/dbs-diagnosis-证据附录.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/10_中文精读/07_流程执行与交付运维/freeze.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/11_机制说明/07_流程执行与交付运维/freeze-机制说明.md`
  - `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack/12_证据附录/07_流程执行与交付运维/freeze-证据附录.md`

### 剩余边界

- 三层页面结构已经进入正式 LifeAtlas 200；仍需要用户在 Obsidian 中人工验收阅读体验。

## 2026-06-29 证据附录去机器化

### 背景

用户在 Obsidian 查看 `dbs-diagnosis-证据附录` 后指出：源块统计、行号、hash 等内容对读者没有直接意义，属于 ReaderLab 内部校验工具，不应要求用户处理。

### 已完成

- 修改 `scripts/readerlab.py`：
  - `12_证据附录` 不再展示源块统计表。
  - `12_证据附录` 不再内嵌完整原始 `SKILL.md`。
  - 证据附录改为读者版结构：
    - 页面关系
    - 源文件
    - 验收状态
    - 读者可用证据
    - 关联文件清单
    - 机器校验数据在哪里
  - 源块 ID、行号、hash 和完整机器校验数据仍保留在 `manifest.json` 和 `source.md`。
- 修改 `tests/test_readerlab.py`：
  - 断言证据附录包含 `## 读者可用证据` 和 `## 机器校验数据在哪里`。
  - 断言证据附录不再包含 `## 源块统计` 和 `## 原始 SKILL.md`。
- 更新状态文档：
  - `docs/current-task.md`
  - `docs/dev-state.md`
  - `docs/next-session-prompt.md`

### 已验证并重刷

```bash
python3 tests/test_readerlab.py
python3 -m py_compile scripts/readerlab.py tests/test_readerlab.py
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id dbs-suite --title dbs-suite --goal "验证 ReaderLab 复杂材料阅读化标准是否适用于 dbskill 套件，并在 Obsidian/LifeAtlas 200 区完成预览审阅与批注闭环" --force --preserve-comments
python3 scripts/readerlab.py import-skills /Users/tianqiang/技能项目/skills-canonical/packages/gstack --dest /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料 --book-id gstack --title gstack --goal "把 gstack 作为复杂 Skill 包压力样本，生成可读、可批注、可讨论的 ReaderLab v0.1 阅读包" --force --preserve-comments
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
```

结果：

- 单元测试通过：17 tests OK。
- py_compile 通过。
- 正式 `dbs-suite` validate 通过：23 total / 5 completed / 0 needs_review / 18 not_started / human accepted 3 / human pending 20。
- 正式 `gstack` validate 通过：59 total / 11 completed / 0 needs_review / 48 not_started / human accepted 0 / human pending 59。
- 抽查正式 `dbs-diagnosis-证据附录.md`：不含 `## 源块统计`，不含 `## 原始 SKILL.md`，含 `## 读者可用证据` 和 `## 机器校验数据在哪里`。

## 2026-06-29 阅读页中心方案调研与文档维护

### 背景

用户暂停开发性改动，要求先把方案聊清楚：ReaderLab 剥离执行壳后，不能只关注 frontmatter，而要让 Codex 吸收整份材料里“不适合读者直接阅读、但有设计价值”的非正文部分；本会话负责调研和维护文档，下个会话再开始施工。

### 已执行

- 主会话只读检查：
  - `docs/current-task.md`
  - `docs/dev-state.md`
  - `docs/complex-material-reading-sop.md`
  - `docs/decisions.md`
  - `docs/adversarial-review.md`
  - `scripts/readerlab.py` 渲染、manifest、validate 相关函数
  - 正式 LifeAtlas 200 中 `dbs-diagnosis`、`freeze`、`benchmark-models`、`setup-browser-cookies` 页面样例
- 调用三个只读子 Agent：
  - 内容生产调研：提出“页面三层改为逻辑三层”，默认取消 `11_机制说明` / `12_证据附录` 镜像目录，使用 `codex_absorption` 记录非正文吸收。
  - 用户体验审核：确认当前 `benchmark-models`、`freeze`、`guard` 仍被执行壳污染；主控清单和页面分层说明不应作为读者入口。
  - 对抗性检查：提醒不要让 Codex 批注回复丢失机制上下文；页面大改后不能盲目继承 `human_status=accepted`。

### 结论

下一版施工目标从“三层页面结构”校正为：

- 主阅读优先：读者默认只进入 `10_中文精读`。
- 机制按需：只有真实脚本、模板、hook、状态文件、外部依赖或运行约束影响理解时才生成机制页。
- 证据退后：源块、行号、hash、覆盖统计、完整执行视图进入 `manifest.json` / `source.md`，不作为普通阅读入口。
- Codex 吸收非正文机制：frontmatter、hooks、脚本、模板、测试、权限、工具限制、输出格式、失败处理、验证方式、目录结构等都应由 Codex 吸收，并转成设计说明、机制边界和可迁移经验。

### 文档更新

- `docs/current-task.md`：改为下个会话唯一施工切片。
- `docs/complex-material-reading-sop.md`：加入“逻辑三层”、Codex 吸收层、书/长文完整章节正文、机制按需、证据退后。
- `docs/decisions.md`：新增 D-022“主阅读优先，机制按需，证据退后”。
- `docs/dev-state.md`：记录当前正式输出问题和下一版方案校正事实。
- `docs/adversarial-review.md`：同步三层 demo 已落地但被校正为过渡方案的事实。
- `docs/next-session-prompt.md`：更新为下个会话施工 prompt。

### 验证

本轮没有运行生成器、没有重刷 LifeAtlas、没有执行代码测试；这是按用户要求进行的方案调研和文档维护。后续代码施工时必须重新运行完整验证命令。

## 2026-06-30 Review pack validator 证据链补强

### 背景

对抗审查指出 `scripts/readerlab_review_pack_validate.py` 仍偏口径检查，缺少 source registry、location map、contract refs 和专项 assertions 的证据链校验。本轮按 Worker 边界只修改 repo 内 validator、测试和状态说明，不改 LifeAtlas、不改 canonical package、不改 `scripts/readerlab.py`，也不改 review pack JSON 绕过校验。

### 改动

- 修改 `scripts/readerlab_review_pack_validate.py`：
  - 固定要求 11 个 review pack 文件存在。
  - 校验 `source-registry.sources` 非空、`source_id` 非空唯一。
  - 校验 `location-map.locations` 非空、`location_id` 非空唯一，且每个 `location.source_id` 回链到对应 source registry。
  - 递归校验 `location_refs`、`source_refs`、`primary_location_refs`、`derived_location_refs` 都指向对应 scope 的 location map；其中 capability domain 的 `source_refs` 按本 pack 当前语义视为 location ids。
  - 增加 Elon A05 检查：每个 `distillation_candidate` 必须有 `claim_refs`，主证据非空，主证据不能只指向 distillation/derived page，candidate claim refs 要和 top-level claim refs 按 claim id 或 primary refs 对齐。
  - 增加 DBS 检查：capability-map/source-registry 均保持 `sample`，`capability_domains_scope` 如存在也必须 `sample`，能力域非空且 source refs 存在，README/assertions/review_items 必须记录 sample、24 Skills、cross_skill_routes、旧 LifeAtlas global-map conflict blocker。
  - assertions 改为逐 ID 校验期望状态，不再只统计 pass/partial 数量。
- 修改 `tests/test_review_pack_validate.py`：
  - 保留当前 pack pass、accepted `human_status`、`coverage_status=full` 负例。
  - 新增缺 source registry、location source_id 断链、Elon candidate 主证据只指向 distillation、assertion ID/status 篡改、DBS sources 为空、DBS domain source_refs 断链、forbidden grounded-global-map schema 负例。
- 更新 `docs/current-task.md`、`docs/dev-state.md` 和 review pack `README.md` 的 validator 说明。

### 验证

```bash
python3 tests/test_review_pack_validate.py
python3 scripts/readerlab_review_pack_validate.py
python3 tests/test_readerlab.py
```

结果：

- `tests/test_review_pack_validate.py`：10 tests OK。
- `scripts/readerlab_review_pack_validate.py`：PASS。
- `tests/test_readerlab.py`：18 tests OK。

## 2026-06-30 Review pack validator 第二轮 false-pass 修复

### 背景

第二轮对抗审查发现上一轮 validator 仍有 3 个 false pass：Elon A05 candidate 可用不存在的 `claim_ref_id` 搭配另一个 claim 的 primary refs 通过；DBS `cross_skill_routes` 清空后仍通过；DBS `capability-map.review_items` 清空后仍可被 README/assertions 中的 blocker 字样兜底。本轮按 Worker 边界只改 repo 内 validator、测试和状态说明，不改 LifeAtlas、不改 canonical package、不改 `scripts/readerlab.py`，也不改 review pack JSON。

### 改动

- 修改 `scripts/readerlab_review_pack_validate.py`：
  - Elon A05 改为逐 `claim_ref_id` 映射顶层 `claim_refs[].claim_id`，不再允许只靠任意 primary refs 集合匹配。
  - Candidate primary refs 必须匹配对应顶层 claim 的 primary refs，或是其非空子集；主证据仍不能只指向 distillation/derived page。
  - Candidate `derived_location_refs` 必须是列表，且其中每个 ref 必须指向 Elon location map。
  - DBS `cross_skill_routes` 必须是非空列表；每项必须是对象，且包含非空 `route_id` / `from` / `to` / `when` / `uncertainty`。
  - DBS `cross_skill_routes[].from` 和 `.to` 必须回链到 `capability_domains[].domain_id`。
  - DBS `capability-map.review_items` 必须是非空列表，且结构化包含 24 Skills、cross_skill_routes、旧 LifeAtlas global-map conflict 的 blocked item。
- 修改 `tests/test_review_pack_validate.py`：
  - 新增 A05 mismatched claim id/ref 负例。
  - 新增 DBS empty `cross_skill_routes` 负例。
  - 新增 DBS route 指向不存在 domain 负例。
  - 新增 DBS empty `review_items` 负例。
- 更新 `docs/current-task.md` 和 `docs/dev-state.md` 的 validator 当前事实。

### 验证

```bash
python3 tests/test_review_pack_validate.py
python3 scripts/readerlab_review_pack_validate.py
python3 tests/test_readerlab.py
```

结果：

- `tests/test_review_pack_validate.py`：14 tests OK。
- `scripts/readerlab_review_pack_validate.py`：PASS。
- `tests/test_readerlab.py`：18 tests OK。

## 2026-06-30 《埃隆之书》Fullbook demo v0

### 背景

用户要求新增一个仓库内《埃隆之书》全书级阅读地图 demo，证明 ReaderLab 不只做单章节局部深读，而能产出“全书级地图 + 总收获/亮点 + 跨章节主题关系”。本轮只写 repo 内 demo 和独立 validator，不写 LifeAtlas，不改 `scripts/readerlab.py`，不新增依赖。

### 改动

- 新增 `docs/reports/readerlab-fullbook-demo-v0/README.md`：说明 demo 目标、边界、覆盖口径、验收命令和缺口。
- 新增 `docs/reports/readerlab-fullbook-demo-v0/elon/source-registry.v1.json`：登记 EPUB、OPF、NCX TOC、XHTML TOC；EPUB sha256 为 `282554f2c89b817b7ad5535fa62383b099fb5b75ca4ce6e2a2e75c868ce8bb7a`。
- 新增 `docs/reports/readerlab-fullbook-demo-v0/elon/location-map.v1.json`：登记完整 OPF spine 36/36 个 xhtml item，location ids 为 `elon-spine-001` 到 `elon-spine-036`。
- 新增 `docs/reports/readerlab-fullbook-demo-v0/elon/grounded-global-map.v1.json`：产出全书主线、部件/章节地图、跨章节主题、总收获、亮点和可迁移原则；所有主张使用 spine 级 refs，`human_status=pending`。
- 新增 `docs/reports/readerlab-fullbook-demo-v0/elon/fullbook-reader-demo.md`：面向读者的中文全书导读，明确不是精选译文完整阅读页，不是 LifeAtlas 正式写入。
- 新增 `docs/reports/readerlab-fullbook-demo-v0/elon/assertions.md`：FULLBOOK-A01 到 FULLBOOK-A06 均为 machine pass，人工阅读质量验收仍 pending。
- 新增 `scripts/readerlab_fullbook_demo_validate.py` 和 `tests/test_fullbook_demo_validate.py`：检查 required files、36/36 spine coverage、full coverage 条件、refs、assertions 和 `human_status=pending`。
- 更新 `docs/current-task.md` 和 `docs/dev-state.md`：记录 fullbook demo v0 当前事实和下一步人工/reviewer 判断点。

### 覆盖口径

本轮 `coverage_status=full` 只表示完整 EPUB OPF spine 登记和 spine 级 refs 完整，不表示精选译文正文完成、不表示写入 LifeAtlas、不表示人工验收通过。

### 验证

```bash
python3 scripts/readerlab_fullbook_demo_validate.py docs/reports/readerlab-fullbook-demo-v0
python3 tests/test_fullbook_demo_validate.py
python3 tests/test_readerlab.py
```

结果：

- `scripts/readerlab_fullbook_demo_validate.py`：PASS。
- `tests/test_fullbook_demo_validate.py`：6 tests OK。
- `tests/test_readerlab.py`：18 tests OK。

## 2026-06-30 《埃隆之书》source-aligned 长样张 v0

### 背景

用户要求补固定 7 个闭环中的 `2. 样本质量闭环`：书籍侧长样张。上一轮 proof/toy sample 信息量不足，因此本轮只写 repo 内产物，不写 LifeAtlas，不新增依赖，不声称半自动化或 product ready。

### 改动

- 新增 `docs/reports/readerlab-elon-source-aligned-demo-v0/README.md`：说明样张目标、来源边界、文件清单、状态和不声称事项。
- 新增 `docs/reports/readerlab-elon-source-aligned-demo-v0/reader/00_全书地图.md`：给出全书主问题、结构地图、主题线索和 pending 结论。
- 新增 `docs/reports/readerlab-elon-source-aligned-demo-v0/reader/01_大单元深读.md`：围绕第二部分“极限硬核工作”写 source cards，包含 source_id / EPUB spine / 短摘录定位 / 处理过的一手正文 / AI 深读 / 误读降级。
- 新增 `docs/reports/readerlab-elon-source-aligned-demo-v0/audit/source-alignment.md`：列出 source registry、covered unit、location refs 和高层 claim trace。
- 新增 `docs/reports/readerlab-elon-source-aligned-demo-v0/audit/eval.md`：按信息密度、原文对应、非显然洞察、读者收益、过度升格风险自评，`human_status=pending`。
- 更新 `docs/current-task.md`、`docs/dev-state.md`、`docs/progress.md`：记录本轮是样本质量闭环，不是自动化闭环。

### 覆盖口径

第二部分标题边界为 `spine-015 / v101-13.xhtml`；实质 source cards 覆盖 `spine-016` 至 `spine-020`，即 `v101-14.xhtml` 至 `v101-18.xhtml`。本轮复用 `docs/reports/readerlab-elon-full-product-v0/contracts/location-map.v1.json` 的 location refs，没有重新生成 JSON contract。

### 验证

```bash
python3 tests/test_readerlab.py
git diff --check
```

结果：

- `tests/test_readerlab.py`：30 tests OK。
- `git diff --check`：PASS，无 whitespace/error 输出。
