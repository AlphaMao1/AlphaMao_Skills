# Serenity Thesis Tracker

把 Serenity 的 X 帖子整理成可持续追踪的投资研究资产。

高质量信息源的问题不是“有没有看到”，而是看完以后有没有沉淀。这个 Skill 用来把 Serenity 的 X 帖子转成结构化研究状态：thesis、claim、ticker、公司文件、供应链关系、日报、周报和后续研究 backlog。

## 适合

- 跟踪 Serenity / @aleabitoreddit 的投资观点
- 把 X 帖子转成可验证的研究线索
- 维护公司级 research file 和 supply-chain map
- 生成日度 intake、周度 review 和后续研究任务

## 它会做什么

- 抓取或整理 Serenity 帖子
- 识别 ticker、公司、供应链关系和投资 thesis
- 把观点拆成可验证 claim
- 更新公司文件和研究 backlog
- 输出 daily / weekly research report

## 当前版本说明

这一版是 **PaiWork 适配版**。它默认使用 PaiWork 的研究工作区、analyst/report 工具、市场数据、搜索能力和研究数据源来完成抓取后的分类、验证、公司文件更新与报告生成。

如果你在其他 Agent 环境中安装，建议安装后先让 Agent 检查本地可用工具、数据源、浏览器登录态和工作区结构，再把 `SKILL.md` 中的 PaiWork 相关步骤适配为你的本地流程。也可以先收藏这个 Skill，等待后续通用版本更新。

如果你在 **PaiWork** 上使用，建议安装后直接让 Agent 根据这个 Skill 创建自动化任务，例如定时抓取 Serenity 最新内容、生成每日 intake、更新 thesis / claim / company files，并把日报或周报写入指定研究工作区。这样它就不是一次性整理工具，而是一个持续运行的研究跟踪流程。

## 怎么触发

```text
整理 Serenity 今天的推文
生成 Serenity daily report
把这条 tweet 变成 thesis tracker
更新公司研究文件
```

## 安装

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/serenity-thesis-tracker
安装后先检查我的本地环境，把 PaiWork 相关工具和数据源适配成可用流程
如果我在 PaiWork 上使用，请基于这个 skill 创建 Serenity 跟踪自动化任务
```

## 小红书讲解

把 Serenity 的 X 变成可持续追踪的研究

<http://xhslink.com/o/4y5hTyS0hnf>

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
- [scripts/](./scripts/)
- [assets/](./assets/)
