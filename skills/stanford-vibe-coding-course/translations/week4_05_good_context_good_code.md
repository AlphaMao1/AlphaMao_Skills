---
原文链接: https://blog.stockapp.com/good-context-good-code/
原文标题: Good context leads to good code: How we built an AI-Native Eng Culture
所属周次: Week 4
阅读时间: 12min
优先级: ⭐必读
翻译日期: 2026-02-03
---

# 好的上下文带来好的代码：我们如何建立 AI 原声工程文化 (Good Context Good Code)

**来源**: StockApp Engineering Blog

## TL;DR (太长不看版)
创建 StockApp 给了我们要给从头开始建立 **AI 原生 (AI-native)** 开发文化的机会。我们的经验是，这比手动开发效率高约 **2.5倍**，比仅仅用 AI 增强现有开发流程效率高约 **2倍**。
AI 原生开发不是要取代工程师——而是通过精心制作的共享上下文，建立系统的**人机协作 (Human-AI Collaboration)**。为了做到这一点，我们不得不做出一些改变：
- **单体仓库 (Monorepo)**: 将所有的代码、技术文档和 Agent 指南组织在一个单体仓库中。这是人与 Agent 的共享工作区。
- **高层设计优先**: 从高层设计开始，在这个层面上与 Agent 对齐，然后向下工作到代码。
- **全面使用 Agent**: 尽可能在任何地方使用 Agent，但要**监督和审计**它们的工作。
- **MCP 与工具**: 设置 MCP 服务器和命令行工具，给 AI 提供它需要的上下文。
- **多 Agent 审查**: 使用多个不同的 Agent 来审查工作。人类+多 Agent 集成 (Ensembles) 始终优于单一 Agent。

## 详情 (Details)
StockApp 始于 2025 年 1 月。我们没有将 AI 工具改造进现有的流程，而是架构了我们整个开发工作流以系统地利用人机协作。
虽然衡量开发者的生产力出了名地困难，但我们的主观经验（辅以客观测量）指向了大约 2.5 倍的生产力收益。
我们的核心洞察是：**好的代码是好的上下文的副作用 (Good code is a side effect of good context)。**
新的 AI 原生开发过程是关于人类和 Agent 如何共同通过渐进式地构建和共享上下文。当做得有效时，优质的软件工件会自然涌现。

有一点需要强调：这种方法需要**更多**的软件工程专业知识，而不是更少。有效地定义上下文在技术上至少与编写好代码一样具有挑战性：你需要仔细考虑什么是最关键的信息，以及 Agent 将如何解释它。而且，Agent 搞砸时的“爆炸半径”可能很大（行为不端的 Agent 曾几次摧毁了我们的开发数据库）。

## 我们学到的五个原则

### 1. 仓库是人类和 Agent 的共享工作区
我们的仓库不仅是为人类组织的，也是为机器组织的，因为 AI 的性能严重依赖于可访问的上下文。这就是为什么**上下文工程 (Context Engineering)** 现在比 Prompt 工程更重要。
自然语言与编程语言一样关键，所以我们要像对待 TypeScript 或 Python 一样对待英语散文。
关键上下文存储在：
- `docs/designs/`: 产品需求、高层目标和 Schema。这是“为什么”和“什么”。
- `docs/plans/`: 详细的、分阶段的实施计划，通常由人类和 Agent 共同生成。这是“怎么做”。
- `docs/guides/`: API 和工具的教程。
- `schema.sql`: 整个项目的单一、规范的 Schema。
- `README.md` & `CLAUDE.md`: 放置在整个代码库中，为特定部分提供本地化指令。

### 2. 分层开发允许渐进式构建上下文
更好的上下文带来更好的代码。我们采用自上而下的工作方式：
1. **设计 (Design)**: 人类提供需求；Agent 起草设计文档；双方迭代并提交。
2. **计划 (Plan)**: Agent 将设计转化为分阶段的任务；人类审查并批准。
3. **实施 (Implement)**: Agent 处理大部分编码；人类审查结果。
4. **兜底 (Backstop)**: 测试和其他保障措施确保后续更改不会侵蚀来之不易的上下文。
5. **审查 (Review)**: 人类和 Agent 进行最终审查。
6. **更新与完善**: 更新文档、CLAUDE.md 和 Schema。

### 3.除非有充分理由，否则一切都使用 Agent
我们几乎在工作的所有方面都使用 Agent。
- Agent 是很好的想法在回音壁。
- Agent 编写我们的大部分 Commit 和 PR 信息。
- 我们指示 Agent 更新文档而不是自己编辑。
- 我们指示 Agent 更新 `CLAUDE.md` 文件。
- 我们**不写 Prompt**。我们要求 Agent 考虑到上下文和我们的“元 Prompt”来为我们编写 Prompt。
- 我们让 Agent 编写测试，但要注意防止它们“过度 Mock”。
- **调试是联合活动**: 通常人类提出根本原因的假设，然后要求 Agent 验证。Agent 在插桩（Instrumentation）方面非常出色。

### 4. MCP 和命令使理解和增强上下文变得更容易
我们广泛使用 MCP 服务器。我们有一个 `install_mcp.sh` 脚本来安装我们使用的约 6 个服务器，包括：
- **Notion 和 Linear**: 获取决策上下文并更新状态。
- **AWS 和 SQL Dev 数据库**: Agent 可以直接读取日志和数据来调试。
- **Git 和 GitHub**: 研究以前的版本，查看 Commit 历史。

### 5. 集成优于个体 (Ensembles outperform individuals)
就像在机器学习中集成方法（如随机森林）优于单个分类器一样，只要分类器有足够的差异性，集成就会产生更好的结果。
我们使用 **Zen MCP Server** 让 Claude Code 能够寻求其他 LLM（如 Gemini 和 o3）的反馈。
例如，在实现 Auth 时，Gemini 强烈推荐基于 Payload 的验证，而 o3 更谨慎，推荐每用户客户端。不同的视角有助于发现盲点。
最终，人类和 Agent 形成了一个集成。让这个集成表现优于任何个体的桥梁就是**共享上下文**。

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Monorepo | 单体仓库 | 将多个项目存储在同一个代码仓库中的策略 |
| Context Engineering | 上下文工程 | 设计和组织信息以最大化 AI 理解和输出质量的实践 |
| Ensembles | 集成/合奏 | 结合多个模型或 Agent 的预测以提高整体性能的方法 |
| Blast Radius | 爆炸半径 | 错误发生时可能影响的系统范围 |
| Instrumentation | 插桩 | 在代码中插入监控或日志语句以诊断行为 |
