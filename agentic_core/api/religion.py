"""
Religion Domain API — Islamic jurisprudence, interfaith dialogue, and scholarly tools.

  POST /api/v1/religion/fatwa-research   — research a jurisprudential question
  POST /api/v1/religion/quran-tafsir     — AI-assisted Quran exegesis (tafsir)
  POST /api/v1/religion/halal-review     — halal certification pre-assessment
  POST /api/v1/religion/interfaith       — interfaith dialogue and comparison tool
  GET  /api/v1/religion/schools          — list Islamic jurisprudence schools (madhabs)
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text

router = APIRouter(prefix="/api/v1/religion", tags=["religion"])

_MADHABS = [
    {"id": "hanafi", "name": "Hanafi", "region": "South Asia, Turkey, Central Asia", "founder": "Abu Hanifa (699–767 CE)"},
    {"id": "maliki", "name": "Maliki", "region": "North Africa, West Africa, Andalusia", "founder": "Malik ibn Anas (711–795 CE)"},
    {"id": "shafi", "name": "Shafi'i", "region": "East Africa, Southeast Asia, Egypt", "founder": "Muhammad al-Shafi'i (767–820 CE)"},
    {"id": "hanbali", "name": "Hanbali", "region": "Arabian Peninsula", "founder": "Ahmad ibn Hanbal (780–855 CE)"},
    {"id": "jafari", "name": "Ja'fari (Shia)", "region": "Iran, Iraq, Lebanon", "founder": "Ja'far al-Sadiq (702–765 CE)"},
]

_FAITH_TRADITIONS = [
    "Islam", "Christianity", "Judaism", "Hinduism", "Buddhism",
    "Sikhism", "Zoroastrianism", "Baha'i", "Jainism", "Taoism",
]


@router.get("/schools")
async def list_schools():
    """Return the main schools of Islamic jurisprudence."""
    return {
        "madhabs": _MADHABS,
        "faith_traditions": _FAITH_TRADITIONS,
        "total_madhabs": len(_MADHABS),
    }


class FatwaResearchRequest(BaseModel):
    question: str
    madhab: str = "hanafi"  # preferred school of jurisprudence
    context: str = ""  # geographic/circumstantial context
    language: str = "english"


@router.post("/fatwa-research")
async def fatwa_research(req: FatwaResearchRequest):
    """
    AI-assisted jurisprudential research on an Islamic question.
    NOT a fatwa — provides scholarly research for qualified scholars to review.
    """
    madhab_info = next((m for m in _MADHABS if m["id"] == req.madhab), _MADHABS[0])

    prompt = (
        f"You are an Islamic studies scholar with expertise in classical jurisprudence (fiqh). "
        f"Provide scholarly research on the following question from the perspective of the "
        f"{madhab_info['name']} school of jurisprudence.\n\n"
        f"Question: {req.question}\n"
        f"Primary madhab: {madhab_info['name']}\n"
        + (f"Context: {req.context}\n" if req.context else "")
        + "\nStructure your research as:\n"
        "## The Question (Mas'ala)\n"
        "## Primary Sources (Quran and Hadith)\n"
        "## Position of the " + madhab_info['name'] + " School\n"
        "## Positions of Other Schools (brief comparison)\n"
        "## Legal Reasoning (Qiyas/Ijtihad)\n"
        "## Contemporary Considerations\n"
        "## Scholarly Consensus (Ijma) if applicable\n"
        "## Research Summary\n\n"
        "Cite sources precisely (surah:ayah for Quran; narrator, collection, hadith number for Sunnah). "
        "Be academically rigorous. Note areas of scholarly disagreement honestly.\n\n"
        "IMPORTANT: Clearly state this is scholarly research only, not a personal fatwa, "
        "and recommend consulting a qualified mufti for personal rulings."
    )

    research, provenance = await ai_text(prompt, "religion_fiqh")

    return {
        "research_id": uuid.uuid4().hex[:10],
        "question": req.question,
        "madhab": req.madhab,
        "madhab_name": madhab_info["name"],
        "research": research,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
            "This is AI-assisted scholarly research only. It is NOT a fatwa and does not constitute "
            "a religious ruling. Please consult a qualified Islamic scholar or mufti for personal guidance."
        ),
    }


class QuranTafsirRequest(BaseModel):
    surah: int  # 1–114
    ayah_start: int
    ayah_end: int = 0  # 0 = same as start (single ayah)
    tafsir_approach: str = "classical"  # classical | thematic | contemporary | linguistic


@router.post("/quran-tafsir")
async def quran_tafsir(req: QuranTafsirRequest):
    """
    AI-assisted Quranic exegesis (tafsir) for a specified verse range.
    """
    surah = max(1, min(req.surah, 114))
    ayah_start = max(1, req.ayah_start)
    ayah_end = req.ayah_end if req.ayah_end >= ayah_start else ayah_start
    reference = f"Surah {surah}:{ayah_start}" + (f"–{ayah_end}" if ayah_end > ayah_start else "")

    approach_instructions = {
        "classical": "Apply classical tafsir methodology, drawing on Ibn Kathir, Al-Tabari, and Al-Qurtubi.",
        "thematic": "Apply thematic (mawdu'i) tafsir, connecting this passage to related themes across the Quran.",
        "contemporary": "Apply contemporary tafsir, addressing modern context and relevance to today's world.",
        "linguistic": "Apply linguistic analysis: root words (Arabic root letters), grammatical structures, and rhetorical devices.",
    }.get(req.tafsir_approach, "Apply classical tafsir methodology.")

    prompt = (
        f"You are an Islamic scholar and Quranic exegete. "
        f"Provide a scholarly tafsir (exegesis) of {reference}.\n\n"
        f"Approach: {req.tafsir_approach}\n"
        f"{approach_instructions}\n\n"
        "Structure as:\n"
        f"## {reference} — Arabic Text\n"
        "## Transliteration\n"
        "## Translation (provide your own scholarly translation)\n"
        "## Context of Revelation (Asbab al-Nuzul) if applicable\n"
        "## Linguistic Analysis (key Arabic terms, root words)\n"
        "## Exegesis (detailed explanation)\n"
        "## Related Verses (cross-references)\n"
        "## Key Lessons and Guidance\n\n"
        "Be rigorous. Cite classical scholars where relevant. "
        "Acknowledge differing scholarly interpretations where they exist."
    )

    tafsir, provenance = await ai_text(prompt, "religion_tafsir")

    return {
        "tafsir_id": uuid.uuid4().hex[:10],
        "reference": reference,
        "surah": surah,
        "ayah_start": ayah_start,
        "ayah_end": ayah_end,
        "approach": req.tafsir_approach,
        "tafsir": tafsir,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class HalalReviewRequest(BaseModel):
    product_name: str
    product_description: str
    ingredients: list[str] = []
    manufacturing_process: str = ""
    target_markets: list[str] = []


@router.post("/halal-review")
async def halal_pre_assessment(req: HalalReviewRequest):
    """
    AI-assisted halal certification pre-assessment.
    Identifies potential compliance issues before formal certification.
    """
    ingredients_text = "\n".join(f"  - {i}" for i in req.ingredients) if req.ingredients else "Not specified"
    markets_text = ", ".join(req.target_markets) if req.target_markets else "Not specified"

    prompt = (
        f"You are a halal certification consultant with expertise in Islamic dietary law (fiqh al-at'ima) "
        f"and international halal standards (ESMA UAE.S/GSO 2055, JAKIM Malaysia, HFA UK).\n\n"
        f"Product: {req.product_name}\n"
        f"Description: {req.product_description}\n"
        f"Ingredients:\n{ingredients_text}\n"
        + (f"Manufacturing process: {req.manufacturing_process}\n" if req.manufacturing_process else "")
        + f"Target markets: {markets_text}\n\n"
        "Conduct a pre-assessment and provide:\n"
        "## Halal Status Assessment (COMPLIANT / REQUIRES REVIEW / NON-COMPLIANT)\n"
        "## Critical Issues (ingredients or processes requiring resolution)\n"
        "## Flagged Ingredients (E-numbers, derivatives, ambiguous items to verify)\n"
        "## Cross-Contamination Risks\n"
        "## Manufacturing Considerations\n"
        "## Recommended Certifying Bodies (by target market)\n"
        "## Steps to Achieve Certification\n"
        "## Market-Specific Requirements\n\n"
        "Be specific about which standards apply. Flag anything ambiguous — err on the side of caution.\n"
        "Note: This is a pre-assessment tool only; formal certification requires an accredited certifying body."
    )

    assessment, provenance = await ai_text(prompt, "religion_halal")

    return {
        "assessment_id": uuid.uuid4().hex[:10],
        "product_name": req.product_name,
        "target_markets": req.target_markets,
        "assessment": assessment,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
            "This is an AI pre-assessment tool only. Official halal certification must be obtained "
            "from an accredited halal certifying body. This assessment does not constitute certification."
        ),
    }


class InterfaithRequest(BaseModel):
    topic: str
    traditions: list[str] = ["Islam", "Christianity", "Judaism"]
    dialogue_purpose: str = "understanding"  # understanding | commonalities | differences | dialogue


@router.post("/interfaith")
async def interfaith_dialogue(req: InterfaithRequest):
    """
    Generate an interfaith comparative analysis and dialogue resource.
    """
    traditions = req.traditions[:5] if req.traditions else ["Islam", "Christianity", "Judaism"]
    traditions_text = ", ".join(traditions)

    purpose_map = {
        "understanding": "to deepen mutual understanding of each tradition's perspective",
        "commonalities": "to identify shared values and common ground between traditions",
        "differences": "to map genuine theological differences with respect and accuracy",
        "dialogue": "to prepare materials for an interfaith dialogue or educational event",
    }
    purpose_text = purpose_map.get(req.dialogue_purpose, purpose_map["understanding"])

    prompt = (
        f"You are a scholar of comparative religion and interfaith dialogue. "
        f"Create a respectful, academically rigorous comparative analysis of the following topic "
        f"across {len(traditions)} faith traditions, {purpose_text}.\n\n"
        f"Topic: {req.topic}\n"
        f"Traditions: {traditions_text}\n\n"
        "Structure as:\n"
        "## Overview\n"
        + "\n".join(f"## {t}'s Perspective on {req.topic}" for t in traditions)
        + "\n## Points of Convergence\n"
        "## Points of Divergence\n"
        "## Dialogue Questions (5 open questions for respectful discussion)\n"
        "## Suggested Resources for Further Study\n\n"
        "Approach with equal respect for all traditions. "
        "Cite authoritative sources from each tradition. "
        "Avoid stereotypes and represent the mainstream scholarly position of each tradition, "
        "noting internal diversity where significant."
    )

    analysis, provenance = await ai_text(prompt, "religion_interfaith")

    return {
        "analysis_id": uuid.uuid4().hex[:10],
        "topic": req.topic,
        "traditions": traditions,
        "dialogue_purpose": req.dialogue_purpose,
        "analysis": analysis,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
