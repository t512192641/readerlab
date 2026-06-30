# dbs-good-question source notes

## Source registry

- source_id: dbs-good-question-skill-md
- material_type: Skill / engineering workflow
- source_path: `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-good-question/SKILL.md`
- source_role: complete primary source
- coverage: full
- source_line_count: 466
- sha256: `fb5629c1c7d86082f3152b1e5a5667f4dbc0071bfb9760a8bd1bf2f1b69dce89`

## Extraction and cleaning

- Read the complete `SKILL.md` file.
- Removed YAML/frontmatter wrapper lines 1-8 from the reader-facing净化正文.
- Reader净化正文 starts at source line 9 and preserves source heading order, examples, tables, output templates, constraints, language rule, and fallback route.
- No installation commands, package paths, hash values, machine status, source refs, or claim trace are shown in the reader page.
- AI high-level explanation and design asset cards are placed after the净化正文.

## Location refs

- L10: # dbs-good-question：好问题生成器
- L18: ## 核心哲学
- L20: ### 原则 1：好问题先钉现象
- L34: ### 原则 2：好问题要暴露冲突
- L45: ### 原则 3：Agent 需要约束场
- L55: ### 原则 4：自动化解决需要反馈回流
- L64: ### 原则 5：不要装确定
- L68: ### 原则 6：先给抓手，再做审计
- L76: ## 工作模式
- L78: ### 模式 A：用户给了模糊问题
- L87: ### 模式 B：用户给了现象和背景
- L93: ### 模式 C：用户问能否自动化解决
- L99: ### 模式 D：用户想要候选解释
- L107: ## 标准流程
- L109: ### Phase 1：识别输入类型
- L119: ### Phase 2：好问题五项检查
- L150: ### Phase 3：判断 Agent 可解性
- L170: ### Phase 4：改写成问题说明书
- L207: ### Phase 5：生成候选解释并批评
- L229: ### Phase 6：给下一步
- L241: ## 输出格式
- L243: ### 格式 A：默认输出
- L246: # 好问题拆解
- L248: ## 我看到的断点
- L255: ## 低置信候选解释
- L259: ## 半成品问题说明书
- L267: ## 先补这几个信息
- L273: ### 格式 B：严格问题质量审计
- L278: # 好问题诊断
- L280: ## 原问题
- L283: ## 当前评分
- L294: ## 最大缺口
- L297: ## 改写成好问题草案
- L300: ## 先补这几个信息
- L306: ### 格式 C：Agent 可解性判断
- L309: # Agent 可解性判断
- L311: ## 结论
- L314: ## 为什么
- L324: ## 可自动化部分
- L327: ## 需要人类介入的部分
- L330: ## 最小下一步
- L334: ### 格式 D：完整问题说明书
- L337: # 问题说明书
- L339: ## 我要分析的问题
- L342: ## 现象
- L345: ## 目标
- L348: ## 核心冲突
- L351: ## 背景事实
- L354: ## 约束
- L357: ## 反馈入口
- L360: ## 请 Agent 做
- L366: ### 格式 E：候选解释与批评
- L369: # 候选解释与批评
- L371: ## 当前问题
- L374: ## 候选解释
- L379: ## Hard to Vary 对比
- L383: ## 当前最强解释
- L386: ## 仍然不确定的地方
- L389: ## 最小验证动作
- L395: ## 典型场景
- L397: ### 场景 1：内容转化
- L408: ### 场景 2：内容到主页承接
- L419: ### 场景 3：商业问题
- L428: ### 场景 4：Agent 自动化
- L439: ## 说话风格
- L450: ## 语言
- L458: ## 不知道下一步用哪个 skill？

## Removed from reader and kept here

- Exact source path.
- YAML/frontmatter metadata boundary.
- Hash and audit status.
- Source line refs and claim trace.

### Removed frontmatter content

```yaml
name: dbs-good-question
description: |
  dontbesilent 好问题生成器。把模糊问题改写成 Agent 可推理、可批评、可验证的问题说明书，并判断它能被自动化解决到什么程度。
  触发方式：/dbs-good-question、/好问题、/问题说明书、/Agent可解性、「这个问题能不能自动化解决」「帮我把问题说清楚」
  Turn fuzzy problems into agent-solvable problem briefs and evaluate automation readiness.
  Trigger: /dbs-good-question, "clarify this problem", "can an agent solve this"
```

## Claim trace

| Reader claim | Source basis | Status |
|---|---|---|
| The Skill turns fuzzy problems into Agent-solvable problem briefs. | Frontmatter description and opening mission paragraph. | source-supported |
| The Skill prioritizes observable phenomena before explanation. | “原则 1：好问题先钉现象”. | source-supported |
| The Skill uses object, goal, conflict, constraint and feedback as quality checks. | “Phase 2：好问题五项检查”. | source-supported |
| The Skill judges automation readiness in A/B/C/D levels. | “Phase 3：判断 Agent 可解性”. | source-supported |
| The default interaction gives a grasp before strict audit. | “原则 6：先给抓手，再做审计” and 输出格式 A/B. | source-supported |
| Design asset cards identify reusable product patterns. | Codex technical-lead inference from the full Skill structure. | AI inference, unreviewed |

## Human / machine status

- machine_status: source_exists; complete_file_read; frontmatter_removed; reader_written; audit_written
- human_status: pending_reader_review

## Downgrade / refusal notes

- No claim is made that this is product ready.
- No claim is made that ReaderLab can automatically generate this page yet.
- No source package file, dependency, old demo, or LifeAtlas material was modified.
