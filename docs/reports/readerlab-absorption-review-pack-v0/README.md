# ReaderLab Absorption Review Pack v0

本目录是 absorption review pack，用来把上一轮“吸收程度小样草案”落成可审查的 repo 内产物。

它不是正式 LifeAtlas 样张，不写入 LifeAtlas，不修改 canonical source package，不安装 Skill，不新增依赖，也不表示人工验收通过。所有 `human_status` 均保持 `pending`。

当前对抗审查后结论：`PARTIAL`。本 pack 只能继续作为 repo 内审查材料，不能进入 LifeAtlas 写入。

## 样本目的

### Elon

- 样本：`埃隆之书 ReaderLab Demo`
- 目的：证明低覆盖图书样本应先拆成目录地图和局部深读，不把局部处理包装成全书理解。
- 范围：只引用现有 demo 包、原 EPUB 和已完整处理的 `部件 II：极致艰苦工作`。
- 产物：
  - `elon/source-registry.v1.json`
  - `elon/location-map.v1.json`
  - `elon/catalog-map.v1.json`
  - `elon/part2-local-deepread.v1.json`
  - `elon/assertions.md`

### DBS

- 样本：`dbs-suite__v2.15.1_096f726`
- 目的：证明 Skill package 应使用 `capability-map.v1`，围绕能力域、触发信号、方法原子、输出契约、验收方式和读者路线进行审查。
- 范围：代表性 sample 级来源，覆盖 route-core、diagnosis-and-problem-framing、content-expression-and-publishing、state-and-content-engineering 四个能力域。
- 产物：
  - `dbs/source-registry.v1.json`
  - `dbs/location-map.v1.json`
  - `dbs/capability-map.v1.json`
  - `dbs/assertions.md`

DBS 口径是 sample-level：当前只登记 8 个 representative sources，并把四个能力域作为代表性样本，不代表 24 个 upstream Skills exhaustive 覆盖。

### 外部方法吸收证据

- `absorption-evidence.md`：记录 cangjie、book-to-skill、ljg-paper、qiaomu-read-helper、source-grounded、yao-meta-skill、CTK-MEM 分别借用什么、不借什么、已落地字段或流程，以及仍停留在设计层的部分。

## 如何验收

1. JSON 必须能被 `python3` 的 `json` 模块解析。
2. 检查所有契约都有 `schema`、`material`、`source_scope`、`confidence`、`review_items`、`machine_status`、`human_status`、`display`。
3. 检查 Elon 没有生成全书 grounded map 契约，也没有声称全书覆盖。
4. 检查 DBS 使用 `capability-map.v1`，没有套用图书式全局地图。
5. 检查所有 `human_status` 都是 `pending`。
6. 阅读 `assertions.md`，确认每条断言的 pass/partial/fail 和剩余风险。
7. DBS 写入 LifeAtlas 前必须先处理旧 `dbs-suite` 包中的 global-map/distillation full 冲突；这是 blocker，不是本轮新产物。

## 确定性验证命令

```bash
python3 scripts/readerlab_review_pack_validate.py
python3 scripts/readerlab_review_pack_validate.py docs/reports/readerlab-absorption-review-pack-v0
```

该命令只验证本 repo 内 review pack 的主要机器边界：固定文件清单存在、JSON 可解析、共享字段齐全、所有 `human_status` 保持 `pending`、没有新增 `readerlab.grounded-global-map.v1`、pack 内 `coverage_status` 不使用 `full`、source registry / location map 非空唯一且互相回链、contract refs 指向已登记 locations、Elon A05 局部提炼候选有主证据且不能只指向派生提炼页、DBS 能力地图保持 sample 口径，且结构化记录 24 Skills / cross_skill_routes / 旧 LifeAtlas global-map conflict blocker；其中 cross_skill_routes 必须非空、route_id 唯一，并回链到 capability_domains。`assertions.md` 必须逐 ID 状态符合预期。命令通过不代表人工阅读质量通过，也不代表可以写入 LifeAtlas。

## 当前汇总

| 样本 | pass | partial | fail | 结论 |
|---|---:|---:|---:|---|
| Elon | 6 | 1 | 0 | PARTIAL；`local-deepread.v1` 已补契约，A05 仍缺精确 EPUB span，不得写入 LifeAtlas。 |
| DBS | 3 | 4 | 0 | PARTIAL；sample-level 能力地图，不代表 24 Skills exhaustive，不得写入 LifeAtlas。 |

## Blockers Before LifeAtlas Write

- Elon：局部提炼项已有 reader-page item-level refs，但还不是精确 EPUB char span；不能把 A05 当 full pass。
- DBS：当前 pack 是 representative sample。必须补全 24 Skills 或明确保留 sample 口径，补 cross_skill_routes 真实路由证据，并处理旧 LifeAtlas `dbs-suite` global-map/distillation full 冲突后，才允许讨论写入 LifeAtlas。
- 本轮没有生成新的 `grounded-global-map.v1`；任何关于旧 global-map 的提法都只是 blocker 记录。
