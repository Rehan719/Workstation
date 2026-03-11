import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VersionResolver:
    """v100.1: Resolves version precedence."""
    def resolve(self, versions: List[str]) -> str:
        if not versions: return "1.0.0"
        # Sort by semver-ish logic
        def sort_key(v):
            return [int(x) for x in v.split('.') if x.isdigit()]

        sorted_v = sorted([v for v in versions if v.replace('.', '').isdigit()], key=sort_key, reverse=True)
        return sorted_v[0] if sorted_v else versions[-1]

class ConflictResolver:
    """v100.1: Resolves conflicts between variations."""
    def resolve_variation(self, variations: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Priority: stable > patch > experimental
        priority = {"stable": 0, "patch": 1, "beta": 2, "alpha": 3, "experimental": 4}
        sorted_vars = sorted(variations, key=lambda x: priority.get(x.get("tag", "experimental"), 5))
        return sorted_vars[0] if sorted_vars else {}
