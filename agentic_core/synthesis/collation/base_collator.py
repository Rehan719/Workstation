from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class BaseCollator(ABC):
    """Abstract base for all v101.x collators."""

    @abstractmethod
    async def collate(self, source_dir: str) -> Dict[str, Any]:
        """Extract versions/variations from source files."""
        pass
