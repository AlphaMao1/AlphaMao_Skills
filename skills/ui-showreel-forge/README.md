# UI Showreel Forge

把 UI 截图转成风格一致的 showreel 垫图序列和视频导演脚本。

UI 演示动画最常见的问题不是“不会生成图”，而是每一帧看起来像不同产品：载体形状、材质、角度、厚度和光影都在漂移。这个 Skill 的核心是跨帧一致性，让图生视频模型更容易接住同一个 UI 世界。

## 适合

- 给产品做 UI showreel
- 把静态 UI 截图转成关键帧序列
- 给 Kling、Omni 等图生视频模型准备垫图和导演脚本
- 做商业展示、产品宣传、设计稿动态化

## 核心方法

- 建立帧 / 效果帧成对出现
- 用上一张生成图作为下一帧的物理参考
- 先保证 UI 载体一致，再叠加运动和特效
- 最后把关键帧编译成视频模型可读的导演脚本

## 怎么触发

```text
/ui-showreel-forge
把这组 UI 做成 showreel
给我生成 Kling 可用的导演脚本
把这些界面变成产品演示动画
```

## 安装

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/ui-showreel-forge
```

## 小红书讲解

[运镜乱飘？一个 Skill 搞定 UI 演示动画](http://xhslink.com/o/7LmFimZYx8m)

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
