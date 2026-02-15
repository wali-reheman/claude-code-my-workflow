# Plan: Context Window Management for `/create-dataset` — Claude Code Native Architecture

**Date:** 2026-02-13
**Status:** COMPLETED
**Task:** Optimize the dataset coding workflow to handle large-scale projects (50 vars × 20 countries × 100 years = 100K cells) entirely within Claude Code, exploiting advanced features: rules auto-loading, subagents, hooks, rolling context files, PROJECT_MEMORY, dynamic `!` command injection, and structured JSON state.

---

## Context

The `/create-dataset` workflow currently has no context window management. For a 100K-cell project:
- No token budget estimation → batches overflow context
- No temporal continuity between sessions → each `--resume` starts blind
- Codebook consumes ~7,500 tokens for 50 variables even when coding just one
- No rolling context → Claude can't compare to previous coding decisions
- Majority voting (3 runs) triples context pressure with no isolation strategy
- 100+ sessions needed with no automated state management between them

**Design philosophy:** Use **files on disk as external memory** and Claude Code's **subagent isolation** to keep the working context lean. The context window is a workbench, not a warehouse — load only what the current task needs.

---

## Architecture Overview: The "Context Relay" Pattern

```
                    ┌─────────────────────────┐
                    │     coding_progress.json │  ← Cross-session state (what's done, what's next)
                    └────────┬────────────────┘
                             │
    ┌────────────────────────┼─────────────────────────┐
    │ SESSION START          │                          │
    │                        ▼                          │
    │  ┌─────────────────────────────┐                  │
    │  │  SessionStart hook fires    │                  │
    │  │  → reads coding_progress    │                  │
    │  │  → reads rolling context    │                  │
    │  │  → injects batch briefing   │                  │
    │  └────────────┬────────────────┘                  │
    │               │                                   │
    │               ▼                                   │
    │  ┌─────────────────────────────┐                  │
    │  │  SKILL.md Step 3            │                  │
    │  │  (loads ONLY what's needed: │                  │
    │  │   1 var def + bridge cases  │                  │
    │  │   + rolling context file    │                  │
    │  │   + batch instructions)     │                  │
    │  └────────────┬────────────────┘                  │
    │               │                                   │
    │               ▼                                   │
    │  ┌─────────────────────────────┐                  │
    │  │  CODE BATCH                 │                  │
    │  │  (each majority-vote run    │                  │
    │  │   = separate subagent       │                  │
    │  │   with isolated context)    │                  │
    │  └────────────┬────────────────┘                  │
    │               │                                   │
    │               ▼                                   │
    │  ┌─────────────────────────────┐                  │
    │  │  WRITE TO DISK              │                  │
    │  │  → batch CSV                │                  │
    │  │  → update rolling context   │                  │
    │  │  → update progress.json     │                  │
    │  └────────────┬────────────────┘                  │
    │               │                                   │
    │               ▼                                   │
    │  ┌─────────────────────────────┐                  │
    │  │  Next batch or --resume     │                  │
    │  └─────────────────────────────┘                  │
    └──────────────────────────────────────────────────┘
```

---

## Component 1: Structured Cross-Session State (`coding_progress.json` enhancement)

**File:** `Replication/data/coded/coding_progress.json`

Currently tracks batch status. Enhance to become the **single source of truth for session resumption**.

### New fields:

```json
{
  "project": {
    "concept": "religious_governance",
    "strategy": "variable-first",
    "majority_voting": true,
    "total_cells": 100000,
    "completed_cells": 34200,
    "current_step": "step-3"
  },
  "batch_queue": {
    "current_variable": "clergy_appointment",
    "current_region": "middle_east",
    "current_run": 2,
    "next_batch_id": "clergy_appointment_mena_r2",
    "batches_since_sentinel_check": 7
  },
  "context_management": {
    "codebook_token_estimate": 7500,
    "rolling_context_token_estimate": 800,
    "batch_size_cells": 60,
    "last_session_id": "abc123",
    "sessions_completed": 47
  },
  "calibration": { "...existing fields..." },
  "drift_monitoring": { "...existing fields..." }
}
```

### How it's used:
- **`--resume step-3`**: reads `batch_queue.next_batch_id` to know exactly where to start
- **Batch sizing**: reads `context_management.codebook_token_estimate` to compute how many cells fit
- **Sentinel timing**: reads `batches_since_sentinel_check` to know if a drift check is due

---

## Component 2: Rolling Context Files (External Memory)

**Key insight:** Instead of carrying all previous coding decisions in context, write compact summaries to disk files that get loaded selectively.

### 2a. Variable-First Rolling Context

**File:** `Replication/data/coded/.context/variable_[varname].md`

One file per variable, updated after each regional batch. Contains cross-country calibration context.

```markdown
# Rolling Context: clergy_appointment
Updated: 2026-02-13 batch 14

## Score Distribution So Far
- Mean: 2.1 | Median: 2 | Range: 0-4
- Latin America (N=22): mean 2.8, range 1-4
- Sub-Saharan Africa (N=38): mean 1.4, range 0-3
- MENA (in progress): mean 1.2, range 0-3

## Bridge Cases (calibration anchors)
- Turkey (640): 2 [established pilot]
- Iran (630): 0 [established pilot]
- USA (2): 4 [established pilot]

## Coding Decisions Log (last 5 notable)
- Jordan 2005: scored 1 not 2 because appointed Grand Mufti lacks independence (2/3 agree)
- Morocco 2011: scored 2, constitutional reform gave some clerical autonomy (3/3 agree)
- Tunisia 2014: scored 3, post-revolution religious freedom (3/3 agree)

## Alerts
- None
```

**Size:** ~200-400 tokens per variable. Loaded ONLY for the current variable being coded.

### 2b. Country-First Rolling Context

**File:** `Replication/data/coded/.context/country_[cow_code].md`

One file per country, updated after each variable within that country. Contains temporal continuity.

```markdown
# Rolling Context: Turkey (COW: 640)
Updated: 2026-02-13

## Score Vector (compact)
| Variable | 1920 | 1925 | ... | 2000 | 2005 | 2010 | 2015 | 2020 |
|----------|------|------|-----|------|------|------|------|------|
| clergy_appt | 0 | 0 | ... | 1 | 2 | 2 | 1 | 1 |
| relig_court | 0 | 0 | ... | 0 | 0 | 0 | 0 | 0 |

## Key Transitions
- 1924: Caliphate abolished, Diyanet established (clergy_appt 0→0, confirms state control)
- 2002: AKP election, gradual shift (multiple vars affected)
- 2010: Constitutional referendum (clergy_appt 1→2)
- 2016: Post-coup purges (clergy_appt 2→1)

## Coding Decisions Log
- clergy_appt 2003: scored 1 (not 2) because AKP hadn't yet enacted formal changes
- Consistent pattern: all religion-state vars show 2002-2010 liberalization, 2013+ reversal

## Cross-Variable Coherence
- clergy_appt and relig_education move together (r=0.85 so far)
- relig_court stays at 0 throughout — Turkey abolished religious courts in 1924
```

**Size:** ~300-600 tokens per country. Loaded ONLY for the current country being coded.

### 2c. `.context/` directory structure

```
Replication/data/coded/.context/
├── variable_clergy_appointment.md
├── variable_religious_court_authority.md
├── ...
├── country_640.md          # Turkey
├── country_630.md          # Iran
├── ...
├── batch_briefing.md       # Auto-generated for next session (Component 3)
└── codebook_production.md  # Compressed codebook (Component 4)
```

---

## Component 3: Session Start Hook + Batch Briefing

**Mechanism:** A `SessionStart` hook with `"compact"` matcher re-injects critical context after auto-compression. Plus a general SessionStart hook that displays progress on every session start.

### 3a. Hook configuration (`.claude/settings.json` additions)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/scripts/session-context-loader.py\"",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/scripts/session-context-loader.py\" --post-compact",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/scripts/log-reminder.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### 3b. `scripts/session-context-loader.py`

New Python script. Reads `coding_progress.json` and generates a compact briefing:

**On normal session start:**
```
## Dataset Coding Progress
- Concept: religious_governance | Strategy: variable-first | Majority voting: ON
- Progress: 34,200 / 100,000 cells (34.2%)
- Current: clergy_appointment → MENA region → Run 2 of 3
- Next batch: clergy_appointment_mena_r2
- Sentinel check: due in 3 batches
- To continue: /create-dataset religious_governance --resume step-3
```

**After auto-compaction (`--post-compact`):**
Same as above PLUS reads `.context/batch_briefing.md` and outputs its contents — this is the critical context that might have been lost during compression.

### 3c. Batch briefing auto-generation

At the end of each batch (before stopping), the skill writes `.context/batch_briefing.md`:

```markdown
# Batch Briefing (auto-generated for next session)

## What was just completed
- Batch: clergy_appointment_mena_r1 (Run 1 of 3)
- Cells coded: 380 (19 countries × 20 years)
- Agreement with bridge cases: all within 1 point

## What to do next
1. Code Run 2: same cells, independent context (DO NOT read Run 1 results)
2. After Run 3: merge runs, compute majority vote
3. Then: move to Sub-Saharan Africa region

## Active alerts
- None

## Key decisions from this session
- Jordan pre-1946: coded UNABLE_TO_CODE (not independent state)
- Palestine: coded as 699 (COW for West Bank/Gaza), per interview decision
```

**This file is the "relay baton"** — it carries exactly what the next session needs to know, nothing more.

---

## Component 4: Two-Tier Codebook (Full vs Production)

**Problem:** The full codebook with inclusion/exclusion criteria is ~150 tokens/variable × 50 variables = 7,500 tokens. During production coding of a single variable, 49 of those variable definitions are dead weight.

### Solution: Generate a production codebook at Step 2f

**File:** `Replication/data/coded/.context/codebook_production.md`

**For variable-first:** Contains ONLY the current variable's full definition (including inclusion/exclusion). Generated dynamically by the skill when loading context for each variable.

**For country-first:** Contains a medium-format codebook (~80 tokens/variable) that keeps definitions + inclusion/exclusion but drops anchor examples and methodology context:

```markdown
## clergy_appointment (0-4)
Degree of government control over appointment of religious leaders.
- 0: Full state control over all appointments
- 4: Religious bodies appoint independently
INCLUDE WHEN: Government has formal/informal role in selecting religious leaders
EXCLUDE WHEN: Government regulates religious organizations but not appointments
DO NOT CONFUSE WITH: religious_freedom (broader concept)
```

vs the full format which also has 3+ anchor examples per scale point, scale justification, methodological context, etc.

### Token savings:
- Variable-first: load 1 variable at ~150 tokens instead of 50 at ~7,500 = **98% reduction**
- Country-first: load medium codebook at ~80 × 50 = 4,000 instead of 7,500 = **47% reduction**

---

## Component 5: Majority Voting via Task-Tool Subagent Isolation

**Problem:** 3 runs must be independent — Claude shouldn't see its own previous answers. Within a single Claude Code session, all conversation history is visible.

### Solution: Each run = one Task-tool subagent (general-purpose)

**Mechanism:** The SKILL.md Step 3 orchestrates majority voting by spawning Task-tool subagents. The Task tool already provides context isolation — each subagent gets a fresh context window with no access to the parent's conversation history or other runs' results.

**No separate skill file needed.** The main SKILL.md writes a batch specification file (`.context/current_batch.json`) and then spawns subagents with explicit prompts:

```
Main session (orchestrator):
  │
  ├── Write .context/current_batch.json (cells to code, run_id=1)
  ├── Spawn Task subagent (type: general-purpose, Run 1)
  │   └── Prompt: "Read .context/current_batch.json, codebook section, bridge cases,
  │   │            rolling context. Code all cells. Write to runs/run1_*.csv.
  │   │            Return summary: N cells, score distribution, bridge case values."
  │   └── Context: ISOLATED (fresh window, cannot see main session or other runs)
  │   └── Returns: summary text only (not full CSV content)
  │
  ├── Spawn Task subagent (Run 2) — SAME prompt, different run_id
  │
  ├── Spawn Task subagent (Run 3) — SAME prompt, different run_id
  │   (Runs 2 and 3 can run in PARALLEL with Run 1 — max 3 parallel subagents)
  │
  └── Main session: read 3 CSV files from disk, compute majority vote, write merged output

```

**Why this works:**
- Task-tool subagents get **fresh context windows** — documented Claude Code behavior
- The main session's context stays lean (it only sees the summaries, not 3× the coding output)
- Each subagent loads only what it needs from disk: variable def + bridge cases + rolling context + cells
- After the subagent returns, only the summary text enters the main context
- All 3 runs can execute in parallel (Task tool supports up to 3 parallel agents)
- No need for a separate `coding-run.md` skill — the prompt provides all instructions

**Batch sizing for subagents:** Subagents get their own 200K context window. Use **50% budget** (conservative): 100K tokens available. With ~1,200 tokens overhead, that's ~800 cells per subagent. But cap at **80 cells** for judgment quality — better more small batches than risk degraded attention.

**What the subagent prompt includes:**
1. The production prompt template (from conventions Section 7)
2. Variable definition (full, including inclusion/exclusion — ~150 tokens)
3. Bridge case values for this variable (~100 tokens)
4. Rolling context file content (~300 tokens)
5. List of cells to code: `[{cow_code, country_name, year, variable}]`
6. Output instructions: write CSV to specific path, return summary

**What the subagent prompt does NOT include:**
- Other variables' definitions
- Other runs' results (isolation guarantee)
- Full conventions file (subagent doesn't need rules about codebook design)
- Conversation history from the main session

---

## Component 6: Prompt Restructuring (Lost in the Middle)

**Problem:** Research shows models attend most to the beginning and end of long prompts, with degraded attention in the middle.

**Current structure:**
1. Variable definition (beginning)
2. Bridge cases
3. Rules 7-9 (MIDDLE — weakest attention)
4. Instructions (end)

**New structure:**
1. **RULES + TEMPORAL BOUNDARY** (beginning — highest attention)
2. **Instructions + output format** (still near top)
3. Variable definition + bridge cases (middle — reference material)
4. **Regional comparison reminder + confidence requirements** (end — attention recovers)

### Implementation: Edit conventions Section 7 prompt template

---

## Component 7: Strategy-Specific Context Loading Rules

Add to conventions as **Section 18: Context Management Protocol**.

### Variable-first context loading:
```
Per batch, load:
1. codebook_production.md (ONE variable section: ~150 tokens)
2. bridge_cases.csv (filtered to this variable: ~100 tokens)
3. .context/variable_[varname].md (rolling context: ~300 tokens)
4. Cells to code (country × year list: ~200 tokens)
5. Prompt template with rules (~400 tokens)
────────────────────────────────────────
Total overhead: ~1,150 tokens
Remaining for coding output: ~195,000 tokens (200K model)
Cells per batch at ~100 output tokens each: ~100-150 cells
```

### Country-first context loading:
```
Per batch, load:
1. codebook_production.md (ALL variables, medium format: ~4,000 tokens)
2. bridge_cases.csv (all bridge cases: ~300 tokens)
3. .context/country_[cow].md (rolling context: ~500 tokens)
4. Years to code for all variables (~300 tokens)
5. Prompt template with rules (~400 tokens)
────────────────────────────────────────
Total overhead: ~5,500 tokens
Remaining for coding output: ~190,500 tokens
Cells per batch at ~100 output tokens each: ~80-100 cells
(~20 years × ~5 variables, or ~10 years × ~10 variables)
```

### Dynamic batch sizing formula:
```
cells_per_batch = floor((context_budget - overhead_tokens) / tokens_per_cell)
context_budget = 120,000 tokens (60% of 200K, leaving room for reasoning)
overhead_tokens = codebook + bridge + rolling_context + prompt + instructions
tokens_per_cell = 100 (output) + 20 (input: country/year/variable identifiers)
cap: max 100 cells per batch (quality degrades beyond this for judgment tasks)
```

This formula is computed by the skill at Step 2f (after codebook is finalized and token costs are known) and stored in `coding_progress.json`.

---

## Component 8: Rules File Splitting (Context Budget Protection)

**Problem:** `dataset-construction-conventions.md` (~900 lines, ~4,000+ tokens) auto-loads via `paths: ["Replication/data/**"]` every time Claude touches any coded data file. During production coding (Step 3), Claude doesn't need the codebook design template, calibration protocol, or narrative template — it needs only the production prompt template, CSV schema, and batch protocol.

### Solution: Split into design-time and production-time rules

**File 1 (existing, tighten paths):** `dataset-construction-conventions.md`
- Change paths to: `["Replication/data/coded/codebook.md", "Replication/data/coded/interview_summary.md", "Replication/data/coded/gold_standard/**"]`
- Loads during: Steps 0-2 (design phases), Step 5 (documentation)
- Contains: Sections 1-6, 9-12, 14, 16-17 (design, calibration, documentation, pre-testing, gold-standard, DSL)

**File 2 (new):** `dataset-production-protocol.md`
- Paths: `["Replication/data/coded/*.csv", "Replication/data/coded/runs/**", "Replication/data/coded/.context/**"]`
- Loads during: Step 3 (production coding)
- Contains: Section 7 (prompt template), Section 13 (majority voting rules), Section 15 (sentinel protocol), Section 18 (context management), CSV schema
- **Size target: ~200 lines** (vs 900 for the full conventions)

**Token savings during production:** ~4,000 → ~800 tokens for auto-loaded rules. That's ~3,200 tokens freed per batch.

### Also add compact instructions to CLAUDE.md:

```markdown
# Compact instructions
When compacting during a /create-dataset session, preserve:
- Current batch state: variable, region, run number, batch_id
- Rolling context file paths (.context/ directory)
- Any unwritten batch results or partial CSVs
- Coding decisions and scope clarifications from this session
- The batch briefing (.context/batch_briefing.md path)
```

---

## Component 9: Rolling Context Update Protocol

**Who updates rolling context files?** The main orchestrator, NEVER the subagents.

**Timing:** After all 3 runs complete and majority vote is computed for a batch:
1. Read the current rolling context file (`.context/variable_*.md` or `.context/country_*.md`)
2. Compute updated statistics from the merged majority-vote output:
   - Score distribution (mean, median, range by region)
   - Bridge case values (did they match?)
   - Notable coding decisions (any 2/3 or 0/3 cells worth logging)
3. Append/update the rolling context file
4. Keep file under 500 tokens — when it grows too long, compress older entries (replace specific decisions with summary stats)
5. Write `.context/batch_briefing.md` with what-just-happened + what-to-do-next

**Rolling context file size management:**
- Coding Decisions Log: keep last 10 entries, oldest fall off
- Score Distribution: overwrite with current stats (not append)
- Alerts: clear resolved alerts, keep active ones
- Target: 300-500 tokens always

---

## Component 10: PROJECT_MEMORY Integration

### Existing: `[LEARN:dataset]` tags in PROJECT_MEMORY.md

### New: Automatic learning from coding patterns

After each session, the skill checks for patterns worth remembering:
- If a country was consistently UNABLE_TO_CODE → `[LEARN:dataset] [country] has very limited coverage for [concept]. Consider excluding from production or flagging as known gap.`
- If bridge case drifted → `[LEARN:dataset] Bridge case [country] for [variable] tends to drift upward in MENA batches. Extra vigilance needed.`
- If majority voting showed consistent disagreement on a variable → `[LEARN:dataset] [variable] has high 2/3 disagreement rate (~25%). Consider tightening inclusion/exclusion criteria.`

These get appended to PROJECT_MEMORY.md and are read at every session start.

---

## Files to Create (3 new)

| # | File | Purpose |
|---|------|---------|
| 1 | `scripts/session-context-loader.py` | SessionStart hook: reads progress.json, generates compact briefing for context injection. Post-compact mode re-injects batch briefing. |
| 2 | `.claude/rules/dataset-production-protocol.md` | Lean production-only rules (~200 lines): prompt template, CSV schema, majority voting rules, sentinel protocol, context management. Auto-loads only during Step 3. |
| 3 | `Replication/data/coded/.context/README.md` | Documents the .context/ directory purpose and file formats |

## Files to Edit (6 existing)

| # | File | Changes |
|---|------|---------|
| 4 | `.claude/settings.json` | Add SessionStart hooks (normal + compact matcher) |
| 5 | `.claude/rules/dataset-construction-conventions.md` | Tighten `paths:` to design-phase files only. Add Section 18 (Context Management Protocol). Edit Section 7 (prompt restructuring — rules at beginning). Move production-relevant sections to new file. |
| 6 | `.claude/skills/create-dataset/SKILL.md` | Major updates: Step 0 (context budget interview question), Step 2f (codebook compression + batch size computation + rolling context init), Step 3 (Task-tool subagent majority voting, rolling context loading/updating, batch briefing generation) |
| 7 | `CLAUDE.md` | Add context management to Working Philosophy. Add compact instructions. Update folder structure with `.context/`. |
| 8 | `.claude/agents/coding-reliability-reviewer.md` | Add context management checks: .context/ files present, batch sizing documented, rolling context not stale |
| 9 | `.gitignore` or equivalent | Add `Replication/data/coded/.context/` (session-specific, not versioned) |

---

## Implementation Order

**Phase A (independent — can run in parallel):**
1. `scripts/session-context-loader.py` — the SessionStart hook script
2. `.claude/rules/dataset-production-protocol.md` — the lean production rules file
3. `Replication/data/coded/.context/README.md` — directory documentation

**Phase B (depends on Phase A, can be partially parallelized):**
4. `.claude/settings.json` — add SessionStart hook configuration
5. `.claude/rules/dataset-construction-conventions.md` — tighten paths, add Section 18, restructure prompt in Section 7, remove production sections (moved to new file)
6. `.claude/skills/create-dataset/SKILL.md` — update Steps 0, 2f, 3 with context management, Task-tool subagent orchestration, rolling context, batch briefing

**Phase C (finishing):**
7. `CLAUDE.md` — add context management to working philosophy + compact instructions
8. `.claude/agents/coding-reliability-reviewer.md` — add context artifact checks
9. `.gitignore` — add `.context/` exclusion

---

## Verification

- [ ] SessionStart hook fires and displays progress summary (test with mock `coding_progress.json`)
- [ ] Post-compact hook re-injects batch briefing from `.context/batch_briefing.md`
- [ ] `dataset-production-protocol.md` auto-loads when touching CSV files (check `paths:` frontmatter)
- [ ] `dataset-construction-conventions.md` does NOT auto-load when touching CSV files (tightened paths)
- [ ] Prompt template (Section 7) has rules + temporal boundary at BEGINNING, not middle
- [ ] Section 18 has token budget formulas for BOTH strategies (variable-first and country-first)
- [ ] SKILL.md Step 3 uses Task tool (not a separate skill) for majority voting subagents
- [ ] Subagent prompt includes: variable def, bridge cases, rolling context, cells, output path
- [ ] Subagent prompt does NOT include: other variables, other runs' results, full conventions
- [ ] Rolling context file templates specified for both strategies (variable_*.md and country_*.md)
- [ ] Rolling context files capped at ~500 tokens with compression protocol for older entries
- [ ] Dynamic batch sizing formula stored in `coding_progress.json` at Step 2f
- [ ] Batch size capped at 80 cells (judgment quality threshold)
- [ ] `.context/` directory in `.gitignore` (session-specific, not versioned)
- [ ] CLAUDE.md has compact instructions for dataset coding sessions
- [ ] PROJECT_MEMORY auto-learning rules specified in SKILL.md
- [ ] All existing majority voting, sentinel, gold-standard, pre-testing, and DSL functionality PRESERVED
- [ ] No new external dependencies (no API key, no Python packages beyond stdlib)

---

## What This Does NOT Change

- Steps 0-2 (interview, codebook, pilot) — these are small enough to fit in context already
- The reliability architecture (majority voting, sentinels, gold-standard) — preserved exactly
- The review agent protocol — preserved, with minor additions
- The quality gates — preserved
- No API key or external tools required — pure Claude Code
