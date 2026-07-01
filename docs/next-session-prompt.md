# ReaderLab Next Session Prompt

本文件从 `docs/current-task.md` 派生，不是事实源。若两者冲突，以 `docs/current-task.md` 为准。

```text
/goal 从 /Users/tianqiang/Documents/读书伴侣 继续 ReaderLab。

先读两个入口文件：
1. AGENTS.md
2. docs/current-task.md

启动阶段不要读取 dev-state、progress、旧 fullbook、旧 bakeoff、旧 GPT Pro prompt、旧报告、长 ledger 或原始聊天。
docs/current-task.md 是当前执行事实唯一入口；它会告诉你哪些文件只有在具体动作发生时才需要读取。

当前阶段：
- ReaderLab 已完成 demo 验证、private material validation、Skill delivery design docs、最小 trace validator、最小 comment replay fixture。
- 当前可以进入“正式 ReaderLab Skill 草案实现合同”阶段。
- 还不允许直接创建正式可运行 SKILL.md，除非本轮先完成合同并得到用户明确批准。

当前状态口径必须保持：
- two_demo_internal_pass: 2/2
- private_material_validation_local_pass: 2/2
- formal_skill_delivery_design_ready: yes
- skill_delivery_design_docs: created
- trace_validator_implemented: minimal_pass
- comment_replay_fixture_pass: 1/1
- comment_replay_verified: fixture_pass_real_obsidian_ui_deferred
- transferable_method_kernel_pass: not_verified
- skill_draft_not_started
- public_external_material_validation_not_started

不要使用的旧口径：
- 不得把 15 章高阶讲解称为 reader_package_pass。
- 不得把 two-demo、private validation 或 fixture replay 称为 transferable_method_kernel_pass。
- 不得把 Skill delivery design docs 称为正式可运行 Skill。
- 不得把 fixture replay 说成真实 Obsidian UI replay。
- 不得把 private/local validation 说成 public external validation。

本轮目标：
写清并落地“正式 ReaderLab Skill 草案实现合同”，让下一步能安全进入正式 Skill draft。
合同要回答：
1. 这个 Skill 接收什么输入。
2. 如何判断材料路线：book_or_longform / skill_or_engineering_doc / mixed_material_package。
3. 每条路线生成什么文件。
4. 哪些步骤由脚本自动做，哪些必须由 agent 判断。
5. 哪些 gate 必须先过，才能生成正式 SKILL.md。
6. 如何调用现有 trace validator 和 comment replay fixture。
7. 真实 Obsidian UI replay 如何作为后补验收项，而不是当前阻塞项。

推荐多 agent 协作模式：

主控 agent：
- 只负责读入口文件、确认边界、拆任务、回收结果、验证和对用户汇报。
- 不把旧报告或聊天历史当事实源。
- 不直接宣称 pass，除非有命令或文件证据。

Contract writer agent：
- 只读：
  - docs/current-task.md
  - docs/readerlab-skill-delivery-spec.md
  - docs/readerlab-skill-ir-v1.md
  - docs/contracts/location-anchor-v1.md
  - docs/contracts/trace-validation-v1.md
  - docs/contracts/comment-replay-v1.md
  - scripts/readerlab_trace_validator.py
  - tests/test_readerlab_trace_validator.py
- 产出正式 Skill 草案前的实现合同，不写正式 SKILL.md。
- 合同必须包含输入、输出、路线、workflow、agent/script boundary、gates、状态机、stop conditions、验证命令。

Reviewer agent：
- 只评价 Contract writer 的合同，不改写。
- 检查是否误启动正式 Skill、是否过度声明 transferable pass、是否遗漏真实 Obsidian UI replay 后补项、是否混淆 private/local 和 public external。
- 给出 pass/fail 和 P0/P1/P2。

Implementation planner agent（可选）：
- 只在合同通过后参与。
- 把合同拆成正式 Skill draft 的最小实现步骤。
- 不创建 SKILL.md，除非主控确认用户已经明确批准进入正式草案。

本轮允许读取：
- docs/readerlab-skill-delivery-spec.md
- docs/readerlab-skill-ir-v1.md
- docs/contracts/location-anchor-v1.md
- docs/contracts/trace-validation-v1.md
- docs/contracts/comment-replay-v1.md
- scripts/readerlab_trace_validator.py
- tests/test_readerlab_trace_validator.py
- docs/reports/readerlab-comment-replay-v0/README.md
- docs/reports/readerlab-comment-replay-v0/results/eval.md

按需读取：
- docs/product-spec.md：需要产品边界时。
- docs/readerlab-package-spec.md：需要最终包结构时。
- docs/dev-state.md：需要稳定路径或工具状态时。
- docs/decisions.md：需要耐久决策时，优先 D-052 之后。
- docs/agent-run-ledger.md：只读顶部最新一两条，用于验证证据。

不要读取：
- 旧 fullbook。
- 旧 bakeoff。
- 旧 GPT Pro prompt。
- 旧长报告。
- 原始聊天。
- 除非合同明确需要，不展开 docs/reports/** 的历史目录。

建议产物：
- docs/readerlab-formal-skill-draft-contract.md

如果合同需要机器可检验，可新增：
- docs/contracts/formal-skill-draft-readiness-v1.md

但不要创建：
- SKILL.md
- .agents/skills/readerlab/
- 可安装 Skill 包
- LifeAtlas 正式沉淀区产物

验收标准：
- 合同能让后续 agent 明确知道什么时候可以创建正式 ReaderLab Skill draft。
- 合同明确 fixture replay 已过，但 real Obsidian UI replay deferred。
- 合同明确 trace validator 的调用方式：
  python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
- 合同不把私有验证、公版验证、外部公开泛化混在一起。
- 合同不让 reader-facing 暴露内部 audit 字段。
- Reviewer agent 无 P0/P1 后，主控才能更新 current-task 和 ledger。

验证命令：
- python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
- python3 tests/test_readerlab_trace_validator.py
- python3 tests/test_readerlab.py
- git diff --check

停止条件：
- 创建正式 SKILL.md。
- 标记 formal_skill_draft_started。
- 标记 transferable_method_kernel_pass。
- 把 fixture replay 说成真实 Obsidian UI replay。
- 把 private/local validation 说成 public external validation。
- 合同没有明确 human approval gate。
- 合同没有明确 agent/script boundary。
- reviewer agent 给出 P0/P1。
```
