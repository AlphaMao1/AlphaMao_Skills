---
原文链接: https://github.com/vijaythecoder/awesome-claude-agents
原文标题: Awesome Claude Agents - AI Development Team
所属周次: Week 4
阅读时间: 15min
优先级: ⭐推荐
翻译日期: 2026-02-03
---

# Awesome Claude Agents - AI 开发团队 (AI Development Team)

**来源**: GitHub (vijaythecoder/awesome-claude-agents)
**核心**: 将 Claude Code 转变为一个交付生产就绪功能的 AI 开发团队，并教你如何创建自己的 Agent。

## 一、什么是 Claude Agents？
Claude Agents 是专门的、以任务为中心的 AI “队友”，通过简单的 Markdown+YAML 文件定义。
每个 Agent 生活在 `.claude/agents/` 中，并具有明确的角色、工具集和行为 Prompt。
通过子 Agent 支持，Claude Code 现在可以将复杂的项目委托给并行工作的专家 Agent——就像真正的工程团队一样！

---

## 二、认识你的 AI 开发团队 (Meet Your AI Development Team)

这个仓库提供了 24 个专门的 Agent，分为三类：

### 1. 编排者 (Orchestrators - 3个)
负责分析项目、配置团队和协调任务。
- **Tech Lead Orchestrator (技术主管)**: 分析复杂项目并协调多步开发任务。
- **Project Analyst (项目分析师)**: 技术栈检测专家，启用智能 Agent 路由。
- **Team Configurator (团队配置者)**: AI 团队设置专家，检测你的堆栈并配置最佳 Agent 映射。

### 2. 框架专家 (Framework Specialists - 13个)
针对特定技术栈的深度优化。
- **Laravel**: Backend Expert, Eloquent Expert.
- **Django**: Backend Expert, API Developer, ORM Expert.
- **Rails**: Backend Expert, API Developer, ActiveRecord Expert.
- **React**: Component Architect (现代模式/Hooks), Next.js Expert (SSR/SSG).
- **Vue**: Component Architect, Nuxt Expert, State Manager.

### 3. 通用专家 (Universal Experts - 4个)
跨语言和框架的通用能力。
- **Backend Developer**: 多语言后端开发。
- **Frontend Developer**: 现代 Web 技术和响应式设计。
- **API Architect**: RESTful 设计、GraphQL 和与框架无关的架构。
- **Tailwind Frontend Expert**: Tailwind CSS 样式和实用优先开发。

### 4. 核心团队 (Core Team - 4个)
基础维护和质量保证。
- **Code Archaeologist (代码考古学家)**: 探索、记录和分析不熟悉或遗留的代码库。
- **Code Reviewer (代码审查员)**: 具有严重性标记报告的严格安全感知审查。
- **Performance Optimizer (性能优化师)**: 识别瓶颈并应用优化。
- **Documentation Specialist (文档专家)**: 编写全面的 README、API 规范和技术文档。

---

## 三、如何创建 Claude Agents (Creating Agents)

创建强大的、互联的 Claude 子 Agent 是一个高级模式。

### 1. 快速入门模板
Agent 定义在 `.claude/agents/your-agent-name.md` 中：

```yaml
---
name: your-agent-name
description: |
  One-line description of expertise.
  
  Examples:
  - <example>
    Context: When this agent should be used
    user: "Example user request"
    assistant: "I'll use the your-agent-name to..."
    <commentary>
    Why this agent was selected
    </commentary>
  </example>
tools: Read, Write, Edit, Bash  # 可选 - 如果省略则继承所有工具
---

You are an expert [role] specializing in [domain].

## Core Expertise
- [Specific skill 1]
- [Specific skill 2]

## Task Approach
1. [How you handle tasks]
2. [Your methodology]

## Return Format
Provide clear, structured output that other agents can understand.
```

### 2. XML 风格的描述模式 (高级)
Claude 使用描述中的 XML 风格示例来进行智能 Agent 选择。
- **模式学习**: Claude 从示例中学习何时调用 Agent。
- **上下文感知**: 理解项目阶段和用户意图。
- **智能委托**: 知道何时移交给其他专家。

### 3. 工具配置与继承
`tools` 字段是**可选**的。
- **省略时**: Agent 继承所有可用工具（Read, Write, Bash, WebFetch, MCP tools）。这是推荐的做法。
- **指定时**: 仅用于**限制** Agent 的能力（例如为代码审查员仅提供只读工具 `Read, Grep`）。

### 4. 最佳实践
- **专注的专业知识**: 单一领域精通，清晰的边界。
- **智能示例**: 提供 2-3 个覆盖不同场景的示例，包括边缘情况。
- **清晰的输出**: 提供结构化结果，确定下一步。

### 5. 常见模式
- **后端 → 前端流**:
  `@backend-dev` → API 完成 → `@frontend-dev` → UI 构建 → `@reviewer`
- **全栈开发**:
  `@tech-lead` → `@backend-dev + @frontend-dev` → 集成 → 测试

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Orchestrators | 编排者 | 负责协调其他 Agent 工作的高级 Agent |
| Tool Inheritance | 工具继承 | 子 Agent 默认拥有父环境所有工具的能力 |
| XML-Style Pattern | XML 风格模式 | 在 Prompt 中使用 XML 标签来结构化示例和指令的技术 |
| Code Archaeologist | 代码考古学家 | 专门用于理解和记录遗留代码的 Agent 角色 |
