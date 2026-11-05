"""Belief revision engine using entrenchment ordering."""
from typing import Dict, List, Set, Any, Optional


class Belief:
    def __init__(self, key: str, value: Any, entrenchment: float = 1.0, derived_from: Optional[List[str]] = None):
        self.key = key
        self.value = value
        self.entrenchment = float(entrenchment)
        self.derived_from = derived_from or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "entrenchment": self.entrenchment,
            "derived_from": self.derived_from
        }


class BeliefRevisionEngine:
    def __init__(self):
        self._beliefs: Dict[str, Belief] = {}

    def add_belief(self, key: str, value: Any, entrenchment: float = 1.0, derived_from: Optional[List[str]] = None) -> Belief:
        b = Belief(key, value, entrenchment, derived_from)
        self._beliefs[key] = b
        return b

    def contract(self, key: str) -> List[str]:
        """Contract a belief and cascade retraction to all beliefs derived from it."""
        if key not in self._beliefs:
            return []

        evicted = [key]
        del self._beliefs[key]

        # Find cascading dependencies
        changed = True
        while changed:
            changed = False
            for b_key, b in list(self._beliefs.items()):
                if any(dep in evicted for dep in b.derived_from):
                    evicted.append(b_key)
                    del self._beliefs[b_key]
                    changed = True

        return evicted

    def revise(self, key: str, value: Any, entrenchment: float = 1.0) -> List[str]:
        """Revise with a potentially conflicting fact. If key exists with different value, contract first."""
        retracted = []
        if key in self._beliefs and self._beliefs[key].value != value:
            # Check entrenchment: higher entrenchment incoming replaces lower
            if entrenchment >= self._beliefs[key].entrenchment:
                retracted = self.contract(key)
            else:
                return [] # Incoming rejected due to lower entrenchment

        self.add_belief(key, value, entrenchment)
        return retracted

    def get_beliefs(self) -> Dict[str, Any]:
        return {k: b.value for k, b in self._beliefs.items()}
