"""
Main CDTFW-inspired operating pipeline for Silent Sentinel edge AI.
"""

from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .edge_llm import EdgeLLM, load_config
from .four_questions import analyze_four_questions
from .levels import analyze_levels
from .convergence import analyze_convergence
from .human_aligned import check_alignment, AlignmentReport
from .sensor_ingest import normalize_event
from .bridge import post_to_worldmonitor

logger = logging.getLogger(__name__)
console = Console()


class SilentSentinelPipeline:
    def __init__(self, config_path: str | Path = "config/settings.yaml"):
        self.config = load_config(config_path)
        self.llm = EdgeLLM(self.config)
        self.cfg = self.config.get("pipeline", {})
        self.output_cfg = self.config.get("output", {})

    def process_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        event = normalize_event(raw_event)
        results: Dict[str, Any] = {"event": event}

        console.print(Panel(f"[bold cyan]New Edge Event[/]\n{event['description']}", title="Silent Sentinel"))

        # 1. Four questions (mandatory)
        if self.cfg.get("enable_four_questions", True):
            console.print("[yellow]→ Running four-question analysis...[/]")
            four_q = analyze_four_questions(self.llm, event)
            results["four_questions"] = four_q
            console.print(Markdown(four_q))

        # 2. Levels translation
        if self.cfg.get("enable_levels", True):
            console.print("[yellow]→ Translating across tactical / operational / strategic levels...[/]")
            levels = analyze_levels(self.llm, event, results.get("four_questions", ""))
            results["levels"] = levels
            console.print(Markdown(levels))

        # 3. Convergence
        if self.cfg.get("enable_convergence", True):
            console.print("[yellow]→ Evaluating technology convergence...[/]")
            conv = analyze_convergence(self.llm, event)
            results["convergence"] = conv
            console.print(Markdown(conv))

        # 4. Human-aligned checks
        full_text = "\n".join(
            str(results.get(k, "")) for k in ("four_questions", "levels", "convergence")
        )
        alignment: AlignmentReport = check_alignment(event, full_text)
        results["alignment"] = {
            "human_in_loop_required": alignment.human_in_loop_required,
            "escalation_flags": alignment.escalation_flags,
            "authority_gaps": alignment.authority_gaps,
            "ethical_notes": alignment.ethical_notes,
            "recommended_action": alignment.recommended_action,
        }

        console.print(
            Panel(
                f"[bold]Human-in-the-loop:[/] {alignment.human_in_loop_required}\n"
                f"[bold]Flags:[/] {alignment.escalation_flags or 'None'}\n"
                f"[bold]Action:[/] {alignment.recommended_action}",
                title="Alignment Guard",
                style="green" if not alignment.escalation_flags else "red",
            )
        )

        # Optional JSON log
        if self.output_cfg.get("json_log", False):
            log_path = Path(self.output_cfg.get("log_path", "/tmp/silent_sentinel_events.jsonl"))
            with open(log_path, "a") as f:
                f.write(json.dumps(results, default=str) + "\n")

        # 5. Edge ↔ Cloud bridge (World Monitor)
        bridge_resp = post_to_worldmonitor(results, self.config)
        if bridge_resp is not None:
            results["bridge"] = bridge_resp
            console.print("[green]✓ Posted to World Monitor bridge[/]")

        return results
