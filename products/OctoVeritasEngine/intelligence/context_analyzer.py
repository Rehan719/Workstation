from typing import List, Any, Dict

class ContextAnalyzer:
    def __init__(self, registry: Any):
        self.registry = registry

    def analyze_pipeline_context(self, recent_assets: List[Any]) -> Dict[str, Any]:
        """
        Analyzes recent activity to determine which pipelines are currently active
        and if any specific context-driven priorities should be applied.
        """
        active_pipelines = set()
        for asset in recent_assets:
            pipeline = asset.get('pipeline')
            if pipeline:
                active_pipelines.add(pipeline)

        # Heuristic: If 'Introspection' (QA) is active, increase caution/verification
        context = {
            "active_pipelines": list(active_pipelines),
            "verification_level": "high" if "Introspection" in active_pipelines else "standard",
            "suggested_modifiers": []
        }

        if "Learning" in active_pipelines:
            context["suggested_modifiers"].append("show_confidence_interval")

        return context
