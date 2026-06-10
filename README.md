<div align="center">

# AlphaMao Skills

#### 我在小红书分享的 AI Agent Skills，都整理在这里

[![Skills](https://img.shields.io/badge/Skills-7-10B981?style=for-the-badge)](#skills)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-SKILL.md-8B5CF6?style=for-the-badge)](#install)
[![Codex](https://img.shields.io/badge/Codex-Ready-111827?style=for-the-badge&logo=openai&logoColor=white)](#install)
[![Xiaohongshu](https://img.shields.io/badge/小红书-Alpha%20Mao-FF2442?style=for-the-badge)](#about)

![Research](https://img.shields.io/badge/Research-Current_Model-3B82F6?style=flat-square)
![Investment](https://img.shields.io/badge/Investment-Agent_Workflow-10B981?style=flat-square)
![Content](https://img.shields.io/badge/Content-Build_in_Public-F97316?style=flat-square)

</div>

这里不是提示词合集，而是一组可以被 Agent 直接加载的工作流。

我在小红书账号 **Alpha Mao** 分享自己实际使用的 AI Skill、投研工作流、技术研究方法和内容生产实践。小红书笔记负责解释“为什么值得这样做”，这个仓库负责提供“怎么让 Agent 真的去做”。

---

<a id="skills"></a>

## Skills

| Skill | 一句话 | 小红书讲解 | 目录 |
|---|---|---|---|
| Progressive Investment Research | 把零散材料、判断和数字维护成可持续更新的投研工作区 | 我用 Skill 搭了个持续更新的投研工作区<br><http://xhslink.com/o/4GUbrB6dvLr> | [`skills/progressive-investment-research`](./skills/progressive-investment-research/) |
| Technology Mapping | 从一个硬科技关键词出发，生成技术源流、学术谱系和商业化图谱 | 一个 Skill 搞定硬科技投资中的技术 mapping<br><http://xhslink.com/o/9vGoxXSqLrS> | [`skills/technology-mapping`](./skills/technology-mapping/) |
| Serenity Thesis Tracker | 把 Serenity 的 X 帖子变成可持续追踪的投资研究线索 | 把 Serenity 的 X 变成可持续追踪的研究<br><http://xhslink.com/o/4y5hTyS0hnf> | [`skills/serenity-thesis-tracker`](./skills/serenity-thesis-tracker/) |
| Creator Research Tracker | 把 X / YouTube / newsletter 博主更新变成 progressive research 工作区增量 | 把 X 博主的每日更新接进自己的投研工作区<br><http://xhslink.com/o/7cunSYmYq2d> | [`skills/creator-research-tracker`](./skills/creator-research-tracker/) |
| UI Showreel Forge | 把 UI 截图变成风格一致的 showreel 垫图和视频导演脚本 | 运镜乱飘？一个 Skill 搞定 UI 演示动画<br><http://xhslink.com/o/7LmFimZYx8m> | [`skills/ui-showreel-forge`](./skills/ui-showreel-forge/) |
| Market Sizing | 用 Fermi、Monte Carlo 和公开数据源估算 TAM / SAM / SOM | 一个 Skill 搞定 Market Sizing<br><http://xhslink.com/o/9zGJ009rm21> | [`skills/market-sizing`](./skills/market-sizing/) |
| Stanford Vibe Coding Course | 把 Stanford CS146S / vibe coding 课程变成可跟踪的学习系统 | 斯坦福 Vibe Coding 课程学习系统开源<br><http://xhslink.com/o/1qmfBbWYKku> | [`skills/stanford-vibe-coding-course`](./skills/stanford-vibe-coding-course/) |

---

<a id="install"></a>

## Install

在支持 `SKILL.md` 的 Agent 里，可以直接说：

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/<skill-name>
```

例如：

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/progressive-investment-research
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/technology-mapping
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/creator-research-tracker
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/ui-showreel-forge
```

你也可以直接 clone 本仓库，然后把需要的目录复制到自己的 skills 目录：

```bash
git clone https://github.com/AlphaMao1/AlphaMao_Skills.git
```

---

## Featured

<table>
<tr><td>

### Progressive Investment Research

> 不要让 AI 每次从零写报告。真正有价值的是一个能持续恢复、持续更新的研究模型。

它把长期研究维护成一个 `dossier`：当前模型、研究地图、开放问题、模块、计算模型和更新日志。适合投资研究、产业研究、公司研究和任何需要长期积累判断的复杂问题。

**适合**

- 持续研究一个行业、公司或技术主题
- 把材料、数字、假设和冲突沉淀成可恢复的 Current Model
- 多轮研究后继续接上，不想每次从聊天记录里重新找状态

**触发方式**

```text
研究一下这个行业
继续这个 dossier
更新 Current Model
把这批材料吸收到模型里
```

→ [SKILL.md](./skills/progressive-investment-research/SKILL.md) · 小红书讲解：<http://xhslink.com/o/4GUbrB6dvLr>

</td></tr>
</table>

<table>
<tr><td>

### Technology Mapping

> 硬科技投资最难的不是查公司，而是看懂技术源流、学术谱系和商业化分叉。

它从一个技术关键词出发，自动梳理领域锚点、创业公司、创始团队、师承链、技术路线和里程碑，最后生成技术 mapping 图谱和可追溯报告。

**适合**

- VC / 投资人做硬科技赛道扫描
- 从零理解一个前沿技术领域
- 找出学术源头、公司分支和商业化路径

**触发方式**

```text
做一个技术 mapping
帮我画一下这个赛道的技术全景图
研究一下这个硬科技方向的源流
```

→ [SKILL.md](./skills/technology-mapping/SKILL.md) · 小红书讲解：<http://xhslink.com/o/9vGoxXSqLrS>

</td></tr>
</table>

<table>
<tr><td>

### Serenity Thesis Tracker

> 好的 X 信息源不是看完就划走，而是要变成可追踪、可验证、可复盘的研究资产。

这个 Skill 用来把 Serenity 的 X 帖子整理成投资 thesis、claim ledger、公司研究文件、供应链关系图、日报、周报和后续研究 backlog。

**适合**

- 跟踪高质量投资信息源
- 把碎片化 X 帖子转成结构化研究线索
- 做公司、供应链、ticker 和 thesis 的连续跟踪

**触发方式**

```text
整理 Serenity 今天的推文
生成 Serenity daily report
把这条 tweet 变成 thesis tracker
更新公司研究文件
```

→ [SKILL.md](./skills/serenity-thesis-tracker/SKILL.md) · 小红书讲解：<http://xhslink.com/o/4y5hTyS0hnf>

</td></tr>
</table>

<table>
<tr><td>

### Creator Research Tracker

> 把“我每天看了哪些博主”升级成“哪些观点进入了可验证的研究工作区”。

这个 Skill 是 Serenity 案例的通用本地版。它保留每日跟踪体验，但不依赖 PaiWork 专有工具：先生成 creator daily report，再把有价值内容拆到 progressive research 的 source leads、公司页、行业模块和开放问题。

使用前需要安装 `progressive-investment-research`；安装后可以让 Agent 创建每日自动化任务，定时抓取已注册来源、生成日报并拆到研究工作区。

**适合**

- 跟踪 X/Twitter、YouTube、newsletter 或类似个人信息源
- 用 Chrome 登录态抓 X 原文，并拦截 UI 自动翻译、搜索摘要和公开镜像
- 把博主观点转成可审计的公司、行业和机制研究增量
- 每天自动生成 creator daily report 并 route 到 progressive research

**触发方式**

```text
把这个博主加入跟踪
生成 RihardJarc daily report
把这条 X 拆成研究线索
更新 creator 研究工作区
```

→ [SKILL.md](./skills/creator-research-tracker/SKILL.md) · 小红书讲解：<http://xhslink.com/o/7cunSYmYq2d>

</td></tr>
</table>

<table>
<tr><td>

### UI Showreel Forge

> UI 演示动画最怕每一帧都像重新生成的产品。这个 Skill 解决的是跨帧一致性。

它把静态 UI 截图转成 showreel 垫图序列和视频模型可直接使用的导演脚本，特别适合 Kling、Omni 等图生视频工作流。

**适合**

- 做产品演示动画
- 把 UI 截图变成一组风格稳定的关键帧
- 给视频模型准备分镜、垫图和运镜说明

**触发方式**

```text
/ui-showreel-forge
把这组 UI 做成 showreel
给我生成 Kling 可用的导演脚本
```

→ [SKILL.md](./skills/ui-showreel-forge/SKILL.md) · 小红书讲解：<http://xhslink.com/o/7LmFimZYx8m>

</td></tr>
</table>

<table>
<tr><td>

### Market Sizing

> 市场规模不是拍脑袋写一个大数字，而是把假设、口径和不确定性拆开。

这个 Skill 用来做 TAM / SAM / SOM 测算，支持 Fermi 拆解、Monte Carlo 不确定性估计、公开数据源辅助和结构化报告输出。

**适合**

- 估算一个新市场有多大
- 投资 memo / 商业计划里的市场规模测算
- 把“看起来很大”拆成可讨论的假设

**触发方式**

```text
测算一下这个市场规模
帮我做 TAM/SAM/SOM
这个赛道市场有多大
```

→ [SKILL.md](./skills/market-sizing/SKILL.md) · 小红书讲解：<http://xhslink.com/o/9zGJ009rm21>

</td></tr>
</table>

<table>
<tr><td>

### Stanford Vibe Coding Course

> 看课程不难，难的是把课程变成可持续学习、复盘和输出的系统。

这个 Skill 面向 Stanford CS146S / The Modern Software Developer 课程学习，把课程材料、笔记、作业、复习和进度追踪组织成一个学习工作流。

**适合**

- 系统学习 vibe coding / AI-assisted software development
- 用 Obsidian 管理课程笔记和复习
- 让 Agent 帮你解释概念、安排进度、检查作业

**触发方式**

```text
开始学习 CS146S
继续 Stanford vibe coding 课程
解释这一周课程
帮我复习这节课
```

→ [SKILL.md](./skills/stanford-vibe-coding-course/SKILL.md) · 小红书讲解：<http://xhslink.com/o/1qmfBbWYKku>

</td></tr>
</table>

---

<a id="about"></a>

## About

我是 **Alpha Mao**，一线市场投资人，长期关注 AI Agent、硬科技投资、投资研究自动化、AI-native 内容生产和个人知识系统。

我会在小红书分享自己实际使用的 Skill、工作流和实验过程。这个仓库是这些分享背后的开源执行层。

如果这些 Skill 对你有帮助，欢迎 star，也欢迎提 issue 交流使用场景。
