# PR #2 GPT 审核 — 第 1 轮

- **审核对象：** HEAD `167a401`（分析目录全文 + M2-C 第一名模型，zip 上传）
- **审核会话：** ChatGPT 项目 TWEAKR-oncoFetal →「深入分析TWEAKR蛋白结构」（PR #2 的指定审核会话，后续各轮复用）
- **时间：** 2026-11-03 18:20（EST）提交，约 5.5 分钟后返回
- **判定：** **REQUEST_CHANGES** —— P0 0 项，P1 3 项，P2 3 项；不需要 HOLD，不要求重跑 M1b/M2，不要求湿实验

## 逐模块判定（审核原表）

| 模块 | 判定 |
|---|---|
| B32 / Fig. TR1 | PASS |
| Fig. TR2 | PASS with caveats |
| M1b 事先注册 / 结果 | ACCEPT / ACCEPT（完整原始结构未随附件提供） |
| M2 事先注册 / 结果 | ACCEPT / PASS（审核方独立解析 cif，复核了第一名模型的四个位点距离、二硫键、沟槽接触和无原子重叠） |
| M2 manuscript claim | 需修改（缺少 TWEAK 侧实验交叉验证） |

审核方还核对了 commit 时间：事先注册 `6caeebe`（21:12 UTC）早于结果 `167a401`（23:04 UTC），但附件中没有 Slurm 时间戳，
不能独立证明运行与首次查看结果的全过程。

## 必改（P1）

1. **P1-1** 补 TWEAK Y176/W231 的外部功能对照（Dhruv 2013, JBC）：Y176 在模型界面上是有价值的旁证，但 W231 也在界面上，
   说明接触不等于功能必需。
2. **P1-2** 超几何"机会水平"只能作描述性几何参照：位点是事先选定的阳性对照，零模型没有控制表面暴露、空间聚集、电荷和结构域；
   0.0034 不是 P 值。"界面整体位置是确定的"改为"给出一致预测、未经实验验证"；25/25 称为采样稳定性。
3. **P1-3** 评估脚本 fail-closed：不完整或不匹配的原子集合必须报错；加失败测试；模板核对同时覆盖 Fn14、TWEAK 和已知复合物。

## 建议（P2）

1. TRAF motif：标注 PIEET（Q9NP84 113–117），引用原始研究。
2. TR2 panel a 加 "illustrative orientation only"。
3. README 去掉"未 push、无 PR"等过时状态；提供 M1b-C 第一名结构或其位置。

## 审核认可的最高 claim

AF3 recapitulates a mutagenesis-consistent TWEAK–Fn14 binding interface — 一个可信的结构工作模型；不确立实验结构、
生理化学计量比、结合能、膜上取向或信号活性；不能声称首次发现该界面（Lammens 2013、Dhruv 2013 已有对接模型）。
合并后的定位是 *Fn14 structural reference and hypothesis-generation resource*，不是 manuscript 的结构机制实验证据。

## 下一步（审核建议）

1. **Fn14 therapeutic epitope atlas**（下一条分支）：Enavatuzumab/PDL192、BIIB036、18D1、ITEM4、Fn14 immunotoxin/ADC；
   核实靶标、VH/VL 可得性、表位证据、激动/拮抗、内吞与递送；anti-TWEAK（如 RG7212）另表。
2. 把已验证位点与候选表位映射到 M2 模型；有公开 VH/VL 的再做 Fn14–Fab AF3。
3. isoform 2 暂缓：审核称 2013 年已有 Fn14-ΔEC（缺 33–67）研究——外源表达不能结合 TWEAK 但仍诱导 NF-κB；
   **出处未给出 PMID，本项目尚未核实**。

## 本项目的处理

全部 6 项已修改，见分析目录 README §15。审核中两条事实性陈述尚未独立核实，已如实标注：
（a）Brown 2003 用 alanine scanning 定位 PIEET（全文未能取得）；（b）2013 年 Fn14-ΔEC 研究（出处待查）。

**第 2 轮更正（2026-11-03）：**（a）用 alanine scanning 定位 PIEET 的是 Han 2003（REF-039），不是 Brown 2003——第 1 轮归属有误；（b）Fn14-ΔEC 研究为 Brown 2013（REF-040）。
