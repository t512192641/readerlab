# Source Alignment

## Source Registry

| source_id | source_path | extraction boundary |
|---|---|---|
| `elon-epub-original` | `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub` | 本轮直接读取本地 EPUB；复用 `readerlab-elon-full-product-v0` 的 location ids；未联网，未新增依赖。 |

## Covered Unit

| unit | EPUB spine | reused location refs |
|---|---|---|
| 第二部分“极限硬核工作” | title boundary `spine-015 / v101-13.xhtml`; source-card coverage `spine-016` to `spine-020` / `v101-14.xhtml` to `v101-18.xhtml` | `loc-responsibility`, `loc-deep-understanding`, `loc-team-goal`, `loc-org-barrier`, `loc-org-communication`, `loc-algorithm-way`, `loc-urgency-speed`, `loc-parallel-processing`, `loc-factory-as-product`, `loc-manufacturing-bottleneck`, `loc-manufacturing-moat` |

## Location Refs

| location_id | EPUB spine / file | heading path | short excerpt | supports |
|---|---|---|---|---|
| `loc-responsibility` | `spine-016 / v101-14.xhtml` | `成功之道 / 承担责任` | “最棘手的问题” | CEO 责任不是职位奖励，而是难题入口。 |
| `loc-deep-understanding` | `spine-016 / v101-14.xhtml` | `成功之道 / 掌握深度理解` | “工程决策与支出决策” | 深度理解要求工程、成本、产品判断闭环。 |
| `loc-factory-floor` | `spine-016 / v101-14.xhtml` | `成功之道 / 睡在工厂车间` | “紧急状态” | 危机强度只能作为边界案例，不能常态化。 |
| `loc-team-goal` | `spine-017 / v101-15.xhtml` | `打造卓越团队 / 目标导向的团队` | “共同目标” | 公司是一群人围绕目标创造产品或服务。 |
| `loc-org-barrier` | `spine-018 / v101-16.xhtml` | `组织设计 / 破除组织壁垒` | “组织边界的痕迹” | 组织边界可能物化为产品冗余。 |
| `loc-org-communication` | `spine-018 / v101-16.xhtml` | `组织设计 / 简化沟通` | “最短路径” | 问题应沿最短路径流向能解决它的人。 |
| `loc-algorithm-way` | `spine-018 / v101-16.xhtml` | `组织设计 / 算法之道` | “顺序至关重要” | 先质疑、删除，再简化、加速、自动化。 |
| `loc-urgency-speed` | `spine-019 / v101-17.xhtml` | `极致紧迫感 / 速度即是最强攻防` | “时间才是” | 速度/紧迫性是组织攻防能力，不是情绪化催促。 |
| `loc-parallel-processing` | `spine-019 / v101-17.xhtml` | `极致紧迫感 / 并行处理` | “并行推进” | 并行推进用于压缩复杂任务周期，PayPal 并行系统例子归入此 ref。 |
| `loc-factory-as-product` | `spine-020 / v101-18.xhtml` | `我们必须实干制造 / 工厂即产品` | “工厂本身” | 工厂/生产系统是产品能力的一部分。 |
| `loc-manufacturing-bottleneck` | `spine-020 / v101-18.xhtml` | `我们必须实干制造 / 攻克瓶颈` | “关键瓶颈” | 量产速率受最慢、最不稳定环节限制。 |
| `loc-manufacturing-moat` | `spine-020 / v101-18.xhtml` | `我们必须实干制造 / 制造即护城河` | “规模经济与技术” | 制造竞争力来自规模和技术同时最大化。 |

## High-Level Claim Trace

| claim | reader location | required refs | status |
|---|---|---|---|
| “硬核工作不是单纯拼命，而是难题执行系统。” | `reader/01_大单元深读.md` | `loc-responsibility`, `loc-deep-understanding`, `loc-team-goal`, `loc-org-barrier`, `loc-org-communication`, `loc-algorithm-way`, `loc-urgency-speed`, `loc-parallel-processing`, `loc-factory-as-product` | supported_for_demo |
| “危机强度不能常态化。” | `reader/00_全书地图.md`, `reader/01_大单元深读.md` | `loc-factory-floor` | supported_as_boundary |
| “组织边界会进入产品。” | `reader/01_大单元深读.md` | `loc-org-barrier` | supported_for_demo |
| “问题应沿最短路径抵达能解决的人。” | `reader/01_大单元深读.md` | `loc-org-communication` | supported_for_demo |
| “算法之道的关键是顺序，而不是自动化。” | `reader/01_大单元深读.md` | `loc-algorithm-way` | supported_for_demo |
| “并行推进可以压缩不可串行等待的复杂任务周期。” | `reader/01_大单元深读.md` | `loc-parallel-processing` | supported_for_demo |
| “制造系统是产品的一部分。” | `reader/00_全书地图.md`, `reader/01_大单元深读.md` | `loc-factory-as-product`, `loc-manufacturing-bottleneck`, `loc-manufacturing-moat` | supported_for_demo |
| “ReaderLab 不能先造自动化再证明样张质量。” | `reader/01_大单元深读.md` | `loc-algorithm-way` as analogy; project state docs as product boundary | interpretive_transfer_pending |

## Known Boundaries

- 短 excerpt 只用于定位，不承担完整原文展示职责。
- `char_range` 沿用旧 `location-map.v1.json` 的 cleaned XHTML 文本偏移，本轮没有重新生成 contract JSON。
- `spine-015 / v101-13.xhtml` 只作为“第二部分”标题边界；本轮没有从标题页制造 source card。
- 本轮只覆盖一个大单元；全书地图使用旧 full-product-v0 的全书 refs 作为结构边界，不声称全书 reader 包完成。
- `interpretive_transfer_pending` 表示迁移洞察需要人工判断，不能直接升格为产品结论。
