# Silent Sentinel Edge AI – Strategic Sensemaking Core

**Target Platform:** NVIDIA Jetson Orin Nano (JetPack 6.x / 7.x)  
**Concept:** Edge implementation of a CDTFW-inspired strategic analysis pipeline for passive RF / local sensing systems.

This codebase turns the Center for Disruptive Technology and Future Warfare (CDTFW) “operating system” into runnable edge AI software.  
It helps Silent Sentinel (and related concepts such as CAM-Pulse + human-aligned intelligence) answer the central question at the tactical/operational edge:

> How can distributed, passive, locally intelligent sensor systems alter reconnaissance, force protection, signature management, command authority, adversarial countermeasures and escalation risk?

## Core Idea

Do **not** treat technology as an object.  
Study the **network of decisions, people, resources, vulnerabilities and consequences** that becomes possible around it.

The software implements the CDTFW pipeline on constrained edge hardware:

```
Sensor / RF / Local AI detections
         ↓
Questions derived from national strategy & operator intent
         ↓
Local expert modules + small LLM (human-aligned)
         ↓
Technology → Military meaning conversion
         ↓
Convergence analysis + four-direction evaluation
         ↓
Tactical / Operational / Strategic assessment
         ↓
Decision-advantage outputs (alerts, recommendations, risk flags)
         ↓
Human operator review (always in the loop)
```

## Key Modules

| Module | Purpose |
|--------|---------|
| `pipeline.py` | Orchestrates the full CDTFW-style flow |
| `four_questions.py` | Employment / Exploitation / Defeat / Governance analysis |
| `levels.py` | Strategic ↔ Operational ↔ Tactical translation |
| `convergence.py` | Multi-technology system-of-systems evaluation |
| `framework.py` | 9-question diagnostic for any organization or capability |
| `edge_llm.py` | Local LLM interface (Ollama / llama.cpp / TensorRT-LLM) optimized for Orin Nano |
| `sensor_ingest.py` | Placeholder for passive RF, CAM-Pulse style local sensing, YOLO detections, etc. |
| `human_aligned.py` | Ethics, escalation, authority and human-override checks |

## Hardware Notes (Jetson Orin Nano)

- **Memory:** Prefer 8 GB model. Keep models ≤ 4–7 B parameters (Q4/Q5).
- **Recommended local models:**
  - `qwen2.5:3b` or `llama3.2:3b` (fast)
  - `gemma2:2b` / `phi-3-mini` (very low resource)
  - `mistral:7b-instruct-q4` (higher quality, tighter fit)
- Install Ollama or use NVIDIA TensorRT-LLM / llama.cpp with CUDA.
- Power modes: Prefer 15 W or 25 W for sustained inference.
- Passive RF front-end can feed IQ samples or feature vectors into `sensor_ingest.py`.

## Quick Start on Jetson

```bash
# 1. Clone / copy this folder to the Orin Nano
cd silent_sentinel_edge

# 2. Create virtualenv (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Install Ollama (if using)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:3b

# 4. Run demo pipeline with simulated passive RF event
python -m src.main --demo
```

## Design Principles (from CDTFW analysis)

1. **Direction from above** – Inputs are driven by real operator questions / ROE / mission intent, not curiosity.
2. **Experts convert technology into military meaning** – Small local models + domain rules act as the “fellows”.
3. **Technologies evaluated as converging systems** – AI + passive RF + local sensing + human interpretation = new architecture.
4. **Every technology examined from both directions** – The four questions are mandatory.
5. **Product is influence / decision advantage** – Outputs are concise recommendations that a human can act on, not raw data dumps.
6. **Human-aligned by design** – Explicit governance, escalation flags, and override points.

## License & Intent

Research / prototype code for edge AI exploration of passive sensing + strategic sensemaking.  
Not a finished military system. Always keep a human in the decision loop.

---

*Built to operationalize the insight:*  
> “Do not study a technology as an object. Study the network of decisions, people, resources, vulnerabilities and consequences that becomes possible around it.”
