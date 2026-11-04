
## 2026-11-04 — PR #4 审核第 2 轮：我判断错了，三篇文献其实可读（WL-20261104-FN14-009）

**最重要的一条：本项目的判断错误。** 我在第 2 轮提交中告诉审核方，三篇关键文献非开放获取、无法独立核实，
并据此把已有一手依据的结论降级标注。审核方指出这是错的。**复核后确认审核方正确：**
Europe PMC 的 `isOpenAccess: N` 和 PMC API 只返回摘要，不等于 PMC 网站没有全文。
改抓网页后三篇正文（194–226 KB）全部取到，逐条核对，结论与审核转述一致。已记入记忆与 results_v2 第 9 节。

**核对原文后确认.** Salzmann 2013 原话："two mutants of human Fn14 (W42A and R56P) that do not interfere with
ligand binding but either fail to interact with P4A8 (W42A) or with PDL192 (R56P)"；小节标题直接写
"P4A8 Efficiently Blocks … whereas PDL192 Barely Interferes with TWEAK Binding"；Fig 1F："practically no
competition between the TWEAK variant and PDL192"。Michaelson 2011："mBIIB036 (P4A8) … humanized by CDR
grafting to generate … BIIB036"，Fig 2B 在 WiDr 结肠癌细胞中双向竞争。

**新结果：方位角解释了竞争性差异。** 埋藏面积（都是 0 Å²）和最短距离（6.3 vs 6.9 Å）都分不开 W42 与 R56，
但以 CRD 核心为原点看方位：**W42 在 TWEAK 结合面内（47°、距足迹中心 6 Å，与四个结合残基的 22–56°／5 Å 同区），
R56 在受体另一侧（139°、18 Å）**。这正好对应 P4A8（W42 敏感）竞争、PDL192（R56 敏感）不竞争。
三个拷贝一致到 0.1°。实验上两个突变本身都不影响 TWEAK 结合，与"都未被埋藏"独立吻合。

**专利推翻了"不能建模"的结论.** 审核的专利检索找到六个族，本项目逐条核对 Google Patents 确认：
Astellas US20210388096A1（VH/VL = SEQ ID NO: 2/4）、Kyowa Kirin、La Trobe ×2、Omeros、Bayer。
v1 说"没有公开 VH/VL"只对文献成立，专利里有。Fab 建模现在可行。

**修掉一个 bug.** `dist_to_nearest_interface_residue_A` 对所有残基都返回约 1.33 Å——肽键长度，
因为只排除了残基自身、没排除序列相邻残基。已改为 |i−j| ≥ 2 并改名。该列原先不含任何信息。

**其他修改.** 18D1/4G5/5B6 拆为三个独立 lineage（功能不同，不能按发现平台归并）；ITEM-4 的内吞证据
撤回到 ITEM4-rGel（属偶联物而非裸抗体）；GrB-TWEAK 移出抗体表；`verification_status` 回归事先冻结的两个取值。

**状态：** PR #4 未合并，待第 3 轮审核。
