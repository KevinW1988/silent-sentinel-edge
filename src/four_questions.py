"""
Four connected questions that every technology / detection must answer
(Employment, Exploitation, Defeat, Governance).
"""

from __future__ import annotations
from typing import Any, Dict
from .edge_llm import EdgeLLM


SYSTEM_PROMPT = """You are a strategic sensemaking assistant running on a Silent Sentinel edge node.
Your job is to evaluate a sensing event or technology through four mandatory lenses.
Be concise, military-relevant, and always surface risks to human decision-makers.
Never recommend autonomous lethal action. Always keep a human in the loop.
Respond in clear structured markdown.
"""


def analyze_four_questions(llm: EdgeLLM, event: Dict[str, Any]) -> str:
    user_prompt = f"""
Analyze the following edge sensing event using the four mandatory questions:

EVENT:
{event}

1. EMPLOYMENT – How could friendly forces usefully employ this capability / information?
2. EXPLOITATION – How could an adversary employ a similar capability against us or use this signature for deception?
3. DEFEAT – How could either side disrupt, spoof, or neutralize this sensing modality?
4. GOVERNANCE – What ethical, legal, command, escalation, or authority problems accompany acting on this information?

Finish with a short "Net Strategic Value" assessment using the equation:
Capability gained − new vulnerabilities − adversary countermeasures − integration burden − ethical/command risk = actual strategic value
"""
    return llm.generate(SYSTEM_PROMPT, user_prompt)
