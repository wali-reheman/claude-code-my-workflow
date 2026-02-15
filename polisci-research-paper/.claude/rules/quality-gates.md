---
paths:
  - "scripts/**/*.R"
  - "Manuscripts/**/*.tex"
  - "Replication/**/*.R"
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

## Manuscripts (.tex files in Manuscripts/)

### Critical (Must Pass for Commit)
| Issue | Deduction |
|-------|-----------|
| XeLaTeX compilation failure | -100 (auto-fail) |
| Undefined citation (`?` in output) | -15 per citation |
| Broken cross-reference (`\ref` to undefined `\label`) | -15 per reference |
| Math error (wrong equation, mismatched notation) | -20 per instance |
| Missing main result (key finding not stated in abstract + body) | -20 |

### Major (Should Pass for PR)
| Issue | Deduction |
|-------|-----------|
| Claim without citation | -5 per claim |
| Inconsistent notation across sections | -5 per occurrence |
| Missing section transition (abrupt topic change) | -3 per instance |
| Abstract missing key element (question, method, finding, or contribution) | -5 per element |
| Table/figure referenced but content doesn't match description | -5 per instance |
| Anonymization failure in blinded version (author name, institution, self-citation) | -10 per instance |

### Minor (Nice-to-Have)
| Issue | Deduction |
|-------|-----------|
| Informal language in formal section | -1 per instance |
| Excessive hedging on own contributions | -1 per instance |
| Paragraph without clear topic sentence | -1 per paragraph |
| Inconsistent citation format (`\citet` vs `\citep` used incorrectly) | -1 per instance |

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
| `/create-paper` | Max 3 review-fix rounds (vs orchestrator default 5) | Manuscripts need deeper per-round fixes; fewer rounds with more thorough attention |

Skills specify overrides in their SKILL.md. The orchestrator respects skill-defined limits when present.
