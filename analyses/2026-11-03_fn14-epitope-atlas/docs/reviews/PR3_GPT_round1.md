# PR #3 GPT 审核 — 第 1 轮

- **审核对象：** HEAD `55bb9ed`（分析目录全文 + M2-C 第一名模型）
- **审核会话：** ChatGPT 项目 TWEAKR-oncoFetal →「深入分析TWEAKR蛋白结构」（与 PR #2 同一会话）
- **时间：** 2026-11-03 19:33（EST）提交
- **判定：** **REQUEST_CHANGES** —— P0 0，P1 4，P2 2。设计方向与预注册规则可保留；需改的是证据清单与生物学解释，不是 AF3 结构模型。

**重要时序说明：** 用户于 2026-11-04 00:38 UTC 授权合并 PR #3，当时本审核尚未返回。审核随后发现 3 处实质错误
（见下），修订通过 PR #4 提交。

## 独立复核结构计算：PASS

审核方用 Biopython Shrake–Rupley 独立计算 SASA 并复算距离，与本项目结果一致：

| 残基 | 本项目报告 | 审核独立计算（D 链） | 审核算 SASA 埋藏 |
|---|---|---|---|
| W42 | 6.28 Å | 6.282 Å | 0.0 Å² |
| R56 | 6.86 Å | 6.864 Å | 0.0 Å² |
| D45 | 2.75 Å | 2.747 Å | 112.4 Å² |
| K48 | 2.54 Å | 2.542 Å | 63.1 Å² |
| M50 | 3.71 Å | 3.707 Å | 29.1 Å² |
| D62 | 3.05 Å | 3.054 Å | 7.6 Å² |

结论保留：在 M2-C 中 W42、R56 不与 TWEAK 形成 5 Å 接触，SASA 无可检测减少。但这是两个残基的几何性质，
不是完整表位的几何性质。

## P1（必改，均已在 PR #4 处理）

1. **P1-1 纠正抗体身份与残基归属。** Salzmann 2013 Fig 1A：PDL192 对 R56P 敏感、仍结合 W42A；P4A8 相反。
   Michaelson 2011：BIIB036 是 P4A8 经 CDR grafting 人源化而来，不是独立抗体。要求加 `binder_lineage_id`。
2. **P1-2 补入已有的直接竞争实验。** Salzmann 2013 Fig 1F：PDL192 几乎不阻断 TWEAK 结合；P4A8 有效阻断。
   Michaelson 2011 Fig 2B：BIIB036 剂量依赖阻断。"本项目最想回答的问题已经存在直接实验答案。"
3. **P1-3 补齐真实存在的 Fn14 ADC 与内吞研究。** Bayer TWEAKR-KSPi-ADC1/ADC2（CT26 结肠癌模型）；
   GrB-Fc-IT4 / GrB(C210A)-Fc-IT4 的内吞数据；hSGZ 是以人源化 ITEM-4 scFv 为基础。
   因此"ITEM-4 是唯一有内吞证据的抗体"不成立。建议把 atlas 拆成 lineage 表与 construct 表。
4. **P1-4 按已知实验重写结构假说。** v1 的"两残基都未被埋 → 可能非竞争性"不再成立：P4A8 对 W42A 敏感、
   W42 未被埋，但 P4A8 确实阻断 TWEAK。更有价值的问题变成：为什么两个都未被埋的敏感位点分别对应
   竞争性与非竞争性抗体？M2 的作用应定位为**解释已观察到的竞争性差异**，而不是预测未知结果。

## P2

1. E1–E5 框架可保留，不需重新定义；但 E2 应精确定义为 *mutation-sensitive binding determinant*，而不是 epitope。
2. 审核称 Trebing 2014 全文在 PMC（PMC3929451）可获取，Figure 1B 直接给出 W42A/R56P 结合结果。
   **本项目复核：Europe PMC 标 `isOpenAccess: N`，PMC efetch 只返回题录与摘要（约 9.6 KB，无正文）。
   三篇关键文献（PMC3929451、PMC3650383、PMC3218533）均如此。** 因此本项目仍无法独立核实图级结果。

## 本项目的处理（PR #4）

- 全部 4 项 P1 已改；P2-1 的措辞已采纳。
- **诚实标注：** 所有来自审核转述的图级结果（竞争实验、W42/R56 归属、P4A8→BIIB036 lineage）在表中标为
  `verified(abstract) + review(figure)`，并在 `results_v2.md` 第 6 节写明本项目未能独立核实、原文非开放获取。
- 本项目**独立核实**（摘要级）的新增项：Sommer 2022（PMID 35154909，TWEAKR-KSPi-ADC，CT26 结肠癌）、
  Zhou 2014（PMID 25239934，GrB-Fc-IT4）。
- 补做同义词完整检索（Fn14 OR TWEAKR OR TNFRSF12A OR CD266），这是 v1 漏掉 Bayer ADC 的根因。
