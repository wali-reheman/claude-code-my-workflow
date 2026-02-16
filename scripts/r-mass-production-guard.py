#!/usr/bin/env python3
"""
R Mass-Production Guard — PostToolUse Hook

Detects when Claude writes multiple .R files back-to-back without reading
any input data or running scripts in between. Emits a soft warning (non-blocking)
reminding Claude to examine the specific input data before writing the next script.

Design:
  - PostToolUse fires AFTER Write/Edit/Read/Bash complete.
  - On Write/Edit of .R file: log it as an "R write event."
  - On Read of data file (.csv, .rds, .dta, .xlsx, .tsv, .sav, .parquet):
    reset the guard (Claude is examining data).
  - On Bash running Rscript: reset the guard (Claude is executing/testing).
  - If a second .R write happens without an intervening data read or Rscript run,
    emit a warning via stderr (exit 2 = soft block, but we use stderr + exit 0
    so it's truly non-blocking — Claude sees the message but isn't stopped).

State: /tmp/claude-r-mass-production-guard/<project_hash>.json
"""

import json
import sys
import hashlib
import time
from pathlib import Path
from typing import Optional, Tuple

STATE_DIR = Path("/tmp/claude-r-mass-production-guard")
# Data file extensions that count as "Claude examined input"
DATA_EXTENSIONS = {".csv", ".rds", ".dta", ".xlsx", ".tsv", ".sav", ".parquet", ".xls"}


def get_hook_input() -> dict:
    """Read hook input from stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return {}


def get_state_path(project_dir: str) -> Path:
    """Project-keyed state file."""
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:12]
    return STATE_DIR / f"{project_hash}.json"


def load_state(state_path: Path) -> dict:
    try:
        return json.loads(state_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_r_write": None, "last_r_write_time": 0, "warned_for": None}


def save_state(state_path: Path, state: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state))


def is_r_file(file_path: str) -> bool:
    """Check if a file path is an R script."""
    return file_path.endswith(".R") or file_path.endswith(".r")


def is_data_file(file_path: str) -> bool:
    """Check if a file path is a data file."""
    return Path(file_path).suffix.lower() in DATA_EXTENSIONS


def is_rscript_run(hook_input: dict) -> bool:
    """Check if this was a Bash call running Rscript."""
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        return False
    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")
    return "Rscript" in command or "rscript" in command


def get_file_path(hook_input: dict) -> Optional[str]:
    """Extract file_path from tool_input."""
    tool_input = hook_input.get("tool_input", {})
    return tool_input.get("file_path", None)


def main():
    hook_input = get_hook_input()
    project_dir = hook_input.get("cwd", "")
    if not project_dir:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    state_path = get_state_path(project_dir)
    state = load_state(state_path)

    file_path = get_file_path(hook_input)

    # --- Event: Claude READ a data file → reset guard ---
    if tool_name == "Read" and file_path and is_data_file(file_path):
        state["last_r_write"] = None
        state["last_r_write_time"] = 0
        save_state(state_path, state)
        sys.exit(0)

    # --- Event: Claude ran Rscript → reset guard ---
    if is_rscript_run(hook_input):
        state["last_r_write"] = None
        state["last_r_write_time"] = 0
        save_state(state_path, state)
        sys.exit(0)

    # --- Event: Claude WROTE an .R file ---
    if tool_name in ("Write", "Edit") and file_path and is_r_file(file_path):
        previous_r = state.get("last_r_write")
        previous_time = state.get("last_r_write_time", 0)
        warned_for = state.get("warned_for")
        now = time.time()

        # Is this a DIFFERENT .R file from the last one we tracked?
        # (Editing the same file multiple times is fine)
        if previous_r and previous_r != file_path:
            # Second .R file without data read in between → warn
            # But only warn once per pair (don't spam)
            warn_key = f"{previous_r}→{file_path}"
            if warned_for != warn_key:
                state["warned_for"] = warn_key
                state["last_r_write"] = file_path
                state["last_r_write_time"] = now
                save_state(state_path, state)

                prev_name = Path(previous_r).name
                curr_name = Path(file_path).name
                # JSON output with additionalContext — soft warning, non-blocking
                warning_msg = (
                    f"R MASS-PRODUCTION WARNING: You just wrote {curr_name} "
                    f"right after {prev_name} without reading any input data "
                    f"or running scripts in between. Per r-code-conventions.md "
                    f"Section 0: each R script needs individual analytical "
                    f"attention. Before continuing, read the actual input data "
                    f"this script will process, or review the output of the "
                    f"previous script."
                )
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": warning_msg,
                    }
                }
                json.dump(output, sys.stdout)
                sys.exit(0)
            # Already warned for this pair — don't repeat
            state["last_r_write"] = file_path
            state["last_r_write_time"] = now
            save_state(state_path, state)
            sys.exit(0)

        # First .R write (or same file re-edited) — just record it
        state["last_r_write"] = file_path
        state["last_r_write_time"] = now
        state["warned_for"] = None
        save_state(state_path, state)
        sys.exit(0)

    # --- Any other tool use: don't touch state ---
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Fail open
        sys.exit(0)
