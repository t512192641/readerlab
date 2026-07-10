---
name: readerlab-v3
description: Route a source-first ReaderLab V3 run through book or Skill protocols, isolated evidence, role-sized contracts, independent quality gates, and honest scope claims.
---

# ReaderLab V3

## 边界

这是 repo-local 草案，不得未经批准安装或复制到全局 Skill 目录。V3 只使用 Prompt / Markdown；不写生成用 Python，不改原始材料，不自动写入 LifeAtlas 正式登记簿。

五条总原则、两线专属规则和冲突优先级以 `v3/standards/constraint-architecture.md` 为唯一权威。本文件只负责运行声明、路由、最小上下文分发和停止闸门。

## 开始前必须声明运行模式

每次运行先复制 `v3/skill/templates/run-manifest.md`，在读取生成产物前填好 `run_id`、模式、原始来源、样本确认、任务上限和新输出目录。

### Fresh run

- 用途：验证当前流程能否从登记的原始材料独立工作。
- 必须重新读取原始来源，重新执行声明范围内的正文/source map、识别、候选、核查、裁判、装配和验收。
- 旧 URL 只能作定位线索；旧净化正文、source map、候选、audit、reader page、资产卡和复现结果不得作为输入。
- 使用全新唯一输出目录；`reused_generated_artifacts` 必须为 `none`。

### Revision run

- 用途：修补已有产物的明确局部问题，不验证从零运行。
- 必须声明复用基线、实际重跑阶段、未重跑阶段和不可声称范围。
- 只能声称实际局部修订及对应检查通过，不能升级为完整流程通过。

## 必需输入

- 原始材料路径、材料类型和本次实际读取范围。
- `fresh | revision` 运行模式与新输出目录。
- 样本是否已由用户或当前权威文件固定；若选择会影响结论，先停下请用户确认。
- 已确认可用的资产层登记簿只读路径；生成期间不得回写。
- 本次任务数上限和需要通过的独立验收门。

## 路由与最小上下文

主控读取：

- `v3/standards/constraint-architecture.md`
- 本次 run manifest
- `v3/skill/protocols/judge.md`
- `v3/skill/roles/orchestrator.md`

图书或长文的主控 / 线路编排只追加：

- `v3/skill/protocols/book-engine.md`

Skill 或工程材料的主控 / 线路编排只追加：

- `v3/skill/protocols/skill-engine.md`

单个执行 Agent 只接收：主控提供的本线路两条专属规则摘录、`v3/skill/roles/` 下自己的合同、完成任务所需输入，以及该角色确需填写的模板。它不读取整份线路协议。

只有裁判或回归执行者可按 case 读取 `v3/standards/regression-suite.md` 及其证据。普通作者、成文者和冷读者不得加载历史病历、另一条线路协议或完整生产日志。

## 调度与成本

- 图书标准章的无早停计划为 11 个 Agent 任务；合法 0 候选会跳过无输入任务，`actual_tasks` 不凑数。短文 5—7，深读档 15—18；Skill 标准为 5 个任务，简单材料可降为 3—4。
- 正文整理、最终成文和冷读是低分歧任务，不增加投票 Agent。
- 图书盲区检查并入认知裁判，不另计任务；扩容仅因首轮认知皆普通、事实冲突会改变结论、裁判发现关键遗漏、Skill 需要额外事实核查或用户明确要求。
- 未经用户同意不得突破 manifest 声明的任务上限。

## 运行顺序

1. 主控验证原始来源、模式、输出隔离、样本确认和任务预算。
2. 按材料类型分发线路规则摘录和单个角色合同，不把全套规则塞给所有执行者。
3. 证据产物只写本次 run 的 audit / contracts / eval 目录；读者页只从已通过项目装配。
4. 依次执行事实、绝对价值、读者理解、冷启动/复现和运行完整性中适用的独立门。
5. 在 manifest 逐项记录实际执行、跳过、复用、验证结果、可声称和不可声称。
6. 等用户确认后，才可写回任何耐久资产或进入下一阶段。

## 输出边界

- 图书页：完整正文，以及 0 个或多个通过绝对价值门的单认知陪读单元；不得用数量或固定槽位逼迫上页。
- Skill 主读页：可追溯净化正文；产品/技术解释不得混入正文。
- 技术负责人页：机制、取舍、失败与迁移边界；不复制主读页摘要。
- audit：source map、候选、事实、裁判、回归、冷读、运行与复用证据。
- 沉淀只产生候选；未经用户确认不得成为正式资产。

## 完成声明

报告必须分开列出：真实读取的输入、实际执行阶段、通过的门、复用内容、未执行/失败项、待用户验收项。机器检查、局部页、资产卡冷启动或 revision 都不能升级为完整 ReaderLab 流程通过。

## 停止条件

遇到以下任一项，停止并报告：

- 原始来源或 source map 无法确认；fresh 将复用旧生成产物或污染旧输出。
- 样本选择会改变结论但尚未获用户确认。
- 事实冲突会改变可见判断；锁定正例与硬负例无法同时守住。
- 任务预算需超限，或只能靠继续堆禁令维持协议。
- 读者页将泄漏 audit，或局部结果将被扩大成完整流程声明。
- 准备生成真实内容、进入下一 Phase 或写回 LifeAtlas，但用户尚未批准。
