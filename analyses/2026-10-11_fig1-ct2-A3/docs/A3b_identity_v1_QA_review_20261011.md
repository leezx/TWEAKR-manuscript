# A3b identity_v1 QA — ChatGPT review (2026-10-11, verbatim copy)

Conversation: TWEAKR-oncoFetal / "Fig.1b-CT2 plasticity". Reviewed commit e7627d3.

ChatGPT said:
A3b identity_v1 QA 审核
Conditional APPROVED — Stage S limited GO

我的决定：接受并冻结现有 identity_v1，放行不依赖恶性身份判定的 A3b Stage S 分析；E3/E4 和身份组成相关的生物学推断不予放行。

已核对 commit e7627d3 的 QA 报告、公开门控表，以及 export、inferCNV、Evidence N、identity 和 eligibility 代码。未发现需要为了 E1 主分析重新设计或调整分类阈值的问题。

本次最重要的结论是：A3b 的 tissue-context 分析仍然成立，但 normal-like / tumour-evidence classifier 没有达到可以可靠量化肿瘤残留或恶性细胞组成的程度。 应保留这一失败模式，而不是继续优化分类器。

1. identity_v1：批准冻结，但限定其用途

Frozen identity_v1 · 425,183 epithelial cells

Normal-like 72.1%

Ambiguous 27.1%

Tumour-evidence 0.7%

三类为预设证据规则的输出，不代表真实正常与恶性细胞比例。

项目

	

审核




F1 concordance

	

PASS，报告为 0 mismatch




Joint inferCNV

	

165/165 完成；153 可评估




CNV concordance gate

	

30 名患者失败，按预设规则处理




Normal-side CNV gate

	

5/10 studies T void，规则正确执行




Evidence N calibration

	

10/10 studies PASS




Identity SHA256

	

已在 QA JSON 与报告中核对一致




E1 eligibility

	

6 studies / 86 patients，达到合同门槛

冻结标识：

2098d172dd36431fc745c4ca0a4b793d812214206396dc437ee91d4512d57819

这是对报告与公开元数据中 checksum 一致性的核验；我无法直接读取 Argos 上的私有 gzip 文件来独立重新计算 SHA256。正式 Stage S 启动前应由 Argos 再验证一次该 checksum。

冻结的含义是保存这一版细胞身份与 QA 结论，不是认证它具有可靠的 malignant-versus-normal 分类准确率。

2. 哪些 Stage S 分支批准？

Estimand

	

最终资格

	

决定




E1：Normal–primary CT2

	

86 patients / 6 studies

	

GO — primary




E1 mandatory sensitivities

	

与 E1 对应的预设分析

	

GO




E1-L：Axis-L matching

	

待 class-specific eligibility 确认

	

Conditional GO




R：四个 A3a programmes

	

配对上皮样本

	

GO — secondary




E1-pp Qin

	

18 patients

	

GO — exploratory ED




E1-pp Chen

	

10 patients

	

GO — exploratory ED




E2 / E2-pp

	

已有 identity labels

	

QA/descriptive only




E3：Tumour-evidence

	

Pelka 6、Lee 5

	

Descriptive only




E3-pp

	

0

	

NO-GO




E4：Normal-like comparison

	

分类缺乏充分鉴别力

	

NO-GO for biological inference




Li pre/post

	

8 patients，主要为 pCR

	

Composition QA only

这意味着 可以开始 E1 及其预设技术敏感性分析、E1-L 的合格性检查，以及四个 programme readouts，但不能把这个授权解释为允许进行完整的 malignant-cell-specific A3b 分析。

3. E2 / E4：我同意降级，而且需要纠正一个概念

选择方案 (b)：E4 降为描述性 QA；E2 和 E2-pp 只保留表达相似性组成的描述。

这里不建议把 tumour-side normal-like fraction 直接称为“残余正常上皮的上限”。

原因是 Evidence N 不只是漏掉恶性细胞，也会把部分真正正常的上皮细胞判为 reference-outlying。因此 normal-like fraction 并不构成一个严格的数学上界。

允许的解释是：

The normal-like fraction represents the proportion of epithelial cells transcriptionally similar to the matched study's normal-mucosa reference, rather than an estimate of residual non-malignant epithelium.

这个区别会直接影响 pre/post 的解读。

例如 Qin 的 tumour-side normal-like fraction 从约 0.62 增至 0.80，只能说明 post-treatment specimens contained a higher proportion of normal-reference-like epithelial transcriptomes。

不能据此声称：

正常上皮替代了恶性肿瘤细胞；

chemotherapy 诱导 malignant-to-normal differentiation；

残余正常上皮比例从 62% 增加到 80%。

因为这些观察也可能来自治疗后的细胞选择、组织取样、细胞组成及样本处理差异。

E4 也是同样的逻辑：两侧都是由同一个 normal similarity criterion 选出的细胞，再比较其 transcriptional identity 或 CT2，容易产生选择效应。可以将其保留为 reference-consistency QA，但不建议进行生物学机制解释。

4. E3：保留为两研究描述性结果，不再进行正式推断

E3 目前只有：

Study

	

Eligible patients




Pelka 2021

	

6




Lee 2020

	

5




Joanito 2022

	

4，未达到研究门槛

严格执行冻结合同，只有 Pelka 和 Lee 满足每研究至少五名患者的要求，合计 11 名患者，少于三项独立研究。

因此，E3 不满足 pooled inference eligibility。

可以报告两个研究各自的细胞数、患者数量及 CT2 分布，明确注明 selected CNV-supported, normal-reference-outlying epithelial subset。

不建议对这 11 人做正式的跨研究 meta-analysis，也不要通过降低研究门槛将 Joanito 强行加入。

更重要的是，这一子集并非经过独立 DNA 测序验证的全部恶性细胞，而是 CNV 和 normal-reference distance 双重筛选出的极小群体。它存在 MSS/CNV selection bias，以及对正常参考距离有明确依赖的选择偏倚。

E3 可以作为技术探索保留，但没有必要占据 Fig. 1 主图。

5. inferCNV：必须在 Methods / Extended Data 中报告其局限

同意，而且我认为这是一项必须公开的负面 QC 结果。

正常侧 CNV-high 率 · 按研究计算的患者中位数

Uhlitz

14.8%

Chen

7.9%

Khaliq

7.2%

MUI

4.3%

Qin

3.2%

Pelka

1.3%

Joanito

1.1%

Lee

1.0%

Qian

0.2%

Li

0.1%

预设 2% threshold；超过该值的五个研究，其 Evidence T 按合同作废。

这表明 immune/stromal-referenced inferCNV 在部分研究的正常上皮中产生了明显的 CNV-high calls，限制了将该方法用于 normal-versus-tumour classification 的可靠性。

但需要区分 观察到的现象 和 对现象的解释。

可以确认的是，五个研究未通过正常侧校准门槛，而且 CNV-high calls 与原 A2.1 存在部分不一致。

尚不能证明的是，这些正常侧 CNV-high calls 全部由 immune/stromal reference 的 epithelial-lineage expression bias 造成。该解释合理，但还可能涉及样本组成、技术批次、表达区域性变化及其他原因。

因此，不建议在 Results 中直接写成 we demonstrated that immune/stromal references induce false CNV calls。

与 Fig. 1B 的关系

这并不推翻 Fig. 1B 的 L1 primary comparisons。后者不依赖 malignancy classification。

但会进一步限制此前 high-confidence malignant epithelial subset 的解释。Fig. 1B 使用了肿瘤样本内的 inferCNV evidence，而 A3b 新增的 matched-normal calibration 揭示了该证据的谱系特异性限制。

建议在 Methods/ED 加入：

RNA-inferred CNV calls were used as conservative, operational evidence of malignancy rather than definitive malignant-cell labels. In paired normal–tumour analyses, five of ten studies exceeded the prespecified normal-side CNV-high calibration threshold, highlighting limitations in the specificity and cross-sample stability of these calls.

无需追溯修改冻结的 annotation_v1，但需要避免将其称为已经获得独立验证的 malignant ground truth。

6. 代码核查中两项需要记录的非阻断事项

我在 a3b_identity_qa.py 中发现，N_space_cnv_high.tsv 是从所有 CNV-high 且 clear-CNV 的细胞构建，没有进一步限制为 tumour-side、T-calibrated、T-evaluable 的细胞。因此报告中的 4–45% 不能严格称为对“明确恶性细胞”的 sensitivity，也不能将其作为独立的 malignant-cell validation metric。

请在最终 QA/Methods 中改为 CNV-high cells' out-of-reference fraction，并注明其范围。这只需要调整 QC 解释，不需要改变 identity labels。

另外，a3b_identity.py 在 N 不可评估时允许部分 T-positive 细胞进入 tumour-evidence；这比冻结合同的严格双证据规则宽。不过本次 10/10 studies 的 N 都通过了校准，因此该代码分支未影响现有 identity_v1。建议登记为 dormant implementation discrepancy，后续若要复用分类器，必须先使代码和合同一致，不能未经审核重新生成本次身份文件。

7. Stage S 的执行边界与验收

可以按下列顺序进行：

在 Argos 上验证 identity_v1 SHA256，并冻结纳入患者和样本清单。

对需要补充的样本运行 CytoTRACE2 1.1.0 whole-sample；对重叠样本执行已有 scores 的 hash/version check。

按固定 
𝑇
𝑠
𝐴
3
𝑏
T
s
A3b
	​

 和 seeds 1–5 进行全样本 UMI downsampling；保留 CT2 final 与 raw model outputs。

严格按已生成的 E1 eligibility 运行 86 名患者、6 项研究的配对比较，并执行 original-depth、depth-matched raw 和 complexity-adjusted sensitivities。

对 Qin 18 名患者、Chen 10 名患者分别报告探索性 pre/post estimates；四个 A3a programmes 按冻结方案计算，E1-L 仅在 class-level gate 通过时合并推断。

正式分析时还应核对所有 sample/patient joins 的唯一性，避免 Chen 的 naive samples 因同时属于 normal–primary 和 pre/post 两个分支而被重复当成独立观测。

在出结果之前，先保存 CT2 scoring QC、样本成功率、depth-matched retained-cell counts、各研究 model-gene coverage，以及最终分析患者清单。即使某项结果不符合预期，也不得更改 inclusion 或 depth 规则。

最终决定

审核对象

	

状态




identity_v1 checksum / annotation freeze

	

APPROVED




Identity 作为 malignant classification 的有效性

	

NOT ESTABLISHED




E1 normal–primary

	

GO




E1 mandatory sensitivities

	

GO




E1-L、四个 A3a programme readouts

	

GO，按冻结 eligibility




Qin / Chen E1-pp

	

GO，探索性 ED




E2 / E2-pp

	

Descriptive QA only




E3

	

Two-study descriptive only




E4

	

QA only，不作生物学推断




E3-pp

	

NO-GO




Chen surgical specimen comparison

	

HOLD

正式指令：FREEZE identity_v1 → LIMITED GO for Stage S CT2 + UCell → Submit E1 and sensitivity results for final review。

本次 QA 实际上提供了一个清晰的决策依据：A3b 仍然能够回答 tumour-specimen epithelium 与 adjacent-normal epithelium 是否存在 CT2-predicted developmental potential 差异；但不能可靠区分这种差异来自 malignant-cell-intrinsic programmes、上皮谱系组成，还是不同组织环境中的正常样细胞。

这正是应当保留的 claim ceiling。

ChatGPT can make mistakes. Check important info.
Latest response




High
Response complete
-0.15
⋮⋮
⋮⋮