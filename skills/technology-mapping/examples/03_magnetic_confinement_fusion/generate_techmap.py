# -*- coding: utf-8 -*-
"""
磁约束核聚变技术图谱 — Obsidian Canvas 生成脚本 v3
竖轴: 时间 (从上到下 1950s → 2020s+)
横轴: 技术路线 (5列)
"""
import json, uuid, os

def uid():
    return uuid.uuid4().hex[:16]

# ── 布局常量 ──
# 列 X 坐标 (每列 600px 宽, 间距 100px)
# 列:  时间线 | HTS托卡马克 | 球形ST | 仿星器 | FRC | 大科学装置
COL_TL   = -600   # 时间线
COL_HTS  = 0      # HTS 托卡马克
COL_ST   = 700    # 球形 ST
COL_STEL = 1400   # 仿星器
COL_FRC  = 2100   # FRC
COL_BIG  = 2800   # 大科学装置

# 行 Y 坐标 (每层间距 ~350px)
ROW_HEAD = -600   # 标题行
ROW_0    = 0      # 1950s 奠基
ROW_1    = 400    # 1960s T-3
ROW_2    = 800    # 1980-90s JET/TFTR
ROW_3    = 1200   # 2000s TAE/ITER/EAST
ROW_4    = 1600   # 2010s W7-X/Whyte
ROW_5    = 2000   # 2018-21 CFS/Helion
ROW_6    = 2400   # 2023-26 中国创业潮
ROW_TECH = 2900   # 技术概念层

# 节点尺寸
W = 300; H = 120   # 标准节点
WL = 350; HL = 160  # 大节点
WS = 250; HS = 80   # 小节点
WT = 200; HT = 50   # 时间线节点
WG = 580; HG = 200  # group 内部间距

nodes = []
edges = []

def text_node(x, y, text, color=None, w=W, h=H):
    n = {"id": uid(), "type": "text", "x": x, "y": y, "width": w, "height": h, "text": text}
    if color: n["color"] = color
    nodes.append(n)
    return n["id"]

def group_node(x, y, w, h, label, color=None):
    n = {"id": uid(), "type": "group", "x": x, "y": y, "width": w, "height": h, "label": label}
    if color: n["color"] = color
    nodes.insert(0, n)  # groups at bottom z-index
    return n["id"]

def edge(from_id, to_id, label=None, color=None, from_side="bottom", to_side="top"):
    e = {"id": uid(), "fromNode": from_id, "toNode": to_id,
         "fromSide": from_side, "toSide": to_side}
    if label: e["label"] = label
    if color: e["color"] = color
    edges.append(e)

# ════════════════════════════════════════════════════════
#  ROW HEAD: 列标题 + 图例
# ════════════════════════════════════════════════════════
text_node(COL_TL, ROW_HEAD, "# 📅 时间轴\n\n⬇️ 从上到下 = 从源头到商业化", w=WS, h=120)

group_node(COL_HTS-20, ROW_HEAD-30, WG, HG+40, "常规托卡马克 + HTS 高温超导", "5")
group_node(COL_ST-20, ROW_HEAD-30, WG, HG+40, "球形托卡马克 ST", "4")
group_node(COL_STEL-20, ROW_HEAD-30, WG, HG+40, "仿星器 Stellarator", "6")
group_node(COL_FRC-20, ROW_HEAD-30, WG, HG+40, "场反位形 FRC", "2")
group_node(COL_BIG-20, ROW_HEAD-30, WG+200, HG+40, "国家大科学装置", "1")

# 列内技术概念说明
text_node(COL_HTS, ROW_HEAD, "🔬 **HTS 紧凑高场**\nREBCO 超导 20T+\n✅ 紧凑 ✅ 成本降低\n❌ 工程热管理", color="6", w=W, h=HL)
text_node(COL_ST, ROW_HEAD, "🔬 **球形托卡马克**\n低纵横比 A~1.5\n✅ 高β ✅ 紧凑\n❌ 中心柱工程", color="6", w=W, h=HL)
text_node(COL_STEL, ROW_HEAD, "🔬 **仿星器**\n外部3D扭转线圈\n✅ 稳态 ✅ 无破裂\n❌ 线圈复杂", color="6", w=W, h=HL)
text_node(COL_FRC, ROW_HEAD, "🔬 **场反位形 FRC**\n自生磁场约束\n✅ 结构简单 ✅ 紧凑\n❌ 稳定性挑战", color="6", w=W, h=HL)
text_node(COL_BIG, ROW_HEAD, "🏛️ **国家大科学装置**\n国际/国家合作\n科学验证 → 工程验证\n为所有商业路线提供基础", color="6", w=WL, h=HL)

# 图例
text_node(COL_BIG+450, ROW_HEAD, "# 📍 图例 Legend\n\n**节点颜色**\n🟡 **Preset 3** = 里程碑装置\n🔵 **Preset 5** = 海外学者\n🟢 **Preset 4** = 海外公司\n🔴 **Preset 1** = 中国实体\n🟣 **Preset 6** = 技术概念\n\n**连线颜色**\n🔵 Cyan = 师承\n🟢 Green = 创办\n🟠 Orange = 技术传承\n⚫ 默认 = 关系", color=None, w=350, h=350)

# ════════════════════════════════════════════════════════
#  ROW 0: 1950s — 奠基人
# ════════════════════════════════════════════════════════
t1950 = text_node(COL_TL, ROW_0+20, "## 1950s\n理论奠基", w=WT, h=HT+30)

tamm = text_node(COL_HTS, ROW_0,
    "**Igor Tamm 塔姆**\n(1895-1971)\n🏆 1958 诺贝尔物理学奖\n托卡马克概念提出者 ⛔", color="5", w=W, h=HL)

sakharov = text_node(COL_ST, ROW_0,
    "**Andrei Sakharov 萨哈罗夫**\n(1921-1989)\n🏆 1975 诺贝尔和平奖\n托卡马克概念共同提出者 ⛔", color="5", w=W, h=HL)

spitzer = text_node(COL_STEL, ROW_0,
    "**Lyman Spitzer 斯皮策**\n(1914-1997)\n仿星器发明者 (1951)\nPrinceton PPPL 创始人\n导师: H.N. Russell ⛔", color="5", w=W, h=HL)

alfven = text_node(COL_FRC, ROW_0,
    "**Hannes Alfvén 阿尔文**\n(1908-1995)\n🏆 1970 诺贝尔物理学奖\n磁流体力学(MHD)奠基人 ⛔", color="5", w=W, h=HL)

# ════════════════════════════════════════════════════════
#  ROW 1: 1960s — T-3 突破
# ════════════════════════════════════════════════════════
t1960 = text_node(COL_TL, ROW_1+20, "## 1960s\nT-3突破", w=WT, h=HT+30)

artsimovich = text_node(COL_HTS, ROW_1,
    "**Lev Artsimovich 阿齐莫维奇**\n(1909-1973)\nT-3 托卡马克实验验证\n⛔ 托卡马克实验奠基人", color="5", w=W, h=HL)

t3 = text_node(COL_BIG, ROW_1,
    "🏗️ **T-3 托卡马克 (1968)**\n新西伯利亚会议\nTe=1keV, nτ=10¹⁸ m⁻³·s\n**确立托卡马克优势地位**", color="3", w=WL, h=HL)

edge(tamm, artsimovich, "师承", "5")
edge(sakharov, t3, "概念→实验", None, "bottom", "top")
edge(artsimovich, t3, "领导实验", "4", "right", "left")

# ════════════════════════════════════════════════════════
#  ROW 2: 1980-90s
# ════════════════════════════════════════════════════════
t1980 = text_node(COL_TL, ROW_2+20, "## 1980-90s\n实验验证", w=WT, h=HT+30)

pppl = text_node(COL_STEL, ROW_2,
    "**Princeton PPPL**\n(1951- ) Spitzer 创立\nTFTR 运行 | 仿星器复兴", color="4", w=W, h=H)

sykes = text_node(COL_ST, ROW_2,
    "**Alan Sykes**\nUKAEA Culham\n球形托卡马克预言者\n⛔ 球形 ST 奠基人", color="5", w=W, h=HL)

start_mast = text_node(COL_ST+330, ROW_2,
    "🏗️ **START/MAST**\nUKAEA (1991)\n首个大型球形 ST", color="3", w=WS, h=H)

rostoker = text_node(COL_FRC, ROW_2,
    "**Norman Rostoker**\n(1925-2014)\nUC Irvine 教授\nFRC聚变方案 | ⛔ 奠基人", color="5", w=W, h=HL)

jet = text_node(COL_BIG, ROW_2,
    "🏗️ **JET** (1983-2023)\n欧洲 Culham\n69 MJ 聚变能 (2023)\nQ=0.67 | 唯一 D-T 实验", color="3", w=WL, h=HL)

tftr = text_node(COL_BIG+400, ROW_2,
    "🏗️ **TFTR** (1982-97)\nPrinceton PPPL\n10.7 MW 聚变功率\n5.1亿°C 温度纪录", color="3", w=WL, h=HL)

edge(spitzer, pppl, "创立(1951)", "4")
edge(sykes, start_mast, "预言/研发", "4", "right", "left")
edge(t3, jet, "发展", "2", "bottom", "top")
edge(t3, tftr, "发展", "2", "bottom", "top")
edge(alfven, rostoker, "等离子体理论", None, "bottom", "top")

# ════════════════════════════════════════════════════════
#  ROW 3: 2000s — TAE / ITER / EAST / SUNIST
# ════════════════════════════════════════════════════════
t2000 = text_node(COL_TL, ROW_3+20, "## 2000s\n国际合作", w=WT, h=HT+30)

binderbauer = text_node(COL_FRC, ROW_3,
    "**Michl Binderbauer**\nTAE CEO\nUCI PhD (导师: Rostoker)", color="5", w=W, h=H)

tae = text_node(COL_FRC+330, ROW_3,
    "**TAE Technologies** (1998)\n🏷️继承 Rostoker/UCI\n💰 $1.79B | FRC\np-B11 无中子 | Google投资", color="4", w=WL, h=HL)

wanyuanxi = text_node(COL_BIG, ROW_3,
    "🇨🇳 **万元熙 院士**\nASIPP 等离子体物理所\nEAST 项目总负责人\n40年+磁约束聚变研究", color="1", w=WL, h=HL)

east = text_node(COL_BIG+400, ROW_3,
    "🏗️ 🇨🇳 **EAST** (2006-)\n合肥 ASIPP\n世界首个全超导托卡马克\n1亿°C × 1000秒 (2025.1)", color="3", w=WL, h=HL)

iter_node = text_node(COL_BIG+200, ROW_3+200,
    "🏗️ **ITER** (2007-)\n法国 Cadarache | 7国合作\n目标 Q≥10 | 500MW 聚变功率\nD-T运行 ~2039", color="3", w=WL, h=HL)

sunist = text_node(COL_ST, ROW_3,
    "🏗️ 🇨🇳 **SUNIST**\n清华大学\n中国首个球形托卡马克\n20年+运行经验", color="3", w=W, h=H)

edge(rostoker, binderbauer, "PhD advisor", "5")
edge(rostoker, tae, "联合创办", "4", "bottom", "top")
edge(binderbauer, tae, "CEO", "4", "right", "left")
edge(wanyuanxi, east, "总负责", "4", "right", "left")
edge(jet, iter_node, "验证→放大", "2")
edge(tftr, iter_node, "验证→放大", "2")
edge(start_mast, sunist, "路线影响", "2", "bottom", "top")

# ════════════════════════════════════════════════════════
#  ROW 4: 2010s — W7-X / Whyte / 李建刚
# ════════════════════════════════════════════════════════
t2010 = text_node(COL_TL, ROW_4+20, "## 2010s\nHTS突破", w=WT, h=HT+30)

whyte = text_node(COL_HTS, ROW_4,
    "**Dennis Whyte**\nMIT PSFC 前主任 (2015-23)\nHitachi America 教授\nCFS 联合创始人\n高场紧凑路线推动者", color="5", w=W, h=HL+20)

greenwald = text_node(COL_HTS+330, ROW_4,
    "**Martin Greenwald**\nMIT PSFC 高级科学家\nGreenwald 密度极限", color="5", w=WS, h=H)

klinger = text_node(COL_STEL, ROW_4,
    "**Thomas Klinger**\nMax Planck IPP 所长\nW7-X 项目负责人 (2005-)", color="5", w=W, h=H)

w7x = text_node(COL_STEL+330, ROW_4,
    "🏗️ **Wendelstein 7-X** (2015-)\nMPG IPP Greifswald\n超导磁体 | 优化位形\n世界最先进仿星器", color="3", w=WL, h=HL)

slough = text_node(COL_FRC, ROW_4,
    "**John Slough**\nU. Washington PhD\nFRC 推进器研究\nHelion 联合创始人", color="5", w=W, h=HL)

lijiangang = text_node(COL_BIG, ROW_4,
    "🇨🇳 **李建刚 院士**\nASIPP 等离子体物理所\n师从万元熙\nEAST 核心科学家", color="1", w=WL, h=H)

edge(spitzer, w7x, "仿星器传承", "2", "bottom", "top")
edge(klinger, w7x, "领导", "4", "right", "left")
edge(wanyuanxi, lijiangang, "师承", "5")
edge(lijiangang, east, "核心科学家", "4", "right", "left")

# ════════════════════════════════════════════════════════
#  ROW 5: 2018-21 — CFS / Helion / Tokamak Energy
# ════════════════════════════════════════════════════════
t2018 = text_node(COL_TL, ROW_5+20, "## 2018-21\n创业爆发", w=WT, h=HT+30)

mumgaard = text_node(COL_HTS, ROW_5,
    "**Bob Mumgaard**\nCFS CEO & 联合创始人\nMIT PhD (导师: Whyte)", color="5", w=W, h=H)

sorbom = text_node(COL_HTS, ROW_5+140,
    "**Brandon Sorbom**\nCFS CSO & 联合创始人\nMIT PhD | ARC设计", color="5", w=W, h=H)

cfs = text_node(COL_HTS+330, ROW_5,
    "**CFS** (2018)\n🏷️继承 MIT PSFC\n💰 ~$3B+ | HTS 紧凑托卡马克\nSPARC→ARC | 20T HTS磁体\nGoogle 签约购电", color="4", w=WL, h=HL+20)

sparc = text_node(COL_HTS+330, ROW_5+200,
    "🏗️ **SPARC**\nMIT+CFS 联合项目\nHTS 20T (2021突破)\n目标 Q>1", color="3", w=WS, h=H)

gryaznevich = text_node(COL_ST, ROW_5,
    "**M. Gryaznevich**\nTokamak Energy 首席科学家\nCulham (1990-)", color="5", w=W, h=H)

tokamak_energy = text_node(COL_ST+330, ROW_5,
    "**Tokamak Energy** (2009)\n🏷️继承 UKAEA Culham\n💰 $336M | 球形 ST+HTS\nST80-HTS (2026)", color="4", w=WL, h=HL)

tanyi = text_node(COL_ST, ROW_5+200,
    "🇨🇳 **谭熠**\n清华工物系副教授\nSUNIST 运行 | 博导\n星环聚能创始人 & 首席科学家", color="1", w=W, h=HL)

kirtley = text_node(COL_FRC, ROW_5,
    "**David Kirtley**\nHelion CEO & 创始人\nU.Michigan → U.Texas PhD\nMSNW 等离子体推进", color="5", w=W, h=HL)

helion = text_node(COL_FRC+330, ROW_5,
    "**Helion Energy** (2013)\n🏷️独立 MSNW spin-off\n💰 估值 $5.4B | FRC\nD-He3 | Microsoft 购电 (2028)", color="4", w=WL, h=HL)

yangzhao = text_node(COL_HTS, ROW_5+280,
    "🇨🇳 **杨钊**\n北大物理 → Stanford PhD\n理论物理\n能量奇点 CEO & 创始人", color="1", w=W, h=H)

edge(whyte, mumgaard, "PhD advisor", "5")
edge(whyte, sorbom, "PhD advisor", "5")
edge(whyte, cfs, "联合创办", "4", "bottom", "top")
edge(mumgaard, cfs, "CEO", "4", "right", "left")
edge(sorbom, cfs, "CSO", "4", "right", "left")
edge(cfs, sparc, "研发", "2")
edge(sykes, tokamak_energy, "联合创办", "4", "bottom", "top")
edge(gryaznevich, tokamak_energy, "首席科学家", "4", "right", "left")
edge(sunist, tanyi, "运行", "2", "bottom", "top")
edge(slough, helion, "联合创办", "4", "bottom", "top")
edge(slough, kirtley, "MSNW 同事", "5", "bottom", "top")
edge(kirtley, helion, "CEO", "4", "right", "left")
edge(whyte, "placeholder_sciortino", None, None)  # placeholder, remove later

# ════════════════════════════════════════════════════════
#  ROW 6: 2023-26 — 中国创业潮 / Proxima
# ════════════════════════════════════════════════════════
t2023 = text_node(COL_TL, ROW_6+20, "## 2023-26\n商业化", w=WT, h=HT+30)

energy_singularity = text_node(COL_HTS, ROW_6,
    "🇨🇳 **能量奇点** (2021)\n🏷️独立 | 💰 ~4亿+\n\"洪荒70\" 全HTS托卡马克\n120秒稳态运行 (2026.1)", color="1", w=WL, h=HL)

startorus = text_node(COL_ST, ROW_6,
    "🇨🇳 **星环聚能** (2021)\n🏷️继承 清华工物系\n💰 10亿 A轮 (2026.1)\n球形 ST + HTS 重复重联", color="1", w=WL, h=HL)

sciortino = text_node(COL_STEL, ROW_6,
    "**Francesco Sciortino**\nProxima CEO & 创始人\nMIT PhD (等离子体) → MPG IPP\n从托卡马克转向仿星器", color="5", w=W, h=HL)

proxima = text_node(COL_STEL+330, ROW_6,
    "**Proxima Fusion** (2023)\n🏷️继承 MPG IPP\n💰 €185M+ | 仿星器\nAI 优化设计 | 首个IPP spin-off", color="4", w=WL, h=HL)

swjtu = text_node(COL_STEL, ROW_6+200,
    "🇨🇳 **西南交通大学**\n准环对称仿星器测试平台\n🏷️自主研发", color="1", w=W, h=H)

nova_fusion = text_node(COL_FRC, ROW_6,
    "🇨🇳 **诺瓦聚变** (上海)\n🏷️独立 | 💰 5亿天使轮\nFRC + 磁压缩\n小型化/模块化/分布式", color="1", w=WL, h=HL)

hanhai = text_node(COL_FRC, ROW_6+200,
    "🇨🇳 **瀚海聚能** (2022)\n🏷️独立 | 💰 5000万+\nFRC 直线型装置", color="1", w=W, h=H)

xingneng = text_node(COL_FRC+330, ROW_6+200,
    "🇨🇳 **星能玄光** (2024)\n🏷️继承 中科大\n💰 亿元天使轮\n直线型场反磁镜", color="1", w=W, h=HL)

xumin = text_node(COL_BIG, ROW_6,
    "🇨🇳 **许敏 教授**\n复旦大学现代物理研究所\n高温强磁场聚变 + AI", color="1", w=WL, h=H)

dongsheng = text_node(COL_BIG, ROW_6+140,
    "🇨🇳 **东昇聚变** (2025)\n🏷️继承 复旦大学\n💰 数亿天使轮\n红杉/IDG/高瓴 | D-He3", color="1", w=WL, h=HL)

best = text_node(COL_BIG+400, ROW_6,
    "🏗️ 🇨🇳 **BEST 夸父启明**\n合肥 ASIPP | 💰 85亿\n2027 聚变燃烧实验\n2035 工程堆 | 2045 商用", color="3", w=WL, h=HL)

duanxuru = text_node(COL_BIG+400, ROW_6+200,
    "🇨🇳 **段旭如**\n中核集团聚变首席科学家\n西物院前院长 | 德国PhD\nCFETR 推动者", color="1", w=WL, h=HL)

cfei = text_node(COL_BIG+200, ROW_6+400,
    "🇨🇳 **中国聚变能源** (2023.12)\n🏷️国家队 | 中核+各方共建\n国家聚变商业化平台", color="1", w=WL, h=H)

# Remove placeholder edge and add real ones
edges.pop()  # remove placeholder
edge(yangzhao, energy_singularity, "创办/CEO", "4")
edge(tanyi, startorus, "创办/首席科学家", "4")
edge(w7x, proxima, "技术传承", "2")
edge(sciortino, proxima, "创办/CEO", "4", "right", "left")
edge(xumin, dongsheng, "孵化", "4")
edge(duanxuru, cfei, "推动建立", "4")
edge(east, best, "后续项目", "2")
edge(whyte, sciortino, "MIT研究背景", None, "bottom", "top")

# 时间线连接
for pair in [(t1950, t1960), (t1960, t1980), (t1980, t2000), (t2000, t2010), (t2010, t2018), (t2018, t2023)]:
    edge(pair[0], pair[1], None, None)

# ════════════════════════════════════════════════════════
#  写入 .canvas 文件
# ════════════════════════════════════════════════════════
canvas_data = {"nodes": nodes, "edges": edges}
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "MCF_TechMap.canvas")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(canvas_data, f, ensure_ascii=False, indent=2)

print(f"✅ Canvas 图谱已生成: {out_path}")
print(f"   节点数: {len(nodes)}")
print(f"   连线数: {len(edges)}")
print(f"   请在 Obsidian 中打开此文件查看")
