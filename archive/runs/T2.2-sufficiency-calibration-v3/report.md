# T2.2 足够增量校准 v3 报告

## 结论

- 执行状态：`COMPLETE`
- 校准成绩：`FAIL`
- positive：`2/2` 命中
- hard negative：`2/5` 命中
- non-pass borderline：`1/3` 命中
- reference：`CASE-B9Q5J=放行`、`CASE-L3E7W=拦截`，只记录、不进入硬门
- 本任务不以取得 `PASS` 为完成条件；冻结输入、唯一 fresh judge、后置评分、可复算证据和本地提交均如实保留
- 没有为改变成绩修改 Prompt、packet、excerpt、brief、answers 或补跑 judge

同题校准不证明未知材料泛化。此次 `FAIL` 更不能作为未知材料裁判资格、M2、T3 或真实图书生产许可。

## Git 与两个增量

- branch：`HEAD (detached)`
- starting commit／第一 commit：`e8bd46c166531aa291dd83e89450a1b300f3cb4b`
- 第一 commit parent／v2 evidence commit：`0891ecf3366573c2142fb3ce36120dcd0614ebf6`
- main merge-base：`c9988591b97ed472d2341f0747316d4ea650c9b7`
- 第一 commit message：`T2.2-v3: record sufficient-value product standard`
- 第二 commit message：`T2.2-v3: run sufficient-value judge calibration`
- 第二 commit：本报告与全部 v3 run 证据位于同一个本地提交；实际 hash 由提交后的 `git rev-parse HEAD` 作为 Git 外部证据解析，避免文件自含所属 commit hash 的循环引用

第一 commit changed paths 恰为：

1. `PRODUCT-DECISIONS.md`
2. `GOLD-STANDARDS.md`
3. `taskcards/T2.2.md`
4. `audit/manifest.json`

第二 commit changed paths 恰为：

1. `runs/T2.2-sufficiency-calibration-v3/run-manifest.json`
2. `runs/T2.2-sufficiency-calibration-v3/packet.md`
3. `runs/T2.2-sufficiency-calibration-v3/product-standard-excerpt.md`
4. `runs/T2.2-sufficiency-calibration-v3/judge-brief.md`
5. `runs/T2.2-sufficiency-calibration-v3/judge-input-manifest.json`
6. `runs/T2.2-sufficiency-calibration-v3/judge-answers.md`
7. `runs/T2.2-sufficiency-calibration-v3/scoring-key.json`
8. `runs/T2.2-sufficiency-calibration-v3/verify.py`
9. `runs/T2.2-sufficiency-calibration-v3/receipt.json`
10. `runs/T2.2-sufficiency-calibration-v3/report.md`

未 push。

## 第一增量固定核对

| owner 文件 | SHA-256 | 结果 |
| --- | --- | --- |
| `PRODUCT-DECISIONS.md` | `66f772dd629b1bd1428dfc94ee2c64524f72067a7302d1342c9ef1a2ffa46cce` | 匹配 |
| `GOLD-STANDARDS.md` | `88bf346022a6b7776042082b3a42798d15ae499d22b0dc5ebb98202f3db13a4b` | 匹配 |
| `taskcards/T2.2.md` | `126348788576e0a31acafdf6739b8b95479cff8e38e289e4cba7df2b5ff8a38a` | 匹配 |
| `audit/manifest.json` | `8d4352f8f8cbe62cbee8e75b332428fad844007314bda33f420850c571e6a73d` | 匹配 |

## 原始 v2 证据现场

- 唯一核对 Worktree：`/Users/tianqiang/.codex/worktrees/d0fb/readerlab`
- `git status --short --branch`：只有分支行，工作树干净
- HEAD：`0891ecf3366573c2142fb3ce36120dcd0614ebf6`
- 原始 verifier：`PASS`
- verifier 实际输出：`exam=FAIL; positive=2/2; negative=1/8; references=CASE-B9Q5J:放行,CASE-L3E7W:拦截`
- 没有打开、搜索或复制该 Worktree 正文
- 没有在当前 v3 树、Git archive、新 checkout 或复制品中运行 v2 verifier
- v2 原始 GOLD 与当前 GOLD 分开核对，没有混用

## v3 冻结身份与输入隔离

- v3 packet SHA-256：`e09ce22554cfc693b358348ab85eca794023a9b6df9e6f6e5b339c31668869d0`
- v2 commit 中 packet SHA-256：`e09ce22554cfc693b358348ab85eca794023a9b6df9e6f6e5b339c31668869d0`
- `cmp` 与 verifier 均证明 v3 packet 和 v2 commit 中 packet 字节完全相同
- product excerpt：`0e199ad969a4e2e6ae2916d638a38ade45c891c94f0d1c5c47f90427b1b3fb27`
- judge brief：`cb873e315d5e0ec9d7569667a812837ba8b000dc398c626ae643da3fd6738c88`
- judge input manifest：`d47f3fd4bc4be0246c25d13d26ab06e86a20675778094a530f2cd9e0e0db4fc2`
- judge answers：`232364e0bb664e1308d5c2ffd12d07b4d35ca618370407e0aa62aa9bc1dba80f`
- scoring key：`71391d6d9f9551fa8ceb844b8aa3dbbd2551cbf5964fceb0924d3273ed7b16bc`
- receipt：`6c743314be4b5bc55d48c75b529fe1782ee2fab919b502ab9f34ba1a2bda4374`
- T1.8：`7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093`

judge 启动前已经冻结并检查 packet、excerpt、brief 与 input manifest；逐字摘录检查、CASE 与处置邻接扫描、分类／答案词扫描、symlink 检查均通过。excerpt 只含 `PRODUCT-DECISIONS.md` 当前 B2 通用门槛；judge 没有读取整个产品 owner。

## Fresh judge

- Agent ID：`/root/t2_2_v3_fresh_judge`
- model：`gpt-5.6-terra`
- reasoning：`high`
- `fork_turns="none"`
- 调用次数：`1`
- 单次处理：全部 `12` 项
- 完成时间：`2026-07-20T15:19:17Z`
- 唯一读取闭集：`AGENTS.md`、v3 excerpt、T1.8、v3 packet、v3 brief
- 唯一写入：v3 `judge-answers.md`
- judge 未请求额外材料、未搜索仓库、未获得 scoring key、GOLD、example、产品逐题判词或主执行上下文

answers 于 `2026-07-20T15:19:17Z` 完成并封存；scoring key 于 `2026-07-20T15:21:03Z` 首次创建，并绑定 answers SHA-256。时间戳与文件系统创建时间均证明 key 晚于 answers。

## 机械评分

| ID | 类别 | 允许处置 | judge 处置 | 命中 |
| --- | --- | --- | --- | --- |
| `CASE-K7M2Q` | positive | 放行 | 放行 | 是 |
| `CASE-C2F6P` | hard negative | 拦截 | 拦截 | 是 |
| `CASE-J9W4D` | hard negative | 拦截 | 放行 | 否 |
| `CASE-B9Q5J` | reference | 只记录 | 放行 | 不适用 |
| `CASE-M5A8S` | non-pass borderline | 边缘或拦截 | 放行 | 否 |
| `CASE-V8H3L` | positive | 放行 | 放行 | 是 |
| `CASE-Q3L7X` | hard negative | 拦截 | 拦截 | 是 |
| `CASE-H6N2B` | hard negative | 拦截 | 放行 | 否 |
| `CASE-L3E7W` | reference | 只记录 | 拦截 | 不适用 |
| `CASE-T8C5R` | hard negative | 拦截 | 边缘 | 否 |
| `CASE-D4V9K` | non-pass borderline | 边缘或拦截 | 边缘 | 是 |
| `CASE-P7G3M` | non-pass borderline | 边缘或拦截 | 放行 | 否 |

三类硬门没有全部命中，因此 calibration result 为 `FAIL`。结果按首次冻结答案机械计算，没有人工改分。

## 验证与禁止范围

- 原始 v2 verifier：`PASS`
- v3 verifier：`PASS`
- root `python3 -B validate.py`：`PASS`
- `git diff --check`：`PASS`
- 第二 commit 只新增 `runs/T2.2-sufficiency-calibration-v3/**`
- run 中所有文件均为普通文件，无 symlink
- 无 TODO、占位符、死文件或未连接产物
- owner、T1.8、examples、v2 run、历史 diagnostics：未修改
- T2.2-R01—R21：未注册、未读取正文
- M2 receipt：未创建
- T3：未进入
- `materials/`、Skills 线样张、真实图书生产材料：未读取
- 新依赖、联网、云端写入、push：均未发生

## 技术状态与接受边界

- implemented：十个规定 run 文件存在
- integrated：owner 摘录、同字节 packet、brief、输入清单、唯一 judge answers、后置 key、receipt、report 与 verifier 构成同一真实 run 证据链
- verified：原始 v2 verifier、v3 verifier、根验证器、Git diff 与范围检查全部通过
- accepted：产品负责人的既有标准已落库；本次校准不是新的产品判词

remaining risk：同题校准不证明未知材料泛化；本次固定同题校准为 `FAIL`，仍不能作为裁判上岗、未知材料资格、M2、T3 或生产许可。
