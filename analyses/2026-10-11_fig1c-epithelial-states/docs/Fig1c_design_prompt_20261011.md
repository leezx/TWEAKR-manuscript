我在写一篇 CRC 论文（目标 Nature 主刊）。主线：CRC 中存在空间组织的 oncofetal CSC 状态，由巨噬细胞 TWEAK → 上皮 TWEAKR（TNFRSF12A）/YAP 信号维持。现在要设计 Figure 1c。请你先帮我**设计分析方案**（不是写代码），我会按你的方案冻结 contract 后执行。

## 我对 Fig. 1c 的定位（作者草稿原文要点）

- B = annotation-independent scoring, annotation-stratified interpretation；C = within-epithelium resolution。
- C 这里才使用 cell-type annotation，但不能称为“无偏”——annotation 已经带入 biological prior。
- C 把上皮展开为：Normal differentiated / TA-like / canonical stem-like (LGR5) / proliferative CSC (proCSC) / revival-oncofetal (revCSC) / secretory / EMT-like……，然后显示 plasticity distribution。
- 关键不是“stem cells score 高”这种已知结论，而是：**CRC epithelial plasticity is concentrated in more than one stem-like state** —— 不是一个 CSC population，而是至少两个 highly plastic stem-like configurations。
- Fibroblast 的 zoom-in 放 Extended Data；主图 B 保留它以证明 pan-cellular，然后明确 zoom into epithelium（scope restriction，不是 cherry-picking）。
- TODO（我自己的疑问）：可以深化——不仅问哪个状态 plasticity 最高，还可以问 evolution 后（正常→原发→转移）、治疗后 plasticity 是否系统性变化。但不能无限拓展，需要一个核心 claim。

## 已有证据（已完成、已审核）

**Fig. 1b（CytoTRACE2，CT2）**：13 个研究、222 名 treatment-naive 原发 CRC 患者、~100 万细胞。患者中位 CT2：基质 0.287 > 上皮 0.131 > 免疫 0.062；13/13 研究方向一致；但 depth-matched 后效应缩小 43–55%，depth-matched raw 的 E−I 只剩 +0.012 且 PI 跨 0。成纤维细胞 0.495 最高。审核措辞约束：**不把 CT2 称为 plasticity**；必须报告深度敏感性；不写 fibroblasts 是 plasticity 主要来源。结论：上皮整体并不比 TME 更“原始”，可塑性若存在应体现在上皮内部状态结构。

**上皮注释现状（重要限制）**：
- Atlas 的上皮标签由样本类型决定：原发肿瘤里 100% 上皮叫 "Cancer cell"，正常样本只有正常亚型（progenitor、goblet 等），转移只有 "CRLM"。即**肿瘤上皮内部目前没有任何状态注释**。
- infercnv 只能识别 34,764 个高置信恶性细胞（76 患者/8 研究，强烈偏向 MSS；MSI-H 近二倍体检不出）；86.9% 上皮为 CNV-uncertain。Epithelial 整合 ARI 0.26（按患者聚类）。
- 治疗后 RECIST CR 患者仍有中位 ~600 个 "Cancer cell"，很可能是再生/正常黏膜。

**A3a（已冻结并正在全量运行，结果未出）**：cohort v1 的 285,703 个 L1 上皮细胞，UCell 打分 proCSC(27 基因)/revCSC(32)/Lgr5CSC(27)/Extended CIOC(222)/YAP core(12)/ECOS-38；样本内 Spearman ρ（程序 × CT2 final，主指标未调整），partial ρ（调整 log UMI、log genes、mito、S/G2M）为强制稳健性指标；Fisher z → 患者 → 研究 → REML+HK；CT2 raw、depth-matched、CCAT（secondary）为敏感性；proCSC–revCSC 共激活（样本内 75 百分位）作为 ED 描述读数。

**单队列先验（DS-010 GSE254249，21 患者）**：proCSC–CT2 ρ +0.59（调整后 +0.32）；revCSC–CT2 +0.18（调整后 −0.05）；用 CCAT 时 revCSC +0.47 → 调整后 −0.06。即 **revCSC 与 potency proxy 的正关联在调整复杂度后消失**；YAP-oncofetal、regeneration、placenta 程序跨 MP 与 CT2 关联负向。这对“两个 highly plastic stem-like configurations”是一个直接威胁：CT2 可能只把 proCSC 判为高 potency，而 revCSC/oncofetal 在 CT2 下并不高。

**A3b 元数据门控（仅元数据）**：正常–原发配对 128 对/8 研究；治疗前后 52 对/3 研究（化疗仅 Qin 2023 MSS 27 对；抗 PD-1 Chen 2024 + Li 2023 共 24 对，多为 MSI；治疗与 MSI 强混杂）；原发–转移 25 对/2 研究（NO-GO）。

## 请你回答

1. **核心 claim**：Fig. 1c 应该锁定哪一个可检验、可被证伪的核心 claim？“plasticity 集中于 ≥2 个 stem-like 状态”是否成立的门槛是什么？如果数据显示只有 proCSC 高 CT2、revCSC 不高，图 1c 应该怎么改写（例如改为“两种不同类型的可塑性：增殖-干性型 vs 再生-oncofetal 型，CT2 只捕获前者”）？请预先写出各种结果下的解释规则。
2. **“plasticity” 的度量**：既然审核禁止把 CT2 称为 plasticity，Fig. 1c 的 y 轴应该是什么？是否需要多 proxy 组合（CT2 final/raw/depth-matched、CCAT、状态熵/多程序共表达、RNA velocity 不可用时的替代如 transition entropy/diffusion pseudotime 不确定性、kNN 邻域状态多样性等）？哪些能放主图，哪些只能做敏感性？如何避免与 A3a 循环论证（A3a 已经用连续程序分数 × CT2）——1c 相对 A3a 的增量是什么？
3. **上皮状态注释方案**：在没有现成状态标签、ARI 低、恶性判定偏 MSS 的前提下，如何定义状态类别（marker-based 分类 vs 连续程序最大值 vs 参考映射如 Pelka/Joanito/Qin 的 epithelial states vs 聚类后注释）？类别清单是否采用我草稿中的 7 类？如何处理多状态共表达（hybrid）和 unassigned？必须在看 CT2 之前冻结，且定义状态的基因不能与 CT2 模型特征/复杂度强耦合——如何设计这一独立性检查？恶性 vs 全部肿瘤来源上皮哪个做主分析？
4. **统计设计**：患者为单位、研究为随机效应的框架下，比较 ≥7 个状态的 proxy 分布用什么估计量（患者内状态间差值？状态 vs 患者内上皮中位的差值？）；多重比较；必需的深度/复杂度控制；MSI/MSS 分层；最小细胞数门槛。
5. **范围控制（我的 TODO）**：evolution（正常→原发→转移）和治疗后变化是否应该进入 Fig. 1c 主图，还是留给 Extended Data / 后续 Figure？请结合 A3b 门控结果给出 GO/HOLD/NO-GO，并说明理由。正常–原发对于“oncofetal 状态是否是肿瘤获得的”是否有必要放在 1c？
6. **面板设计**：给出 Fig. 1c（以及必要的 ED）的 panel map，每个 panel 回答一个问题。
7. **审稿风险与执行顺序**：列出主要 reviewer 攻击点，并给出分阶段执行顺序（哪些要等 A3a 结果出来后再定）。

请按：核心 claim → 度量 → 注释 → 统计 → 范围 → panel map → 风险与执行顺序 → 需要我决定的事项，输出一个可冻结的 Fig. 1c analysis contract 草案。中文回答，术语保留英文。
