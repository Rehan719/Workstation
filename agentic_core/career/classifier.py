from typing import Any, Dict, List

CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "cv_history": [
        "curriculum vitae", " cv ", "resume", "work experience", "professional summary",
        "career history", "employment history", "personal profile",
    ],
    "past_applications": [
        "application form", "previously applied", "submitted application",
        "application reference", "candidate id", "your application",
    ],
    "star_examples": [
        "situation, task, action, result", "star method", "star example",
        "competency example", "situation:", "task:", "action:", "result:",
    ],
    "job_ad": [
        "we are looking for", "job advert", "vacancy", "salary", "job title",
        "apply now", "join our team", "competitive salary", "exciting opportunity",
    ],
    "job_description": [
        "job description", "job purpose", "role purpose", "main duties",
        "duties and responsibilities", "key responsibilities", "responsibilities include",
        "reports to", "principal accountabilities", "job summary",
    ],
    "person_spec": [
        "essential criteria", "desirable criteria", "person specification",
        "qualifications required", "selection criteria",
    ],
    "application_guidance": [
        "how to apply", "application process", "application guidance",
        "closing date", "submission instructions", "applying for this role",
    ],
    "interview_prep_materials": [
        "interview", "assessment centre", "competency based interview",
        "interview panel", "interview questions",
    ],
}

FALLBACK_CATEGORY = "uncategorized"


def classify_content(filename: str, text: str) -> Dict[str, Any]:
    """Heuristic keyword-scored classifier assigning uncategorised uploads to an input category."""
    haystack = f"{filename}\n{text}".lower()
    scores: Dict[str, int] = {}
    matched: Dict[str, List[str]] = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        hits = [kw.strip() for kw in keywords if kw in haystack]
        if hits:
            scores[category] = len(hits)
            matched[category] = hits

    if not scores:
        return {
            "category": FALLBACK_CATEGORY,
            "confidence": 0.0,
            "matched_keywords": [],
            "candidates": {},
        }

    best_category = max(scores, key=lambda c: scores[c])
    total_hits = sum(scores.values())
    confidence = round(scores[best_category] / total_hits, 2) if total_hits else 0.0

    return {
        "category": best_category,
        "confidence": confidence,
        "matched_keywords": matched[best_category],
        "candidates": scores,
    }
