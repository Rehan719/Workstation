import subprocess
import re
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GitHistoryAnalyzer:
    """
    ULTIMATE GIT ANALYSIS PIPELINE.
    Performs forensic reconstruction of version history from Git commits.
    """
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def analyze_full_history(self) -> List[Dict[str, Any]]:
        logger.info("GitAnalyzer: Starting forensic reconstruction of commit history...")
        try:
            # Get full log with all details
            cmd = ["git", "log", "--pretty=format:%H|%an|%ad|%s", "--name-status"]
            result = subprocess.check_output(cmd, cwd=self.repo_path).decode("utf-8")

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
                        "inferred_version": self._infer_version(s)
                    }
                elif line.strip() and current_commit:
                    current_commit["files_changed"].append(line.strip())

            if current_commit:
                commits.append(current_commit)

            logger.info(f"GitAnalyzer: Successfully analyzed {len(commits)} commits.")
            return commits
        except Exception as e:
            logger.error(f"GitAnalyzer: History analysis failed: {e}")
            return []

    def _infer_version(self, message: str) -> str:
        match = re.search(r"v(\d+\.\d+(\.\d+)?)", message)
        return match.group(1) if match else "0.0.0"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    analyzer = GitHistoryAnalyzer()
    history = analyzer.analyze_full_history()
    with open("docs/knowledge/git_forensic_analysis.json", "w") as f:
        json.dump(history, f, indent=2)
