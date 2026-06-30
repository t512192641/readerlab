# Source Notes

本页只服务审计和后续复核，不作为 reader-facing 主体。

## Source refs

| source_ref | 来源 | 角色 | 使用方式 |
| --- | --- | --- | --- |
| src-router | `docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample/audit/source-excerpts/module-router.md` | primary_module | 支撑任务路由模块的用途、触发条件、输出要求和越权边界。 |
| src-evidence | `docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample/audit/source-excerpts/module-evidence.md` | primary_module | 支撑证据边界模块的来源登记、覆盖范围和低覆盖限制。 |
| src-output-eval | `docs/reports/readerlab-contract-validator-proof-v0/skill-engineering-sample/audit/source-excerpts/module-eval.md` | primary_module | 支撑输出评估模块的 reader/audit 分离、正文保护、引用和状态边界。 |

## Location refs

| location_ref | source_ref | 原位置 | 支撑的 reader 内容 |
| --- | --- | --- | --- |
| loc-router-contract | src-router | paragraph 1 | 路由先识别材料类型和目标，选择下游路径，并不得执行下游任务。 |
| loc-evidence-boundary | src-evidence | paragraph 1 | 解释前记录来源范围、覆盖状态和位置引用；覆盖不足不能生成完整全局理解。 |
| loc-output-eval-status | src-output-eval | paragraph 1 | 输出评估检查 reader/audit 分离、正文未被摘要替代、引用具体、机器状态不冒充人工验收。 |

## Machine / human 状态

- machine_status：author_self_check_pass
- human_status：pending_reader_review
- coverage_status：sample
- review_scope：只覆盖三个工程模块的最小样章，不覆盖完整 ReaderLab 包。

## 降级 / 拒绝说明

- 拒绝生成完整全局讲解：当前只有三个小模块，不能冒充完整材料理解。
- 拒绝宣称 product ready：本样章只用于后续纯读者审查。
- 拒绝把机器检查说成人工验收：人工阅读质量尚未确认。
- 降级 capability-map：本轮不生成独立 JSON contract，只在 reader 页中展示设计资产卡，并在本审计页保留来源追溯。

## 被剥离内容

- 未把源文件路径放入 reader 主体，只在本页保留。
- 未把 machine_status、human_status、coverage_status 放入 reader 主体。
- 未把 source refs、location refs、claim trace 或 contract 字段作为 reader 主体内容。
- 参考样本未包含安装命令、hash 或调试日志；本轮没有编造这类内容。

## 自检

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skill/工程材料有净化正文 | PASS | reader 页第一节为净化正文，并保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点。 |
| reader-facing 与 audit 分离 | PASS | 内部 refs、状态和拒绝说明集中在本页。 |
| 高阶讲解成段服务理解 | PASS | 未拆成导读、旁批、误读提醒固定栏目。 |
| 技术负责人层输出设计资产卡 | PASS | 三张卡均包含适用场景、解决问题、原材料依据、可复用做法、使用前提、失败风险和什么时候不要用。 |
| 机器状态冒充人工验收 | PASS | 明确保留 pending_reader_review。 |
| 完整产品能力 | FAIL_BY_SCOPE | 当前范围不是 product ready，也不证明完整生成器能力。 |
