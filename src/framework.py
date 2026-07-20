"""
Repeatable 9-question diagnostic for studying any defense center,
lab, or capability (including Silent Sentinel itself).
"""

from __future__ import annotations
from typing import Any, Dict
from .edge_llm import EdgeLLM


SYSTEM_PROMPT = """You are applying the 9-element diagnostic framework used to understand
organizations such as the Center for Disruptive Technology and Future Warfare.
Answer each question concisely. Surface the hidden layer of power and incentives.
"""


QUESTIONS = [
    ("Mandate", "What authority created or sponsors it?"),
    ("Mission", "What uncertainty is it supposed to reduce?"),
    ("Customers", "Who actually requests and consumes its work?"),
    ("Inputs", "What data, intelligence, science and strategy feed it?"),
    ("People", "What disciplines and institutional backgrounds are represented?"),
    ("Process", "How are questions researched, tested, reviewed and approved?"),
    ("Outputs", "Does it produce papers, prototypes, doctrine, funding decisions or operations?"),
    ("Influence", "Where do those outputs enter real decision systems?"),
    ("Feedback", "How does the organization learn whether its assessment was correct?"),
]


def run_framework_diagnostic(llm: EdgeLLM, subject: str) -> str:
    q_text = "\n".join(f"{i+1}. {name}: {q}" for i, (name, q) in enumerate(QUESTIONS))
    user_prompt = f"""
Apply the 9-question diagnostic to the following subject:

SUBJECT: {subject}

Questions:
{q_text}

After answering the nine, also address the hidden layer:
- Who selects the questions?
- Who defines success?
- Who controls publication / release of findings?
- Who controls funding?
- Who can act on the findings?
- Who bears the consequences if the analysis is wrong?
"""
    return llm.generate(SYSTEM_PROMPT, user_prompt)
