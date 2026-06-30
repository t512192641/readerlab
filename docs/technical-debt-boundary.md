# ReaderLab 技术债边界

本文件记录 v0.4/v0.5 当前切片里，技术债 worker 对 `scripts/readerlab.py` 的检查结论。它不是新的产品路线图，也不是重构方案；用途是帮助主 Agent 验收哪些问题本轮已经收口，哪些必须等 `global-map.v1` / `distillation.v1` 契约稳定后再处理。

## 本轮已收口

- 新增 v0.4/v0.5 能力时，不再继续往 `scripts/readerlab.py` 增加 dbs、gstack 或 Elon Demo 专用常量。
- `delivery_status=deliverable` 继续只表示机器包可交付；人工阅读质量必须看 `human_status`，不能由 validate 绿灯替代。
- 页面清洗规则只视为 Skill 包执行壳清理工具，不能直接复用为书籍、长文、代码文档或混合材料的正文保留规则。
- 现有 dbs/gstack 样本逻辑作为 v0.1 历史过渡保留；本轮不再扩大样本专用规则的覆盖面。

## 本轮不做的修改

- 不拆分 `scripts/readerlab.py`。当前脚本同时承载导入、分组、页面生成、清洗、manifest、validate 和批注处理；直接拆分会和当前契约 worker 的 validate 改动产生冲突。
- 不迁移现有 `HUMAN_REVIEW_REGISTRY`、`READING_UNIT_CLASSIFIERS`、`TRIAL_SKILL_DESCRIPTIONS_ZH`、`COMPLETED_SKILL_TRANSLATIONS`。它们虽然有样本痕迹，但正在支撑既有 dbs/gstack 回归验证，移动成本高于本轮收益。
- 不调整 `reader_page_forbidden_terms` 或清洗正则。当前黑名单适合拦截后台信息进入 Skill 主阅读页，但一旦扩展到书籍/长文，可能误删来源编号、脚注、代码解释或材料原有结构。
- 不修改 `validate_pack` 的状态语义。C worker 正在处理契约与 validate，D 本轮只给风险边界，避免两边同时改同一段逻辑。

## 后续保留项

1. 契约稳定后，把材料类型显式纳入入口：Skill 包、书籍、长文、代码文档和混合材料应走不同的正文保留与清洗策略。
2. 把样本路由和人工验收 registry 从通用生成路径中分离出来，至少形成可替换的数据层，而不是继续扩展 Python 常量。
3. 拆分 validate：结构检查、来源覆盖检查、阅读页后台信息检查、人工状态检查、契约产物检查应有清晰边界。
4. 为 `global-map.v1` / `distillation.v1` 增加独立事实层校验后，再决定是否由生成器渲染 Markdown 展示页。

## 对 C worker 的风险提醒

- 新契约 validate 不应复用 `delivery_status=deliverable` 表示人工完成；建议继续保持机器状态和人工状态分离。
- `global-map.v1` / `distillation.v1` 的检查点应检查来源范围、置信度、待复核项和人工状态，不能只检查页面是否存在。
- 若 C 需要接入 `validate_pack`，建议先追加窄范围契约检查；不要顺手改页面清洗、dbs/gstack 路由或现有完成状态计算。
- 若 C 需要读取契约产物，建议先按文件存在和 schema 字段检查，不把 Elon Demo 或 dbs-suite 的特殊目录结构写成默认规则。
