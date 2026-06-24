# market-sizing

Excel-first TAM/SAM/SOM market sizing skill.

## What It Does

- Builds a first-principles market sizing model under uncertainty.
- Uses Excel formulas as the primary calculation surface.
- Creates a first-sheet `核心结论` overview with annual TAM/SAM/SOM and TAM composition.
- Produces a Markdown memo that explains market definition, source cards, formulas, assumptions, side checks, and sensitivities.
- Allows assumptions, but requires logic for rates, shares, adoption, penetration, and market share.
- Uses deterministic scenarios and side checks instead of Monte Carlo.

## What It Does Not Do

- No Monte Carlo.
- No HTML report or visual UI.
- No confidence labels as a substitute for reasoning.
- No static or cumulative TAM/SAM/SOM numbers when annual formulas can be built.

## Main Files

```text
market-sizing/
├── SKILL.md
├── references/
│   ├── methodology.md
│   ├── data_sources.md
│   ├── fermi_patterns.md
│   └── industry_templates.md
├── scripts/
│   ├── data_fetcher.py
│   ├── fermi_calculator.py
│   ├── generate_template.py
│   └── report_generator.py
└── templates/
    └── market_sizing_report.md
```

## Dependencies

Required:

```bash
pip install openpyxl pandas
```

Optional data helpers:

```bash
pip install fredapi wbdata akshare yfinance pytrends
```

## Minimal Usage

```python
from scripts.report_generator import MarketSizingData, ReportGenerator

data = MarketSizingData(
    market_name="Example Market",
    geography="China",
    base_year=2026,
    forecast_years=5,
    tam=9.6,
    sam=5.8,
    som=0.3,
    unit="亿元",
    cagr=0.08,
    market_segments=[
        {"name": "核心场景 A", "base_value": 6.0, "growth_rate": 0.10, "logic": "对象数 x 采用率 x 年费。"},
        {"name": "验证场景 B", "base_value": 3.6, "growth_rate": 0.05, "logic": "由相邻场景 proxy 推导。"},
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
            "value_or_path": "API series",
            "url_or_endpoint": "https://api.worldbank.org/v2/country/CN/indicator/SP.POP.TOTL",
            "accessed_at": "2026-06-24",
            "transform_note": "Converted to 100m people.",
            "used_in": "base_pop",
        }
    ],
    assumptions=[
        {"key": "base_pop", "name": "基础人口", "numeric_value": 1.0, "unit": "亿人", "source_ref": "SRC-001", "logic": "目标城市人口换算。"},
        {"key": "core_pop_pct", "name": "核心人群占比", "numeric_value": 0.40, "unit": "%", "logic": "年龄、收入和场景筛选。"},
        {"key": "pene_rate", "name": "付费渗透率", "numeric_value": 0.20, "unit": "%", "logic": "参考相邻市场 40%，因教育成本和替代品冲击折半。"},
        {"key": "freq", "name": "年购买频次", "numeric_value": 12, "unit": "次/年", "logic": "按月度订阅处理。"},
        {"key": "price", "name": "单次价格", "numeric_value": 100, "unit": "元", "logic": "公开价格带中位数。"},
        {"key": "sam_ratio", "name": "可服务比例", "numeric_value": 0.60, "unit": "%", "logic": "扣除不可服务地域、渠道和客户。"},
        {"key": "som_share", "name": "年度可获取份额", "numeric_value": 0.05, "unit": "%", "logic": "按销售产能、竞品份额和进入节奏估算。"},
        {"key": "cagr", "name": "年增长率", "numeric_value": 0.08, "unit": "%", "logic": "用户增长、价格变化和渗透率提升合成。"},
    ],
)

ReportGenerator().generate(data, "./output", formats=["xlsx", "md"])
```
