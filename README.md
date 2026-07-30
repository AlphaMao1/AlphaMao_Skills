<div align="center">

# AlphaMao Skills

#### 我在小红书分享的 AI Agent Skills，都整理在这里

[![Skills](https://img.shields.io/badge/Skills-10-10B981?style=for-the-badge)](#skills)
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
| Market Sizing | 用 Excel 公式链、source cards 和逐年 TAM / SAM / SOM 做市场规模测算 | 一个 Skill 搞定 Market Sizing<br><http://xhslink.com/o/9zGJ009rm21> | [`skills/market-sizing`](./skills/market-sizing/) |
| 直觉泵 | 把《直觉泵》的 77 个思考工具变成 Agent 可以路由、学习和调用的思考工具箱 | 把《直觉泵》的77个思考工具变成一个 skill<br><http://xhslink.com/o/5LGsU9I2FoV> | [`skills/intuition-pumps`](./skills/intuition-pumps/) |
| Stanford Vibe Coding Course | 把 Stanford CS146S / vibe coding 课程变成可跟踪的学习系统 | 斯坦福 Vibe Coding 课程学习系统开源<br><http://xhslink.com/o/1qmfBbWYKku> | [`skills/stanford-vibe-coding-course`](./skills/stanford-vibe-coding-course/) |
| Notion Course Pack Init | 把一本书或一门课程初始化成可在 ChatGPT 中持续学习、在 Notion 中保存真实进度的 Course Pack | 怎么用 AI 快速读懂一本书<br><http://xhslink.com/o/AAYwJyc1roT> | [`skills/notion-course-pack-init`](./skills/notion-course-pack-init/) |
| Pick Movie Theater | 按影片版本、位置、具体影厅和场次证据推荐影院、影厅与座位 | 《蜘蛛侠》《奥德赛》看什么厅？<br> | [`skills/pick-movie-theater`](./skills/pick-movie-theater/) |

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
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/intuition-pumps
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/notion-course-pack-init
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

这个 Skill 用来做 TAM / SAM / SOM 测算，强调市场边界、source cards、可解释假设、Excel 公式链、逐年核心结论页和结构化备忘。

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

### 直觉泵

> 面对一个说不清的问题，先找到合适的思考工具，再继续推理。

这个 Skill 把《直觉泵》的 77 个思考工具整理成 Agent 可以使用的路由器和工具卡。它会先根据问题推荐工具，再读取选定卡片，把强烈直觉拆成可比较的版本、边界、反例、机制和验证动作。

**适合**

- 检查一个观点是否偷换了前提或打成了稻草人
- 拆开意识、理解、身份、自由和责任等概念混淆
- 发现解释里的“聪明小人”、魔法步骤或当然跳步
- 在写作、研究和复杂决策中找到可检查的思考路径

**触发方式**

```text
帮我为这个问题推荐合适的思考工具
学习 003 拉波波特
用 010 小心当然检查这个判断
```

→ [SKILL.md](./skills/intuition-pumps/SKILL.md) · 小红书讲解：<http://xhslink.com/o/5LGsU9I2FoV>

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

<table>
<tr><td>

### Notion Course Pack Init

> 把一本书或一门课程变成可以持续学习、持续写回的 Notion 课程系统。

它由 Codex 完成材料读取、路线校准、8 页 Course Pack 创建和写后验证；初始化完成后，ChatGPT 从 Notion 读取真实课程状态，一讲一对话地继续推进。

**适合**

- 把一本完整书籍或课程材料初始化成长期学习系统
- 在 Notion 中保存课程路线、真实进度、Sessions 和候选笔记
- 让 ChatGPT 每次从同一个课程事实源继续，不依赖聊天记忆

**触发方式**

```text
初始化我的 Notion 课程工作区
把这本书做成一个 Course Pack
用 Notion 继续《课程名》
```

→ [README](./skills/notion-course-pack-init/README.md) · [SKILL.md](./skills/notion-course-pack-init/SKILL.md) · 小红书讲解：<http://xhslink.com/o/AAYwJyc1roT>

</td></tr>
</table>

<table>
<tr><td>

### Pick Movie Theater

> 不只告诉你看 IMAX 还是杜比，而是落到这部电影、这座城市、这个影厅和这个场次。

这个 Skill 从公开免费来源重新搜索影片版本和全城效果型影厅，区分影院品牌、具体厅能力与当前排片，再把效果上限、通勤时间、证据风险和选座一起解释清楚。

**适合**

- 比较 IMAX、杜比影院、CINITY、ScreenX、影院 LED 等放映格式
- 在全城最佳和附近通勤方案之间做取舍
- 没有座位图时先选区域，有截图时再选具体座位

**触发方式**

```text
我在这个位置，看《电影名》应该选哪个影院和影厅？
这几个 IMAX、杜比和 CINITY 场次有什么区别？
这是选座截图，帮我挑两个连座。
```

→ [README](./skills/pick-movie-theater/README.md) · [SKILL.md](./skills/pick-movie-theater/SKILL.md) · 小红书讲解：

</td></tr>
</table>

---

<a id="about"></a>

## About

我是 **Alpha Mao**，一线市场投资人，长期关注 AI Agent、硬科技投资、投资研究自动化、AI-native 内容生产和个人知识系统。

我会在小红书分享自己实际使用的 Skill、工作流和实验过程。这个仓库是这些分享背后的开源执行层。

如果这些 Skill 对你有帮助，欢迎 star，也欢迎提 issue 交流使用场景。
