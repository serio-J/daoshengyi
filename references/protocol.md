# 可选完整建模流程

只在跨来源冲突、多个竞争机制、需要审计或显式要求时使用。
普通任务遵循 SKILL.md 的轻量流程。此文不额外要求轻量任务创建任何 JSON。

SCOPE → INGEST → MODEL ↔ COMPRESS → CIR_VALIDATE → REVIEW → COMPILE → RUNTIME_VALIDATE。

- SCOPE：目标、范围、格式、保真维度、成功与关键失败条件。
- INGEST：可追溯证据，来源依赖、主张/观察/推断分开；未解冲突不删除。
- MODEL：W、Gamma、配套知识、边界；保留无法区分的竞争假设。
- COMPRESS：每次重要合并或删除说明行为差异是否保留。
- CIR_VALIDATE：新情境、冲突、边界、反事实，记录模型预测和可观察结果。
- REVIEW：用户要求或高影响用途才要求真实审批；没有审批不得填 approved。
- COMPILE：按选定格式交付，Skill 不是所有路线唯一终点。
- RUNTIME_VALIDATE：真实执行才能记录 model_execution；缺环境标未执行。

证据缺失回到 INGEST；模型忠实执行仍错误回到 MODEL；
压缩丢区分回到 COMPRESS；输出丢知识或边界回到 COMPILE。
最小因果修复后回归相关案例，不通过追加大量补丁遮蔽问题。
完整档案字段见 contracts.md；不以旧样例的合成 PASS 作为验证依据。

