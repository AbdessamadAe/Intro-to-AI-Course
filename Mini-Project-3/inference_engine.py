"""Forward chaining inference engine with variable unification."""

from typing import List, Tuple, Dict, Optional, Set
from knowledge_base import KnowledgeBase
from rule_system import Rule
from datetime import datetime


class Explanation:
    """Tracks rule firing: which rule, matched conditions, conclusion, substitution."""
    
    def __init__(self, rule_name: str, matched_conditions: List[Tuple], 
                 conclusion: Tuple, substitution: Dict[str, str]):
        self.rule_name = rule_name
        self.matched_conditions = matched_conditions
        self.conclusion = conclusion
        self.substitution = substitution
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        conditions_str = ", ".join(str(c) for c in self.matched_conditions)
        subst_str = ", ".join(f"{k}={v}" for k, v in self.substitution.items()) if self.substitution else "none"
        return (f"Rule: {self.rule_name}\n"
                f"  Conditions matched: {conditions_str}\n"
                f"  Substitution: {subst_str}\n"
                f"  Conclusion: {self.conclusion}")


class ForwardChainingEngine:
    """Data-driven inference: applies rules until fixpoint (no new facts)."""
    
    def __init__(self):
        self.explanations: List[Explanation] = []
    
    def infer(self, kb: KnowledgeBase, rules: List[Rule]) -> tuple:
        """Forward chaining until fixpoint. Returns (explanations, fixpoint_msg)."""
        self.explanations = []
        iteration = 0
        sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)
        
        while True:
            iteration += 1
            new_facts_added = False
            
            for rule in sorted_rules:
                substitutions = self._find_all_substitutions(rule, kb)
                
                for substitution in substitutions:
                    conclusion = self._apply_substitution(rule.conclusion, substitution)
                    
                    if not kb.contains(conclusion):
                        kb.add_fact(conclusion)
                        new_facts_added = True
                        
                        matched_conditions = [
                            self._apply_substitution(cond, substitution) 
                            for cond in rule.conditions
                        ]
                        explanation = Explanation(
                            rule.name,
                            matched_conditions,
                            conclusion,
                            substitution
                        )
                        self.explanations.append(explanation)
            
            if not new_facts_added:
                fixpoint_msg = f"✓ FIXPOINT REACHED after {iteration} iteration(s): No more rules applicable"
                break
        
        return self.explanations, fixpoint_msg
    
    def _find_all_substitutions(self, rule: Rule, kb: KnowledgeBase) -> List[Dict[str, str]]:
        """Find all variable substitutions satisfying all rule conditions."""
        if not rule.conditions:
            return [{}]
        
        # Start with substitutions for first condition, then filter by remaining
        all_substitutions = self._find_substitutions_for_condition(rule.conditions[0], kb)
        
        for condition in rule.conditions[1:]:
            all_substitutions = self._filter_substitutions(
                all_substitutions, condition, kb
            )
        
        return all_substitutions
    
    def _find_substitutions_for_condition(self, condition: Tuple, 
                                          kb: KnowledgeBase) -> List[Dict[str, str]]:
        """Find all substitutions making a single condition true."""
        substitutions = []
        
        for fact in kb.get_all_facts():
            subst = self._match_predicate(condition, fact)
            if subst is not None:
                substitutions.append(subst)
        
        return substitutions
    
    def _filter_substitutions(self, substitutions: List[Dict[str, str]], 
                              condition: Tuple, kb: KnowledgeBase) -> List[Dict[str, str]]:
        """Keep only substitutions that also satisfy an additional condition."""
        filtered = []
        
        for subst in substitutions:
            instantiated_condition = self._apply_substitution(condition, subst)
            
            # If condition still has unbound variables, find new substitutions
            if self._has_variables(instantiated_condition):
                new_substs = self._find_substitutions_for_condition(instantiated_condition, kb)
                for new_subst in new_substs:
                    merged = {**subst, **new_subst}
                    if merged not in filtered:
                        filtered.append(merged)
            else:
                # No variables, just check if fact exists
                if kb.contains(instantiated_condition):
                    filtered.append(subst)
        
        return filtered
    
    def _match_predicate(self, pattern: Tuple, fact: Tuple) -> Optional[Dict[str, str]]:
        """Match pattern against fact, return variable bindings or None."""
        if len(pattern) != len(fact):
            return None
        
        substitution = {}
        
        for pattern_elem, fact_elem in zip(pattern, fact):
            if isinstance(pattern_elem, str) and pattern_elem.startswith('?'):
                var_name = pattern_elem
                if var_name in substitution:
                    # Variable already bound, verify consistency
                    if substitution[var_name] != fact_elem:
                        return None
                else:
                    substitution[var_name] = fact_elem
            else:
                # Constant must match exactly
                if pattern_elem != fact_elem:
                    return None
        
        return substitution
    
    def _apply_substitution(self, predicate: Tuple, substitution: Dict[str, str]) -> Tuple:
        """Replace variables in predicate with their bindings."""
        result = []
        for elem in predicate:
            if isinstance(elem, str) and elem.startswith('?'):
                result.append(substitution.get(elem, elem))
            else:
                result.append(elem)
        return tuple(result)
    
    def _has_variables(self, predicate: Tuple) -> bool:
        """Check if predicate contains variables (start with '?')."""
        return any(isinstance(elem, str) and elem.startswith('?') for elem in predicate)
    
    def get_explanations(self) -> List[Explanation]:
        return self.explanations
    
    def clear_explanations(self):
        self.explanations = []
