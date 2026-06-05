---
原文链接: https://developers.cloudflare.com/agents/guides/remote-mcp-server/#add-authentication
原文标题: Build a Remote MCP server - Add Authentication
所属周次: Week 2
阅读时间: 15min
优先级: ⭐必读
翻译日期: 2026-02-03
---

# 构建远程 MCP 服务器 - 添加身份验证

现在你已经部署了一个公共 MCP 服务器，让我们逐步了解如何使用 **OAuth** 启用用户身份验证。

你之前部署的公共服务器示例允许任何客户端连接并调用工具而无需登录。要添加身份验证，你需要更新你的 MCP 服务器以充当 **OAuth 提供者**，处理安全登录流程并在颁发访问令牌，MCP 客户端可以使用这些令牌来进行经过身份验证的工具调用。

如果用户已经需要登录才能使用你的服务，这尤其有用。一旦启用了身份验证，用户可以使用其现有帐户登录，并授予其 AI 代理与其 MCP 服务器公开的工具进行交互的权限（使用范围权限）。

在此示例中，我们使用 GitHub 作为[OAuth 提供者](https://developers.cloudflare.com/agents/model-context-protocol/authorization/#2-third-party-oauth-provider)，但你可以将 MCP 服务器与任何支持 OAuth 2.0 规范的 OAuth 提供者连接，包括 Google、Slack、Stytch、Auth0、WorkOS 等。

## 步骤 1 — 创建一个新的 MCP 服务器

运行以下命令创建一个新的 MCP 服务器：

```bash
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

现在，你已经设置好了 MCP 服务器，并安装了依赖项。进入该项目文件夹：

```bash
cd my-mcp-server-github-auth
```

你会注意到，在示例 MCP 服务器中，如果你通过 `src/index.ts` 打开文件，主要的区别是 `defaultHandler` 被设置为了 `GitHubHandler`：

```typescript
import GitHubHandler from "./github-handler"; 

export default new OAuthProvider({ 
  apiRoute: "/mcp", 
  apiHandler: MyMCP.Router, 
  defaultHandler: GitHubHandler, 
  authorizeEndpoint: "/authorize", 
  tokenEndpoint: "/token", 
  clientRegistrationEndpoint: "/register",
});
```

这将确保你的用户被重定向到 GitHub 进行身份验证。但是要使其工作，你需要按照下面的步骤创建 OAuth 客户端应用程序。

## 步骤 2 — 创建一个 OAuth 应用程序

你需要创建两个 [GitHub OAuth App ↗](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app) 才能使用 GitHub 作为 MCP 服务器的身份验证提供者——一个用于本地开发，一个用于生产。

### 首先为本地开发创建一个新的 OAuth App
导航到 [github.com/settings/developers ↗](https://github.com/settings/developers) 创建一个新的 OAuth App，设置如下：
- **Application name**: My MCP Server (local)
- **Homepage URL**: `http://localhost:8788`
- **Authorization callback URL**: `http://localhost:8788/callback`

对于刚创建的 OAuth 应用程序，添加客户端 ID 作为 `GITHUB_CLIENT_ID` 并生成一个客户端密钥，将其作为 `GITHUB_CLIENT_SECRET` 添加到项目根目录下的 `.dev.vars` 文件中，该文件[用于在本地开发中设置密钥](https://developers.cloudflare.com/workers/configuration/secrets/)。

```bash
touch .dev.vars
echo 'GITHUB_CLIENT_ID="your-client-id"' >> .dev.vars
echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .dev.vars
```

### 接下来，在本地运行你的 MCP 服务器
运行以下命令启动开发服务器：

```bash
npm start
```

你的 MCP 服务器现在运行在 `http://localhost:8788/mcp`。

在一个新终端中，运行 [MCP Inspector ↗](https://github.com/modelcontextprotocol/inspector)。MCP Inspector 是一个交互式 MCP 客户端，允许你连接到 MCP 服务器并从 Web 浏览器调用工具。

```bash
npx @modelcontextprotocol/inspector@latest
```

在 Web 浏览器中打开 MCP Inspector（通常是 `http://localhost:5173`）。
在 Inspector 中，输入你的 MCP 服务器的 URL `http://localhost:8788/mcp`。

在右侧的主面板中，点击 **OAuth Settings** 按钮，然后点击 **Quick OAuth Flow**。
你应该会被重定向到 GitHub 登录或授权页面。在授权 MCP Client (Inspector) 访问你的 GitHub 帐户后，你将被重定向回 Inspector。
点击侧边栏中的 **Connect**，你应该会看到 "List Tools" 按钮，它将列出你的 MCP 服务器公开的工具。

### 其次 — 为生产环境创建一个新的 OAuth App
你需要重复这些步骤为生产环境创建一个新的 OAuth App。
导航到 [github.com/settings/developers ↗](https://github.com/settings/developers) 创建一个新的 OAuth App，设置如下：
- **Application name**: My MCP Server (production)
- **Homepage URL**: 输入你部署的 MCP 服务器的 workers.dev URL (例如: `worker-name.account-name.workers.dev`)
- **Authorization callback URL**: 输入你部署的 MCP 服务器的 `/callback` 路径 (例如: `worker-name.account-name.workers.dev/callback`)

使用 Wrangler CLI 为刚创建的 OAuth 应用程序添加客户端 ID 和客户端密钥：

```bash
wrangler secret put GITHUB_CLIENT_ID
wrangler secret put GITHUB_CLIENT_SECRET
# 添加任何随机字符串作为 COOKIE_ENCRYPTION_KEY
npx wrangler secret put COOKIE_ENCRYPTION_KEY 
```

> **警告**
> 当你创建第一个密钥时，Wrangler 会询问你是否要创建一个新的 Worker。提交 "Y" 以创建一个新的 Worker 并保存密钥。

### 设置 KV 命名空间
- 创建 KV 命名空间：
```bash
npx wrangler kv namespace create "OAUTH_KV"
```

- 使用生成的 KV ID 更新 `wrangler.jsonc` 文件：
```json
{ 
  "kvNamespaces": [ 
    { 
      "binding": "OAUTH_KV", 
      "id": "<YOUR_KV_NAMESPACE_ID>" 
    } 
  ]
}
```

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Remote MCP Server | 远程 MCP 服务器 | 运行在云端而非本地的 MCP 服务 |
| OAuth Provider | OAuth 提供者 | 提供身份验证服务的实体（如 GitHub, Google） |
| Client ID/Secret | 客户端 ID/密钥 | OAuth 应用的凭证 |
| Callback URL | 回调 URL | 认证成功后重定向回应用的地址 |
| KV Namespace | KV 命名空间 | Cloudflare Workers 的键值存储 |
| Wrangler | Wrangler | Cloudflare Workers 的命令行工具 |
