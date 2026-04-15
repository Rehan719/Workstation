import logging
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from core.models import EvidenceGraph, EvidenceItem, EvidenceSource

logger = logging.getLogger(__name__)

class ResearchReport(BaseModel):
    research_question: str
    conclusion: str
    confidence: float
    evidence_count: int
    research_log: List[Dict[str, Any]]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DeepResearchEngine:
    """
    Performs autonomous, multi-source, iterative deep research on complex questions.
    """

    def __init__(self, mushahida_engine, jaiza_engine):
        self.mushahida = mushahida_engine
        self.jaiza = jaiza_engine
        self.research_memory: List[ResearchReport] = []

    async def conduct_research(self, question: str, domain_id: str, depth: str = 'standard') -> ResearchReport:
        """Runs the deep research lifecycle."""
        logger.info(f"DeepResearch: Starting investigation for: {question}")
        research_log = []

        # 1. Hypothesis Generation
        hypotheses = await self._generate_hypotheses(question)
        research_log.append({"step": "hypothesis_generation", "count": len(hypotheses)})

        # 2. Multi-source evidence collection (Iterative)
        iterations = 1 if depth == 'fast' else 3 if depth == 'standard' else 5
        all_evidence = []

        for i in range(iterations):
            queries = await self._formulate_queries(question, hypotheses, all_evidence)
            evidence_graph = await self.mushahida.acquire_evidence_async(queries)
            all_evidence.extend(evidence_graph.items)
            research_log.append({"step": "evidence_gathering", "iteration": i+1, "count": len(evidence_graph.items)})

            # Check for early convergence or need for new hypotheses
            if self._check_convergence(all_evidence):
                break

        # 3. Synthesis and Contradiction Resolution
        synthesis = await self.jaiza.analyze_async(EvidenceGraph(items=all_evidence))
        research_log.append({"step": "synthesis", "confidence": synthesis.confidence_intervals.get("overall", 0)})

        report = ResearchReport(
            research_question=question,
            conclusion=f"Investigative synthesis for '{question}' based on {len(all_evidence)} source items.",
            confidence=synthesis.confidence_intervals.get("overall", 0.8),
            evidence_count=len(all_evidence),
            research_log=research_log
        )

        self.research_memory.append(report)
        return report

    async def _generate_hypotheses(self, question: str) -> List[str]:
        """Uses LLM to decompose question into testable hypotheses."""
        prompt = f"Decompose the following research question into 3 testable hypotheses for investigation:\nQuestion: {question}\nOutput: Return a JSON list of strings."
        try:
            from ollama import AsyncClient
            import json
            client = AsyncClient()
            response = await client.generate(model="llama3.1:8b", prompt=prompt)
            text = response['response']
            start = text.find('[')
            end = text.rfind(']') + 1
            return json.loads(text[start:end])
        except Exception as e:
            logger.warning(f"Hypothesis generation fallback: {e}")
            return [f"{question} is occurring", f"{question} has external drivers"]

    async def _formulate_queries(self, question: str, hypotheses: List[str], current_evidence: List[EvidenceItem]) -> List[str]:
        """Uses LLM to generate targeted search queries based on knowledge gaps."""
        context = " ".join([e.content[:200] for e in current_evidence[-5:]])
        prompt = f"Based on the question '{question}' and these hypotheses {hypotheses}, and current knowledge '{context}', generate 4 specific search queries to find missing evidence.\nOutput: Return a JSON list of strings."
        try:
            from ollama import AsyncClient
            import json
            client = AsyncClient()
            response = await client.generate(model="llama3.1:8b", prompt=prompt)
            text = response['response']
            start = text.find('[')
            end = text.rfind(']') + 1
            return json.loads(text[start:end])
        except Exception as e:
            logger.warning(f"Query formulation fallback: {e}")
            return [question] + hypotheses

    def _check_convergence(self, evidence: List[EvidenceItem]) -> bool:
        """Determines if enough evidence has been gathered."""
        if len(evidence) < 5: return False
        if len(evidence) >= 20: return True

        # Check for redundancy in recent evidence
        recent_hashes = [e.sha256 for e in evidence[-3:]]
        return len(set(recent_hashes)) < len(recent_hashes)
