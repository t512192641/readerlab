# ReaderLab 阶段实现状态

> 本表是工程状态投影，不拥有产品目标、产品判词或长期合同。当前任务只实现已验证的 Expert Teaching
> 控制层，不授权下游生产。

| 阶段 | 当前状态 | 当前实现 | 是否进入生产 |
|---|---|---|---|
| 材料冻结 | 可用 | 根目录 `tools/run.py` 的确定性工具 + Skill 输入冻结 | 部分 |
| Discovery | 未验证 | 历史实验记录；本轮未运行 | 否 |
| Expert Teaching | Skill v0.1 候选 | `.agents/skills/readerlab-book-expert-teaching` | 否 |
| Expert Review | Skill v0.1 候选 | 同一 Skill 的独立 read set 与双门解析 | 否 |
| Writer | 待专项验证 | T2.37 sidecar | 否 |
| Fidelity | 实验态 | sidecar | 否 |
| B2 装配 | 未集成 | 候选工具／历史记录 | 否 |
| 总编排 | 人工 | 无 orchestrator | 否 |

当前是人工串联的阶段 Skills，不是完整 ReaderLab runtime。

## v0.1 实现边界

Skill v0.1.0 只固定三项输入（原文、框架身份、来源白名单），生成 Expert／审核任务和精确 read set，
冻结输出，解析 `SOURCE_FIDELITY_*` 与 `TEACHING_*` 双门，机械生成可读产品包，验证并归档。语义调用、
来源搜索、Agent 启动和产品负责人接受仍由人工控制；Skill 不发现 C、不调用 Writer、不做 Reader 压缩、
Fidelity、B2、ABC、Discovery 或完整 orchestrator。

## 版本与验证

- `VERSION`: `0.1.0`。
- 每个 run 保存 Skill／合同／模板 fingerprint；漂移使 `verify` 失败。
- T2.38 仅作为冻结输出注入的 mechanical replay fixture；不重新调用模型，不产生新产品判词。
- v0.1.0 冻结后，后续两个迁移样本必须使用相同版本；问题只记录 observation，不能静默修改并混算。
