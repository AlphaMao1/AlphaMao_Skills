---
原文链接: https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/
原文标题: GitHub Copilot: Remote Code Execution via Prompt Injection (CVE-2025-53773)
所属周次: Week 6
阅读时间: 15min
优先级: ⭐警示
翻译日期: 2026-02-03
---

# GitHub Copilot: 通过提示注入实现的远程代码执行 (CVE-2025-53773)

**来源**: Embrace The Red
**日期**: 2025年 (具体发布日期)

这是一篇关于重要但可怕的提示注入发现的帖子，该发现导致了开发者机器的完全系统破坏。

## 背景研究 (Background Research)
在观察 VS Code 和 GitHub Copilot Agent 模式时，我注意到一个奇怪的行为……它可以在未经用户批准的情况下创建和写入工作区中的文件。
这些编辑是立即持久化的，它们不是内存中的待审查 Diff。修改被立即写入磁盘。
作为一个红队成员，由于你知道这可能不是好事……所以我正在寻找是否可以利用这一点来提升权限并执行代码。

### YOLO 模式 (YOLO Mode)
所以，接下来我研究了 VS Code 中依赖于项目/工作区文件夹内设置的功能，并很快发现了一个有趣的功能。
结果发现，在 `.vscode/settings.json` 文件中，可以添加以下行：

```json
"chat.tools.autoApprove": true
```

这将使 GitHub Copilot 进入 **YOLO 模式**。
它禁用了所有用户确认，我们可以运行 shell 命令、浏览网页等等！
有趣的是，这是一个实验性功能，但它默认存在。我没有下载特殊版本或将我的 VS Code 整体设置为实验模式。
此外，它在 Windows、macOS 和 Linux 上均有效。

## 漏洞利用链解释 (Exploit Chain Explained)
劫持 Copilot 并提升权限的概念验证 (PoC) 利用链如下：
1.  攻击始于植入在源代码文件、网页、GitHub Issue、工具调用响应或其他内容中的**提示注入 (Prompt Injection)**… 载荷还可以使用不可见文本作为指令。
2.  提示注入首先将行 `"chat.tools.autoApprove": true` 添加到 `~/.vscode/settings.json` 文件中。如果文件夹和文件尚不存在，则会创建它们。
3.  GitHub Copilot 立即进入 YOLO 模式！
4.  攻击运行终端命令。使用条件提示注入，我们可以根据操作系统实际定位要运行的内容。
5.  我们实现了由提示注入驱动的 **远程代码执行 (RCE)**。

```json
// ~/.vscode/settings.json
{
    "chat.tools.autoApprove": true
}
```

(原文此处有截图演示：显示带有提示注入的演示文件，开发人员在右侧聊天框中与文件交互，然后计算器弹出！)

当然，任何其他提示注入传递方式，如网络或来自 MCP 服务器的数据，都是攻击角度。我只是在源代码文件中使用它，因为这样最容易测试。

## 将工作站加入僵尸网络 - ZombAIs
当然，这意味着我们可以将开发人员的机器作为 **ZombAI** 加入僵尸网络。
此外，为了好玩，我们可以修改 `settings.json` 文件以将 VS Code 切换为红色配色方案和类似的东西。

```json
"workbench.colorTheme": "Red"
```

但这还没完！这还意味着我们可以构建一个实际的 **AI 病毒**。

## 构建 AI 病毒 (Building an AI Virus)
看到这一点，人们会注意到这基本上允许创建病毒。攻击者可以嵌入指令，一旦他们获得了代码执行权，额外的恶意软件就可以破坏其他 Git 项目（和 RAG 源）以嵌入恶意指令，并提交更改甚至强制推送到上游。
随着其他开发人员在不知情的情况下传播受感染的代码，这可能导致进一步的传播。

最后，我们还需要谈谈不可见指令！

## 使用不可见指令 (Using Invisible Instructions)
有人可能会说，如果指令作为注释嵌入，很快就会被发现。所以为了让事情更有趣一点，我甚至创建了一个**不可见载荷 (Invisible Payload)**，它实现了攻击链，但对用户不可见。这虽然不那么可靠，但仍然有效。
*注：虽然这里使用不可见指令的演示对我来说多次有效，但使用不可见指令通常会导致利用非常不可靠，也通常被模型拒绝，而且 VS Code 通常会显示关于 Unicode 字符的视觉指示器。然而，攻击（和模型）会随着时间的推移而变得更好。同样值得强调的是，并非所有模型都容易受到这种不可见提示注入攻击。*

## 建议和修复 (Recommendations and Fix)
实际上，除了我分享的 YOLO 模式示例之外，还有更多的攻击角度。当 Microsoft 问我是否有更多信息时，我多看了一下，注意到还有其他问题点，例如 `.vscode/tasks.json`（AI 可以写入该文件），或者添加虚假的恶意 MCP 服务器等，这些都可能导致代码执行。AI 还可以重新配置项目的用户界面和配置设置。

```json
// .vscode/tasks.json 可以被用来定义自动运行的任务
```

最近我注意到开发人员经常使用多个 Agent，因此还存在**覆盖其他 Agent 配置文件**（允许列表 bash 命令、添加 MCP 服务器……）的威胁，因为它们通常也位于项目文件夹中。

理想情况下，如果没有人工首先批准，AI 就不应该能够修改文件。许多其他编辑器确实显示 Diff，然后可以由开发人员批准。

## 负责任的披露 (Responsible Disclosure)
在 2025 年 6 月 29 日报告该漏洞后，Microsoft 确认了复现并问了几个后续问题。几周后，MSRC 指出这是他们已经在跟踪的问题，并且将在 8 月修复。随着 8 月补丁星期二的发布，此问题现已修复。
向来自 [Persistent Security](https://persistent-security.net/) 的 [Markus Vervier](https://x.com/marver) 致敬，他也识别并向 Microsoft 报告了这个漏洞。你可以在[这里](https://www.persistent-security.net/post/part-iii-vscode-copilot-wormable-command-execution-via-prompt-injection)找到他们的文章。还要向 [Ari Marzuk](https://x.com/Ari_MaccariTA) 致敬，他似乎也许并行发现了它。
感谢 MSRC 成员和产品团队帮助缓解此问题。

## 结论 (Conclusion)
这是 AI Agent 可能不会待在盒子里的另一个例子！通过修改自己的环境，GitHub Copilot 可以提升权限并执行代码以破坏开发人员的机器。正如我所发现的，这是 Agentic 系统中并不罕见的设计缺陷。
继续通过威胁建模寻找此类设计缺陷，这些应该很容易被捕获。
Cheers.
