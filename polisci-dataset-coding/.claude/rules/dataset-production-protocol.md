---
paths:
  - "Replication/data/coded/*.csv"
  - "Replication/data/coded/runs/**"
  - "Replication/data/coded/.context/**"
  - "Replication/data/coded/coding_progress.json"
---

# Dataset Production Protocol

**Purpose:** Lean rules for production coding (Step 3). This file auto-loads when touching coded CSV files, run outputs, or context files. For codebook design, calibration, and documentation rules, see `dataset-construction-conventions.md`.

> **Sync note:** The production prompt template and CSV schema in this file mirror Section 7 of `dataset-construction-conventions.md`. The conventions file is the **authoritative source**. If you modify the prompt template or CSV schema, update BOTH files. Last synced: 2026-02-14 (Phase 8k: evidence source hierarchy — reasoning scaffold, soft signal, post-hoc audit column).

---

## The 11 Coding Rules

Every production coding prompt must comply with all of these:

1. **Confidence is mandatory** — every cell gets HIGH, MEDIUM, or LOW
2. **Evidence is mandatory** — 1-2 sentences citing specific events, laws, institutions, or documented patterns
3. **Evidence must be dated** — the evidence must reference something that occurred BEFORE December 31 of the coding year
4. **No invented specifics** — if uncertain about a detail, say so rather than fabricating
5. **UNABLE_TO_CODE is always available** — better NA with an honest reason than a coded guess
6. **Temporal boundary** — code as of December 31 of the year. Do not use knowledge of events after this date
7. **No uniform blocks** — if coding > 5 consecutive identical scores for the same country, pause and justify each individually
8. **Overconfidence correction** — if > 70% of cells in any batch are HIGH confidence, pause and re-examine 5 HIGH cells
9. **Comparison** — variable-first: compare to others in the regional batch; country-first: compare to cross-country distribution in the variable summary
10. **Acknowledge uncertainty** — for MEDIUM and LOW confidence, state the specific reason
11. **Evidence hierarchy** — classify evidence tier (1-4) BEFORE scoring. Tier 3/4 triggers active search for better evidence. HIGH confidence with Tier 3/4 requires explicit justification in uncertainty_reason.

---

## Production Prompt Template

**Structure follows "Lost in the Middle" research: rules at beginning (highest attention), reference material in middle, reminders at end (attention recovers).**

```
RULES (read these FIRST — they govern all coding below):
1. Temporal boundary: Code as of December 31, [YEAR]. Do NOT use knowledge
   from events after this date.
2. If assigning > 5 consecutive identical scores for this country, STOP and
   justify each year individually.
3. UNABLE_TO_CODE is always available — prefer honest NA over a guess.
4. No invented specifics — if uncertain, say so.
5. [IF DE FACTO]: Code ACTUAL PRACTICE, not law on paper. A constitutional
   provision or law that is unenforced, circumvented, or contradicted by
   practice should be noted as context but NOT determine the score.
   Evidence must document what actually happens — not just what the law says.
   [IF DE JURE]: Code the formal legal/institutional framework as written.
   [OMIT RULE 5 ENTIRELY if codebook does not specify de jure/de facto.]
6. Evidence hierarchy — BEFORE assigning a score, classify your evidence:
   Tier 1 (specific dated event/action) → strongest basis, assign directly.
   Tier 2 (institutional description of practice) → solid basis.
   Tier 3 (scholarly characterization) → indirect. Actively search for
     something more concrete. If nothing exists, consider whether the
     characterization is precise enough to determine a score.
   Tier 4 (general inference/undated claim) → weakest. Consider
     UNABLE_TO_CODE. If you assign a score, it must be tentative.
   If your best evidence is Tier 3 or 4 AND you assign HIGH confidence,
   you MUST explain why in the uncertainty_reason field.

INSTRUCTIONS — Output exactly:
1. Score: [integer on the scale, or UNABLE_TO_CODE]
2. Confidence: HIGH / MEDIUM / LOW
3. Evidence: 1-2 sentences citing a specific event, action, institution, or
   documented pattern. Include a DATE for the evidence.
   [IF DE FACTO]: Evidence must document actual practice or enforcement, not
   just the legal text. Legal provisions may be cited as context (e.g.,
   "although the constitution states X, in practice Y"), but the score
   must reflect reality, not the statute book.
4. Evidence Tier: 1 / 2 / 3 / 4
   1 = specific dated event, action, or document
   2 = credible institutional source describing practice
   3 = scholarly characterization
   4 = general inference or undated claim
5. If MEDIUM or LOW: explain the specific reason for uncertainty
6. If UNABLE_TO_CODE: explain what knowledge is missing
7. Comparison:
   [VARIABLE-FIRST]: Regional comparison — briefly note how this score
     compares to others in this batch already coded.
   [COUNTRY-FIRST]: Cross-country comparison — briefly note how this
     score compares to the cross-country distribution for this variable
     (see VARIABLE SUMMARY below). Flag if this country appears to be
     an outlier (> 1.5 SD from the cross-country mean).

--- VARIABLE DEFINITION ---
[Full definition from codebook, including inclusion/exclusion criteria]

--- SCALE ---
[Full scale with anchor examples from codebook]

--- BRIDGE CASE REFERENCE (for calibration) ---
[Bridge case country] ([era label], [year_start]-[year_end]):
  [VARIABLE-FIRST]: [score] (this variable only)
  [COUNTRY-FIRST]: {var1: score, var2: score, ...}
NOTE: Bridge scores are ERA-SPECIFIC. Use the bridge score whose era
overlaps with the year you are currently coding. If a bridge country
has multiple eras, the transition itself is informative.

--- ROLLING CONTEXT ---
[Contents of .context/variable_*.md or .context/country_*.md — loaded from disk]

--- VARIABLE SUMMARY (country-first only) ---
[Contents of .context/variable_summary.md — cross-country score distributions]
[Omit this section entirely for variable-first strategy]

REMINDERS (check these AFTER coding):
- After completing this batch: if > 70% of cells are HIGH confidence,
  re-examine 5 HIGH cells and consider downgrading to MEDIUM.
- Compare this country to bridge cases and the cross-country distribution.
- Check: does this score tell a coherent story with adjacent years?
```

---

## Output CSV Schema

| Column | Type | Description |
|---|---|---|
| cow_code | integer | COW country code |
| country_name | string | Country name |
| year | integer | Coding year |
| variable | string | Variable name |
| score | integer or NA | Coded score (NA if UNABLE_TO_CODE) |
| confidence | string | HIGH / MEDIUM / LOW / NA |
| evidence | string | Evidence citation with date |
| evidence_date | integer | Year of the cited evidence |
| evidence_tier | integer (1-4) or NA | Evidence source tier: 1=specific dated event/action, 2=institutional source, 3=scholarly characterization, 4=general inference. NA if UNABLE_TO_CODE. See conventions Section 20. |
| uncertainty_reason | string | Reason for non-HIGH confidence. MUST include justification if HIGH confidence + Tier 3/4 evidence. |
| batch_region | string | Which regional batch |
| coding_pass | integer | 1 = first pass, 2 = dual-pass recode |
| run_id | integer | Majority voting run (1, 2, or 3). Only in raw run files. |
| vote_agreement | string | "3/3", "2/3", or "0/3". Only in merged output. |
| final_score | integer or NA | Majority-vote score. Replaces `score` in final output. |

---

## Majority Voting Rules

Each cell is coded 3 times independently. Each run = one Task-tool subagent with isolated context.

| Vote Pattern | Final Score | Agreement | Action |
|---|---|---|---|
| 3/3 agree (e.g., 2, 2, 2) | Majority (2) | `3/3` | Accept |
| 2/3 agree (e.g., 2, 2, 1) | Majority (2) | `2/3` | Flag minority for review |
| 0/3 agree (e.g., 1, 2, 3) | None | `0/3` | Escalate: 4th run or human |
| UNABLE_TO_CODE in 2/3+ | UNABLE_TO_CODE | — | Accept |
| UNABLE_TO_CODE in 1/3, other 2 agree | Majority score | — | Flag as UNABLE_IN_MINORITY |
| UNABLE_TO_CODE in 1/3, other 2 disagree | None | — | Escalate to human |

**File structure:**
```
Replication/data/coded/
├── runs/                              # Raw per-run outputs
│   ├── run1_coded_[concept]_[batch].csv
│   ├── run2_coded_[concept]_[batch].csv
│   └── run3_coded_[concept]_[batch].csv
├── coded_[concept]_[batch].csv        # Majority-vote merged
└── disagreements_[concept].csv        # All < 3/3 cells
```

**Subagent isolation:** Each run is a Task-tool subagent (type: general-purpose) with a fresh context window. The subagent:
- Reads: `current_batch.json` ONLY (self-contained — includes prompt template, variable def, bridge cases with per-variable scores, rolling context, variable summary [country-first], CSV schema, and all coding rules)
- Writes: run CSV to path specified in the Task prompt (NOT in `current_batch.json` — each run gets its own path)
- Returns: summary only (N cells, score distribution, bridge case values)
- Does NOT see: other runs' results, parent conversation, full conventions, or auto-loaded rules files

**`current_batch.json` schema** (fully self-contained — subagents read ONLY this file):
```json
{
  "batch_id": "clergy_appointment_mena",
  "concept": "religious_governance",
  "variable": "clergy_appointment",
  "region": "middle_east",
  "cells": [
    {"cow_code": 630, "country_name": "Iran", "year": 2000, "variable": "clergy_appointment"},
    {"cow_code": 640, "country_name": "Turkey", "year": 2000, "variable": "clergy_appointment"}
  ],
  "prompt_template": "RULES (read these FIRST):\n1. Temporal boundary: ...",
  "variable_definition": "### clergy_appointment: ...\n**Scale:**\n| Score | ...",
  "scale": "0 = Full state control ... 4 = Independent",
  "bridge_cases": [
    {"country": "Turkey", "cow_code": 640, "era": "AKP era", "year_start": 2002, "year_end": 2023,
     "scores": {"clergy_appointment": 2, "religious_court": 0, "relig_education": 1}, "source": "pilot"},
    {"country": "Turkey", "cow_code": 640, "era": "Kemalist", "year_start": 1923, "year_end": 2001,
     "scores": {"clergy_appointment": 4, "religious_court": 0, "relig_education": 3}, "source": "pilot"},
    {"country": "Iran", "cow_code": 630, "era": "Islamic Republic", "year_start": 1979, "year_end": 2023,
     "scores": {"clergy_appointment": 0, "religious_court": 0, "relig_education": 0}, "source": "pilot"},
    {"country": "Iran", "cow_code": 630, "era": "Pahlavi", "year_start": 1925, "year_end": 1978,
     "scores": {"clergy_appointment": 3, "religious_court": 1, "relig_education": 3}, "source": "pilot"},
    {"country": "Egypt", "cow_code": 651, "era": "Nasser", "year_start": 1952, "year_end": 1970,
     "scores": {"clergy_appointment": 3, "religious_court": 1, "relig_education": 2}, "source": "pilot"},
    {"country": "Egypt", "cow_code": 651, "era": "Sadat/Mubarak", "year_start": 1971, "year_end": 2012,
     "scores": {"clergy_appointment": 3, "religious_court": 1, "relig_education": 1}, "source": "pilot"},
    {"country": "Egypt", "cow_code": 651, "era": "post-2013", "year_start": 2013, "year_end": 2023,
     "scores": {"clergy_appointment": 3, "religious_court": 1, "relig_education": 1}, "source": "pilot"}
  ],
  "rolling_context": "# Rolling Context: clergy_appointment\n...",
  "variable_summary": "# Variable Summary — Cross-Country Calibration\n...(country-first only, omit for variable-first)",
  "csv_columns": ["cow_code", "country_name", "year", "variable", "score", "confidence", "evidence", "evidence_date", "evidence_tier", "uncertainty_reason", "batch_region", "coding_pass", "run_id"],
  "coding_rules_summary": "1. Confidence mandatory (HIGH/MEDIUM/LOW). 2. Evidence mandatory — 1-2 sentences citing specific events, laws, institutions, or documented patterns. 3. Evidence must be dated — before Dec 31 of coding year. 4. No invented specifics — if uncertain, say so. 5. UNABLE_TO_CODE always available — better NA than a guess. 6. Temporal boundary: code as of Dec 31 of the year. 7. No >5 consecutive identical scores without individual justification. 8. Overconfidence check: if >70% HIGH in a batch, re-examine 5 HIGH cells. 9. Comparison (variable-first: regional; country-first: cross-country distribution). 10. Acknowledge uncertainty: for MEDIUM/LOW, state specific reason. 11. Evidence hierarchy: classify tier (1-4) BEFORE scoring. Tier 1=specific dated event, Tier 2=institutional description, Tier 3=scholarly characterization, Tier 4=general inference. For Tier 3/4: actively search for better evidence. HIGH confidence with Tier 3/4 MUST be justified in uncertainty_reason. ADDITIONAL (if applicable): [IF DE FACTO]: Code ACTUAL PRACTICE — law on paper that is unenforced does NOT determine the score."
}
```

**Why self-contained:** Task-tool subagents do NOT inherit auto-loaded rules files from the parent session. They get a fresh context window. Everything the subagent needs must be either (a) in `current_batch.json` or (b) in the Task prompt itself. The output path is in the Task prompt (per-run), not in `current_batch.json` (per-batch).

**Subagent failure handling:**
After each subagent returns, the orchestrator verifies:
1. **CSV exists** at the expected path
2. **Column headers match** the expected schema (all `csv_columns` present)
3. **Row count matches** the number of cells in `current_batch.json`
4. **Score values are valid** (integers within scale range, or NA for UNABLE_TO_CODE)

If any check fails:
- **Retry once** — spawn a new Task subagent for that run_id only (same prompt, fresh context)
- **If retry fails** — mark that run as FAILED, proceed with remaining runs:
  - 2 valid runs that agree → use their majority
  - 2 valid runs that disagree → escalate to human
  - Only 1 valid run → flag entire batch for manual review

---

## Sentinel Drift Monitoring

50 known-answer cells embedded in production batches without marking.

**Check interval:** Every 10 batches (configurable in `coding_progress.json`).

| Metric | Green | Yellow | Red |
|---|---|---|---|
| Exact agreement | >= 85% | 70-84% | < 70% |
| ICC | >= 0.80 | 0.65-0.79 | < 0.65 |
| Delta from prev | < 0.05 | 0.05-0.10 | > 0.10 |

**Yellow:** Log warning, increase hallucination spot-check rate (5 -> 10 per batch).
**Red:** PAUSE coding. Investigate domain shift, context pressure, or prompt compliance. Re-calibrate the most recent batch.

---

## Data-Sparsity Hallucination Escalation

**Purpose:** Sentinel drift monitoring catches *global* quality degradation, but misses *country-specific* hallucination spikes. When coding moves from well-documented countries (Turkey, Egypt) to data-sparse ones (Oman, Bahrain, pre-unification Yemen), fabrication risk increases even if sentinels stay green. This protocol detects data-sparsity signals within each batch and escalates automatically.

**After each batch merge, compute these batch-level indicators:**

| Indicator | Threshold | Signal |
|---|---|---|
| UNABLE_TO_CODE rate | > 20% of cells in batch | Data-sparse country/period |
| LOW confidence rate | > 40% of cells in batch | Thin evidence base |
| 0/3 majority vote rate | > 10% of cells in batch | High ambiguity |
| Evidence word count (mean) | < 15 words per cell | Terse/vague citations |

**Escalation rules (base rates depend on gold-standard status):**

| Indicators Triggered | With Gold-Standard | Without Gold-Standard |
|---|---|---|
| 0 (normal) | 5-citation spot-check | 10-citation spot-check |
| 1 (ELEVATED) | 10-citation spot-check | 15-citation spot-check |
| 2+ (HIGH) | 15-citation spot-check | 20-citation spot-check |

- **ELEVATED:** Log warning.
- **HIGH:** Log alert to rolling context. Flag batch in `coding_progress.json` with `"sparsity_alert": true`.
- **If spot-check finds ANY fabricated citation at ELEVATED or HIGH level:** PAUSE and escalate to user. The hallucination rate for data-sparse countries may be systematically higher than the pilot estimate.

**This is automatic — the orchestrator computes indicators after Step 5 (post-batch checks) and adjusts the spot-check count before executing it.** No user intervention needed unless a fabricated citation is found at elevated levels.

**Logging:** Add to `coding_progress.json` per batch:
```json
"sparsity_indicators": {
  "unable_to_code_rate": 0.25,
  "low_confidence_rate": 0.45,
  "zero_agreement_rate": 0.05,
  "mean_evidence_words": 12,
  "escalation_level": "HIGH",
  "spot_check_count": 15
}
```

---

## No-Gold-Standard Compensating Checks

**Activate automatically when `gold_standard_opted_out: true` in `coding_progress.json`.** Run at reduced intensity even when gold-standard IS present (useful for all projects). See conventions Section 19 for full specification.

### Temporal Monotonicity Check (post-batch)

After each batch merge, scan for **year-over-year score changes ≥ 2** within the same country × variable. For each flagged jump, check if the evidence field mentions a major event (keywords: "coup", "revolution", "reform", "constitution", "abolished", "established", "war", "independence", "amendment", "law").

- **Without gold-standard:** Flag jumps lacking major-event evidence for re-examination
- **With gold-standard:** Log only (report in batch summary, don't flag)
- **Scope:** Consecutive years only. Does NOT flag era boundary transitions. Threshold ≥ 2 (single-point changes are normal).

### Cross-Variable Coherence Check (post-country)

After completing each country (country-first) or after all variables are coded (variable-first), check for logically incoherent score profiles using `coherence_rules` from `coding_progress.json`.

- **Without gold-standard:** Flag country-years with 2+ coherence violations for re-examination
- **With gold-standard:** Report only (log in batch summary)
- **Coherence rules** define expected variable pair correlations. Pairs violating by > 2 scale points are flagged.

---

## Evidence Source Hierarchy

**Purpose:** Guides Claude's reasoning before scoring, provides post-hoc audit signal for researchers. See conventions Section 20 for full specification.

### The 4 Tiers (specificity of claim, not source prestige)

| Tier | What Qualifies |
|---|---|
| **1** | Specific dated event, action, or document directly referenced |
| **2** | Credible source describing institutional practice (no single dateable event) |
| **3** | Scholarly characterization — interpretation, not primary observation |
| **4** | General inference, undated claim, or regime-type reasoning |

### Role in Coding

Tiers are a **reasoning scaffold** (Rule 6 in the prompt), not a hard confidence cap:
- Claude classifies evidence BEFORE scoring → forces reflection on evidence quality
- Tier 3/4 + HIGH confidence → MUST justify in `uncertainty_reason` field
- Tier 4 → Claude should actively consider UNABLE_TO_CODE before assigning a score

**No hard caps on confidence.** Tiers create friction, not prohibition. Researchers use `evidence_tier` for targeted post-hoc review (e.g., filter for `tier >= 3 AND confidence == HIGH`).

### Post-Batch Tier Monitoring

After each batch merge, compute:
- **Mean evidence tier** for the batch. If > 2.5 → flag as evidence-poor in rolling context Alerts
- **Tier-confidence mismatch rate**: % of cells with `tier >= 3 AND confidence == HIGH`. If > 20% without justification → flag for review

### Hallucination Audit: Tier Inflation

When spot-checking evidence citations, verify the claimed `evidence_tier`:
- Tier 1 claim → evidence MUST reference a specific dateable event/action
- Tier 2 claim → evidence MUST reference a credible institutional source
- Mismatch → classify as **TIER_INFLATED** (new status). Threshold: < 15% inflation rate.

---

## CSV Validation Protocol

**Run BEFORE merging majority-vote results.** Each of the 3 run CSVs must pass all checks:

| Check | Condition | On Failure |
|---|---|---|
| File exists | CSV file present at expected path | Retry run (max 1 retry) |
| Headers match | All `csv_columns` from batch spec present | Retry run |
| Row count | Rows == number of cells in batch spec | Retry run |
| Score range | All scores within scale range or NA | Log warning, flag rows |
| Required fields | No blank `evidence` or `confidence` (except UNABLE_TO_CODE) | Log warning, flag rows |
| Run ID correct | All rows have correct `run_id` value | Fix automatically |

**Retry protocol:** If a run fails validation, spawn one new Task subagent with the same prompt and a fresh context. If the retry also fails, mark the run as FAILED (see Subagent failure handling above).

---

## Batch-to-Disk Protocol

After completing each batch (all 3 runs validated and merged):

1. **Validate** all 3 run CSVs (see CSV Validation Protocol above)
2. Write majority-vote merged CSV: `coded_[concept]_[batch].csv`
3. Write disagreements to `disagreements_[concept].csv` (append)
4. Update `coding_progress.json`: batch status, summary stats, bridge case values, cell counts
5. Update rolling context file (`.context/variable_*.md` or `.context/country_*.md`)
6. Write `.context/batch_briefing.md` with what-happened + what-next (this is the relay baton)

**All coded output goes to `Replication/data/coded/`.**

---

## Post-Country Calibration Checkpoint (Country-First Only)

After completing ALL batches for a country, before moving to next country:

1. **Update `variable_summary.md`** — OVERWRITE per-variable distribution table with current aggregate stats (N, mean, median, SD, min, max). OVERWRITE this country's row in the Country Means table.
2. **Anomaly check** (activates at N >= 5 countries; skip for first 4) — flag any variable where this country's mean deviates > 1.5 SD from cross-country mean. Log to Alerts in `variable_summary.md`. For N < 5: bridge calibration pulse (step 3) is the only cross-country check.
3. **Bridge calibration pulse** — re-code all bridge cases for all variables (single-run, not 3-run majority). Compare to pilot values. Deviation > 1 on ANY variable → PAUSE.
4. **Log** — append to `coding_progress.json` under `calibration.post_country_checks`.
5. **If drift detected** — YELLOW alert. User chooses: re-code, re-establish bridge values, or continue with monitoring.

---

## Context Management Protocol

### Dynamic Batch Sizing

Computed at Step 2f and stored in `coding_progress.json`:

```
cells_per_batch = floor((context_budget - overhead_tokens) / tokens_per_cell)
context_budget  = 120,000 tokens (60% of 200K window, room for reasoning)
tokens_per_cell = 120 (100 output + 20 input identifiers)
cap: max 80 cells per batch (judgment quality threshold)
```

### Variable-First Context Loading

Per subagent batch, load:
1. Production codebook: ONE variable section (~150 tokens)
2. Bridge cases: filtered to this variable (~100 tokens)
3. Rolling context: `.context/variable_[varname].md` (~300 tokens)
4. Cells to code: country x year list (~200 tokens)
5. Prompt template with rules (~400 tokens)

Total overhead: ~1,150 tokens. Remaining: ~195K for coding output.

### Country-First Context Loading

Per subagent batch, load:
1. Production codebook: ALL variables, medium format (~4,000 tokens)
2. Bridge cases: all, with per-variable scores (~500 tokens)
3. Rolling context: `.context/country_[cow].md` (~500 tokens)
4. Variable summary: `.context/variable_summary.md` (~600 tokens)
5. Years to code x all variables (~300 tokens)
6. Prompt template with rules (~400 tokens)

Total overhead: ~6,300 tokens. Remaining: ~189K for coding output.

### Rolling Context Update Protocol

**Who updates:** The main orchestrator, NEVER the subagents.

**When:** After all 3 runs complete and majority vote is computed:
1. Read current rolling context file
2. **Score Distribution** — OVERWRITE entirely with current aggregate stats (mean, median, range, per-region breakdown). Never append.
3. **Bridge Cases** — OVERWRITE with current values. If deviation > 1 from established pilot score, add to Alerts.
4. **Coding Decisions Log** — FIFO queue, max 10 entries. When adding entry 11, delete entry 1. Only log notable decisions: 2/3 cells, 0/3 cells, UNABLE_TO_CODE, or score that deviates > 1 from regional mean.
5. **Alerts** — DELETE resolved alerts (e.g., bridge case drift that was investigated and accepted). KEEP active alerts. Add new alerts from this batch.
6. **Size check** — If file exceeds ~500 tokens after update, compress Coding Decisions Log: keep only last 5 entries instead of 10. If still over, summarize Score Distribution to one line per region.

### Batch Briefing Protocol

Written at end of each batch as `.context/batch_briefing.md`:

```markdown
# Batch Briefing (auto-generated for next session)

**Status:** COMPLETED | IN_PROGRESS | FAILED
**Timestamp:** [ISO 8601]

## What was just completed
- Batch: [batch_id] (Run [N] of 3 / Merged)
- Cells coded: [N] ([N] countries x [N] years)
- Bridge case agreement: [status]
- Majority vote: [N]% 3/3, [N]% 2/3, [N]% 0/3

## What to do next
1. [Next action: run 2, merge, next region, etc.]

## Active alerts
- [None / Yellow / Red with details]

## Key decisions from this session
- [Notable coding decisions, scope clarifications]

## Failed runs (if any)
- [Run N: reason for failure, retry status]
```

**Status values:**
- `COMPLETED` — batch fully merged, all post-checks passed, ready for next batch
- `IN_PROGRESS` — session ended mid-batch (e.g., context pressure). Resume from `batch_queue.next_batch_id`
- `FAILED` — batch failed validation/merge. Requires investigation before proceeding.

### PROJECT_MEMORY Auto-Learning

After each session, check for patterns worth remembering:
- Country consistently UNABLE_TO_CODE -> `[LEARN:dataset] [country] limited coverage`
- Bridge case drift -> `[LEARN:dataset] [country] bridge drift in [region]`
- High disagreement variable -> `[LEARN:dataset] [variable] high 2/3 rate, tighten criteria`

---

## Regional Batch Order

1. Latin America and Caribbean
2. Sub-Saharan Africa
3. Middle East and North Africa
4. South Asia
5. Southeast Asia
6. East Asia and Pacific
7. Post-Soviet / Central Asia
8. Central and Eastern Europe
9. Western Europe and Anglosphere

Bridge cases inserted at the START of every batch. Deviation > 1 point triggers investigation. Bridge cases are **era-specific** — filter to the era overlapping the batch's year range. If a batch spans an era boundary, include both eras.
