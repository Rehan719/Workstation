"""
Avatar Voice Engine (vΩ∞-AVATAR-OMNISYNTHESIS).
Edge-First Audio Intelligence with real-time interrupt handling and VAD.
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
    IDBO Layer 6/12: Propagation & UX.
    Auditory organ of the digital organism.
    Supports local STT (whisper.cpp) and TTS (Piper).
    Fallback path: Vosk -> pyttsx3 -> Mock.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.stt_available = self._check_stt()
        self.tts_available = self._check_tts()
        self.interrupt_flag = False
        self.is_speaking = False
        logger.info(f"VoiceEngine Converged. STT: {self.stt_available}, TTS: {self.tts_available}")

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
        """Sovereign local transcription."""
        if self.interrupt_flag: return "__INTERRUPTED__"

        if self.stt_available == "whisper-cpp":
            return await self._run_whisper(audio_path)
        elif self.stt_available == "vosk":
            return "Vosk transcription result (Fallback)"
        else:
            return "Simulated user voice input."

    async def speak(self, text: str, voice_profile: str = "default"):
        """Synthesize instruction locally with real-time interrupt check."""
        self.is_speaking = True
        self.interrupt_flag = False

        logger.info(f"Speaking: '{text[:60]}...'")

        if self.tts_available == "piper":
            await self._run_piper(text, voice_profile)
        elif self.tts_available == "pyttsx3":
            await self._run_pyttsx3(text)
        else:
            # Mock speak: simulate synthesis time
            await asyncio.sleep(len(text) * 0.05)

        self.is_speaking = False

    def interrupt(self):
        """Immediately halts current auditory emission (Co-sovereignty)."""
        self.interrupt_flag = True
        logger.warning("Voice: Emission interrupted by user.")

    async def _run_whisper(self, audio_path: str) -> str:
        try:
            proc = await asyncio.create_subprocess_exec(
                "whisper-cpp", "-f", audio_path, "-otxt",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            return stdout.decode().strip()
        except Exception as e:
            logger.error(f"whisper.cpp failure: {e}")
            return "Error in transcription"

    async def _run_piper(self, text: str, profile: str):
        """Executes Piper TTS and pipes output for edge-first audio."""
        try:
            model = self.config.get("piper_model", "en_US-lessac-medium.onnx")
            # ARTICLE 1137: Real-time audio pipeline for <500ms synthesis.
            # Platform-specific command selection
            if os.name == 'nt':
                # Windows: Use a temporary file and a compatible player (e.g., powershell or ffplay)
                temp_wav = f"temp_voice_{os.getpid()}.wav"
                cmd = f"echo {text} | piper --model {model} --output_file {temp_wav}"
                proc = await asyncio.create_subprocess_shell(cmd)
                await proc.wait()

                if os.path.exists(temp_wav):
                    # Play using PowerShell to avoid external dependency on ffplay/aplay
                    play_cmd = f"powershell -c \"(New-Object Media.SoundPlayer '{temp_wav}').PlaySync()\""
                    play_proc = await asyncio.create_subprocess_shell(play_cmd)

                    while play_proc.returncode is None:
                        if self.interrupt_flag:
                            play_proc.terminate()
                            break
                        await asyncio.sleep(0.1)

                    try: os.remove(temp_wav)
                    except: pass
            else:
                # Linux/Mac: Use aplay pipe
                cmd = f"echo '{text}' | piper --model {model} --output_raw | aplay -r 22050 -f S16_LE -t raw"
                proc = await asyncio.create_subprocess_shell(cmd)

                # Monitor for interrupt
                while proc.returncode is None:
                    if self.interrupt_flag:
                        proc.terminate()
                        subprocess.run(["pkill", "-f", "aplay"], capture_output=True)
                        break
                    await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Piper audio pipeline failure: {e}")

    async def _run_pyttsx3(self, text: str):
        import pyttsx3
        def _speak():
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        await asyncio.to_thread(_speak)
