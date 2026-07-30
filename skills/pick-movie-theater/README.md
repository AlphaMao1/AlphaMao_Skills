# Pick Movie Theater

按影片版本、用户位置、具体影厅能力和当前场次，选择值得去的影院、影厅与座位区域。

这个 Skill 解决的不是“哪家影院名气最大”，而是：这部电影在你所在城市有哪些真正值得比较的放映格式，具体是哪一个厅，本场能否兑现影片版本，以及为了效果需要多走多远。

## 适合

- 不知道 IMAX、杜比影院、CINITY、ScreenX、4DX、影院 LED 等格式怎么选
- 想在“效果最好”和“离我更近”之间做有理由的取舍
- 需要确认推荐落到具体影厅，而不是只停留在影院品牌
- 想知道某部电影是否真的有对应的特殊画幅、声音、HDR 或高帧率版本
- 没有座位图时先选区域，提供猫眼、淘票票或影院购票页截图后再选具体座位

## 不适合

- 自动购票、锁座或代替用户完成支付
- 绕过登录、验证码、反爬或付费数据库
- 把影院宣传名称直接当成已经核实的设备能力
- 承诺全国所有普通影院零遗漏
- 在没有当前排片和具体厅号证据时编造可购场次

## 它会做什么

1. 建立影片版本卡，区分创作格式、当地发行版本和当前场次实际可取得的版本。
2. 按整个城市召回效果型影厅，覆盖 IMAX、Dolby、CINITY、CGS、影院 LED、ScreenX、动感效果、沉浸声和其他 PLF。
3. 把影院、具体影厅、场次和影片版本作为四个独立对象核验，避免能力错误继承。
4. 解释购票标签真正保证什么、不保证什么，以及本片为什么值得选择该格式。
5. 在效果、声音、观看几何、交通、价格、证据质量和用户偏好之间排序。
6. 没有截图时给平衡、沉浸、舒适和避雷区域；有截图时再判断具体可售座位。
7. 输出关键来源、证据等级、搜索覆盖范围、停止原因和购票前复核动作。

## 怎么触发

```text
我在成都南部，想看这部电影，开车 30 分钟内哪个厅效果最好？
北京看《电影名》应该选 IMAX、杜比影院还是 CINITY？
帮我比较这几个场次，告诉我为什么选其中一个。
这是猫眼选座截图，帮我选两个连座。
```

只要提供影片名称和能限定城市的位置，Skill 就能开始。日期、通勤时间、偏好和选座截图都是可选增强。

## 安装

在支持 `SKILL.md` 的 Agent 中安装：

```text
帮我安装这个 skill：https://github.com/AlphaMao1/AlphaMao_Skills/tree/main/skills/pick-movie-theater
```

手动安装时，请保留整个目录结构：

```text
pick-movie-theater/
├── SKILL.md
├── README.md
├── agents/
├── references/
├── scripts/
└── tests/
```

## 依赖与数据来源

- 核心脚本只使用 Python 标准库。
- 不依赖付费 API，也不要求登录态或 Cookie。
- 影院和影厅数据不预建全国数据库，而是每次从官方影片页、影院公告、公开排片、行业资料和可访问的社区页面重新搜索。
- 小红书等需要登录的平台只作为用户明确同意后的可选增强；遇到验证码或访问限制立即停止。

数据会变化，因此 Skill 把结果分为“当前可确认”“条件式候选”和“理论最佳”，并要求在购票前复核日期、影院、厅号和版本标签。

## 选座依据

选座不是固定套用“黄金排数”。Skill 优先结合：

- 银幕宽度与座位距离形成的水平视场角
- 横向偏移、仰角和字幕阅读负担
- 厅内中轴、坡度、栏杆、过道和特殊座椅
- 影片时长，以及用户对沉浸、舒适、眩晕和动感效果的偏好

数据允许时，可以运行：

```powershell
python -X utf8 scripts/decision_support.py seat --screen-width-m 20 --seat-distance-m 20 --lateral-offset-m 0 --screen-top-delta-m 5
```

## 验证

在 Skill 目录下运行：

```powershell
python -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

当前测试覆盖影片版本与具体场次绑定、格式家族覆盖审计、来源独立性、弱证据降级、座位几何，以及多个公开地理回归案例。公开案例中的出发点均为合成测试输入，不代表维护者或任何真实用户的居住位置。

## 目录说明

```text
pick-movie-theater/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── film-version-card.md
│   ├── source-and-evidence-policy.md
│   ├── search-playbook.md
│   ├── hall-and-screening.md
│   ├── format-taxonomy.md
│   ├── decision-and-output.md
│   ├── seat-selection.md
│   └── requirements-traceability.md
├── scripts/
│   └── decision_support.py
└── tests/
    ├── test_skill_contract.py
    └── cases/
```

## 已知边界

- 免费公开搜索无法保证覆盖所有普通影院，只能对本轮效果优先候选说明覆盖范围。
- 票务平台、影厅设备和排片会变化，历史资料不能静默当成当前事实。
- 社交媒体可以发现候选和近期体验，但单一帖子不能独立证明决定性技术规格。
- 没有座位图、厅内几何或当前余座时，只给区域建议，不伪造具体座号。

## 小红书讲解

《蜘蛛侠》《奥德赛》看什么厅？一个 Skill 帮你选影院和座位

链接：

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
- [scripts/](./scripts/)
- [tests/](./tests/)
