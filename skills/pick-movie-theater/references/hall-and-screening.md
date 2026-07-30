# 影院、影厅与场次核验

## 目录

- 四层对象
- 影院字段
- 影厅字段与核验顺序
- 场次字段
- 最小购票前复核

## 四层对象

| 对象 | 主键建议 | 不能自动继承的事实 |
| --- | --- | --- |
| 影片版本 | 影片 + 地区 + 发行窗口 + 版本 | 海外或另一格式的母版 |
| 影院 | 标准名 + 地址 | 旗下任一影厅的投影与声音 |
| 影厅 | 影院 + 当前厅号／厅名 + 有效日期 | 同影院其他厅或升级前设备 |
| 场次 | 日期时间 + 影院 + 影厅 + 购票版本标注 | 影厅理论能力或过期排片 |

座位建议附属于具体影厅；当前可售座位附属于具体场次和核查时间。

## 影院字段

```yaml
canonical_name:
aliases: []
former_names: []
address:
mall_or_landmark:
operator:
opened_or_reopened_at:
official_page:
checked_at:
```

用地址和商场消除同名；保存旧名以继续搜索，但不要把旧公告静默视为当前事实。

## 影厅字段

```yaml
hall_id:
hall_name:
former_hall_ids: []
format_or_certification:
projection:
  system:
  generation:
  light_source:
  resolution:
  projector_count:
  max_effective_aspect_ratio:
screen:
  width_m:
  height_m:
  native_aspect_ratio:
  geometry:
  masking_type: none／fixed／movable／unknown
  masking_positions: []
sound:
  system:
  generation:
seating:
  rows:
  seat_count:
  aisles:
  accessible_or_special_seats:
  known_obstructions:
last_upgrade_at:
last_verified_at:
```

每个技术字段单独附证据等级、来源和冲突状态。格式名不能填满未知设备字段。

## 影厅核验顺序

1. 格式认证方或官方影院名录。
2. 影院／院线页面、开业或改造公告。
3. 设备商、施工方和可靠行业报道。
4. 当前购票页或影院排期对厅号的映射。
5. 两个独立且近期的具体厅社区来源。
6. 单一帖子、图片或营销名只保留为线索。

如果厅号在升级后发生变化，建立显式映射并附日期；无法证明映射时不要合并。

## 场次字段

```yaml
film:
date_time:
cinema:
hall:
ticket_label:
ticket_url:
observed_at:
sale_status:
film_version_match: confirmed／conditional／conflicted
presentation:
  dcp_aspect_ratio:
  image_fit: matched／letterbox／pillarbox／cropped／unknown
  actual_frame_rate:
  native_audio_mix:
  playback_sound_path:
source_binding:
  source_kind: direct_ticket_page／official_schedule／search_index_snapshot
  source_block_id:
  field_block_ids:
    film:
    date:
    time:
    cinema:
    hall:
    ticket_label:
  page_reopened: true／false
  observed_at:
```

推荐时分别写：

- **影厅理论最佳**：能力已确认，但不表示本片当前上映。
- **当前可确认场次**：日期、影院、具体厅和票务标注可复核。
- **条件式场次**：厅或版本有一项未确认，给出购票前核查动作。

### 同一影片区块绑定

票务页、搜索摘要或影院页同时列出多部影片时，先按影片标题切分区块。每条场次的影片、日期、时间、影院、厅号和购票标签必须来自同一目标影片区块，并保存相同的 `source_block_id`。页面级影院名称可以填入该区块，但另一影片区块的时间、厅号和格式不能继承。

出现以下任一情况时，不得写成当前可确认：

- 目标影片标题与场次字段之间出现另一部影片标题；
- 字段来自不同搜索摘要、轮播卡片或表格区块；
- 搜索索引只展示局部文本，无法判断字段所属影片；
- 原始票务页打不开，只能依赖搜索引擎旧快照；
- 日期、厅号或购票标签中至少一项没有区块级来源。

把所有具体场次写入绑定包并运行：

```powershell
python -X utf8 scripts/decision_support.py screenings --input screenings.json
```

`invalid` 场次必须删除或重新核验；`conditional` 只能作为购票线索；只有 `current_confirmed` 才能声称当前可确认。脚本验证的是记录的一致性，仍需人工确认区块切分和来源文本没有抄错。

购票页没有厅号时，不能把该场次归入影院的最佳厅。过期页面只能证明历史排片。

银幕与影片必须单独接线。影厅有可变遮幅不等于本场正确使用；固定2.39银幕也不等于1.85版本更差。记录片源画幅、银幕原生比例、遮幅位置和实际适配方式后再判断。影厅支持120fps、Atmos或12声道不等于本片拷贝具有对应帧率或原生音轨。

## 最小购票前复核

让用户核对：

1. 影院标准名和地址；
2. 日期、时间与具体厅号；
3. 页面显示的格式／2D／3D／语言；
4. 该厅是否刚改名、升级或临时维护；
5. 截图或页面核查时间。

实时排片不可访问时，不伪造场次；保留条件式推荐并说明下一步到猫眼、淘票票或影院官方页确认。
