---
原文链接: https://github.com/modelcontextprotocol/typescript-sdk
原文标题: MCP TypeScript SDK
所属周次: Week 2
阅读时间: 10min
优先级: ⭐推荐
翻译日期: 2026-02-03
---

# MCP TypeScript SDK

Model Context Protocol (MCP) 的官方 TypeScript SDK，用于构建服务器和客户端。

> **重要提示**
>
> 主分支 (`main`) 包含 SDK 的 **v2** 版本（目前处于开发中，pre-alpha 阶段）。
>
> 我们预计在 2026 年第一季度发布稳定的 v2 版本。在此之前，**v1.x 仍然是生产使用的推荐版本**。在 v2 发布后，v1.x 将继续接收至少 6 个月的错误修复和安全更新，以便人们有时间升级。
>
> 有关 v1 文档和代码，请参阅 [v1.x 分支](https://github.com/modelcontextprotocol/typescript-sdk/tree/v1.x)。

## 概述

模型上下文协议 (MCP) 允许应用程序以标准化方式为 LLM 提供上下文，将提供上下文的关注点与实际的 LLM 交互分离开来。

此存储库包含 MCP 规范的 TypeScript SDK 实现，并提供：
- **MCP 服务器库** (工具/资源/提示, Streamable HTTP, stdio, auth 助手)
- **MCP 客户端库** (传输, 高级助手, OAuth 助手)
- **可选的中间件包** 用于特定的运行时/框架 (Express, Hono, Node.js HTTP)
- **可运行的示例** (位于 `examples/` 下)

## 包 (Packages)

此 monorepo 发布拆分的包：
- `@modelcontextprotocol/server`: 构建 MCP 服务器
- `@modelcontextprotocol/client`: 构建 MCP 客户端

这两个包都有对 `zod` 的必需对等依赖项 (peer dependency) 用于模式验证。

## 安装

### Server (服务器)
```bash
npm install @modelcontextprotocol/server zod
```

### Client (客户端)
```bash
npm install @modelcontextprotocol/client zod
```

### 可选的中间件包
SDK 还发布了可选的“中间件”包，帮助你将 MCP 接入特定的运行时或 Web 框架（例如 Express, Hono 或 Node.js http）。

```bash
# Node.js HTTP (IncomingMessage/ServerResponse) Streamable HTTP transport:
npm install @modelcontextprotocol/node

# Express integration:
npm install @modelcontextprotocol/express express

# Hono integration:
npm install @modelcontextprotocol/hono hono
```

这些包是有意设计的瘦适配器，不应引入额外的 MCP 功能或业务逻辑。

## Server SDK 详解 (Server SDK Details)
**来源**: `docs/server.md`

### 服务器概览
大多数用例将使用 `@modelcontextprotocol/server` 中的 `McpServer` 类。
推荐使用 **Streamable HTTP** 进行远程部署，或使用 **stdio** 进行本地进程集成。

### 传输层 (Transports)
- **Streamable HTTP**: 现代、全功能的传输方式。支持 HTTP POST 请求/响应，SSE 通知（可选），以及会话管理。
    - *Stateless (无状态)*: 无会话跟踪，适合简单的 API 类型服务器。
    - *Stateful (有状态)*: 会话具有 ID，支持可恢复性和高级功能。
- **HTTP + SSE (已弃用)**: 仅为了向后兼容而保留。新实现应首选 Streamable HTTP。

### 注册功能
- **Tools (工具)**: 让客户端要求服务器执行操作。通过 `server.registerTool` 注册，定义输入/输出 Schema。
- **Resources (资源)**: 向客户端公开数据，但不执行繁重计算或副作用。通过 `server.registerResource` 注册。
- **Prompts (提示)**: 可重用的模板，帮助人类（或客户端 UI）以一致的方式与模型对话。通过 `server.registerPrompt` 注册。

## Client SDK 详解 (Client SDK Details)
**来源**: `docs/client.md`

### 客户端概览
SDK 提供了一个高级 `Client` 类，通过不同的传输方式连接到 MCP 服务器：
- `StdioClientTransport`: 用于生成的本地进程。
- `StreamableHTTPClientTransport`: 用于远程 HTTP 服务器。
- `SSEClientTransport`: 用于遗留的 HTTP+SSE 服务器（已弃用）。

### 连接与基本操作
典型流程：
1. 构建一个带有名称、版本和功能的 `Client`。
2. 创建传输层并调用 `client.connect(transport)`。
3. 使用高级助手方法：
    - `listTools`, `callTool`
    - `listPrompts`, `getPrompt`
    - `listResources`, `readResource`

### OAuth 客户端认证助手
对于受 OAuth 保护的 MCP 服务器，客户端 `auth` 模块公开了：
- `ClientCredentialsProvider`
- `PrivateKeyJwtProvider`
- `StaticPrivateKeyJwtProvider`

这些助手帮助执行动态客户端注册（如果需要），获取访问令牌，并将 OAuth 据点附加到 Streamable HTTP 请求中。

## 快速入门 (可运行示例)

可运行的示例位于 `examples/` 下，并与文档保持同步。

1. 安装依赖项（从 repo 根目录）：
```bash
pnpm install
```

2. 运行 Streamable HTTP 示例服务器：
```bash
pnpm --filter @modelcontextprotocol/examples-server exec tsx src/simpleStreamableHttp.ts
```
或者，从示例包内部：
```bash
cd examples/server
pnpm tsx src/simpleStreamableHttp.ts
```

3. 在另一个终端中运行交互式客户端：
```bash
pnpm --filter @modelcontextprotocol/examples-client exec tsx src/simpleStreamableHttp.ts
```
或者，从示例包内部：
```bash
cd examples/client
pnpm tsx src/simpleStreamableHttp.ts
```

**后续步骤**:
- 服务器示例索引: `examples/server/README.md`
- 客户端示例索引: `examples/client/README.md`
- 引导式演练: `docs/server.md` 和 `docs/client.md`

## 贡献
此存储库是开源的。

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Peer Dependency | 对等依赖 | 项目必须安装的依赖项，但由宿主环境提供 |
| Middleware | 中间件 | 连接不同软件组件的软件胶水 |
| Monorepo | 单一代码库 | 一个代码库包含多个项目或包 |
| Streamable HTTP | 流式 HTTP | 支持流传输的 HTTP 通信方式 |
| Zod | Zod | TypeScript 优先的模式声明和验证库 |
