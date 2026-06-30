# ReaderLab DBS Suite Capability v1

## 结论

这是 repo 内 `dbs-suite` 能力地图 v1 试产包。它修正旧 demo 的核心问题：不再用 7 个代表样本冒充完整能力地图，而是覆盖当前 canonical package 的 24 个 upstream `SKILL.md`，并按能力域、触发、边界、方法原子、输出契约、验收和跨 Skill 路由组织。

它仍然不是 product ready，也不是安装或启用 `dbs-suite`。人工阅读状态保持 `pending`。`dbs-content-system` 的 tools/templates/scaffold/docs 和 `dbs-wechat-html/templates/styles.md` 只做存在性登记，没有做执行完整性深审。

## 文件

- `reader/01_能力地图.md`：读者可读能力地图，不混入 hash、validator 或机器状态长段。
- `contracts/source-registry.v1.json`：来源登记，含 package metadata 和 24 个 `SKILL.md`。
- `contracts/location-map.v1.json`：每个 Skill 至少一个可回链位置。
- `contracts/capability-map.v1.json`：能力域、24 单元 inventory、cross_skill_routes、reader_routes、coverage_plan。
- `audit/90_来源与审计.md`：来源范围、覆盖、未深审项、人工 pending 边界。
- `audit/method-absorption.md`：ReaderLab/Meta Skill 方法如何进入 v1。
- `assertions.md`：DBS-A01 到 DBS-A11 自评。

## 覆盖

- known_total_units: 24
- covered_units: dbs, dbs-action, dbs-agent-migration, dbs-ai-check, dbs-benchmark, dbs-chatroom, dbs-chatroom-austrian, dbs-content, dbs-content-system, dbs-decision, dbs-deconstruct, dbs-diagnosis, dbs-goal, dbs-good-question, dbs-hook, dbs-learning, dbs-report, dbs-resonate, dbs-restore, dbs-save, dbs-slowisfast, dbs-spread, dbs-wechat-html, dbs-xhs-title
- not_yet_covered_units: 空
- auxiliary_assets_not_deep_audited: 30 个辅助文件

## 验证命令

```bash
python3 tests/test_readerlab.py
jq empty docs/reports/readerlab-dbs-suite-capability-v1/contracts/source-registry.v1.json
jq empty docs/reports/readerlab-dbs-suite-capability-v1/contracts/location-map.v1.json
jq empty docs/reports/readerlab-dbs-suite-capability-v1/contracts/capability-map.v1.json
jq -r '.suite_overview.coverage_plan.covered_units[]' docs/reports/readerlab-dbs-suite-capability-v1/contracts/capability-map.v1.json
```
