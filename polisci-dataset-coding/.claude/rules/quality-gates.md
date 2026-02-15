---
paths:
  - "scripts/**/*.R"
  - "Replication/**/*.R"
  - "Replication/data/**"
---

# Quality Gates & Scoring Rubrics

**Purpose:** Define objective quality thresholds for committing and deploying academic materials.

**Prerequisite:** Scoring assumes verification has passed (see `.claude/rules/verification-protocol.md`). Compilation success is a prerequisite, not a scored item — auto-fail deductions enforce this.

---

## Scoring System

- **80/100 = Commit threshold** — Good enough to save progress
- **90/100 = PR threshold** — High quality ready for deployment
- **95/100 = Excellence** — Aspirational target

---

## R Scripts (.R files)

### Critical
| Issue | Deduction |
|-------|-----------|
| Syntax errors | -100 (auto-fail) |
| Known domain-specific bugs | -30 |
| Hardcoded absolute paths | -20 |

### Major
| Issue | Deduction |
|-------|-----------|
| Missing set.seed() | -10 |
| Missing figure generation | -5 per figure |
| Wrong color palette | -3 per figure |

---

## Data Processing Scripts (.R files in Replication/)

### Critical (Must Pass for Commit)
| Issue | Deduction |
|-------|-----------|
| Script fails to run | -100 (auto-fail) |
| Merge without pre-merge duplicate check | -20 per merge |
| Polity special codes (-66, -77, -88) not recoded | -20 |
| Merging by country name instead of country code | -20 per merge |
| WDI aggregate rows (World, regions) included | -15 |

### Major (Should Pass for PR)
| Issue | Deduction |
|-------|-----------|
| Missing post-merge diagnostics (match rate, N) | -5 per merge |
| Missing `custom_match` for known ambiguous country codes | -5 per case |
| No codebook or data documentation | -10 |
| Event data: missing country-years coded as NA instead of zero | -5 |
| Inner join without reporting dropped observations | -5 per join |

### Minor (Nice-to-Have)
| Issue | Deduction |
|-------|-----------|
| Missing script header (purpose, inputs, outputs) | -1 per script |
| Inconsistent variable naming across scripts | -1 per inconsistency |
| Missing `sessionInfo()` or `renv.lock` | -2 |

---

## Replication Packages (Replication/ directory)

### Critical (Must Pass for Commit)
| Issue | Deduction |
|-------|-----------|
| `00_master.R` or run order missing | -20 |
| Script fails to run in numbered order | -100 (auto-fail) |
| Raw data modified in place (no raw/processed separation) | -20 |
| No README documenting software versions and run order | -15 |

### Major (Should Pass for PR)
| Issue | Deduction |
|-------|-----------|
| Missing codebook or data documentation | -10 |
| Numbered script gap (e.g., 01, 03 — missing 02) | -5 |
| No `sessionInfo()` or `renv.lock` for reproducibility | -5 |
| Output directory empty after running scripts | -5 |
| Download script lacks date stamp or version info | -3 |

### Minor (Nice-to-Have)
| Issue | Deduction |
|-------|-----------|
| README missing estimated runtime | -1 |
| No disk space or memory requirements noted | -1 |
| Output files not clearly named to match tables/figures in paper | -1 per file |

---

## AI-Coded Datasets (Replication/data/coded/)

### Critical (Must Pass for Commit)
| Issue | Deduction |
|-------|-----------|
| Calibration ICC < 0.75 (Track A) or < 3/5 proxy correlations (Track B) | -100 (auto-fail) |
| No gold-standard validation AND no documented opt-out justification | -100 (auto-fail) |
| Gold-standard validation opted out (with documented justification) | -15 |
| Hallucination verification rate < 70% | -100 (auto-fail) |
| No calibration performed | -30 |
| No behavioral pre-testing performed | -25 |
| No temporal boundary enforcement in prompt templates | -25 |
| No evidence citations for coded cells | -20 |
| No majority voting AND no sentinel monitoring (neither quality control) | -20 |

### Major (Should Pass for PR)
| Issue | Deduction |
|-------|-----------|
| Gold-standard validation ICC < 0.60 | -15 |
| Gold-standard set < 200 cells | -10 |
| Gold-standard not coded blind (expert saw AI scores) | -10 |
| No majority voting (single-run without documented justification) | -10 |
| Majority vote 0/3 cells unresolved | -10 |
| Hallucination verification rate 70-79% | -10 |
| Missing methodology transparency report (or < 10 sections) | -10 |
| No memorization check | -10 |
| No sentinel drift monitoring in production | -10 |
| Sentinel drift red alert without documented response | -10 |
| Bridge case deviation > 1 point across batches | -10 |
| No prompt variant testing in pilot | -8 |
| No inclusion/exclusion criteria in codebook | -8 |
| No downstream bias correction guidance in documentation | -5 |
| Word "expert" used to describe Claude's coding | -5 |

### Minor (Nice-to-Have)
| Issue | Deduction |
|-------|-----------|
| No prompt sensitivity test (--extended) | -5 |
| No adversarial stability test (--extended) | -5 |
| No construct validity check (--extended) | -5 |
| Majority vote 3/3 agreement rate < 70% (suggests codebook ambiguity) | -5 |
| UNABLE_TO_CODE rate not reported by region | -3 |
| Confidence criteria not explicit in codebook | -3 |
| < 3 anchor examples per scale point | -2 |
| Label semantics or scale direction pre-test not performed | -2 |

---

## Quality Gate Enforcement

### Commit Gate (score < 80)
Block commit. List blocking issues with required actions.

### PR Gate (score < 90)
Allow commit but warn. List issues with recommendations to reach PR quality.

### User can override with justification when needed.

### Skill-Specific Thresholds

Some skills define their own thresholds that override the defaults above:

| Skill | Override | Rationale |
|-------|----------|-----------|
| `/create-dataset` | Max 3 review-fix rounds | Datasets need focused per-round attention on reliability metrics |

Skills specify overrides in their SKILL.md. The orchestrator respects skill-defined limits when present.
