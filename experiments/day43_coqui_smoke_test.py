from TTS.api import TTS
import os

OUTPUT_DIR = "experiments/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_NAME = "tts_models/en/ljspeech/tacotron2-DDC"

def main():
    print("Loading Coqui TTS model...")
    tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)

    text = "This is a basic offline text to speech test."
    out_path = os.path.join(OUTPUT_DIR, "day43_test.wav")

    print("Synthesizing...")
    tts.tts_to_file(text=text, file_path=out_path)

    print(f"Saved output to: {out_path}")
    print("DAY 43 BASE MODEL TEST SUCCESSFUL")

if __name__ == "__main__":
    main()
