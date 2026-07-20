"""
Translate a sensing event across Strategic / Operational / Tactical levels.
CDTFW primarily works at the strategic-to-operational bridge; this module
makes the same translation available at the edge.
"""

from __future__ import annotations
from typing import Any, Dict
from .edge_llm import EdgeLLM


SYSTEM_PROMPT = """You are an edge strategic analyst for Silent Sentinel.
Translate the given sensing event into the three classic levels of war.
Keep language precise and actionable for a human operator.
"""


def analyze_levels(llm: EdgeLLM, event: Dict[str, Any], four_q_result: str = "") -> str:
    user_prompt = f"""
Sensing event:
{event}

Previous four-question analysis (if available):
{four_q_result[:1500] if four_q_result else "None"}

Produce a short assessment at each level:

**TACTICAL**
What can a unit or operator physically do with this information right now?
(examples: cue a sensor, change posture, navigate without GPS, classify a contact)

**OPERATIONAL**
How does this change campaigns, joint-force operations, contested logistics,
C2 speed, reconnaissance persistence, or autonomous mass?

**STRATEGIC**
What national or theater-level advantage (or risk) does this create?
(deterrence, signature management, escalation control, alliance signaling, industrial independence)

End with a one-sentence recommendation for the human operator.
"""
    return llm.generate(SYSTEM_PROMPT, user_prompt)
