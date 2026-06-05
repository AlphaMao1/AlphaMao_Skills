# Why This Matters - 前置解释参考

> 供 Agent 在推送 "Needs Context" 类型阅读前查阅

| 文件 | Why This Matters |
|------|------------------|
| week1_05_openai_codex | Codex 是 GitHub Copilot 的前身。理解它的能力边界和设计理念，能帮你明白 AI Coding 工具的演化路径，以及为什么现代 Agent 需要更多上下文。 |
| week3_03_devin_coding_agents_101 | Devin 是首个被称为 "AI Software Engineer" 的产品。理解它的架构（长时任务、工具链、自主调试）能帮你明白 Agent 自主性的边界在哪里。 |
| week4_04_super_claude | 这不是配置教程。SuperClaude 框架解决两个核心问题：**Context Pollution**（上下文污染）和 **多工作流并行管理**。它是 "Agent 管理 Agent" 的原型。 |
| week9_04_your_new_autonomous_teammate | 这是 Resolve AI 的产品介绍，但核心价值是展示 **AI On-call** 的愿景：Agent 能自动诊断、修复问题，人类只需审批关键决策。重点理解自动化运维的可能性，而非产品本身。 |

## 使用方法

Agent 发送材料前检查 content-audit.md：
1. 如果类型是 🔧 Needs Context，先从本文件获取 "Why"
2. 用对话形式解释给用户
3. 然后再推送材料
