import logging
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class SwarmFinding(BaseModel):
    agent_id: str
    role: str
    content: str
    confidence: float

class SuperResearchReport(BaseModel):
    question: str
    consensus: str
    findings: List[SwarmFinding]
    agreement_score: float

from ollama import AsyncClient
import json

class ResearchAgent:
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.model = "llama3.1:8b"

    async def investigate(self, question: str) -> SwarmFinding:
        """Role-specific investigation using LLM."""
        prompt = f"""
        System: You are a Research Agent with the role of '{self.role}'.
        Task: Provide a deep investigative perspective on the following question from your role's specific viewpoint.
        Question: {question}
        Output: Respond with a concise paragraph of your findings and a confidence score (0.0 to 1.0).
        Format: JSON {{ "content": "...", "confidence": 0.8 }}
        """
        try:
            client = AsyncClient()
            response = await client.generate(model=self.model, prompt=prompt)
            text = response['response']
            start = text.find('{')
            end = text.rfind('}') + 1
            data = json.loads(text[start:end])
            return SwarmFinding(
                agent_id=self.agent_id,
                role=self.role,
                content=data.get("content", f"Failed to extract {self.role} content"),
                confidence=data.get("confidence", 0.5)
            )
        except Exception as e:
            logger.error(f"Agent {self.agent_id} ({self.role}) failed: {e}")
            return SwarmFinding(
                agent_id=self.agent_id,
                role=self.role,
                content=f"Error in {self.role} investigation: {str(e)}",
                confidence=0.0
            )

class SuperResearchSwarm:
    """
    Orchestrates specialized research agents to investigate complex questions.
    Uses structured debate and consensus synthesis.
    """

    def __init__(self, agent_roles: List[str] = None):
        self.roles = agent_roles or ["skeptic", "innovator", "synthesizer", "historian"]
        self.agents = [ResearchAgent(f"A-{i}", role) for i, role in enumerate(self.roles)]
        self.model = "llama3.1:8b"

    async def conduct_super_research(self, question: str, domain_id: str) -> SuperResearchReport:
        """Spawn agents and converge on consensus findings."""
        logger.info(f"Swarm: Investigating '{question}' in domain '{domain_id}'")

        # 1. Individual Investigations
        tasks = [agent.investigate(question) for agent in self.agents]
        findings = await asyncio.gather(*tasks)

        # 2. Consensus Synthesis
        consensus_prompt = f"""
        System: You are the Swarm Synthesizer.
        Task: Synthesize a consensus from the following research findings from different roles.
        Question: {question}
        Findings:
        {json.dumps([f.model_dump() for f in findings], indent=2)}
        Output: Respond with a definitive consensus statement and an overall agreement score (0.0 to 1.0).
        Format: JSON {{ "consensus": "...", "agreement_score": 0.85 }}
        """
        try:
            client = AsyncClient()
            response = await client.generate(model=self.model, prompt=consensus_prompt)
            text = response['response']
            start = text.find('{')
            end = text.rfind('}') + 1
            data = json.loads(text[start:end])
            consensus = data.get("consensus", "No consensus reached due to synthesis failure.")
            agreement_score = data.get("agreement_score", 0.0)
        except Exception as e:
            logger.error(f"Swarm synthesis failed: {e}")
            consensus = f"Consensus synthesis failed: {str(e)}"
            agreement_score = 0.0

        return SuperResearchReport(
            question=question,
            consensus=consensus,
            findings=findings,
            agreement_score=agreement_score
        )
