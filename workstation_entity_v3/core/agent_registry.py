import logging
class AgentRegistry:
    def __init__(self):
        self.registry = {}
    async def register(self, agent_id, blueprint):
        self.registry[agent_id] = blueprint
