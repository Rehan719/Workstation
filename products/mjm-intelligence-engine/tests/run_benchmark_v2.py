import asyncio
import logging
import time
import sys
import os

# Add product root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.meta_cognition.meta_cognitive_loop import MetaCognitiveLoop
from core.learning.omni.omni_learning_engine import OmniLearningEngine, OmniSignal
from core.research.deep_research_engine import DeepResearchEngine
from core.mushahida.engine import MushahidaEngine
from core.jaiza.engine import JaizaEngine
from core.provenance_graph import ProvenanceGraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BenchmarkV2")

async def run_v2_benchmark():
    logger.info("🧠 Starting Meta-Cognitive Benchmark v2.0")

    prov = ProvenanceGraph()
    mush = MushahidaEngine({}, prov)
    jaiza = JaizaEngine({}, prov)
    meta = MetaCognitiveLoop()
    omni = OmniLearningEngine()
    research = DeepResearchEngine(mush, jaiza)

    # 1. Meta-Cognition: Strategy Selection
    logger.info("Step 1: Meta-Cognitive Strategy Selection")
    context = {"urgency": 0.2, "complexity": 0.9}
    report = await meta.think_about_thinking(context)
    logger.info(f"✅ Strategy Selected: {report.chosen_strategy.name} (Conf: {report.confidence})")

    # 2. Deep Research: Iterative Investigation
    logger.info("Step 2: Autonomous Deep Research")
    question = "Long-term germline risks of AAV gene therapy in pediatrics"
    res_report = await research.conduct_research(question, "patient_safety", depth="standard")
    logger.info(f"✅ Research Completed: {res_report.evidence_count} sources cited. Conf: {res_report.confidence}")

    # 3. Omni-Learning: Signal Ingestion
    logger.info("Step 3: Omni-Learning Ingestion")
    signal = OmniSignal(
        source="deep_research",
        type="execution_outcome",
        payload={"success": True, "strategy_id": report.chosen_strategy.id, "domain_id": "patient_safety"}
    )
    receipt = await omni.omni_ingest(signal)
    logger.info(f"✅ Signal Ingested: {receipt.signal_id}. Patterns extracted: {receipt.patterns_extracted}")

    # 4. Meta-Learning: Evaluation and Improvement
    logger.info("Step 4: Meta-Learning Feedback")
    await meta.evaluate_decision_outcome(report.chosen_strategy.id, 0.96)

    logger.info("🎉 Benchmark v2.0 Completed Successfully")

if __name__ == "__main__":
    asyncio.run(run_v2_benchmark())
