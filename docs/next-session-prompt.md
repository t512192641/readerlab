# ReaderLab Next Session Prompt

本文件从 `docs/current-task.md` 派生，不是事实源。若两者冲突，以 `docs/current-task.md` 为准。

```text
/goal 从 /Users/tianqiang/Documents/读书伴侣 继续 ReaderLab。

先读：
1. AGENTS.md
2. docs/current-task.md

不要启动时读取 dev-state、progress、旧报告、旧 prompt、旧 fullbook、旧 bakeoff 或原始聊天。

当前目标：
- 不写正式 SKILL.md。
- 不继续跑大 demo。
- 不标记 transferable_method_kernel_pass。
- 只补正式 Skill 草案前的两个硬缺口：
  1. 最小 trace validator
  2. 最小 comment replay fixture

当前状态：
- two_demo_internal_pass: 2/2
- private_material_validation_local_pass: 2/2
- formal_skill_delivery_design_ready: yes
- skill_delivery_design_docs: created
- trace_validator_implemented: not_started
- comment_replay_verified: not_verified
- skill_draft_not_started

先读设计文档：
- docs/readerlab-skill-delivery-spec.md
- docs/readerlab-skill-ir-v1.md
- docs/contracts/location-anchor-v1.md
- docs/contracts/trace-validation-v1.md
- docs/contracts/comment-replay-v1.md

下一步：
1. 在现有 scripts/tests 结构中实现或设计最小 trace validator。
2. 用 A2 private longform 和 B2 planning-with-files 各做 2 条 comment replay fixture。
3. 验证：
   - python3 tests/test_readerlab.py
   - git diff --check
   - 新增 validator / replay 检查命令
4. 更新 docs/current-task.md 和 docs/agent-run-ledger.md。

停止条件：
- 创建正式 SKILL.md。
- 把 private/local validation 说成 public external validation。
- 标记 transferable_method_kernel_pass。
- trace validator 不能连接 reader paragraph、anchor、claim、candidate/gate。
- comment replay 不能从 comment 回到 body anchor、claim、candidate 和 gate decision。
```
