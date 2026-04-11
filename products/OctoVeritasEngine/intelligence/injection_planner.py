from typing import List, Dict, Any, Optional
from ..pipelines.registry import PipelineRegistry
from ..modes.mode_router import ModeRouter

class InjectionJob:
    def __init__(self, asset: Any, format: str, pipeline: str, modifiers: List[str]):
        self.asset = asset
        self.format = format
        self.pipeline = pipeline
        self.modifiers = modifiers

class InjectionPlanner:
    def __init__(self, registry: PipelineRegistry, router: ModeRouter, effectiveness_db_path: str):
        self.registry = registry
        self.router = router
        self.effectiveness_db_path = effectiveness_db_path
        # Note: DecisionEngine will handle the database interactions

    def plan_injection(self,
                       assets: List[Any],
                       mode: Optional[str] = None,
                       audience: str = "general",
                       device: str = "desktop",
                       accessibility: str = "AAA") -> List[InjectionJob]:

        target_mode = mode if mode else self.router.get_mode()
        plan = []

        # 1. Filter assets by pipeline availability in target mode
        filtered_assets = []
        for asset in assets:
            pipeline = asset.get('pipeline', 'Knowledge') # Default if missing
            if self.registry.is_pipeline_allowed_in_mode(pipeline, target_mode):
                filtered_assets.append(asset)

        # 2. Sort assets by priority
        filtered_assets.sort(key=lambda x: self.registry.get_pipeline_priority(x.get('pipeline', 'Knowledge')), reverse=True)

        # 3. Create injection jobs
        for asset in filtered_assets:
            pipeline = asset.get('pipeline', 'Knowledge')
            # Select format based on mode and pipeline preferences
            mode_formats = self.router.get_default_formats(target_mode)
            pipeline_formats = self.registry.get_format_preferences(pipeline)

            # Intersection or fallback
            chosen_formats = [f for f in pipeline_formats if f in mode_formats]
            if not chosen_formats:
                chosen_formats = [mode_formats[0]] if mode_formats else ["HTML"]

            modifiers = self.registry.get_injection_modifiers(pipeline)

            # For simplicity in v3.0, we pick the primary format
            plan.append(InjectionJob(asset, chosen_formats[0], pipeline, modifiers))

        return plan
