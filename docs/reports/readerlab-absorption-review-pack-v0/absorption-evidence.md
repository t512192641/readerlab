# Absorption Evidence

本表记录外部方法如何被 ReaderLab 吸收。它只证明 repo 内设计吸收，不证明 LifeAtlas 样张合格，也不表示任何 `human_status` 已通过。

| 外部方法 | 借什么 | 不借什么 | 已落地到哪个字段或流程 | 仍停留在设计层 |
|---|---|---|---|---|
| cangjie | 多视角读后提炼：框架、原则、案例、反例、术语、可迁移方法原子；强调提炼前要有材料证据。 | 不直接把局部读后提炼升级成 Skill；不照搬三重验证为 ReaderLab 默认流程；不让提炼页替代第一次阅读正文。 | Elon `local_deepread.distillation_candidates`、`claim_refs`、`applicability_boundary`、`misread_guards`；A05 要求 source refs 和适用边界。 | 精确 EPUB span、人工三重验证、候选 Skill 晋级流程仍未实现。 |
| book-to-skill | 从书籍中抽取可复用方法时，先区分章节主线、可迁移原则和应用边界。 | 不把任何书籍章节自动转成可启用 Skill；不把传记语境中的个人风格当通用方法。 | Elon `catalog-map.v1` 区分 route hypothesis / covered units；`local-deepread.v1` 只允许局部提炼候选。 | 从 full-book coverage 到正式 Skill 草案的门槛仍未定义为工具化流程。 |
| ljg-paper | 把复杂材料拆成问题、结构、论点、证据和可复核结论。 | 不采用论文式长篇综述作为默认读者页；不牺牲 Obsidian 附近批注体验。 | `readerlab-output-eval-v0.md` 的可检查断言；契约中的 `confidence`、`review_items`、`claim_refs`。 | 尚未形成自动评分器或 blind review 表单。 |
| qiaomu-read-helper | 面向读者路线：先读什么、如何分层、哪些内容只是路线假设。 | 不引入额外阅读系统或新插件；不把助手建议当人工阅读判断。 | Elon `catalog.route_hypothesis`、`known_covered_units`、`not_yet_covered_units`；DBS `reader_routes`。 | 真实读者试读反馈和批注响应闭环仍待验证。 |
| source-grounded | 每个地图、能力判断和提炼项都要能回到 source registry / location map / item-level refs。 | 不接受无来源精华、包级模糊引用或派生页主证据；不把 validate 通过当阅读质量通过。 | `source-registry.v1`、`location-map.v1`、`claim_refs.primary_location_refs`、coverage status 规则；DBS sample/full 边界。 | 精确 char offsets、EPUB span validator、source ref 自动交叉检查尚未实现。 |
| yao-meta-skill | Skill 工程化方法：瘦入口、资源分层、output eval、risk/gate、review pack。 | 不把 yao-meta-skill 当读书方法本体；不把 ReaderLab 变成 Skill 专项。 | `readerlab-skill-ir-v0.md`、`readerlab-output-eval-v0.md`、本 review pack 的 assertions 和 blockers。 | 正式 ReaderLab Skill 包、provider-backed eval、gate runner 还未落地。 |
| CTK-MEM | CTK 提供任务边界、执行契约和验收；MEM 提供 current task / dev state / decisions / ledger 的状态层分工。 | 不把 CTK/MEM 文档直接复制进读者包；不让流程治理污染主阅读页。 | `docs/current-task.md`、`docs/dev-state.md`、`docs/decisions.md`、`docs/agent-run-ledger.md` 的项目状态分层；review pack 中的 pass/partial/fail 和 blocker 口径。 | 面向 ReaderLab worker 的自动派发、统一 completion review、阶段性 memory cleanup 仍是人工流程。 |

## 当前吸收结论

- 已落地的是方法边界和事实字段，不是正式 LifeAtlas 内容。
- Elon 的主要进展是把局部深读契约化，并把提炼项主证据从派生提炼页退回到 part II reader page 原文行段。
- DBS 的主要修复是把能力地图降回 representative sample，并把 24 Skills、cross_skill_routes、旧 LifeAtlas full 冲突列为 blocker。
