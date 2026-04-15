import logging
import hashlib
from typing import Dict, Any, List
from pydantic import BaseModel
from core.hyperdimensional.hd_omni_learner import HDOmniLearner

logger = logging.getLogger(__name__)

class ProjectToDomainSynthesizer:
    """
    Extracts implicit intelligence genomes from existing project artifacts
    (dossiers, reports, etc.) to instantiate new domains.
    """

    def __init__(self, hd_fabric: HDOmniLearner):
        self.hd = hd_fabric

    async def synthesize_from_project(self, project_data: Dict[str, Any], target_description: str) -> Dict[str, Any]:
        """
        Reverse-engineers a project's blueprint and adapts it to a new domain.
        Uses HD analogies: source_project : target_domain :: source_patterns : target_patterns
        """
        logger.info(f"ProjectToDomain: Extracting blueprint from project: {project_data.get('id', 'unknown')}")

        # 1. Project extraction (Real extraction from project_data)
        source_domain_id = project_data.get("domain_id", "base_domain")
        # Extract patterns from previous analysis if available
        source_patterns = project_data.get("analysis", {}).get("patterns", ["procedural_integrity", "causal_linkage"])

        # 2. HD Analogy
        # Create vectors
        source_vec = self.hd.get_or_create_vector(source_domain_id)
        target_vec = self.hd.get_or_create_vector(target_description)

        # Map string patterns to HD space
        pattern_components = [p if isinstance(p, str) else p.get("pattern_id", "unknown") for p in source_patterns]
        pattern_vec = self.hd.encode_pattern("blueprint", pattern_components)

        # Transfer the blueprint into the new context
        transferred_vec = self.hd.analogical_transfer(source_domain_id, target_description, pattern_vec)

        # Compute similarity to identify best-fit templates (Real computation)
        sim = self.hd.compute_similarity(pattern_vec, transferred_vec)
        logger.info(f"HD Transfer Similarity: {sim:.4f}")

        # 3. Generate new config (Deterministic mapping based on synthesis)
        new_domain_id = f"synth_{hashlib.md5(target_description.encode()).hexdigest()[:8]}"

        return {
            "domain": {
                "id": new_domain_id,
                "name": f"Autonomous {target_description.title()}",
                "description": f"Genome synthesized from {project_data.get('id')} for {target_description}",
                "derived_from": project_data.get('id'),
                "synthesis_fidelity": round(sim, 4)
            },
            "mushahida": project_data.get("mushahida", {"allowed_sources": ["web_search", "academic_db"]}),
            "jaiza": {
                "pattern_libraries": pattern_components,
                "adaptation_logic": "hyperdimensional_transfer"
            },
            "muaina": project_data.get("muaina", {"output_templates": ["markdown", "litigation_bundle"]})
        }
