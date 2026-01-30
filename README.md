# Rudra — Intelligent Voice & System Assistant 🧠🎙️🖥️

Rudra is a **deterministic, modular, Python-based intelligent assistant framework**
engineered for **reliability, safety, and explainability** on Linux systems.

This is **not** a demo chatbot.
Rudra is built step-by-step with **hard architectural contracts**, **explicit permissions**, and **zero silent authority**.

The long-term vision is an **offline-first, algorithm-driven assistant**
capable of **system control, memory, and natural interaction** — without black boxes.

---

## 🔖 Project Status

### ✅ Current Stable Milestone: **Day 61 — OS Control Stub & Execution Safety Lock**

As of **Day 61**, Rudra has reached a **major architectural stability milestone**:

- All core reasoning, memory, persona, voice, permissions, and execution layers are **sealed**
- OS-level control is **explicitly declared but non-executable**
- Every action path is **auditable, explainable, and test-covered**
- **136/136 tests passing**
- Project tagged as **most stable**

🔒 **All systems up to Day 61 are complete, tested, and frozen.**

---

## 🧱 What Is Completed (Day 1 → Day 61)

### 🧱 Phase 1 — Core Assistant Foundation (Day 1–7)
Deterministic main loop, intent routing, execution pipeline, interrupts, logging.

### 🧠 Phase 2 — Intent & Planning Core (Day 8–14)
Intent graph, chaining, multi-step planning, planner–executor contract.

### 🧠 Phase 3 — OS Action Model (Day 15–20)
Immutable ActionSpec, GuardedExecutor, risk levels, permission scopes.

### 🔐 Phase 4 — Permissions & Safety (Day 21–30)
PermissionEvaluator, explain surfaces, persona isolation and sealing.

### 🗣️ Phase 5 — Voice & TTS Safety (Day 31–41)
TTS contract, engine isolation, persona–voice sealing, explainable voice.

### 📁 Phase 6 — File Actions (Day 42–54)
Safe file intents, preview & confirmation, guarded execution.

### 🧭 Phase 7 — Confirmation & Control (Day 55–59)
YES/NO hooks, cancel, replay prevention, orchestrator hardening.

### 🚀 Phase 8 — App Actions (Day 60)
OPEN_APP integration with permission-gated live execution.

### 🛑 Phase 9 — OS Control Safety (Day 61)
OS_CONTROL declared, stubbed, never executed, contract enforced.

---

## 🧠 Architecture Overview

```
core/
├── assistant.py
├── main.py
├── input_controller.py
├── actions/
├── context/
├── explain/
├── intelligence/
├── memory/
├── nlp/
├── orchestrator/
├── os/
│   ├── action_spec.py
│   ├── control_capabilities.py
│   ├── executor/
│   │   ├── guarded_executor.py
│   │   └── os_control_stub.py
│   ├── linux/
│   └── permission/
├── persona/
├── response/
├── skills/
├── speech/
├── tts/
└── tests/
```

---

## 🛠️ Tech Stack

- Python 3.10 / 3.11
- Linux (Ubuntu tested)
- Google Speech Recognition
- MySQL + SQLAlchemy
- Pytest (136 tests)

---

## ▶️ Running Rudra

```bash
source venv/bin/activate
python3 -m core.main
```

---

## 📌 Philosophy

Deterministic. Explainable. Auditable.

No shortcuts.  
No magic.  
No silent decisions.

---

**Author:** Ankesh  
**Project:** Rudra — Intelligent Voice & System Assistant  
**Status:** Day 93 · Most Stable