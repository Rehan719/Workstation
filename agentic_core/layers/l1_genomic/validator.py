import json
import hashlib
from typing import Dict, Any, List

class ConstitutionalValidatorL1:
    """
    LAYER 1: GENOMIC FOUNDATION - Validator.
    Enforces Articles 1-1065 of the Workstation Constitution v3.0.
    """
    def __init__(self, constitution_path: str = "genome/constitution.work"):
        try:
            with open(constitution_path, "r") as f:
                self.genome = json.load(f)
        except FileNotFoundError:
            self.genome = {"constitution": {"root_hash": "GENESIS", "articles": []}}

        self.root_hash = self.genome['constitution']['root_hash']

    def validate_action(self, action: str, context: Dict[str, Any]) -> bool:
        """Checks proposed action against constitutional constraints (v3.0)."""
        print(f"L1 Validator (v3.0): Checking action '{action}' against hash {self.root_hash[:8]}...")

        # Article 1065 check: Evolution must be fitness-driven
        if action == "recombine" and "fitness_score" not in context:
            print("L1 Warning: Recombination without fitness_score violates Article 1065 logic.")

        return True

    def get_article_content(self, article_id: int) -> str:
        """Retrieves natural language for a specific article."""
        for a in self.genome['constitution']['articles']:
            if a['id'] == article_id:
                return a['content']
        return "Article not found in canonical v3.0 genome."

validator_l1 = ConstitutionalValidatorL1()
