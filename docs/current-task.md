# Current Task

## Authority

本文件是当前执行事实的唯一入口。新会话默认只读：

1. `AGENTS.md`
2. `docs/current-task.md`

按需再读：

- 当前 PRD：`docs/readerlab-v2-shareable-skill-prd.md`
- 当前包边界：`docs/readerlab-v2-package-boundary.md`
- 当前 RFC：`docs/rfc/2026-07-04-readerlab-v2-installable-skill-package.md`
- 当前读者产品形态：`docs/readerlab-v2-reader-product-shape.md`
- 历史运行摘要：`docs/agent-run-ledger.md` 顶部最新两条
- 稳定路径和验证命令：`docs/dev-state.md`
- 耐久决策：`docs/decisions.md`

旧 prompt、旧样章、旧报告、旧聊天摘要和单纯 `git diff` 不是当前事实源。当前 #2-#8 已由 PR #10-#16 合并落地；#9 / PR #17 是当前唯一 GitHub issue slice。

## 2026-07-05 当前执行更新

PR #10/#11/#12/#13/#14/#15/#16 已合并到 `readerlab-elon-checkpoint`，对应 #2/#4/#3/#5/#6/#7/#8 的实现已经进入提交树。GitHub 上 #2/#3/#5/#6/#7/#8 曾因 auto-close 未触发而保持 open，已在本轮按对应 merged PR 手动关闭；#4 此前已关闭。当前 GitHub 队列只剩 #9：ReaderLab V2 installable release candidate 复核。

当前 slice 是 #9。目标是增加一个可复跑的 RC 复核入口，证明当前最多可以进入 `installable_release_candidate`，同时明确不能声明 production ready、friend smoke passed 或 reader accepted。

## 2026-07-06 产品形态纠偏

真实材料试跑暴露出一个集成断层：当前可安装包候选能跑包构建、配置、安装和路线 smoke，但仍可能调用旧的 `import-skills` / contract renderer 形态，产出目录、清单、状态表、fixture 语言或待生成页面，而不是 V2 已确认的 reader-facing 陪读包。

因此新增权威产品形态文档：`docs/readerlab-v2-reader-product-shape.md`。后续任何“reader accepted”或真实材料验收，必须分别按两条主线判断：

- 图书 / 长文线：读者打开后是在读书或长文正文，带自然方位说明和正文旁陪读；不能像 EPUB 抽取报告、contract proof 或 audit dump。
- Skill / 工程材料线：读者打开后能读到净化正文主读页、技术负责人解说页和可独立复用的设计资产卡；不能只是目录、manifest、状态表或待生成清单。

GSTACK `spec` / `review` 只作为复杂 Skill 压力样本，不是产品边界。任何规则必须能泛化到 Matt 等非 GSTACK Skill 包，禁止写 GSTACK 专项适配。

#9 的交付边界：

- 增加 RC 复核脚本，重新构建干净包并复跑 clean package audit、package smoke、install / discovery smoke、三类材料路线 smoke。
- 增加 RC 复核说明，固定复核层次和状态口径。
- 包内应包含 install smoke 和 RC 复核入口，方便分享包候选自查。
- 结论必须仍然区分配置结构、runner contract、Quality Gate request、机器 reader-page smoke、controller / blocking controller、人工验收。
- 当前通过只能说明结构 / runner / smoke 通过，不代表人工读者验收通过。

## Active Slice

ReaderLab V2 当前处于 **发布形态明确后的重整开发阶段**。

当前目标已经从“继续打磨单个工程材料 prototype”调整为 **ReaderLab V2 可安装、可分享的干净 Skill 包候选**。这不是正式发布阶段，也不能声明 production ready；它要求先把发布边界、历史防回归、包构建、安装 smoke 和三类材料路线验收重新组织清楚，再继续开发和 debug。

当前 PRD：`docs/readerlab-v2-shareable-skill-prd.md`。

当前包边界：`docs/readerlab-v2-package-boundary.md`。

当前读者产品形态：`docs/readerlab-v2-reader-product-shape.md`。

当前 RFC：`docs/rfc/2026-07-04-readerlab-v2-installable-skill-package.md`。#2-#8 的 GitHub issue 开发链路已经完成；#9 / PR #17 仍按 PR -> Codex review -> feedback fixes -> ready-to-merge candidate -> merge 执行。

当前 GitHub issue 状态：

- #2 固定 ReaderLab V2 可分享 Skill 包边界：closed，PR #10 merged。
- #3 构建最小 ReaderLab V2 Skill 发布包：closed，PR #12 merged。
- #4 外置 ReaderLab V2 运行配置并去除本机路径耦合：closed，PR #11 merged。
- #5 验证 ReaderLab V2 Skill 安装与发现 smoke：closed，PR #13 merged。
- #6 建立 ReaderLab V2 图书路线 smoke：closed，PR #14 merged。
- #7 建立 ReaderLab V2 长文 / 报告 / 访谈稿路线 smoke：closed，PR #15 merged。
- #8 建立 ReaderLab V2 Skill / 工程材料路线 smoke：closed，PR #16 merged。
- #9 ReaderLab V2 installable release candidate 复核：open，PR #17 active。

生产约束 / 验收约束分层仍然有效：验收矩阵保留为评价语言，但不自动进入生产 runner。验收发现的问题必须先反推到最小上游 fault stage，再判断能否形成稳定、低误伤、可执行的生产条件。

本阶段在本机未提交 V2 原型中，曾从一个 `gstack/spec` 窄 block 推进到两个完整单 Skill 样本：

- `v2-real-skill-gstack-spec-complete-20260704`
  - `block_id`: `spec-complete-skill`
  - source: `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md`
- `v2-real-skill-gstack-review-complete-20260704`
  - `block_id`: `review-complete-skill`
  - source: `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/review/SKILL.md`

两个完整 case 在本机原型验证中通过过 `check-evaluation`，controller decision 是 `limited_accept`，不是 production ready。除非相应 runner、builder 和 reports 在后续 issue 中提交，否则下游 worker 不能把这些路径当成已提交事实源。

## Current Facts In Submitted Tree

- 已提交发布边界和调度材料：
  - `docs/readerlab-v2-shareable-skill-prd.md`
  - `docs/readerlab-v2-package-boundary.md`
  - `docs/rfc/2026-07-04-readerlab-v2-installable-skill-package.md`
- 已提交可运行包构建和配置外置：
  - `scripts/build_readerlab_package.py`
  - `packaging/readerlab-package-manifest.json`
  - `packaging/package_smoke_test.py`
  - `scripts/readerlab.py` 的外置 run config 校验和包相关入口。
- 已提交安装 / 发现 smoke：
  - `packaging/install_smoke_test.py`
  - `tests/test_readerlab_install_smoke.py`
- 已提交三类路线 smoke：
  - `packaging/book_route_smoke_test.py`
  - `packaging/longform_route_smoke_test.py`
  - `packaging/engineering_route_smoke_test.py`
  - `tests/fixtures/readerlab/book-route-smoke-v0/`
  - `tests/fixtures/readerlab/longform-route-smoke-v0/`
  - `tests/fixtures/readerlab/engineering-route-smoke-v0/`
- #9 / PR #17 新增 RC 复核入口：
  - `packaging/release_candidate_review.py`
  - `tests/test_readerlab_release_candidate_review.py`
  - `docs/readerlab-v2-release-candidate-review.md`
- 用户指出并确认：验收不能混成一句“读者视角 OK”。ReaderLab 应拆成多类检查：
  - 合同履约 / 结构合规
  - 内容完整性
  - 人类读者体验
  - 产品预期
  - Skill / 工程材料路线额外有 Agent 读者可复用性

## Local Prototype History

以下内容是本机未提交 V2 原型中的历史线索。除非对应文件在后续 issue 中提交，否则不能作为 fresh checkout 的当前事实。

- 工程材料路线硬边界曾在本机 runner 原型中落地：
  - `engineering_source_scope` 中声明的原始 source 必须先完整读过一次。
  - `full-source-track.md` 是 evidence packet / seam，不是摘要替身。
  - `technical-cofounder-notes.md` / `technical-asset-cards.md` 必须站在 evidence layer 上，不能只依赖 `body.md`。
  - `technical-cofounder-notes.md` 必须保留至少一个可精确回原始 source 的入口。
- 正式包结构也已收紧：
  - 正式包顶层白名单已落地。
  - `audit/` 和 reader-facing 目录拆开。
  - `manifest.json` 仍允许留顶层作为兼容例外，但额外 JSON 不能随便留顶层。
- `gstack/spec` 完整单 Skill case 已通过。
- `gstack/review` 完整单 Skill case 已通过。
- 本机原型曾把这点落入代码；在这些文件提交前，下列路径只代表待落地的历史线索：
  - `scripts/readerlab_v2_quality_gate_adapter.py`
    - quality gate request 会写明 `check_class`、`Audience`、`isolation_rule` 和分开的 review dimensions。
    - `asset_cards` 的受众明确为 `background-free Agent reader`。
  - `scripts/readerlab_v2_runner.py`
    - `asset_cards` reader page 必须提供 `purpose`、`reader`、`use_boundary`、`selection_rule` 四个冷启动字段。
  - `tests/test_readerlab_v2_runner.py`
    - 新增资产卡缺冷启动上下文的红灯测试。
  - `tests/test_readerlab_v2_quality_gate_adapter.py`
    - 新增 quality gate request 必须区分人类读者和无背景 Agent 读者的检查。
- `review-complete-skill.assets.md` 和 `spec` 相关资产页已补冷启动元信息。
- 已完成第一轮 runner 约束分层审计：
  - 继续保留为生产硬 gate：来源范围、证据层、净化正文、最小追责字段、页面存在和中文 H1、audit 不污染读者页、资产页四个冷启动入口字段、quality gate packet / blocking controller 协议。
  - 已从 runner 下沉到 Quality Gate / Reader Evaluation：工程页是否真正让产品负责人看懂、术语解释是否自然、资产卡是否真的可复用、逐卡技术材料是否足够深、state handoff 是否解释到位、高价值陪读是否被低干扰策略误删。

## Important Distinction

以后说“验收通过”必须说明是哪类检查通过，不能混说。

| 检查类型 | 图书 / 长文线 | Skill / 工程材料线 |
|---|---|---|
| 合同履约 | 保留正文、source registry、location map、audit 不污染阅读面 | source scope、evidence packet、技术页/资产卡不站在 body 上二次转述 |
| 内容完整性 | 覆盖章节主线、关键论证、上下文 | 覆盖完整 Skill 的关键机制、流程、边界、失败条件 |
| 人类读者体验 | 普通读者能不能读懂正文和陪读 | 不懂技术的人能不能看懂 Skill 在干什么、为什么这样设计 |
| 产品预期 | 是否像陪读包，不是摘要包或笔记包 | 是否像工程材料陪读包，不是 prompt 摘要或 audit dump |
| 复用 / 沉淀 | 支持后续批注、讨论、沉淀候选 | 资产卡支持未来无背景 Agent 冷启动复用 |

同时必须区分：

- 生产时约束：来源范围、正文 / 净化正文、证据层、产物结构、顺序依赖、失败回指、controller 阻断关系。
- 验收时约束：内容完整性、人类读者体验、产品预期、Agent 冷启动复用、高阶讲解是否有认知增量。

验收时约束不应直接放进生产流程。只有当验收问题反复出现，并且能反推成可观察、可复跑、低误伤的前置条件时，才升级为 runner 或生产 prompt 约束。

## Current Verification

最近一次本机原型验证：

```bash
python3 tests/test_readerlab_v2_runner.py
python3 tests/test_readerlab_v2_quality_gate_adapter.py
python3 tests/test_readerlab_v2_gstack_spec_builder.py
python3 tests/test_readerlab.py
python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-review-complete-20260704
python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-spec-complete-20260704
python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-spec-20260703
git diff --check
```

结果曾全部通过。本轮生产 / 验收分层后，最新复跑重点是两个完整单 Skill case；`v2-real-skill-gstack-spec-20260703` 仍是窄样本，`controller_decision: revise`，`case_acceptance: false`，但 evaluation 命令本身通过，因为它能正确识别 protocol seed / revise 状态。这些验证在相关 V2 文件提交前不能作为 fresh checkout 的可复跑证据。

## Not Yet Claimed

当前仍然不能声称：

- ReaderLab V2 production ready。
- 图书路线最终阅读质量已经合格。
- 完整 GSTACK 包已通过。
- AI 质量评估已完全智能化。
- 两个 Skill case 是强样本基线，只能说是 `limited_accept` 的完整单 Skill prototype candidate。

当前可以声称：

- 已提交文档固定了 ReaderLab V2 可分享 Skill 包边界、状态口径、发布顺序和历史防回归要求。
- 已提交包构建器、运行配置外置、安装 / 发现 smoke 和三类材料路线 smoke。
- PR #17 中已提交 RC 复核入口，用来复跑 clean package audit、package smoke、install / discovery smoke 和三类路线 smoke。
- 已提交文档固定了验收矩阵必须拆成合同履约 / 结构合规、内容完整性、人类读者体验、产品预期、无上下文 Agent 复用。
- 已提交 `docs/readerlab-v2-reader-product-shape.md` 固定了两条 reader-facing 产品线的最终形态：图书 / 长文线与 Skill / 工程材料线必须分别验收，不能合并成一条笼统 reader gate。
- 已提交文档固定了 `limited_accept` 只能表示有限 prototype 接受，不能说成 production ready。
- 本机未提交原型中，工程材料路线曾有两个完整单 Skill case 通过：`gstack/spec` 和 `gstack/review`；这只能作为后续 issue 的历史线索，不能作为 fresh checkout 的已提交能力。
- 本机未提交原型中，runner / quality gate / assets page 曾具备的若干结构和冷启动约束，只有已进入 PR #10-#17 的部分才是当前可运行事实。

## Next Work Queue

当前不要再回到 #2-#8，也不要先扩第三个 GSTACK Skill。权威下一步分两段：

第一段，完成 #9 / PR #17：

1. 处理 PR #17 的 Codex Review 反馈，直到当前 head commit 被 review 覆盖且没有 actionable blocker。
2. PR #17 `mergeStateStatus: CLEAN` 且 Review 无 major issues 后，按用户授权可直接 merge。
3. Merge 后关闭 #9，并删除 PR #17 heartbeat。
4. 合并后状态最多推进到 `installable_release_candidate`，不能说 production ready、friend smoke passed 或 reader accepted。

第二段，从工程链路转到读者产品形态接入。#18 由当前产品形态 gate PR 完成；后续不要回到 #18 重新做形态定义，直接推进两条并列集成 issue：

1. #19 Book / Longform reader product shape integration：把可安装包的图书输出从 sample / contract renderer 形态接回正文优先章节陪读包。
2. #20 Skill / Engineering reader product shape integration：把可安装包的 Skill 输出从 `import-skills` 清单形态接回净化正文主读页、技术负责人解说页和设计资产卡。

两条线都必须先在本地实现和真实材料验证，再开 PR、唤醒云端 Codex Review、轮询 review 结果、按反馈本地修复并继续。通过声明必须说明是安装 / route smoke，还是 reader product shape，还是人工 reader accepted。

## Stop Conditions

- 把 `limited_accept` 说成 production ready。
- 把 runner 结构通过说成读者质量通过。
- 把“内容完整性”“合同履约”“读者体验”“产品预期”“Agent 复用性”混成一个笼统验收。
- 把图书 / 长文线和 Skill / 工程材料线合并成一套 reader-facing 形态。
- 把旧 `import-skills` 目录 / 清单 / 待生成页面当作 Skill 线 reader accepted 输出。
- 把 contract renderer 的 sample 页面当作图书 / 长文线 reader accepted 输出。
- 只修最终读者页，不修 builder / 中间 artifact / gate request。
- 修改 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack` 原始 source。
- 新会话只看 `git diff`，忽略 `docs/current-task.md`、PRD、RFC 和包边界；未提交 V2 原型文件和真实产物只能作为历史线索，不能当成 fresh checkout 的当前事实。

## Delivery Gates

每次交付前必须用中文回答：

1. 这次跑通的是合同、runner 测试，还是某个真实 Skill case。
2. 如果是 Skill case，具体是哪个 `case_id`、哪个 `block_id`。
3. 如果失败，失败是否能回到具体 artifact 和具体 fault stage。
4. 当前结论是否建立在刚刚验证过的命令和真实产物上，而不是旧摘要或旧印象。
