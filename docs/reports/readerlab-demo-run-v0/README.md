# ReaderLab Demo Run v0

本目录是一个仓库内可打开查看的 ReaderLab demo run。它证明新流程不只停留在契约骨架：同一目录内同时有可验证的契约 JSON、机器断言说明，以及面向读者的中文 Markdown 样张。

它不是 LifeAtlas 正式写入，不修改 canonical package，不安装或启用 Skill，不新增依赖，也不表示人工验收通过。所有 `human_status` 均保持 `pending`。

## Demo 内容

### Elon

- 样本：`埃隆之书 ReaderLab Demo`
- 读者输出：`elon/reader-demo.md`
- 范围：只做 `部件 II：极致艰苦工作` 局部深读，来源范围是 `v101-13.xhtml` 到 `v101-18.xhtml`，不声称全书覆盖。
- 契约事实层：
  - `elon/source-registry.v1.json`
  - `elon/location-map.v1.json`
  - `elon/catalog-map.v1.json`
  - `elon/part2-local-deepread.v1.json`
  - `elon/assertions.md`

### DBS

- 样本：`dbs-suite__v2.15.1_096f726`
- 读者输出：`dbs/reader-demo.md`
- 范围：sample-level capability map，解释代表性能力域、触发信号、方法原子、输出契约、验收方式和跨 Skill 路由；不声称 24 Skills full coverage。
- 契约事实层：
  - `dbs/source-registry.v1.json`
  - `dbs/location-map.v1.json`
  - `dbs/capability-map.v1.json`
  - `dbs/assertions.md`

### 方法吸收证据

- `absorption-evidence.md` 记录外部方法如何被吸收到 ReaderLab 的字段、流程和 gate 中。它仍只是 repo 内设计与证据说明，不代表 LifeAtlas 样张合格。

## 如何验收

1. 打开 `elon/reader-demo.md` 和 `dbs/reader-demo.md`，确认它们是给读者看的中文输出，不是 JSON 契约复述。
2. 检查 reader demo 中的判断是否附有 `source/location refs`，并且没有越过已登记范围。
3. 运行确定性验证：

```bash
python3 scripts/readerlab_review_pack_validate.py docs/reports/readerlab-demo-run-v0
python3 tests/test_review_pack_validate.py
python3 tests/test_readerlab.py
```

验证通过只说明 repo 内 demo 的结构、引用链和已声明断言符合当前 gate；不说明人工阅读质量已接受。

## 当前断言汇总

| 样本 | pass | partial | fail | 结论 |
|---|---:|---:|---:|---|
| Elon | 6 | 1 | 0 | PARTIAL；有局部深读和读者 demo，但 A05 仍缺精确 EPUB char span。 |
| DBS | 3 | 4 | 0 | PARTIAL；有 sample-level 能力读者 demo，但不代表 24 Skills exhaustive coverage。 |

## Blockers Before LifeAtlas Write

- Elon：局部提炼项已有 reader-page item-level refs，但还不是精确 EPUB char span；不能把 A05 当 full pass。
- DBS：当前仍是 representative sample。必须补全 24 Skills 或明确保留 sample 口径，补 cross_skill_routes 真实路由证据，并处理旧 LifeAtlas `dbs-suite` global-map/distillation full 冲突后，才允许讨论写入 LifeAtlas。
- 本 demo 没有生成新的 `readerlab.grounded-global-map.v1`；任何旧 global-map 提法都只是 blocker 记录。
