# ReaderLab 可复用研究索引

## 2026-07-26：开放世界认知发现的相邻方法

来源底稿：
`/Users/tianqiang/Downloads/readerlab-gpt-pro-core-brief-v3-20260726.md` 的 F 节。以下只记录可复用
索引；本轮未重新核对论文正文，也没有据此完成 ReaderLab 选型或验证。

- [STORM／Co-STORM](https://aclanthology.org/2024.emnlp-main.554/)：可借鉴多视角检索、主持与
  动态概念图来暴露“未知未知”；即时角色不等于稳定、可追溯认知库存。
- [文献发现 ABC 模型](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215313)：
  可借鉴中间桥梁连接分离知识域；简单共现会制造大量牵强关系。
- [Expert Finding](https://krisztianbalog.com/files/sigir2006-expertsearch.pdf)、
  [Step-Back Prompting](https://arxiv.org/abs/2310.06117) 与
  [HyDE](https://arxiv.org/abs/2212.10496)：可借鉴从问题抽象、资料和作者关系发现候选；主题
  相关或生成的中间查询都不能代替真实框架与材料连接。
- [xQuAD](https://terrierteam.dcs.gla.ac.uk/publications/ecir2010_rodrygo_div.pdf)／MMR：
  可借鉴候选去同质化；多样性本身不证明认知价值。
- [AnyTool](https://arxiv.org/abs/2402.04253)／
  [SkillRouter](https://arxiv.org/abs/2603.22455)：可借鉴大规模已知能力库的路由，以及“完整
  能力正文优于名称简介”的结论；ReaderLab 的认知对象比工具功能更模糊。
- [R³AG](https://aclanthology.org/2026.acl-long.939/)／DyLAN：可借鉴以下游真实效果判断路由；
  其客观答案与预设候选池前提不能直接搬到主观阅读价值判断。
- [GraphRAG](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/)：
  可借鉴已有语料的实体、关系和主题社区地图；索引成本与封闭语料边界仍在。

共同边界：这些方法分别缓解未知问题发现、远距连接、专家检索、查询扩展、候选多样化、能力路由
或语料建图，没有一种单独证明能够完成 ReaderLab 所需的“真实稳定框架发现 + 忠实恢复 + 自然
连接 + 人类可读陪读”。组合方式、离线库存与实时发现的分工仍为 `unknown`。
