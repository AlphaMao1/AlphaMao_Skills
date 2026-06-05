# Week 9-1: Introduction to Site Reliability Engineering
# 站点可靠性工程 (SRE) 简介

> **Original Link**: [https://sre.google/sre-book/introduction/](https://sre.google/sre-book/introduction/)
> **Title**: Introduction to Site Reliability Engineering
> **Author**: Google SRE Team
> **Week**: 9
> **Reading Time**: 15 min
> **Priority**: High
> **Translation Date**: 2026-02-03

---

## 介绍 (Introduction)

希望系统高度可靠是理所当然的，但这并不意味着冲突也不可避免。Google 选择了一种不同的方式来运行我们的系统：我们的 [站点可靠性工程 (SRE) 团队](https://sre.google/sre-book/software-engineering-in-sre/) 专注于雇佣软件工程师来运行我们的产品，并 [创建系统来完成那些工作](https://sre.google/sre-book/distributed-periodic-scheduling/)——那些通常由系统管理员手动完成的工作。

如果不以冲突为代价，那么站点可靠性工程到底是什么？我在 Google 定义它的方式很简单：**SRE 是当你要求软件工程师设计一个运维团队时会发生的事情**。

Google 的服务管理方法的一个主要基石是每个 SRE 团队的组成。总体而言，SRE 可以分为两大类：
1.  **50–60% 是 Google 软件工程师**：即通过 Google 软件工程师标准程序招聘的人。
2.  **40–50% 是接近 Google 软件工程师资格的人选**：他们拥有 SRE 有用但大多数软件工程师罕见的一套技术技能。目前为止，UNIX 系统内部结构和网络（第 1 层到第 3 层）专业知识是我们寻求的两种最常见的替代技术技能。

所有 SRE 的共同点是相信并有能力开发软件系统来解决复杂问题。

SRE 做的根本工作在历史上一直由运维团队完成，但使用的是具有软件专业知识的工程师。我们依靠这样一个事实：这些工程师在本质上通过设计和 [实施自动化](https://sre.google/sre-book/automation-at-google/) 来取代人工劳动。

这就涉及到 SRE 的一个关键点：**SRE 团队必须专注于工程**。如果没有持续的工程，运维负载就会增加，团队就需要更多的人来跟上工作量。为了避免这种命运，管理服务的团队**如果不写代码就会被淹没 (code or it will drown)**。因此，Google 为所有 SRE 的总“运维”工作设定了 **50% 的上限**——包括工单、随叫随到 (on-call)、手动任务等。这个上限确保 SRE 团队有足够的时间使服务稳定和可操作。

## DevOps 还是 SRE？(DevOps or SRE?)
“DevOps”一词出现于 2008 年底。其核心原则——IT 职能在系统设计和开发的每个阶段的参与、严重依赖自动化而非人力、将工程实践和工具应用于运维任务——与许多 [SRE 的原则和实践](https://sre.google/sre-book/part-II-principles/) 是一致的。可以将 DevOps 视为将几个核心 SRE 原则推广到更广泛的组织、管理结构和人员。同样也可以将 SRE 视为 DevOps 的一种特定实现，并带有一些独特的扩展。

## SRE 的信条 (Tenets of SRE)

虽然工作流程、优先级和日常运营的细微差别因 SRE 团队而异，但所有团队都对他们支持的服务负有一套基本的责任，并遵守相同的核心信条。一般来说，SRE 团队负责其服务的可用性、延迟、性能、效率、变更管理、监控、紧急响应和容量规划。

### 确保对工程的持久关注 (Ensuring a Durable Focus on Engineering)
如前所述，Google 将 SRE 的运维工作上限设定为其时间的 50%。这在实践中是通过监控运维工作量来实现的，并将 [多余的运维工作](https://sre.google/sre-book/dealing-with-interrupts/) 重定向回产品开发团队。

### 在不违反服务 SLO 的情况下追求最大变更速度 (Pursuing Maximum Change Velocity Without Violating a Service’s SLO)
产品开发和 SRE 团队可以通过消除各自目标中的结构性冲突来享受 [富有成效的工作关系](https://sre.google/workbook/engagement-model/)。这种冲突在于创新速度和产品稳定性之间。我们引入 **错误预算 (Error Budget)** 来解决这个问题。

错误预算源于这样一个观察：**对于几乎所有事物来说，100% 都是错误的可靠性目标**（心脏起搏器和防抱死制动系统是明显的例外）。对于任何软件服务，由业务或产品确定的可用性目标（例如 99.99%）决定了错误预算（即 0.01% 的不可用性）。只要我们不超过这个预算，我们可以将其花在任何我们想要的地方，比如发布新功能和进行实验。

### 监控 (Monitoring)
监控不应要求人类解释警报域的任何部分。相反，软件应该进行解释，只有当人类需要采取行动时才通知他们。
这主要有三种有效的监控输出：
1.  **警报 (Alerts)**：意味着人类需要立即采取行动。
2.  **工单 (Tickets)**：意味着人类需要采取行动，但不是立即。
3.  **日志 (Logging)**：不应由人直接查看，用于事后分析。

### 紧急响应 (Emergency Response)
可靠性是平均故障时间 (MTTF) 和平均修复时间 (MTTR) 的函数。评估紧急响应有效性的最相关指标是 MTTR。我们发现，提前思考并记录最佳实践的“剧本 (Playbook)”相比“临场发挥”的策略，能产生大约 **3 倍的 MTTR 改进**。

### 变更管理 (Change Management)
SRE 发现大约 **70% 的中断是由实时系统的变更引起的**。该领域的最佳实践使用自动化来实现：渐进式发布、快速准确地检测问题、在出现问题时安全回滚。

### 需求预测和容量规划 (Demand Forecasting and Capacity Planning)
容量规划应确保在这个容量需要的时候已经在位。这必须考虑有机增长（自然产品采用）和无机增长（如功能发布、营销活动）。

### 资源调配 (Provisioning)
资源调配结合了变更管理和容量规划。容量是昂贵的，因此必须在必要时快速且正确地进行。

### 效率和性能 (Efficiency and Performance)
SRE 最终控制资源调配，因此也必须参与任何关于利用率的工作。SRE 预测需求、调配容量并可以修改软件。这三个因素是服务效率的很大一部分。
