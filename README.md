Rudra — Intelligent Voice Assistant

Rudra is a modular, Python-based intelligent voice assistant designed to run reliably on Linux systems.
The project is built step-by-step with a strong focus on architecture, stability, and extensibility, rather than quick features.

Current implementation uses Google Speech Recognition for accurate voice input, with a long-term goal of becoming an offline-first, algorithm-driven assistant.

📌 Project Status

Current stable milestone: ✅ Day 9 (Stable)

Day 9 focuses entirely on input intelligence, stability, and conversational reliability.

✔ Robust input validation
✔ Confidence-based intent gating
✔ Active listening with silence handling
✔ Repeat-safe retry logic
✔ Stable conversation loop

Action-based system control begins from Day 10.

🚀 Features (Implemented)
✅ Core Assistant

Intent-based command processing

Modular NLP pipeline

Short-term & long-term memory

MySQL-backed persistent storage

Clean separation of concerns

✅ Input System (Day 8)

Voice input using Google Speech Recognition

Text input fallback

Push-to-talk (press ENTER to speak)

Configurable input mode (voice / text)

Controlled listening (no always-on mic)

✅ Input Intelligence (Day 9)

Input normalization & validation

Rejection of weak, noisy, or partial input

Confidence scoring & refinement

Safe retry handling (no accidental blocking)

Explicit handling of unknown intents

✅ Active Listening (Day 9)

Listening states: idle, active, waiting

Silence-aware behavior

Automatic sleep on repeated silence

Natural conversation flow (no mic lock)

✅ Stability & Logging

Structured logging with Loguru

Graceful handling of speech errors

Environment-variable based configuration

Safe .env usage (never committed)

🧠 Architecture Overview

Rudra follows a layered, deterministic pipeline:

Input
 ↓
Normalization & Validation
 ↓
Tokenization
 ↓
Intent Scoring
 ↓
Confidence Refinement
 ↓
Skill Execution
 ↓
Memory Update


Each layer is independent, testable, and replaceable.

🗂️ Project Structure
core/
├── assistant.py            # Main assistant loop
├── main.py                 # Entry point
├── config.py               # Input configuration
├── input_controller.py     # Centralized input handling
│
├── input/
│ └── input_validator.py    # Input validation & retry logic
│
├── speech/
│ └── google_engine.py      # Google Speech Recognition
│
├── nlp/
│ ├── tokenizer.py
│ ├── normalizer.py
│ └── intent.py
│
├── intelligence/
│ ├── intent_scorer.py
│ └── confidence_refiner.py
│
├── skills/
│ └── basic.py
│
├── context/
│ ├── short_term.py
│ └── long_term.py
│
├── storage/
│ ├── mysql.py
│ └── models.py

▶️ How to Run
Requirements

Python 3.10+

MySQL (running locally)

Linux OS

Working microphone

Run Command
python3 -m core.main

🛠️ Configuration

Sensitive values are stored in .env

.env is never committed

MySQL credentials and speech settings are configurable

🧭 Roadmap
Upcoming

Day 10 — Action-based intents (system commands)

Day 11 — Contextual multi-step commands

Day 12+ — Memory intelligence improvements

Long-Term Vision

Offline-first intelligence

Algorithmic & ML-based intent engine

Multi-device sync

Android & Raspberry Pi support

Alexa/Siri-class assistant behavior

🏷️ Milestones

day-8-stable — Input system & voice pipeline

day-9-stable — Input intelligence & active listening

📄 License

This project is under active development and intended for learning, research, and portfolio use.