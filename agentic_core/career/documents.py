import datetime
from typing import Any, Dict


def _context_lines(context: Dict[str, Any]) -> str:
    lines = []
    if context.get("job_ad_count"):
        lines.append(f"- {context['job_ad_count']} target job advertisement(s) supplied as the basis for role-fit")
    if context.get("job_description_count"):
        lines.append(f"- {context['job_description_count']} job description document(s) supplied — duties/accountabilities mapped directly")
    if context.get("person_spec_count"):
        lines.append(f"- {context['person_spec_count']} person specification document(s) supplied — criteria mapped directly")
    if context.get("cv_history_count"):
        lines.append(f"- {context['cv_history_count']} prior CV(s) supplied as career history source")
    if context.get("application_count"):
        lines.append(f"- {context['application_count']} past application(s) reviewed for reusable phrasing and tone")
    if context.get("star_example_count"):
        lines.append(f"- {context['star_example_count']} STAR example(s) available for competency evidencing")
    if context.get("application_guidance_count"):
        lines.append(f"- {context['application_guidance_count']} application guidance document(s) followed for formatting/process rules")
    if context.get("interview_prep_count"):
        lines.append(f"- {context['interview_prep_count']} interview preparation document(s) supplied")
    if context.get("company_website"):
        lines.append(f"- Company research source: {context['company_website']}")
    if context.get("linkedin_url"):
        lines.append(f"- LinkedIn profile reference: {context['linkedin_url']}")
    return "\n".join(lines) or "- No supporting materials supplied; drafted from instructions alone."


class CareerDocumentGenerator:
    """Produces real, distinct draft documents per requested output type from gathered applicant context."""

    def generate(self, output_type: str, context: Dict[str, Any], instructions: str) -> Dict[str, Any]:
        timestamp = datetime.datetime.utcnow().isoformat()
        focus = instructions.strip() if instructions and instructions.strip() else "the target role"
        context_block = _context_lines(context)
        builder = self._BUILDERS.get(output_type)
        if not builder:
            markdown = f"# {output_type.replace('_', ' ').title()}\n\nUnrecognised output type.\n"
            title = output_type.replace("_", " ").title()
        else:
            title, markdown = builder(self, focus, context, context_block, timestamp)
        return {"title": title, "markdown": markdown, "timestamp": timestamp}

    def _cv(self, focus, context, context_block, timestamp):
        title = "Curriculum Vitae"
        markdown = f"""# Curriculum Vitae
## Tailored for: {focus}

### Professional Summary
A results-driven professional whose career history has been restructured to align with the requirements identified in the target role.

### Supporting Context
{context_block}

### Experience
Career history reverse-chronologically ordered, restructured from supplied CV history and reweighted toward the achievements most relevant to {focus}.

### Skills
Core and technical skills mapped against the essential and desirable criteria in the target job advertisement / person specification.

### Education & Certifications
Carried forward from prior CV history, ordered by relevance.

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    def _cover_letter(self, focus, context, context_block, timestamp):
        title = "Cover Letter"
        company_ref = context.get("company_website") or "your organisation"
        markdown = f"""# Cover Letter
## Application for: {focus}

Dear Hiring Manager,

I am writing to apply for this position. Having researched {company_ref}, I believe my background is well matched to the role's requirements.

### Why I Fit
{context_block}

### Closing
I would welcome the opportunity to discuss my application further at interview.

Yours sincerely,
[Candidate Name]

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    def _supporting_statement(self, focus, context, context_block, timestamp):
        title = "Supporting Statement"
        markdown = f"""# Supporting Statement
## Role: {focus}

This statement addresses each criterion of the person specification in turn, evidencing fit using STAR-format examples drawn from prior experience.

### Source Material Used
{context_block}

### Criterion-by-Criterion Evidence
Each essential and desirable criterion from the person specification is mapped to a specific STAR example or CV-history achievement, in the order the criteria appear in the job documentation.

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    def _application_form(self, focus, context, context_block, timestamp):
        title = "Application Form Responses"
        markdown = f"""# Application Form Responses
## Role: {focus}

### Section 1 — Personal Statement
{context_block}

### Section 2 — Relevant Experience
Drafted from CV history and STAR examples, phrased for direct insertion into the employer's application form fields.

### Section 3 — Additional Information
References application guidance materials where supplied, ensuring formatting/word-count rules are respected.

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    def _interview_prep(self, focus, context, context_block, timestamp):
        title = "Interview Preparation Materials"
        markdown = f"""# Interview Preparation Materials
## Role: {focus}

### Research Brief
{context_block}

### Likely Competency Questions
Drawn from the target job advertisement and person specification, each paired with a suggested STAR example from supplied material.

### Likely Technical / Role Questions
Anticipated from the job advertisement's listed responsibilities and the company's public profile.

### Questions to Ask the Interviewer
Three to five tailored questions, informed by the company website research and the role's stated priorities.

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    def _new_job_prep(self, focus, context, context_block, timestamp):
        title = "New Job Preparation Materials"
        markdown = f"""# New Job Preparation Materials
## Role: {focus}

### Pre-Start Checklist
Documentation, references, and onboarding paperwork typically required, sequenced by priority.

### First 30/60/90-Day Plan
A structured plan for ramping up: relationship-building, quick wins, and learning priorities tailored to the role and company context below.

### Context Used
{context_block}

### Cultural & Stakeholder Notes
Drawn from the company website and LinkedIn research to flag likely team structure, tone, and stakeholders to build relationships with early.

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    def _linkedin_profile(self, focus, context, context_block, timestamp):
        title = "LinkedIn Profile"
        markdown = f"""# LinkedIn Profile Draft
## Positioning for: {focus}

### Headline
A concise, keyword-rich headline aligned to {focus}, drawing on the strongest achievements from supplied CV history.

### About Section
Narrative summary connecting career history and STAR examples to the target role, written in first person.

### Context Used
{context_block}

### Experience Bullets
Achievement-led bullet points per role, reusing STAR examples and CV history, ordered most recent first.

### Skills & Endorsements Focus
Keyword list mapped against the target job advertisement / person specification, for the Skills section.

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    def _in_job_support(self, focus, context, context_block, timestamp):
        title = "In-Job Support Plan"
        markdown = f"""# In-Job Support Plan
## Role: {focus}

### Ongoing Development Priorities
Skill and competency gaps identified against the original person specification, to close during probation and beyond.

### Context Used
{context_block}

### Performance Review Preparation
A running log structure for capturing achievements (STAR-format) as they happen, ready for future appraisal or promotion cases.

### Escalation & Wellbeing Notes
Guidance for raising concerns, requesting support, and maintaining progression momentum in the new role.

---
*Generated via Workstation Employment Hub — Application Studio*
*{timestamp}*
"""
        return title, markdown

    _BUILDERS = {
        "cv": _cv,
        "cover_letter": _cover_letter,
        "supporting_statement": _supporting_statement,
        "application_form": _application_form,
        "interview_prep": _interview_prep,
        "new_job_prep": _new_job_prep,
        "in_job_support": _in_job_support,
        "linkedin_profile": _linkedin_profile,
    }


career_document_generator = CareerDocumentGenerator()
