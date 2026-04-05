"""Smart Home Knowledge-Based Agent - Main simulation.

Implements a knowledge-based agent using:
- Horn clause rules
- Forward chaining inference
- Variable unification
- Explainable reasoning

Usage: python smart_home_agent.py
"""

import sys
from knowledge_base import KnowledgeBase
from rule_system import build_rule_set
from inference_engine import ForwardChainingEngine
from environment import SmartHomeEnvironment


class TeeOutput:
    """Duplicates output to both console and file."""
    
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.file = open(filename, 'w', encoding='utf-8')
    
    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
    
    def flush(self):
        self.terminal.flush()
        self.file.flush()
    
    def close(self):
        self.file.close()


def print_header(text: str, char: str = '='):
    print(f"\n{char * 70}")
    print(text)
    print(char * 70)


def print_subheader(text: str):
    print(f"\n{text}")
    print('-' * 70)


def print_facts(kb: KnowledgeBase, show_actions: bool = True):
    facts = sorted(kb.get_all_facts())
    
    if not facts:
        print("  [No facts in KB]")
        return
    
    # Separate environmental facts from action facts
    action_predicates = {'turn_on_light', 'turn_off_light', 'turn_on_ac', 'turn_off_ac',
                        'turn_on_heater', 'turn_off_heater', 'turn_on_fan', 'turn_off_fan',
                        'open_window', 'close_window', 'turn_off_climate'}
    
    environmental_facts = []
    action_facts = []
    
    for fact in facts:
        if len(fact) == 2 and fact[0] in action_predicates:
            action_facts.append(fact)
        else:
            environmental_facts.append(fact)
    
    # Group by room
    facts_by_room = {}
    other_facts = []
    
    for fact in environmental_facts:
        if len(fact) == 2:
            _, room = fact
            if room not in facts_by_room:
                facts_by_room[room] = []
            facts_by_room[room].append(fact)
        else:
            other_facts.append(fact)
    
    if environmental_facts:
        print("\n  ENVIRONMENTAL FACTS (state observations):")
        for room in sorted(facts_by_room.keys()):
            print(f"\n    {room}:")
            for fact in sorted(facts_by_room[room]):
                print(f"      {fact}")
        
        if other_facts:
            print("\n    Other:")
            for fact in sorted(other_facts):
                print(f"      {fact}")
    
    if action_facts and show_actions:
        print("\n  DERIVED ACTION FACTS (inferred by rules):")
        actions_by_room = {}
        for fact in action_facts:
            action, room = fact
            if room not in actions_by_room:
                actions_by_room[room] = []
            actions_by_room[room].append(fact)
        
        for room in sorted(actions_by_room.keys()):
            print(f"\n    {room}:")
            for fact in sorted(actions_by_room[room]):
                print(f"      {fact}")


def run_simulation(num_time_steps: int = 5):
    """Run smart home simulation for specified time steps."""
    print_header("SMART HOME KNOWLEDGE-BASED AGENT SIMULATION")
    print("\nThis simulation demonstrates a knowledge-based agent using:")
    print("  • Forward chaining inference (DATA-DRIVEN reasoning)")
    print("  • Horn clause rules: (A ∧ B ∧ ...) → C")
    print("  • Variable unification for generic rule application")
    print("  • Explainable reasoning with full traceability")
    print("\n[THEORETICAL FOUNDATION]")
    print("  - Rules are represented as Horn clauses")
    print("  - Inference is DATA-DRIVEN (forward chaining from facts)")
    print("  - Process continues until FIXPOINT (no new facts inferrable)")
    
    # Initialize
    print_subheader("INITIALIZATION")
    
    room_names = ["living_room", "bedroom", "kitchen", "bathroom"]
    env = SmartHomeEnvironment(room_names)
    print(f"✓ Created smart home with {len(room_names)} rooms: {', '.join(room_names)}")
    
    rules = build_rule_set()
    print(f"✓ Loaded {len(rules)} Horn clause rules")
    
    kb = KnowledgeBase()
    engine = ForwardChainingEngine()
    print(f"✓ Initialized knowledge base and forward chaining engine")
    
    # Display rules
    print_subheader("RULE SET")
    print("\nRules sorted by priority (higher priority fires first):")
    for rule in sorted(rules, key=lambda r: r.priority, reverse=True):
        print(f"\n  {rule.name} (Priority: {rule.priority})")
        cond_str = " AND ".join(str(c) for c in rule.conditions)
        print(f"    IF {cond_str}")
        print(f"    THEN {rule.conclusion}")
    
    # Run simulation
    for step in range(1, num_time_steps + 1):
        print_header(f"TIME STEP {step}", char='=')
        
        print(env.get_state_summary())
        
        # Clear KB, repopulate from environment
        kb.clear()
        current_facts = env.generate_facts()
        for fact in current_facts:
            kb.add_fact(fact)
        
        print_subheader("KNOWLEDGE BASE BEFORE INFERENCE")
        print(f"\nTotal facts: {len(kb.get_all_facts())} (all environmental state facts)")
        print_facts(kb, show_actions=False)
        
        # Forward chaining
        print_subheader("FORWARD CHAINING INFERENCE (Data-Driven Reasoning)")
        print("\nApplying Horn clause rules via forward chaining...")
        print("Process: Match conditions → Fire rules → Add conclusions → Repeat until fixpoint")
        
        initial_fact_count = len(kb.get_all_facts())
        explanations, fixpoint_msg = engine.infer(kb, rules)
        final_fact_count = len(kb.get_all_facts())
        
        print(f"\n{fixpoint_msg}")
        print(f"\n✓ Inference Statistics:")
        print(f"  Facts before inference: {initial_fact_count}")
        print(f"  Facts after inference: {final_fact_count}")
        print(f"  New facts inferred: {final_fact_count - initial_fact_count}")
        print(f"  Rules fired: {len(explanations)}")
        
        if explanations:
            print_subheader("RULES FIRED (with Explanations)")
            for i, explanation in enumerate(explanations, 1):
                print(f"\n  [{i}] {explanation}")
        else:
            print("\n  [No rules fired - all conditions already satisfied or no applicable rules]")
        
        # Show KB after
        print_subheader("KNOWLEDGE BASE AFTER INFERENCE")
        print(f"\nTotal facts: {len(kb.get_all_facts())} (environmental facts + derived actions)")
        print_facts(kb, show_actions=True)
        
        # Apply actions
        print_subheader("ACTIONS TAKEN")
        actions = env.apply_actions(kb.get_all_facts())
        
        if actions:
            print("\nDevice state changes:")
            for action in actions:
                print(f"  • {action}")
        else:
            print("\n  [No actions taken - no device state changes]")
        
        # Update environment
        if step < num_time_steps:
            print_subheader("ENVIRONMENT UPDATE")
            print("\nSimulating environmental changes...")
            env.update_environment()
            print("✓ Environment updated (random changes applied)")
            
            print("\n" + "·" * 70)
            print("Press Ctrl+C to stop simulation early...")
            print("·" * 70)
    
    # Summary
    print_header("SIMULATION COMPLETE", char='=')
    print(f"\n✓ Completed {num_time_steps} time steps")
    print(f"✓ Knowledge-based reasoning with forward chaining")
    print(f"✓ All inferences traced and explained")
    print("\nThe agent successfully demonstrated:")
    print("  • Data-driven reasoning (forward chaining)")
    print("  • Generic rule application (variables)")
    print("  • Fixpoint convergence")
    print("  • Explainable AI (full trace of inferences)")
    print("\n" + "=" * 70 + "\n")


def demonstrate_theoretical_concepts():
    """Show key theoretical concepts of the KB agent."""
    print_header("THEORETICAL CONCEPTS DEMONSTRATION")
    
    print("\n1. KNOWLEDGE-BASED AGENT ARCHITECTURE:")
    print("   KB = Facts + Rules")
    print("   Agent = Perceive → Update KB → Infer → Act")
    
    print("\n2. LOGIC REPRESENTATION (Horn Clauses):")
    print("   Rules are Horn Clauses: (A ∧ B ∧ ...) → C")
    print("   Example: presence(?room) ∧ dark(?room) → turn_on_light(?room)")
    print("   - Conditions: Conjunctions of predicates (can have variables)")
    print("   - Conclusion: Single predicate to infer")
    
    print("\n3. FORWARD CHAINING (Data-Driven Inference):")
    print("   • Start from known facts (environmental observations)")
    print("   • Repeatedly match and apply rules")
    print("   • Add newly inferred facts to KB")
    print("   • Stop at FIXPOINT (no new facts can be inferred)")
    print("   - This is DATA-DRIVEN reasoning (facts trigger rules)")
    
    print("\n4. VARIABLE UNIFICATION:")
    print("   Pattern: ('presence', '?room')")
    print("   Fact: ('presence', 'kitchen')")
    print("   Substitution: {?room: 'kitchen'}")
    print("   - Enables generic rules applicable to all rooms")
    
    print("\n5. EXPLAINABILITY:")
    print("   Every inference includes:")
    print("   • Which rule fired")
    print("   • Which conditions matched")
    print("   • What was concluded")
    print("   • Variable substitutions used")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    # Redirect output to both console and report.txt
    tee = TeeOutput('report.txt')
    sys.stdout = tee
    
    try:
        demonstrate_theoretical_concepts()
        run_simulation(num_time_steps=6)
        
    except KeyboardInterrupt:
        print("\n\n[Simulation interrupted by user]")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Restore stdout and close file
        sys.stdout = tee.terminal
        tee.close()
        print("✓ Simulation output saved to report.txt")
