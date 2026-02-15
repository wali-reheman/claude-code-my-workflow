# Session Log: Dataset Coding Workflow Improvements

**Date:** 2026-02-13
**Goal:** Fix remaining bugs, add pre-coding interview, coding strategies, country narratives, and assess country expertise triggering.

## Context

Continued from previous session that created two standalone template folders (polisci-research-paper and polisci-dataset-coding). This session focuses exclusively on the dataset-coding workflow.

## Phase 1: Bug Fixes (from previous session's hostile audit)

### Fixes Applied

1. **`coding_progress.json` schema undefined** — Added full JSON schema with calibration, batches, bridge cases, timestamps to conventions Section 7
2. **`bridge_cases.csv` schema undefined** — Added 7-column CSV schema
3. **Production prompt missing rules 7-9** — Embedded "no uniform blocks", "overconfidence correction", "regional comparison" as RULES directly in the prompt template
4. **Batch file naming collision** — `coded_[region].csv` → `coded_[concept]_[region].csv` everywhere
5. **Pilot output path undefined** — `pilot_results.csv` → `Replication/data/coded/pilot_[concept].csv`
6. **Robustness checklists bloat** — Stripped Modules A-X (830 lines of irrelevant methodology modules), kept only Module Y (47 lines)
7. **Orphaned critic-fixer sub-loop** — Removed from orchestrator
8. **R code paths** — All R snippets now reference correct `Replication/data/coded/` and `Replication/data/raw/` paths
9. **`--resume` path references** — SKILL.md specifies full paths and points to conventions for schemas

## Phase 2: Pre-Coding Interview (Step 0 Redesign)

Replaced the old "Scope & Load" Step 0 with a phased interview:
- **0a: Research Context** — project purpose, concept definition, dataset gaps, audience
- **0b: Scope Decisions** — state system, micro-states, temporal gaps (existing table, now highlighted per-concept)
- **0c: Coding Strategy** — country-first vs variable-first with recommendation logic
- **0d: Comparability Safeguards** — bridge cases, per-variable benchmarks, ambiguous test cases
- **0e: Technical Setup** — load conventions, memory, handle --resume/--audit

Key design decision: interview is phased (ask, wait, adapt), NOT a configuration dump.

## Phase 3: Coding Strategies (Step 3 Redesign)

Added `--strategy country-first/variable-first` flag.

**Country-first:** Code one country through full codebook before moving on. Best for small-N, interrelated variables, narrative generation.
- File naming: `coded_[concept]_[country_cow_code].csv`
- Includes within-country consistency check

**Variable-first:** Code one variable across all countries before moving on. Best for large-N, independent variables, benchmark calibration.
- File naming: `coded_[concept]_[variable]_[region].csv`
- Bridge cases re-anchor at start of each variable

Added conventions Section 11 with full protocols, risks, and mitigations for each strategy.

## Phase 4: Country Narratives (Step 3b)

Added `--narratives` flag and new Step 3b. For each coded country:
- Context paragraph → per-variable transition explanations → cross-variable synthesis → coverage uncertainty
- Citations with DOIs/URLs for every transition
- Stable periods summarized briefly, transitions explained in detail
- Country-first: generates inline (context is fresh). Variable-first: generates post-hoc.

Added conventions Section 12 with full markdown template.
Updated coding-reliability-reviewer with Lens 7 (narrative consistency checks).

## Phase 5: Country Expertise Assessment

Traced how country-specific knowledge currently enters the coding prompt. Found:
- **Only mechanism:** Production Prompt Template says "[COUNTRY] in [YEAR]" and relies on Claude's training data
- **Methodological Context** field is per-variable (concept keywords), NOT per-country
- **Step 3 "Load context"** loads codebook + bridge cases + progress — nothing country-specific
- **Uploaded PDFs** inform codebook design but aren't re-loaded during production coding

Gap identified: no structured country-level context injection. The workflow trusts training data + confidence system + hallucination audit as detection, but has no prevention mechanism.

## Key Decisions

- Interview is phased conversation, not configuration dump
- Country-first recommended for < 5 countries or when --narratives used
- Variable-first recommended for large-N panels
- Narratives generate inline for country-first, post-hoc for variable-first
- Country expertise triggering identified as the next major gap to address

## Files Modified

- `.claude/skills/create-dataset/SKILL.md` — major: interview, strategies, narratives, new args
- `.claude/rules/dataset-construction-conventions.md` — major: schemas, rules in prompt, Sections 11-12
- `.claude/agents/coding-reliability-reviewer.md` — Lens 7 (narratives), interview inventory check
- `.claude/rules/robustness-checklists.md` — stripped to Module Y only
- `.claude/rules/orchestrator-protocol.md` — removed critic-fixer sub-loop
- `CLAUDE.md` — updated pipeline, folder structure, skill descriptions

## Phase 6: Country Expertise Design (Envisioned, Not Built)

Discussed country briefing system design. Key decisions:
- Facts in, not persona on — structured factual scaffolds, NOT expert roleplay
- One brief per country per concept (at dimension level for multi-dimension codebooks)
- Briefs live in `Replication/data/coded/country_briefs/[concept]/[country]_[cow].md`
- Generated at Step 2a.5, auto-generated from training data, user reviews THIN briefs
- Injected into production prompt as COUNTRY CONTEXT block
- Country-first loads full brief; variable-first loads filtered rows by variable tags
- Self-assessed knowledge depth: STRONG/MODERATE/THIN with adaptive confidence criteria
- NOT YET IMPLEMENTED — awaiting user go-ahead

## Phase 7: Literature-Based Best Practices (7 Improvements)

Researched best practices from recent literature (2024-2026). Implemented 7 improvements:

### 1. Multi-Run Majority Voting (Wang et al. 2023, Carlson et al. 2025)
- Each cell coded 3 times independently, majority vote determines final score
- Vote distribution (3/3, 2/3, 0/3) replaces self-reported confidence as primary reliability measure
- 0/3 ties escalated to 4th run or human adjudication
- Per-run files stored in `runs/` directory, merged output in main files
- Disagreements tracked in `disagreements_[concept].csv`
- Files: conventions Section 13, SKILL.md Steps 2a/3 updated

### 2. Behavioral Pre-Testing (Halterman & Keith 2024)
- 5 tests before any coding: label compliance, definition recall, example classification, label semantics check, scale direction check
- ~50 API calls, catches fundamental codebook failures before pilot investment
- New Step 1b in pipeline
- Files: conventions Section 14, SKILL.md Step 1b added

### 3. Sentinel Drift Monitoring (OLAF Framework, Imran et al. 2025)
- 50 known-answer cells embedded in production batches without marking
- Checked every 10 batches: exact agreement and ICC vs known values
- Green/Yellow/Red alert thresholds with escalation protocol
- Files: conventions Section 15, SKILL.md Step 2f + Step 3 sentinel checks

### 4. Gold-Standard Validation Set (Egami et al. 2024, Carlson et al. 2025)
- 200+ expert-coded cells (up from 30-50), stratified sampling
- Serves triple duty: pilot validation, sentinel source, downstream correction input
- First-class project artifact in `gold_standard/` directory
- Coded BLIND — expert does not see Claude's scores
- Files: conventions Section 16, SKILL.md Step 2e

### 5. Inclusion/Exclusion Criteria (Halterman & Keith 2024)
- Added to codebook template: "Code X WHEN...", "Do NOT code X WHEN..."
- Boundary clarification: "Do NOT confuse this variable with..."
- Addresses finding that models rely on label semantics rather than definitions
- Files: conventions Section 2 updated, SKILL.md Step 1 updated

### 6. Prompt Variant Testing
- 3 semantically equivalent prompt variants tested on 10% of pilot cells
- Variant A: standard, Variant B: reversed scale order, Variant C: rephrased definition
- Cross-variant ICC >= 0.80 required
- Detects prompt fragility before production investment
- Files: SKILL.md Step 2b added

### 7. Downstream Bias Correction (Egami et al. 2024, NeurIPS)
- Documented that even 90%+ accurate AI labels produce biased regression coefficients
- Referenced Egami et al.'s DSL estimator with R code example
- Added mandatory 10th section to methodology transparency report
- Every paper using AI-coded data must apply correction or disclose non-correction
- Files: conventions Section 17, Section 9 updated to 10 sections

### Cross-Cutting Updates
- coding-reliability-reviewer: updated all 7 lenses + inventory + report template
- robustness-checklists.md: restructured into Pre-Coding, Calibration, Production, Extended, Coverage sections; 9 new citations; 7 new common mistakes
- quality-gates.md: 8 new deduction items across Critical/Major/Minor
- CLAUDE.md: updated pipeline diagram, folder structure, quality gates table, "What Human Teams Get" comparison

## Files Modified (Phase 6-7)

- `.claude/rules/dataset-construction-conventions.md` — Sections 13-17 added (majority voting, pre-testing, sentinels, gold-standard, DSL); Section 2 updated (inclusion/exclusion); Section 7 updated (CSV schema); Section 9 updated (10 sections)
- `.claude/skills/create-dataset/SKILL.md` — Steps 1b, 2b, 2e, 2f added; Steps 2a, 3, 3b, 5 updated for majority voting and sentinels; Step 0 updated with reliability strategy decision; "What This Skill Does" list expanded
- `.claude/agents/coding-reliability-reviewer.md` — All 7 lenses updated; inventory expanded; report template statistics table expanded; "What This Agent Does" list expanded
- `.claude/rules/robustness-checklists.md` — Checklist restructured into 5 sections; 9 citations added; 7 common mistakes added
- `.claude/rules/quality-gates.md` — 8 new deduction items in AI-Coded Datasets rubric
- `CLAUDE.md` — pipeline, folder structure, quality gates, comparison table, getting started all updated

## Open Questions

- Country briefing system designed but not implemented — awaiting user go-ahead
- Batch API architecture (generate JSONL → submit to Anthropic Batch API) identified as future evolution for 100K+ cell projects — not built yet
- Turkey/MENA example codebook discussed — user may start actual coding soon
