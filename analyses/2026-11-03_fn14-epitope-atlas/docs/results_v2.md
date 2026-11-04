# 结果 v2：Fn14 治疗性抗体 / ADC 表位清单与结构映射

**2026-11-03 初版（按 PR #3 审核第 1 轮修订）；2026-11-04 修订 2（按 PR #4 审核第 2 轮修订）。**
v1 见 `results_v1.md`（保留，不改写）。规则见 `design.md`（commit `afd15b4`，早于任何检索）。
审核记录：`reviews/PR3_GPT_round1.md`、`reviews/PR4_GPT_round2.md`。

## 0. 两轮修订改掉的错误

### v1 → v2（第 1 轮审核）

| v1 的说法 | 实际情况 |
|---|---|
| W42 与 R56 同属 enavatuzumab/P4A8 的表位约束 | **两者分属不同抗体** |
| "没有 enavatuzumab 与 TWEAK 的竞争实验" | **已有直接竞争实验** |
| 清单中没有 Fn14 ADC | **Bayer TWEAKR-KSPi-ADC 存在**（检索未覆盖 TWEAKR 这个名字） |

### v2 修订 2（第 2 轮审核）——**本项目的一处判断错误**

v2 初版说三篇关键文献"非开放获取、无法独立核实"，并据此把审核转述的结论标为 `review(figure)`。
**这个判断是错的，审核方是对的。** Europe PMC 的 `isOpenAccess: N` 与 PMC **API**（efetch）只返回摘要，
**不等于** PMC 网站没有可读全文。改用 PMC 网站页面抓取后，三篇正文全部取到：

| 文献 | PMC | 本项目取到的正文 |
|---|---|---|
| Salzmann 2013 | PMC3650383 | 199,785 B（提取正文 58,901 字符） |
| Michaelson 2011 | PMC3218533 | 226,003 B（75,527 字符） |
| Trebing 2014 | PMC3929451 | 194,477 B（58,127 字符） |

因此本版**所有关键结论都已由本项目直接核对原文**，不再依赖转述。教训记在第 8 节。

## 1. 清单（13 条抗体及抗体衍生物，`tables/fn14_binders.tsv`）

`binder_lineage_id` 把同一抗体的不同开发形式归并，避免当成独立的表位发现：

| lineage | 成员 | 依据 |
|---|---|---|
| LIN-19.2.1 | enavatuzumab/PDL192 | 鼠源 19.2.1 人源化 |
| LIN-P4A8 | P4A8 = mBIIB036、**BIIB036**、PE38-P4A8、STX2a-PE15-P4A8 | **Michaelson 2011 原文**："The murine antibody mBIIB036 (P4A8) … was subsequently humanized by CDR grafting to generate a drug candidate, BIIB036, with a human IgG1 backbone." |
| LIN-ITEM4 | ITEM-4、ITEM4-rGel、hSGZ、GrB-Fc-IT4 | Cheng 2013 综述（开放获取） |
| LIN-18D1 / LIN-4G5 / LIN-5B6 | 各自独立（共享 `discovery_campaign_id` = ARGENX-LLAMA） | 三者是不同克隆，功能也不同（5B6 不阻断 TWEAK），不能因同一发现平台就并为一个 lineage |
| （未说明） | TWEAKR-KSPi-ADC1/ADC2 | Bayer，抗体身份未公开 |

E1 = **0**（仍没有任何 Fn14–抗体复合物实验结构），E2 = 2，E3 = 3，其余 E4。
`verification_status` 只用事先冻结的两个取值 `verified` / `unverified`，不再出现自造的中间状态。

另有三张关联表：`other_fn14_targeted_constructs.tsv`（配体类构建体，如 GrB-TWEAK、Fn14-Fc，不含抗体表位）、
`tweak_ligand_binders_excluded.tsv`（靶向 TWEAK 配体的药物）、`patent_disclosed_binders.tsv`（见第 7 节）。

## 2. 残基归属与竞争性：已全部核对原文

**Salzmann 2013（JBC 288:13455，PMC3650383）正文原话：**

> "…two mutants of human Fn14 (W42A and R56P) **that do not interfere with ligand binding** but either
> fail to interact with P4A8 (W42A) or with PDL192 (R56P)"
>
> "PDL192 failed to interact with murine Fn14 and the R56P variant but significantly bound to the W42A
> mutant of human Fn14. In contrast, P4A8 did not interact with the latter but recognized murine Fn14 as
> well as R56P variant (Fig. 1A). In conclusion, this confirmed that **PDL192 and P4A8 recognize two
> different epitopes**."
>
> 小节标题："The Anti-Fn14 mAb P4A8 **Efficiently Blocks** TWEAK-induced Cellular Reactions whereas the
> Anti-Fn14 PDL192 **Barely Interferes** with TWEAK Binding"
>
> "Although P4A8 inhibited binding of the GpL-TWEAK fusion protein efficiently, there was **practically no
> competition** between the TWEAK variant and PDL192 for Fn14 binding (Fig. 1F)."

**Michaelson 2011（PMC3218533）：** "binding of TWEAK to Fn14 can be blocked by BIIB036 in a
dose-dependent fashion. Likewise, binding of BIIB036 can be blocked by TWEAK" —— WiDr **结肠癌**细胞，互为竞争。

| 抗体 | 敏感突变 | 是否阻断 TWEAK | 跨物种 |
|---|---|---|---|
| enavatuzumab / PDL192 | **R56P**（仍结合 W42A） | **几乎不阻断** | 不结合小鼠 Fn14 |
| P4A8 = mBIIB036 | **W42A**（仍结合 R56P） | **有效阻断** | 结合小鼠 Fn14 |
| BIIB036（P4A8 人源化） | 未单独定位 | 剂量依赖阻断（双向） | 人/鼠/大鼠/食蟹猴 |
| 18D1 / 4G5 | 均能结合两个突变体 | 阻断（0.2–2 µg/ml） | 人鼠交叉 |
| 5B6 | 均能结合 | 不阻断 | 人鼠交叉 |

**一个关键的实验事实：W42A 与 R56P 本身都不影响 TWEAK 结合。** 这与结构模型独立吻合——
下一节显示这两个残基都没有被 TWEAK 埋藏。

## 3. 结构映射：方位（而非埋藏或距离）解释了竞争性差异

几何量（三个 Fn14 拷贝；审核方用 Biopython Shrake–Rupley 独立复算，数值一致）：

| 残基 | 对应抗体（竞争性） | 到 TWEAK 距离 | 被 TWEAK 埋藏 | **相对足迹方位角** | **到足迹中心距离** |
|---|---|---|---|---|---|
| D45 | （TWEAK 结合参照） | 2.74–2.75 Å | 111 Å² | 22° | 5 Å |
| K48 | （参照） | 2.54–2.55 Å | 61 Å² | 32° | 5 Å |
| M50 | （参照） | 3.71–3.77 Å | 27 Å² | 56° | 5 Å |
| D62 | （参照） | 3.05–3.09 Å | 9 Å² | 50° | 5 Å |
| **W42** | **P4A8（阻断）** | 6.28–6.35 Å | **0 Å²** | **47°** | **6 Å** |
| **R56** | **PDL192（几乎不阻断）** | 6.86–6.89 Å | **0 Å²** | **139°** | **18 Å** |

方位角 = 以 CRD 核心（36–67 的 Cα 质心）为原点，该残基质心方向与四个 TWEAK 结合残基质心方向的夹角。

**结论：埋藏面积和最短距离都分不开这两个残基**（都是 0 Å²，6.3 vs 6.9 Å），**但方位分得很开**：

- **W42（竞争性抗体 P4A8）落在 TWEAK 结合面内**：47°、距足迹中心 6 Å，与四个 TWEAK 结合残基
  （22–56°、5 Å）完全处于同一区域。围绕 W42 结合的 Fab 必然压住 TWEAK 的结合面 → **竞争**。
- **R56（非竞争性抗体 PDL192）在受体的另一侧**：139°、距足迹中心 18 Å。从该方向接近的 Fab 不必与
  TWEAK 冲突 → **不竞争**。

三个拷贝高度一致（W42 47.3/47.3/47.3°；R56 138.9/138.9/139.0°）。

**这是本清单最有价值的结果：M2 预测模型的几何与两个抗体已被实验测定的竞争表型相符，且给出了机制解释——
差别不在于关键残基是否被配体埋藏，而在于表位位于受体的哪一面。** v1 的推论（"未被埋藏 → 非竞争"）
之所以错，正是因为它用了错的判据。

### 第三条独立证据：Kyowa Kirin 专利声明的拮抗抗体表位

WO2020128927A1（Kyowa Kirin）权利要求明确（本项目已读权利要求原文）：该抗体是 **antagonist，且不是 agonist**，
"attenuates the binding of TWEAK to Fn14"，并 "interacts with ... Gly32, Thr33, Ala34, Pro35, **Trp42**,
Ala44, **Asp45**, Leu46, Asp47, **Lys48**, Cys49"。专利定义 subdomain 1 = `APGTAPCSRGSSWSADLDKCM`，
本项目按 Q9NP84 序列核对，正好是 **30–50**。

把这 11 个残基映射到同一个模型（`tables/kyowa_epitope_geometry.tsv`）：

- 方位角 **9–84°，均值 44°**——整片落在 TWEAK 结合面上；
- 11 个中有 6 个与 TWEAK 距离 ≤ 5 Å，其中 D45、D46、K48 被埋 112 / 91 / 62 Å²（D45 与 K48 本身就是 TWEAK 结合残基）；
- 对照：R56（enavatuzumab，**不**阻断）在 139°，完全在这个区间之外。

于是三个相互独立的抗体都落在同一条规律上：

| 抗体 | 表位所在方位 | 是否阻断 TWEAK | 证据 |
|---|---|---|---|
| P4A8 / mBIIB036 | W42，47° | **阻断** | Salzmann 2013 Fig 1F（已读原文） |
| Kyowa Kirin 拮抗抗体 | 32–49，9–84°（均值 44°） | **阻断**（权利要求明示） | WO2020128927A1（已读权利要求） |
| enavatuzumab / PDL192 | R56，139° | **不阻断** | Salzmann 2013 Fig 1F（已读原文） |

**措辞收敛（第 2 轮审核要求）：** 不应说两个残基"局部环境相似"——本项目自己的数据就不支持
（W42 距 D62 仅 4.9 Å，R56 距 D45/D62 有 11–16 Å）。准确的问法是：

> 两个都保持溶剂暴露、且到 TWEAK 最短距离相近（6.3 vs 6.9 Å）的突变敏感残基，为什么对应相反的竞争表型？

本节给出的方位角差异（47° vs 139°）是对这个问题的一个**候选解释**，仍需 Fab 层面的验证。
另外两个待检验的解释是：两个抗体的完整 Fab 足迹不同；Fab 接近角度不同造成不同的空间干涉。
受体在膜上的取向也可能施加额外约束（但 B32 已说明膜取向本身未被确定）。

**仍是预测，不是证明：** 三个拷贝由对称性关联，不是独立观测；两个残基不等于完整表位；Fab 的真实接近角度
未知。要确证需要 Fn14–Fab 复合物结构或建模。

## 4. ADC / 内吞

- **TWEAKR-KSPi-ADC1 / ADC2（Bayer）**：小分子 payload ADC，在 **CT26 结肠癌**模型中有效；次优剂量下只在
  免疫健全小鼠有效，提示免疫机制参与。**与 CRC 最相关。**
- **GrB-Fc-IT4**：人源化抗 Fn14 单链抗体 + 颗粒酶 B。
- **ITEM4-rGel**：2 小时内特异内吞；ITEM4 针对人 Fn14 胞外区制备，结合人与小鼠 Fn14，具弱激动活性（Cheng 2013）。
- v1 说"ITEM-4 是唯一有内吞证据的抗体"**不成立**。
- 临床：**在本轮检索范围内**未找到已进入临床试验的 Fn14 ADC（这是检索范围内的结论，不是对未公开研发的否定）；enavatuzumab Phase 1（NCT00738764，Abbott，2008-07 至 2011-10）是唯一确认的临床记录。

## 5. 一个被修掉的计算 bug

`dist_to_nearest_interface_residue_A` 原先对所有残基都返回约 1.33 Å——那是肽键长度：代码只排除了残基自身，
没有排除序列上相邻的残基，于是当 c±1 在界面内时测到的是共价键长。该列不含任何信息。
已改为排除序列相邻残基（|i−j| ≥ 2），改名 `dist_to_nearest_nonadjacent_interface_residue_A`。
修正后 W42 = 3.11 Å、R56 = 3.19 Å——**这个指标同样分不开两者**，真正有区分力的是第 3 节的方位角。
其余列不受影响。

## 6. 限制（claim ceiling）

1. 继承 B32 全部限制：M2-C 是**预测模型**，不是实验测定的复合物结构。
2. 第 2 节的实验结论现已全部核对原文；**第 3 节的几何与机制解释仍是模型推断**。
3. 单个残基的埋藏情况不能预测抗体竞争性（v1 已被证伪）；方位角能分开本例的两个抗体，但只有 n = 2，
   不能当作普遍规则。
4. 突变导致结合丧失 ≠ 直接接触。W42 仅约 1/3 暴露（84 Å²），W42A 可能通过局部折叠间接起作用；
   R56 高度暴露（225 Å²），更可能是直接接触。
5. 专利未检索，"VH/VL 未公开"应读作"本轮未在文献中找到"。
6. 不含 CRC 数据；不支持任何关于抗体在 CRC 中效果的主张；不涉及正常组织表达与安全窗口。

## 7. 专利：VH/VL 序列确实存在（本轮新增）

第 2 轮审核做了专利检索，本项目逐条核对了 Google Patents 记录（标题、受让人、权利要求文字），
结果见 `tables/patent_disclosed_binders.tsv`：

| 专利 | 受让人 | 序列披露 |
|---|---|---|
| **US20210388096A1** | Astellas Pharma | VH/VL 的 CDR 以 SEQ ID NO: 2 / 4 的残基区间明确定义 |
| WO2020128927A1 | Kyowa Kirin | VH CDR3 = SGWFTY（SEQ ID NO: 121）；**本项目已核对权利要求**：antagonist 且非 agonist，attenuates TWEAK binding，表位 = subdomain 1（aa 30–50）中的 Gly32/Thr33/Ala34/Pro35/Trp42/Ala44/Asp45/Leu46/Asp47/Lys48/Cys49 |
| WO2022155705A1 / WO2016061632A1 | La Trobe University | VH 为 SEQ ID NO: 8 等 |
| WO2012122513A2 | Omeros | VH 为 SEQ ID NO: 82 |
| WO2015189143A1 | Bayer Pharma | 可能是 TWEAKR-KSPi ADC 的抗体来源 |

**这改变了 v1/v2 初版的结论。** v1 说"没有公开的 VH/VL，因此暂不具备建模条件"——那只对**文献**成立；
**专利里有**。Fn14–Fab 建模现在是可行的。

专利披露**不升级**为 E2/E3 实验证据，单列一表。

## 8. 下一步

1. **用专利序列做 Fn14–Fab 建模**，检验第 3 节的方位解释。这是一个**有实验标准答案**的检验
   （PDL192 不竞争、P4A8 竞争），不是预测未知结果。Astellas 的 US20210388096A1 序列最明确。
2. 补 Bayer 2018 年系列 ADC（ADC 1.1–1.4、2.1、2.2），目前只记录了 2022 年的 ADC1/ADC2。
3. 本轮一手文献登记 REF 编号。

## 9. 方法教训（记入项目规范）

**不要用 Europe PMC 的 `isOpenAccess` 标志或 PMC API 的返回长度来判断全文是否可得。**
本项目因此误判三篇关键文献"无法核实"，把已经可以核对的一手结论降级为转述。
正确做法：API 只返回题录/摘要时，再抓 `https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/` 页面确认。
