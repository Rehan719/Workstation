from typing import Dict, Any, List
import random

class PubMedAdapter:
    """Mock PubMed Adapter with realistic fixture data from Appendix K."""
    def search_literature(self, query: str) -> List[Dict[str, Any]]:
        return [
            {
                "pmid": "39542107",
                "title": "AAV2/9 mediates robust and widespread transduction of murine testicular germ cells",
                "author": "Wu et al.",
                "date": "Nov 2025",
                "findings": "Robust germ cell transduction; premier vector for germ-cell directed therapy.",
                "truth_dimension": "Truth I: Objective Record"
            },
            {
                "pmid": "39811005",
                "title": "Longitudinal Proteomic Study of mRNA Vaccine-Induced Autoimmunity",
                "author": "Chazarin et al.",
                "date": "Jan 2026",
                "findings": "214/342 proteins altered at 16-24 weeks; complement activation; modest IL-1B autoantibody increases.",
                "truth_dimension": "Truth I: Objective Record"
            }
        ]

class FDAAdapter:
    """Mock FDA Adapter for regulatory guidance and panel reasoning."""
    def fetch_guidance(self, search_term: str) -> List[Dict[str, Any]]:
        return [
            {
                "guidance_id": "FDA-2023-D-LTFU",
                "title": "Long-Term Follow-Up After Administration of Human Gene Therapy Products",
                "date": "2023",
                "relevance": "High: 10-15 years monitoring required for integrating vectors.",
                "truth_dimension": "Truth III: Procedural Compliance"
            }
        ]

class EMAAdapter:
    """Mock EMA Adapter for PRAC and CAT interface."""
    def fetch_prac_updates(self) -> List[Dict[str, Any]]:
        return [
            {
                "topic": "PRAC Oversight of ATMPs",
                "date": "Sept 2025",
                "details": "Regular assessment of safety signals, RMPs, PASS for CAR-T and other ATMPs.",
                "truth_dimension": "Truth III: Procedural Compliance"
            }
        ]
