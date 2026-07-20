#!/usr/bin/env python3
"""
Silent Sentinel Edge AI – Strategic Sensemaking entry point.
Designed for NVIDIA Jetson Orin Nano.
"""

from __future__ import annotations
import argparse
import logging
import sys
from pathlib import Path

# Allow running as module or script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline import SilentSentinelPipeline
from src.sensor_ingest import event_stream, load_demo_events
from src.framework import run_framework_diagnostic
from src.edge_llm import EdgeLLM, load_config
from rich.console import Console

console = Console()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_demo(config_path: str = "config/settings.yaml"):
    console.print("[bold green]Silent Sentinel Edge – Demo Pipeline[/]")
    console.print("Target: Jetson Orin Nano | CDTFW-inspired strategic sensemaking\n")

    pipe = SilentSentinelPipeline(config_path)

    for event in event_stream(config_path):
        pipe.process_event(event)
        console.print("\n" + "─" * 60 + "\n")


def run_framework(subject: str, config_path: str = "config/settings.yaml"):
    cfg = load_config(config_path)
    llm = EdgeLLM(cfg)
    console.print(f"[bold]Running 9-question diagnostic on:[/] {subject}\n")
    result = run_framework_diagnostic(llm, subject)
    console.print(result)


def main():
    parser = argparse.ArgumentParser(description="Silent Sentinel Edge AI Strategic Core")
    parser.add_argument("--demo", action="store_true", help="Run demo with simulated passive RF / local AI events")
    parser.add_argument("--framework", type=str, help="Run 9-question diagnostic on a subject string")
    parser.add_argument("--config", type=str, default="config/settings.yaml", help="Path to settings.yaml")
    args = parser.parse_args()

    if args.demo:
        run_demo(args.config)
    elif args.framework:
        run_framework(args.framework, args.config)
    else:
        parser.print_help()
        console.print("\n[yellow]Tip: start with  python -m src.main --demo[/]")


if __name__ == "__main__":
    main()
