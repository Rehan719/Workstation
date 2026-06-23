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
`image_is_external` so vision provenance is explicit. Voice STT/TTS (`/transcribe`, `/speak`) still
require an external key (browser-native voice is used client-side for the in-house path).
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
        return (
            "\n\nYou are THIS VSB's enterprise-aware avatar — ground every answer in its live state:\n"
            f"- VSB: {v.get('name')} (domain: {v.get('domain')}, stage: {v.get('stage')})\n"
            f"- Mission: {v.get('challenge', '')}\n"
            f"- Chief (owner digital twin): {chief}\n"
            f"- Entity type: {eco.get('entity_type', '')}\n"
            + (f"- {bp}\n" if bp else "")
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
            # Optional external accelerant — only if a key is configured (never a dependency).
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
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
                    image_is_external = True
                except Exception as e:
                    image_note = f"(Image attached but could not be analysed: vision backend unavailable — {str(e)[:150]})"
            else:
                # Honest: the image was received but NOT analysed — no fabricated description.
                image_note = ("(Image attached and received, but no in-house vision model (set OLLAMA_VISION_MODEL, "
                              "e.g. llava/llama3.2-vision) or external vision key is available, so its contents were not analysed.)")

    grounding = _vsb_grounding(request.vsb_id) if request.vsb_id else ""
    history_block = "\n".join(f"{h['role']}: {h['content']}" for h in history[-10:])
    prompt = (
        f"{domain_prompt}{grounding}\n\n"
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
        grounded_in=request.vsb_id,
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
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
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
    """Real Whisper transcription — requires a working OpenAI key."""
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise HTTPException(status_code=503, detail="Voice transcription requires a configured OPENAI_API_KEY.")
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
    """Real TTS — requires a working OpenAI key. Returns raw MP3 audio bytes."""
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise HTTPException(status_code=503, detail="Voice output requires a configured OPENAI_API_KEY.")
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
