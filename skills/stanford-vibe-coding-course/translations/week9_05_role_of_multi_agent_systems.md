# Week 9-5: The Role of Multi-Agent Systems in AI-Native Engineering
# 多智能体系统在构建 AI 原生工程中的角色

> **Original Link**: [https://resolve.ai/blog/role-of-multi-agent-systems-AI-native-engineering](https://resolve.ai/blog/role-of-multi-agent-systems-AI-native-engineering)
> **Title**: The role of multi agent systems in making software engineers AI-native
> **Author**: Resolve AI Team
> **Week**: 9
> **Reading Time**: 12 min
> **Priority**: High
> **Translation Date**: 2026-02-03

---

## 什么是 AI 原生 (AI-Native) 工程？为什么它很重要？
**AI 原生工程** 是指工程师主要通过与 AI 交互来编排他们的工作：无论是编写代码还是处理生产系统。这与仅仅“使用 AI”（即 **AI 辅助**）有显著区别。

-   **AI 辅助 (AI-Assisted)**：你使用 AI 工具来更快地完成任务。工作流程仍然是以人为中心的：工程师 -> 系统和工具 -> 关联 -> 行动。
-   **AI 原生 (AI-Native)**：AI 成为你进行生产工作的主要界面。工作流程变为 AI 主导：工程师 -> 自然语言请求 -> AI 系统 -> 响应/行动。工程师设定目标，让 AI 代理处理操作性工作。

例如，在事件响应中：
-   **AI 辅助**：你仍在生成假设，决定哪些证据重要，并手动关联跨工具的信号。AI 帮助检索数据，但你做繁重的调查工作。
-   **AI 原生**：AI 代理自动鉴别调查优先级，并行生成竞争假设，并根据跨系统证据迭代细化理论。你不再问“你能分析这些日志吗？”，而是说“解决这个结账失败问题”，然后代理协调整个调查。

这种转变需要 **持久的 AI 代理 (Persistent AI Agents)**，而不仅仅是 AI 工具。虽然 LLM 可以加速单个任务，但只有有状态的代理才能维持调查上下文，跨多个工具协调，并自主执行复杂的多步工作流程。

## 为什么多智能体系统 (Multi-Agent Systems) 对于 AI 原生至关重要？
现代生产系统表现出学术界所说的“不可约的相互依赖性 (irreducible interdependence)”：理解它们需要跨领域的专业知识，无法统一成单一的连贯模型。
没有单一的 AI 工具可以在协调调查的同时维持跨所有这些领域的专家级知识。

随着系统复杂性的增加，单个 AI 工具面临上下文需求的指数级增长。这就是多智能体系统可以通过结合 **协调 (coordination)** 和 **个人领域专业化 (individual domain specialization)** 来扩展的地方。

每一级架构都有不同的可扩展性上限：
-   **LLMs**：缺乏持久状态。
-   **工具增强的 LLM**：无法在多次对话中维持调查上下文。
-   **单智能体 (Single Agents)**：随着系统复杂性增长，成为决策瓶颈。顺序推理限制了它们。
-   **多智能体系统 (Multi-Agent Systems)**：突破了限制之前所有方法的顺序推理约束。它们启用 **并行假设测试**，而单智能体必须顺序调查，这使得单智能体根本不适合生产事件的时间需求。

## 构建多智能体系统是一个艰难的工程问题
构建生产就绪的多智能体系统需要深厚的领域专业知识和 AI 工程能力的罕见结合：

1.  **领域专业知识决定架构**：如果没有理解生产现实，你就无法架构代理。只有在凌晨 3 点调试过生产环境的人才知道，日志模式和指标异常需要根本不同的调查策略。
2.  **AI 专业知识让代理协同工作**：一旦分解了问题，你就碰到了计算机科学的硬部分。代理之间的上下文传播不是直觉，而是管理信息的有向无环图 (DAG)。编排并行代理需要正式的协调协议来防止竞争条件和死锁。
3.  **交集创造突破性系统**：突破发生在你结合两者时：知道数据库连接池在负载下做什么（领域），并构建可以与部署时间线分析和上游服务验证协调池健康检查的代理——所有这些都在并行运行而互不干扰（AI 系统）。

在 Resolve AI，我们的团队包括拥有超过 20 年生产系统经验的工程师，共同创建 OpenTelemetry 的创始人，以及具有 Deep AI 专业知识的研究人员（Google DeepResearch 和 Gemini Agents 背后的大脑）。这种组合使我们能够构建这样的系统。
