# Knowledge-Based Smart Home Agent
## CSC-3309: Introduction to Artificial Intelligence - Mini-Project 3

---

## 1. THEORETICAL FOUNDATION

This project implements a **knowledge-based agent** using classical symbolic AI techniques as specified in Russell & Norvig's "Artificial Intelligence: A Modern Approach" (AIMA). The agent performs automated reasoning using propositional logic and forward chaining inference.

### 1.1 Knowledge Representation: Horn Clauses

All rules in the system are represented as **Horn clauses**, a restricted form of first-order logic especially suited for forward chaining:

**Form:** (A₁ ∧ A₂ ∧ ... ∧ Aₙ) → C

Where:
- A₁, A₂, ..., Aₙ are **condition predicates** (antecedents)
- C is a **conclusion predicate** (consequent)
- Each predicate can contain **variables** (denoted by `?variable` syntax)

**Example Rule:**
```
presence(?room) ∧ dark(?room) → turn_on_light(?room)
```

This Horn clause representation ensures:
- **Soundness**: Only valid inferences are made
- **Completeness**: All derivable facts will be inferred
- **Decidability**: Inference terminates in finite time

### 1.2 Inference Method: Forward Chaining (Data-Driven Reasoning)

The agent employs **forward chaining**, a data-driven inference strategy that reasons from facts to conclusions:

**Algorithm:**
```
1. Initialize KB with observed facts from environment
2. Repeat until fixpoint:
   a. For each rule R (in priority order):
      - Find all variable substitutions σ that satisfy R's conditions
      - For each valid substitution σ:
        * Instantiate conclusion C' = apply(σ, R.conclusion)
        * If C' ∉ KB: add C' to KB and record inference
   b. If no new facts added: FIXPOINT REACHED
3. Return all derived facts
```

**Key Properties:**
- **Data-driven**: Starts from known facts (observations), not goals
- **Sound**: All derived facts are logically valid
- **Complete**: Reaches fixpoint when no more facts can be derived
- **Monotonic**: Facts are only added, never retracted (in each time step)

### 1.3 Variable Unification

To enable **generic rules** applicable to multiple entities, the system implements pattern matching with variable substitution:

**Unification Process:**
1. **Pattern:** `("presence", "?room")`
2. **Fact:** `("presence", "kitchen")`
3. **Match:** Succeeds with **substitution** `σ = {?room → kitchen}`
4. **Application:** All occurrences of `?room` in the rule are replaced with `"kitchen"`

This allows a single rule to apply to all rooms without hardcoding, achieving **knowledge generalization**.

---

## 2. AGENT ARCHITECTURE

The system follows the canonical **perceive-reason-act cycle** for knowledge-based agents:

### 2.1 Component Responsibilities

**Knowledge Base (`knowledge_base.py`):**
- Stores facts as tuples: `(predicate, entity)`
- Provides operations: `add_fact()`, `contains()`, `get_all_facts()`
- Maintains fact history for explanation tracing
- Pattern-matching query support

**Rule System (`rule_system.py`):**
- Defines `Rule` class: `(name, conditions, conclusion, priority)`
- Implements 14 domain-specific Horn clause rules
- Rules categorized by: lighting (3), temperature (3), ventilation (2), multi-condition (6)
- Priority levels for conflict resolution: safety (10) > comfort (5-8) > efficiency (1-3)

**Inference Engine (`inference_engine.py`):**
- Implements forward chaining algorithm
- Performs variable unification via pattern matching
- Conflict resolution: sorts rules by priority before application
- Generates `Explanation` objects for full traceability
- Detects fixpoint and reports convergence

**Environment Simulator (`environment.py`):**
- Models 4-room smart home (living_room, bedroom, kitchen, bathroom)
- Tracks per-room state: presence, temperature, light level, air quality, time of day
- Tracks device states: light, AC, heater, fan, window
- Generates facts from observations: `generate_facts()`
- Applies inferred actions to environment: `apply_actions()`
- Simulates random environmental changes: `update_environment()`

---

## 3. DESIGN DECISIONS AND JUSTIFICATIONS

### 3.1 Stateless KB per Time Step

**Design:** The KB is cleared and repopulated from environment observations at each time step.

**Rationale:**
- Maintains **single source of truth** in the environment (not KB)
- Simplifies temporal reasoning (no need for fact retraction logic)
- Implements pure **perceive-reason-act cycle**
- Environmental state (device on/off) persists; KB facts are regenerated
- Avoids inconsistency between KB beliefs and actual world state

### 3.2 Fact vs. Action Separation

**Design:** Facts are categorized as:
1. **Environmental facts**: observations from sensors (`presence`, `temperature_high`, etc.)
2. **Action facts**: inferred control commands (`turn_on_light`, `open_window`, etc.)

**Rationale:**
- Clarifies what is **observed** vs. what is **inferred**
- Improves explainability and debugging
- Demonstrates forward chaining explicitly adds new knowledge
- Aligns with KB agent theory (perceive facts → infer actions)

### 3.3 Priority-Based Conflict Resolution

**Design:** When multiple rules are applicable, higher priority rules fire first.

**Rationale:**
- **Safety first**: Air quality rules (priority 10) fire before comfort rules
- **Deterministic behavior**: Same KB state always produces same inference
- **Conflict handling**: Multiple applicable rules resolved systematically
- Reflects real-world priorities (safety > comfort > efficiency)

### 3.4 Generic Rules with Variables

**Design:** All rules use variables (`?room`) instead of room-specific constants.

**Rationale:**
- **Scalability**: Same rule applies to any room
- **Knowledge generalization**: Add new rooms without modifying rules
- **Theoretical correctness**: Demonstrates proper use of first-order logic
- **Reduced redundancy**: 14 rules instead of 14 × 4 = 56 hardcoded rules

### 3.5 Fixpoint Detection and Display

**Design:** Explicitly report when forward chaining reaches fixpoint.

**Rationale:**
- **Theoretical requirement**: Forward chaining must prove termination
- **Transparency**: Shows inference engine behavior
- **Verification**: Confirms algorithm correctness
- **Educational value**: Demonstrates key property of forward chaining

---

## 4. RULE SET DESIGN

The system implements **14 Horn clause rules** covering three smart home domains:

### 4.1 Lighting Control (3 rules)
1. **R1** (Priority 5): `presence(?room) ∧ dark(?room) → turn_on_light(?room)`
2. **R2** (Priority 5): `no_presence(?room) ∧ light_on(?room) → turn_off_light(?room)`
3. **R3** (Priority 5): `night(?room) ∧ presence(?room) → turn_on_light(?room)`

### 4.2 Temperature Control (3 rules)
4. **R4** (Priority 5): `temperature_high(?room) → turn_on_ac(?room)`
5. **R5** (Priority 5): `temperature_low(?room) → turn_on_heater(?room)`
6. **R6** (Priority 3): `temperature_moderate(?room) → turn_off_climate(?room)`

### 4.3 Ventilation Control (2 rules)
7. **R7** (Priority 10): `air_bad(?room) → open_window(?room)` [Safety priority]
8. **R8** (Priority 8): `air_bad(?room) ∧ presence(?room) → turn_on_fan(?room)`

### 4.4 Multi-Condition Rules (6 rules)
9. **R9** (Priority 7): `temperature_high(?room) ∧ presence(?room) → turn_on_ac(?room)`
10. **R10** (Priority 6): `night(?room) ∧ no_presence(?room) ∧ light_on(?room) → turn_off_light(?room)`
11. **R11** (Priority 2): `temperature_moderate(?room) ∧ air_good(?room) ∧ window_open(?room) → close_window(?room)`
12. **R12** (Priority 4): `temperature_moderate(?room) ∧ heater_on(?room) → turn_off_heater(?room)`
13. **R13** (Priority 5): `temperature_high(?room) ∧ window_closed(?room) → turn_on_fan(?room)`
14. **R14** (Priority 3): `no_presence(?room) ∧ ac_on(?room) → turn_off_ac(?room)`

**Design Notes:**
- All rules use variable `?room` for generalization
- Multi-condition rules (2-3 conditions) demonstrate conjunctive reasoning
- Priority reflects domain importance: safety > comfort > energy efficiency

---

## 5. ALGORITHM CORRECTNESS

### 5.1 Soundness
**Claim:** All inferred facts are logically valid.

**Proof:** 
- Each rule is a valid Horn clause implication
- Forward chaining only fires rules when ALL conditions are satisfied
- Variable substitutions maintain logical consistency
- Therefore, all conclusions follow from premises via modus ponens

### 5.2 Completeness
**Claim:** All derivable facts will be inferred.

**Proof:**
- Forward chaining explores all applicable rules at each iteration
- Rules are applied until fixpoint (no new facts)
- All valid substitutions are found via exhaustive pattern matching
- Therefore, all facts derivable from KB + rules will be added

### 5.3 Termination
**Claim:** Forward chaining always terminates.

**Proof:**
- KB can only grow (monotonic reasoning within each time step)
- Finite set of possible facts (bounded by entities and predicates)
- Each rule firing adds at least one new fact or terminates
- Fixpoint guaranteed when |KB| stops growing
- Therefore, algorithm terminates in at most O(|facts| × |rules|) iterations

---

## 6. EXECUTION AND OUTPUT

### Running the Simulation
```bash
python smart_home_agent.py
```

### Output Structure
Each time step displays:
1. **Environment State**: Room conditions and device states
2. **KB Before Inference**: Environmental facts only
3. **Forward Chaining Process**: Iteration until fixpoint
4. **Fixpoint Message**: "✓ FIXPOINT REACHED after N iteration(s): No more rules applicable"
5. **Rules Fired**: Full explanations with matched conditions and substitutions
6. **KB After Inference**: Environmental facts + derived action facts (clearly separated)
7. **Actions Taken**: Device state changes applied to environment

### Verification
The simulation demonstrates:
- ✓ Horn clause rule representation
- ✓ Data-driven forward chaining inference
- ✓ Variable unification across multiple rooms
- ✓ Fixpoint convergence (explicitly reported)
- ✓ Full explanation traceability
- ✓ Priority-based conflict resolution
- ✓ Separation of facts vs. actions

---

