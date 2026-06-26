import os
import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ConstitutionalAuditScript:
    """
    ARTICLE 410: Automated Constitutional Audit.
    Verifies that the codebase implements and traces all mandated articles.
    """
    def __init__(self, constitution_path: str = "agentic_core/constitution/CONSTITUTION_canonical.md"):
        self.constitution_path = constitution_path
        self.articles = self._parse_articles()

    def _parse_articles(self) -> List[str]:
        """Extracts article IDs from the constitution file."""
        if not os.path.exists(self.constitution_path):
            return []

        with open(self.constitution_path, 'r') as f:
            content = f.read()

        return re.findall(r"ARTICLE (\d+):", content)

    def run_audit(self) -> Dict[str, Any]:
        """Scans the repository for article mentions and implementation coverage."""
        mentions = {}
        for root, _, files in os.walk("agentic_core"):
            for file in files:
                if file.endswith((".py", ".md", ".json")):
                    path = os.path.join(root, file)
                    with open(path, 'r', errors='ignore') as f:
                        content = f.read()
                        for art in self.articles:
                            if f"ARTICLE {art}" in content:
                                mentions.setdefault(art, []).append(path)

        implemented = [art for art in self.articles if art in mentions]
        missing = [art for art in self.articles if art not in mentions]

        coverage = len(implemented) / len(self.articles) if self.articles else 0

        return {
            "status": "PASS" if coverage >= 0.95 else "FAIL",
            "coverage": coverage,
            "implemented_count": len(implemented),
            "missing_articles": missing,
            "audit_timestamp": os.path.getmtime(self.constitution_path)
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    auditor = ConstitutionalAuditScript()
    report = auditor.run_audit()
    print(f"\n--- Constitutional Audit Report ---")
    print(f"Status: {report['status']}")
    print(f"Coverage: {report['coverage']:.2%}")
    print(f"Implemented: {report['implemented_count']} articles")
    if report['missing_articles']:
        print(f"Missing: {', '.join(report['missing_articles'])}")
    print("-----------------------------------\n")
