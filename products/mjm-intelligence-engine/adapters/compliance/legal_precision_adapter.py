from typing import List, Dict, Any, Optional

class LegalPrecisionAdapter:
    """
    Ensures intelligence outputs align with UK legal standards.
    Provides templates for Employment Tribunal submissions.
    """

    STATUTES = {
        "equality_act": "Equality Act 2010",
        "employment_rights": "Employment Rights Act 1996",
        "acas_code": "ACAS Code of Practice on Disciplinary and Grievance Procedures"
    }

    def get_et1_guidance(self) -> str:
        return """
# ET1 Claim Form Guidance (UK Employment Tribunal)
- **Section 8.1:** Check the boxes for the type of claim (e.g., Unfair Dismissal, Discrimination).
- **Section 8.2:** Provide the 'Grounds of Complaint'. Use the MJM Jaiza analysis for facts.
- **Statement of Truth:** Ensure all dates match the Mushahida chronology.
"""

    def generate_witness_statement_template(self, chronology: List[Dict[str, Any]]) -> str:
        statement = "IN THE EMPLOYMENT TRIBUNAL\nCASE NO: [XXX]\n\nBETWEEN:\n[Claimant Name] -and- [Respondent Name]\n\n"
        statement += "WITNESS STATEMENT OF [Name]\n\nI, [Name], of [Address], WILL SAY AS FOLLOWS:\n\n"

        for i, entry in enumerate(chronology, 1):
            statement += f"{i}. On {entry.get('date')}, {entry.get('event')}\n"

        statement += "\nSTATEMENT OF TRUTH\nI believe that the facts stated in this witness statement are true."
        return statement

    def get_regulatory_citation(self, key: str) -> str:
        return self.STATUTES.get(key, "Unknown Statute")
