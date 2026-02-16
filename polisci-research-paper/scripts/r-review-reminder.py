#!/usr/bin/env python3
"""
R-Reviewer Reminder Hook for Claude Code

A Stop hook that checks whether .R files were modified in the current session
(via git diff). If so, and r-reviewer hasn't been run yet, it blocks Claude
and reminds it to run the r-reviewer agent before stopping.

Usage (in .claude/settings.json):
    "Stop": [{ "hooks": [{ "type": "command", "command": "python3 scripts/r-review-reminder.py" }] }]
"""

import json
import sys
import subprocess
import hashlib
from pathlib import Path
from typing import Optional


STATE_DIR = Path("/tmp/claude-r-review-reminder")


def get_hook_input() -> dict:
    """Get hook input from stdin JSON."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return {}


def get_state_path(project_dir: str) -> Path:
    """Return a project-keyed state file path."""
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:12]
    return STATE_DIR / f"{project_hash}.json"


def load_state(state_path: Path) -> dict:
    """Load persisted state, or return defaults."""
    try:
        return json.loads(state_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"reminded": False, "reviewed_files": []}


def save_state(state_path: Path, state: dict):
    """Persist state to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state))


def get_modified_r_files(project_dir: str) -> list:
    """Find .R files that have been modified (staged + unstaged + untracked)."""
    r_files = []
    try:
        # Staged and unstaged changes
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=project_dir, timeout=5
        )
        if result.returncode == 0:
            r_files.extend(
                f for f in result.stdout.strip().split("\n")
                if f.endswith(".R") and f
            )

        # Untracked files
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, cwd=project_dir, timeout=5
        )
        if result.returncode == 0:
            r_files.extend(
                f for f in result.stdout.strip().split("\n")
                if f.endswith(".R") and f
            )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return list(set(r_files))


def check_review_reports(project_dir: str, r_files: list) -> list:
    """Check which R files do NOT have a recent review report."""
    unreviewed = []
    quality_dir = Path(project_dir) / "quality_reports"

    for r_file in r_files:
        script_name = Path(r_file).stem
        report = quality_dir / f"{script_name}_r_review.md"
        if not report.exists():
            unreviewed.append(r_file)
        else:
            # Report exists — check if R file is newer than report
            r_path = Path(project_dir) / r_file
            if r_path.exists() and r_path.stat().st_mtime > report.stat().st_mtime:
                unreviewed.append(r_file)

    return unreviewed


def main():
    hook_input = get_hook_input()

    # If stop_hook_active, Claude is already continuing from a previous
    # Stop hook block — let it stop to avoid infinite loops.
    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    project_dir = hook_input.get("cwd", "")
    if not project_dir:
        sys.exit(0)

    state_path = get_state_path(project_dir)
    state = load_state(state_path)

    # Find modified R files
    r_files = get_modified_r_files(project_dir)
    if not r_files:
        # No R files modified — nothing to do
        sys.exit(0)

    # Check which ones lack review reports (or have stale reports)
    unreviewed = check_review_reports(project_dir, r_files)
    if not unreviewed:
        # All modified R files have up-to-date reviews
        sys.exit(0)

    # Already reminded once this session — let Claude proceed
    if state.get("reminded", False):
        # Check if the files changed since last reminder
        if set(unreviewed) == set(state.get("unreviewed_files", [])):
            sys.exit(0)

    # Block and remind
    state["reminded"] = True
    state["unreviewed_files"] = unreviewed
    save_state(state_path, state)

    file_list = ", ".join(unreviewed)
    output = {
        "decision": "block",
        "reason": (
            f"R-REVIEWER REMINDER: {len(unreviewed)} R file(s) were modified "
            f"without review: {file_list}. Run /review-r on these files before "
            f"finishing, or use the r-reviewer agent directly."
        ),
    }
    json.dump(output, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
