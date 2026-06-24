from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR))

from scripts.report_generator import MarketSizingData, ReportGenerator


def build_sample() -> MarketSizingData:
    return MarketSizingData(
        market_name="中国示例新兴服务市场",
        geography="中国大陆",
        base_year=2026,
        forecast_years=5,
        tam=9.6,
        sam=5.76,
        som=0.288,
        unit="亿元",
        cagr=0.08,
        core_insight="该模型用于演示公式链，不代表真实市场结论。",
        market_segments=[
            {
                "name": "核心场景 A",
                "base_value": 6.0,
                "growth_rate": 0.10,
                "logic": "对象数、渗透率和年费相乘得到，代表主要需求池。",
            },
            {
                "name": "验证场景 B",
                "base_value": 3.6,
                "growth_rate": 0.05,
                "logic": "由相邻场景 proxy 推导，适合作为早期切入市场。",
            },
        ],
        market_definition={
            "产品/服务": {"in": "目标服务年费", "out": "硬件一次性收入"},
            "地理": {"in": "中国大陆", "out": "港澳台及海外"},
            "客户/用户": {"in": "目标城市核心人群", "out": "非目标场景用户"},
        },
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
                "transform_note": "筛选目标城市后换算为亿人，示例中简化为 1.0 亿人。",
                "used_in": "base_pop",
            },
            {
                "source_id": "SRC-002",
                "provider": "Comparable market scan",
                "dataset_or_title": "相邻市场渗透率对比",
                "metric": "penetration benchmark",
                "geography": "China",
                "period": "latest available",
                "unit": "%",
                "value_or_path": "A/B 类产品 60%/40% 对比",
                "url_or_endpoint": "manual research notes",
                "accessed_at": "2026-06-24",
                "transform_note": "根据目标市场差异下调至 20%。",
                "used_in": "pene_rate",
            },
        ],
        assumptions=[
            {
                "key": "base_pop",
                "name": "基础人口",
                "numeric_value": 1.0,
                "unit": "亿人",
                "source_ref": "SRC-001",
                "logic": "从总人口中筛出目标城市和相关消费场景后换算。",
                "used_in": "TAM",
            },
            {
                "key": "core_pop_pct",
                "name": "核心人群占比",
                "numeric_value": 0.40,
                "unit": "%",
                "logic": "按年龄、收入、使用场景三层筛选，保留 40%。",
                "used_in": "TAM",
            },
            {
                "key": "pene_rate",
                "name": "付费渗透率",
                "numeric_value": 0.20,
                "unit": "%",
                "source_ref": "SRC-002",
                "logic": "甲市场 A/B 渗透率约 60%/40%；乙市场更适合 B 的低部署成本，但教育成本更高且面临 C 替代冲击，所以基准取 20%。",
                "used_in": "TAM",
            },
            {
                "key": "freq",
                "name": "年购买频次",
                "numeric_value": 12,
                "unit": "次/年",
                "logic": "按月度订阅或月度复购处理。",
                "used_in": "TAM",
            },
            {
                "key": "price",
                "name": "单次价格",
                "numeric_value": 100,
                "unit": "元",
                "logic": "参考公开价格带，取可持续付费中位水平。",
                "used_in": "TAM",
            },
            {
                "key": "sam_ratio",
                "name": "可服务比例",
                "numeric_value": 0.60,
                "unit": "%",
                "logic": "扣除暂不可覆盖地域、渠道和客户类型后，约 60% 可服务。",
                "used_in": "SAM",
            },
            {
                "key": "som_share",
                "name": "年度可获取份额",
                "numeric_value": 0.05,
                "unit": "%",
                "logic": "按销售产能、渠道进入速度和竞品集中度，年度可获取份额取 5%。",
                "used_in": "SOM",
            },
            {
                "key": "cagr",
                "name": "年增长率",
                "numeric_value": 0.08,
                "unit": "%",
                "logic": "由目标人群扩大、渗透率提升和价格变化三项合成。",
                "used_in": "Forecast",
            },
        ],
        side_checks=[
            {
                "method": "相邻市场收入上限检查",
                "result": "主模型低于相邻成熟市场收入量级",
                "interpretation": "说明示例市场仍处早期，量级没有超过可比市场约束。",
            }
        ],
    )


if __name__ == "__main__":
    output_dir = SKILL_DIR / "output"
    results = ReportGenerator().generate(build_sample(), output_dir, formats=["xlsx", "md"])
    for kind, path in results.items():
        print(f"{kind}: {path}")
