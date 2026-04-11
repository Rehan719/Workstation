import logging
import json
import asyncio
from typing import List, Dict, Any, Optional
from ollama import AsyncClient
from core.models import EvidenceGraph, AnalysisDossier
from core.provenance_graph import ProvenanceGraph

logger = logging.getLogger(__name__)

class JaizaEngine:
    """
    Review / Evaluation / Survey Layer
    - Contextual analysis using pattern recognition AI
    - Risk-benefit assessment with configurable weighting schemas
    """
    def __init__(self, domain_config: Dict[str, Any], provenance: ProvenanceGraph):
        self.config = domain_config
        self.provenance = provenance
        self.jaiza_config = self.config.get("jaiza", {})
        self.model = "llama3.1:8b" # Default model

    def analyze(self, graph: EvidenceGraph) -> AnalysisDossier:
        """Synchronous wrapper for async analysis."""
        return asyncio.run(self.analyze_async(graph))

    async def analyze_async(self, graph: EvidenceGraph) -> AnalysisDossier:
        logger.info(f"Analyzing evidence graph with {len(graph.items)} items")

        # Prepare context for LLM
        context_text = self._prepare_llm_context(graph)

        try:
            analysis_data = await self._run_llm_analysis(context_text)
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}. Falling back to rule-based analysis.")
            analysis_data = self._run_rule_based_analysis(graph)

        dossier = AnalysisDossier(
            evidence_graph_ref=graph.sha256 or "unknown",
            patterns=analysis_data.get("patterns", []),
            risks=analysis_data.get("risks", []),
            strategic_options=analysis_data.get("strategic_options", []),
            regulatory_compliance=analysis_data.get("regulatory_compliance", {}),
            confidence_intervals=analysis_data.get("confidence_intervals", {"overall": 0.75})
        )

        dossier.calculate_hash()

        # Record in provenance
        parent_ids = [item.provenance_id for item in graph.items if item.provenance_id]
        prov_id = self.provenance.add_node(
            node_type="analysis",
            content=dossier.model_dump_json(),
            parents=parent_ids,
            metadata={"engine": "jaiza", "model": self.model if "patterns" in analysis_data else "rule-based"}
        )

        return dossier

    def _prepare_llm_context(self, graph: EvidenceGraph) -> str:
        context = "Evidence for Intelligence Assessment:\n"
        for i, item in enumerate(graph.items):
            context += f"Source {i+1} ({item.source.uri}): {item.content[:500]}...\n\n"
        return context

    async def _run_llm_analysis(self, context: str) -> Dict[str, Any]:
        prompt = f"""
        System: You are the Jaiza (Evaluation) Engine of the MJM Intelligence Framework.
        Task: Analyze the following evidence for patterns, risks, and strategic options.
        Output: Respond ONLY with a valid JSON object matching the following structure:
        {{
            "patterns": [{{ "name": string, "description": string }}],
            "risks": [{{ "type": string, "severity": "low"|"medium"|"high", "description": string }}],
            "strategic_options": [{{ "id": string, "description": string, "expected_outcome": string }}],
            "regulatory_compliance": {{ "status": string, "violations": [] }},
            "confidence_intervals": {{ "overall": float }}
        }}

        Evidence:
        {context}
        """

        client = AsyncClient()
        response = await client.generate(model=self.model, prompt=prompt)
        # Attempt to parse JSON from response
        try:
            # Basic JSON extraction in case of conversational padding
            text = response['response']
            start = text.find('{')
            end = text.rfind('}') + 1
            return json.loads(text[start:end])
        except Exception as e:
            logger.warning(f"Failed to parse LLM JSON: {e}")
            raise

    def _run_rule_based_analysis(self, graph: EvidenceGraph) -> Dict[str, Any]:
        """Heuristic fallback for Zero-Placeholder compliance."""
        patterns = []
        risks = []

        # Simple keyword-based heuristics
        combined_text = " ".join([i.content.lower() for i in graph.items])

        if "risk" in combined_text or "danger" in combined_text or "hazard" in combined_text:
            risks.append({"type": "safety_risk", "severity": "medium", "description": "Keywords indicating risk detected in evidence."})

        if "policy" in combined_text or "regulation" in combined_text:
            patterns.append({"name": "regulatory_focus", "description": "Evidence frequently mentions policy or regulatory frameworks."})

        return {
            "patterns": patterns or [{"name": "baseline_observation", "description": "Standard evidence accumulation detected."}],
            "risks": risks or [{"type": "information_gap", "severity": "low", "description": "No explicit risks identified via heuristic search."}],
            "strategic_options": [
                {"id": "opt-1", "description": "Continuous Monitoring", "expected_outcome": "Early detection of emerging patterns"},
                {"id": "opt-2", "description": "In-depth Investigation", "expected_outcome": "Clarification of ambiguous evidence"}
            ],
            "regulatory_compliance": {"status": "unverified", "violations": []},
            "confidence_intervals": {"overall": 0.6}
        }
