# ReaderLab V2 release candidate 复核

## 结论口径

`installable_release_candidate` 只表示干净可分享包、安装 / 发现 smoke、图书路线 smoke、长文 / 报告 / 访谈稿路线 smoke、Skill / 工程材料路线 smoke 在当前仓库提交上通过。

它不表示：

- production ready
- friend smoke passed
- reader accepted
- public validation pass
- 完整 GSTACK 包通过

## 复核命令

在研发仓库运行：

```bash
python3 packaging/release_candidate_review.py
```

在已构建的可分享包根目录运行：

```bash
python3 tests/release_candidate_review.py
```

研发仓库模式会重新构建临时包；已构建包模式会对当前包自检。复核按顺序执行：

1. clean package audit：确认 `PACKAGE_AUDIT.json` 为 `pass`，且包内没有 `docs/reports/`、`private-material-validation`、`comment-replay`、`experiments/`、GSTACK 原始源仓库等污染路径。
2. package smoke：确认包内入口、脚本、fixtures、三路线 smoke、安装 smoke 和 RC 复核入口存在。
3. install / discovery smoke：把包安装到临时 Skill root，验证 `SKILL.md` 可发现、入口说明可读、最小配置命令可跑。
4. book route smoke：验证图书路线的配置结构、runner contract、Quality Gate request、机器 reader-page smoke 和 controller 状态边界。
5. longform / report / interview route smoke：验证长文路线不是按固定长度或文件顺序盲切，并区分论证结构、访谈转折、runner contract 和机器 reader-page smoke。
6. skill / engineering route smoke：验证净化正文、full-source evidence packet、技术解说页、资产卡冷启动字段和 blocking controller。

## 分层说明

当前复核把结果分成这些层：

- `configuration_structure`：配置参数、source paths、declared scope / units、material family 是否闭合。
- `runner_contract`：产物结构、正文 / 净化正文、reader-facing / audit 分离、渲染关系是否成立。
- `quality_gate_request`：机器可检查的 gate packet 和 rendered package eval 是否成立。
- `reader_evaluation`：当前只允许是 `machine_smoke_only`，不能说成人工读者通过。
- `blocking_controller` / `controller`：blocking gate 失败时 controller 不能给 `accept` 或 `limited_accept`。
- `human_acceptance`：当前固定为 `not_run`。

## 防回归清单

RC 复核必须继续阻断这些误报：

- 把 runner 通过说成读者质量通过。
- 把安装 smoke 说成 production ready。
- 把 `limited_accept` 说成发布通过。
- 把旧实验 reports、私有 source、本机路径、旧 handoff 或 GSTACK 原始仓库打进可分享包。
- 在 Skill / 工程材料路线中绕过 evidence layer 或 blocking controller。

## 后续状态

如果本复核通过，状态最多推进到 `installable_release_candidate`。下一层仍然需要独立的朋友环境 smoke 和具体输出包读者验收。
