# Fig. TR2 — 图注

**Fig. TR2 | TWEAKR / Fn14（TNFRSF12A）三维结构在膜参考系中的位置与功能域。**
颜色与 Fig. TR1 相同，按冻结的 B32 坐标（UniProt Q9NP84 前体编号）着色：N-segment 28–35、
CRD 36–67、stalk 68–80、跨膜螺旋 81–101、膜内侧碱性簇 102–109（`RRCRRREK`）、
胞质尾 110–129。黄色棍状为三对二硫键（C36–C49、C52–C67、C55–C64），
红色棍状为定点突变实验中高亲和力 TWEAK 结合所必需的残基（D45、K48、M50、D62；Brown 2006，REF-034，用的是小鼠 Fn14，四个位点在人序列中残基相同）。突变实验说明它们是结合所必需的，不等于已测得它们与 TWEAK 直接接触。

**a,** AlphaFold DB 模型 AF-Q9NP84-F1（v6）的成熟链 28–129（信号肽 1–27 已移除）。**取向仅为示意**（图中以红色斜体注明）：域间几何未被确定，见限定 2。
模型做刚体旋转，使跨膜螺旋 81–101 的 Cα 主轴（PCA 第一主成分）竖直、N 端朝胞外；
双分子层以该螺旋 Cα 中点为中心绘制，疏水核心取 ±15 Å。比例尺 10 Å。
**b,** 实验结构 PDB 2KMZ（hFn14 胞外区 28–80，溶液 NMR，20 个模型中的第 1 个；
文件编号 1–53 加 27 即为 UniProt 编号）。以 CRD 的 32 个 Cα 叠合到 a 中 AF 模型的 CRD，
因此取向与 a 相同；CRD Cα RMSD 为 1.74 Å（对 model 1），对全部 20 个 NMR model 为 1.30–2.14 Å（中位数 1.59 Å），
落在 2KMZ 集合自身的离散范围内（两两比较中位数 1.48 Å，最大 2.60 Å）。
**c,** 线性功能域图（1–129，含信号肽），上方弧线为二硫键，三角为 TWEAK 结合残基；
下方为 AF 每残基 pLDDT，按 AlphaFold DB 的四档着色。

**限定（都不可省）：**

1. **膜是画上去的，不是模拟或预测出来的。** 膜的位置只由 TM 螺旋的轴线决定，
   没有用 PPM/OPM、MD 或任何膜插入计算。TM 螺旋 pLDDT 均值 87.5，用它定位是可以接受的。
2. **CRD 相对膜的位置和取向没有被确定。** AF 的 PAE 显示两个结构域各自可信
   （CRD 内 3.9 Å，TM 内 2.8 Å），但 CRD↔TM 之间平均 22–24 Å（上限 31.75 Å），
   即 AF 对两者的相对摆放基本没有约束。连接二者的 stalk 68–80 pLDDT 均值 64.8。
   a 中胞外域"立在膜上方、结合残基朝外"只是 AF 输出的其中一种构象，**不能**用来论证
   TWEAK 的接近方向、受体间距或膜上抗体可及性。这与 TR1 图注的限定一致：TR2 只借用
   AF 模型的域内折叠（CRD 已被 2KMZ 独立验证）和 TM 螺旋轴，不借用域间几何。
3. **胞质尾 110–129 为低置信区（pLDDT 均值 47.6）。** AF 把 124–129 的 Cα 放进了
   疏水核心（|y| < 15 Å），这在物理上不合理，是低置信模型的伪影，图中以星号注明。
   胞质尾标注了 PIEET 113–117：其中 P113–I–E–E116 符合 TRAF2 的主要结合 consensus (P/S/A/T)x(Q/E)E
   （Ye 1999，REF-037）；TRAF1/2/3/5 结合 Fn14 胞质尾见 Brown 2003（REF-036，小鼠 Fn14）。
   本项目只核对了序列匹配与摘要；该 motif 经 alanine scanning 定位的说法来自 GPT 审核，
   Brown 2003 全文未能取得，尚未逐条核实。
4. **2KMZ 只显示 model 1。** N-segment 和 stalk 在 NMR 集合中本身就柔性较大：
   以 CRD 叠合后，ECD 28–80 全长 Cα RMSD（AF vs 2KMZ model 1）为 12.8 Å，
   差异集中在两端，而不在 CRD。
5. 本图不含任何 CRC 数据，不支持任何关于 TWEAKR 在 CRC 中功能的主张。

**来源：** AlphaFold DB AF-Q9NP84-F1 v6（模型与 PAE，2026-11-03 取回）；PDB 2KMZ
（Pellegrini 2013，REF-033）；结合残基 Brown 2006（REF-034）；TRAF motif Ye 1999（REF-037）、Brown 2003（REF-036）；UniProt Q9NP84。checksum 见 `../manifests/inputs.tsv`。
**生成：** `code/render_fig_TR2_structures.py`（开源 PyMOL 3.2.0a，`pymol-open-source-whl` 3.2.0.2，
numpy 1.26.4）→ `code/make_fig_TR2_structure_membrane.R`（R 4.5.2；ggplot2 4.0.3、ggforce 0.5.0、
patchwork 1.3.2、png 0.1.9、jsonlite 2.0.0）。
**Source data：** `Fig_TR2_source_data.tsv`（每残基 domain、pLDDT、膜参考系坐标）、
`Fig_TR2_pae_blocks.tsv`。
