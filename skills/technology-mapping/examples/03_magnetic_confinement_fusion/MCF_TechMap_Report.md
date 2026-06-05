# 磁约束核聚变技术全景图谱报告
# Magnetic Confinement Fusion (MCF) Technology Map Report

**生成日期**: 2026-03-19
**图谱文件**: `MCF_TechMap.svg`
**生成脚本**: `generate_techmap.py`

---

## 一、赛道概述

磁约束核聚变（Magnetic Confinement Fusion, MCF）是利用强磁场将高温等离子体约束在特定空间内，使氢同位素（氘、氚）发生核聚变反应释放巨大能量的技术路线。作为"终极能源"的候选方案，MCF 自 1950 年代萨哈罗夫和塔姆提出托卡马克概念以来，历经 70 余年发展，已从纯学术研究进入商业化竞赛阶段。

2024-2026 年期间，全球 MCF 领域私人投资超过 70 亿美元，涌现出 CFS、TAE、Helion 等估值超 10 亿美元的独角兽企业，中国也出现了星环聚能、能量奇点、东昇聚变等获得亿元级融资的创业公司。技术路线呈现多元并进格局：常规托卡马克 + 高温超导（HTS）、球形托卡马克、仿星器、场反位形（FRC）等方案各展所长。

---

## 二、领域适应分析 (Domain Profile)

| 维度 | 分析 |
|------|------|
| 领域 | 磁约束核聚变 (MCF) |
| 知识载体权重 | 论文 0.85 / 专利 0.4 / 装置 0.6 / 开源 0.05 |
| 人才流动模式 | 大学PhD → 博后/教授 → 创业；国家实验室 → spin-off |
| 上游溯源类型 | PhD advisor chain (2-3层) + 国家实验室传承 |
| 中国模式 | 国家装置 (EAST/BEST) + 大学教授创业 (清华/复旦/中科大) |

---

## 三、识别到的技术路线

### 路线 1: 常规托卡马克 + HTS 高温超导
- **核心方案**: 用 REBCO 高温超导磁体产生 20T+ 强磁场，实现紧凑化
- **优势**: 显著缩小装置体积和成本，工程可行性高
- **挑战**: HTS 磁体大规模工程化、热管理
- **代表**: CFS/SPARC → ARC, 能量奇点/洪荒70
- **商业化阶段**: 原型机验证

### 路线 2: 球形托卡马克 (Spherical Tokamak)
- **核心方案**: 低纵横比 (A~1.5) "苹果核"形等离子体
- **优势**: 紧凑性极佳，高等离子体压力 (高β)
- **挑战**: 中心柱工程、功率处理
- **代表**: Tokamak Energy/ST80-HTS, 星环聚能
- **商业化阶段**: 原型机验证

### 路线 3: 仿星器 (Stellarator)
- **核心方案**: 外部线圈产生扭转磁场，无需等离子体电流
- **优势**: 稳态运行、无大破裂风险
- **挑战**: 复杂3D线圈设计制造
- **代表**: W7-X → Proxima Fusion
- **商业化阶段**: 实验验证

### 路线 4: 场反位形 (FRC)
- **核心方案**: 等离子体自生磁场约束，"烟环"形态
- **优势**: 结构简单、高β、紧凑
- **挑战**: 等离子体稳定性、规模化
- **代表**: TAE Technologies, Helion Energy, 诺瓦聚变
- **商业化阶段**: 实验验证 → 原型机

### 路线 5: 国家大科学装置
- **核心方案**: 大规模国际/国家合作，以验证聚变可行性为目标
- **代表**: ITER, EAST/BEST, JET, TFTR
- **特征**: 非商业化导向，但为所有商业路线提供科学基础

---

## 四、所有节点清单

### 学术 / 科学家节点

| 姓名 | 类型 | 所属流派 | 简介 | 置信度 |
|------|------|---------|------|--------|
| Igor Tamm 塔姆 | 海外学者 | 奠基人 | 1958诺贝尔奖，托卡马克概念提出者 | 95% |
| Andrei Sakharov 萨哈罗夫 | 海外学者 | 奠基人 | 1975诺贝尔和平奖，托卡马克概念提出者 | 95% |
| Lev Artsimovich 阿齐莫维奇 | 海外学者 | 奠基人 | T-3 托卡马克实验验证 | 95% |
| Lyman Spitzer 斯皮策 | 海外学者 | 仿星器 | 仿星器发明者 (1951)，PPPL 创始人 | 95% |
| Hannes Alfvén 阿尔文 | 海外学者 | 奠基人 | 1970诺贝尔物理学奖，MHD奠基人 | 95% |
| Dennis Whyte | 海外学者 | HTS 托卡马克 | MIT PSFC 前主任，CFS 联合创始人 | 90% |
| Martin Greenwald | 海外学者 | HTS 托卡马克 | MIT PSFC 高级科学家 | 85% |
| Bob Mumgaard | 海外学者 | HTS 托卡马克 | CFS CEO，MIT PhD | 90% |
| Brandon Sorbom | 海外学者 | HTS 托卡马克 | CFS CSO，MIT PhD，ARC 设计 | 90% |
| Alan Sykes | 海外学者 | 球形托卡马克 | UKAEA，球形托卡马克预言者 | 90% |
| Mikhail Gryaznevich | 海外学者 | 球形托卡马克 | Tokamak Energy 首席科学家 | 90% |
| Thomas Klinger | 海外学者 | 仿星器 | MPG IPP 所长，W7-X 负责人 | 85% |
| Francesco Sciortino | 海外学者 | 仿星器 | Proxima CEO，MIT PhD → MPG IPP | 85% |
| Norman Rostoker (1925-2014) | 海外学者 | FRC | UC Irvine，TAE 联合创办 | 95% |
| Michl Binderbauer | 海外学者 | FRC | TAE CEO，UC Irvine PhD (导师:Rostoker) | 90% |
| John Slough | 海外学者 | FRC | Helion 联合创办，U.Washington PhD | 85% |
| David Kirtley | 海外学者 | FRC | Helion CEO，U.Michigan → U.Texas | 85% |
| 🇨🇳 万元熙 | 中国学者 | 大科学装置 | 院士，EAST 项目总负责人 | 90% |
| 🇨🇳 李建刚 | 中国学者 | 大科学装置 | 院士，EAST 核心科学家，师从万元熙 | 85% |
| 🇨🇳 段旭如 | 中国学者 | 大科学装置 | 中核聚变首席科学家，CFEI 推动者 | 85% |
| 🇨🇳 谭熠 | 中国学者 | 球形托卡马克 | 清华副教授，星环聚能创始人 | 90% |
| 🇨🇳 杨钊 | 中国学者 | HTS 托卡马克 | 北大→Stanford PhD，能量奇点创始人 | 85% |
| 🇨🇳 许敏 | 中国学者 | 大科学装置 | 复旦教授，东昇聚变孵化 | 80% |

### 公司节点

| 公司 | 类型 | 技术路线 | 估值/融资 | VC 标注 |
|------|------|---------|----------|---------|
| CFS | 海外公司 | HTS 托卡马克 | ~$3B+ | 🏷️ 继承 MIT PSFC |
| TAE Technologies | 海外公司 | FRC | $1.79B | 🏷️ 继承 UC Irvine |
| Helion Energy | 海外公司 | FRC | $5.4B 估值 | 🏷️ 独立 (MSNW) |
| Tokamak Energy | 海外公司 | 球形 ST | $336M | 🏷️ 继承 UKAEA |
| Proxima Fusion | 海外公司 | 仿星器 | €185M+ | 🏷️ 继承 MPG IPP |
| 🇨🇳 星环聚能 | 中国公司 | 球形 ST | 10亿 A轮 | 🏷️ 继承 清华 |
| 🇨🇳 能量奇点 | 中国公司 | HTS 托卡马克 | 4亿+ | 🏷️ 独立 |
| 🇨🇳 东昇聚变 | 中国公司 | 托卡马克 D-He3 | 数亿天使轮 | 🏷️ 继承 复旦 |
| 🇨🇳 诺瓦聚变 | 中国公司 | FRC | 5亿天使轮 | 🏷️ 独立 |
| 🇨🇳 瀚海聚能 | 中国公司 | FRC | 5000万+ | 🏷️ 独立 |
| 🇨🇳 星能玄光 | 中国公司 | 场反磁镜 | 亿元天使轮 | 🏷️ 继承 中科大 |
| 🇨🇳 中国聚变能源 | 国家平台 | — | 国资 | 🏷️ 国家队 |

### 里程碑 / 装置节点

| 名称 | 年代 | 关键突破 |
|------|------|---------|
| T-3 托卡马克 | 1968 | Te=1keV，确立托卡马克优势 |
| TFTR | 1982-1997 | 10.7MW 聚变功率，5.1亿°C |
| JET | 1983-2023 | 69MJ 聚变能，Q=0.67 |
| ITER | 2007- | 目标 Q≥10，500MW 聚变功率 |
| EAST | 2006- | 1亿°C × 1000秒 (2025) |
| BEST 夸父启明 | 建设中 | 2027 聚变燃烧实验 |
| W7-X | 2015- | 世界最先进仿星器 |
| SPARC | 建设中 | HTS 20T 磁体验证 |
| START/MAST | 1991- | 首个大型球形托卡马克 |
| SUNIST | — | 中国首个球形托卡马克 |

---

## 五、关键发现

### 1. 师承脉络
- **托卡马克核心链**: Tamm/Sakharov → Artsimovich → T-3 → (全球托卡马克热潮) → ITER/EAST
- **CFS 师承链**: Dennis Whyte → Bob Mumgaard / Brandon Sorbom → CFS
- **TAE 师承链**: Norman Rostoker → Michl Binderbauer → TAE Technologies
- **仿星器链**: Lyman Spitzer → PPPL → ... → W7-X → Proxima Fusion
- **球形 ST 链**: Alan Sykes (UKAEA) → Tokamak Energy; 谭熠 (清华 SUNIST) → 星环聚能

### 2. 流派竞争格局
- **HTS 路线** 最被看好: CFS ($3B+) + 能量奇点 (洪荒70 突破) — 技术成熟度最高
- **FRC 路线** 融资最多: Helion ($5.4B估值) — 但技术风险也最高
- **球形 ST** 中国领先: 星环聚能 10 亿 A轮国内最大，且有 20 年清华 SUNIST 积累
- **仿星器** 欧洲独有: Proxima Fusion 是唯一仿星器创业公司

### 3. 中国独特优势
- **国家装置基础设施**: EAST 已创造多项世界纪录，BEST 85 亿建设中
- **学术→产业转化加速**: 2025-2026 年集中爆发，清华/复旦/中科大系公司密集诞生
- **国资+市场双轮驱动**: 中国聚变能源 (国家队) 与民营创业公司并行

### 4. VC 投资关键洞察
- 创始人技术深度最强: CFS (Dennis Whyte 团队)、TAE (Rostoker 团队)、星环聚能 (谭熠 团队)
- 技术来源最透明: CFS、Tokamak Energy、星环聚能均有清晰学术→公司传承链
- 潜在风险信号: 部分公司创始人非核心技术领域出身 (如杨钊理论物理→工程聚变)

---

## 六、溯源验证表

| 人物 | 关系声明 | Source 1 | Source 2 | 置信度 | 状态 |
|------|---------|----------|----------|--------|------|
| Tamm → 托卡马克概念 | 与 Sakharov 共同提出 | Wikipedia | IAEA | 95% | ✅ 已验证 |
| Sakharov → 托卡马克概念 | 与 Tamm 共同提出 | AIP.org | IAEA | 95% | ✅ 已验证 |
| Artsimovich → T-3 | 领导实验 (1968) | ITER.org | Wikipedia | 95% | ✅ 已验证 |
| Spitzer → 仿星器 | 1951年发明 | PPPL.gov | ASME | 95% | ✅ 已验证 |
| Spitzer 导师: H.N. Russell | PhD advisor | Wikidata | Caltech | 85% | ✅ 已验证 |
| Whyte → Mumgaard | PhD advisor | MIT.edu | CFS.energy | 90% | ✅ 已验证 |
| Whyte → Sorbom | PhD advisor | CFS.energy | MIT.edu | 90% | ✅ 已验证 |
| Rostoker → Binderbauer | PhD advisor | TAE.com | UCI.edu | 95% | ✅ 已验证 |
| Sykes → 球形 ST | UKAEA 预言 | AIP.org | Wikipedia | 90% | ✅ 已验证 |
| Slough/Kirtley → MSNW | MSNW 同事 → Helion | Contrary.com | House.gov | 85% | ✅ 已验证 |
| 万元熙 → EAST | 项目总负责人 | CAS.cn | 新华社 | 90% | ✅ 已验证 |
| 万元熙 → 李建刚 | 师承 | USTC.edu.cn | CAS.cn | 85% | ✅ 已验证 |
| 谭熠 → 清华 SUNIST | 副教授/运行 | 清华官网 | Startorus.cn | 90% | ✅ 已验证 |
| 杨钊 → Stanford PhD | 北大→Stanford | 上海临港 | 新浪 | 85% | ✅ 已验证 |
| Sciortino → MIT PhD → MPG | 学术路径 | Proxima.com | MIT.edu | 85% | ✅ 已验证 |
| Klinger → W7-X | 项目负责人 | MPG.de | Wikipedia | 85% | ✅ 已验证 |
| 许敏 → 复旦 → 东昇 | 团队孵化 | 复旦教务 | 投资界 | 80% | ⚠️ 单源 |
| 瀚海聚能创始人 | — | — | — | — | 🔍 孤儿 |
| 诺瓦聚变创始人 | — | — | — | — | 🔍 孤儿 |

---

## 七、溯源质量统计

```
📊 溯源完成率: 82.6% (19/23 需溯源人物节点)
📊 多源验证率: 84.2% (16/19 已溯源)
📊 孤儿率: 8.7% (2/23 孤儿节点: 瀚海聚能/诺瓦聚变创始人)
📊 平均置信度: 89.2%
```

> ✅ 溯源完成率 82.6% > 70% 目标 | ✅ 孤儿率 8.7% < 20% 目标

---

## 八、技术演进时间线

| 年代 | 里程碑 | 核心能力解锁 |
|------|--------|-------------|
| **1950s** | Tamm/Sakharov 提出托卡马克概念; Spitzer 发明仿星器 | 磁约束聚变理论框架 |
| **1968** | Artsimovich T-3 实验突破 | 确立托卡马克优势地位 |
| **1970** | Alfvén 获诺贝尔物理学奖 (MHD) | MHD 理论基础奠定 |
| **1982-94** | TFTR: 10.7MW 聚变功率 | 首次 D-T 聚变产能 |
| **1991** | START: 首个大型球形托卡马克 | 球形 ST 实验验证 |
| **1997-2023** | JET: 69MJ 聚变能 | D-T 聚变能量记录 |
| **1998** | TAE Technologies 成立 | FRC 商业化开始 |
| **2006** | EAST 首次等离子体 | 全超导托卡马克时代 |
| **2007** | ITER 正式签约 | 国际聚变大科学合作 |
| **2015** | W7-X 首次等离子体 | 仿星器工程验证 |
| **2018** | CFS 成立 | HTS 紧凑托卡马克商业化 |
| **2021** | CFS HTS 磁体 20T; 星环聚能/能量奇点成立 | HTS 关键工程突破; 中国创业潮 |
| **2023** | JET 最终记录; 中国聚变能源成立; Proxima Fusion 成立 | 行业里程碑/国家队+创业双轨 |
| **2025** | EAST 1亿°C×1000秒; Helion $5.4B 估值 | 长脉冲稳态突破; FRC 融资高峰 |
| **2026** | 星环聚能 10亿A轮; 能量奇点洪荒70 120秒; 东昇聚变成立 | 中国聚变商业化爆发 |
