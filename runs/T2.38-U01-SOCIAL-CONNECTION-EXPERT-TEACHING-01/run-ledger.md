# T2.38 U01 Social Connection Expert teaching · run ledger

> 本账本只记录本轮 Expert teaching 与独立来源／教学审核；不构成 Writer、生产资格、产品判词或长期合同。

## 预检

- 启动：`unavailable`（Expert 已完成一次语义执行；本轮无重试）
- 审计基线：`c8ef926216a99c45ae1341d1c74acde94fd92ae3`
- 当前 commit：`7200081254bf35a5cdec6db6ef5e7b2ce25899c4`
- 分支：`experiment/u01-social-connection-depth-seam`
- U01 与 source map 只读副本已复制；原始 SHA-256 见 `control/input-freeze.json` 与 `control/freeze-stage-0.sha256`。
- 固定 C 未变；Writer、ABC、Discovery、旧稿、T2.36/T2.37 Reader 与产品装配未运行。
- 来源政策：只允许 T2.36 source map 登记 URL；禁止搜索与新增来源。
- 临时脚本：`0`。

## 阶段记录

| 阶段 | 实际开始 | 实际结束 | 墙钟分钟 | Agent | 模型 | reasoning | 终局 | 重试 | Prompt 修改 | token | 成本 | 网络 |
|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| 1 Expert teaching | unavailable | unavailable | unavailable | `/root/u01_expert_teaching` | unavailable | unavailable | outputs frozen; `SOURCE_FIDELITY` not applicable | no | no | unavailable | unavailable | allowlist only; no search |
| 2 来源／教学审核 | unavailable | unavailable | unavailable | `/root/u01_expert_teaching_review` | unavailable | unavailable | `SOURCE_FIDELITY_PASS` + `TEACHING_PASS` | no | no | unavailable | unavailable | allowlist only; no search |

## 来源访问记录

Expert 实际打开：Cambridge 2006（成功）；Paperzz 2006（成功，镜像限制）；MIT 2004 PDF（成功）；Oxford 2011（成功）；SEP（成功）；Springer Zheng 2018（成功）；Cambridge Gunnemyr 2020（初次成功，后续行定位 timeout，未重试）；OUP24 原 URL（成功并重定向至登记允许的 `https://oup.silverchair-cdn.com/book-minimal/58181/chapter-minimal/480373479`）；UGR PDF（Internal Error，未采用、未重试）。仅直接打开 allowlist URL，无开放式搜索、无新增来源。
审核实际打开：Cambridge 2006（成功）；Paperzz 2006（成功，镜像限制）；MIT 2004 PDF（成功）；Oxford 2011（成功）；SEP（成功）；Springer Zheng 2018（成功）；Cambridge Gunnemyr 2020（Internal Error，本次未重试）；OUP24 原 URL（Internal Error），按登记允许尝试 OUP CDN（Internal Error），均未作为本次内容依据；UGR PDF（Internal Error，未采用、未重试）。仅直接打开 allowlist URL 及登记的 OUP CDN 重定向，无开放式搜索、无新增来源。

## 结果与停止点

- Expert draft：`raw/expert-teaching-draft.md`，SHA-256 `13d5cd6ae520fda515cc2a3a6c105ddd564d88d50d5232feea9ac399789053b2`，阶段 1 冻结。
- Expert source map：`raw/expert-teaching-source-map.md`，SHA-256 `1b518fc97a5bf0abe2d2c664ed049294ee7b42079c7401aa2e5ed3e4d71043f8`，阶段 1 冻结。
- 来源忠实：`SOURCE_FIDELITY_PASS`；教学完整度：`TEACHING_PASS`。
- Review：`acceptance/expert-teaching-review.md`，SHA-256 `9c9f7c64cce0bd17cbc9747775b00ca938bb4b5962b69821a1b4583eab87846f`，阶段 2 冻结。
- 产品包：`acceptance/expert-product-review.md`，SHA-256 `fe194eea4666ffd55bf25a4a33c11f2062b28e7fdffe26de41a994e73b9dde33`，由控制层机械装配；产品负责人判词仍为 `unknown`，无版本密钥。
- 全部 freeze hash：阶段 0、Prompt、阶段 1、阶段 2、阶段 3 均已 `shasum -c` 通过。
- Expert 与审核各一次；无重试、无 Prompt 修改、无 Writer／Reader／ABC／Discovery；完整归档路径已写入 manifest，最终 archive SHA-256 在仓库外层 closeout ledger 记录，避免归档自引用。
- staged `git diff --cached --check` 的唯一告警来自必须逐字节保留的 U01 原文及其在产品包中的机械复制；排除这两个 exact-byte 文件后的 staged diff check 通过，未修改原文行尾空白。
