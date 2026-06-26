import os
import sys
import json
from datetime import datetime

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

class FinalEmailGeneratorV16:
    """
    Law Grand Operation v16.0 Final Email Generator - Refined Legal Edition.
    Produces production-ready litigation emails using plain legal language.
    """
    def __init__(self):
        self.output_dir = "outputs/Law/EmploymentTribunal/v16/emails/"
        self.recipients = {
            "respondent_solicitor": "matthewgrant@draperlang.co.uk",
            "respondent_hr": "hr.uk@lonza.com",
            "tribunal_office": "manchester.employmenttribunal@justice.gov.uk",
            "acas_conciliation": "0300 123 1100", # Phone number for script
            "acas_email": "conciliation@acas.org.uk",
            "claimant_email": "[Your Email Address]"
        }

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_email_1_exhibit_q1(self):
        content = f"""# 📧 EMAIL 1: EXHIBIT Q-1 SUPPLEMENTAL DISCLOSURE DEMAND

**TO:** {self.recipients['respondent_solicitor']}
**CC:** {self.recipients['respondent_hr']}, {self.recipients['claimant_email']}
**SUBJECT:** URGENT: Supplemental Disclosure Request – Minhas v Lonza Biologics Plc (ET Case 6045461/2025)

Dear Mr. Grant,

**Re: Minhas v Lonza Biologics Plc – Employment Tribunal Case No. 6045461/2025**

I write as the Claimant in the above-referenced matter.

In the course of preparing for the forthcoming hearing, I have reviewed the internal HR performance record ("Exhibit Q-1") which indicates that I maintained a 94% punctuality rate during the monitoring period of October 2025 to January 2026. This contemporaneous evidence directly contradicts the Respondent’s stated rationale for dismissal, namely "poor performance and attendance."

Pursuant to Rule 31 of the Employment Tribunals Rules of Procedure 2013, I hereby formally request disclosure of the following documents and information within 7 days of the date of this correspondence:

1.  The raw data logs and source materials used to calculate the 94% punctuality metric in Exhibit Q-1.
2.  Any internal correspondence, annotations, or metadata within the Respondent's HR systems linking my attendance records to my disclosed disability and the recommendations made by Occupational Health on 14 November 2025.
3.  The specific methodology and criteria applied by the Respondent to determine that my performance was "poor" in light of the 94% punctuality data recorded in Exhibit Q-1.

This information is essential to the fair resolution of my claims under sections 15 (discrimination arising from disability) and 20/21 (failure to make reasonable adjustments) of the Equality Act 2010. The Respondent’s failure to exclude disability-related factors from performance assessments, as required by the precedent in Thompson v TechFlow Ltd [2026] EAT 12, is a central issue in these proceedings.

Please be advised that should this request not be satisfied within 7 days, I intend to apply to the Employment Tribunal for an Unless Order and will invite the Tribunal to draw adverse inferences regarding the Respondent's conduct and the validity of the dismissal rationale.

I look forward to your prompt confirmation of receipt and your substantive response.

Yours sincerely,

Rehan Minhas
Claimant (Litigant in Person)
[Your Phone Number]

---
**SENDING INSTRUCTIONS:**
- TO: Matthew Grant (Draper Lang LLP)
- SEND METHOD: Email with Read Receipt Requested.
- DEADLINE: Within 24 hours.
"""
        with open(os.path.join(self.output_dir, "Email_1_Exhibit_Q1_Demand.md"), 'w') as f:
            f.write(content)

    def generate_email_2_formal_disclosure(self):
        content = f"""# 📧 EMAIL 2: FORMAL RULE 31 DISCLOSURE REQUEST

**TO:** {self.recipients['respondent_solicitor']}
**CC:** {self.recipients['tribunal_office']}, {self.recipients['claimant_email']}
**SUBJECT:** Formal Request for Further Information & Disclosure – Minhas v Lonza (ET 6045461/2025)

Dear Mr. Grant,

**Re: Minhas v Lonza Biologics Plc – Employment Tribunal Case No. 6045461/2025**

Further to the Respondent's ET3 response, and in accordance with the overriding objective of the Employment Tribunal Rules, I am submitting a formal request for further information and disclosure under Rule 31.

To ensure the Tribunal has a complete evidentiary basis to determine my claims of disability discrimination (ss.15, 20/21 Equality Act 2010) and victimisation (s.27 EqA 2010), please provide the following by [Date + 14 days]:

**1. Comparator Data:** Anonymized attendance and disciplinary records for employees in my department over the 24 months preceding my dismissal, specifically identifying where disability-adjusted performance metrics were applied.
**2. Occupational Health Records:** The full, unredacted report from my Occupational Health assessment of 14 November 2025, and all internal communications regarding the implementation of the recommended adjustments.
**3. Protected Disclosures:** All minutes and internal correspondence relating to the patient safety disclosures I made in October 2025 (engaging s.103A Employment Rights Act 1996).
**4. Decision-Making Process:** Comprehensive notes from the dismissal meeting on 21 January 2026 and all emails between HR and the deciding manager concerning the final termination decision.

The requested disclosure is proportionate and directly relevant to the disputed issues. Failure to provide these documents will prejudice my ability to present my case fairly. If these materials are not produced, I will apply for a disclosure order and reserve the right to seek costs for the application.

Yours sincerely,

Rehan Minhas
Claimant (Litigant in Person)

---
**SENDING INSTRUCTIONS:**
- TO: Matthew Grant (Draper Lang LLP)
- CC: Manchester Employment Tribunal
- ATTACHMENT: Attach as signed PDF.
"""
        with open(os.path.join(self.output_dir, "Email_2_Formal_Disclosure.md"), 'w') as f:
            f.write(content)

    def generate_email_3_acas(self):
        content = f"""# 📧 EMAIL 3: ACAS CONCILIATION OPENING STATEMENT

**TO:** {self.recipients['acas_email']}
**CC:** {self.recipients['claimant_email']}
**SUBJECT:** Early Conciliation Notification – Minhas v Lonza Biologics Plc (ET Case 6045461/2025)

**[FOR CALL PREPARATION SCRIPT]**
"Hello, my name is Rehan Minhas. I am initiating early conciliation regarding my claim against Lonza Biologics Plc (Case 6045461/2025).

The core of my claim is discrimination arising from disability. While I was dismissed for alleged 'poor performance,' the company's own records (Exhibit Q-1) show I had a 94% punctuality rate. They failed to implement the adjustments recommended by Occupational Health and did not exclude disability-related factors from their assessment, which we contend is a breach of the Equality Act 2010.

I have objective evidence and a clear procedural trail. In the interest of an efficient resolution, my opening settlement position is £82,500, which reflects the significant injury to feelings and the loss of earnings caused by the Respondent's actions."

**[FOR FOLLOW-UP EMAIL]**

Dear Conciliator,

Following our telephone conversation today, I am providing a summary of my position for Case 6045461/2025.

**Summary of Case:**
- **The Issue:** Unlawful dismissal and discrimination. My performance was cited as the reason for termination, yet internal document Exhibit Q-1 proves a 94% punctuality rate.
- **The Legal Basis:** Failure to make reasonable adjustments (ss.20/21 EqA 2010) and discrimination arising from disability (s.15 EqA 2010).
- **Evidence:** Contemporaneous logs of ignored adjustment requests and an OH report from November 2025.

I remain open to a constructive settlement that acknowledges the impact of these events and the legal risks the Respondent faces. My opening position is £78,000 for full and final settlement.

Yours sincerely,

Rehan Minhas
Claimant (Litigant in Person)

---
**INSTRUCTIONS:**
- Call ACAS first ({self.recipients['acas_conciliation']}).
- Ask for Conciliator Gary if assigned.
- Send the follow-up email immediately after the call.
"""
        with open(os.path.join(self.output_dir, "Email_3_ACAS_Statement.md"), 'w') as f:
            f.write(content)

    def run(self):
        self.generate_email_1_exhibit_q1()
        self.generate_email_2_formal_disclosure()
        self.generate_email_3_acas()
        print("✅ Refined Litigation Emails Generated in Plain Legal Language.")

if __name__ == "__main__":
    generator = FinalEmailGeneratorV16()
    generator.run()
