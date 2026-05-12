from typing import List, Dict, Any, Optional

class LegalPrecisionAdapter:
    """
    Ensures intelligence outputs align with UK legal standards.
    Provides templates for Employment Tribunal submissions.
    """

    STATUTES = {
        "equality_act": "Equality Act 2010",
        "employment_rights": "Employment Rights Act 1996",
        "acas_code": "ACAS Code of Practice on Disciplinary and Grievance Procedures",
        "whistleblowing": "Public Interest Disclosure Act 1998 (PIDA)"
    }

    def get_et1_guidance(self, claim_type: str = "disability_discrimination") -> str:
        base_guidance = """
# ET1 Claim Form Guidance (UK Employment Tribunal)
- **Section 8.1:** Check the boxes for the type of claim.
- **Section 8.2:** Provide the 'Grounds of Complaint'. Use the MJM Jaiza analysis for facts.
- **Statement of Truth:** Ensure all dates match the Mushahida chronology.
"""
        if claim_type == "disability_discrimination":
            return base_guidance + """
- **Disability Specialization:** Cite 'Section 15' (Discrimination arising from disability) or 'Section 20' (Duty to make adjustments) of the Equality Act 2010.
- **Evidence:** Focus on the 'Mushahida' findings regarding the failure to implement specific medical recommendations.
"""
        elif claim_type == "whistleblowing":
            return base_guidance + """
- **Whistleblowing Specialization:** Cite 'Section 43B' of the Employment Rights Act 1996.
- **Protected Disclosure:** Clearly identify the 'Mushahida' evidence item that constitutes the disclosure and show it was in the public interest.
"""
        return base_guidance

    def generate_witness_statement_template(self, chronology: List[Dict[str, Any]]) -> str:
        statement = "IN THE EMPLOYMENT TRIBUNAL\nCASE NO: [CASENO]\n\nBETWEEN:\n[Claimant Name] -and- [Respondent Name]\n\n"
        statement += "WITNESS STATEMENT OF [Name]\n\nI, [Name], of [Address], WILL SAY AS FOLLOWS:\n\n"

        for i, entry in enumerate(chronology, 1):
            statement += f"{i}. On {entry.get('date')}, {entry.get('event')}\n"

        statement += "\nSTATEMENT OF TRUTH\nI believe that the facts stated in this witness statement are true."
        return statement

    def get_regulatory_citation(self, key: str) -> str:
        return self.STATUTES.get(key, "Unknown Statute")
