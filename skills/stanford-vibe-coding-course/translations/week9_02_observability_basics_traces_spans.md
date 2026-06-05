# Week 9-2: Traces & Spans: Observability Basics You Should Know
# 追踪与跨度：你应该知道的可观测性基础 (Last9)

> **Original Link**: [https://last9.io/blog/traces-spans-observability-basics/](https://last9.io/blog/traces-spans-observability-basics/)
> **Title**: Traces & Spans: Observability Basics You Should Know
> **Author**: Last9 Team
> **Week**: 9
> **Reading Time**: 10 min
> **Priority**: Medium
> **Translation Date**: 2026-02-03

---

## 理解追踪 (Traces) 和跨度 (Spans)：核心概念

**Trace (追踪)** 捕捉请求在分布式系统中移动的旅程。把 Trace 想象成一个请求从开始到结束的完整故事——从用户点击按钮直到他们看到结果。

**Span (跨度)** 是 Trace 的构建块。每个 Span 代表该旅程中的一个工作单元——比如数据库查询、API 调用或函数执行。Span 相互嵌套以显示操作之间的父子关系。

简单的关系如下：
- 一个 **Trace** 包含多个 **Span**。
- 每个 **Span** 代表一个操作。
- Span 具有时间数据和元数据。
- Span 可以嵌套以显示操作之间的关系。

```
Trace
├── Span (API Gateway)
│   ├── Span (Auth Service)
│   │   └── Span (User Service)
│   │       └── Span (Database Query)
└── Span (Response Formatting)
```

## Trace 和 Span 对 DevOps 专业人员的好处
如果你运行着一个拥有数十个微服务的复杂系统，而没有追踪，当用户报告结账流程缓慢时，你需要单独检查每个服务，浪费宝贵的时间。

有了 Trace 和 Span，你可以：
1.  **即时发现瓶颈**：准确查看哪个服务或函数花费的时间太长。
2.  **跨服务边界调试**：跟随请求在服务之间跳转。
3.  **理解依赖关系**：可视化服务如何连接和相互依赖。
4.  **提高性能**：精确识别并修复缓慢的操作。
5.  **减少平均恢复时间 (MTTR)**：在出现问题时更快地找到根本原因。

## 技术实现

### 追踪上下文和传播 (Trace Context and Propagation)
为了使追踪跨越服务边界工作，每个服务都需要知道它正在处理同一个请求的一部分。这是通过 **上下文传播** 实现的——在服务之间传递 Trace ID 和 Span ID（通常作为 HTTP 头）。

### Span 属性和事件 (Span Attributes and Events)
Span 不仅仅是时间戳，它们包含丰富的数据：
- **Name**：此 Span 代表什么操作。
- **Timing**：开始和结束时间。
- **Status**：成功、错误等。
- **Attributes**：自定义键值对（如 user_id 或 cart_size）。
- **Events**：Span 内值得注意的事件。
- **Links**：与其他 Span 的连接。

### 采样策略 (Sampling Strategies)
追踪所有内容会产生大量数据。因此大多数系统使用 **采样**：
- **基于头部的采样 (Head-based)**：在请求开始时决定是否采样。
- **基于尾部的采样 (Tail-based)**：在请求完成后决定（更适合捕获错误）。
- **优先级采样 (Priority)**：始终追踪重要操作，但对常规操作进行采样。

## 工具和框架

### OpenTelemetry：行业标准
[OpenTelemetry](https://opentelemetry.io/) 已成为实现 Trace 和 Span 的首选框架。它提供所有主要编程语言的库、供应商中立的 API 和 SDK，以及一致的数据收集和导出方式。

### 高级技术
- **分布式上下文管理**：使用 W3C Trace Context 标准（traceparent, tracestate）。
- **关联 Trace、指标和日志**：通过 Exemplar trace 将指标链接到 Trace，在日志中添加 Trace ID。
- **错误处理**：用错误状态标记 Span，记录带有堆栈跟踪的异常。

## 有效的追踪模式与反模式
**有效模式**：
- 有意义的 Span 名称（如 `service_name/operation`）。
- 正确的粒度（为重要操作创建 Span，而不是每个函数调用）。
- 正确的上下文传播。

**反模式**：
- **过度仪表化**：创建太多 Span 会导致性能问题。
- **缺少上下文**：未能传播上下文会破坏跨服务的 Trace。
- **不一致的命名**：使用不同的命名标准使 Trace 难以解释。
