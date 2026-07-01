# ReaderLab Eval Gates

## 目的

ReaderLab 的评估目标不是证明文件存在，而是证明最终读者产物更适合阅读、批注、讨论和沉淀。

## 功能验收

一个最小 ReaderLab 包必须满足：

```text
[ ] 有 source-registry.json
[ ] 有 location-map.json
[ ] 每个高层判断有 source refs
[ ] coverage 状态明确：toc_only / partial / sample / full / unknown
[ ] machine_status 和 human_status 分开
[ ] reader-facing 和 internal audit 分开
[ ] 一手正文没有被摘要、导读或 AI 解释替代
[ ] 书籍/长文过 Body Track Gate：阅读页内存在完整正文，且陪读不能替代正文
[ ] 高阶讲解通过和阅读包通过状态分开
[ ] claim ledger 区分 direct_source_claim / composite_interpretation / external_analogy / needs_verification
[ ] candidate tournament 有真实 promote / keep / downgrade / reject 决策
[ ] Skillization Gate 没有把普通 insight 过早 Skill 化
[ ] annotation triggers 都有 body-adjacent anchor
[ ] Skill/工程材料有 capability-map
[ ] 技术材料有 design atom analysis 和设计资产提炼
[ ] 有 rejected / downgraded 清单
[ ] 有 output-eval
```

## 输出契约验收

不同材料类型必须先满足各自正文契约：

```text
[ ] 书籍/长文保留原样正文和章节顺序
[ ] 书籍/长文没有被 AI 压缩、改写、重述或导读替代，除非用户明确要求
[ ] 书籍/长文页面若无完整正文，只能标为 `high_order_explanation_pass`，不能标为 `reader_package_pass`
[ ] Skill/工程材料有净化正文
[ ] 净化正文保留用途、触发条件、用户意图、核心流程、约束、失败条件、输出要求和设计亮点
[ ] 安装命令、重复模板、执行外壳、机器状态、路径、hash、调试信息进入 audit、附录或技术负责人解析
[ ] 高阶讲解用成段语言服务材料理解，不把正文切成固定栏目墙
[ ] 高阶讲解提供非摘要型认知增量：能用全局视角、跨学科模型、历史 / 商业 / 组织 / 工程经验或用户既往经历照亮材料
[ ] 高阶讲解区分原文依据、AI 解释重组、外部类比和待验证判断
[ ] 技术负责人层输出设计资产卡
[ ] reader-facing 页不把 source refs、location map、claim trace、machine/human 状态、降级/拒绝记录当主内容
```

## 阅读质量验收

读者打开包后，应能在 3 分钟内回答：

```text
这份材料解决什么问题？
这本书/这组材料整体在讲什么？
当前这一章/模块讲什么？
它为什么出现在全文/全包的这个位置？
它承接前面什么，又为后面什么服务？
哪些部分是主干，哪些只是外壳、案例、背景或审计？
AI 建议我重点注意什么？
为什么这些点值得注意？
哪些判断有原文依据？
哪些只是 AI 推断？
```

读者页还必须满足：

- 不把内部 `source refs`、claim trace、machine/human 状态暴露为主要阅读内容。
- 不把“降级/拒绝理由”整段塞进正文；读者只需要自然语言误读提醒。
- 不用 AI 重述冒充一手正文。
- 书籍/长文默认必须保留原文正文和章节顺序；除非用户明确要求整理原文，否则只允许做空格、空行、断行等轻量排版清理。
- Skill/工程材料必须提供净化正文：剥离安装命令、重复模板、执行外壳和机器噪音，但保留用途、触发条件、用户意图、核心流程、约束、失败条件、输出要求和设计亮点。
- 页面读起来应像给人介绍和陪读一本书，而不是 contract 审计报告。
- AI 高阶讲解应成段讲透材料，不应把同一段内容切成过多固定栏目。
- AI 高阶讲解不能停在“本章讲了什么”。它必须帮助读者重新看待材料：指出更大的问题结构、可迁移的底层逻辑、跨领域同构关系、必要边界和误用风险。
- 旁征博引必须反向服务正文理解；如果只是堆模型、堆名人、堆历史例子，视为 FAIL。

## 深读质量验收

每个 deepread card 必须回答：

```text
这个点是什么？
为什么它对理解材料重要？
它的原文依据在哪里？
它的机制链是什么？
有什么案例？
有什么反例或边界？
它有什么迁移价值？
V1 / V2 / V3 是否通过？
它和哪些其他学科、历史结构、产品/组织/工程经验存在同构关系？
这些连接哪些来自原文，哪些是 AI 的解释性重组？
```

如果不能回答，就不能升格为 deepread card，只能保留在正文、降级到背景或进入审计拒绝清单。

## 高阶讲解 Delta Eval

每个高阶讲解必须证明它不是普通总结。机器 eval 可以检查结构存在，人工 eval 必须判断读者是否获得认知增量。

最低 8 问：

```text
[ ] 这段讲解是否把章节主题升级成了一个更大的问题？
[ ] 是否给出了正文内部的机制链，而不是只列重点？
[ ] 是否明确说出普通读者最容易读浅在哪里？
[ ] 是否至少有一个镜头真正照亮正文？
[ ] 外部模型 / 类比是否能反向解释正文，而不是并列摆放？
[ ] 是否明确区分原文支持、AI 解释、外部类比和待验证判断？
[ ] 是否完成吸收 / 降级 / 拒绝，而不是只说“有启发”？
[ ] 和 baseline summary 相比，是否让读者产生“原来这章可以这样看”的认知增量？
```

高阶讲解 reader-facing 通过标准：

- 新版与 baseline summary 对照，必须明显增加问题框架、机制、镜头、边界或裁决。
- 如果做 blind A/B，新版至少应在“更像见识丰富的人陪读、重新理解材料、区分可学/降级/不可照搬、受正文约束、少像报告”五项中赢四项。
- 外部模型、历史案例、名人观点和跨学科类比只有在反向照亮正文时才能进入读者页。
- 即使高阶讲解通过，只要没有完整一手正文轨，也不能称为 ReaderLab 阅读包通过。

### 读者 12 分验收

章节级高阶讲解还必须使用读者 12 分 rubric。先过硬门槛，任一失败则不能 `pass`：

- 一手正文没有被 AI 讲解替代。
- reader-facing 页面不暴露 `source refs`、`claim trace`、`lens score`、`machine/human status` 等内部字段。
- 有明确升维问题，不是章节摘要。
- 有正文内部机制链。
- 至少一个镜头反向照亮正文，不抢正文。
- 自然完成吸收 / 降级 / 拒绝。
- 不美化长工时、创伤、强控制或英雄崇拜。
- 不把局部章节升格成全书结论。

六项读者评分每项 0-2 分，满分 12：

| 维度 | 2 分 | 1 分 | 0 分 |
|---|---|---|---|
| 重新理解 | 读完产生“原来这章可以这样看” | 有新说法但不稳定 | 只是复述 |
| 正文贴合 | 关键判断能回到正文场景 | 部分贴合 | 脱离正文 |
| 机制清晰 | 能串起因果链 | 有链条但松散 | 只列重点 |
| 镜头有效 | 镜头反向解释正文 | 镜头有启发但偏装饰 | 镜头抢戏或无效 |
| 边界锋利 | 清楚区分可吸收/需降级/必须拒绝 | 有边界但模糊 | 全部泛化 |
| 表达穿透 | 像见识丰富的人陪读 | 像较好的报告 | 像普通总结 |

通过线：硬门槛全过，读者分至少 `10/12`，读者评价 agent 给出 `pass`，且没有 P0/P1 问题。

`Lens Auction` 的 `>= 7` 是内部镜头筛选分；读者 12 分是最终阅读验收分。两套分数不能混用。

## 技术负责人 / 设计资产验收

每个技术洞察必须回答：

```text
这个设计解决什么问题？
它为什么放在这里？
它约束了什么行为？
它防止了什么失败？
它带来什么代价？
它能否迁移？
什么时候不要用？
它是原文显性说明，还是 AI 工程推断？
```

不满足这些问题，就不是技术洞察，只是复述。

对 Skill 包、代码文档、Agent 工作流和工程资料，还必须面向产品负责人回答：

```text
这个设计模式适合什么场景？
它可以沉淀成什么卡片？
下次遇到什么问题可以调出来复用？
复用时最容易错在哪里？
什么时候不要用？
```

## Output Eval

每轮样本 eval 至少检查：

- reader-facing 是否混入 audit 噪音。
- audit 是否保留足够来源证据。
- 一手正文是否被 AI 摘要替代。
- AI 陪读是否降低理解成本。
- 高价值细节是否保留。
- source refs 是否具体。
- 技术设计洞察是否非泛泛。
- 过度升格是否被降级。
- machine_status 是否冒充 human_status。

## 失败条件

出现以下任一情况，本轮失败：

```text
[FAIL] 主阅读页变成普通摘要。
[FAIL] AI 重点替代了一手正文。
[FAIL] 书籍/长文阅读页没有完整一手正文，却标为 reader_package_pass。
[FAIL] 用“讲解贴合正文锚点”替代“一手正文存在”。
[FAIL] candidate_pool 只有字段，没有真实影响 promote / downgrade / reject。
[FAIL] 没有 rejected / downgraded 项却声称完成候选筛选。
[FAIL] 高层判断没有 claim tier。
[FAIL] composite_interpretation 被写成作者原意。
[FAIL] insight 不满足 trigger / input / steps / output / boundary / evidence 却被 Skill 化。
[FAIL] annotation question 没有 body-adjacent anchor。
[FAIL] reader-facing narrative 没有消费 gate 输出，而是自由发挥。
[FAIL] 高阶讲解只比 baseline summary 更流畅，但没有问题框架、机制链、镜头、边界或裁决。
[FAIL] 高阶讲解没有把章节主题升级成更大的问题。
[FAIL] 高阶讲解没有正文内部机制链。
[FAIL] 高阶讲解的跨学科镜头不能反向照亮正文。
[FAIL] 高阶讲解没有吸收 / 降级 / 拒绝。
[FAIL] 书籍/长文正文被 AI 压缩、改写或导读替代，且没有用户明确要求。
[FAIL] Skill/工程材料只做摘要，没有净化正文。
[FAIL] 没有 source refs 却写全局判断。
[FAIL] 低覆盖材料冒充完整全书理解。
[FAIL] Skill 包 capability-map 只是目录列表。
[FAIL] 技术洞察全是正面夸奖，没有代价和边界。
[FAIL] 技术负责人层只解释术语或实现，没有沉淀产品负责人可复用的设计资产。
[FAIL] 把命令行、安装步骤、模板噪音当主体内容。
[FAIL] 把局部案例升格为全书原则。
[FAIL] 把 AI 推断写成作者原意。
[FAIL] validator 通过被当成人工验收通过。
[FAIL] 读者页主要呈现内部 refs、审计字段或机器状态。
[FAIL] “阅读路线/主题线索”等内部分析词替代了清楚的全书/章节方位说明。
```

## 状态用语

- `machine_validated`：工具检查通过。
- `ready_for_human_review`：可供人工阅读验收。
- `human_accepted`：人工确认通过。
- `high_order_explanation_pass`：reader-facing 高阶讲解通过；不等于阅读包通过。
- `reader_package_pass`：完整阅读包通过；书籍/长文必须先过 Body Track Gate。
- `method_kernel_probe_pass`：受限样本上的方法核探针通过；不等于可迁移方法核完成。
- `reader_package_not_verified`：阅读包未验证，不能用通过章节讲解代替。
- `product_ready`：只有完整流程、样本、验收和风险闭环都成立时才能使用。
