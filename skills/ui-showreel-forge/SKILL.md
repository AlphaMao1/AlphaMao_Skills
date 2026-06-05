---
name: ui-showreel-forge
version: 0.1.0
description: "将 UI 设计稿转化为风格一致的 showreel 垫图序列与可直接用于可灵/Kling、Omni 等图生视频模型的导演脚本工作流。手工触发：/ui-showreel-forge。"
license: MIT
---

# UI Showreel Forge

从 UI 设计稿到商业级动态视频的完整生产工作流。

核心方法论：**链式垫图法**。通过将已生成的图像作为后续帧的物理参考输入，在 AI 图像生成中实现跨帧风格一致性。配套「建立帧/效果帧」分镜规划和可灵/Kling、Omni 等图生视频模型可直接使用的导演脚本格式。

## 何时使用

在以下场景使用本 skill：

- 你已经有一组 UI 设计稿，想做成高质感 showreel、产品宣传片或动态展示视频
- 你需要先产出风格一致的关键帧/垫图，再交给可灵/Kling、Omni 等视频模型生成动态片段
- 你希望把“截图变视频”从拍脑袋式提示词，升级成稳定、可复用的生产流程

## 默认工具链

本 skill 当前默认围绕下面这套组合设计：

- `Stitch MCP`：生成或批量获取 UI 截图
- `图像生成模型`：基于风格参考图和链式垫图法生成建立帧/效果帧
- `可灵 / Kling` 或 `Omni`：消费关键帧和导演脚本，生成最终动态视频

如果你不用可灵/Kling，只要目标模型支持多图输入、图生视频或导演脚本式控制，也可以复用这套方法。

## 典型输入

- Stitch MCP 生成的 UI 截图
- 1 张风格参考图
- 可选的反面案例图
- 目标视频比例、节奏和镜头风格要求

## 典型输出

- N 张风格一致的 showreel 垫图序列
- 一份建立帧/效果帧分镜表
- 一份可直接粘贴到可灵/Kling、Omni 等模型中的导演脚本

## 整体流程

```
[Phase 0] Stitch MCP 生成 UI 设计稿
    ↓
[Phase 1] 素材准备：截图 + 风格锚定参考图
    ↓
[Phase 2] 分镜规划：建立帧/效果帧交替 + 过渡逻辑
    ↓
[Phase 3] 链式图像生成：锚点帧 → 建立帧 → 效果帧（DAG 顺序执行）
    ↓ 每帧生成后立即目视自检，不合格立即返工
[Phase 4] 自检与返工
    ↓
[Phase 5] 导演脚本编译（面向可灵/Kling、Omni 等模型）
```

## 强约束

- 先有完整分镜，再开始生成图片
- 每个效果帧前必须有对应建立帧
- 所有效果帧必须基于对应建立帧继续生成，而不是回到原始截图重建
- 每次生成完立即目视检查，不要把问题积累到最后

## 参考文档

- `references/phase1_material_prep.md`：素材准备与风格锚定
- `references/phase2_storyboard.md`：分镜规划与视觉盲点设计
- `references/phase3_chain_reference.md`：链式垫图生成方法论
- `references/phase4_self_check.md`：自检与返工协议
- `references/phase5_omni_script.md`：导演脚本编译模板
