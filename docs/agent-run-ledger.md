# Agent Run Ledger

本文件只保留阶段级摘要。旧过程报告和长日志已清理；需要查逐步细节时使用 git 历史或 Codex 会话。

## 2026-07-04 ReaderLab V2 可分享 Skill 包 PRD

- 用户确认：ReaderLab V2 的目标不是本机 demo，也不是脏运行目录，而是一套完整、独立、可安装、可分享给朋友的 Skills；必须支持图书长文和 Skill / 工程材料。
- 当前阶段判断：
  - 还没有进入正式发布阶段。
  - 已经明确发布形态，下一步是发布形态明确后的重整开发和 debug。
  - 核心能力仍未完成三类材料最终验收，不能称 production ready。
- 已按 `/to-prd` 把当前对话和仓库事实综合成 PRD：
  - `docs/readerlab-v2-shareable-skill-prd.md`
- PRD 特别固化历史防回归：
  - Elon v1 是负样本，不是通过样张。
  - 正文 / 陪读不能恢复三文件分离。
  - 机器验证不等于读者验收。
  - runner 不能用 Python 字符串检查冒充质量判断。
  - `limited_accept` 不能说成 production ready。
  - `make-pdf` / `setup-deploy` 是新合同下的诊断失败样本，不是代表性正样本。
  - `gstack/spec` / `gstack/review` 只是完整单 Skill prototype candidate，不代表完整 GSTACK 包通过。
  - 可分享包必须排除实验 reports、私有 source、本机路径、GSTACK 原始仓库和旧 handoff。
- 已更新 `docs/current-task.md`：当前目标调整为 ReaderLab V2 可安装、可分享的干净 Skill 包候选；下一步先拆 issue 和建立发布边界 / 包构建 / 安装 smoke / 三类路线 smoke。
- 已按 `/to-issues` 发布 GitHub issue 队列：
  - #2 固定 ReaderLab V2 可分享 Skill 包边界
  - #3 构建最小 ReaderLab V2 Skill 发布包
  - #4 外置 ReaderLab V2 运行配置并去除本机路径耦合
  - #5 验证 ReaderLab V2 Skill 安装与发现 smoke
  - #6 建立 ReaderLab V2 图书路线 smoke
  - #7 建立 ReaderLab V2 长文 / 报告 / 访谈稿路线 smoke
  - #8 建立 ReaderLab V2 Skill / 工程材料路线 smoke
  - #9 ReaderLab V2 installable release candidate 复核
- 下一步执行顺序已被 PR #10 后续 review 修正为：#2 合并后先做 #4，去掉 `scripts/readerlab.py` 的本机路径耦合；再做 #3 的可运行包构建；随后 #5 和三类路线 smoke；最后 #9。当前仍不能称 production ready。
- 用户追问现有 issue 是否已经覆盖产物质量核验、核验标准是否明确，以及后续 GitHub 开发是否可参考 Controller-Agent GitHub Workflow SOP。
- 已读取 `/Users/tianqiang/LifeAtlas/800_Skills与流程/840_开发复盘Skills/2026-06-25_Controller-Agent-GitHub工作流SOP.md`。
- 已新增 RFC：`docs/rfc/2026-07-04-readerlab-v2-installable-skill-package.md`
  - 固定质量核验五类视角：合同履约 / 结构合规、内容完整性、人类读者体验、产品预期、无上下文 Agent 复用。
  - 固定参数验证范围：source paths、output root、permission boundary、material family、requested scope、declared scope / units、full_book_required、dual_view_required、engineering_source_scope。
  - 固定 GitHub 开发方式：一个 issue 一个 worktree，一个 worker 一个 PR，PR 走 Codex Review，主控只报告 ready-to-merge candidate，最终 merge 等用户明确批准。
- 已新增 `docs/readerlab-v2-package-boundary.md`，专门固定可分享 Skill 包必须包含、必须排除、配置输入、质量核验边界、五类复核视角、历史防回归和状态梯子。

## 2026-07-04 生产约束 / 验收约束分层收口

- 用户指出：验收时的约束不应直接放到生产流程里；验收发现的问题必须先反推，才能推出生产时要加的条件。
- 用 `/domain-modeling` 和 `/codebase-design` 收口术语和模块边界：
  - 生产时约束：来源范围、正文 / 净化正文、证据层、产物结构、顺序依赖、失败回指、controller 阻断关系。
  - 验收时约束：内容完整性、人类读者体验、产品预期、Agent 冷启动复用、高阶讲解是否有认知增量。
  - Runner 只承载生产硬约束；Quality Gate / Reader Evaluation / 分离读者 Agent 承载验收判断。
  - 验收问题只有在能反推成稳定、低误伤、可观察、可复跑的前置条件时，才升级为 runner 或生产 prompt 约束。
- 已更新，其中 `experiments/readerlab-v2/`、`scripts/readerlab_v2_*` 和 `tests/test_readerlab_v2_*` 相关条目属于本机未提交 prototype 历史，不属于 PR #10 的 submitted tree，后续 worker 不能把它们当成 fresh checkout 当前事实：
  - `docs/decisions.md`：新增 D-035，固定生产约束和验收约束分层。
  - `docs/eval-gates.md`：新增约束分层和“验收问题反推生产条件”路径。
  - `experiments/readerlab-v2/workflow-contract-v2.md`：新增生产 / 验收约束边界和新增硬 gate 默认门槛。
  - `experiments/readerlab-v2/runner-contract-v2.md`：新增 Runner 约束边界，明确哪些约束不能进入 runner。
  - `docs/current-task.md`：更新当前阶段和下一步队列。
- 当前结论：
  - 多视角验收矩阵保留，但它是评价语言，不自动等于生产流程约束。
  - 已完成第一轮 runner 约束分类：保留生产硬 gate，下沉读者质量 / 产品预期 / Agent 复用判断。
  - 暂不扩第三个 GSTACK Skill，除非分层稳定。
- 第一轮 runner 下沉改动属于本机未提交 prototype 历史，必须由后续 issue 正式提交并复验后才算当前可运行事实：
  - 保留：来源范围、证据层、净化正文、最小追责字段、页面存在和中文 H1、audit 不污染读者页、资产页四个冷启动入口字段、quality gate packet / blocking controller 协议。
  - 下沉到 Quality Gate / Reader Evaluation：工程页是否真正让产品负责人看懂、术语解释是否自然、资产卡是否真的可复用、逐卡技术材料是否足够深、state handoff 是否解释到位、高价值陪读是否被低干扰策略误删。
  - `scripts/readerlab_v2_runner.py` 已移除这些质量判断的硬失败调用。
  - `tests/test_readerlab_v2_runner.py` 已改成验证 runner 不再把这些验收判断当生产硬 gate。
  - `scripts/readerlab_v2_quality_gate_adapter.py` 已把工程页 `product_owner_explanation` / `term_grounding`、资产页 `card_operability` 写入 review request，让下沉后的判断仍在验收层出现。
- 本机 prototype 验证命令曾通过；这些结果依赖未提交 V2 runner / adapter / tests，不能作为 fresh checkout 可复跑证据：
  - `python3 tests/test_readerlab_v2_runner.py`：`Ran 47 tests ... OK`
  - `python3 tests/test_readerlab_v2_quality_gate_adapter.py`：`Ran 3 tests ... OK`
  - `python3 tests/test_readerlab_v2_gstack_spec_builder.py`：`Ran 3 tests ... OK`
  - `python3 tests/test_readerlab.py`：`Ran 38 tests ... OK`
  - `python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-review-complete-20260704`：pass, `limited_accept`, `case_acceptance: true`
  - `python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-spec-complete-20260704`：pass, `limited_accept`, `case_acceptance: true`
  - `git diff --check`：pass

## 2026-07-04 两个完整 GSTACK Skill case + 多视角验收矩阵

- 代表性工程材料样本从 `gstack/spec` 窄切片推进到两个完整单 Skill case：
  - `v2-real-skill-gstack-spec-complete-20260704`
    - `block_id`: `spec-complete-skill`
    - source: `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md`
  - `v2-real-skill-gstack-review-complete-20260704`
    - `block_id`: `review-complete-skill`
    - source: `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/review/SKILL.md`
- 新增 / 更新主要文件：
  - `scripts/build_readerlab_v2_gstack_spec_demo.py`
  - `scripts/build_readerlab_v2_gstack_spec_complete_demo.py`
  - `scripts/build_readerlab_v2_gstack_review_complete_demo.py`
  - `tests/test_readerlab_v2_gstack_spec_builder.py`
  - `scripts/readerlab_v2_quality_gate_adapter.py`
  - `scripts/readerlab_v2_runner.py`
  - `tests/test_readerlab_v2_quality_gate_adapter.py`
  - `tests/test_readerlab_v2_runner.py`
  - `experiments/readerlab-v2/reports/v2-real-skill-gstack-spec-20260703/`
  - `experiments/readerlab-v2/reports/v2-real-skill-gstack-spec-complete-20260704/`
  - `experiments/readerlab-v2/reports/v2-real-skill-gstack-review-complete-20260704/`
- `gstack/review` case 中先发现资产卡缺 `adversarial review / cross-model synthesis` 可复用卡片；已修在 builder 和真实产物中。
- 用户进一步指出：验收不能混成一句“读者视角”。ReaderLab 的验收至少要拆开：
  - 合同履约 / 结构合规
  - 内容完整性
  - 人类读者体验
  - 产品预期
  - Skill / 工程材料额外的 Agent 读者可复用性
- 已落地的验收矩阵改动：
  - `scripts/readerlab_v2_quality_gate_adapter.py`
    - quality gate request 现在输出 `check_class`、`Audience`、`isolation_rule` 和分开的 review dimensions。
    - `asset_cards` 明确面向 `background-free Agent reader`，并要求不要打开 `body.md` 或 source 来补资产卡缺失上下文。
  - `scripts/readerlab_v2_runner.py`
    - `asset_cards` reader page 必须有 `purpose`、`reader`、`use_boundary`、`selection_rule` 四个冷启动字段。
  - `tests/test_readerlab_v2_runner.py`
    - 新增资产卡缺冷启动上下文的红灯测试。
  - `tests/test_readerlab_v2_quality_gate_adapter.py`
    - 新增 gate request 必须分开人类读者和无背景 Agent 读者的检查。
- 最新验证命令均通过：
  - `python3 tests/test_readerlab_v2_runner.py`：`Ran 47 tests ... OK`
  - `python3 tests/test_readerlab_v2_quality_gate_adapter.py`：`Ran 3 tests ... OK`
  - `python3 tests/test_readerlab_v2_gstack_spec_builder.py`：`Ran 3 tests ... OK`
  - `python3 tests/test_readerlab.py`：`Ran 38 tests ... OK`
  - `python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-review-complete-20260704`：pass, `limited_accept`, `case_acceptance: true`
  - `python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-spec-complete-20260704`：pass, `limited_accept`, `case_acceptance: true`
  - `python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-skill-gstack-spec-20260703`：command pass, `controller_decision: revise`, `case_acceptance: false`
  - `git diff --check`：pass
- 结论：
  - 现在可以说工程材料路线已有两个完整单 Skill prototype candidate 通过。
  - 仍不能说 production ready、完整 GSTACK 包通过、图书路线质量合格或 AI 质量评估已经完全智能化。
  - 下一步不应扩第三个 Skill，应先按新矩阵做一轮分离复验：人类读者看主读者页/工程页，无背景 Agent 只看资产卡页。

## 2026-07-03 工程证据层合同收口 + `gstack/spec` 交接

- 用 `/codebase-design` + `/tdd` 收紧了 ReaderLab V2 工程路线的三条硬边界：
  - `engineering_source_scope` 是首轮完整原始 source 阅读义务
  - `full-source-track.md` 是 evidence packet / seam，不是摘要替身
  - `technical-cofounder-notes.md` / `technical-asset-cards.md` 必须站在 evidence layer 上，且工程解说必须保留至少一个 direct source back-reference
- 已更新的合同 / 路线 / step files：
  - `experiments/readerlab-v2/workflow-contract-v2.md`
  - `experiments/readerlab-v2/runner-contract-v2.md`
  - `experiments/readerlab-v2/route-modules/technical-material-route.md`
  - `experiments/readerlab-v2/step-contracts/04t-full-source-evidence-packet.md`
  - `experiments/readerlab-v2/step-contracts/04u-technical-cofounder-notes.md`
  - `experiments/readerlab-v2/step-contracts/04v-technical-asset-cards.md`
  - `experiments/readerlab-v2/step-contracts/07t-engineering-reader-page.md`
- runner / test 落地：
  - `scripts/readerlab_v2_runner.py`
  - `tests/test_readerlab_v2_runner.py`
  - 新增检查：scope closure、evidence-layer `source_basis`、direct source back-reference
  - `python3 tests/test_readerlab_v2_runner.py`：`Ran 44 tests ... OK`
- 重新复跑两个旧 Skill case：
  - `v2-real-skill-gstack-make-pdf-20260703` 被拦在：
    `full-source-track.md missing engineering_source_scope coverage for: /Users/tianqiang/技能项目/skills-canonical/packages/gstack/make-pdf/src/print-css.ts`
  - `v2-real-skill-gstack-setup-deploy-20260703` 被拦在：
    `technical-cofounder-notes.md must preserve at least one direct source back-reference from engineering_source_scope`
- 结论：
  - 这两个失败是合理的合同迁移信号，不是当前优先修的 runner 回归。
  - `make-pdf` 正式退出代表性强基线，只保留为诊断样本。
  - `setup-deploy` 也先不手修成演示正样本，只保留为“旧产物在新合同下会被精确拦住”的证据。
  - 下一轮代表性验证目标改为 `gstack/spec`。
- 新会话交接材料：
  - `docs/current-task.md`
  - `experiments/readerlab-v2/next-session-prompt.md`
  - `/private/tmp/readerlab-handoff-20260703-gstack-spec.md`
- 重要状态：
  - 当前工作区有大量 untracked 的 V2 文件；新会话不能只看 `git diff`。

## 2026-07-03 会话交接：Python 临时 gate 之后转向 AI 质量评估 gate

- 用户指出关键概念偏差：ReaderLab 应该是一条完整流水线，其中部分环节由 Agent 智能判断，部分环节调用预先写好的透镜 / prompt；不能只改 Python 文件就宣称测试通过或质量通过。
- 当前修正结论：
  - `python3 tests/test_readerlab_v2_runner.py` 通过只代表 Python runner 临时红灯在人工构造样本上工作。
  - 这不代表完整 ReaderLab 智能流水线已通过，不代表陪读质量合格，也不代表技术解说和资产卡达到产品要求。
  - Python gate 应只承担硬规则：文件存在、结构字段、正文出现、来源引用、中文标题、失败可回指。
  - AI prompt 质量评估 gate 才应该判断：陪读是否有认知增量、技术解说是否让产品负责人听懂、资产卡是否能让未来 Agent 离开原始材料复用。
- `/code-review` 复核结果：
  - 技术解说 gate 仍可能被“产品负责人 / 为什么 / 避免 / 边界”等关键词堆词假通过。
  - 资产卡 gate 仍可能被单行字段和长废话假通过，不能证明逐卡可执行。
  - 主读者页 gate 能防完全没有正文，但不能证明净化正文是主体。
  - 高价值陪读 gate 可能误伤合法的“记录价值 + 记录节制策略”选择说明。
  - 中文标题 gate 只检查 H1，尚未覆盖正式交付层目录 / 文件名中文化。
- 已更新 `docs/current-task.md`：下一轮主线改为用 `/codebase-design` 固定“双层 gate”模块形状，再用 `/tdd` 接入 AI 质量评估 gate。
- 交接文件：`/private/tmp/readerlab-handoff-20260703-ai-quality-gate.md`。
- 重要工作区状态：V2 runner、builder、reports 和 tests 仍有大量 untracked 文件；新会话不能只看 `git diff`。

## 2026-07-03 正式红灯 gate：Skill 正文、技术解说、资产卡、中文交付面、陪读密度

- 按 `/tdd` 补正式红灯测试并接入 `scripts/readerlab_v2_runner.py`。
- 新增 runner 拦截：
  - Skill / 工程主读者页没有 `净化正文` 主体，失败。
  - 技术解说页写成工程师实现复盘，没有面向产品负责人解释设计为什么有效、不这样做会坏在哪里，失败。
  - 资产卡缺 Agent 调用方式、来源依据或独立复用要素，失败。
  - 读者可见 H1 标题不是中文，失败。
  - 因“少量 / 低干扰”删除高价值陪读，失败。
- 验证结果：
  - `python3 tests/test_readerlab_v2_runner.py`：22 tests OK。
  - `python3 tests/test_readerlab.py`：32 tests OK。
  - `python3 tests/test_readerlab_trace_validator.py`：8 tests OK。
  - `python3 tests/test_readerlab_v2_elon_fullbook_builder.py`：1 test OK。
  - `python3 tests/test_readerlab_v2_bottom_logic_builder.py`：1 test OK。
  - `python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-book-elon-fullbook-20260703`：pass。
  - `python3 scripts/readerlab_v2_runner.py check-evaluation v2-real-book-bottom-logic-insight-20260703`：pass。
  - `git diff --check`：pass。
- 诊断结果：`v2-real-skill-gstack-make-pdf-20260703` 现在按预期失败，错误指向主读者页缺净化正文主体、技术解说页未面向产品负责人、资产卡缺 Agent 调用说明。该样本不能再作为 Skill 工程合格样本。

## 2026-07-03 产品复核后纠偏：正文、技术解说、资产卡和陪读密度

- 用户复核三组样本后确认：runner 已经能跑通，但当前产物质量和读者形态仍未达到产品要求，不能把机器 `limited_accept` 当成阅读质量通过。
- 图书线：
  - 《埃隆之书》大体约 60 分，结构流程可用，但读者可见目录应中文化。
  - 陪读将就够用但不够高；此前“少量 / 低干扰”规则被过度执行，压低了本应出现的高价值经济、组织、工程、历史等视角。
  - 《底层逻辑》局部样本只证明非 Elon 图书路线能跑通，不证明图书陪读质量最终合格。
- Skill / 工程线：
  - GSTACK / make-pdf 选样偏功能性，不足以作为代表性强基线，只能保留为 runner 路径证据。
  - Skill 主读者页必须对应图书正文页：展示清洗掉执行壳后的净化正文，不能用 AI 解说替代一手材料。
  - 技术解说页的读者是产品负责人；技术负责人要讲清设计为什么有效、为什么这样设计、不这样做会坏在哪里。
  - 资产卡必须能让未来 Agent 离开原始 source 独立理解和复用。
- 已修正的误导源：
  - `docs/current-task.md`
  - `docs/product-spec.md`
  - `docs/readerlab-package-spec.md`
  - `docs/eval-gates.md`
  - `docs/readerlab-pipeline.md`
  - `docs/readerlab-agent-protocols.md`
  - `docs/technical-cofounder-method.md`
  - `docs/decisions.md`
  - `AGENTS.md`
  - `.agents/skills/readerlab/SKILL.md`
- 下一步不继续沉淀 make-pdf baseline；先补机械 gate，再选择更能展示复杂逻辑的 Skill / 工程样本。
