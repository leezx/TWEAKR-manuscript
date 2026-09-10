到 Figure 5 这里，文章其实已经到了一个很关键的决策点：**不要再让最后一张图承担“把所有有趣想法都塞进去”的任务。** 前四张图已经足够形成一篇完整论文：

Fig.1 定义 recurrent oncofetal state；Fig.2 建立 clinical aggressiveness / treatment persistence；Fig.3 nominate TAM–TWEAK–TWEAKR niche；Fig.4 建立 TWEAKR–YAP–oncofetal 因果链。

因此 Figure 5 的唯一必要任务应该是：

> **证明 Figure 4 的 cell-state mechanism 在体内成立，并连接一个真实疾病表型。**

Placenta、immune suppression、macrophage origin 都只能在它们能够加强这个闭环时进入，不能反过来要求 Figure 5 再开三条机制线。

还有一个技术前提要先钉住：如果你说的是真正的 immunodeficient xenograft，那么 ICI 基本不能作为有效 functional endpoint；ICI 需要 immunocompetent/syngeneic setting。你的 King proposal 实际设计的是 AKP → C57BL/6 syngeneic transplantation，这个体系才适合讨论 ICI。

我会把最后一张主图设计成：

## Figure 5. TWEAKR–YAP signaling maintains the oncofetal state in vivo and modulates therapeutic response

**5A. In vivo experimental design**

至少：

Control
TWEAK / vehicle
TWEAKR KO
YAP perturbation

如果资源允许，再叠加一个 treatment arm：

chemo 或 ICI 二选一作为主 endpoint。

我不建议主图里同时 chemo + ICI 都做完整 factorial design，动物量和解释复杂度会急剧上升。Figure 2 已经告诉你哪个临床 context 最强，就让 Figure 5 验证那个。

---

**5B. In vivo malignant-state landscape**

scRNA：

control / TWEAK / TWEAKR KO / YAP perturbation

看：

* oncofetal/revCSC
* proCSC
* differentiation
* YAP activity

最好不仅是 UMAP，而是 mouse-level state proportion。

真正需要看到的是：

TWEAK → OnF expansion
TWEAKR loss → OnF contraction
YAP loss/inhibition → phenocopy TWEAKR loss

如果出来，这就是全文最重要的 in vivo validation。

---

**5C. Pseudobulk confirms transcriptional state remodeling in vivo**

每只 mouse 一个 pseudobulk。

比较：

* Figure 1 NMF-OnF MP
* published revCSC
* fetal
* YAP/TEAD
* proCSC

这部分甚至比 UMAP 更重要，因为它避免 pseudoreplication。

---

**5D. In vitro and in vivo perturbations converge on the same transcriptional program**

这是非常漂亮的 closure：

Figure 4 TWEAK-induced genes
vs
Figure 5 TWEAK-induced in vivo genes

以及：

TWEAKR-KO in vitro
vs
TWEAKR-KO in vivo

再进一步：

Figure 1 human patient OnF MP
↔ Figure 4 in vitro perturbation
↔ Figure 5 in vivo perturbation

如果这三者高度一致，你的主机制故事就真正闭环了。

这是我认为 Nature Communications 水平最应该追求的图，而不是 placenta。

---

**5E. Therapeutic pressure interacts with the oncofetal state**

这里只选 Figure 2 最强的临床出口。

如果 chemo 数据最稳：

Control
Chemo
TWEAKR KO
TWEAKR KO + chemo

看：

* tumor response
* residual OnF fraction
* proCSC fraction
* regrowth/persistence

如果 ICI 最稳并且是 syngeneic：

Control IgG
ICI
TWEAKR KO
TWEAKR KO + ICI

同样看 residual state + response。

如果发现 TWEAKR KO 改变 drug response，这时才开始有资格写：

> TWEAKR-dependent oncofetal plasticity contributes to treatment persistence.

如果只有 drug treatment 后 OnF 比例变化，而 tumour response 没有改变，就只能说：

> therapy remodels the abundance of the TWEAKR-associated oncofetal state.

两者差别很大。

---

**5F. Working model**

最后非常简单：

TWEAK+ TAM
→ TWEAKR
→ YAP/TEAD
→ oncofetal/revival plasticity
→ persistence under disease/treatment pressure

下面用虚线表示尚未完全证明的 extension：

immune phenotype
placental convergence

这比在 model 里把所有箭头画成实线要可信得多。

---

然后我们可以正式处理你说的三个“番外篇”。我的判断很明确：

| 模块                              | 我建议的位置                                                       | 当前能安全支持的 claim                                                                                          | 主要原因                                                         |
| ------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Macrophage-derived TWEAK**    | **主线保留，但需要降措辞或补一个极小实验**                                      | TAMs are the predominant/enriched TNFSF12-expressing source and are spatially positioned near OnF cells | 它是整个 TME→epithelium 故事的来源，删除会损伤 novelty                      |
| **Immune suppression**          | **Supplement + Figure 2/5 的 exploratory clinical extension** | OnF/TWEAKR-high states are associated with antigen-presentation/cytotoxicity/ICI-response programs      | 当前没有 functional immune evidence，不能叫 immune evasion mechanism |
| **Placenta**                    | **Supplement / Discussion；默认不进入主故事**                         | OnF CRC states show partial transcriptional convergence with selected placental/trophoblast programs    | 证据债务最大，且不是 TWEAKR–OnF 主链所必需                                  |
| **Placenta–macrophage analogy** | **优先删除**                                                     | 最多是 developmental/ecological analogy                                                                    | 距离主问题太远，相关性的相关性，几乎不增加主线可信度                                   |

这里我尤其想把三者拆开讲。

### Macrophage-derived TWEAK：值得救

这是三者里面唯一一个我认为值得投入一点额外实验去救的。

因为它直接回答文章最重要的问题：

> 为什么 CRC tumour cell 的 oncofetal state 会在 TME 中被激活？

你已有 human/mouse scRNA + spatial data，本身已经可以很强地证明 TNFSF12 的 macrophage enrichment 和空间定位。proposal 现在也是把这些结果定位成“nominate a TAM-derived TNFSF12 axis”，而真正验证 macrophage sufficiency / ligand dependence 被放到了后续 co-culture 和 depletion experiments。

所以最低成本实验我仍然推荐：

macrophage-conditioned medium
→ organoid OnF/YAP ↑

然后：

CM + TWEAK neutralization
或 Tnfsf12-deficient macrophage CM
→ effect significantly reduced。

这一个小实验可能比你做十张 placenta figure 更有价值。

因为它直接解决 title 中 **“macrophage-derived”** 这两个词。

如果不做，那标题和全文就改成：

> **TWEAK–TWEAKR signaling...**

或者：

> **A TWEAK+ macrophage niche is associated with...**

不要硬写 macrophage-derived TWEAK drives。

你以前的 figure planning 里其实也已经准确识别了这一点：如果要把“macrophage-derived”作为强 claim，需要至少 macrophage-derived signal recapitulation，否则 source identification 与 receptor mechanism 中间仍缺 functional bridge。

---

### Immune suppression：有价值，但不要再称为机制线

这一块比 Placenta 有价值得多，因为你已经有：

ICI patient data
cytotoxicity-associated expression
antigen-presentation programs
YAP/TEAD ChIP-seq
空间 immune context

而且 Figure 2 已经在临床层看到 therapy response。

所以它不是垃圾。

但目前能证明的是：

> **the TWEAKR/oncofetal state has an immune-associated transcriptional phenotype**

而不是：

> **TWEAKR creates immune evasion.**

尤其你提到 YAP/TEAD ChIP-seq 有 direct binding，这一点需要严格理解：

YAP/TEAD peak at immune-regulatory loci
+
TWEAK/YAP perturbation causes expression change

可以支持：

> YAP/TEAD directly regulates components of this transcriptional program.

但它仍然不能证明：

> these transcriptional changes make tumour cells resistant to T-cell killing.

binding ≠ functional immune suppression。

你们之前规划文档自己其实已经给出了正确证据层级：signature、MHC-I/IFNγ、CD8/TAM associations 是描述性证据；要真正 claim immune evasion，最低也需要 IFNγ challenge，更强才是 T-cell killing 或免疫完整小鼠中的 functional reversal。

所以我建议把 immune 做成一个非常完整的 Supplementary Figure，而不是半吊子 Main Figure：

OnF high vs low：
antigen presentation
IFNγ response
cytotoxic resistance
checkpoint ligands

然后 public YAP/TEAD binding 支持 direct regulation。

再加 ICI cohort association。

标题可以是：

> **The TWEAKR-associated oncofetal state exhibits an immune-modulatory transcriptional phenotype**

这完全可以发表。

如果未来顺手做一个特别简单的 IFNγ challenge：

TWEAK ± IFNγ
TWEAKR KO ± IFNγ

然后看 B2M / HLA-I / TAP1 / NLRC5，

结果如果非常漂亮，就把这一块从 supplement 升回来。

它是一个高 ROI optional experiment。

---

### Placenta：现在应该主动降级，而不是想办法救

这里我会比之前更激进。

你现在已经有一个非常自然的 biological lineage：

normal intestinal stemness
→ fetal/regenerative state
→ revCSC/oncofetal CRC
→ YAP

这个链条文献上非常扎实。公开的 fetal intestinal epigenomic work甚至显示 Tnfrsf12a 本身是 YAP-associated fetal gene，而且 YAP activation 足以推动 adult organoid 向 fetal-like state转换。

**你根本不缺 developmental concept。**

Placenta 是额外加上去的。

它只有在出现一种结果时才值得进入主图：

> 在严格拆除 generic fetal/YAP/EMT/stress components 后，仍然存在一个真正 placenta/trophoblast-specific transcriptional module，并且这个 module 被 TWEAK→TWEAKR→YAP 因果调控。

如果这个结果特别漂亮，我允许它成为 Figure 4 或 Figure 5 的一个小 panel：

> TWEAKR-driven oncofetal reprogramming partially converges with an extraembryonic developmental program.

仅此而已。

但如果目前只是：

OnF score ↔ placenta score
TWEAKR ↔ placenta score
placenta ↔ macrophage
spatial proximity

我建议全部移出主文。

因为这种证据链是：

A correlates B
B correlates C
C resembles D
therefore A recapitulates D

这是 reviewer 最容易攻击的一类 narrative overreach。

甚至已有“cancer–placenta similarities”这一概念本身并不新；你上传的文献就明确讨论了 cancer 与 placentation 的共同抗原和 immune escape analogy。 所以单纯证明 CRC 有 placenta-like expression 并不会自然给文章增加 novelty，反而会要求你证明为什么这不是 generic developmental reactivation。

因此我会给 Placenta 一个明确的 stop rule：

> **不再为 Placenta 开任何新的湿实验。**

只允许使用已经存在的 public computational analysis。

做完以后，如果有清楚的 placenta-specific signal：

放 Supplement。

如果特别惊艳：

升一个小 main panel。

如果拆除 fetal/YAP/shared genes 后基本消失：

直接删。

这不是失败，而是一个很好的 negative result——说明你的 biology 其实就是更干净的 fetal/revival program。

---

还有一个你现在应该主动避免的概念组合：

> **oncofetal–placental immune-evasive state**

我认为这个名字现在应该废弃。

因为它一次性要求你证明三个层级：

oncofetal identity
placental identity
immune evasion function

目前只有第一个是真的很硬。

更合适的主体就是：

> **TWEAKR–YAP-dependent oncofetal/revival state**

Immune 和 placenta 只作为 possible phenotypic extensions。

---

如果按 Nature Communications 的“最小完备项目”思路，我会把所有资源按照下面的顺序砍：

**必须完成：**

Fig 1 — recurrent OnF state
Fig 2 — clinical / treatment relevance
Fig 3 — TWEAK+ TAM niche nomination
Fig 4 — TWEAK → TWEAKR → YAP → OnF causality
Fig 5 — in vivo OnF state remodeling ± one clinically relevant treatment

这五张已经完整。

**一个最值得额外做的小实验：**

macrophage CM ± TWEAK blockade。

因为它补的是主轴缺口。

**第二个值得做、但有时间才做：**

IFNγ challenge。

因为它有机会把 immune 从“相关”提升到“functional phenotype”。

**不值得继续投入新实验：**

Placenta。

---

这样全文最后的 model 也应该有证据等级：

**实线：**

TWEAK
→ TWEAKR
→ YAP/TEAD
→ oncofetal/revival cell-state remodeling

**有实验再实线，否则虚线：**

TWEAK+ macrophage
→ TWEAK

**虚线 / shaded associations：**

OnF → treatment persistence
OnF → immune-modulatory phenotype
OnF ↔ placental developmental convergence

这会让 reviewer 很容易区分：

**what you discovered, what you proved, and what you propose.**

而不是看到一个非常漂亮但证据等级混在一起的模型。

最核心的取舍实际上只有一句话：**Macrophage值得补桥，Immune值得保留但降级，Placenta默认放弃承重。** 这会让你的项目明显更容易 close，同时不会牺牲真正的 novelty。
