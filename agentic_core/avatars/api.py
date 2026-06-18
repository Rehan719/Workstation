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

Voice transcription (STT), voice output (TTS), and image understanding all require
a working OpenAI (or other multimodal) API key — currently neither the configured
OPENAI_API_KEY (invalid) nor GOOGLE_API_KEY (valid but IP-restricted in Cloud
Console, blocking this server's outbound IP) works from this environment. Those
endpoints are wired for real against the OpenAI client and will start working the
moment a valid, unrestricted key is available — no other code changes needed.
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


class ChatResponse(BaseModel):
    session_id: str
    response: str
    image_understood: bool = False
    context: str


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
    if request.image_base64:
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
            except Exception as e:
                image_note = f"(Image attached but could not be analyzed: vision backend unavailable — {str(e)[:150]})"
        else:
            image_note = "(Image attached but no working vision-capable API key is configured, so it could not be analyzed.)"

    history_block = "\n".join(f"{h['role']}: {h['content']}" for h in history[-10:])
    prompt = (
        f"{domain_prompt}\n\n"
        f"{f'Conversation so far:\n{history_block}\n\n' if history_block else ''}"
        f"{f'Image analysis: {image_note}\n\n' if image_note else ''}"
        f"User: {request.message}"
    )

    response_text = await gateway.query(prompt, agent=f"avatar:{request.context}")

    history.append({"role": "user", "content": request.message})
    history.append({"role": "assistant", "content": response_text})
    memory_v01.add_exchange(f"AVATAR[{request.context}]: {request.message}", response_text)

    return ChatResponse(
        session_id=session_id,
        response=response_text,
        image_understood=image_understood,
        context=request.context,
    )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Clears a session's conversation history and removes it from memory."""
    if session_id in _sessions:
        del _sessions[session_id]
    return {"cleared": True, "session_id": session_id}


@router.get("/status")
async def ai_status():
    """Quick health check: probes Ollama and reports AI availability."""
    import httpx as _httpx
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    base_url = ollama_url.rsplit("/api/", 1)[0]
    try:
        async with _httpx.AsyncClient(timeout=4.0) as client:
            r = await client.get(f"{base_url}/api/tags")
            online = r.status_code == 200
    except Exception:
        online = False
    return {
        "ollama_online": online,
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
