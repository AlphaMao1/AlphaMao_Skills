# Market Sizing

用 Excel 公式链做可复核的 TAM / SAM / SOM 市场规模测算。

这个 Skill 适合在市场还不清晰、公开数据不完整、但你需要先判断规模量级时使用。它不会把一个拍脑袋数字包装成精确预测，而是把市场边界、数据来源、假设逻辑和计算公式拆开，最后落到一个可以继续调整的 Excel 模型里。

## 适合

- 估算一个新市场、细分市场或新产品方向的规模
- 给投资研究、立项、商业计划或战略讨论准备 TAM / SAM / SOM
- 把零散公开数据、行业报告、类比市场和业务假设整理成可审计模型
- 需要逐年输出未来 5 年市场规模，而不是只给一个末年数字
- 需要 Excel 作为最终承载，方便继续改参数、看公式、做情景分析

## 不适合

- 只想要一句“市场很大”的结论
- 没有市场定义，也不准备先拆边界
- 把行业报告里的总市场直接当成自己的 SAM
- 用复杂图表或概率模拟替代清楚公式链

## 它会做什么

1. 先定义市场边界：产品、地域、客户、时间口径和单位。
2. 选择计算架构：Top-down、Bottom-up、替代法、价值链法或价值基础法。
3. 建 `source card`：记录每个进入模型的数据来源、口径、访问日期和转换方式。
4. 写 `assumption ledger`：每个渗透率、采用率、份额、价格、频次都必须有来源或推导逻辑。
5. 生成 Excel 模型：关键输出由公式驱动，不是手填静态数。
6. 输出 Markdown 备忘：解释市场定义、公式链、核心假设、side check 和敏感变量。

## 核心产物

默认 Excel 工作簿包含这些工作表：

| 工作表 | 用途 |
| --- | --- |
| `核心结论` | 第一页总览，展示逐年 TAM / SAM / SOM、TAM 构成和一句话判断 |
| `Market_Definition` | 市场边界、地理范围、客户口径、时间口径和单位 |
| `Source_Cards` | 数据来源、原始口径、访问日期和转换说明 |
| `Assumptions` | 可调假设、数值、单位、来源和逻辑 |
| `Calculation_Model` | 中间计算链和公式 |
| `TAM_SAM_SOM` | 年度 TAM / SAM / SOM 明细 |
| `Checks` | source、logic、单位、层级和构成合计检查 |

Markdown 备忘用于给人读，Excel 才是模型本体。报告里的关键数字应能回到 Excel 的某个输入、公式或检查项。

## 怎么触发

在支持 `SKILL.md` 的 Agent 中，可以这样说：

```text
帮我测算这个市场的 TAM/SAM/SOM
给这个产品做一个市场规模模型，最后要 Excel
估算未来 5 年市场规模，并拆出 TAM 构成
重新审查这个市场规模假设，看看数据源和公式链有没有问题
```

## 安装

在 Agent 中安装：

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/market-sizing
```

如果手动复制，保持整个目录结构不变，至少需要保留：

```text
market-sizing/
├── SKILL.md
├── README.md
├── agents/
├── references/
├── scripts/
├── templates/
└── examples/
```

## 依赖

生成 Excel 需要：

```bash
pip install openpyxl pandas
```

如果要辅助抓取公开数据，可以按需安装：

```bash
pip install fredapi wbdata akshare yfinance pytrends
```

这些库只负责提高取数效率。进入模型的每个关键数据，仍然需要写入 `source card`。

## 快速试跑

在 skill 目录下运行示例：

```powershell
cd skills/market-sizing
python examples/formula_first_sample.py
```

示例会在 `output/` 下生成 Excel 和 Markdown。`output/` 是本地生成物，不应提交到仓库。

## 目录说明

```text
market-sizing/
├── SKILL.md                         # Agent 使用的主说明
├── README.md                        # 给开源用户看的入口说明
├── agents/openai.yaml               # Codex / OpenAI Agent 元数据
├── references/
│   ├── methodology.md               # 市场定义、公式链和假设纪律
│   ├── data_sources.md              # 常用数据源和 source card 要求
│   ├── fermi_patterns.md            # 常见 Fermi 拆解模式
│   ├── industry_templates.md        # SaaS、B2B、消费、硬件等模板
│   └── presentation_guide.md        # 如何解释模型
├── scripts/
│   ├── report_generator.py          # Excel + Markdown 生成器
│   ├── data_fetcher.py              # 数据源辅助工具
│   ├── fermi_calculator.py          # Fermi 计算辅助
│   └── generate_template.py         # Excel 模板生成器
├── templates/
│   └── market_sizing_report.md      # Markdown 备忘模板
└── examples/
    └── formula_first_sample.py      # 公式链示例
```

## 质量要求

- 市场边界必须先写清楚，再计算。
- TAM / SAM / SOM 默认是年度口径，预测期内要逐年列出。
- TAM 如果由多个细分市场组成，组成项要能对回总 TAM。
- Excel 关键输出必须是公式，不是硬编码结果。
- 渗透率、采用率、可服务比例、可获取份额等假设不能裸写数字，必须有类比、来源或推导逻辑。
- 数据不完美可以使用，但要说明它如何进入公式、影响哪个结论。
- side check 用来发现口径差异，不用来强行调参。

## 小红书讲解

一个 Skill 搞定 Market Sizing

<http://xhslink.com/o/9zGJ009rm21>

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
- [scripts/](./scripts/)
- [templates/](./templates/)
- [examples/](./examples/)
