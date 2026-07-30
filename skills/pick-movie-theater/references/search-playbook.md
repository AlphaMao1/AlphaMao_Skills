# 免费搜索与覆盖审计

## 范围

- **发现范围**：默认整个地级市／直辖市，不只搜索中心城区；覆盖下辖区县、县级市和新区中可能改变结论的效果型影厅。目标是建立“效果优先候选全集”，不是穷举所有普通影院。
- **推荐范围**：约 45 分钟为日常参考；出现画幅、胶片、投影或声音的显著跃迁时可到约 90 分钟。
- **跨城范围**：只在本地没有稀缺格式时作为增强建议，明确交通代价。
- 路线不可得时使用公开距离、地标或行政区近似，标注“非实时路线”。

## 先建立效果优先候选全集

使用本 Skill 的用户默认追求观影效果。开始影片匹配前，先逐项召回本地可能成为画面、声音或独占体验首选的影厅；普通厅不做全量枚举。

每次必须逐项搜索并记录以下格式家族，不能用一次宽泛的“城市 + 高端影院”代替：

| 覆盖键 | 必查家族与同义词 |
| --- | --- |
| `imax` | IMAX 70mm、GT Laser、激光 IMAX、Commercial Laser／CoLa、Laser XT、数字／氙灯 IMAX |
| `dolby` | Dolby Cinema／杜比影院、Dolby Vision、Dolby Atmos／杜比全景声、杜比 7.1、带杜比字样的营销厅 |
| `cinity` | CINITY、CINITY 4K／HFR、CINITY 投影厅 |
| `cgs` | CGS、中国巨幕、中国巨幕 CINITY 等当前组合名称 |
| `cinema_led` | CINITY LED、Samsung Onyx、HeyLED、DCI LED、透声 LED 电影屏 |
| `screenx` | ScreenX、ULTRA 4DX 中的侧幕能力、其他有专用侧画面的认证格式 |
| `motion_effects` | 4DX、MX4D、D-BOX、ICE Immersive、其他动感／环境效果厅 |
| `premium_sound` | Dolby Atmos、DTS:X、THX 及其他可核验沉浸声或高规格声学厅 |
| `other_plf` | LUXE、激光巨幕、双机激光、4K 激光巨幕、院线自有 PLF 和无法从名称判断的高规格厅 |

某家影院可以进入多个家族，但去重后仍以具体影厅为核验对象。某家族没有候选，也必须记录 `searched: true` 和零结果；来源受阻则记录受阻，不能当成已覆盖。

地理搜索至少包含：

1. 城市标准名；
2. 用户所在区县；
3. 城市下辖区县、县级市和新区名称与上述格式词组合；
4. 约90分钟范围内可能形成明显能力跃迁的相邻地点。

只有形成候选全集后，才按影片当地版本淘汰不相关格式。影片没有相应版本，不等于本地该格式家族没有搜索。

## 必做发现入口

按顺序执行并记录每轮新增候选：

1. `format_official`：影片相关格式方、发行方和官方参与影院。
2. `city_format`：按上表逐个家族执行城市、下辖区县和县级市组合搜索。
3. `reputation`：城市 + 最佳影院／顶级影厅／影院测评／最佳音效／银幕尺寸。
4. `upgrade`：城市／影院 + 新开业／改造／换机／激光／升级／重新开业。
5. `snowball`：候选影院全名 + 厅号／设备／银幕／座位／对比／缺点／排片。

影片、院线或格式官方名录有相关入口时先检查。某格式与本片无关时记录“本片不适用”，但仍保留城市候选召回是否完成的记录。

## 查询矩阵

对全城召回使用：

```text
"城市／下辖区县／县级市" IMAX／杜比影院／CINITY／CINITY LED／CGS
"城市／下辖区县／县级市" ScreenX／4DX／MX4D／ICE／LUXE
"城市／下辖区县／县级市" LED电影屏／Onyx／HeyLED／透声屏
"城市／下辖区县／县级市" Atmos／DTS:X／THX／双机激光／4K激光巨幕
"城市" "影片名" IMAX／杜比影院／CINITY／ScreenX／4DX／LED
"城市" 最佳 影厅 OR 顶级 影院
"城市" 影院 升级 OR 改造 OR 换机 OR 新开业
site:weibo.com "城市" "影院名" 厅
site:zhihu.com "城市" 影院 IMAX
site:bilibili.com "影院名" 测评
site:mp.weixin.qq.com "影院名" 升级
site:xiaohongshu.com "影院名" 厅号
```

对收敛候选使用：

```text
"影院标准名" "厅号" 投影机／双机／激光／2K／4K
"影院标准名" 银幕 尺寸／比例／1.43／1.90
"影院标准名" Dolby Cinema／Dolby Atmos／CINITY／CGS
"影院标准名" 排片 "影片名" 日期
"影院标准名" 遮挡／偏色／亮度／音响／维修
```

同义词、旧名、商场名和英文名分别搜索；同一转载不要计为独立入口。

搜索引擎展开票务页时可能混排多部影片。摘要只承担发现；必须回到目标影片区块核对影片、日期、时间、影院、厅号和标签。原页无法打开时记录 `search_index_snapshot`，不得把摘要升级为实时可购，也不得从同页其他影片区块补齐缺失字段。

## 社交媒体路径

公开模式优先用普通网页搜索和 `site:`，再使用公开可访问的微博、知乎、微信公众号、B站、社区和小红书页面。社交内容适合发现：

- 新开／升级／临时故障；
- 具体厅号、座位图和银幕实拍；
- 亮度、遮挡、异响等近期体验线索；
- 进一步检索所需的设备名或旧厅名。

社交热度不证明认证或技术字段。“站内未找到”也不证明信息不存在。

把“院线电影资料库”作为影片发行版本的固定专业线索源时，只使用微博账号 `@院线电影资料库`，不再同时检查其小红书账号。它与其他平台同名账号按同一来源家族去重；其内容只产生版本字段线索，决定性事实仍按证据政策复核。

仅在用户明确同意且运行环境有 Chrome 控制能力时，才用已有登录态对已收敛的候选做小红书等站内精确搜索。只读，不批量抓取，不访问无关账号信息；遇验证码、登录限制或访问异常立即停止，记录为 `blocked_sources`，核心流程继续。

## 去重与候选晋级

用标准名、地址、商场和旧名归并影院；影厅仍保留独立实体。满足以下任一条件才深入核验：

- 出现在本片相关的官方格式入口；
- 有本片特殊格式场次；
- 有影院、院线或设备方的明确能力说明；
- 被多个独立来源反复列为当地优质选择；
- 存在足以改变结论的非品牌稀缺能力。

高级候选不足时可加入证据完整的普通厅作为稳妥备选。

## 覆盖包与停止条件

维护一个临时包：

```json
{
  "official_relevant_checked": true,
  "required_passes": {
    "format_official": true,
    "city_format": true,
    "reputation": true,
    "upgrade": true,
    "snowball": true
  },
  "format_families": {
    "imax": {"searched": true, "candidate_ids": []},
    "dolby": {"searched": true, "candidate_ids": []},
    "cinity": {"searched": true, "candidate_ids": []},
    "cgs": {"searched": true, "candidate_ids": []},
    "cinema_led": {"searched": true, "candidate_ids": []},
    "screenx": {"searched": true, "candidate_ids": []},
    "motion_effects": {"searched": true, "candidate_ids": []},
    "premium_sound": {"searched": true, "candidate_ids": []},
    "other_plf": {"searched": true, "candidate_ids": []}
  },
  "discovery_passes": [
    {"name": "upgrade", "independent": true, "new_candidates": 0},
    {"name": "snowball", "independent": true, "new_candidates": 0}
  ],
  "candidates": [
    {"id": "影院标准名", "status": "verified"}
  ],
  "screening_binding_audit": {
    "ready": true,
    "invalid_screening_ids": []
  },
  "blocked_sources": []
}
```

只有官方相关入口已检查、九个效果型格式家族逐项搜索、规定入口已执行、连续两个独立补漏入口零新增、剩余候选均为 `verified` 或 `unresolved`，且场次绑定审计没有无效项时，才能声明“本轮优质候选搜索达到饱和”。同时输出停止原因、受阻来源和剩余风险；不能声称全市影院零遗漏。
