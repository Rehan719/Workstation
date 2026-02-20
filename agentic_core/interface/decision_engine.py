from typing import Any, Dict, List, Optional

class DecisionEngine:
    """
    Decides on granularity changes based on implicit and explicit inputs (Article S).
    """
    def __init__(self):
        self.rules = [
            # Priority: Explicit mode always overrides
            {'condition': lambda i, e: e is not None, 'action': lambda i, e: f"set_{e}"},
            # Heuristic: Prolonged pause -> simplify
            {'condition': lambda i, e: i.get('pause_detected'), 'action': lambda i, e: 'show_summary'},
        ]

    async def decide(self, user_id: str, implicit_state: Dict[str, Any], explicit_mode: Optional[str]) -> str:
        if explicit_mode:
            return f"set_{explicit_mode}"

        for rule in self.rules:
            if rule['condition'](implicit_state, explicit_mode):
                return rule['action'](implicit_state, explicit_mode)

        return 'no_change'
