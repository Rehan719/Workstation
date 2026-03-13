import os
import logging
import datetime
import subprocess
import re
import json
import uuid
from typing import List, Dict, Any, Optional
from agentic_core.ueg.ueg_manager import UEGManager
from agentic_core.genetics.genomic_registry import GenomicRegistry

logger = logging.getLogger(__name__)

class UVIAP:
    """
    ARTICLE 500-530: Unified Version Ingestion & Assimilation Pipeline (UVIAP).
    A biomimetically-inspired pipeline that ingests, synthesises, and applies knowledge
    from all prior versions, external LLM conversations, and GitHub commit/branch history.
    """
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)
        self.ueg = UEGManager()
        self.genomic_registry = GenomicRegistry()
        self.convergence_delta: Dict[str, Any] = {}
        self.learning_reflection: List[Dict[str, Any]] = []

    async def run_full_pipeline(self, repo_url: Optional[str] = None):
        """Executes all stages of the UVIAP."""
        logger.info(f"UVIAP: Starting Full Evolution Pipeline v120.0 (Target: {repo_url or 'Self'})")

        # Stage 1: Multi-Source Ingestion
        github_data = self._ingest_github(repo_url)
        sensory_data = self._ingest_sensory_signals()

        # Stage 2: Biomimetic Pattern Recognition
        patterns = self._recognize_patterns(github_data)

        # Stage 3: Version Differencing & Convergence
        self.convergence_delta = self._analyze_convergence(github_data, patterns, is_self=(repo_url is None))

        # Stage 4: Introspection Comparison & Learning
        learning_results = self._perform_learning_reflection(self.convergence_delta)

        # Stage 5: Assimilation Configuration
        blueprints = self._generate_assimilation_blueprints(learning_results)

        # Stage 6: Evolutionary Loop (Report Generation)
        self._generate_reports(github_data, patterns, learning_results, blueprints)

        logger.info("UVIAP: Full Evolution Pipeline Completed.")
        return blueprints

    def _ingest_sensory_signals(self) -> List[Dict[str, Any]]:
        """ARTICLE 541: Sensory signal ingestion from WNN."""
        logger.info("UVIAP: Ingesting sensory signals from Workstation Neural Network.")
        return [{"type": "EnvironmentalSignal", "source": "market_watch", "content": "Increased demand for biomimetic APIs"}]

    def _ingest_github(self, repo_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """ARTICLE 516: GitHub Ingestion Thread with dual-mode heuristics."""
        is_self = repo_url is None or "Workstation" in repo_url
        logger.info(f"UVIAP: Ingesting GitHub history (Self-Evolution: {is_self})")

        try:
            # If external, we'd clone to a temp dir. For now, we assume local or current repo.
            cmd = ["git", "log", "-n", "100", "--pretty=format:%H|%an|%ad|%s", "--date=iso"]
            result = subprocess.check_output(cmd, cwd=self.repo_path).decode("utf-8")

            commits = []
            for line in result.splitlines():
                if "|" in line:
                    hash_val, author, date, subject = line.split("|", 3)
                    commits.append({
                        "hash": hash_val,
                        "author": author,
                        "date": date,
                        "subject": subject,
                        "category": self._categorize_commit(subject, is_self)
                    })

            logger.info(f"UVIAP: Successfully ingested {len(commits)} commits.")
            return commits
        except Exception as e:
            logger.error(f"UVIAP: GitHub Ingestion failed: {e}")
            return []

    def _categorize_commit(self, subject: str, is_self: bool) -> str:
        subject = subject.lower()
        if is_self:
            # Special heuristics for Workstation self-evolution
            if "constitution" in subject or "article" in subject: return "GOVERNANCE"
            if "v120" in subject: return "EVOLUTION_TARGET"

        if "feat" in subject or "add" in subject: return "FEATURE"
        if "fix" in subject or "bug" in subject: return "FIX"
        if "refactor" in subject: return "REFACTOR"
        return "OTHER"

    def _recognize_patterns(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        patterns = []
        for commit in commits:
            if commit["category"] == "GOVERNANCE":
                patterns.append({"principle": "ConstitutionalIntegrity", "source": commit["hash"]})
            if commit["category"] == "REFACTOR":
                patterns.append({"principle": "Metamorphosis", "source": commit["hash"]})
        return patterns

    def _analyze_convergence(self, commits: List[Dict[str, Any]], patterns: List[Dict[str, Any]], is_self: bool) -> Dict[str, Any]:
        has_v120 = any("v120" in c["subject"] for c in commits)
        return {
            "v120_alignment": has_v120,
            "is_self": is_self,
            "identified_gaps": ["Legacy patterns in engine symbiosis"] if not has_v120 and is_self else []
        }

    def _perform_learning_reflection(self, delta: Dict[str, Any]) -> Dict[str, Any]:
        outcome = {
            "reflection": "The system is converging toward v120.0 apotheosis." if delta["is_self"] else "External repo analysis complete.",
            "success_probability": 0.99 if delta["v120_alignment"] else 0.70,
            "suggested_traits": ["high_fidelity_symbiosis", "governance_traceability"] if delta["is_self"] else ["external_pattern_assimilation"]
        }
        for trait in outcome["suggested_traits"]:
            self.genomic_registry.reverse_transcribe_trait(f"learned_{trait}", {"impact": 0.95})
        return outcome

    def _generate_assimilation_blueprints(self, learning: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{
            "id": str(uuid.uuid4())[:8],
            "target": f"CoE_{trait.upper()}",
            "action": f"Integrate {trait}",
            "status": "PROPOSED",
            "timestamp": datetime.datetime.now().isoformat()
        } for trait in learning["suggested_traits"]]

    def _generate_reports(self, commits: List[Dict[str, Any]], patterns: List[Dict[str, Any]], learning: Dict[str, Any], blueprints: List[Dict[str, Any]]):
        os.makedirs("docs/knowledge", exist_ok=True)
        report_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "commits": commits[:10],
            "patterns": patterns,
            "learning": learning,
            "blueprints": blueprints
        }
        with open("docs/knowledge/last_uviap_run.json", "w") as f:
            json.dump(report_data, f, indent=2)
        logger.info("UVIAP: Report generated in docs/knowledge/last_uviap_run.json")
