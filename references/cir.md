# 认知中间表示（CIR）

CIR 与具体运行宿主无关：`Evidence → CIR → Runtime`。

## 顶层结构
`CIR = <Anchor, EvidenceGraph, RepresentationModel, GenerativeGraph, BoundarySystem, Provenance, ValidationState>`

## W — 表示模型（Representation Model）
包含实体、关系、变量、状态、因果关系、观察、信念及相关历史。一项区分只有「删掉它会导致需要不同行为的情境坍缩在一起」时，才应留在 W 中。

当认识状态影响行为时，保留 `WorldState`（世界状态）、`Observation`（观察）、`BeliefState`（信念状态），以及最低必要深度的 `HigherOrderBelief`（高阶信念）。

## Γ — 生成图（Generative Graph）
可包含生成单元（GU）、激活、顺序、竞争、抑制、组合、模式切换与终止。它回答：**在当前表示状态下，认知下一步发生什么？**

## GU — 生成单元
`GU = <Condition, Mechanism, Response, Boundary>`。应局部自洽、具生成力、可独立测试、可组合，且可溯源到证据。

## 边界系统（Boundary System）
显式表示适用域（Applicability）、失效信号（FailureSignal）、降级（Fallback）、模式切换（ModeSwitch）与终止（Termination）。**不会改变实际执行的口头免责声明，不是功能边界。**

## 验证状态
常用节点状态：`candidate`（候选）、`supported`（有支撑）、`validated`（已验证）、`contested`（存争议）、`deprecated`（已废弃）。置信度与验证状态是两回事。

## 视图（Views）
知识卡、行为卡、思维公式、人格视图、专长视图、验证报告与运行提示词，全都是 `View = f(CIR, Purpose)`。按用途切换视图，不要为了迁就视图而扭曲本体。

## 功能类型
可能的角色：Evidence（证据）、Representation（表示）、Generative Mechanism（生成机制）、Routing/Coordination（路由/协调）、Objective/Preference（目标/偏好）、Boundary（边界）、State/Memory（状态/记忆）、Expression（表达）。判断标准：**如果删掉这条信息，哪个执行阶段会改变？**

完整模式下可用 `references/contracts.md` 将可执行 CIR 编码为 `cir.json`：每个节点配稳定 ID、溯源或显式推断链、置信度与验证状态，并把编译不变量与描述性说明分开记录。
