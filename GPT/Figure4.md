这一张 Figure 4 可以成为整篇文章真正的 causal anchor，但我会先纠正你一句：“这个假设基本是真的，已经无可辩驳了”现在还不能这么说。你真正接近钉死的是：

> TWEAK–TWEAKR controls the oncofetal/revival transcriptional state, and YAP/TEAD is a major downstream component.

而“macrophage-derived TWEAK drives this state”目前仍然主要是 Figure 3 的 source + spatial inference。两者要严格分开。

另外，“sufficient and necessary”也要拆开定义。TWEAK treatment 诱导 state，只证明 ligand sufficiency；TWEAKR KO 阻断 TWEAK response，证明 receptor dependence；只有 TWEAKR KO 在没有外源 TWEAK 时也使 endogenous oncofetal state collapse，才比较接近 receptor requirement。YAP inhibitor/KO phenocopy 加 active-YAP rescue，才真正把 YAP 放在 TWEAKR downstream。

所以 Figure 4 的任务最好不是“把所有 perturbation 塞进去”，而是建立一个明确的 pathway hierarchy：

> TWEAK → TWEAKR → YAP/TEAD → oncofetal/revival state

公开数据负责 orthogonal triangulation，你们自己的 matched perturbation 负责真正的因果主证据。

我建议 Figure 4 排成这样。

**Figure 4. TWEAK–TWEAKR activates a YAP-dependent oncofetal transcriptional program in CRC**

**4A. A public perturbation atlas converges on the TWEAKR–YAP–oncofetal axis**

这是你公共 perturbation 数据最适合出现的位置，但不要让它成为主角。

可以做一个 perturbation × program matrix：

* TWEAK treatment
* TNFRSF12A OE
* TNFRSF12A KO/KD
* YAP1 KO/KD
* TEAD perturbation
* TGFβ treatment
* 其他 regeneration-inducing perturbations

readout统一成：

* CRC-atlas-derived oncofetal MP
* published revCSC
* fetal intestine
* YAP/TEAD
* proCSC
* cell cycle

最漂亮的结果不是某一个 dataset 显著，而是方向一致：

TWEAK / TWEAKR OE / TGFβ → OnF ↑
TNFRSF12A KO / YAP / TEAD loss → OnF ↓

这张 panel 的 claim 应该是：

> Independent perturbation datasets converge on a TWEAKR–YAP-associated regulatory architecture of the oncofetal state.

不要用不同研究之间的效果大小去推 pathway order，因为 cell line、剂量、时间和平台完全不同。

---

**4B. Isogenic perturbation design in CRC organoids**

这是从“公共证据”正式进入你们实验。

理想矩阵：

Control
TWEAK
TWEAKR KO
TWEAKR KO + TWEAK
YAP inhibition / KO
TWEAK + YAP inhibition
如果能做，再加 active YAP rescue in TWEAKR KO。

不一定所有条件都必须同时做 RNA-seq。可以设计成：

核心四组做 RNA-seq；
YAP epistasis 做 focused molecular readout。

最好至少两个模型，哪怕：

一个 mouse Apc/Kras/p53 organoid
+
一个 human CRC model。

这样不是单模型现象。

---

**4C. TWEAK induces a receptor-dependent global transcriptional state transition**

这里放：

* PCA
* sample correlation
* DE gene counts
* trajectory / centroid shift

真正漂亮的 PCA 应该看到：

Control → TWEAK 一个方向
TWEAKR KO 向反方向
TWEAKR KO + TWEAK 不能走到 TWEAK 位置。

这比一上来只展示几个 marker 更能说明“state reprogramming”。

---

**4D. TWEAK–TWEAKR reciprocally controls the oncofetal/proCSC state axis**

这是 signature-level causal panel。

主 readout：

oncofetal MP
revCSC
fetal/regenerative
YAP/TEAD
proCSC
differentiation / cell cycle

如果结果理想：

TWEAK：
OnF ↑
revCSC ↑
YAP ↑
proCSC ↓

TWEAKR KO：
方向相反

KO + TWEAK：
无法恢复。

这里就可以很稳地写：

> TWEAK induces an oncofetal/revival-like transcriptional state in a TWEAKR-dependent manner.

这应该成为 Figure 4 的主结论之一。

---

**4E. Patient-derived oncofetal genes are induced by TWEAK and depleted by TWEAKR loss**

我认为这是整张 Figure 最重要的计算 panel。

因为如果只做 predefined signature，reviewer 永远可以说你选了一套符合预期的 genes。

这里直接使用 Figure 1 从患者 CRC 中无偏得到的 oncofetal MP。

做三种关系中的一种或两种：

patient OnF MP loading
vs
TWEAK treatment logFC

以及：

patient OnF MP loading
vs
TWEAKR KO logFC

理想结果：

high-loading OnF genes preferentially induced by TWEAK；
同一批 genes preferentially lost after TWEAKR KO。

甚至可以定义：

**TWEAK-induced ∩ TWEAKR-dependent core**

再看它是不是高度落在 patient-derived OnF MP。

这会完成非常漂亮的：

**human observational discovery → experimental perturbation → same transcriptional state**

这是这篇文章非常值钱的一环。

---

**4F. YAP/TEAD sits downstream of TWEAK–TWEAKR**

这张 panel 决定你最后到底能写：

“YAP-associated”

还是：

“YAP-dependent”。

我建议至少做到两个层次。

第一层：
TWEAK treatment
→ YAP nuclear localization ↑
→ p-YAP inhibitory state ↓ 或 compatible biochemical change
→ TEAD reporter ↑

第二层：
TWEAK + YAP inhibitor
→ OnF induction disappears。

这样已经可以相当有力地说：

> YAP/TEAD activity is required for TWEAK-induced oncofetal reprogramming.

如果再有：

TWEAKR KO + constitutively active YAP
→ OnF state rescued

那 pathway hierarchy 基本就锁死：

> TWEAKR acts upstream of YAP.

这会显著提升 Figure 4。

---

**4G. Mechanistic convergence with known fetal-regenerative signaling**

TGFβ 我不会单独拉成第二条故事，但它非常适合做 positive biological comparator。

原因是 TGFβ → YAP/SOX9 → fetal reprogramming 本来已有很强文献基础，而你现在发现的是另一个外源 niche signal 也可以汇入同一 regenerative state。

所以可以用一个小 panel 做：

TWEAK perturbation signature
vs
TGFβ-induced fetal reprogramming signature

或者公共 TGFβ RNA-seq 与你 TWEAK RNA-seq 的 concordance。

最后说：

> TWEAK engages a transcriptional program convergent with established fetal-regenerative signaling.

不要说 TWEAK 就是通过 TGFβ，也不要把 TGFβ 拉进你的 pathway。

---

至于 macrophage co-culture，我会把它的地位说得很清楚：

## 它不是 TWEAKR–YAP mechanism 必需的，但如果你的标题和 central claim 要保留 “macrophage-derived TWEAK”，它就没有你想象中那么 optional。

现在存在一个明显的不对称：

Figure 3 可以证明：

macrophages express TNFSF12
+
TNFSF12+ macrophages 靠近 OnF/TWEAKR-high tumour cells

Figure 4 可以证明：

exogenous TWEAK
→ TWEAKR
→ OnF/YAP

但是中间缺：

**真正的 macrophage 能不能产生足够的 TWEAK 去造成这个 phenotype？**

这是 reviewer 非常自然的一问。

所以有两个版本。

如果文章 central claim 改成：

> TWEAK–TWEAKR signaling regulates oncofetal plasticity

那么 macrophage co-culture 完全可以 optional / supplement。

但如果文章 central claim 保持：

> Macrophage-derived TWEAK drives TWEAKR-dependent oncofetal plasticity

我至少会做一个很小但干净的 macrophage experiment。

不需要搞成一个庞大 Aim。

最小闭环其实只要：

Organoid alone
Macrophage-conditioned medium
Macrophage-conditioned medium + anti-TWEAK
或者 Tnfsf12-KO macrophage CM

readout：

OnF score / SOX9 / TROP2
YAP nuclear localization / TEAD target

如果：

Macrophage CM → phenotype
anti-TWEAK or Tnfsf12 loss → phenotype significantly reduced

那么你已经非常高效地把“macrophage-derived”从计算推测升级成实验支持。

甚至 direct co-culture 都不是必须的。

**Conditioned medium + ligand-specific blockade** 对你的问题反而更干净，因为它直接测试 soluble factor。

---

所以我会把 macrophage experiment 从 Figure 4 主体里拿出去。

Figure 4 专心完成：

> **ligand → receptor → transcription factor → state**

然后有两个选择：

如果 macrophage experiment 很漂亮：
放 Figure 5 的第一小部分，或者 Figure 4 最后一个小 panel。

如果一般：
Supplement。

如果完全不做：
全文把 “macrophage-derived drives” 降级成 “macrophage-associated / macrophage-enriched source”。

---

最终 Figure 4 我会锁成六个核心 panel：

**4A** Independent perturbation datasets converge on TWEAKR/YAP regulation of the oncofetal state
**4B** Isogenic TWEAK–TWEAKR perturbation design
**4C** TWEAK induces a receptor-dependent global transcriptional transition
**4D** TWEAK and TWEAKR loss reciprocally regulate oncofetal/revival versus proliferative CSC programs
**4E** Patient-derived oncofetal MP genes are induced by TWEAK and depleted after TWEAKR loss
**4F** YAP/TEAD inhibition and rescue establish pathway hierarchy downstream of TWEAKR

可选：

**4G** TWEAK converges with established fetal-regenerative perturbations such as TGFβ

这张完成以后，文章的 mechanistic core 基本就真正站起来了。

而且有一个战略上很重要的原则：**不要因为你手里公共 perturbation 数据很多，就让 Figure 4 变成“perturbation encyclopedia”。**

Figure 4 只回答一个问题：

> **TNFSF12–TNFRSF12A 是否因果控制 Figure 1 定义的那个 state，以及 YAP 是否位于这条因果链中？**

任何不能帮助回答这个问题的 perturbation，即使结果再有意思，也扔 Supplement。

至此，你前四张图其实已经形成非常成熟的结构：

Fig. 1：发现 state。
Fig. 2：证明 clinical relevance / therapy persistence。
Fig. 3：从 population + spatial evidence 收敛出 TAM–TWEAK–TWEAKR hypothesis。
Fig. 4：用 perturbation 把 TWEAKR–YAP–OnF 因果链钉住。

这时候 Placenta、immune evasion 都已经不是“必须加”的东西了。它们只有在能让后面的功能图明显变强时才值得回来。
