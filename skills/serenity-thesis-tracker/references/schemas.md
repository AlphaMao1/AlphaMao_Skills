# Schemas

## Thesis Schema

```yaml
thesis_id: "SIVE-001"
ticker: "SIVE"
thesis_title: "CPO光收发器客户扩展驱动TAM指数级增长"
thesis_summary: "Sivers正在与新的pluggable光收发器公司合作，Jabil 1.6T LRO验证了其激光器护城河，预计更多光收发器公司将宣布采用SIVE激光器"
direction: "bullish"          # bullish / bearish / neutral / mixed
horizon: "中期"               # 短期(<3M) / 中期(3-12M) / 长期(>12M) / 未说明
confidence: "high"            # high / medium / low / unclear
thesis_type: "TAM_expansion"  # 见下方类型列表
source_status_ids: 
source_urls: 
original_quotes: 
first_mentioned: "2026-06-01"
latest_update: "2026-06-01"
status: "active"              # active / strengthened / weakened / revised / contradicted / closed
materiality_score: 13
```

### thesis_type 枚举

- revenue_growth：收入增长驱动
- margin_expansion：毛利/利润率扩张
- TAM_expansion：可寻址市场扩大
- supply_chain_inflection：供应链拐点
- customer_win：客户导入/设计赢得
- product_cycle：产品周期/技术迭代
- valuation_mispricing：估值错误定价
- short_seller_rebuttal：反驳做空报告
- competitive_advantage：竞争优势/护城河
- catalyst_driven：催化剂驱动
- risk_or_bear_case：风险/看空逻辑

## Claim Schema

```yaml
claim_id: "SIVE-001-C1"
thesis_id: "SIVE-001"
ticker: "SIVE"
claim_text: "SIVE正在与新的pluggable光收发器公司合作（co-development/qualification阶段）"
claim_category: "customer_relationship"  # 见下方类型列表
verification_method: "客户公告、订单披露、收入增长、毛利率变化"
required_data_sources: "公司公告、财报、行业新闻"
baseline_value: "当前已知客户：Jabil、Ayar Labs"
tracking_variable: "SIVE pluggable transceiver客户数"
trigger_condition: "任何光收发器公司宣布使用SIVE激光器"
expected_timeframe: "2026Q3-Q4"
current_status: "unverified"  # unverified / partially_verified / verified / contradicted / stale
evidence_log: []
source_urls: 
```

### claim_category 枚举

- company_fact：公司事实（客户、产品、产能）
- industry_variable：行业变量（TAM、渗透率、技术路线）
- customer_relationship：客户关系/导入
- financial_forecast：财务预测（收入、利润）
- margin_assumption：毛利/利润率假设
- product_milestone：产品里程碑
- valuation_assumption：估值假设
- risk_factor：风险因素

## Ticker Mention Schema

```yaml
ticker: "SIVE"
company_name: "Sivers Semiconductors"
mention_count: 5
first_mentioned_at: "2026-06-01T08:32Z"
last_mentioned_at: "2026-06-01T14:33Z"
related_status_ids: 
associated_keywords: 
sentiment: "bullish"
materiality_score: 14
```

&nbsp;