# After Fig. 1b: next CytoTRACE2 questions — ChatGPT consultation (2026-10-10, not executed)

- Conversation: TWEAKR-oncoFetal / "Fig.1b-CT2 plasticity" (same review thread).
- Status: consultation only. No scoring, no new analysis. A3a/A3b await user approval.
- Counts in the question are Atlas metadata sample-level counts; treatment types were not verified per paper.

## Question sent

【咨询，不执行】Fig.1b 已完成（结果获批、主图+ED 已出图、Results/Methods 草稿已写）。用户希望在执行前先请你判断：基于 CRC Atlas + CytoTRACE2（CT2），还有哪些**与本文主线直接相关、且能被现有数据回答**的更有价值的问题？以及具体怎么做。本轮只要方案，不会执行任何计算。

## 1. 本文主线（用于判断"直接相关"）
- Fig.1：CRC 中空间组织的 oncofetal CSC 状态（oncofetal signature；Atlas NMF meta-programs）
- Fig.2：巨噬细胞 TNFSF12（TWEAK）→ 上皮 TNFRSF12A（Fn14/TWEAKR）信号轴
- Fig.3：TWEAK–TWEAKR 的充分性/必要性与 YAP 依赖
- Fig.4：placenta-like immune-tolerance program
- Fig.5：免疫抑制、低抗原呈递的肿瘤生态
- Fig.6：巨噬细胞来源 TWEAK 的体内功能

## 2. 已有 CT2 结果（重要：覆盖范围）
- **CT2 目前只打分了 cohort v1**：13 研究、222 患者、361 个 treatment-naive 原发肿瘤样本、1,000,926 个细胞（L1 上皮/免疫/基质 + 冻结的 L2）。Atlas 其余样本**尚未打分**。
- 结果：Stromal 0.287 > Epithelial 0.131 > Immune 0.062（患者中位数）；E−I +0.073、E−S −0.162、S−I +0.244，13/13 方向一致；depth matching 使效应缩小 43–55%；raw score 下 depth-matched E−I 仅 +0.012（PI 跨 0）。Fibroblast 0.495 最高；高置信 malignant 上皮子集 0.138（76 患者/8 研究，MSS 富集；上皮 86.9% CNV Uncertain，MSI-H 仅 4.5% CNV-clear）。
- 平行工作（GSE254249，26 样本，28,645 Cancer 细胞，新 23 MP）：MP 连续评分与 CT2 的患者内 Spearman；M20/M10/M11 最高；signature 组趋势：proCSC +0.70，YAP-oncofetal −0.59，Nusse regeneration −0.48，placenta −0.42（无正式显著性，非动态 plasticity）。

## 3. Atlas 中尚未打分、可能可用的样本（样本级计数，来自 Atlas 元数据；治疗类型尚未逐篇核验）
| 样本类型 × 治疗 | 样本 / 患者 / 研究 | 细胞 |
|---|---|---|
| 原发肿瘤 naive（全部，含 v1 以外） | 515 / 359 / 29 | 1.24 M |
| 原发肿瘤 treated | 105 / 86 / 9 | 0.51 M |
| 癌旁正常 adjacent normal | 284 / ~250 / 19+ | 0.77 M |
| 健康正常（Chen 2021 Cell，TruDrop） | 90 / 59 / 1 | 75 k |
| 息肉 polyp（Chen 2021 94 例 + Zheng 3 例） | 116 / 97 / 2 | 107 k |
| 转移 metastasis（naive 35 / treated 135） | 175 / ~90 / 10 | 0.41 M |
| 淋巴结、血液 | — | — |

**患者内配对设计：**
- 正常 + 原发：227 患者 / 24 研究（Pelka 36、Lee 21、Chen 2024 20、Wu 2022 17、Joanito 16 …）
- 原发 + 转移：49 患者 / 7 研究（Wu 2022 18，但 CD45+ 富集，几乎无上皮；Liu 2024 13；Che 2021 6；Wang 2023 6 …）；正常+原发+转移：27 / 5
- 原发 治疗前 + 治疗后：56 患者 / 4 研究（Qin 2023 27、Chen 2024 20、Li 2023 8、Yang 1）。Chen 2024 / Li 2023 推测为 dMMR/MSI-H 新辅助 PD-1，Qin 2023 治疗类型未核验；Chen 2024 治疗前样本可能是活检。
- 治疗后转移：Tian 2023 Nat Med 27 患者（全部 treated，几乎全为上皮）
- 息肉 + 原发同一患者：仅 3（无法做患者内 adenoma→carcinoma）

## 4. 请回答
1. **问题优先级**：按与本文主线的相关性和可回答性，排出 3–5 个最值得做的 CT2 问题（含你认为比"正常→原发→转移"和"治疗前后"更有价值的问题，例如：上皮内部 CT2 与 oncofetal/proCSC/YAP 程序、TNFRSF12A 表达的关系；巨噬细胞 TNFSF12 生态位与邻近上皮 CT2；MSI/CMS 分层）。每个问题写出：可主张的结论上限、主图/ED/不做。
2. **正常→（息肉）→原发→转移**：比较对象应是哪一种细胞（全上皮？CNV 高置信 malignant vs 正常上皮 stem/TA 等匹配 L2？）；用患者内配对还是跨研究；如何处理 depth、平台、研究、CD45 富集、正常上皮的 stem/TA 构成差异；转移以肝转移为主且多为治疗后，如何避免把治疗和转移混在一起。
3. **治疗前后**：56 对配对患者能回答什么、不能回答什么；是否需要按治疗类型/疗效（缓解 vs 非缓解）分层；活检 vs 切除、残余肿瘤细胞选择偏倚、上皮细胞数过少时如何处理；如果只能作为探索性 ED，请明确。
4. **打分范围与前置条件**：需要把 CT2 扩展到哪些样本（全部 Atlas？只扩展配对设计？）；正常上皮/肿瘤上皮如何在不使用 CT2 输出的前提下注释；是否需要先冻结一个新的 contract（A3）——请列出 A3 必须写死的内容（终点、比较、统计模型、depth 规则、最低细胞数、停止规则、哪些是 primary/secondary）。
5. **不该做的事**：哪些问题看起来诱人但数据无法支持或会被审稿人质疑（例如把 CT2 当作 plasticity、跨研究直接比较转移 vs 原发等）。
6. 给出推荐的执行顺序和每步的 go/no-go 关卡。

## Reply (verbatim copy)

### Fig. 1B 之后：CytoTRACE2 的下一步分析策略

我的建议是：不要继续扩展一个泛化的 CRC developmental potential atlas。应该转向一个更有价值的问题——oncofetal reprogramming 与 developmental potential 究竟是什么关系，以及 TWEAK–TWEAKR 是否与这一关系相关。

目前的数据已经足以说明，CytoTRACE2 的跨谱系比较受到测序深度和细胞类型特征的明显影响。继续比较正常、肿瘤、转移中的所有细胞，未必能够为文章增加强证据。

反而，你提供的 GSE254249 初步结果值得优先追踪：

- proCSC 与 CT2 强正相关（ρ 约 +0.70）。
- YAP-oncofetal、Nusse regeneration、placenta-like programs 与 CT2 负相关（ρ 约 −0.59、−0.48、−0.42）。

这些相关性目前还不能外推到整个 CRC Atlas，也不是独立的 plasticity 测量。但它们提示一个重要的可能性：

Oncofetal reprogramming and predicted developmental potential may represent distinct dimensions of colorectal cancer cell-state plasticity.

这比简单证明 oncofetal cells 具有更高的 CytoTRACE2 score 更值得研究。

### 一、最值得做的五个问题

按与 manuscript 的直接相关性、现有数据的可回答性，以及预期论文价值排序：

| 优先级      | 科学问题                                                                  | 现有数据                               | 结论上限                                                                      | 建议位置                      |
| -------- | --------------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------- | ------------------------- |
| P1 — 最高  | Oncofetal/revCSC 与 proCSC 是否对应不同的 developmental potential？            | 已评分的 13 studies，加 GSE254249        | 不同 CSC transcriptional programs 与 predicted developmental potential 呈不同关联 | Fig. 1 主图候选               |
| P2 — 高   | TNFRSF12A–YAP–oncofetal 程序是否仅仅反映一般性 stemness？                         | 已评分 epithelial cells               | TWEAKR/oncofetal program 与 CT2 可区分，或其关联可以被 CT2 解释                         | Fig. 2 / ED               |
| P3 — 中高  | TWEAK-expressing macrophages 与 oncofetal epithelial states 是否在患者层面共现？ | 已评分的 epithelial 和 macrophage cells | 同一样本中 ligand-associated macrophage features 与 epithelial programs 相关      | Fig. 2 ED；若结合独立空间证据，可进入主图 |
| P4 — 中   | 治疗前后，CT2 与 revCSC/proCSC state balance 是否呈不同变化？                       | 尚未评分的最多 56 名潜在配对患者                 | 与治疗相关的 developmental-potential 或 cell-state composition changes           | Exploratory ED            |
| P5 — 低至中 | 正常、原发及转移上皮的 CT2 是否不同？                                                 | 扩展 Atlas，取决于可用配对                   | 各疾病阶段的 predicted developmental potential 差异                               | ED；不建议作为主图核心              |

此外，我建议把 Fig. 4–5 的 placenta-like immune-tolerance / antigen-presentation program 作为 P2 的一个下游分析层，而不是再单独启动一个大型 CT2 项目。它们是否与 CT2 独立相关，更适合作为解释 oncofetal program 的补充证据。

### 二、P1：最值得投入的分析

### 科学问题

Does oncofetal reprogramming reflect increased developmental potential, or a distinct transcriptional state?

传统 CSC 框架容易隐含这样一种假设：越 stem-like 的癌细胞，越未分化，越具有可塑性。

但你的数据初步提示，canonical/proCSC 与 fetal-revival/YAP-associated programs 可能不是同一条连续分化轴。

这实际上对应两个不同的概念：

Developmental potential

CT2 predicts where a transcriptome lies along a learned developmental-potential hierarchy.

Oncofetal state

A transcriptional program associated with fetal-like adaptation, injury responses and tumor cell-state remodeling.

二者不必正相关。即使出现负相关，也不能据此否定 oncofetal plasticity，因为 CT2 不是对状态转换能力的直接测量。

### 具体怎么做

第一层：在 13 个已评分 studies 中做 epithelial-only analysis。

不要仅使用 34,764 个 CNV-high malignant cells，因为这个群体存在严重 MSS/CNV 选择偏倚。

Primary analysis 使用原发肿瘤来源 L1 epithelial cells；F1-clean 和 high-confidence malignant subset 作为敏感性分析。

每个细胞计算冻结的 proCSC、revCSC、YAP-oncofetal、placenta-like 及 canonical intestinal stemness signatures，并保留原有 CT2 final score 与 raw model score。

第二层：每位患者内部计算相关性。

建议采用：

\\[ \rho\_{p,k}=\operatorname{Spearman}(CT2,\ Signature_k) \\]

其中 \\(p\\) 是患者，\\(k\\) 是 signature。

如果同一患者有多个样本，优先在每个样本内部计算，再以患者为单位汇总，避免样本组成差异制造相关性。

不要直接对一百万个细胞计算一个 Spearman P 值并作为主要推断。患者和研究才是独立性更合理的统计层级。

随后：

- 汇总患者层面的相关系数，展示分布与 study consistency。
- 对患者相关系数进行 Fisher z 转换，并采用 study-aware random-effects meta-analysis。
- 检查控制 detected genes、UMI depth 和 cell-cycle scores 后的关联。
- 用 CT2 raw model score 和 depth-matched results 检查排序是否稳健。

第三层：在患者内部比较 oncofetal-high 与 proCSC-high 细胞群。

这里不能先用 CT2 划分细胞，再证明 CT2 有差异。

可以预先按独立的 signature score 定义状态；对每位患者中细胞数足够的两种状态计算 CT2 median difference。对于两种程序均较高的细胞，应允许 overlapping 或 intermediate 状态，不要强制二分类。

更推荐展示连续关系：CT2 与两种 signature 的二维密度分布，或者按患者计算的相关系数森林图。

第四层：独立验证。

GSE254249 已经提供了先验线索，应明确作为探索性数据。其余未参与形成该假设的 CRC studies 更适合承担验证角色。

这一点很重要：我们已经知道了部分相关性的方向，不能把全部后续分析包装成完全没有方向假设的预注册发现。

### 可以主张什么？

如果结果稳健，最强的合理表述是：

> Canonical stem-like and oncofetal transcriptional programs exhibit distinct relationships with predicted developmental potential in CRC epithelial cells.

如果两个程序的关联方向在多数独立队列中相反，才进一步考虑：

> Oncofetal reprogramming is not uniformly accompanied by increased predicted developmental potential.

不要写成 oncofetal cells are less plastic，因为负 CT2 相关性并不等于低动态可塑性。

这项分析优先级最高，而且不需要先扩展 Atlas 的 CT2 打分。

### 三、P2–P3：把 CT2 真正连接到 TWEAK–TWEAKR 主线

### P2：TWEAKR/YAP 是否是独立于一般 stemness 的肿瘤状态轴？

我认为这个问题比再比较正常与癌组织的整体 CT2 更有价值。

可在现有 222 名患者的 epithelial cells 内检验：

1. TNFRSF12A 表达或检出率与 CT2 的患者内关系。
2. TNFRSF12A 与 revCSC、YAP-oncofetal、proCSC 的关系。
3. YAP/oncofetal program 与 CT2 的关系在控制 proCSC、细胞周期、基因检出数及 study 后是否依然存在。
4. Placenta-like / immune-tolerance transcriptional program 是否更接近 oncofetal axis，而不是简单地随 CT2 上升。

这里最有价值的是区分两种模型。

模型 A：generic stemness model。 TWEAKR-high 细胞只是 CT2-high、proCSC-high 的普通干细胞样细胞。

模型 B：distinct adaptive-state model。 TWEAKR-high 细胞具有 fetal-revival/YAP/placenta-like 特征，但不一定具有更高的 CT2 developmental potential。

模型 B 会更自然地连接你后面的 Fig. 3–5。但必须允许数据支持模型 A，不能预先把 B 当成结论。

建议以患者内关联及患者间重复性为主要统计证据。由于 signature 与 CT2 都来自同一份 RNA 表达矩阵，它们的相关性并非正交生物学验证；如果部分基因在模型特征与 signature 之间重叠，也必须承认。

### P3：TWEAK-positive macrophage ecosystem

这一项建议优先使用原有 naive primary cohort，不扩展 CT2。

具体分析单位为患者或样本：

| Predictor（macrophage compartment）         | Outcome（epithelial compartment）         |
| ----------------------------------------- | --------------------------------------- |
| TNFSF12-expressing macrophage fraction    | revCSC / oncofetal signature            |
| Macrophage TNFSF12 pseudobulk expression  | epithelial TNFRSF12A expression         |
| TWEAK-associated macrophage program       | epithelial oncofetal score、CT2 和 proCSC |
| Macrophage abundance / inflammatory state | 用于检验是否存在组成及炎症混杂                         |

需要先核查 TNFSF12 的实际检出率。如果过于稀疏，应以 pseudobulk 或预先固定的 macrophage program 为分析单位，不能将单个 dropout 当成真实 TNFSF12-negative cells。

模型需控制 study、测序深度、macrophage cell recovery、患者免疫组成，必要时进一步控制 MSI status。

这里可以获得 sample-level co-occurrence，但不能获得真实的 spatial proximity。

因此：

- 单细胞 Atlas 只能支持生态组成的相关性。
- VISIUM HD、Xenium 或其他真实空间数据才能检验邻近与空间富集。
- 只有在空间层面存在独立支持时，才值得将这项分析进一步提升为 Fig. 2 主图。

不要把共同出现在一个 patient sample 中的 ligand 和 receptor，写成 direct macrophage–tumor interaction。

### 四、正常 → 息肉 → 原发 → 转移：如何避免把分析做成混杂因素比较

我的判断是：值得保留为探索性问题，但不值得现在启动全 Atlas 重打分。

最重要的是，不应直接比较四个阶段的全部细胞，也不应将其表述为一条已经观测到的演化轨迹。

### 1. 应该比较哪些细胞？

| 比较                                | 推荐对象                                        | 不推荐对象                                                    |
| --------------------------------- | ------------------------------------------- | -------------------------------------------------------- |
| Adjacent normal vs primary CRC    | 同一患者的正常上皮 vs tumor-derived epithelial cells | 把正常所有上皮与 CNV-high malignant subset 直接视为等价                |
| Healthy normal vs adjacent normal | 同一类明确注释的正常上皮 subtype；跨研究探索                  | 未校正细胞组成的全上皮比较                                            |
| Polyp vs primary CRC              | 同一研究、尽可能相似的 epithelial states               | 将两个不同研究的细胞直接拼成 adenoma→carcinoma trajectory              |
| Primary vs metastasis             | 同患者、同治疗背景、同为 tumor-derived epithelium       | 把正常肝细胞、肝间质与原发 CRC 肿瘤上皮混合                                 |
| Normal stem/TA vs tumor states    | 以独立 marker/program 定义的上皮状态作为分层比较            | 假设 normal stem/TA 与 malignant stem-like cells 是完全相同的细胞类型 |

特别需要澄清：

Tumor-derived epithelial 不等于经过严格证明的 malignant epithelial。

鉴于已冻结的 CNV 规则只能识别约 13% 的高置信恶性上皮，新的跨疾病阶段分析应把来源组织和 malignancy confidence 作为两个独立字段。

主分析可以使用 tumor-derived epithelium，但不能将所有来自肿瘤样本的上皮细胞直接称为 malignant cells。

对于正常上皮，应该重新建立不依赖 CT2 的 differentiation annotation，例如 canonical stem、TA/cycling、absorptive、goblet、enteroendocrine 等。这个 normal epithelial reference 不能直接套用此前 primary-tumor cohort 中实际上几乎为空的正常上皮 L2。

### 2. 优先使用配对患者，而非跨研究比较

你提供的数据中，有 227 名患者具有正常加原发样本，这是最有价值的扩展入口。

但 227 是 metadata 层面的潜在配对数量，不等于 227 名满足上皮细胞数量、样本质量和临床条件的有效分析对象。

建议先筛选 true paired patients，并区分 adjacent normal 与 healthy donor normal。前者可能存在 field effects，不能当成完全健康的肠上皮。

统计设计：

\\[ \Delta_p = \operatorname{median}(CT2\_{\mathrm{tumor},p})- \operatorname{median}(CT2\_{\mathrm{normal},p}) \\]

以患者为独立单位，每个研究计算 paired effect，再进行 random-effects meta-analysis。

同时报告一项 state-stratified comparison，例如正常 stem/TA 与特定 tumor epithelial programs 的分布，但只在两组细胞状态有明确可比性时解释。

全上皮比较反映的是两种组织的总体细胞组成加上细胞内部状态差异，不能单独解释为 dedifferentiation。

### 3. Depth、平台和样本组成

这是整个演化分析能否成立的主要限制。

CytoTRACE2 final score 包含样本内后处理，因此正常和肿瘤分别运行时，其参考细胞组成不同，会影响跨样本的连续分数。

我建议：

跨 normal/tumor/metastasis 的比较以 raw model score 作为主要稳健性锚点，final CT2 score 作为并列结果，而不能只使用 final score。

还需要实行与 A2.1 原理一致的 matched-cell depth control：在保留相同细胞的情况下，区分细胞选择效应与 UMI 下采样效应。新的 normal–tumor 配对应该使用事先固定的 study-或 pair-specific depth target，不能直接套用原来 13-study 三大 compartment 的阈值。

此外，必须在研究内比较后再合并。不同平台和不同 sample processing 的影响，不能依靠一个简单的 global batch correction 全部消除。

### 4. 转移样本：目前证据明显弱于正常–原发配对

你的 metadata 提示有 49 名原发加转移配对患者，但 Wu 2022 的 18 名患者以 CD45+ 富集为主，可能难以进行 epithelial comparison。

剩余配对中，真正拥有足量肿瘤上皮细胞、明确器官来源和治疗信息的人数必须重新核实。

尤其要区分：

- Treatment-naive primary vs treatment-naive metastasis。
- Treated primary vs treated metastasis。
- Untreated primary vs post-treatment metastasis。

第三种比较同时包含转移过程和治疗选择，不能将差异归因于 metastasis。

转移位置也应分层，至少把 liver metastasis 与其他器官区分开。

对这部分，我不建议现在承诺完成 normal→polyp→primary→metastasis 的 CT2 progression figure。

Polyp 数据只有两个研究、同患者 polyp–primary 配对仅 3 人；它只能支持有限的横断面比较，不能支持患者内演化推断。

如果正常–原发数据质量很好，可以先完成这一段。转移和息肉是否加入，根据前置 metadata gate 决定。

### 五、治疗前后：56 名潜在配对患者能回答什么？

这部分与 Fig. 1、Fig. 4、Fig. 5 的 therapeutic persistence 主线有关，因此科学价值高于一般性的跨阶段 CT2 图。

但我仍建议将其定位为 exploratory Extended Data，除非治疗注释、有效配对数量和独立队列一致性均达到较高标准。

### 推荐分析

先建立四个 study 的 patient × timepoint × therapy manifest。

尤其需要逐篇验证 Qin 2023、Chen 2024 和 Li 2023 的治疗类型、采样时间、取材部位、pre/post 定义和 response annotation。目前不能根据 cohort 名称将全部样本归为 ICI-treated。

主要读出建议分开两层：

| 层面                          | 分析对象                                                              | 可以回答                                                     |
| --------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------- |
| CT2 developmental potential | 每位患者治疗前后 tumor-derived epithelial cells 的 median raw/final CT2    | 治疗后残余肿瘤上皮的 predicted developmental potential 是否不同        |
| CSC state composition       | revCSC-high、proCSC-high 或 oncofetal-high 细胞比例及连续 signature scores | 治疗前后观察到的 CSC-associated transcriptional composition 是否改变 |

第二层其实与你已有的 ICI paired proCSC 下降、revCSC 相对稳定的观察更直接相关。

如果能够将这两层整合，会比单独比较 CT2 before/after 更有信息量：例如治疗后 proCSC score 下降，但 CT2 和 revival program 并不以相同方式变化。

不过，这不能证明 proCSC cells 转变成 revCSC cells。

### 必须处理的四类混杂

治疗类型。 ICI、化疗、放化疗或联合治疗必须分别分析，不能将 56 对一概合并。治疗类型不明确的患者不能进入 therapy-specific analysis。

疗效。 Responder/non-responder 只有在有明确的临床或病理疗效注释、且每组有足够患者时才能分层。不要依据治疗后剩余癌细胞多少反向定义 response。

取材差异。 Pre-treatment biopsy 与 post-treatment resection 的测序深度、细胞回收以及肿瘤区域取样均可能不同，需要在模型和结果解释中注明。

残余细胞选择。 治疗后能够被测序的细胞是存活并被取样的细胞，不是治疗前所有细胞的随机样本。治疗前后 CT2 分数的改变，不能直接视为同一细胞发生了状态转换。

具体统计上，先计算每位患者的 paired Δ，然后在治疗类型内汇总。如果同一治疗类型只有一个独立研究，应只报告该研究的估计和置信区间，不作 pan-CRC treatment effect 的主张。

对于 post-treatment epithelial cell yield 特别低的患者，按照冻结的最低细胞数标准排除并报告，不进行细胞层面补齐或伪配对。

结论：治疗前后值得做，但重点应是 CT2 与 proCSC/revCSC response 的关系，而非证明治疗导致细胞去分化。

### 六、CT2 扩展范围：不建议全 Atlas 重算

现在已评分的 222 名患者，足以完成优先级最高的 P1–P3。

其余 Atlas 的 CT2 计算，应当遵循 question-driven expansion，而不是先把所有样本打分，再寻找值得解释的差异。

| 数据范围                                | 是否需要新增 CT2     | 决定                    |
| ----------------------------------- | -------------- | --------------------- |
| 现有 13-study naive primary cohort    | 不需要            | 立即可做 P1–P3            |
| GSE254249                           | 已有 CT2         | 作为既有探索结果，继续用于技术和生物学对照 |
| Normal + primary paired samples     | 仅缺失 CT2 的合格样本  | 条件性 GO                |
| Pre/post-treatment paired samples   | 仅治疗和时间点明确的有效配对 | 条件性 GO                |
| Primary + metastasis paired samples | 先筛选上皮细胞覆盖      | 暂缓                    |
| Polyp samples                       | 不优先            | 暂缓                    |
| Healthy normal、血液、淋巴结及其余 Atlas      | 暂无直接需求         | 不做                    |

你有 1.24 million cells 的全部 naive primary tumor 数据，但 Fig. 1B 已经通过明确筛选得到 13-study cohort。不要仅为了增加患者数就放弃原先的数据选择标准。

如果 P1 在 13 个 studies 内重复性很好，再考虑选择若干独立 naive-primary studies 进行外部验证即可。

### 七、A3 contract：需要，但应当非常简短

我建议冻结 A3，而且在新分析计算之前冻结。

不需要再次编写 A2.1 那种大型技术合同。CT2 算法本身已经完成技术验证；A3 应专门规定新的 biological questions、数据选择、统计检验及 claim ceiling。

为了避免无限扩展，我建议将它拆成两个相互独立的工作包：

A3a：已评分 naive primary cohort 的 epithelial/program analysis。 覆盖 P1–P3，不需要新增 CT2。

A3b：paired normal/tumor 和 treatment analysis。 只有 metadata gate 通过才启动；不强制一定执行。

### A3 必须冻结的内容

| 项目                   | 推荐预设                                                                                                                        |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Scientific endpoints | P1：CT2 与 proCSC、revCSC、YAP-oncofetal 的患者内关联；P2：TWEAKR/YAP 与 CT2 的关联；P3：TWEAK macrophage–epithelial sample-level association |
| Primary cohort       | 已冻结的 13 studies、222 patients；以 tumor-derived L1 epithelial 为主要研究对象                                                          |
| Annotation           | 沿用 `annotation_v1`；状态由已冻结 gene signatures 独立定义，不依据 CT2 调整                                                                   |
| Primary CT2 metric   | A3a 维持 whole-sample final score；raw model score 为必需敏感性分析                                                                    |
| Cross-condition CT2  | A3b 并列报告 raw model 与 final score，避免仅依据 composition-dependent final score 得出结论                                               |
| Statistical unit     | 患者；患者内细胞相关性先汇总到 patient，再采用 study-aware inference                                                                           |
| Minimum cell count   | A3a 每样本建议 ≥100 epithelial cells 用于稳定相关性；配对阶段比较每组至少 30 个目标上皮细胞                                                               |
| Study eligibility    | 跨研究合并推断原则上需 ≥3 independent studies，每项研究 ≥5 eligible patients；不足则为 cohort-specific exploratory evidence                      |
| Depth sensitivity    | 原始 counts、raw model score、matched-cell UMI downsampling；depth target 在看新 CT2 结果前固定                                          |
| Clinical covariates  | Study、platform、patient、MSI/MMR、therapy type、sample site、biopsy/resection、UMI/gene complexity、cycling                        |
| Multiple testing     | 为 P1 的有限核心 signatures 单独定义检验 family；预先采用 BH-FDR，不再事后选择显著 gene sets                                                          |
| Stopping rules       | 样本注释不足、上皮细胞过少、患者配对无法验证或跨研究覆盖不足时停止升级为 pooled inference                                                                       |
| Claim ceiling        | Association with predicted developmental potential；不主张 lineage transition、causal reprogramming 或真实 spatial interaction      |

还需要一个小但重要的记录：A3a 的方向假设并非完全未知。 GSE254249 的 proCSC/CT2 正相关和 YAP-oncofetal/CT2 负相关已经被观察到。A3 应标明其为 prior exploratory observations，并用未参与这些观察的研究检验重复性。

对于 MSI/CMS，我建议它们作为预设的 effect-modifier 或 confounder analysis，而不是另立一个独立的主要问题。

MSI/MMR 状态可以优先使用已有的患者临床标签。CMS 如果需要重新预测，必须先固定分类器、适用样本和分类不确定性的处理；不能把不完全等价的 CIT/CMS 标签直接合并。

### 八、明确不建议做的分析

这里有几条边界，建议从一开始就写入 A3 的 exclusion 或 interpretation rules。

1\. 不将 CT2 高分称为高 plasticity。 它预测 developmental potential，不直接测量状态切换的能力或频率。

2\. 不把 Fibroblast CT2 最高解释成 TME 是癌症可塑性的主要来源。 这种跨谱系排序可能受发育参考体系、转录组复杂度和 ECM-related genes 影响。

3\. 不使用 CNV-high malignant subset 代表整个 CRC epithelium。 目前这一群体只覆盖 76 名 eligible patients 和 8 个 studies，而且 MSS 富集。

4\. 不从正常→息肉→原发→转移的横断面数据推断连续 lineage trajectory。 四个阶段并非同一批细胞的时间序列。

5\. 不把治疗后 revCSC-high 细胞增多等同于 proCSC→revCSC 转换。 它可能是细胞选择、差异存活或取样效应。

6\. 不把 TNFSF12 和 TNFRSF12A 在同一个 sample 内表达等同于 spatial niche。 Atlas 只能提供共同出现和统计关联。

7\. 不直接对低基因覆盖度的 Xenium panel 运行 CT2 并与完整 scRNA-seq 分数比较。 CT2 对输入特征覆盖有明确要求；需要空间关联时应使用经过独立验证的 signature transfer 或已评分的 scRNA reference。

8\. 不依据 CT2 结果重新筛选 proCSC/revCSC signatures。 这会导致以 CT2 构造预测变量，再使用 CT2 验证它们的循环论证。

### 九、推荐执行顺序与 GO/NO-GO

Stage 0 — 冻结 A3a

先固定 signature versions、统计方法、患者细胞数标准及多重检验 family。

GO：数据与基因集可溯源，分析对象明确；否则只修复 metadata，不启动 CT2 扩展。

Stage 1 — P1：CT2 × CSC transcriptional programs

使用现有 13 studies。先患者内相关，再 study-level replication，最后 depth/raw-score sensitivity。

GO：至少 3 个独立研究具备可评估患者，且效应在多数研究和关键敏感性分析中方向稳定；否则作为探索性 ED 或阴性结果报告，不提升为主图。

Stage 2 — P2/P3：TWEAKR–YAP and macrophage association

先核查 TNFRSF12A/TNFSF12 的基因覆盖、检测率、患者与 study coverage，再进行预定义关联模型。

GO：具有足够的受体与配体测量信息，并能控制主要组成混杂；否则不强行进行 cell–cell communication inference。

Stage 3 — A3b metadata gate

核查 227 个潜在 normal–primary pairs、56 个潜在 pre/post pairs、49 个潜在 primary–metastasis pairs。

GO：确认真实配对、治疗状态、组织部位及两侧足量 epithelial cells。否则停止对应分支，不提交 CT2 作业。

Stage 4 — 仅为合格配对补充 CT2

保持 CytoTRACE2 1.1.0、whole-sample processing、原始 raw count input 及预设 depth controls，不重跑原有 13-study cohort。

GO：主要结果具有可解释的配对效应和研究间重复性；否则保留 ED，不加入 Fig. 1 主叙事。

这里的 GO/NO-GO 不是按 P 值是否显著选择保留数据。所有符合纳入标准的研究都应报告；GO 指是否具备足够的技术和生物学证据，将其升级为跨队列结论或主图。

### 最终建议

我的优先顺序是：

P1 oncofetal/proCSC–CT2 relationship → P2 TWEAKR/YAP–CT2 relationship → P3 macrophage TWEAK ecosystem → 有条件执行 P4 therapy pairs → 最后考虑 P5 normal/progression。

其中 P1 是最有机会改变论文叙事的一项。

你现在的论文核心假设是 oncofetal plasticity 与肿瘤适应和免疫生态相关。但如果 oncofetal signature 与 CytoTRACE2 developmental potential 呈负相关，而 canonical stemness 呈正相关，那么我们有机会说明：CRC 的 oncofetal adaptive program 不能被简单归结为 canonical stemness 或更原始的发育状态。

这是一个值得独立检验的、有明确生物学意义的结果，而且现有 CT2 输出已经足以启动。

本轮建议仅批准 A3a 的方案设计；A3b 不应自动启动。 先完成 P1–P3 的研究问题与统计定义，再根据 metadata feasibility 决定是否有必要投入新的 CT2 计算。