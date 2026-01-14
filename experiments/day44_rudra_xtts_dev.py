from TTS.api import TTS
import os

OUTPUT_DIR = "experiments/output/generic_hindi"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("Loading XTTS generic multilingual model...")
    tts = TTS(
        model_name="tts_models/multilingual/multi-dataset/xtts_v2",
        gpu=False
    )

    text = "नमस्ते बॉस, यह एक अस्थायी हिंदी आवाज़ है।"
    out_path = os.path.join(OUTPUT_DIR, "generic_hindi.wav")

    tts.tts_to_file(
        text=text,
        file_path=out_path,
        language="hi"
    )

    print(f"Saved output to: {out_path}")

if __name__ == "__main__":
    main()
