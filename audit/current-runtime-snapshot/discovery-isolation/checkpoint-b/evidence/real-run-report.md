# Discovery V0 / V1′ 真实 Scout 调用报告

## 结论

已按 frozen run-plan 完成 `18/18` 次 Scout；没有运行 Normalizer、Judge、Clusterer 或 Verifier。18 次进程均 `exit_code=0`，完整 JSONL 均已保存并可解析，最终 agent message 均为可解析 JSON、通过对应 response schema，并另存为 `raw-response.json`。

九个 paired block 的两侧均使用同一 source hash、同一 `gpt-5.4 / medium`、同一 CLI 与 isolation flags；V0 和 V1′ 的最终 `seed_batch` 字段合同完全相同。不存在本轮允许的三类阻塞：变体基础输入不一致、最终 seed 输出合同不一致、调用结果无法保存。

## 本轮创建或修改的全部 run 和文件

### 项目内正式文件

无。ReaderLab 仓库保持只读，没有运行生产 promotion。

### 项目外工作文件

共同路径：`/private/tmp/readerlab-new-route-20260726/discovery-isolation/`。全部文件逐项路径、字节与 SHA-256 见 `checkpoint-b/evidence/full-file-manifest.json`；该 manifest 同时覆盖 Checkpoint A 冻结输入、Checkpoint B 既有候选文件、18 个正式 Scout run、失败或未采用的 probe，以及本轮证据账本。

## 18 次原始保存状态

逐 run 结果见 `basic-call-ledger.json` 的 `runs` 数组。汇总如下：

| 检查 | 结果 |
|---|---:|
| 完成调用 | 18 / 18 |
| 进程 exit 0 | 18 / 18 |
| JSONL 可解析 | 18 / 18 |
| 存在最终 agent message | 18 / 18 |
| 最终 message 是可解析 JSON | 18 / 18 |
| 通过对应 response schema | 18 / 18 |
| 独立 `raw-response.json` 已保存 | 18 / 18 |
| 最终 `seed_batch` 字段合同一致 | 18 / 18 |
| paired block 基础输入一致 | 9 / 9 |
| 下游语义调用 | 0 |

原始 seed 数只作调用事实记录：

- V0：9 次，共 34 个 seed；
- V1′：9 次，共 37 个 seed。

这些原始数尚未经过任何 Normalizer、技术 Judge、聚类、核验或产品判断，不能解释为 V1′ 已胜出。

## 基础调用账本

- 模型：`gpt-5.4`
- reasoning effort：`medium`
- CLI：`codex-cli 0.142.5`
- 固定 isolation flags：
  - `features.plugins=false`
  - `features.apps=false`
  - `skills.include_instructions=false`
- 调用顺序：`protocol/run-plan.json` 的 1–18
- 每次保存：exact prompt、output schema、preflight、read-set manifest、request、完整 JSONL、stderr、receipt、raw response

Provider usage 原始合计：

| cohort | input tokens | cached input | output tokens | reasoning output |
|---|---:|---:|---:|---:|
| V0 | 449,673 | 215,808 | 20,996 | 10,674 |
| V1′ | 325,761 | 172,288 | 25,701 | 10,569 |

`cached_input_tokens` 是 input 的子集，`reasoning_output_tokens` 是 output 的子集，这里不重复相加。Provider billed cost、resolved backend snapshot 与 exact system prompt 仍不可观测。

## 限制

18 个 run 都至少有一个 `source_anchor_quote_en` 未成为冻结 source 的逐字连续子串；V0 的 34 个锚点中逐字命中 0 个，V1′ 的 37 个中命中 1 个。因此既有 harness 把 18 次都标为 `MODEL_CONTRACT_FAILURE`。

该标记和原始保存事实必须分开理解：

- 模型返回的 JSON 结构和两变体最终 `seed_batch` 字段合同均有效；
- 完整原始结果均可解析、可保存；
- 锚点问题是两侧共同出现的内容级限制，不构成“只有一个变体换了输入或输出合同”；
- 本轮按用户最新指令不新增修复、不重跑、不进入下游，只保留证据。

另外，部分调用自行使用了较多上下文或工具，造成 token 差异很大；这是调用成本 limitation，不在本轮三个 smoke blocker 内，也未被解释为产品结果。

## 技术状态与停止点

- `implemented`：18 次原始 Scout 调用及证据存在；
- `integrated`：只集成到外部 sidecar 运行目录，未进入 ReaderLab 生产；
- `verified`：18 次 JSONL/最终 JSON/schema/save、9 个 paired block 基础输入与最终字段合同已机械复算；
- `accepted`：不存在。尚未进行任何知识质量或产品体验验收。

现在停止。下一步只能由总控基于这 18 份原始 evidence 决定是否读取或比较内容；本轮没有授权，也没有执行任何下游处理。
