---
paths:
  - "Replication/**"
  - "scripts/**/*.R"
  - "data/**"
---

# Panel Data Conventions for Political Science

**Purpose:** Standardize how country-year (and other panel) datasets are constructed, merged, cleaned, and documented. This rule prevents the most common data processing errors in comparative politics and international relations research.

**Scope:** This rule covers data acquisition, identifier systems, merging, cleaning, and documentation. It does NOT cover:

| Concern | Handled By |
|---|---|
| R code style and structure | `r-code-conventions.md` |
| Replication package standards | `replication-protocol.md` + `manuscript-conventions.md` Section 8 |
| Estimator choice and robustness | `robustness-checklists.md` |
| Research design methodology | `methodology-reviewer` agent |

---

## Section 1: Identifier Systems

Political science has no universal country code. Every dataset uses a different system. Understanding these differences prevents silent merge failures.

### The Big Five Coding Systems

| System | Type | Range/Format | Coverage | Maintained By | Key Characteristic |
|---|---|---|---|---|---|
| **COW** (Correlates of War) | Numeric | 2-990 | 1816-2016 | COW Project | Treats successor states as continuous (USSR→Russia = 365) |
| **GW** (Gleditsch-Ward) | Numeric | Similar to COW | 1816-present | Gleditsch & Ward | Slight derivation from COW; some codes differ |
| **ISO 3166-1 alpha-3** | Alpha | 3 letters (USA, GBR) | Current | ISO | UN/WHO standard; new codes for new states |
| **ISO 3166-1 alpha-2** | Alpha | 2 letters (US, GB) | Current | ISO | Internet/World Bank standard |
| **ISO 3166-1 numeric** | Numeric | 3 digits | Current | ISO | New numeric code for territorial changes |

### Critical Divergences

These cases cause silent merge failures if not handled explicitly:

| Entity | COW | GW | ISO-3 | Transition | What Can Go Wrong |
|---|---|---|---|---|---|
| **USSR → Russia** | 365 (continuous) | 365 (continuous) | SUN → RUS | 1991 | COW/GW treat as same entity; ISO treats as different. Merging by ISO drops all USSR observations. |
| **Yugoslavia → Serbia** | 345 → 340 | 345 → 340 | YUG → SRB | 1991-2006 | Multiple successor states with different independence dates across datasets |
| **Czechoslovakia** | 315 → 316/317 | 315 → 316/317 | CSK → CZE/SVK | 1993 | "Velvet Divorce" — clean split but code schemes differ |
| **Germany** | 260+265 → 255 | 260+265 → 255 | DDR+DEU → DEU | 1990 | Unification — different datasets handle transition year differently |
| **Vietnam** | 816+817 → 816 | 816+817 → 816 | VNM | 1976 | Unification under communist government |
| **Yemen** | 678+680 → 679 | 678+680 → 679 | YEM | 1990 | North + South Yemen → Republic of Yemen |
| **Ethiopia/Eritrea** | 530 → 530+531 | 530 → 530+531 | ETH + ERI | 1993 | Eritrean independence; COW treats Ethiopia as continuous |
| **Sudan/South Sudan** | 625 → 625+626 | 625 → 625+626 | SDN + SSD | 2011 | South Sudan independence |
| **Timor-Leste** | 860 | 860 | TLS | 2002 | Independence from Indonesia |

**Rule:** Always document which coding system you use as primary and how you handle transitions. Never assume COW = GW = ISO.

### The `countrycode` Package

**This is the canonical tool for code conversion in R.** Always use it instead of manual lookup tables.

```r
library(countrycode)

# Basic conversion
df$iso3c <- countrycode(df$cow_code, origin = "cown", destination = "iso3c")

# For panel data: use codelist_panel (one row per country-year, pre-reconciled)
panel_codes <- countrycode::codelist_panel

# Custom matches for unmatched cases (ALWAYS handle these explicitly)
df$iso3c <- countrycode(df$cow_code, origin = "cown", destination = "iso3c",
                         custom_match = c("345" = "SRB",  # Yugoslavia → Serbia
                                          "678" = "YEM")) # North Yemen → Yemen
```

**Rules:**
1. NEVER use manual lookup tables when `countrycode` can do the conversion
2. ALWAYS check for `NA` values after conversion — they indicate unmatched codes
3. ALWAYS use `custom_match` for known ambiguous cases rather than silently dropping them
4. For panel data, prefer `codelist_panel` over `codelist` — it already handles transitions
5. Document every `custom_match` decision in a comment explaining why

---

## Section 2: Major Dataset Reference

Quick reference for datasets frequently used in comparative politics and IR. Organized by domain.

### Democracy & Governance

| Dataset | Package | Unit | Coverage | Key Variables | Gotchas |
|---|---|---|---|---|---|
| **V-Dem** | `vdemdata` | Country-year | 1789-present | 450+ indicators, polyarchy, liberal, etc. | Very wide — select variables before merging |
| **Polity V** | `democracyData` | Country-year | 1800-2018 | polity2, democ, autoc | **Special codes: -66, -77, -88 (see Section 3)** |
| **Freedom House** | `democracyData` | Country-year | 1973-present | PR, CL, FIW status | Scale changed in 2003 |
| **QoG (Quality of Governance)** | Manual download | Country-year | Varies | 2500+ variables from 100+ sources | Pre-merged omnibus — convenient but check variable provenance |
| **WGI (World Governance Indicators)** | `WDI` | Country-year | 1996-present | 6 governance dimensions | Estimates, not direct measures; confidence intervals matter |

### Economic

| Dataset | Package | Unit | Coverage | Key Variables | Gotchas |
|---|---|---|---|---|---|
| **World Bank WDI** | `WDI` | Country-year | 1960-present | 1600+ indicators | Uses ISO-2; temporal gaps by country; use `extra = TRUE` |
| **Penn World Table** | `pwt10` / manual | Country-year | 1950-2019 | GDP, capital, productivity | Multiple GDP concepts (PPP, exchange rate) |
| **Maddison Project** | Manual | Country-year | 1-2018 | Historical GDP per capita | Very long time series but thin coverage early |
| **IMF WEO** | Manual | Country-year | Varies | Fiscal, monetary, trade | Forecasts included — filter for actuals only |

### Conflict & Violence

| Dataset | Package | Unit | Coverage | Key Variables | Gotchas |
|---|---|---|---|---|---|
| **UCDP/PRIO Armed Conflict** | `peacesciencer` | Country-year / dyad-year | 1946-present | Conflict type, intensity | Conservative coding; underreports rural areas |
| **UCDP-GED** | Manual | Event (georeferenced) | 1989-present | Deaths, location, actors | Requires aggregation to country-year |
| **ACLED** | Manual (API) | Event (georeferenced) | 1997-present | Event type, fatalities, actors | Uneven quality control; different coding rules than UCDP |
| **SCAD** | Manual | Event | 1990-2017 | Protests, riots, repression | Africa + Latin America only |
| **GTD** | Manual | Event | 1970-2020 | Terrorism events | Different definition of "terrorism" than UCDP |
| **COW MID** | `peacesciencer` | Dyad-year | 1816-2014 | Militarized interstate disputes | Directed vs undirected dyads matter |

### Elections

| Dataset | Package | Unit | Coverage | Key Variables | Gotchas |
|---|---|---|---|---|---|
| **CLEA** | Manual | Constituency-election | Varies | Votes, seats per party | Constituency boundaries change |
| **V-Dem Elections** | `vdemdata` | Election-level | 1789-present | Election quality indicators | Nested in V-Dem country-year |
| **ParlGov** | Manual | Election/cabinet | EU + OECD | Party positions, coalitions | Limited to democracies |
| **IDEA Voter Turnout** | Manual | Election-level | 1945-present | Turnout rates | Registered voters sometimes > voting age population |

### Surveys

| Dataset | Package | Unit | Coverage | Key Variables | Gotchas |
|---|---|---|---|---|---|
| **Afrobarometer** | Manual | Individual | Africa (R1-R9) | Democratic attitudes, trust | Use `Combinwt` for cross-national; waves are not annual |
| **WVS** | Manual | Individual | Global (7 waves) | Values, beliefs | Wave timing differs by country |
| **ANES** | Manual | Individual | US only | Vote choice, ideology | US-only; not for cross-national |
| **Eurobarometer** | Manual | Individual | EU | EU attitudes, economics | Sampling frame changes with EU expansion |
| **LAPOP/AmericasBarometer** | Manual | Individual | Latin America + Caribbean | Democratic attitudes, corruption | Complex survey design; use weights |
| **Arab Barometer** | `retroharmonize` | Individual | MENA (6 waves) | Governance, religion, identity | Variable names inconsistent across waves |

### Dyadic & Relational

| Dataset | Package | Unit | Coverage | Key Variables | Gotchas |
|---|---|---|---|---|---|
| **COW Trade** | `peacesciencer` | Dyad-year | 1870-2014 | Bilateral trade flows | Directed; importer vs exporter reports may differ |
| **CEPII Gravity** | Manual | Dyad-year | 1948-present | Distance, colonial ties, language | Pre-computed gravity variables |
| **Alliance Treaty Obligations** | `peacesciencer` | Dyad-year | 1816-2018 | Alliance type | ATOP vs COW alliances differ |
| **UN Comtrade** | Manual/API | Bilateral-commodity-year | Varies | Commodity-level trade | Very granular; requires aggregation decisions |

---

## Section 3: Data Cleaning Protocols

### Protocol A: Polity Special Codes

Polity V uses special codes that MUST be recoded before analysis. Failure to recode them is one of the most common errors in polisci replication packages.

| Code | Meaning | Standard Recoding | Rationale |
|---|---|---|---|
| **-66** | Foreign "interruption" | `NA` (system missing) | Country not sovereign; score is meaningless |
| **-77** | Interregnum / anarchy | `NA` or `0` (depends on research question) | No functioning polity; `0` treats as "neutral" on dem-aut scale |
| **-88** | Transition period | Prorate across transition span, or `NA` | Score will change; prorating uses start/end values |

```r
# Standard Polity recoding — ALWAYS include this in cleaning scripts
df <- df %>%
  mutate(
    polity2_clean = case_when(
      polity2 %in% c(-66, -77, -88) ~ NA_real_,  # Conservative: all to NA
      TRUE ~ polity2
    )
  )

# Alternative: -77 to 0 (treat anarchy as neutral)
# Document your choice and justify it
```

**Rule:** ALWAYS document which recoding you chose and why. Different choices can change your results.

### Protocol B: V-Dem Variable Selection

V-Dem has 450+ variables. Loading the full dataset and merging it is wasteful and error-prone.

```r
library(vdemdata)

# GOOD: Select only what you need
vdem_subset <- vdem %>%
  select(country_name, country_text_id, year, COWcode,
         v2x_polyarchy, v2x_libdem, v2x_partipdem,
         v2x_delibdem, v2x_egaldem) %>%
  filter(year >= 1900)

# BAD: Merging the full 30MB dataset
# df <- left_join(df, vdem, by = c("cow_code" = "COWcode", "year"))
```

**Rules:**
1. ALWAYS select variables before merging — never merge the full V-Dem dataset
2. Use `COWcode` for merging with COW-coded datasets, `country_text_id` for ISO-3
3. Be aware that V-Dem includes non-sovereign entities (colonies, occupied territories) — filter if needed
4. V-Dem indices (v2x_*) are on different scales than Polity or Freedom House — never directly compare values

### Protocol C: World Bank WDI Downloads

```r
library(WDI)

# GOOD: Specify exactly what you need
wdi_data <- WDI(
  country = "all",        # Or specific ISO-2 codes: c("US", "GB", "FR")
  indicator = c(
    gdp_pc = "NY.GDP.PCAP.KD",        # GDP per capita (constant 2015 US$)
    pop = "SP.POP.TOTL",               # Total population
    gini = "SI.POV.GINI"               # Gini index
  ),
  start = 1990,
  end = 2023,
  extra = TRUE             # Adds iso3c, region, incomeLevel
)

# ALWAYS filter out aggregates (World Bank includes regional/income group aggregates)
wdi_data <- wdi_data %>%
  filter(!is.na(iso3c))    # Removes aggregates like "World", "Sub-Saharan Africa"

# For temporal gaps: use most recent non-empty value
wdi_recent <- WDI(
  country = "all",
  indicator = c(gini = "SI.POV.GINI"),
  start = 2015, end = 2023,
  extra = TRUE
) %>%
  filter(!is.na(iso3c)) %>%
  group_by(iso3c) %>%
  filter(!is.na(gini)) %>%
  slice_max(year, n = 1) %>%  # Keep most recent non-NA observation
  ungroup()
```

**Rules:**
1. ALWAYS use `extra = TRUE` to get ISO-3 codes and region info
2. ALWAYS filter out aggregate rows (World, regions, income groups) — they have `iso3c = NA`
3. Name indicators in the `WDI()` call for human-readable column names
4. Document the exact indicator codes used — names change across WDI updates
5. Be explicit about constant vs current dollars for GDP variables

### Protocol D: Survey Data Harmonization

When merging survey data across waves or across barometer programs:

```r
library(retroharmonize)  # For cross-survey harmonization

# Step 1: Standardize variable names
# Different waves may name the same variable differently
# "date" vs "date_of_interview" vs "int_date"

# Step 2: Standardize value labels
# "Algeria" vs "algeria" vs "1. Algeria" — all must match

# Step 3: Apply survey weights
# Afrobarometer: ALWAYS use "Combinwt" for cross-national comparisons
# It standardizes effective sample sizes across countries

# Step 4: Aggregate to country-level (if needed for panel)
# Document aggregation function (mean, median, proportion)
# Report N per country — small N countries should be flagged
```

**Rules:**
1. ALWAYS use survey weights when aggregating to country level
2. Document which weight variable you use and why
3. Survey waves are NOT annual — do not treat wave number as year
4. When merging survey aggregates into country-year panels, use the actual fieldwork year, not the wave label
5. Report the within-country N for each survey observation — analyses may be driven by small-N countries

### Protocol E: Event Data Aggregation

When converting event-level data (ACLED, UCDP-GED, GTD) to country-year panels:

```r
# Step 1: Define aggregation rules BEFORE coding
# What counts as an "event"? Which event types are included?
# Document inclusion/exclusion criteria

# Step 2: Aggregate
events_cy <- events %>%
  filter(event_type %in% c("battles", "violence_against_civilians")) %>%
  group_by(country, year) %>%
  summarise(
    n_events = n(),
    total_fatalities = sum(fatalities, na.rm = TRUE),
    max_fatalities = max(fatalities, na.rm = TRUE),
    .groups = "drop"
  )

# Step 3: Handle country-years with ZERO events
# These are REAL observations (peace), not missing data
# Must be explicitly created
all_cy <- expand_grid(
  country = unique(events_cy$country),
  year = min(events_cy$year):max(events_cy$year)
)
events_cy <- left_join(all_cy, events_cy) %>%
  mutate(across(c(n_events, total_fatalities), ~replace_na(., 0)))
```

**Rules:**
1. Zero-event country-years are DATA, not missing — create them explicitly
2. Document event type inclusion criteria
3. ACLED and UCDP code the same events differently — never combine counts across datasets without harmonization
4. Fatality estimates from different datasets are NOT comparable (different coding rules)
5. Georeferenced data: document the spatial aggregation unit (admin1, admin2, country)

### Protocol F: Dyad-Year Data Construction

When building dyadic datasets (trade, conflict, alliances):

```r
library(peacesciencer)

# GOOD: Use peacesciencer for standard dyad construction
dyad_data <- create_dyadyears(subset_years = 1945:2014) %>%
  add_cow_trade() %>%
  add_democracy()   # Adds democracy scores for BOTH sides

# IMPORTANT: Country-year data must be merged TWICE into dyad-year
# Once for ccode1 (side A) and once for ccode2 (side B)
dyad_data <- dyad_data %>%
  left_join(country_data, by = c("ccode1" = "cow_code", "year")) %>%
  rename_with(~paste0(., "_1"), .cols = new_cols) %>%
  left_join(country_data, by = c("ccode2" = "cow_code", "year")) %>%
  rename_with(~paste0(., "_2"), .cols = new_cols)
```

**Rules:**
1. Directed vs undirected dyads: know the difference and document your choice
2. Country-year variables must be merged TWICE — once per side of the dyad
3. Dyadic observations are NOT independent — cluster standard errors appropriately
4. Use `peacesciencer` for standard COW-based dyads — don't build from scratch
5. The number of dyads grows quadratically with the number of states — filter early

---

## Section 4: Merge Protocol

The merge is where most data errors occur. Follow this protocol for every merge.

### Pre-Merge Checklist

Before any `left_join`, `inner_join`, or `merge`:

- [ ] **Identify the unit of analysis** in both datasets (country-year? country-month? individual?)
- [ ] **Identify the key variables** used for merging (which country code? which year variable?)
- [ ] **Check for duplicates** in the key variables of both datasets
- [ ] **Check the coding system** — are both datasets using the same country codes?
- [ ] **Check temporal coverage** — do both datasets cover the same years?
- [ ] **Document expected merge outcome** — how many observations should match?

### Merge Execution

```r
# Step 1: Standardize identifiers BEFORE merging
df_a <- df_a %>%
  mutate(iso3c = countrycode(cow_code, "cown", "iso3c",
                              custom_match = c(...)))

df_b <- df_b %>%
  mutate(iso3c = countrycode(country_name, "country.name", "iso3c",
                              custom_match = c(...)))

# Step 2: Check for duplicates in merge keys
stopifnot(!any(duplicated(df_a[, c("iso3c", "year")])))
stopifnot(!any(duplicated(df_b[, c("iso3c", "year")])))

# Step 3: Merge
merged <- left_join(df_a, df_b, by = c("iso3c", "year"))

# Step 4: ALWAYS check merge diagnostics
message("Dataset A: ", nrow(df_a), " rows")
message("Dataset B: ", nrow(df_b), " rows")
message("Merged:    ", nrow(merged), " rows")
message("Matched:   ", sum(!is.na(merged$key_var_from_b)), " rows")
message("Unmatched: ", sum(is.na(merged$key_var_from_b)), " rows")

# Step 5: Investigate unmatched observations
unmatched <- merged %>%
  filter(is.na(key_var_from_b)) %>%
  distinct(iso3c, year)
# Are these expected? (e.g., countries not in dataset B)
# Or are these merge errors? (e.g., code mismatches)
```

### Post-Merge Validation

| Check | How | Severity |
|---|---|---|
| Row count reasonable | Compare to expected N | FAIL if wildly different |
| No unexpected duplicates | `nrow(merged) == nrow(df_a)` for left join | FAIL if row explosion |
| Match rate acceptable | `sum(!is.na(key_var)) / nrow(merged)` | WARN if < 80% |
| Unmatched cases explained | Review `anti_join(df_a, df_b)` | WARN if unexplained |
| No country-code artifacts | Spot-check merged data for obvious mismatches | FAIL if present |
| Key variables have expected range | `range(merged$gdp_pc, na.rm = TRUE)` | WARN if extreme |

### Join Type Decision

| Join Type | When to Use | Risk |
|---|---|---|
| `left_join(a, b)` | Keep all observations from `a`, add matching data from `b` | Unmatched rows get `NA` — acceptable if documented |
| `inner_join(a, b)` | Keep only observations that exist in BOTH datasets | **Silently drops observations** — always report how many dropped |
| `full_join(a, b)` | Keep everything from both datasets | Can create unexpected `NA` patterns |
| `anti_join(a, b)` | Find observations in `a` that DON'T match `b` | Diagnostic tool — use to investigate unmatched cases |

**Default rule:** Use `left_join` with your analysis dataset as `a`. Always report the match rate.

---

## Section 5: Missing Data Documentation

### Report Missing Data Explicitly

Every cleaning script should produce a missingness summary:

```r
# At the end of every cleaning script, produce this summary
missingness <- merged %>%
  summarise(across(everything(), ~sum(is.na(.)) / n() * 100)) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "pct_missing") %>%
  filter(pct_missing > 0) %>%
  arrange(desc(pct_missing))

message("\n=== Missing Data Summary ===")
print(missingness, n = Inf)

# Also report by country (which countries are driving missingness?)
country_miss <- merged %>%
  group_by(iso3c) %>%
  summarise(pct_complete = mean(complete.cases(.)) * 100) %>%
  filter(pct_complete < 80) %>%
  arrange(pct_complete)
```

### Missing Data Decision Tree

| Pattern | Likely Mechanism | Standard Treatment | Document |
|---|---|---|---|
| Random gaps across countries/years | MCAR | Listwise deletion acceptable | Sample size before/after |
| Concentrated in poor/autocratic countries | MAR (conditional on observables) | Multiple imputation or bounded analysis | Which countries, which years |
| Variable not measured until year X | Structural | Restrict sample to post-X or use alternative measure | Why you chose this cutoff |
| Survey not conducted in year Y | Design feature | Interpolation or restrict to survey years | Interpolation method if used |
| Conflict data zero vs missing | Ambiguous | Code as zero if country is in dataset coverage | Coverage rules of the dataset |

**Rule:** NEVER silently drop observations due to missingness. Always report the N before and after any sample restriction and explain why observations were dropped.

---

## Section 6: Script Structure for Data Processing

### Naming Convention

```
Replication/code/
├── 00_master.R                    # Runs everything in order
├── 01_download_data.R             # Downloads/loads raw data
├── 02_clean_[dataset_name].R      # One script per raw dataset
├── 03_merge_panel.R               # Merges all cleaned datasets
├── 04_construct_variables.R       # Creates derived variables
├── 05_analysis.R                  # Main analysis
├── 06_robustness.R                # Robustness checks
├── 07_figures.R                   # All figures
└── sessionInfo.txt                # R session info
```

### Script Header Template for Data Scripts

Every data processing script MUST begin with:

```r
# ============================================================
# Script: 02_clean_vdem.R
# Purpose: Clean and subset V-Dem data for analysis
# Input:  data/raw/vdem_v14.rds (or downloaded via vdemdata package)
# Output: data/processed/vdem_clean.rds
# Author: [Name]
# Date:   [YYYY-MM-DD]
# Notes:  V-Dem v14, using COWcode for merging
#         Selected variables: polyarchy, liberal democracy, electoral democracy
#         Coverage: 1900-2023, sovereign states only
# ============================================================
```

### Data Provenance Documentation

For every raw data file, document in `data/codebook.md`:

```markdown
## Data Sources

### V-Dem v14
- **Source:** https://v-dem.net/data/the-v-dem-dataset/
- **Downloaded:** 2026-01-15
- **Version:** v14
- **File:** data/raw/vdem_v14.rds
- **Variables used:** v2x_polyarchy, v2x_libdem, v2x_egaldem, COWcode, year
- **Coverage:** 1789-2023 (filtered to 1945-2023 in cleaning)
- **Notes:** Includes non-sovereign entities; filtered in 02_clean_vdem.R

### World Bank WDI
- **Source:** World Bank API via WDI package
- **Downloaded:** 2026-01-15
- **Indicators:** NY.GDP.PCAP.KD, SP.POP.TOTL, SI.POV.GINI
- **File:** data/raw/wdi_2026.rds
- **Coverage:** 1960-2023 (varies by indicator and country)
- **Notes:** Aggregates (World, regions) removed in cleaning
```

---

## Section 7: Common Pitfalls Checklist

These are the errors that appear most frequently in published replication packages. Check for all of them.

### Merge Errors

- [ ] Country codes assumed to be identical across datasets (COW ≠ GW ≠ ISO)
- [ ] Merging by country NAME instead of code (name spelling varies across datasets)
- [ ] Not handling state transitions (USSR/Russia, Yugoslavia/Serbia)
- [ ] Row count explosion after merge (duplicate keys not caught)
- [ ] Using `inner_join` without reporting dropped observations
- [ ] Merging full V-Dem dataset instead of selecting variables first

### Coding Errors

- [ ] Polity special codes (-66, -77, -88) not recoded
- [ ] Freedom House scale change (pre/post-2003) not addressed
- [ ] WDI aggregate rows (World, regions) included in analysis
- [ ] IMF forecast data included alongside actual data
- [ ] ACLED and UCDP event counts combined as if comparable
- [ ] Zero-event country-years treated as missing instead of zeros

### Temporal Errors

- [ ] Survey wave number treated as year (Afrobarometer R7 ≠ year 7)
- [ ] Different time frequencies merged without explicit aggregation
- [ ] Lagged variables computed across state transitions (lagging USSR data into Russia)
- [ ] Panel not balanced and this is not acknowledged

### Documentation Errors

- [ ] Raw data not included or access instructions missing
- [ ] Cleaning decisions not documented (which recoding? why?)
- [ ] Merge diagnostics not reported (match rate, unmatched cases)
- [ ] Missing data patterns not reported
- [ ] Data download date/version not recorded

---

## Section 8: R Package Reference

### Must-Have Packages for Polisci Data Work

| Package | Purpose | Key Function |
|---|---|---|
| `countrycode` | Convert between 40+ country coding schemes | `countrycode()`, `codelist_panel` |
| `WDI` | Download World Bank data | `WDI()` with `extra = TRUE` |
| `vdemdata` | Access V-Dem dataset | `vdem` (the full dataset) |
| `democracyData` | Download Polity, FH, WGI + auto-standardize | `download_polity5()`, `download_fh()` |
| `peacesciencer` | Build COW dyad-year/country-year panels | `create_dyadyears()`, `create_stateyears()` |
| `states` | State system membership panels | `cowstates`, `gwstates` |
| `retroharmonize` | Survey harmonization across waves | Variable/label standardization |
| `haven` | Read Stata/SPSS/SAS files | `read_dta()`, `read_sav()` |
| `readxl` | Read Excel files | `read_excel()` |

### Useful but Situational

| Package | Purpose | When to Use |
|---|---|---|
| `psData` | Download polisci datasets with duplicate handling | When `countrycode` needs extra ID help |
| `pwt10` | Penn World Table 10 | Historical GDP/productivity analysis |
| `Amelia` | Multiple imputation for panel data | When missingness is non-trivial and MAR |
| `naniar` | Missing data visualization | During data exploration |
| `pointblank` | Data validation pipelines | For automated data quality checks |
| `janitor` | Data cleaning utilities | `clean_names()`, `tabyl()`, `remove_empty_cols()` |

---

## Integration Points

| Component | Connection |
|---|---|
| **`r-code-conventions.md`** | Script structure, header format, console output rules |
| **`replication-protocol.md`** | Phase 1-2 data preparation before analysis |
| **`manuscript-conventions.md`** | Section 8 replication package structure |
| **`/prep-data`** | Skill that orchestrates data processing following these conventions |
| **`polisci-data-engineer`** | Agent that reviews data processing code against these conventions |
| **`/reviewer-2`** | Lens 2 (Data & Measurement) checks data quality |
| **`r-reviewer` agent** | Reviews R code quality (this rule adds data-specific checks) |
| **`/submission-checklist`** | Section G checks replication package against these standards |
