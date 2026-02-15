# Session Log: Context Window Management Implementation

**Date:** 2026-02-14
**Goal:** Implement the "Context Relay" architecture for managing context window pressure in large-scale dataset coding projects (100K+ cells).

## Context

Continued from the 2026-02-13 session. The previous session built the full `/create-dataset` workflow (Phases 1-7: bug fixes, interview, strategies, narratives, country expertise design, literature-based improvements). This session addresses the identified gap: no context window management for production coding at scale.

## Design Phase (previous session, carried over)

### Three Architectural Paths Evaluated

1. **Path A: Pure Claude Code** — optimize with hooks, rules auto-loading, subagents, rolling context files. Scale limit: ~30-50K cells comfortable, 100K possible with session chaining.
2. **Path B: Automation harness + API** — Python script orchestrates, Anthropic Batch API for 50% discount. Handles 100K+ cells.
3. **Path C: Hybrid** — Claude Code for design (Steps 0-2, 5), API for production (Step 3).

**User chose Path A** — stay entirely within Claude Code, exploit all advanced features.

### Key Design Decision: Context Relay Pattern

"The context window is a workbench, not a warehouse — load only what the current task needs."

10 components designed across two sessions with two rounds of self-critique:
1. Enhanced `coding_progress.json` as cross-session state
2. Rolling context files (`.context/` directory)
3. SessionStart hooks + batch briefing
4. Two-tier codebook (full vs production)
5. Majority voting via Task-tool subagent isolation
6. Prompt restructuring (Lost in the Middle)
7. Strategy-specific context loading rules
8. Rules file splitting (design-time vs production-time)
9. Rolling context update protocol
10. PROJECT_MEMORY auto-learning

## Phase 8: Implementation

### Files Created (3 new)

1. **`scripts/session-context-loader.py`** — SessionStart hook that reads `coding_progress.json` and injects compact progress briefing. Post-compact mode re-injects `.context/batch_briefing.md`. Follows same pattern as `log-reminder.py` (fail-open, stdin JSON input). Output capped at ~500 tokens.

2. **`.claude/rules/dataset-production-protocol.md`** — Lean production rules (~200 lines). Auto-loads via `paths: ["Replication/data/coded/*.csv", "runs/**", ".context/**"]`. Contains: restructured prompt template (rules at beginning, reminders at end), CSV schema, majority voting rules, sentinel protocol, context management protocol, batch sizing formula, rolling context update protocol, PROJECT_MEMORY auto-learning rules.

3. **`Replication/data/coded/.context/README.md`** — Documents the `.context/` directory: file types, update protocol, lifecycle.

### Files Modified (6 existing)

4. **`.claude/settings.json`** — Added SessionStart hooks: normal (fires every session) + compact matcher (fires after auto-compaction). Both run `session-context-loader.py`.

5. **`.claude/rules/dataset-construction-conventions.md`** — Three changes:
   - Tightened `paths:` from `["Replication/data/**"]` to design-phase files only (`codebook.md`, `interview_summary.md`, `gold_standard/**`, etc.). This prevents the 900-line conventions from auto-loading during production coding, saving ~3,200 tokens per batch.
   - Restructured Section 7 prompt template: rules + temporal boundary at BEGINNING (highest attention), reference material in MIDDLE, reminders at END (attention recovery). "Lost in the Middle" fix.
   - Added Section 18: Context Management Protocol — cross-session state schema, rolling context files, dynamic batch sizing formula, two-tier codebook, subagent isolation, SessionStart hooks, rules file splitting.

6. **`.claude/skills/create-dataset/SKILL.md`** — Three major updates:
   - Step 0 Phase 0e: added project scale estimation and context relay notification for 5K+ cell projects
   - Step 2f: expanded from sentinel-only to sentinel + context management initialization (generate production codebook, compute batch sizing, initialize rolling context files, enhance progress.json, write initial batch briefing)
   - Step 3: completely rewritten with Task-tool subagent orchestration for majority voting. Full orchestration flow documented: write batch spec → spawn 3 parallel subagents → merge votes → post-batch checks → update rolling context → update progress → write batch briefing. Added PROJECT_MEMORY auto-learning. Added session management (mid-session context pressure, `--resume` flow, SessionStart hook integration).

7. **`CLAUDE.md`** — Four updates:
   - Added `.context/` directory to folder structure
   - Added `session-context-loader.py` to scripts listing
   - Added "Context Window Management" subsection to Working Philosophy
   - Added "Compact Instructions" subsection with preservation directives
   - Updated Pipeline to show Step 2f context initialization

8. **`.claude/agents/coding-reliability-reviewer.md`** — Added context management artifact checks to Phase 1 inventory: `.context/` directory, enhanced progress.json fields, batch sizing documentation, rolling context staleness check.

9. **`.gitignore`** — Added `Replication/data/coded/.context/` (session-specific, not versioned).

## Key Design Decisions

- **Subagent isolation, not `context: fork` skills**: Task-tool subagents already get fresh context windows by design. No need for a separate `coding-run.md` skill — the prompt IS the specification.
- **Rules file splitting**: The 900-line conventions file was causing ~4K tokens of dead weight during production. Split into design-time (tightened paths) and production-time (~200 lines) saves ~3,200 tokens per batch.
- **80-cell batch cap**: Even though token math allows 100-150 cells, judgment quality degrades beyond 80 for subjective coding tasks.
- **Orchestrator updates rolling context, never subagents**: Prevents race conditions and ensures consistency.
- **Batch briefing as relay baton**: The `.context/batch_briefing.md` file carries exactly what the next session needs, nothing more. Re-injected after auto-compaction.

## Phase 8b: Critical Assessment Fixes (9 problems identified and resolved)

After initial implementation, a critical assessment identified 9 problems. All fixed in a follow-up pass.

### Problems Fixed

| # | Severity | Problem | Fix | Files Modified |
|---|----------|---------|-----|----------------|
| P1 | CRITICAL | `current_batch.json` had shared `output_path` — 3 subagents would overwrite each other | Output path moved to per-run Task prompt; removed from `current_batch.json` | production-protocol.md, SKILL.md |
| P2 | MAJOR | Subagents can't read auto-loaded rules files (fresh context window) | Made `current_batch.json` fully self-contained: embeds prompt template, variable def, scale, bridge cases, rolling context, CSV schema, coding rules summary | production-protocol.md, SKILL.md, .context/README.md, conventions Section 18 |
| P3 | MAJOR | No CSV validation before majority-vote merge | Added CSV Validation Protocol: check file exists, headers, row count, score range, required fields. Retry failed runs once. | production-protocol.md, SKILL.md |
| P4 | MODERATE | SessionStart hook output format | **Non-issue**: verified SessionStart hooks use plain text stdout (correct), not JSON `decision`/`reason` (that's Stop hooks) | No changes needed |
| P5 | MODERATE | Hardcoded token estimates (~150, ~100, ~300, ~400) | Step 2f now computes from actual file content using `len(text)/4`. All estimates stored in `coding_progress.json` with `estimation_method` field. Re-estimate after first batch. | SKILL.md |
| P6 | MODERATE | Rolling context compression was vague ("compress older entries") | Made mechanical: FIFO queue (max 10 decisions), OVERWRITE stats, DELETE resolved alerts. If >500 tokens: compress to 5 decisions, then summarize stats. | production-protocol.md, conventions Section 18 |
| P7 | MINOR | Production protocol duplicated conventions with no sync tracking | Added prominent sync note at top of production protocol with last-sync date | production-protocol.md |
| P8 | MODERATE | No subagent failure handling | Added: verify CSV + retry once + degrade gracefully (2 valid runs: use majority; 1 valid run: flag for manual review) | production-protocol.md, SKILL.md, conventions Section 18 |
| P9 | MINOR | Batch briefing had no completion status | Added `Status: COMPLETED/IN_PROGRESS/FAILED` + `Timestamp` + `Failed runs` section | production-protocol.md, SKILL.md, .context/README.md |

### Files Modified in Phase 8b

1. **`.claude/rules/dataset-production-protocol.md`** — P1, P2, P3, P6, P7, P8, P9: sync note, self-contained JSON schema, CSV validation protocol, mechanical compression, failure handling, batch briefing status
2. **`.claude/skills/create-dataset/SKILL.md`** — P1, P2, P3, P5, P8: self-contained batch spec, per-run output paths, validation step, runtime token estimation, failure handling
3. **`.claude/rules/dataset-construction-conventions.md`** — P2, P6, P8: updated Section 18 subagent isolation (self-contained), mechanical compression rules, validation/failure handling
4. **`Replication/data/coded/.context/README.md`** — P2, P9: self-contained JSON description, batch briefing status field

## Phase 8c: User Verification of P1 Fix (majority voting preserved)

User asked whether the P1 fix (removing `output_path` from `current_batch.json`) broke the majority voting architecture. Confirmed:

- **3-run independence fully preserved.** The fix only changed WHERE the output path lives — moved from the shared JSON to the per-run Task prompt.
- Each subagent still reads the same `current_batch.json` (shared batch spec), codes all cells independently, and writes to its own unique file path (`run1_...`, `run2_...`, `run3_...`).
- The orchestrator still reads all 3 CSVs, validates them, and computes majority vote exactly as before.
- Traced through the full flow in SKILL.md lines 343-395 to confirm the architecture diagram is correct.

## Phase 8d: Cross-Country Calibration Fixes (4 gaps identified and resolved)

After user asked about country-first coding at scale (20 MENA countries × 40 variables × 100 years), analysis identified 4 gaps in cross-country calibration. All fixed.

### Gaps and Fixes

| # | Gap | Fix | Files Modified |
|---|-----|-----|----------------|
| A | No cross-country variable-level rolling context in country-first mode | Added `variable_summary.md` — per-variable score distribution table, updated after each country. Loaded into `current_batch.json` for subagent context. | .context/README.md, production-protocol.md, SKILL.md, conventions Section 18 |
| B | Prompt instruction "regional comparison" is dead in country-first mode (batch = 1 country) | Made prompt instruction #6 strategy-aware: variable-first uses regional comparison, country-first uses cross-country comparison referencing variable summary. Added VARIABLE SUMMARY section to prompt template. | conventions Section 7, production-protocol.md (prompt template + Rule 9) |
| C | No calibration checkpoint between countries | Added post-country calibration checkpoint: (1) update variable_summary.md, (2) anomaly detection >1.5 SD, (3) bridge case calibration pulse (re-code all bridges for all vars), (4) log to progress.json. | conventions Section 11, production-protocol.md, SKILL.md (country-first steps 9-11) |
| D | Bridge cases carry only one overall score, not per-variable | Bridge cases now carry per-variable scores for ALL variables. `bridge_cases.csv` already had per-variable rows; `current_batch.json` schema updated to show `scores: {var1: N, var2: N, ...}`. `coding_progress.json` bridge schema updated. | conventions Section 7 (prompt template), conventions Section 11 (bridge case example), production-protocol.md (JSON schema), SKILL.md (Step 1 bridge case definition) |

### Files Modified in Phase 8d

1. **`Replication/data/coded/.context/README.md`** — Added Variable Summary file type with full template, added to `current_batch.json` fields, updated lifecycle
2. **`.claude/rules/dataset-production-protocol.md`** — Sync note updated, country-first context loading updated (6 items, ~6,300 tokens overhead), `current_batch.json` schema updated (per-variable bridge cases + variable_summary field), Rule 9 updated, prompt template updated (strategy-aware comparison, per-variable bridge format, VARIABLE SUMMARY section), post-country calibration checkpoint section added, coding rules summary updated
3. **`.claude/skills/create-dataset/SKILL.md`** — Step 1 bridge case definition expanded, Step 2f variable_summary.md initialization added, country-first strategy steps expanded (9-11: variable summary update, post-country checkpoint, narratives), self-contained JSON contents list updated (9 items)
4. **`.claude/rules/dataset-construction-conventions.md`** — Rule 9 updated, Section 7 prompt template updated (strategy-aware comparison, per-variable bridge format, VARIABLE SUMMARY section, updated reminders), bridge case insertion note expanded, coding_progress.json bridge schema updated (per-variable scores), Section 11 country-first risks/mitigations expanded, post-country calibration checkpoint protocol added, Section 18 rolling context files list updated, country-first overhead updated (~6,300 tokens), subagent isolation description updated

## Phase 8e: Thought Experiment Stress-Test (State Secularization in MENA)

Ran full mental walkthrough of `/create-dataset state_secularization --countries mena --years 1920-2023 --strategy country-first --narratives`. Traced Steps 0-5 with concrete cases (Turkey, Iran, Egypt, Gulf states). Identified 3 gaps and fixed all.

### Gaps and Fixes

| # | Gap | Fix | Files Modified |
|---|-----|-----|----------------|
| 1 | Bridge cases assume stable anchors — fails for concepts with regime changes (Iran 1979, Turkey post-2002) | **Era-specific bridge cases**: `bridge_cases.csv` now has `era`, `year_start`, `year_end` columns. Each era gets its own row. Batch loading filters to era overlapping batch's year range. Interview (Step 0, 8b) asks about regime changes. | conventions (Section 7 prompt, bridge CSV schema, Section 11, coding_progress.json), production-protocol (JSON schema, prompt, insertion note), SKILL.md (Step 0 Phase 0d, Step 1) |
| 2 | Sentinel monitoring catches global drift but misses country-specific hallucination spikes on data-sparse countries (Oman, Bahrain, pre-unification Yemen) | **Data-Sparsity Hallucination Escalation**: auto-computes 4 batch indicators (UNABLE_TO_CODE rate, LOW confidence rate, 0/3 rate, evidence word count). Escalates spot-check from 5→10→15 citations. If fabrication found at elevated level → PAUSE. | production-protocol (new section), SKILL.md (post-batch checks), conventions (Section 10 pitfall #9) |
| 3 | Post-country anomaly detection (>1.5 SD) is meaningless with N < 5 countries | **N >= 5 threshold**: anomaly detection skips for first 4 countries. Bridge calibration pulse still runs. | conventions (Section 11), production-protocol (post-country checkpoint), SKILL.md (step 10) |

### Key Design Decision

Era-specific bridge cases add a small schema change (`bridge_cases.csv` gains 3 columns) but solve a fundamental problem: for any concept spanning 50+ years in a region with regime changes, single-point bridge scores are actively misleading. The pilot must establish scores for each era separately.

## Open Questions

- Batch API architecture identified as future evolution for 100K+ cell projects — not built
- The actual per-token cost estimates for subagent overhead need empirical testing with a real codebook
- `current_batch.json` embedding the full prompt template means it grows to ~2-3K tokens; acceptable but should be monitored
- Country-first overhead grew from ~5,500 to ~6,300 tokens with variable_summary addition — should be monitored for large codebooks (50+ variables)
- Post-country calibration pulse is single-run (not 3-run majority) for efficiency — may want to make this configurable
- Colonial-era coding (pre-independence MENA states) is a scope decision for Step 0 — the workflow surfaces it but doesn't prescribe a default

## Phase 8f: Second Thought Experiment Pass — Final Fixes

Re-traced full thought experiment after Phase 8e fixes. Found 2 more issues:

| # | Issue | Fix | Files |
|---|-------|-----|-------|
| 1 | Pilot sampling says "50 countries, 5-7 per region" — fails for regional datasets (MENA has ~20 countries, 1 region) | Pilot adapts to scope: global → 50 countries, regional → all available, small-N → all + more years | SKILL.md Step 2a, 2e |
| 2 | Track B calibration doesn't specify per-variable vs aggregate for multi-variable codebooks | Per-variable calibration: each variable must pass individually (2/5 proxies at r≥0.4). Aggregate can compensate only as a flag-and-proceed mechanism. | SKILL.md Step 2c, conventions Section 4 Track B |

After these fixes, the full thought experiment traces through cleanly from Step 0 through Step 5.

## Phase 8g: Real Codebook Stress-Test (35-Variable Secularization Codebook)

User shared actual codebook from `State-led-Secularization-Campaign-in-MENA/codebook_core.md`: 35 sub-variables across 8 dimensions (D1-D8), 1920-2019, currently coded for 6 countries. Traced through full workflow. Architecture handles it well; 3 minor fixes needed.

### Issues Found

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | 🟡 | Q8b implies binary (before/after) era splits — Egypt has 3 eras (Nasser, Sadat/Mubarak, post-2013) | Updated Q8b wording in SKILL.md and conventions to explicitly support multi-era countries. Updated bridge example in conventions and production-protocol to show 3-era Egypt. |
| 2 | 🟡 | Gold-standard Section 16 says "≥ 4 world regions" — fails for regional datasets (already fixed for pilot in Phase 8f, but not for gold-standard) | Updated conventions Section 16 sampling design table with separate columns for global vs regional datasets. Regional: "≥ 3 sub-regions or country clusters." |
| 3 | 🟡 | Cost/time table in SKILL.md assumes 3-5 variables — wildly inaccurate for 35-variable codebooks (pilot goes from 750 cells to 3,500) | Expanded cost table with formula, more rows including "Large pilot (many vars)" and "High-variable production", plus explanatory note. |
| 4 | 🔴 | Track B calibration nearly impossible for ~15/35 variables (no external proxy for waqf, kuttab, fatwa, D8 governance vars) | NOT a workflow bug — fundamental property of novel measurement. Workflow correctly surfaces the limitation via flag-and-proceed. No fix needed. |
| 5 | 🟡 | D8 variables (governance inclusion) require subjective judgment about informal power — highest hallucination/disagreement risk | NOT a workflow issue — codebook design consideration. The confidence/evidence requirements and majority voting handle it. No fix needed. |

### Key Observation

User's existing 6-country coded data is a massive asset: serves as ready-made gold standard, calibration benchmark, and bridge case library. Most users build this from scratch; this codebook already has ~21,000 expert-coded cells.

### Files Modified

1. **SKILL.md** — Q8b multi-era wording, cost/time table expanded
2. **conventions.md** — Section 16 gold-standard stratification (global vs regional columns), era-specific bridge section (multi-era wording + 3-era Egypt example)
3. **production-protocol.md** — Bridge case JSON example expanded with 3-era Egypt

## Phase 8h: Gold-Standard Opt-Out Option

User asked: "could we make the gold-standard expert coding optional?" Implemented full opt-out pathway.

### Design

Gold-standard validation is now **recommended but optional**. The user decides during the Step 0 interview (new question 7b). If they opt out:

- Step 2e ICC gate is skipped entirely
- Sentinels fall back to **bridge-only mode** (bridge cases as sentinel pool — tests scale stability, not accuracy against expert judgment)
- Methodology report must disclose the opt-out and its consequences
- DSL bias correction is unavailable
- The user can always provide gold-standard data later via `--audit`

### What Remains Without Gold-Standard

Majority voting (3-run), bridge case consistency, hallucination audits, Track A/B calibration, data-sparsity escalation, all 10 coding rules. These are substantial — the dataset isn't unvalidated, it's just missing the strongest accuracy check.

### Files Modified

1. **SKILL.md** — New question 7b (gold-standard opt-out) in Step 0 interview. Step 2e split into opt-in/opt-out paths. Step 2f sentinel setup split into gold-standard/bridge-only modes. Step 5 documentation adjusted. Principle 3 softened from "non-negotiable" to "strongly recommended."
2. **conventions.md** — Section 15 sentinel protocol: added bridge-only mode with explanation of weaker guarantees. Section 16: added Gold-Standard Opt-Out subsection with what-is-lost / what-remains lists and retroactive audit note. Section 9: updated Sections 4 and 10 of methodology report with opt-out disclosure language.

## Phase 8i: No-Gold-Standard Compensating Checks

User asked: "check again to see how we can improve the workflow to perform better without gold-standard." Investigated all existing quality mechanisms and identified 3 enhancements.

### What Was Added

**1. Cross-Variable Coherence Check (conventions Section 19a):**
- During codebook design (Step 1), define expected correlation patterns between related variables
- After each country, check for logically incoherent score profiles (e.g., high on one family law variable but zero on a related one)
- Without gold-standard: flag country-years with 2+ violations for re-examination
- With gold-standard: report only

**2. Temporal Monotonicity Check (conventions Section 19b):**
- After each batch, scan for year-over-year score jumps ≥ 2 within same country × variable
- Check if evidence field mentions a major event (coup, revolution, reform, etc.)
- Without gold-standard: flag jumps lacking major-event evidence
- With gold-standard: report only

**3. Hallucination Audit Intensity Increase (conventions Section 19c):**
- Pilot: 30 citations (up from 20) when gold-standard opted out
- Production base rate: 10/batch (up from 5). Data-sparsity escalation: 15/20 (up from 10/15)
- Rationale: without expert review, the hallucination audit is the ONLY external fabrication check

### What Cannot Be Improved

No automated check can substitute for the accuracy anchor that gold-standard provides. These checks catch *inconsistency* (cross-variable), *implausibility* (temporal jumps), and *fabrication* (hallucination audit). They cannot catch *systematic bias* where Claude consistently misinterprets a concept. This is an honest limitation, not a workflow gap.

### Files Modified

1. **conventions.md** — New Section 19 (No-Gold-Standard Compensating Checks: 19a cross-variable coherence, 19b temporal monotonicity, 19c hallucination intensity). Section 5 hallucination audit: increased N for opt-out. Section 16 opt-out "What remains": added the 3 new mechanisms.
2. **production-protocol.md** — New No-Gold-Standard Compensating Checks section (temporal monotonicity + cross-variable coherence). Updated hallucination escalation table with dual-column (with/without GS). Sync note updated.
3. **SKILL.md** — Step 1: added coherence rules definition (item 5). Step 2d: increased hallucination audit N for opt-out. Step 3 post-batch: added temporal monotonicity check. Step 3 post-country: added cross-variable coherence check (item 11).

## Phase 8j: De Facto Coding Rule in Production Prompt

User identified that most political science coding cares about de facto (actual practice), not de jure (law on paper). The workflow already asks de jure vs de facto during codebook design (Step 1) and records it, but that decision **did not flow into the production prompt template** — the part Claude actually reads during coding.

### The Gap

The production prompt's evidence instruction said "citing a specific event, **law**, institution, or documented pattern" — which actively invited de jure evidence. Nothing in the RULES section (highest attention zone) told Claude to prioritize actual practice over legal text. For de facto variables, this means Claude might code a constitutional provision as the score even when the reality on the ground contradicts the law.

### The Fix

Added **Rule 5** to the production prompt template (both conventions Section 7 and production-protocol.md):
- `[IF DE FACTO]`: "Code ACTUAL PRACTICE, not law on paper. A constitutional provision that is unenforced should be noted as context but NOT determine the score."
- `[IF DE JURE]`: "Code the formal legal/institutional framework as written."
- Rule is omitted entirely if the codebook doesn't specify.

Also updated the evidence instruction: for de facto variables, evidence must document actual practice/enforcement. Legal text may be cited as context ("although the constitution states X, in practice Y") but the score reflects reality. Changed "law" to "action" in the evidence instruction to avoid inviting statute citations.

Updated `coding_rules_summary` in `current_batch.json` schema to include Rule 5 for de facto codebooks.

### How It Works in Practice

The `[IF DE FACTO]` / `[IF DE JURE]` tags are resolved at Step 2f when generating `current_batch.json`. The orchestrator reads the codebook's measurement type decision and bakes the appropriate version of Rule 5 into the prompt template embedded in the batch spec. The subagent sees a concrete rule, not a conditional.

### Files Modified

1. **conventions.md** — Section 7 production prompt: added Rule 5 (de facto/de jure), updated evidence instruction
2. **production-protocol.md** — Mirror of Section 7 changes, updated `coding_rules_summary` in `current_batch.json` schema, sync note updated

## Phase 8k: Evidence Source Hierarchy

User asked: "should we add a hierarchy of sources?" Led to multi-round design discussion before implementation.

### Design Evolution

1. **Initial envision:** 4-tier hierarchy with hard confidence caps (Tier 3 → MEDIUM cap, Tier 4 → LOW cap). Partially implemented before user said "let's optimize first."

2. **User insight:** Tiers should guide Claude's *reasoning* when coding, not mechanically cap the confidence output. The hierarchy is for the thinking part, not primarily for the confidence score.

3. **Critical assessment identified 3 problems with hard caps:**
   - **Perverse incentive:** Hard caps incentivize tier inflation (claim Tier 1 to unlock HIGH confidence). The tier inflation detection we'd build is defending against a problem the caps themselves create.
   - **Signal destruction:** If 40% of cells get MEDIUM purely from evidence availability (not actual uncertainty), MEDIUM becomes noise. Confidence loses its differentiating signal.
   - **False precision:** Some Tier 3 evidence IS genuinely definitive (the authoritative monograph on a specific country's policy). Mechanically capping at MEDIUM destroys real information.

4. **Final design — three roles, no hard caps:**
   - **Reasoning scaffold:** Rule 6 in the RULES section (highest attention zone) forces Claude to classify evidence BEFORE scoring. Tier 3/4 triggers "actively search for something more concrete."
   - **Soft signal:** HIGH confidence with Tier 3/4 is allowed but MUST be explicitly justified in `uncertainty_reason`. Creates friction without prohibition.
   - **Post-hoc audit signal:** Researchers filter `evidence_tier >= 3 AND confidence == HIGH` for targeted human review. The justification in `uncertainty_reason` is auditable.

### What Was Implemented

**New conventions Section 20: Evidence Source Hierarchy**
- 4 tiers based on specificity-of-claim (not source prestige): (1) specific dated event/action, (2) institutional description of practice, (3) scholarly characterization, (4) general inference/undated claim
- Soft confidence interaction table: expected defaults but no hard caps. HIGH + Tier 3/4 requires justification.
- De facto codebooks: law alone without enforcement evidence is Tier 2 at best, not Tier 1
- Tier inflation detection in hallucination audit (TIER_INFLATED status, < 15% threshold)
- Rolling context tracks mean evidence tier per batch/cumulative. Mean > 2.5 triggers alert.

**New Rule 11 added to AI Coder Regulation (conventions Section 3 + production-protocol):**
- Evidence hierarchy — classify tier BEFORE scoring. Tier 3/4 triggers active search. HIGH + Tier 3/4 requires justification.

**Production prompt template (both files) — Rule 6 + output field #4:**
- Rule 6 in RULES section: reasoning scaffold instruction
- Output field #4: Evidence Tier: 1/2/3/4

**CSV schema (both files):** New `evidence_tier` column between `evidence_date` and `uncertainty_reason`.

**Hallucination audit (conventions Section 5):**
- New TIER_INFLATED classification status
- Tier inflation rate threshold (< 15%)
- Audit log table expanded with Claimed Tier / Actual Tier columns

**Production-protocol.md:**
- New Evidence Source Hierarchy section (lean reference)
- Updated `current_batch.json` schema: `evidence_tier` in `csv_columns`, Rule 10 in `coding_rules_summary`
- Updated sync note to Phase 8k

**SKILL.md:**
- Post-batch checks: added evidence tier monitoring (mean tier, tier-confidence mismatch rate) and tier inflation check
- Rolling context update: added mean evidence tier to OVERWRITE stats
- Self-contained JSON contents list updated

**.context/README.md:**
- Rolling context templates expanded with Evidence Quality section (mean tier, tier distribution)

### Legacy Cleanup

Post-implementation review found one legacy artifact from before the evidence hierarchy existed: the **codebook template** (conventions Section 2) defined confidence criteria as a function of evidence source type (HIGH = "cite specific legislation", MEDIUM = "general pattern", LOW = "inferring from regime type"). This was essentially a proto-hard-cap baked into variable definitions. Updated to reflect the new design: confidence = certainty about the score (well-determined / reasonable judgment / uncertain), with an explicit NOTE that evidence source quality is captured separately by `evidence_tier`.

Also aligned `uncertainty_reason` description in conventions CSV schema with production-protocol (added "MUST include justification if HIGH + Tier 3/4").

### Files Modified

1. **conventions.md** — Section 2 (codebook template: confidence criteria rewritten), Section 3 (Rule 11), Section 5 (TIER_INFLATED + audit log), Section 7 (prompt template: Rule 6 + output field #4 + CSV schema + uncertainty_reason description), new Section 20
2. **production-protocol.md** — 11 Coding Rules (Rule 11), prompt template (Rule 6 + output field #4), CSV schema, `current_batch.json` schema, new Evidence Source Hierarchy section, sync note
3. **SKILL.md** — Post-batch checks (tier monitoring + inflation), rolling context update (mean tier), JSON contents list
4. **.context/README.md** — Rolling context templates (Evidence Quality section), coding_rules_summary reference

## Final Audit (Phase 8l)

Comprehensive final audit of the entire `/create-dataset` workflow using 3 parallel audit agents:
1. **Cross-file consistency audit** — CSV schema parity, prompt template parity, rule numbering, section references, thresholds, terminology
2. **SKILL.md completeness audit** — step completeness, interview questions, subagent spec, post-batch checks, rolling context, flow gaps, error handling, resume logic
3. **Dead code / orphaned features audit** — orphaned sections, missing implementations, contradictions, stale references, hook config, quality gates

### CRITICAL Findings Fixed

1. **Gold-standard auto-fail contradicts opt-out** — `quality-gates.md` and CLAUDE.md listed "No gold-standard validation" as auto-fail (-100), but the workflow explicitly supports gold-standard opt-out (conventions Section 16, SKILL.md Step 2e). Fixed: auto-fail now requires *undocumented* absence; documented opt-out is a Major deduction (-15).

2. **Section numbering out of order** — Section 10 (Common Pitfalls) appeared after Sections 11 and 12 in conventions.md. Moved to correct sequential position (between Sections 9 and 11).

### MAJOR Findings Fixed

3. **`coding_rules_summary` renumbering** — The compact summary in `current_batch.json` had merged/renumbered rules (e.g., rules 2+3 merged, rule 6 moved to position 3, de facto/de jure inserted as rule 9). Rewrote to maintain strict 1:1 correspondence with the canonical 11-rule numbering, with de facto/de jure as an ADDITIONAL rule.

4. **Interview question numbering collision** — Phase 0c.5 question 8 (majority voting) and Phase 0d question 8 (bridge cases) were different questions with the same number. Renumbered Phase 0d: 8→9, 8b→9b, 9→10, 10→11, and Phase 0e: 11→12, 12→13, 13→14, 14→15, 15→16.

5. **Tier distribution missing from rolling context update** — SKILL.md Step 3 item 6 only mentioned mean evidence tier, but `.context/README.md` template includes tier distribution (T1/T2/T3/T4 percentages). Added tier distribution to the update instructions.

6. **Tier-confidence mismatch flag destination unspecified** — Post-batch check computed the rate but didn't say where to put it. Added: rolling context Alerts AND batch summary presented to user.

7. **Hallucination HARD STOP no recovery path** — Conventions Section 5 said "HARD STOP" but gave no guidance on what to do next. Added recovery protocol: examine 5 worst fabrications → variable-specific fix or codebook redesign → max 2 retry cycles.

8. **Section 17 "Add a 10th mandatory section" duplicated Section 9 item 10** — Section 9 already listed downstream correction as item 10. Section 17 redundantly said "Add a 10th mandatory section" with the same content. Replaced with a cross-reference to Section 9 item 10.

### MINOR Findings Fixed

9. **Prompt template parity** — Two micro-differences between conventions Section 7 and production-protocol prompt templates: "from codebook" and "loaded from disk" annotations. Aligned production-protocol to match conventions (authoritative source).

10. **`uncertainty_reason` description** — Parenthetical vs sentence form between files. Aligned to sentence form.

### Acknowledged (Not Fixed — Design Decisions)

- **`--resume step-N` format doesn't accommodate sub-steps (1b, 2a-2f, 3b)** — Step 3 has resume via `batch_queue.next_batch_id`. Earlier steps are interactive and rarely need resume. Would add complexity without clear benefit. Documented as a known limitation.
- **SessionStart `compact` matcher** — Validity depends on Claude Code's hook implementation. Cannot verify without runtime testing. The script is fail-open, so worst case is no re-injection (user can manually read batch_briefing.md).
- **`log-reminder.py` not documented in workflow files** — This is a general-purpose session management hook, not dataset-specific. Its behavior is self-explanatory from the script.
- **Country-first rolling context template lacks "Bridge Cases" section** — Intentional: country-first mode has bridge cases in the variable summary, not per-country context.

### Files Modified

1. **quality-gates.md** — Gold-standard auto-fail split into undocumented (auto-fail) vs documented opt-out (-15)
2. **CLAUDE.md** — Quality gates table updated to match
3. **conventions.md** — Section 10 moved to correct position, hallucination HARD STOP recovery added, Section 17 duplication removed
4. **production-protocol.md** — `coding_rules_summary` rewritten with 1:1 canonical numbering, prompt template micro-differences aligned, `uncertainty_reason` description aligned
5. **SKILL.md** — Interview questions renumbered (Phase 0d: 9-11, Phase 0e: 12-16), tier distribution added to rolling context update, tier-confidence mismatch flag destination specified

---

## Phase 9: Variable Curation (Phase 0.5)

**Goal:** Add an optional Variable Curation step between the pre-coding interview (Step 0) and codebook design (Step 1) that transforms a large brainstormed variable list into a curated, prioritized, costed set.

**Motivation:** The workflow had a gap — it jumped from "what is your concept?" directly to "let's design full codebook entries for every variable." When a user arrives with 160+ brainstormed variables (like the secularization example in `variable_list_example.txt`), Step 1 would naively build codebook entries for all of them. Phase 0.5 fills this gap.

**Critical assessment before building:** Identified 8 problems with the initial proposal:
1. Six independent lenses is wrong decomposition — decisions are entangled → one integrated pass per dimension
2. Missing the most important lens: "what is your research question?" → every recommendation ties back to RQ
3. Comparability lens too simplistic → structured assessment: coverage estimate, temporal variation profile, cross-context validity
4. Missing dimension-level assessment → Pass 1 evaluates dimensional architecture before variable triage
5. Codability assessment too vague → evidence tier distribution + de jure/de facto gap + knowledge cutoff risk
6. Output format wrong (flat list vs tiered) → Core / Recommended / Optional / Drop
7. Interaction with Step 1 unclear → Phase 0.5 recommends scale *type* only; Step 1 designs scale *content*
8. No gap analysis for missing variables → Pass 4 suggests additions, clearly marked as Claude-proposed

**Implementation (4 passes):**
- Pass 1: Dimension Architecture Review — conceptual distinctness, alignment with RQ, gaps
- Pass 2: Variable-Level Triage — 6 lenses (relevance, redundancy, coverage, temporal profile, codability, scale type) evaluated simultaneously per variable, one table per dimension
- Pass 3: Cost-Benefit Summary — tier counts + cell/cost projections per configuration
- Pass 4: Gap Suggestions — Claude-proposed additions, max 10-15

**Files modified:**
1. **SKILL.md** — Pipeline diagram updated, Phase 0.5 section added (Passes 1-4, output templates, GATE), Step 0 adaptive follow-up added after Q2, Step 0 GATE updated, Step 0e Q16 range estimate, Step 1 conditional for curated vs from-scratch
2. **conventions.md** — Section 21 (Variable Curation Standards) added with tier definitions, 6 lenses, flag variable rules, cost estimation, 7 rules. Frontmatter paths updated. Integration Points updated.
3. **CLAUDE.md** — Pipeline diagram updated, folder structure updated with curation artifacts

**Verification:** 14/14 checks pass (pipeline diagram, section content, cross-references, frontmatter, Integration Points, CLAUDE.md, no production-protocol changes, question numbering preserved, section ordering)
