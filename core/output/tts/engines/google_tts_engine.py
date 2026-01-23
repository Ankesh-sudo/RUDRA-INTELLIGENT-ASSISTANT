import os
import uuid
from typing import Union

from google.cloud import texttospeech

from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_contract import FinalizedText


class GoogleTTSEngine(TTSEngine):
    """
    Google Cloud Text-to-Speech engine.

    🔒 Invariants:
    - Output-only (no logic, no intent access)
    - Finalized text only
    - Fail-closed (errors produce silence)
    - Temporary production backend
    """

    def __init__(
        self,
        language_code: str,
        voice_name: str,
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
    ):
        self.language_code = language_code
        self.voice_name = voice_name
        self.speaking_rate = speaking_rate
        self.pitch = pitch

        # Client init may raise if credentials missing;
        # allow it to propagate once, then fail-closed at runtime.
        self.client = texttospeech.TextToSpeechClient()

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def speak(self, text: Union[FinalizedText, str]) -> None:
        """
        Speak finalized text.

        Accepts:
        - FinalizedText (preferred)
        - str (compatibility; wrapped internally)

        Failure => silent no-op.
        """

        try:
            final_text = (
                text.text if isinstance(text, FinalizedText) else str(text)
            ).strip()

            if not final_text:
                return  # nothing to say

            synthesis_input = texttospeech.SynthesisInput(
                text=final_text
            )

            voice = texttospeech.VoiceSelectionParams(
                language_code=self.language_code,
                name=self.voice_name,
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate=self.speaking_rate,
                pitch=self.pitch,
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )

            out_dir = "runtime_tts"
            os.makedirs(out_dir, exist_ok=True)

            out_path = os.path.join(
                out_dir,
                f"google_tts_{uuid.uuid4().hex}.wav",
            )

            with open(out_path, "wb") as f:
                f.write(response.audio_content)

            # 🔒 Fire-and-forget playback (never blocks core)
            os.system(f"aplay '{out_path}' >/dev/null 2>&1 &")

        except Exception:
            # 🔒 FAIL-CLOSED: silence is always safe
            return
