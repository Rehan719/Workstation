import subprocess
import re
import json
import logging
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class EnhancedGitHistoryAnalyzer:
    """
    SUPREME GIT ANALYSIS PIPELINE.
    Forensically reconstructs the Workstation evolutionary record.
    """
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def analyze_full_history(self) -> List[Dict[str, Any]]:
        logger.info("GitAnalyzer: Initiating forensic deep-dive into commit history...")
        try:
            # 1. Get full log with file stats and diff summaries
            cmd = ["git", "log", "--pretty=format:%H|%an|%ad|%s", "--name-status", "--all"]
            result = subprocess.check_output(cmd, cwd=self.repo_path).decode("utf-8")

            # 2. Get Tags
            tags_cmd = ["git", "tag", "-l"]
            tags = subprocess.check_output(tags_cmd, cwd=self.repo_path).decode("utf-8").splitlines()

            commits = []
            current_commit = None

            for line in result.splitlines():
                if "|" in line and len(line.split("|")) == 4:
                    if current_commit:
                        commits.append(current_commit)
                    h, a, d, s = line.split("|")
                    current_commit = {
                        "commit_hash": h,
                        "author": a,
                        "timestamp": d,
                        "message": s,
                        "files_changed": [],
                        "inferred_version": self._infer_version(s),
                        "tags": [t for t in tags if self._is_tag_at_commit(t, h)]
                    }
                elif line.strip() and current_commit:
                    current_commit["files_changed"].append(line.strip())

            if current_commit:
                commits.append(current_commit)

            logger.info(f"GitAnalyzer: Mapped {len(commits)} commits to the evolutionary record.")
            return commits
        except Exception as e:
            logger.error(f"GitAnalyzer: Forensic audit failed: {e}")
            return []

    def _infer_version(self, message: str) -> str:
        # Improved regex for Workstation versioning patterns
        match = re.search(r"v(\d+\.\d+(\.\d+)?)", message)
        if match: return f"v{match.group(1)}"
        if "Apotheosis" in message: return "v120.0"
        if "Galactic" in message: return "v138.0"
        return "v0.0.0"

    def _is_tag_at_commit(self, tag: str, commit_hash: str) -> bool:
        try:
            tag_hash = subprocess.check_output(["git", "rev-list", "-n", "1", tag], cwd=self.repo_path).decode("utf-8").strip()
            return tag_hash == commit_hash
        except:
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    analyzer = EnhancedGitHistoryAnalyzer()
    history = analyzer.analyze_full_history()
    os.makedirs("docs/knowledge", exist_ok=True)
    with open("docs/knowledge/git_forensic_deep_analysis.json", "w") as f:
        json.dump(history, f, indent=2)
