"""
Avatar Interaction API — the real, working multimodal user-interaction layer for
the Workstation avatar widget.

Note on scope: this module deliberately does NOT route through
`agentic_core/avatars/core/recirculation_orchestrator.py` (the "metabolic cycle"
architecture) — and the REASON changed in W533, so the old one is corrected here
rather than left to be repeated. That orchestrator no longer fails on its first
stage: since W533 it runs all six, driven from the heartbeat, with each stage's
latency measured. What it does is WITHHOLD — its clearance chain refuses the
emission because the engines supply no constitutional verdict, for want of a model
path. So routing live user chat through it would replace a working reply with a
chain of correct refusals, which is why P3.16's bar holds the avatar wiring on the
engines having a model path (P3.20–P3.24) rather than on the loop working.
This module instead implements a smaller, genuinely functional chat/voice/vision
pipeline, reusing the already-real `agentic_core.ai.gateway.gateway` (Ollama, with
OpenAI used automatically the moment a valid OPENAI_API_KEY is configured) and the
real `memory_v01` ChromaDB store, while reusing `AvatarState` from the existing
avatar_engine for genuine per-session identity.

Vision (image understanding) is IN-HOUSE-FIRST: `/chat` analyses an attached image with a LOCAL
Ollama vision model (e.g. `llava` / `llama3.2-vision` / `moondream`, set via OLLAMA_VISION_MODEL) —
owned, no external dependency — and only falls back to an external provider (OpenAI) if a key is
configured. If neither is available the image is received but its contents are NOT analysed and this is
stated honestly (never a fabricated description). The response reports `image_served_by` +
`image_is_external` so vision provenance is explicit. Voice: the CLIENT uses browser-native Web
Speech (STT) + speechSynthesis (TTS) as the in-house default (W325 — genuinely wired in
useAvatarSession, no key needed); the `/transcribe` + `/speak` endpoints are the OPTIONAL external
accelerant (OpenAI Whisper/tts-1, 503 without a working key — honestly labelled).
"""
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response

from agentic_core.auth.core import get_current_user, require_admin
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.ai.ceo.memory_v01 import memory_v01
from agentic_core.avatars.core.avatar_engine import AvatarState

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/avatar", tags=["Avatar Interaction"])

DOMAIN_PROMPTS: Dict[str, str] = {
    "ceo": "You are the Workstation AI CEO's executive assistant avatar. Be decisive, strategic, and concise.",
    "c-suite": "You are a C-Suite advisory avatar (CFO/CTO/COO perspective). Focus on operational and financial clarity.",
    "coe": "You are a Center of Excellence advisory avatar. Focus on best practice, standards, and cross-team enablement.",
    "bto": "You are the BTO (Build-to-Order) Catalog avatar. Help the user configure, understand, and order BTO products.",
    "capital": "You are the Capital Fund avatar. Help with investment, allocation, and financial reporting questions.",
    "employment": "You are the Employment Hub avatar. Help with applications, CVs, interviews, and job search.",
    "realms": "You are a Realm avatar. Help the user navigate and configure their sovereign realm.",
    "domains": "You are a Domain Suite avatar (Religion/Science/Law/Care/Education). Be domain-appropriate and precise.",
    "products": "You are the Product Catalog avatar. Help the user discover and understand available products.",
    "organism": "You are the Workstation Organism avatar, speaking to the system's overall health and self-evolution.",
    "entity": "You are the Workstation Entity avatar, representing the sovereign system's unified identity.",
    "vsb": "You are the VSB (Virtual Sovereign Business) avatar, helping with business operations across the mesh.",
    "general": "You are the Workstation Sovereign Mesh avatar — a helpful, concise assistant across the whole platform.",
}


class AvatarSession(BaseModel):
    session_id: str
    avatar_id: str
    state_checksum: str


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    context: str = "general"
    image_base64: Optional[str] = None
    vsb_id: Optional[str] = None       # when set, the avatar is grounded in this live VSB entity
    language: Optional[str] = None     # respond in this language (e.g. "Arabic", "Urdu", "French"); default English


class ChatResponse(BaseModel):
    session_id: str
    response: str
    #  P3.28 clause (5) / FU-412 (W606) — whether the constitutional clearance chain cleared this reply. None
    #  means the chain was NOT RUN (no approval is recorded for this learner and mode), which is said in
    #  clearance_reason rather than left to read as a pass; False means it was withheld, and `response` then
    #  carries the gate's reason, never the withheld draft.
    cleared: Optional[bool] = None
    clearance_reason: Optional[str] = None
    clearance_gates: Optional[List[Dict[str, Any]]] = None
    image_understood: bool = False
    image_served_by: Optional[str] = None  # which resource analysed the image: "ollama" (in-house) | "openai" | None
    image_is_external: bool = False        # honest: was the image sent to an external provider?
    # W490 (refutation) — WHICH not-read state it was. The reached page said "no vision model was
    # available" for all of them, which is false when one WAS available and the image was
    # transmitted to it and the call failed — and that wording suppressed the one fact the user
    # most needs on that path: their image left the platform.
    #   read | failed_external | blocked_by_policy | no_vision_model | none (no image sent)
    image_status: str = "none"
    # P3.5 clause (2) — WHY, when the status is no_vision_model. A status is a label; the clause asks for
    # "an accurate reason naming what is missing", and `image_status` names only the outcome. This carries
    # the MEASURED shortfall — the perception tier's memory and GPU requirement and what the machine
    # actually has — read from the tier registry rather than written here, so it cannot drift from reality.
    image_refusal: Optional[str] = None
    # P3.5 clause (3) — what this deployment CAN read, computed from the installed resource. Empty when
    # nothing can read an image, which is the honest answer; a list naming a format nothing can read would
    # be a promise the deployment cannot keep.
    image_accepts: List[str] = []
    context: str
    served_by: str = "native"          # which OWNED resource answered the TEXT (in-house-first provenance)
    is_external: bool = False
    grounded_in: Optional[str] = None  # the vsb_id the answer was grounded in, if any
    #  W648 (FU-650, ledger v14 R5) - WHETHER THE GROUNDING WAS USED, and why. `grounded_in` says an entity's
    #  record reached the PROMPT. The native floor does not read it, so on a floor reply the page printed
    #  "grounded in your enterprise" over text that used none of the enterprise's state. `grounded_in` keeps
    #  its meaning; these say what happened with it. None when there was no grounding at all.
    grounding_used: Optional[bool] = None
    grounding_basis: Optional[str] = None
    language: Optional[str] = None     # the language the answer was requested in (echoed back)
    # W505 (P2.3) — a null that SAYS WHY. W326 correctly stopped echoing a requested language the floor
    # cannot deliver; the user was then left with a null and no reason. This is that reason, and it is
    # present ONLY when a language was asked for and not honoured.
    language_note: Optional[str] = None
    # W505 (P2.3) — whether the user's profile shaped this answer. gateway.query_meta has produced this
    # since W428 and the avatar's reply never carried it: a field produced and rendered nowhere.
    profile_applied: bool = False
    profile_state: Optional[str] = None     # W616 (FU-397) — applied | none_written | unreadable | …
    profile_basis: Optional[str] = None
    suggested_areas: List[Dict[str, str]] = []   # §5/§9 guided navigation — WHITELISTED platform areas only


# ── §5/§9 guided navigation — the avatar can take the user to any platform area ──
# A WHITELISTED catalogue of REAL routes (mirrors App.tsx). Selection is a deterministic keyword
# match on the user's message — the avatar can only ever point at areas that exist; it can never
# invent a route, and the match reason is surfaced honestly.
_PLATFORM_AREAS: List[Dict[str, Any]] = [
    {"route": "/genesis", "label": "Genesis — Concept → Commercialisation",
     "keywords": ["genesis", "journey", "concept", "commercialis", "start a business", "my idea",
                  "establish", "new venture", "found a", "startup"]},
    {"route": "/domains", "label": "Work in a Domain",
     "keywords": ["domain tool", "law", "legal", "science", "care plan", "education", "religion",
                  "quran", "employment", "cv", "lesson"]},
    {"route": "/resource-fabric", "label": "Resource Fabric Composer",
     "keywords": ["fabric", "compose", "composition", "combine resources", "reconfigure", "reactor",
                  "incubator", "petri", "simulator"]},
    {"route": "/native-ai", "label": "Native AI Fabric",
     "keywords": ["native ai", "own model", "swarm", "orchestrat", "ollama", "ensemble", "local model"]},
    {"route": "/organism", "label": "Living Organism",
     "keywords": ["organism", "heartbeat", "immune", "vitals", "nervous", "biomimetic", "health of the"]},
    {"route": "/economy", "label": "Economic Organism (virtual WST)",
     "keywords": ["economy", "waterfall", "charity", "wst", "ledger", "profit", "distribution",
                  "owner payment", "finance", "balance sheet", "period close"]},
    {"route": "/vsb-cockpit", "label": "VSB Cockpit",
     "keywords": ["my vsb", "cockpit", "my enterprise", "living enterprise", "my business"]},
    {"route": "/business-plan", "label": "Living Business Plan",
     "keywords": ["business plan", "objectives", "strategy", "kpi", "mission", "milestones"]},
    {"route": "/deliverables", "label": "Living Deliverables",
     "keywords": ["deliverable", "export", "download report", "my outputs", "documents"]},
    {"route": "/governance-hub", "label": "Governance & Trust",
     "keywords": ["governance", "constitution", "compliance", "audit", "change control", "halal check", "gaas"]},
    {"route": "/generator", "label": "The Generator",
     "keywords": ["generate code", "schema", "artefact", "generator", "config file"]},
    {"route": "/marketplace", "label": "Marketplace",
     "keywords": ["marketplace", "catalogue", "products", "buy", "listing"]},
    {"route": "/my-work", "label": "My Work",
     "keywords": ["my work", "history", "past results", "saved outputs", "previous"]},
    {"route": "/ceo", "label": "Living Organisation (AI CEO · Board)",
     "keywords": ["ceo", "c-suite", "board", "chief", "org chart", "organisation"]},
]

ALLOWED_NAVIGATION_ROUTES = {a["route"] for a in _PLATFORM_AREAS}


def _suggest_areas(message: str, limit: int = 3) -> List[Dict[str, str]]:
    """Deterministic keyword match over the whitelisted catalogue. Returns at most `limit` REAL
    platform areas with an honest match reason; empty when nothing matches (no forced suggestions)."""
    low = f" {(message or '').lower()} "
    scored = []
    for area in _PLATFORM_AREAS:
        hits = [k for k in area["keywords"] if k in low]
        if hits:
            scored.append((len(hits), {"route": area["route"], "label": area["label"],
                                       "because": "matched: " + ", ".join(hits[:3])}))
    scored.sort(key=lambda x: -x[0])
    return [a for _, a in scored[:limit]]


def _hold_phrase(reg: dict) -> str:
    """W503 (FU-059, FU-063) — what the roster row actually says about this entity, in one phrase.

    Four outcomes, not one word: a DECISION hold names the decision; a decision hold with no Change
    Control record is the gate erroring, and says so rather than claiming a ruling; anything else in the
    hold position is the platform unable to act; and a visit that RAISED is not a hold at all. The
    module's own classifier is reused so the avatar cannot drift from the roster page."""
    from agentic_core.economy.living_vsbs import _DECISION_HOLDS, _RECORD_UNKNOWN, _outcome_of_hold
    hold = reg.get("last_hold")
    parts = []
    if hold:
        record = reg.get("last_hold_record", _RECORD_UNKNOWN)
        if hold in _DECISION_HOLDS and record is None:
            parts.append(f" — HELD ({hold}), but NO Change Control record was written: the gate could "
                         "not be reached, so nothing has been decided about this enterprise")
        elif _outcome_of_hold(hold, record) == "held":
            parts.append(f" — HELD by a decision ({hold})")
        else:
            parts.append(f" — no cycle runs: {hold} could not be used (about the platform, not this "
                         "enterprise)")
    if reg.get("decision_hold"):
        parts.append(f" · a standing Change Control decision ({reg['decision_hold']}) sits behind that")
    if reg.get("last_error"):
        parts.append(f" · the last visit RAISED: {str(reg['last_error'])[:120]}")
    return "".join(parts)


def _vsb_grounding(vsb_id: str) -> str:
    """Build a grounding block from a live VSB entity so the avatar answers IN its context."""
    try:
        from agentic_core.api.vsb import _load_vsb
        v = _load_vsb(vsb_id)
        if not v:
            return ""
        eco = v.get("economy") or {}
        chief = ((v.get("board") or {}).get("chief") or {}).get("title", "")
        bp = ""
        try:
            from agentic_core.api.business_plan import _load as _bp_load
            objs = [o.get("title") for o in (_bp_load(vsb_id).get("objectives") or [])][:4]
            bp = f"Objectives: {', '.join(o for o in objs if o)}" if any(objs) else ""
        except Exception:
            pass
        # §9 (W325) — LIVE figures, not just static header fields: the economy's real operating
        # state, the latest §11 verdict, and any hold — so 'enterprise-aware' is true.
        live = []
        try:
            from agentic_core.economy.living_vsbs import _load as _lv_load
            reg = _lv_load().get(vsb_id) or {}
            if reg:
                # W491 (FU-192) - the roster's tally is not the entity's cycle count; the avatar says which
                live.append(f"- Economy (virtual WST): {reg.get('operating_cycles', 0)} cycles run by the "
                            f"autonomous roster (cycles run by other paths are on the books, not in this tally)"
                            + (f", last distributable {reg.get('last_distributable')} WST"
                               if reg.get("last_distributable") is not None else "")
                            # W503 (FU-059, FU-063) — this printed the raw roster field as "HELD (x)",
                            # blind to whether x is a DECISION or the platform simply unable to act, and
                            # blind to `decision_hold` and `last_error` entirely. A gate that errors
                            # records `held_for_change_control` with NO record, so the founder's own
                            # avatar would have told them Change Control had ruled on their enterprise.
                            + _hold_phrase(reg))
        except Exception:
            pass
        try:
            # W506 (FU-075) - a partial read made an entry look ABSENT, so this silently omitted a screen
            # result, including a FAIL. A person asking their enterprise about compliance must not be told
            # nothing when the answer is "the record is damaged".
            from agentic_core.config import data_path, read_json_reported
            _all_comp, _comp_why = read_json_reported(data_path("vsb_compliance_history.json"), {})
            comp = (_all_comp or {}).get(vsb_id) or {}
            if comp.get("overall"):
                live.append(f"- Latest §11 compliance screen: {comp['overall']}"
                            + (" (REGRESSION)" if comp.get("regression") else ""))
            elif _comp_why:
                live.append("- Latest §11 compliance screen: NOT AVAILABLE - the compliance history could "
                            "not be read whole, so this enterprise's latest screen is unknown rather than "
                            "absent. It is not a pass.")
        except Exception:
            pass
        return (
            "\n\nYou are THIS VSB's enterprise-aware avatar — ground every answer in its live state:\n"
            f"- VSB: {v.get('name')} (domain: {v.get('domain')}, stage: {v.get('stage')})\n"
            f"- Mission: {v.get('challenge', '')}\n"
            f"- Chief (owner digital twin): {chief}\n"
            f"- Entity type: {eco.get('entity_type', '')}\n"
            + (f"- {bp}\n" if bp else "")
            + ("".join(f"{ln}\n" for ln in live))
        )
    except Exception:
        return ""


async def _ollama_vision(image_base64: str, message: str) -> Optional[str]:
    """In-house vision: analyse an image with a LOCAL Ollama vision model (e.g. llava / llama3.2-vision /
    moondream) — owned, no external dependency. Returns the analysis text, or None if no local vision
    model is available (caller then falls back honestly — never fabricates image content)."""
    import httpx
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    model = os.getenv("OLLAMA_VISION_MODEL", "llava")
    try:
        async with httpx.AsyncClient(timeout=float(os.getenv("OLLAMA_VISION_TIMEOUT", "30"))) as client:
            r = await client.post(ollama_url, json={
                "model": model,
                "prompt": f"{message}\n\nDescribe what is relevant in this image for the user's request. Be specific and honest; if the image is unclear, say so.",
                "images": [image_base64],
                "stream": False,
            })
            if r.status_code == 200:
                out = (r.json().get("response") or "").strip()
                return out or None
    except Exception:
        pass
    return None


class SpeakRequest(BaseModel):
    text: str


class SessionSummary(BaseModel):
    session_id: str
    avatar_id: str
    context: str
    message_count: int
    last_message: Optional[str] = None


# session_id -> {avatar: AvatarState, history: [{role, content}], context: str}
_sessions: Dict[str, Dict[str, Any]] = {}


def _get_or_create_session(session_id: Optional[str], user_id: str = "demo_user",
                           owner_id: str | None = None) -> str:
    """§17.5 invariant 1 (W350) — every session is stamped with its creator's namespace at
    creation: the Round-10 audit proved any ANONYMOUS caller could list, read (with message
    previews), and DELETE every user's conversations. owner_id=None = the single-user namespace
    (auth off); under auth it is the authenticated username."""
    if session_id and session_id in _sessions:
        return session_id
    new_id = session_id or str(uuid.uuid4())
    avatar_id = f"did:workstation:{uuid.uuid4().hex[:16]}"
    state = AvatarState(avatar_id=avatar_id, user_id=user_id)
    state.state_checksum = state.compute_state_hash()
    _sessions[new_id] = {"avatar": state, "history": [], "context": "general",
                         "owner_id": owner_id}
    return new_id


def _require_session_access(session_id: str, user: dict | None) -> dict:
    """§17.5 invariant 1 (W350) — session reads/mutations are owner-scoped: 404 (never 403)
    when scoped out; auth-off single-user mode unguarded (one tenant)."""
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    from agentic_core.auth.core import user_can_access
    u = user if isinstance(user, dict) else None
    if not user_can_access(u, session.get("owner_id")):
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/session", response_model=AvatarSession)
async def create_session(user: dict | None = Depends(get_current_user)):
    """Creates a new avatar identity + conversation session (owner-stamped, W350)."""
    session_id = _get_or_create_session(
        None, owner_id=(user.get("username") if isinstance(user, dict) else None))
    session = _sessions[session_id]
    return AvatarSession(
        session_id=session_id,
        avatar_id=session["avatar"].avatar_id,
        state_checksum=session["avatar"].state_checksum,
    )


class RatificationRequest(BaseModel):
    purpose: str
    modes: List[str] = ["instructor"]
    user_id: Optional[str] = None      # single-user mode only; under auth the caller is always the learner


class ObjectivesRequest(BaseModel):
    objectives: List[Dict[str, Any]]


def _learner_id(user: dict | None, requested: Optional[str]) -> str:
    """The same identity the chat route clears against: the signed-in username, else the session default."""
    from agentic_core.auth.core import request_owner_id
    return request_owner_id(user, requested or "demo_user")


@router.post("/ratifications")
async def record_ratification(req: RatificationRequest, user: dict | None = Depends(get_current_user)):
    """FU-471 option 3 — a learner records, once, what they want the avatar for. Clearance gate 2 counts it."""
    from agentic_core.avatars.core import ratifications as _rat
    _uid = _learner_id(user, req.user_id)
    res = _rat.record(_uid, req.purpose, req.modes, by=_uid)
    if not res["recorded"]:
        raise HTTPException(status_code=422, detail=res)
    return res


@router.get("/ratifications")
async def list_ratifications(user_id: Optional[str] = None, user: dict | None = Depends(get_current_user)):
    from agentic_core.avatars.core import ratifications as _rat
    _uid = _learner_id(user, user_id)
    rows = [r for r in (_rat._load().get("ratifications") or []) if r.get("user_id") == _uid]
    return {"user_id": _uid, "ratifications": rows, "high_impact_modes": list(_rat.HIGH_IMPACT_MODES)}


@router.post("/ratifications/{rid}/revoke")
async def revoke_ratification(rid: str, user: dict | None = Depends(get_current_user)):
    from agentic_core.avatars.core import ratifications as _rat
    _row = next((r for r in (_rat._load().get("ratifications") or []) if r.get("id") == rid), None)
    from agentic_core.auth.core import auth_enabled
    if _row is None or (auth_enabled() and _row.get("user_id") != _learner_id(user, None)
                        and (user or {}).get("role") != "admin"):
        raise HTTPException(status_code=404, detail=f"ratification {rid} not found")
    return _rat.revoke(rid, by=_learner_id(user, None))


@router.post("/ratifications/{rid}/cosign")
async def cosign_ratification(rid: str, admin: dict = Depends(require_admin)):
    """The Owner co-signs a learner's approval, which a HIGH-IMPACT mode needs as its second signature."""
    from agentic_core.avatars.core import ratifications as _rat
    res = _rat.cosign(rid, by_owner=str(admin.get("username") or "owner"))
    if not res.get("cosigned"):
        raise HTTPException(status_code=404 if res.get("refused") == "not_found" else 422, detail=res)
    return res


@router.get("/balance-objectives")
async def get_balance_objectives(user: dict | None = Depends(get_current_user)):
    """The Owner's goals are PLATFORM-level, not one tenant's data, so any caller may read them; the dependency is
    taken so this route sits inside the tenancy matrix like every other, rather than outside it."""
    from agentic_core.avatars.core import balance_objectives as _bo
    return {**_bo.get(), "measured": _bo.MEASURED, "directions": list(_bo.DIRECTIONS)}


@router.put("/balance-objectives")
async def put_balance_objectives(req: ObjectivesRequest, admin: dict = Depends(require_admin)):
    """The Owner's goals for a reply's depth against its load, which clearance gate 3 balances over."""
    from agentic_core.avatars.core import balance_objectives as _bo
    res = _bo.set_objectives(req.objectives, by=str(admin.get("username") or "owner"))
    if not res["recorded"]:
        raise HTTPException(status_code=422, detail=res)
    return res


_CHAT_CHAIN = None


def _chat_chain():
    """One clearance chain for chat, built on first use with the same engines the loop consults."""
    global _CHAT_CHAIN
    if _CHAT_CHAIN is None:
        from agentic_core.avatars.cognition.mushawara_bridge import AvatarCognitiveOrchestrator
        from agentic_core.avatars.core.clearance_chain import ConstitutionalClearanceChain
        from agentic_core.ueg.logger import VSBUEGLogger
        from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme
        _ueg = VSBUEGLogger()
        _CHAT_CHAIN = ConstitutionalClearanceChain(_ueg, AvatarCognitiveOrchestrator(
            _ueg, OmniEnforcementPatternSupreme({"fail_on_missing_validator": False}, {"task": "avatar_chat"})))
    return _CHAT_CHAIN


async def _clear_chat_answer(session: Dict[str, Any], owner: Optional[str], text: str) -> Dict[str, Any]:
    """Run an approved learner's reply through the clearance chain (FU-471 option 3, P3.28 clause 5).

    No approval recorded for this learner and mode -> the chain is NOT run and the reply says so (cleared None):
    the hold continues for them, with no silent regression and no silent pass. Gate 4's state is the session
    avatar's own recorded numbers, compared with the previous turn of this session.
    """
    from agentic_core.avatars.core import ratifications as _rat
    from agentic_core.avatars.core.recirculation_orchestrator import clearance_inputs
    _av = session.get("avatar")
    _uid = str(owner or getattr(_av, "user_id", "") or "")
    _mode = str(getattr(_av, "mode", "") or "instructor")
    if not _rat.signatures_for(_uid, _mode)["ratification_ids"]:
        return {"cleared": None, "gates": None,
                "reason": (f"NOT cleared by the constitutional clearance chain: no approval is recorded for this "
                           f"learner in mode {_mode!r}, so the chain was not run and this is the avatar's ordinary "
                           f"answer. Record what you want the avatar for to have replies cleared")}
    _ctx = clearance_inputs(_uid, _mode, {"emitted": text})
    _cur: Dict[str, float] = {}
    for _dom, _vals in (getattr(_av, "skill_profile", None) or {}).items():
        for _k, _v in (_vals or {}).items():
            if isinstance(_v, (int, float)) and not isinstance(_v, bool):
                _cur[f"skill.{_dom}.{_k}"] = float(_v)
    _e = getattr(_av, "energy_budget_j", None)
    if isinstance(_e, (int, float)) and not isinstance(_e, bool):
        _cur["energy_budget_j"] = float(_e)
    _ctx.update(baseline=session.get("drift_baseline"), current=_cur, user_id=_uid)
    try:
        _res = await _chat_chain().validate_emission({"id": f"chat_{uuid.uuid4().hex[:10]}", "text": text}, _ctx)
    except Exception as exc:  # noqa: BLE001 - a chain that could not run WITHHOLDS, it never passes
        session["drift_baseline"] = _cur
        return {"cleared": False, "gates": None,
                "reason": f"the clearance chain could not run ({exc.__class__.__name__}: {str(exc)[:120]})"}
    session["drift_baseline"] = _cur
    #  FU-472 (Owner ruling, choice 1) — A CLEARED REPLY SAYS WHAT ITS CLEARANCE DOES NOT COVER. The coverage
    #  bases of the gates that cleared by coverage are carried verbatim, so every unchecked rule is named.
    _cov_bases = [g.get("basis") for g in (getattr(_res, "gates", None) or [])
                  if isinstance(g, dict) and g.get("coverage")]
    return {"cleared": bool(_res.passed), "gates": getattr(_res, "gates", None),
            "reason": (_res.reason if not _res.passed else
                       "cleared by every gate of the constitutional clearance chain"
                       + (". What this clearance does NOT cover: " + " | ".join(_cov_bases) if _cov_bases else ""))}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, user: dict | None = Depends(get_current_user)):
    # §17.5 invariant 1 (W343) — the avatar's identity-blind route was the widest memory-bleed
    # surface: every conversation (with VSB grounding baked into the prompt) entered the global
    # pool twice. The authenticated caller's namespace now scopes BOTH stores.
    """Real text (and, when a multimodal key is available, image-aware) chat turn."""
    _owner = user.get("username") if isinstance(user, dict) else None
    #  P3.5 clauses (2) and (3) — computed ONCE per turn from what is actually installed. Read here rather
    #  than written anywhere: the refusal names the perception tier's declared requirement and the measured
    #  machine, and the accept list is derived from the matched resource, so neither can drift from reality.
    from agentic_core.ai.native.tiers import image_intake as _image_intake
    _img_intake = _image_intake()
    session_id = _get_or_create_session(request.session_id, owner_id=_owner)   # W350 — stamped
    session = _require_session_access(session_id, user)   # resuming another tenant's id → 404
    history: List[Dict[str, str]] = session["history"]

    session["context"] = request.context
    domain_prompt = DOMAIN_PROMPTS.get(request.context, DOMAIN_PROMPTS["general"])

    image_understood = False
    image_note = ""
    image_served_by: Optional[str] = None
    image_is_external = False
    if request.image_base64:
        # IN-HOUSE-FIRST vision: try a LOCAL Ollama vision model first (owned, no external dependency).
        vision_out = await _ollama_vision(request.image_base64, request.message)
        image_status = "no_vision_model"
        if vision_out:
            image_note = vision_out
            image_understood = True
            image_served_by = "ollama"
            image_is_external = False
            image_status = "read"
        else:
            # §6 (W335) — the external accelerant requires the EXPLICIT platform opt-in, never key
            # presence alone: previously a configured key shipped the user's image to OpenAI with
            # AI_ALLOW_EXTERNAL off. And is_external is truthful the moment transmission is
            # ATTEMPTED — a failed call still sent the image externally.
            from agentic_core.ai.native.model_resource import external_allowed
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key and external_allowed():
                image_is_external = True   # transmission attempted = the image left the platform
                try:
                    from openai import AsyncOpenAI
                    client = AsyncOpenAI(api_key=openai_key)
                    vision_resp = await client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"{request.message}\n\nDescribe what's relevant in this image for the user's request."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{request.image_base64}"}},
                            ],
                        }],
                        timeout=20,
                    )
                    image_note = vision_resp.choices[0].message.content or ""
                    image_understood = True
                    image_served_by = "openai"
                    image_status = "read"
                except Exception as e:
                    image_served_by = "openai"
                    image_status = "failed_external"   # it LEFT the platform and the call failed
                    image_note = f"(Image attached but could not be analysed: vision backend unavailable — {str(e)[:150]})"
            elif openai_key and not external_allowed():
                image_status = "blocked_by_policy"
                image_note = ("(Image attached and received. An external vision key is configured but "
                              "AI_ALLOW_EXTERNAL is off, so the image was NOT sent externally and was "
                              "not analysed — set OLLAMA_VISION_MODEL for in-house vision.)")
            else:
                # Honest: the image was received but NOT analysed — no fabricated description.
                image_note = ("(Image attached and received, but no in-house vision model (set OLLAMA_VISION_MODEL, "
                              "e.g. llava/llama3.2-vision) or external vision key is available, so its contents were not analysed.)")

    grounding = _vsb_grounding(request.vsb_id) if request.vsb_id else ""
    history_block = "\n".join(f"{h['role']}: {h['content']}" for h in history[-10:])
    # All-language: instruct the in-house fabric to answer in the requested language (default English).
    lang = (request.language or "").strip()
    lang_instr = f"Respond ENTIRELY in {lang}. " if lang and lang.lower() not in ("english", "en") else ""
    #  W637 (FU-597) — THE AVATAR SAYS WHAT IT IS. It named no domain, so the floor told every reader their
    #  request "named no domain" — and for a user with a VSB, the engine's case-insensitive field read would
    #  take the grounding block's "(domain: <the entity's>, stage: …)" as the domain of whatever they asked.
    #  An exact-case line first settles both: a fact about this caller, not a domain inferred for the user.
    prompt = (
        "Domain: cross-domain (the avatar is a conversation across every domain, not a domain tool)\n"
        f"{domain_prompt}{grounding}\n\n"
        f"{lang_instr}"
        f"{f'Conversation so far:\n{history_block}\n\n' if history_block else ''}"
        f"{f'Image analysis: {image_note}\n\n' if image_note else ''}"
        f"User: {request.message}"
    )

    # In-house-first via the native fabric — always answers (native floor) and reports which
    # OWNED resource served it; bounded so the avatar stays responsive.
    _owner = user.get("username") if isinstance(user, dict) else None
    # W488 (refutation) — one of the TWO callers that keep recall, deliberately and on the record
    # (the other is the AI-CEO chat, api/v138/ceo.py). W490 corrected this comment: it said "the ONE
    # generation caller" four lines above text naming two, and a guard pinned the wrong half.
    # A conversation is the surface recall is for: the avatar is answering this person, its answer is not
    # persisted as anyone's authored content, and W333 scopes the recall to `owner_id` — this caller's own
    # namespace plus platform memory, never the whole pool. Recall is OFF by default at the gateway
    # since W489; this caller and the AI-CEO chat are the two that opt back in, by name
    # (W332, extended to all of them in W488); an unauthenticated caller here has no namespace, so it
    # reaches platform memory only.
    meta = await gateway.query_meta(prompt, agent=f"avatar:{request.context}", timeout=20.0,
                                    owner_id=_owner, augment=True,
                                    user_text=(request.message or None))   # W641 - the message typed
    response_text = meta.get("output", "")
    #  P3.28 clause (5) — THE HOLD IS RELEASED BY THE CHAIN, NOT AROUND IT. An approved learner's reply is
    #  delivered only if the clearance chain clears it; otherwise the gate's reason is what they see.
    _clr = await _clear_chat_answer(session, _owner, response_text)
    if _clr["cleared"] is False:
        response_text = ("This reply was withheld by the constitutional clearance chain: "
                         f"{_clr['reason']}")

    history.append({"role": "user", "content": request.message})
    history.append({"role": "assistant", "content": response_text})
    memory_v01.add_exchange(f"AVATAR[{request.context}]: {request.message}", response_text,
                            owner_id=_owner)   # W343 — tenant-stamped

    return ChatResponse(
        session_id=session_id,
        response=response_text,
        cleared=_clr["cleared"],
        clearance_reason=_clr["reason"],
        clearance_gates=_clr["gates"],
        image_understood=image_understood,
        image_served_by=image_served_by,
        image_is_external=image_is_external,
        image_status=image_status if request.image_base64 else "none",
        #  P3.5 clauses (2) and (3) — the REASON and the accept list, both computed from what is installed
        #  rather than written here. `image_intake()` reads the perception tier's declared requirements and
        #  the measured machine, so the refusal names the actual shortfall and the accept list is empty
        #  exactly when nothing can read an image. Only populated on the no-vision-model path: a successful
        #  read needs no refusal, and asserting one would contradict the reading it just performed.
        #  ON EVERY not-understood path, not only `no_vision_model`. Measured W599: with no owned vision
        #  model AND an external key present while AI_ALLOW_EXTERNAL is off, the status is
        #  `blocked_by_policy` — which attributes the failure to POLICY when a resource is ALSO missing, so
        #  a reader concludes an administrator blocked it. Both facts are true and the owned-resource
        #  shortfall is the primary one on an in-house-first platform, so it is stated whenever the image
        #  was not read, whatever the status says about the external path.
        image_refusal=(_img_intake["refusal"]
                       if (request.image_base64 and not image_understood) else None),
        image_accepts=list(_img_intake["accepts"]),
        context=request.context,
        served_by=meta.get("served_by", "native"),
        is_external=bool(meta.get("is_external")),
        # §9 (W325) — HONEST: grounded_in is asserted only when a grounding block actually built
        # (previously the request's vsb_id was echoed back even for a missing entity).
        grounded_in=(request.vsb_id if grounding else None),
        grounding_used=((meta.get("served_by", "native") != "native") if grounding else None),
        grounding_basis=((("your enterprise's record reached the prompt, but the native floor does not read "
                           "it: this reply used none of it") if meta.get("served_by", "native") == "native" else
                          "your enterprise's record was in the prompt the model answered from")
                         if grounding else None),
        # W326 — language reports what was HONOURED: the deterministic floor cannot translate,
        # so a requested language served by the floor is not echoed back as an achievement.
        language=((lang or None) if ((not lang_instr) or meta.get("served_by", "native") != "native")
                  else None),
        # W505 (P2.3) — the same condition, stated. When a language WAS requested and the floor served it,
        # the answer is in English and the reason is the floor's own limit, not the user's request.
        language_note=(f"Answered in English — your language needs the owned model. "
                       f"You asked for {lang}, and the deterministic floor served this answer; it cannot "
                       f"translate. Set up the owned local model and ask again."
                       if (lang and lang_instr and meta.get("served_by", "native") == "native") else None),
        profile_applied=bool(meta.get("profile_applied")),
        profile_state=meta.get("profile_state"), profile_basis=meta.get("profile_basis"),
        suggested_areas=_suggest_areas(request.message),
    )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str, user: dict | None = Depends(get_current_user)):
    """Clears a session's conversation history and removes it from memory.
    §17.5 invariant 1 (W350) — owner-scoped: an anonymous caller could previously delete ANY
    user's conversation."""
    if session_id in _sessions:
        _require_session_access(session_id, user)
        del _sessions[session_id]
    return {"cleared": True, "session_id": session_id}


@router.get("/status")
async def ai_status():
    """Health check. The avatar is ALWAYS online: it runs on Workstation's OWN native fabric
    (the native floor always serves), so `online` is true regardless of any external/local
    model. The provider flags below indicate optional accelerants only."""
    import httpx as _httpx
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    base_url = ollama_url.rsplit("/api/", 1)[0]
    try:
        async with _httpx.AsyncClient(timeout=4.0) as client:
            r = await client.get(f"{base_url}/api/tags")
            ollama = r.status_code == 200
    except Exception:
        ollama = False
    # W505 (P2.3) — THE EFFECTIVE SERVING MODE. The flags below say what EXISTS; none of them said which
    # tier would actually serve the next request, which is what "effective serving mode" means. Computed
    # from the same three facts the gateway decides on, and it names its own limit: an env var's presence is
    # not a working key, so a mode that depends on one is reported as expected, never as confirmed.
    _local_off = os.getenv("AI_DISABLE_LOCAL", "").lower() in ("1", "true", "yes")
    # the SAME gate the gateway decides on (gateway.py:425) — external accelerants are OFF by default
    _external_allowed = os.getenv("AI_ALLOW_EXTERNAL", "false").lower() == "true"
    _key_present = bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    if ollama and not _local_off:
        _mode, _basis = "owned local model", "Ollama answered its tags endpoint and local serving is enabled"
    elif _external_allowed and _key_present:
        _mode, _basis = ("external accelerant (expected)",
                         "no owned local model is reachable, external use is permitted and a key is "
                         "PRESENT — whether that key works is only known at call time")
    else:
        _why = ("no owned local model is reachable" if not _key_present else
                "no owned local model is reachable and, although an external key is present, external use "
                "is NOT permitted (AI_ALLOW_EXTERNAL is off)")
        _mode, _basis = ("deterministic floor",
                         f"{_why}; the floor always answers, and it cannot translate or reason like a model")
    return {
        "online": True,                 # native fabric guarantees the avatar always answers
        "posture": "in-house-first",
        "native": True,
        "effective_serving_mode": _mode,
        "effective_serving_mode_basis": _basis,
        "local_serving_disabled": _local_off,
        "external_use_permitted": _external_allowed,   # W505 — a present key is not permission
        "ollama_online": ollama,
        # W326 — honest naming: these report ENV-VAR PRESENCE only, not a validated working key
        # (a present-but-invalid key still 401s at call time — the voice endpoints say so live).
        "openai_key_present": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_key_present": bool(os.getenv("ANTHROPIC_API_KEY")),
        "key_note": "presence of the env var only — validity is only known at call time",
    }


@router.get("/session/{session_id}/history")
async def get_history(session_id: str, user: dict | None = Depends(get_current_user)):
    # §17.5 invariant 1 (W350) — owner-scoped read (any caller could previously read any
    # user's full conversation, message previews included)
    session = _require_session_access(session_id, user)
    return {"session_id": session_id, "history": session["history"]}


@router.get("/sessions", response_model=List[SessionSummary])
async def list_sessions(user: dict | None = Depends(get_current_user)):
    """Lists the CALLER's active avatar conversation sessions (owner-scoped, W350 — the listing
    previously exposed every user's sessions with message previews to anonymous callers). Real,
    live, in-memory data — resets on server restart, no fabricated entries."""
    from agentic_core.auth.core import user_can_access
    _u = user if isinstance(user, dict) else None
    summaries: List[SessionSummary] = []
    for sid, data in _sessions.items():
        if not user_can_access(_u, data.get("owner_id")):
            continue
        history: List[Dict[str, str]] = data["history"]
        last_message = history[-1]["content"] if history else None
        summaries.append(SessionSummary(
            session_id=sid,
            avatar_id=data["avatar"].avatar_id,
            context=data.get("context", "general"),
            message_count=len(history),
            last_message=last_message,
        ))
    summaries.sort(key=lambda s: s.message_count, reverse=True)
    return summaries


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Real Whisper transcription — the labelled EXTERNAL accelerant: requires BOTH a working
    OpenAI key AND the explicit AI_ALLOW_EXTERNAL opt-in (§6, W335 — key presence alone
    previously shipped the user's voice recording externally with the flag off). The in-house
    default is browser-native Web Speech in the client (W325)."""
    from agentic_core.ai.native.model_resource import external_allowed
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or not external_allowed():
        raise HTTPException(status_code=503, detail=(
            "External voice transcription is unavailable: requires a configured OPENAI_API_KEY "
            "AND AI_ALLOW_EXTERNAL=true (Owner-gated). The browser's own speech recognition is "
            "the in-house path — nothing was sent externally."))
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=openai_key)
        audio_bytes = await file.read()
        transcript = await client.audio.transcriptions.create(
            model="whisper-1",
            file=(file.filename or "audio.webm", audio_bytes),
        )
        return {"text": transcript.text}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Voice transcription backend unavailable: {str(e)[:200]}")


@router.post("/speak")
async def speak(request: SpeakRequest):
    """Real TTS — the labelled EXTERNAL accelerant: requires BOTH a working OpenAI key AND the
    explicit AI_ALLOW_EXTERNAL opt-in (§6, W335). The in-house default is browser-native
    speechSynthesis in the client (W325). Returns raw MP3 audio bytes."""
    from agentic_core.ai.native.model_resource import external_allowed
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or not external_allowed():
        raise HTTPException(status_code=503, detail=(
            "External voice output is unavailable: requires a configured OPENAI_API_KEY AND "
            "AI_ALLOW_EXTERNAL=true (Owner-gated). The browser's speechSynthesis is the in-house "
            "path — nothing was sent externally."))
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=openai_key)
        audio_resp = await client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=request.text[:4000],
        )
        return Response(content=audio_resp.content, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Voice output backend unavailable: {str(e)[:200]}")
