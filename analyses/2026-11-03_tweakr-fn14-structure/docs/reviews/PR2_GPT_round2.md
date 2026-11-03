# PR #2 GPT 审核 — 第 2 轮

- **审核对象：** HEAD `ff9b7ca`（分析目录全文、167a401→ff9b7ca diff、M2 全部 50 个模型、M1b-C 全部 25 个模型、2KMZ）
- **审核会话：** 同第 1 轮（ChatGPT 项目 TWEAKR-oncoFetal →「深入分析TWEAKR蛋白结构」）
- **时间：** 2026-11-03 18:36（EST）提交
- **判定：** **APPROVE** —— P0 0，P1 0，P2 4（文档与 manifest 清理）。允许合并；不允许作为 manuscript 结构机制证据；
  允许作为后续 Fn14 结构研究、表位映射与假说生成的参考资源。

## 独立复核（审核方自行解析原始文件）

| 项 | 结果 |
|---|---|
| M2-C / M2-D 全部模型，四项判定 | 25/25、25/25 |
| 每条 Fn14 同时接触两条 TWEAK 链 | 25/25、25/25 |
| M2-C 第一名模型四个位点距离 | 与提交值一致（D45 2.742–2.750、K48 2.542–2.552、M50 3.707–3.772、D62 3.054–3.092 Å） |
| M1b-C 全部 25 个模型 | 25/25 通过；最近构象 CRD RMSD 1.101–1.529 Å，中位数 1.550–1.969 Å，二硫键最大 2.264 Å |
| `test_m2_checks.py` | 实际运行，4 tests passed |
| Fig. TR1 / TR2（PNG） | PASS；"Illustrative orientation only" 足够醒目 |

## P2（建议合并后修正；本项目已在本轮清理，见 README §16）

1. PIEET 的 alanine scanning 出处是 **Han 2003**（PMID 12767899），不是 Brown 2003——审核方更正了自己第 1 轮的归属。
2. `M2_summary.tsv` / `M2_per_sample.tsv` 仍有 `chance_P` 字段名，应改名。
3. 两种 75/75 分母（Fn14 拷贝 vs TWEAK 链观测）应在表头写清。
4. `manifests/outputs.tsv` 有 9 个路径重复，应整理为唯一当前版本或明确为版本历史。另：本次 zip 未含 PDF/SVG 导出，未能检查矢量文件。

## 文献核实（回答第 1 轮遗留问题）

- (a) Han S et al. *Biochem Biophys Res Commun* 2003;305:789–796（PMID 12767899）——摘要明确 alanine scanning 定义 PIEET。→ REF-039
- (b) Brown SA, Cheng E, Williams MS, Winkles JA. *PLoS One* 2013;8:e65248（PMID 23750247）——Fn14-ΔEC。→ REF-040
  审核转述的全文要点：MDA-MB-231/U87 RT-PCR 检出 105-bp 缺失转录本（预测缺 33–67）；不能结合 TWEAK；过表达可激活 NF-κB 并自聚集；
  未用 Western 确证内源蛋白；Cys122 二聚体在裂解中形成；需将 AB035481 product B 与 Q9NP84-2/BAB17850 比对后再统一命名。

## 冻结的 claim ceiling（审核建议原文）

> AlphaFold 3 consistently predicts a symmetric TWEAK₃–Fn14₃ extracellular assembly across independent model samples and template
> conditions. The predicted interface accommodates the four previously reported Fn14 residues implicated in high-affinity TWEAK binding
> (D45, K48, M50 and D62), as well as the experimentally validated TWEAK anchoring residue Y176. The predicted architecture is consistent
> with previously reported mutagenesis and homology-modeling studies and provides a structural reference for subsequent epitope mapping and
> interaction studies. However, this model does not establish the experimentally determined complex structure, physiological stoichiometry,
> binding affinity, membrane orientation or downstream signaling activity.

不得越界：3:3 是输入设定；M2 不证明 Fn14 clustering 激活 YAP；M2 不证明任何抗体/ADC 的实际表位；不声称首次发现界面。

## 审核建议的下一步

合并 PR #2，冻结 M2-C 第一名结构，研究重心转向 **Fn14 therapeutic epitope atlas**；不再扩大 M2。
