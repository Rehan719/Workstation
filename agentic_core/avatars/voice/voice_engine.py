import shutil
import subprocess
import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class VoiceEngine:
    """
    Edge-first Voice Engine: local STT/TTS with system-level fallbacks.
    STT: whisper.cpp -> Vosk -> Mock
    TTS: Piper -> pyttsx3 -> Mock
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.stt_available = self._check_stt()
        self.tts_available = self._check_tts()

    def _check_stt(self) -> str:
        if shutil.which("whisper-cpp"): return "whisper-cpp"
        if shutil.which("vosk-transcriber"): return "vosk"
        return "mock"

    def _check_tts(self) -> str:
        if shutil.which("piper"): return "piper"
        try:
            import pyttsx3
            return "pyttsx3"
        except ImportError:
            return "mock"

    async def transcribe(self, audio_path: str) -> str:
        """Transcribe audio to text."""
        if self.stt_available == "whisper-cpp":
            return self._run_whisper(audio_path)
        elif self.stt_available == "vosk":
            return self._run_vosk(audio_path)
        else:
            logger.warning("Voice: STT unavailable, using mock transcription.")
            return "Mock transcription of user voice."

    async def speak(self, text: str, voice_profile: str = "default"):
        """Synthesize text to speech."""
        logger.info(f"Voice: Speaking '{text}' using {self.tts_available}")
        if self.tts_available == "piper":
            self._run_piper(text, voice_profile)
        elif self.tts_available == "pyttsx3":
            self._run_pyttsx3(text)
        else:
            logger.info(f"MOCK SPEAK: {text}")

    def _run_whisper(self, audio_path: str) -> str:
        # Simplified CLI call
        try:
            result = subprocess.run(
                ["whisper-cpp", "-f", audio_path, "-otxt"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"whisper.cpp failure: {e}")
            return "Error in transcription"

    def _run_piper(self, text: str, profile: str):
        try:
            # Simplified CLI call
            model = self.config.get("piper_model", "en_US-lessac-medium.onnx")
            cmd = f"echo '{text}' | piper --model {model} --output_raw"
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            logger.error(f"Piper failure: {e}")

    def _run_pyttsx3(self, text: str):
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
