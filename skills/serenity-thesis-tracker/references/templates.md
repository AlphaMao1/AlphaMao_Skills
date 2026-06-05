# Templates

## Company Research File Template

```markdown
# {TICKER} — {company_name}

**供应链位置**: [{chain_theme}](../supply_chain_map/{chain_file}.md) → {layer_description}
**最后更新**: {date}
**Serenity立场**: {direction} | Materiality: {score}/15 ({level})

---

## Serenity 核心观点

{核心投资逻辑，含方向、信心、交易框架。一段话。}

---

## 关键关系（→ 详见 [{chain_theme}](../supply_chain_map/{chain_file}.md)）

| 对手方 | 关系 | 验证状态 | 关键点 |
|---|---|---|---|
| **{TICKER}** | {关系类型} | ✅/❓ {状态} | {一句话} |

---

## Active Thesis

| ID | 标题 | 方向 | 信心 | 状态 | 起始 |
|---|---|---|---|---|---|
| {id} | {title} | {dir} | {conf} | {status} | {date} |

## Claim Ledger

| ID | Claim | 验证状态 | 触发条件 | 下次检查 |
|---|---|---|---|---|
| {id} | {text} | {status} | {trigger} | {date} |

## 推文时间线

| 日期 | 摘要 | 影响 | URL |
|---|---|---|---|
| {date} | {summary} | {impact} | [链接]({url}) |

## 数据跟踪

| 变量 | 当前值 | 检查频率 | 触发阈值 |
|---|---|---|---|
| {var} | {val} | {freq} | {threshold} |

## 复盘记录

| 日期 | 价格 | 验证进展 | 观点状态 |
|---|---|---|---|
| {date} | {price} | {progress} | {status} |

---

## 独立研究（我们自己的验证）

> 以下部分待填充。每次做独立研究后，在此追加。

### 财务数据
*待查*

### 客户验证台账
*待验证*

### 与 Serenity 判断的对比
*待建立*
```

## Supply Chain Map Template

```markdown
# {Theme} 供应链

**最后更新**: {date}
**核心逻辑**: {一句话描述从终局需求到瓶颈的因果链}

---

## 供应链层级与公司定位

（ASCII art 层级图，从 L0 到 L5，标注瓶颈层）

---

## 关键关系（本研究的核心资产）

每条关系都是一个可验证的 claim，验证状态直接影响投资逻辑。

### {TICKER} 的供应关系网络

| 关系 | 方向 | 内容 | 验证状态 | 证据 | 来源 |
|---|---|---|---|---|---|
| {A} → {B} | {类型} | {内容} | ✅/❓ {状态} | {证据} | [推文]({url}) |

### 板块联动关系

| 关系 | 内容 | 来源 |
|---|---|---|
| {A} → {B} | {内容} | [推文]({url}) |

---

## 瓶颈分析

| 瓶颈 | 层级 | 关键公司 | 严重程度 | 状态 |
|---|---|---|---|---|
| {bottleneck} | {layer} | {companies} | {severity} | {status} |

---

## 待验证的关键问题

1. {question}
```

## Daily Report Template (Incremental)

```markdown
# Serenity 每日研究报告 — {YYYY-MM-DD}

## 执行摘要
- 推文总数：{N}条 | 有研究价值：{N}条 | 过滤：{N}条
- 涉及ticker：{N}个 | 新增thesis：{N}个 | 新增claim：{N}个
- **新增/变化的供应链关系**：{N}条

## 今日变化

### {TICKER}（Materiality: {score}, {level}）
- 新增thesis: {id} — {一句话}
- 新增关系: {A}→{B} ({验证状态})
- → 详见 [companies/{TICKER}.md](../companies/{TICKER}.md)

### {TICKER2} ...

## 新增供应链关系

| 关系 | 内容 | 验证状态 | 所在Map |
|---|---|---|---|
| {A} → {B} | {内容} | {状态} | [{theme}](../supply_chain_map/{file}.md) |

## 新增研究任务
-  {task}

## 低价值内容
- 推文#{N}: {一句话}（{content_type}）

## 最值得人工查看的原文链接
1. {url} — {理由}
```

&nbsp;