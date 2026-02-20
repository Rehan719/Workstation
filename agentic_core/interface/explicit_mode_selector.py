from typing import Any, Dict, List, Optional
from datetime import datetime

class ExplicitModeSelector:
    """
    Manages explicit user granularity preferences: summary, detailed, expert (Article S).
    """
    def __init__(self):
        self.user_modes = {}
        self.available_modes = ['summary', 'detailed', 'expert']

    async def set_mode(self, user_id: str, mode: str):
        if mode in self.available_modes:
            self.user_modes[user_id] = mode

    async def get_current_mode(self, user_id: str) -> Optional[str]:
        return self.user_modes.get(user_id)
