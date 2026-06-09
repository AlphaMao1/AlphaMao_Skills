# 研究工作区写入桥

判断日报 item 是否应写入 progressive research dossier 时读这里。

## 默认恢复面

写入前先读：

- `context.md`
- `current-synthesis.md`
- `model-map.md`
- `source-leads-index.md`
- `open-questions.md`
- `update-log.md`
- 相关 `modules/`
- 相关 `companies/`

archive 里的每日报告供人查看和审计。除非要追溯来源，agent 默认不要读 archive。

## 归档布局

每日报告：

```text
archive/creator-daily/<source_id>/<YYYY-MM-DD>.md
```

raw/transcript artifact：

```text
archive/creator-raw/<platform>/<source_id>/
```

archive 不属于默认 active recovery surface。

`source-leads-index.md` 属于默认 active recovery surface。它只索引博主 source lead 的路由结果和证据边界，不是事实源，也不是模型变化日志。

## 写入门禁

| action | 是否可写 active files | 目标 |
| --- | ---: | --- |
| `archive-only` | 否 | 只写日报 |
| `open-question` | 是 | `open-questions.md` |
| `company-update` | 是 | `companies/<company>.md` |
| `module-update` | 是 | `modules/<axis>.md` |
| `model-candidate` | 只写候选 | model patch candidate 区域或 `open-questions.md` |
| `current-model-update` | 是，但必须过证据门禁 | `current-synthesis.md` 和 `update-log.md` |
| `bridge-to-dossier` | 不直接写外部 dossier | 日报或 `open-questions.md` 里的 bridge candidate |

`noise` 永不写 active files。

非模型变化的路由事件不写 `update-log.md`。`update-log.md` 只记录新增/加强/削弱/矛盾/关闭开放问题等研究认知变化。

## Active File 形态

开放问题：

```markdown
## Q: [可验证问题]
Priority: P0 | P1 | P2
Impact: [影响的判断/module/model]
- [ ] c1: [具体检查条件] (source-lead: [source_id item_id])
- [ ] c2: [需要的一手或更强二手来源]
```

公司 source-lead 区：

```markdown
## 博主 Source Leads

| 日期 | 来源 | item | claim | 验证状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
```

模块 source-lead 区：

```markdown
## 博主 Source Leads

| 日期 | 来源 | item | mechanism | 模型相关性 | 下一步 |
| --- | --- | --- | --- | --- | --- |
```

Bridge candidate：

```markdown
## Bridge Candidate: [目标 dossier/topic]
- 来源: [source_id item_id]
- 为什么可能属于外部 dossier:
- 未复核前不要修改目标 dossier。
```

## Current Model 门禁

只有同时满足以下条件，才更新 `current-synthesis.md`：

1. item 影响当前判断、边界、冲突或下一步优先级。
2. claim 有明确 verification path。
3. 文本保留来源限制。
4. `update-log.md` 记录模型变化和 source lead。

重要但未验证的博主观点，优先写 `open-question` 或 `model-candidate`。

## 收尾汇报

每次运行都要汇报：

- 每日报告路径；
- 收集/跳过了多少 item；
- 写了哪些 research files；
- model candidates 和 bridge candidates；
- 访问失败、缺依赖或权限状态；
- 跑了哪些验证。

汇报和日报正文默认中文。源材料是英文时，摘要用中文，短摘录可保留 source-language 原文。

禁止把 X UI 自动翻译、搜索摘要、公开镜像片段、未展开 `显示原文/Show original` 或 `显示更多/Show more` 的文本写入 active research surface。它们只能作为 rejected/blocked 抓取状态供排障查看；不能形成 source lead，也不能触发 company/module/open question 写入。
