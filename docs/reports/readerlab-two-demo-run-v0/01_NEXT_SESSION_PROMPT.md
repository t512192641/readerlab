# Next Session Prompt: Run Two Internal ReaderLab Demos

Use this prompt in the next Codex session. It is for running demos internally, not for GPT Pro review.

```text
/goal 从 /Users/tianqiang/Documents/读书伴侣 继续 ReaderLab 方法核验证。

先读两个入口文件：
1. AGENTS.md
2. docs/current-task.md

然后只读本轮执行合同：
3. docs/reports/readerlab-two-demo-run-v0/README.md

当前目标：
- 跑两个新的内部 demo，而不是写 GPT Pro 审核 prompt。
- Demo A：书籍/长文完整正文轨 demo，证明 Body Track Gate 和 reader package 最小形态。
- Demo B：Skill/工程材料 demo，证明净化正文、设计资产、Skillization Gate 和批注触发。
- 两个 demo 都必须经过 writer agent 产出、reader evaluation agent 评价、主控回收验证。
- 只有两个 demo 都内部通过，才允许下一步准备 GPT Pro review packet。

严格边界：
- 不写正式 ReaderLab Skill。
- 不做外部书泛化验证。
- 不扩写整本《埃隆之书》。
- 不把 copyrighted full text 提交到 GitHub。
- 不用 AI 生成假正文或摘要冒充正文。
- 不读取旧 fullbook、旧 bakeoff、旧 GPT Pro prompt，除非 current-task 或 run contract 明确触发。

执行顺序：
1. 选择 Demo A 合规长文源。
   - 优先用户自有或公版/许可文本。
   - 若没有可提交完整正文的源，停止并报告 blocked_missing_compliant_longform_source。
2. 选择 Demo B Skill/工程源。
   - 默认 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md`。
   - 如果下一会话判断 `spec` 过重或机器协议噪音过多，可改用 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/design-review/SKILL.md`。
   - 如果需要 DB Skills 备选，可用 `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-xhs-title/SKILL.md` 或 `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-diagnosis/SKILL.md`。
   - 只选一个 Skill 单元；不整包重跑 gstack 或 dbs-suite。
   - 不安装、不同步、不启用 Skill，只作为阅读材料。
3. 为每个 demo 调用 writer agent。
   - writer 只能读所选源、contracts、必要方法文档。
   - writer 产出正文轨/净化正文、reader-facing 页和 audit contracts。
4. 为每个 demo 调用 reader evaluation agent。
   - reader 只评价，不改写。
   - 硬门槛全过、读者分 >= 10/12、无 P0/P1，才可进入主控落地。
5. 主控回收。
   - 任何一个 demo 未通过，就只写 failure report，不准备 GPT Pro review。
   - 两个都通过，更新 docs/current-task.md 和 ledger，说明 demo_internal_pass。

产物位置：
docs/reports/readerlab-two-demo-run-v0/demos/

每个 demo 必须包含：
- README.md
- source-registry.json
- 10_一手正文/
- 20_AI陪读/
- audit/contracts/body-track-gate.json
- audit/contracts/material-profile.json
- audit/contracts/claim-ledger.json
- audit/contracts/candidate-tournament.json
- audit/contracts/skillization-gate.json
- audit/contracts/annotation-trigger.json
- audit/contracts/high-order-explanation.v1.json
- audit/eval.md

通过线：
- Body Track Gate 对 demo 类型成立。
- candidate tournament 至少有一个真实 downgrade 或 reject。
- claim ledger 约束 reader-facing，不把 AI 解释写成作者原意。
- skillization gate 阻止不满足六项条件的 insight。
- annotation triggers 有 3-7 个 body-adjacent questions。
- reader-facing 不暴露内部字段。
- `python3 -m json.tool` 全部 JSON 通过。
- `python3 tests/test_readerlab.py` 通过。
- `git diff --check` 通过。

验证命令：
find docs/reports/readerlab-two-demo-run-v0/demos -name '*.json' -print -exec python3 -m json.tool {} /tmp/readerlab-demo-json.out \;
rg -n "source refs|claim trace|lens score|machine_status|human_status|Body Track Gate|Claim Ledger|Candidate Tournament|Skillization Gate|Annotation Trigger" docs/reports/readerlab-two-demo-run-v0/demos/*/20_AI陪读
python3 tests/test_readerlab.py
git diff --check

停止条件：
- 合规长文正文源缺失。
- writer 使用旧 fullbook / bakeoff / GPT Pro prompt。
- 任一 demo reader-facing 暴露内部字段。
- 任一 demo 无 downgrade/reject。
- 任一 demo reader evaluation fail、有 P0/P1，或分数 < 10/12。
- 只有一个 demo 通过。
```
