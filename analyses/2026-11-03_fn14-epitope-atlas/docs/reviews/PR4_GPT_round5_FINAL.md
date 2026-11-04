# PR #4 GPT 审核 — 第 5 轮（最终）

- **审核对象：** HEAD `329fcec` · **判定：APPROVE，允许合并**
- **最终定位：** *Fn14 therapeutic epitope atlas v1 candidate*
- P0 0 / P1 0 / P2 4（非阻断性维护建议，本项目已在 `fd?` 收尾 commit 中处理）
- 结构计算保留 PASS；E1–E5 分级 PASS；预注册修订 PASS；输出文件 20/20 checksum 与大小匹配。

审核方明确表示："不应该再因为发现一篇新的专利或一个新的抗体衍生物而重新打开整个审核。"

## 审核方特别认可的两点

1. **预注册没有被悄悄修改。** 保留原始 `design.md`，增加修订 1，证据分 A/B/C 三层，只有 A 进入 E1–E5 统计。
   审核称这是"正确的科研审计方式"。
2. **Biogen Example 21 没有被过度包装。** 记录了 3.5 Å、仅 50–67 可解释、R-factor 46%、H3 CDR 与 N 端缺失、
   界面为 NMR 叠合 + Rosetta + 约束优化，以及 W42 不在解析区——因此 E1 = 0 的限定合理。

## 审核方完成的最后核对

- **SEQ ID 配对确认（打开原始专利）：** PDL192 VH = SEQ ID NO: 3、VL = 4（US20090074762A1 Fig. 2A）；
  P4A8 VH = SEQ ID NO: 2、VL = 5（WO2009140177A2 Example 11）。本项目先前看到的 NO: 25 确为 PDL192 的 HCDR3。
- **最后一轮定向检索：** 只发现 US20250277046（基于已有 LIN-18D1 的多价构建体）——按 `freeze_criteria.md`
  属同一 lineage 的新构建体，**不是新的独立 binder lineage**，不触发重开。冻结条件 3 因此满足。

## 四项非阻断建议（已处理）

| 项 | 内容 | 处理 |
|---|---|---|
| P2-1 | README/Worklog/results 中仍有"专利未检索、VH/VL 未确认"等过时陈述 | 已更新 |
| P2-2 | 登记 US20250277046 | 已作为 LIN-18D1 的关联构建体录入 |
| P2-3 | "四条相互独立的证据"措辞过强：Bayer 的多项残基结果出自同一专利同一次扫描，Kyowa 属 C 级权利要求 | 已改为"三组、并非彼此完全独立"，并标明 A/B/C 等级 |
| P2-4 | patent table 的 `verification_status` 统一为两值 | 已统一，细节移入 notes |
