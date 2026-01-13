import os
import csv
import wave
import contextlib
import sys

# =========================
# CONFIGURATION (LOCKED)
# =========================

MIN_FILES = 50
REQUIRED_RATE = 22050
MAX_DURATION = 12.0

# ---- DEV MODE SWITCH ----
DEV_MODE = True  # ⚠️ MUST BE False BEFORE DAY 50 VOICE FREEZE

DEV_MIN_DURATION = 1.0
PROD_MIN_DURATION = 3.0


# =========================
# VALIDATION LOGIC
# =========================

def validate_dataset(path: str) -> bool:
    wav_dir = os.path.join(path, "wav")
    meta_path = os.path.join(path, "metadata.csv")

    errors = []
    checked = 0

    if not os.path.isdir(wav_dir):
        print(f"[FAIL] Missing wav directory: {wav_dir}")
        return False

    if not os.path.isfile(meta_path):
        print(f"[FAIL] Missing metadata.csv: {meta_path}")
        return False

    with open(meta_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if len(rows) < MIN_FILES:
        errors.append(f"Only {len(rows)} metadata rows (min {MIN_FILES})")

    min_duration = DEV_MIN_DURATION if DEV_MODE else PROD_MIN_DURATION
    mode_label = "DEV" if DEV_MODE else "PROD"

    for row in rows:
        filename = row["filename"]
        wav_path = os.path.join(wav_dir, filename)

        if not os.path.isfile(wav_path):
            errors.append(f"{filename}: file missing")
            continue

        with contextlib.closing(wave.open(wav_path, "rb")) as wf:
            channels = wf.getnchannels()
            rate = wf.getframerate()
            frames = wf.getnframes()
            duration = frames / float(rate)

            if channels != 1:
                errors.append(f"{filename}: not mono")

            if rate != REQUIRED_RATE:
                errors.append(f"{filename}: wrong sample rate ({rate})")

            if not (min_duration <= duration <= MAX_DURATION):
                errors.append(
                    f"{filename}: duration {duration:.2f}s "
                    f"(min {min_duration}s, mode={mode_label})"
                )

        checked += 1

    if errors:
        print(f"\n[FAIL] {path}")
        for err in errors:
            print("  -", err)
        print(f"\nChecked {checked} files")
        return False

    print(f"[OK] {path} dataset valid ({checked} files)")

    if DEV_MODE:
        print("⚠️  DATASET RUNNING IN DEV MODE — NOT ALLOWED FOR VOICE FREEZE")

    return True


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    base = "data/voices"

    ok_female = validate_dataset(os.path.join(base, "maahi_female"))
    ok_male = validate_dataset(os.path.join(base, "rudra_male"))

    if ok_female and ok_male:
        print("DATASET STATUS: VALID")
        sys.exit(0)
    else:
        print("DATASET STATUS: INVALID")
        sys.exit(1)
