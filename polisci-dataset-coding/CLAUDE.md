# CLAUDE.MD — Political Science AI-Coded Dataset Construction

**Project:** [YOUR DATASET NAME]
**Institution:** [YOUR INSTITUTION]
**Working Branch:** main

---

## Quick Reference: Available Skills & Agents

| Command | What It Does |
|---------|-------------|
| `/create-dataset [concept]` | AI-coded dataset construction with pre-coding interview, strategy selection, calibration, narratives, and reliability |
| `/prep-data [task]` | Data processing: download existing datasets, standardize codes, merge panels |
| `/review-r [file]` | R code review: quality, reproducibility, correctness |
| `/reviewer-2` | Research design devil's advocate (includes Module Y for AI-coded data) |
| `/commit [message]` | Stage, commit, create PR, and merge to main |

**Agents:** `coding-reliability-reviewer`, `methodology-reviewer`, `r-reviewer`, `polisci-data-engineer`, `verifier`

---

## What This Workflow Does

This is a standalone template for constructing **original cross-national coded datasets** where Claude serves as the coder. It is designed for political science concepts like judicial independence, media freedom, electoral integrity, etc.

**This is NOT expert coding.** It is LLM-assisted measurement with systematic quality controls:
- Comprehensive pre-coding interview to define scope, strategy, and comparability goals
- Coding strategy choice: country-first (deep profiles) or variable-first (broad comparison)
- Behavioral pre-testing to verify Claude can follow the codebook before any coding
- Codebook with inclusion/exclusion criteria (Halterman-Keith format)
- Calibration against benchmark datasets
- Prompt variant testing to detect coding fragility
- Gold-standard validation set (200+ expert-coded cells) for validation, drift monitoring, and downstream correction
- 3-run majority voting with per-cell empirical reliability
- Sentinel drift monitoring throughout production coding
- Hallucination auditing of evidence citations
- Temporal boundary enforcement
- Country narratives with transition explanations and citations (optional)
- Downstream bias correction guidance (Egami et al. 2024)

Copy this folder to start a new dataset project. All skills, agents, and rules are self-contained.

---

## Folder Structure

```
[your-dataset]/
├── CLAUDE.md                          # This file
├── .claude/                           # Claude Code configuration
│   ├── settings.json                  # Project permissions + hooks
│   ├── rules/                         # Domain-specific rules (auto-loaded)
│   │   ├── dataset-construction-conventions.md  # THE reference document
│   │   ├── panel-data-conventions.md  # Country codes and merge protocols
│   │   ├── quality-gates.md           # Scoring rubrics (incl. AI-coded datasets)
│   │   ├── robustness-checklists.md   # Module Y for AI-coded data
│   │   └── ...                        # Other shared rules
│   ├── skills/                        # Slash commands
│   │   ├── create-dataset/            # The main workflow
│   │   ├── prep-data/                 # For merging with existing datasets
│   │   ├── review-r/                  # R code review
│   │   ├── reviewer-2/               # Methodology review
│   │   └── commit/                    # Git workflow
│   └── agents/                        # Specialized agents
│       ├── coding-reliability-reviewer.md  # THE review agent for coded data
│       ├── methodology-reviewer.md
│       ├── r-reviewer.md
│       ├── polisci-data-engineer.md
│       └── verifier.md
├── Replication/
│   ├── code/                          # R scripts for analysis
│   ├── data/
│   │   ├── raw/                       # Downloaded benchmark datasets
│   │   ├── processed/                 # Cleaned/merged datasets
│   │   └── coded/                     # AI-coded output (the product)
│   │       ├── codebook.md            # Variable definitions (incl/excl criteria)
│   │       ├── coding_progress.json   # Batch tracking + drift monitoring
│   │       ├── pretesting_results.md  # Behavioral pre-test results
│   │       ├── pilot_[concept].csv    # Pilot majority-vote codings
│   │       ├── coded_[concept]_*.csv  # Per-batch majority-vote data
│   │       ├── runs/                  # Raw per-run outputs (3 runs per batch)
│   │       │   └── run[1-3]_coded_[concept]_*.csv
│   │       ├── disagreements_[concept].csv  # All < 3/3 agreement cells
│   │       ├── majority_vote_summary.md     # Agreement statistics
│   │       ├── sentinel_cells.csv     # 50 known-answer drift monitors
│   │       ├── bridge_cases.csv       # Cross-regional calibration
│   │       ├── hallucination_audit_log.md
│   │       ├── interview_summary.md   # Pre-coding interview decisions
│   │       ├── curation_report.md    # Phase 0.5: variable curation analysis
│   │       ├── curated_variables.md  # Phase 0.5: approved variable list with tiers
│   │       ├── provenance.md          # Model version, dates, prompt hash
│   │       ├── methodology_transparency.md  # 10-section report
│   │       ├── gold_standard/         # Expert-coded validation set
│   │       │   ├── gold_standard.csv  # 200+ expert-coded cells
│   │       │   ├── sampling_design.md # How cells were selected
│   │       │   └── README.md          # ICC results + DSL instructions
│   │       ├── .context/              # Rolling context (NOT versioned — in .gitignore)
│   │       │   ├── README.md          # Context directory documentation
│   │       │   ├── batch_briefing.md  # Session relay baton
│   │       │   ├── codebook_production.md  # Compressed codebook
│   │       │   ├── current_batch.json # Subagent batch spec
│   │       │   ├── variable_*.md      # Per-variable rolling context
│   │       │   └── country_*.md       # Per-country rolling context
│   │       └── narratives/            # Country narratives (if --narratives)
│   │           ├── README.md          # Index of all narratives
│   │           └── [country]_[cow].md # One narrative per country
│   └── output/                        # Analysis output
├── master_supporting_docs/
│   ├── supporting_papers/             # Methodology papers
│   └── codebooks/                     # Existing dataset codebooks (V-Dem, Polity)
├── quality_reports/
│   ├── plans/                         # Saved implementation plans
│   └── session_logs/                  # Session history
├── scripts/                           # Utility scripts
│   ├── log-reminder.py               # Session log reminder hook (Stop)
│   └── session-context-loader.py     # Dataset progress injector (SessionStart)
└── PROJECT_MEMORY.md                  # Learned corrections
```

---

## Working Philosophy

### This Is LLM-Assisted Measurement, Not Expert Coding

Claude is a **systematic coder**, not an expert. The workflow manufactures quality controls:

| What Human Teams Get | What This Workflow Does Instead |
|---------------------|-------------------------------|
| Multiple independent coders | 3-run majority voting with per-cell agreement |
| Coder training and certification | Behavioral pre-testing + codebook with inclusion/exclusion criteria |
| Inter-coder reliability | ICC against gold-standard + majority vote agreement rates |
| Coder expertise verification | Hallucination audit of evidence citations |
| Disagreement resolution | Majority vote + human adjudication of 0/3 ties |
| Quality monitoring over time | Sentinel drift monitoring (50 embedded known-answer cells) |
| Measurement error correction | Gold-standard set + DSL estimator (Egami et al. 2024) |

### Context Window Management (The "Context Relay" Pattern)

For large-scale projects (5,000+ cells), the workflow uses **files on disk as external memory**:

- **Rolling context files** (`.context/`) carry cross-batch calibration — only the current variable or country is loaded
- **Subagent isolation** — each majority-vote run is a separate Task-tool subagent with a fresh context window
- **SessionStart hook** — auto-injects progress summary; re-injects batch briefing after auto-compaction
- **Two-tier codebook** — full codebook for design phases, compressed codebook for production (~98% token reduction for variable-first)
- **Rules file splitting** — design-time rules vs lean production protocol (~200 lines vs 900+)

See `dataset-construction-conventions.md` Section 18 and `dataset-production-protocol.md` for details.

### Plan-First Approach

For any non-trivial task, Claude enters plan mode first. Plans are saved to `quality_reports/plans/`.

### Continuous Learning

Tag corrections with `[LEARN:dataset]` — appended to `PROJECT_MEMORY.md`. Auto-learning during production coding detects patterns (bridge drift, coverage gaps, high disagreement) and appends `[LEARN:dataset]` entries automatically.

### Compact Instructions

When compacting during a `/create-dataset` session, preserve:
- Current batch state: variable, region, run number, batch_id
- Rolling context file paths (`.context/` directory)
- Any unwritten batch results or partial CSVs
- Coding decisions and scope clarifications from this session
- The batch briefing path (`.context/batch_briefing.md`)

---

## The Pipeline

```
/create-dataset judicial_independence --countries all --years 2000-2023 --narratives

Step 0:  INTERVIEW   -> Pre-coding interview: concept, scope, strategy, comparability
                        Choose: country-first or variable-first + majority voting decision
                        GATE: User confirms all decisions
Step 0.5: CURATE     -> (if variable list provided) Dimension review, variable triage,
                        cost-benefit by tier (Core/Rec./Optional/Drop), gap suggestions
                        GATE: User approves curated list
Step 1:  CODEBOOK    -> Design variables with anchors + inclusion/exclusion criteria
                        GATE: User approves
Step 1b: PRE-TEST    -> Behavioral pre-testing (5 tests: labels, recall, examples, semantics, direction)
                        GATE: All tests pass
Step 2:  PILOT       -> 50 countries x 5 years, 3 runs per cell (majority voting)
                        Prompt variant testing (3 variants, ICC >= 0.80)
                        Calibrate (ICC >= 0.75)
                        Hallucination audit (>= 80% verified)
                        Gold-standard: user codes 200+ cells
                        GATE: Gold-standard ICC >= 0.60
Step 2f: SENTINELS   -> Designate 50 sentinel cells from gold-standard
         + CONTEXT   -> Generate production codebook, compute batch sizing,
                        initialize rolling context files, enhance progress.json
Step 3:  PRODUCTION  -> Code with 3-run majority voting (subagent isolation)
                        Write to disk per batch, update rolling context
                        Sentinel drift check every 10 batches
Step 3b: NARRATIVES  -> (if --narratives) Country narratives with transitions + citations
Step 4:  EXTENDED    -> (optional) Prompt sensitivity, adversarial, construct validity
Step 5:  DOCS        -> Methodology transparency report (10 sections)
                        Majority vote statistics + drift report
                        Downstream bias correction guidance
                        Launch coding-reliability-reviewer
                        GATE: User reviews
```

---

## Quality Gates

| Threshold | Gate |
|-----------|------|
| Calibration ICC < 0.75 | Auto-fail |
| No gold-standard validation (undocumented) | Auto-fail |
| Gold-standard opted out (documented) | Major (-15) |
| Hallucination rate < 70% verified | Auto-fail |
| No behavioral pre-testing | Critical (-25) |
| No majority voting AND no sentinel monitoring | Critical (-20) |
| Gold-standard ICC < 0.60 | Major (-15) |
| Gold-standard < 200 cells | Major (-10) |
| No prompt variant testing | Major (-8) |
| No sentinel drift monitoring | Major (-10) |

Full rubric in `.claude/rules/quality-gates.md` under "AI-Coded Datasets".

---

## Key Rules (from dataset-construction-conventions.md)

1. **Confidence is mandatory** for every cell (HIGH/MEDIUM/LOW)
2. **Evidence must be dated** — before December 31 of the coding year
3. **UNABLE_TO_CODE is always available** — better NA than a guess
4. **No uniform blocks** — justify > 5 consecutive identical scores
5. **Never use "expert"** to describe Claude's coding in any output
6. **Write to disk after every batch** — never rely on context persistence

---

## Session Startup

```
Claude, please:
1. Read CLAUDE.MD
2. Read dataset-construction-conventions.md
3. Read PROJECT_MEMORY.md
4. Check quality_reports/plans/ for in-progress plans
5. Check Replication/data/coded/ for existing progress
6. State what you understand our goals to be
```

---

## Getting Started

1. Update this CLAUDE.md with your project details
2. Upload relevant codebook PDFs to `master_supporting_docs/codebooks/`
3. Upload methodology papers to `master_supporting_docs/supporting_papers/`
4. Run `/create-dataset "your concept" --countries [scope] --years [range]`
5. **Be ready to code 200+ cases by hand** during pilot (Step 2e) — this gold-standard set is the foundation for validation, drift monitoring, and downstream bias correction. Budget 4-8 hours of expert coding time.
