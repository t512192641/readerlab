---
name: readerlab-functional-role-isolation
description: Run a fictional ReaderLab producer-to-judge check with two fresh Codex agents, frozen JSON handoffs, a post-judgment hidden key, mechanical scoring, and a reproducible receipt. Use when validating functional role/input isolation without claiming an OS or container security boundary.
---

# ReaderLab 功能性角色隔离

只对明显虚构、首个非空行是 `FICTIONAL TEST MATERIAL` 的短材料运行。把本 Skill 当作功能性上下文与输入隔离；它不是防止 Agent 主动越权读取的文件系统安全沙箱。

## 顺序执行

1. 在 run 目录外准备 `source.md`、`producer-brief.md` 与 `rubric.md`。在 brief 中加入本次唯一私有标记；不要提前创建标准答案。
2. 执行：

   ```bash
   python3 scripts/role_run.py init --run <new-run> --source <source.md> --brief <producer-brief.md> --rubric <rubric.md> --candidate-id <id>
   ```

3. 用 `spawn_agent` 启动 producer，必须设置 `fork_turns="none"`。启动消息只能列出：
   - `<run>/producer/input/source.md`
   - `<run>/producer/input/brief.md`
   - `<run>/producer/output/candidate.json`
   - 下方 candidate JSON 格式

   明确要求只读这两个输入、只写该输出、不搜索仓库、不列目录、不读其他路径；缺信息就报告 blocker。不要传递主控历史、rubric 或标准答案。
4. producer 完成后，先检查私有标记没有出现在 candidate，再执行：

   ```bash
   python3 scripts/role_run.py seal-candidate --run <run>
   ```

   命令会先独占写入 candidate seal，再复制 judge 输入并写入 handoff 证据。成功后再次确认私有标记没有出现在 judge 输入。
5. 用另一个 `spawn_agent` 启动 judge，也必须设置 `fork_turns="none"`。启动消息只能列出：
   - `<run>/judge/input/source.md`
   - `<run>/judge/input/candidate.json`
   - `<run>/judge/input/rubric.md`
   - `<run>/judge/output/judgment.json`
   - 下方 judgment JSON 格式

   明确要求只读这三个输入、只写该输出、不搜索仓库、不列目录、不读其他路径；缺信息就报告 blocker。不要传递 producer brief、producer 对话、主控历史、其他 run 产物或标准答案。
6. judge 完成后执行：

   ```bash
   python3 scripts/role_run.py seal-judgment --run <run>
   ```

7. 只有上一步成功后，才把预期 verdict 交给 scorer：

   ```bash
   python3 scripts/role_run.py score --run <run> --expected-verdict PASS
   python3 scripts/role_run.py verify --run <run>
   ```

8. 检查私有标记没有出现在 judgment 中，并复核它在整个 run 中只存在于 `producer/input/brief.md`。报告两个 Agent ID、两次 `fork_turns="none"`、两个 SHA-256、标准答案时序、机械比较、verify 和 run 路径。

## 精确 JSON 格式

Candidate 只允许这些字段：

```json
{
  "schema": "readerlab-functional-candidate/v1",
  "candidate_id": "fictional-001",
  "claim": "候选主张",
  "evidence": ["仅来自本次虚构 source 的证据"]
}
```

Judgment 只允许这些字段：

```json
{
  "schema": "readerlab-functional-judgment/v1",
  "candidate_id": "fictional-001",
  "verdict": "PASS",
  "reasons": ["依据本次 rubric 的理由"]
}
```

把两份示例中的 `fictional-001` 替换为 `init --candidate-id` 使用的同一个值。`verdict` 只能是 `PASS` 或 `FAIL`。任何命令失败都停止链路；不得覆盖、修补或绕过冻结产物。
