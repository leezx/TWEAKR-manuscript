# A3b contract v0.2 — ChatGPT final-head check (2026-10-11, verbatim copy)

Conversation: TWEAKR-oncoFetal / "Fig.1b-CT2 plasticity". Reviewed commit 6439a32.

ChatGPT said:
A3b v0.2 — Final-head review
REVISE — Core GO, Chen surgical branch HOLD

已核查 commit 6439a32 的合同、clinical manifest、eligibility funnel 和两个生成脚本，并与 Fig. 1B 冻结的 L1/F1 规则对照。

决定：尚不能 FREEZE v0.2，但已经非常接近。 上轮六项主要设计问题基本关闭，不需要新增算法、改变研究对象或重新讨论 E1–E4。现在只剩下四项必须修正的实现定义，以及 Chen 2024 的手术标本身份问题。

我建议 A3b core 与 Chen surgical branch 分开冻结，不要让仅 9 名有效配对患者的 Chen 分支阻塞整个 normal–primary 分析。

一、Chen 2024：GEO Post 可以确认，surgical specimen 不能确认

这是本次最明确的临床判断。

GSE236581 确实属于多时点取样的新辅助 PD-1 治疗队列，包含肿瘤、癌旁正常及血液样本。原始论文也确认研究涉及连续取样及接受手术与未接受手术的不同患者。
PubMed
+1

但这两项事实并不能证明：

某患者接受了手术，因此该患者最后一次标记为 Post 的 scRNA-seq 样本一定来自手术切除组织。

你的临床 manifest 将这些样本明确标记为 surgical specimen (inferred)，如实区分了推断与事实，这一点正确。

我的判定：

Chen 分析

	

决定




I → GEO-confirmed Post

	

可以保留为临床阶段已定义的探索性配对




I → On

	

可以保留为描述性分析




I → Post surgical resection

	

HOLD，直至逐访视组织来源确认




将全部 II/III/IV 合并为 Post

	

NO-GO




根据最后一次访视推断患者发生细胞状态转换

	

NO-GO

不要求为此重新检查全部 22 名患者。只需核实当前 9 名满足 E1 的患者，逐个取得 Fig. S1 或其他原始 sample-level specimen annotation。

如果最终无法证明这些 Post 样本是手术标本，应将 Chen 分支的比较名称改为 Pre versus GEO-annotated Post，不使用 biopsy-versus-resection 或 residual surgical tumour 的措辞，并保留为 exploratory ED。

这不应阻止其他 A3b 分支冻结。

二、冻结前剩余四项阻断问题
1. F1 定义必须与冻结的 Fig. 1B 完全一致

这是一个明确的规则冲突。

v0.2 §1 写：

no foreign-lineage panel ≥ epithelial panel

但 Fig. 1B 的 L2_implementation_notes.md 和 l2_config.yaml 实际冻结的是：

Foreign-lineage panel 中至少两个基因，各自 ≥2 UMI，即标记 F1。

原规则不要求外谱系 panel 强于 epithelial panel。

请直接复用 A2.1 的原始 marker panels、阈值和判断代码，不要改用相对 marker dominance。对既有 cohort-v1 细胞必须检查新旧 F1 完全一致。

2. Evidence N 的 null calibration 仍存在一层训练泄漏

当前方案对 query patient 
𝑝
p 的独立性处理正确：患者 
𝑝
p 不参与其 reference 的 HVG/PCA 拟合。

但计算 null 时，reference patient 
𝑞
q 虽然从 kNN reference 中排除，却仍参与了该 fold 的 HVG selection、scaling 和 PCA fitting。

因此它是 neighbor-held-out，但不是 fully model-held-out。

这可能使 null distances 偏小，从而影响 P90 cutoff。

在冻结前请二选一并明确写死：

对 null patient 
𝑞
q 完整地排除其训练贡献，重新拟合必要的 preprocessing，再计算 held-out distance；或

使用独立的 calibration patients 建立阈值，并明确 reference-training 与 calibration 的分离规则。

90th percentile 和正常侧 normal-like fraction ≥0.75 的门槛均可保持不变。无需重新寻找最佳 cutoff。

3. E1 depth matching 后的 eligibility 必须定义

目前 ≥100 epithelial cells/sample 是原始样本 eligibility。

但每侧按 
𝑇
𝑠
𝐴
3
𝑏
T
s
A3b
	​

 下采样后，低于目标 UMI 的细胞被移除。一个原本有 100 个 epithelial cells 的样本，可能只保留 70–80 个。

需要明确：

Primary E1 是否要求 下采样后仍有 ≥100 epithelial cells/side。

如果患者一侧没有样本达到这个要求，该患者如何排除。

如果一个研究最终少于 5 名有效配对患者，是否停止该研究的 pooled inference。

当 depth matching 导致有效患者不足时，是否停止 E1 而仅报告 original-depth sensitivity。

我建议全部采用严格处理：primary E1 两侧都必须在 depth matching 后满足 ≥100 cells；否则不进入 primary inference。 原始深度结果不能事后替代 primary。

4. Complexity-adjusted OLS 的系数需要统一尺度

v0.2 §4 将调整后的 patient estimate 定义为：

cell-level OLS of the CT2 final rank on side, ...

如果直接使用整数 ranks，则 rank 范围会随每位患者的细胞总数改变。不同患者的 side coefficient 不在统一尺度上，不能直接进行 study-level pooling。

建议将 outcome 定义为患者内 0–1 normalized rank，或者使用保持 CT2 原始 0–1 分数的调整模型。二选一后冻结，不能混用。

该分析仍只是 mandatory sensitivity，不改变唯一 primary E1。

三、其他修订：接受，无需继续调整

模块

	

决定




Evidence T 联合 inferCNV

	

APPROVED




与旧 CNV calls 的 κ ≥0.40 及 clear-CNV 一致性

	

APPROVED




正常侧 CNV-high 中位率 2% gate

	

APPROVED，维持既定严格阈值




Evidence C 删除

	

APPROVED




E1 tissue-context primary

	

APPROVED




E2 composition

	

APPROVED




E3 selected tumour-evidence subset

	

APPROVED，必须注明 MSS/CNV-high 选择偏倚




E4 normal-like tissue-context

	

APPROVED




Axis-L E1-L

	

APPROVED，Pelka 排除




A3a 四个 programmes

	

APPROVED，secondary BH family




Qin surgical pre/post

	

Conditional GO，明确活检/手术与冻存/新鲜混杂




Li composition/descriptive

	

APPROVED，E3-pp NO-GO




Metastasis / healthy / polyp

	

维持 NO-GO

尤其要维持你的三分类解释边界：Normal-like 是正常黏膜表达相似性，不是已经证明非恶性；Tumour-evidence 是保守的 CNV-supported subset，不能代表全部恶性上皮。

四、执行顺序：批准 §8 的总体工作流

你的执行顺序合理，不需要重新设计：

Export — 按冻结 L1/F1 规则导出 counts 与样本注释

Joint inferCNV — 完成 T calls、旧版 concordance 和 normal-side calibration

Evidence N — 按修正后的交叉验证规则完成 normal-reference similarity

Identity classification — 三类身份、Axis-L、E2 composition、生成并核验 identity_v1 SHA256

Independent QA review — 审核 identity coverage、CNV uncertainty、MSI bias、normal-like calibration 和最终可用患者数

CT2 + UCell — 仅对通过门控的分支运行，原始分数和 depth-matched 分数按合同处理

Estimands — E1 主分析、mandatory sensitivities、E1-L、E3/E4 与 programme comparisons

这个顺序的关键优点是：在 CT2 和 programme outputs 被读取之前，就已经冻结了上皮身份及患者纳入规则，减少了根据结果反向修改分类的风险。

最终决定

A3b v0.2：REVISE → v0.3 final freeze。

仅需关闭上述四项技术定义问题；Chen surgical branch 独立 HOLD，不要求因此停止整个合同。

Normal–primary core： Design GO，待四项修正后 FREEZE。

Qin / Li： 按既定探索性分析范围保留。

Chen： GEO Pre/On/Post 映射接受；surgical specimen 身份未验证，手术特异性比较 HOLD。

Stage I/C computation： 当前尚未授权提交；v0.3 冻结后可按 §8 依次执行。

Stage S CT2： 必须等待 identity_v1 的 QA 通过后另行 GO。

不建议继续扩大 A3b 范围。下一个审核只需针对四项修复及 Chen branch 的最终状态，不需要重新讨论整个分析设计。

ChatGPT can make mistakes. Check important info.
Latest response




High
Response complete
-0.15
⋮⋮
⋮⋮