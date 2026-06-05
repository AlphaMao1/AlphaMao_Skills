# CS146S 完整课程内容

> ⭐ = 必做 (核心内容) | 📖 = 选做 (有时间再看)
> 
> 📺 Slides = 选读资源，建议配合阅读材料观看

---

## Week 1: LLM入门与Prompt Engineering
**主题**: 大语言模型基础 | **必做**: 2h | **完整**: 4h

### 📺 Slides (选读)
- [Introduction and how an LLM is made](https://docs.google.com/presentation/d/1zT2Ofy88cajLTLkd7TcuSM4BCELvF9qQdHmlz33i4t0/edit?usp=sharing)
- [Power prompting for LLMs](https://docs.google.com/presentation/d/1MIhw8p6TLGdbQ9TcxhXSs5BaPf5d_h77QY70RHNfeGs/edit?usp=drive_link)

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 |
|---|------|--------|------|----------|
| 1 | Deep Dive into LLMs | ⭐ | 60min | week1_01_Deep_Dive_into_LLMs.md |
| 2 | Prompt Engineering Overview | 📖 | 15min | week1_02_Prompt_Engineering_for_AI_Guide.md |
| 3 | Prompt Engineering Guide | ⭐ | 30min | week1_03_prompt_engineering_guide.md |
| 4 | AI Prompt Engineering Deep Dive | 📖 | 45min | week1_04_AI_prompt_engineering.md |
| 5 | How OpenAI Uses Codex | ⭐ | 20min | week1_05_openai_codex.md |

### Assignment (可选)
- [LLM Prompting Playground](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week1) ⭐

### 核心概念
- **LLM**: 大型语言模型，通过海量文本训练的神经网络
- **Prompt**: 给LLM的输入指令
- **Token**: LLM处理文本的基本单位 (~4字符)
- **Temperature**: 控制输出随机性 (0=确定, 1=创造)
- **Context Window**: LLM能处理的最大token数

---

## Week 2: Agent架构 (MCP协议) ⭐⭐⭐
**主题**: Coding Agent核心 | **必做**: 2.5h | **完整**: 3h
**重要性**: 整个课程的核心！MCP是现代AI工具的基础架构。

### 📺 Slides (选读)
- [Building a coding agent from scratch](https://docs.google.com/presentation/d/11CP26VhsjnZOmi9YFgLlonzdib9BLyAlgc4cEvC5Fps/edit?usp=sharing) ⭐
- [Building a custom MCP server](https://docs.google.com/presentation/d/1zSC2ra77XOUrJeyS85houg1DU7z9hq5Y4ebagTch-5o/edit?usp=drive_link)

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 | 备注 |
|---|------|--------|------|----------|------|
| 1 | MCP Introduction | ⭐ | 20min | week2_01_mcp_introduction.md | |
| 2 | Sample MCP Server Implementations | ⭐ | 30min | week2_02_sample_mcp_server_implementations.md | 🔗需访问原链接 |
| 3 | MCP Server Authentication | ⭐ | 15min | week2_03_mcp_server_authentication.md | |
| 4 | MCP Server SDK | ⭐ | 20min | week2_04_mcp_server_sdk.md | 🔗需访问原链接 |
| 5 | MCP Registry | ⭐ | 10min | week2_05_mcp_registry.md | |
| 6 | MCP Food-for-Thought | ⭐ | 15min | week2_06_mcp_food_for_thought.md | |

### Assignment (可选)
- [First Steps in the AI IDE](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week2) 📖

### 核心概念
- **Agent**: 能自主执行任务、使用工具的AI系统
- **MCP**: Model Context Protocol，LLM与工具交互的标准协议
- **Tool Calling**: LLM调用外部函数的能力
- **Context Window**: LLM能处理的最大文本长度

---

## Week 3: AI IDE与上下文管理
**主题**: 高效使用AI IDE | **必做**: 2h | **完整**: 3h

### 📺 Slides (选读)
- [From first prompt to optimal IDE setup](https://docs.google.com/presentation/d/11pQNCde_mmRnImBat0Zymnp8TCS_cT_1up7zbcj6Sjg/edit?usp=sharing)

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 | 备注 |
|---|------|--------|------|----------|------|
| 1 | Specs Are the New Source Code | ⭐ | 15min | week3_01_specs_are_the_new_source_code.md | |
| 2 | How Long Contexts Fail | ⭐ | 20min | week3_02_how_long_contexts_fail.md | |
| 3 | Devin: Coding Agents 101 | ⭐ | 25min | week3_03_devin_coding_agents_101.md | |
| 4 | Getting AI to Work In Complex Codebases | ⭐ | 30min | week3_04_getting_ai_to_work_in_complex_codebases.md | 🔗需访问原链接 |
| 5 | How FAANG Vibe Codes | 📖 | 10min | week3_05_how_faang_vibe_codes.md | |
| 6 | Writing Effective Tools for Agents | 📖 | 20min | week3_06_writing_effective_tools_for_agents.md | |

### Assignment (可选)
- [Build a Custom MCP Server](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week3/assignment.md) ⭐

### 核心概念
- **Context Engineering**: 精心设计给Agent的上下文信息
- **PRD**: Product Requirements Document，产品需求文档
- **RAG**: Retrieval Augmented Generation，检索增强生成

---

## Week 4: Coding Agent模式 (Claude Code) ⭐⭐
**主题**: 实战 Claude Code | **必做**: 2h | **完整**: 3h

### 📺 Slides (选读)
- [How to be an agent manager](https://docs.google.com/presentation/d/19mgkwAnJDc7JuJy0zhhoY0ZC15DiNpxL8kchPDnRkRQ/edit?usp=sharing)

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 | 备注 |
|---|------|--------|------|----------|------|
| 1 | How Anthropic Uses Claude Code | ⭐ | 25min | week4_01_how_anthropic_uses_claude_code.md | |
| 2 | Claude Best Practices | ⭐ | 20min | week4_02_claude_best_practices.md | |
| 3 | Awesome Claude Agents | 📖 | 15min | week4_03_awesome_claude_agents.md | 🔗需访问原链接 |
| 4 | Super Claude | ⭐ | 20min | week4_04_super_claude.md | 🔗需访问原链接 |
| 5 | Good Context Good Code | ⭐ | 15min | week4_05_good_context_good_code.md | |
| 6 | Peeking Under the Hood of Claude Code | 📖 | 20min | week4_06_peeking_under_the_hood_of_claude_code.md | |

### Assignment (可选)
- [Coding with Claude Code](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week4/assignment.md) ⭐

### 核心概念
- **Agent Autonomy**: Agent自主程度
- **HITL**: Human-in-the-Loop，人在回路
- **CLAUDE.md**: Claude Code项目配置文件

---

## Week 5: 现代终端 (Warp)
**主题**: AI终端工具 | **必做**: 1h | **完整**: 1.5h

### 📺 Slides (选读)
- [How to Build a Breakout AI Developer Product](https://docs.google.com/presentation/d/1Djd4eBLBbRkma8rFnJAWMT0ptct_UGB8hipmoqFVkxQ/edit?usp=sharing)

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 | 备注 |
|---|------|--------|------|----------|------|
| 1 | Warp University | ⭐ | 30min | week5_01_warp_university.md | 🔗需访问原链接操作 |
| 2 | Warp vs Claude Code | 📖 | 15min | week5_02_warp_vs_claude_code.md | |
| 3 | How Warp Uses Warp to Build Warp | 📖 | 20min | week5_03_how_warp_uses_warp.md | |

### Assignment (可选)
- [Agentic Development with Warp](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week5) 📖

---

## Week 6: AI测试与安全 ⭐⭐
**主题**: 安全意识 | **必做**: 2.5h | **完整**: 3.5h
**重要性**: 安全意识必须尽早建立！

### 📺 Slides (选读)
- [AI QA, SAST, DAST, and Beyond](https://docs.google.com/presentation/d/1C05bCLasMDigBbkwdWbiz4WrXibzi6ua4hQQbTod_8c/edit?usp=sharing) ⭐

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 | 备注 |
|---|------|--------|------|----------|------|
| 1 | SAST vs DAST | ⭐ | 15min | week6_01_sast_vs_dast.md | |
| 2 | Copilot Remote Code Execution | ⭐ | 20min | week6_02_copilot_remote_code_execution.md | |
| 3 | Finding Vulnerabilities with Claude Code | 📖 | 25min | week6_03_finding_vulnerabilities_with_claude_code.md | |
| 4 | Agentic AI Threats | ⭐ | 20min | week6_04_agentic_ai_threats.md | |
| 5 | OWASP Top Ten | ⭐ | 30min | week6_05_owasp_top_ten.md | 🔗需访问原链接 |
| 6 | Context Rot | 📖 | 15min | week6_06_context_rot.md | |

### Assignment (可选)
- [Writing Secure AI Code](https://github.com/mihail911/modern-software-dev-assignments/blob/master/week6/assignment.md) ⭐

### 核心概念
- **SAST**: 静态应用安全测试
- **DAST**: 动态应用安全测试
- **Prompt Injection**: 通过恶意输入操控LLM
- **OWASP**: 开放Web应用安全项目

---

## Week 7: 代码审查与文档
**主题**: AI辅助审查 | **必做**: 1.5h | **完整**: 3h

### 📺 Slides (选读)
- [AI code review](https://docs.google.com/presentation/d/1NkPzpuSQt6Esbnr2-EnxM9007TL6ebSPFwITyVY-QxU/edit?usp=sharing)

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 |
|---|------|--------|------|----------|
| 1 | Code Reviews: Just Do It | ⭐ | 10min | week7_01_code_reviews_just_do_it.md |
| 2 | How to Review Code Effectively | ⭐ | 20min | week7_02_how_to_review_code_effectively.md |
| 3 | AI-Assisted Assessment of Coding Practices | 📖 | 30min | week7_03_auto_commenter.md |
| 4 | AI Code Review Best Practices | ⭐ | 15min | week7_04_ai_code_review_implementation.md |
| 5 | Code Review Essentials | 📖 | 15min | week7_05_code_review_essentials.md |
| 6 | Lessons from millions of AI code reviews | 📖 | 30min | week7_06_Lessons_from_millions_of_AI_code_reviews.md |

### Assignment (可选)
- [Code Review Reps](https://github.com/mihail911/modern-software-dev-assignments/tree/master/week7) 📖

---

## Week 8: Agent运维与可观测性
**主题**: SRE与运维 | **必做**: 1.5h | **完整**: 2.5h

### 📺 Slides (选读)
- [Incident response and DevOps](https://docs.google.com/presentation/d/1Mfe-auWAsg9URCujneKnHr0AbO8O-_U4QXBVOlO4qp0/edit?usp=sharing)

### 阅读材料
| # | 材料 | 优先级 | 时间 | 翻译文件 |
|---|------|--------|------|----------|
| 1 | Introduction to SRE | ⭐ | 25min | week9_01_introduction_to_sre.md |
| 2 | Observability Basics | ⭐ | 15min | week9_02_observability_basics_traces_spans.md |
| 3 | Kubernetes Troubleshooting with AI | 📖 | 15min | week9_03_kubernetes_troubleshooting_with_ai.md |
| 4 | Your New Autonomous Teammate | 📖 | 15min | week9_04_your_new_autonomous_teammate.md |
| 5 | Role of Multi Agent Systems | ⭐ | 15min | week9_05_role_of_multi_agent_systems.md |
| 6 | Benefits of Agentic AI in On-call | 📖 | 10min | week9_06_top_5_benefits_of_agentic_ai.md |

### 核心概念
- **SRE**: 站点可靠性工程
- **Observability**: 可观测性 (Logs, Metrics, Traces)
- **Incident Response**: 事件响应

---

## Week 9: AI软件工程的未来
**主题**: 展望未来 | **必做**: 0.5h | **完整**: 1h

### 📺 Slides (选读)
- Software development in 10 years
- Guest - Martin Casado (a16z General Partner)

> 本周为展望性内容，无阅读材料和作业

---

## 课程总量一览

| 类型 | 数量 | 必做时间 | 全部时间 |
|------|------|----------|----------|
| Reading | 45篇 | ~16小时 | ~30小时 |
| Slides | 15个 | ~2小时 | ~4小时 |
| Assignment | 8个 | ~6小时 | ~12小时 |
| **总计** | | **~24小时** | **~46小时** |

## 推荐学习路径

```
Week 1 → Week 2⭐ → Week 4⭐ → Week 3 → Week 6⭐ → Week 5 → Week 7 → Week 8 → Week 9
```
先打LLM基础，Week 2 (MCP) 是核心，Week 6 (安全) 很重要

## 外部链接说明

部分阅读材料标记了 🔗需访问原链接，这些内容包括：
- **GitHub 仓库**: 代码库需要实际浏览和操作
- **工具教程**: 如 Warp 需要安装并实际使用
- **动态内容**: 如 OWASP 列表会定期更新

翻译提供了核心概念和结构，但完整学习需访问原链接。
