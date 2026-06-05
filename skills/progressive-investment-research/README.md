# Progressive Investment Research

把长期研究维护成一个可恢复、可审计、可持续更新的 `dossier`。

很多研究不是一次性报告，而是一个会持续变化的判断系统。今天读一份材料，明天补几个数字，下周发现原来的假设有冲突。如果这些变化只散落在聊天记录和临时文档里，下一次接续时就会重新迷路。

这个 Skill 的目标是把研究对象维护成一个 Current Model：当前怎么看、知道什么、不知道什么、哪里有冲突、下一步最值得验证什么。

## 适合

- 投资研究、行业研究、公司研究、技术主题研究
- 把零散材料吸收到同一个研究模型里
- 需要长期跟踪开放问题、数字、假设和判断变化
- 多轮研究后希望快速恢复状态，而不是从头读聊天记录

## 不适合

- 只想查一个事实
- 只需要一次性文章或报告
- 没有持续更新需求的轻量问题

## 核心产物

```text
dossier/
├── current-synthesis.md  # 当前模型，人类恢复入口
├── model-map.md          # 研究边界、分析轴、模块和问题地图
├── open-questions.md     # 开放问题、watchlist、暂时关闭的问题
├── update-log.md         # 模型为什么发生变化
├── modules/              # 证据模块、概念框架、审计记录
└── models/               # 公式、参数、情景和可复算推理
```

## 怎么触发

```text
研究一下这个行业
继续这个 dossier
更新 Current Model
把这批材料吸收到模型里
现在这个研究对象是什么状态
```

## 安装

在支持 `SKILL.md` 的 Agent 中说：

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/progressive-investment-research
```

## 小红书讲解

我用 Skill 搭了个持续更新的投研工作区

<http://xhslink.com/o/4GUbrB6dvLr>

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
- [scripts/](./scripts/)
- [templates/](./templates/)
