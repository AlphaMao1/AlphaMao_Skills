---
原文链接: https://medium.com/@OutSightAI/peeking-under-the-hood-of-claude-code-be9182046875
原文标题: Peeking Under the Hood of Claude Code
所属周次: Week 4
阅读时间: 15min
优先级: ⭐深度
翻译日期: 2026-02-03
---

# 窥探 Claude Code 的引擎盖之下 (Peeking Under the Hood of Claude Code)

**来源**: OutSight AI
**日期**: 2025年8月20日

**Anthropic 的工程师是如何设计 Claude Code 的？**
注意看 Claude Code 是如何完成编码工作的！它专注于任务，遵循约束，并安全地运行你不想手动输入的命令。
Anthropic 很少透露它是如何构建的，所以我们要设置了一个 LiteLLM 代理来观察 Claude Code 发送和接收的内容。
我们发现的不是一个单一的“魔法”，而是一堆精心设计的 Prompt 脚手架、安全护栏和通过细微提醒来保持 Agent 诚实和专注的机制。

**如果你是新手**：Claude Code 是 Anthropic 的 Agentic 编码工具，运行在你的终端中。

## TL;DR (太长不看版)
- **前置加载上下文 (Front-loads context)**: Claude Code 在做实际工作之前，会用微小的、有针对性的 Prompt（标题、主题检查、摘要）来加载上下文。
- **系统提醒 (System-reminders)**: 它到处散布“系统提醒”，包括在系统/用户 Prompt、工具调用甚至工具结果中，以减少偏离。
- **风险控制**: 在 Bash 运行之前，它通过显式的命令前缀提取和注入检查来控制风险。
- **子 Agent**: 当工作变得多步骤时，它会生成具有更窄指令的子 Agent（“Task”工具），然后根据任务复杂性动态调整它们的上下文。

## 设置：使用 LiteLLM 监控 Claude Code
为了理解 Claude Code 的行为，我们将 LiteLLM 作为一个透明代理放置在 Claude Code 和 Anthropic 的 API 服务器之间。
通过这种监控，我们在真实的编码会话中捕获了数百个 API 调用。我们的发现解释了为什么这么多开发者会有那些“它就是能用”的时刻。

## 令人惊叹的因素 (The Wow Factor)
如果不提及人们在使用 Claude Code 时报告的那些“顿悟时刻”，那就太遗憾了。
在观察他们的 API 请求时，我们发现魔法甚至在你开始 Claude Code 会话之前就开始了。
例如，如果你在一个现有项目中启动 Claude 会话，它首先会总结你的实际对话以提取标题。
然后它会分析你当前的消息，以判断当前对话是否是一个新话题，然后从那里继续。这初始的上下文只是一个例子。还有很多其他地方它在做类似的事情。

### 上下文前置加载示例
以下是 Claude Code 在会话期间自动添加的一些系统和用户 Prompt：
> "Summarize this coding conversation in under 50 characters..." (在50个字符内总结此编码对话...)
> "Analyze if this message indicates a new conversation topic..." (分析此消息是否表示一个新的对话主题...)

## Anthropic 可能试图隐藏的秘密武器：`<system-reminder>`
整个练习中最有趣和值得努力的发现是 `<system-reminder>` 标签的广泛使用。
这些标签不仅用于系统 Prompt 中，而且在任何地方都被频繁使用——它们嵌入在整个管道中，从用户消息到工具调用的结果，甚至在检测恶意文件和避免处理它们时也会使用。

### 示例：系统提醒无处不在
在对话的第一条消息中，即便有了详尽的系统 Prompt，Anthropic 还是在用户消息中插入了 `<system-reminder>`：
> "Do what has been asked; nothing more, nothing less." (做被要求的事；除此之外无他。)
> "NEVER create files unless they're absolutely necessary..." (除非绝对必要，否则切勿创建文件...)
> "ALWAYS prefer editing an existing file to creating a new one." (总是通过编辑现有文件而不是创建新文件。)

甚至在工具调用的结果中，也会插入提醒：
> "Called the LS tool with the following input..." (使用以下输入调用了 LS 工具...)
> "Result of calling the LS tool: ..." (调用 LS 工具的结果...)

以及关于 TodoList 的提醒：
> "This is a reminder that your todo list is currently empty. DO NOT mention this to the user explicitly..." (提醒你的待办事项列表目前是空的。不要明确向用户提及这一点...)

注意 `<system-reminder>` 标签的数量。仿佛上面的提醒还不够，Anthropic 决定在每次调用 `todoWrite` 函数时添加更多的 reminder。

## 命令注入检测 / Bash 执行期间的权限批准
如果你不是通过“意念编码”阅读本文，你可能并没有在 YOLO 模式下操作——这意味着你可能见过 Claude 请求运行命令的权限。
令我惊讶的是，这些权限不是硬编码的。它们也是生成的，Claude 有特定的子 Prompt 来询问此类权限，甚至检测命令注入。

### 命令前缀检测策略
Claude 使用一个名为 `<policy_spec>` 的文档来定义如何确定 Bash 命令的前缀。
- **命令注入**: 任何导致运行非检测到的前缀的命令的技术。
- **前缀提取**: 例如 `cat foo.txt` 的前缀是 `cat`。
- **安全机制**: 如果命令似乎包含命令注入（如 `git diff $(cat secrets...)`），它必须返回 "command_injection_detected"。这会触发用户的手动确认。

## 子 Agent 架构 (The Sub-Agent Architecture)
如果你在 X、LinkedIn 和 YouTube 上关注 Claude Code 的炒作，你可能已经看到成千上万的人告诉你如何最好地使用 Claude Code 的子 Agent 功能来启动多个并行 Agent 以完成更多工作。
在我们的观察中，我们注意到 `Task` 工具基本上是在内部启动它自己的 Claude Code 版本。
然而，有一个关键的区别，这个区别非常微妙。Task 工具调用 Agent 时**没有**主要用于指示模型使用 `todoWrite` 工具的 system-reminder 标签。
这意味着 Anthropic 试图避免在子 Agent 中使用待办事项列表，这是实用的，因为你希望子 Agent 有非常具体的任务，而不是需要待办事项列表的复杂任务。

### 聪明的上下文工程
但是，如果子 Agent 最终得到一个需要待办事项列表的复杂任务怎么办？
Anthropic 非常聪明地设计了上下文。他们设计了有条件地注入系统提醒标签的工具。
例如，如果 `ls -la` 命令运行后，系统检测到 TodoWrite 工具最近没有被使用，它会注入：
> "The TodoWrite tool hasn't been used recently... consider using the TodoWrite tool..." (TodoWrite 工具最近没被使用... 考虑使用它...)

## 真正的秘密武器 (The Real Secret Sauce)
到目前为止我们所看到的表明，Claude Code 的魔法不仅仅是因为基础模型不同，或者 Anthropic 知道我们不知道的什么花哨东西。
它只是**一个巨大的漂亮 Prompt**，加上**聪明的工具描述**和**带有正确标签的系统化上下文工程**的组合。

### 仍未解决的大问题
`<system-reminder>` 标签在 Claude 的训练中有什么特殊含义吗？为什么 Anthropic 如此大量地使用这个标签，而我几乎没看到其他人在他们的 Agent/系统 Prompt 中使用它？

## 给 Agent 构建者的启示
如果我能用一句话总结，那就是：**微小的提醒，在正确的时间，改变 Agent 的行为。**
无论 `<system-reminder>` 是否特殊，或者只是重复得足够多让模型注意到的占位符，这个想法是可靠的。我们都应该开始这样构建我们的 Agent。

### 4个清晰的模式
1.  **上下文前置加载**: 在做实际工作之前，总结对话，分析主题并设置上下文。
2.  **带有特殊标签的提醒**: 在整个系统中使用 `<system-reminder>` 标签，以避免偏离实际目标。
3.  **嵌入式安全和权限**: 通过专门的 Prompt、工具结果和系统提醒，将命令验证和注入检测直接集成到 Agent 循环中。
4.  **通过主循环控制的专用 Agent**: 使用不同的 Agent 用于不同的目的，主循环根据任务复杂性使用条件上下文工程来协调它们。

Claude Code 的成功在于通过上下文加载、提醒、嵌入式权限和子 Agent 的巧妙工程模式，在正确的时间避免了漂移。

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Prompt Scaffolding | Prompt 脚手架 | 围绕核心 Prompt 构建的结构化辅助信息和指令 |
| System-Reminder | 系统提醒 | Anthropic 广泛使用的标签 `<system-reminder>`，用于在上下文中不断强化指令 |
| Front-loading Context | 前置加载上下文 | 在任务开始前先加载摘要、标题等元信息 |
| Command Injection | 命令注入 | 通过操纵输入在预期的命令之外执行恶意命令的攻击技术 |
| LiteLLM Proxy | LiteLLM 代理 | 一个中间层工具，用于拦截和监控 LLM API 的流量 |
