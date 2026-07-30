# ReaderLab v0.4 Contract Task

version: `v0.4-control-candidate`
date: `2026-07-30`
status: `control-only / not-executed`

## Purpose

本文件只定义 C5、K10、C1 的固定合同字段和填写边界。它不是候选评判、Expert 课、知识卡或 Writer
草稿；语义字段的实际值只能来自对应的冻结输入，不能在本文件内补写。

## Input whitelist

运行本合同任务时只允许读取：

- 本文件自身的字段定义；
- `run-manifest.md` 的运行元数据；
- `routing-task.md` 中 C5、K10、C1 的路由类别；
- 一个已冻结、带版本身份的 v0.4 candidate packet，仅用于填充字段，不能从中扩展对象或结论。

禁止读取 source context、搜索结果、历史 run、金标、反例、Expert／Writer 输出或其他候选的语义材料。

## Fixed contract fields

下表是三候选必须保持相同顺序和字段名的合同。`<frozen input only>` 是控制占位符，不是候选结论。

| 固定字段 | C5 | K10 | C1 |
|---|---|---|---|
| ID | `C5` | `K10` | `C1` |
| 当前类 | `CORE`（由路由任务拥有） | `DEEPENING`（由路由任务拥有） | `HOLD`（由路由任务拥有） |
| source anchors | `<frozen input only>` | `<frozen input only>` | `<frozen input only>` |
| external object | `<frozen input only>` | `<frozen input only>` | `<frozen input only>` |
| native problem | `<frozen input only>` | `<frozen input only>` | `<frozen input only>` |
| cognitive turn | `<frozen input only>` | `<frozen input only>` | `<frozen input only>` |
| independent syntax | `<frozen input only>` | `<frozen input only>` | `<frozen input only>` |
| highest allowed claim | `<frozen input only>` | `<frozen input only>` | `<frozen input only>` |
| new result | `<frozen input only>` | `<frozen input only>` | `<frozen input only>` |
| minimum skeleton | `1 look / 2 why / 3 use / 4 boundary / 5 transfer` | `1 look / 2 why / 3 use / 4 boundary / 5 transfer` | `1 look / 2 why / 3 use / 4 boundary / 5 transfer` |
| prohibited claims | `<frozen input only; must be explicit>` | `<frozen input only; must be explicit>` | `<frozen input only; must be explicit>` |
| Expert must complete | `<field completion contract only>` | `<field completion contract only>` | `<field completion contract only>` |
| Writer must preserve | `<field preservation contract only>` | `<field preservation contract only>` | `<field preservation contract only>` |
| stop | `<stop conditions below>` | `<stop conditions below>` | `<stop conditions below>` |

## Field rules

- `source anchors` 必须是可回到冻结 source context 的锚点；不得凭记忆、搜索或当前案例补造。
- `external object` 必须只记录冻结输入已经识别的对象身份；不得把原文主题、比喻或当前冲突改写成外部对象。
- `native problem` 必须保留外部对象原本要解决的问题；不得替换成“如何解释本案例”。
- `cognitive turn` 必须说明读者重看原文时发生的认知转向；不得提前写成最终文章。
- `independent syntax` 必须保留外部结构自身的关系、条件和推理语法；不得只留名词或标签。
- `highest allowed claim` 是本合同允许的最高强度；任何更强的普遍、因果或事实性断言都禁止。
- `new result` 只允许记录外部结构为重读带来的新判断接口；不得写成 C5 的最终内容。
- `minimum skeleton` 只规定控制顺序：`1 look` 看见锚点，`2 why` 说明为何，`3 use` 说明用途，
  `4 boundary` 说明边界，`5 transfer` 指向可迁移使用；它不是语义段落模板。

## Expert must complete

Expert（仅在路由允许时）必须从冻结输入完成所有固定字段，尤其是外部对象身份、native problem、
独立结构、最高允许主张、new result、五步 minimum skeleton、prohibited claims，并分别标出来源身份、
外部结构和当前原文应用。缺一项、来源不闭合、对象身份与结构不一致，均不得交 Writer。

## Writer must preserve

Writer（仅对 CORE 路由）必须保留：`source anchors` 的指向、`external object` 的身份、native problem、
cognitive turn、independent syntax、最高允许主张、new result、prohibited claims、五步 minimum skeleton
的逻辑顺序，以及 Expert 已锁定的条件和边界。Writer 只能组织表达，不能选题、添事实、补机制、提高
主张强度或把被禁止的当前案例结论捞回。

## Prohibited claims

- 不得把原文复述、常识、主题相似或当前冲突包装成外部认知框架。
- 不得把外部对象的身份、结构、来源或条件写成冻结输入未支持的事实。
- 不得把条件式判断升级为普遍规律、确定因果、道德裁决或对当前案例的唯一解释。
- 不得生成 C5 的最终内容、任何候选结论、Expert 课、结构化资产正文或 Writer 草稿。

## Stop

出现以下任一情况立即停止，不进入下一角色：

1. 任一固定字段缺失，或字段值无法回到冻结输入；
2. `source anchors` 不可定位，或外部对象身份与独立结构不匹配；
3. `highest allowed claim`、`new result` 或 `transfer` 需要超出冻结证据；
4. 路由类别不是 `routing-task.md` 明确给出的类别；
5. 需要搜索、新 seed、新 Expert、新 Writer 或改写候选语义才能继续。

验收门：字段顺序、字段名、三候选 ID、当前类和停止条件全部一致；只通过结构验收不代表任何候选
已获得产品接受。
