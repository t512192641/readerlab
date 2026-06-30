# DBS Assertions v1

对象：`docs/reports/readerlab-dbs-suite-capability-v1/`。

结论：11 pass / 0 partial / 0 fail。该结论只表示 repo 内手工试产包满足 DBS-A01..A11，不表示 product ready 或人工阅读验收通过。

| ID | 结果 | 证据 | 路径 | 未解决项 |
|---|---|---|---|---|
| DBS-A01 | pass | 使用 `readerlab.capability-map.v1`，没有生成图书式 `grounded-global-map.v1`。 | `contracts/capability-map.v1.json` | 无；仍需人工阅读复核。 |
| DBS-A02 | pass | 8 个能力域都有 trigger signal、method atom、output contract、verification method。 | `contracts/capability-map.v1.json` | 无；仍需人工阅读复核。 |
| DBS-A03 | pass | 每个能力域和 24 个 inventory unit 都有 source_refs，回到 canonical SKILL.md location。 | `contracts/source-registry.v1.json, contracts/location-map.v1.json` | 无；仍需人工阅读复核。 |
| DBS-A04 | pass | suite 顶层 not_for、每个能力域 near_neighbor_exclusions、route_conflicts 均已写入。 | `contracts/capability-map.v1.json` | 无；仍需人工阅读复核。 |
| DBS-A05 | pass | reader_routes 覆盖第一次理解、真实任务选择、输出验收。 | `contracts/capability-map.v1.json, reader/01_能力地图.md` | 无；仍需人工阅读复核。 |
| DBS-A06 | pass | `machine_status` 与 `human_status` 分开，人工状态保持 pending；审计明确不能把机器状态当人工接受。 | `contracts/*.json, audit/90_来源与审计.md` | 无；仍需人工阅读复核。 |
| DBS-A07 | pass | review_items 覆盖来源精度、路由冲突、辅助资产未深审和生成器能力未证明。 | `contracts/capability-map.v1.json, audit/90_来源与审计.md` | 辅助资产执行深审和真实路由反测仍待做。 |
| DBS-A08 | pass | 每个能力域都有 route_decisions，且 cross_skill_routes 覆盖入口、诊断、内容、发布、状态、content-system、聊天室/agent 迁移。 | `contracts/capability-map.v1.json` | 无；仍需人工阅读复核。 |
| DBS-A09 | pass | coverage_plan known_total_units=24，covered_units 列 24 个 Skill，not_yet_covered_units 为空。 | `contracts/capability-map.v1.json` | 辅助资产不是 SKILL unit，未计入 not_yet_covered_units；已在 review item 标注。 |
| DBS-A10 | pass | 读者稿不放 hash、validator 或机器状态长段；审计细节进入 audit/contracts。 | `reader/01_能力地图.md, audit/90_来源与审计.md` | 无；仍需人工阅读复核。 |
| DBS-A11 | pass | 每个能力域说明预期产物和验收检查，不只列技能名或路径。 | `reader/01_能力地图.md, contracts/capability-map.v1.json` | 无；仍需人工阅读复核。 |


## 剩余风险

- v1 是手工试产包，不证明 ReaderLab 生成器稳定能力。
- `dbs-content-system` tools/templates/scaffold/docs 和 `dbs-wechat-html/templates/styles.md` 尚未执行完整性审计。
- 跨 Skill 路由优先级仍需要真实用户任务反测。
- 人工状态仍为 `pending`。
