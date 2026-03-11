from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class BaseCollator(ABC):
    """Abstract base for all v100.1 collators."""

    @abstractmethod
    async def collate(self, source_dir: str) -> Dict[str, Any]:
        """Extract versions/variations from source files."""
        pass

    def generate_report(self, data: Dict[str, Any]) -> str:
        """Return markdown report of collation results."""
        report = f"# Collation Report\n\nFound {len(data.get('versions', []))} versions.\n"
        return report
