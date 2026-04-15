import logging
class IntentPlanner:
    def __init__(self, nemo, gaas):
        self.nemo = nemo
        self.gaas = gaas
    async def plan_task(self, intent: str):
        return {"steps": ["decompose", "reason", "execute"], "intent": intent}
