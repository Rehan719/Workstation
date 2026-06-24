import json
import logging

logger = logging.getLogger(__name__)

class CommitReportGenerator:
    """
    ARTICLE 5.1: Commit History Traceability.
    Summarizes the impact of every repo commit on the Main 0.0 baseline.
    """
    def __init__(self):
        self.commit_data = "docs/knowledge/commit_analysis_raw.json"

    def generate_report(self):
        logger.info("CommitReporter: Generating exhaustive history summary...")

        with open(self.commit_data, "r") as f:
            commits = json.load(f)

        content = "# WORKSTATION COMMIT ANALYSIS REPORT\n\n"
        content += "## Forensic Traceability of the Canonical Baseline\n\n"

        for c in commits:
            content += f"### Commit {c['hash'][:8]}\n"
            content += f"- **Author**: {c['author']}\n"
            content += f"- **Intent**: {c['inferred_intent']}\n"
            content += f"- **Message**: {c['message']}\n"
            content += f"- **Impact**: {len(c['files'])} files modified. {c['inferred_intent'].replace('_', ' ').title()}.\n\n"

        with open("COMMIT_ANALYSIS_REPORT.md", "w") as f:
            f.write(content)

        logger.info("CommitReporter: COMMIT_ANALYSIS_REPORT.md generated.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reporter = CommitReportGenerator()
    reporter.generate_report()
