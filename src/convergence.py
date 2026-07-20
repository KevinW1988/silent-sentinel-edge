"""
Technologies are rarely disruptive in isolation.
The greatest effects appear when they converge into a new operational architecture.
"""

from __future__ import annotations
from typing import Any, Dict, List
from .edge_llm import EdgeLLM


SYSTEM_PROMPT = """You are analyzing technology convergence for Silent Sentinel edge AI.
Remember the equation:
Technology + trained people + doctrine + communications + logistics + authorities + data + security = operational capability
Technology alone ≠ capability.
"""


def analyze_convergence(
    llm: EdgeLLM,
    event: Dict[str, Any],
    related_techs: List[str] | None = None,
) -> str:
    if related_techs is None:
        related_techs = [
            "passive RF sensing",
            "edge AI classification",
            "local human-machine interpretation",
            "distributed low-signature nodes",
            "resilient mesh communications",
        ]

    user_prompt = f"""
Current sensing event:
{event}

Related technology set under consideration:
{related_techs}

Assess:

1. What new operational architecture becomes possible when these elements converge?
2. What integration burdens (power, data, training, doctrine, security) appear?
3. What single-point failures or cascading vulnerabilities are created by the convergence?
4. What is the net change in signature management and force protection?

Keep the answer short and focused on decision-relevant insight.
"""
    return llm.generate(SYSTEM_PROMPT, user_prompt)
