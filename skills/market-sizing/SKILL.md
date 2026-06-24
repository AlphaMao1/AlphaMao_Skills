---
name: market-sizing
description: 市场规模测算工具 (TAM/SAM/SOM)。适用于用户提到「市场规模」「market size」「TAM」「SAM」「SOM」或需要估算目标市场大小时使用。
---

# Market Sizing

这个 skill 的目标不是制造精确幻觉，而是在市场不确定时，基于清楚的市场定义、可复核的数据和自洽的公式链，建立一个可在 Excel 中继续推演的规模量级判断。

## 工作原则

- 先定义市场，再找数据，再建公式。市场边界不清时，不开始计算。
- Excel 是核心交付物，所有 TAM/SAM/SOM 关键数值必须由公式承载；Markdown 只解释公式、来源和判断。
- Excel 第一页必须是 `核心结论` 总览页：用一页展示未来 5 年逐年 TAM/SAM/SOM、TAM 由哪些市场组成、各市场逐年规模和一句话判断。
- 可以做假设，但不能跳步骤。比例、渗透率、市占率、采用率等必须写出来源、类比、约束或推导逻辑。
- 不使用 Monte Carlo，不输出 HTML/UI。敏感性用 Excel 中的确定性情景和关键驱动测试表达。
- 不给必要但 imperfect 的数据贴无意义的「低可信」标签。重点判断是：这是当前最好可用数据吗？如何被转换进公式？哪些结论最受它影响？
- 交叉验证用于发现口径差异，不用于强行调参让两个结果一致。

## 必读参考

- `references/methodology.md`：第一性原理、公式链和假设纪律。
- `references/data_sources.md`：数据源层级、source card 和常用 API 路线。
- `references/fermi_patterns.md`：人口、机构、替代、价值链、价值基础等分解模式。
- `references/industry_templates.md`：SaaS、Marketplace、Consumer、B2B、Hardware 的常见变量。

## 标准流程

### 1. 锁定市场边界

必须明确：

- 产品/服务：包含什么，排除什么。
- 地理范围：国家、区域、城市或全球口径。
- 客户/使用者：B2B/B2C、细分人群、机构类型、购买主体。
- 时间口径：基准年、预测期、现价/不变价、年化/一次性。
- 单位：金额、销量、用户数、设备数、容量或其他。

如果边界有两种合理解释，先拆成两个口径，不要混在一个数字里。

### 2. 选择计算架构

优先选择能解释市场形成机制的方法：

- Top-down：行业总量 -> 细分口径 -> 可服务范围。
- Bottom-up：客户/用户/设备数 -> 采用率/频率 -> 单价/ARPU。
- Substitution：现有市场 -> 替代率 -> 价格或价值调整。
- Value-chain：终端市场 -> 价值环节占比 -> 可服务部分。
- Value-based：目标对象数 -> 问题频率/损失/收益 -> 愿付比例。

常用做法是主模型 + 一条 side check。side check 可以很粗，但必须能解释结果是否在合理量级。

### 3. 建 source card

每条进入模型的数据都要能追溯到 source card：

| 字段 | 要求 |
|------|------|
| `source_id` | 稳定编号，如 `SRC-001` |
| `provider` | 数据提供方 |
| `dataset_or_title` | 数据集、报告或页面名称 |
| `metric` | 使用的指标 |
| `geography` / `period` / `unit` | 口径 |
| `value_or_path` | 数值或提取路径 |
| `url_or_endpoint` | URL/API endpoint/文件路径 |
| `accessed_at` | 访问日期 |
| `transform_note` | 如何清洗、换算、筛选 |
| `used_in` | 用于哪个假设或公式 |

### 4. 写 assumption ledger

每个假设至少包含：

```python
{
    "key": "pene_rate",
    "name": "目标市场渗透率",
    "numeric_value": 0.20,
    "unit": "%",
    "source_ref": "SRC-003",
    "logic": "甲市场 A/B 渗透率约 60%/40%；乙市场更适合 B 的低部署成本，同时面临 C 替代冲击，且当前教育成本更高，所以基准假设取 20%。",
    "used_in": "TAM"
}
```

禁止「裸比例」：`pene_rate = 5%` 这种没有上下文的假设不能进入最终模型。

### 5. 生成 Excel 模型

使用 `scripts/report_generator.py`：

```python
from scripts.report_generator import MarketSizingData, ReportGenerator

data = MarketSizingData(
    market_name="中国某新兴服务市场",
    geography="中国大陆",
    base_year=2026,
    forecast_years=5,
    tam=9.6,
    sam=5.76,
    som=0.288,
    unit="亿元",
    cagr=0.08,
    market_definition={
        "产品/服务": {"in": "目标服务年费", "out": "硬件一次性收入"},
        "地理": {"in": "中国大陆", "out": "港澳台及海外"},
    },
    market_segments=[
        {
            "name": "核心场景 A",
            "base_value": 6.0,
            "growth_rate": 0.10,
            "logic": "由对象数、采用率、年费三项相乘得到，代表最大组成市场。",
        },
        {
            "name": "验证场景 B",
            "base_value": 3.6,
            "growth_rate": 0.05,
            "logic": "由相邻场景 proxy 推导，体量较小但更适合早期验证。",
        },
    ],
    source_cards=[
        {
            "source_id": "SRC-001",
            "provider": "World Bank",
            "dataset_or_title": "Population, total",
            "metric": "SP.POP.TOTL",
            "geography": "China",
            "period": "2024",
            "unit": "people",
            "value_or_path": "1.408B",
            "url_or_endpoint": "https://api.worldbank.org/v2/country/CN/indicator/SP.POP.TOTL",
            "accessed_at": "2026-06-24",
            "transform_note": "换算为亿人后进入 base_pop",
            "used_in": "base_pop",
        },
        {
            "source_id": "SRC-002",
            "provider": "内部筛选逻辑",
            "dataset_or_title": "目标人群筛选假设",
            "metric": "核心人群占比",
            "geography": "中国大陆",
            "period": "基准年",
            "unit": "%",
            "value_or_path": "40%",
            "url_or_endpoint": "logic-only",
            "accessed_at": "2026-06-24",
            "transform_note": "按年龄、收入和使用场景三层筛选。",
            "used_in": "core_pop_pct",
        },
        {
            "source_id": "SRC-003",
            "provider": "Comparable market scan",
            "dataset_or_title": "相邻市场渗透率对比",
            "metric": "penetration benchmark",
            "geography": "中国大陆",
            "period": "latest available",
            "unit": "%",
            "value_or_path": "相邻市场约 40%",
            "url_or_endpoint": "manual research notes",
            "accessed_at": "2026-06-24",
            "transform_note": "因教育成本和替代品冲击下调至 20%。",
            "used_in": "pene_rate",
        },
        {
            "source_id": "SRC-004",
            "provider": "业务机制假设",
            "dataset_or_title": "购买频次假设",
            "metric": "年购买频次",
            "geography": "中国大陆",
            "period": "基准年",
            "unit": "次/年",
            "value_or_path": "12",
            "url_or_endpoint": "logic-only",
            "accessed_at": "2026-06-24",
            "transform_note": "按月度订阅或月度复购处理。",
            "used_in": "freq",
        },
        {
            "source_id": "SRC-005",
            "provider": "公开价格页/价格带",
            "dataset_or_title": "目标服务价格假设",
            "metric": "单次价格",
            "geography": "中国大陆",
            "period": "基准年",
            "unit": "元",
            "value_or_path": "100",
            "url_or_endpoint": "manual pricing notes",
            "accessed_at": "2026-06-24",
            "transform_note": "取公开价格带中位数。",
            "used_in": "price",
        }
    ],
    assumptions=[
        {"key": "base_pop", "name": "基础人口", "numeric_value": 1.0, "unit": "亿人", "source_ref": "SRC-001", "logic": "只计入目标城市人群，按总人口筛选后换算。"},
        {"key": "core_pop_pct", "name": "核心人群占比", "numeric_value": 0.40, "unit": "%", "source_ref": "SRC-002", "logic": "按年龄、收入和场景三层筛选得到。"},
        {"key": "pene_rate", "name": "付费渗透率", "numeric_value": 0.20, "unit": "%", "source_ref": "SRC-003", "logic": "参考相邻市场 40% 渗透率，并因教育成本和替代品冲击折半。"},
        {"key": "freq", "name": "年购买频次", "numeric_value": 12, "unit": "次/年", "source_ref": "SRC-004", "logic": "按月度订阅/复购频率处理。"},
        {"key": "price", "name": "单次价格", "numeric_value": 100, "unit": "元", "source_ref": "SRC-005", "logic": "参考公开价格带的中位数。"},
        {"key": "sam_ratio", "name": "可服务比例", "numeric_value": 0.60, "unit": "%", "logic": "扣除非目标渠道、地域和暂不可服务客户。"},
        {"key": "som_share", "name": "年度可获取份额", "numeric_value": 0.05, "unit": "%", "logic": "按目标进入节奏、销售产能和竞品份额推导。"},
        {"key": "cagr", "name": "年增长率", "numeric_value": 0.08, "unit": "%", "logic": "由用户增长、价格变化和渗透率提升合成。"},
    ],
)

ReportGenerator().generate(data, output_dir="./output", formats=["xlsx", "md"])
```

默认工作簿包含：

1. `核心结论`：给用户看的首页，展示逐年 TAM/SAM/SOM、TAM 构成、末年占比和一句话判断。
2. `Market_Definition`：市场边界、地理、客户、时间和单位口径。
3. `Source_Cards`：所有进入模型的数据来源和转换说明。
4. `Assumptions`：所有可调假设及 `logic`。
5. `Calculation_Model`：中间公式链。
6. `TAM_SAM_SOM`：年度 TAM/SAM/SOM 明细，必须是单年口径，不是 5 年合计。
7. `Checks`：公式层级、source、logic、单位和构成合计检查。

### 6. 交付 Markdown 备忘

Markdown 必须回答：

- 未来 5 年每一年的 TAM/SAM/SOM 是多少，不能只写预测期合计或末年数字。
- TAM 由哪几个市场组成，每个市场逐年多大，末年占比是多少。
- 市场边界是什么。
- 核心公式链是什么。
- 哪些数据来自 source card，哪些是推导，哪些是假设。
- TAM/SAM/SOM 是如何从公式得出的。
- side check 是否支持这个量级。
- 哪些变量最能改变结论，以及 Excel 中对应哪个输入单元。

## 质量门

完成前必须检查：

- 没有 Monte Carlo、HTML、Plotly 或展示 UI 作为交付要求。
- 有 `核心结论` 首页，且第一页不堆过程，只放核心读数、年度表、市场构成和一句话判断。
- TAM/SAM/SOM 是逐年单年口径；不得用 5 年累计值冒充年度市场规模。
- 如果 TAM 由多个细分市场组成，组成项合计必须能对回总 TAM；如果对不回，必须解释口径差异并在 Checks 中提示。
- Excel 关键输出单元是公式，不是手填静态值。
- 所有比例、渗透率、采用率、市占率都有 `logic`。
- 假设中的 `source_ref` 能在 source card 中找到，或明确说明为什么只能用逻辑假设。
- TAM >= SAM >= SOM；如果不成立，必须解释口径，否则修正模型。
- 单位换算可追溯，例如人、亿人、元、亿元不能混用。
- side check 与主模型差异较大时，报告差异来源，而不是为了接近结果改假设。

## 常见错误

- 直接写「渗透率 5%」但没有类比市场、竞争约束、采用路径或销售产能逻辑。
- 把行业报告里的总市场直接当成自己的 SAM。
- 只标「数据不确定」却没有说明它如何影响公式。
- 为了看起来专业而输出复杂图表，却没有留下可编辑、可追踪的 Excel 模型。
- 使用旧脚本或旧样例中的 HTML/Monte Carlo 输出。
