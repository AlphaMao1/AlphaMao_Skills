---
原文链接: https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/
原文标题: Introducing the MCP Registry
所属周次: Week 2
阅读时间: 5min
优先级: ⭐必读
翻译日期: 2026-02-03
---

# 介绍 MCP Registry (MCP 注册表)

**发布日期**: 2025年9月8日

今天，我们推出了 **Model Context Protocol (MCP) Registry**——这是一个针对公开可用的 MCP 服务器的开放目录和 API，旨在提高可发现性和实现性。通过标准化服务器的分发和发现方式，我们正在扩大它们的覆盖范围，同时使客户端更容易连接。

MCP Registry 现在提供**预览版**。要开始使用：
- **服务器维护者**: 按照我们的指南[将服务器添加到 MCP Registry](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx)。
- **客户端维护者**: 按照我们的指南[访问 MCP Registry 数据](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)。

## MCP 服务器的单一事实来源

在 2025 年 3 月，我们分享了我们想要为 MCP 生态系统建立一个中央注册表的想法。今天我们宣布，我们已经推出了 [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) 作为官方的 MCP Registry。作为 MCP 项目的一部分，MCP Registry 以及父级 [OpenAPI 规范](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/official-registry-api.md)都是开源的——允许每个人构建兼容的子注册表。

我们的目标是标准化服务器的分发和发现方式，提供一个子注册表可以构建其上的主要事实来源。反过来，这将扩大服务器的覆盖范围，并帮助客户端更容易地在整个 MCP 生态系统中找到服务器。

## 公共和私有子注册表

在构建中央注册表时，对我们来说重要的是不要夺走社区和公司已经建立的现有注册表。MCP Registry 作为公开可用 MCP 服务器的主要事实来源，组织可以选择基于自定义标准[创建子注册表](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)。例如：

- **公共子注册表**：如与每个 MCP 客户端关联的固执己见的“MCP 市场”，可以自由地扩充和增强它们从上游 MCP Registry 摄取的数据。每个 MCP 最终用户角色都有不同的需求，这取决于 MCP 客户端市场以固执己见的方式适当地服务于他们的最终用户。
- **私有子注册表**：将存在于具有严格隐私和安全要求的企业内部，但 MCP Registry 为这些企业提供了一个它们可以构建其上的单一上游数据源。至少，我们的目标是与这些私有实现共享 API 模式，以便相关的 SDK 和工具可以在整个生态系统中共享。

在这两种情况下，MCP Registry 都是起点——它是 MCP 服务器维护者发布和维护其自我报告信息的中心位置，供这些下游消费者处理并交付给他们的最终用户。

## 社区驱动的审核机制

MCP Registry 是一个由注册表工作组维护并获得许可的官方 MCP 项目。社区成员可以提交 issue 来标记违反 MCP [审核指南](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/moderation-policy.mdx)的服务器——例如包含垃圾邮件、恶意代码或冒充合法服务的服务器。注册表维护者随后可以将这些条目列入黑名单，并追溯性地从公共访问中将其删除。

---

## 关键术语

| 英文 | 中文 | 说明 |
|------|------|------|
| Registry | 注册表 | 集中存储和管理资源的系统 |
| Sub-registry | 子注册表 | 基于主注册表数据构建的下游注册表 |
| Single Source of Truth (SSOT) | 单一事实来源 | 数据的唯一权威来源 |
| Moderation | 审核 | 对内容进行检查和管理的机制 |
| Denylist | 黑名单 | 禁止访问的列表 |
