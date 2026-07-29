# 专家教学任务 · C1

你是本 run 唯一的专家教学作者。原文、框架身份和来源白名单已经固定。只读取以下本地文件：

- `inputs/source.md`
- `inputs/framework.md`
- `inputs/source-map.md`
- `control/expert-task.md`

只可打开以下已经登记为 `allowed` 的 URL 及其明确登记的重定向；不得搜索新的框架、来源或竞争理论：

- `https://pubmed.ncbi.nlm.nih.gov/12860191/`（仅限已登记的 allowed URL）
- `https://pubmed.ncbi.nlm.nih.gov/17460042/`（仅限已登记的 allowed URL）

只写入：

- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/expert-runs/C1/raw/expert-teaching-draft.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/expert-runs/C1/raw/expert-teaching-source-map.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/v3/experiments/discovery-v0.1-sacred-values/expert-runs/C1/raw/expert-source-access.json`

用普通中文向正常成年人讲清固定框架：它原生解决的问题、关键区分、内部关系、一个独立低背景案例、回到固定原文的应用、一次迁移提示和重要边界。区分原作者内容、后续扩展、ReaderLab 教学整理和当前原文应用推论；不要把教学整理写成原作者正式命名的方法。不得写 Reader、Writer、产品判词或路线比较；记录实际打开的已登记页面。

必须如实填写 `raw/expert-source-access.json`。它必须使用 `readerlab-book-expert-teaching/source-access/v1`，`opened_urls` 只能列 `allowed` URL 或其明确登记的重定向，`cited_only_urls` 可列 `allowed` 或 `reference_only` URL；两数组不得重叠，不能出现 `blocked` 或未登记 URL。写明 `provenance: agent_declared` 和“不是浏览器或 OS 网络审计”的 audit scope。

## 稳定中文表达规则

1. 默认使用中文。
2. 人名首次出现使用“中文译名（英文原名）”，后续只使用中文姓氏或通行中文名。
3. 理论首次出现使用“中文名称（英文名称）”，后续只使用中文名称。
4. 不只写英文人名或英文理论名，避免连续中英混杂。
5. 专业术语先用普通中文解释。
6. 明确说明 ReaderLab 的教学整理不等于原作者正式命名的方法。

本 Skill 不执行语义调用，也不会在封存后修补课程。
