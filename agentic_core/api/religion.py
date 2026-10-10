"""
Religion Domain API — Islamic jurisprudence, interfaith dialogue, and scholarly tools.

  POST /api/v1/religion/fatwa-research   — research a jurisprudential question
  POST /api/v1/religion/hadith-study     — hadith sciences research (narration, grading, sharh)
  POST /api/v1/religion/quran-tafsir     — AI-assisted Quran exegesis (tafsir)
  POST /api/v1/religion/halal-review     — halal certification pre-assessment
  POST /api/v1/religion/interfaith       — interfaith dialogue and comparison tool
  GET  /api/v1/religion/schools          — list Islamic jurisprudence schools (madhabs)
"""
from __future__ import annotations

import re
import time
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

import functools

from agentic_core.api._ai_provenance import ai_text as _ai_text, person_said, disclaimer_for

#  W637 (FU-597) — this router's domain, bound once. Every ai_text call below carries it, so the native floor
#  prints the real domain instead of "the request named no domain".
ai_text = functools.partial(_ai_text, domain="religion")

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
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


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

    research, provenance = await ai_text(prompt, "religion_fiqh", realm=req.realm,
        user_text=person_said(req.question))

    # §15 (W498, FU-185, class C6) — THE TAFSIR PATTERN, APPLIED HERE. On the deterministic floor these
    # headings came back filled with keyword bigrams and a "service frame", and the response carried no
    # floor_note and no sections_withheld: a reader saw "## Position of the Hanafi School" and "## Primary
    # Sources (Quran and Hadith)" over text that researched nothing, under a disclaimer that called it
    # "AI-assisted scholarly research". The floor composes headings, not madhab positions, so the
    # scholarly sections are withheld and named, and the disclaimer says what actually served it.
    _floor = (provenance or {}).get("served_by") == "native"
    sections_withheld: list[str] = []
    floor_note = None
    if _floor:
        research, sections_withheld = _withhold_sections(research, (
            "Primary Sources (Quran and Hadith)", "Primary Sources",
            "Position of the " + madhab_info["name"] + " School",
            "Positions of Other Schools (brief comparison)", "Positions of Other Schools",
            "Legal Reasoning (Qiyas/Ijtihad)", "Legal Reasoning",
            "Scholarly Consensus (Ijma) if applicable", "Scholarly Consensus",
            # bare forms the floor shortens to
            "Primary", "Position", "Positions", "Legal", "Consensus",
            # a summary of nothing researched, and "considerations" nothing considered, are the same
            # claim as the sections above - only the restated question survives the floor
            "Contemporary Considerations", "Contemporary", "Research Summary", "Research"))
        floor_note = (
            "served by the deterministic native floor — NO jurisprudential research happened. The floor "
            "composes the headings it is asked for from the words of the request; it does not read a "
            "madhab's position, locate a primary source, or reason by qiyas. Those sections are withheld "
            "rather than shown as a frame: a citation or a school's position that nothing looked up is "
            "worse than silence. Take this question to a qualified scholar or mufti.")

    return {
        "research_id": uuid.uuid4().hex[:10],
        "question": req.question,
        "madhab": req.madhab,
        "madhab_name": madhab_info["name"],
        "research": research,
        "sections_withheld": sections_withheld,
        **({"floor_note": floor_note} if floor_note else {}),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
            ("NO RESEARCH WAS PERFORMED — the deterministic floor served this, so what remains is a "
             "structured frame over your own question, not scholarship. It is NOT a fatwa and NOT a "
             "ruling. Consult a qualified Islamic scholar or mufti." if _floor else
             "This is AI-assisted scholarly research only. It is NOT a fatwa and does not constitute "
             "a religious ruling. Please consult a qualified Islamic scholar or mufti for personal "
             "guidance.")
        ),
    }


class HadithStudyRequest(BaseModel):
    hadith: str                       # the hadith text, or a reference
    focus: str = "authentication"     # authentication | explanation | thematic
    madhab: str = ""                  # optional jurisprudential lens
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/hadith-study")
async def hadith_study(req: HadithStudyRequest):
    """AI-assisted hadith study (ulum al-hadith): identify the narration, discuss its grading/authenticity
    and isnad considerations, where it appears, and its meaning/application. Scholarly research ONLY — never a
    ruling; fabricating a grade or attribution is a serious error, so uncertainty is stated honestly and
    everything must be verified against authenticated collections and qualified scholars."""
    prompt = (
        "You are a scholar of hadith sciences (ulum al-hadith). Research the following hadith rigorously.\n\n"
        f"Hadith (text or reference): {req.hadith}\nFocus: {req.focus}\n"
        + (f"Jurisprudential lens: {req.madhab}\n" if req.madhab else "")
        + "\nStructure your research as:\n"
        "## Identification (the likely narration; the collection(s) and hadith number(s) where it appears, if recognisable)\n"
        "## Text (Matn) — the Arabic if known, plus an English translation\n"
        "## Chain (Isnad) Considerations (narrators and any well-known points about the chain)\n"
        "## Grading (authenticity grade — sahih / hasan / da'if / mawdu' — per recognised scholars, naming who graded it)\n"
        "## Explanation (Sharh) — the meaning and context\n"
        "## Application & Rulings Derived (how scholars have understood and applied it)\n"
        "## Related Narrations\n\n"
        "Cite collections precisely (e.g. Sahih al-Bukhari with hadith number; Sahih Muslim; the four Sunan). "
        "Where you are UNSURE of the exact grading or attribution, say so EXPLICITLY rather than guessing — "
        "fabricating a hadith grade or attribution is a serious error. Recommend verifying against authenticated "
        "collections and a qualified scholar."
    )

    research, provenance = await ai_text(prompt, "religion_hadith", realm=req.realm,
        user_text=person_said(req.focus))

    # §15 (W498, FU-185, class C6) — the same pattern, and here it matters most. The prompt itself says
    # "fabricating a hadith grade or attribution is a serious error", and on the floor the response came
    # back with "## Grading", "## Chain (Isnad) Considerations" and "## Text (Matn)" over keyword bigrams
    # and a service frame — with no floor_note to say so. A grade, an isnad or a matn that nothing looked
    # up must not be rendered under those headings at all.
    _floor = (provenance or {}).get("served_by") == "native"
    sections_withheld: list[str] = []
    floor_note = None
    if _floor:
        research, sections_withheld = _withhold_sections(research, (
            "Identification (the likely narration; the collection(s) and hadith number(s) where it appears, if recognisable)",
            "Identification",
            "Text (Matn) — the Arabic if known, plus an English translation", "Text (Matn)",
            # the floor emits SHORTENED headings ("## Chain"), so the bare form is listed too: a
            # withhold list that only knows the long form leaves the section standing (measured W498)
            "Chain (Isnad) Considerations", "Chain (Isnad)", "Chain",
            "Grading (authenticity grade — sahih / hasan / da'if / mawdu' — per recognised scholars, naming who graded it)",
            "Grading",
            "Explanation (Sharh) — the meaning and context", "Explanation (Sharh)",
            "Application & Rulings Derived (how scholars have understood and applied it)",
            "Application & Rulings Derived", "Related Narrations"))
        floor_note = (
            "served by the deterministic native floor — NOTHING WAS RESEARCHED, GRADED OR ATTRIBUTED. The "
            "floor composes the headings it is asked for from the words of the request; it does not "
            "identify a narration, read an isnad, grade authenticity or reproduce a matn. Every one of "
            "those sections is withheld: a grade or an attribution nothing verified is the error this "
            "tool's own prompt calls serious. Verify any hadith against an authenticated collection and "
            "a qualified scholar.")

    return {
        "study_id": uuid.uuid4().hex[:10],
        "focus": req.focus,
        "study": research,
        "sections_withheld": sections_withheld,
        **({"floor_note": floor_note} if floor_note else {}),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
            ("NOTHING WAS GRADED OR ATTRIBUTED — the deterministic floor served this, so no narration was "
             "identified and no authenticity grade was determined. What remains is a structured frame "
             "over your own text. Verify any hadith against an authenticated collection (Bukhari, Muslim, "
             "the four Sunan) and a qualified scholar." if _floor else
             "AI-assisted scholarly research only — NOT a ruling and NOT a substitute for authenticated "
             "hadith collections. Hadith grading and attribution must be verified with qualified "
             "scholars; treat any grade stated here as provisional until confirmed against a recognised "
             "source.")
        ),
    }


class QuranTafsirRequest(BaseModel):
    surah: int  # 1–114
    ayah_start: int
    ayah_end: int = 0  # 0 = same as start (single ayah)
    tafsir_approach: str = "classical"  # classical | thematic | contemporary | linguistic
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/quran-tafsir")
async def quran_tafsir(req: QuranTafsirRequest):
    """
    AI-assisted Quranic exegesis (tafsir) for a specified verse range.
    """
    # W625 (FU-513, M2 v9 R1.1) — A REFERENCE THAT DOES NOT EXIST IS REFUSED, NEVER REPLACED. This clamped: surah 200
    # served An-Nas, surah 0 Al-Fatiha, ayah -5 ayah 1, and nothing told the reader their request was swapped. §11
    # rule 2 refuses nonexistent ayaat, and every other sacred-text route here (/qep/ayah, hifz) already refuses.
    from fastapi import HTTPException as _HE625
    if not 1 <= int(req.surah) <= 114:
        raise _HE625(status_code=422, detail=f"surah {req.surah} does not exist - the Qur'an has 114 surahs. Nothing was served.")
    if int(req.ayah_start) < 1:
        raise _HE625(status_code=422, detail=f"ayah {req.ayah_start} does not exist - ayaat are numbered from 1. Nothing was served.")
    surah = int(req.surah)
    ayah_start = int(req.ayah_start)
    ayah_end = req.ayah_end if req.ayah_end >= ayah_start else ayah_start
    reference = f"Surah {surah}:{ayah_start}" + (f"–{ayah_end}" if ayah_end > ayah_start else "")

    approach_instructions = {
        "classical": "Apply classical tafsir methodology, drawing on Ibn Kathir, Al-Tabari, and Al-Qurtubi.",
        "thematic": "Apply thematic (mawdu'i) tafsir, connecting this passage to related themes across the Quran.",
        "contemporary": "Apply contemporary tafsir, addressing modern context and relevance to today's world.",
        "linguistic": "Apply linguistic analysis: root words (Arabic root letters), grammatical structures, and rhetorical devices.",
    }.get(req.tafsir_approach, "Apply classical tafsir methodology.")

    # W439 audit catch (HIGH — constitutional): the old prompt structure asked the model for
    # "## {reference} — Arabic Text", instructing whatever model served to EMIT Quranic Arabic
    # from its weights — a direct violation of the immovable constraint (never AI-generate Quran
    # Arabic; authoritative sources only). The authentic text is now FETCHED and injected as
    # given material; the model is explicitly forbidden to produce Arabic beyond quoting it.
    from agentic_core.religious_domain.api import fetch_ayah_arabic, _AYAH_COUNTS
    # refuter catches, round 2: (a) nonexistent ayaat used to get AI exegesis under a note blaming
    # the network — validate against the real counts and refuse; (b) the 10-ayah cap was SILENT
    # while the reference claimed the full range — the covered range is now the reported range.
    if not 1 <= ayah_start <= _AYAH_COUNTS[surah]:
        from fastapi import HTTPException
        raise HTTPException(status_code=422,
                            detail=f"surah {surah} has {_AYAH_COUNTS[surah]} ayaat — "
                                   f"ayah {ayah_start} does not exist")
    _requested_end = ayah_end
    ayah_end = min(ayah_end, _AYAH_COUNTS[surah])
    covered_end = min(ayah_end, ayah_start + 9)
    #  W625 (FU-513) — clipping the end to the surah's length is said too, not only the 10-ayah cap
    range_note = ("; ".join(n for n in (
        (f"surah {surah} has {_AYAH_COUNTS[surah]} ayaat, so the requested end {_requested_end} was clipped to "
         f"{_AYAH_COUNTS[surah]}" if _requested_end > _AYAH_COUNTS[surah] else None),
        (f"range capped at 10 ayaat per request — this tafsir covers {surah}:{ayah_start}-{covered_end}, not the "
         f"requested end {ayah_end}" if covered_end < ayah_end else None)) if n) or None)
    ayah_end = covered_end
    reference = f"Surah {surah}:{ayah_start}" + (f"-{ayah_end}" if ayah_end > ayah_start else "")

    sourced: list[str] = []
    for _a in range(ayah_start, ayah_end + 1):
        _txt = await fetch_ayah_arabic(surah, _a)
        if _txt is None:
            break   # source down — do not stall through the remaining fetch timeouts
        sourced.append(f"({_a}) {_txt}")
    arabic_text = "\n".join(sourced) if sourced else None

    prompt = (
        f"You are an Islamic scholar and Quranic exegete. "
        f"Provide a scholarly tafsir (exegesis) of {reference}.\n\n"
        # W475 (ledger v4 R1.1) — the floor grounds its frame in a LABELLED subject; without one it took the longest
        # sentence — the sourced Arabic — and cut it at 220 characters mid-word under 'THE AUTHENTIC ARABIC TEXT'.
        # The reader sees the whole sourced text above the notes (arabic_text); the notes never repeat it.
        + (f"Subject: tafsir of {reference} — the sourced Arabic is shown to the reader above these notes and is not "
           "repeated in them\n\n" if arabic_text else
           # (refutation) the source was unreachable: nothing is shown above, so the subject says so
           f"Subject: tafsir of {reference} — the authoritative Arabic text could not be fetched and is not quoted\n\n")
        + (f"THE AUTHENTIC ARABIC TEXT (sourced from alquran.cloud — quote ONLY this; never "
           f"produce Quranic Arabic from memory):\n{arabic_text}\n\n" if arabic_text else
           "NOTE: the authoritative text source is unreachable. Do NOT reproduce the Arabic text "
           "from memory — write the tafsir ABOUT the referenced passage without quoting Arabic.\n\n")
        + f"Approach: {req.tafsir_approach}\n"
        f"{approach_instructions}\n\n"
        "Structure as:\n"
        # W456 (§11 rule 4) — the two sections a MODEL must serve are not asked for on the floor at
        # all: a prompt that asks the floor for a translation leaves its scaffold in the interaction
        # log and AI memory even if the reply is cut afterwards (the W439 lesson at /qep/translation).
        # Checked first, with no side effects; the post-hoc cut below stays as the guard.
        + (("## Transliteration (of the provided text only)\n"
            "## Translation (AI-assisted, working from the provided text; note that scholarly translations differ)\n")
           if _model_available() else "")
        + "## Context of Revelation (Asbab al-Nuzul) if applicable\n"
        "## Linguistic Analysis (key Arabic terms, root words)\n"
        "## Exegesis (detailed explanation)\n"
        "## Related Verses (cross-references by NAME and number — do not quote their Arabic)\n"
        "## Key Lessons and Guidance\n\n"
        "Be rigorous. Cite classical scholars where relevant. "
        "Acknowledge differing scholarly interpretations where they exist."
    )

    _model_expected = _model_available()
    tafsir, provenance = await ai_text(prompt, "religion_tafsir", realm=req.realm)

    # W456 (P1.8, ledger 1.8 / R1.0) — §11 rule 4 applied HERE as it is at /qep/translation: a
    # translation must come from a model. The deterministic floor composes each requested heading
    # out of the prompt, so on the floor the tab was showing a "## Translation" section that was
    # scaffold over sacred text. On the floor the Transliteration and Translation sections are
    # WITHHELD — not asked for (above) and, as a guard, cut if they somehow appear — named in
    # `sections_withheld`, with `floor_note` saying why; the sourced Arabic and the reference stand.
    # A model-served tafsir keeps them. Refuter (W456): when a model WAS available and the floor
    # still answered, the prompt had asked for a translation — its scaffold is already in the
    # interaction log and the QMS record sealed the uncut text — so that case is refused outright,
    # as /qep/translation refuses it, rather than cut and shipped under a seal of a different text.
    sections_withheld: list[str] = []
    floor_note = None
    if (provenance or {}).get("served_by") == "native":
        if _model_expected:
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail=(
                "a model resource was available but the deterministic native floor served this tafsir — "
                "a tafsir requested with a translation is not served from the floor; retry"))
        #  W637 (FU-589) — THE SIBLINGS' RULE, applied to the one tool over sacred text that lacked it.
        #  Fatwa, hadith and interfaith withhold every research section on the floor; tafsir withheld two
        #  and SERVED five study headings, each filled with words lifted from this handler's own "Subject:"
        #  instruction line and labelled the reader's request terms. The floor composes headings, not
        #  exegesis, so the five are withheld and named; the sourced Arabic, the reference and the referral
        #  stand. Matched on leading words: the prompt's headings carry parenthetical tails.
        tafsir, _cut = _withhold_sections(tafsir, (
            "Transliteration", "Translation",
            "Context of Revelation", "Linguistic Analysis", "Exegesis", "Related Verses",
            "Key Lessons and Guidance"))
        #  what was never requested on the floor, plus what was ACTUALLY cut — not a fixed pair, because a
        #  list naming a section as withheld while the reply still carries it is the defect itself
        sections_withheld = ["Transliteration", "Translation"] + [
            h for h in _cut if h not in ("Transliteration", "Translation")]
        floor_note = ("served by the deterministic native floor — no translation or transliteration is "
                      "offered (a translation must come from a model; the floor composes headings, not "
                      "meaning). "
                      + ("The sourced Arabic above is authentic; " if arabic_text else
                         "No Arabic is shown because the authoritative source was unreachable; ")
                      + "no exegesis, linguistic analysis, cross-references or lessons are offered here: the "
                        "floor composes headings, not scholarship, and those sections are withheld. Study "
                        "this passage with a qualified teacher.")

    return {
        "tafsir_id": uuid.uuid4().hex[:10],
        "reference": reference,
        "arabic_text": arabic_text,
        "arabic_source": ("alquran.cloud — authentic sourced text, never AI-generated" if arabic_text
                          else "unavailable — source unreachable; the Arabic is never AI-generated, "
                               "so none is shown"),
        **({"range_note": range_note} if range_note else {}),
        "surah": surah,
        "ayah_start": ayah_start,
        "ayah_end": ayah_end,
        "approach": req.tafsir_approach,
        "tafsir": tafsir,
        "sections_withheld": sections_withheld,
        **({"floor_note": floor_note} if floor_note else {}),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        # W456 — the §11 disclaimer the fatwa and halal tools carried and this one did not
        #  W635 (FU-577) - the disclaimer says what THIS response carries: no Arabic when none was fetched, and
        #  'a structured frame' rather than 'AI-labelled content' when the floor wrote it
        "disclaimer": (
            "Study aid — NOT a scholarly tafsir and NOT a ruling. "
            + ("The Arabic is sourced from alquran.cloud and is never AI-generated. " if arabic_text else
               "No Arabic is shown: it could not be fetched, and it is never AI-generated. ")
            + ("Everything else here is a structured frame composed by the native floor, not scholarship"
               if str((provenance or {}).get("served_by", "native")).startswith("native") else
               "Everything else here is AI-labelled content")
            + " - read it with, and check it against, the classical tafasir and a qualified teacher. Scholarly "
              "translations and interpretations differ; where they do, learn from a scholar."
        ),
    }


def _model_available() -> bool:
    """W456 — is any MODEL resource (owned local or opt-in external) available to serve? The floor is
    never a model. Mirrors /qep/translation's pre-check; a refusal has no side effects."""
    try:
        from agentic_core.ai.native.model_resource import local_models, external_allowed
        return bool(local_models()) or external_allowed()
    except Exception:
        return False


def _withhold_sections(text: str, headings: tuple) -> tuple:
    """Cut the named `## ` sections (heading + body up to the next `## `) out of a markdown text.
    Returns (text, [headings actually removed])."""
    import re as _re
    removed: list[str] = []
    out = text or ""
    for h in headings:
        pat = _re.compile(rf"(?ms)^##\s+{_re.escape(h)}\b[^\n]*\n.*?(?=^##\s|\Z)")
        if pat.search(out):
            out = pat.sub("", out)
            removed.append(h)
    return out.strip(), removed


# W483 (R5.2) — a deterministic ingredient screen. Each entry is a term and WHY it is listed; the
# screen returns matches and says plainly what it is. It cannot clear an ingredient (the W483 rule:
# a word list may flag, never clear), so an unmatched list is reported as "nothing matched", never
# as "no concerns". Sources for the concern statements: the E-number's own definition (E471 is
# mono- and diglycerides of fatty acids, which may be animal- or plant-derived) and the standard
# categories of the certifying bodies this tool already names (ESMA/GSO 2055, JAKIM, HFA).
_INGREDIENT_CONCERNS: tuple[tuple[str, str], ...] = (
    ("gelatin", "may be porcine or non-zabiha bovine; the source animal and slaughter method decide"),
    ("gelatine", "may be porcine or non-zabiha bovine; the source animal and slaughter method decide"),
    ("e471", "mono- and diglycerides of fatty acids — may be animal- or plant-derived"),
    ("e472", "esters of mono- and diglycerides — may be animal- or plant-derived"),
    ("e441", "gelatine by another name"),
    ("e542", "edible bone phosphate — animal-derived"),
    ("e631", "disodium inosinate — may be meat- or fish-derived"),
    ("e627", "disodium guanylate — may be meat- or fish-derived"),
    ("e120", "cochineal / carmine — insect-derived"),
    ("e904", "shellac — insect-derived"),
    ("e920", "l-cysteine — may be derived from hair or feathers"),
    ("lard", "porcine fat"),
    ("pork", "porcine"),
    ("bacon", "porcine"),
    ("rennet", "may be animal rennet from a non-zabiha source"),
    ("pepsin", "usually porcine-derived"),
    ("lipase", "may be animal-derived"),
    ("whey", "may be produced with animal rennet"),
    ("glycerin", "may be animal- or plant-derived"),
    ("glycerol", "may be animal- or plant-derived"),
    ("mono- and diglycerides", "may be animal- or plant-derived"),
    ("stearate", "stearic acid may be animal- or plant-derived"),
    ("stearic acid", "may be animal- or plant-derived"),
    ("alcohol", "ethanol as an ingredient or carrier; treatment differs between standards"),
    ("ethanol", "treatment as an ingredient or carrier differs between standards"),
    ("wine", "alcoholic"),
    ("rum", "alcoholic"),
    ("brandy", "alcoholic"),
    ("vanilla extract", "commonly carried in ethanol"),
    ("enzyme", "the source organism decides; microbial is generally accepted"),
    ("emulsifier", "the source of the emulsifier decides"),
    ("collagen", "animal-derived"),
    ("keratin", "animal-derived"),
    ("carmine", "insect-derived"),
)


def _screen_ingredients(ingredients: list[str]) -> dict:
    """Match a declared ingredient list against the terms known to require verification.

    This is a WORD LIST, and the response says so. It flags; it never clears. An ingredient that
    matches nothing is not reported as acceptable — it is reported as not matched, which is a
    different statement and the only one this screen can make.
    """
    items = [str(i) for i in (ingredients or [])]
    flagged = []
    for raw in items:
        # W483 (refutation) — match the forms ingredients are actually DECLARED in. The strict
        # boundary missed every real label: "E-471", "E 471", "INS 471", and the sub-classes
        # "E472a".."E472f" (which is where most of the animal-derived emulsifiers live). E-numbers
        # are normalised before matching, and an E-term may be followed by a sub-class letter.
        low = re.sub(r"\b(?:e|ins)[\s\-]?(\d{3})", r"e\1", raw.lower())
        hits = sorted({term for term, _why in _INGREDIENT_CONCERNS
                       if re.search((rf"(?<![a-z0-9])e{term[1:]}[a-f]?(?![0-9])"
                                     if re.fullmatch(r"e\d{3}", term) else
                                     rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])"), low)})
        if hits:
            why = {t: w for t, w in _INGREDIENT_CONCERNS if t in hits}
            flagged.append({"ingredient": raw, "matched": hits,
                            "why": "; ".join(f"{t}: {why[t]}" for t in hits)})
    return {
        "declared": len(items),
        "flagged": flagged,
        "unmatched": [i for i in items if not any(f["ingredient"] == i for f in flagged)],
        "verdict": None,
        "basis": (f"a deterministic screen of {len(_INGREDIENT_CONCERNS)} terms that commonly require "
                  "verification. It flags ingredients to check with a certifying body; it does not "
                  "assess them, and an ingredient it did not match is NOT thereby acceptable — the "
                  "screen has no view on it. No halal status is produced here."),
    }


class HalalReviewRequest(BaseModel):
    product_name: str
    product_description: str
    ingredients: list[str] = []
    manufacturing_process: str = ""
    target_markets: list[str] = []
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/halal-review")
async def halal_pre_assessment(req: HalalReviewRequest):
    """
    AI-assisted halal certification pre-assessment.
    Identifies potential compliance issues before formal certification.
    """
    ingredients_text = "\n".join(f"  - {i}" for i in req.ingredients) if req.ingredients else "Not specified"
    markets_text = ", ".join(req.target_markets) if req.target_markets else "Not specified"
    _model_expected = _model_available()

    prompt = (
        f"You are a halal certification consultant with expertise in Islamic dietary law (fiqh al-at'ima) "
        f"and international halal standards (ESMA UAE.S/GSO 2055, JAKIM Malaysia, HFA UK).\n\n"
        f"Product: {req.product_name}\n"
        f"Description: {req.product_description}\n"
        f"Ingredients:\n{ingredients_text}\n"
        + (f"Manufacturing process: {req.manufacturing_process}\n" if req.manufacturing_process else "")
        + f"Target markets: {markets_text}\n\n"
        "Conduct a pre-assessment and provide:\n"
        # W483 (ledger v5 R5.2) — the enum used to live IN the heading. The deterministic floor
        # composes its reply out of the requested headings, so it emitted "## Halal Status Assessment
        # (COMPLIANT /" five times — the enum cut short, reading as a COMPLIANT verdict on a product
        # containing gelatin. The heading carries no verdict tokens now, and on the floor the three
        # judging sections are not asked for at all (the W456 tafsir rule: a prompt that asks the
        # floor for a judgement leaves its scaffold in the interaction log even if the reply is cut).
        + (("## Halal Status Assessment\n"
            "## Critical Issues (ingredients or processes requiring resolution)\n"
            "## Flagged Ingredients (E-numbers, derivatives, ambiguous items to verify)\n")
           if _model_expected else "")
        + "## Cross-Contamination Risks\n"
        "## Manufacturing Considerations\n"
        "## Recommended Certifying Bodies (by target market)\n"
        "## Steps to Achieve Certification\n"
        "## Market-Specific Requirements\n\n"
        "Be specific about which standards apply. Flag anything ambiguous — err on the side of caution.\n"
        + ("State the halal status in the first line of the Assessment section as exactly one of: "
           "COMPLIANT, REQUIRES REVIEW, NON-COMPLIANT.\n" if _model_expected else "")
        + "Note: This is a pre-assessment tool only; formal certification requires an accredited certifying body."
    )

    assessment, provenance = await ai_text(prompt, "religion_halal", realm=req.realm,
        user_text=person_said(req.product_name, req.product_description))

    _judging = ("Halal Status Assessment", "Critical Issues", "Flagged Ingredients")
    sections_withheld: list[str] = []
    floor_note = None
    if (provenance or {}).get("served_by") == "native":
        if _model_expected:
            # A model was available and the floor still answered: the judging sections were in the
            # prompt, so their scaffold is already logged. Refuse rather than cut and ship, exactly
            # as the tafsir route does.
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail=(
                "a model resource was available but the deterministic native floor served this halal "
                "pre-assessment — a halal status is not composed from prompt headings; retry"))
        #  W637 (ledger v13 R1.8) — THE TWO RESEARCH SECTIONS GO THE SAME WAY. The floor kept "Recommended
        #  Certifying Bodies" and "Market-Specific Requirements" and filled them from a template: a list of
        #  recommended bodies nobody looked up. A halal status rests on a certificate verified with its
        #  body (Owner, 2026-09-29), so on the floor these are withheld and named, like the judging three.
        _research637 = ("Recommended Certifying Bodies", "Market-Specific Requirements")
        assessment, _cut = _withhold_sections(assessment, _judging + _research637)
        sections_withheld = list(_judging) + [h for h in _research637 if h in _cut]
        floor_note = (
            "served by the deterministic native floor — no halal status, critical issues or flagged "
            "ingredients are offered. The floor composes the headings it is given and cannot read an "
            "ingredient list, so a status from it would be the shape of a verdict with nothing behind "
            "it. The ingredient screen below is a deterministic word list, and the notes that remain "
            "are a structured frame. A halal status comes from an accredited certifying body.")

    return {
        "assessment_id": uuid.uuid4().hex[:10],
        "product_name": req.product_name,
        "target_markets": req.target_markets,
        "assessment": assessment,
        # W483 — a real, deterministic contribution in place of the withheld prose: the ingredients
        # this repository's list knows require verification, each with the reason. Named a screen,
        # never a status (the naming invariant: a quantity carries a method's name only when that
        # method computed it).
        "ingredient_screen": _screen_ingredients(req.ingredients),
        "sections_withheld": sections_withheld,
        **({"floor_note": floor_note} if floor_note else {}),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": disclaimer_for(
            provenance, "This is an AI pre-assessment tool only.",
            "Official halal certification must be obtained from an accredited halal certifying body. This "
            "assessment does not constitute certification."),
    }


class InterfaithRequest(BaseModel):
    topic: str
    traditions: list[str] = ["Islam", "Christianity", "Judaism"]
    dialogue_purpose: str = "understanding"  # understanding | commonalities | differences | dialogue
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


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

    analysis, provenance = await ai_text(prompt, "religion_interfaith", realm=req.realm,
        user_text=person_said(req.topic, req.dialogue_purpose))

    # §15 (W593, FU-421, M1 R1.2) — THE TAFSIR PATTERN, APPLIED TO THE ONE RELIGION TOOL THAT LACKED IT.
    # Its four siblings all withhold on the floor and say so; this route returned a scholar persona over
    # per-tradition "Perspectives", Points of Convergence and "authoritative sources" that nothing looked
    # up, with no floor_note, no sections_withheld and no disclaimer. A tradition's position that nothing
    # researched is worse than silence, and §11 binds hardest here. The per-tradition headings are built
    # FROM THE REQUEST, so the withheld list is built the same way — a fixed list would miss the headings
    # this route invents on every call.
    _floor = (provenance or {}).get("served_by") == "native"
    sections_withheld: list[str] = []
    floor_note = None
    if _floor:
        _heads = []
        for _t in traditions:
            _heads += [f"{_t}'s Perspective on {req.topic}", f"{_t}'s Perspective", f"{_t}"]
        analysis, sections_withheld = _withhold_sections(analysis, tuple(
            _heads + ["Points of Convergence", "Points of Divergence", "Convergence", "Divergence",
                      "Suggested Resources for Further Study", "Suggested Resources", "Resources",
                      "Dialogue Questions (5 open questions for respectful discussion)",
                      "Dialogue Questions", "Overview"]))
        floor_note = (
            "served by the deterministic native floor — NO comparative research happened. The floor "
            "composes the headings it is asked for from the words of the request; it does not read a "
            "tradition's scholarly position, locate an authoritative source, or compare what two faiths "
            "actually teach. Those sections are withheld rather than shown as a frame: a tradition's "
            "position that nothing looked up misrepresents that tradition. Take this to qualified "
            "representatives of the traditions concerned.")

    return {
        "analysis_id": uuid.uuid4().hex[:10],
        "topic": req.topic,
        "traditions": traditions,
        "dialogue_purpose": req.dialogue_purpose,
        "analysis": analysis,
        "sections_withheld": sections_withheld,
        **({"floor_note": floor_note} if floor_note else {}),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": disclaimer_for(
            provenance, "AI-assisted comparative material.",
            "Not scholarship and not a statement of any tradition's position. It represents no faith community "
            "and speaks for none of them; where it was served by the deterministic floor the research sections "
            "are WITHHELD and named in `sections_withheld`. Consult qualified representatives of each tradition."),
    }
