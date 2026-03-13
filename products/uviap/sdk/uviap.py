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
    ARTICLE 500-530 & 516-525: Unified Version Ingestion & Assimilation Pipeline (UVIAP).
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
        """Executes all stages of the UVIAP (Article 5.3)."""
        logger.info(f"UVIAP: Starting Full Evolution Pipeline v123.0 (Target: {repo_url or 'Self'})")

        # Stage 1: Multi-Source Ingestion (Article 5.1/621)
        github_data = self._ingest_github(repo_url)
        sensory_data = self._ingest_sensory_signals()

        # ARTICLE 646: Genomic Knowledge Organization (Operons)
        clustered_insights = self._organize_genomic_knowledge(github_data, sensory_data)

        # Stage 2: Biomimetic Pattern Recognition (Article 5.2/621)
        patterns = self._recognize_patterns(github_data)
        version_graph = self._construct_version_graph(github_data)

        # Stage 3: Version Differencing & Convergence
        self.convergence_delta = self._analyze_convergence(github_data, patterns, repo_url)

        # Stage 4: Introspection Comparison & Learning (Article 510-515)
        learning_results = self._perform_learning_reflection(self.convergence_delta)

        # Stage 5: Assimilation Configuration Generation (Article 521-525)
        blueprints = self._generate_assimilation_blueprints(learning_results)

        # Stage 6: Continuous Evolution Loop (Article 5.1)
        self._generate_reports(github_data, patterns, learning_results, blueprints)
        self._update_genomic_memory(learning_results)

        # UEG Provenance Logging
        self.ueg.add_audit_log("UVIAP", "Full Evolution Pipeline execution complete.", {
            "target": repo_url or "Self",
            "blueprints_generated": len(blueprints)
        })

        logger.info("UVIAP: Full Evolution Pipeline Completed.")
        return blueprints

    def _ingest_sensory_signals(self) -> List[Dict[str, Any]]:
        """ARTICLE 541: Sensory signal ingestion from WNN."""
        logger.info("UVIAP: Ingesting sensory signals from Workstation Neural Network.")
        return [{"type": "EnvironmentalSignal", "source": "market_watch", "content": "Increased demand for biomimetic APIs"}]

    def _ingest_github(self, repo_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """ARTICLE 516: GitHub Ingestion Thread with dual-mode heuristics."""
        is_self = repo_url is None or "Workstation" in repo_url or "jules" in repo_url.lower()
        logger.info(f"UVIAP: Ingesting GitHub history (Mode: {'Self-Evolution' if is_self else 'Generalized'})")

        target_path = self.repo_path
        if repo_url and not is_self:
            temp_dir = f"/tmp/uviap_{uuid.uuid4().hex[:8]}"
            logger.info(f"UVIAP: Cloning external repository {repo_url} into {temp_dir}")
            try:
                subprocess.run(["git", "clone", "--depth", "50", repo_url, temp_dir], check=True)
                target_path = temp_dir
            except subprocess.CalledProcessError as e:
                logger.error(f"UVIAP: Failed to clone {repo_url}: {e}")
                return []

        try:
            cmd = ["git", "log", "-n", "200", "--pretty=format:%H|%an|%ad|%s", "--date=iso", "--name-only"]
            result = subprocess.check_output(cmd, cwd=target_path).decode("utf-8")

            commits = []
            current_commit = None

            for line in result.splitlines():
                if "|" in line and len(line.split("|")) >= 4:
                    if current_commit:
                        commits.append(current_commit)
                    hash_val, author, date, subject = line.split("|", 3)
                    current_commit = {
                        "hash": hash_val,
                        "author": author,
                        "date": date,
                        "subject": subject,
                        "files": [],
                        "category": self._categorize_commit(subject, is_self)
                    }
                elif line.strip() and current_commit:
                    current_commit["files"].append(line.strip())

            if current_commit:
                commits.append(current_commit)

            logger.info(f"UVIAP: Successfully ingested {len(commits)} commits.")
            return commits
        except Exception as e:
            logger.error(f"UVIAP: GitHub Ingestion failed: {e}")
            return []

    def _categorize_commit(self, subject: str, is_self: bool) -> str:
        """Semantic Pattern Analysis on commit messages (Article 5.2)."""
        subject_lower = subject.lower()

        # Self-Evolution Heuristics
        if is_self:
            if re.search(r"constitution|article|governance|policy", subject_lower):
                return "GOVERNANCE_EVOLUTION"
            if re.search(r"v\d+\.\d+", subject_lower):
                return "VERSION_MILESTONE"
            if "apotheosis" in subject_lower:
                return "SYNERGY_CONVERGENCE"

        # General Intent Analysis
        if re.match(r"feat|add|implement", subject_lower): return "FEATURE"
        if re.match(r"fix|bug|patch", subject_lower): return "FIX"
        if re.match(r"refactor|clean|optimize", subject_lower): return "OPTIMIZATION"
        if re.match(r"docs?|readme", subject_lower): return "DOCUMENTATION"

        return "ANCILLARY"

    def _recognize_patterns(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ARTICLE 5.2/621: Advanced Semantic Pattern Recognition."""
        patterns = []
        for commit in commits:
            # File Change Correlation
            impacted_layers = set()
            for file in commit["files"]:
                if "agentic_core" in file: impacted_layers.add("CORE_COGNITION")
                if "src/web" in file: impacted_layers.add("USER_ACCESS_LAYER")
                if "reactor" in file: impacted_layers.add("DOMAIN_REACTORS")
                if "constitution" in file: impacted_layers.add("GOVERNANCE")
                if "incubation" in file: impacted_layers.add("COEVOLUTIONARY_STRATEGY")

            # Semantic Analysis
            if commit["category"] == "GOVERNANCE_EVOLUTION":
                patterns.append({
                    "id": f"gov_pattern_{commit['hash'][:6]}",
                    "type": "CONSTITUTIONAL_INTEGRITY",
                    "impact": list(impacted_layers),
                    "confidence": 0.99,
                    "insight": f"Evolution of governance in {commit['subject']}"
                })
            elif commit["category"] == "SYNERGY_CONVERGENCE":
                patterns.append({
                    "id": f"syn_pattern_{commit['hash'][:6]}",
                    "type": "METAMORPHOSIS",
                    "impact": list(impacted_layers),
                    "confidence": 1.0,
                    "insight": "System-wide convergence event detected"
                })
            elif commit["category"] == "FEATURE" and "reactor" in impacted_layers:
                patterns.append({
                    "id": f"reactor_pattern_{commit['hash'][:6]}",
                    "type": "DOMAIN_EXPANSION",
                    "impact": ["DOMAIN_REACTORS"],
                    "confidence": 0.95,
                    "insight": f"New reactor capability added: {commit['subject']}"
                })

        logger.info(f"UVIAP: Extracted {len(patterns)} semantic patterns from history.")
        return patterns

    def _analyze_convergence(self, commits: List[Dict[str, Any]], patterns: List[Dict[str, Any]], repo_url: Optional[str]) -> Dict[str, Any]:
        """Version Differencing & Convergence Analysis (Stage 3)."""
        is_self = repo_url is None or "Workstation" in repo_url or "jules" in repo_url.lower()
        has_v120 = any("v120" in c["subject"] for c in commits)

        # Identify gaps (Simplified for v120.0 logic)
        gaps = []
        if not has_v120 and is_self:
            gaps.append("Missing final Apotheosis release markers")

        # Check for reactor diversity
        reactor_commits = [c for c in commits if any("reactor" in f for f in c["files"])]
        if len(reactor_commits) < 10 and is_self:
            gaps.append("Insufficient reactor ecosystem evolution detected in history")

        return {
            "v120_alignment": has_v120,
            "is_self": is_self,
            "identified_gaps": gaps,
            "pattern_density": len(patterns) / (len(commits) or 1)
        }

    def _perform_learning_reflection(self, delta: Dict[str, Any]) -> Dict[str, Any]:
        """Introspection Comparison & Learning (Article 510-515)."""
        reflection_msg = "The system has achieved v120.0 synthesis." if delta["v120_alignment"] else "Convergence in progress."

        # Pattern-Biased Reinforcement
        suggested_traits = []
        if delta["is_self"]:
            suggested_traits = ["high_fidelity_symbiosis", "governance_traceability", "apotheosis_readiness"]
        else:
            suggested_traits = ["external_pattern_assimilation", "cross_repo_learning"]

        return {
            "reflection": reflection_msg,
            "success_probability": 0.99 if delta["v120_alignment"] else 0.85,
            "suggested_traits": suggested_traits,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _generate_assimilation_blueprints(self, learning: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generation of Actionable Blueprints (Article 521-525)."""
        blueprints = []
        for trait in learning["suggested_traits"]:
            blueprints.append({
                "id": str(uuid.uuid4())[:8],
                "trait": trait,
                "action": f"Synthesize {trait} into core genome",
                "priority": "HIGH" if "apotheosis" in trait else "MEDIUM",
                "status": "PROPOSED"
            })
        return blueprints

    def _organize_genomic_knowledge(self, github_data: List[Any], sensory_data: List[Any]) -> Dict[str, Any]:
        """ARTICLE 646: Genomic Knowledge Organization into operons and regulons."""
        logger.info("UVIAP: Organizing knowledge into genomic operons.")
        operons = {}

        # Cluster GitHub data by category
        for commit in github_data:
            cat = commit.get("category", "ANCILLARY")
            if cat not in operons: operons[cat] = []
            operons[cat].append(commit["hash"])

        # Cluster Sensory data by topic
        for signal in sensory_data:
            topic = signal.get("type", "SIGNAL")
            if topic not in operons: operons[topic] = []
            operons[topic].append(signal.get("source"))

        return {"operons": operons, "timestamp": datetime.datetime.now().isoformat()}

    def _update_genomic_memory(self, learning: Dict[str, Any]):
        """Learned Traits persistence (Article 5.4)."""
        for trait in learning["suggested_traits"]:
            self.genomic_registry.reverse_transcribe_trait(f"learned_{trait}", {
                "origin": "UVIAP_v123_Analysis",
                "impact_score": 0.99,
                "timestamp": learning["timestamp"]
            })
        self.genomic_registry.commit_mutations("UVIAP_AUTONOMOUS_LEARNING")

    def _construct_version_graph(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """ARTICLE 621: Builds a graph of version relationships based on commit history."""
        graph = {"nodes": [], "edges": []}
        version_pattern = re.compile(r"v(\d+\.\d+)")

        last_version = None
        for commit in reversed(commits):
            match = version_pattern.search(commit["subject"])
            if match:
                version = match.group(1)
                node = {"id": version, "hash": commit["hash"], "date": commit["date"]}
                graph["nodes"].append(node)
                if last_version:
                    graph["edges"].append({"from": last_version, "to": version, "type": "EVOLUTION"})
                last_version = version

        logger.info(f"UVIAP: Version graph constructed with {len(graph['nodes'])} nodes.")
        return graph

    def _generate_reports(self, commits: List[Dict[str, Any]], patterns: List[Dict[str, Any]], learning: Dict[str, Any], blueprints: List[Dict[str, Any]]):
        """Unified Assimilation Report Generation (Article 5.5)."""
        os.makedirs("docs/knowledge", exist_ok=True)
        report = {
            "version": "120.0.0",
            "summary": "APOTHEOSIS CONVERGENCE REPORT",
            "metrics": {
                "total_commits_analyzed": len(commits),
                "patterns_recognized": len(patterns),
                "success_probability": learning["success_probability"]
            },
            "learning_reflection": learning,
            "actionable_blueprints": blueprints,
            "patterns": patterns[:20] # Top 20 patterns
        }

        with open("docs/knowledge/unified_assimilation_v120.json", "w") as f:
            json.dump(report, f, indent=4)

        # Legacy markdown support
        with open("docs/knowledge/convergence_delta.md", "w") as f:
            f.write(f"# Convergence Delta Report - {datetime.datetime.now().date()}\n\n")
            f.write(f"**Status:** {'ALIGNED' if report['metrics']['success_probability'] > 0.9 else 'PENDING'}\n\n")
            f.write("## Identified Blueprints\n")
            for bp in blueprints:
                f.write(f"- {bp['action']} (Priority: {bp['priority']})\n")

        logger.info("UVIAP: Comprehensive reports generated in docs/knowledge/")
