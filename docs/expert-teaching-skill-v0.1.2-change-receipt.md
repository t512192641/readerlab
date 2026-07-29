# ReaderLab Book Expert Teaching Skill 0.1.2 change receipt

- previous version: `0.1.1`
- new version: `0.1.2`
- baseline commit: `24512d27987a03add95fb81663418eed700bd6a6`
- release branch: `feature/readerlab-book-expert-teaching-skill-v0.1`
- change type: migration-boundary and source-access hardening only

## 修复内容

1. 将 current dispatcher 移到 Skill 根目录 `run-current.py`，删除 `scripts/run-current.py`，因此历史
   0.1.0 fingerprint 只覆盖原有根实现；用显式三段数字版本格式，并要求目标目录与 `VERSION` 精确一致。
2. 发布独立 `versions/0.1.2/` 实现，冻结 0.1.0 发布基线 aggregate fingerprint
   `4730c7392c67bd927b9d3609854141f6b8fb6297631381834d1d43275690233f`，增加旧入口漂移与错版本拒绝测试。
3. 增加 `readerlab-book-expert-teaching/source-access/v1`，由 Expert 和 reviewer 分别写入访问回执；
   `opened_urls` 只允许 `allowed`，`cited_only_urls` 允许 `allowed`／`reference_only`，数组互斥，
   `blocked`／未登记 URL 机械失败。回执明确 `provenance: agent_declared`，不是浏览器或 OS 级网络审计。
4. 在 `init` 生成并冻结 `control/source-boundary.json`，严格闭合 source map 与 allowlist：source map 中每个 URL
   必须登记；每个 canonical allowlist URL 必须出现在 source map；只有显式 redirect 可以额外存在。
5. seal／verify 检查 Expert 正文、Expert 来源表、Expert 回执、review 正文和 reviewer 回执的 URL，
   stage freeze、manifest、ledger 和 archive 都保留两份回执及其 hash。
6. 删除 0.1.2 中未使用的 `urls_from_source_map()`；修正 source map 与机器网络 allowlist 的合同语义，
   合并 Expert 任务中的重复归属规则；保持自然正文中的 M1/M2/M3/Writer 不误杀。
7. T2.38 mechanical replay 改为使用显式访问回执 fixture，逐项验证新增 fixture hash、产品身份、archive
   条目和两份回执 hash；回放不调用模型或网络。

## 为什么修改

外部 Code Review 发现，dispatcher 位于 0.1.0 fingerprint 扫描目录会污染历史身份；缺少访问回执无法区分
“打开”与“仅引用”；source map 与网络 allowlist 没有严格闭合；只冻结来源表会漏检正文 URL；旧 replay
fixture 也没有证明访问事实和 archive 身份。上述修改只补可复验的工程边界，不改变六个阶段命令、双门终局、
人工编排定位或 Expert Teaching 语义目标。

## 版本和结果隔离

- `0.1.0` 尚未运行迁移样本；本轮没有运行迁移样本，也没有启动语义 Agent、Writer、Discovery、ABC 或完整编排器。
- `0.1.0`、`0.1.1`、`0.1.2` 的实现、run、fingerprint、产品 hash 和结果不得静默混算。
- T2.38 replay 只注入已冻结字节，是 deterministic mechanical replay，不产生新的语义结果或产品判词。

## 验证范围

- Skill-local tests：`36/36` 通过；quick validation、mechanical replay、`git diff --check` 和敏感信息检查通过。
- repository active tests：`35/36` 通过；唯一失败为资产登记之外的基线遗留未跟踪 Markdown 全树穷举项；该类文件不由本轮修改。
- `integrated: not_integrated`；`accepted: unknown`；不得把本 receipt 当作迁移资格或产品接受。
