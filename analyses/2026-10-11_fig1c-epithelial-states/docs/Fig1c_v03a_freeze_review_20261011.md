# Fig. 1c v0.3a freeze review (GPT, 2026-10-11)

Conversation: https://chatgpt.com/c/6acbaf02-1bc8-83ea-a533-5d9a9c06e138 ("设计Fig 1c分析方案")
Request sent: scratchpad msg5 (v0.3a lineage audit, label transition, recomputed gates, 4 questions).
Text below is GPT's reply, extracted verbatim from the page (table layout flattened).

---

Fig. 1c Stage 1 v0.3a — Final Audit

v0.3a annotation freeze: **APPROVE** — 接受预设 audit verdict，不再修改 OOD、lineage 或 Axis S 规则。
Stage 3 execution: **CONDITIONAL GO** — 完成下述 metadata reconciliation 和 analysis specification lock 后，即可合并 CT2。不需要再进行一次 annotation amendment，也不需要重跑 Stage 1。

根据你提供的汇总结果，G1–G10 已经充分支持将 v0.3a 作为正式 operational annotation。我的批准不等于认定所有 transferred lineage labels 均正确，也不等于确认存在两个独立的 CSC populations。

有两个重要限制必须随标签一起冻结：Stem/TA-like 尚未通过预设 lineage audit；而 rev-dominant 很多细胞缺少可信 lineage assignment。

## 1. Stage 1 审核结果

| 模块 | 判定 | 最终解释 |
|---|---|---|
| G1 | PASS | Pelka 内部 transfer performance 很好，外部研究仍存在 domain uncertainty |
| G2 | PASS | pro/rev programme measurements 稳定 |
| G3 | PASS | 独立 gene sets 支持两条生物学上不同的 programmes |
| G4 | PASS | pro/rev 可区分，但没有证明 discrete cell populations |
| G5 | PASS with selection warning | 四项 contrasts 具备基本可行性，但 reference selection 严重不随机 |
| G6 | PASS | 两种 operational strata 广泛共同检出 |
| G7 | HIGH RISK | RNA complexity、cell cycle confounding 仍需严格控制 |
| G8 | ACCEPT AMENDED VERDICT | 原 OOD 不再用于 hard rejection；lineage audit verdict 生效 |
| G9 | PASS | 没有明显单研究主导 |
| G10 | PASS | 冻结与 provenance 记录齐全 |

G3、G4 的结果支持 distinguishable transcriptional programmes。但 hybrid-high 观察比例 6.6%，独立期望 6.3%，并没有提供明显的超独立共激活证据。因此，接受现有分支：**Distinct transcriptional configurations, possibly with overlapping activation.** 不应将 hybrid continuum 描述为已证明的连续状态转换轨迹。

## 2. Stem/TA-like 全部失败：接受，不做事后修复

决定：APPROVE AS IS。这说明 Stem/TA-like 没有达到本次审核阈值，而不是证明这些细胞不是 stem-like。尤其 Pelka 自身只有 0.50，提示阈值可能不适合验证这一类相对弱表达、连续分布的 stem/progenitor identity。但是，既然规则在查看结果前冻结，就不应现在降低阈值来挽救这个类别。处理：
- 全部 75,695 个 Stem/TA-like predicted cells 保留原始预测标签和 lineage-transfer-unverified 标记。
- 不进入 verified-lineage comparisons。
- 不从全局 pro/rev continuous programmes 或不依赖 Axis L 的 operational contrasts 中删除。
- 原 within-stem analysis 正式改称 **Cycling Stem/TA-restricted pro-versus-rev contrast**（59 患者/6 研究，不再代表整个 stem/progenitor compartment）。
- 不需要强制新增 post-hoc sensitivity；如做，必须标记为 post hoc，不能替代冻结结果。

## 3. rev-dominant lineage uncertainty：不是无影响

pro-dominant 50,539 cells，73.3% Cycling Stem/TA；rev-dominant 46,048 cells，64.6% unverified/unresolved。
- pro vs rev comparison 仍然有效（strata 由独立于 Axis L 的 Qin programme scores 定义；203 患者/13 研究）。
- 不能声称该差异独立于 lineage composition：任何总体 CT2 差异都可能同时反映 programme 差异、cycling vs non-cycling composition、lineage composition、RNA depth/complexity、cross-study annotation uncertainty。
- 可写：Programme-defined epithelial strata differ in predicted developmental potency. 不可写：Proliferative and revival CSC states have intrinsically different developmental potency independent of lineage identity.

## 4. 进入 Stage 3 前的必须项（M1–M5，不涉及重新注释）

**M1. Reconcile G5 patient counts.** pro vs ref formal eligible 108，但 G5 audit included 120 / excluded 102。须在 manifest 中区分：(i) 有 sufficient differentiated reference 的患者；(ii) 同时满足 reference 与 pro-dominant thresholds 的患者；(iii) 最终满足 study-level meta-analysis eligibility 的患者。rev vs ref 同样。

**M2. Freeze secondary continuous model.**
- Population：所有满足基本 epithelial QC 和 sample-size 条件的患者，不以 reference availability 筛选。
- Model：每个样本内分别估计 proCSC 和 revCSC 与 CT2 的 partial Spearman；每个 programme 同时控制另一个 programme、log UMI、log genes、mito fraction、S/G2M、可评估的 verified Axis L lineage categories。
- Unverified/unresolved 保留，作为单独 annotation-status categories 调整，不假装为已验证谱系；未经 module audit 的 transitional/rare labels 也单独标记。
- 样本内无变化的类别项自动不入模；设计矩阵不可估计 → 该样本 conditional-model ineligible；不能事后删改协变量。
- Inference：sample partial r → Fisher z → 患者 → 研究 → REML+HK（与 A3a 相容）。
- 同时保留一个不依赖 Axis L 的 all-epithelium model 作为 sensitivity。

**M3. OOD-pass only sensitivity.** 必须执行，不作为 discovery。用 v0.3a 同一 scores/verdict/分组/统计，仅保留原 v0.3 OOD-pass 细胞；报告四项 contrast 剩余患者/研究、与 full 的方向和幅度、患者/研究构成变化；不满足 G5 时只做 descriptive。保留 v0.3→v0.3a transition table。

**M4. Depth-matched CT2 覆盖全部四项 contrasts**（CT2 final / raw / ds1–5 / adjusted 全部必需）。前三项为 Holm primary family；Cycling-restricted 为 planned sensitivity，不升级为 primary。ds1–5 先在患者内平均再做 study-level meta-analysis。ds 不完整时报告 missingness 和共同可比较集合，不得悄悄删除 unmatched cells。

**M5. Final label and join integrity.** 归档：562 cells 排除原因；cell_id 在 CT2 outputs 与 v0.3a 中唯一一对一；reference 27,976 是否含 5,415 discordant（按冻结规则 discordant absorptive 只属 reference，不进 pro/rev）；unverified/unresolved/not-evaluable/未经 audit 类别分开保留；v0.3、v0.3a 标签、verdict、G5 eligibility、代码与 hashes 全部归档不覆盖。

## 5. Stage 3 之后的解释边界

reference-based comparisons 仍有相当大的 selection bias（纳入患者 UMI 明显较低，rev-high tumours 常缺 reference）；即使显著也不能泛化为 222 名患者的共同规律，需与 continuous model 合并解释。G1 的 84.8% assigned 是 Pelka validation 指标，不等于全队列 84.8% 细胞获得 audit-supported lineage；Stage 3 coverage report 应区分 classifier assignment 与 study×class audit-supported assignment。

## Final decision

APPROVE v0.3a annotation freeze. 接受 Stem/TA-like 预设失败结果，不做事后阈值修复；pro/rev programmes 定义保留在所有 QC-passed epithelial cells 上，并明确 lineage-independent contrast 可能受 lineage composition 混杂。Stage 3：GO，前提是先完成 M1–M5。正式关闭 Stage 1 annotation decision process：后续即便出现 proCSC 高 CT2、revCSC 低 CT2，也不得回头修改 lineage audit、OOD handling 或 p75 operational strata。Fig. 1c 的核心证据取决于两种 programmes 是否呈现患者层面可重复、经技术稳健性检验后仍可解释的不同 potency profiles。
