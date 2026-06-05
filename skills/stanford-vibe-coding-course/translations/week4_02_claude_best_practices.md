---
原文链接: https://code.claude.com/docs/en/best-practices
原文标题: Best Practices for Claude Code
所属周次: Week 4
阅读时间: 20min
优先级: ⭐必读
翻译日期: 2026-02-03
---

# Claude Code 最佳实践与架构 (Best Practices & Architecture)

**来源**: Anthropic Documentation
**核心**: 获取 Claude Code 最大价值的技巧、模式以及其底层工作原理。

## 一、Claude Code 是如何工作的？(The Agentic Loop)
理解 Claude Code 的核心循环对于掌握它至关重要。它不仅仅是一个聊天机器人，它是一个 **Agentic Loop (代理循环)**。

1.  **用户输入**: 你在终端输入命令。
2.  **规划 (Planning)**: Claude 分析请求，决定需要哪些工具（读文件、运行命令等）。
3.  **工具执行 (Tool Execution)**: Claude 调用工具，工具在你的本地环境中执行，并将输出返回给 Claude。
4.  **观察与推理 (Observation & Reasoning)**: Claude 读取输出，判断任务是否完成。如果未完成，它会制定下一步计划。
5.  **循环**: 这个过程会一直重复，直到任务完成或需要用户反馈。

**上下文窗口 (Context Window)**: Claude Code 会智能地管理上下文。当上下文填满时，它会触发 **Auto Compaction (自动压缩)**，总结之前的交互以释放空间，但保留关键信息（如修改的文件列表）。

## 二、核心工作流最佳实践

### 1. 探索，然后计划，然后编码 (Explore, then plan, then code)
不要让 Claude 直接写代码。遵循以下“三步走”：
1.  **探索 (Explore)**: 阅读相关文件和代码。
    > "read /src/auth and understand how we handle sessions..." (读取 /src/auth 并理解我们如何处理会话...)
2.  **计划 (Plan)**: 使用 `Ctrl+G` 进入计划模式，或者明确要求制定计划。
    > "I want to add Google OAuth... Create a plan." (我想添加 Google OAuth... 创建一个计划。)
3.  **实施 (Implement)**: 根据批准的计划执行。
    > "implement the OAuth flow from your plan..." (实现计划中的 OAuth 流程...)

### 2. 给 Claude 一种验证其工作的方法
Claude 在能够运行测试或查看其更改的效果时表现最好。
- **提供测试命令**: 告诉它如何运行测试。
- **要求自测**: "Write a test for this function and run it to verify." (为这个函数写一个测试并运行它以验证。)

### 3. 在 Prompt 中提供具体上下文
与其问模糊的问题，不如提供“路标”：
- **差**: "Fix the bug." (修复这个 Bug。)
- **好**: "Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases..." (审查 rateLimiter.ts 中的实现，寻找边缘情况...)

## 三、配置你的环境

### 编写有效的 CLAUDE.md
这是 Claude 的永久记忆，放在项目根目录。
- **Code style**: "Use ES modules, destructure imports..."
- **Workflow**: "Run typecheck after changes..."
- **Commands**: 记录项目中特有的构建和测试命令。

### 配置权限与安全
- **Allowlists**: 允许已知的安全工具（如 `npm run lint`）自动运行。
- **Sandboxing**: 启用 `/sandbox` 进行操作系统级隔离，限制文件系统和网络访问。
- **Safe Autonomous Mode**: 使用 `--dangerously-skip-permissions` 进行全自动运行（**警告**: 仅在沙箱或无关紧要的环境中使用）。

## 四、高级自动化与扩展

### 1. 运行 Headless 模式
使用 `-p` 标志进行脚本化运行，这对于 CI/CD 或批处理非常有用：
```bash
claude -p "Analyze this log file" --output-format stream-json
```

### 2. 扇出 (Fan out) 跨文件操作
结合 Bash 脚本和 Claude Code 批量处理文件：
```bash
# 生成文件列表并循环处理
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue..." --allowedTools "Edit,Bash"
done
```

### 3. 并行会话与 Git Worktrees
在处理长任务时，使用 Git Worktrees 开启多个并行的 Claude 会话，每个会话在独立的工作树中运行，互不干扰。

## 五、避免常见失败模式

1.  **厨房水槽会话 (The kitchen sink session)**:
    - *问题*: 在一个会话中混合多个不相关的任务，导致上下文污染。
    - *解决*: 任务之间使用 `/clear`。这是保持 Claude 智商在线的最重要习惯。
2.  **反复纠正 (Correcting over and over)**:
    - *问题*: Claude 一直改不对，你一直纠正，上下文充满了错误的尝试。
    - *解决*: 两次失败后，果断 `/clear`，并根据你学到的教训写一个更好的初始 Prompt。
3.  **过度指定的 CLAUDE.md**:
    - *问题*: 文件太长，Claude 忽略了一半。
    - *解决*: 无情地修剪。如果 Claude 已经知道怎么做，就不要写在文档里。

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Agentic Loop | 代理循环 | AI 代理感知环境、规划行动、执行工具并观察结果的迭代过程 |
| Plan Mode | 计划模式 | Claude Code 的一种模式，专注于分析和规划而不立即执行代码 |
| Auto Compaction | 自动压缩 | 当上下文填满时，系统自动总结历史信息以释放 Token 空间 |
| Headless Mode | 无头模式 | 无交互界面的运行模式，适合脚本自动化 |
| Fan out | 扇出 | 将一个大任务分散到多个并行或独立的小任务中处理 |
