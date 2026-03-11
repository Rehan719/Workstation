import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VersionResolver:
    """v101.0: Semver-based version resolution."""
    def resolve(self, versions: List[str]) -> str:
        if not versions: return "100.0.0"
        def sort_key(v):
            return [int(x) for x in v.split('.') if x.isdigit()]
        sorted_v = sorted([v for v in versions if v.replace('.', '').isdigit()], key=sort_key, reverse=True)
        return sorted_v[0] if sorted_v else versions[-1]

class ConflictResolver:
    """v101.0: Resolves variations by tag priority."""
    def resolve_variation(self, variations: List[Dict[str, Any]]) -> Dict[str, Any]:
        priority = {"stable": 0, "patch": 1, "beta": 2, "alpha": 3, "experimental": 4}
        sorted_vars = sorted(variations, key=lambda x: priority.get(x.get("tag", "experimental"), 5))
        return sorted_vars[0] if sorted_vars else {}
