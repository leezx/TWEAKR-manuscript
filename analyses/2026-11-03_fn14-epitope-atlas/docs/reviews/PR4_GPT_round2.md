# PR #4 GPT 审核 — 第 2 轮

- **审核对象：** HEAD `9cb8335`
- **审核会话：** 同前（ChatGPT 项目 TWEAKR-oncoFetal →「深入分析TWEAKR蛋白结构」）
- **时间：** 2026-11-03 19:49（EST）提交
- **判定：** **REQUEST_CHANGES**。P1-1、P1-2、P1-4 主体完成；P1-3 未完全通过；另发现数据分级问题。

## 一、本项目的判断错误：三篇文献其实可读

本项目在第 2 轮提交中声称 Salzmann 2013、Michaelson 2011、Trebing 2014 "非开放获取、无法独立核实"，
并据此把审核转述的结论降级标注。**审核方指出这是错的，并给出了图号。本项目复核后确认审核方正确：**

> Europe PMC 的 `isOpenAccess: N`、PMC **API** 只返回摘要，**不等于** PMC 网站没有可读全文。

改抓 `https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/` 后，三篇正文全部取到（194–226 KB）。
本项目已逐条核对原文，结论与审核方一致（原话引用见 `results_v2.md` 第 2 节）。教训已记入 `results_v2.md` 第 9 节。

## 二、四项 P1 验收与本轮处理

| 项 | 审核裁定 | 本项目处理 |
|---|---|---|
| P1-1 身份与归属 | 部分通过：`LIN-llama` 分组错误 | 18D1/4G5/5B6 拆为 `LIN-18D1`/`LIN-4G5`/`LIN-5B6`，新增 `discovery_campaign_id = ARGENX-LLAMA`。理由（审核）：三者是不同克隆且功能不同（5B6 不阻断），发现平台不等于 lineage |
| P1-2 竞争实验 | 部分通过 | 全部改为核对原文后的 `verified`；BIIB036 的竞争证据改记为 Michaelson 2011 Fig 2B（WiDr 结肠癌细胞，双向竞争） |
| P1-3 ADC 与内吞 | 未完全通过 | ITEM-4 的内吞 "YES" **撤销**（该证据属于 ITEM4-rGel 偶联物，不是裸抗体），移到 FNB-012；GrB-TWEAK 移出抗体表，新建 `other_fn14_targeted_constructs.tsv` |
| P1-4 结构假说 | 通过，建议收敛措辞 | 删去"局部环境相似"的说法（本项目数据不支持：W42 距 D62 4.9 Å，R56 距 11–16 Å），改为审核建议的问法，并列出三个待检验解释 |

**数据字典：** 审核指出 `verified(abstract) + review(figure)` 不符合 `design.md` 事先冻结的取值。
已统一为 `verified` / `unverified` 两值。

## 三、专利检索（审核新增，本项目已逐条核对）

审核做了专利检索，指出 VH/VL 序列**在专利中存在**，推翻了 v1/v2 初版"暂不具备建模条件"的结论。
本项目逐条核对 Google Patents 记录（标题、受让人、权利要求文字）后确认六个专利族均存在，
写入 `tables/patent_disclosed_binders.tsv`。最明确的是 Astellas US20210388096A1（VH/VL 以 SEQ ID NO: 2/4 定义）。

**未核对的转述：** Bayer 的 TPP-2090 等抗体编号、Kyowa Kirin 权利要求涉及 aa 30–50——两条都由审核提出，
本项目尚未从专利正文确认，已在表中标注。

## 四、仍未完成

- Bayer 2018 年系列 ADC（ADC 1.1–1.4、2.1、2.2）尚未录入，目前只有 2022 年的 ADC1/ADC2。
- GrB-Fc-IT4 / GrB(C210A)-Fc-IT4 的直接内吞证据尚未补齐。
- 临床 Fn14 ADC：审核与本项目一致——**在检索范围内**未找到，措辞已按审核建议收敛。
