import subprocess
import json
import logging
import re
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ExhaustiveGitAuditor:
    """
    ULTIMATE GIT AUDIT PIPELINE.
    Performs forensic reconstruction of every commit, diff, and intent.
    """
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def audit_all_commits(self) -> List[Dict[str, Any]]:
        logger.info("GitAuditor: Initiating bit-for-bit forensic audit...")
        try:
            # 1. Get exhaustive log
            cmd = ["git", "log", "--pretty=format:%H|%an|%ad|%s", "--name-status", "--all"]
            result = subprocess.check_output(cmd, cwd=self.repo_path).decode("utf-8")

            commits = []
            current_commit = None

            for line in result.splitlines():
                if "|" in line and len(line.split("|")) == 4:
                    if current_commit:
                        commits.append(current_commit)
                    h, a, d, s = line.split("|")
                    current_commit = {
                        "hash": h,
                        "author": a,
                        "timestamp": d,
                        "message": s,
                        "files": [],
                        "inferred_intent": self._analyze_intent(s),
                        "version_marker": self._extract_version(s)
                    }
                elif line.strip() and current_commit:
                    current_commit["files"].append(line.strip())

            if current_commit:
                commits.append(current_commit)

            # 2. Extract full diff summaries for each commit
            for commit in commits:
                commit["impact_summary"] = self._get_diff_summary(commit["hash"])

            logger.info(f"GitAuditor: Audit complete for {len(commits)} commits.")
            return commits
        except Exception as e:
            logger.error(f"GitAuditor: Audit failed: {e}")
            return []

    def _analyze_intent(self, msg: str) -> str:
        msg = msg.lower()
        if "feat" in msg: return "FEATURE_INTRODUCTION"
        if "fix" in msg: return "BUG_RESOLUTION"
        if "refactor" in msg: return "CODE_OPTIMIZATION"
        if "docs" in msg: return "DOCUMENTATION_ENHANCEMENT"
        if "merge" in msg: return "BRANCH_CONSOLIDATION"
        return "GENERIC_EVOLUTION"

    def _extract_version(self, msg: str) -> str:
        match = re.search(r"v(\d+\.\d+(\.\d+)?)", msg)
        return match.group(1) if match else None

    def _get_diff_summary(self, commit_hash: str) -> str:
        try:
            cmd = ["git", "show", "--summary", commit_hash]
            return subprocess.check_output(cmd, cwd=self.repo_path).decode("utf-8")
        except:
            return "Summary unavailable."

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    auditor = ExhaustiveGitAuditor()
    audit_data = auditor.audit_all_commits()
    os.makedirs("docs/knowledge", exist_ok=True)
    with open("docs/knowledge/commit_analysis_raw.json", "w") as f:
        json.dump(audit_data, f, indent=2)
