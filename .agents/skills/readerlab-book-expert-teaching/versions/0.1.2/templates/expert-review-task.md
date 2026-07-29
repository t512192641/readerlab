# 独立专家教学审核任务 · {{RUN_NAME}}

你是独立的来源忠实与教学完整度审核者。请使用全新上下文，只读取以下本地文件：

{{REVIEW_READ_SET}}

只可打开已经登记为 `allowed` 的 URL 及其明确登记的重定向；不得搜索：

{{ALLOWED_SOURCES}}

只写入以下两个文件：

- `{{RUN_DIR}}/acceptance/expert-teaching-review.md`
- `{{RUN_DIR}}/acceptance/reviewer-source-access.json`

文件首两行必须严格为：

```text
SOURCE_FIDELITY_FINAL: <SOURCE_FIDELITY_PASS|RETURN_EXPERT_SOURCE|SOURCE_BLOCKED>
TEACHING_FINAL: <TEACHING_PASS|TEACHING_PARTIAL|TEACHING_FAIL>
```

分别判断来源忠实性和教学完整度。检查原作者内容、后续扩展、教学整理和应用推论是否分开；读者能否解释内部关系、使用独立案例和迁移提示、识别误用边界。不得重写课程，不得读取旧 run、Writer/Reader 材料、产品判词、隐藏推理或路线历史。报告默认使用中文；引用 URL 只能来自允许列表或已登记的 `reference_only` 项。

必须如实填写 `reviewer-source-access.json`。它必须使用 `readerlab-book-expert-teaching/source-access/v1`，`opened_urls` 只能列 `allowed` URL 或明确登记的重定向，`cited_only_urls` 可列 `allowed` 或 `reference_only` URL；不得列 `blocked` 或未登记 URL，且两数组不得重叠。写明 `provenance: agent_declared` 和“不是浏览器或 OS 网络审计”的 audit scope。
