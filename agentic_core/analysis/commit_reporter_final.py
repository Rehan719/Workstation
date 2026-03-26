import json
import logging

logger = logging.getLogger(__name__)

class FinalCommitReporter:
    """
    ARTICLE 5.1: Repository Forensic Summary.
    Analyzes and summarizes every commit across all branches for the Main 0.0 baseline.
    """
    def __init__(self):
        self.commit_data = "docs/knowledge/commit_analysis_exhaustive.json"

    def generate(self):
        logger.info("CommitReporter: Generating ultimate history report...")

        with open(self.commit_data, "r") as f:
            commits = json.load(f)

        content = "# WORKSTATION COMMIT ANALYSIS REPORT FINAL\n\n"
        content += "## Forensic Audit of the Workstation Git Record\n\n"

        # Summary Stats
        content += "### Summary Statistics\n"
        content += f"- **Total Commits Analyzed**: {len(commits)}\n"
        content += f"- **Authors Identified**: {len(set(c['author'] for c in commits))}\n"
        content += f"- **Branches Mapped**: {len(set([b for c in commits for b in c['branches']]))}\n\n"

        content += "## Detailed Commit Log\n\n"
        for c in commits:
            content += f"### Commit {c['hash'][:8]}\n"
            content += f"- **Author**: {c['author']}\n"
            content += f"- **Intent**: {c['intent']}\n"
            content += f"- **Branches**: {', '.join(c['branches']) if c['branches'] else 'Main'}\n"
            content += f"- **Message**: {c['message']}\n"
            content += f"- **Files**: {len(c['files'])} paths impacted.\n\n"

        with open("COMMIT_ANALYSIS_REPORT.md", "w") as f:
            f.write(content)

        logger.info("CommitReporter: COMMIT_ANALYSIS_REPORT.md generated.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reporter = FinalCommitReporter()
    reporter.generate()
