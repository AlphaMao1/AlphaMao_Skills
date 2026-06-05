---
原文链接: https://owasp.org/www-project-top-10-for-large-language-model-applications/
原文标题: OWASP Top 10 for Large Language Model Applications
所属周次: Week 6
阅读时间: 15min
优先级: ⭐必读
翻译日期: 2026-02-03
---

# OWASP 大型语言模型应用 Top 10 (OWASP Top 10 for LLMs)

**来源**: OWASP Foundation
**核心**: 针对构建和部署 LLM 应用程序的开发人员、架构师和管理者的关键安全风险清单。

## 风险清单

### LLM01: 提示注入 (Prompt Injection)
攻击者通过精心设计的输入操纵 LLM，使其偏离预期行为。
- **直接注入 (Direct)**: 覆盖系统提示（"忽略之前的指令..."）。
- **间接注入 (Indirect)**: LLM 处理受污染的外部内容（如网页、邮件），导致非预期的操作。

### LLM02: 不安全的输出处理 (Insecure Output Handling)
盲目接受 LLM 的输出并将其传递给后端系统或其他组件，而未进行适当的清理或验证。
- **后果**: XSS、CSRF、甚至后端系统的远程代码执行。

### LLM03: 训练数据投毒 (Training Data Poisoning)
操纵预训练数据、微调数据或嵌入（Embeddings），引入后门、漏洞或偏见。
- **影响**: 破坏模型的安全性、有效性或道德行为。

### LLM04: 模型拒绝服务 (Model Denial of Service)
攻击者通过执行资源密集型操作使 LLM超载，导致服务中断或成本激增。
- **例子**: 发送超长或极其复杂的递归查询。

### LLM05: 供应链漏洞 (Supply Chain Vulnerabilities)
应用程序生命周期受到脆弱组件、服务或数据集的影响。
- **范围**: 第三方模型、插件、预训练数据。

### LLM06: 敏感信息泄露 (Sensitive Information Disclosure)
LLM 无意中泄露了训练数据或交互历史中的机密信息（PII、专有算法）。

### LLM07: 不安全的插件设计 (Insecure Plugin Design)
插件接受不受信任的输入或缺乏足够的访问控制。
- **风险**: 导致严重的漏洞，如远程代码执行。

### LLM08: 过度代理 (Excessive Agency)
授予 LLM 过多的自主权、权限或功能，导致意外的后果。
- **防范**: 最小权限原则，人机回环 (Human-in-the-loop)。

### LLM09: 过度依赖 (Overreliance)
用户或系统在没有适当验证的情况下盲目信任 LLM 的输出。
- **风险**: 决策失误、包含幻觉的代码部署。

### LLM10: 模型盗窃 (Model Theft)
未经授权访问或窃取专有的大型语言模型。
- **后果**: 知识产权损失、经济损失、敏感信息泄露。

**结论**: 该列表为 LLM 安全提供了一个基准框架。随着技术的发展，"过度代理" (LLM08) 和 "不安全的插件设计" (LLM07) 在 Agentic AI 时代变得尤为重要。
