---
原文链接: https://www.anthropic.com (Internal PDF)
原文标题: How Anthropic teams use Claude Code
所属周次: Week 4
阅读时间: 20min
优先级: ⭐必读
翻译日期: 2026-02-03
---

# Anthropic 团队如何使用 Claude Code (How Anthropic teams use Claude Code)

**来源**: Anthropic Internal Report
**摘要**: Anthropic 的内部团队正在利用 Claude Code 转变工作流程，使开发人员和非技术人员能够处理复杂项目、自动化任务并弥合以前限制其生产力的技能差距。

## 目录
1.  Claude Code 用于数据基础设施
2.  Claude Code 用于产品开发
3.  Claude Code 用于安全工程
4.  Claude Code 用于推理
5.  Claude Code 用于数据科学和可视化
6.  Claude Code 用于 API
7.  Claude Code 用于增长营销
8.  Claude Code 用于产品设计
9.  Claude Code 用于 RL 工程
10. Claude Code 用于法律

---

## 1. Claude Code 用于数据基础设施 (Data Infrastructure)
数据基础设施团队为全公司的团队组织所有业务数据。

### 主要用例
-   **使用截图调试 Kubernetes**: 当 Kubernetes 集群宕机时，团队将仪表板截图提供给 Claude Code，它引导团队逐个菜单检查 Google Cloud UI，发现 Pod IP 地址耗尽警告，并提供修复命令。
-   **财务团队的纯文本工作流**: 财务成员编写描述数据工作流的纯文本文件，Claude Code 自动执行查询和 Excel 生成。
-   **新员工的代码库导航**: Claude Code 读取 `Claude.md` 文档，帮助新数据科学家理解数据管道依赖关系。

### 团队影响
-   解决基础设施问题无需网络专家介入。
-   加速新员工入职。
-   增强支持工作流，能监控大量仪表板。

### 建议
-   **编写详细的 Claude.md 文件**: 详细记录工作流、工具和期望。
-   **使用 MCP 服务器**代替 CLI 处理敏感数据。

---

## 2. Claude Code 用于产品开发 (Product Development)
Claude Code 团队使用自己的产品来构建更新。

### 主要用例
-   **自动接受模式 (Auto-Accept Mode) 快速原型**: 使用 Shift+Tab 启用自动接受，让 Claude 自主编写代码、运行测试并迭代。
-   **核心功能同步编码**: 对关键功能进行实时监控和详细指导。
-   **构建 Vim 模式**: Claude 自主完成了约 70% 的 Vim 键绑定实现。

### 建议
-   **创建自给自足的循环**: 让 Claude 自动运行构建和测试。
-   **任务分类**: 区分适合异步工作的外围任务和需要同步监督的核心任务。

---

## 3. Claude Code 用于安全工程 (Security Engineering)
专注于保护软件开发生命周期。

### 主要用例
-   **复杂基础设施调试**: 通过跟踪堆栈和控制流，将调试时间从 15 分钟缩短到 5 分钟。
-   **Terraform 代码审查**: 询问“这会做什么？我会后悔吗？”。
-   **文档合成**: 摄取文档并创建 Runbooks。
-   **测试驱动开发**: 让 Claude 编写伪代码并指导 TDD。

### 建议
-   **使用自定义 Slash 命令**: 占 Monorepo 中自定义命令的 50%。
-   **让 Claude 先说话**: "Commit your work as you go"。

---

## 4. Claude Code 用于推理 (Inference)
管理内存系统。

### 主要用例
-   **代码库理解**: 快速理解复杂架构。
-   **单元测试生成**: 自动覆盖边缘情况。
-   **ML 概念解释**: 帮助非 ML 背景成员理解模型特定功能。
-   **跨语言翻译**: 消除 Rust 等语言障碍。

### 建议
-   **测试知识库功能**: 比较 Claude 与 Google 搜索的速度。
-   **从代码生成开始**: 建立信任。

---

## 5. Claude Code 用于数据科学和可视化
构建可视化工具。

### 主要用例
-   **构建 JS/TS 仪表板**: 不懂前端的团队也能构建 React 应用。
-   **处理重复重构**: 像“老虎机”一样使用 Claude，提交状态 -> 运行 30 分钟 -> 接受或重试。

### 建议
-   **像老虎机一样对待**: 经常重试比通过纠正错误更有效。
-   **为了简单性而中断**: 如果它把问题复杂化，叫停它。

---

## 6. Claude Code 用于 API (API)
致力于 PDF 支持和网络搜索。

### 主要用例
-   **第一步工作流规划**: 将 Claude 作为任务的第一站来识别文件。
-   **独立调试**: 处理不熟悉的代码库部分。
-   **消除上下文切换**: 直接在终端提问。

### 建议
-   **迭代伙伴**: 不要期望一次成功。
-   **从最少信息开始**。

---

## 7. Claude Code 用于增长营销 (Growth Marketing)
### 主要用例
-   **自动化 Google Ads 创意**: 处理 CSV，生成符合字符限制的新广告。
-   **Figma 插件**: 批量生成广告变体。

### 建议
-   **识别 API 启用的任务**。
-   **分解为专用子 Agent**。

---

## 8. Claude Code 用于产品设计 (Product Design)
### 主要用例
-   **前端润色**: 设计师直接实施视觉调整。
-   **快速原型**: 粘贴 Mockup 图像生成代码。

### 建议
-   **利用图像粘贴**。
-   **让工程师协助设置**。

---

## 9. Claude Code 用于 RL 工程 (RL Engineering)
### 主要用例
-   **监督自主性**: 让 Claude 编写大部分代码。
-   **Kubernetes 操作指导**。

### 建议
-   **自定义 Claude.md** 防止重复错误。
-   **重检查点工作流**: 频繁提交以便回滚。

---

## 10. Claude Code 用于法律 (Legal)
### 主要用例
-   **辅助功能**: 为有语言障碍的家庭成员构建应用。
-   **法律工作流自动化**: 构建内部工具。

### 建议
-   **先在 Claude.ai 规划**。
-   **分享原型**。
