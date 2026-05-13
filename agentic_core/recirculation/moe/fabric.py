import numpy as np, yaml, os
from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType
class MoEFabric:
    def __init__(self, registry=None):
        self.registry = registry or CognitiveEngineRegistry()
        self.expert_embeddings = {EngineType.INKASHAF: np.array([1,0,0,0,0,0]), EngineType.AQAL: np.array([0,1,0,0,0,0]), EngineType.SAMAJH: np.array([0,0,1,0,0,0]), EngineType.HOSHIYARI: np.array([0,0,0,1,0,0]), EngineType.SOCH: np.array([0,0,0,0,1,0]), EngineType.IMAN: np.array([0,0,0,0,0,1]), EngineType.NIYYAH: np.array([0.5,0.5,0,0,0,0]), EngineType.TAWAZUN: np.array([0,0,0.5,0.5,0,0]), EngineType.TAFAKKUR: np.array([0,0,0,0,0.5,0.5])}
    def route(self, task_vector, context, top_k=None):
        tier = context.get("tier", "free")
        k = min(top_k or 3, {"free": 2, "standard": 3, "advanced": 5}.get(tier, 2))
        scores = {e: np.dot(task_vector, emb) / (np.linalg.norm(task_vector) * np.linalg.norm(emb) + 1e-9) for e, emb in self.expert_embeddings.items()}
        return [e for e, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]]
    async def execute_moe_supreme(self, desc, vec, ctx, enf):
        results = {}
        for et in self.route(vec, ctx):
            res = await self.registry.get(et).process({"task": desc}, ctx, enf)
            results[et.value] = res.model_dump()
        return {"aggregated_result": "SUCCESS", "expert_responses": results}
