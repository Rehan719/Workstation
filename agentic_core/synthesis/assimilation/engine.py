import logging
from typing import Dict, Any
from .components import CodePatcher, ConstitutionUpdater, EngineReconfigurator

logger = logging.getLogger(__name__)

class AssimilationEngine:
    """v100.1: Transactional integration of converged configurations."""
    def __init__(self):
        self.patcher = CodePatcher()
        self.constitution = ConstitutionUpdater()
        self.reconfig = EngineReconfigurator()

    async def assimilate_all(self, converged_configs: Dict[str, Any]):
        logger.info("Starting v100.1 Assimilation cycle...")

        for category, config in converged_configs.items():
            success = self.patcher.apply_patch(category, config)
            if not success:
                logger.error(f"Assimilation failed at patch stage for {category}")
                return False

        self.constitution.update(converged_configs)
        self.reconfig.reconfigure(converged_configs)

        logger.info("v100.1 Assimilation complete.")
        return True
