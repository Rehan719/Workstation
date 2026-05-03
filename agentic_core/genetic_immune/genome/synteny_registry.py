import logging
from typing import List, Dict, Any
from .chromosome import Chromosome
from .gene import Gene, GeneType

logger = logging.getLogger(__name__)

class SyntenyRegistry:
    """
    ARTICLE 165: The GENESPACE Synteny Registry.
    Tracks orthologs, paralogs, and copy number variation across versions.
    """
    def __init__(self):
        self.ortholog_groups: Dict[str, List[str]] = {} # group_id -> [gene_ids]
        self.version_history: Dict[str, List[str]] = {} # version -> [gene_ids]
        self.cnv_map: Dict[str, int] = {} # gene_id -> count

    def register_gene_version(self, gene_id: str, version: str, ortholog_group: str):
        if ortholog_group not in self.ortholog_groups:
            self.ortholog_groups[ortholog_group] = []
        self.ortholog_groups[ortholog_group].append(gene_id)

        if version not in self.version_history:
            self.version_history[version] = []
        self.version_history[version].append(gene_id)

        self.cnv_map[gene_id] = self.cnv_map.get(gene_id, 0) + 1

    def detect_paralogs(self, group_id: str) -> List[str]:
        """Identifies duplicated genes within the same functional group."""
        return self.ortholog_groups.get(group_id, [])

    def get_cnv_score(self, gene_id: str) -> int:
        return self.cnv_map.get(gene_id, 1)
