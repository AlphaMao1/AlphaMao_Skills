---
原文链接: https://github.com/modelcontextprotocol/servers
原文标题: Model Context Protocol Servers
所属周次: Week 2
阅读时间: 10min
优先级: ⭐推荐
翻译日期: 2026-02-03
---

# 模型上下文协议 (MCP) 服务器参考实现

此存储库是[模型上下文协议 (MCP)](https://modelcontextprotocol.io/) 的参考实现集合，以及社区构建的服务器和额外资源的参考。

> **重要提示**
>
> 如果你正在寻找 MCP 服务器列表，你可以在 [MCP Registry](https://registry.modelcontextprotocol.io/) 上浏览已发布的服务器。此存储库仅用于托管由 MCP 指导小组维护的少量参考服务器。

> **警告**
>
> 此存储库中的服务器旨在作为演示 MCP 功能和 SDK 用法的参考实现。它们旨在作为开发人员构建自己的 MCP 服务器的教育示例，**而不是**作为生产就绪的解决方案。开发人员应根据其特定的威胁模型和用例评估自己的安全要求并实施适当的保障措施。

## 🌟 参考服务器 (Reference Servers)

这些服务器旨在演示 MCP 功能和官方 SDK。

- **[Everything](https://github.com/modelcontextprotocol/servers/blob/main/src/everything)**: 包含提示、资源和工具的参考/测试服务器。
- **[Fetch](https://github.com/modelcontextprotocol/servers/blob/main/src/fetch)**: 用于高效 LLM 使用的 Web 内容获取和转换。
- **[Filesystem](https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem)**: 具有可配置访问控制的安全文件操作。
- **[Git](https://github.com/modelcontextprotocol/servers/blob/main/src/git)**: 读取、搜索和操作 Git 存储库的工具。
- **[Memory](https://github.com/modelcontextprotocol/servers/blob/main/src/memory)**: 基于知识图谱的持久记忆系统。
- **[Sequential Thinking](https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking)**: 通过思维序列进行动态和反思性的问题解决。
- **[Time](https://github.com/modelcontextprotocol/servers/blob/main/src/time)**: 时间和时区转换功能。

## 核心参考实现详情 (Key Reference Implementation Details)

为了深入理解 MCP 服务器的构建，以下是两个最核心的参考实现的详细说明。

### 1. Filesystem MCP Server (文件系统服务器)
**设计目标**: 实现用于文件系统操作的模型上下文协议 (MCP)。

#### 功能特性
- 读/写文件
- 创建/列出/删除目录
- 移动文件/目录
- 搜索文件
- 获取文件元数据
- 通过 [Roots](https://modelcontextprotocol.io/docs/learn/client-concepts#roots) 进行动态目录访问控制

#### 目录访问控制
服务器使用灵活的目录访问控制系统。目录可以通过命令行参数指定，也可以通过 Roots 动态指定。

**方法 1: 命令行参数**
在启动服务器时指定允许的目录：
```bash
mcp-server-filesystem /path/to/dir1 /path/to/dir2
```

**方法 2: MCP Roots (推荐)**
支持 Roots 的 MCP 客户端可以动态更新允许的目录。客户端通知的 Roots 会完全替换服务器端允许的任何目录。
**工作原理**:
1. **服务器启动**: 如果未提供参数，则以空允许目录启动。
2. **客户端连接**: 客户端连接并发送 `initialize` 请求。
3. **Roots 协议处理**: 服务器请求 `roots/list`，客户端响应其配置的 roots，服务器替换所有允许的目录。

#### API 工具列表
- **read_text_file**: 读取文件完整内容（UTF-8）。
- **read_media_file**: 读取图像或音频文件（返回 Base64）。
- **read_multiple_files**: 同时读取多个文件。
- **write_file**: 创建新文件或覆盖现有文件。
- **edit_file**: 使用高级模式匹配和格式化进行选择性编辑（支持 Git 风格的 diff）。
- **create_directory**: 创建新目录。
- **list_directory**: 列出目录内容。
- **list_directory_with_sizes**: 列出目录内容及大小统计。
- **move_file**: 移动或重命名文件/目录。
- **search_files**: 递归搜索匹配模式的文件。
- **get_file_info**: 获取详细的文件/目录元数据（大小、时间、权限等）。

---

### 2. Knowledge Graph Memory Server (知识图谱记忆服务器)
**设计目标**: 使用本地知识图谱实现持久记忆。这让 Claude 能够跨聊天记住有关用户的信息。

#### 核心概念
- **实体 (Entities)**: 知识图谱中的主节点。包含唯一名称、实体类型（如“人”、“组织”）和观察列表。
- **关系 (Relations)**: 实体之间的有向连接。始终以主动语态存储（例如 `works_at`）。
- **观察 (Observations)**: 关于实体的离散信息片段。作为字符串存储，应为原子事实（每个观察一个事实）。

#### API 工具列表
- **create_entities**: 创建多个新实体。
- **create_relations**: 创建实体之间的多个新关系。
- **add_observations**: 向现有实体添加新观察。
- **read_graph**: 读取整个知识图谱。
- **search_nodes**: 根据查询（名称、类型、观察内容）搜索节点。
- **open_nodes**: 按名称检索特定节点及其关系。

## 🚀 快速入门

### 使用此存储库中的 MCP 服务器

此存储库中的 TypeScript 服务器可以直接使用 `npx` 运行。

例如，這将启动 [Memory](https://github.com/modelcontextprotocol/servers/blob/main/src/memory) 服务器：
```bash
npx -y @modelcontextprotocol/server-memory
```

此存储库中的 Python 服务器可以直接使用 `uvx` 或 `pip` 运行。推荐使用 `uvx` 以便于使用和设置。

例如，這将启动 [Git](https://github.com/modelcontextprotocol/servers/blob/main/src/git) 服务器：
```bash
# 使用 uvx
uvx mcp-server-git

# 使用 pip
pip install mcp-server-git
python -m mcp_server_git
```

### 使用 MCP 客户端

单独运行服务器并没有太大用处，应该将其配置到 MCP 客户端中。例如，这是使用上述服务器的 Claude Desktop 配置：

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

使用 Claude Desktop 作为 MCP 客户端的其他示例可能如下所示：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "path/to/git/repo"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

## 🤝 第三方服务器 (Third-Party Servers)

越来越多的社区开发和维护的服务器展示了 MCP 在不同领域的各种应用。

> **注意**
>
> 社区服务器未经测试，使用风险自负。它们不隶属于 Anthropic，也不受其认可。

一些示例包括：
- **1mcpserver**: MCP 的 MCP。在本地机器上自动发现、配置和添加 MCP 服务器。
- **Adobe Commerce**: 与 Adobe Commerce GraphQL API 交互。
- **Airbnb**: 搜索 Airbnb 并获取房源详情。
- **PostgreSQL**: 可以只读访问 PostgreSQL 数据库并运行 SQL。
- **Slack**: 用于与 Slack 交互的服务器。
... (更多请参阅[完整列表](https://github.com/modelcontextprotocol/servers))

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Reference Implementation | 参考实现 | 官方提供的标准代码示例 |
| SDK | 软件开发工具包 | 用于开发 MCP 服务器的库 |
| Claude Desktop | Claude 桌面版 | 支持 MCP 的官方客户端应用 |
| npx/uvx | 包执行器 | 用于直接运行 Node/Python 包的命令行工具 |
