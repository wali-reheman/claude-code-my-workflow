---
paths:
  - "Replication/data/coded/codebook.md"
  - "Replication/data/coded/interview_summary.md"
  - "Replication/data/coded/gold_standard/**"
  - "Replication/data/coded/pretesting_results.md"
  - "Replication/data/coded/methodology_transparency.md"
  - "Replication/data/coded/curation_report.md"
  - "Replication/data/coded/curated_variables.md"
  - "Replication/data/raw/**"
  - "data/**"
---

# AI-Coded Dataset Construction Conventions

Reference document for `/create-dataset` skill and `coding-reliability-reviewer` agent. Contains all templates, thresholds, procedures, and scope decisions for constructing original AI-coded cross-national datasets.

---

## Scope

| Concern | Handled Here | Handled Elsewhere |
|---|---|---|
| Variable design and coding protocols | Yes | |
| Country code standardization | | `panel-data-conventions.md` section 1 |
| Merging with existing datasets | | `/prep-data` |
| Statistical analysis of coded data | | `/reviewer-2`, analysis scripts |
| R code style | | `r-code-conventions.md` |

---

## Section 1: Scope and Boundary Decisions

The researcher must resolve each of these BEFORE coding begins. The skill presents this table in Step 0 and requires explicit answers.

| Decision | Options | Default | Notes |
|---|---|---|---|
| State system | COW / Gleditsch-Ward / custom list | COW | Determines which entities get coded |
| Partially recognized states | Include (list which) / Exclude | Exclude | Somaliland, Taiwan, Kosovo, etc. |
| Occupied territories | Code occupier / Code population / Exclude | Researcher decides | No default — must justify |
| Micro-state threshold | All / Population > N / Exclude list | All COW members | May have high UNABLE_TO_CODE rates |
| Temporal gap handling | Carry forward (with flag) / UNABLE_TO_CODE / Interpolate | Carry forward + flag | For years between known events |
| Training data cutoff | Acknowledge and UNABLE_TO_CODE | Required | Claude cannot code years beyond training data |
| State succession | Code predecessor until dissolution; successor from sovereignty | Required | Use panel-data-conventions.md for transition dates |

**Rules:**
1. Every scope decision must be documented in `codebook.md`
2. No default may be accepted silently — the user must explicitly confirm or override
3. Custom state lists must reference an established system (COW, GW) with documented additions/removals

---

## Section 2: Codebook Design Standards

**Variable naming:** `concept_indicator` in lowercase with underscores. Examples: `judind_tenure`, `medfree_censor`, `elecinteg_fraud`.

**Scale types supported:**

| Type | Example | When to Use |
|---|---|---|
| Ordinal 0-4 | V-Dem style | Most governance concepts |
| Ordinal 0-2 | Simplified | When finer distinctions are unreliable |
| Binary 0/1 | Presence/absence | Events, institutional features |
| Continuous 0-100 | Index-style | Composite scores (constructed, not directly coded) |

**Codebook template** (every variable must include all fields):

```markdown
### [variable_name]: [Descriptive Title]

**Concept:** [1-2 sentence definition of what this variable measures]

**Unit of analysis:** [country-year / country-month / etc.]

**Decision:** [de jure / de facto / behavioral — with justification]

**Scale:**

| Score | Label | Definition | Anchor Example |
|---|---|---|---|
| 0 | [label] | [precise definition] | [Country, Year: brief description] |
| 1 | [label] | [precise definition] | [Country, Year: brief description] |
| 2 | [label] | [precise definition] | [Country, Year: brief description] |
| 3 | [label] | [precise definition] | [Country, Year: brief description] |
| 4 | [label] | [precise definition] | [Country, Year: brief description] |
| UNABLE_TO_CODE | — | Insufficient knowledge for this country-year | — |

**Scale justification:** [Why this granularity? Why not 0-2 or 0-10?]

**Inclusion criteria** (Halterman-Keith format):
- Code [score] WHEN: [specific observable condition]
- Code [score] WHEN: [specific observable condition]
- [List concrete, verifiable conditions that warrant each score level]

**Exclusion criteria** (Halterman-Keith format):
- Do NOT code [score] WHEN: [condition that might seem to qualify but doesn't]
- Do NOT confuse this variable with: [related but distinct concept]
- [List common misclassification traps and how to avoid them]

**Confidence criteria:**
- **HIGH:** The score is well-determined — the available evidence clearly maps to a specific scale point with little ambiguity
- **MEDIUM:** The score is a reasonable judgment, but the evidence is compatible with an adjacent scale point (e.g., could be a 2 or a 3)
- **LOW:** The score is uncertain — evidence is thin, ambiguous, or contradictory; a different coder could reasonably assign a different score
NOTE: Confidence reflects certainty about THE SCORE, not evidence source type. Evidence source quality is captured separately by `evidence_tier` (Rule 11). A Tier 3 scholarly source CAN yield HIGH confidence if the characterization unambiguously maps to a scale point.

**Methodological Context:**
- *Required uploads:* [List specific documents user should provide]
- *Prompt activation:* [Keywords and frameworks to trigger relevant training knowledge]
```

**Rules:**
1. Minimum 3 real-country anchor examples per scale point (at least one non-Western)
2. If the concept has both de jure and de facto dimensions, specify which is coded and why
3. Anchor examples must span at least 3 world regions
4. UNABLE_TO_CODE must always be available
5. Scale granularity must be justified

---

## Section 3: AI Coder Regulation

**The 11 rules. Every production coding prompt must comply with all of these.**

1. **Confidence is mandatory** — every cell gets HIGH, MEDIUM, or LOW
2. **Evidence is mandatory** — 1-2 sentences citing specific events, laws, institutions, or documented patterns
3. **Evidence must be dated** — the evidence must reference something that occurred BEFORE December 31 of the coding year
4. **No invented specifics** — if uncertain about a detail, say so rather than fabricating
5. **UNABLE_TO_CODE is always available** — better NA with an honest reason than a coded guess
6. **Temporal boundary** — code as of December 31 of the year. Do not use knowledge of events after this date.
7. **No uniform blocks** — if coding > 5 consecutive identical scores for the same country, pause and justify each individually
8. **Overconfidence correction** — if > 70% of cells in any batch are HIGH confidence, pause and re-examine 5 HIGH cells
9. **Comparison** — variable-first: compare to others in the regional batch; country-first: compare to cross-country distribution in the variable summary
10. **Acknowledge uncertainty** — for MEDIUM and LOW confidence, state the specific reason
11. **Evidence hierarchy** — classify evidence tier (1-4) BEFORE assigning a score. Tier 1 = specific dated event/action, Tier 2 = institutional description of practice, Tier 3 = scholarly characterization, Tier 4 = general inference. Tier 3/4 triggers active search for better evidence. HIGH confidence with Tier 3/4 requires explicit justification. See Section 20.

---

## Section 4: Calibration Protocol

### Track A: Existing Concept with Benchmark Data

Use when coding a concept that V-Dem, Polity, Freedom House, or another established dataset already measures.

**Procedure:**
1. Select 15-20 countries from the pilot sample that have benchmark coverage
2. Code these countries using the codebook
3. Compute ICC (two-way mixed, single measures) between Claude's scores and the benchmark
4. Threshold: ICC >= 0.75

```r
# R code for ICC computation
library(irr)
pilot_data <- read.csv("Replication/data/coded/pilot_[concept].csv")
benchmark <- read.csv("Replication/data/raw/benchmark_scores.csv")
merged <- merge(pilot_data, benchmark, by = c("cow_code", "year"))
icc_result <- icc(merged[, c("claude_score", "benchmark_score")],
                  model = "twoway", type = "agreement", unit = "single")
cat("ICC:", round(icc_result$value, 3), "\n")
cat("95% CI:", round(icc_result$lbound, 3), "-", round(icc_result$ubound, 3), "\n")
```

### Track B: Novel Concept with Proxy Indicators

Use when no direct benchmark exists.

**Procedure:**
1. Identify 3-5 proxy variables that should theoretically correlate
2. State the expected direction of each correlation and justify
3. Code the pilot sample
4. Compute correlations
5. Threshold: at least 3 of 5 proxies at |r| >= 0.4

**Multi-variable codebooks:** Run Track B for EACH coded variable separately. A variable passes if at least 2/5 proxies at |r| >= 0.4. The overall concept passes if ALL variables pass individually. If a variable fails individually but the aggregate concept score passes, flag the variable for enhanced monitoring during production (increase spot-check rate for that variable's batches) but allow proceeding.

### Memorization Check

1. Take 10 pilot countries
2. Replace real names with fictional names (e.g., "Country A", "Nordavia")
3. Include only geographic and institutional descriptions, not the name
4. Recode these cases
5. If scores identical for > 8/10 cases, flag as possible memorization

### Failure Protocol

1. Identify which variable(s) failed calibration
2. Examine the 5 highest-disagreement cases
3. Revise codebook: add specificity to scale definitions, add anchor examples
4. Re-pilot the failed variable(s) only
5. Max 2 retries. If still fails: STOP.

---

## Section 5: Hallucination Audit Protocol

**Purpose:** Verify that evidence citations refer to real events, laws, institutions, or documented patterns.

**Procedure:**
1. Sample N evidence citations:
   - **Pilot:** N=20 (standard) or N=30 (if gold-standard opted out — evidence verification is the primary fabrication check)
   - **Production batch:** N=5 (standard) or N=10 (if gold-standard opted out). Data-sparsity escalation (see `dataset-production-protocol.md`) may further increase this to 15 or 20.
2. For each citation, attempt verification:
   - Search for the specific event, law, or institution mentioned
   - Cross-reference with uploaded reference materials
   - Check whether the claimed date is plausible
3. Classify each as:
   - **VERIFIED:** Confirmed real through independent source
   - **PLAUSIBLE:** Consistent with known facts but specific claim unverified
   - **FABRICATED:** No evidence the claimed event/law/institution exists, or date is wrong
   - **TIER_INFLATED:** Evidence exists but self-reported `evidence_tier` overstates its specificity (e.g., claims Tier 1 but evidence is a general characterization = actual Tier 3 or 4)
4. Compute verification rate: (VERIFIED + PLAUSIBLE) / total
5. Compute tier inflation rate: TIER_INFLATED / total

**Thresholds:**
- Verification rate >= 80%: Proceed
- Verification rate 70-79%: Warning. Review codebook — are definitions prompting Claude to over-specify?
- Verification rate < 70%: HARD STOP. Hallucination rate too high. Recovery: (1) examine the 5 worst fabrications to identify the pattern, (2) if variable-specific → revise that variable's definitions and add concrete anchor examples, re-pilot that variable only, (3) if concept-wide → return to Step 1 for codebook redesign, (4) max 2 retry cycles before concluding the concept may not be suitable for AI coding at this granularity.
- Tier inflation rate < 15%: Proceed
- Tier inflation rate >= 15%: Warning. Revise tier definitions in the prompt template — they may be ambiguous.

**Log format:** Write each audited citation to `hallucination_audit_log.md`:

| Country | Year | Variable | Evidence Claim | Claimed Tier | Actual Tier | Verification | Status |
|---------|------|----------|---------------|-------------|------------|-------------|--------|

---

## Section 6: Human Validation Protocol

**Purpose:** The single most credible quality signal.

**Template generation:**
- Select 30-50 country-years from the pilot
- Ensure mix: high/mid/low expected scores, data-rich and data-sparse countries, >= 4 regions
- Generate CSV: country, year, variable definition, scale, empty score column, empty confidence column, empty notes column

**Comparison procedure:**

```r
# ICC between Claude and human coder
library(irr)
human <- read.csv("human_validation.csv")
claude <- read.csv("Replication/data/coded/pilot_[concept].csv")
# Note: join on cow_code + year + variable to match production CSV schema
merged <- merge(human, claude, by = c("cow_code", "year", "variable"),
                suffixes = c("_human", "_claude"))
icc_result <- icc(merged[, c("score_human", "score_claude")],
                  model = "twoway", type = "agreement", unit = "single")
```

**Thresholds:**
- ICC >= 0.60: Proceed to production
- ICC 0.40-0.59: Examine disagreements, revise codebook, re-pilot
- ICC < 0.40: STOP. Concept not suitable for AI coding.

**Rules:**
1. Human validator should be a domain expert
2. Human codes independently — does NOT see Claude's scores first
3. Disagreement cases examined qualitatively
4. Results must be reported in methodology transparency report

---

## Section 7: Production Coding Protocol

**Prompt template:**

**Note:** The production prompt is also maintained in `dataset-production-protocol.md` (the lean production rules file). During production coding (Step 3), Claude loads that file instead of this one. The template below is the authoritative source; the production file mirrors it.

**Structure follows "Lost in the Middle" research:** Rules and temporal boundary at the BEGINNING (highest attention zone), reference material in the MIDDLE, and reminders at the END (attention recovery zone).

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

**Regional batch order:**
1. Latin America and Caribbean
2. Sub-Saharan Africa
3. Middle East and North Africa
4. South Asia
5. Southeast Asia
6. East Asia and Pacific
7. Post-Soviet / Central Asia
8. Central and Eastern Europe
9. Western Europe and Anglosphere

**Bridge case insertion:** Include all bridge cases at the START of every batch. Deviation > 1 scale point triggers investigation.
- **Variable-first:** Bridge cases carry the score for the current variable only (filtered from `bridge_cases.csv`), filtered to the era overlapping the batch's year range.
- **Country-first:** Bridge cases carry **per-variable scores for ALL variables** (full score vector), filtered to the era overlapping the batch's year range.
- **Era filtering:** When loading bridge cases, select the era whose `[year_start, year_end]` overlaps the batch's year range. If a batch spans an era boundary, include BOTH eras so the subagent can see the transition. For bridge countries with era = "all", always include.

**Output CSV schema:**

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
| evidence_tier | integer (1-4) or NA | Evidence source tier: 1=specific dated event/action, 2=institutional source, 3=scholarly characterization, 4=general inference. NA if UNABLE_TO_CODE. See Section 20. |
| uncertainty_reason | string | Reason for non-HIGH confidence. MUST include justification if HIGH confidence + Tier 3/4 evidence. |
| batch_region | string | Which regional batch |
| coding_pass | integer | 1 = first pass, 2 = dual-pass recode |
| run_id | integer | Majority voting run (1, 2, or 3). Only present in raw run files. |
| vote_agreement | string | Majority vote agreement: "3/3", "2/3", or "0/3" (tie). Only in final merged output. |
| final_score | integer or NA | Majority-vote score. Replaces `score` in final output. |

**Batch-to-disk protocol:**
After completing each regional batch:
1. Write `coded_[concept]_[region_snake_case].csv` (e.g., `coded_judind_latin_america.csv`)
2. Update `coding_progress.json` with batch status, summary stats, bridge case values
3. Update `bridge_cases.csv`

**All coded output files go to `Replication/data/coded/`** — including pilot results, batch CSVs, bridge cases, and progress tracking.

**`coding_progress.json` schema:**

```json
{
  "concept": "judicial_independence",
  "variables": ["judind_tenure", "judind_removal"],
  "year_range": [2000, 2023],
  "calibration": {
    "track": "A",
    "benchmark": "vdem_v2x_jucon",
    "icc": 0.81,
    "status": "PASS"
  },
  "human_validation": {
    "n_cases": 40,
    "icc": 0.65,
    "status": "PASS"
  },
  "hallucination_audit": {
    "pilot_n": 20,
    "pilot_verification_rate": 0.85,
    "production_audits": [
      {"batch": "latin_america", "n": 5, "verification_rate": 0.80}
    ]
  },
  "batches": {
    "latin_america": {"status": "complete", "n_countries": 22, "n_cells": 528, "pct_high": 0.45, "pct_low": 0.12},
    "sub_saharan_africa": {"status": "in_progress", "n_countries": 15, "n_cells": 360},
    "middle_east_north_africa": {"status": "pending"}
  },
  "bridge_cases": {
    "United States": {
      "cow_code": 2,
      "eras": [{"era": "all", "year_start": 2000, "year_end": 2023, "scores": {"judind_tenure": 4, "judind_removal": 4, "judind_salary": 3}}]
    },
    "Russia": {
      "cow_code": 365,
      "eras": [{"era": "all", "year_start": 2000, "year_end": 2023, "scores": {"judind_tenure": 1, "judind_removal": 1, "judind_salary": 2}}]
    },
    "Brazil": {
      "cow_code": 140,
      "eras": [{"era": "all", "year_start": 2000, "year_end": 2023, "scores": {"judind_tenure": 3, "judind_removal": 2, "judind_salary": 2}}]
    }
  },
  "last_updated": "2026-02-13T14:30:00Z"
}
```

**`bridge_cases.csv` schema:**

| Column | Type | Description |
|---|---|---|
| cow_code | integer | COW country code |
| country_name | string | Country name |
| variable | string | Variable name |
| era | string | Era label (e.g., "1920-1978", "1979-2023", or "all") |
| year_start | integer | First year this bridge score applies |
| year_end | integer | Last year this bridge score applies |
| score | integer | Established bridge score for this era |
| source | string | How this score was established ("pilot", "gold_standard", "expert") |
| deviations | string | Pipe-separated list of batches where deviation > 1 occurred |

**Era-specific bridge cases:** For concepts where bridge countries undergo regime changes (e.g., Iran 1979, Turkey post-2002, Egypt 1952/2013), a single bridge score per variable is misleading for historical coding. Bridge cases support **era-specific scores**: one row per country × variable × era. **A country can have two, three, or more eras** — there is no limit.

Example for state secularization:
```
cow_code, country_name, variable, era, year_start, year_end, score, source
630, Iran, secular_law, "Pahlavi", 1925, 1978, 3, pilot
630, Iran, secular_law, "Islamic Republic", 1979, 2023, 0, pilot
651, Egypt, secular_law, "Nasser", 1952, 1970, 3, pilot
651, Egypt, secular_law, "Sadat/Mubarak", 1971, 2012, 2, pilot
651, Egypt, secular_law, "post-2013", 2013, 2023, 2, pilot
640, Turkey, clergy_state, "Kemalist", 1923, 2001, 4, pilot
640, Turkey, clergy_state, "AKP era", 2002, 2023, 2, pilot
682, Saudi Arabia, secular_law, "all", 1932, 2023, 0, pilot
```

**Era assignment rules:**
1. The interview (Step 0) must identify ALL distinct eras for each bridge country. Ask: "Do any bridge case countries experience major regime changes? A country can have multiple eras (e.g., Egypt: Nasser, Sadat/Mubarak, post-2013)."
2. Each era must have clear start/end years (no overlap within a country)
3. A country with no regime change uses era = "all" with year_start/year_end spanning the full coding period
4. When loading bridge cases for a batch, **filter to the era that overlaps with the batch's year range**. If a batch spans an era boundary (e.g., Iran 1975-1985), include BOTH eras and note the transition year.
5. Bridge calibration pulses (post-country checkpoint) must re-code bridge cases **for the era matching the most recently coded years**, not just the latest era

---

## Section 8: Extended Reliability Protocol

**Only runs with `--extended` flag.**

**Prompt sensitivity:**
- Sample 10% of coded cells (stratified by region and confidence)
- Alternative framings of the same concept
- Threshold: agreement >= 80%, ICC >= 0.80

**Adversarial stability:**
- Sample 5% of coded cells
- Present counter-argument for each
- Threshold: flip rate <= 15%

**Construct validity:**
- Identify 2-3 observable outcomes that should correlate
- Compute correlations using full dataset
- At least 1 significant at p < 0.05 in expected direction

**Coverage and bias report** (descriptive, always include):
- UNABLE_TO_CODE rate by region and by decade
- Mean confidence level by region
- Mean evidence word count by decade (temporal detail bias)
- Mean scores for Anglophone vs non-Anglophone (language bias)

---

## Section 9: Documentation Requirements

**Methodology transparency report** (`methodology_transparency.md`) — 10 mandatory sections:

1. **What was coded and why** — Concept definition, research motivation, variables, scope
2. **How Claude was used** — Model version, date of coding, FULL prompt templates
3. **Calibration results** — Track (A or B), benchmark, sample size, ICC or correlations, memorization check
4. **Human validation results** — N cases, validator expertise, ICC, highest-disagreement cases. If gold-standard was opted out: state "No expert validation performed. Reason: [from interview_summary.md]. Reliability rests on majority voting, bridge case consistency, and hallucination audits."
5. **Hallucination audit results** — N audited, verification rate, any fabricated citations
6. **Reliability metrics** — Majority vote agreement rates (% 3/3, 2/3, 0/3), sentinel drift monitoring results, test-retest ICC (if extended), prompt sensitivity, adversarial flip rate. Use correct metric names.
7. **Coverage gaps** — UNABLE_TO_CODE distribution by region and decade, confidence distribution
8. **Known limitations** — Explicit list (>= 5 items): single-coder, training data dependency, hallucination risk, post-training-cutoff gap, coverage variation
9. **How this differs from expert-coded data** — Mandatory section. Single coder vs multi-coder, no differential expertise, self-reported confidence vs model-derived uncertainty, consistency is not accuracy.
10. **Downstream correction protocol** — Gold-standard set size and sampling design, DSL correction applied (yes/no), uncorrected vs corrected estimates for key analyses, R package version used (Egami et al. 2024). If gold-standard was opted out: state "DSL correction not available — no gold-standard validation set. Researchers using this dataset for regression analysis should collect their own gold-standard sample to enable bias correction."

**Rules:**
1. Never use the word "expert" to describe Claude's coding
2. All prompt templates published in full
3. Limitations section must be substantive, not boilerplate

---

## Section 10: Common Pitfalls

1. **Present bias** — Knowing outcomes makes past coding teleological
2. **Western-centric anchoring** — Nordic countries as default "high"
3. **Conflating similar concepts** — Judicial independence is not rule of law is not access to justice
4. **Anchoring drift across regions** — Without bridge cases, regional scales diverge
5. **Overconfidence on famous countries** — HIGH confidence may reflect familiarity, not precision
6. **Absence of evidence is not evidence of absence** — No evidence of interference does not mean independence
7. **Coding regime type instead of the specific variable** — Lazy coding shortcut
8. **Temporal interpolation masking change** — Carrying forward for 10 years hides potential changes
9. **Data-sparsity hallucination** — Fabrication risk increases for data-sparse countries/periods. The workflow auto-escalates hallucination spot-checks when batch indicators trigger (see `dataset-production-protocol.md` Data-Sparsity Hallucination Escalation), but researchers should also stratify their gold-standard sample to include data-sparse cases.

---

## Section 11: Coding Strategy Protocols

Two strategies govern how production coding is organized. The choice is made during the pre-coding interview (Step 0) and recorded in `interview_summary.md`.

### Variable-First Strategy

**Logic:** Code one variable at a time across all countries, then move to the next variable. Within each variable, code by regional batch.

**Batch structure:** variable → region → countries × years

**When to use:**
- Large-N cross-national panels (> 20 countries)
- Variables are conceptually independent (e.g., different dimensions of governance that don't require seeing the full country profile)
- Primary goal is cross-country comparability on individual indicators
- Benchmark dataset exists for calibration (Track A)

**Advantages:**
- Cross-country comparability: coding the same variable for all countries in sequence makes it easier to maintain consistent scale application
- Natural calibration: benchmark ICC is computed per variable
- Efficient context use: each batch loads only one variable definition

**Risks and mitigations:**
- *Risk:* Within-country coherence may suffer (judicial tenure coded at 4 but judicial removal coded at 1 without realizing the inconsistency). *Mitigation:* After all variables are coded, run a cross-variable consistency check per country.
- *Risk:* Cannot generate narratives in-line. *Mitigation:* Generate narratives after all coding is complete (Step 3b post-hoc).

**File naming:** `coded_[concept]_[variable]_[region].csv`

### Country-First Strategy

**Logic:** Code one country (or a small batch of 3-5 related countries) at a time, going through the FULL codebook — all variables × all years — before moving to the next country.

**Batch structure:** country → variables (in codebook order) → years

**When to use:**
- Single-country or small-N studies (< 10 countries)
- Variables are interrelated (e.g., multiple dimensions of judicial independence that should tell a coherent story)
- Researcher wants country narratives
- Deep contextual understanding matters more than breadth

**Advantages:**
- Within-country coherence: Claude builds a full picture of the country before moving on
- Natural narrative generation: narratives are a byproduct of country-first coding
- Better temporal consistency: coding all years for one country in sequence helps track change over time

**Risks and mitigations:**
- *Risk:* Cross-country scale drift (what counts as "3" may shift as Claude codes different countries). *Mitigation:* Bridge cases at the START of every country batch. Deviation > 1 point triggers recalibration. Post-country calibration checkpoint (see below).
- *Risk:* Context exhaustion for countries with many variables × many years. *Mitigation:* Write to disk after each variable within the country.
- *Risk:* No cross-country perspective within country context. *Mitigation:* `variable_summary.md` loaded into subagent context. Cross-country comparison instruction in prompt.

**Post-country calibration checkpoint** (runs after completing ALL batches for a country, before moving to next):

1. **Update `variable_summary.md`** — compute per-variable mean/median/SD across all countries coded so far. Add this country's scores to the Country Means table.
2. **Anomaly detection** (activates only when N >= 5 countries coded — SD is meaningless with fewer) — for each variable, check if this country's mean score deviates > 1.5 SD from the cross-country mean. If so: log an alert, but do NOT automatically recode. Human reviews flagged variables. For the first 4 countries, skip SD-based anomaly detection but still run the bridge calibration pulse (step 3).
3. **Bridge case calibration pulse** — re-code ALL bridge cases for ALL variables (quick single-run, not 3-run majority). Compare each bridge case score to the pilot-established value. If deviation > 1 for ANY variable: PAUSE and investigate before proceeding to next country.
4. **Log results** — write to `coding_progress.json` under `calibration.post_country_checks`:
   ```json
   "post_country_checks": [
     {
       "country": "Turkey",
       "cow_code": 640,
       "anomaly_vars": ["religious_court"],
       "bridge_drift": false,
       "status": "PASSED"
     }
   ]
   ```
5. **If bridge drift detected** — this is a YELLOW alert. Options: (a) re-code the most recent country for the drifting variable, (b) re-establish bridge values with fresh context, (c) continue with enhanced monitoring (user decides).

**File naming:** `coded_[concept]_[country_cow_code].csv`

### Within-Country Coding Order (both strategies)

When coding multiple variables for one country (always true for country-first; happens during cross-variable consistency check for variable-first):

1. Code variables in **codebook order** — the codebook should order variables from most observable/concrete to most abstract/composite
2. For each variable, code years **chronologically** (earliest to latest) — this respects the temporal boundary rule and prevents future-knowledge contamination
3. After coding all variables for a country, check: do the scores tell a coherent story? Flag any anomalies (e.g., high judicial independence but low rule of law).

---

## Section 12: Country Narrative Template

Country narratives explain the *story* behind the data — not every year, but every meaningful transition. They serve as both quality control and research output.

**File location:** `Replication/data/coded/narratives/[country_name]_[cow_code].md`

**Template:**

```markdown
# [Country Name] (COW: [code]) — [Concept] Narrative

**Coded period:** [start_year]-[end_year]
**Variables coded:** [list]
**Overall confidence:** [HIGH: N%, MEDIUM: N%, LOW: N%, UNABLE_TO_CODE: N%]

## Country Context

[1-2 paragraphs: political system, region, key features relevant to the concept.
E.g., "Turkey is a secular republic founded in 1923, with a parliamentary system
that transitioned to a presidential system in 2017. Its political history is marked
by periodic military interventions (1960, 1971, 1980, 1997) and a tension between
secular Kemalist institutions and Islamist political movements."]

## [Variable 1: variable_name — Descriptive Title]

### Stable Period: [start]-[end] — Score: [N] ([confidence])
[Brief summary of why the score is stable during this period.]

### Transition: [year] — Score changed from [N] to [M]
**What changed:** [1-2 sentences describing the specific change]
**Evidence:** [Specific event, law, or institutional change with date]
**Citation:** [Author (Year). "Title." *Journal/Source.* DOI/URL if available]
**Why it matters:** [1 sentence on substantive significance]

### Stable Period: [start]-[end] — Score: [N] ([confidence])
[...]

### Transition: [year] — Score changed from [N] to [M]
[...]

## [Variable 2: variable_name — Descriptive Title]
[Same structure as above]

## Cross-Variable Synthesis

[1-2 paragraphs: How do the variables interact? Do transitions cluster around
specific political events? Are there periods where variables move in opposite
directions, and if so, why?]

## Coverage and Uncertainty

| Period | Confidence | Notes |
|--------|-----------|-------|
| [year range] | HIGH | Well-documented period |
| [year range] | LOW | Limited sources available |
| [year range] | UNABLE_TO_CODE | [reason] |

## Sources

[Numbered reference list. Include URLs/DOIs where available. Prefer:
- Academic publications (DOI links)
- Government legislation databases
- Established think tank reports (Freedom House, V-Dem country briefs)
- Major news sources for specific events (with date)]
```

**Rules:**
1. Every transition must have at least one dated citation with a link or reference
2. Stable periods can be summarized briefly — do not explain each year individually
3. Cross-variable synthesis is mandatory (even if brief) — it catches coding inconsistencies
4. Coverage and uncertainty section is mandatory — it signals honesty
5. Narrative must be consistent with the coded CSV — if the narrative describes a change in 2005 but the CSV shows the score changing in 2007, flag the discrepancy and resolve it
6. Do NOT use the word "expert" to describe Claude's analysis in narratives
7. Cite real, verifiable sources — if a citation cannot be verified, mark it as "[unverified]"

---

## Section 13: Multi-Run Majority Voting Protocol

**Purpose:** Code each cell 3 times independently and take the majority vote. This is the single biggest reliability improvement available (Wang et al. 2023, Carlson et al. 2025).

**How it works:**

1. Each production cell is coded 3 times using the **same prompt** but as independent API calls (not in the same conversation turn)
2. The 3 runs produce 3 scores per cell
3. Majority vote determines the final score
4. The vote distribution replaces self-reported confidence as the primary uncertainty measure

**Aggregation rules:**

| Vote Pattern | Final Score | Agreement | Action |
|---|---|---|---|
| 3/3 agree (e.g., 2, 2, 2) | Majority (2) | `3/3` | High reliability — accept |
| 2/3 agree (e.g., 2, 2, 1) | Majority (2) | `2/3` | Acceptable — flag minority score for review |
| 0/3 agree (e.g., 1, 2, 3) | None | `0/3` | **Escalate to human review** or code a 4th run as tiebreaker |
| UNABLE_TO_CODE in any run | See rules below | — | Special handling |

**UNABLE_TO_CODE voting rules:**
- If 2/3 or 3/3 runs return UNABLE_TO_CODE → final = UNABLE_TO_CODE
- If 1/3 returns UNABLE_TO_CODE and 2/3 agree on a score → final = majority score, flag as `UNABLE_IN_MINORITY`
- If 1/3 returns UNABLE_TO_CODE and the other 2 disagree → escalate to human review

**File structure:**

```
Replication/data/coded/
├── runs/                                    # Raw per-run outputs
│   ├── run1_coded_[concept]_[batch].csv
│   ├── run2_coded_[concept]_[batch].csv
│   └── run3_coded_[concept]_[batch].csv
├── coded_[concept]_[batch].csv              # Majority-vote merged output
└── disagreements_[concept].csv              # All cells with < 3/3 agreement
```

**disagreements CSV schema:**

| Column | Type | Description |
|---|---|---|
| cow_code | integer | COW country code |
| country_name | string | Country name |
| year | integer | Coding year |
| variable | string | Variable name |
| run1_score | integer/NA | Score from run 1 |
| run2_score | integer/NA | Score from run 2 |
| run3_score | integer/NA | Score from run 3 |
| vote_agreement | string | "2/3" or "0/3" |
| final_score | integer/NA | Majority score (NA if 0/3) |
| resolution | string | "majority", "tiebreaker", "human", or "pending" |

**Confidence derivation from votes:**
Majority voting replaces self-reported confidence as the PRIMARY reliability signal. Self-reported confidence (HIGH/MEDIUM/LOW) is retained as a SECONDARY signal for the evidence quality audit.

| Vote Agreement | Derived Reliability |
|---|---|
| 3/3 + all HIGH self-reported | Very high |
| 3/3 + mixed self-reported | High |
| 2/3 | Medium — review minority run's evidence |
| 0/3 | Low — requires human adjudication |

**Cost implications:**
3x coding cost. For 100K cells at ~500 input tokens + ~50 output tokens per call:
- Single run: ~100K calls
- 3-run majority voting: ~300K calls
- Batch API discount (50%): makes this affordable

**When to use fewer runs:**
- Pilot phase: 3 runs always (establishes baseline agreement rate)
- Production, if pilot shows > 95% 3/3 agreement: user may opt for 1-run with sentinel monitoring (see Section 15)
- This trade-off is presented during the pre-coding interview

---

## Section 14: Behavioral Pre-Testing Protocol

**Purpose:** Before any actual coding, verify that Claude can follow the codebook. Catches fundamental failures before investing in a pilot. Costs ~50 API calls. Based on Halterman & Keith (2024) Stage 1.

**When:** After codebook design (Step 1), before pilot coding (Step 2). This becomes Step 1b.

**Test 1: Label Compliance**

Present 20 country-year pairs and check:
- Does Claude output only valid scale values? (e.g., 0, 1, 2, 3 — not 1.5, "N/A", "moderate")
- Does Claude always include all required fields (score, confidence, evidence)?
- Does Claude use UNABLE_TO_CODE when appropriate?

**Pass criteria:** 100% valid labels. Any invalid output = revise prompt template.

**Test 2: Definition Recall**

For each variable, ask Claude:
- "What does a score of 2 mean for [variable_name]?"
- "What is the difference between a 2 and a 3 for [variable_name]?"

**Pass criteria:** Claude's answers match the codebook definitions. If Claude paraphrases with different meaning, the scale definitions are ambiguous — revise them.

**Test 3: Example Classification**

Present the codebook's anchor examples **without labels** and ask Claude to classify them:
- "Code [Country] in [Year] for [variable_name]."
- Compare Claude's scores to the anchor scores in the codebook.

**Pass criteria:** >= 80% exact match with anchor scores. If Claude disagrees with its own codebook anchors, the anchors are confusing or the prompt is failing.

**Test 4: Label Semantics Check (Halterman-Keith Ablation)**

Rename all variables to neutral labels (e.g., `clergy_appointment` → `Variable_A`) and reclassify 10 cases:
- If scores change significantly (> 20% differ), Claude is relying on the variable NAME, not the DEFINITION
- This means the definitions aren't doing the work — they need to be more explicit

**Pass criteria:** <= 20% score change when labels are neutralized. Above 20% = revise definitions.

**Test 5: Scale Direction Check**

For 5 cases, present the scale in REVERSED order (high to low instead of low to high):
- If scores flip (Claude now gives low scores where it gave high), there's a positional bias
- This catches cases where Claude defaults to "middle of the presented scale" regardless of content

**Pass criteria:** <= 10% score change when scale is reversed. Above 10% = add stronger anchor examples.

**Output:** `Replication/data/coded/pretesting_results.md` — a brief report documenting each test, pass/fail, and any revisions made.

---

## Section 15: Sentinel Drift Monitoring Protocol

**Purpose:** Detect if coding quality degrades across production batches. Based on OLAF Framework (Imran et al. 2025).

**Sentinel cells:** A fixed set of country-year-variable cells with **known correct scores**.

**With gold-standard (recommended):** 50 sentinel cells. Sources:
1. Gold-standard cells validated by the user/expert (from Section 16) — primary source
2. Bridge cases with established scores
3. Well-documented cases where the correct score is unambiguous

**Without gold-standard (bridge-only mode):** Use ALL bridge case × era × variable combinations as sentinels. Typical count: 3-4 bridge countries × 2-3 eras × N variables (e.g., 4 × 2 × 35 = 280 cells for a 35-variable codebook). These sentinels test **scale stability** (does Claude still assign Turkey-Kemalist the same score?) but NOT accuracy (the bridge scores themselves were established by Claude during the pilot, not by an expert). Bridge-only sentinels are weaker — log this in `coding_progress.json` as `"sentinel_mode": "bridge_only"`.

**How sentinels work:**

1. At project start, designate 50 sentinel cells with known scores. Save to `Replication/data/coded/sentinel_cells.csv`
2. Sentinel cells are embedded in production batches **without any marking** — Claude codes them like any other cell
3. After every 10 batches (or user-configured interval), extract sentinel scores from the coded output
4. Compare sentinel scores to known values using ICC and exact agreement rate
5. Track metrics over time in `coding_progress.json`

**Sentinel CSV schema:**

| Column | Type | Description |
|---|---|---|
| cow_code | integer | COW country code |
| country_name | string | Country name |
| year | integer | Coding year |
| variable | string | Variable name |
| known_score | integer | Expert-validated correct score |
| source | string | How the score was established (e.g., "gold_standard", "bridge_case", "benchmark") |

**Alert thresholds:**

| Metric | Green | Yellow | Red |
|---|---|---|---|
| Sentinel exact agreement | >= 85% | 70-84% | < 70% |
| Sentinel ICC | >= 0.80 | 0.65-0.79 | < 0.65 |
| Delta from previous check | < 0.05 | 0.05-0.10 | > 0.10 |

**When an alert fires:**
- **Yellow:** Log a warning. Continue coding but increase hallucination spot-check rate (5 → 10 per batch).
- **Red:** **PAUSE coding.** Investigate:
  1. Did the concept domain change (e.g., moved from well-documented Western Europe to data-sparse Central Asia)?
  2. Did context window pressure increase (batches getting too large)?
  3. Is the prompt template still being followed correctly?
  4. Re-calibrate: re-run the most recent batch with fresh context.

**Progress tracking addition to `coding_progress.json`:**

```json
{
  "drift_monitoring": {
    "sentinel_count": 50,
    "check_interval_batches": 10,
    "checks": [
      {
        "after_batch": 10,
        "exact_agreement": 0.88,
        "icc": 0.83,
        "delta_icc": null,
        "status": "GREEN"
      },
      {
        "after_batch": 20,
        "exact_agreement": 0.84,
        "icc": 0.79,
        "delta_icc": -0.04,
        "status": "YELLOW"
      }
    ]
  }
}
```

---

## Section 16: Gold-Standard Validation Set

**Purpose:** A reusable, expert-coded subset that serves triple duty: (1) pilot evaluation, (2) sentinel drift monitoring, (3) downstream bias correction (Egami et al. 2024). Based on convergent recommendations from Carlson et al. (2025), OLAF (Imran et al. 2025), and Egami et al. (2024).

**This is a first-class project artifact — not a throwaway pilot check.**

**Location:**

```
Replication/data/coded/gold_standard/
├── gold_standard.csv                # Expert-coded cells
├── sampling_design.md               # How cells were selected and why
├── inter_coder_reliability.md       # If multiple experts coded: agreement stats
└── README.md                        # Documentation
```

**Minimum size:** 200 cells (Egami et al. 2024 recommendation). Ideal: 500 cells.

**Sampling design:**
Gold-standard cells must be stratified across:

| Dimension | Global datasets | Regional datasets |
|---|---|---|
| Countries | >= 4 world regions represented | >= 3 sub-regions or country clusters represented (e.g., MENA: Maghreb, Levant, Gulf, Iran/Turkey) |
| Time periods | >= 3 decades represented | >= 3 decades represented |
| Score levels | Full scale range represented (including extremes and middle) | Full scale range represented (including extremes and middle) |
| Variables | All variables represented (proportional to importance) | All variables represented (proportional to importance) |
| Difficulty | Mix of easy (well-documented) and hard (data-sparse) cases | Mix of easy (well-documented) and hard (data-sparse) cases |

**Who codes the gold standard:**
- The user (primary researcher) — mandatory
- Ideally: a second domain expert codes independently, and inter-coder reliability is computed
- Gold-standard coding happens BEFORE seeing Claude's scores (blind coding)

**Gold-standard CSV schema:**

| Column | Type | Description |
|---|---|---|
| cow_code | integer | COW country code |
| country_name | string | Country name |
| year | integer | Coding year |
| variable | string | Variable name |
| expert_score | integer or NA | Expert-coded score |
| expert_confidence | string | Expert's confidence (HIGH/MEDIUM/LOW) |
| expert_notes | string | Expert's reasoning |
| coder_id | string | Which expert coded this (for multi-coder designs) |
| is_sentinel | boolean | Whether this cell is used for drift monitoring |

**Three uses:**

1. **Pilot evaluation (Step 2d):** Compute Claude-vs-expert ICC on the gold-standard subset. This replaces the ad-hoc "generate human validation template" approach — the gold standard IS the validation set.

2. **Sentinel monitoring (Section 15):** A subset of gold-standard cells (50) are designated as sentinels and embedded in production batches.

3. **Downstream bias correction (Section 17):** The gold-standard set is the required input for Egami et al.'s DSL estimator, which corrects regression coefficients for measurement error introduced by AI coding.

**Rules:**
1. Gold-standard coding is done BLIND — expert does not see Claude's scores
2. Gold-standard cells are never used as training data or few-shot examples in prompts
3. Gold-standard disagreements with Claude are analyzed qualitatively (5 highest-disagreement cases documented)
4. Gold-standard set is versioned and immutable once established (do not revise scores to match Claude)
5. If the codebook is revised after gold-standard coding, the affected gold-standard cells must be re-coded by the expert

### Gold-Standard Opt-Out

The user may opt out of gold-standard validation during the Step 0 interview. This is a legitimate choice for exploratory datasets, personal research tools, or projects where manual coding is infeasible.

**What is lost:**
- No Claude-vs-expert ICC (the strongest accuracy measure)
- No gold-standard sentinels (drift monitoring uses bridge cases only — tests scale stability, not accuracy)
- No downstream bias correction via Egami et al. DSL estimator
- Methodology report must disclose: "No expert validation performed"

**What remains:**
- Majority voting (3-run) as the primary reliability signal
- Bridge case consistency checks (scale stability)
- Hallucination audit (evidence verification) — **intensity automatically increased** (see Section 5)
- Track A/B calibration (benchmark or proxy correlations)
- Data-sparsity escalation (auto-adjusted spot-checks)
- All production quality controls (Rule 7, Rule 8, overconfidence check)
- **Cross-variable coherence check** — detects logically incoherent score profiles (see Section 19)
- **Temporal monotonicity check** — flags year-over-year jumps > 1 without major-event evidence (see Section 19)

**Decision is recorded** in `interview_summary.md` with the user's reason. The methodology transparency report (Section 9) must include this decision and its implications.

**The user can always provide gold-standard data later** — run `/create-dataset --audit` with the gold-standard CSV to retroactively compute ICC, establish sentinels, and enable DSL correction.

---

## Section 17: Downstream Bias Correction Protocol

**Purpose:** AI-coded variables contain measurement error. Even 90%+ accuracy produces biased regression coefficients and invalid confidence intervals when used in statistical analysis (Egami et al. 2024, NeurIPS). This section documents the mandatory correction protocol.

**The problem:**
- AI coding error is NOT random — it's systematic (varies by region, time period, difficulty)
- Standard regression with AI-coded variables produces biased β estimates
- Standard errors are wrong — confidence intervals have incorrect coverage
- This affects ALL downstream analyses, not just regressions (correlations, t-tests, factor analysis)

**The solution: Design-based Supervised Learning (DSL)**

Egami et al.'s DSL estimator uses the gold-standard validation set (Section 16) to statistically correct for AI coding error. It is a doubly-robust procedure that:
1. Learns the relationship between AI-coded and expert-coded scores
2. Corrects regression coefficients and confidence intervals
3. Provides valid inference even when AI accuracy varies across subgroups

**R implementation:**

```r
# DSL correction for downstream analysis
# Requires: gold-standard validation set + full AI-coded dataset

# Install: devtools::install_github("naoki-egami/dsl")
library(dsl)

# Load data
ai_coded <- read.csv("Replication/data/coded/[concept]_final.csv")
gold <- read.csv("Replication/data/coded/gold_standard/gold_standard.csv")

# Merge: gold-standard cells have both expert and AI scores
merged <- merge(gold, ai_coded,
                by = c("cow_code", "year", "variable"),
                suffixes = c("_expert", "_ai"))

# DSL-corrected regression
# Y = outcome, S = AI-coded surrogate, X = covariates, Y_gold = expert scores (in labeled subset)
result <- dsl_regression(
  formula = outcome ~ ai_score + covariates,
  data = ai_coded,
  surrogate = "ai_score",
  gold_data = merged,
  gold_label = "expert_score"
)
summary(result)
```

**Documentation requirement:**

Every paper using AI-coded data from this workflow MUST include in its methodology section:

> "AI-coded variables contain systematic measurement error that varies by region and time period. We correct for this using Egami et al.'s (2024) Design-based Supervised Learning estimator, which uses a gold-standard validation set of [N] expert-coded observations to produce bias-corrected regression coefficients and valid confidence intervals."

**Methodology transparency report:** Section 9 item 10 already covers the downstream correction protocol. Ensure it includes: gold-standard set size, DSL correction applied (yes/no), uncorrected vs corrected estimates reported, R package version.

**Key citation:**
- Egami, N., Hartman, E., & Yin, G. (2024). "Using Imperfect Surrogates for Downstream Inference: Design-based Supervised Learning for Social Science Applications of LLMs." *NeurIPS 2024.*

---

## Section 18: Context Management Protocol

**Purpose:** Manage context window pressure for large-scale projects (50+ variables, 100+ countries, 100K+ cells). Uses files on disk as external memory and Claude Code's subagent isolation to keep the working context lean.

**Design philosophy:** The context window is a workbench, not a warehouse — load only what the current task needs.

### Cross-Session State

`coding_progress.json` is the **single source of truth** for session resumption. Enhanced schema:

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
    "last_session_id": "",
    "sessions_completed": 47
  },
  "calibration": { },
  "drift_monitoring": { }
}
```

### Rolling Context Files

External memory stored in `Replication/data/coded/.context/`. See `.context/README.md` for full documentation.

- **Variable-first:** One file per variable (`variable_[varname].md`) — score distributions, bridge cases, recent decisions
- **Country-first:** One file per country (`country_[cow_code].md`) — score vectors, key transitions, cross-variable coherence
- **Country-first also:** `variable_summary.md` — cross-country per-variable score distributions for calibration (updated after each country, not each batch)
- **Batch briefing:** `batch_briefing.md` — the "relay baton" between sessions
- **Production codebook:** `codebook_production.md` — compressed codebook for production use

**Size target:** 300-500 tokens per rolling context file. Compression rules (mechanical, not discretionary):
- **Score Distribution:** OVERWRITE entirely with current stats. Never append.
- **Bridge Cases:** OVERWRITE with current values. Flag deviations in Alerts.
- **Coding Decisions Log:** FIFO queue, max 10 entries. When adding entry 11, delete entry 1.
- **Alerts:** DELETE resolved alerts. KEEP active. ADD new.
- **If file > 500 tokens after update:** Compress to last 5 decisions. If still over, summarize Score Distribution to one line per region.

### Dynamic Batch Sizing

Computed at Step 2f after codebook is finalized:

```
cells_per_batch = floor((context_budget - overhead_tokens) / tokens_per_cell)
context_budget  = 120,000 tokens (60% of 200K, room for reasoning)
tokens_per_cell = 120 (100 output + 20 input identifiers)
cap: max 80 cells per batch (judgment quality threshold)
```

**Variable-first overhead:** ~1,150 tokens (1 variable def + bridge cases + rolling context + prompt)
**Country-first overhead:** ~6,300 tokens (all variables medium format + bridge cases with per-variable scores + rolling context + variable summary + prompt)

### Two-Tier Codebook

- **Full codebook:** Used during Steps 0-2 (design phases). Contains all anchor examples, methodological context, scale justifications.
- **Production codebook** (`codebook_production.md`): Generated at Step 2f.
  - Variable-first: contains ONLY the current variable's full definition (~150 tokens vs ~7,500 for all)
  - Country-first: contains medium-format definitions for all variables (~80 tokens/var vs ~150 full)

### Subagent Isolation for Majority Voting

Each majority-vote run = one Task-tool subagent (type: general-purpose) with a fresh, isolated context window. The subagent:

1. Reads ONLY `current_batch.json` — this file is **self-contained** (includes prompt template, variable definition, bridge cases with per-variable scores, rolling context, variable summary [country-first], CSV schema, and coding rules summary). Subagents cannot read auto-loaded rules files.
2. Codes all cells in the batch
3. Writes output to path specified in the Task prompt (per-run: `runs/run[N]_coded_*.csv`). Output path is NOT in `current_batch.json`.
4. Returns to the orchestrator: summary only (N cells, score distribution, bridge case values)

The subagent does NOT see: other runs' results, the parent conversation, the full conventions file, or any auto-loaded rules files. All 3 runs can execute in parallel.

**Validation and failure handling:** After each subagent returns, verify CSV exists with correct headers, row count, and score range. Retry failed runs once (new subagent). After retry failure, proceed with remaining valid runs (see `dataset-production-protocol.md` for full protocol).

### SessionStart Hook

A Python hook (`scripts/session-context-loader.py`) fires at session start and after auto-compaction:

- **Normal start:** Reads `coding_progress.json`, outputs progress summary
- **Post-compact:** Also re-injects `.context/batch_briefing.md` content

### Rules File Splitting

- **This file** (`dataset-construction-conventions.md`): Auto-loads during design phases (Steps 0-2, 5). Contains codebook design, calibration, documentation standards.
- **`dataset-production-protocol.md`**: Auto-loads during production coding (Step 3). Contains prompt template, CSV schema, majority voting rules, sentinel protocol, context management rules. ~200 lines vs ~900+ here.

This splitting saves ~3,200 tokens per production batch.

---

## Section 19: No-Gold-Standard Compensating Checks

**Purpose:** When the user opts out of gold-standard validation (Section 16), these automated checks partially compensate by catching errors that an expert would normally spot. They do NOT replace expert validation — they catch *inconsistency* and *fabrication*, not *systematic bias*.

**These checks activate automatically when `gold_standard_opted_out: true` in `coding_progress.json`.** When gold-standard IS present, these checks still run but at lower intensity (they're useful regardless, just more critical without expert validation).

### 19a. Cross-Variable Coherence Check

**What it catches:** Logically incoherent score profiles — e.g., a country scores high on `polygamy_restriction` but zero on `divorce_reform` in the same year. Possible, but suspicious enough to warrant re-examination.

**When:** After completing each country (country-first) or after all variables are coded for all countries (variable-first, as part of the post-coding consistency pass).

**Procedure:**

1. **Define expected correlation patterns** — during codebook design (Step 1), the workflow identifies variable pairs that should be positively or negatively correlated. These are stored in `coding_progress.json` under `coherence_rules`:
   ```json
   "coherence_rules": [
     {"var_a": "polygamy_restriction", "var_b": "divorce_reform", "direction": "positive", "reason": "Both reflect family law modernization"},
     {"var_a": "state_religion_control_direction", "var_b": "clergy_appointment", "direction": "negative", "reason": "More state control = less clerical autonomy"},
     {"var_a": "religious_education_state", "var_b": "kuttab_status", "direction": "positive", "reason": "Both reflect state control over religious education"}
   ]
   ```

2. **For each country-year**, compute a coherence score: how many variable pairs violate their expected direction by > 2 scale points? (e.g., `var_a = 4` and `var_b = 0` when they should be positively correlated).

3. **Flag** country-years with 2+ coherence violations. These are re-examined — the orchestrator logs them in the rolling context file and presents them in the batch summary.

4. **Resolution:** Flagged cells are NOT automatically recoded. They are presented for user review. If the user is unavailable (fully automated mode), they are logged in `disagreements_[concept].csv` with `resolution: "coherence_flag"`.

**Intensity:**
- With gold-standard: run as a reporting check (log, don't flag)
- Without gold-standard: run as an active check (flag for re-examination)

### 19b. Temporal Monotonicity Check

**What it catches:** Implausible year-over-year jumps — e.g., a score changes by 2+ points between consecutive years without evidence of a major event (coup, revolution, constitutional reform, landmark legislation).

**When:** After each batch merge (post-batch check, Step 3 item 5).

**Procedure:**

1. Scan all cells in the merged batch output for **year-over-year score changes ≥ 2** within the same country × variable.

2. For each flagged jump, check the `evidence` field: does it mention a major event (keywords: "coup", "revolution", "reform", "constitution", "abolished", "established", "war", "independence", "amendment", "law")?

3. **If a jump ≥ 2 lacks major-event evidence:** flag for re-examination. The jump may be real, but it needs stronger justification.

4. **Log** flagged jumps in the rolling context file under Alerts and in the batch summary.

**Scope limits:**
- Only checks consecutive years within the same country × variable. Does NOT flag jumps across era boundaries in bridge cases (those are expected).
- Threshold is **≥ 2**, not ≥ 1. Single-point changes are normal year-to-year variation.
- This is a heuristic, not a hard rule. Legitimate 2-point jumps exist (e.g., Iran 1979). The check ensures they have evidence.

**Intensity:**
- With gold-standard: report only (log jumps, don't flag)
- Without gold-standard: active check (flag for re-examination)

### 19c. Hallucination Audit Intensity Increase

**What it catches:** Fabricated evidence citations — the most dangerous failure mode without expert review.

**When:** Always (Section 5 governs pilot; data-sparsity escalation governs production batches).

**Adjustment when gold-standard is opted out:**
- Pilot audit: N=30 (up from 20)
- Production base rate: N=10 per batch (up from 5)
- Data-sparsity escalation thresholds unchanged, but the base rate they escalate FROM is higher:
  - 0 indicators triggered: 10 citations (was 5)
  - 1 indicator triggered: 15 citations (was 10)
  - 2+ indicators triggered: 20 citations (was 15)

**Rationale:** Without expert review, the hallucination audit is the ONLY external fabrication check. Doubling its intensity partially compensates. The cost is modest (~2x audit time per batch, negligible compared to 3x coding cost from majority voting).

### What These Checks Cannot Do

These automated checks catch **inconsistency** (cross-variable), **implausibility** (temporal jumps), and **fabrication** (hallucination audit). They cannot catch **systematic bias** — if Claude consistently misinterprets a concept (e.g., treats all Gulf monarchies as "high state control" when the reality is more nuanced), no automated check will catch it. Only expert validation can anchor the scores to ground truth. The methodology report must be transparent about this limitation.

---

## Section 20: Evidence Source Hierarchy

**Purpose:** Not all evidence is created equal. A score backed by a specific dated government action is more trustworthy than one inferred from a general regional characterization. The hierarchy serves three roles: (1) **reasoning scaffold** — forces Claude to evaluate its evidence quality *before* assigning a score, (2) **soft confidence signal** — creates friction when claiming HIGH confidence on weak evidence, (3) **post-hoc audit signal** — gives researchers a filterable column to target human review at the weakest cells.

**Design note:** This hierarchy is calibrated for **de facto coding** (the default in comparative politics). What counts as top-tier evidence is *documented practice*, not law on paper. For de jure codebooks, Tier 1 shifts to primary legal texts — but the 4-tier structure remains identical.

**Key design choice: NO hard confidence caps.** Tiers do not mechanically override confidence. Hard caps create a perverse incentive to inflate tiers (claim Tier 1 to unlock HIGH confidence) and destroy the signal value of the confidence field — if 40% of cells are MEDIUM purely because of evidence availability, MEDIUM becomes noise. Instead, Claude must *reason* about its evidence quality and *justify* when claiming high confidence on weak evidence.

### The 4 Tiers

Tiers reflect **specificity of the claim**, not the prestige of the source. What matters: can you pin the evidence to a concrete, dateable action? If yes → Tier 1, whether the source is a newspaper, academic paper, or government document.

| Tier | Label | What Qualifies | Examples |
|---|---|---|---|
| **1** | Specific documented event/action | A concrete, dateable event, action, or institutional fact is referenced. The evidence directly describes what happened and when. | "2005 Personal Status Code amended Art. 12" + evidence of enforcement; dated court ruling or executive decree; specific government action reported in contemporary media; official statistics with date and source; named policy implementation with documented outcomes |
| **2** | Institutional description of practice | A credible source describing how things actually work in practice, but without citing a single dateable event. Describes institutional patterns. | Academic case study describing day-to-day institutional operation; think tank or IGO report characterizing a country's practices (e.g., Freedom House country report, V-Dem country brief); investigative journalism describing systemic patterns; legal analysis of institutional design |
| **3** | Scholarly characterization | A credible academic or analytical source that *characterizes* a situation without directly documenting it. The evidence is an interpretation, not a primary observation. | "Zeghal (2008) argues that the Tunisian state controlled religious education through..."; comparative politics textbook characterization; cross-national dataset coding note; secondary source citing another source |
| **4** | General inference or pattern | No specific source cited. The evidence is a general statement about the country or region, or an inference from regime type, analogous cases, or undated claims. | "The country generally followed a secular model"; "As a Gulf monarchy, Oman likely..."; "Given the authoritarian regime, it is reasonable to assume..."; undated or vague claims; inference from regional patterns |

### How Tiers Guide Reasoning (the RULES section instruction)

The evidence hierarchy is injected into the **RULES section** of the production prompt (highest attention zone) as a reasoning instruction, not an output constraint:

> **Rule 6 [Evidence Hierarchy]:** Before assigning a score, classify your evidence:
> - **Tier 1** (specific dated event/action) — strongest basis. Assign score directly.
> - **Tier 2** (institutional description) — solid basis. Assign score with moderate confidence.
> - **Tier 3** (scholarly characterization) — indirect basis. Actively search your knowledge for something more concrete. If nothing exists, note this in evidence and consider whether the characterization is precise enough to determine a score.
> - **Tier 4** (general inference) — weakest basis. Consider UNABLE_TO_CODE. If you assign a score, it must be tentative.
>
> If your best evidence is Tier 3 or 4 and you assign HIGH confidence, you MUST explain why in the uncertainty_reason field — what makes this characterization reliable enough to be confident despite indirect evidence?

This creates **friction without prohibition**: Claude can still assign HIGH to a Tier 3 cell if the scholarly source is genuinely authoritative and precise, but it must justify it — and that justification becomes auditable.

### Confidence Interaction (soft signal, not hard cap)

| Best Evidence Tier | Default Expectation | HIGH Confidence Allowed? |
|---|---|---|
| Tier 1 | HIGH confidence is natural | Yes — no justification needed |
| Tier 2 | HIGH confidence is reasonable | Yes — no justification needed |
| Tier 3 only | MEDIUM confidence is expected | Yes — but MUST justify in `uncertainty_reason`: "HIGH despite Tier 3 because [specific reason]" |
| Tier 4 only | LOW confidence is expected | Yes — but MUST justify in `uncertainty_reason`: "HIGH despite Tier 4 because [specific reason]" |

**Post-hoc audit use:** Researchers can filter for `evidence_tier >= 3 AND confidence == "HIGH"` to find cells that warrant human review. The `uncertainty_reason` field contains the justification — if it's weak or formulaic, the cell should be re-examined.

### Rules

1. The `evidence_tier` is determined by the **best (lowest-numbered) evidence** cited in the cell's evidence field. If the evidence cites both a Tier 1 event and a Tier 3 characterization, the tier is 1.
2. Tiers reflect **evidence availability**, not coder quality. Data-sparse cases will naturally have higher tiers — that is informative, not a failing.
3. For de facto codebooks: a law or constitutional provision alone (without enforcement evidence) is **Tier 2 at best**, not Tier 1. Tier 1 requires evidence of actual practice.
4. Self-reported confidence may be lower than the tier suggests — a Tier 1 evidence cell can still be LOW confidence if the event's coding implications are ambiguous.

### CSV Column

| Column | Type | Description |
|---|---|---|
| evidence_tier | integer (1-4) or NA | Tier of the best evidence cited. 1 = specific dated event/action, 4 = general inference. NA if UNABLE_TO_CODE. |

This column is added to the output CSV schema (Section 7) between `evidence_date` and `uncertainty_reason`.

### Hallucination Audit: Tier Inflation Detection

**New failure mode:** Tier inflation — Claude claims Tier 1 evidence (specific dated event) but the evidence field contains only a general characterization (actual Tier 3 or 4). This is distinct from fabrication (claiming a non-existent event) — it's misclassifying the *type* of evidence. Without hard caps, the incentive to inflate tiers is reduced, but monitoring is still warranted.

**Added to hallucination audit procedure (Section 5):**
- When auditing evidence citations, also check the self-reported `evidence_tier`:
  - If tier = 1, the evidence MUST reference a specific dateable event, action, or document
  - If tier = 2, the evidence MUST reference a credible institutional source
  - If the evidence doesn't match its claimed tier, classify as **TIER_INFLATED** (new status alongside VERIFIED/PLAUSIBLE/FABRICATED)
- Compute tier inflation rate: TIER_INFLATED / total audited
- Threshold: tier inflation rate < 15%. If >= 15%: revise the tier definitions in the prompt template (they may be ambiguous)

### Rolling Context: Mean Evidence Tier

After each batch, the rolling context file tracks the **mean evidence tier** for the batch and cumulative. This surfaces data-sparsity patterns:
- A batch with mean tier > 2.5 is evidence-poor — flag in the rolling context Alerts section
- A variable with cumulative mean tier > 3.0 across all countries may not be reliably codeable — flag for review

### Token Cost

~80 additional tokens per batch: ~30 for the tier instruction in the prompt template, ~50 for the `evidence_tier` column values across cells. Negligible relative to total batch overhead.

---

## Section 21: Variable Curation Standards

**Purpose:** Standards for curating a brainstormed variable list into a codable set (Phase 0.5 of `/create-dataset`). Defines tier criteria, assessment lenses, output format, and decision rules.

### When Curation Applies

Variable curation is triggered when the user provides a pre-existing variable list with > ~15 variables. It is OPTIONAL — if the user arrives with only a concept name, Step 1 generates variables from scratch.

**The user's brainstorm is the starting point, not the ceiling.** Curation may add variables (Pass 4 gap suggestions) as well as remove them. Every recommendation ties back to the research question stated in the Step 0 interview.

### Tier Definitions

| Tier | Criteria | Implication for Step 1 |
|---|---|---|
| **Core** | Directly tests the research question. Codability is High or Medium. Not redundant. | Full codebook entry with complete anchor examples, inclusion/exclusion criteria, and methodological context. Designed first. |
| **Recommended** | Supports the research question (contextual, moderating, or control variable). Codability is High or Medium. Not redundant. OR: Core relevance but Low codability (high-risk, flagged). | Full codebook entry. Designed after Core variables. |
| **Optional** | Supporting relevance with Low codability, or Low coverage but conceptually interesting. | Abbreviated codebook entry (scale + basic criteria, fewer anchor examples). Designed last, only if budget allows. |
| **Drop** | Tangential to the research question, OR redundant with a surviving variable, OR Low codability AND Low coverage. | No codebook entry. Documented in curation report with reason for exclusion. |

### Assessment Lenses

Six lenses are applied simultaneously per variable (not as separate passes):

**1. Relevance** — How directly does this variable address the research question? Core variables are necessary for the analysis; Supporting variables provide context, controls, or moderation; Tangential variables are intellectually interesting but not connected to the research design.

**2. Redundancy** — Does this variable measure the same underlying concept as another variable? When two variables overlap substantially, recommend which survives based on: (a) which is more directly codable, (b) which has better cross-national coverage, (c) which is more closely aligned with the research question. The surviving variable inherits any unique information from the dropped one (noted in the curation report).

**3. Cross-national coverage** — What percentage of country-years in the dataset scope will have meaningful variation on this variable? Variables that are constant across all countries (e.g., a feature unique to one country) have low coverage and are poor candidates for cross-national coding. Estimate coverage as High (>70% of country-years show variation), Medium (40-70%), or Low (<40%).

**4. Temporal profile** — How does this variable change over time? Time-invariant events (e.g., "was X abolished?") are cheap to code but provide limited panel variation. Slow-moving institutions change across decades. Fast-changing policies change year-to-year. The temporal profile informs scale design in Step 1 and affects cell count (time-invariant events may need fewer years coded).

**5. Codability** — Can Claude reliably code this variable from training knowledge? High codability means most country-years will have Tier 1-2 evidence (specific events, institutional descriptions). Low codability means most country-years will rely on Tier 3-4 evidence (scholarly characterizations, general inference). Variables requiring specialized knowledge unlikely to be in Claude's training data (e.g., details of minority religious practice in small states) should be flagged as Low.

**6. Scale type** — Coarse recommendation only: Binary (0/1), Ordinal 0-2, Ordinal 0-4, Flag (contextual binary marker), or Composite (constructed from other variables, not directly coded). Step 1 designs the actual scale content. The curation recommendation flags cases where the wrong scale type would waste effort (e.g., designing a 5-point ordinal for something that is essentially binary).

### Flag Variables

Variables with contextualizing suffixes (`_clerical_control`, `_minority_differential`, `_state_power`, etc.) are binary indicators that modify or contextualize other variables in the same dimension. They are NOT standalone ordinal measures.

**Rules for flag variables:**
1. Always assign Scale type = Flag
2. Relevance assessment should consider the flag in relation to its parent dimension, not in isolation
3. Flag variables are typically Core if their parent dimension contains Core variables, Supporting otherwise
4. Redundancy: flag variables are rarely redundant with ordinal variables (they capture a different facet)
5. Cost: flags are cheap (binary, typically codable with HIGH confidence) — they add minimal cost to a dimension

### Cost Estimation

Use the formula: `total_cells = N_countries × N_years × N_variables × 3 (majority voting)`.

Per-cell cost ranges (from SKILL.md cost table):
- Pilot: ~$0.01-0.02 per cell (shorter coding, smaller context)
- Production: ~$0.01-0.03 per cell (full context, rolling calibration)

Time ranges:
- Pilot: ~100-200 cells/hour
- Production: ~50-150 cells/hour (includes post-batch checks, context loading)

Present configurations in decreasing order of cost: Full brainstorm > Core + Recommended + Optional > Core + Recommended > Core only. This makes the savings from curation tangible.

### Curation Report Format

See Phase 0.5 in SKILL.md for the full output template. The curation report is saved to `Replication/data/coded/curation_report.md` and the approved curated list to `Replication/data/coded/curated_variables.md`.

### Rules

1. Every keep/drop recommendation must reference the research question — no "this seems interesting" without connecting to the stated research design
2. Redundancy pairs must be identified with a clear winner and explanation
3. Cost projections must use the actual scope from the Step 0 interview (countries, years, voting strategy), not generic estimates
4. Claude-proposed additions (Pass 4) must be clearly marked and are never auto-included — user approval required
5. The curated list does not commit the user to any scale design — that happens in Step 1. Scale type recommendations are advisory.
6. If the user disagrees with a tier assignment, the user's decision is final. Update the curation report to reflect the override with the user's reasoning.
7. Curation does not replace domain expertise — Claude's assessments of relevance and codability are informed but fallible. The user should scrutinize recommendations for variables in their area of expertise.

---

## Integration Points

| Component | Connection |
|---|---|
| `/create-dataset` | Skill that orchestrates the coding workflow following these conventions |
| `coding-reliability-reviewer` | Agent that reviews coded data against these standards |
| `dataset-production-protocol.md` | Lean production rules (auto-loads during Step 3) |
| `panel-data-conventions.md` | Country codes, state transitions, merge protocols |
| `/prep-data` | Merges AI-coded output with existing datasets |
| `/reviewer-2` + Module Y | Interrogates papers using AI-coded data |
| `quality-gates.md` | Scores the coded dataset |
| `pdf-processing.md` | Handles uploaded reference materials |
| `curation_report.md` | Phase 0.5 output: full 4-pass curation analysis (Section 21) |
| `curated_variables.md` | Phase 0.5 output: approved variable list with tiers for Step 1 |
