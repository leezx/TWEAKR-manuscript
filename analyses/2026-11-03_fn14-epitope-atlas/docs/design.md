# 设计（事先写定）：Fn14 治疗性抗体 / ADC 表位清单

**写于 2026-11-03，开始检索之前。** 评级规则与纳入标准在看到检索结果之前定好；之后若要改，另起修订并注明时间。
前置：B32 已完成并合并（PR #2，merge `762efb1`），M2-C 第一名模型冻结为结构参考坐标。

## 问题

哪些临床或临床前药物**直接结合 Fn14（TNFRSF12A）本身**？其中哪些公开了可用于结构建模的信息
（VH/VL 序列、实验表位、复合物结构）？这些表位与 M2 预测的 TWEAK 结合界面是什么关系？

这一步的产物是**一份可核查的清单**，不是结构预测。只有清单建立之后，才决定对哪些抗体做 AF3 Fn14–Fab 建模。

## 纳入 / 排除

**纳入：** 作用靶点是 Fn14 蛋白本身的抗体、ADC、免疫毒素、抗体偶联递送系统。

**排除（但单独列一张表，避免与 Fn14 靶向药混淆）：**
- 只结合 TWEAK 配体的抗体（如 RG7212/RO5458640、BIIB023）——它们不给出 Fn14 表位；
- 只作用于下游信号（NF-κB、TRAF、YAP 等）的小分子；
- 以 Fn14 为递送配体但不含抗体的纳米颗粒（另记，不进主表）。

**物种：** 记录每条证据所用的 Fn14 物种（人 / 小鼠）。跨物种的残基编号一律换算为人 UniProt Q9NP84 前体编号，
并注明换算依据。

## 证据分级（先定，后检索）

| 级别 | 含义 | 可支持的用途 |
|---|---|---|
| **E1** | 实验解析的 Fn14–抗体复合物结构（X 射线 / cryo-EM / NMR），可直接读出接触残基 | 可直接标注残基级表位 |
| **E2** | 实验表位定位：丙氨酸扫描、定点突变、HDX-MS、肽段扫描、交联质谱 | 可标注残基或区段，须注明方法 |
| **E3** | 竞争结合实验（与 TWEAK 或与另一抗体竞争） | 只能说明**可能**存在空间重叠，不能定位残基 |
| **E4** | 只知道结合 Fn14 胞外区，无更细定位 | 只能进域级表格，不上结构图 |
| **E5** | 由公开 VH/VL 序列做的结构预测（本项目尚未做） | 一律标为 predicted epitope，不得与 E1/E2 混用 |

**硬规则：** 结构图上，E1/E2 用实线边界，E3/E5 用虚线，E4 不画。任何一条记录必须带出处（PMID / 专利号 / 临床试验号）。
无法核实出处的条目不进表，宁可留空。

## 主表字段（`tables/fn14_binders.tsv`）

`agent_id`（本项目编号 FNB-xxx）、`name`、`aliases`、`modality`、`target`（Fn14 / TWEAK / other）、
`sponsor`、`highest_phase`、`clinical_trial_ids`、`agonist_antagonist`、`internalization_evidence`、
`vh_vl_public`（yes/no/patent-only + 出处）、`epitope_evidence_level`（E1–E5）、`epitope_residues_Q9NP84`、
`epitope_method`、`species_tested`、`competes_with_TWEAK`、`primary_refs`（PMID/DOI）、`verification_status`、`notes`。

`verification_status` 只有两个值：`verified`（本项目已核对该字段的一手出处）与 `unverified`（转述，注明来源）。

## 检索来源（按顺序，均记录检索日期与查询式）

1. PubMed / Europe PMC（一手文献，优先）；
2. ClinicalTrials.gov（研发阶段、适应症）；
3. WHO INN 名单（确认靶点与命名）；
4. 专利（仅用于确认 VH/VL 是否公开，不作为生物学证据）。

公共数据库中的二手汇总（如抗体数据库、综述表格）只用于**发现候选**，不作为 `verified` 的依据。

## 本步骤不回答的问题

- 任何抗体在 CRC 或 oncofetal 细胞中的实际效果；
- Fn14 作为 ADC 靶点的安全窗口（需要正常组织表达、膜丰度、内吞效率，均不在本步骤内）；
- 抗体是否会激活 Fn14–YAP（B32 已明确 M2 不能回答 YAP 问题）；
- 预测表位与真实表位是否一致。

## 与 B32 的关系

M2-C 第一名模型
（`DATA/HotData/TWEAKR-oncoFetal/analysis/af3_M2/frozen/af3_M2/m2_tweak3_fn14x3_tmplc/m2_tweak3_fn14x3_tmplc_model.cif`）
是本步骤唯一的结构坐标来源。B32 的 claim ceiling 全部继承：它是结构参考与假说生成资源，不是实验验证的复合物结构。
