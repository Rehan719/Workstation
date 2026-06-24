"""
Workstation Meta API — real, live data about the Workstation project itself
(not the avatar/business domains), for the "Projects & Sessions" dock.

`git_history` shells out to the actual `git log` for this repo — genuine
commit activity, not sample/placeholder data. No fabricated entries: if git
isn't available or the call fails, this returns a real 503 rather than fake
commits.
"""
import subprocess
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/workstation", tags=["Workstation Meta"])

# agentic_core/analysis/api.py -> agentic_core/analysis -> agentic_core -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]


class CommitEntry(BaseModel):
    hash: str
    author: str
    date: str
    message: str


class GitHistoryResponse(BaseModel):
    branch: str
    commits: List[CommitEntry]


@router.get("/git-history", response_model=GitHistoryResponse)
async def git_history(limit: int = 30):
    """Real `git log` output for this repo — actual commit hashes, authors,
    timestamps, and messages. Capped to a sane range to keep this endpoint fast."""
    limit = max(1, min(limit, 200))
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT, timeout=5,
        ).decode("utf-8", errors="replace").strip()

        raw = subprocess.check_output(
            ["git", "log", f"-{limit}", "--pretty=format:%h|%an|%ad|%s", "--date=iso-strict"],
            cwd=REPO_ROOT, timeout=10,
        ).decode("utf-8", errors="replace")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Could not read git history: {str(e)[:200]}")

    commits: List[CommitEntry] = []
    for line in raw.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            h, a, d, s = parts
            commits.append(CommitEntry(hash=h, author=a, date=d, message=s))

    return GitHistoryResponse(branch=branch, commits=commits)
