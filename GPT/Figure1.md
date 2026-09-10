这个 Figure 1 的方向基本对，但现在还差一个最关键的问题：**你得先想清楚这张图到底要证明哪三件事**。不然 panel 会越堆越散。

我建议 Figure 1 只证明三件事，而且每个 panel 都服务于这三件事：

1. **CRC 里确实存在一个无偏发现的 oncofetal/revival-like epithelial state**
2. **这个 state 不是你拿已有 signature 硬打分打出来的假象，而是能被独立 fetal/revival signatures 交叉支持**
3. **这个 state 在 disease progression 中反复出现，并在 malignant / advanced context 中富集**

你刚才列的内容已经覆盖了 1 和 2，也碰到了 3，但**还缺一个非常重要的“recurrent / robust”证据层**：
如果没有“跨 cohort / 跨 patient 可重复出现”，那 reviewer 很容易说这是 integration artifact，或者是某个 study 特有的 technical program。

所以我先给你一句话总结：

## Figure 1 需要补的不是更多生物学，而是“重现性与非伪影性”的证据。

---

# 一、Figure 1 的主逻辑建议

我建议这张图按下面这个叙事顺序走：

### Part I. 先定义 state

不是先讲 disease，也不是先讲 signature，而是先回答：

**在 CRC epithelial compartment 里，数据驱动地有没有一个 oncofetal-like MP？**

### Part II. 再做外部注释

回答：

**这个 MP 为什么可以被叫做 oncofetal/revival-like，而不是 generic stress / EMT / YAP / low-proliferation program？**

### Part III. 最后讲 disease context

回答：

**这个 state 在哪些病理 context 中出现和扩张？**

这样 Figure 1 就会非常干净。

---

# 二、我建议的主图 Panel 排序

我会建议做成 **7 个主 panel**，最多 8 个。
再多就会太挤，很多 atlas 描述应扔到 supplement。

---

## **Figure 1. A recurrent oncofetal/revival-like epithelial state is present across colorectal cancer**

---

## **Panel A. Study design / CRC atlas overview（简洁版）**

**目的**：给读者一个最小必要背景，说明你不是分析一个小数据集，而是一个跨 cohort 的 CRC epithelial atlas。

### 内容

* 一个简洁 schematic
* 数据来源：多少 studies、多少 patients、多少 samples、多少 epithelial cells
* 包含哪些 major disease contexts：normal, adenoma/FAP, primary tumor, metastasis
* 只保留最关键数字，不要塞太多 metadata

### 为什么要放

因为后面所有 “recurrent” 的 claim 都要靠这个 panel 托底。

### 注意

你发来的 atlas 大图里很多信息太细，主图不需要全搬。
比如 stage、ethnicity、sex、study composition 这些大部分放 supplement。

### 建议

这个 panel 要**比你发来的图更简化**，只保留：

* integrated CRC atlas
* epithelial-focused analysis
* disease contexts covered

---

## **Panel B. Epithelial lineage landscape**

**目的**：展示你后面所有分析都聚焦在 epithelial compartment，并且内部确实存在多个 transcriptional states。

### 内容

* epithelial-only UMAP
* 颜色按 normal / premalignant / malignant，或者按 major epithelial states
* 最好标出：

  * normal epithelial
  * differentiated-like
  * proliferative CSC-like
  * oncofetal-like

### 为什么要放

这一步是“state discovery”的舞台搭建。

### 注意

这里不要一开始就过多讲 TWEAKR。
Figure 1 的主角应当是 **state**，不是 receptor。

---

## **Panel C. Unbiased NMF/meta-program discovery identifies an oncofetal-like program**

**目的**：这是整张图最核心的 panel。

### 内容

推荐做成两部分组合：

1. **Meta-program heatmap / loading heatmap**

   * 展示所有主要 epithelial MPs
   * 明确有一个 MP 与已知 oncofetal/revival biology一致
2. **该 MP 的 top-weight genes**

   * 比如 top 20 或 top 30 genes
   * 其中可出现 CLU, TACSTD2, ANXA1, SOX9 等
   * 如果 TNFRSF12A/TWEAKR 确实稳定排在前列，可以出现，但**不要把这个 panel 的重心写成“TWEAKR is the top gene”**

### 为什么

因为这一步要证明：

> 这是无偏发现出来的程序，而不是你先拿 signature 去打分。

### 非常重要的提醒

你说“TWEAKR 是这个 MP 权重最大的基因”，我建议你非常谨慎。

原因有两个：

1. **如果这点不够稳，后面 reviewer 会抓住不放**
   尤其 NMF 对 rank、subset、normalization、cohort composition 都敏感。
2. **Figure 1 不宜过早把一个候选 receptor 变成主角**
   否则会让人觉得 state discovery 为 mechanism 铺垫得太刻意。

### 更稳的写法

不是：

* “TNFRSF12A is the top weighted gene”

而是：

* “TNFRSF12A is among the highest-weighted genes within the oncofetal-like meta-program”

如果你后面 Figure 2 再专门提 receptor，会更自然。

---

## **Panel D. Projection of the oncofetal MP onto the epithelial landscape**

**目的**：把 NMF 抽象 program 投影回单细胞空间，证明它对应的是一个真实的 cell state 区域，而不是热图里的数学向量。

### 内容

* 同一个 epithelial UMAP
* 连续色显示 oncofetal MP score
* 旁边可以并列放一个 proCSC / proliferative MP score UMAP

### 为什么要放

这能非常直观地说明：

* oncofetal-like cells 是一个可定位的细胞群/状态
* 它和 proliferative CSC 不是完全重合
* 不是简单的 cell-cycle high or low

### 这一步很重要

因为你不能只说“有一个 MP”，你必须让它看起来像一个 **state**。

---

## **Panel E. Independent fetal/revival signatures nominate the same state**

**目的**：这是“交叉验证 panel”，非常关键。

### 内容

我建议做成一个 **signature-by-state heatmap** 或者 **enrichment matrix**：

行：

* fetal intestine signature
* revival stem cell signature
* regenerative/YAP program
* published oncofetal/revCSC signatures
* proliferative CSC signature
* differentiation signature

列：

* normal epithelial
* differentiated tumor
* proCSC
* oncofetal MP-high state

或者列用 epithelial MPs。

### 你要展示的核心

* 你的 oncofetal MP-high state
  **同时**富集 fetal / revival / regenerative / published oncofetal signatures
* 而 proCSC state 富集 proliferative stemness / cell-cycle / WNT-related programs
* 两者分离

### 为什么要放

这一步回答 reviewer 最常见的问题：

> 你说这是 oncofetal/revival-like，凭什么？

### 进一步建议

如果图能放下，我还建议加一个小 panel：

* oncofetal MP score vs published oncofetal signature score 的 cell-level / sample-level concordance

这会让“同一 state 被不同定义反复捕获”更加清楚。

---

## **Panel F. Recurrent across patients and cohorts**

**目的**：这是我认为你目前方案里最缺、但非常该补的 panel。

### 内容

推荐任选一种，最好两种合并：

#### 方案 1：patient-level dot plot

* 每个 patient 一个点
* x 轴：study / disease category
* y 轴：oncofetal MP-high cells fraction，或该 patient 是否检测到该 MP

#### 方案 2：cohort recurrence heatmap

* 行：study
* 列：patients or samples
* 标记：是否存在 oncofetal MP-high state，或 state abundance

#### 方案 3：leave-one-study-out robustness

* 每个 study 单独重建 / mapping
* 看 oncofetal MP 是否仍能被 recover

### 为什么必须补

因为 Figure title 里有 **“recurrent”** 这个词。
如果你没有 patient-level recurrence 证据，这个词其实站不住。

### 这一 panel 的价值非常高

它比再做一个花哨 UMAP 更有说服力。

---

## **Panel G. Disease context: normal → adenoma/FAP → primary → metastasis**

**目的**：把 biological relevance 放到最后收束。

### 内容

推荐做成两层：

1. **state abundance**

   * x 轴：normal / adenoma/FAP / primary / metastasis
   * y 轴：oncofetal MP-high cell fraction
2. **score-level validation**

   * x 轴同上
   * y 轴：published oncofetal signature score / revival score

最好 patient-level aggregation，不要纯 cell-level p-value。

### 你真正要说的话

* oncofetal-like state 在 premalignant / malignant progression 中出现
* 在 metastasis 中更高
* 和传统 signature 捕获结果一致

### 注意

这里不要追求把所有结论一次讲完。
Figure 1 只要把 **progression enrichment** 讲清楚就够了。
survival、drug response、ICI 都放后面，不要在 Figure 1 里抢戏。

---

# 三、如果还有空间，我只会再加一个小 panel，不会再多

## **可选 Panel H. Core marker expression panel**

如果你觉得 Figure 1 还差一点“分子直观性”，可以加一个很小的 marker panel：

* violin / dot plot / mini heatmap
* 展示：

  * oncofetal markers：CLU, TACSTD2, ANXA1, SOX9…
  * proliferative markers：MKI67, TOP2A, LGR5…
  * differentiation markers

### 用处

帮助读者快速建立对两个 state 的直觉。

### 但这不是必须

如果版面紧，完全可以放 supplement。

---

# 四、Figure 1 目前还缺什么？

你刚才问“还差什么”，我直接给结论：

## 最缺的有三样

### 1）**Recurrent / robustness**

这是最大缺口。
没有这个，就不像 atlas discovery 图，更像某个 dataset 的漂亮例子。

---

### 2）**证明它是一个独立 state，而不是 confounded program**

你现在已经有 proCSC 对照，这是对的。
但还要进一步避免 reviewer 说它只是：

* low proliferation
* stress response
* EMT-like
* YAP-only
* dissociation artifact

所以最好在 supplement 里补一些负面对照：

* cell cycle score
* EMT score
* hypoxia / stress score
* dissociation signature

证明 oncofetal MP 不等于这些。

---

### 3）**Patient-level summary**

Figure 1 里很多统计不要只停留在 cell level。
尤其 disease progression，那样很容易虚高显著性。

你最好统一成：

* sample-level
* patient-level
* study-level

三层里至少有一层是 patient-level。

---

# 五、哪些东西不要进 Figure 1 主图

这个也很重要。Figure 1 很容易过载。

## 不建议进入主图的内容：

### 1. TWEAKR 机制

你自己也说了不进入机制，那就不要让 TNFRSF12A 抢戏。
最多作为 oncofetal MP top gene 之一轻轻出现。

### 2. Immune

不要在 Figure 1 里讨论 immune niche。
这属于 Figure 2 以后。

### 3. Spatial

Figure 1 可以不放 spatial。
如果特别想放，也最多是很轻的“later we investigate niche organization”。
否则图会散。

### 4. Pan-cancer oncofetal

完全同意放 supplement。
主文第一张图一定要先把 CRC 讲透。

### 5. Clinical drug response

不要进 Figure 1。
那是后面的 disease-pressure / clinical-outcome section。

---

# 六、我建议的主图结构，最终版

如果让我替你定稿，我会这样排：

## **Main Figure 1**

**A.** CRC atlas overview and epithelial-focused analysis schema
**B.** Epithelial landscape identifies major normal, premalignant, and malignant states
**C.** Unbiased NMF/meta-program discovery identifies an oncofetal/revival-like epithelial program
**D.** Oncofetal MP and proliferative MP projected onto the epithelial landscape
**E.** Independent fetal/revival/regenerative signatures nominate the same state
**F.** The oncofetal-like state recurs across patients and cohorts
**G.** The oncofetal-like state expands across disease progression and is enriched in metastasis

如果版面允许，再加：

**H.** Core marker expression distinguishing oncofetal-like and proliferative CSC states

---

# 七、Supplement 我建议这样分担

## **Supplementary Figure S1 — Atlas construction and metadata**

* full atlas UMAP
* study composition
* sample origin
* patient characteristics
* lineage annotation
* QC/integration details

你发来的那张 atlas 图，绝大多数内容应该去这里。

## **Supplementary Figure S2 — Robustness of the oncofetal MP**

* different NMF ranks
* leave-one-study-out
* per-study recovery
* per-patient recurrence
* top genes stability

## **Supplementary Figure S3 — Cross-validation and negative controls**

* concordance with published oncofetal/revCSC/fetal signatures
* distinction from cell cycle / EMT / hypoxia / dissociation

## **Supplementary Figure S4 — Pan-cancer extension**

* if you want it

---

# 八、一个更本质的建议：Figure 1 的标题和 claim 要再收紧一点

你现在的标题：

**A recurrent oncofetal/revival-like epithelial state is present across colorectal cancer**

这个没问题。
但你在写 panel 时，最好始终盯住这几个词：

* recurrent
* oncofetal/revival-like
* epithelial state
* across colorectal cancer

所以每个 panel 都要回答一个词：

* recurrent → Panel F
* oncofetal/revival-like → Panel E
* epithelial state → Panel B + D
* across colorectal cancer → Panel A + G

如果某个 panel 不能服务这些词，就说明它应该去 supplement。

---

# 九、最后一句直接判断

如果你问我“Figure 1 现在最大的短板是什么”，我的答案非常明确：

## 不是 atlas 描述不够，不是 marker 不够，也不是 disease context 不够。

## 而是你还没有把“这个 state 是跨 patient、跨 cohort、无偏且可复现的”打得足够硬。

这个一旦补上，Figure 1 就会从“描述性不错”升级成“真正站得住的发现图”。

如果你愿意，下一步我可以直接继续帮你做：

1. **把 Figure 1 的 panel 标题逐个写成 manuscript 风格小标题**
2. **给每个 panel 配一句结果段落 claim**
3. **进一步帮你设计 Figure 2：macrophage-associated niche，但仍然不进入机制**
