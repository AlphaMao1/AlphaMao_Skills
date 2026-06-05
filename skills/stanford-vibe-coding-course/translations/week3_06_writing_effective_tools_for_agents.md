---
原文链接: https://www.anthropic.com/engineering/writing-tools-for-agents
原文标题: Writing effective tools for agents — with agents
所属周次: Week 3
阅读时间: 20min
优先级: ⭐必读
翻译日期: 2026-02-03
---

# 与 Agent 一起为 Agent 编写有效的工具 (Writing Effective Tools for Agents)

**来源**: Anthropic Engineering
**包含**: 核心原则、工具开发指南、优化策略

**什么是工具？**
在计算中，确定性系统（如函数 `getWeather("NYC")`）每次给定相同的输入都会产生相同的输出。
工具反映了确定性系统与**非确定性 Agent** 之间的契约。当用户问“我今天应该带伞吗？”时，Agent 可能会调用天气工具，也可能根据常识回答，或者先问地点。
这意味着我们需要从根本上重新思考软件编写方式：不是像为其他开发者编写 API 那样编写工具和 [MCP 服务器](https://modelcontextprotocol.io/)，而是需要**为 Agent 设计它们**。

我们的目标是增加 Agent 在解决广泛任务时的有效表面积。幸运的是，对 Agent 最“符合人体工程学”的工具，对人类来说通常也出奇地直观。

## 如何编写工具 (How to write tools)

### 1. 构建原型 (Building a prototype)
如果不亲自动手，很难预料哪些工具对 Agent 来说是顺手的。
- **使用 Claude Code**: 为 Claude 提供你工具依赖的库、API 或 SDK 的文档。LLM 友好的文档通常可以在 `llms.txt` 中找到（例如 [Anthropic 的 llms.txt](https://docs.anthropic.com/llms.txt)）。
- **本地测试**: 将工具包装在本地 MCP 服务器中，使用 `claude mcp add <name> <command>` 连接到 Claude Code 进行测试。

### 2. 编写有效工具的原则 (Principles)

#### 选择正确的工具
更多工具并不总是带来更好的结果。常见的错误是仅仅包装现有的 API 端点。
- **Agent 的限制**: LLM Agent 的上下文（Context）是有限的。如果一个工具返回所有联系人列表让 Agent 逐个 Token 阅读，那是对有限上下文的浪费（就像暴力搜索）。
- **自然的方法**: 应该实施 `search_contacts`（搜索联系人）或 `message_contact`，而不是 `list_contacts`（列出所有联系人）。

**合并功能**: 工具可以在底层处理多个离散操作。
- 不要实现 `list_users`, `list_events`, `create_event`。
- 而是实现 `schedule_event`（安排日程），它负责查找可用性并安排事件。
- 不要实现 `read_logs`，而是实现 `search_logs`，只返回相关的日志行和周围的上下文。
- 不要实现 `get_customer_by_id`, `list_transactions`, `list_notes`，而是实现 `get_customer_context`，一次性编译客户的所有近期相关信息。

**清晰且独特**: 确保每个工具都有明确、独特的用途。重叠的工具会分散 Agent 的注意力。

#### 优化工具响应以提高 Token 效率
优化上下文的**质量**很重要，优化返回给 Agent 的上下文**数量**也很重要。
- **实施截断**: 结合分页、范围选择、过滤和/或截断。对于 Claude Code，默认将工具响应限制为 25,000 个 Token。
- **有用的错误信息**: 如果工具调用引发错误（例如输入验证），请通过 Prompt 工程设计错误响应，以清楚地传达具体的、可操作的改进，而不是不透明的错误代码。

#### 对工具描述进行 Prompt 工程
这是改进工具最有效的方法之一：**对工具描述和规范进行 Prompt 工程**。
- **显式化上下文**: 将你可能隐式带入的上下文（专用查询格式、利基术语定义、底层资源之间的关系）显式化。
- **避免歧义**: 明确描述预期输入和输出。特别是参数命名应明确：用 `user_id` 代替 `user`。

### 3. 评估与迭代 (Running an evaluation)
一旦原型完成，运行全面的评估来衡量后续更改的影响。
与 Agent 一起工作，你可以重复评估和改进工具的过程，直到你的 Agent 在现实世界的任务中达到强大的性能。

## 结论
为 Agent 编写工具需要一种新的思维方式：
1.  **高杠杆率**: 设计能让 Agent 以类似人类方式解决任务的工具。
2.  **上下文效率**: 通过聚合、过滤和截断来尊重 Agent 的 Token 预算。
3.  **描述即 Prompt**: 将工具定义视为给 Agent 的指令，清晰、明确、无歧义。

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Deterministic System | 确定性系统 | 相同输入产生相同输出的系统（如传统代码） |
| Non-deterministic Agent | 非确定性 Agent | 相同输入可能产生不同输出的 AI 系统 |
| Context Window | 上下文窗口 | LLM 一次能处理的信息量上限 |
| Tool Ergonomics | 工具人体工程学 | 工具设计对 Agent 使用的友好程度 |
| Token Efficiency | Token 效率 | 在完成任务前提下最小化 Token 消耗 |
