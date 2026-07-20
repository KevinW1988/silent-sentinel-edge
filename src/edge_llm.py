"""
Local LLM interface optimized for Jetson Orin Nano.
Supports Ollama (recommended) and a pure-mock backend for testing without a model.
"""

from __future__ import annotations
import json
import logging
from typing import Any, Dict, Optional
import requests
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


class EdgeLLM:
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config.get("llm", {})
        self.backend = self.cfg.get("backend", "mock")
        self.model = self.cfg.get("model", "qwen2.5:3b")
        self.base_url = self.cfg.get("base_url", "http://localhost:11434")
        self.temperature = self.cfg.get("temperature", 0.3)
        self.max_tokens = self.cfg.get("max_tokens", 512)
        self.timeout = self.cfg.get("timeout_seconds", 60)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if self.backend == "ollama":
            return self._ollama_generate(system_prompt, user_prompt)
        elif self.backend == "mock":
            return self._mock_generate(system_prompt, user_prompt)
        else:
            raise ValueError(f"Unknown LLM backend: {self.backend}")

    def _ollama_generate(self, system: str, user: str) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            "stream": False,
        }
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            return f"[LLM ERROR] {e}"

    def _mock_generate(self, system: str, user: str) -> str:
        """Deterministic mock for development without a running model."""
        return (
            "MOCK ANALYSIS (no real LLM loaded)\n"
            f"System context length: {len(system)} chars\n"
            f"User query length: {len(user)} chars\n"
            "— Employment: Useful for silent cueing of higher-fidelity sensors.\n"
            "— Exploitation: Adversary could use similar passive signatures for deception.\n"
            "— Defeat: Direction-finding + multi-static correlation can localize the emitter.\n"
            "— Governance: Requires clear ROE before any kinetic or electronic response.\n"
            "Recommendation: Flag for human review at operational level. Confidence moderate."
        )


def load_config(path: str | Path = "config/settings.yaml") -> Dict[str, Any]:
    with open(path, "r") as f:
        return yaml.safe_load(f)
