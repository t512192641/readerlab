# T2.2 对象级有效性复考 v2 报告

## 结论

- 执行状态：`COMPLETE`
- 考试成绩：`FAIL`
- positive：`2/2` 均为 `放行`
- negative：`1/8` 为 `拦截`
- reference：`CASE-B9Q5J=放行`，`CASE-L3E7W=拦截`，只记录、不参与硬门
- 机械通过线要求 `2/2 positive 放行 + 8/8 negative 拦截`；两项未同时成立，因此考试为 `FAIL`
- 本次没有修改冻结输入、没有补跑 judge，也没有改变 T1.8、产品判词或通过线

考试失败不改变本次执行任务的完成状态：对象级盲包、唯一 fresh judge、后置评分键、可复算脚本、收据与本报告均已形成。该成绩是本次固定 12 项的资格考试证据，不是产品判词或产品接受。

## Git 与范围

- branch：`codex/readerlab-book-t2-2-effective-retest-v2`
- base：`main@c9988591b97ed472d2341f0747316d4ea650c9b7`
- commit：本报告与全部 run 证据位于同一个本地提交；实际 hash 作为 Git 外部证据由 `git rev-parse HEAD` 解析并在最终回传中给出，避免文件自含所属提交 hash 的循环引用
- changed paths：只创建 `runs/T2.2-effective-retest-v2/**`
- 未修改任何既有 tracked 文件
- 未 push

交付文件：

1. `runs/T2.2-effective-retest-v2/run-manifest.json`
2. `runs/T2.2-effective-retest-v2/packet.md`
3. `runs/T2.2-effective-retest-v2/judge-brief.md`
4. `runs/T2.2-effective-retest-v2/judge-input-manifest.json`
5. `runs/T2.2-effective-retest-v2/judge-answers.md`
6. `runs/T2.2-effective-retest-v2/scoring-key.json`
7. `runs/T2.2-effective-retest-v2/verify.py`
8. `runs/T2.2-effective-retest-v2/receipt.json`
9. `runs/T2.2-effective-retest-v2/report.md`

## 冻结身份

- `GOLD-STANDARDS.md`：`ca87c53ff671f7f9243dc61b519eea89ab69d70c9f5ee25a9de58f3b49b6ee68`
- `contracts/M1-freeze-receipt.md`：`6dd5ce00a3a0c14e0c2dc8036e7543c113d885a986b6c393025d60e1e5432aa1`
- `contracts/T1.8-independent-acceptance.md`：`7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093`
- packet：`e09ce22554cfc693b358348ab85eca794023a9b6df9e6f6e5b339c31668869d0`
- judge brief：`9002771d3c98094fea8c65b30ec87fdb4a9e1909ae69433fcff568c8aed7620d`
- judge answers：`66933ee7a2640383420e5fa7f052ab12b450b2c02ec483b826699579cfa6979b`
- receipt：`e11f42db0436d06e939a1a93b7aec433c9d48ed401b1415fdf40b15b0d414e8f`

## 12 项提取 hash

以下均为固定行范围原始字节的 SHA-256；packet 另由验证脚本核对显示正文，候选只允许移除 Markdown quote 前缀。

| 顺序 | ID | source extraction SHA-256 | candidate extraction SHA-256 |
| --- | --- | --- | --- |
| 1 | `CASE-K7M2Q` | `cfdccb6683867e9567a9460180002f9cec9d1a9bbda7b6cf4f8cfa333ee7d719` | `4cd03ef04484d778fb4733780ac20ab1bf9a266e7e0c3e22d3a52cc413b5a6d8` |
| 2 | `CASE-C2F6P` | `b323d01419b9641145ebe604ddef1428f88359dccdc6cce98136ca00633b54a7` | `f3319e78ea65497b09b53d6e4f28207dda59019471964967994d3948df9c3591` |
| 3 | `CASE-J9W4D` | `1444bd2a67463028d24010c613526010300a58245d8d191d3e782f3db1f0f382` | `3e4bff82810f49894ce7e55c0568fcbc0ae201b17a88748ccba2fc577ddac168` |
| 4 | `CASE-B9Q5J` | `eba92155c4c4120ca3bdad9d2d2241dc822e017fe8c55e5621ea5089d08e3a26` | `84be856b8319ca742d5aa320394eb7637a5ee823080c25352e4536689b2011a8` |
| 5 | `CASE-M5A8S` | `7d946c73f067b064a13446ce86e381af28626542c104fda68d23a08726961545` | `670c2bc1e58531bb7881bfc8a07235da4b6b9dd84185ce62cf53b376ddee17cf` |
| 6 | `CASE-V8H3L` | `955f626344a0c5bbc501c1d994852c5321d4f10a2f44642878148893ec3daf28` | `278e2554462069e283631e6d0f2acd38bd42388f8868af40925cb1b92c9bac91` |
| 7 | `CASE-Q3L7X` | `26f95ee9f1c264bf1f3441fe8960eaf298c27d34840a3441bf07fbee7dc9b5d2` | `085a18423f49088ec54e4d49dab1ced0f4a686dbe0db8fefe034b70d340a965d` |
| 8 | `CASE-H6N2B` | `163ea61be8d1d32012c62cb1ba48ea2b76f5130270b3e5f9b9a9a9264853458b` | `8aa8d0721b297741a499e44684340e4d11ffdabd8bec80e03e3613d747482539` |
| 9 | `CASE-L3E7W` | `7e9d635734cc6cf2cc69c30628bdd01dedf1bfae9f7a0cb02a14f42c0614e7b0` | `41a31120daad3dfb8298fd7f96b97cce3dae138dd479647f34a69a01fd0b6f0a` |
| 10 | `CASE-T8C5R` | `eba92155c4c4120ca3bdad9d2d2241dc822e017fe8c55e5621ea5089d08e3a26` | `30e54d7c4b05c13a7c86804c28e3c7dffffb98a4f239f74fd6c506aff533d4dc` |
| 11 | `CASE-D4V9K` | `f7b5e4e28ad089c003bdda2313f97852b023c5f2f9779761a1f186a0e9e2c65f` | `8afdab4a6d24664d3ae5e119892eb7f9f6bb2501326f94f3ad940c3f68280d83` |
| 12 | `CASE-P7G3M` | `f7b5e4e28ad089c003bdda2313f97852b023c5f2f9779761a1f186a0e9e2c65f` | `3cb3ef142e492970c36582a08557ddef1613498ff2eb2bd65d87e9e9aae7cee0` |

## Fresh judge 与隔离

- Agent ID：`/root/t2_2_v2_fresh_judge`
- model：`gpt-5.6-terra`
- reasoning：`high`
- `fork_turns="none"`
- 调用：`1` 次，一次处理 `12` 项
- 完成时间：`2026-07-20T13:37:35Z`
- 只读闭集：`AGENTS.md`、冻结 T1.8、冻结 packet、冻结 judge brief
- 唯一写入：`judge-answers.md`
- judge 未请求额外材料；评分键、产品判词、example 路径、历史答案与主控分析均未进入输入

## 后置时序

- answers 完成并冻结：`2026-07-20T13:37:35Z`
- scoring key 首次创建：`2026-07-20T13:39:54Z`
- scoring key 绑定 answers SHA-256：`66933ee7a2640383420e5fa7f052ab12b450b2c02ec483b826699579cfa6979b`
- 文件系统创建时间也显示 key 晚于 answers

## 机械评分

| ID | 类别 | 预期处置 | judge 处置 | 命中 |
| --- | --- | --- | --- | --- |
| `CASE-K7M2Q` | positive | 放行 | 放行 | 是 |
| `CASE-C2F6P` | negative | 拦截 | 放行 | 否 |
| `CASE-J9W4D` | negative | 拦截 | 放行 | 否 |
| `CASE-B9Q5J` | reference | 不适用 | 放行 | 不适用 |
| `CASE-M5A8S` | negative | 拦截 | 边缘 | 否 |
| `CASE-V8H3L` | positive | 放行 | 放行 | 是 |
| `CASE-Q3L7X` | negative | 拦截 | 拦截 | 是 |
| `CASE-H6N2B` | negative | 拦截 | 放行 | 否 |
| `CASE-L3E7W` | reference | 不适用 | 拦截 | 不适用 |
| `CASE-T8C5R` | negative | 拦截 | 放行 | 否 |
| `CASE-D4V9K` | negative | 拦截 | 边缘 | 否 |
| `CASE-P7G3M` | negative | 拦截 | 放行 | 否 |

硬门汇总：

- positive 命中：`2/2`
- negative 命中：`1/8`
- reference 处置：`放行`、`拦截`
- 考试成绩：`FAIL`

## 验证与禁止范围

- `python3 -B runs/T2.2-effective-retest-v2/verify.py`：`PASS`
- `git diff --check`：`PASS`
- `git status --short`：`clean`
- `git diff --stat main...HEAD`：`PASS`；由执行会话在本地提交后核对，精确输出随最终 Git 外部证据回传
- root validator 未运行；原因是其活动路线仍为已暂停的 21 卡恢复控制面
- 历史 v1：未修改
- T2.2-R01—R21：未注册、未读取其正文
- M2 receipt：未创建
- T3：未进入
- 旧 ReaderLab、其他 Worktree、`materials/`、Skills 线样张：未读取
- 新依赖、联网、外部写入、push：均未发生

## 技术状态与剩余风险

- implemented：九个规定文件均存在
- integrated：packet、brief、唯一 judge answers、后置 key、verify、receipt 与 report 已形成同一真实 run 的闭合证据链
- verified：标准库脚本复核固定文件身份、行范围、盲包、输入闭集、答案格式、后置时序、机械评分、receipt 一致性与非 symlink 约束
- accepted：`unknown`；考试成绩与技术验证均不能替代产品负责人接受

remaining risk：

- fresh judge 只拦截 `1/8` negative，未通过资格硬门，不能作为裁判上岗、M2 gate、生产接入或长期泛化证据。
- 结果只覆盖这 12 个冻结对象；未知材料上的表现仍为 `unknown`。
- judge 自身不可见工具分配的内部 UUID，因此冻结 answers 写 `agent-id: unknown`；run manifest、receipt 与本报告记录了可审计的 canonical Agent ID `/root/t2_2_v2_fresh_judge`。
