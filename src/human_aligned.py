"""
Human-aligned intelligence guards.
Enforces the principle that the product of Silent Sentinel is decision advantage
for a human, never autonomous action beyond clearly defined authority.
"""

from __future__ import annotations
from typing import Any, Dict, List
from dataclasses import dataclass, field


@dataclass
class AlignmentReport:
    human_in_loop_required: bool = True
    escalation_flags: List[str] = field(default_factory=list)
    authority_gaps: List[str] = field(default_factory=list)
    ethical_notes: List[str] = field(default_factory=list)
    recommended_action: str = "Present to human operator for decision"


def check_alignment(event: Dict[str, Any], analysis_text: str) -> AlignmentReport:
    report = AlignmentReport()

    # Simple rule-based guards (can be expanded with LLM later)
    text_lower = analysis_text.lower()
    event_type = event.get("type", "").lower()

    if "kinetic" in text_lower or "lethal" in text_lower or "engage" in text_lower:
        report.escalation_flags.append("Potential kinetic implication detected – human authorization mandatory")
        report.authority_gaps.append("No automatic weapons release authority exists on this edge node")

    if event.get("features", {}).get("confidence", 1.0) < 0.7:
        report.escalation_flags.append("Confidence below threshold – treat as cue only, not confirmed track")

    if "adversary" in text_lower and "deception" in text_lower:
        report.ethical_notes.append("Possible adversary deception / spoofing – corroborate with independent sources")

    if "escalation" in text_lower:
        report.escalation_flags.append("Escalation risk explicitly mentioned – elevate to operational command")

    # Always keep human in the loop for this prototype
    report.human_in_loop_required = True
    report.recommended_action = (
        "Display full analysis to human operator. "
        "Do not autonomously task sensors beyond passive observation or local cueing "
        "without explicit ROE and operator confirmation."
    )

    return report
