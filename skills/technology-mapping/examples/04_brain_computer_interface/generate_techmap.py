"""
Brain-Computer Interface (BCI) Technology Mapping
Generate with: python generate_techmap.py
Output: BCI_TechMap.svg
"""
import graphviz

g = graphviz.Digraph(
    'BCI_TechMap',
    format='svg',
    engine='dot',
)
g.attr(
    rankdir='TB',
    dpi='150',
    fontname='Microsoft YaHei',
    bgcolor='white',
    label='脑机接口 (Brain-Computer Interface) 技术全景图谱',
    labelloc='t',
    fontsize='24',
    pad='0.5',
    nodesep='0.4',
    ranksep='0.6',
)

# === Color Palette ===
# Node fill colors (by type)
FILL_PERSON_OVERSEAS = '#dae8fc'   # soft blue
FILL_PERSON_CHINA    = '#fce5cd'   # soft orange
FILL_COMPANY_OVERSEAS = '#d5e8d4'  # soft green
FILL_COMPANY_CHINA   = '#f8cecc'   # soft pink
FILL_MILESTONE       = '#fff2cc'   # soft yellow
FILL_TECH_CONCEPT    = '#e1d5e7'   # soft purple

# Group border colors (by 流派)
GROUP_RIGID   = '#3d85c6'  # blue  — rigid electrode
GROUP_FLEX    = '#6aa84f'  # green — flexible electrode
GROUP_ENDO    = '#8e7cc3'  # purple — endovascular
GROUP_NONINV  = '#cc4125'  # red   — non-invasive EEG/fNIRS
GROUP_ULTRA   = '#e69138'  # orange — ultrasound

# Edge colors
EDGE_MENTOR   = '#5b9bd5'
EDGE_FOUNDED  = '#27ae60'
EDGE_COAUTHOR = '#cc4125'
EDGE_TECH     = '#e69138'
EDGE_TIMELINE = '#cccccc'

# =====================================================
# TIMELINE (left column)
# =====================================================
timeline = ['1920s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
for yr in timeline:
    g.node(yr, yr, shape='plaintext', fontsize='11', fontcolor='#666666')
for i in range(len(timeline) - 1):
    g.edge(timeline[i], timeline[i+1],
           style='dotted', arrowhead='none', color=EDGE_TIMELINE, weight='1')

# =====================================================
# NODES
# =====================================================

# --- Milestones ---
def milestone(nid, label, group_color):
    g.node(nid, label, shape='diamond', style='filled',
           fillcolor=FILL_MILESTONE, color=group_color, fontsize='9')

milestone('EEG_1924', 'EEG 发明\n(Hans Berger, 1924)', GROUP_NONINV)
milestone('BCI_1973', 'BCI 概念提出\n(Jacques Vidal, 1973)', GROUP_NONINV)
milestone('Utah_1980s', 'Utah Array 发明\n(Richard Normann, 1980s)', GROUP_RIGID)
milestone('First_Implant_1998', '首例侵入式 BCI 植入\n(Philip Kennedy, 1998)', GROUP_RIGID)
milestone('BG_2004', 'BrainGate 首例人体\n(Matt Nagle, 2004)', GROUP_RIGID)
milestone('NL_Human_2024', 'Neuralink 首例人体\n(Noland Arbaugh, 2024)', GROUP_FLEX)

# --- Academic Founders / Pioneers ---
def person_overseas(nid, label, group_color, bold=False):
    pw = '2.2' if bold else '1.0'
    g.node(nid, label, shape='box', style='filled',
           fillcolor=FILL_PERSON_OVERSEAS, color=group_color,
           penwidth=pw, fontsize='10')

def person_china(nid, label, group_color, bold=False):
    pw = '2.2' if bold else '1.0'
    g.node(nid, label, shape='box', style='filled',
           fillcolor=FILL_PERSON_CHINA, color=group_color,
           penwidth=pw, fontsize='10')

def company_overseas(nid, label, group_color):
    g.node(nid, label, shape='box', style='filled,rounded',
           fillcolor=FILL_COMPANY_OVERSEAS, color=group_color, fontsize='10')

def company_china(nid, label, group_color):
    g.node(nid, label, shape='box', style='filled,rounded',
           fillcolor=FILL_COMPANY_CHINA, color=group_color, fontsize='10')

def tech_concept(nid, label):
    g.node(nid, label, shape='note', style='filled',
           fillcolor=FILL_TECH_CONCEPT, color='#a64d79', fontsize='9')

# === UPSTREAM ANCESTORS ===
person_overseas('Berger', 'Hans Berger\n⛔ EEG 奠基人\n(Jena, 1924)', GROUP_NONINV, bold=True)
person_overseas('Vidal', 'Jacques Vidal\n⛔ BCI 概念提出者\n(UCLA, 1973)', GROUP_NONINV, bold=True)
person_overseas('Ebner', 'Ford F. Ebner\n(Vanderbilt)\n⛔ 溯源终止', GROUP_RIGID, bold=False)

# Bert Sakmann — Nobel 1991 — upstream of Paradromics
person_overseas('Sakmann', 'Bert Sakmann\n🏆 诺奖 1991 (膜片钳)\n⛔ 溯源终止', GROUP_FLEX, bold=True)
person_overseas('Schaefer', 'Andreas T. Schaefer\n(MPI / Crick Institute)', GROUP_FLEX)

# === GROUP 1: RIGID ELECTRODE (Utah Array 系) ===
person_overseas('Normann', 'Richard A. Normann\n🔬 Utah Array 发明人\n(UC Berkeley PhD → Utah)', GROUP_RIGID, bold=True)
person_overseas('Donoghue', 'John Donoghue\n🔬 BrainGate 之父\n(Brown PhD 1979)', GROUP_RIGID, bold=True)
person_overseas('Hochberg', 'Leigh Hochberg\n🔬 BrainGate 临床负责人\n(Brown/MGH)', GROUP_RIGID)
person_overseas('Solzbacher', 'Florian Solzbacher\n(Ilmenau PhD → Utah Prof)', GROUP_RIGID)
person_overseas('Kennedy', 'Philip Kennedy\n🔬 首例侵入式 BCI 植入 1998\n(Emory)', GROUP_RIGID)
company_overseas('Blackrock', 'Blackrock Neurotech\n🏷️ 继承 (Utah Array)\n$200M+ 融资', GROUP_RIGID)
company_overseas('BrainGate_Co', 'BrainGate Inc.\n🏷️ 继承 (Donoghue 实验室)\n(捐赠 Tufts 2019)', GROUP_RIGID)

# === GROUP 2: FLEXIBLE ELECTRODE (新一代) ===
person_overseas('Musk', 'Elon Musk\n(Neuralink 创始人)\n🏷️ 独立', GROUP_FLEX)
person_overseas('Rapoport', 'Benjamin Rapoport\n🔬 Neuralink 联合创始人\n(Harvard MD / MIT PhD)\n→ Precision 创始人', GROUP_FLEX)
person_overseas('Hodak', 'Max Hodak\n(Duke BME → Nicolelis Lab)\nNeuralink 联合创始人', GROUP_FLEX)
person_overseas('Nicolelis', 'Miguel Nicolelis\n🔬 灵长类 BCI 先驱\n(Duke)', GROUP_FLEX, bold=True)
person_overseas('Shenoy', 'Krishna Shenoy\n🔬 神经解码算法\n(Stanford, 1968-2023)\n⛔ 已故', GROUP_FLEX, bold=True)
person_overseas('Angle', 'Matt Angle\n(Heidelberg PhD → MPI)', GROUP_FLEX)
company_overseas('Neuralink', 'Neuralink\n🏷️ 独立 (Musk 主导)\n$90B 估值 (2025)', GROUP_FLEX)
company_overseas('Precision', 'Precision Neuroscience\n🏷️ 继承 (Rapoport)\n$102M 融资', GROUP_FLEX)
company_overseas('Paradromics', 'Paradromics\n🏷️ 继承 (Sakmann 系)\n$33M 融资', GROUP_FLEX)

# === GROUP 3: ENDOVASCULAR (血管内介入) ===
person_overseas('Oxley', 'Thomas Oxley\n🔬 血管内 BCI 先驱\n(Melbourne PhD → Mt Sinai)', GROUP_ENDO, bold=True)
person_overseas('Opie', 'Nicholas Opie\n(Melbourne)\n血管仿生学实验室', GROUP_ENDO)
company_overseas('Synchron', 'Synchron\n🏷️ 继承 (Oxley 实验室)\n$345M 累计融资', GROUP_ENDO)

# === GROUP 4: NON-INVASIVE EEG / fNIRS ===
person_china('Gao', '🇨🇳 高小榕\n🔬 中国 BCI 学科创建者\n(清华大学)', GROUP_NONINV, bold=True)
person_china('Han', '🇨🇳 韩璧丞\n(KAIST → 哈佛 PhD 在读创业)', GROUP_NONINV)
company_china('BrainCo', '🇨🇳 强脑科技 (BrainCo)\n🏷️ 继承 (哈佛孵化)\n~20亿元 (中国首个BCI独角兽)', GROUP_NONINV)
company_china('BrainControl', '🇨🇳 博睿康 (BrainControl)\n🏷️ 继承 (清华高小榕团队)\n35-40亿估值，筹备IPO', GROUP_NONINV)

# === GROUP 5: CHINA INVASIVE ===
person_china('TaoHu', '🇨🇳 陶虎\n(中科大→中科院→\n波士顿大学 PhD)\n脑虎科技首席科学家', GROUP_FLEX)
person_china('LiXue', '🇨🇳 李雪\n(华中科大→UT Austin/Rice PhD\n→中科院脑智中心)', GROUP_FLEX)
person_china('ZhaoZT', '🇨🇳 赵郑拓\n(中科院脑智中心研究员)', GROUP_FLEX)
company_china('NeuronTiger', '🇨🇳 脑虎科技\n🏷️ 自主 (中科院体系)\n柔性植入式', GROUP_FLEX)
company_china('StairMed', '🇨🇳 阶梯医疗\n🏷️ 自主 (中科院脑智中心)\n累计11亿元', GROUP_FLEX)

# === GROUP: ULTRASOUND (新兴) ===
company_overseas('MergeLabs', 'Merge Labs\n🏷️ 独立 (Sam Altman)\n$8.5B 估值 (2026)\n非侵入-超声', GROUP_ULTRA)

# === TECH CONCEPT NODES ===
tech_concept('TC_rigid', '刚性微电极阵列\n100通道 Utah Array\n精度高/组织损伤大')
tech_concept('TC_flex', '柔性电极 / 薄膜阵列\n高通道(1024+)\n组织兼容性好')
tech_concept('TC_endo', '血管内支架电极 (Stentrode)\n微创(无需开颅)\n信号分辨率有限')
tech_concept('TC_eeg', '非侵入式 EEG/fNIRS\n零创伤/便携\n信号精度低')
tech_concept('TC_ultra', '聚焦超声神经调控\n非侵入/高空间分辨\n技术极早期')

# =====================================================
# EDGES (source = upstream/上方, target = downstream/下方)
# =====================================================

# Mentor chains (Tier 1 — weight=3)
g.edge('Ebner', 'Donoghue', label='PhD advisor', color=EDGE_MENTOR, penwidth='1.5', weight='3')
g.edge('Sakmann', 'Schaefer', label='PhD advisor', color=EDGE_MENTOR, penwidth='1.5', weight='3')
g.edge('Schaefer', 'Angle', label='PhD advisor', color=EDGE_MENTOR, penwidth='1.5', weight='3')
g.edge('Nicolelis', 'Hodak', label='导师实验室', color=EDGE_MENTOR, penwidth='1.5', weight='3')

# Founded / co-founded (Tier 1 — weight=2)
g.edge('Donoghue', 'BrainGate_Co', label='founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Normann', 'Blackrock', label='技术来源', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Solzbacher', 'Blackrock', label='co-founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Musk', 'Neuralink', label='founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Rapoport', 'Neuralink', label='co-founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2', constraint='false')
g.edge('Hodak', 'Neuralink', label='co-founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2', constraint='false')
g.edge('Rapoport', 'Precision', label='founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Angle', 'Paradromics', label='founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Oxley', 'Synchron', label='co-founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Opie', 'Synchron', label='co-founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Han', 'BrainCo', label='founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('Gao', 'BrainControl', label='技术来源', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('TaoHu', 'NeuronTiger', label='founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('LiXue', 'StairMed', label='co-founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')
g.edge('ZhaoZT', 'StairMed', label='co-founded', color=EDGE_FOUNDED, penwidth='1.2', weight='2')

# Lab colleague (Tier 1 — constraint=false to avoid vertical distortion)
g.edge('Donoghue', 'Hochberg', label='Brown 同事', color=EDGE_MENTOR, penwidth='1.2', constraint='false')
g.edge('Oxley', 'Opie', label='Melbourne 同事', color=EDGE_MENTOR, penwidth='1.2', constraint='false')
g.edge('LiXue', 'ZhaoZT', label='中科院脑智同事', color=EDGE_MENTOR, penwidth='1.2', constraint='false')

# Spun-off / departed
g.edge('Neuralink', 'Precision', label='Rapoport 离开创办', color=EDGE_TECH, penwidth='0.8', style='dashed')

# Nicolelis → BrainCo (顾问)
g.edge('Nicolelis', 'BrainCo', label='首席科学顾问 (2021)', color=EDGE_MENTOR, penwidth='0.8', style='dashed', constraint='false')

# Technology evolution edges (dashed, low weight)
g.edge('TC_rigid', 'TC_flex', label='技术演进', color='#999999', style='dashed', penwidth='0.7', constraint='false')
g.edge('TC_eeg', 'TC_ultra', label='技术演进', color='#999999', style='dashed', penwidth='0.7', constraint='false')

# Tech concept → company links
g.edge('TC_rigid', 'Blackrock', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_rigid', 'BrainGate_Co', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_flex', 'Neuralink', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_flex', 'Precision', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_flex', 'Paradromics', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_endo', 'Synchron', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_eeg', 'BrainCo', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_eeg', 'BrainControl', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('TC_ultra', 'MergeLabs', color='#999999', style='dashed', penwidth='0.5', constraint='false')

# Milestone → person/event links
g.edge('Berger', 'EEG_1924', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('Vidal', 'BCI_1973', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('Normann', 'Utah_1980s', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('Kennedy', 'First_Implant_1998', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('Donoghue', 'BG_2004', color='#999999', style='dashed', penwidth='0.5', constraint='false')
g.edge('Neuralink', 'NL_Human_2024', color='#999999', style='dashed', penwidth='0.5', constraint='false')

# =====================================================
# RANK CONSTRAINTS (timeline alignment)
# =====================================================
with g.subgraph() as s:
    s.attr(rank='min')
    s.node('1920s')
    s.node('Berger')
    s.node('EEG_1924')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('1970s')
    s.node('Vidal')
    s.node('BCI_1973')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('1980s')
    s.node('Normann')
    s.node('Utah_1980s')
    s.node('Ebner')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('1990s')
    s.node('Sakmann')
    s.node('Kennedy')
    s.node('Donoghue')
    s.node('First_Implant_1998')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('2000s')
    s.node('BG_2004')
    s.node('Hochberg')
    s.node('Solzbacher')
    s.node('Schaefer')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('2010s')
    s.node('Nicolelis')
    s.node('Shenoy')
    s.node('Angle')
    s.node('Gao')
    s.node('Oxley')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('2020s')
    s.node('Neuralink')
    s.node('Synchron')
    s.node('BrainCo')
    s.node('StairMed')
    s.node('NL_Human_2024')

# =====================================================
# CLUSTER SUBGRAPHS (流派分组)
# =====================================================
with g.subgraph(name='cluster_rigid') as c:
    c.attr(label='侵入式 — 刚性电极 (Utah Array 系)', style='dashed',
           color=GROUP_RIGID, fontcolor=GROUP_RIGID, fontsize='12')
    c.node('Normann')
    c.node('Donoghue')
    c.node('Hochberg')
    c.node('Solzbacher')
    c.node('Kennedy')
    c.node('Blackrock')
    c.node('BrainGate_Co')
    c.node('TC_rigid')

with g.subgraph(name='cluster_flex') as c:
    c.attr(label='侵入式 — 柔性电极 (新一代)', style='dashed',
           color=GROUP_FLEX, fontcolor=GROUP_FLEX, fontsize='12')
    c.node('Musk')
    c.node('Rapoport')
    c.node('Hodak')
    c.node('Shenoy')
    c.node('Angle')
    c.node('Schaefer')
    c.node('Neuralink')
    c.node('Precision')
    c.node('Paradromics')
    c.node('TC_flex')
    # 中国侵入式
    c.node('TaoHu')
    c.node('LiXue')
    c.node('ZhaoZT')
    c.node('NeuronTiger')
    c.node('StairMed')

with g.subgraph(name='cluster_endo') as c:
    c.attr(label='血管内介入式', style='dashed',
           color=GROUP_ENDO, fontcolor=GROUP_ENDO, fontsize='12')
    c.node('Oxley')
    c.node('Opie')
    c.node('Synchron')
    c.node('TC_endo')

with g.subgraph(name='cluster_noninv') as c:
    c.attr(label='非侵入式 — EEG/fNIRS', style='dashed',
           color=GROUP_NONINV, fontcolor=GROUP_NONINV, fontsize='12')
    c.node('Gao')
    c.node('Han')
    c.node('BrainCo')
    c.node('BrainControl')
    c.node('TC_eeg')

with g.subgraph(name='cluster_ultra') as c:
    c.attr(label='非侵入式 — 超声 (新兴)', style='dashed',
           color=GROUP_ULTRA, fontcolor=GROUP_ULTRA, fontsize='12')
    c.node('MergeLabs')
    c.node('TC_ultra')

# =====================================================
# LEGEND
# =====================================================
with g.subgraph(name='cluster_legend') as lg:
    lg.attr(label='图例 Legend', style='filled', fillcolor='#f9f9f9',
            color='#cccccc', fontsize='11')
    lg.node('L1', '海外学者', shape='box', style='filled',
            fillcolor=FILL_PERSON_OVERSEAS, fontsize='9')
    lg.node('L2', '🇨🇳 中国学者', shape='box', style='filled',
            fillcolor=FILL_PERSON_CHINA, fontsize='9')
    lg.node('L3', '海外公司', shape='box', style='filled,rounded',
            fillcolor=FILL_COMPANY_OVERSEAS, fontsize='9')
    lg.node('L4', '🇨🇳 中国公司', shape='box', style='filled,rounded',
            fillcolor=FILL_COMPANY_CHINA, fontsize='9')
    lg.node('L5', '里程碑', shape='diamond', style='filled',
            fillcolor=FILL_MILESTONE, fontsize='9')
    lg.node('L6', '技术概念', shape='note', style='filled',
            fillcolor=FILL_TECH_CONCEPT, fontsize='9')
    lg.edge('L1', 'L2', style='invis')
    lg.edge('L2', 'L3', style='invis')
    lg.edge('L3', 'L4', style='invis')
    lg.edge('L4', 'L5', style='invis')
    lg.edge('L5', 'L6', style='invis')

# =====================================================
# RENDER
# =====================================================
output_path = g.render(filename='BCI_TechMap', directory='.', cleanup=True)
print(f'Generated: {output_path}')
