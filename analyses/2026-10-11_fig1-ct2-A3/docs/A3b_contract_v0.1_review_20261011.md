# A3b contract v0.1 — ChatGPT review (2026-10-11, verbatim copy)

Conversation: TWEAKR-oncoFetal / "Fig.1b-CT2 plasticity". Reviewed commit 3219b10. Decision: REVISE (not ready to freeze); Stage S scoring NO-GO.

A3b v0.1 合同审核
REVISE — Not ready to freeze

已阅读 commit 3219b10 的合同草稿、A3b metadata gate 和相关代码，并检索 Chen 2024 的原始论文与 GEO GSE236581。

总体决定：科学设计可以继续，Stage I（epithelial identity）与 Stage C（clinical gate）原则上批准；但 v0.1 尚不能冻结，Stage S 的表达和 CT2 打分仍为 NO-GO。

最需要修复的不是选择哪个分类器，而是身份判定的校准、CNV 跨样本一致性，以及临床时间点的精确定义。

一、七项问题的直接裁定

问题

	

决定

	

审核意见




Q1. Evidence N

	

Conditional GO

	

Same-study leave-patient-out 合理；90th percentile 可保留，但必须定义 cross-fitted calibration，且只能称 normal-like similarity




Q2. CNV

	

同患者全部样本联合重跑

	

不能混用旧版和新版 CNV calls；2% 作为预设 study QC gate 可以接受，但要明确统计分母与失效行为




Q3. Evidence C

	

DROP

	

不增加监督式 classifier；当前 CNV-positive 参考 MSS 富集，验证价值有限




Q4. Chen 2024

	

HOLD

	

III/IV 是否真正属于术后手术标本尚未证实，不批准立即定义 I→III/IV 为 primary




Q5. Axis-L matching

	

YES，secondary sensitivity

	

应在谱系相似状态内比较，但不能替代全上皮 tissue-context primary




Q6. A3a programmes

	

YES

	

固定版本作为 secondary readouts；不能反向用于身份分类




Q7. NO-GO

	

转移、未经核验的治疗对比及不可靠恶性判定

	

停止相应分支，不阻止其余合格研究继续

二、Evidence N：方法可以保留，但 90% cutoff 不是 malignancy threshold

你的 normal-reference distance 设计总体合理，尤其是：

同研究参考，减少 platform/study 差异。

Leave-patient-out，避免患者自身正常细胞充当自己的参考。

排除 A3a programme genes 和 Fig. 1c holdout genes，减少直接循环论证。

使用 kNN distance 而不是强制把所有肿瘤来源细胞分类到某个正常 subtype。

但存在一个关键问题：

Normal similarity percentile ＞90 只能表示细胞偏离了所构建的正常参考分布，不能直接表示细胞是恶性的。

你的三分类规则已经避免了把 N-positive 单独定义为 tumour-evidence，这一点正确。

建议保留 percentile=90，不再优化阈值，但必须将 I2/I4 的校准规则补充完整：

HVG selection、scaling 和 PCA 必须在每个 leave-patient-out training fold 内重新拟合，不能先使用全体正常患者计算 PCA 再留出患者。

正常参考的 null distribution 必须由独立的 held-out normal cells 得到；同一患者的正常细胞不得同时参与该患者使用的 reference 和 calibration。

明确如何处理不同患者的细胞数差异，例如每个 reference patient 固定最多贡献多少细胞，避免一个细胞数极多的患者主导 kNN。

报告每个 study 的正常侧距离分布及 leave-patient-out calibration；若正常侧分布明显受患者或处理批次影响，Evidence N 应标记为不可评估。

此外，“normal-side approximately 90% normal-like” 是阈值定义的预期校准结果，不是独立的分类准确率验证。

真正有价值的验证是：高置信 CNV-positive tumor cells 是否较正常上皮更频繁地位于正常参考分布之外。

如果一个 CNV-clear 患者中大量高置信 CNV-high 细胞也落入 normal-like reference range，应该允许它们保留 ambiguous，而不是事后移动 cutoff。

三、Evidence T：批准全部样本联合 inferCNV，但不要改变已有 Fig. 1B 结果

推荐在每个患者内部，将其所有相关上皮样本一并作为 observation，并使用按固定规则选择的非上皮参考细胞。

原因是 inferCNV 的相对表达基线、参考细胞选择和 denoising 会影响 CNV scores。如果原发肿瘤使用旧版本，正常或治疗后样本使用新版本，再直接比较 CNV-high calls，可能引入算法处理差异。

因此批准重新计算 A3b patient-level CNV。

但须区分：

A2.1 的 annotation_v1：继续冻结，不修改。

A3b 的 identity_v1：独立生成，允许由于联合样本推断而与旧 calls 有一定差异。

建议在合同写死两项 QC：旧版与新版重叠细胞的 Cohen's κ 和 CNV-high agreement；若低于预先设定的最低一致性标准，则停止该患者的 tumour-evidence 分类并调查原因，而不是直接接受变化。最低标准应在运行前指定。

关于正常上皮 CNV-high 率 ＞2%

我接受它作为严格的技术质量门槛，但不建议直接称为 true false-positive rate。

正常侧上皮本身来自癌旁黏膜，且并非所有细胞都经过正交基因组验证；这里测得的是 empirical normal-side CNV-high rate。

要在 v0.2 中规定：

每患者如何计算该比例。

每研究至少有多少正常侧上皮细胞和可评估患者。

研究中位比例超过 2% 时，整个 study 的 Evidence T 标记为不可用，而不是重新寻找一个更宽松 cutoff。

N 仍可独立运行，但不凭 N alone 产生 tumour-evidence labels。

并且必须保留 MSI-H/CNV-low 细胞为 ambiguous 的规则。否则会重新制造 Fig. 1B 的 MSS selection bias。

四、Chen 2024：时间点映射是当前最明确的临床阻断项

我查询了原始 Spatiotemporal single-cell analysis decodes cellular dynamics underlying different responses to immunotherapy in colorectal cancer 和 
GSE236581 GEO record
。

原始论文和 GEO 明确支持：

22 名患者接受新辅助 PD-1 blockade。

169 个单细胞样本。

存在多次连续采样，涵盖肿瘤、癌旁正常及外周血。

GEO/下游样本信息使用 Pre、On、Post 阶段。
ncbi.nlm.nih.gov
+1

但我目前无法从已经获取的原始 Methods 确认 II、III、IV 与具体采样日期、治疗周期、手术切除之间的一一映射。

还有一项需要特别警惕的线索：公开的 GSE236581 数据集描述在某些再分析中将 II–IV 统称为 on-treatment。因此，单凭后缀数字递增，不能将 III/IV 自动认定为手术后标本。
bioRxiv

我的决定：

Chen 对比

	

判定




I vs II

	

候选 early/on-treatment contrast，待样本阶段核验




I vs III

	

候选 later-treatment / post-treatment contrast，待核验




I vs IV

	

候选 later-treatment / post-treatment contrast，待核验




I vs 合并 III/IV

	

目前不批准作为 primary




I vs verified surgical specimen

	

首选 primary candidate，前提是原始样本信息证明它确实是手术标本

如果 III/IV 是同一患者不同治疗时点，则不能将它们简单聚合为一个 post。

如果两个后缀代表同一手术时间点的不同组织区域，则可以作为区域内重复样本，在患者层聚合，但不可把它们当成独立患者。

冻结前必须建立 patient × sample × suffix × collection stage × treatment cycle × biopsy/resection 的映射表。

Qin 和 Li 也需要完成相同级别的来源核验。尤其不能把 RECIST complete response 当成 pathological complete response。

五、Axis-L：必须纳入次要分析，但不能取代 E1

我支持增加 Axis-L lineage-matched comparison，因为 normal–primary 的全上皮 CT2 差异可能大部分来自正常黏膜中分化 colonocytes、goblet cells 的组成，与 tumour-derived epithelium 的组成不同。

建议分析层级：

Estimand

	

对象

	

角色




E1

	

全体符合条件的 paired epithelial compartments

	

Primary tissue-context




E1-L

	

相同 Axis-L lineage class 内的 normal vs tumour-derived epithelial

	

Secondary composition sensitivity




E3

	

CNV-supported tumour-evidence vs normal-side normal-like epithelial

	

Secondary selected subset




E3-L

	

两侧处于相近 lineage class 的 E3 细胞

	

Exploratory；仅当有效患者数足够

但是有一个重要限制：我未能从本次提交文件独立核查 Fig. 1c Axis-L 的完整定义。

因此在使用前，需要确认 Axis-L 是一个已经冻结、可投射到正常和肿瘤上皮、且未使用 CT2 或 A3a programme scores 训练的状态分类。如果 Axis-L 本身依赖 oncofetal/CSC programme，就不能再把其分层结果解释为独立于这些 programme 的验证。

建议预先固定 stem/TA-like 及 differentiated absorptive/goblet-like 等可比类别，不允许在结果出来后仅选取能出现预期效应的 lineage class。

E3-L 如果只剩少数 MSS/CNV-clear 患者，直接降级为 descriptive，不要求强行做 random-effects meta-analysis。

六、A3a programmes：允许纳入 A3b secondary readouts

批准。

建议固定为 proCSC、revCSC、Extended CIOC-222 和 YAP core，保持 A3a 的基因集版本及 UCell scoring definition。

它们不参与 Evidence N feature selection，也不参与 Evidence T calls，因此至少避免了直接使用 outcome 定义细胞身份的循环问题。

但仍需要承认：CNV 和 transcriptomic classification 均从 RNA counts 推断，与 programme score 并非真正的独立检测技术。

对于正常–原发，应分别报告 tissue-context programme difference 及 identity-selected subset difference。对于治疗前后，报告变化方向，但不能直接写成癌细胞发生了 proCSC→revCSC conversion。

另外，A3b 如欲使用 A3a 的 programme 结果，必须在看新表达/CT2 结果之前写死这四项 secondary endpoints 和它们的多重比较或 descriptive 地位。

七、冻结前必须修改的项目

以下六项是阻断项，不是建议再开展一轮开放式方法探索。

Evidence N calibration：明确完整的 leave-patient-out preprocessing、null calibration、reference cell balancing、缺乏正常参考时的处理，以及 90th percentile 的解释边界。

Evidence T comparability：规定 A3b 全患者联合 CNV、旧新版 concordance 的量化及失败规则、2% normal-side gate 的分母和触发后行为。

Chen/Qin/Li clinical sample manifest：完成可靠的时间点、样本类型、治疗方案及临床缓解核验；Chen 在时间点明确前不预设 III/IV 为 surgical post。

E1/E3 eligibility 和 depth 规则：冻结每侧每样本最低 epithelial cells、多个样本的 patient aggregation、matched-depth target、CT2 final/raw 的层级及 adjustment 规则。建议主 E1 每侧至少 100 cells，E3 每侧至少 30 个符合身份标准的细胞；只满足较低细胞数的患者可以用于 composition feasibility，但不能自动进入主 CT2 比较。

Axis-L sensitivity：确认并冻结可跨正常/肿瘤使用的 lineage definitions、适用患者阈值和停止规则；不把分层比较替代 E1。

Evidence C 和 readout freeze：明确删除 Evidence C，不再保留为可以事后启用的可选分支；固定四个 A3a secondary programmes 及其统计地位。

这里特别强调，E1 目前同时写了 depth-matched + adjusted primary，但统计层级尚不够清晰。建议锁定一个主要 CT2 estimand（例如 matched-depth final CT2 的患者内差值），将 raw-model 和复杂度调整结果设为强制敏感性分析，而不是三个平行的 primary endpoints。

还要明确 CT2 final 的样本组成依赖：正常和肿瘤细胞数、谱系组成不同，即使 depth-matched，whole-sample smoothing 仍可能改变预测分数。因此 raw-model sensitivity 必须保留。

八、是否存在需要直接停止的分支？

分支

	

当前决定




Naive normal–primary（此前 8 studies / 116 usable pairs）

	

Conditional GO；优先推进身份分类




Qin 2023 pre/post chemotherapy

	

Conditional exploratory GO；等待 Methods/临床注释




Chen 2024 longitudinal ICI

	

Clinical HOLD；先解决 II/III/IV




Li 2023 pre/post ICI

	

Conditional exploratory GO；等待样本采集与病理核验




Primary–metastasis

	

NO-GO




Healthy normal / polyp

	

不作为 inferential A3b 分支




Evidence C supervised tumour classifier

	

DROP




A3b CT2 scoring

	

NO-GO until Stage I/C freeze and QC

尤其是 Chen 2024，我不建议为追求更大的 pre/post 数量而将所有 treated samples 合并。宁可有效配对减少，也要保证比较的是明确的临床时间点。

最终审核决定

A3b contract v0.1

REVISE

身份分类策略的基本方向可接受，临床样本映射和若干关键实现参数尚未满足冻结要求。

Stage I / Stage C design

Conditional GO

Contract FREEZE

NOT YET

Expression / inferCNV / CT2 run

NOT AUTHORIZED

建议把上述六项落实为 A3b v0.2 后做一次 final-head check。不要再增加新算法、扩大队列或改变已冻结的 A3a。

下一次提交只需提供修订合同、Chen/Qin/Li 的样本时点来源表和明确的 eligibility/depth 参数。如果临床原文仍无法确认 Chen III/IV，允许将 Chen longitudinal branch 标记为 HOLD，先冻结其他部分，而不是让整个 A3b 无限等待。

最终指令：REVISE v0.1 → v0.2；暂不 FREEZE，不提交 A3b 计算。

ChatGPT can make mistakes. Check important info.
Latest response




High
Response complete
-0.15
⋮⋮
⋮⋮