---
paths:
  - "scripts/**/*.R"
  - "Replication/**/*.R"
---

# R Code Standards

**Standard:** Senior Principal Data Engineer + PhD researcher quality

These standards apply to all R scripts in this repository.

---

## 0. NO MASS-PRODUCTION OF R SCRIPTS (MANDATORY)

**Claude MUST give each R script individual, focused attention. Templated mass-production of R scripts is FORBIDDEN.**

The problem: When asked to create multiple R scripts (e.g., a numbered pipeline `01_`–`04_`, or several figure scripts), Claude's natural instinct is to write one script carefully, then copy-paste its structure across the rest with superficial modifications. This produces scripts that *look* complete but contain shallow analytical decisions — wrong variable selections, naive merge keys, misapplied transformations, untested assumptions — because Claude was pattern-matching instead of thinking.

### The Rule

**Write each R script as if it were the only one.** Before writing any `.R` file, stop and think about what *this specific script* needs to do:

- What data does *this* script actually receive as input? (Not what the plan says — what does the previous step *actually* produce?)
- What are the analytical decisions specific to *this* step? (Variable selection, merge keys, filtering criteria, transformations)
- What can go wrong *here*? (Missing values, unexpected duplicates, type mismatches, encoding issues)
- What diagnostics should *this* script report? (Not generic diagnostics copy-pasted from the last script)

### What This Forbids

| Forbidden Pattern | Why It's Bad |
|-------------------|-------------|
| Writing a "template" script then adapting it 4 times | Each script has different analytical logic — templates obscure this |
| Copy-pasting diagnostic blocks across scripts | Diagnostics should target each script's specific failure modes |
| Generating all numbered scripts (`01_`–`04_`) in one pass | Later scripts depend on earlier scripts' actual output, not assumed output |
| Using identical error-handling across scripts | Each script has different edge cases |
| Reusing variable selection logic without re-examining the source data | Different datasets have different structures, coding schemes, and quirks |

### What This Allows

- Writing multiple scripts in one session is fine — as long as each gets genuine thought
- Running and testing can happen after all scripts are written if the user prefers
- Using consistent *style* (headers, section numbering, naming conventions) across scripts is good — that's convention, not mass-production
- Referencing a previous script's approach while writing a new one is fine — as long as you adapt rather than copy

### How Claude Should Work

1. **Read the input data** (or the previous script's output specification) before writing
2. **Think through the specific logic** this script needs — don't assume it mirrors another script
3. **Write the script** with decisions tailored to its specific task
4. **Move to the next script** — and repeat the thinking step fresh, not just the writing step

---

## 1. Script Structure

Every script MUST follow this section layout:

```r
# ==============================================================================
# [Paper]: [Script Purpose]
# ==============================================================================
#
# Author:   [Your Name]
# Source:   [Paper(s) replicated / adapted from]
#
# Purpose:
#   [2-4 sentence description]
#
# Inputs:
#   - [data source or URL]
#
# Outputs (saved to Replication/output/):
#   - [file.pdf]  -- [description]
#   - [file.rds]  -- [description]
#
# Runtime: ~X min
# ==============================================================================
```

Numbered sections: 0. Setup, 1. Data/DGP, 2. Estimation, 3. Run, 4. Figures, 5. Export

## 2. Console Output Policy

**Scripts are NOT notebooks.**

- **Allowed:** `message()` for progress milestones only
- **Forbidden:** `cat()`, `print()`, ASCII banners, per-iteration output

## 3. Reproducibility

- `set.seed()` called ONCE at top (YYYYMMDD format)
- All packages loaded at top via `library()` (not `require()`)
- All paths relative to repository root
- `dir.create(..., recursive = TRUE)` for output directories

## 4. Function Design

- `snake_case` naming, verb-noun pattern
- Roxygen-style documentation
- Default parameters, no magic numbers
- Named return values (lists or tibbles)

## 5. Domain Correctness

<!-- Customize for your field's known pitfalls -->
- Verify estimator implementations match paper equations
- Check known package bugs (document in Section 12 below)

## 6. Visual Identity

```r
# --- Your institutional palette ---
# Customize these colors for your institution
primary_blue  <- "#012169"
primary_gold  <- "#f2a900"
accent_gray   <- "#525252"
positive_green <- "#15803d"
negative_red  <- "#b91c1c"
```

### Custom Theme
```r
theme_custom <- function(base_size = 14) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title = element_text(face = "bold", color = primary_blue),
      legend.position = "bottom"
    )
}
```

### Figure Dimensions for Manuscripts
```r
ggsave(filepath, width = 8, height = 5)
```

## 7. RDS Data Pattern

**Heavy computations saved as RDS; analysis scripts and tables load pre-computed data.**

```r
saveRDS(result, file.path(out_dir, "descriptive_name.rds"))
```

## 8. Code Quality Checklist

```
[ ] Header with all fields
[ ] Numbered sections
[ ] Packages at top via library()
[ ] set.seed() once at top
[ ] All paths relative
[ ] Functions documented
[ ] No cat/print output
[ ] Figures: explicit dimensions
[ ] RDS: every computed object saved
[ ] Comments explain WHY not WHAT
```

## 9. Common Pitfalls

<!-- Add your field-specific pitfalls here -->
| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Missing explicit dimensions | Inconsistent figure sizing | Always specify width/height in ggsave() |
| `cat()` for status | Noisy stdout | Use message() sparingly |
| Hardcoded paths | Breaks on other machines | Use relative paths |
