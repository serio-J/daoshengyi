# Daoshengyi Theory v1

Daoshengyi is an evidence-constrained cognitive compiler: it estimates a minimal sufficient cognitive model from heterogeneous evidence, compiles it into an executable Agent, validates it by forward generation, and repairs it causally after failure.

## Core ontology
`Agent = <W, Γ>`.
W is the target-relevant representational model. Γ is the generative dynamics over represented states. Runtime: `Observation → W → State_t → Γ → (Action_t, State_{t+1})`.

## Six axioms
1. Generative: `Agent != InformationSet`; cognition must map state to behavior.
2. Evidence: `Material != Mind`; `Statement != Truth`.
3. Anchoring: `CognitiveModel = f(Evidence, Anchor)`.
4. Minimal generative sufficiency: minimize model complexity subject to adequate generative and boundary fidelity.
5. Non-uniqueness: finite evidence does not imply a unique true cognitive model.
6. Falsifiability: a useful model must survive new, conflicting, boundary, and counterfactual tests; it must Explain Past + Generate Future.

## Anchor
`Anchor = <Target, Scope, Runtime, Fidelity>`. There is no target-independent optimal compression.

## Personality
A projection of stable biases over cognitive transitions: attention, interpretation, objective priority, decision thresholds, arbitration, and mode switching. Personality is not primarily an adjective list.

## Learning
Learning modifies future state-transition structure: `(W, Γ)_t → (W, Γ)_{t+1}`. It may update representation, mechanisms, objectives, or policies. Learning is not required for minimal agenthood.

## Identity
Identity is stable generative invariants plus lineage across change. Reforge preserves selected core; Fork changes core.

## Fidelity
Useful dimensions include Decision, Reasoning, Priority, Boundary, Adaptation, Expression, and Source Fidelity. Highest-value fidelity is generative: novel contexts should follow the latent mechanism rather than memorized examples.

## Epistemic principle
Evidence, interpretation, hypothesis, and model are different layers. Preserve uncertainty and competing hypotheses when evidence underdetermines cognition.

## Repair principle
Failure is an observation. Diagnose the causal layer, make the smallest repair, and validate again.
