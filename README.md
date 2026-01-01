# Rudra — Intelligent Voice Assistant 🧠🎙️

Rudra is a modular, Python-based intelligent voice assistant designed to run reliably on Linux systems.
The project is built step-by-step with a strong emphasis on architecture, stability, and extensibility, rather than quick or fragile features.

The long-term vision is to evolve Rudra into an offline-first, algorithm-driven AI assistant, capable of system control, memory, and natural interaction across devices.

## 🔖 Project Status

Current Stable Milestone: ✅ Day 12 — Argument Extraction & Safe System Control

Day 12 completes Rudra’s action execution pipeline, making system commands contextual, validated, and confidence-gated.

✔ Argument extraction for system commands
✔ Intent → Argument → Action flow
✔ Confidence-based execution gating
✔ Safe rejection of ambiguous commands
✔ MySQL persistence restored & verified
✔ .env loading hardened for production

🔒 Day 12 is complete, tested, and locked.

## 🚀 Features (Implemented)
### ✅ Core Assistant

Enum-driven intent-based command processing

Modular NLP pipeline (no hardcoded logic)

Short-term & long-term conversational memory

MySQL-backed persistent storage

Clean separation of concerns

Predictable, debuggable execution flow

### ✅ Input System (Day 8)

Voice input using Google Speech Recognition

Text input fallback

Push-to-talk (press ENTER to speak)

Configurable input mode (voice / text)

Controlled listening (no always-on microphone)

### ✅ Input Intelligence (Day 9)

Input normalization & validation gate

Minimum-length and word-count filtering

Repeat suppression (only for previously accepted inputs)

Confidence refinement after intent scoring

Safe handling of unknown intents

Clear retry prompts (no infinite loops)

### ✅ Active Listening & Silence Handling (Day 9)

Listening state machine (IDLE → ACTIVE → WAITING)

Automatic silence detection

Context-aware prompts:

“I’m listening.”

“Going to sleep.”

No accidental intent execution during silence

Natural conversational pacing

### ✅ System Actions (Day 10)

Enum-driven Intent → Action abstraction

Centralized system execution layer

Linux-safe application launching

Terminal launch hardened (Snap / GLIBC safe)

No direct OS access from NLP or skills

Strict OS boundary enforcement

### ✅ Argument Extraction & Action Gating (Day 12)

Context-aware argument extraction:

URLs

File paths

Directories

Search queries

Validation before execution

Confidence-based execution gate:

High confidence → execute

Ambiguous → reject safely

Low confidence → request rephrase

Deterministic behavior (no guessing)

### ✅ Stability, Persistence & Logging

Structured logging using Loguru

Detailed debug traces for:

Input validation

Intent scoring

Confidence decisions

Argument extraction

Action execution

Graceful handling of speech, microphone, and OS errors

Secure .env usage (never committed)

Explicit .env loading for production reliability

## 🧠 Project Architecture
core/
├── main.py                  # Entry point
├── assistant.py             # Main assistant loop (state-driven)
├── input_controller.py      # Centralized input handling
│
├── input/
│   └── input_validator.py   # Input intelligence & repeat control
│
├── speech/
│   └── google_engine.py     # Google Speech Recognition engine
│
├── nlp/
│   ├── normalizer.py        # Text normalization
│   ├── tokenizer.py         # Tokenization
│   ├── intent.py            # Intent enum definitions
│   └── argument_extractor.py# Day 12 argument extraction
│
├── intelligence/
│   ├── intent_scorer.py     # Rule-based intent scoring
│   └── confidence_refiner.py
│
├── actions/
│   └── action_executor.py   # Confidence-gated execution layer
│
├── skills/
│   ├── basic.py             # Non-system skills
│   └── system_actions.py    # System action handlers
│
├── context/
│   ├── short_term.py        # Session memory
│   └── long_term.py         # Persistent memory (MySQL)
│
├── storage/
│   ├── mysql.py             # Database connection
│   └── models.py            # DB models

## 🛠️ Tech Stack

Language: Python 3.10+

Speech Engine: Google Speech Recognition

Database: MySQL

ORM: SQLAlchemy

Logging: Loguru

OS Target: Linux (Ubuntu tested)

## ▶️ Running the Assistant
### Activate virtual environment
```bash
source venv/bin/activate
```

### Run Rudra
```bash
python3 -m core.main
```

Usage

Press ENTER → speak

Say commands naturally (e.g., open browser github)

Silence is handled automatically

Say exit rudra to quit

## 🧭 Roadmap (High Level)

Day 13–14: Follow-up context (“open it”, “do that again”)

Day 15–25: Advanced skills & workflows

Day 26–40: Memory intelligence & personalization

Day 41–60: Offline intent engine & algorithms

Day 61–70: Multi-device sync & Raspberry Pi build

## 📌 Philosophy

Rudra is not built to demo quickly —
it is built to last, scale, and evolve.

Every feature must be:

Predictable

Debuggable

Extendable

Safe to modify later

No shortcuts. No magic. No fragile abstractions.

## 📜 License

This project is currently for learning, research, and portfolio purposes.
License will be finalized once the core system stabilizes.

Author: Ankesh
Project: Rudra — Intelligent Voice Assistant