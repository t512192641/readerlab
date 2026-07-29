# ReaderLab 阶段实现状态

> 本表是工程状态投影，不拥有产品目标、产品判词或长期合同。当前任务只实现已验证的 Expert Teaching
> 控制层，不授权下游生产。

| 阶段 | 当前状态 | 当前实现 | 是否进入生产 |
|---|---|---|---|
| 材料冻结 | 可用 | 根目录 `tools/run.py` 的确定性工具 + Skill 输入冻结 | 部分 |
| Discovery | 未验证 | 历史实验记录；本轮未运行 | 否 |
| Expert Teaching | Skill v0.1.1 候选 | 版本化 `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1`，人工 dispatcher | 否 |
| Expert Review | Skill v0.1.1 候选 | 同一版本的独立 read set、来源 allowlist 与双门解析 | 否 |
| Writer | 待专项验证 | T2.37 sidecar | 否 |
| Fidelity | 实验态 | sidecar | 否 |
| B2 装配 | 未集成 | 候选工具／历史记录 | 否 |
| 总编排 | 人工 | 无 orchestrator | 否 |

当前是人工串联的阶段 Skills，不是完整 ReaderLab runtime。

## v0.1.1 实现边界

Skill v0.1.1 固定四项输入（原文、框架身份、source map、结构化来源 allowlist），生成 Expert／审核任务和
精确 read set，冻结输出，解析 `SOURCE_FIDELITY_*` 与 `TEACHING_*` 双门，机械生成可读产品包，验证并归档。
任务只显示 `allowed` URL 与显式登记的 redirect；`reference_only` 可以被输出引用但不是网络权限，
`blocked` 和新增 URL 均失败。中文表达规则、内部泄露门、版本 fingerprint 和 replay hash 是确定性控制。
语义调用、来源搜索、Agent 启动和产品负责人接受仍由人工控制；Skill 不发现 C、不调用 Writer、不做 Reader
压缩、Fidelity、B2、ABC、Discovery 或完整 orchestrator。

## 版本与验证

- 历史 `0.1.0` 根入口保持不可变；当前 dispatcher 由 `CURRENT_VERSION` 明确指向独立的 `0.1.1` 目录。
- 每个 run 保存版本、Skill／合同／模板 fingerprint 与来源 allowlist hash；漂移或错误版本使 `verify` 失败。
- T2.38 仅作为冻结输出注入的 mechanical replay fixture；不重新调用模型、不打开网络、不产生新产品判词，
  并逐项核验输入、输出、产品包和 archive 成员 hash。
- `0.1.0` 尚未运行迁移样本；`0.1.0` 与 `0.1.1` 结果不得静默混算。当前仍为人工编排、`not_integrated`，
  不是完整 runtime 或生产资格。
