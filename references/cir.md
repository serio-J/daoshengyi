# Cognitive Intermediate Representation

CIR is runtime-independent: `Evidence → CIR → Runtime`.

## Root
`CIR = <Anchor, EvidenceGraph, RepresentationModel, GenerativeGraph, BoundarySystem, Provenance, ValidationState>`.

## W — Representation Model
Entities, relations, variables, states, causal relations, observations, beliefs, relevant history. A distinction belongs in W only if removing it can collapse situations requiring different target behavior.

When epistemic state matters preserve `WorldState`, `Observation`, `BeliefState`, and only the lowest necessary `HigherOrderBelief` depth.

## Γ — Generative Graph
May include GU, activation, sequence, competition, inhibition, composition, mode switch, termination. It answers: given the current represented state, what happens cognitively next?

## GU
`GU = <Condition, Mechanism, Response, Boundary>`. It should be locally coherent, generatively useful, independently testable, composable, and evidence-traceable.

## Boundary System
Represent Applicability, FailureSignal, Fallback, ModeSwitch, Termination. A textual caveat that does not alter execution is not a functional boundary.

## Validation state
Useful node states: candidate, supported, validated, contested, deprecated. Confidence and validation state are distinct.

## Views
Knowledge Card, Behavior Card, Thinking Formula, Personality View, Expertise View, Validation Report, and Runtime Prompt are `View = f(CIR, Purpose)`. Change the view rather than distorting ontology.

## Functional typing
Possible roles: Evidence, Representation, Generative Mechanism, Routing/Coordination, Objective/Preference, Boundary, State/Memory, Expression. Ask: if this information disappeared, which execution stage would change?

Encode executable CIR in `cir.json` using `contracts.md`. Give every node a stable ID, provenance or explicit inference trace, confidence, and validation state. Record compile-invariants separately from descriptive prose.
