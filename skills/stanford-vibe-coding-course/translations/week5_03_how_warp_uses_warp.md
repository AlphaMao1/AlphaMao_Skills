---
原文链接: https://www.warp.dev/blog/how-we-use-warp-to-build-warp
原文标题: The Coding Mandate: How Warp Uses Warp to Build Warp
所属周次: Week 5
阅读时间: 12min
优先级: ⭐深度
翻译日期: 2026-02-03
---

# 编码指令：Warp 如何使用 Warp 构建 Warp (How Warp Uses Warp to Build Warp)

**来源**: warp.dev
**核心理念**: "The Coding Mandate"（编码指令）—— Warp 内部的一项政策，要求每项编码任务都必须以 Warp 中的 Prompt 开始。

## 什么是“编码指令” (The Coding Mandate)?
这是一项旨在通过**吃自己的狗粮 (Dogfooding)** 来改进产品的激进策略。它要求工程师在编写任何代码之前，首先尝试使用 Warp 的 AI Agent 来生成它。
这不仅仅是为了测试，而是为了：
1.  **提高工程产出**: 减少手动样板代码的编写。
2.  **多线程开发**: 允许开发者同时通过 AI 处理多个任务。
3.  **发现痛点**: 工程师是第一个遇到产品缺陷的人，提供最直接的反馈循环。

## 就像手动编写一样 (Just Like Hand-Written Code)
Agent 生成的代码必须符合与手动代码相同的严格标准：
- **质量**: 必须由人类工程师审查。
- **规范**: 符合 Warp 的代码风格、API 使用规范和导入规则。
- **测试**: 必须包含并通过测试。
这确保了虽然 AI 加速了开发，但代码库的完整性不会下降。

## Warp 2.0: Agentic Development Environment (ADE)
Warp 2.0 的发布标志着它从一个终端进化为一个 ADE。
- **跨仓库操作**: Agent 现在可以跨多个仓库工作，理解大型代码库的上下文。
- **工作流原生**: 集成了 Code, Agents, Terminal, 和 Drive。
- **高接受率**: 内部数据显示，通过这种方式生成的代码具有极高的接受率，这得益于 Warp 对自身代码库的深度索引和理解。

## 实际影响
- **数亿行代码**: 开发团队每周通过这种方式生成大量的代码。
- **知识民主化**: AI 帮助工程师快速上手他们不熟悉的代码库部分（例如，后端工程师修改前端组件）。
- **持续进化**: 通过不断使用，Warp 的 AI 越来越了解 Warp 自己的构建方式，形成了一个正向反馈循环。

**总结**: "Warp 构建 Warp" 不仅仅是一句口号，它是一种通过 AI 彻底改变软件开发生命周期的实践证明。
