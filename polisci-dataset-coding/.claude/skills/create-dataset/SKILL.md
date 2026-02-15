---
name: create-dataset
description: Construct original AI-coded cross-national datasets with calibration, human validation, hallucination audit, and reliability testing. Follows dataset-construction-conventions.md.
argument-hint: "[concept, e.g., 'judicial independence'] [--countries region/list] [--years 2000-2023] [--benchmark vdem/polity/fh] [--strategy country-first/variable-first] [--narratives] [--extended] [--resume step-N] [--audit]"
---

# /create-dataset — AI-Coded Dataset Construction

Build original cross-national coded datasets where Claude serves as a systematic coder — regulated by calibration gates, hallucination audits, and mandatory human validation.

**Philosophy:** AI-coded data without external validation is opinion formatted as CSV. This workflow manufactures the quality controls that human coding teams get from disagreement between independent coders — through calibration against benchmarks, evidence verification, and mandatory human validation.

---

## What This Skill Does

1. Conducts a comprehensive pre-coding interview to define scope, strategy, and comparability goals
2. Designs codebooks with explicit scale anchors, inclusion/exclusion criteria, and UNABLE_TO_CODE provisions
3. Runs behavioral pre-tests to verify Claude can follow the codebook before any coding
4. Calibrates Claude's coding against benchmark datasets or proxy indicators before production
5. Runs a pilot with hallucination audit, prompt variant testing, and human validation gate
6. Establishes a gold-standard validation set for drift monitoring and downstream correction
7. Codes systematically using user's chosen strategy (country-first or variable-first) with 3-run majority voting
8. Monitors coding drift via embedded sentinel cells throughout production
9. Generates country narratives explaining score transitions with citations (optional)
10. Writes intermediate outputs to disk after every batch (context-window safe)
11. Generates a methodology transparency report with downstream bias correction guidance
12. Launches the `coding-reliability-reviewer` agent for independent assessment

---

## What This Skill Does NOT Do

- Replace expert-coded datasets like V-Dem (this is LLM-assisted measurement, not expert coding)
- Guarantee factual accuracy of evidence citations (hallucination audit catches some, not all)
- Run your statistical analysis (use `/prep-data` to merge this output with other data)
- Code post-training-cutoff years (acknowledged as coverage gap)
- Scale beyond ~80 countries per session chain (use `--resume` for larger datasets)

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `[concept]` | YES | The concept to code (e.g., "judicial independence", "media freedom") |
| `--countries` | NO | Country scope: `all`, region name, or comma-separated list (default: all COW members) |
| `--years` | NO | Year range (default: 2000-2023) |
| `--benchmark` | NO | Benchmark dataset for calibration: `vdem`, `polity`, `fh`, or `proxy` (default: auto-detect) |
| `--strategy` | NO | Coding order: `country-first` or `variable-first` (default: recommended during pre-coding interview) |
| `--narratives` | NO | Generate country narratives with transition explanations and citations after production coding |
| `--extended` | NO | Run full reliability battery (adversarial stability, prompt sensitivity, construct validity, full bias audit) |
| `--resume step-N` | NO | Resume from a specific step using saved progress files |
| `--audit` | NO | Audit an existing coded dataset without recoding |

---

## Cost and Time Estimates

**Formula:** `total_cells = countries × years × variables`. Each cell is coded 3 times (majority voting). Cost and time scale linearly with total cells.

| Scale | Example | Total Cells | Time | Approx. Cost |
|---|---|---|---|---|
| Small pilot | 20 x 5 x 3 | 300 | 1-2 hours | $10-30 |
| Medium pilot | 50 x 5 x 5 | 1,250 | 2-4 hours | $30-60 |
| Large pilot (many vars) | 20 x 5 x 35 | 3,500 | 4-8 hours | $60-120 |
| Medium production | 80 x 20 x 5 | 8,000 | 8-15 hours | $100-200 |
| Large production | 150 x 30 x 5 | 22,500 | 15-50 hours (multi-session) | $200-500 |
| High-variable production | 20 x 100 x 35 | 70,000 | 50-100 hours (multi-session) | $500-1,000 |
| + Extended | adds ~30% | — | +5-15 hours | +$50-150 |

**Note:** High-variable codebooks (15+ variables) multiply costs significantly. A 35-variable MENA dataset with 100-year coverage generates more cells than a 5-variable global dataset. Plan accordingly.

---

## The Pipeline

```
User: /create-dataset judicial_independence --countries all --years 2000-2023

Step 0: INTERVIEW --> Comprehensive pre-coding interview
         |            Conceptual scope, research context, comparability goals
         |            Coding strategy selection (country-first vs variable-first)
         |            Majority voting decision (3-run default, 1-run if user opts out)
         |            GATE: User confirms all scope decisions
         |
Step 0.5: CURATE (if variable list provided) --> Dimension architecture review
         |            Variable-level triage (relevance, redundancy, coverage,
         |              temporal profile, codability, scale type)
         |            Cost-benefit summary by tier (Core/Recommended/Optional/Drop)
         |            Gap suggestions (Claude-proposed additions)
         |            GATE: User approves curated variable list
         |
Step 1: CODEBOOK --> Design variables with uploaded references + anchors
         |           Inclusion/exclusion criteria per variable (Halterman-Keith format)
         |         GATE: User approves codebook
         |
Step 1b: PRE-TEST --> Behavioral pre-testing (conventions Section 14)
         |            Label compliance, definition recall, example classification
         |            Label semantics check, scale direction check
         |            GATE: All 5 tests pass. If fail → revise codebook, retest.
         |
Step 2: PILOT --> 50 countries x 5 years (or adapted for single-country)
         |       2a. Claude codes pilot sample (3 runs for majority voting)
         |       2b. Prompt variant testing (3 prompt phrasings on 10% sample)
         |       2c. Calibrate against benchmark (ICC >= 0.75 Track A / correlations Track B)
         |       2d. Hallucination audit (verify 20 evidence citations, rate >= 80%)
         |       2e. Gold-standard collection: user codes 200+ cells (see Section 16)
         |       GATE: User (or expert) codes gold-standard set, ICC >= 0.60
         |       If fail -> revise codebook, re-pilot (max 2 retries then STOP)
         |
Step 2f: SENTINEL SETUP --> Designate 50 sentinel cells from gold-standard
         |                   Embed in production batch schedule
         |
Step 3: PRODUCTION --> Code using chosen strategy with 3-run majority voting
         |             Write batch CSV to disk after each batch (per-run + merged)
         |             Hallucination spot-check per batch (5 citations)
         |             Bridge case consistency check per batch
         |             Sentinel drift check every 10 batches (Section 15)
         |
Step 3b: NARRATIVES (if --narratives) --> Country narrative for each coded country
         |             Transition explanations with citations and links
         |             Write one .md file per country to Replication/data/coded/narratives/
         |
Step 4: EXTENDED (if --extended) --> Prompt sensitivity, adversarial stability,
         |                            construct validity, full bias audit
         |
Step 5: DOCUMENTATION --> Methodology transparency report (10 mandatory sections)
                          Majority vote agreement statistics
                          Sentinel drift monitoring results
                          Downstream bias correction guidance (Egami et al. 2024)
                          Launch coding-reliability-reviewer agent
                          GATE: Present reliability report + agent verdict
```

---

### Step 0: Pre-Coding Interview

**This step is a structured conversation, not a configuration dump.** The skill asks questions, waits for answers, and adapts subsequent questions based on responses. Do NOT present all questions at once.

**Phase 0a: Research Context** (ask these first)

1. "What is the research project this dataset will support?" — Understand whether this is for a specific paper, a replication, or an exploratory dataset.
2. "What is the concept you want to measure? In 2-3 sentences, define it as you understand it." — Capture the researcher's working definition before imposing structure.
   **Adaptive follow-up to Q2:** If the user mentions a pre-existing variable brainstorm or list, ask them to upload or paste it. Note the file path for Phase 0.5. If the user does not have a pre-existing list, note this — Step 1 will generate variables from scratch.
3. "What existing datasets have you looked at, and why are they insufficient?" — Identifies gaps and clarifies what the new dataset adds.
4. "Who is the intended audience? (Your own paper / shared with collaborators / public release)" — Determines documentation depth and comparability requirements.

**Phase 0b: Scope Decisions** (present these as a structured table)

5. Present the **Scope Decision Table** from conventions section 1. Require explicit answers for each row. Highlight decisions that are especially consequential given the user's concept (e.g., occupied territories matter more for "state capacity" than for "media freedom").

**Phase 0c: Coding Strategy** (recommend based on context)

6. Present the two coding strategies with a recommendation:

   **Option A: Country-first** — For each country, code ALL variables across ALL years before moving to the next country.
   - *Best for:* Single-country or small-N studies, deep contextual understanding, concepts where variable interactions matter (e.g., judicial independence dimensions are interrelated)
   - *Produces:* Internally consistent country profiles, natural narrative generation
   - *Risk:* Cross-country comparability may drift without bridge cases

   **Option B: Variable-first** — For each variable, code ALL countries across ALL years before moving to the next variable.
   - *Best for:* Large-N cross-national panels, concepts with independent dimensions, replicating existing dataset structures
   - *Produces:* Cross-nationally comparable single indicators, easier calibration against benchmarks
   - *Risk:* May miss within-country interactions between variables

   **Recommendation logic:**
   - If `--countries` is a single country or < 5 countries → recommend **country-first**
   - If `--countries` is a region or `all` AND codebook has > 3 variables → recommend **variable-first**
   - If codebook has highly interrelated variables → recommend **country-first** regardless
   - If user wants narratives (`--narratives`) → recommend **country-first** (narratives are a natural byproduct)

7. "Do you want country narratives explaining score transitions with citations?" — Recommend yes for country-first strategy, optional for variable-first.

**Phase 0c.5: Reliability Strategy**

7b. Present the gold-standard validation decision:
   > "The workflow can generate a gold-standard validation template — a stratified sample of 200+ cells that you (or a domain expert) code independently, BEFORE seeing Claude's scores. This expert-coded set serves three purposes:
   >
   > **(a) Validation:** Compute Claude-vs-expert ICC to verify coding quality.
   > **(b) Sentinel monitoring:** 50 cells embedded in production batches to detect drift.
   > **(c) Downstream bias correction:** Required input for Egami et al.'s DSL estimator, which corrects regression coefficients for AI measurement error.
   >
   > **Recommended: Yes.** Without gold-standard data, there is no external check on accuracy — only internal consistency (majority voting, bridge cases). Any paper using the dataset cannot apply bias correction.
   >
   > **If you opt out:** The workflow proceeds using bridge cases as the only sentinels, majority voting as the primary reliability signal, and the methodology report will disclose that no expert validation was performed. This is acceptable for exploratory analysis but weakens the dataset's publishability.
   >
   > **If you have existing coded data** (e.g., you already coded several countries by hand): provide it as the gold standard. No new manual coding needed."
   >
   > Record the decision in `interview_summary.md`. If the user opts out, record the reason.

8. Present the majority voting decision:
   > "For production coding, each cell can be coded 3 times independently with majority voting (recommended), or 1 time with sentinel drift monitoring as the primary quality control.
   >
   > **3-run majority voting (recommended):** 3x cost, but provides the strongest reliability signal. Every cell gets an empirical agreement measure. Recommended for all projects."
   >
   > **1-run with sentinel monitoring:** Lower cost, but relies on sentinel cells (50 embedded known-answer cells) to detect quality issues. Acceptable ONLY if pilot shows > 95% of cells with 3/3 agreement on 3-run pilot."
   >
   > "I recommend 3-run majority voting. Would you like to proceed with that, or use single-run?"

   Record the decision in `interview_summary.md`. If the user chooses single-run, the methodology report must disclose this.

**Phase 0d: Comparability Safeguards** (ask based on chosen strategy)

9. For **country-first**: "Which 3-4 countries should serve as bridge cases (anchors coded in every batch to prevent scale drift)?" — Suggest candidates spanning the full scale range.
9b. For **bridge cases with long time spans** (coding period > 30 years): "Do any of your bridge case countries experience major regime changes during the coding period? If so, we need era-specific bridge scores. A country can have two, three, or more eras." — Identify ALL distinct eras with clear start/end years. Countries may have multiple eras (e.g., "Egypt: Nasser 1952-1970, Sadat/Mubarak 1971-2012, post-2013 2013-2019"; "Iran: Pahlavi 1925-1978, Islamic Republic 1979-2023"). Each era gets its own row in `bridge_cases.csv` with `era`, `year_start`, `year_end` columns. Countries without regime changes get era = "all".
10. For **variable-first**: "For each variable, what is the primary benchmark dataset for calibration?" — Map each variable to V-Dem, Polity, FH, or proxy indicators.
11. For **both**: "Are there any specific country-year cases you consider ambiguous or contentious? These will be coded in the pilot to test codebook clarity."

**Phase 0e: Technical Setup**

12. Read `dataset-construction-conventions.md` (auto-loaded via paths)
13. Read `PROJECT_MEMORY.md` for `[LEARN:dataset]` entries
14. If `--resume`: read `Replication/data/coded/coding_progress.json`, `Replication/data/coded/codebook.md`, `Replication/data/coded/bridge_cases.csv`. Load `.context/batch_briefing.md` if it exists. Report what is complete and what remains (see conventions section 7 for schemas).
15. If `--audit`: skip to agent launch with existing data files.
16. Check: does `master_supporting_docs/` contain relevant codebook PDFs or methodology papers? If not, prompt user to upload reference materials.
16. Estimate project scale: `total_cells = N_countries × N_years × N_variables`. If total_cells > 5,000: inform user that multi-session production will use the Context Relay architecture (rolling context files, subagent isolation for majority voting, SessionStart hooks for session resumption). See conventions Section 18. **If a variable brainstorm list was provided but Phase 0.5 has not yet run:** N_variables is TBD pending curation. Provide a range estimate using the brainstorm count (upper bound) and a typical Core-only count of ~30-40% of the brainstorm (lower bound).

**GATE: Present a summary of all decisions and wait for user confirmation. Save the interview summary to `Replication/data/coded/interview_summary.md`. If a variable brainstorm list was provided, note its location in the interview summary — Phase 0.5 will process it next.**

---

### Step 0.5: Variable Curation (Optional)

**Trigger:** The user provides a pre-existing variable brainstorm list (uploaded file, pasted text, or referenced in interview). This step activates when the interview (Step 0) reveals a variable list with more than ~15 variables or when the user explicitly asks for curation. If the user arrives with just a concept name and no pre-existing variable list, skip this step entirely — Step 1 generates variables from scratch as before.

**Purpose:** Reduce an unwieldy brainstorm (potentially 100-200 variables across many dimensions) into a costed, prioritized, research-question-aligned set before committing to full codebook design. Step 1 is expensive — each variable gets anchor examples, inclusion/exclusion criteria, scale definitions, and methodological context. Curating first prevents wasted effort on variables that will never be coded.

**What this step does NOT do:**
- Design scales or codebook entries (that is Step 1)
- Make final decisions — all recommendations require user approval
- Drop variables without explanation — every cut ties back to the research question

**Edge cases:**
- **< 15 variables:** Offer a lightweight curation (Pass 1 dimension check + Pass 3 cost estimate) but note that full triage may not be necessary. The user can skip directly to Step 1 if they prefer.
- **> 200 variables:** Likely indicates many redundant or tangential items. Run full curation but flag in the report that aggressive pruning is expected — typically 40-60% of a 200+ variable brainstorm is redundant or tangential.
- **No dimension structure provided:** If the user provides a flat list without dimensions, propose a dimensional structure in Pass 1 before proceeding to variable-level triage.

---

#### Pass 1: Dimension Architecture Review

Analyze the dimensional structure of the variable list as a whole. Present findings as a structured assessment.

**Output format:**

```markdown
## Dimension Architecture Assessment

### Dimensions Provided
| # | Dimension | Variable Count | Core Concept |
|---|-----------|---------------|--------------|
| D1 | [name] | [N] | [1-sentence summary] |
| ... | ... | ... | ... |

### Conceptual Distinctness
- [For each dimension pair with potential overlap]: "D[X] and D[Y] overlap on [specific concept]. Recommendation: [merge / keep separate because...]"

### Alignment with Research Question
- [Does each dimension map to a theoretical mechanism or empirical prediction in the research design?]
- [Flag any dimensions that are empirically interesting but not connected to the stated research question]

### Gap Analysis
- [Any dimensions missing given the research question and literature?]
- [Any dimensions that are conceptually important but would be extremely difficult to code?]
```

Present to user. Discuss and resolve any structural changes (merges, splits, additions) before proceeding to Pass 2. This is conversational — not a GATE, but substantive decisions should be settled before variable-level triage.

---

#### Pass 2: Variable-Level Triage

For each dimension, produce ONE integrated assessment table. Do NOT run 6 separate passes — assess all lenses simultaneously per variable. Process dimensions in order (D1, D2, ...).

**Assessment lenses** (evaluated simultaneously per variable — see conventions Section 21 for detailed definitions):

| Lens | What It Assesses | Rating Scale |
|---|---|---|
| **Relevance** | How directly does this variable address the research question? | Core / Supporting / Tangential |
| **Redundancy** | Does this variable overlap with another? If so, which survives? | Unique / Partial overlap (flag pair) / Redundant (recommend drop) |
| **Cross-national coverage** | What % of country-years will have meaningful variation? | High (>70%) / Medium (40-70%) / Low (<40%) |
| **Temporal profile** | How does this variable change over time? | Time-invariant event / Slow-moving institution / Fast-changing policy |
| **Codability** | Can Claude reliably code this from training knowledge? | High (mostly Tier 1-2 evidence) / Medium (mix) / Low (mostly Tier 3-4) |
| **Scale type** | What measurement scale is appropriate? | Binary / Ordinal 0-2 / Ordinal 0-4 / Flag / Composite |

**Output format per dimension:**

```markdown
## D[N]: [Dimension Name] — Variable Triage

| Variable | Relevance | Redundancy | Coverage | Temporal | Codability | Scale | Tier | Notes |
|----------|-----------|------------|----------|----------|------------|-------|------|-------|
| `var_name` | Core | Unique | High | Slow | High | Ord 0-4 | Core | |
| `var_name` | Supporting | Overlap w/ `other` | Medium | Fast | Medium | Binary | Rec. | |
| `var_name` | Tangential | Unique | Low | Time-inv | Low | Binary | Drop | Not connected to RQ |

### Redundancy Pairs in This Dimension
- `var_a` vs `var_b`: [Explanation. Recommendation: keep `var_a` because...]

### Dimension-Level Notes
- [Cross-cutting observations about codability, coverage patterns, etc.]
```

**Tier assignment rules:**
- **Core:** Relevance = Core AND (Codability = High or Medium) AND NOT Redundant
- **Recommended:** Relevance = Supporting AND (Codability = High or Medium) AND NOT Redundant. OR: Relevance = Core but Codability = Low (important but risky — flag this tension)
- **Optional:** Relevance = Supporting AND Codability = Low. OR: Coverage = Low but conceptually interesting
- **Drop:** Relevance = Tangential. OR: Redundant (weaker member of pair). OR: Codability = Low AND Coverage = Low

**Flag variables** (variables with `_clerical_control`, `_minority_differential`, or similar suffixes) are contextual binary markers, not standalone ordinal measures. Mark as Scale type = Flag. See conventions Section 21 for flag variable rules.

---

#### Pass 3: Cost-Benefit Summary

Aggregate the triage into a decision-ready summary with cost estimates.

**Output format:**

```markdown
## Cost-Benefit Summary

### Variable Counts by Tier
| Tier | Variables | % of Brainstorm |
|------|-----------|----------------|
| Core | [N] | [%] |
| Recommended | [N] | [%] |
| Optional | [N] | [%] |
| Drop | [N] | [%] |
| **Total brainstorm** | **[N]** | **100%** |

### Cost Projections

Using scope from interview: [N] countries × [N] years = [N] country-years.
Each cell coded 3 times (majority voting).

| Configuration | Variables | Total Cells | Est. Pilot Cost | Est. Production Cost | Est. Time |
|--------------|-----------|-------------|----------------|---------------------|-----------|
| Core only | [N] | [cells] | $[X] | $[Y] | [hours] |
| Core + Recommended | [N] | [cells] | $[X] | $[Y] | [hours] |
| Core + Rec. + Optional | [N] | [cells] | $[X] | $[Y] | [hours] |
| Full brainstorm (no curation) | [N] | [cells] | $[X] | $[Y] | [hours] |

### Key Trade-offs
- [If dropping all Optional saves X% of cells but loses coverage of Y concept...]
- [If a dimension is entirely Recommended/Optional, dropping it removes an analytical dimension...]
- [Flag any Core variables with Low codability — high-risk high-reward]
```

---

#### Pass 4: Gap Suggestions

Identify variables NOT in the brainstorm that the concept and literature suggest should be present. These are Claude-proposed additions based on training knowledge of the concept domain.

**Output format:**

```markdown
## Suggested Additions (Claude-Proposed)

| Variable | Dimension | Rationale | Relevance | Codability |
|----------|-----------|-----------|-----------|------------|
| `suggested_var` | D[N] or New: [name] | [Why this matters for the RQ] | Core/Supp. | High/Med/Low |

**Note:** These variables were NOT in the original brainstorm. Accept, modify, or reject each one individually. Any accepted additions should be assigned a tier and included in the curated list.
```

Rules for gap suggestions:
- Maximum 10-15 suggestions (not a second brainstorm)
- Each must be tied to the research question, not just "interesting"
- Each must include an honest codability assessment
- Mark every suggestion as `[Claude-proposed]` in the final curated list

---

#### Curation Report and Output

**Save to disk:** `Replication/data/coded/curation_report.md`

The curation report combines all four passes:

```markdown
# Variable Curation Report

**Concept:** [from interview]
**Research question:** [from interview]
**Brainstorm source:** [uploaded file / pasted / generated]
**Total variables in brainstorm:** [N]
**Dimensions:** [N]
**Date:** [YYYY-MM-DD]

## 1. Dimension Architecture Assessment
[Pass 1 output]

## 2. Variable-Level Triage
[Pass 2 output — all dimensions]

## 3. Cost-Benefit Summary
[Pass 3 output]

## 4. Suggested Additions
[Pass 4 output]

## 5. Curated Variable List (Proposed)

### Core Variables ([N])
| Variable | Dimension | Scale Type | Notes |
|----------|-----------|-----------|-------|

### Recommended Variables ([N])
| Variable | Dimension | Scale Type | Notes |
|----------|-----------|-----------|-------|

### Optional Variables ([N])
| Variable | Dimension | Scale Type | Notes |
|----------|-----------|-----------|-------|

### Dropped Variables ([N])
| Variable | Dimension | Reason for Drop |
|----------|-----------|----------------|

### Claude-Proposed Additions (pending user review) ([N])
| Variable | Dimension | Scale Type | Notes |
|----------|-----------|-----------|-------|
```

---

#### GATE: User Approves Curated List

**Present the curated variable list (Section 5 of the curation report) and wait for user approval.**

Approval interaction:
1. Present the curated list with tier assignments and cost projections
2. Ask the user to:
   - Confirm or override tier assignments for any variable
   - Accept or reject Claude-proposed additions
   - Move variables between tiers if desired
   - Decide which configuration to proceed with (Core only / Core + Recommended / etc.)
3. User confirms the final variable list and configuration
4. Update `curation_report.md` with the user's decisions
5. Save the approved curated list to `Replication/data/coded/curated_variables.md`

**What "approved" means:** The user has explicitly confirmed which variables to include and at what tier. The approved list becomes the input to Step 1.

**If the user says "skip curation" or "just use them all":** Record this decision in the interview summary. Do NOT generate a curation report. Proceed to Step 1 with the full brainstorm list.

---

### Step 1: Codebook Design

1. **If Phase 0.5 was run:** Build variable definitions ONLY for variables in the approved curated list (`Replication/data/coded/curated_variables.md`). Use the tier assignments (Core/Recommended/Optional) to prioritize: design Core variables first, then Recommended, then Optional. The curation report's scale type recommendations inform initial design but are not binding — Step 1 may refine them.
   **If Phase 0.5 was NOT run:** Build variable definitions from scratch using the **Codebook Template** from conventions section 2, based on the concept definition from the interview.
2. For each variable:
   - Name following convention: `concept_indicator` (e.g., `judind_tenure`, `judind_removal`)
   - Scale definition with **minimum 3 real-country anchor examples per scale point**
   - Decision: de jure vs de facto, institutional vs behavioral — document which and why
   - Defend scale granularity: why this range and not coarser/finer?
   - **Inclusion/exclusion criteria** (Halterman-Keith format):
     - *Inclusion:* "Code [score] WHEN: [specific observable condition]" — for each scale level
     - *Exclusion:* "Do NOT code [score] WHEN: [condition that seems to qualify but doesn't]"
     - *Boundary clarification:* "Do NOT confuse this variable with: [related but distinct concept]"
   - **Methodological Context** section (two parts):
     - *Required uploads*: specific documents the user should provide
     - *Prompt activation*: keywords and frameworks to trigger relevant training knowledge
   - Confidence criteria: what makes HIGH vs MEDIUM vs LOW (specific, verifiable)
   - UNABLE_TO_CODE criteria: when to use it
3. Define **bridge cases**: 3-4 countries spanning the full scale range. Bridge cases must include scores for ALL variables in the codebook (not just one). Store in `bridge_cases.csv` with one row per bridge-case-country × variable × era combination:
   - Variable-first: each batch loads only the bridge scores for the current variable, filtered to the era matching the batch's year range
   - Country-first: each batch loads the FULL per-variable score vector for all bridge cases, filtered to the era matching the batch's year range
   - For concepts with regime changes: bridge cases carry **era-specific** scores (see Step 0, Phase 0d, question 8b). Each era has its own row in `bridge_cases.csv`.
4. If user uploaded reference PDFs, process via PDF pipeline, extract relevant definitions
5. **Define cross-variable coherence rules** (if codebook has > 1 variable): Identify variable pairs with expected positive or negative correlations. Store in `coding_progress.json` under `coherence_rules`. These are used by the automated coherence check during production (see conventions Section 19). Minimum: 1 rule per 3 variables. Example:
   ```json
   "coherence_rules": [
     {"var_a": "judind_tenure", "var_b": "judind_removal", "direction": "positive", "reason": "Both reflect judicial independence dimensions"}
   ]
   ```

**GATE: Present codebook and wait for user approval. Do not proceed until approved.**

---

### Step 1b: Behavioral Pre-Testing

**Run after codebook approval, before any coding.** See conventions Section 14 for full protocol.

This step verifies that Claude can actually follow the codebook. It costs ~50 API calls and catches fundamental failures before investing in a pilot.

1. **Label compliance** — 20 country-year pairs. Claude must output only valid scale values and all required fields. Pass: 100%.
2. **Definition recall** — For each variable, ask Claude to explain what each score means. Answers must match codebook. If not: definitions are ambiguous.
3. **Example classification** — Present codebook anchor examples without labels. Claude must match >= 80% of anchor scores.
4. **Label semantics check** — Rename variables to neutral labels (Variable_A, Variable_B). Reclassify 10 cases. If > 20% of scores change: Claude is relying on variable names, not definitions. Revise definitions.
5. **Scale direction check** — Reverse the scale for 5 cases. If > 10% of scores flip: positional bias present. Add stronger anchor examples.

**Output:** `Replication/data/coded/pretesting_results.md`

**GATE: All 5 tests pass. If any test fails, revise the codebook and retest. Max 2 retries, then STOP and escalate to user for manual codebook revision.**

---

### Step 2: Pilot Coding

**2a. Claude codes pilot sample (with majority voting)**
- **Global dataset** (`--countries all`): Select 50 countries: 5-7 per region ensuring geographic diversity + all bridge cases
- **Regional dataset** (`--countries [region]`): Select ALL available countries in the region (or minimum 15 if region has more). Ensure bridge cases included and sub-regional diversity.
- **Small-N dataset** (< 10 countries): Pilot uses ALL countries. Increase years per country to compensate (10 years instead of 5).
- Code 5 years per country (first year, last year, 3 evenly spaced) — or 10 years for small-N
- **Each cell coded 3 times** independently (see conventions Section 13)
- Use **Production Prompt Template** from conventions section 7
- Output: `Replication/data/coded/runs/run[1-3]_pilot_[concept].csv` + merged `Replication/data/coded/pilot_[concept].csv`
- Report: % of cells with 3/3, 2/3, and 0/3 agreement. If > 10% are 0/3: codebook needs revision.

**2b. Prompt variant testing**
- Take 10% of pilot cells (or minimum 25 cells)
- Create 3 semantically equivalent but differently worded versions of the production prompt:
  - **Variant A:** Standard production prompt (baseline)
  - **Variant B:** Reordered scale (present from high to low instead of low to high)
  - **Variant C:** Rephrased variable definition (same meaning, different wording)
- Code the same cells with all 3 variants
- Compute cross-variant agreement rate and ICC
- **Pass criteria:** Cross-variant ICC >= 0.80, agreement >= 80%
- If fail: the coding is **prompt-fragile**. Identify which variables are most sensitive. Revise their definitions and inclusion/exclusion criteria.
- Output: results appended to `Replication/data/coded/pretesting_results.md`

**2c. Calibration**
- Track A (existing concept): compare pilot majority-vote scores to benchmark. Compute **ICC**. Threshold: ICC >= 0.75.
- Track B (novel concept): correlate pilot majority-vote scores with 3-5 proxy variables. Threshold: at least 3/5 at |r| >= 0.4.
  - **Multi-variable codebooks:** Run Track B for EACH coded variable separately. A variable passes if at least 2/5 proxies at |r| >= 0.4. The overall concept passes if ALL variables pass individually. If a variable fails calibration individually but the aggregate concept score passes, flag the variable but allow proceeding with enhanced monitoring for that variable during production.
- **Memorization check**: 10 pilot countries with scrambled names. If scores near-identical, flag.

**2d. Hallucination audit**
- Sample N evidence citations from pilot: N=20 (standard) or N=30 (if gold-standard opted out — evidence verification is the primary fabrication check without expert review)
- For each: attempt to verify the cited event/law/institution
- Classify as: VERIFIED / PLAUSIBLE / FABRICATED
- Verification rate threshold: >= 80%. Below 70%: HARD STOP.

**2e. Gold-standard validation set**

**If user opted IN to gold-standard (recommended path):**
- Generate a validation template with **200+ country-year-variable cells** (not just 30-50)
- Stratified sampling: full scale range, all variables represented, mix of easy/hard cases, >= 3 decades
  - For global datasets: >= 4 world regions represented
  - For regional datasets: >= 3 sub-regions or country clusters represented (e.g., for MENA: Maghreb, Levant, Gulf, Iran/Turkey)
- Present to user: "You or a domain expert must independently code these cases BEFORE seeing Claude's scores."
- If user has existing coded data: import it as gold standard (map columns to gold-standard schema)
- Save to: `Replication/data/coded/gold_standard/gold_standard.csv` (see conventions Section 16)
- This set serves triple duty: (1) validation ICC, (2) sentinel cells, (3) downstream bias correction

**GATE: Wait for gold-standard validation scores. Compute Claude-vs-expert ICC.**
- ICC >= 0.60: proceed
- ICC 0.40-0.59: revise codebook, re-pilot (max 2 retries)
- ICC < 0.40: STOP

**If user opted OUT of gold-standard:**
- Skip validation template generation
- Skip ICC gate
- Log in `interview_summary.md`: "Gold-standard validation: OPTED OUT. Reason: [user's reason]."
- Print warning: "Proceeding without expert validation. Reliability rests entirely on majority voting, bridge case consistency, and hallucination audits. The methodology report will disclose this. Downstream bias correction (Egami et al.) will not be available."
- Proceed directly to Step 2f

**2f. Sentinel setup + Context management initialization**

**Sentinels (with gold-standard):**
- From the gold-standard set, designate 50 cells as sentinels (conventions Section 15)
- Distribute sentinels across the production batch schedule so they are embedded in regular batches
- Save sentinel list to `Replication/data/coded/sentinel_cells.csv`

**Sentinels (without gold-standard — bridge-only mode):**
- Use bridge cases as the sentinel pool. Bridge cases already have established scores from the pilot.
- Designate ALL bridge case × era combinations as sentinels (typically 3-4 countries × 2-3 eras × N variables). For a 35-variable codebook with 4 bridge countries and 2 eras average: ~280 sentinel cells.
- These are weaker sentinels — they test scale consistency (does Claude still give Turkey-Kemalist the same score?), not accuracy against expert judgment.
- Save to `sentinel_cells.csv` with `source: "bridge_case"` for all entries.
- Log: "Sentinel mode: bridge-only (no gold-standard). Sentinels test scale stability, not accuracy."

**Context management initialization** (conventions Section 18):

1. **Generate production codebook** — `Replication/data/coded/.context/codebook_production.md`:
   - Variable-first: write the full definition for the FIRST variable to be coded (others loaded on demand)
   - Country-first: write medium-format definitions for ALL variables (~80 tokens/var: scale + inclusion/exclusion, no anchor examples or methodology context)

2. **Compute dynamic batch sizing** — estimate token costs from ACTUAL file content (not hardcoded guesses):
   - Read the codebook file, compute `codebook_tokens = len(codebook_text) / 4` (chars-to-tokens approximation)
   - For variable-first: use the LARGEST single variable definition as `codebook_tokens`
   - For country-first: use the full medium-format codebook as `codebook_tokens`
   - Read `bridge_cases.csv`, compute `bridge_tokens = len(bridge_text) / 4`
   - Estimate `rolling_context_tokens = 400` (initial empty template; will be re-estimated after first batch)
   - Read the production prompt template, compute `prompt_tokens = len(prompt_text) / 4`
   - Apply the formula:
     ```
     overhead = codebook_tokens + bridge_tokens + rolling_context_tokens + prompt_tokens
     cells_per_batch = min(80, floor((120000 - overhead) / 120))
     ```
   - Store ALL computed values in `coding_progress.json` under `context_management`:
     ```json
     "context_management": {
       "codebook_token_estimate": 1250,
       "bridge_token_estimate": 95,
       "rolling_context_token_estimate": 400,
       "prompt_token_estimate": 380,
       "total_overhead_tokens": 2125,
       "batch_size_cells": 80,
       "estimation_method": "chars_div_4"
     }
     ```
   - After the first production batch, re-estimate `rolling_context_tokens` from the actual file and update batch sizing if needed

3. **Initialize rolling context files** — create empty templates in `.context/`:
   - Variable-first: `variable_[varname].md` for each variable (with header and empty sections)
   - Country-first: `country_[cow_code].md` for each country (with header and empty sections)
   - Country-first ALSO: `variable_summary.md` with header and empty tables (cross-country calibration context — updated after each country is completed)

4. **Initialize enhanced `coding_progress.json`** — add `project`, `batch_queue`, and `context_management` sections (see conventions Section 18 for schema)

5. **Write initial batch briefing** — `.context/batch_briefing.md` with what's about to happen (first batch details)

**Confidence calibration:** If > 70% HIGH in pilot, tighten criteria. Also check: does majority voting agreement (3/3 rate) correlate with self-reported confidence? If 3/3 cells are often LOW-confidence, the confidence criteria need revision.

---

### Step 3: Production Coding

**Strategy determines batch structure** (see conventions section 11 for full protocols).

**Context management:** Production coding uses the Context Relay architecture (conventions Section 18). Each batch loads ONLY what it needs from disk. Rolling context files carry cross-batch calibration. The `dataset-production-protocol.md` rules file auto-loads (not the full conventions).

#### Majority Voting via Task-Tool Subagent Isolation

Each majority-vote run is executed as a **Task-tool subagent** (type: `general-purpose`) with a fresh, isolated context window. This guarantees independence between runs — no run can see another run's results.

**Per-batch orchestration flow:**

```
Orchestrator (main session):
  │
  ├── 1. Prepare SELF-CONTAINED batch specification
  │      Write .context/current_batch.json containing EVERYTHING
  │      the subagent needs (it cannot read auto-loaded rules):
  │      {batch_id, concept, variable, region,
  │       cells: [{cow_code, country_name, year, variable}],
  │       prompt_template: "RULES (read these FIRST):\n...",
  │       variable_definition: "...",
  │       scale: "0 = ... 4 = ...",
  │       bridge_cases: [...],
  │       rolling_context: "...",
  │       csv_columns: [...],
  │       coding_rules_summary: "..."}
  │      NOTE: output_path is NOT in current_batch.json —
  │            it's per-run, specified in each Task prompt.
  │
  ├── 2. Spawn 3 Task subagents in PARALLEL (max_turns: 30)
  │      Each gets an explicit prompt specifying its own output path:
  │      "Read Replication/data/coded/.context/current_batch.json.
  │       This file contains EVERYTHING you need: prompt template,
  │       variable definition, bridge cases, rolling context, CSV
  │       column schema, and coding rules. Do NOT try to read any
  │       other rules files or conventions files.
  │       Code all cells listed. Write output CSV with run_id=[N]
  │       to: Replication/data/coded/runs/run[N]_coded_[concept]_[batch].csv
  │       Return: N cells coded, score distribution, bridge case values.
  │       Do NOT read any other run's output files."
  │
  │      Run 1 → writes runs/run1_coded_[concept]_[batch].csv
  │      Run 2 → writes runs/run2_coded_[concept]_[batch].csv
  │      Run 3 → writes runs/run3_coded_[concept]_[batch].csv
  │      (Context: ISOLATED — fresh window per subagent)
  │
  ├── 3. VALIDATE each run CSV (see dataset-production-protocol.md)
  │      Check: file exists, headers match, row count, score range,
  │             required fields, correct run_id
  │      If validation fails: retry that run ONCE (new subagent)
  │      If retry fails: mark run as FAILED, proceed with remaining:
  │        - 2 valid + agree → majority
  │        - 2 valid + disagree → escalate to human
  │        - Only 1 valid → flag entire batch for manual review
  │
  ├── 4. Compute majority vote from validated CSVs
  │      Write merged: coded_[concept]_[batch].csv
  │      Write disagreements: disagreements_[concept].csv (append)
  │
  ├── 5. Post-batch checks (in main session)
  │      - Bridge case consistency (deviation > 1 → investigate)
  │      - Data-sparsity check: compute UNABLE_TO_CODE rate, LOW
  │        confidence rate, 0/3 rate, mean evidence word count.
  │        Escalate spot-check count if thresholds triggered
  │        (see Data-Sparsity Hallucination Escalation in production protocol)
  │      - Hallucination spot-check (base rate depends on gold-standard status:
  │        with GS: 5/10/15; without GS: 10/15/20 — see production protocol).
  │        Include tier inflation check: verify claimed evidence_tier matches
  │        actual evidence specificity. TIER_INFLATED rate < 15%.
  │      - **Evidence tier monitoring** (conventions Section 20):
  │        compute mean evidence_tier for the batch. If > 2.5 → flag as
  │        evidence-poor in rolling context Alerts. Compute tier-confidence
  │        mismatch rate (tier >= 3 AND HIGH confidence). If > 20% → flag
  │        in rolling context Alerts AND present to user in batch summary.
  │      - **Temporal monotonicity check** (conventions Section 19b):
  │        scan for year-over-year jumps ≥ 2 without major-event evidence.
  │        Without gold-standard: flag for re-examination.
  │        With gold-standard: report only.
  │      - Sentinel check (if batches_since_sentinel_check >= 10)
  │      - 0/3 cell handling: 4th run tiebreaker or flag for human
  │
  ├── 6. Update rolling context file (.context/variable_*.md or country_*.md)
  │      - Score distribution: OVERWRITE with current stats
  │      - Evidence quality: OVERWRITE with batch + cumulative mean tier
  │        AND tier distribution (T1/T2/T3/T4 percentages)
  │      - Bridge case values: OVERWRITE, flag deviations
  │      - Coding decisions: FIFO queue, max 10 entries
  │      - Alerts: DELETE resolved, KEEP active, ADD new
  │        (ADD alert if mean evidence tier > 2.5 for this batch)
  │      - Size check: if >500 tokens, compress (keep last 5 decisions)
  │
  ├── 7. Update coding_progress.json
  │      - Batch status, cell counts, sentinel gap counter
  │      - batch_queue.next_batch_id for --resume
  │      - Re-estimate rolling_context_tokens if first batch
  │
  └── 8. Write .context/batch_briefing.md (the relay baton)
         - Status: COMPLETED / IN_PROGRESS / FAILED
         - What was completed, what to do next, active alerts
         - Key decisions, failed runs (if any)
```

**`current_batch.json` is SELF-CONTAINED.** Task-tool subagents do NOT inherit auto-loaded rules files from the parent session. They get a fresh context window. Everything the subagent needs is embedded directly in `current_batch.json`:
1. Production prompt template (full text, not a file reference)
2. Variable definition — full including inclusion/exclusion
3. Scale definition with anchor examples
4. Bridge case values — per-variable scores for each bridge case country
5. Rolling context file content (full text)
6. Variable summary (country-first only) — cross-country score distributions for calibration
7. CSV column schema (list of column names, including `evidence_tier`)
8. Coding rules summary (compact version of all rules including evidence hierarchy)
9. List of cells to code with identifiers

**The Task prompt specifies the output path** (per-run: `runs/run[N]_...`), NOT `current_batch.json`.

**Subagent prompt does NOT contain:**
- Other variables' definitions
- Other runs' results (isolation guarantee)
- Full conventions file or production protocol file (embedded in JSON instead)
- Conversation history from the main session

#### If Variable-First Strategy (default for large-N)

For each variable, for each regional batch (order from `dataset-production-protocol.md`):

1. **Load context**: Read `.context/codebook_production.md` (this variable only) + `bridge_cases.csv` (filtered) + `.context/variable_[varname].md` (rolling context) + `coding_progress.json`
2. **Write batch spec**: `.context/current_batch.json` — SELF-CONTAINED with embedded prompt template, variable def, scale, bridge cases, rolling context, CSV schema, coding rules
3. **Spawn 3 subagent runs** (see orchestration flow above). All 3 can run in parallel. Output paths specified per-run in each Task prompt.
4. **Validate run CSVs**: check file exists, headers, row count, score range (see CSV Validation Protocol in production protocol). Retry failed runs once.
5. **Merge and check**: majority vote, bridge cases, hallucination spot-check, sentinel check
6. **Update rolling context**: `.context/variable_[varname].md` — OVERWRITE stats, FIFO decisions (max 10), delete resolved alerts
7. **Write to disk**: per-run CSVs + merged CSV + disagreements + progress + batch briefing (with status field)
8. **Present batch summary** for user spot-check — include majority vote statistics (% 3/3, 2/3, 0/3) and any failed/retried runs

After all regions for one variable:
- Update `.context/codebook_production.md` to contain the NEXT variable's definition
- Bridge cases re-anchor at the start of each variable
- Move to next variable

#### If Country-First Strategy (default for small-N / single-country)

For each country (or country batch of 3-5 related countries):

1. **Load context**: Read `.context/codebook_production.md` (ALL variables, medium format) + `bridge_cases.csv` (all, with per-variable scores) + `.context/country_[cow_code].md` (rolling context) + `.context/variable_summary.md` (cross-country calibration) + `coding_progress.json`
2. **Write batch spec**: `.context/current_batch.json` — SELF-CONTAINED with embedded prompt template, all variable defs (medium format), scale, bridge cases (per-variable scores), rolling context, **variable summary**, CSV schema, coding rules
3. **Spawn 3 subagent runs** (see orchestration flow above). All 3 can run in parallel. Output paths specified per-run in each Task prompt.
4. **Validate run CSVs**: check file exists, headers, row count, score range. Retry failed runs once.
5. **Merge and check**: majority vote, within-country consistency, bridge cases, hallucination, sentinel check
6. **Update rolling context**: `.context/country_[cow_code].md` — OVERWRITE score vectors, FIFO decisions (max 10), delete resolved alerts
7. **Write to disk**: per-run CSVs + merged CSV + disagreements + progress + batch briefing (with status field)
8. **Present country summary** for user spot-check — include any failed/retried runs

**After completing ALL batches for a country** (before moving to next country):

9. **Update variable summary**: Read merged CSVs for this country, compute per-variable mean/median/SD. OVERWRITE the country's row in the Country Means table. OVERWRITE per-variable stats (N, mean, SD etc.) in the Per-Variable Score Distribution table. Flag any variable where this country is > 1.5 SD from cross-country mean.
10. **Post-country calibration checkpoint** (see below):
    - If N >= 5 countries coded: compare this country's per-variable scores to cross-country distribution in `variable_summary.md`. Flag variables where this country deviates > 1.5 SD from the cross-country mean. (For N < 5: skip anomaly detection — SD is meaningless with few countries.)
    - Re-code ALL bridge cases for ALL variables (calibration pulse — quick check that the scale hasn't drifted)
    - If any bridge case deviates > 1 from pilot value: investigate before proceeding
    - Log results to `coding_progress.json` under `calibration.post_country_checks`
11. **Cross-variable coherence check** (conventions Section 19a):
    - For this country, check all `coherence_rules` from `coding_progress.json`
    - Flag country-years where 2+ variable pairs violate expected direction by > 2 scale points
    - Without gold-standard: flag for user review (or log in `disagreements_[concept].csv` with `resolution: "coherence_flag"`)
    - With gold-standard: report only (log in batch summary)
12. **If `--narratives`**: generate the country narrative (Step 3b) before moving to the next country.

#### Context Limit and Session Management

- **Batch sizing**: Use `context_management.batch_size_cells` from `coding_progress.json` (computed at Step 2f). Cap at 80 cells per batch.
- **Mid-session context pressure**: If context fills mid-batch, write partial CSV, update progress with `batch_queue.next_batch_id`, write batch briefing with status `IN_PROGRESS`, instruct user to run `--resume step-3`.
- **Session resumption**: `--resume step-3` reads `batch_queue.next_batch_id` from progress, loads `.context/batch_briefing.md`, and continues from exactly where it left off.
- **SessionStart hook**: automatically displays progress summary at each session start. After auto-compaction, re-injects the batch briefing.

#### PROJECT_MEMORY Auto-Learning

After each session's batches, check for patterns worth remembering and append to `PROJECT_MEMORY.md`:
- Country consistently UNABLE_TO_CODE → `[LEARN:dataset] [country] has limited coverage for [concept]`
- Bridge case drift → `[LEARN:dataset] [country] bridge for [variable] drifts in [region] batches`
- High disagreement variable → `[LEARN:dataset] [variable] has high 2/3 rate (~N%). Consider tightening criteria.`

**Majority voting opt-out:** If pilot showed > 95% cells with 3/3 agreement, user may opt for single-run production with sentinel monitoring as the primary quality control. This decision is recorded in `interview_summary.md` and must be disclosed in the methodology transparency report.

---

### Step 3b: Country Narratives (if `--narratives`)

For each coded country, generate a structured narrative document. See conventions section 12 for the full template.

**When to generate:**
- **Country-first strategy**: generate immediately after coding each country (natural byproduct — the context is fresh)
- **Variable-first strategy**: generate after ALL variables are coded for ALL countries (requires re-reading the coded CSVs)

**For each country:**

1. **Read all coded data** for this country across all variables and years
2. **Identify transition points** — years where any variable score changed by >= 1 point
3. **Write the narrative** following the Country Narrative Template (conventions section 12):
   - Opening context paragraph (political system, region, key features)
   - For each variable in codebook order:
     - Stable periods (summarize briefly: "From 1990-2003, [variable] remained at [score] (HIGH confidence)")
     - Transition points (explain in detail: what changed, why, with dated evidence and citations)
     - Citations with links where available (DOI, URL, or "see [author, year]")
   - Cross-variable synthesis (how do the variables interact? Do transitions cluster around political events?)
   - Coverage gaps and uncertainty (which periods have LOW confidence or UNABLE_TO_CODE? Why?)
4. **Write to disk**: `Replication/data/coded/narratives/[country_name]_[cow_code].md`
5. **Update progress**: mark narrative as complete in `coding_progress.json`

**Quality rules for narratives:**
- Narratives must be consistent with the coded data — if the narrative says "major reform in 2005" but the score doesn't change until 2007, flag the discrepancy
- Every transition must have at least one dated citation
- Do NOT explain every single year — group stable periods and focus detail on transitions
- Acknowledge uncertainty: if a transition is based on MEDIUM/LOW confidence coding, say so

---

### Step 4: Extended Reliability Protocol (only with `--extended`)

**4a. Prompt sensitivity** — 10% sample, different framing. Threshold: agreement >= 80%.
**4b. Adversarial stability** — 5% sample with counter-arguments. Threshold: flip rate <= 15%.
**4c. Construct validity** — correlate with 2-3 observable outcomes. At least 1 significant at p < 0.05.
**4d. Coverage and bias report** — UNABLE_TO_CODE rates, language bias, temporal detail bias. Descriptive, not pass/fail.

---

### Step 5: Documentation & Export

1. Concatenate batch majority-vote CSVs into final dataset: `Replication/data/coded/[concept]_final.csv`
2. Generate: `codebook.md`, `provenance.md`, `methodology_transparency.md`, `interview_summary.md`
3. Methodology transparency report has **10 mandatory sections** (from conventions section 9), including:
   - Section 6: Majority vote agreement rates (% 3/3, 2/3, 0/3 across all cells), sentinel drift results
   - Section 10: Downstream bias correction guidance (gold-standard set size, DSL estimator reference)
   - If gold-standard was opted out: Section 4 states "No expert validation performed" with reason. Section 10 states "DSL correction not available — no gold-standard set."
4. Generate `Replication/data/coded/majority_vote_summary.md`:
   - Overall agreement rates by variable, region, and time period
   - List of all 0/3 cells and their resolution (tiebreaker, human, pending)
   - Correlation between majority-vote agreement and self-reported confidence
5. If narratives were generated, create `narratives/README.md` listing all country narratives with summary statistics
6. If gold-standard exists: package `gold_standard/README.md` with sampling design, ICC results, and instructions for DSL correction. If opted out: skip this step.
7. Launch `coding-reliability-reviewer` agent
8. Present: reliability report + agent verdict

**GATE: User reviews final output.**

---

### Audit Mode (`--audit`)

Load existing coded data from `Replication/data/coded/`, launch `coding-reliability-reviewer` agent, optionally run Step 4. Report without modifying data.

---

## Integration Points

| Component | Connection |
|---|---|
| `dataset-construction-conventions.md` | All templates, thresholds, procedures, scope decisions |
| `coding-reliability-reviewer` agent | Launched in Step 5 and audit mode |
| `/prep-data` | Downstream: merge AI-coded CSV with existing datasets |
| `/reviewer-2` + Module Y | Interrogates papers using AI-coded data |
| Quality gates | AI-Coded Datasets rubric scores output |
| `pdf-processing.md` | Handles uploaded reference materials |
| Orchestrator protocol | Agent selection for `Replication/data/coded/` files |

---

## Principles

1. **Honesty over branding** — This is LLM-assisted measurement, not expert coding. Never use "expert" to describe Claude's coding.
2. **NA over noise** — UNABLE_TO_CODE is always better than a low-confidence guess that looks like data.
3. **External validation is strongly recommended** — Human gold-standard validation is the strongest reliability check. If opted out, the methodology report must disclose it and downstream bias correction is unavailable.
4. **Evidence is the product** — A score without a dated evidence citation is not a coding; it is a guess.
5. **Context limits are real** — Write to disk after every batch. Never rely on context persistence.
6. **Disclose everything** — Prompt templates, coverage gaps, hallucination rates, model version.
