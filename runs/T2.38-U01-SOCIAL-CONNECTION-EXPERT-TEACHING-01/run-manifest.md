# T2.38 U01 Social Connection Expert teaching · run manifest

## 身份与范围

- 任务：`T2.38`
- run：`runs/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01`
- 分支：`experiment/u01-social-connection-depth-seam`
- 审计基线：`c8ef926216a99c45ae1341d1c74acde94fd92ae3`
- 当前源 commit：`7200081254bf35a5cdec6db6ef5e7b2ce25899c4`
- 启动时间：`pending`
- 固定 C：艾丽斯·玛丽恩·杨（Iris Marion Young）的社会联结责任模型（Social Connection Model）
- 固定 U01：16368 bytes，SHA-256 `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`
- 固定来源范围：T2.36 source map，SHA-256 `f89b357700f05eb8ab9ee12602ddc81a736d28443fa10b4cb53fc0e825d33f0a`
- 状态：`STOPPED_AFTER_EXPERT_TEACHING_REVIEW`
- 实验性质：`diagnostic sidecar; writer, ABC, discovery and production integration are not run`

## 预注册边界

- 两个全新 Agent 上下文：Expert teaching 与独立来源／教学完整度审核；均 `fork_turns="none"`，不得合并。
- Expert 与审核者只能打开 source map 登记的 URL；禁止开放搜索、新 C、新理论或新来源。
- 每个语义阶段一次执行；重试 `no`；Prompt 修改 `no`；来源表记录实际打开页面及失败页面。
- 只有 `SOURCE_FIDELITY_PASS + TEACHING_PASS` 才生成产品审阅包；否则停止且不创建条件性文件。

## 执行上下文（完成后补全）

| 阶段 | 角色 | Agent ID | 模型 | reasoning | 精确读取 | 来源联网 | 终局 |
|---|---|---|---|---|---|---|---|
| 1 | Expert teaching | `/root/u01_expert_teaching` | unavailable | unavailable | `inputs/u01-frozen.md`; `inputs/frozen-source-map.md`; `control/expert-teaching-task.md`; allowlisted frozen sources only | allowlist only; no search | outputs frozen; review pending |
| 2 | 来源／教学审核 | `/root/u01_expert_teaching_review` | unavailable | unavailable | `inputs/u01-frozen.md`; `inputs/frozen-source-map.md`; `raw/expert-teaching-draft.md`; `raw/expert-teaching-source-map.md`; `control/expert-teaching-review-task.md`; allowlisted frozen sources only | allowlist only; no search | `SOURCE_FIDELITY_PASS` + `TEACHING_PASS` |

## 冻结与停止

- Input freeze：`control/freeze-stage-0.sha256`。
- Prompt freeze：`control/prompt-freeze.sha256`。
- Expert draft SHA-256：`13d5cd6ae520fda515cc2a3a6c105ddd564d88d50d5232feea9ac399789053b2`。
- Expert source map SHA-256：`1b518fc97a5bf0abe2d2c664ed049294ee7b42079c7401aa2e5ed3e4d71043f8`。
- Review SHA-256：`9c9f7c64cce0bd17cbc9747775b00ca938bb4b5962b69821a1b4583eab87846f`。
- 来源忠实终局：`SOURCE_FIDELITY_PASS`；教学完整度终局：`TEACHING_PASS`。
- 产品包：`acceptance/expert-product-review.md`，SHA-256 `fe194eea4666ffd55bf25a4a33c11f2062b28e7fdffe26de41a994e73b9dde33`；仅控制层机械装配，产品负责人判词仍为 `unknown`。
- 冻结：阶段 0 `control/freeze-stage-0.sha256`；Prompt `control/prompt-freeze.sha256`；阶段 1 `control/freeze-stage-1.sha256`；阶段 2 `control/freeze-stage-2.sha256`；阶段 3 `control/freeze-stage-3.sha256`，均已 `shasum -c` 通过。
- 最终停止点：双门通过后已生成产品审阅包；不启动 Writer、Reader、ABC、Discovery 或任何后续产品装配，等待产品负责人审阅。
- 完整归档：`artifacts/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01.tar.gz`；最终归档 SHA-256 记录在仓库外层
  closeout ledger，避免把 archive hash 写入归档自身造成自引用。
