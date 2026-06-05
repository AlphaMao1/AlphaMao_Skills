# Archive Workflow

归档不是删除，也不是把研究判断改写成历史。它是把不应默认进入 agent 恢复路径的材料移到 `archive/`，让当前 dossier 继续保持人类可控。

## Trigger

使用 `archive` 当出现以下情况：

- `current-synthesis.md` 或 `model-map.md` 已无法在 30-60 秒内恢复当前状态。
- `generated/`、缓存、demo、dashboard、搜索结果或 agent findings 开始被当作默认事实源读取。
- 已完成的 handoff、审计记录、可读派生文件或旧版本框架仍留在活跃导航里。
- 文件已被当前模型吸收，只剩历史验证价值。
- 用户明确要求瘦身、归档、清理臃肿或让 agent 默认不访问旧材料。

## Archive Boundary

默认可以归档：

- `generated/` 下的 dashboard、demo、validation report、preview 和 graph cache。
- `frameworks/readable-models/` 等明确标为 `non-canonical` 的可读派生文件。
- 已完成或过期的 `handoff.current.md`、旧 `important-paths`、旧 startup prompts。
- 历史审计记录、subagent review、readability audit、标准迁移记录。
- 长文档中已被 `update-log.md` 或 canonical model 吸收的历史流水段落。

默认不要归档：

- `context.md`、`current-synthesis.md`、`model-map.md`、`open-questions.md`、`update-log.md`。
- 仍被当前结论引用的 `models/` calculation sheet。
- 仍承载来源边界或数字锚点的 active `modules/`。
- 当前 active company card。

如果必须归档核心文件的一部分，只移动历史附录或长流水；保留当前判断、row_id、公式、证据边界和反证条件。

## Archive Layout

使用批次目录，保留原相对路径：

```text
<dossier>/archive/YYYY-MM-DD-<slug>/
  archive-manifest.md
  generated/...
  frameworks/readable-models/...
  modules/...
  handoff/...
```

`archive-manifest.md` 必须记录：

- archive date
- reason
- moved paths
- active replacements
- references updated
- restore conditions
- validation commands and results

## Default Access Rule

Agent 默认不读取 `archive/`。只有以下情况才打开：

- 用户要求恢复、核验历史、追溯一次旧判断。
- 活跃文件显式指向归档路径并说明需要读取。
- 验证断链、审计历史或重生成 dashboard 需要旧 artifacts。

活跃导航应写清楚：归档文件不是事实源；事实仍以 canonical Markdown 为准。

## Procedure

1. 只读扫描：列出文件体量、入链关系、断链、candidate archive items。
2. 分类：按 canonical source、active module、process/history、generated/cache、non-canonical derivative 分层。
3. 影响评估：逐项说明关联文件、是否会影响 Current Model、是否需要导航替换。
4. 创建归档批次并移动文件，保留原路径结构。
5. 更新活跃导航：`model-map.md`、`context.md`、`important-paths.current.json`、必要的 `current-synthesis.md`。
6. 修复断链：活跃文件不应引用不存在路径；历史引用可指向 archive manifest 或留在归档内。
7. 验证：运行 `validate_dossier.py`，再做 Markdown 引用扫描。

## Pass / Fail

通过标准：

- `validate_dossier.py <dossier>` 通过；`generated_cache_ignored` 可接受。
- 活跃目录中没有指向缺失 Markdown 的核心断链。
- `archive/` 没有出现在默认 startup order。
- `model-map.md` 仍能说明当前 active 文件和归档边界。
- 当前模型判断、计算 row_id 和证据状态没有漂移。

失败信号：

- 归档后 Current Model 无法恢复。
- 归档文件仍被默认读取。
- 非 canonical 派生物继续出现在 facts/source-of-truth 位置。
- 为了归档而丢失可复算 calculation sheet、source boundary 或 active open question。
