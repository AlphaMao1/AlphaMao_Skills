# 数据源与 Source Card 指南

市场规模测算的数据源不是为了追求完美，而是为了让每个输入有来路、能换算、能被复查。没有直接数据时，可以用 proxy 和假设，但必须说明为什么这是当前最好可用路径。

## 数据源优先级

1. 官方统计、官方 API、监管披露、政府开放数据。
2. 上市公司年报、招股书、公告、投资者材料。
3. 行业协会、交易所、海关、专门数据库。
4. 有方法说明的咨询/券商/研究报告。
5. 新闻、访谈、专家判断、价格页、招聘/搜索/流量等 proxy。
6. 显式假设。

低优先级数据不是不能用。真正的问题是：口径是什么、怎么进入公式、是否有更好的替代、对结论影响多大。

## Source Card 字段

| 字段 | 说明 |
|------|------|
| `source_id` | 稳定编号，如 `SRC-001` |
| `provider` | 数据提供方 |
| `dataset_or_title` | 数据集、报告、页面或文件名称 |
| `metric` | 具体指标 |
| `geography` | 地理口径 |
| `period` | 数据期间或版本 |
| `unit` | 原始单位 |
| `value_or_path` | 原始数值、表格位置、API 参数或文件路径 |
| `url_or_endpoint` | URL、API endpoint 或本地文件 |
| `accessed_at` | 访问日期 |
| `last_updated_or_vintage` | 可得时记录 |
| `transform_note` | 换算、筛选、合并、通胀调整、汇率处理 |
| `used_in` | 对应假设 key 或公式行 |

## 常用公共数据路线

| 路线 | 适用 | 备注 |
|------|------|------|
| World Bank API | 国家人口、GDP、宏观指标 | 无 key，适合跨国基本盘 |
| FRED / ALFRED | 美国宏观、利率、价格、产业序列 | FRED 需要免费 API key；ALFRED 可查历史 vintage |
| DBnomics | 多机构宏观数据聚合 | 统一 API，可覆盖 World Bank、IMF、OECD 等数据集 |
| OECD Data API | OECD 国家结构性指标 | SDMX API，适合政策、产业、劳动力、教育等指标 |
| IMF DataMapper / SDMX | IMF 宏观、WEO、金融统计 | 适合宏观口径和国际比较 |
| UN Comtrade | 进出口、HS 商品贸易 | 适合硬件、原材料、设备市场的外贸 side check |
| Eurostat | 欧盟统计 | 适合欧洲人口、行业、消费和企业数据 |
| US Census / BEA / BLS | 美国人口、行业、企业、工资、消费 | 官方 API，适合美国市场 |
| 国家统计局 / 地方统计局 | 中国人口、宏观、行业产量 | 优先使用原始表格；AkShare 可作为抓取封装 |
| SEC EDGAR / CNInfo | 上市公司披露 | 适合竞品收入、分部收入、客户结构 |
| yfinance / AkShare / TuShare / Baostock | 公司财务、行情、A 股数据 | 用于快速拉取，不替代对原始披露的复查 |
| Google Trends / pytrends | 搜索热度 proxy | 只用于相对趋势，不直接当市场规模 |

## 选择数据源的方法

1. 先问模型需要什么变量，而不是先逛数据源。
2. 对每个变量找最直接数据；找不到时找能解释机制的 proxy。
3. 记录原始口径，不要只记录最后数字。
4. 做单位换算时写在 `transform_note`，并在 Excel 里尽量保留换算公式。
5. 数据冲突时优先比较口径、年份、覆盖范围和一手性；无法消解时保留冲突并解释采用哪一个。

## API 使用建议

- 能用官方 API 时优先用官方 API。
- Python 包可以提高效率，但不要让包名代替 source card。source card 记录的应是原始 provider 和数据集。
- 对 AkShare 这类大型封装，不要凭函数名猜含义；先搜索函数、读取返回列、核对官网或数据说明，再纳入模型。
- 对付费报告摘要，只能引用公开可见内容；不可编造页码或内部数据。

## 公开参考入口

- World Bank API: `https://api.worldbank.org/v2/`
- FRED API: `https://fred.stlouisfed.org/docs/api/fred/`
- DBnomics: `https://db.nomics.world/`
- OECD Data API: `https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html`
- IMF DataMapper API: `https://www.imf.org/external/datamapper/api/help`
- UN Comtrade API: `https://comtrade.un.org/`
- UN Comtrade Python package: `https://github.com/uncomtrade/comtradeapicall`
- SEC EDGAR APIs: `https://www.sec.gov/edgar/sec-api-documentation`
