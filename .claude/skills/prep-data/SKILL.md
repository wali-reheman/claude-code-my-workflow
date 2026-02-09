---
name: prep-data
description: Orchestrate data processing for polisci research. Downloads datasets, standardizes country codes, merges panels, validates joins, documents provenance, and generates a clean analysis-ready dataset. Follows panel-data-conventions.md.
argument-hint: "[task description, e.g., 'merge V-Dem and WDI for country-year panel 1990-2023'] [--paper paper_name] [--audit]"
---

# /prep-data — Political Science Data Processing

Build clean, merge-verified, documented analysis datasets from public political science data sources.

**Philosophy:** Data processing is where most replication failures originate. This skill enforces conventions that prevent silent errors — wrong codes, dropped observations, undocumented decisions — before they contaminate your analysis.

---

## What This Skill Does

1. **Downloads** datasets via R packages or guides manual download
2. **Standardizes** country codes using `countrycode` with explicit transition handling
3. **Cleans** dataset-specific issues (Polity special codes, WDI aggregates, V-Dem subsetting)
4. **Merges** multiple datasets into a single analysis panel with full diagnostics
5. **Validates** merge results (match rates, unmatched cases, duplicate detection)
6. **Documents** every decision in a data provenance file (`data/codebook.md`)
7. **Generates** numbered R scripts following project conventions

---

## What This Skill Does NOT Do

- Run your statistical analysis (that's separate)
- Choose your variables (you specify what you need)
- Decide how to handle missing data for causal inference (that's a research design decision — but it will surface the patterns for you)
- Build the replication package (that's `/submission-checklist` — but it structures code to be replication-ready from the start)

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `[task]` | YES | Natural language description of what data you need |
| `--paper` | NO | Link to a manuscript folder — will read `main.tex` for variable hints |
| `--audit` | NO | Audit-only mode: review existing data scripts against `panel-data-conventions.md` without writing new code |
| `--datasets` | NO | Explicitly list datasets: `--datasets "V-Dem, WDI, UCDP"` |
| `--years` | NO | Year range: `--years 1990-2023` |
| `--unit` | NO | Unit of analysis: `country-year`, `dyad-year`, `country-month`, `event` |

---

## Workflow

### Step 0: Parse & Plan

1. Parse `$ARGUMENTS` for task description, datasets, year range, and unit of analysis
2. Read `panel-data-conventions.md` for cleaning protocols and merge standards
3. Read `r-code-conventions.md` for script structure requirements
4. Read `./PROJECT_MEMORY.md` for `[LEARN:data]`, `[LEARN:merge]`, `[LEARN:r-code]` entries
5. If `--paper` specified: read the manuscript for variable names, data descriptions, and sample definitions
6. If `--audit` specified: skip to Step 6 (audit mode)

**Present a data processing plan before writing any code:**

```
## Data Processing Plan

**Goal:** [what the user asked for]
**Unit of analysis:** [country-year / dyad-year / etc.]
**Year range:** [start-end]
**Primary identifier:** [ISO-3 / COW / etc.]

### Datasets to Process
1. [Dataset] — via [package/download] — key variables: [list]
2. [Dataset] — via [package/download] — key variables: [list]

### Merge Strategy
- Primary dataset: [which one forms the base panel]
- Join order: [sequence of left_joins]
- Expected final N: ~[estimate] observations

### Known Pitfalls
- [Dataset-specific issues from panel-data-conventions.md]

### Scripts to Create
- `01_download_data.R`
- `02_clean_[name].R` (one per dataset)
- `03_merge_panel.R`
- `04_construct_variables.R` (if derived variables needed)
```

**GATE: Wait for user approval before writing scripts.**

### Step 1: Download / Load Scripts

For each dataset, generate the appropriate download script:

**Datasets with R packages (preferred — reproducible):**

| Dataset | Code Pattern |
|---|---|
| V-Dem | `library(vdemdata); vdem_raw <- vdem` |
| WDI | `library(WDI); wdi_raw <- WDI(indicator = c(...), extra = TRUE)` |
| Polity V | `library(democracyData); polity_raw <- download_polity5()` |
| Freedom House | `library(democracyData); fh_raw <- download_fh()` |
| COW dyads | `library(peacesciencer); dyads <- create_dyadyears(...)` |
| COW state system | `library(states); cow_states <- cowstates` |

**Datasets requiring manual download:**

| Dataset | Instructions |
|---|---|
| ACLED | API registration required — generate download script with API placeholder |
| UCDP-GED | Direct download from ucdp.uu.se — provide URL and `read_csv()` code |
| Afrobarometer | Download from afrobarometer.org — provide `haven::read_dta()` code |
| CLEA | Download from electiondataarchive.org |
| QoG | Download from qog.pol.gu.se |

For manual downloads:
1. Create `data/raw/` directory
2. Generate placeholder script with download URL and instructions
3. Generate loading code assuming the file will be placed in `data/raw/`
4. Save raw data as `.rds` after first load for faster subsequent access

### Step 2: Clean Scripts (One Per Dataset)

For each dataset, generate a cleaning script following Protocol A-F from `panel-data-conventions.md`:

**Every cleaning script MUST:**

1. Start with the standard header (script name, purpose, input, output)
2. Load the raw data
3. Apply dataset-specific cleaning protocol:
   - **Polity:** Recode -66, -77, -88 (Protocol A)
   - **V-Dem:** Select variables, filter to sovereign states (Protocol B)
   - **WDI:** Remove aggregates, handle temporal gaps (Protocol C)
   - **Survey data:** Standardize variables, apply weights (Protocol D)
   - **Event data:** Define inclusion criteria, aggregate, create zeros (Protocol E)
   - **Dyadic data:** Construct properly, merge country-level twice (Protocol F)
4. Standardize the country identifier using `countrycode()` with `custom_match` for transitions
5. Check for and remove duplicates in the merge key
6. Save cleaned data to `data/processed/[name]_clean.rds`
7. Print a cleaning summary (N observations, N countries, year range, missingness)

### Step 3: Merge Script

Generate `03_merge_panel.R` following the Merge Protocol (Section 4 of `panel-data-conventions.md`):

```r
# === MERGE PROTOCOL ===

# Step 1: Load all cleaned datasets
vdem   <- readRDS("data/processed/vdem_clean.rds")
wdi    <- readRDS("data/processed/wdi_clean.rds")
# ... etc

# Step 2: Pre-merge checks
# Check for duplicates in merge keys
stopifnot(!any(duplicated(vdem[, c("iso3c", "year")])))
stopifnot(!any(duplicated(wdi[, c("iso3c", "year")])))

# Step 3: Sequential left joins
panel <- vdem %>%                           # Primary dataset (largest coverage)
  left_join(wdi, by = c("iso3c", "year"))   # Add economic data

# Step 4: Merge diagnostics (MANDATORY after every join)
message("\n=== Merge Diagnostic: V-Dem + WDI ===")
message("V-Dem rows:  ", nrow(vdem))
message("WDI rows:    ", nrow(wdi))
message("Merged rows: ", nrow(panel))
message("Match rate:  ", round(sum(!is.na(panel$gdp_pc)) / nrow(panel) * 100, 1), "%")

# Step 5: Investigate unmatched
unmatched <- panel %>%
  filter(is.na(gdp_pc)) %>%
  distinct(iso3c) %>%
  pull(iso3c)
message("Unmatched countries: ", paste(unmatched, collapse = ", "))

# Repeat for each additional dataset...

# Step 6: Final panel summary
message("\n=== Final Panel ===")
message("Observations: ", nrow(panel))
message("Countries:    ", n_distinct(panel$iso3c))
message("Year range:   ", min(panel$year), "-", max(panel$year))

# Step 7: Missing data summary
panel %>%
  summarise(across(everything(), ~round(sum(is.na(.)) / n() * 100, 1))) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "pct_missing") %>%
  filter(pct_missing > 0) %>%
  arrange(desc(pct_missing)) %>%
  print(n = Inf)

# Step 8: Save
saveRDS(panel, "data/processed/analysis_panel.rds")
```

### Step 4: Variable Construction (if needed)

If the user needs derived variables (lags, logs, interactions, indices):

```r
# 04_construct_variables.R
panel <- readRDS("data/processed/analysis_panel.rds")

panel <- panel %>%
  group_by(iso3c) %>%
  arrange(year) %>%
  mutate(
    # Lags (CAREFUL: don't lag across state transitions)
    gdp_pc_lag1 = lag(gdp_pc, 1),
    # Verify no transition in lagged data
    # [CHECK: does iso3c change? Are there gaps in years?]

    # Logs
    ln_gdp_pc = log(gdp_pc),

    # Growth rates
    gdp_growth = (gdp_pc - lag(gdp_pc)) / lag(gdp_pc) * 100
  ) %>%
  ungroup()

saveRDS(panel, "data/processed/analysis_panel_final.rds")
```

### Step 5: Generate Documentation

Create/update `data/codebook.md` with:

1. **Data sources table** (dataset, source URL, download date, version, file)
2. **Variable definitions** (name, description, source dataset, original variable name, transformation applied)
3. **Country code decisions** (which system used as primary, how transitions were handled)
4. **Cleaning decisions** (Polity recoding choice, event type inclusion, etc.)
5. **Merge diagnostics** (match rates, unmatched cases, explanations)
6. **Missing data summary** (by variable and by country)
7. **Final panel description** (N, countries, year range, balance)

### Step 6: Audit Mode (when `--audit` flag is present)

Review existing data scripts against `panel-data-conventions.md`:

1. **Read all R scripts** in `Replication/code/` or `scripts/`
2. **Check against Section 7 pitfalls checklist** — every item
3. **Check merge diagnostics** — are they present after every join?
4. **Check country code handling** — is `countrycode` used? Are transitions handled?
5. **Check documentation** — does `codebook.md` exist? Is it complete?
6. **Check for common errors:**
   - Polity special codes not recoded
   - WDI aggregates not filtered
   - Inner joins without dropped-N reporting
   - Event data without explicit zeros
   - Survey data without weights

**Produce audit report to `quality_reports/data_audit.md`**

### Step 7: Present Results

```
## /prep-data Summary

**Task:** [description]
**Unit:** [country-year / dyad-year / etc.]
**Coverage:** [N] countries, [start]-[end]

### Scripts Created
- `01_download_data.R` — downloads/loads [N] datasets
- `02_clean_vdem.R` — [N] variables selected, [M] observations
- `02_clean_wdi.R` — [N] indicators, aggregates removed
- `03_merge_panel.R` — [N] sequential joins, [M]% overall match rate
- `04_construct_variables.R` — [N] derived variables

### Merge Diagnostics
| Join | Left N | Right N | Merged N | Match Rate |
|------|--------|---------|----------|------------|
| V-Dem + WDI | X | Y | Z | 95% |
| + UCDP | Z | W | Z | 87% |

### Data Quality
- Missing data: [top 3 variables with highest missingness]
- Unmatched countries: [list, with explanation]
- Panel balance: [balanced / unbalanced — if unbalanced, why]

### Output
- `data/processed/analysis_panel.rds` — [N] obs, [M] variables
- `data/codebook.md` — full documentation

### Next Steps
- Run `/review-r` on the data scripts
- Proceed to analysis (`05_analysis.R`)
```

---

## Dataset-Specific Quick Reference

For each dataset, the skill knows which cleaning protocol to apply:

| Dataset | Cleaning Protocol | Key Rule |
|---|---|---|
| V-Dem | Protocol B | Select variables BEFORE merging; filter non-sovereign |
| Polity V | Protocol A | Recode -66/-77/-88 ALWAYS; document choice |
| Freedom House | Custom | Handle 2003 scale change |
| WDI | Protocol C | `extra = TRUE`; filter aggregates; handle temporal gaps |
| UCDP/ACLED | Protocol E | Create explicit zeros; don't combine across datasets |
| Afrobarometer/WVS | Protocol D | ALWAYS use survey weights; wave ≠ year |
| COW/GW dyads | Protocol F | Merge country-level data TWICE |
| QoG | Custom | Pre-merged — verify variable provenance |

---

## Integration Points

| Component | Connection |
|---|---|
| **`panel-data-conventions.md`** | Source of all cleaning protocols, merge rules, pitfalls checklist |
| **`r-code-conventions.md`** | Script structure, header format, output conventions |
| **`replication-protocol.md`** | Data preparation feeds into replication workflow |
| **`manuscript-conventions.md`** | Replication package structure (Section 8) |
| **`polisci-data-engineer` agent** | Reviews data processing code against conventions |
| **`r-reviewer` agent** | Reviews R code quality |
| **`/create-paper`** | Phase 2 (Inputs) uses this skill to prepare analysis data |
| **`/reviewer-2`** | Lens 2 (Data & Measurement) reviews data quality |

---

## Principles

1. **Every merge gets diagnostics.** No silent joins. Match rate, unmatched cases, and row counts after every `left_join`.
2. **Country codes are treacherous.** Always use `countrycode` with explicit `custom_match` for transitions. Never merge by country name.
3. **Zeros are data.** In event/conflict datasets, country-years with zero events must be explicitly created — they are not missing.
4. **Document as you go.** Every cleaning decision goes in `codebook.md` immediately, not at the end.
5. **Raw data is sacred.** Never modify files in `data/raw/`. All transformations happen in scripts and save to `data/processed/`.
6. **Reproducibility from the start.** Use R packages for downloads when available. Record exact versions and download dates.
7. **Separate cleaning from analysis.** Data processing scripts (01-04) should produce a clean `.rds` file. Analysis scripts (05+) should load that file and never touch raw data.
