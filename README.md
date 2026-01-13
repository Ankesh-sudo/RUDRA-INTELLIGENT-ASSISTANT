# Rudra — Intelligent Voice Assistant 🧠🎙️

Rudra is a **deterministic, modular, Python-based intelligent assistant framework** designed to run reliably on Linux systems.

It is **not** a quick-demo chatbot.
Rudra is engineered step-by-step with strict architectural rules, safety guarantees, and explainability at every layer.

The long-term vision is an **offline-first, algorithm-driven AI assistant** capable of system control, memory, and natural interaction across devices — without black boxes or silent authority.

---

## 🔖 Project Status

### ✅ Current Stable Milestone: **Day 38 — Voice Explainability Lock**

As of **Day 38**, Rudra’s **core reasoning, memory, persona, and voice layers are fully sealed and auditable**.

Voice (TTS) exists only as a **non-authoritative output channel** and is now **visible in explain traces** without influencing logic or text.

🔒 **All systems up to Day 38 are complete, tested, and hard-locked.**

---

## 🧱 What Is Completed (Day 1 → Day 38)

### 🧱 Phase 1 — Core Assistant Foundation (Day 1–7)
- Deterministic main loop
- Input validation → normalization
- Rule-based intent routing
- Action execution framework
- Global interrupt system (HARD / SOFT / IGNORE)
- Deterministic execution order
- Structured logging
- Test-first discipline

**Result:** No undefined paths. Fully auditable core.

---

### 🧠 Phase 2 — NLP & Intent Intelligence (Day 8–13)
- Tokenization & normalization
- Rule-based intent scoring (no ML)
- Best-intent selection
- Confidence calculation & refinement
- Slot extraction & merging
- Context-aware confidence adjustment
- Clarification loop
- Unknown-intent handling

**Result:** Explainable understanding. Zero black boxes.

---

### 🧠 Phase 3 — Short-Term Memory (Day 14–18)
- Working memory model
- STM lifecycle & eviction
- Context-pack builder
- Threshold-based recall
- Follow-up resolution
- Interrupt-safe lifecycle

**Result:** Conversational continuity without persistence risk.

---

### 🧠 Phase 4 — Long-Term Memory (Day 19–23)
- LTM schema
- Memory classification
- Promotion evaluator
- Explicit consent gate
- User approval flow
- Conflict detection & replacement
- No silent learning

**Result:** Ethical, user-owned memory only.

---

### 🔍 Phase 5 — Read-Only Memory Recall (Day 24)
- Deterministic recall APIs
- Category & confidence filters
- Exact vs contains matching
- Presentation-only formatting

**Result:** Memory is visible, not influential.

---

### 🔐 Phase 6 — Controlled Memory Usage (Day 25)
- Usage modes (OFF / ONCE / SESSION / SCOPED)
- Immutable permits
- Permit expiry
- Single guarded recall entry
- Usage trace
- `explain_last()` / `explain_all()`

**Result:** Memory affects behavior only with permission.

---

### 🧩 Phase 7 — Opt-In Memory Influence (Day 26)
- Influence contracts
- Immutable influence signals
- Deterministic influence gate
- Explain trace emission

**Result:** Influence exists architecturally but is inert.

---

### 🟦 Day 27–30 — Preference System (Final)
- Whitelisted preference schema
- Deterministic resolution
- Preview → confirm → apply enforcement
- Explicit scope & expiry
- Persona-safe boundary lock

**Result:** Preferences affect wording only. System permanently frozen.

---

### 🟦 Day 31–33 — Maahi Persona (Text-Only)
- Persona adapter & contract
- Semantic guard
- Suffix-only expressiveness
- Deterministic selection
- Affection Tier-A hard cap
- No memory, intent, or preference access

**Result:** Persona feels human but has zero authority.

---

### 🟦 Day 34–35 — TTS Architecture Lock
- Final-text-only TTS contract
- Abstract engine interface
- No-op engine
- Closed registry
- Interrupt-safe adapter
- Tests proving TTS cannot affect text

**Result:** Voice is optional, powerless, and replaceable.

---

### 🟦 Day 36–37 — Persona ↔ Voice Sealing
- Immutable PersonaProfile
- Fingerprinted persona identity
- FinalResponseEnvelope (sealed)
- Persona applied exactly once
- Voice consumes envelope only
- Removability safety proofs

**Result:** Persona and voice are fully isolated and non-evolving.

---

### 🟦 Day 38 — Voice Explainability
- TTS execution surfaced in explain traces
- Voice status: requested / skipped / failed / ok
- No control-flow or text impact

**Result:** Voice is explainable, not powerful.

---

## 🧠 Architecture Overview

```text
core/
├── main.py
├── assistant.py
├── input_controller.py
│
├── input/
├── speech/
├── nlp/
├── intelligence/
├── actions/
├── skills/
├── context/
├── influence/
├── persona/
├── tts/
├── explain/
└── tests/
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10 / 3.11
- **OS Target:** Linux (Ubuntu tested)
- **Speech Engine:** Google Speech Recognition
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Logging:** Loguru
- **Testing:** Pytest

---

## ▶️ Running Rudra

```bash
source venv/bin/activate
python3 -m core.main
```

---

## 🧭 Roadmap

- **Day 39–40:** Voice failure isolation & permanent freeze
- **Day 41–55:** Real assistant capabilities (OS control, automation, devices)
- **Day 56–70:** Safe, explainable learning & ML

Persona has **zero role** beyond presentation.

---

## 📌 Philosophy

Rudra is built for:
- Determinism
- Explainability
- Auditability
- Long-term evolution

No shortcuts.
No magic.
No silent decisions.

---

**Author:** Ankesh  
**Project:** Rudra — Intelligent Voice Assistant