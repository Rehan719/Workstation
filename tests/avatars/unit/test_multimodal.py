import pytest
from agentic_core.avatars.output.voice_engine import VoiceEngine
from agentic_core.avatars.output.multimodal_renderer import AvatarRenderer, MultimodalRenderer

@pytest.mark.asyncio
async def test_voice_engine_fallback():
    engine = VoiceEngine({})
    # Should fallback to mock if no binaries found
    assert engine.stt_available in ["whisper-cpp", "vosk", "mock"]
    text = await engine.transcribe("fake.wav")
    assert text is not None

@pytest.mark.asyncio
async def test_multimodal_render():
    voice = VoiceEngine({})
    renderer = AvatarRenderer({"type": "2d"})
    multi = MultimodalRenderer(voice, renderer)

    await multi.render("Hello world", "happy", [{"type": "checklist", "data": {"items": []}}])
    assert renderer.current_expression == "happy"
