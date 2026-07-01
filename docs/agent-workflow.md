# ReaderLab Agent Workflow

> Authority boundary: 本文件是半自动工作流设计说明，不是当前任务源。文中的“当前阶段 / 下一步”按设计语境理解；当前执行以 `docs/current-task.md` 为准。

## 目的

本文件定义 ReaderLab 半自动生成器前的工作流边界：哪些事情必须由脚本确定性完成，哪些事情允许 Agent 判断，哪些事情必须由 human / product owner 决定。

当前阶段仍不是完整生成器，不写 LifeAtlas 正式区，不自动进入人工验收通过状态。

## 三方边界

### Script

脚本只做确定性、可复验的工作：

- 读取已声明的文件路径和 contract JSON。
- 校验 `source-registry`、`location-map`、refs、reader/audit 分离、`machine_status` / `human_status` 边界。
- 从已存在的 contract JSON 和 `audit/source-excerpts` 渲染 Markdown 阅读页。
- 执行 `eval-rendered-package` 机器 gate。
- 按用户指定路径写 eval Markdown 报告。
- 默认拒绝覆盖已有 eval Markdown 报告；只有显式 `--overwrite-report` 才可替换。
- 拒绝把 eval Markdown 报告写入 `/Users/tianqiang/LifeAtlas`。

脚本不能做：

- 判断材料最终产品价值。
- 推断未声明来源。
- 把低覆盖样本升格为完整材料理解。
- 把 `human_status` 改成 accepted。
- 写 LifeAtlas 正式沉淀区。

### Agent

Agent 负责需要语义判断但仍可被 contract / eval 约束的步骤：

- 判断材料类型：书籍、长文、课程、访谈、代码文档、Skill 包、混合材料。
- 执行 E-R-D-D 判断：
  - Evidence：识别来源、覆盖范围、不能下结论的边界。
  - Route：拆阅读单元，区分主体、外壳、证据、实现细节和审计噪音。
  - Deepen：合成 deepread、误读防护、迁移候选和技术判断。
  - Decide：决定 promote / keep / downgrade / reject。
- 对工程材料生成 capability-map / design atoms。
- 对失败报告提出修复建议，例如补 source refs、降级过度主张、拆分 reader/audit 噪音。

Agent 不能做：

- 跳过 source registry / location map 直接写最终页。
- 用摘要替代一手正文。
- 把机器 gate 通过说成人工验收通过。
- 自行决定进入 LifeAtlas `300/600/800` 正式沉淀区。

### Human / Product Owner

人工只负责不可外包给机器的产品判断：

- 判断读者收益是否成立：是否真的降低理解成本，是否比直接读原文更有帮助。
- 判断品味和取舍：字段负担、页面节奏、旁批密度、是否啰嗦或过度工程化。
- 决定 `human_status=accepted` 是否成立。
- 决定是否进入 LifeAtlas 正式沉淀区。
- 决定是否扩大到第二类真实材料迁移测试或完整生成器开发。

## 阶段流程

### Stage 1：输入准备

输入：

- 原始材料或样本材料。
- 可读取的一手片段。
- 用户指定的临时输出路径。

输出：

- Agent 生成或修正的 `source-registry.v1`、`location-map.v1`。
- 明确 coverage status。

失败路径：

- 来源路径不存在：停止。
- 来源为空：停止。
- 覆盖范围不明：只允许输出结构诊断，不允许输出完整理解。

### Stage 2：语义建模

输入：

- source registry。
- location map。
- 一手正文片段。

输出：

- 长文 / 图书：`catalog-map`、`local-deepread`。
- Skill / 工程材料：`capability-map`、技术旁批候选。
- `rejected-downgraded.md`。
- `output-eval.v1`。

失败路径：

- 高层判断没有 refs：降级或拒绝。
- 技术洞察没有代价、边界或验证：降级为普通说明。
- AI 判断替代一手正文：失败。

### Stage 3：确定性渲染

输入：

- contract JSON。
- `audit/source-excerpts`。

脚本：

```bash
python3 scripts/readerlab.py render-contract-package <sample_dir> <output_dir>
```

输出：

- `reader/*.md`。
- 复制后的 `audit/`。

失败路径：

- 缺 source excerpt：失败。
- 空 source excerpt：失败。
- 缺可渲染 route contract：失败。
- 输出目录非空：失败，避免覆盖用户文件。

### Stage 4：机器评估与报告

输入：

- 渲染后的临时阅读包。
- 用户指定的报告路径。

脚本：

```bash
python3 scripts/readerlab.py eval-rendered-package <path> --report-md <report.md>
```

输出：

- JSON 结果。
- Markdown 报告，列出 target、`validate_contract_passed`、runner gates、failures、machine/human 边界。
- 默认不覆盖已有报告；如确需重写临时报告，使用 `--overwrite-report`。

失败路径：

- 报告路径已存在且未显式 `--overwrite-report`：失败。
- 报告路径位于 `/Users/tianqiang/LifeAtlas`：失败。
- `validate-contract` 失败：报告失败。
- reader markdown 缺失：报告失败。
- reader/audit 混淆：报告失败。
- 一手正文未进入 reader 页：报告失败。
- output-eval 9 gate 不全：报告失败。
- `human_status` 被机器改成 accepted：报告失败。

### Stage 5：人工审查

输入：

- 渲染后的 reader markdown。
- eval Markdown 报告。
- audit 层。

人工判断：

- 读者收益是否成立。
- 页面负担是否可接受。
- 哪些内容必须降级、删除、补证。
- 是否可以标为 `human_status=accepted`。

输出：

- human gate 结论：pending / accepted / rejected / needs_revision。
- 下一步：修复、第二类材料迁移测试、或进入半自动生成器开发。

失败路径：

- 读者收益不成立：回到 Stage 2。
- 字段负担过重：回到 Stage 2 或 Stage 3 调整展示层。
- 人工拒绝：不能进入正式沉淀。

## 当前最小闭环

当前已存在的最小闭环是：

```text
proof sample contracts
-> render-contract-package
-> validate-contract
-> eval-rendered-package --report-md
-> human gate pending
```

它只能证明当前两个 proof 样本的半自动前置链路可运行，不能证明完整生成器、真实材料迁移或人工验收已经完成。
