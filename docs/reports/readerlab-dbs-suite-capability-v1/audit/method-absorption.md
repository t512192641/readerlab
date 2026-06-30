# 方法吸收审计

## 吸收结论

这版不是把 `dbs-suite` 再写成一篇包介绍，而是把 ReaderLab 现有方法层落到能力地图合同里：

| 方法来源 | v1 吸收点 | 落点 | 避免的问题 |
|---|---|---|---|
| ReaderLab `capability-map.v1` | 能力域必须有 owned_job、trigger、exclusion、method atom、input、output、verification、route decision、source refs | `contracts/capability-map.v1.json` | Skill 名字和目录分组冒充能力地图 |
| ReaderLab source/location 纪律 | 每个 Skill 至少一个可回链来源和位置 | `source-registry.v1.json`, `location-map.v1.json` | 高层能力判断无证据 |
| ReaderLab reader/audit 分离 | 读者稿只解释怎么选择和验收能力；审计信息进 audit/contracts | `reader/01_能力地图.md`, `audit/90_来源与审计.md` | 读者页混入内部状态和 validator 细节 |
| `yao-meta-skill` Skill IR 方法 | recurring job、trigger、not-trigger、near-neighbor、resources、eval/gate | 能力域字段和 route conflicts | 只写功能说明，不写边界 |
| `yao-meta-skill` output eval 方法 | baseline vs with-ReaderLab、可检查断言、禁止 false pass | `assertions.md` 的 DBS-A01..A11 | 文件存在或 sample 绿灯冒充质量提升 |
| 旧负面 baseline | sample 不能冒充 full；目录不能冒充 route | `coverage_plan` 和 `cross_skill_routes` | 7 个代表样本冒充 24 Skill full map |

## 和 v0 的关键差异

1. v0 demo 只覆盖 7 个代表位置；v1 覆盖 24 个 upstream `SKILL.md`。
2. v0 主要证明 contract shape；v1 把能力域、inventory units、route decisions、cross_skill_routes 和 reader_routes 组合起来。
3. v0 读者路线仍偏“读几个域”；v1 改成真实任务选择路线和输出验收路线。
4. v0 把 `dbs-content-system` 工具完整性作为 review item；v1 继续保留该边界，没有把辅助工具存在说成执行通过。
5. v1 仍保持人工 `pending`，不把 JSON 可解析或测试通过说成 product ready。

## 仍未吸收完成的部分

- 真实任务反测还没跑：尤其 `dbs-diagnosis` / `dbs-good-question` / `dbs-goal` / `dbs-action`，以及 `dbs-content` / `dbs-resonate` / `dbs-spread` / `dbs-hook` / `dbs-xhs-title` 的边界。
- 辅助资产未执行审计：`dbs-content-system/tools` 和 `dbs-wechat-html/templates/styles.md` 需要单独 runner 或人工验收。
- 这仍是手工试产包，不是 ReaderLab 生成器能力证明。
