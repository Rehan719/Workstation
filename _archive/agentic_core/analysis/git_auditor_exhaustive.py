import subprocess
import json
import logging
import re
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ExhaustiveBranchAuditor:
    """
    ULTIMATE GIT AUDIT PIPELINE v2.0.
    Performs forensic reconstruction of every commit across all branches.
    """
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def audit_all_branches(self) -> List[Dict[str, Any]]:
        logger.info("GitAuditor: Initiating exhaustive multi-branch audit...")
        try:
            # 1. Get exhaustive log for all branches
            cmd = ["git", "log", "--all", "--pretty=format:%H|%an|%ad|%s", "--name-status"]
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
                        "intent": self._infer_intent(s),
                        "version": self._extract_version(s)
                    }
                elif line.strip() and current_commit:
                    current_commit["files"].append(line.strip())

            if current_commit:
                commits.append(current_commit)

            # 2. Map branch membership
            for commit in commits:
                commit["branches"] = self._get_branches_for_commit(commit["hash"])

            logger.info(f"GitAuditor: Audit complete for {len(commits)} commits across all branches.")
            return commits
        except Exception as e:
            logger.error(f"GitAuditor: Audit failed: {e}")
            return []

    def _infer_intent(self, msg: str) -> str:
        msg = msg.lower()
        if "feat" in msg: return "FEATURE"
        if "fix" in msg: return "FIX"
        if "refactor" in msg: return "REFACTOR"
        if "merge" in msg: return "MERGE"
        if "docs" in msg: return "DOCS"
        return "EVOLUTION"

    def _extract_version(self, msg: str) -> str:
        match = re.search(r"v(\d+\.\d+(\.\d+)?)", msg)
        return f"v{match.group(1)}" if match else "v0.0.0"

    def _get_branches_for_commit(self, commit_hash: str) -> List[str]:
        try:
            cmd = ["git", "branch", "-a", "--contains", commit_hash]
            result = subprocess.check_output(cmd, cwd=self.repo_path).decode("utf-8")
            return [b.strip().replace("* ", "") for b in result.splitlines()]
        except:
            return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    auditor = ExhaustiveBranchAuditor()
    audit_data = auditor.audit_all_branches()
    os.makedirs("docs/knowledge", exist_ok=True)
    with open("docs/knowledge/commit_analysis_exhaustive.json", "w") as f:
        json.dump(audit_data, f, indent=2)
