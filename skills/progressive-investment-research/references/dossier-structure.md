# Dossier 结构

Dossier 是独立 Research 工作区，不是主知识库。它允许粗糙、冲突和临时判断，但必须让当前模型可恢复。

## 默认骨架

```text
<dossier>/
  context.md
  model-map.md
  current-synthesis.md
  open-questions.md
  update-log.md
  modules/
```

只默认创建这些。以下目录按需创建：

- `models/`：反复复用的计算模型、市场拆解模型或比较框架。
- `materials/`：需要保留原始材料、派生材料或人工笔记时再建。
- `generated/`：需要可重建索引或缓存时再建。
- 审计记录目录：只有用户要求保留审计过程时再建。

不要默认创建 `team-runs/`。Agent findings 是临时输入，不是事实源。

## 文件职责
### `context.md`

接续入口，说明这个 dossier / workspace 的使用方式，而不是研究结论本身。它用于减少跨会话恢复成本：

- 研究对象和边界的一句话说明。
- 默认使用的 skill / workflow。
- 接续时优先读取哪些文件。
- 何时应写入、何时只讨论不写入。
- 本地路径、工具、权限或验证约定。
- 不应破坏的研究口径或用户偏好。

`context.md` 不替代 `current-synthesis.md`。前者回答“下一个 agent 怎么进入这个工作区”，后者回答“当前研究模型是什么”。用户只是提问、讨论或表达直觉时，不默认更新 `context.md`；只有冷启动、接续入口变化、研究范围变化，或用户明确要求写入时才更新。

### `current-synthesis.md`

人类入口，标题为 `# Current Model`。它必须能在 30-60 秒内恢复全局状态：

- 当前一句话判断。
- model map 摘要。
- 我们知道什么。
- 我们不确定什么。
- 当前冲突。
- 最近变化。
- 下一步 3-5 件事。

当它变得太长，说明范围可能需要拆分，或模块内容没有沉淀。

### `model-map.md`

研究地图。说明边界、核心问题、分析轴、模块索引、相关 dossier 和 promote 候选。

它不是报告目录，也不是资料清单。只保留能指导后续研究的结构。

### `modules/`

稳定研究对象，例如公司、技术路线、产业环节、比较模块、场景边界、监管问题。模块应服务当前模型，不要把每篇材料都变成模块。

如果模块中存在关键数字，必须保留数字来源边界。可以在模块内写数字表，也可以建立专门的 `numeric-anchors` 模块。数字表至少包含：指标、数值、单位、时间点、来源、来源类型、复核状态、用途。

### `models/`

可复用的计算模型、市场拆解模型、单位经济、供应链倒推和敏感性分析放在 `models/`。`models/` 不是默认创建目录，但当公式、参数、倒推或敏感性会成为后续依据时，应创建。

模型文件至少说明：

- 服务的问题。
- 公式或逻辑。
- 参数、单位、数值、来源类型、来源、复核状态。
- `Calculation Sheet`：当模型包含多步算术、倒推链或口径转换时，用 row-level 表展示完整计算过程。
- 假设与敏感性。
- 当前结果。
- 局限和反证条件。
- 支持或挑战的判断。

模型输出不能直接变成事实。它是基于参数和假设的派生结果，必须标记为 `derived` 或模型输出。

`Calculation Sheet` 可以是 Markdown 表，也可以是 dossier 内部 `data/` 下的 CSV canonical row store。选择规则：

- 小型语义表、少量解释表：留在 Markdown。
- 大型事实表、反复更新的输入行、情景行、输出行：放入 `data/calculation-rows/` 或 `data/calculation-outputs/`。
- 需要反复复算、跨行依赖、low/base/high 联动、敏感性排序或 Monte Carlo：增加薄 Python 脚本，读取 input CSV 并生成 output CSV。

模型 Markdown 不能只给 CSV 链接。它必须说明：每类输入是什么、怎么来的、为什么这样组合、输出公式是什么、结果怎么读、不能怎么误读。CSV / Python 变化后，Agent 必须复算并判断 Markdown 读数是否需要更新。

`Calculation Sheet` / CSV row store 的最低字段：

| 字段 | 说明 |
| --- | --- |
| `row_id` | 稳定行号，如 `CP-03`、`SC-12`，供摘要、审计和下游模块引用 |
| `line_item` | 这一行在算什么 |
| `formula / source` | 公式、原始来源或派生逻辑 |
| `inputs` | 输入数字和口径 |
| `value` | 输出或输入值 |
| `unit` | 单位 |
| `source_status` | `verified-primary` / `needs-primary-check` / `secondary-estimate` / `assumption` / `derived` / `source-lead` |
| `interpretation` | 这一行对判断的含义和误读风险 |

一致性规则：

- 模型内 `Calculation Sheet` 或链接的 CSV row store 是计算事实源；其它表是摘要、读数或可视化。
- `current-synthesis.md`、模块摘要和审计应引用 `row_id`，不要维护第二套手工数字。
- 若需要 Excel、CSV 或 research graph，优先放在 dossier 内部 `data/` 并由模型 Markdown 直接链接；不要在 Markdown 和 CSV 中手工维护两套完整表。
- 如果公式、输入、口径或计算脚本变化，先改 canonical rows / script 并复算，再由 Agent 同步“当前结果”、相关模块和 `update-log.md`。

### `open-questions.md`

真正会影响判断的问题，不是普通待办。每个问题尽量拆成可验证条件：

```markdown
## Q: [会影响判断的问题]
优先级: P0 | P1 | P2
影响: [核心判断 / 模块 / promote 候选]
- [ ] c1: [具体可验证条件]（事实型 | 来源质量型 | 计算型 | 比较型）
- [x] c2: [已验证条件] → [结论] (来源: [文件/段落])
```

`P0` 会改变核心判断；`P1` 会影响置信度或边界；`P2` 补充理解。

### `update-log.md`

模型变化日志，不是编辑记录。只记录对研究认知有意义的变化：

- 新增判断。
- 加强/削弱判断。
- 矛盾或冲突。
- 重要定义澄清。
- 开放问题关闭。
- promote 到主知识库。

## 事实源规则

`context.md` 是入口协议，不是研究事实源。结构化 Markdown 中的研究事实源包括 `current-synthesis.md`、`model-map.md`、`open-questions.md`、模块和模型文件。搜索结果、subagent findings、缓存和生成物必须经主 agent 综合，不能直接覆盖核心文件。

冲突可以存在于 Current Model 中。成熟研究不是没有冲突，而是知道冲突在哪里。

## 范围关系

研究对象可大可小。默认从一个 dossier 开始，只有当 current model 失控时才做 scope refactoring。

拆分时，父子 dossier 平级存在，通过 `model-map.md` 的 `Related Dossiers` 说明关系，不通过深层目录表达世界观。

子 dossier 第一版 Current Model 应说明：

- Parent。
- This dossier covers。
- Inherited assumptions。
- Needs re-validation。

合并时，把稳定判断吸收到保留 dossier，避免双事实源。
