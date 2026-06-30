# dbs-suite v2.15.1 版本差异说明

- 生成时间：2026-06-29T09:39:56+00:00
- old_version：2.12.0+local
- new_version：2.15.1
- old_source：{'type': 'git', 'url': 'https://github.com/dontbesilent2025/dbskill.git', 'subdir': 'skills', 'version_file': 'VERSION'}
- new_source：{'type': 'git', 'url': 'https://github.com/dontbesilent2025/dbskill.git', 'subdir': 'skills', 'version_file': 'VERSION'}
- upstream_tag：v2.15.1
- upstream_commit：096f726a20407901ca517cfc42509f96232fd0ea
- old_snapshot：/private/tmp/dbs-suite-before-update-20260629-096f726-target
- new_canonical_package：/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite
- new_lifeatlas_book：/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/dbs-suite__v2.15.1_096f726

## 汇总

- old_skill_count：23
- new_skill_count：24
- added_upstream：dbs-content-system, dbs-resonate, dbs-spread, dbs-wechat-html
- removed_upstream：无。本次删除项不是 upstream 删除，而是旧本地包里非 upstream overlay 不再保留。
- removed_local_only：chatroom-austrian, dbskill-upgrade, evaluating-candidates
- approved_local_extensions：无
- changed_common：dbs, dbs-action, dbs-agent-migration, dbs-ai-check, dbs-benchmark, dbs-chatroom, dbs-chatroom-austrian, dbs-content, dbs-decision, dbs-deconstruct, dbs-diagnosis, dbs-goal, dbs-good-question, dbs-hook, dbs-learning, dbs-report, dbs-restore, dbs-save, dbs-slowisfast, dbs-xhs-title

## 新增 upstream Skill

- `dbs-content-system`
- `dbs-resonate`
- `dbs-spread`
- `dbs-wechat-html`

## 移出旧本地非 upstream 项

- `chatroom-austrian`：旧本地非 upstream overlay；本轮未获批准作为本地扩展保留。
- `dbskill-upgrade`：旧本地非 upstream overlay；本轮未获批准作为本地扩展保留。
- `evaluating-candidates`：旧本地非 upstream overlay；本轮未获批准作为本地扩展保留。

## 公共 Skill 文件级变化

### `dbs`
- `SKILL.md`：+232/-30

### `dbs-action`
- `SKILL.md`：+13/-13

### `dbs-agent-migration`
- `SKILL.md`：+136/-60

### `dbs-ai-check`
- `SKILL.md`：+13/-11

### `dbs-benchmark`
- `SKILL.md`：+13/-14

### `dbs-chatroom`
- `SKILL.md`：+43/-0

### `dbs-chatroom-austrian`
- `SKILL.md`：+13/-12

### `dbs-content`
- `SKILL.md`：+13/-15

### `dbs-decision`
- `SKILL.md`：+14/-16

### `dbs-deconstruct`
- `SKILL.md`：+13/-24

### `dbs-diagnosis`
- `SKILL.md`：+14/-19

### `dbs-goal`
- `SKILL.md`：+13/-14

### `dbs-good-question`
- `SKILL.md`：+13/-18

### `dbs-hook`
- `SKILL.md`：+13/-12

### `dbs-learning`
- `SKILL.md`：+13/-23

### `dbs-report`
- `SKILL.md`：+13/-10

### `dbs-restore`
- `SKILL.md`：+13/-0

### `dbs-save`
- `SKILL.md`：+13/-9

### `dbs-slowisfast`
- `SKILL.md`：+13/-12

### `dbs-xhs-title`
- `SKILL.md`：+13/-10

## 需要人工复核页

新版 24 个 Skill 的 `human_status` 均为 `pending`。新增 Skill、正文变化较大的 Skill，以及任何从旧版 completed/accepted 逻辑迁移而来的判断都需要人工复核。优先复核：
- `dbs`
- `dbs-agent-migration`
- `dbs-chatroom`
- `dbs-content-system`
- `dbs-resonate`
- `dbs-spread`
- `dbs-wechat-html`

## 包治理备注

- canonical package 本体已按 upstream v2.15.1 更新，目录中不再包含 `chatroom-austrian`、`dbskill-upgrade`、`evaluating-candidates`。
- `skillsctl show dbs-suite` 的 alias 展示仍可能混入历史兼容 alias；ReaderLab 新版生产只读取 canonical package 实际目录，不读取这些 alias。
- 回滚路径：用 old_snapshot 对照恢复，或重新执行 `skillsctl update-package dbs-suite` 并按 PACKAGE.json 策略同步。
