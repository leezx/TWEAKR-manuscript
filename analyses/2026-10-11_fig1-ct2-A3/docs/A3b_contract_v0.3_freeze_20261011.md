# A3b contract v0.3 — ChatGPT freeze check (2026-10-11, verbatim copy)

Conversation: TWEAKR-oncoFetal / "Fig.1b-CT2 plasticity". Reviewed commit cd4bab5. Decision: FREEZE / GO Stage I/C steps 1–4.

ChatGPT said:
A3b v0.3 — Final-head review
FREEZE / GO — Stage I/C approved

结论：批准冻结 A3b v0.3（commit cd4bab5），授权执行 §8 的步骤 1–4。CT2 和 A3a programme scoring 仍须等待 identity_v1 QA 通过后单独放行。

已核对 
A3b_contract.md
、与 v0.2 的 Git diff、新增的 a3b_samples.py 及样本清单，并对照 Fig. 1B 的 l2_build.py 和 inferCNV 实现。

上轮四项阻断问题均已关闭。

项目

	

审核结论




F1 rule

	

PASS。已恢复 A2.1 的绝对 marker-conflict 判定，取消错误的相对优势条件，并规定旧版细胞 F1 必须完全一致




Evidence N

	

PASS。对 reference patient q 重新拟合 HVG、scaling 和 PCA，完成 fully model-held-out null calibration




Depth-matched eligibility

	

PASS。E1 两侧在匹配后均须保留 ≥100 epithelial cells，且研究及合并分析有明确停止规则




Adjusted E1

	

PASS。使用 CT2 原始 0–1 分数，side coefficient 具有统一尺度




Chen 2024

	

PASS。GEO Pre/Post 允许探索性分析；未确认的 surgical comparison 独立 HOLD




CNV top 5% profile

	

PASS。只用 pre/primary tumour-side epithelial cells 建立 CNV correlation profile




Reference subsampling

	

PASS。每患者独立 seed 0，可重复；新旧抽样的潜在差异交由预设 κ / clear-CNV gate 评估

Chen 2024：保留一个明确边界

批准的是 Pre vs GEO-annotated Post，不是已经证实的 Pre-biopsy vs Post-resection。

这两个临床命题必须严格区分。Chen 分支可纳入 identity 和 composition QA，但手术标本特异性分析继续 HOLD，直到九名候选患者的实际 specimen provenance 得到确认。

对于 Qin，TRG0 患者仅参与 composition analysis；Li 的 E3-pp 维持 NO-GO。以上都不妨碍 Stage I/C 启动。

授权执行范围

Stage 1 — Export：GO

按冻结的 broad L1/F1 规则导出 all-gene counts、patient/sample identifiers 和完整 QC metadata。对已有 cohort-v1 细胞执行 F1 exact-match assertion，任何不一致立即停止。

Stage 2 — Joint inferCNV：GO

按患者联合运行所有合格样本；完成 κ、clear-CNV concordance、normal-side 2% calibration gate。CNV 失败者保留不可评估状态，不放宽阈值。

Stage 3 — Evidence N：GO

使用 fully model-held-out reference/null、患者均衡抽样和冻结的 P90 threshold。报告每研究 normal-side calibration fraction；低于 0.75 的研究按合同标记 N not assessable。

Stage 4 — Identity / Axis-L / Composition：GO

按固定规则生成 Normal-like、Tumour-evidence、Ambiguous，进行 Axis-L projection 和 E2 composition summary，并生成 identity_v1 SHA256。

Stage 5 — Independent QA：MANDATORY HOLD POINT

检查完整分类结果和最终患者覆盖率。QA 未获批准前，不执行后续 CT2 / UCell scoring。

执行时需要保留的 QC 记录

这些是已经冻结规则的验证，不是要求增加新分析：

F1：旧新版重叠细胞数、mismatch count（必须为零）；参考免疫/基质细胞也应按原 A2.1 的 F1 排除原则处理。

CNV：每患者 reference cell count、新旧 κ、clear-CNV 翻转、每研究 normal-side CNV-high fraction，以及 T not assessable 的原因。

Evidence N：每研究参考患者数、held-out normal-like fraction、CNV-high 细胞在 N 空间的分布，以及 N calibration failure。

Identity：按 study × patient × specimen × MSI/therapy 分层报告三类比例，特别是 MSI-H 和 post-treatment 样本中 Ambiguous 的覆盖率。

Final eligibility：报告 E1/E2/E3/E4 可评估患者及研究数、被排除原因；不要继续沿用 metadata screening 时的 98 对、22 对、11 对作为最终可用数量。

新增的 a3b_samples.py 可以作为导出清单。注意其中 role="pair" 表示进入候选样本清单，不应被解释为该患者已经满足最终配对 eligibility。正式统计纳入仍以冻结的 sample-level 和 patient-level criteria 为准。

identity_v1 QA 交付要求

完成步骤 1–4 后，下次审核只需提交：

Identity QC report：总体执行成功率、F1/CNV/N 各门控结果。

Study-level identity composition 表及 MSI/therapy 分层。

Per-patient E1/E2/E3/E4 eligibility funnel。

CNV concordance、Evidence N calibration 表和 Axis-L coverage。

identity_v1 路径、细胞总数、SHA256 及代码版本。

不需要上传受限的 per-cell gene signatures 或重新提供已经批准的 A3a 结果。

最终授权

项目

	

状态




A3b v0.3 contract

	

FREEZE APPROVED




Stage 1 — Export

	

GO




Stage 2 — Joint inferCNV

	

GO




Stage 3 — Evidence N

	

GO




Stage 4 — Identity / Axis-L / E2

	

GO




Chen surgical-specific comparison

	

HOLD




Stage 5 — Identity QA

	

Pending




Stage 6 — CT2 + UCell

	

NOT AUTHORIZED




Stage 7 — E1/E3/E4 estimands

	

NOT AUTHORIZED

正式决定：FREEZE A3b v0.3 at cd4bab5 → Execute Stage I/C steps 1–4 → Submit identity_v1 for QA.

从现在起，不再修改 classification thresholds、reference definition 或患者纳入标准来适配观察到的结果。即使大部分 epithelial cells 最终落入 Ambiguous，也应按照已冻结的失败与停止规则报告。

本次是设计和执行范围授权；并不表示实际作业已经提交或 identity_v1 已经生成。

ChatGPT can make mistakes. Check important info.
Latest response




High
Response complete
-0.15
⋮⋮
⋮⋮