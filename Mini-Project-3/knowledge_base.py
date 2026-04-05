"""Knowledge Base: stores facts as tuples and provides query/update methods."""

from typing import Set, Tuple, List, Optional
from datetime import datetime


class KnowledgeBase:
    """Stores facts (tuples) and tracks history for explanation."""
    
    def __init__(self):
        self.facts: Set[Tuple] = set()
        self.fact_history: List[Tuple[Tuple, datetime]] = []
    
    def add_fact(self, fact: Tuple) -> bool:
        if fact not in self.facts:
            self.facts.add(fact)
            self.fact_history.append((fact, datetime.now()))
            return True
        return False
    
    def contains(self, fact: Tuple) -> bool:
        return fact in self.facts
    
    def get_all_facts(self) -> Set[Tuple]:
        return self.facts.copy()
    
    def remove_fact(self, fact: Tuple) -> bool:
        if fact in self.facts:
            self.facts.remove(fact)
            return True
        return False
    
    def clear(self):
        self.facts.clear()
    
    def get_facts_matching_pattern(self, pattern: Tuple) -> List[Tuple]:
        """Get facts matching a pattern (variables start with '?')."""
        matching_facts = []
        for fact in self.facts:
            if self._matches_pattern(pattern, fact):
                matching_facts.append(fact)
        return matching_facts
    
    def _matches_pattern(self, pattern: Tuple, fact: Tuple) -> bool:
        """Check if fact matches pattern (variables match anything)."""
        if len(pattern) != len(fact):
            return False
        
        for pattern_elem, fact_elem in zip(pattern, fact):
            if isinstance(pattern_elem, str) and pattern_elem.startswith('?'):
                continue  # Variables match anything
            if pattern_elem != fact_elem:
                return False
        
        return True
    
    def __repr__(self) -> str:
        return f"KnowledgeBase(facts={len(self.facts)})"
    
    def __str__(self) -> str:
        if not self.facts:
            return "KnowledgeBase: [empty]"
        
        fact_strings = [str(fact) for fact in sorted(self.facts)]
        return "KnowledgeBase:\n  " + "\n  ".join(fact_strings)
