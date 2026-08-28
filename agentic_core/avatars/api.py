"""
Avatar Interaction API — the real, working multimodal user-interaction layer for
the Workstation avatar widget.

Note on scope: this module deliberately does NOT route through
`agentic_core/avatars/core/recirculation_orchestrator.py` (the "metabolic cycle"
architecture). That orchestrator instantiates cleanly but fails on its very first
execution stage — its nine-engine cognitive registry was never actually populated
with working engines — so building on it would mean shipping another broken layer.
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

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response
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
    image_understood: bool = False
    image_served_by: Optional[str] = None  # which resource analysed the image: "ollama" (in-house) | "openai" | None
    image_is_external: bool = False        # honest: was the image sent to an external provider?
    context: str
    served_by: str = "native"          # which OWNED resource answered the TEXT (in-house-first provenance)
    is_external: bool = False
    grounded_in: Optional[str] = None  # the vsb_id the answer was grounded in, if any
    language: Optional[str] = None     # the language the answer was requested in (echoed back)
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
                live.append(f"- Economy (virtual WST): {reg.get('operating_cycles', 0)} operating cycles"
                            + (f", last distributable {reg.get('last_distributable')} WST"
                               if reg.get("last_distributable") is not None else "")
                            + (f" — HELD ({reg.get('last_hold')})" if reg.get("last_hold") else ""))
        except Exception:
            pass
        try:
            from agentic_core.config import data_path, load_json_tolerant
            comp = (load_json_tolerant(data_path("vsb_compliance_history.json"), {}) or {}).get(vsb_id) or {}
            if comp.get("overall"):
                live.append(f"- Latest §11 compliance screen: {comp['overall']}"
                            + (" (REGRESSION)" if comp.get("regression") else ""))
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


def _get_or_create_session(session_id: Optional[str], user_id: str = "demo_user") -> str:
    if session_id and session_id in _sessions:
        return session_id
    new_id = session_id or str(uuid.uuid4())
    avatar_id = f"did:workstation:{uuid.uuid4().hex[:16]}"
    state = AvatarState(avatar_id=avatar_id, user_id=user_id)
    state.state_checksum = state.compute_state_hash()
    _sessions[new_id] = {"avatar": state, "history": [], "context": "general"}
    return new_id


@router.post("/session", response_model=AvatarSession)
async def create_session():
    """Creates a new avatar identity + conversation session."""
    session_id = _get_or_create_session(None)
    session = _sessions[session_id]
    return AvatarSession(
        session_id=session_id,
        avatar_id=session["avatar"].avatar_id,
        state_checksum=session["avatar"].state_checksum,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Real text (and, when a multimodal key is available, image-aware) chat turn."""
    session_id = _get_or_create_session(request.session_id)
    session = _sessions[session_id]
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
        if vision_out:
            image_note = vision_out
            image_understood = True
            image_served_by = "ollama"
            image_is_external = False
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
                except Exception as e:
                    image_served_by = "openai"
                    image_note = f"(Image attached but could not be analysed: vision backend unavailable — {str(e)[:150]})"
            elif openai_key and not external_allowed():
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
    prompt = (
        f"{domain_prompt}{grounding}\n\n"
        f"{lang_instr}"
        f"{f'Conversation so far:\n{history_block}\n\n' if history_block else ''}"
        f"{f'Image analysis: {image_note}\n\n' if image_note else ''}"
        f"User: {request.message}"
    )

    # In-house-first via the native fabric — always answers (native floor) and reports which
    # OWNED resource served it; bounded so the avatar stays responsive.
    meta = await gateway.query_meta(prompt, agent=f"avatar:{request.context}", timeout=20.0)
    response_text = meta.get("output", "")

    history.append({"role": "user", "content": request.message})
    history.append({"role": "assistant", "content": response_text})
    memory_v01.add_exchange(f"AVATAR[{request.context}]: {request.message}", response_text)

    return ChatResponse(
        session_id=session_id,
        response=response_text,
        image_understood=image_understood,
        image_served_by=image_served_by,
        image_is_external=image_is_external,
        context=request.context,
        served_by=meta.get("served_by", "native"),
        is_external=bool(meta.get("is_external")),
        # §9 (W325) — HONEST: grounded_in is asserted only when a grounding block actually built
        # (previously the request's vsb_id was echoed back even for a missing entity).
        grounded_in=(request.vsb_id if grounding else None),
        # W326 — language reports what was HONOURED: the deterministic floor cannot translate,
        # so a requested language served by the floor is not echoed back as an achievement.
        language=((lang or None) if ((not lang_instr) or meta.get("served_by", "native") != "native")
                  else None),
        suggested_areas=_suggest_areas(request.message),
    )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Clears a session's conversation history and removes it from memory."""
    if session_id in _sessions:
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
    return {
        "online": True,                 # native fabric guarantees the avatar always answers
        "posture": "in-house-first",
        "native": True,
        "ollama_online": ollama,
        # W326 — honest naming: these report ENV-VAR PRESENCE only, not a validated working key
        # (a present-but-invalid key still 401s at call time — the voice endpoints say so live).
        "openai_key_present": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_key_present": bool(os.getenv("ANTHROPIC_API_KEY")),
        "key_note": "presence of the env var only — validity is only known at call time",
    }


@router.get("/session/{session_id}/history")
async def get_history(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "history": session["history"]}


@router.get("/sessions", response_model=List[SessionSummary])
async def list_sessions():
    """Lists all currently active avatar conversation sessions. Real, live,
    in-memory data — resets on server restart, no fabricated entries."""
    summaries: List[SessionSummary] = []
    for sid, data in _sessions.items():
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
