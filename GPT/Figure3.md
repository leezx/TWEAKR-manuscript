对，这张 Figure 3 应该成为整篇文章的“hypothesis-definition figure”。但我会纠正一个措辞：它不是“把主要假设打穿”，而是把主要假设**收敛到几乎只有一个最优解释**。因为它仍然是 observational + inference + spatial triangulation，能非常强地 nominate，但不能证明 TAM-derived TWEAK 在体内因果维持 oncofetal state。

这一区分很重要。Figure 3 的任务不是 causal proof，而是做到：

> 从上万种可能的 TME–epithelial interaction 中，系统地收敛出 TNFSF12–TNFRSF12A，并证明 ligand source、receiver state、macrophage subtype、patient-level coupling 和 spatial organization 全部指向同一个模型。

如果做成这样，这张图虽然“不是最 solid”，但会是整篇文章**最重要的逻辑枢纽**。

我建议标题也稍微改一下，避免提前越过因果边界：

> **Population-scale and spatial analyses nominate a TWEAK+ macrophage niche for TNFRSF12A-high oncofetal tumour cells**

或者稍微更强：

> **TWEAK+ macrophages are positioned to signal to TNFRSF12A-high oncofetal tumour cells in colorectal cancer**

“Macrophage-derived TWEAK drives...” 留给实验图之后。

---

Figure 3 的逻辑最好不是“source–receptor–spatial”简单三块，而是按一条收敛路径：

**receiver discovery → ligand nomination → source identification → source-state definition → population coupling → spatial coupling**

这样 reader 会感觉是你一步一步把 hypothesis 推出来，而不是后验拼图。

我会这样排。

**3A. Population-scale receptor screen nominates TNFRSF12A as a receptor associated with the oncofetal state**

这是 Figure 3 的入口，而且很重要。

不要一开始直接拿 TNFRSF12A 出来。

做：

* epithelial receptor universe
* patient-level correlation / voting
* oncofetal MP 或 frozen oncofetal signature
* 每个 receptor 跨 patient 一致性
* TNFRSF12A 排名前列

最好有：

* rank plot
* recurrence across cohorts/patients
* TNFRSF12A 在 oncofetal-high vs other epithelial states 的 enrichment

这一步的 claim：

> **TNFRSF12A is one of the epithelial receptors most consistently associated with the oncofetal state across CRC patients.**

不是：

> TNFRSF12A regulates the state.

这部分你 proposal 里已经有类似 patient-level voting 的 preliminary framework。

---

**3B. Ligand–target inference converges on TNFSF12–TNFRSF12A**

现在才问：

既然 receiver 是 TNFRSF12A，谁在 upstream？

这里可以整合：

* NicheNet
* LIANA
* CellChat
* curated LR prior

但我不建议同时摆三个软件的 logo，然后说“三个软件都支持”。那很容易变成方法堆砌。

最好做成一个统一 evidence ranking：

* receptor associated with target state
* ligand expression in TME
* known LR compatibility
* ligand-target regulatory potential
* cross-patient recurrence

最后 TNFSF12–TNFRSF12A 排上来。

如果 TGFβ / PGE2 / IL33 / IL36 也很高，反而不要隐藏。

最好展示：

* TGFβ
* TNFSF12
* 其他已知 regenerative ligands

然后强调：

> TNFSF12–TNFRSF12A emerged as one of the most recurrent candidate axes.

这比“唯一 pathway”更可信。

---

**3C. TNFSF12 is predominantly expressed by macrophages across CRC ecosystems**

这是 source panel。

这里你现在有很好的优势：human atlas + 自己的 mouse scRNA。

主图最好不是只放一个 human dot plot，而是：

Human CRC atlas
+
AOM/DSS mouse CRC
+
Cdx2/APC/KRAS model

三个 context 并列。

问同一个问题：

> 哪个 major cell compartment 提供 TNFSF12？

如果三个体系都是 macrophage dominant，这会非常强。

这里 claim 可以逐渐变强：

如果 human + mouse 都非常稳定：

> **Macrophages are the predominant cellular source of TNFSF12 across human and mouse CRC.**

如果 human 稍杂：

> **TNFSF12 is consistently enriched in macrophages across human and mouse CRC.**

你自己 mouse 数据的价值就在这里：它不只是“更干净”，而是**正交体系 validation**。

但仍然是 expression source，不是 secretion source。

也就是说，不要写：

> macrophages secrete TWEAK

除非你有 protein/secretome evidence。

写：

> macrophages are the major transcriptional source of TNFSF12.

---

**3D. TNFSF12-high macrophages correspond to an SPP1+/lipid-associated TAM state**

这一 panel 非常值得做，但我赞成你的判断：不要人为发明一个“TWEAK+ TAM subtype”。

如果 TNFSF12-high cells 落在：

* SPP1+
* LAM-like
* inflammatory/remodeling TAM

那就把它定位成：

> **TNFSF12 expression is concentrated within an SPP1+/LAM-like macrophage state.**

这里可以做：

* macrophage-only UMAP
* TNFSF12 feature plot
* SPP1 / APOE / TREM2 / GPNMB / LPL 等 marker
* TNFSF12-high vs low macrophage DEG
* reference TAM signature enrichment

这个 panel 的目的不是发现一个新 macrophage taxonomy，而是回答：

> 什么样的 TAM 最可能提供 TWEAK？

这会给后面的 biological model 加很多质感。

但要小心一个点：

**SPP1+ 和 LAM 不是完全等价术语。**

如果你的 macrophage state 只是部分 overlap，最好写：

> SPP1+/LAM-like

不要直接写：

> TWEAK+ TAMs are LAMs.

---

**3E. TNFSF12-high TAM abundance couples with TNFRSF12A/oncofetal epithelial state across patients**

这是我认为这张图最容易被低估、但实际上很关键的一张 panel。

空间图很漂亮，但 reviewer 会问：

> 这是一个 sample 的偶然结构吗？

你要做 population-level ecological coupling。

每个 patient / sample：

x：

* macrophage TNFSF12 pseudobulk
  或
* fraction of TNFSF12-high macrophages
  或
* TNFSF12+ TAM abundance

y：

* epithelial TNFRSF12A
* oncofetal MP
* revCSC score

最好不是只做一个相关性。

我会做一个小矩阵：

| macrophage feature        | epithelial feature |
| ------------------------- | ------------------ |
| TNFSF12 expression        | TNFRSF12A          |
| TNFSF12-high TAM fraction | oncofetal MP       |
| SPP1/LAM TAM abundance    | oncofetal MP       |

然后挑最干净的一个放 scatter。

这里一定：

* patient-level
* study-aware
* 最好 mixed model / meta-analysis across cohorts
* 不要 cell-level

如果这个结果很稳，Figure 3 的“population-scale communication”就真正建立了。

---

**3F. Spatial transcriptomics places TNFSF12+ macrophages adjacent to TNFRSF12A-high/oncofetal tumour regions**

现在进入 spatial。

这部分你现在很可能会做得非常漂亮，但不要只放 feature maps。

最好有两层：

第一层，representative images：

* H&E / tumor annotation
* oncofetal score
* TNFRSF12A
* macrophage
* TNFSF12

第二层，quantification：

* distance
* neighborhood enrichment
* boundary-zone enrichment
* permutation null

最重要的是：

**spatial figure 必须从“图片”升级到“统计”。**

比如：

distance from TNFSF12+ TAM to:

* oncofetal-high tumor
* proCSC-high tumor

如果 TNFSF12+ TAM 更接近 oncofetal than proCSC，这比单纯 co-localization 高一个等级。

甚至可以做：

TNFSF12-high TAM
vs TNFSF12-low TAM

谁更靠近 oncofetal tumor。

这个会非常强。

---

**3G. Cross-sample spatial reproducibility**

如果你有多个 Visium HD / Xenium / spatial cohort，我强烈建议单独给一个小 panel。

每个 sample 一个 effect size：

* enrichment odds ratio
* mean distance difference
* neighborhood association coefficient

然后 forest plot / dot plot。

这张图可以把：

> “这里有一张特别漂亮的 slide”

升级成：

> “这一 spatial relationship 在患者层面可复现。”

如果版面只能放一个 additional panel，我会优先放这个，而不是再加一个花哨的 ligand-receptor heatmap。

---

所以整个 Figure 3 最终我会排成：

**3A** Population-scale epithelial receptor screen identifies TNFRSF12A
**3B** Ligand–target inference nominates TNFSF12–TNFRSF12A
**3C** Macrophages are the predominant TNFSF12-expressing population across human and mouse CRC
**3D** TNFSF12 is concentrated in SPP1+/LAM-like TAM states
**3E** TNFSF12-high TAMs covary with TNFRSF12A/oncofetal epithelial states across patients
**3F** TNFSF12+ TAMs preferentially localize near TNFRSF12A-high/oncofetal tumour regions
**3G** Spatial coupling is reproducible across independent CRC sections/patients

这张图结束以后，reader 应该产生一个非常明确的感觉：

> “OK，TNFRSF12A 不是随便挑的 receptor；TNFSF12 不是随便挑的 ligand；macrophage 不是随便挑的 source；SPP1/LAM TAM 不是随便挑的 cell type；而且这一轴在 patient-level 和 spatial level 都成立。”

这就是你想要的“hypothesis彻底定型”。

但我仍然会把 claim 停在：

> **These orthogonal analyses nominate a TNFSF12+ macrophage–TNFRSF12A-high epithelial niche associated with the oncofetal state.**

而不是：

> “TAM-derived TWEAK maintains the oncofetal state.”

后一句留给 Figure 4。

这样 Figure 4 一开始只需要问一句：

> **Is this computationally nominated interaction causal?**

然后：
TWEAK stimulation
→ TNFRSF12A KO
→ RNA-seq
→ YAP/oncofetal state
→ public perturbation

故事就完全接上了。

还有一个战略建议：**Figure 3 不要引入 Placenta，也不要引入 immune evasion。**

这张图已经足够复杂，而且它是整个故事最核心的 hypothesis-construction figure。任何 placenta / MHC-I / ICI 机制在这里出现，都会稀释真正重要的信息：

**TAM → TWEAK → TWEAKR-high oncofetal epithelial state。**

如果最后全文只有一张图让 reviewer记住你怎么发现这条轴，我希望就是 Figure 3。
