"""Quick smoke test using the mock LLM backend (no Ollama required)."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.edge_llm import EdgeLLM
from src.pipeline import SilentSentinelPipeline
from src.sensor_ingest import load_demo_events
import yaml


def test_mock_pipeline():
    # Force mock backend
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "settings.yaml"
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    cfg["llm"]["backend"] = "mock"

    # Temporarily write a test config
    test_cfg = Path("/tmp/ss_test_settings.yaml")
    with open(test_cfg, "w") as f:
        yaml.dump(cfg, f)

    pipe = SilentSentinelPipeline(test_cfg)
    events = load_demo_events(cfg_path)
    assert len(events) > 0

    result = pipe.process_event(events[0])
    assert "four_questions" in result
    assert "levels" in result
    assert "alignment" in result
    assert result["alignment"]["human_in_loop_required"] is True
    print("Mock pipeline test passed.")


if __name__ == "__main__":
    test_mock_pipeline()
