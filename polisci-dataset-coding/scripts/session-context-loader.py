#!/usr/bin/env python3
"""
Session Context Loader — SessionStart Hook for Dataset Coding

A SessionStart hook that reads coding_progress.json and injects a compact
progress briefing into Claude's context at the start of every session.

Two modes:
  - Normal:       Displays project progress summary
  - Post-compact: Re-injects the batch briefing that may have been lost
                   during auto-compression

Usage (in .claude/settings.json):
    "SessionStart": [
      { "hooks": [{ "type": "command",
          "command": "python3 scripts/session-context-loader.py" }] },
      { "matcher": "compact",
        "hooks": [{ "type": "command",
          "command": "python3 scripts/session-context-loader.py --post-compact" }] }
    ]
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def get_project_dir():
    """Get project directory from stdin JSON or environment."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}
    return hook_input.get("cwd", ""), hook_input


def load_progress(project_dir: str) -> dict | None:
    """Load coding_progress.json if it exists."""
    progress_path = Path(project_dir) / "Replication" / "data" / "coded" / "coding_progress.json"
    if not progress_path.exists():
        return None
    try:
        return json.loads(progress_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def load_batch_briefing(project_dir: str) -> str | None:
    """Load the batch briefing file if it exists."""
    briefing_path = Path(project_dir) / "Replication" / "data" / "coded" / ".context" / "batch_briefing.md"
    if not briefing_path.exists():
        return None
    try:
        content = briefing_path.read_text().strip()
        return content if content else None
    except OSError:
        return None


def format_progress(progress: dict) -> str:
    """Generate a compact progress summary from coding_progress.json."""
    lines = []
    lines.append("## Dataset Coding Progress")

    # Project overview
    project = progress.get("project", {})
    concept = project.get("concept", progress.get("concept", "unknown"))
    strategy = project.get("strategy", "unknown")
    majority = project.get("majority_voting", False)
    total = project.get("total_cells", 0)
    completed = project.get("completed_cells", 0)
    step = project.get("current_step", "unknown")

    majority_str = "ON" if majority else "OFF"
    lines.append(f"- Concept: {concept} | Strategy: {strategy} | Majority voting: {majority_str}")

    if total > 0:
        pct = (completed / total) * 100
        lines.append(f"- Progress: {completed:,} / {total:,} cells ({pct:.1f}%)")
    lines.append(f"- Current step: {step}")

    # Batch queue info
    batch_queue = progress.get("batch_queue", {})
    if batch_queue:
        current_var = batch_queue.get("current_variable", "")
        current_region = batch_queue.get("current_region", "")
        current_run = batch_queue.get("current_run", "")
        next_batch = batch_queue.get("next_batch_id", "")
        sentinel_gap = batch_queue.get("batches_since_sentinel_check", 0)
        check_interval = progress.get("drift_monitoring", {}).get("check_interval_batches", 10)

        if current_var:
            run_str = f" -> Run {current_run} of 3" if majority and current_run else ""
            region_str = f" -> {current_region}" if current_region else ""
            lines.append(f"- Current: {current_var}{region_str}{run_str}")
        if next_batch:
            lines.append(f"- Next batch: {next_batch}")
        if sentinel_gap > 0:
            remaining = check_interval - sentinel_gap
            if remaining <= 0:
                lines.append(f"- Sentinel check: **OVERDUE** (due {abs(remaining)} batches ago)")
            elif remaining <= 3:
                lines.append(f"- Sentinel check: due in {remaining} batches")

    # Context management info
    ctx = progress.get("context_management", {})
    batch_size = ctx.get("batch_size_cells", 0)
    sessions = ctx.get("sessions_completed", 0)
    if batch_size:
        lines.append(f"- Batch size: {batch_size} cells | Sessions completed: {sessions}")

    # Calibration status (compact)
    cal = progress.get("calibration", {})
    if cal:
        cal_status = cal.get("status", "")
        cal_icc = cal.get("icc", "")
        if cal_status:
            lines.append(f"- Calibration: {cal_status} (ICC: {cal_icc})" if cal_icc else f"- Calibration: {cal_status}")

    # Drift monitoring status (compact)
    drift = progress.get("drift_monitoring", {})
    checks = drift.get("checks", [])
    if checks:
        latest_check = checks[-1]
        status = latest_check.get("status", "UNKNOWN")
        exact_agree = latest_check.get("exact_agreement", "")
        if status in ("YELLOW", "RED"):
            lines.append(f"- **DRIFT ALERT: {status}** (sentinel agreement: {exact_agree})")

    # Resume command
    lines.append(f"- To continue: /create-dataset {concept} --resume {step}")

    return "\n".join(lines)


def format_batch_status(progress: dict) -> str:
    """Generate a compact batch completion summary."""
    batches = progress.get("batches", {})
    if not batches:
        return ""

    complete = sum(1 for b in batches.values() if isinstance(b, dict) and b.get("status") == "complete")
    in_prog = sum(1 for b in batches.values() if isinstance(b, dict) and b.get("status") == "in_progress")
    pending = sum(1 for b in batches.values() if isinstance(b, dict) and b.get("status") == "pending")

    return f"- Batches: {complete} complete, {in_prog} in progress, {pending} pending"


def main():
    project_dir, hook_input = get_project_dir()
    if not project_dir:
        sys.exit(0)

    post_compact = "--post-compact" in sys.argv

    progress = load_progress(project_dir)

    # No coding project active — nothing to inject
    if progress is None:
        sys.exit(0)

    # Check if this is actually a dataset coding project (has project or concept field)
    if not progress.get("project") and not progress.get("concept"):
        sys.exit(0)

    output_lines = []

    # Always output progress summary
    summary = format_progress(progress)
    output_lines.append(summary)

    batch_status = format_batch_status(progress)
    if batch_status:
        output_lines.append(batch_status)

    # Post-compact mode: also inject the batch briefing
    if post_compact:
        briefing = load_batch_briefing(project_dir)
        if briefing:
            output_lines.append("")
            output_lines.append("---")
            output_lines.append("")
            output_lines.append("## Batch Briefing (recovered after context compaction)")
            output_lines.append("")
            output_lines.append(briefing)

    # Output as a system message for Claude to consume
    full_output = "\n".join(output_lines)

    # Cap output at ~500 tokens (~2000 chars) to avoid bloating context
    if len(full_output) > 2000:
        full_output = full_output[:1950] + "\n\n[... truncated for context budget]"

    print(full_output)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
