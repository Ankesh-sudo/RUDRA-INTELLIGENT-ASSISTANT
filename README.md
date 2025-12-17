# Rudra — Intelligent Voice Assistant

Rudra is a modular, Python-based intelligent voice assistant designed to work reliably on Linux systems.  
The project is built step-by-step with a strong focus on **architecture, stability, and extensibility**.

Current implementation uses **Google Speech Recognition** for accurate voice input, with future plans for hybrid and offline support.

---

## 🚀 Features (Implemented)

### ✅ Core Assistant
- Intent-based command processing
- Modular NLP pipeline
- Short-term & long-term memory
- MySQL-backed persistent storage
- Clean separation of concerns

### ✅ Input System (Day 8)
- Voice input using **Google Speech Recognition**
- Text input fallback
- **Push-to-talk** (press ENTER to speak)
- Configurable input mode (voice / text)
- Controlled listening (no always-on mic)

### ✅ Stability & Logging
- Structured logging with Loguru
- Graceful handling of speech errors
- Environment-variable based configuration
- Safe `.env` usage (not committed)

---

## 🧠 Project Architecture

core/
├── assistant.py # Main assistant loop
├── main.py # Entry point
├── config.py # Input configuration
├── input_controller.py # Centralized input handling
│
├── speech/
│ └── google_engine.py # Google Speech Recognition
│
├── nlp/
│ ├── tokenizer.py
│ ├── normalizer.py
│ ├── intent.py
│
├── intelligence/
│ └── intent_scorer.py
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


