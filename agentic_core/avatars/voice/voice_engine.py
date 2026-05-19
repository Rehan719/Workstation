"""
Edge-First Voice Engine.
Local STT/TTS with sovereign fallback architecture.
"""
import shutil
import subprocess
import logging
import os
import asyncio
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class VoiceEngine:
    """
    IDBO Layer 12: User Experience / Auditory organ.
    Listens via local STT (whisper.cpp), speaks via local TTS (Piper).
    Fallback path: Vosk -> pyttsx3 -> Mock.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.stt_available = self._check_stt()
        self.tts_available = self._check_tts()
        logger.info(f"VoiceEngine Initialized. STT: {self.stt_available}, TTS: {self.tts_available}")

    def _check_stt(self) -> str:
        """Sovereign availability check for STT engines."""
        if shutil.which("whisper-cpp"): return "whisper-cpp"
        if shutil.which("vosk-transcriber"): return "vosk"
        return "mock"

    def _check_tts(self) -> str:
        """Sovereign availability check for TTS engines."""
        if shutil.which("piper"): return "piper"
        try:
            import pyttsx3
            return "pyttsx3"
        except ImportError:
            return "mock"

    async def transcribe(self, audio_path: str) -> str:
        """Transcribe user voice to text sovereignly."""
        if self.stt_available == "whisper-cpp":
            return await self._run_whisper(audio_path)
        elif self.stt_available == "vosk":
            return await self._run_vosk(audio_path)
        else:
            logger.warning("Voice: STT fallback to mock.")
            return "Simulated user input text."

    async def speak(self, text: str, voice_profile: str = "default"):
        """Synthesize instruction to speech locally."""
        logger.info(f"Voice: Speaking ({self.tts_available}) -> '{text[:50]}...'")

        if self.tts_available == "piper":
            await self._run_piper(text, voice_profile)
        elif self.tts_available == "pyttsx3":
            await self._run_pyttsx3(text)
        else:
            logger.info(f"MOCK SPEAK: {text}")

    async def _run_whisper(self, audio_path: str) -> str:
        """Execute whisper.cpp via subprocess."""
        try:
            # -f (file), -otxt (output text to stdout)
            proc = await asyncio.create_subprocess_exec(
                "whisper-cpp", "-f", audio_path, "-otxt",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            return stdout.decode().strip()
        except Exception as e:
            logger.error(f"whisper.cpp execution failure: {e}")
            return "Error in transcription"

    async def _run_vosk(self, audio_path: str) -> str:
        """Execute Vosk CLI fallback."""
        return "Vosk transcription result (Stub)"

    async def _run_piper(self, text: str, profile: str):
        """Execute Piper ONNX TTS via subprocess."""
        try:
            model = self.config.get("piper_model", "en_US-lessac-medium.onnx")
            cmd = f"echo '{text}' | piper --model {model} --output_raw"
            # Using shell=True for simple piping, or could use Popen
            proc = await asyncio.create_subprocess_shell(cmd)
            await proc.wait()
        except Exception as e:
            logger.error(f"Piper execution failure: {e}")

    async def _run_pyttsx3(self, text: str):
        """Execute system TTS fallback (blocking wrapper)."""
        import pyttsx3
        # Wrap in thread to avoid blocking event loop
        def _speak():
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        await asyncio.to_thread(_speak)
