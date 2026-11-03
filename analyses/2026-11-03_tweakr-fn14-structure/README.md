# TWEAKR / Fn14 结构参考：拓扑图与坐标冻结

**对话日期：** 2026-11-03 · **执行者：** Claude Opus 5 for Zhixin Li
**状态：** S1（结构图集）完成：Fig. TR1 拓扑图 + Fig. TR2 膜内三维结构参考图（2026-11-03 第二轮）；未审核、未 push、无 PR
**UDE 分支：** B32（见 `../../UDE/root-branch-history.md`）

## 1. 问题与目标

把 TWEAKR（TNFRSF12A / Fn14）的膜拓扑坐标**一次性核实并冻结**，作为后续所有结构工作
（AF3 建模 M1–M4、跨膜示意图、界面位点标注）的唯一坐标来源，避免每次从综述或 GPT 文本里
重新抄一遍数字。

交付物是一张可引用的拓扑参考图加一份坐标表。

## 2. 对应 Figure / panel

目前**不对应任何已规划的 manuscript panel**。这是 B32 结构机制支线的内部参考图
（Fig. TR1）。若将来 B32 进入正文，它可作为机制示意图的底图。

## 3. 输入数据

本分析不使用项目数据集（无 `DS-xxx`）。输入全部是公共数据库记录，于 2026-11-03 取回：

| 来源 | ID | 取回方式 | 用到的内容 |
|---|---|---|---|
| UniProt | **Q9NP84**（TNFRSF12A_HUMAN） | `rest.uniprot.org/uniprotkb/Q9NP84.txt` 与 `.fasta` | 序列、SIGNAL、CHAIN、TOPO_DOM、TRANSMEM、REPEAT、DISULFID、VAR_SEQ |
| UniProt | Q9CR75（小鼠） | 同上 | 边界比对（与人相同） |
| PDBe | **2KN1** | `ebi.ac.uk/pdbe/api/pdb/entry/summary/2kn1` | 条目标题核实 |
| PDB | 2KMZ / 2KN0 | 文献 PubMed 23438059 | 实验结构参考（未下载坐标文件） |

**没有重数据**，没有下载结构坐标文件，没有外部计算。

## 4. 参考文献

- **REF（待登记）** Winkles JA. The TWEAK–Fn14 cytokine–receptor axis: discovery, biology and
  therapeutic targeting. *Nat Rev Drug Discov* 2008;7(5):411–425. doi:10.1038/nrd2488（PMC3018765）
- PubMed 23438059（2013，hFn14 与 xFn14 的 NMR 胞外结构；2KMZ、2KN0）

两条都应补进 `1.TWEAKR-oncoFetal/reference.md` 并分配 `REF-xxx`，本次未做。

## 5. 方法、软件版本与参数

R 4.5.2（cairo 可用）· ggplot2 4.0.3 · ggforce 0.5.0 · patchwork 1.3.2 · svglite 2.2.2 · ragg 1.5.2。

**无随机过程，无随机种子**：图中每个几何对象的位置都是脚本里写死的常数，
每个残基编号都是 UniProt 注释，每个序列片段都由 `substr()` 从序列取出而不是手打。

脚本内置 11 项 `stopifnot` 自检，任一不符立即报错而不出图：

1. 序列长度 = 129；
2. 四个边界残基身份：G27|E28（信号肽|ECD）、P80|I81（ECD|TM）、W101|R102（TM|胞内）、Q129（C 端）；
3. 四个结合位点身份：D45、K48、M50、D62；
4. CRD 36–67 内六个半胱氨酸的位置恰为 36/49/52/55/64/67；
5. 分段长度加和：成熟链 102 aa、ECD 53 aa、TM 21 aa、ICD 28 aa。

## 6. 产出文件

全部由 `code/make_fig_TR1_topology.R` 生成（`cd code && Rscript make_fig_TR1_topology.R`）：

| 文件 | 内容 |
|---|---|
| `figures/Fig_TR1_Fn14_topology.{pdf,svg,png}` | 拓扑参考图，95 × 125 mm，PNG 600 dpi |
| `figures/Fig_TR1_source_data.tsv` | 七个区段的起止、长度和序列 |
| `figures/Fig_TR1_disulfides.tsv` | 三对二硫键 |
| `figures/Fig_TR1_sessionInfo.txt` | R 会话记录 |

冻结坐标（人鼠边界相同）：

```
Signal 1-27 · 成熟链 28-129 (102 aa)
ECD 28-80 (53) · TM 81-101 (21, helical) · ICD 102-129 (28)
CRD (TNFR-Cys, atypical) 36-67 · 二硫键 36-49 / 52-67 / 55-64
膜内侧碱性簇 102-109 RRCRRREK
结合位点 D45 K48 M50 D62（全部在 CRD 内）
```

## 7. 验证与质控

- UniProt 注释由我直接向 `rest.uniprot.org` 取回核对，不是转述。
- 脚本硬编码的 129 aa 序列与 UniProt FASTA **逐字符比对完全一致**。这一步是必要的：
  脚本的自检是拿序列去验位点，如果序列本身抄错，自检会在错序列上**全部通过**。
- 图渲染后目视检查过一次，修掉了 `M50` 与边界标签 `36` 的重叠。

## 8. 负结果与更正

核对过程中发现两处既有记录错误，已在 `../../UDE/TWEAKR-AF3.md` 内标注更正：

1. **2KN1 不是 Fn14 结构。** PDBe 条目标题是 "Solution NMR Structure of BCMA"。
   PubMed 23438059 的摘要同时列出 2KMZ/2KN0/2KN1，但只有前两个是 Fn14。
2. **TM = 21 aa 的来源是 UniProt，不是 Winkles 2008。** 该综述给出 129/102/53/28，
   但没有给跨膜段长度，也没有讨论 Fn14 的糖基化。

另：agent 报告中把 ECD 28–80 的序列写成 `GEQAPGTAP…`，多了首位 G（G27 属信号肽）。
正确起始是 E28。脚本不受影响（按坐标 substr 取段）。

## 9. 限制与 claim ceiling

- **这是拓扑示意图，不是结构渲染。** 膜平面是人工参考线，不来自任何模型。
  CRD 画成椭圆团块，内部二硫键连线和四个位点的点位**都是示意位置**，
  不携带空间信息 —— 因此四个点不单独标注，身份写在一条注释里。
- ECD 折叠要引实验结构 **2KMZ**。**不得**用 AlphaFold 全长模型定义膜平面或 ECD–尾相对位置：
  AF-Q9NP84-F1 全局 pLDDT 仅 73.19，胞内尾必然低置信。
- **TRAF 结合 motif 的精确残基范围未核实。** Winkles 2008 只说"a single TRAF consensus
  binding motif"，没给坐标。图上把 110–129 整体标为 "TRAF region"，没有标 motif 坐标。
  要标必须先查 TRAF 结合的原始文献。
- 本目录**不含任何 CRC 数据**，不支持任何关于 TWEAKR 在 CRC 中功能的主张。

## 10. 未完成 / 下一步

- [ ] 把 Winkles 2008 和 PubMed 23438059 登记为 `REF-xxx`
- [ ] M1b（ECD 28–80）AF3 预测与 2KMZ 比 RMSD —— 这是 M2 复合物模型可信度的前置校验
- [ ] M2（TWEAK trimer + 3×ECD），验收标准：D45/K48/M50/D62 必须落在预测界面上
- [ ] isoform 2（Q9NP84-2，缺 33–67 即整个 CRD 与三对二硫键）是否纳入 —— 对应
      "ligand-independent clustering" 问题

## 11. PR 与审核状态

未 commit、未 push、无 PR、未审核。按 AGENTS.md §4，合并前不是 canonical evidence。


---

## 12. Fig. TR2 — 膜内三维结构参考图（2026-11-03 第二轮）

**目标。** 用户要求一张「TWEAKR 与细胞膜的参考图」：显示真实蛋白结构，并按 domain 分色标注。
TR1 是手画拓扑示意，TR2 换成真实坐标。

**输入**（全部在 HotData，仓库只存 manifest：`manifests/inputs.tsv`，含 URL、日期、sha256）：
`/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/external/structures_fn14/`
下的 AF-Q9NP84-F1 v6 模型与 PAE、PDB 2KMZ（20 模型 NMR 集合）、UniProt Q9NP84 FASTA。

**方法。**
1. `code/render_fig_TR2_structures.py`（开源 PyMOL 3.2.0a，`SOFTWARES/tools/pymol-open-source/.venv`）：
   AF 模型序列与 UniProt 逐字符比对，并检查 4 个结合位点和 6 个半胱氨酸的身份；
   去掉信号肽 1–27；对 TM 81–101 的 Cα 做 PCA 取主轴，竖直放置（N 端朝外），
   再绕该轴旋转，使 CRD 质心落在像平面内；正交投影渲染，用于后续定位标签的像素↔Å 映射
   写入 `projection.json`。2KMZ model 1 编号加 27，以 CRD 32 个 Cα 叠合到 AF 模型后同向渲染。
2. `code/make_fig_TR2_structure_membrane.R`（R 4.5.2）：画双分子层（由 TM 中点定位，±15 Å），
   叠加渲染图，按 `projection.json` 放置标注；c 为线性 domain 图与 pLDDT；读取 PAE 计算域间块均值。
   没有随机过程。

**运行：** `cd code && $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python render_fig_TR2_structures.py && Rscript make_fig_TR2_structure_membrane.R`

**产出：** `figures/Fig_TR2_Fn14_structure_membrane.{pdf,svg,png}`（180 × 122 mm，PNG 600 dpi）、
`Fig_TR2_legend.md`、`Fig_TR2_source_data.tsv`、`Fig_TR2_pae_blocks.tsv`、`Fig_TR2_sessionInfo.txt`、
`figures/TR2_parts/`（两张中间渲染 + 投影映射 + 每残基表）。sha256 见 `manifests/outputs.tsv`。

**验证与数字。**

| 检查 | 结果 |
|---|---|
| AF 序列 = UniProt Q9NP84 | 一致（129 aa） |
| 2KMZ 编号偏移 | DBREF 1–53 ↔ 28–80；SSBOND 换算后为 36–49 / 52–67 / 55–64，与冻结坐标一致 |
| CRD Cα RMSD（AF vs 2KMZ model 1，32 Cα） | **1.25 Å** |
| ECD 28–80 Cα RMSD（CRD 叠合后，不再拟合） | 10.6 Å（差异来自柔性两端） |
| TM 81→101 沿轴上升 | 29.4 Å |
| 平均 pLDDT | N-seg 52.1 · CRD 86.8 · stalk 64.8 · TM 87.5 · JM 70.0 · C-tail 47.6 |
| 平均 PAE | CRD 内 3.9 Å · TM 内 2.8 Å · **CRD↔TM 24.2 / 22.2 Å** · TM→JM 6.8 Å · TM→C-tail 15.6 Å |
| 像素映射 | 计算的 Q129、TM 端点像素位置与渲染图目视吻合 |

**负结果 / 问题。**
- **PyMOL.app 2.5.7 的许可证已于 2024-07-01 过期**，每张 ray-traced 图都打 "License expired" 水印，
  不可用于出图。改用开源 PyMOL（新装，已登记 `SOFTWARES/TOOL_INDEX.md`）。
  `pymol-open-source-whl` 3.2.0.2 声明需要 numpy≥2.2，但在 numpy 2.5.4 下 `get_coords` 报 ABI 错误，
  必须固定 numpy 1.26.4（pip 会报版本冲突警告，可忽略）。
- AF 把 C 端 124–129 的 Cα 放进了疏水核心，属低置信伪影，图上以星号注明。
- AF DB 直接下载返回 403，需要加 User-Agent 头；RCSB 和 UniProt 不受影响。

**claim ceiling（TR2）。** 域内折叠可引用（CRD 已由 2KMZ 独立确认）；TM 螺旋轴用于放膜。
**域间几何不可引用**：CRD 相对膜的高度、倾角，以及结合残基「朝外」，都只是 AF 的一个构象
（CRD↔TM PAE ≈ 23 Å）。不得据此讨论 TWEAK 的接近方向、受体间距或抗体可及性，
这些问题要等 M2 复合物模型和实验数据。TRAF motif 坐标仍未核实。

**与 TR1 限定的关系。** TR1 写的是「不得用 AF 全长模型定义膜平面或 ECD–尾相对位置」。
TR2 用 AF 的 TM 螺旋轴来放膜：这条螺旋本身是高置信的（pLDDT 87.5，域内 PAE 2.8 Å）；
ECD 相对膜的位置则明确标为「未确定」。因此 TR2 没有违反 TR1 的限定，只是把它量化了。
