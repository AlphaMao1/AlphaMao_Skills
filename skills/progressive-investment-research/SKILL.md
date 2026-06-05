---
name: progressive-investment-research
description: 构建和维护可累积的研究认知模型。适用于持续投资研究、行业/公司/技术主题研究、独立 Research dossier、Current Model 状态恢复、材料吸收、并行搜索、模型更新、范围拆分合并、promote 到 Obsidian 主知识库前审计，以及用户要求“研究一下/更新模型/现在我们知道什么/把重要成果入库”时使用。
---

# 累进式投资研究

这个 Skill 的目标不是多写一份报告，而是让每次研究都推进同一个可控的认知模型。

核心产物是一个 `dossier`：一组轻量 Markdown 文件，记录某个研究对象的当前模型、证据、冲突、开放问题和判断变化。报告、memo、索引、搜索结果和 Obsidian 笔记都是派生输出，不是模型本身。

## 核心定义

**Model = 当前研究对象的可操作认知状态。**

它回答：我们现在怎么看、知道什么、不知道什么、哪里有冲突、下一步最值得验证什么。它必须能被人类快速恢复，而不是只对 AI 友好。

`context.md` 是接续入口，记录这个 dossier / workspace 为什么存在、默认使用哪个 skill、应该从哪里恢复、哪些写入触发需要用户确认。它不是研究结论事实源，也不是每轮讨论都必须更新。用户只是提问、试探想法或讨论机制时，先回答和澄清；只有冷启动、接续成本高、研究边界/入口变化，或用户明确要求“写入/更新 context”时才改它。`current-synthesis.md` 仍是研究模型的人类入口，标题使用 `# Current Model`。用户问“现在是什么状态”“我们知道什么”“model 是什么”时，优先读它，再按需读 `context.md`、`model-map.md`、`open-questions.md` 和相关模块。

**数字和模型也是事实源的一部分。**

研究材料中的关键数字不能只被压缩成文字判断。遇到收入、CapEx、价格、产能、份额、MAU、token、利用率、毛利、折旧、回收期、良率、交付周期等数字时，应记录来源、来源类型、复核状态和用途。尤其是看起来不像普通公开搜索能轻易得到的数字，要提高敏感性：标明它来自用户材料、公司披露、派生材料、估算还是 agent 推断，不要伪装成公开事实。

计算模型是一等产物。只要一个判断依赖公式、参数、倒推、敏感性或层间传导，就应考虑在 `models/` 建立轻量模型或在模块中记录模型 backlog。建模不是为了精确，而是为了暴露假设、单位、依赖关系、卡点和反证条件。

## 设计原则

### 实用优先

研究工作复杂，但工作流应简单。不要为了完整性创建目录、文件、状态机或团队记录。任何新增文件都必须直接服务于：恢复当前模型、追踪重要判断、保存稳定模块、记录开放问题，或执行 promote。

### 人类可控

用户不能被迫信任一堆散落的 md。阶段性工作结束时，输出或更新当前状态：一句话判断、本轮处理了什么、模型变化、最重要未知、风险和未处理材料。

当完成一轮实质研究、模型判断发生变化、或用户要求“详细汇报 / 阶段性汇报 / 做完必须详细跟我汇报”时，必须使用 `references/output-formats.md` 里的 `Stage Research Report` 标准：用户不打开任何 md，也应能完整理解研究目标、方法、证据、推导、结论、证据边界、与其他研究模块的关系、反证条件、实际文件改动和验证结果。不要只交文件变更清单。

### 重要信号与重要假设注册

当研究推进出会反复影响投资判断的信号或假设时，必须单独沉淀到一个可读入口，默认文件名为 `modules/important-signals-assumptions.md`。它不是新的计算事实源，而是索引/读数层：

- 必须标清与源文件的关系：canonical source 是哪个 `models/`、`modules/` 或 `frameworks/` 文件。
- 必须引用源 `row_id` 或稳定小节名，例如 `CP-SIG-*`、`RPP-IN-*`、`PWM-HC-*`。
- 不得在该文件里创造第二套数字口径；源模型变化时先改源模型，再同步 registry。
- 只收少数会改变结论的 P0/P1 信号和假设，不要把所有计算行搬进去。

默认结构：

```markdown
# Important Signals and Assumptions Registry

## Relationship to Source Files
| registry section | canonical source | relationship |

## P0 Signals
| signal_id | signal | current read | source rows | why it matters | reversal / action |

## P0 Assumptions
| assumption_id | assumption | current value / range | source rows | sensitivity | what would invalidate it |
```

用户问“什么信号算反转”“核心假设是什么”“哪些数字最敏感”“这件事以后要持续跟踪什么”时，优先检查这个 registry，再回源模型。

### 公司页 / Company Watchlist

当研究从行业链条推进到具体可跟踪公司，或用户要求“公司板块 / 每个公司一个独立 md / 是持仓还是关注 / 入场点 / 什么条件兑现才买入”时，默认在 dossier 下创建或更新 `companies/<company-slug>.md`。公司页不是公司简介，而是投资候选卡；它必须引用 `models/`、`modules/` 或公开披露中的事实锚点，不另造第二套数字口径。

公司页至少回答：

- 我们知道什么：收入、利润、毛利、订单、产能、客户、价格、市值等关键事实，标来源和 row_id。
- 当前状态：`holding`、`watchlist`、`candidate`、`monitor`、`avoid` 之一；持仓状态不确定时写 `未确认`，不要假装持仓或空仓。
- 为什么关注：它验证了哪条行业假设或瓶颈链条。
- 核心假设：买入逻辑依赖哪些业务变量；哪些已经验证，哪些仍 open。
- 反证条件：什么发生就降级、移出或禁止加仓。
- 入场纪律：若业务核心假设不变，什么估值/价格/情景下进入深度买入评估；区分静态口径和 forward 口径。
- 监控清单：每次财报或重大公告要刷新哪些变量。

价格、市值、PE、PB、股息率等市场数据是高漂移数据。写入公司页时必须标明 snapshot 日期和 `needs refresh before trade`；交易前必须重新刷新，不得把旧行情当当前价格。

若一个价格判断依赖公式，例如 `可接受市值 = forward 扣非利润 × 目标 PE`，应把公式写清楚；若该公式会被复用或影响多家公司，应考虑沉淀到 `models/`，公司页只引用输出。

### 默认路径，不做仪式

标准研究循环是：

1. 定位：这个问题落在 map 的哪里？
2. 处理：读取材料、搜索、比较或解决冲突。
3. 综合：区分事实、判断、假设和未知。
4. 更新：只在模型真的变化时更新 Current Model、模块、开放问题或更新日志。

不要每次机械跑完整流程。没有模型变化就说明没有变化。

### 冷启动先建 Map

冷启动不是 tracer bullet。用户通常会给足量启动材料，先处理第一批材料，建立最小 `model-map.md` 和第一版 `Current Model`，再逐点填充。

最小 map 只需回答：研究边界、核心问题、主要分析轴、首批开放问题。不要假装已经形成完整判断。

### 证据分层

优先使用本地 dossier 和用户提供材料。外部搜索只在材料不足、过期、冲突或需要验证时使用。

| 来源类型 | 用途 | 风险 |
| --- | --- | --- |
| 原始来源 | 事实锚点，如公告、监管文件、原始数据、访谈纪要 | 可能片面或过时 |
| 公司披露 | 公司事实、产品、财务、路线 | 有叙事偏向 |
| 专家/人工笔记 | 经验判断、隐性知识 | 可验证性不稳定 |
| 派生材料 | Deep Research、NotebookLM、摘要、二手报告 | 容易循环引用 |
| Agent 推断 | 结构化判断和假设 | 必须标明，不可当事实 |

遇到冲突时，不要强行调和。记录双方证据、临时判断和需要什么证据解决。

### 数据获取层

数据获取层的目标不是再造搜索器，而是把外部材料转换为可审计证据对象，再由主 agent 判断是否更新模型。

线上公开版默认不要求任何专用搜索或本地解析工具。优先使用当前 agent runtime 已有的搜索、浏览、URL 读取和本地文件读取能力；如果安装了 AnySearch、web-access、markitdown、pdf/docx/xlsx/pptx 等工具，可以把它们作为加速器使用。没有这些工具时，不要中断工作：改用可用的公开搜索、浏览器、官方页面、用户手工导出文件或普通文件读取能力，并在 Source Card 中标明 `acquisition_method` 和限制。

AnySearch 是可选发现/初筛工具：适合实时搜索、批量搜索、垂直域查询和已知 HTML URL 正文抽取。使用垂直域时先调用 `list_domains`，严格遵守返回的 `sub_domain`、query format 和 region；只有 CN 域才使用 `--zone cn`。AnySearch 的金融垂直结果可作为价格、市值、估值倍数、行情和财务摘要的快速 snapshot，但默认属于高漂移或 vendor/聚合数据，不能直接替代公司披露、监管文件或模型内 `Calculation Sheet`。

当研究需要年报、季报、公告、招股书、财报电话会、投资者活动、研报、付费专业站点、播客访谈或终端导出时，先按 `references/data-acquisition-layer.md` 判断来源层级、权限状态和可自动化程度。搜索结果、二手报道、研报和专业站点内容默认产生 `source-lead`、`Claim Row` 或 `open_question`；只有经过来源分层、口径归一、引用锚定和必要复核后，才允许形成 `Model Patch Candidate`。

付费/授权内容只在用户已有授权、登录态或本地导出的前提下 intake；不要设计或执行绕过付费墙、规避终端权限、抓取禁止自动化站点的路径。Bloomberg、FactSet、Wind、Choice、Capital IQ 等终端数据默认走 API、Excel、CSV/XLS 或用户导出导入，不做屏幕抓取或爬虫。

### 数字敏感性

对以下数字默认提高来源敏感性：

- 非公开感数字：私营公司收入、毛利、客户数、合同金额、云 credits、采购承诺、真实成交价、产能分配。
- 口径易混数字：CapEx、PPE、finance lease、operating lease、uncommenced lease、purchase commitment、ARR、RPO、backlog、run-rate、GMV、MAU、DAU、token 调用量。
- 模型输入数字：价格、利用率、吞吐、功耗、PUE、折旧、良率、交付周期、单位消耗系数。
- 模型输出数字：回收期、盈亏平衡价、需求倒推、供应链缺口、市场空间。

记录数字时至少保留：数值、单位、时间点、来源、来源类型、复核状态、是否为假设/估算/模型输出。无法复核时不要删除，但要标记为 `needs-primary-check`、`secondary-estimate` 或 `assumption`。

### 缺数时的估算标准

公开搜索或一手披露无法取得完整输入时，不要直接停止，也不要拍一个高层数字。默认继续建立 `evidence-weighted estimate`：从可验证锚点、来源线索和低层假设出发，用显式公式计算区间或情景。研究型 model 的目标不是只收集 exact data；很多关键数据永远不会完整公开，必须在证据边界内合理推算。

估算输入的优先级：

- `reported-anchor`：上一季度/上一年度披露、公司公告、财报、官方规格、公开价格、订单、RPO、CapEx、收入、成本、token、MAU 等可核验锚点。
- `source-lead`：权威媒体、产业访谈、内部人士转述、付费研究摘要或用户材料中的数字线索；可用于约束区间，但必须标明来源质量和 freshness date。
- `derived`：由 reported-anchor 或 source-lead 通过公式推导出的输入，例如 run-rate、增速、单位成本、coverage ratio。
- `model-assumption`：低层、可解释、可敏感性分析的假设，例如增长率、付费率、ARPU、unit serving cost、utilization、折旧年限、客户-backed 比例。

允许的做法：

- 用上一期披露值加增长率区间估算本期收入或成本。
- 用用户数、tokens、公开价格、折扣区间和单位 serving cost 估算收入、毛利或 compute cost。
- 用订单/RPO、CapEx、租赁承诺、交付周期和客户背书比例估算 coverage、cash pressure 和 commitment quality。
- 用 base / bear / bull 或 low / mid / high 情景展示结果，并标明哪些参数最影响结论。

禁止的做法：

- 直接假设市场份额、利润池分配比例、赢家权重、行业利润率、暴露强弱或置信度，再把它们当作计算底稿输入。
- 用专家判断、1-5 分评分、抽象“强/中/弱”或主观概率补产能、订单、收入、成本、毛利、利用率、交付周期等硬缺口。
- 把 source-lead 或 model-assumption 写成已核验事实。

每个估算输出都应能回溯为：

```text
reported-anchor / source-lead
+ low-level model-assumption
+ formula
= derived estimate / scenario output
```

如果连 reported-anchor、source-lead 或可解释的低层假设都没有，才停在 `missing` 或 `披露不足，无法计算`。

默认完成标准：

- 能搜到就优先搜，且优先一手来源。
- 搜不到 exact data 时，寻找上一期披露、相邻口径、经营指标、管理层口径、可信 source lead 或用户材料。
- 仍缺精确值时，用 low / base / high 情景和敏感性继续推进。
- 只有当缺口无法找到任何锚点，也无法构造可解释低层假设时，才把具体行停在 `missing`；不要让整个模型停在中间。
- 不要把“数据不完整”当作无结论的理由；应输出“在当前锚点和假设下，结论是什么、最敏感的假设是什么、什么证据会推翻它”。

### 建模

常见建模对象：

- 单位经济：单 GPU、单机架、单客户、单 workflow、单 token 或单任务。
- CapEx 回收：现金支出、租赁、采购承诺、backlog、ARR、收入确认和回收期。
- 供应链倒推：从 token / revenue / workload 需求倒推 GPU、HBM、CoWoS、基板、电力、液冷、机架和许可。
- 瓶颈迁移：判断哪个环节最慢、扩产后瓶颈转移到哪里。
- 敏感性：哪些参数变化会改变结论，哪些参数只是二阶影响。

模型文件默认放在 `models/`，只在确实有可复用公式、参数表、敏感性或倒推关系时创建。临时口算可以留在回答里，但如果会成为后续研究依据，应沉淀。

当模型包含多步算术、倒推链或口径转换时，必须加入 `Calculation Sheet` 或等价的 canonical row store。小型、语义性、便于人读的表可以继续放在 Markdown；大型事实表、反复更新的输入行、情景行或输出行应迁到 dossier 内部 `data/`，并在模型 Markdown 中直接链接同一份 CSV，不在 Markdown 中维护第二套完整表格。

CSV 不是附件，而是 dossier 内的 canonical rows。Markdown 仍然是模型说明书和人类恢复入口：必须解释这些数是什么、从哪里来、为什么这样算、结果是什么意思、哪里可能误读。不要让模型 Markdown 只剩 row_id 或 CSV 链接。

只有当计算会反复复算、跨行依赖、low/base/high 情景联动、敏感性排序、Monte Carlo 或一改输入会影响多处输出时，才增加 Python。Python 只能做薄的机械计算层：读取 input CSV、按显式公式生成 output CSV、提供 `--check` 检查 output 是否由当前 input 和脚本生成。研究判断、公式解释和结论读数仍写在 Markdown，不藏进脚本。

CSV + Python 维护规则：input CSV 或脚本变化后，Agent 必须先复算并运行 `--check`；再由 Agent 判断 Markdown 中的读数 / 结论 / 反证条件是否需要更新。Markdown 的读数允许人工维护，但必须明确它是模型读数，不是自动生成的第二套 output table。

#### CSV / Python 数据维护协议

默认采用“小表 Markdown，中型结构化块，大表 CSV，必要时 Python”的分层：

- Markdown 表格只保留小型语义表、读者导览、结论摘要、反证条件和少数关键 row 引用；不要用 Markdown 维护几十行以上、会持续更新、需要排序筛选或会被多个模型引用的事实表。
- `data/markdown-tables/` 存放从 Markdown 迁出的行级事实表、索引表、来源表和非生成型矩阵表。它们仍是 dossier 内部数据层，不是散乱附件。
- `data/calculation-rows/` 存放 canonical input rows。输入可以人工维护，但必须有稳定 `row_id` / `input_key`、单位、来源状态和解释。
- `data/calculation-outputs/` 存放 generated output rows。输出不手工编辑；要改结果，先改 input CSV 或脚本，再重新生成。
- `scripts/calc_*.py` 只做确定性计算：读取 input CSV，按显式公式生成 output CSV，并提供 `--check` 检查输出是否由当前 input 和脚本生成。

是否 Python 化按必要性判断，而不是按“有表就脚本化”：

- 应 Python 化：跨行公式、low/base/high 情景、重复复算、单位换算链、四舍五入敏感、一改输入会影响多个输出、会改变 readout 的模型输出。
- 可只用 CSV：事实表、来源索引、公司/产品矩阵、披露缺口、非生成型指标表、手工维护的 canonical input rows。
- 不应 Python 化：`披露不足，无法计算` 行、范围索引、source-lead 记录、评分/赢家矩阵、判断型 readout、没有公式依赖的小型语义表。

模型 Markdown 不能只剩 CSV 链接。每个使用 CSV/Python 的模型 Markdown 必须保留：

- 这个模型回答什么问题。
- 输入口径和单位定义。
- 中文公式解释：这个数是什么、怎么来的、为什么这样算。
- 输出读法：结果说明什么、不说明什么。
- 关键敏感参数和反证条件。
- canonical input / generated output 链接。
- 复算命令和校验命令。
- 维护规则：input 或脚本变化后，哪些 readout / conclusion 需要 Agent 判断是否更新。

迁移和重构验收默认执行：

- 备份或确认已有可恢复点；大规模迁移前优先生成 dossier 级备份。
- 对迁移表，抽取或脚本对比旧 Markdown 表和新 CSV，确认行数、列名和单元格内容一致；若有差异，必须分类为：预期口径修正、备份后已有更新、Obsidian 链接化、或异常。
- 对 Python 化表，运行生成命令和 `--check`，并把 output 与旧 canonical 表对应值对比；若脚本发现旧手算漂移，优先修正 canonical CSV，再同步相关 readout 和 `update-log.md`。
- 运行所有相关 `calc_*.py --check`、`py_compile`、CSV 链接存在性检查。
- 文件迁移后检查旧路径缺失是否已由 archive 或新位置承接；不要留下未交代的丢失文件。

Obsidian 友好原则：

- Markdown 中直接链接 CSV，让 Obsidian / CSV 插件查看同一份 canonical rows；不要在 Markdown 里复制第二套完整表格。
- 用户需要判断时，Markdown 应给足过程和解释，而不是只列 row_id。
- 工具查看方式、插件说明、临时操作提示不要写进研究正文；正文只保留研究内容、数据入口和维护命令。

维护规则：

- 一个模型只保留一个 canonical calculation sheet / row store；其它表是读数、摘要或可视化。
- 派生行必须标明公式，输入行必须标明来源状态。
- 同一数字若在模块、Current Model 和模型中出现，以模型内 `row_id` 为可追溯入口。
- 如果公式、输入或脚本变化，先更新 canonical rows / calculation script 并复算，再由 Agent 同步“当前结果”和 `update-log.md`。
- 不为没有算术依赖的小型判断强行套表，避免 ceremony。

#### models/ 文件标准

`models/` 只存放可复算模型，或明确标注为非 canonical 的辅助文件。canonical 模型必须从底层事实数据、来源线索或低层情景假设出发，通过显式公式计算输出。

每个 canonical 模型至少包含：模型卡、输入表、计算底稿、输出表、来源状态、局限和反证条件。计算底稿必须使用稳定 `row_id`，并区分 `一手已核验`、`derived`、`source-lead`、`model-assumption`、`missing`、`披露不足，无法计算`。

禁止把高层判断、赢家名单、分配比例、主观评分、置信度、暴露强弱或行业结论直接放进计算底稿。评分表只能作为旧索引或解释材料，必须明确 `non-canonical`，且不得被 `current-synthesis.md`、`model-map.md` 或其它模型当作计算事实源引用。

如果缺少产能、订单、积压订单、收入拆分、成本、毛利、利用率或交付周期，优先按“缺数时的估算标准”寻找 reported-anchor、source-lead、derived 和低层 model-assumption 建立情景估算；若这些也不足，模型必须停在 `missing` 或 `披露不足，无法计算`。不能用专家判断、1-5 分评分或高层比例补洞。

允许的输入包括：公司披露、官方规格、公开价格、订单/积压订单、收入/成本/利润、产能/良率/交期、可标注来源状态的 source lead，以及低层情景假设。允许的输出必须能回指到 `row_id` 和公式。

### Grill Me / 研究对话

`grill me` 不是审计，也不是反方报告。它是和用户对话推进研究模型的机制：把用户对行业的先验、直觉、经验判断、风险偏好和隐含假设问出来，再和 dossier、公开证据、计算模型一起校准。用户的先验可能对，也可能错；处理方式是标明来源和状态，而不是直接采纳或直接否定。

开始 grill 的时机：

- 已经读过当前 dossier 或冷启动材料，能指出问题落在哪个分析轴，而不是空白提问。
- 用户明确说 `grill me`、让我问你、我们讨论一下、帮我把想法问出来。
- 开放问题不是纯公开事实，而是依赖用户的行业经验、投资偏好、判断框架或对某个数字的来源记忆。
- 研究模型出现多条合理分支，继续搜索前需要知道用户更相信哪条机制、为什么。
- 有非公开感数字、派生估算或模型参数，但关键缺口是“这个数字为什么可信/来自什么场景/你当时怎么理解”，而不是简单公开核验。

不触发 grill 的情况：

- 问题可以通过读取本地材料、运行脚本或公开搜索解决。
- 当前还没读材料，无法提出高杠杆问题。
- 只是需要审计、反方、来源核验或一致性检查；那应走审计或 subagent。
- 用户只要结论或 status，且没有暴露需要用户先验补足的缺口。

Grill 默认一次只问 1 个问题；如果用户要求一轮问题，最多问 3-5 个互不依赖的问题。每个问题应说明：问题、为什么问、影响模型、你可以怎样回答、如果暂时不知道怎么办。回答后，主 agent 负责把内容标为 `user-prior`、`judgment`、`assumption`、`source-lead` 或 `open_question`，再决定是否更新模型。


## 默认 Dossier

默认只创建：

```text
<dossier>/
  context.md
  model-map.md
  current-synthesis.md
  open-questions.md
  update-log.md
  modules/
```

`models/`、`materials/`、`generated/`、审计记录目录等都按需创建。`team-runs/` 不作为默认机制；如果某个环境的团队 agent 好用，也只能作为临时发现来源，不是事实源。

结构化 Markdown 是事实源。`context.md` 是接续协议和入口说明，不承载研究事实结论；事实结论仍以 `current-synthesis.md`、`model-map.md`、模块、开放问题和模型文件为准。缓存、索引、搜索结果和 agent findings 不能直接覆盖模型，必须由主 agent 综合后再写入核心文件。

## 工作流入口

- 普通研究：如果存在 `context.md`，先读它恢复工作区入口和写入规则；再读 `current-synthesis.md` 和 `model-map.md`，定位相关模块，只处理必要材料。
- 冷启动：处理用户给的启动材料，建立最小 `context.md`、map、第一版 Current Model 和开放问题。
- status：不做新研究，只恢复并汇报当前模型状态。
- modeling：当判断依赖数字、公式、倒推或敏感性时，建立或更新轻量计算模型。
- grill：通过一问一答抽取用户先验、经验判断和隐含假设，推进开放问题和模型分支选择。
- major update：当判断被新增、加强、削弱或矛盾时，提出模型更新；若该判断会成为后续依据、来源薄弱、存在冲突或影响 promote，先审计。
- promote：把 Research dossier 中少量高价值成果提升到 Obsidian 主知识库。promote 前必须审计。
- scope：当研究范围过大、过小或边界漂移时，诊断 keep / split / merge / archive。
- archive：把不应默认恢复的生成物、历史审计、旧 handoff 和非 canonical 派生材料移入 `archive/`，默认不读取；标准见 `references/archive.md`。

详细流程见：

- `references/workflows.md`：冷启动、日常研究、status、promote、scope。
- `references/dossier-structure.md`：文件职责和默认骨架。
- `references/update-policy.md`：更新分级、冲突和审计触发。
- `references/agent-collaboration.md`：Codex subagent 使用规则。
- `references/output-formats.md`：状态、阶段性研究汇报、更新、审计、promote 输出格式。
- `references/data-acquisition-layer.md`：搜索、披露、研报、授权站点和终端导入如何转换为证据对象。
- `references/source-adapter-backlog.md`：数据获取工具链的优先级、MVP 和不做事项。

## Subagent 使用

Subagent 是增强手段，不是事实源。

- 搜索型 subagent：适合并行查不同公司、政策、竞品、论文、价格、案例。可以使用较低成本模型。只返回 findings。
- 审计型 subagent：适合重大模型更新、promote 前、冲突判断、用户要求反方检查。必须独立上下文、只读、输出反对点和证据缺口。
- 主 agent 负责综合、采纳或拒绝 findings，并决定是否更新模型。

不要默认使用 Agent Teams。不要让 subagent 并发编辑核心 dossier。

## 常用命令

```bash
python scripts/scaffold_dossier.py <path> --title "<topic>"
python scripts/validate_dossier.py <path>
python scripts/regenerate_index.py <path> --stdout
```

脚本只做确定性工作。研究判断仍以 Markdown 文本为准。

## 默认回答形态

普通回答保持轻量：

```markdown
## 定位
相关分析轴 / 模块 / 开放问题：

## 回答
已有模型结论：
新增材料或推理：
未知与证据缺口：
投资含义：

## 模型状态
no model change / minor update / major update / requires restructure
建议补丁：
```

阶段性状态使用 `Status Brief`。完成一轮实质研究、模型判断发生变化、或用户要求详细汇报时，使用 `Stage Research Report`，确保用户不打开 md 也能理解研究过程和结论。只有确实需要更新模型时，才展开完整更新提案。
