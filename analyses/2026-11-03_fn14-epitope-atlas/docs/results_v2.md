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

证据分级计数（13 条）：**E1 = 0，E2 = 2，E3 = 4，E4 = 7**。
（第 4 轮审核指出此处原先漏改 E3 计数——BIIB036 改为 E3 后应为 4，不是 3。）

**E1 = 0 需要加一句限定（第 4 轮新发现）：** PDB 中确实没有 Fn14–抗体复合物结构，但
**Biogen 专利 WO2009140177A2 的 Example 21 报告了鼠源 P4A8 Fab 与人 Fn14 胞外区的晶体**
（3.5 Å，P21，每个不对称单位 2 个复合物）。本项目读了该段原文，发现**审核转述省略了几个决定性的限定**：

> "Only residues **50-67** of Fn14's cysteine rich domain could be accounted for in the electron density maps."
> R-factor **46%**；"Missing from the density were H3 CDR and the N-terminal residues of Fn14 ectodomain."
> 界面表是把 NMR 结构叠合上去、再用 ROSETTA 建 H3 CDR 并做约束优化之后得到的。

所以这是一次真实的晶体学实验，但**不是精修完成、完整可解析的复合物结构**；R-factor 46% 属于未精修水平。
**尤其关键：P4A8 所依赖的 W42 落在未被解析的 50–67 区间之外**，因此这块密度既不能证实也不能推翻 W42 表位归属。
按事先冻结的分级，它不计为 E1；在表中单列并写明上述限定。
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

## 3. 结构映射：表位在受体的哪一面，与竞争性差异一致

**证据分层（按 `design.md` 修订 1）：** 本节用到三类证据——
**A 同行评议实验**（Salzmann 2013 的突变与竞争数据）、**B 专利报告的实验**（Bayer 丙氨酸扫描、Biogen 晶体）、
**C 专利权利要求**（Kyowa 表位主张）。只有 A 计入冻结的 E1–E5 体系；B、C 是事后补充的佐证。
下文每处都标明属于哪一层。

**代表性拷贝：** 下表角度与距离取 Fn14 的 **D 链**（三个拷贝由对称性关联，数值差 ≤ 0.1°，不是三次独立观测）。

**术语（按第 3 轮审核更正）：** 下文的"参考区域"指 **D45/K48/M50/D62 四个残基的质心**
（four-residue TWEAK-binding reference patch），**不是**已解析的 TWEAK–Fn14 原子接触面。
"方位角"是从指定的 CRD 几何中心向外的径向夹角，**不是**抗体的接近角度，也不是表面测地角。

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
  （22–56°、5 Å）完全处于同一区域。围绕 W42 结合的 Fab **很可能**与 TWEAK 的结合面重叠 → 与观察到的竞争相符（不是必然，Fab 姿态未知）。
- **R56（非竞争性抗体 PDL192）在受体的另一侧**：139°、距足迹中心 18 Å。从该方向接近的 Fab **不必然**与 TWEAK 冲突 → 与观察到的不竞争相符。

三个拷贝高度一致（W42 47.3/47.3/47.3°；R56 138.9/138.9/139.0°）。

**对原点选择的稳健性（第 3 轮审核要求，本项目已复算；`tables/orientation_sensitivity.tsv`）：**

| 原点定义 | L46 | D47 | W42 | R56 |
|---|---|---|---|---|
| CRD Cα 质心（正文所用） | 9° | 22° | 47° | 139° |
| CRD 重原子质心 | 11° | 20° | 46° | 145° |
| 全 ECD 重原子质心 | 6° | 18° | 30° | 108° |
| **到参考区域质心的距离（不依赖原点）** | **3.5 Å** | **6.9 Å** | **6.0 Å** | **17.9 Å** |

角度的绝对值随原点变化，**但"在结合面上 vs 在另一侧"的区分不变**。不依赖原点的距离指标更适合直接引用。

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
- 11 个中有 6 个与 TWEAK 距离 ≤ 5 Å，其中 D45、**L46**、K48 被埋 112 / 91 / 62 Å²（D45 与 K48 本身就是 TWEAK 结合残基；L46 正是 Bayer 专利所述 TWEAK 结合所依赖的残基）。**更正：先前误写作 D46，残基 46 是亮氨酸。**
- 对照：R56（enavatuzumab，**不**阻断）在 139°，完全在这个区间之外。

于是三个相互独立的抗体都落在同一条规律上：

| 抗体 | 表位所在方位 | 是否阻断 TWEAK | 证据 |
|---|---|---|---|
| P4A8 / mBIIB036 | W42，47° | **阻断** | Salzmann 2013 Fig 1F（已读原文） |
| Kyowa Kirin 拮抗抗体 | 32–49，9–84°（均值 44°） | **阻断**（权利要求明示） | WO2020128927A1（已读权利要求） |
| enavatuzumab / PDL192 | R56，139° | **不阻断** | Salzmann 2013 Fig 1F（已读原文） |

### 第四条独立证据：Bayer 专利的丙氨酸扫描，结论与本模型一致

WO2015189143A1（Bayer）对 CRD 做了完整丙氨酸扫描（S37A、R38A、S40A、W42A、S43A、D45A、D47A、K48A、
D51A、S54A、R56A、R58A、P59A、H60A、S61A、D62A、F63A、L46A），**专利正文原话**（本项目已读）：

> "TWEAK binding depends on L46 (Pellegrini et al), TPP-2090 binding on D47 and PDL-192 binding on R56.
> **PDL-192 binds opposite of the TWEAK ligand binding site, TPP-2090 binds directly to the TWEAK ligand site.**"
>
> "PDL-192 shows moderate agonistic activity and binds dependent of R56 to the cysteine rich domain
> **but opposite to the TWEAK ligand site**."

**这是独立于本项目、用实验方法（丙氨酸扫描 + Pellegrini NMR 结构）得到的同一结论。** 本模型给出的
到参考区域质心距离与之完全吻合：L46 3.5 Å、D47 6.9 Å（都在结合面上）vs R56 17.9 Å（另一侧）。

于是四条相互独立的证据指向同一几何：

| 决定簇 | 对应分子 | 文献/专利的定位 | 本模型：到参考区域质心 |
|---|---|---|---|
| L46 | TWEAK 配体本身 | 配体结合位点 | 3.5 Å |
| D47 | TPP-2090（Bayer） | "binds directly to the TWEAK ligand site" | 6.9 Å |
| W42 | P4A8 | 实验上阻断 TWEAK | 6.0 Å |
| 32–49 | Kyowa Kirin 拮抗抗体 | 权利要求：attenuates TWEAK binding | 整片在结合面上 |
| **R56** | **PDL192 / enavatuzumab** | **"binds opposite of the TWEAK ligand binding site"** | **17.9 Å** |

**措辞收敛（第 2 轮审核要求）：** 不应说两个残基"局部环境相似"——本项目自己的数据就不支持
（W42 距 D62 仅 4.9 Å，R56 距 D45/D62 有 11–16 Å）。准确的问法是：

> 两个都保持溶剂暴露、且到 TWEAK 最短距离相近（6.3 vs 6.9 Å）的突变敏感残基，为什么对应相反的竞争表型？

本节给出的空间分离（到参考区域质心 6.0 vs 17.9 Å）是对这个问题的一个**候选解释**，仍需 Fab 层面的验证；
但它已经与 Bayer 用实验独立得到的"PDL-192 binds opposite"相符，所以不只是模型内部自洽。
另外两个待检验的解释是：两个抗体的完整 Fab 足迹不同；Fab 接近角度不同造成不同的空间干涉。
受体在膜上的取向也可能施加额外约束（但 B32 已说明膜取向本身未被确定）。

**仍是预测，不是证明：** 三个拷贝由对称性关联，不是独立观测；两个残基不等于完整表位；Fab 的真实接近角度
未知。要确证需要 Fn14–Fab 复合物结构或建模。

## 4. ADC / 内吞

- **TWEAKR-KSPi-ADC1 / ADC2（Bayer）**：小分子 payload ADC，在 **CT26 结肠癌**模型中有效；次优剂量下只在
  免疫健全小鼠有效，提示免疫机制参与。**与 CRC 最相关。**
- **GrB-Fc-IT4**：人源化抗 Fn14 单链抗体 + 颗粒酶 B。
- **ITEM4-rGel**：2 小时内特异内吞；ITEM4 针对人 Fn14 胞外区制备，结合人与小鼠 Fn14，具弱激动活性（Cheng 2013）。
- v1 说"ITEM-4 是唯一有内吞证据的抗体"**不成立**：第 3 轮审核指出 hSGZ、GrB-Fc-IT4、GrB-TWEAK、BAY-356
  都有直接内吞数据（分别为 Zhou 2013 Fig 1A/2F、Zhou 2014 Fig 2B、Fig 2A、2018 KSPi 研究 Fig S6）。
  这些是**审核转述的图级结果，本项目尚未逐条核实**，已在表中逐条标注。
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
| **WO2009020933A2 / WO2009140177A2** | Facet Biotech / Biogen | **PDL192 与 P4A8 的 VH/VL**（审核确认 PDL192 VH=3、VL=4；P4A8 VH=2、VL=5）。本项目此前看到的 SEQ ID NO: 25 是 PDL192 的重链 CDR3，不是完整 VH——审核的解释与本项目所见一致 |
| WO2020128927A1 | Kyowa Kirin | VH CDR3 = SGWFTY（SEQ ID NO: 121）；**本项目已核对权利要求**：antagonist 且非 agonist，attenuates TWEAK binding，表位 = subdomain 1（aa 30–50）中的 Gly32/Thr33/Ala34/Pro35/Trp42/Ala44/Asp45/Leu46/Asp47/Lys48/Cys49 |
| WO2022155705A1 / WO2016061632A1 | La Trobe University | VH 为 SEQ ID NO: 8 等 |
| WO2012122513A2 | Omeros | VH 为 SEQ ID NO: 82 |
| WO2015189143A1 | Bayer Pharma | 可能是 TWEAKR-KSPi ADC 的抗体来源 |

**这改变了 v1/v2 初版的结论。** v1 说"没有公开的 VH/VL，因此暂不具备建模条件"——那只对**文献**成立；
**专利里有**。Fn14–Fab 建模现在是可行的。

专利披露**不升级**为 E2/E3 实验证据，单列一表。

## 8. 下一步

1. **用专利序列做 Fn14–Fab 建模，检验第 3 节的解释。** 第 3 轮审核找到了决定性的两份专利：
   **WO2009020933A2（Facet Biotech）含 PDL192 的 VH/VL，WO2009140177A2（Biogen）含 P4A8 的 VH/VL**——
   正是本节用到的那两个抗体。因此可以直接建模这两个 Fab，看它们是否真的落在受体的两个面上。
   这是一个**有实验标准答案**的检验（PDL192 不竞争、P4A8 竞争），不是预测未知结果。
   本项目已核实两份专利存在并披露序列，但**尚未确认具体 SEQ ID 的对应关系**。
2. 核实各偶联物的内吞原始图（hSGZ、GrB-Fc-IT4、GrB-TWEAK、BAY-356）。
3. 补 Bayer 2018 年系列 ADC（ADC 1.1–1.4、2.1、2.2），目前只记录了 2022 年的 ADC1/ADC2。
4. 本轮一手文献登记 REF 编号。

## 9. 方法教训（记入项目规范）

**不要用 Europe PMC 的 `isOpenAccess` 标志或 PMC API 的返回长度来判断全文是否可得。**
本项目因此误判三篇关键文献"无法核实"，把已经可以核对的一手结论降级为转述。
正确做法：API 只返回题录/摘要时，再抓 `https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/` 页面确认。
