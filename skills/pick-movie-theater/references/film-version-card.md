# 影片版本卡

## 目标

先确认“这部片在这个地区、这段日期实际有哪些版本”，再比较影厅。影片版本卡是本次请求的临时工作对象，不建立持久影片数据库。

## 最小结构

```yaml
film:
  canonical_title: 标准片名
  original_title: 原名或未知
  release_region: 国家／地区
  search_window: YYYY-MM-DD..YYYY-MM-DD
  release_date: 日期或待确认
creative:
  capture_format: 拍摄／动画／创作格式
  intended_aspect_ratios: 比例、片段范围或未知
  sound_mix: Atmos／IMAX 专用混音／其他／未知
masters:
  imax: DMR／Filmed for IMAX／1.90／1.43／70mm／未知
  dolby: Dolby Vision／Atmos／未知
  cinity: 4K／HFR／HDR／3D／未知
  cgs: 专用母版／未知
  screenx: ScreenX／Shot for SCREENX／未知
  motion: 4DX／MX4D／未知
local_distribution:
  confirmed_versions: []
  excluded_or_absent_versions: []
  unknown_versions: []
screening:
  cinema: 待定
  hall: 待定
  ticket_label: 待定
  actual_version: 待确认
```

每个非空事实另附 `status`、`source`、`published_at`、`checked_at` 和 `scope`。状态只用：

- `confirmed`：证据达到决定性字段门槛。
- `inferred`：有推断链但未达到门槛。
- `unknown`：没有足够信息。
- `conflicted`：来源冲突未解决。

## 搜索顺序

1. 影片官方、制片／发行方和本地区定档信息。
2. IMAX、Dolby、CINITY、CGS、CJ 4DPLEX 等格式方的影片页、新闻稿或参与名单。
3. 技术主创访谈、摄影／后期公司、DCP 或放映技术说明。
4. 本地院线和影院公告。
5. 当前票务页；它能证明页面标注和排片，不自动证明底层技术。
6. 社区内容只用于发现版本线索、实拍票根或可二次核验的信息。

## 防误判

- `IMAX release` 不自动变成 `Filmed for IMAX`、1.43:1 或 IMAX 70mm。
- 采用 IMAX 认证摄影机不自动表示整片扩画。
- 影厅支持 4K／120fps 不自动表示本片有 4K／120fps 母版。
- 影院有 ScreenX／4DX 硬件不自动表示当前影片或场次启用专用内容。
- 海外版本存在不自动表示中国大陆或用户所在地区取得相同版本。
- 购票页标签是场次线索；与格式方名单、影院厅号或设备证据冲突时必须保留冲突。

## 完成条件

决定推荐的影片端增量至少有一条当前有效的 A/B 级证据；否则标为待确认，并让推荐降级为条件式。卡片必须带地区和日期，不能把未来、海外或过期场次混入当前可购结论。
