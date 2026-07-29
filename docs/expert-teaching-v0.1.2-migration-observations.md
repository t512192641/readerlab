# Expert Teaching Skill v0.1.2 两样本迁移验证 observation report

本报告只记录本轮预注册的 observation，不改变 Prompt、输入、语义产物、双门或终局。它不替代产品负责人对教学质量的接受判断。

## 1. source-access receipt

最终 receipt 均存在且可解析，均使用 `readerlab-book-expert-teaching/source-access/v1`、`provenance=agent_declared` 和 canonical `audit_scope`。

| 样本／角色 | 最终 opened URLs | 最终 cited-only URLs | 观察 |
|---|---:|---:|---|
| A Expert | 5 | 3 | receipt 完整；5 个 allowlisted 页面被声明打开，3 个 reference-only 页面只声明引用 |
| A Reviewer | 5 | 0 | receipt 完整；声明打开 A 的 5 个 allowlisted 页面 |
| B Expert | 0 | 1 | receipt 完整；Google Books 页面未被工具打开，作为 cited-only 保留 |
| B Reviewer | 0 | 0 | receipt 完整；没有外部网页访问声明 |

合规性观察不是“完全无人工介入”：A Expert 的 `audit_scope` 与 B Expert 的额外 `role`／`audit_scope` 在 seal 前被控制层按合同做了确定性 schema 规范化。该修正不触及语义内容，但说明首次 agent receipt 的原始填写不能直接视为合同级完整。

## 2. URL receipt closure

对教学稿和来源表中出现的 URL 做机械抽取，再与对应 receipt 合并集合比较，四个角色的缺失集合均为 `[]`：

| 样本／角色 | 教学稿／来源表观察 URL 数 | receipt 声明 URL 数 | receipt 缺失 |
|---|---:|---:|---|
| A Expert | 5 | 8 | `[]` |
| A Reviewer | 0 | 5 | `[]` |
| B Expert | 1 | 1 | `[]` |
| B Reviewer | 0 | 0 | `[]` |

因此，本轮未再次发现“稿／来源表出现 URL，但 receipt 中找不到”的问题。receipt 可以多于单一输出中实际出现的 URL，因为角色可声明其 allowlist 访问但未在该文件重复该 URL。

## 3. 名称、结构与知识形态

- 英文人名／理论名：机械检查未发现英文独立行或明显漂移。A、B 均在首次出现时使用中文名并附英文／原名；未发现同一理论在不同段落被改名的明显信号。
- T2.38 七段结构：机械检查未发现 `ReaderLab M1/M2/M3` 等固定标签；A 采用“概念区分—内部关系—证据—独立案例—回到原文—迁移—边界”，B 采用“问题—概念区分—循环关系—独立案例—回到原文—迁移—四层归属—误用边界”。两组标题树不同，未见机械复制 T2.38 七段结构的证据。
- 方法性／迁移性：两组都自然出现独立案例、回到原文后的新增解释和迁移段落。A 明确形成“迁移观察”与谈判／决策问题；B 形成“如何迁移到另一段材料”的问题序列与解释／评价边界。这是结构与内容观察，不是产品接受结论。
- 知识形态差异：A 输出围绕不可交易性、交换方式、反噬与谈判边界展开；B 输出围绕人造秩序、外在／内在现实、合法化、神圣终极参照和可信性结构展开。初步证据支持同一 Skill 没有把两者压成同一套表面机制。

## 4. 提问欲望

仅凭技术检查无法判断读者追问来自正常的深入空间，还是承重部分没有讲清；该项留给产品负责人在审阅入口中判断，当前状态为 `unknown`。本轮没有用一组样本的追问、观察或审核意见回灌另一组。

## 5. 终局边界

- A/B 技术终局均为 `SOURCE_FIDELITY_PASS + TEACHING_PASS`，均已 `PRODUCT_READY` 并 archive。
- observation 不产生 `EXPERT_ACCEPT`，不启动 Writer，也不授权修改 Skill。
- 产品负责人审阅完成前，产品价值与是否进入 Writer 均保持 `unknown`。
