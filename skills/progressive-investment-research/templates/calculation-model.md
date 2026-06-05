---
type: calculation-model
status: draft
---

# 计算模型：{{TITLE}}

## 模型卡

| 项目 | 内容 |
| --- | --- |
| 这个模型在讲什么 |  |
| 初始假设 |  |
| 计算方法 |  |
| 当前结论 |  |
| 最重要的读法 / 误读风险 |  |

## 服务的问题

## 公式或逻辑

## 参数

| 参数 | 单位 | 数值 | 时间点 / 口径 | 来源类型 | 来源 | 复核状态 | 敏感性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  | 用户估计 / 原始来源 / 公司披露 / 专家访谈 / 派生材料 / agent 推断 |  | verified-primary / needs-primary-check / secondary-estimate / assumption / derived | 高 / 中 / 低 |

## 假设

## Calculation Sheet

如果模型包含多步算术、倒推链或口径转换，在这里保留 canonical calculation rows，或链接到 dossier 内部 `data/` 下的 CSV row store。下游摘要、审计和 `current-synthesis.md` 优先引用 `row_id`，不要复制出另一套手工数字。

若使用 CSV / Python：

- input rows: `[filename.csv](../data/calculation-rows/filename.csv)`
- output rows: `[filename.csv](../data/calculation-outputs/filename.csv)`
- recompute: `python scripts/<model_calc>.py`
- check: `python scripts/<model_calc>.py --check`

Markdown 必须解释：这些输入是什么、怎么来的、为什么这样算、输出结果是什么意思、哪些读数需要避免误读。CSV 或脚本变化后，Agent 先复算和 check，再判断下面的读数是否需要更新。

| row_id | line_item | formula / source | inputs | value | unit | source_status | interpretation |
| --- | --- | --- | --- | ---: | --- | --- | --- |
|  |  |  |  |  |  | verified-primary / needs-primary-check / secondary-estimate / assumption / derived / source-lead |  |

## Calculation Sheet 读数

| row_id | 输出 | 当前结论 | 需要避免的误读 |
| --- | --- | --- | --- |
|  |  |  |  |

## 当前结果

## 敏感性

| 变量 | 变化范围 | 结果影响 | 是否改变判断 |
| --- | --- | --- | --- |
|  |  |  |  |

## 局限

## Grill / 研究对话

- 需要向用户确认的行业先验：
- 需要向用户追问的来源记忆：
- 用户回答归类：user-prior / judgment / assumption / source-lead / open_question
- 若无法回答，下一步公开核验或敏感性处理：

## 支持或挑战的判断

## 相关模块

## 最近更新
