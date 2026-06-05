---
原文链接: https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/
原文标题: APIs don't make good MCP tools
所属周次: Week 2
阅读时间: 10min
优先级: ⭐选读
翻译日期: 2026-02-03
---

# 思考：API 并不适合直接作为 MCP 工具

**作者**: Reilly Wood

[模型上下文协议](https://modelcontextprotocol.io/overview) (MCP) 如今是一件大事。它已成为让 LLM 访问他人编写的工具的事实标准，这当然会将它们转变为[代理](https://simonwillison.net/2025/May/22/tools-in-a-loop/)。但是为新的 MCP 服务器编写工具很难，因此人们经常建议[将现有 API 自动转换为 MCP 工具](https://blog.christianposta.com/semantics-matter-exposing-openapi-as-mcp-tools/)；通常使用 OpenAPI 元数据。

以我的经验来看，这**可以**工作，但效果**不好**。原因如下：

## 代理无法很好地处理大量工具

众所周知，[VS Code 有 128 个工具的硬性限制](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode) - 但[许多模型在该数量之前就难以准确调用工具](https://arxiv.org/abs/2411.15399)。此外，每个工具及其描述都占据了宝贵的上下文窗口空间。

大多数 Web API 在设计时并没有考虑到这些限制！当通过代码调用这些 API 时，拥有无数个用于单个产品区域的 API 是可以的，但是如果将这些 API 中的每一个都映射到 MCP 工具，结果可能不会太好。

从头开始设计的 MCP 工具通常比单个 Web API [灵活得多](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)，每个工具都能够完成多个单独 API 的工作。

## API 会迅速耗尽上下文窗口

想象一个一次返回 100 条记录的 API，每条记录都很宽（比如 50 个字段）。将这些结果原样发送给代理会消耗大量 tokens；即使查询只需要几个字段就能满足，每个字段也都会进入上下文窗口。

API 通常按记录数分页，但记录的大小差异很大。一条记录可能包含一个占用 100,000 个 [token](https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens) 的大文本字段，而另一条可能只包含 10 个。将这些 API 结果直接放入代理的上下文窗口就像一场赌博；有时能行，有时会爆炸。

数据的格式也可能是一个问题。如今大多数 Web API 返回 JSON，但 JSON 是一种非常低效的 token 格式。
对比 JSON 和 CSV：CSV 数据更简洁 - 每条记录消耗的 token 只有一半。[通常 CSV, TSV 或 YAML (对于嵌套数据) 是比 JSON 更好的选择](https://david-gilbertson.medium.com/llm-output-formats-why-json-costs-more-than-tsv-ebaf590bd541)。

这些问题都不是不可克服的。你可以想象自动添加工具参数让代理[投影](https://en.wikipedia.org/wiki/Projection_(relational_algebra))字段，自动截断或总结大结果，以及自动将 JSON 结果转换为 CSV。但我见过的大多数服务器都没有做这些事情。

## API 没有充分利用代理的独特能力

API 返回结构化数据供程序消费。这通常也是代理从工具调用中想要的……但代理也可以处理其他更自由形式的指令。

例如，一个 `ask_question` 工具可以对某些文档执行 RAG 查询，然后以纯文本形式返回信息，用于通知下一个工具调用 - 完全跳过结构化数据。

或者，调用 `search_cities` 工具可以返回城市的结构化列表以及下一步调用的建议：
```
city_name,population,country,region
Tokyo,37194000,Japan,Asia
Delhi,32941000,India,Asia
Shanghai,28517000,China,Asia

Suggestion: To get more specific information (weather, attractions, demographics), try calling get_city_details with the city_name parameter.
```
这种分层和工具链在 MCP 服务器中[非常有效](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers)，如果自动将 API 转换为工具，你会完全错过这一点。

## 如果代理需要调用 API，它可以直接调用

像 Claude Code 这样的代理如今非常擅长编写+执行代码，包括调用 Web API 的脚本。有些人甚至[认为根本不需要 MCP](https://lucumr.pocoo.org/2025/7/3/tools/)！

我不同意这个结论，但我确实认为我们应该顺势而为。[代理的沙盒化正在迅速改进](https://github.com/openai/codex)，如果代理直接调用 API 既简单又安全，那么我们不妨这样做，省去中间人。

## 结论

代理与 API 的典型消费者有着根本的不同。可以从现有 API 自动创建 MCP 工具，但这不太可能效果良好。当提供为代理的独特能力和限制而设计的工具时，代理的表现最好。

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Context Window | 上下文窗口 | LLM 一次能处理的最大文本量 |
| OpenAPI | OpenAPI | 描述 REST API 的标准规范 |
| Token | 令牌 | LLM 处理文本的基本单位 |
| RAG | 检索增强生成 | 结合外部知识库的生成方式 |
| Tool Chaining | 工具链 | 将多个工具调用串联起来 |
| Sandboxing | 沙盒化 | 在隔离环境中运行程序以确保安全 |
