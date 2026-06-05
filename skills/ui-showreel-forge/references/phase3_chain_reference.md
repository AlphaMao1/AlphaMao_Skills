# Phase 3: 链式垫图生成（核心方法论）

## 为什么需要链式垫图法

AI 图像生成模型在同一个 session 内，每次调用都是独立的。即使用同一套文字描述，生成出来的载体形状、厚度、颜色、角度也会有微小差异——这些差异放在静图里几乎不可见，但在视频中拼接时会产生明显的跳切感（风格不连续）。

**解决方案**：每次生成时，把**上一帧已生成的图像**作为垫图输入，而不是原始 UI 截图。这样模型会从物理图像本身提取载体特征，而不依赖文字推演，一致性显著提升。

## 垫图 DAG（有向无环图）

```
风格参考图 + UI-A截图
    ↓ generate_image
F1（锚点帧/建立帧）
    ↓ 垫图
F2（过渡帧）← 只用 F1

F1（风格锚）+ UI-B截图
    ↓ generate_image
F3（建立帧）

F3（生成图）
    ↓ 垫图
F4（效果帧）← 只用 F3，不用原始UI截图

F1（风格锚）+ UI-C截图
    ↓ generate_image
F5（建立帧）

F5（生成图）
    ↓ 垫图
F6（效果帧）

...以此类推...

F1（风格锚）
    ↓ 垫图
F9（失重全景建立帧）

F9（生成图）
    ↓ 垫图
F10（粒子解体效果帧）
```

**两条核心链路**：
1. **同-slot 链**：建立帧 → 效果帧。效果帧用该 slot 的建立帧作为垫图，载体保持一致，只叠加效果。
2. **跨-slot 链**：新建立帧用 F1（锚点帧）作为风格参考，確保所有建立帧的载体风格来自同一源头。

## 垫图 Prompt 策略

### 建立帧 Prompt 模板

```
Use the EXACT same [carrier style, shape, edge treatment, background color, camera angle] 
from the FIRST reference image. Replace ONLY the UI content on the surface 
with [UI description from SECOND reference image]. 
Everything else — carrier proportions, floating position, [specific consistent elements] — 
must be identical to the first reference. 
Clean static establishing frame. No effects.
```

**关键词**：
- `EXACT same` — 强调一致性
- `Replace ONLY` — 明确哪个变、哪个不变
- `Everything else... must be identical` — 防止模型自由发挥

### 效果帧 Prompt 模板

```
The EXACT same [carrier description] from the reference image, 
same position, same [background], same [edge treatment]. 
ADDED EFFECT: [具体效果描述]. 
The [carrier] itself remains completely unchanged. Same [background]. 
Premium [effect type] frame.
```

**关键**：先复述「不变的东西」，再说「效果」，模型才不会改变载体。

## 并行 vs 串行执行

- **可以并行**：同一级别的建立帧（F3、F5、F7 都用 F1 作为风格锚，可以同时生成）
- **必须串行**：效果帧需要等对应建立帧生成完毕才能开始
- **必须串行**：F9、F10 各自依赖前一帧

**实际执行顺序**：
1. 同时生成 F1（锚点）
2. 同时生成 F2、F3、F5、F7（F2 用 F1，其余用 F1+UI截图）
3. F2 完成后（一般和 F3/F5/F7 差不多时间），同时生成 F4、F6、F8
4. F8 完成后生成 F9
5. F9 完成后生成 F10

## 常见失败模式

| 症状 | 根因 | 修复 |
|---|---|---|
| 部分帧背景变色（纯黑→深灰→绿色） | 原始UI截图的背景色污染了生成结果 | Prompt 中明确写 `pure black (#000000) background is mandatory` |
| 载体形状/厚度漂移 | 没有用生成图作为垫图，靠文字描述重建 | 检查 DAG，确认每帧的垫图输入是已生成图而非截图 |
| 效果帧载体和建立帧不一样 | 效果帧用了错误的垫图（用了 F1 而不是对应建立帧） | 严格按 DAG 执行，效果帧的垫图 = 该 slot 的建立帧生成图 |
| 建立帧带入了 effect（卡片飞入等） | 风格参考图本身包含 effect | 重新选择风格参考图，或在 Prompt 中加 `NO cards flying out, NO effects, NO exploded elements` |
| 模型容量不足（503） | 高峰期并发限制 | 等待后重试；已成功的帧不需要重新生成 |
