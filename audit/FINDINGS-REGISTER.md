# ReaderLab 开放审计问题台账

> 版本：v0.1
> 快照日期：2026-07-25
> owner：开放审计问题的状态、处理责任和复核条件
> 注意：本台账不执行修复，不拥有产品事实，不覆盖历史报告和任务卡正文。

## 一、状态与处理规则

状态只使用：

- `OPEN`
- `IN_PROGRESS`
- `READY_FOR_REAUDIT`
- `CLOSED`
- `SUPERSEDED`

阻塞级别：

- `STOP`：相关路线不得继续；
- `BEFORE_NEXT_RUN`：下一次正式生产前必须处理；
- `BEFORE_QUALIFICATION`：可以继续受控研究，但不得宣布资格或进入 Skill；
- `OBSERVE`：记录趋势，达到触发条件后升级。

执行现场可以把问题推进到 `READY_FOR_REAUDIT`，只有独立审计依据直接证据才能关闭。

多条问题并存时，取最严格阻塞；单条问题中的“当前允许”不能放宽总行动门。

## 二、唯一当前行动门

- 总体状态：`RED`
- 唯一产品前进行动：产品负责人审阅 `runs/T2.35-CH08-D3-EXPERT-P2-01/acceptance/acceptance-report.md`，决定 D3 Expert 是否值得进入 Writer；这不授权 Writer 或新 run。
- 辅助只读权限：只读审计；不写入生产文件的方案设计；按下方证据展开 manifest 核对直接证据。
- 当前禁止：创建下一次正式生产 run；调用新的生产语义角色；新增长期 Prompt、角色、关卡或合同；让最终 Judge 上岗；移动或删除历史对象。
- 解除 `RED` 的剩余最低条件：产品负责人完成 T2.35 判断；明确下一获批实验；AUD-009 针对该实验达到独立复核允许的终局。第一次综合大审计、完整责任图、单一状态 owner、active／historical 健康入口、宿主元数据修复及图书内容流合同冲突已经完成独立复核，但不替代剩余产品判断与未见材料防过拟合条件。
- 注意：该行动门不阻止产品负责人阅读和判断已经冻结的 T2.35 审阅包。
- 优先级：本门高于 README、蓝图、旧路线报告和单条问题中的局部允许文字；外部路线文档不能放宽 `RED`。

### 下一证据展开 manifest

| 顺序 | 目的 | 固定输入 | 复验方式 | 结果 owner |
|---:|---|---|---|---|
| 1 | 固定 T2.35 待审对象 | `taskcards/T2.35.md` SHA-256 `740717e8...0dbc6`；审阅包 SHA-256 `4c024857...d101f`；两份 freeze hash 见能力地图 `E02` | `shasum -a 256`；只读 freeze 复算 | `audit/PROJECT-SYSTEM-AUDIT-2026-07-25.md` |
| 2 | 核对状态 owner 冲突 | `README.md:17-27`、`blueprints/PIPELINE-MAP.md:106-113`、T2.35 状态头 | 逐 owner／派生层比较 | AUD-001 |
| 3 | 核对长期合同冲突 | `PRODUCT-DECISIONS.md:55-79`、T1.3、T1.4、T1.6、T1.7 | 输入、判断对象、失败动作和生命周期比较 | AUD-003、AUD-012 |
| 4 | 核对默认健康信号 | tests、`validate.py`、`tools/run.py`、四个 `.DS_Store` run | 台账 AUD-005／006 所列命令 | AUD-005、AUD-006 |
| 5 | 核对规则累积与角色必要性 | T2.28—T2.35 指定行段 | 产品结果、调用、墙钟与删除测试 | AUD-009、AUD-010 |
| 6 | 核对生命周期与保留 | taskcard／run／archive 文件列表和 Git tracking | 数量、profile、引用与 retention 投影 | AUD-007、AUD-008 |

短 hash 只作表格识别，完整 hash 以能力地图 `E02` 和系统大审计第 2.1 节为准。

## 三、开放问题

### AUD-001 当前状态入口失真

- 状态：`CLOSED`
- 阻塞级别：`BEFORE_NEXT_RUN`
- 事实：README 自称唯一交接入口但停在 T2.12；派生路线和当前状态文档也落后于 T2.35。
- 证据：`README.md:17-27`；`blueprints/PIPELINE-MAP.md:106-113`；`docs/book-pipeline-current-state-and-skill-roadmap.md:1000-1087`；`taskcards/T2.35.md:1-18`。
- 影响：新执行者和审计者可能选择错误入口或错误下一步。
- 处理结果：新增 `CURRENT-STATE.md` 作为当前任务、run、停止点、下一产品动作、禁止项和 unknown 的 owner；README、两份蓝图与专题路线只保留引用或明确的历史快照。
- 独立复核：相对链接、T2.35 冻结身份和派生入口 diff 通过；owner 不把固定审计基线误写成动态 HEAD。
- 关闭边界：关闭的是状态入口冲突，不代表 T2.35 获得产品接受，也不授权下一 run。

### AUD-002 完整流程和当前实验被混淆

- 状态：`CLOSED`
- 阻塞级别：`BEFORE_NEXT_RUN`
- 事实：首次审计把 T2.35 产品审阅描述为唯一下一步，遗漏视角选择、Writer、B3 和最终 Judge 等长期责任。
- 证据：`audit/ENGINEERING-AUDIT-2026-07-25.md:15-21,140-177` 对照 `PRODUCT-DECISIONS.md:21-27` 与 `taskcards/T2.35.md:10-18`。
- 影响：局部实验停止点可能被误报为整体产品路线。
- 处理结果：`audit/PROJECT-SYSTEM-AUDIT-2026-07-25.md`、能力地图和审计宪章已明确完整功能责任、当前实验停止点与两条产品线；首次报告已标记 superseded。
- 独立复核：第四轮全新上下文可同时恢复完整责任图、`RED` 门、T2.35 唯一产品动作和证据 manifest。
- 关闭边界：完整责任图不是角色数量决定，也不表示其中各责任已经实现或资格通过。

### AUD-003 Writer 长期合同与产品 owner 冲突

- 状态：`CLOSED`
- 阻塞级别：`BEFORE_NEXT_RUN`
- 事实：`contracts/T1.6-writer.md` 冻结为一张锁定知识卡对应一个成品且 Writer 不得拆卡；现行产品决议允许专家初稿包含多张关联知识卡，并允许 Writer 必要时拆分。
- 证据：`contracts/T1.6-writer.md:14-55`；`PRODUCT-DECISIONS.md:55-59`。
- 影响：继续使用旧合同可能错误压缩认知结构，或使执行者无法确定现行权限。
- 处理结果：`contracts/BOOK-CONTENT-FLOW-v2.md` 以完整 Expert 初稿与语义锁作为 Writer 组织单位，允许按阅读体验合并或必要拆分为一个或多个 Reader 单元；旧 T1.6 字节与 M1 receipt 原样保留为历史身份。
- 独立复核：三轮工程审查最终 `PASS`；新 freeze receipt 绑定 v2 身份，`blueprints/PIPELINE-MAP.md` 是唯一 current pointer；active 回归同时锁定新合同身份、旧 T1.3—T1.7 与 M1 receipt 哈希，17/17 PASS。
- 关闭边界：关闭的是长期接口冲突。Writer runtime 仍未 `integrated`，真实 Reader 单元尚未 `verified`，产品能力保留仍须由后续获批真实运行证明；不得因此启动 Writer。

### AUD-004 最终 Judge 未取得资格

- 状态：`OPEN`
- 阻塞级别：`BEFORE_QUALIFICATION`
- 事实：T1.8 只冻结长期验收语义；T2.2 资格结果为 `FAIL`，M2 不存在。
- 证据：`contracts/T1.8-independent-acceptance.md:8-68`；`README.md:39-46,51-60`；`taskcards/T2.2.md`。
- 影响：当前没有可用的最终独立 Judge；P1/P2/P3 不能自动替代。
- 处理责任：执行现场在具备冻结接受稿、对称输入和未见资格条件后另提方案。
- 当前允许：继续受控正例研究和产品负责人判断。
- 当前禁止：让模型 Judge 上岗或用旧 T2.2 恢复设计替代现行授权。
- 复核条件：资格审计在冻结、隔离、正反例和未见材料上通过；产品负责人权力保持不变。

### AUD-005 默认项目健康信号失真

- 状态：`CLOSED`
- 阻塞级别：`BEFORE_NEXT_RUN`
- 事实：默认 `unittest discover` 运行 0 项并退出 5；显式 `-s tests` 后 35 项中 24 PASS、1 FAIL、10 ERROR，失败集中于历史 T2.26 身份和旧 Writer 字节假设。`validate.py` 也落后于当前任务集合。
- 证据：`taskcards/T2.35.md:284-292`；复核命令 `python3 -B -m unittest discover -v`、`python3 -B -m unittest discover -s tests -v` 与 `python3 -B validate.py`，结果由当前综合审计报告固定。
- 影响：团队会习惯忽略红灯，新回归难以识别。
- 处理结果：新增 `tests/entry.py`，无参数运行 active 子集；T2.26 三组测试只能通过 `historical-t226` 显式回放。README 与当前状态 owner 将 `validate.py` 明确为早期 clean-seed 历史回放。
- 独立复核：`python3 -B tests/entry.py` 当前为 17/17 PASS；`python3 -B tests/entry.py historical-t226` 明确运行 27 项并保留当前 1 FAIL／10 ERROR；inventory 对漏分类、交叉分类和零测试 fail closed。
- 关闭边界：active 入口只是当前可维护的确定性测试子集，不是完整项目、语义质量或产品资格证明。

### AUD-006 run 健康检查受宿主元数据污染

- 状态：`CLOSED`
- 阻塞级别：`BEFORE_NEXT_RUN`
- 事实：T2.28 Writer、T2.30、T2.31、T2.35 四个 run 存在 `.DS_Store`；当前 T2.35 `tools/run.py check` 会因此失败。独立复算显示跳过该宿主元数据后，四个 run 的冻结清单仍一致。
- 证据：`find runs -name .DS_Store -print`；`python3 -B tools/run.py check runs/T2.35-CH08-D3-EXPERT-P2-01`；受影响 run 由当前综合审计报告逐项固定。
- 影响：仅打开 Finder 就可能让已冻结 run 从 PASS 变为失败，复验证据不稳定。
- 处理结果：`tools/run.py` 的共享 artifact inventory 只忽略非 symlink 普通文件 `.DS_Store` 并输出 warning；未知文件、symlink 和非普通对象继续硬失败。
- 独立复核：专项回归 10/10 PASS；T2.28 Writer、T2.30、T2.31、T2.35 官方 check 全部 PASS 且 warning 可见；`.Spotlight-V100` 反例继续失败；未删除或改写任何 run。
- 关闭边界：只关闭 Finder 元数据导致的假红灯，不评价 run 的语义质量或产品接受。

### AUD-007 历史、当前、草案和本地载荷未清楚分层

- 状态：`OPEN`
- 阻塞级别：`BEFORE_QUALIFICATION`
- 事实：65 张任务卡、42 个 run、456 个 run 文件主要并列保留；只有一个 run 进入 `archive/`。183 个 run 文件被 Git 跟踪、268 个被忽略，其余为宿主元数据或当前未跟踪控制证据；载荷的可移植性和保留责任未定义。
- 证据：`find taskcards -maxdepth 1 -name '*.md'`；`find runs -mindepth 1 -maxdepth 1 -type d`；`find runs -type f`；`find archive -mindepth 1 -maxdepth 1 -type d`；`git ls-files runs`。
- 影响：认知成本高，容易误读历史，保留和清理责任不明确。
- 处理责任：执行现场先建立引用和保留清单，再提交逻辑归档与物理清理候选。
- 当前允许：只读分类和依赖分析。
- 当前禁止：批量移动、删除、重命名或破坏现有 hash／路径证据。
- 复核条件：42 个 run 和历史任务卡具有明确 profile、生命周期、保留理由与复验入口；当前入口不默认暴露历史噪声，历史证据仍可追溯。

### AUD-008 通用工程逻辑散落在任务卡与超长验证器

- 状态：`OPEN`
- 阻塞级别：`BEFORE_QUALIFICATION`
- 事实：任务卡承担大量运行实现；`validate.py` 约 9,500 行并绑定旧实验；通用检查在任务卡、临时脚本和工具之间重复。
- 证据：`wc -l validate.py tools/run.py taskcards/*.md`；`taskcards/T2.28.md`—`T2.35.md` 共 1,810 行；`taskcards/T2.31.md:83-92,152-173` 记录 T2.30 十个临时脚本。
- 影响：locality 差，修复易形成 Shotgun Surgery，一次性工作持续增长。
- 处理责任：执行现场从真实重复点提出深化现有 module 的方案，不先全面重写。
- 当前允许：依赖和重复逻辑审计。
- 当前禁止：仅因文件长机械拆分，或建立第二套平行验证框架。
- 复核条件：至少两个真实调用方跨同一 interface 获得复用，默认测试覆盖该 interface，旧重复逻辑被替换而非叠加。

### AUD-009 当前流程存在过拟合和规则累积风险

- 状态：`OPEN`
- 阻塞级别：`BEFORE_NEXT_RUN`
- 事实：T2.28—T2.35 围绕连续失败加入 C4 收紧、Writer 指令、范围检查、四向比较和单方向展开，但新组合尚无 P3 接受。
- 证据：`taskcards/T2.28.md:162-176`、`T2.29.md:16-18,86-106`、`T2.30.md:1-17,208-218`、`T2.31.md:175-179`、`T2.32.md:1-9,95-107`、`T2.33.md:195-208`、`T2.34.md:288-324`、`T2.35.md:10-18`。
- 影响：可能为固定章节建立越来越窄的局部最优，并增加日常成本。
- 处理责任：执行现场冻结下一次实验变量；审计总控在运行前检查新增规则必要性。
- 当前允许：T2.35 产品审阅和失败责任定位。
- 当前禁止：在 T2.35 判词前继续为 D3 新增长期 Prompt、硬门或固定格式。
- 复核条件：同一冻结路线在未见材料上运行；新增规则逐项绑定真实失败、收益和能力保留回归。

### AUD-010 角色和关卡尚未经过系统删除测试

- 状态：`OPEN`
- 阻塞级别：`BEFORE_QUALIFICATION`
- 事实：v2 已从长期合同删除 P1／P2／P3 混义名称，并区分课程入口价值、内容锁定、独立 Fidelity 和 B2 装配；但这些功能责任的运行成本、可合并实现与删除后果尚未用真实目标路径验证。
- 证据：`PRODUCT-DECISIONS.md:21-27`；`blueprints/PIPELINE-MAP.md:11-88`；`taskcards/T2.26.md:79-94,215-321,527-570`；`taskcards/T2.34.md:19-32`；`taskcards/T2.35.md:10-18`。
- 影响：可能保留重复判断和多余调用，也可能错误删除真正需要独立性的责任。
- 处理责任：首次大审计逐责任执行删除测试，形成保留、合并、研发期临时或待验证结论。
- 当前允许：角色地图和输入／输出／失败动作分析。
- 当前禁止：按角色名称直接增删，或把所有研发人工门默认写入最终 Skill。
- 复核条件：每项长期责任有唯一问题、必要权限、失败动作和成本依据。

### AUD-011 Skills 包解读线没有当前运行证据

- 状态：`OPEN`
- 阻塞级别：`BEFORE_QUALIFICATION`
- 事实：E1—E4 只有产品责任，没有当前 runtime、语义样张或产品接受证据。
- 证据：`PRODUCT-DECISIONS.md:105-116`；`blueprints/PIPELINE-MAP.md:89-104`。
- 影响：不能把图书线进度或旧 Skills 资产算作本线成熟度。
- 处理责任：执行现场在产品负责人确定优先级并授权材料后提出独立人工端到端方案。
- 当前允许：保留产品责任和共享薄骨架设计。
- 当前禁止：复用图书五项标准、Writer、Judge 或通过证据替本线宣布进展。
- 复核条件：至少一份获授权 Skill 包分别到达 E1—E4 的合法终局并获相应产品判断。

### AUD-012 发现、Expert 与 B2 长期合同仍冻结旧路线

- 状态：`CLOSED`
- 阻塞级别：`BEFORE_NEXT_RUN`
- 事实：T1.3／T1.4 仍以先形成三字段透视需求、再路由并提出一句候选主张为主接口；现行产品 owner 要求 Expert 完整自由阅读、自然决定教什么，控制层不替 Expert 命题。T1.7 的固定 callout 格式也与近期 Reader 命名和未决 `tandem-comments` 接口不一致。
- 证据：`contracts/T1.3-discovery.md:8-76`；`contracts/T1.4-expert-and-knowledge-card.md:8-98`；`contracts/T1.7-b2-assembly.md:38-72`；`PRODUCT-DECISIONS.md:63-79`；`blueprints/PIPELINE-MAP.md:35-77`。
- 影响：下一次生产若直接继承旧合同，可能重新引入中央派题、短主张和过早卡片化，并把未验证的装配格式当成现行接口。
- 处理结果：单一 v2 合同重新定义控制路由、正式透镜优先／真实缺口临时 Expert、受控偶遇、Expert 自主发现与沉默、初稿后审计投影、Writer、独立 Fidelity 与确定性 B2；旧 T1.3—T1.7 不再是现行接口。
- 独立复核：首轮发现 4 P1／1 P2，二轮剩 2 P1，三轮 `PASS`；重点关闭了候选提前生效、价值检查表下沉 Expert、返工读取闭集不闭合、路由责任缺失与 Fidelity gate 歧义。
- 关闭边界：合同技术激活不代表 runtime `integrated`、真实链路 `verified` 或产品 `accepted`；B3 与最终 Judge 仍在合同之外并保持原有阻塞。

## 四、观察项

### AUD-O01 审计体系自身可能增加文档负担

- 状态：`OPEN`
- 阻塞级别：`OBSERVE`
- 观察：当前新增运行机制、能力地图和问题台账三个入口。
- 升级条件：同一事实需要在两个以上审计入口重复维护，或每轮审计需要大规模手工同步。
- 复核：完成两次小审计和一次大审计后执行删除测试。

### AUD-O02 试运行审计频率可能过密

- 状态：`OPEN`
- 阻塞级别：`OBSERVE`
- 观察：暂定每两轮小审计、每五轮大审计。
- 升级条件：审计成本明显高于发现的问题价值，或审计阻塞正常生产。
- 复核：首个完整试运行周期后调整，不冻结为长期规则。
