"""
Sensor / event ingest layer.
In a real deployment this would accept:
- IQ samples or features from a passive RF front-end
- Detections from local edge vision / YOLO models
- CAM-Pulse style local sensing events
- ROS2 topics, ZeroMQ, MQTT, etc.
"""

from __future__ import annotations
from typing import Any, Dict, Generator, List
import yaml
from pathlib import Path
import time


def load_demo_events(config_path: str | Path = "config/settings.yaml") -> List[Dict[str, Any]]:
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg.get("sensing", {}).get("demo_events", [])


def event_stream(config_path: str | Path = "config/settings.yaml") -> Generator[Dict[str, Any], None, None]:
    """Simple generator that yields demo events with a short delay."""
    events = load_demo_events(config_path)
    for ev in events:
        yield ev
        time.sleep(0.5)  # simulate real-time arrival


def normalize_event(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure every event has a consistent schema."""
    return {
        "type": raw.get("type", "unknown"),
        "description": raw.get("description", ""),
        "features": raw.get("features", {}),
        "timestamp": raw.get("timestamp", time.time()),
        "source": raw.get("source", "silent_sentinel_edge"),
    }
