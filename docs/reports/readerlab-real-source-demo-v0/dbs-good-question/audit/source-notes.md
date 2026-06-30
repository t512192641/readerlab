# dbs-good-question source notes

  ## Source registry

  - source_id: dbs-good-question-skill-md
  - material_type: Skill / engineering workflow
  - source_path: `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-good-question/SKILL.md`
  - source_role: complete primary source
  - coverage: full
  - source_line_count: 466

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

  ## What was used in reader

  - Full `SKILL.md` body was used.
  - Frontmatter lines 1-7 were not shown in reader because they are package metadata, but the trigger and description meaning were folded into the purified body.
  - The reader retained purpose, trigger signals, user intent, core philosophy, work modes, six-phase workflow, scoring rules, automation readiness levels, output contracts, typical scenarios, style constraints, language rule, and `/dbs` fallback.

  ## Removed from reader and kept here

  - Exact source path.
  - YAML/frontmatter wrapper.
  - Machine-facing metadata boundary markers.
  - Audit vocabulary such as source_id, coverage, machine_status, human_status.

  ## Claim trace

  | Reader claim | Source basis |
  |---|---|
  | The Skill turns fuzzy problems into Agent-solvable problem briefs. | Frontmatter description and opening mission paragraph. |
  | It prioritizes observable phenomena before explanation. | “原则 1：好问题先钉现象”. |
  | It uses object, goal, conflict, constraint and feedback as quality checks. | “Phase 2：好问题五项检查”. |
  | It judges automation readiness in A/B/C/D levels. | “Phase 3：判断 Agent 可解性”. |
  | It defaults to short output and expands strict audit only on request. | “输出格式” and “说话风格”. |

  ## Source-to-reader coverage map

  | Source section | Source lines | Reader section | Coverage judgment |
  |---|---:|---|---|
  | Frontmatter description and triggers | 1-7 | 净化正文第 1-2 段 | Trigger and purpose folded into reader language; YAML wrapper removed. |
  | Mission paragraph | 10-16 | 净化正文第 1、3 段 | Core user intent and reasoning constraint preserved. |
  | Six principles | 18-72 | 净化正文第 4-9 段 | Observable phenomenon, conflict, constraint field, feedback loop, uncertainty, and grab-first rule preserved. |
  | Four work modes | 76-103 | 净化正文第 10 段 | Mode distinctions preserved as reader-facing workflow explanation. |
  | Six-phase standard workflow | 107-235 | 净化正文第 11-16 段 | Input type, question checks, automation readiness, problem brief, candidate explanations, and next step preserved. |
  | Output formats A-E | 241-391 | 净化正文第 17 段 | Output contracts preserved in compressed reader language; exact templates not duplicated in reader. |
  | Typical scenarios | 395-435 | 净化正文第 18 段 | Content, homepage, business, and automation scenarios retained as use cases. |
  | Speaking style and language | 439-454 | 净化正文第 19 段 | Interaction style and language constraints retained. |
  | `/dbs` fallback | 458-466 | 净化正文第 19 段 | Fallback route preserved. |
  | Design implications inferred from full Skill | full file | 本模块讲解 / 设计资产卡 | AI technical-lead inference; not presented as verbatim author text. |

  ## Status

  - machine_status: source_exists; complete_file_read; demo_written
  - human_status: pending_reader_review

  ## Downgrade / refusal notes

  - No claim is made that this is product ready.
  - No claim is made that ReaderLab can automatically generate this page yet.
  - No package dependency, source package file, or LifeAtlas material was modified.
