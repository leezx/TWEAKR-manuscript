# Fn14 治疗性抗体 / ADC 表位清单（epitope atlas）

**对话日期：** 2026-11-03 · **执行者：** Claude Opus 5 for Zhixin Li
**状态：** **GPT 审核 APPROVE（第 5 轮，HEAD `329fcec`），定位 Fn14 therapeutic epitope atlas v1 candidate，允许合并；
等待用户授权合并 PR #4。** 13 条抗体及抗体衍生物 + 4 张关联表（配体类构建体、TWEAK 靶向、13 个专利族、方位敏感性）+ 结构映射。
现行结论以 `docs/results_v2.md` 为准；冻结标准 `docs/freeze_criteria.md`（六项条件已全部满足）；
审核记录 `docs/reviews/`（PR3 第 1 轮、PR4 第 2–5 轮）
**UDE 分支：** B32 之后的新支线（见 `../../UDE/root-branch-history.md`；B32 已于 PR #2 合并，merge `762efb1`）

## 1. 问题与目标

哪些药物**直接结合 Fn14 蛋白本身**？其中哪些公开了可用于结构建模的 VH/VL 序列或实验表位？
这些表位与 B32（M2）预测的 TWEAK 结合界面是什么关系？

产物是一份可核查的清单加一次结构映射，**不是**结构预测。GPT 审核（PR #2 第 1、2 轮）明确建议：
先建清单，再决定对谁建模。

## 2. 对应 Figure / panel

暂无正式 figure。后续若做 Panel B（治疗表位图），本目录是其证据来源。

## 3. 输入

- **文献：** PubMed / Europe PMC，检索日期 2026-11-03，查询式见 `docs/results_v1.md` 与 `manifests/queries.tsv`。
- **临床试验：** ClinicalTrials.gov API v2，2026-11-03。
- **结构：** B32 冻结的 M2-C 第一名模型
  `DATA/HotData/TWEAKR-oncoFetal/analysis/af3_M2/frozen/af3_M2/m2_tweak3_fn14x3_tmplc/m2_tweak3_fn14x3_tmplc_model.cif`
  （sha256 见 `manifests/inputs.tsv`）。**本目录不产生新的结构预测，也不含重数据。**
- **序列：** UniProt Q9NP84（人 Fn14 前体，129 aa），全部残基编号用前体编号。

## 4. 参考文献

本轮核验的一手文献（均已读摘要，PMID 见 `tables/fn14_binders.tsv`）：Culp 2010（20068083）、Michaelson 2011（21697654）、
Zhou 2011（21586630）、Salzmann 2013（23532848）、Trebing 2014（24135629）、Keshtvarz 2017（28357912）、
Lam 2018（29054986）、Keshtvarz 2022（35978517）。

继承 B32 已登记的 REF-032 至 REF-040（`1.TWEAKR-oncoFetal/reference.md`）。本轮新文献**尚未**分配 REF 编号——
待清单稳定后一并登记，避免为检索到的每篇文章都占号。

## 5. 方法

1. **先定规则后检索：** 证据分级 E1–E5 与纳入/排除标准写在 `docs/design.md`，commit `afd15b4` 早于第一次检索。
2. **检索与核验：** 每条记录的每个字段都要有一手出处；只读到摘要的标 `verified`（摘要级），未核实的标 `unverified`。
3. **结构映射：** `code/map_epitope_residues.py` 把 E2 级表位残基映射到 M2-C 模型，计算到 TWEAK 的最短重原子距离、
   是否在 ≤5 Å 界面内、游离受体与复合物中的 SASA（PyMOL `get_area`，`dot_solvent=1`），三个 Fn14 拷贝分别计算。
   脚本内置残基身份断言（W42/R56/D45/K48/M50/D62），不符即报错。

## 6. 产出文件

- `tables/fn14_binders.tsv` — 主表，13 条抗体及抗体衍生物（含 `binder_lineage_id`、`discovery_campaign_id`）
- `tables/other_fn14_targeted_constructs.tsv` — 配体类构建体（GrB-TWEAK、Fn14-Fc 等），不产生抗体表位
- `tables/patent_disclosed_binders.tsv` — 6 个专利族，含 VH/VL 序列披露
- `tables/tweak_ligand_binders_excluded.tsv` — 靶向 TWEAK 配体的药物（单独列，避免混淆）
- `tables/epitope_residue_geometry.tsv` — E2 表位残基在 M2 模型中的几何量（3 个拷贝 × 6 个残基）
- `code/map_epitope_residues.py` — 结构映射脚本
- `docs/design.md`（事先规则）、`docs/results_v1.md`（第一版，保留备查）、`docs/results_v2.md`（**现行结论**）、
  `docs/reviews/PR3_GPT_round1.md`（审核记录）

## 7. 主要结果

> **本节是 v1 的说法，多条已被两轮审核推翻。请以 `docs/results_v2.md` 为准。** 要点：
> W42 与 R56 分属两个不同抗体（P4A8 / enavatuzumab）；直接竞争实验**已经存在**（PDL192 几乎不阻断、P4A8 阻断）；
> Bayer 的 TWEAKR-KSPi-ADC 是真实存在的 Fn14 ADC（v1 漏掉是因为没检索 **TWEAKR** 这个名字）；
> ITEM-4 的内吞证据属于偶联物 ITEM4-rGel 而非裸抗体；**VH/VL 序列在专利中是公开的**，
> 所以 v1「暂不具备建模条件」也不成立。
> **2026-11-04 进一步更正（经 PR #5 五轮审核后的最终表述）：** 读到 Biogen 专利 Example 21 Table 2
> （P4A8 界面）后，方位论证已收窄——该**专利报告的混合结构模型**给出的 Fab 足迹横跨 9–139°，
> 单个 Fab 可同时覆盖两个"面"，因此"方位远 → 不竞争"的推理强度下调。
> 更简单的解释是：**P4A8 的表位与 TWEAK 接触残基部分重叠**——
> Table 2 所列的 **10 个**残基中 **6 个**（L46、K48、M50、A57、R58、H60）在 M2 模型里距 TWEAK ≤ 5 Å。
> （先前写作"6 个中 5 个"，是因为当初只转录了 Table 2 的重链 CDR 区块；完整集合是 10 个。）
> 这是**工作假说**，不是已确立的机制：重叠量测自一个**预测**界面，Table 2 本身也是混合模型
> （晶体只解析 50–67，R-factor 46%）。PDL192 一侧仍无结构数据。详见 `docs/results_v2.md`。
>
> **另有一条并列的候选机制：** *Differential C-terminal ECD dependence* —— Bayer WO2014198817A1 的截短实验
> 显示 P4A8 需要 CRD 之外的 C 端 69–80，而 PDL-192 不需要。它回答的是"结构依赖为何不同"，
> **不能**直接解释竞争差异（截短测的是抗体结合，不是阻断 TWEAK 的能力）。


1. **PDB 中没有 Fn14–抗体复合物结构（E1 = 0）**，但 Biogen 专利 WO2009140177A2 Example 21 报告过 P4A8 Fab–Fn14 晶体（3.5 Å，仅解析 50–67，R-factor 46%，界面为混合建模；W42 未被解析）。 公开文献中唯一的残基级表位约束是
   Trebing 2014：PDL192（enavatuzumab）与 P4A8 不能有效结合 **W42A** 和 **R56P** 突变体。
2. **映射到 M2 模型：** W42、R56 都不在 TWEAK 接触面上（6.3–6.9 Å），且 TWEAK 结合后它们的 SASA
   **一点也没有被遮住（0 Å²）**；作为对照，D45/K48/M50/D62 被埋掉 9–111 Å²。
   由此得到可检验假说：enavatuzumab 类抗体的表位与 TWEAK 足迹相邻但不重叠，可能是非竞争性的。
3. **18D1/4G5 能阻断 TWEAK 但不受 W42A/R56P 影响**，提示它们的表位落在 TWEAK 足迹本身——与 PDL192/P4A8 是两个不同位点。
4. **ITEM-4 是唯一有明确内吞证据的抗体**（2 小时内特异内吞），对 ADC 方向最有参考价值。
5. **VH/VL 序列在本轮检索到的文献中都没有公开**，所以暂时无法做可靠的 Fn14–Fab 结构预测。专利未检索。

## 8. 负结果 / 缺口

- 没有 E1 证据；E2 只有一组实验、两个残基。
- 没有任何文献报告 enavatuzumab 与 TWEAK 的竞争结合实验。
- 除 ITEM-4 外，所有条目的内吞性质未建立。
- Trebing 2014 全文未能取得（非开放获取），PDL192 与 P4A8 的突变体数据无法分开。

## 9. 限制与 claim ceiling

见 `docs/results_v1.md` 第 4 节。要点：继承 B32 的全部限制（M2 是预测，不是实验结构）；两个点突变不等于一个表位；
突变导致结合丧失不等于直接接触；证据多为摘要级；专利未检索，"VH/VL 未公开"只应读作"本轮未找到"。
不含 CRC 数据，不支持任何关于抗体在 CRC 中效果的主张。

## 10. 未完成 / 下一步

- [x] 检索专利：**6 个专利族含 VH/VL 序列**（`tables/patent_disclosed_binders.tsv`），建模可行
- [x] 取得三篇关键文献全文并逐条核对（经 PMC 网页，不是 API）
- [x] 核对 Kyowa Kirin 的 aa 30–50 权利要求（已读权利要求原文）
- [x] 冻结标准写定并满足（`docs/freeze_criteria.md`）
- [ ] **下一阶段：用 PDL192（VH/VL = SEQ ID 3/4）与 P4A8（2/5）建 Fn14–Fab 模型，检验方位解释**——
      这是有实验标准答案的检验（PDL192 不竞争、P4A8 竞争）
- [ ] 补 Bayer 2018 系列 ADC（ADC 1.1–1.4、2.1、2.2）
- [ ] 本轮一手文献登记 REF 编号
- [ ] 若有序列：AF3 Fn14–Fab 预测（E5，虚线，不得与 E1/E2 混用）

## 10b. 冻结标准

见 `docs/freeze_criteria.md`。范围定义为 *Publicly disclosed Fn14-targeting therapeutic binder and construct
atlas — literature and patent evidence through 2026-11-04*，而不是"穷尽所有曾研究过 Fn14 的抗体"（后者不可验收）。
冻结需连续两轮定向查询无新增**独立** binder lineage；同一抗体的另一个专利文本不算。

## 11. PR 与审核状态

分支 `analysis/20261103-fn14-epitope-atlas`。**PR #4 经 5 轮审核后 APPROVE，未合并（待用户授权）。** PR https://github.com/leezx/TWEAKR-manuscript/pull/3 —— **已由用户授权合并**（merge `cb4ba95`，2026-11-04 00:38 UTC）。

**注意：合并时 GPT 审核尚未返回。** 审核请求已提交到项目的指定审核会话（ChatGPT「深入分析TWEAKR蛋白结构」），回复后再以后续 commit 处理。因此本目录目前是**已合并但未经外部审核**的状态，与 PR #2（两轮审核 + final-head 核对后才合并）不同；按 AGENTS.md §5，其结论在审核完成前不应视为 manuscript canonical evidence。
