import logging
from typing import Dict, Any, List
from enum import Enum

logger = logging.getLogger(__name__)

class GermLayer(Enum):
    ECTODERM = "ui"
    MESODERM = "logic"
    ENDODERM = "infrastructure"

class GermLayerStratification:
    """
    ARTICLE 161: Germ Layer Permission Stratification.
    Enforces access controls between UI, Logic, and Infrastructure layers.
    """

    @classmethod
    def validate_access(cls, actor_layer: GermLayer, target_layer: GermLayer) -> bool:
        """
        Enforces access rules:
        - UI (Ectoderm) cannot directly access Infrastructure (Endoderm).
        - Logic (Mesoderm) can access both.
        """
        if actor_layer == GermLayer.ECTODERM and target_layer == GermLayer.ENDODERM:
            logger.warning("PERMISSION: Ectoderm attempt to bypass Mesoderm to access Endoderm.")
            return False
        return True
