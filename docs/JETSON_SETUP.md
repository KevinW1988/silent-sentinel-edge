# Deploying Silent Sentinel Edge on Jetson Orin Nano

## 1. Base System

- Flash the latest JetPack (6.2 or 7.x recommended) via SDK Manager or SD card image.
- Enable MAXN or 15 W / 25 W power mode depending on cooling:
  ```bash
  sudo nvpmodel -m 0   # MAXN
  sudo jetson_clocks
  ```

## 2. Python Environment

```bash
sudo apt update
sudo apt install python3-pip python3-venv git
cd /path/to/silent_sentinel_edge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Local LLM (Ollama – simplest path)

```bash
curl -fsSL https://ollama.com/install.sh | sh
# Pull a model that fits comfortably in 8 GB
ollama pull qwen2.5:3b
# or
ollama pull llama3.2:3b
ollama pull gemma2:2b
```

Edit `config/settings.yaml` and set:
```yaml
llm:
  backend: "ollama"
  model: "qwen2.5:3b"
```

## 4. Alternative: llama.cpp / TensorRT-LLM

For maximum performance you can compile llama.cpp with CUDA support or use NVIDIA’s TensorRT-LLM containers.  
Keep models quantized (Q4_K_M or lower) to stay inside the 8 GB envelope.

## 5. Run

```bash
source venv/bin/activate
python -m src.main --demo
```

## 6. Integrating Real Sensors

- Passive RF: feed feature vectors (frequency, bandwidth, power, Doppler, modulation class) into `sensor_ingest.normalize_event`.
- Vision: run YOLO / RT-DETR via TensorRT and push detections as events of type `local_ai_detection`.
- CAM-Pulse style local sensing: any low-level anomaly score can be wrapped the same way.

The pipeline will automatically run the four-question analysis, level translation, convergence check, and human-alignment guards.

## 7. Human-in-the-Loop

By design the edge node **never** takes kinetic or high-escalation action.  
All outputs are decision aids for a human operator.  
The `human_aligned.py` module enforces this rule set and can be extended with ROE tables.
