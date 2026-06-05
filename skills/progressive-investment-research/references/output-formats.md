# 输出格式

保持短，除非用户要求完整材料。

## Status Brief

```markdown
## 当前状态
一句话判断：

## 本轮处理了什么
- [材料/问题] → [影响]

## 模型变化
- added:
- strengthened:
- weakened:
- contradicted:

## 当前最重要的未知
1.
2.
3.

## 风险
- AI 推断：
- 来源薄弱：
- 未处理材料：
```

## Stage Research Report

用于完成一轮实质研究、模型更新或用户要求“详细汇报”时。目标是让用户不打开任何 md，也能完整理解研究目标、过程、推导、结论、证据边界、与既有模型的关系和下一步。

不要把它写成文件变更清单。文件路径和验证结果放在后面，研究判断放在前面。

```markdown
## 0. 本轮到底研究什么
用 2-5 句话还原真实问题、研究边界和成功标准。
说明这不是在回答什么，避免用户误读任务范围。

## 1. 研究前的模型状态
说明本轮开始前 dossier 已经知道什么、主判断是什么、关键缺口在哪里。
如果有既有 open question / model / module，点名其角色。

## 2. 方法和判断框架
说明本轮如何分层、分类、核验或建模。
列出证据优先级、分类标准、计算口径、升级/降级规则。
如果涉及数字，说明 reported-anchor / source-lead / assumption / formula 的关系。

## 3. 中间推导
按关键结论逐条展开：
- 起点事实或锚点是什么
- 通过什么机制传导
- 可以推出什么
- 不能推出什么
- 为什么上调、下调或保持不变

这一节必须显式区分事实、判断、假设和证据缺口。

## 4. 本轮结论
给出新的分层、排序、判断或模型读数。
如果适合，用一张小表或一段公式化读法呈现。
结论要带限定词，避免把“相关性”“收入”“利润”“稀缺租”“终端 operating surplus”混用。

## 5. 和其他研究模块的关系
说明本轮结论如何连接、支持、削弱或更新已有模型。
至少覆盖最相关的 current model、open questions、计算模型、信号注册表或反证框架。

## 6. 反证条件和敏感变量
说明哪些信号会推翻、削弱或上调本轮结论。
优先写可观测信号：价格、毛利、库存、订单、客户、利用率、续费、RPO、CapEx、监管文件等。

## 7. 实际改了什么
列出更新过的文件和它们承担的角色。
只写关键文件，不展开冗长 diff。

## 8. 验证
列出运行过的验证命令、结果、warning 和残余风险。
如果无法验证，说明原因。

## 9. 仍然没解决什么
列出本轮未闭合的问题、等待的外部证据、下一轮最值得做的工作。
```

使用规则：

- 只有阶段性研究完成、用户明确要详细汇报、或本轮改变了模型判断时才使用；普通问答继续保持轻量。
- 这不是正式 memo，不新增产物文件，除非用户明确要求。它是对本轮工作的可复盘口头交付。
- 用户应该能仅凭这份汇报理解研究过程和结论；不能只说“已更新某某 md”。
- 不要为了套模板硬填空。小任务可合并章节，但必须覆盖：目标、方法、推导、结论、证据边界、与模型关系、反证、文件与验证。
- 如果研究涉及投资判断，必须说明结论的利润性质、证据类型和不可推出的部分。

## Company Page

用于在 dossier 中维护单公司投资候选页，默认路径为 `companies/<company-slug>.md`。公司页不是公司简介，而是可更新的投资状态页。

```markdown
---
type: company
status: watchlist
company:
ticker:
created:
updated:
source:
---

# 公司名（ticker）

## Company Card
| field | current read |
| --- | --- |
| 公司 |  |
| 代码 |  |
| 所属研究模块 |  |
| 当前状态 | holding / watchlist / candidate / monitor / avoid |
| 持仓状态 | holding / no-position / 未确认 |
| 核心问题 |  |
| 规范事实源 | 指向 models/modules rows |

## Why We Care
说明为什么这家公司值得进入研究池：它验证哪条产业链假设、瓶颈、利润迁移或反证。

## What We Know
| row_id | item | current value | source / row |
| --- | --- | ---: | --- |

## Current Valuation Snapshot
标注 snapshot 日期、行情来源和 `needs refresh before trade`。高漂移数据不能写成永久事实。

| row_id | metric | value | source status | note |
| --- | ---: | --- | --- | --- |

## Current Judgment
一句话判断：好公司 / 好价格 / 需等待验证 / 不合适 / 避免。
必须说明不是在推荐交易，而是在维护研究状态。

## Core Hypotheses
| hypothesis_id | hypothesis | current status | what would validate it | what would break it |
| --- | --- | --- | --- | --- |

## Entry Discipline
说明哪些业务条件兑现、哪些估值条件出现，才从关注进入深度买入评估。

静态口径可用：
`可接受市值 = 当前扣非利润 × 目标 PE`
`可接受股价 = 可接受市值 / 最新总股本`

动态口径优先：
`可接受市值 = 可信 forward 扣非利润 × 目标 PE`
`可接受股价 = 可接受市值 / 最新总股本`

## Monitoring Checklist
| item | why it matters | frequency |
| --- | --- | --- |

## Current Action
| action | condition |
| --- | --- |
```

公司页写作规则：

- 状态要明确；持仓状态不知道时写 `未确认`，不要推断。
- 估值必须区分归母净利、扣非净利、经营现金流、分部毛利和一次性收益。
- 入场价格必须带公式和利润口径，不能只写“便宜/贵”。
- 公司页中的行业判断应回指到 `models/` 或 `modules/`，避免同一数字多处维护。
- 每次财报、重大公告或价格刷新后，更新 `updated`、相关 rows 和 `Current Action`。

## Model Update Proposal

```markdown
## 更新类型
minor update / major update / requires restructure

## 受影响位置
- Current Model:
- Modules:
- Open Questions:

## 判断变化
旧判断：
新判断：
关系：adds / strengthens / weakens / contradicts

## 证据
- 来源：
- 来源类型：
- 置信度：

## 冲突与未知

## 是否需要用户确认
```

## Audit Findings

```markdown
## Scope
## Claims Reviewed
## Overreach Or Unsupported Claims
## Evidence Gaps
## Fact/Judgment/Assumption Mixups
## Strongest Counter-Interpretation
## Recommended Changes
```

## Grill Questions

```markdown
1. 问题：
   为什么问：
   影响模型：
   你可以这样回答：
   如果暂时不知道：
```

默认一次只问 1 个问题。只有用户要求“一轮 grill”时，才一次给 3-5 个互不依赖问题。

## Grill Assimilation

```markdown
## 用户回答归类
- user-prior:
- judgment:
- assumption:
- source-lead:
- open_question:

## 对 Current Model 的影响
- added:
- strengthened:
- weakened:
- contradicted:

## 下一步
- 本地材料：
- 公开搜索：
- 数字核验：
- 建模：
```

## Calculation Model Summary

```markdown
## 模型服务的问题

## 核心公式

## 关键参数
| 参数 | 单位 | 数值 | 来源类型 | 复核状态 | 敏感性 |
| --- | --- | --- | --- | --- | --- |

## Calculation Sheet
| row_id | line_item | formula / source | inputs | value | unit | source_status | interpretation |
| --- | --- | --- | --- | ---: | --- | --- | --- |

## 当前结果

## Calculation Sheet 读数
| row_id | 输出 | 当前结论 | 需要避免的误读 |
| --- | --- | --- | --- |

## 最敏感变量

## 局限与反证
```

使用规则：

- 只有存在多步算术、倒推链或口径转换时才展开 `Calculation Sheet`。
- `row_id` 要稳定，方便 `current-synthesis.md`、审计和模块摘要引用。
- Excel / CSV / research graph 是派生视图，不替代 Markdown canonical rows。

## Promote Draft

```markdown
## 候选成果
要 promote 的稳定判断 / 概念 / 模块 / 框架：

## 为什么值得入库

## 审计结果
- 已检查：
- 剩余不确定性：

## Obsidian 落点
- 主 MOC:
- 次级 MOC / 交叉入口:
- 相关已有笔记:

## 入库内容摘要
```

## Scope Refactoring Proposal

```markdown
## 当前范围问题

## 建议
keep / split / merge / archive

## 关系
Parent:
Child / Merge target:

## 最小迁移内容

## 需要重新验证的判断

## 用户确认点
```
