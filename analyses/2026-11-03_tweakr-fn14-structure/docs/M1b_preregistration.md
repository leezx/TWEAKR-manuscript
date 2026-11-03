# M1b 事先注册：AF3 预测 Fn14 胞外区 vs 实验结构 2KMZ

**写于 2026-11-03，提交 AF3 作业之前；结果出来后不改本文件，偏离之处另行记录。**

## 目的

M2（TWEAK₃–Fn14₃ 复合物）要用 AF3 预测的界面来解释 D45/K48/M50/D62。前提是：
AF3 在**不借用 Fn14 实验结构作模板**时，能独立恢复出 Fn14 CRD 的折叠。M1b 只检验这一点。

## 输入

人 Fn14 成熟胞外区 28–80（53 aa，`EQAPGTAPCSRGSSWSADLDKCMDCASCRARPHSDFCLGCAAAPPAPFRLLWP`，
从 UniProt Q9NP84 FASTA 按坐标截取）。单体，无配体。modelSeeds 1–5，每个 seed 5 个 diffusion
sample，共 25 个结构/条件。AF3 3.0.1（O2 `alphafold/3.0.1`，集中权重）。

| 条件 | 模板截止 | 作用 |
|---|---|---|
| **A** | AF3 默认 2021-09-30 | 2KMZ（2011-06-29 公开）**可能**被用作模板 → 只作对照，**不用于判定** |
| **B** | `--max_template_date=2011-06-01` | 2KMZ / 2KN0 排除在外 → **判定条件** |

运行后必须从条件 B 的 `*_data.json` 核对模板列表里没有 2KMZ 和 2KN0；
如果有，说明 B 条件无效，判定为 **BLOCKED**，而不是 PASS。

## 参照尺度（已算，未看任何 AF3 结果）

2KMZ 20 个 NMR 模型两两之间的 CRD（36–67，32 Cα）RMSD：中位数 1.48 Å，IQR 1.23–1.73 Å，最大 2.60 Å。
model 1 中三对二硫键 SG–SG 均为 2.03 Å。

## 判定（条件 B，ranking_score 最高的结构）

1. CRD 36–67 的 Cα RMSD 与 20 个 NMR 模型中最接近的一个 **≤ 2.0 Å**；
2. 与 20 个 NMR 模型的 RMSD 中位数 **≤ 2.6 Å**（不超过 NMR 集合自身的最大离散）；
3. 三对二硫键 C36–C49、C52–C67、C55–C64 全部形成（SG–SG ≤ 2.5 Å）。

三条全满足 → **PASS**，可以进入 M2。任一不满足 → **FAIL**，M2 的界面解读必须改为依赖实验结构
（例如把 2KMZ 当作模板或约束），并记录为负结果。

另外报告（不参与判定）：25 个 sample 中满足 1–3 的比例；CRD 平均 pLDDT；A 与 B 的差别；
N-segment 和 stalk 的 RMSD（这两段在 NMR 中本身柔性大，预期偏差也大）。

## 不回答的问题

M1b 不检验 TWEAK 结合界面，不检验膜上取向，不涉及任何 CRC 数据。
