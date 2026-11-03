# M2 结果：AF3 预测的 TWEAK₃–Fn14₃ 胞外复合物

**判定：PASS**（判定条件 M2-C，依据 `M2_preregistration.md`；判定标准未在看到结果后改动）。
评估脚本 `code/af3_M2/evaluate_M2.py`；表格在 `tables/M2_{summary,per_sample,interface,templates,c_vs_d}.tsv`。

## 评估脚本更正（看到结果后，只改代码、不改标准）

第一次运行时，条件 4 的 CRD RMSD 在全部 150 条 Fn14 链上都是 0.0。原因是 PyMOL `cmd.rms` 按原子标识（含链名）配对：
复合物中的 Fn14 是 D/E/F 链，2KMZ 是 A 链，因此一个原子也没有配上，函数报 "No atoms selected" 后返回 0。
改为显式的 Cα Kabsch 计算（32 个 Cα，36–67，逐个核对残基编号和残基名后再配对），标准仍是"20 个 NMR 模型的中位数 ≤ 2.6 Å"。
用 PyMOL `rms` 交叉验证：把链名改成 A 后再算，第一名模型 D 链的中位数为 1.594 Å，与 Kabsch 结果一致。
另外把 2RPJ（2009 年的 Fn14 CRD NMR 结构）补进 Fn14 排除列表；两个条件都没有用到它，判定不变。

## 模板核对（BLOCKED 规则）

| 条件 | TWEAK 链（A–C）的模板 | Fn14 链（D–F）的模板 | Fn14 / TWEAK–Fn14 实验结构 |
|---|---|---|---|
| **M2-C（2007-12-31）** | 1IQA、1JTZ（RANKL），1RJ7、1RJ8（EDA-A1/A2） | 1XU1（APRIL–TACI）、2EBR、1VVC、1DAX | **无** |
| M2-D（2021-09-30） | 1RJ8、4ZCH（APRIL–BAFF 异源三聚体）×2、6ZT0（Eiger–Grindelwald） | 2EQP、2KN0、4KT1 ×2 | 2EQP、2KN0（Fn14 单体） |

M2-C 的 TWEAK 模板都是 TNF 家族同源物，不是 TWEAK；Fn14 模板与 M1b-C 相同。因此不判 BLOCKED。

**PDB 中不存在实验测定的 TWEAK–Fn14 复合物**（2026-11-03 按 UniProt 检索 RCSB）：
Fn14（Q9NP84）只有 2EQP、2KMZ、2RPJ（都只有胞外区/CRD，单独成像）；TWEAK（O43508）只有 4HT1（2013，TWEAK 与中和抗体 Fab）。
所以 AF3 不可能直接"记住"这个复合物。

## 判定（M2-C，ranking_score 最高：seed 2 / sample 0，ranking_score 0.955，iptm 0.84，ptm 0.86）

| # | 标准 | 结果 | 是否满足 |
|---|---|---|---|
| 1 | 3 对 TWEAK–TWEAK `chain_pair_iptm` ≥ 0.70 | 最小 0.87 | 是 |
| 2 | 每条 Fn14 与 TWEAK 的最佳 `chain_pair_iptm` ≥ 0.50，且 ≥ 5 个残基 ≤ 4.5 Å | iptm 0.71–0.72；12 个接触残基 | 是 |
| 3 | ≥ 2 个拷贝中，D45/K48/M50/D62 至少 3 个 ≤ 5.0 Å | **3/3 个拷贝，4 个位点全部在界面上**（最近距离 D45 2.74–2.75、K48 2.54–2.55、M50 3.71–3.77、D62 3.05–3.09 Å） | 是 |
| 4 | 每个拷贝的 CRD Cα RMSD（vs 2KMZ 20 个模型）中位数 ≤ 2.6 Å | 1.59–1.60 Å | 是 |

**几何参照（描述性，不是显著性检验；按审核第 1 轮 P1-2 改写）：** 第一名模型中，Fn14 28–80 平均 27%（约 14/53）的残基落在
≤ 5 Å 界面内。若从 53 个残基中随机取 4 个，至少 3 个落在界面上的超几何比例为 0.052，4 个全部落在界面上为 0.0034。
这些数字只描述"界面占 Fn14 片段多大比例"，**不能**当作 P 值，也不能用来估计 AF3 独立发现真实界面的概率，原因有三：
(1) 四个位点是事先从突变文献中选出的阳性对照，不是随机抽取的；(2) 零模型把所有残基视为可互换，没有考虑表面暴露、
空间聚集、电荷或所在结构域——结合位点本来就集中在 CRD 表面；(3) 3 个拷贝由对称性相互关联，不是 3 次独立观测。

## 稳健性（不参与判定）

| | M2-C | M2-D |
|---|---|---|
| 满足 1–4 的 sample（模型采样稳定性，不是 25 次独立验证） | 25/25 | 25/25 |
| ranking_score | 0.921–0.955 | 0.922–0.956 |
| iptm / ptm | 0.84 / 0.86（全部 sample） | 0.84 / 0.86 |
| Fn14 最佳链 iptm | 0.70–0.72 | 0.71–0.73 |
| 4 个位点全部 ≤ 5 Å 的 Fn14 拷贝（25 个模型 × 3 个受体） | 75/75 | 75/75 |
| 位点最近距离的最大值 | D45 2.75，K48 2.62，M50 3.96，D62 3.17 Å | D45 2.74，K48 2.64，M50 3.73，D62 3.20 Å |
| CRD RMSD 中位数（范围） | 1.62（1.59–1.67）Å | 1.62（1.59–1.65）Å |
| 同时接触两条相邻 TWEAK 链（"沟槽"模式） | 75/75 | 75/75 |

M2-C 与 M2-D 第一名模型之间的 Cα RMSD：整个复合物 1.01 Å；TWEAK 链 0.56–0.81 Å；Fn14 链 0.94–1.11 Å（`M2_c_vs_d.tsv`）。
是否提供 Fn14 模板，几乎不改变复合物的结构。

## TWEAK 侧的事后核对（未事先注册，不参与判定；按审核第 1 轮 P1-1 补充）

Dhruv 等（2013，JBC，REF-035）的 TWEAK 定点突变实验显示：**Y176** 突变后 TWEAK 不再结合 Fn14，也不再诱导 NF-κB，
但三聚化不受影响；**W231** 突变则不影响结合。两者在 M2 模型中与 Fn14 的最短重原子距离如下
（`code/af3_M2/posthoc_tweak_sites.py` → `tables/M2_posthoc_tweak_sites.tsv`）。注意分母：这里的 75 是 TWEAK 链观测（25 个模型 × 3 条配体链），
与上文 D45/K48/M50/D62 的 75 个 Fn14 拷贝（25 个模型 × 3 个受体）不同；两者都不是 75 次独立实验：

| TWEAK 残基 | 实验结果（REF-035） | M2-C 最短距离（中位数，范围） | M2-D | ≤ 5 Å 的 TWEAK 链观测（n = 75 = 25 个模型 × 3 条 TWEAK 链；M2-C，M2-D） |
|---|---|---|---|---|
| Y176 | 突变后丧失结合 | 2.87（2.73–2.97）Å | 2.86（2.72–2.93）Å | 75/75，75/75 |
| W231 | 突变不影响结合 | 3.39（3.26–3.68）Å | 3.35（3.22–3.50）Å | 75/75，75/75 |

第一名模型中，Fn14 D62 与 TWEAK Y176 最近约 3.05 Å。

**解读：** 模型把实验证明必需的 Y176 放在界面上，这是独立于判定条件的 TWEAK 侧旁证。但 W231 同样在界面上，
说明**接触距离本身不能区分功能必需的热点和普通接触残基**。M2 可以说"恢复了已知的重要接触区域"，
不能据接触距离指认哪些残基是结合热点。

**先前工作：** 基于 TNF/TNFR 同源结构的 TWEAK–Fn14 对接模型已有发表（Lammens 2013，REF-038；Dhruv 2013，REF-035），
且 Y176 锚定位点已经功能验证。M2 提供的是采样一致、无 Fn14/TWEAK 模板的现代结构预测，**不能声称首次发现这一界面**。

## 界面残基（M2-C 第一名模型，≤ 5 Å，UniProt 编号；供后续与文献比对）

- **Fn14 侧（3 个拷贝相同）：** 43–48、50、54、57、58、60–63（D 链另含 32）。都在 CRD 内，位于 C36–C49 与 C52–C67 两个二硫键模块。
- **TWEAK 侧：** 每条 Fn14 同时接触两条 TWEAK 链：
  - 主要一侧：171、173–178、180、190、192、194、229–232；
  - 相邻一侧：120、(170)、205–207、235。

## 限制（claim ceiling）

1. **这是预测，不是实验结构。** PASS 的意思是：AF3 预测的界面与已报道的突变数据（Fn14 D45/K48/M50/D62，REF-034；
   TWEAK Y176，REF-035）相符，可以作为后续界面分析的工作模型。它不等于实验测得的复合物结构，界面的细节
   （侧链朝向、精确原子接触）仍需实验验证。突变"必需"也不等于"直接接触"；REF-034 用的是小鼠 Fn14。
2. **四个位点是在注册之前就选定的阳性对照，不是盲测。** 它们来自文献，而 AF3 可能从 TNF/TNFR 家族的同源复合物（如 APRIL–TACI）
   学到了类似的结合几何。PDB 中没有 TWEAK–Fn14 复合物，但同源结构的影响无法排除。
3. Fn14 链的 iptm（0.70–0.72）明显低于 TWEAK 三聚体（≥ 0.86）。模型对整体结合位置给出了一致的预测，
   但具体界面仍未经实验结构验证，细节的可信度中等。
4. 3:3 化学计量比是输入时设定的，AF3 的置信度不能证明生理状态下就是 3:3。
5. 不涉及膜上取向、受体聚集、结合亲和力，也不涉及任何 CRC 生物学问题。

**可以写入内部结果的最高表述（审核第 1 轮认可）：**

> AlphaFold 3 predicted a symmetric TWEAK₃–Fn14₃ extracellular complex, with three Fn14 receptors occupying grooves between
> adjacent TWEAK subunits. The predicted interface accommodates all four previously reported Fn14 residues implicated in
> high-affinity TWEAK binding (D45, K48, M50 and D62) and places the experimentally supported TWEAK residue Y176 at the
> receptor interface. The binding geometry was consistent across prediction samples and template conditions. These results
> support a plausible structural working model of the TWEAK–Fn14 interaction, but do not establish an experimentally
> determined complex structure, physiological stoichiometry, binding energetics, membrane orientation or signaling activity.

**不得上升为：** AF3 证明了天然 3:3 复合物、精确原子接触、Fn14 聚集机制、特定抗体的竞争表位，或 TWEAKR–YAP 的直接信号联系；
也不得声称首次发现该界面。

**对后续工作的含义：** M2-C 第一名模型可作为探索性的 Fn14–TWEAK 界面结构底图（例如映射表位），使用时要附上第 1–5 条限制。
它是 structural reference / hypothesis-generation resource，不是 manuscript 中的结构机制实验证据。

## 溯源

- O2 作业：MSA/模板 58464436（short，01:05:36），推理 58464437（gpu l40s，00:13:39）；2026-11-03 完成。
- O2 冻结目录：`/n/data1/dfci/medonc/sethi/lab/zhixin/TWEAKR-oncoFetal/af3_M2`。
- 本地副本：`DATA/HotData/TWEAKR-oncoFetal/analysis/af3_M2/af3_M2_frozen.tar.gz`
  （sha256 `448014ab…80fd28`，与 O2 端一致；通过 o2-sh 会话分 3 段传输，每段 sha256 均已核对）和解压后的 `frozen/af3_M2/`。
  对照 O2 端 `manifest_sha256.txt` 逐个核对，161/161 个文件一致。
- 评估环境：PyMOL open-source 虚拟环境（`SOFTWARES/tools/pymol-open-source/.venv`），运行约 20 秒。
- 防错（审核第 1 轮 P1-3）：几何与模板检查集中在 `code/af3_M2/m2_checks.py`。空选择、原子数不符或残基身份不一致时一律报错，
  不返回数值；模板同时按 Fn14、TWEAK、TWEAK–Fn14 复合物三类核对（任一出现即 BLOCKED，比事先注册的规则更严，两个条件的判定都不变）。
  单元测试 `code/af3_M2/test_m2_checks.py`（4 项，含"0 个配对原子必须报错"）。重跑后，除 `M2_summary.tsv` 新增两列模板报告外，
  其余结果表逐字节不变。
