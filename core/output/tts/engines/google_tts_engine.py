from google.cloud import texttospeech
from core.output.tts.tts_engine import TTSEngine
from core.output.tts.tts_contract import FinalizedText
import uuid
import os


class GoogleTTSEngine(TTSEngine):
    """
    Google Cloud Text-to-Speech engine.
    Temporary production backend.
    Final-text-only. No logic or persona influence.
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

        self.client = texttospeech.TextToSpeechClient()

    def speak(self, text: FinalizedText) -> None:
        synthesis_input = texttospeech.SynthesisInput(
            text=text.text
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
            out_dir, f"google_tts_{uuid.uuid4().hex}.wav"
        )

        with open(out_path, "wb") as f:
            f.write(response.audio_content)

        # 🔒 Play via OS default (pure side-effect)
        os.system(f"aplay '{out_path}' >/dev/null 2>&1 &")
