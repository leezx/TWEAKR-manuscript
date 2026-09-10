我赞成把这一张提前到 Figure 2。Figure 1 定义“这个 state 真实存在且可重复”，Figure 2 立刻回答“为什么这个 state 值得研究”，然后 Figure 3 再进入 TWEAK/TAM niche，叙事会比把 clinical relevance 压到最后更自然。

但我会改一个核心定位：Figure 2 不是简单堆“OS、RFS、chemo、ICI 四类相关性”，而应该证明一个更统一的临床命题：

> **The oncofetal/TWEAKR-associated state marks poor-outcome CRC and preferentially persists under therapeutic pressure.**

这里其实包含两个不同的临床概念，必须分开：OS/RFS 是 prognostic；chemo/ICI 的 longitudinal data 是 treatment-associated state selection/persistence。只有“治疗前 score 能预测 responder vs non-responder”，而且最好能在独立 cohort 复现时，才开始接近 predictive biomarker。不能把 post-treatment enrichment 直接叫“predicts resistance”。

我建议 Figure 2 做成下面这个结构。

**Figure 2. The TWEAKR-associated oncofetal state marks clinically aggressive and treatment-persistent CRC**

**A. Clinical validation framework.** 很小的 schematic，明确 Figure 1 锁定的 frozen oncofetal MP / published revCSC signature，被投影到 independent bulk、single-cell 和 longitudinal treatment cohorts。这里的关键词是 **frozen**：Figure 2 不允许为了 survival 再挑基因、调阈值，否则就会产生 circularity。

**B. Oncofetal state predicts adverse survival across independent CRC cohorts.** 不要只给 TCGA 两张 KM。主结果最好是连续变量 Cox 的 forest plot：每个 cohort 一个 HR，OS / RFS 分开或者选更稳定的 endpoint。右边可以放一张代表性 KM 作可视化。这样 claim 是“cross-cohort prognostic consistency”，比单一 p-value 强得多。

**C. The association is not explained by established high-risk CRC features.** 这是你目前设计里真正缺的一块，而且比再多做一个 survival dataset 更重要。做 multivariable Cox，至少考虑有数据的 stage、MSI/MMR、CMS 或 stromal content。尤其要处理一个 reviewer 必问的问题：

> 你的 oncofetal score 是不是实际上就是 CMS4 / stromal-rich / advanced-stage surrogate？

如果调整以后 oncofetal score 仍然有 independent association，这张 Figure 的临床等级会高很多。如果不独立，也不要硬说 independent prognostic marker，而改成它“marks the clinically aggressive CMS4-like axis”。

**D. Chemotherapy produces a reproducible shift in CSC-state composition.** 这里不要简单写“chemotherapy induces oncofetal”。你最近的数据实际上更微妙，也可能更有意思：**proCSC下降，而 revCSC/oncofetal 相对保持，从而 state balance 向 revival-like side 偏移。**

这个应该用 matched patient-level longitudinal analysis：

PRE → POST
proCSC
revCSC
revCSC–proCSC balance

而不是靠 cell-level significance。

如果真实数据是 revCSC 没有绝对升高，就明确叫：

> **selective persistence / relative enrichment**

而不是 induction。

这反而和 revCSC 的“persister”概念非常吻合。

**E. The treatment-associated state shift is associated with clinical response.** 这是 Figure 2 非常值得补的一块。

如果有 responder/progressor annotation，问两个问题：

治疗前：
baseline oncofetal / balance 是否不同？

治疗后或 delta：
state shift 是否在 progressors 更明显？

这会把“前后变化”变成真正和病人 outcome 联系起来的分析。

其中 baseline prediction 是最值钱的。如果 pretreatment oncofetal score 在 progressor/non-responder 更高，你才开始得到：

> pretreatment oncofetal state is associated with subsequent treatment response.

但仍然暂时不要叫 validated predictive biomarker。

**F. ICI-treated CRC shows analogous enrichment or persistence of the oncofetal state.** 这里我建议把 ICI 当成“第二种治疗压力的外部验证”，而不是另起一条 immune mechanism。

你真正需要问的是：

> chemotherapy 和 ICI 这两种完全不同的治疗，是否都把 tumor ecosystem 推向/保留同一个 revival-like malignant state？

如果答案是 yes，这会形成非常漂亮的高阶 claim：

> **Distinct therapeutic pressures converge on a common oncofetal persistence state.**

这是比“ICI 后 revCSC 高一点”高级得多的结果。

但你之前 ICI patient-level n 很小、TWEAK macrophage delta 与 revCSC delta 的相关性不显著，因此这种相关性不要承担 Figure 2 核心结论。可以展示 paired state change；TWEAK–TAM coupling 若证据弱，留给后面的 niche figure 或 supplement。

**G. TNFRSF12A identifies the clinically adverse fraction of the oncofetal state.** 如果 Figure title 想真正叫 **TWEAKR–oncofetal state**，你还缺这一 panel。

否则整个 Figure 其实只是“oncofetal state clinically aggressive”，TNFRSF12A 只是标题里被偷偷带进来了。

这里可以测试几个层级，按优先级：

TNFRSF12A expression 与 oncofetal MP 在 independent cohorts 的关系；

oncofetal-high/TNFRSF12A-high 双高组是否具有最差 outcome；

continuous Cox 中 TNFRSF12A × oncofetal score interaction；

治疗后 retained oncofetal cells 是否 preferentially TNFRSF12A-high。

如果这些结果不稳定，那 Figure 2 标题就不要叫 TWEAKR–oncofetal state，而叫：

> **The oncofetal/revival-like state marks poor-outcome and treatment-persistent CRC**

然后 Figure 3 再正式 introduce TWEAKR。这个逻辑反而更干净。

---

关于你问的“需不需要做一个 Oncofetal 预后模型并给明确 gene signature”，我的答案是：

**需要一个明确、冻结、可复用的 signature；但我不建议现在做一个专门优化 survival 的 prognostic model。**

这是两个完全不同的东西。

你应该做的是：

Figure 1 通过无偏 NMF 定义一个 **consensus oncofetal MP signature**，比如选稳定的 high-loading genes，经过跨 cohort stability filtering 后冻结。Figure 2 开始之前，gene list 已经完全确定。

然后 Figure 2 用这个 frozen score 去问：

survival；
metastasis；
chemo；
ICI。

这样逻辑是：

> biology-defined signature → predicts clinical phenotype.

这是很强的。

而不是：

> 我从 survival dataset 里挑出最能预测 survival 的 12 个 genes → 再证明它预测 survival。

后者会迅速把论文带到 biomarker/model-building 方向，而且必须做 training/validation、feature selection、calibration、C-index、external validation，工作量大，还容易被 reviewer 认为 overfitting，与主机制故事没有多少帮助。

所以我建议最终存在三个并列但角色不同的 score：

**1. NMF-derived oncofetal MP**
你的 novel、data-driven state definition。

**2. Published revCSC/oncofetal signature**
external biological validation。

**3. proCSC signature**
biological counter-state / reference axis。

而不是再创造第四个“12-gene survival signature”。

甚至 Figure 2 很漂亮的一种做法是，每个重要 clinical analysis 同时画：

NMF-OnF
published revCSC
proCSC

如果前两个 consistently adverse，而 proCSC 没有或方向相反，那么 reviewer 很难说你只是 arbitrary signature engineering。

---

我认为 Figure 2 还应该补两类非常关键的严谨性分析。

第一是 **patient-level statistics**。尤其 chemo / ICI，绝对不能因为有几十万单细胞就得到极小 p-value。实验单位始终是 patient。matched 就 paired test / patient-level mixed model；多个样本属于同一病人，也必须处理 repeated measures。

第二是 **clinical independence / confounding**。这是临床 Figure 和普通生信 Figure 最大的区别。尤其 bulk survival 必须至少考虑：

stage；
MSI/MMR；
CMS / stromal score；
可能的话 age、sex。

因为 oncofetal/revCSC 与 mesenchymal/stromal-rich CRC 有天然联系。你必须知道它到底是：

独立信息，

还是已知 aggressive CRC phenotype 的 epithelial manifestation。

其实两种答案都能发表，但 claim 不一样。

---

这样 Figure 2 最终可以压缩成六到七个 panel：

**2A** Clinical cohort framework and frozen state signatures
**2B** Cross-cohort OS/RFS association
**2C** Multivariable / CMS-MSI-stage independence
**2D** Paired chemotherapy-associated CSC-state shift
**2E** Treatment response versus baseline/post-treatment state or state change
**2F** Independent ICI cohort shows analogous oncofetal persistence
**2G** TNFRSF12A preferentially marks the adverse/treatment-persistent oncofetal compartment

如果 2G 不成立，就删掉“TWEAKR”这个 Figure title，绝对不要为了后面的 mechanism 强塞。

---

这一张 Figure 真正最理想的收束不是：

> Oncofetal score correlates with survival, chemo and ICI.

而是：

> **A recurrent oncofetal/revival-like state identified without clinical supervision is associated with adverse outcome and is preferentially retained across distinct therapeutic pressures.**

然后 Figure 3 非常自然地问：

> **What maintains this clinically persistent state?**

再进入：

TWEAKR receptor nomination
→ TNFSF12 source
→ macrophage spatial niche。

这样你的整篇文章逻辑实际上开始变得很清楚：

**Fig. 1 — What is the state?**
无偏发现 + 外部验证 + disease evolution。

**Fig. 2 — Why does the state matter?**
poor outcome + chemotherapy/ICI persistence。

**Fig. 3 — What is associated with its microenvironmental maintenance?**
TWEAKR + TAM-derived TWEAK + spatial niche。

**Fig. 4 — Is the axis causal?**
public perturbation + TNFSF12 stimulation + TNFRSF12A KO/RNA-seq。

**Fig. 5 — Does it operate in vivo?**
xenograft scRNA / state remodeling。

这已经比原来“先讲完机制最后才告诉 reviewer 为什么临床上重要”的结构明显更强。
