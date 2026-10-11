# Fig. 1c 分析设计咨询（ChatGPT，新对话，2026-10-11）

- 对话：https://chatgpt.com/c/6acbaf02-1bc8-83ea-a533-5d9a9c06e138（"设计Fig 1c分析方案"）
- 提问原文：见 `Fig1c_design_prompt_20261011.md`
- 以下为 GPT 回复原文（页面文本复制；表格被展平）

---

Fig. 1c Analysis Contract v0.1

研究定位：Within-epithelium resolution of CRC stem-like states

总体建议：不要把 Fig. 1c 预先绑定在“两个 highly plastic CSC populations”这个结论上。应该把它设计成一个能够区分两类 stem-like configurations，并检验它们是否具有相同或不同 developmental potency characteristics 的分析。

原因是你已经发现了一个重要的生物学矛盾：

proCSC 与 CytoTRACE2（CT2）呈现较强正相关，而且在调整 transcriptomic complexity 后仍保留部分信号。

revCSC/oncofetal 程序与 CT2 的正相关，在复杂度调整后基本消失。

regeneration、YAP-oncofetal、placenta-related programs 甚至可能与 CT2 呈负相关。

这不只是一个统计学上的麻烦。它可能意味着：CRC 中的 canonical/proliferative stemness 与 revival/oncofetal reprogramming 并不处于同一条 differentiation-potency axis 上。

但目前同样不能据此认定存在两种功能上不同的 plasticity。CT2 结果只能说明它们的 predicted developmental potency characteristics 可能不同，不能直接说明两者的状态转换能力不同。

我建议 Fig. 1c 优先解决三个问题：

State identity： CRC tumor-derived epithelial cells 能否被可重复地解析为至少两种不同的 stem-like transcriptional configurations？

Potency stratification： 这两种 configurations 的 CT2-derived potency 是否均高于 differentiated-like epithelial states？它们之间是否存在稳定差异？

Patient-level reproducibility： 两种状态是否在同一患者肿瘤中共存，且观察结果并非由 sequencing depth、cell cycle、MSI status 或个别研究驱动？

这里必须明确区分三个层次：

概念

	

Fig. 1c 可以证明什么

	

不能直接证明什么




Stem-like transcriptional state

	

与已知 stem/progenitor programs 的表达相似性

	

Functional self-renewal




Predicted developmental potency

	

CT2/CCAT 等模型预测的 differentiation potential

	

实际 lineage potential




Cellular plasticity

	

可以提出由多个状态及相关程序支持的假设

	

真实的 reversible state transition、dedifferentiation 或 fate switching

最重要的 contract 原则：允许 Fig. 1c 得出 proCSC 高 potency、revCSC 低 potency 的结果，而且这个结果不应自动使 Figure 1 失败。 它可能比强行证明“两个高 CT2 populations”更有机制价值。

一、核心 claim：选择什么可检验假设？
1.1 推荐冻结的 primary claim

Primary hypothesis H1

Treatment-naive primary CRC epithelia harbor distinct, reproducible proliferative/canonical and revival–oncofetal stem-like transcriptional configurations, with potentially divergent predicted differentiation potency.

中文含义：

CRC 原发肿瘤上皮中存在至少两种可区分、跨患者可重复的 stem-like transcriptional configurations。这些状态不一定具有相同的 predicted differentiation potency。

这是一个可以被证伪、又不会预先假定 CT2 必须支持 revCSC 的命题。

进一步分成两个独立假设：

H1a — State distinctness： proCSC 与 revCSC 不是同一组细胞的不同 signature 命名，而是具有可重复的、非完全重叠的转录特征。

H1b — Potency association： 这两种状态与 differentiated-like epithelial cells 的 CT2 差异可能不同，检验方向及大小均应预先设定报告规则。

H1a 是状态存在性问题；H1b 是状态与 potency proxy 的关系问题。两者不能混为一谈。

1.2 “≥2 highly plastic stem-like states”的成立门槛

我不建议让 computational proxies 单独承担这个强 claim。可以将其拆分成三个 evidence tiers。

Evidence tier

	

必须达到的证据

	

允许使用的措辞




Tier 1：Distinct configurations

	

独立注释支持两种可区分状态，并具有跨患者／研究的复现性

	

Two distinct stem-like transcriptional configurations




Tier 2：Elevated predicted potency

	

两种状态相对 differentiated-like 细胞的 potency contrasts 均达到预设统计与稳健性标准

	

Two stem-like configurations with elevated predicted developmental potency




Tier 3：Functional plasticity

	

独立 lineage tracing、organoid state conversion、可追踪的 perturbation/recovery 等支持状态转换能力

	

Two functionally plastic stem-like states

Tier 2 不自动等于 Tier 3。

因此，Fig. 1c 最多可以通过单细胞转录组建立 Tier 1–2；真正的 plasticity 结论需要后续功能证据支持。

尤其要注意，Single-cell transcriptomes of the regenerating intestine reveal a revival stem cell 中的 CLU-positive revival stem cells 有 injury-induced、YAP1-dependent expansion 和 lineage regeneration 的实验支持，但这些证据不能直接转移为人 CRC 中 revCSC 的已验证功能。
Nature

1.3 预先冻结的结果解释规则

结果模式

	

允许的结论

	

明确禁止的结论




A：proCSC、revCSC 均高 CT2，调整后仍成立

	

Multiple stem-like configurations exhibit elevated predicted differentiation potency

	

已证明两者均可发生 fate switching




B：仅 proCSC 高，revCSC 不高

	

Proliferative stem-like and oncofetal-like states show divergent potency profiles

	

CT2 证明 revCSC 具有另一种 plasticity




C：proCSC 高，revCSC 显著更低

	

Oncofetal reprogramming is uncoupled from, or inversely associated with, CT2-predicted potency

	

revCSC 不具有 regenerative capacity




D：只有未调整 CT2 显著，depth/complexity control 后消失

	

Apparent potency enrichment is sensitive to transcriptional complexity

	

高 potency 的稳健发现




E：两者均无可靠的 CT2 elevation

	

Distinct transcriptional configurations without evidence of elevated CT2 potency

	

Highly plastic CSC populations




F：proCSC 与 revCSC 不能可靠区分

	

Co-activation or a continuous stem-like/oncofetal spectrum

	

两个独立 CSC states

这些结果中，B 或 C 反而可能与你的 TWEAKR–YAP 主线更契合：oncofetal state 的关键特征可能是特定 regenerative transcriptional program，而不是最高的 CT2 score。

但这个生物学解释需要在后续 Figure 中用功能实验检验，不能作为 Fig. 1c 的既定结果。

二、“plasticity” 的度量：Fig. 1c 到底画什么？
2.1 推荐保留 CT2 作为 primary readout，但重新定义它的角色

你已经在 Fig. 1b 对 CT2 做了系统审核，Fig. 1c 没必要另起一套未经充分验证的 plasticity index。

CT2 原始论文将其定义为对 developmental potential 的预测，包含 supervised gene expression model 与 neighborhood smoothing。它不是直接测量细胞的动态状态转换，而且其输出包含来自训练数据的 differentiation prior。
Nature Methods

因此，推荐：

Primary endpoint

CytoTRACE2-predicted developmental potency

如果主图是各状态的原始分布，纵轴使用：

CytoTRACE2 potency score

如果主图是患者内状态对照，我更推荐：

Within-patient difference in CytoTRACE2 potency

后者的比较更适合你的多中心 atlas，能够避免主要图形被患者组成、不同研究的测序平台和采样比例控制。

不要使用 Plasticity score、Cellular plasticity index 或 Fate-switching potential 作为纵轴。

2.2 Proxy 分级与决策

Metric

	

作用

	

推荐位置

	

是否可以用于证明 plasticity




CT2 final

	

Primary potency endpoint

	

Fig. 1c

	

不能




CT2 raw

	

检验 neighborhood smoothing 的影响

	

ED，必需

	

不能




Depth-matched CT2

	

检验 sequencing depth sensitivity

	

ED，必需

	

不能




Complexity-adjusted CT2 contrast

	

检验状态差异是否独立于复杂度及 cell cycle

	

ED，必需

	

不能




CCAT

	

Alternative potency proxy

	

ED，必需

	

不能




State entropy / program co-expression

	

描述 transcriptional mixing

	

ED，探索性

	

不能




kNN state diversity

	

描述 transcriptomic neighborhood mixing

	

ED，探索性

	

不能




Diffusion pseudotime

	

描述 manifold ordering

	

不进入正式 1c 检验

	

不能




Transition entropy without directional data

	

依赖人为构造的 transition model

	

不推荐

	

不能

CCAT 是基于细胞表达与 protein-interaction network connectivity 的相关性估计，不是 CT2 的独立实验验证，也不是真实的 fate probability。
PMC

这里有两个关键设计原则。

第一，不要把高度相关的 computational proxies 合成为一个未经验证的 plasticity composite score。CT2、CCAT、transcriptomic entropy 都依赖同一个 RNA expression matrix，多个 proxy 一致并不意味着多个独立证据支持。

第二，没有 RNA velocity 或真实 temporal/lineage information 时，kNN graph 主要提供 transcriptional similarity。即便使用 diffusion 或 Markov modeling，也无法凭借 undirected similarity graph 识别细胞状态转换的方向。CellRank 的 directed fate inference 特别依赖方向性信息或相应的模型假设。
PMC

2.3 如果要让 revCSC 的另一种生物学特征可见，应该测什么？

我建议引入一个与 CT2 区分的 secondary descriptive axis：

Lineage-program mixing / identity infidelity

具体概念是：在同一个上皮细胞内，是否出现通常属于不同成熟谱系、regenerative lineage 或 epithelial–mesenchymal programs 的异常共表达？

它与 CT2 的区别在于：

CT2 问：该细胞的转录组有多像具有更高 developmental potential 的细胞？

Lineage-program mixing 问：该细胞是否同时表达多个通常相互区分的 lineage identities？

但设计时必须使用独立的、预先定义的 lineage marker sets，最好不包含用于判定 revCSC/proCSC 的核心 marker，并排除 doublets、ambient RNA 及高度表达造成的假阳性。

例如，可以观察 absorptive、secretory、stem/progenitor 和 mesenchymal-like programs 的混合情况；不要简单统计一个细胞中六种 CSC signatures 的高分数量，那可能只是在重复测量同一个 shared stress/stemness program。

这个 readout 可以帮助发现 revCSC 的转录身份复杂性，但只能称为 transcriptional identity mixing，不能直接叫 plasticity。

2.4 避免与 A3a 循环论证

A3a 已经在回答：

Across epithelial cells, how do predefined continuous programs correlate with CT2 potency within samples?

Fig. 1c 应回答一个不同的问题：

Can the epithelial compartment be resolved into reproducible biological configurations, and how does predicted potency differ between those configurations within the same tumors?

两者的 estimand 不同：

	

A3a

	

Fig. 1c




单位

	

Cell-level program variation，汇总至患者

	

Patient-level state contrasts




自变量

	

连续 UCell scores

	

预先冻结的 epithelial state assignments




核心问题

	

Program–potency association

	

State identity、coexistence 与 potency stratification




主要结果

	

Within-sample Spearman associations

	

Paired state differences、state prevalence




增量

	

识别 potency-associated programs

	

识别不同 epithelial configurations 的共存与表型差异

但要明确：换成离散标签，本身不会自动消除 circularity。

如果 1c 的 proCSC 标签直接依据 A3a 的 27-gene score 定义，再显示 proCSC 具有高 CT2，那么它只是 A3a 的分类版本。

所以我建议 Fig. 1c 使用独立 reference-guided annotation 作为 primary taxonomy，把 A3a 六组 signatures 用于 annotation validation，而不是直接将六组分数的最大值转换为细胞类型。

三、上皮状态注释：如何从零构建可靠 taxonomy？
3.1 我不建议直接采用现有七分类作为互斥真值

你的原始清单方向合理，但是混合了不同维度：

Normal differentiated / secretory：主要是 differentiation lineage。

TA-like / proliferative CSC：包含 proliferation axis。

LGR5 canonical stem-like：主要是 WNT/canonical stem identity。

revCSC：主要是 regenerative/oncofetal identity。

EMT-like：主要是 epithelial–mesenchymal program。

这些不是严格处于同一个层级的 cell types。

例如，一个 revCSC 可以同时 proliferation-high；一个 LGR5-positive cell 可以处于 TA-like cycling 状态；一个 oncofetal cell 可以激活部分 EMT-like programs。

如果强行让所有细胞在七个标签中选择唯一一个，会创造大量人为互斥关系。

3.2 推荐使用 two-layer annotation

Tumor-derived epithelial cells

Treatment-naive primary CRC

Layer 1 · Epithelial identity

Differentiated-like

Secretory-like

TA-like

Canonical LGR5 stem-like

Proliferative CSC-like

Revival/oncofetal-like

EMT-like / partial EMT

Layer 2 · Orthogonal programs

Cell-cycle activity

Canonical WNT activity

Regeneration/oncofetal

YAP/TEAD activity

EMT / invasive programs

Lineage mixing

Potency proxies (outcomes only)

Final outputs

Primary identity + assignment confidence + secondary program activity + hybrid/unassigned status

Layer 1 可以为主图提供七种相对稳定的 transcriptional identities，但不应该暗示它们是七种生物学上严格互斥的 cell types。

Layer 2 则保留 overlapping programs。

特别是 proCSC 和 revCSC，我建议同时保留 continuous program scores，避免 hard classification 把真正的 hybrid state 强行分配到其中一类。

3.3 七类具体定义

这里给出候选 marker anchors，不是已验证的最终基因集。需要先审核与现有 27/32-gene signatures、reference training genes 的重叠。

State

	

候选 annotation anchors

	

主要误判风险




Differentiated-like

	

KRT20, CEACAM7, FABP1, ALPI

	

把 tumor differentiated-like 错叫 normal




Secretory-like

	

MUC2, TFF3, SPINK4, CLCA1

	

正常 goblet contamination




TA-like

	

Transit-amplifying reference program；MKI67, TOP2A 辅助

	

仅凭 cell cycle 错判




Canonical LGR5 stem-like

	

LGR5, ASCL2, SMOC2, OLFM4

	

LGR5 dropout、与 proCSC 重叠




proCSC-like

	

外部或冻结的 proCSC-associated identity anchors

	

增殖程序主导标签




Revival/oncofetal-like

	

CLU, ANXA1, TACSTD2, SOX4 等经参考验证的组合

	

Injury/stress、正常修复细胞混入




EMT-like

	

VIM, ZEB1, FN1 等组合，保留 epithelial identity

	

Fibroblast contamination、doublets

几个必要的修正：

第一，不能把肿瘤上皮里的 differentiated-like cells 直接命名为 Normal differentiated。 它们可能仍是 malignant cells，只是保留成熟分化程序。

第二，proCSC 不应仅由 proliferation markers 定义。 必须检验它能否在控制 S/G2M 后仍具有独立于 TA-like 的 stem-like identity。如果不能，就应将其描述为 proliferative/stem-associated program，而不是独立的 CSC cell type。

第三，EMT-like 应是严格质控后的 partial-EMT epithelial population。 它对 fibroblast admixture、epithelial–stromal doublets 非常敏感，不宜因少数 VIM/FN1-positive epithelial barcodes 就赋予独立身份。

第四，TNFRSF12A/TWEAKR 和 YAP target genes 不应作为 revival/oncofetal identity 的必要定义基因。 否则后续证明 revCSC 富集 TWEAKR/YAP，就是机制分析中的直接 circularity。建议优先将 TNFRSF12A、YAP core、TWEAK-response genes 留作 held-out mechanistic readouts。

3.4 四种注释方法如何选择？

方法

	

推荐角色

	

判断




Marker-based classification

	

Independent biological anchors / QC

	

必需，但单独不足




最大 UCell program score 分类

	

Sensitivity

	

不建议作为 primary




External reference mapping

	

Primary annotation backbone

	

推荐




Re-clustering + manual annotation

	

Stability validation / exploratory

	

不建议作为唯一依据

我推荐的实际架构是：

External reference-guided probabilistic annotation + predefined biological anchors + independent validation。

具体要求：

选择具有 published epithelial state labels 的 CRC reference，并建立事先冻结的 label correspondence table。

参考映射以原始或适当标准化的 expression information 为基础，不依赖 CT2 结果。

若 reference 与你的 atlas 有样本／研究重叠，必须执行 leave-one-study-out 或其他无样本泄漏的映射。

先产生 probabilistic state assignments，再决定 hard labels。

Cross-check 原始 marker、pseudobulk identity、患者内连续程序分布，以及不同研究中的 label consistency。

需要特别说明：Single-cell and bulk transcriptome sequencing identifies two epithelial tumor cell states and refines the consensus molecular classification of colorectal cancer 定义的是 iCMS2/iCMS3 intrinsic epithelial subtypes，并不是 proCSC/revCSC 的现成标准标签；不能直接将其映射为这两种 CSC。
Nature Genetics

Pelka 的 CRC reference 很适合提供 epithelial programs 和跨患者比较背景，但同样需要审核它的具体标签是否足以支持你的七分类，而不是因为文献知名就假设其存在一套同构 taxonomy。
PMC

3.5 Hybrid 与 unassigned 必须是正式输出

建议冻结如下规则：

High-confidence single-state：参考分类达到预定 confidence threshold，且第二候选状态没有接近最高状态的支持度。

Hybrid：两个或更多明确的 identity programs 同时得到较强支持，特别记录 proCSC–revCSC hybrid。

Unassigned：证据不足、marker coverage 不够、reference mapping 不稳定或没有可信的已知状态对应。

Suspected contamination：优先通过 QC 单独标记，不归入 EMT-like 或 hybrid。

可以考虑在 reference classifier 的 probabilities 经过 calibration 后，使用最高概率 0.70、与次高概率差至少 0.20 的初始阈值；但这两个数字只是建议的 operational thresholds，不能直接用于未经校准的 UCell scores。最终必须在不查看 CT2 的情况下，通过 reference held-out performance 冻结。

建议 ED 保留所有状态的 assigned fraction、hybrid fraction、unassigned fraction，以及不同研究中的覆盖情况。

如果结果显示大量细胞处于连续的 proCSC–revCSC mixing spectrum，而不是两个可分离的群体，就把 discrete two-population claim 降级为 two transcriptional programs / configurations，不要为了符合草稿人为制造 cluster boundaries。

3.6 独立性检查：必须冻结的四个层次

独立性

	

强制检查




Annotation vs CT2

	

CT2 不参与 feature selection、threshold optimization 或 label correction




Annotation vs A3a

	

核对 classifier features 与已冻结六组 signatures 的重叠；使用 held-out signatures 验证标签




Annotation vs complexity

	

检查 label confidence、state assignment 与 log UMI、log genes、mito、S/G2M 的关系




Annotation vs study/patient

	

Study-held-out mapping、patient-level marker validation、跨研究稳定性

CT2 是全转录组学习模型，无法保证 annotation genes 与其内部特征完全不重叠。因此这里的目标是避免直接 outcome leakage 和结果导向的 annotation optimization，而不是宣称两个 RNA-derived quantities 在统计学上完全独立。

我建议保存完整的 signature provenance、feature-overlap matrix，以及 CT2 模型公开的 informative features 的 overlap audit。

如果去除高度相关的 marker 后，proCSC 和 revCSC 再也无法区分，这本身就是重要的负面诊断。

3.7 Malignant vs tumor-derived epithelium：主分析选哪个？

Primary population：全部通过严格 QC 的、treatment-naive primary tumor-derived epithelial cells。

不要把它们全部称为 malignant。

你的现有 inferCNV 结果意味着 CNV-positive 是一个高度选择性的子集，而 CNV-uncertain 不能视为 CNV-negative 或 non-malignant。尤其 MSI-H 中，CNV-based malignancy identification 的 sensitivity 可能明显不足。

推荐分三层：

Cohort

	

用途

	

决策




All tumor-derived epithelial cells, QC-passed

	

Primary analysis

	

GO




High-confidence CNV-positive cells

	

Malignant-enriched sensitivity

	

GO，但强调选择偏倚




Histology-supported tumor epithelium，外加 independent epithelial malignancy evidence

	

如元数据可行，进行 refined sensitivity

	

Conditional GO

同时，必须检查原发肿瘤样本中的 normal-like contamination、tissue dissociation 和 doublets。

治疗后 RECIST CR 样本中保留的 “Cancer cell” 更不能当作 malignant 标签的证据。不过 Fig. 1c 主分析只使用 treatment-naive primary tumors，本身已经规避了最严重的 post-treatment contamination 风险。

四、统计设计：患者内比较、研究间 meta-analysis
4.1 Primary estimand：选择患者内状态差值

我的推荐是：

Primary comparison：同一肿瘤样本内，每个 epithelial state 相对于 differentiated-like epithelial state 的 median CT2 difference。

这是你提出的几个方案中最可解释的。

不建议以“state vs 该患者所有 epithelial cells 的中位数”作为 primary contrast。原因是每位患者的 epithelial composition 不同，而总体 epithelial median 会受到优势状态比例的影响。如果某个肿瘤大部分细胞都属于 proCSC，这个基线本身就会发生变化。

建议固定以下三项 planned contrasts：

Contrast

	

目的

	

统计优先级




proCSC-like vs differentiated-like

	

是否存在 elevated potency 的 proliferative/stem-like configuration

	

Primary




revCSC-like vs differentiated-like

	

revival/oncofetal configuration 是否也 elevated

	

Primary




proCSC-like vs revCSC-like

	

两个状态的 potency profiles 是否不同

	

Key secondary

其他状态（TA-like、canonical LGR5、secretory、EMT-like）也全部报告，但主要作为完整 epithelial hierarchy 的参照，不需要将所有两两组合都作为 confirmatory hypotheses。

注意：第三个 contrast 必须来自同一 tumor sample 内同时具有足够 proCSC 和 revCSC 细胞的患者。不能仅比较不同患者、不同研究中两组细胞的 pooled medians。

4.2 Aggregation：防止 pseudoreplication

预定四级分析单位：

Cell

计算 state-specific CT2 values

Tumor sample

计算 state medians 与 paired contrasts

Patient

汇总多个 tumor samples，独立统计单位

Study

REML random-effects meta-analysis

如果一个患者有多个 tumor samples，应先计算 sample-specific paired differences，再以预先确定的规则汇总到 patient-level，避免该患者由于采样次数多而获得更高权重。

对于满足最低要求的研究：

每个研究产生 patient-level paired contrast 的均值及标准误。

在 study level 采用 random-effects meta-analysis，REML 估计 heterogeneity，Hartung–Knapp 计算 confidence intervals。

报告 95% CI、heterogeneity、可估计时的 prediction interval、研究间方向一致性以及 leave-one-study-out。

若只有少数研究支持某个状态，Hartung–Knapp 与异质性估计也可能不稳定；应降级为 descriptive evidence，而不是盲目套用完整 meta-analysis。

CT2 final 应维持原始模型的 score scale。主分析不做任意的 patient-wise z-score transformation，防止改变可解释的 effect size。

4.3 最小样本门槛

以下是建议冻结的 operational thresholds。它们是为保证可靠估计而提出的分析设计值，不是文献确立的生物学标准。允许在不查看 CT2、CCAT 等 outcome 的 annotation-only feasibility audit 中调整一次，但调整必须有记录，且不能按显著性反向优化。

门槛

	

建议值




Tumor sample 最低 QC-passed epithelial cells

	

150




单状态用于患者内 median estimation

	

至少 30 cells




Differentiated-like reference

	

至少 50 cells




单研究用于汇总某个 contrast

	

至少 5 eligible patients




Contrast 进入正式 meta-analysis

	

至少 3 studies，累计至少 20 paired patients




Strong cross-study replication

	

优先要求至少 5 studies、30 paired patients




支持两个状态同肿瘤共存

	

至少 20 patients、覆盖 3 studies




State prevalence / co-occurrence sensitivity

	

检查固定采样深度下的检测稳定性

30 cells 不是说 29 cells 的状态不存在，而是说该样本不提供可靠的 primary median estimate。

患者内不满足 contrast 细胞数门槛时，应保留其 state presence information，但不产生对应的 paired potency contrast。

还必须报告 eligibility funnel：原始细胞数、通过 QC 的细胞、可注释细胞、拥有参考状态的样本、最终进入每个 contrast 的患者及研究。不能只报告最后产生显著结果的细胞数。

4.4 Complexity 与 depth 控制：这是 Fig. 1c 的硬门槛

考虑到 Fig. 1b 中 depth matching 导致 43–55% 的效应衰减，你在 Fig. 1c 必须采取与 Fig. 1b 对等的审核标准。

我建议区分：

Primary biological contrast： 基于 CT2 final，反映状态相关的总体预测差异。

Mandatory robustness analyses：

Depth matching： 在同一样本、不同状态间控制 UMI depth，重新计算或使用与 Fig. 1b 相容的 depth-matched CT2；并检查 repeated downsampling 的结果稳定性。

Expression complexity adjustment： 在样本内控制 log UMI、log detected genes 和 mitochondrial fraction。

Cell-cycle adjustment： 进一步控制 S/G2M，特别检查 proCSC 与 TA-like 的差别。

CT2 raw： 检查 final score 的差异是否主要来自 neighborhood smoothing。

CCAT： 检验另一种 potency proxy 是否支持同一方向。

Gene-count/marker coverage： 检查不同状态的 annotation probability 和可检测 marker 数量。

这里有一个微妙但重要的 statistical interpretation：

Cell cycle 和 transcriptomic complexity 既可能造成测量偏倚，也可能是真实生物学状态的一部分。

尤其是 proCSC，如果“proliferative”本来就是 phenotype 的一部分，那么完全调整掉 cell cycle，可能会消除部分真实的 state-associated biology。

因此，不能简单认为 adjusted result 比 unadjusted result 永远更接近 biological truth。

更合理的区分是：

未调整结果：total state-associated CT2 difference。

调整结果：在指定技术及生物学协变量条件下剩余的 difference。

Depth-matched 结果：针对测序深度敏感性的直接 stress test。

当未调整信号显著、所有技术敏感性分析都消失时，应将其视为 non-robust potency association。即使部分差异可能确实涉及真实的 RNA complexity biology，也不能强行写成已确认的高 developmental potency。

另外，CT2 final 包含 graph-based smoothing，因此应审核 Fig. 1b 与 Fig. 1c 使用的 CT2 是否完全同源：相同模型版本、输入、细胞集合与 smoothing configuration。不要因重新对子集运行 CT2 而使 score definition 悄然改变。

4.5 多重比较与结果判定

建议分两个 hypothesis families：

Family A：三个预先指定的关键 contrasts

采用 Holm correction，控制 family-wise error rate。

Family B：其他 epithelial identities 与 differentiated-like 的比较

采用 BH-FDR，作为 secondary analysis；如进行全部成对比较也应在此 family 中明确列出。

我建议使用下面的判定逻辑。

Evidence

	

判定




Meta-adjusted P 小于 0.05，95% CI 不跨零

	

平均关联的统计证据成立




Depth-matched 效应方向相同，且有统计支持

	

深度稳健性得到支持




Complexity-adjusted 效应方向相同

	

不完全由所调整复杂度变量解释




Leave-one-study-out 不改变主结论

	

跨研究稳定性得到支持




CCAT 同向

	

Alternative proxy concordance




Study prediction interval 不跨零

	

更有理由讨论跨研究普遍性

最后一条不应设为发现平均效应的绝对要求，但如果 prediction interval 跨零，就不能声称该差异在所有研究或所有 CRC 中普遍成立。

“两个 elevated potency configurations”的强判定标准： proCSC 和 revCSC 分别对 differentiated-like 显著升高，同时具有 depth-matched 和 complexity-adjusted 支持，并达到基本跨研究复现要求。

我不建议仅依据两者各自 P 值是否显著来判断它们是否真的不同。要声称 proCSC 与 revCSC 的 potency differs，必须直接检验它们之间的 paired contrast，并报告 effect size 和 CI。

如果你想说两者 potency 相近，还需要预先定义 equivalence margin；普通的 nonsignificant difference 并不能证明等价。

4.6 MSI/MSS 与其他分层

MSI/MSS 必须作为预先指定的 effect-modification analysis。

原因并不只是 MSI 状态可能影响 stemness，更重要的是：

患者构成在不同研究之间不均衡。

CNV-based malignancy confidence 强烈偏 MSS。

MSI-H 与 MSS 可能具有不同的 epithelial identity composition。

我建议：

Primary：全部符合要求的 treatment-naive primary CRC。

Secondary：MSS 与 MSI-H 分层的 state prevalence、CT2 contrasts。

Interaction：在研究内有足够两类患者时检验 MSI-related effect modification。

研究无法提供可靠 MSI 信息时标记 unknown，不进行推断性填补。

当 MSI-H 患者集中在一两个研究中时，不应把 pooled subgroup difference 解释为 MSI biology。

同理，分层后研究或患者数不足时只报告描述性结果。

五、范围控制：evolution 与 treatment 要不要进入 1c？

基于 A3b 目前只有 metadata gating、还没有 expression/QC results，我的建议非常明确：

Normal–primary comparison

GO · ED only

128 paired patients / 8 studies，具备开展 tumor enrichment validation 的基础，但不能直接建立细胞进化方向。

Pre–post treatment

HOLD

52 pairs / 3 studies；不同 treatment 与 MSI 背景严重混杂，不能直接合并推断治疗改变 plasticity。

Primary–metastasis

NO-GO

25 pairs / 2 studies；跨研究泛化与选择性取材问题过大，不进入正式 Fig. 1c 结论。

5.1 Normal–primary：有价值，但不是 1c primary claim 的必要条件

我赞成利用 128 个配对数据回答一个相对明确的问题：

Are revival/oncofetal-like epithelial configurations enriched in primary CRC compared with matched non-tumor epithelium?

这确实能帮助后续 oncofetal narrative。

但不能把它改写成：

Normal cells acquire an oncofetal state during malignant evolution.

因为正常与肿瘤样本是横截面观测，并不能直接识别细胞转化顺序。

另外，肿瘤中特定 state proportion 上升，可能是 malignant cell expansion、normal tissue composition difference、injury response 或 sampling enrichment，而不一定是 normal cell reprogramming。

建议 ED 使用：

每位配对患者的 oncofetal-like cell fraction difference。

同时呈现 proCSC-like、LGR5-like 和 differentiated-like proportions，避免只挑选 revCSC。

独立的 oncofetal program score distribution。

State annotation 在 normal/reference 与 tumor 两种背景中的 performance audit。

只有在配对信息、细胞注释、采样质量和 reference mapping 都可靠的情况下，才将它升级为 supportive biological evidence。

无需为了在 Fig. 1c 中证明两个不同的 stem-like states 而强制加入正常–肿瘤比较。 更适合放 ED，或者在专门讲 oncofetal state emergence 的后续面板中使用。

5.2 Treatment：不要把 chemotherapy 和 ICI 汇总成一个结果

Qin 2023 的化疗配对，以及 Chen/Li 的 ICI 配对，生物学背景不同，且 treatment modality 与 MSI 显著混杂。

治疗后还有 cell composition、residual normal mucosa、response category 和取样时间的影响。

可以后续分别问：

Chemotherapy-associated change in oncofetal state prevalence。

ICI-associated change in oncofetal state prevalence。

Therapy-associated program remodeling within matched patients。

但这些属于 therapy adaptation，不属于 Fig. 1c 的基本定义任务。

在目前的 Figure 1 中应 HOLD。即便后面出现有趣结果，也不应因为显著就临时加入 1c。

5.3 Primary–metastasis：NO-GO 作为本图的正式统计分析

25 对、两个研究，不足以可靠地区分 site biology、患者选择、组织处理和治疗史等影响。

可以保留为 future hypothesis generation，但不要使用它建立 normal → primary → metastasis 的连续 plasticity evolution narrative。

尤其不能把来自不同患者、不同研究的细胞拼成一条 pseudotime，然后称之为 CRC evolution。

六、Fig. 1c 与 Extended Data panel map

我建议 Nature 主刊 Fig. 1c 保持紧凑。不要把一张 Figure 1c 变成完整的 epithelial atlas paper。

Fig. 1c · 推荐主图结构

LEFT

Identity

pro-like

rev-like

hybrid

State identities、separation 与 hybrid occupancy

RIGHT

Potency

Point estimate + 95% CI

Patient-level paired potency contrasts

仅为版式示意。散点、位置及区间均为模拟值，并非你的分析结果；不代表预期效应方向。

主图的两个视觉要素分别回答：

Main panel

	

科学问题

	

主要读数




Fig. 1c-left

	

proCSC 与 revCSC 是分离、重叠，还是连续谱？

	

Independent state assignments、pro/rev axes、hybrid occupancy




Fig. 1c-right

	

在同一患者肿瘤内，不同 epithelial states 的 CT2 potency 如何分层？

	

Patient-paired CT2 contrasts + 95% CI

Left 不能只放一个漂亮的 UMAP。更推荐能清楚展示两个 identity axes 和 hybrid population 的 2D program landscape。若使用 UMAP，也必须同时提供可量化的 assignment reproducibility，而不是通过视觉分隔来证明独立 populations。

Right 如果状态很多，推荐 horizontal effect plot，而不是将几十万细胞画成 violins 后用细胞级显著性做主要统计。

Extended Data 建议

ED panel

	

回答的问题

	

必要性




ED1 · State annotation validation

	

Marker specificity、reference agreement、study-held-out stability、hybrid/unassigned

	

必需




ED2 · Patient/state coverage

	

各状态覆盖多少患者和研究？两种状态是否在同一肿瘤共存？

	

必需




ED3 · Potency robustness

	

CT2 raw、depth matching、complexity adjustment、CCAT 是否支持主结论？

	

必需




ED4 · Cross-study heterogeneity

	

Study-specific contrasts、leave-one-study-out、MSI/MSS

	

必需




ED5 · Normal–primary

	

Oncofetal-like states 在 paired primary tumors 是否富集？

	

Conditional GO




ED6 · Fibroblast zoom-in

	

保留 Fig. 1b 的 pan-cellular 结果，对 stromal compartment 深化解释

	

建议保留




ED7 · Lineage mixing

	

是否存在与 CT2 不同的 transcriptional identity mixing？

	

探索性

我不建议再加一个主图展示所有 7 类的 marker DotPlot。marker validation 放 ED 足够，除非 Fig. 1c-left 的状态可辨识性受到质疑。

同样，Fig. 1c 不应该出现 macrophage TWEAK–TWEAKR 的 causal arrows。单细胞图在这里完成的是 epithelial-state characterization，随后空间数据和 perturbation 再回答 TME 如何调控这些状态。

七、Reviewer 攻击点与执行顺序
7.1 最大的八个审稿风险

风险

	

Reviewer 可能提出的问题

	

防御方案




1. Circular annotation

	

用 stemness markers 定义细胞，再证明它们 stem-like？

	

External reference、held-out markers、annotation-before-CT2




2. CT2 depth bias

	

高 CT2 只是检测到更多基因？

	

Matched-depth、complexity-adjusted contrasts、raw score




3. State vs proliferation

	

proCSC 是否仅仅是 cycling TA cells？

	

Cell-cycle-adjusted comparison、独立 identity markers




4. Artificial discrete states

	

proCSC/revCSC 是否只是一个 continuum？

	

Probabilistic annotation、hybrid cells、continuous axes




5. Malignancy uncertainty

	

这些 oncofetal cells 真的是 malignant？

	

Tumor-derived 而非全部称 malignant；CNV-positive sensitivity




6. Pseudoreplication

	

几十万细胞，但信号是否由几个患者驱动？

	

Paired patient effects、study-level meta-analysis




7. No dynamic evidence

	

为什么称为 plasticity，而不是 transcriptomic state？

	

1c 不使用 functional plasticity claim




8. No spatial/causal evidence

	

1c 如何证明 TWEAK niche？

	

明确将空间组织和因果机制交给后续 Figures

7.2 一个特别重要的 Nature novelty 风险

我核对到一篇与你的工作直接相关的研究：

Oncofetal reprogramming drives phenotypic plasticity in WNT-dependent colorectal cancer，2025 年 2 月发表。

它已经报告了 CRC 中 canonical stem-cell 与 oncofetal transcriptional continuum、YAP/AP-1 驱动的 oncofetal reprogramming，以及相关的 lineage plasticity 和治疗适应。
Nature Genetics

这意味着：

“CRC 存在 canonical 和 oncofetal 两种 stem-like configurations”本身已不足以构成一篇 Nature 主刊论文的核心 novelty。

因此 Fig. 1c 的任务不是重新宣告两种状态的发现，而是为你的真正新机制提供可复现、可量化的人类 CRC 细胞生态背景。

你的论文需要比已有研究多回答一个关键问题：

What maintains the revival/oncofetal configuration in human CRC, and how does the spatially organized macrophage TWEAK–epithelial TWEAKR niche regulate its persistence?

这是从 epithelial intrinsic reprogramming 到 extrinsic niche-dependent state maintenance 的机制推进。

但要证明 maintenance，最终不仅需要 TWEAKR/YAP pathway activation，还需要 TWEAK/TWEAKR perturbation 导致状态改变的因果证据，最好具有 rescue 或其他排除替代机制的实验。

此外，spatially organized 必须由独立空间数据支持，而不是根据 Fig. 1c 的 scRNA-seq 状态分布推断。

7.3 推荐执行顺序

Stage 0 — Freeze eligibility and provenance

现在完成。固定 treatment-naive primary CRC cohort、cell QC、样本／患者 ID、reference datasets、program gene lists、CT2 版本，以及是否存在训练与验证数据重叠。核对 A3a 与 1c 的 cohort eligibility 是否一致。不要重新修改已冻结的 A3a。

Stage 1 — Annotation-only feasibility，CT2-blinded

在不查看 CT2 outcome 的情况下建立 epithelial taxonomy。检查七类的 marker validity、reference confidence、hybrid/unassigned fraction、study coverage、患者内共存和最小细胞数门槛。

这是第一个真正的 GO/NO-GO gate。如果 proCSC 和 revCSC 无法作为两个稳定类别被区分，立即改为 continuous two-axis framework，而不是继续强行分类。

Stage 2 — A3a final review

等待全量 A3a。检查 proCSC 和 revCSC 与 CT2 的关联在患者和研究两个层面的稳定性，特别是 depth-matched、complexity-adjusted、CCAT 结果。

A3a 的作用是帮助确定哪种 biological interpretation 获得支持，不能用来重新选择让 revCSC 看起来最高的 proxy 或分类阈值。

Stage 3 — Run locked Fig. 1c primary comparisons

用已冻结状态标签计算患者内 state medians、三个 planned contrasts、study-level meta-analysis、co-occurrence 和 eligibility funnel。保持分析者对主图美观与显著性偏好的独立。

Stage 4 — Mandatory sensitivity package

Depth matching、raw CT2、complexity adjustment、cell-cycle adjustment、CCAT、MSI/MSS、CNV-positive subset、leave-one-study-out。

如果 primary result 与敏感性结果冲突，优先如实报告冲突，不应只展示 supportive analyses。

Stage 5 — Select the prespecified result branch

按第一节结果判定表，选择 two elevated potency、divergent potency、continuous configuration 或 non-robust association 等对应结论。此时才能确定 Fig. 1c 的最终文字。

Stage 6 — Optional ED expansion

执行通过 A3b 后续 QC 的 paired normal–primary 比较。Treatment 和 primary–metastasis 不因偶然出现显著结果而改变 Fig. 1c 的研究范围。

还有一个容易忽略的 validation design 问题：你已经看过 DS-010 GSE254249 的 21 名患者结果。因此，即使现在冻结 contract，后续全量分析也不能称为完全未受先验结果影响的独立验证。

建议事先把 DS-010 标记为 pilot-informed study，正式结果同时报告包含全部研究和排除 DS-010 后的 cross-study estimates。如果剩余研究也支持同一方向，证据会更有说服力。

八、需要你决定并冻结的事项

我建议按下表直接确立 contract v1。只有少数项目需要 annotation-only feasibility 结果才能最终签字。

Contract item

	

推荐冻结值

	

时间




Scientific scope

	

Treatment-naive primary tumor-derived epithelium

	

现在




Main hypothesis

	

Distinct stem-like configurations with potentially divergent potency

	

现在




Primary endpoint

	

CT2 final，within-patient state contrast

	

现在




Reference state

	

Tumor differentiated-like epithelium

	

现在




Key contrasts

	

pro vs differentiated；rev vs differentiated；pro vs rev

	

现在




State taxonomy

	

Seven candidate identities + hybrid/unassigned；two-layer representation

	

现在固定框架




Classification method

	

External reference-guided、CT2-blinded probabilistic annotation

	

现在




Final classifier/threshold

	

根据 reference validation 和 label coverage 冻结，禁止 CT2-guided tuning

	

Annotation-only gate




Malignancy rule

	

All tumor-derived epithelium primary；CNV-positive sensitivity

	

现在




Inference level

	

Sample → patient → study，REML + HK

	

现在




Technical robustness

	

Depth、complexity、cell cycle、raw CT2、CCAT

	

现在




Subgroups

	

MSI/MSS；CNV-confidence

	

现在




Evolution/treatment

	

Normal–primary ED conditional GO；treatment HOLD；metastasis NO-GO

	

现在




Functional plasticity

	

不由 Fig. 1c 的计算 proxy 单独判定

	

现在




Caption/claim wording

	

使用预先冻结的结果分支规则

	

A3a + 1c 之后

有三个需要真正作出分析设计选择的地方。

Decision 1：七个 hard states 还是 two-axis continuum？

我的选择是 two-layer annotation，以七个 candidate state identities 提供解释，但同时保留完整的 continuous proCSC/revCSC axes 和 hybrid populations。最终是否能用 seven discrete states，需要通过盲于 CT2 的 reference validation。

Decision 2：是否坚持“两个 elevated potency states”？

我的选择是不坚持。将它作为一个有明确门槛的 secondary scientific possibility，而不是主图必须成功的假设。

Decision 3：是否把 normal–primary enrichment 放进主图？

我的选择是不放。保持 1c 聚焦 within-tumor state organization。128 对 normal–primary 样本是值得利用的资源，但应优先进入 ED；只有在后续 manuscript architecture 明确需要 tumor-associated emergence 时，再考虑升级。

最终推荐的 Fig. 1c narrative

我建议先冻结一句不预判结果的 working title：

Distinct epithelial stem-like configurations and their predicted developmental potency in primary colorectal cancer

它明确传达了 Fig. 1c 的生物学定位，也保留了结果不一致时的解释空间。

最终可以按结果写成以下三种主要版本：

Scenario A · 两个状态均稳健升高

Distinct proliferative and revival–oncofetal epithelial configurations exhibit elevated predicted developmental potency in primary CRC.

Scenario B · proCSC 高，revCSC 不高

Proliferative stem-like and revival–oncofetal epithelial configurations display divergent developmental potency profiles.

Scenario C · 只有 states，potency 结果不稳健

CRC epithelia harbor distinct stem-associated transcriptional configurations whose separation is not consistently reflected by computational potency estimates.

其中 Scenario B 目前尤其值得认真对待。但这只是由 DS-010 pilot 支持的先验可能性，不是对 13 个研究最终结果的预测。

我的最终判断：Fig. 1c 应该冻结“epithelial state identity + differential predicted potency”这个分析对象，而不是冻结“≥2 highly plastic CSC populations”这个结论。

如果 proCSC 高 CT2、revCSC 低 CT2，最重要的不是再寻找一个能把 revCSC 变高的计算指标，而是认真研究为什么 oncofetal reprogramming 与 conventional potency prediction 发生分离。

这将为后续章节提出一个更精准的机制问题：TWEAKR–YAP 究竟维持的是 canonical developmental potency，还是一种不同于 canonical proliferative stemness 的、具有特定 regenerative identity 和功能适应性的 epithelial state？

这需要后续实验回答，也正是 Fig. 1c 应该为整篇论文留下的科学空间。

ChatGPT can make mistakes. Check important info.
Latest response




High