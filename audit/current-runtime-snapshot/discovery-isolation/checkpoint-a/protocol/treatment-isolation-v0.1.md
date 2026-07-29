# Discovery treatment isolation v0.1 — Checkpoint A 冻结候选

状态：`CHECKPOINT_A_CANDIDATE / NO_SEMANTIC_RUNS / V1_NOT_PROMOTED`

## 1. 要回答的唯一问题

旧 V1 的结果受输出合同、rubric 对齐、共享聚类代表、材料级 Judge 和弱对照混杂，不能说明“先找触发点”本身有效。本实验只隔离一个处理变量：

- **V0**：直接生成 0–6 个 seed；
- **V1'**：先自由生成独立 trigger_map，再生成 0–6 个 seed。

两者的最终 `seed_batch` 使用完全相同 schema、字段长度、seed 上限、模型、effort、材料和后续流程。trigger_map 只存入密封审计区，不给 Normalizer、Judge、Clusterer、Verifier 或产品负责人。V1' 没有固定答案空间；Judge rubric 也不回写 Scout。

## 2. 固定处理链

```text
material exact bytes
  -> Scout V0 or V1' (only treatment differs)
  -> strip/seal trigger_map
  -> variant-blind unified Normalizer
  -> one blind set / one fresh Judge context
  -> cross-run semantic clustering
  -> representatives verified separately by variant
  -> uniform anonymous product pack
  -> technical eligible ∩ explicit product approval
```

Normalizer 只收到当前 `source.txt` 和 `seed_batch`，不收到 variant、trigger_map、其他 run 或 Judge rubric。它不得添加新机制或新来源，只把每个候选压成 240–280 个中文字符的统一展示卡；超长、缺锚点或无法忠实压缩者标为无效，不补写。产品包只含该展示卡和随机 blind ID，不含人物/机构/路线、来源、variant、run、技术评分或 trigger_map。

每个 blind set（一个材料×一个变体×一次重复）使用独立、无历史的新 Judge 上下文。Judge 只做技术筛选：是否有外部机制增量、锚点是否对应、是否可核验、是否只是换名；可判整组 0 个通过。产品判断始终归产品负责人。

聚类以机制同一性去重，不以名字相似或来源相同自动合并。一个 cluster 若两变体都命中，必须各选本变体自己的代表，各自核验；不得用另一变体的强代表代替。某变体只有其本变体代表技术核验成功，才拥有该机制。

## 3. 18 个 Scout 与交叉平衡顺序

三份材料 × 两变体 × 三次独立重复 = 18 个 Scout。每一材料/重复形成相邻 paired block，先后顺序随机后交叉平衡；固定随机种子 `a39e0c7d91b6425f`，算法为 Python `random.Random(int(seed,16))` 对 9 个 block 与 5 个 V0-first/4 个 V1'-first 标签分别 shuffle。

| 执行 block | pair | 先运行 | 后运行 |
|---:|---|---|---|
| 1 | CTL01-R1 | V1' | V0 |
| 2 | POS01-R1 | V1' | V0 |
| 3 | POS02-R1 | V0 | V1' |
| 4 | POS01-R3 | V0 | V1' |
| 5 | CTL01-R3 | V0 | V1' |
| 6 | POS02-R3 | V0 | V1' |
| 7 | CTL01-R2 | V1' | V0 |
| 8 | POS01-R2 | V0 | V1' |
| 9 | POS02-R2 | V1' | V0 |

每个 Scout 必须新建空工作目录，只挂载单独 material、该变体 prompt 与共同 schema；运行前后校验 exact read-set。Scout 之间不续聊、不共享输出。后续 Normalizer/Judge/Verifier 也必须 fresh context。

## 4. 预注册主结果与停止门

主结果不是原始 seed 数，而是：

> 两个正例中，**技术合格 ∩ 产品负责人明确批准**的去重机制数。

产品负责人对每张匿名卡分别记录：`陌生性`、`重读增益`、`自然度`、`愿不愿进入 Expert`，并给出不可由模型代填的 `approve_for_expert = yes / no / unsure`。只有明确 `yes` 计入产品批准；四维是产品判词的理由记录，不由技术分数自动合成。

V1' 只有同时满足以下条件才通过：

1. 两个正例合计主结果比 V0 **净增至少 2 个**去重机制；
2. 对每个正例，至少一次主结果命中的 paired repeat 数不低于 V0；
3. 对照中产品批准的 false pass 数不高于 V0；
4. 包含 Scout、Normalizer、Judge、聚类和核验的总 input+output tokens 不超过 V0 的 110%；若 provider 报告 billed cost，则费用也不超过 110%。

任一项失败：`DISPROVED_AND_STOP`；全部满足但 billed cost 不可观测：最多 `CANDIDATE_CONTINUE_EVIDENCE`，不能 promotion；全部满足且成本可判：`ADVANCE_LIGHTWEIGHT_CANDIDATE`。小样本只报原始数，不报稳定百分比。

## 5. 能力保护

- V1' 的 trigger 是自由文本关系，不给异常分类、学科清单、框架名或候选答案。
- Scout 不见 Judge rubric，Judge 不见 trigger_map，产品负责人不见技术身份。
- 三个阶段都允许 0 候选/0 通过；海事词不能强迫对照产出。
- Federalist 的材料选择理由不进入任何生产 prompt。
- V1' 当前仍为 `NOT_PROMOTED`；本实验通过也只证明 Discovery 前端，不证明完整 Expert 环节。

## 6. P0 调用冻结与可观测边界

正式候选 invocation 固定：

- Codex CLI `0.142.5`；
- `codex exec --json --ephemeral --ignore-user-config --ignore-rules`；
- model alias `gpt-5.4`，reasoning effort `medium`；
- `--sandbox read-only`，空工作目录；
- session flags：`features.plugins=false`、`features.apps=false`、`skills.include_instructions=false`；
- 每 run 保存 exact user request bytes/hash、完整 argv 与 canonical request hash、CLI version、完整 JSONL、stderr、UTC start/end、exit code和 provider token usage。

无隔离 flags 的非语义 probe 输入为 17,697 tokens，并出现 skills context 注入；加 flags 后不再出现该提示，输入降至 9,830 tokens，证明参数有效，正式 harness 必须固定。仍不可观测：

| 项 | 状态 | 是否阻塞 |
|---|---|---|
| exact user prompt/request、model alias、effort、CLI version、JSONL、起止时间、token | observed + hash | 否 |
| resolved backend snapshot | unknown | 不阻塞同一短窗口的 paired 相对比较；若运行中 alias/CLI 改变，阻塞并作废受影响 pair |
| exact system prompt | unknown | 不阻塞相同 flags 的 paired 相对比较；隔离提示再次出现则阻塞 |
| provider billed cost | unknown | 不阻塞收集技术证据，但阻塞“成本门已通过”与 promotion |

`gpt-5.6-terra` 在当前 CLI 明确失败（要求更新版本），失败 transcript 保留；不得静默回退或把失败 probe 算入实验。P0 prompt 不含三份材料的任何语义。

## 7. Checkpoint 停止点

Checkpoint A 只冻结材料、协议、prompt/schema 和 invocation 证据。未获得总控接受前，不运行 18 个 Scout，不运行 Normalizer/Judge/Verifier，不制作产品包，不改仓库，不 promotion。
