"""
类脑智能 技术全景图谱 v4 — VC 技术尽调视角
改进: 全面创始人溯源 + 技术概念/架构节点 + 时间轴锚定 + VC 分析标注
"""
import graphviz, os

g = graphviz.Digraph(
    'NeuromorphicComputing_v4', format='svg', engine='dot',
    graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white',
        'fontname': 'Microsoft YaHei', 'fontsize': '14',
        'label': '<<B>类脑智能 (Neuromorphic Computing) 技术全景图谱</B><BR/>'
                 '<FONT POINT-SIZE="10" COLOR="#7f8c8d">'
                 'VC 技术尽调视角  |  学术源头→技术分化→商业化  |  1971–2025</FONT>>',
        'labelloc': 't', 'fontcolor': '#2c3e50',
        'pad': '0.5', 'nodesep': '0.30', 'ranksep': '0.55',
        'splines': 'true', 'dpi': '150', 'size': '34,26', 'compound': 'true',
    },
    node_attr={'fontname': 'Microsoft YaHei', 'fontsize': '7.5', 'style': 'filled', 'penwidth': '0.8'},
    edge_attr={'fontname': 'Microsoft YaHei', 'fontsize': '6.5', 'fontcolor': '#7f8c8d', 'penwidth': '0.7'},
)

# ═══ 配色 ═══
P    = '#dae8fc'; P_CN = '#fce5cd'; CO = '#d5e8d4'; CO_CN = '#f8cecc'
ML   = '#fff2cc'; TECH = '#e1d5e7'; BDR = '#5d6d7e'
B_CAL= '#3d85c6'; B_ZUR= '#6aa84f'; B_MAN= '#8e7cc3'
B_TSI= '#cc4125'; B_ZJU= '#e69138'; B_IND= '#999999'; B_TH= '#a64d79'
B_BCI= '#0b5394'  # BCI 分支

# ═══ 辅助 ═══
def pn(nid, lbl, cn=False, b=BDR, bold=False):
    g.node(nid, lbl, shape='box', fillcolor=P_CN if cn else P,
           color=b, penwidth='2.2' if bold else '0.8')
def co(nid, lbl, cn=False, b=BDR):
    g.node(nid, lbl, shape='box', fillcolor=CO_CN if cn else CO,
           color=b, style='filled,rounded')
def ml(nid, lbl, b=BDR):
    g.node(nid, lbl, shape='diamond', fillcolor=ML, color=b, width='1.8', height='0.7')
def tc(nid, lbl, b=B_TH):
    g.node(nid, lbl, shape='note', fillcolor=TECH, color=b, fontsize='7', style='filled')
def era(nid, lbl):
    g.node(nid, lbl, shape='plaintext', fillcolor='white', fontsize='8', fontcolor='#95a5a6')

# ═══ 时间轴 ═══
eras = [('E71','1971'),('E80','1980s'),('E99','~2000'),('E05','~2005'),
        ('E14','2014'),('E17','2017'),('E19','2019'),('E23','2023'),('E25','2025')]
for eid,el in eras: era(eid,el)
for i in range(len(eras)-1):
    g.edge(eras[i][0], eras[i+1][0], style='dotted', color='#dcdcdc', arrowhead='none')

# ════════════════════ 理论层 (1971-1980s) ════════════════════
tc('T_mem', 'Memristor 忆阻器\nLeon Chua 1971 | 第四基本元件\n→ 人工突触的物理基础', B_TH)
tc('T_hebb', 'Hebb 学习规则 (1949)\n突触可塑性 | 学习理论基础', B_TH)
pn('Hopfield', 'John Hopfield\nPrinceton\n🏆 2024 诺贝尔物理学奖', bold=True, b='#f39c12')

with g.subgraph() as s:
    s.attr(rank='same'); s.node('E71'); s.node('T_mem'); s.node('T_hebb'); s.node('Hopfield')

# ════════════════════ 奠基层 (1980s) ════════════════════
pn('Middlebrook', 'R.D. Middlebrook\nCaltech 教授\n⛔ 电力电子 (跨领域终止)', b=B_CAL)
pn('Mead', 'Carver Mead\nCaltech 教授 (1989)\n⬛ 「类脑工程」奠基人\n🔬 模拟VLSI仿神经电路', bold=True, b=B_CAL)
tc('T_aVLSI', '模拟VLSI类脑电路\nMead 提出 | 用模拟电路的\n物理特性直接模拟神经元', B_CAL)
pn('Williams', 'Bowcs Williams\n曼大 教授\n⛔ 跨领域终止', b=B_MAN)
pn('JiangMH', '🇨🇳 蒋民华 院士\n山东大学 晶体学\n⛔ 跨领域终止', cn=True, b=B_TSI)

with g.subgraph() as s:
    s.attr(rank='same'); s.node('E80'); s.node('Mead'); s.node('T_aVLSI'); s.node('Williams')

# 师承
g.edge('Middlebrook', 'Mead', label='PhD advisor', color=B_CAL, penwidth='1.5')
g.edge('Williams', 'Furber', label='PhD advisor', color=B_MAN, penwidth='1.5')
g.edge('Mead', 'Hopfield', label='合作→神经网络', style='dashed', color='#f39c12')
g.edge('T_hebb', 'T_aVLSI', label='理论基础', style='dashed', color=B_TH)
g.edge('T_mem', 'T_aVLSI', label='器件启发', style='dashed', color=B_TH)

# ════════════════════ 核心学者层 (~2000) ════════════════════
pn('Mahowald', 'Misha Mahowald\nCaltech PhD → 硅视网膜 (1988)', b=B_CAL)
pn('Delbruck', 'Tobi Delbruck\n苏黎世 INI 教授\n🔬 DVS 事件相机发明人', bold=True, b=B_ZUR)
pn('Furber', 'Steve Furber\n曼大 教授 | ARM联合创始人\n🔬 SpiNNaker 主导者', bold=True, b=B_MAN)
pn('Indiveri', 'Giacomo Indiveri\nETH/UZH 教授 | 热那亚PhD\n🔬 混合信号DYNAP处理器\nCaltech 博后(Mead影响)', bold=True, b=B_ZUR)
pn('Donoghue', 'John Donoghue\nBrown 教授\n🔬 BrainGate BCI 先驱\n🏆 2026 QE Prize', bold=True, b=B_BCI)

with g.subgraph() as s:
    s.attr(rank='same'); s.node('E99'); s.node('Delbruck'); s.node('Furber'); s.node('Donoghue')

g.edge('Mead', 'Mahowald', label='PhD advisor', color=B_CAL, penwidth='1.5')
g.edge('Mead', 'Delbruck', label='类脑工程\n传承(INI)', style='dashed', color=B_CAL)
g.edge('Mead', 'Indiveri', label='Caltech博后\n类脑传承', color=B_CAL, penwidth='1.2')

# ════════════════════ 技术分化层 (~2005) ════════════════════
tc('T_snn', 'SNN 脉冲神经网络\n第3代神经网络 | 事件驱动\n稀疏通信 | 超低功耗', B_TH)
tc('T_dvs', '事件驱动视觉 (DVS)\n异步像素 | μs时间分辨率\nDelbruck→iniVation', B_ZUR)
tc('T_dig', '全数字架构\nCMOS工艺 | 精度高 | 可编程\n功耗较高 | 易量产\n▸ TrueNorth, Loihi', B_CAL)
tc('T_mix', '混合信号架构\n模拟计算+数字控制\n超低功耗 | 加速1万倍\n▸ BrainScaleS, DYNAP, Innatera', B_ZUR)
tc('T_fus', 'ANN+SNN 异构融合\n同时运行ANN和脉冲SNN\n两种范式优势互补\n▸ 天机芯 (🇨🇳 自主创新)', B_TSI)
tc('T_scl', '大规模脉冲阵列\n堆芯片→逼近大脑规模\n▸ SpiNNaker, 达尔文', B_MAN)
tc('T_memr', '忆阻器计算\n存算一体 | MN3纳米线网络\n▸ Rain Neuromorphics', B_TH)

# 人物 → 技术
pn('Davies', 'Mike Davies\nCaltech 校友 → Fulcrum\n→ Intel Loihi 架构师', b=B_CAL)
pn('Nino', 'Juan Nino 教授\nU. Florida 材料科学\n🔬 MN3忆阻器共同发明人', b=B_IND)

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('E05'); s.node('T_snn'); s.node('T_dvs'); s.node('T_dig'); s.node('T_mix')

g.edge('Mead', 'Davies', label='Caltech 师生', color=B_CAL, penwidth='1.2')
g.edge('Mahowald', 'T_dvs', label='硅视网膜\n→事件视觉', color=B_CAL)
g.edge('Delbruck', 'T_dvs', label='发明DVS', color=B_ZUR, penwidth='1.5')
g.edge('Indiveri', 'T_mix', label='DYNAP系列\n核心设计', color=B_ZUR, penwidth='1.2')
g.edge('T_aVLSI', 'T_snn', label='bottom-up', style='dashed', color=B_TH)
g.edge('T_snn', 'T_dig', color=B_TH, style='dashed')
g.edge('T_snn', 'T_mix', color=B_TH, style='dashed')
g.edge('T_snn', 'T_fus', color=B_TH, style='dashed')
g.edge('T_snn', 'T_scl', color=B_TH, style='dashed')
g.edge('T_mem', 'T_memr', label='物理实现\n(2008 HP验证)', color=B_TH, style='dashed')

# ════ 中国学者(深度追溯) ════
pn('ShiLP', '🇨🇳 施路平\n清华 教授 | 科隆大学 PhD (1992)\n硕导: 蒋民华院士(山东大学)\n🔬 ANN+SNN融合 独创', cn=True, bold=True, b=B_TSI)
pn('PanG', '🇨🇳 潘纲\n浙大 教授 | 浙大本硕博(2004)\n🔬 大规模脉冲芯片 国内自主', cn=True, bold=True, b=B_ZJU)
pn('HuangTJ', '🇨🇳 黄铁军\n北大 教授 | 华中理工 PhD(1998)\n中科院博后 → Stanford访问\n🔬 仿真主义/脉冲视觉', cn=True, bold=True, b=B_TSI)
pn('QiaoN', '🇨🇳 乔宁 (Ning Qiao)\n中科院半导体所 PhD\nETH博后(Indiveri实验室)\n→ SynSense CEO', cn=True, b=B_ZUR)
pn('Rao', 'Naveen Rao\nBrown PhD (Donoghue 实验室)\n计算神经科学 → Qualcomm\n→ 连续创业 (非独立发明)', b=B_BCI)
pn('vanderMade', 'Peter van der Made\n🔬 45年行业经验 无PhD\n独立发明数字类脑架构\n著《Higher Intelligence》', b=B_IND)
pn('Kendall', 'Jack Kendall\nU.Florida BSc 物理+化工\n🔬 MN3忆阻器共同发明人\n与Nino教授合作', b=B_IND)
pn('Posch', 'Christoph Posch\n维也纳理工 PhD (CERN)\n🔬 事件视觉传感器专家\nInstitut de la Vision (巴黎)', b=B_ZUR)
pn('ZhuYL', '🇨🇳 祝夭龙\n灵汐科技 CEO\n天机芯Nature共同一作\n清华类脑中心孵化', cn=True, b=B_TSI)

g.edge('JiangMH', 'ShiLP', label='硕士导师', color=B_TSI, penwidth='1.2')
g.edge('Donoghue', 'Rao', label='PhD advisor\n(BCI/计算神经)', color=B_BCI, penwidth='1.5')
g.edge('Indiveri', 'QiaoN', label='ETH博后导师\n(DYNAP项目)', color=B_ZUR, penwidth='1.5')
g.edge('Nino', 'Kendall', label='MN3 共同\n发明人', color=B_IND, penwidth='1.2')
g.edge('HuangTJ', 'T_dvs', label='仿真主义\n脉冲视觉', style='dashed', color=B_TSI)

# ════════════════════ 芯片平台层 (2014-2019) ════════════════════
ml('TrueNorth', 'IBM TrueNorth (2014)\n100万神经元 | 全数字 | 70mW', B_IND)
ml('Loihi', 'Intel Loihi (2017→2026)\n13万神经元 | 全数字 | 在线学习', B_CAL)
ml('SpiNNaker', 'SpiNNaker (2005→2018)\nARM阵列 | 10亿神经元仿真', B_MAN)
ml('BrainScaleS', 'BrainScaleS (海德堡)\n混合信号 | 1万倍加速', B_ZUR)
ml('Tianjic', '🇨🇳 天机芯 (2019)\nNature封面 | ANN+SNN融合', B_TSI)
ml('Darwin3', '🇨🇳 达尔文3代 (2023)\n235万脉冲神经元/芯片', B_ZJU)

with g.subgraph() as s:
    s.attr(rank='same'); s.node('E14'); s.node('TrueNorth'); s.node('BrainScaleS')
with g.subgraph() as s:
    s.attr(rank='same'); s.node('E17'); s.node('Loihi'); s.node('SpiNNaker')
with g.subgraph() as s:
    s.attr(rank='same'); s.node('E19'); s.node('Tianjic')
with g.subgraph() as s:
    s.attr(rank='same'); s.node('E23'); s.node('Darwin3')

g.edge('Davies', 'Loihi', label='主导设计', color=B_CAL, penwidth='1.5')
g.edge('Furber', 'SpiNNaker', label='主导设计', color=B_MAN, penwidth='1.5')
g.edge('ShiLP', 'Tianjic', label='主导设计', color=B_TSI, penwidth='1.5')
g.edge('PanG', 'Darwin3', label='主导设计', color=B_ZJU, penwidth='1.5')
g.edge('T_dig', 'TrueNorth', style='dashed', color=B_TH)
g.edge('T_dig', 'Loihi', style='dashed', color=B_TH)
g.edge('T_scl', 'SpiNNaker', style='dashed', color=B_TH)
g.edge('T_mix', 'BrainScaleS', style='dashed', color=B_TH)
g.edge('T_fus', 'Tianjic', style='dashed', color=B_TH)
g.edge('T_scl', 'Darwin3', style='dashed', color=B_TH)

# ════════════════════ 商业化层 (2023-2025) ════════════════════
co('SynSense', '🇨🇳 SynSense 时识科技\n苏黎世→上海 | 8轮>8亿元\nSpeck™ | 三星入股\n🏷️ 继承: Indiveri实验室', cn=True, b=B_ZUR)
co('Prophesee', 'Prophesee\n法国 | €127M | 事件相机\n🏷️ 继承: Delbruck DVS技术', b=B_ZUR)
co('SpiNNCloud', 'SpiNNCloud\n德国 | EIC €10M\n🏷️ 继承: Furber SpiNNaker', b=B_MAN)
co('Lingxi', '🇨🇳 灵汐科技\nB+轮 | 北京\n🏷️ 继承: 施路平/清华 天机芯', cn=True, b=B_TSI)
co('DarwinM', '🇨🇳 Darwin Monkey\n之江实验室 2025\n960芯片 20亿神经元\n🏷️ 自主: 浙大国内培养', cn=True, b=B_ZJU)
co('BrainChip', 'BrainChip\nASX上市 | Akida芯片\n🏷️ 独立: 创始人独立发明', b=B_IND)
co('Innatera', 'Innatera\n荷兰 | $21M Series A\n🏷️ 继承: TU Delft spin-off', b=B_IND)
co('Rain', 'Rain Neuromorphics\nSam Altman投资\n🏷️ 继承: Nino MN3忆阻器', b=B_IND)
co('Nervana', 'Nervana Systems\nIntel收购 $408M (2016)\n⚠️ DL加速ASIC 非类脑', b=B_IND)
co('MosaicML', 'MosaicML\nDatabricks收购 $1.3B\n⚠️ 非类脑 (ML infra)', b=B_IND)
co('Unconventional', 'Unconventional AI 🦄\n$475M seed | $4.5B估值\n🏷️ 回归: 生物启发类脑 (2025)', b='#e74c3c')

with g.subgraph() as s:
    s.attr(rank='same'); s.node('E25'); s.node('Unconventional'); s.node('DarwinM')

# 创始人 → 公司
g.edge('QiaoN', 'SynSense', label='CEO co-founded', color='#27ae60', penwidth='1.2')
g.edge('Indiveri', 'SynSense', label='co-founded\n学术源头', color='#27ae60', penwidth='1.2')
g.edge('Posch', 'Prophesee', label='CTO co-founded', color='#27ae60', penwidth='1.2')
g.edge('T_dvs', 'Prophesee', label='核心技术', style='dashed', color=B_ZUR)
g.edge('T_dvs', 'SynSense', label='事件视觉', style='dashed', color=B_ZUR)
g.edge('SpiNNaker', 'SpiNNCloud', label='spin-off', color='#27ae60', penwidth='1.2')
g.edge('ZhuYL', 'Lingxi', label='CEO', color='#27ae60', penwidth='1.2')
g.edge('ShiLP', 'Lingxi', label='联合创始人\n/董事', color='#27ae60')
g.edge('Tianjic', 'Lingxi', label='技术商业化', color='#27ae60')
g.edge('Darwin3', 'DarwinM', label='升级→20亿', color=B_ZJU)
g.edge('vanderMade', 'BrainChip', label='founder/CTO\n独立发明专利', color='#27ae60', penwidth='1.2')
g.edge('Kendall', 'Rain', label='CTO→CEO\nMN3忆阻器', color='#27ae60', penwidth='1.2')
g.edge('T_memr', 'Rain', label='核心技术', style='dashed', color=B_TH)
g.edge('Rao', 'Nervana', label='co-founded (2014)', color='#27ae60')
g.edge('Rao', 'MosaicML', label='founded', color='#27ae60')
g.edge('Rao', 'Unconventional', label='founded (2025)', color='#e74c3c', penwidth='1.8')
g.edge('Nervana', 'Unconventional', label='Intel经历→\n回归类脑', style='dashed', color=B_IND)

# ════ Legend ════
with g.subgraph(name='cluster_legend') as lg:
    lg.attr(label='图例 Legend', style='rounded', color='#bdc3c7',
            fontcolor='#7f8c8d', fontsize='8', bgcolor='#fafafa')
    lg.node('L1', '海外学者\n(🔬=核心贡献)', shape='box', fillcolor=P, color=BDR, fontsize='6.5')
    lg.node('L2', '🇨🇳 中国学者', shape='box', fillcolor=P_CN, color=BDR, fontsize='6.5')
    lg.node('L3', '海外公司\n(🏷️=技术来源)', shape='box', fillcolor=CO, color=BDR, fontsize='6.5', style='filled,rounded')
    lg.node('L4', '🇨🇳 中国公司', shape='box', fillcolor=CO_CN, color=BDR, fontsize='6.5', style='filled,rounded')
    lg.node('L5', '芯片/里程碑', shape='diamond', fillcolor=ML, color=BDR, fontsize='6.5')
    lg.node('L6', '技术概念', shape='note', fillcolor=TECH, color=BDR, fontsize='6.5')
    lg.node('L7', '⛔ 溯源终止点', shape='box', fillcolor='#f5f5f5', color=BDR, fontsize='6.5')
    for a,b in [('L1','L2'),('L2','L3'),('L3','L4'),('L4','L5'),('L5','L6'),('L6','L7')]:
        lg.edge(a, b, style='invis')

# ════ 输出 ════
out = os.path.join(r"C:\Users\lenovo\.gemini\antigravity\scratch", 'NeuromorphicComputing_TechMap_v4')
for p in [r"C:\Program Files\Graphviz\bin", r"C:\Program Files (x86)\Graphviz\bin"]:
    if os.path.exists(p) and p not in os.environ.get('PATH',''):
        os.environ['PATH'] = p + os.pathsep + os.environ.get('PATH','')
g.render(out, cleanup=True, view=False)
print(f"✅ v4 图谱: {out}.svg")
