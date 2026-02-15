---
paths:
  - "Replication/**/*.R"
  - "Replication/data/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

**After verification passes**, quality scoring applies (see `.claude/rules/quality-gates.md`). Verification checks whether outputs work; quality gates check whether they're good enough.

---

## For Data Processing Scripts (.R in Replication/):
1. Run scripts in numbered order: `Rscript Replication/code/01_download.R` etc.
2. Verify output datasets were created with non-zero size
3. Check that merge diagnostics were printed (grep output for match rates)
4. Verify final panel dimensions: expected N countries × T years
5. Spot-check: are there observations from aggregate entities (World, regions)?

## For R Scripts (Analysis):
1. Run `Rscript scripts/R/filename.R`
2. Verify output files (PDF, RDS) were created with non-zero size
3. Spot-check estimates for reasonable magnitude

---

## Common Pitfalls:
- **Assuming success**: Always verify output files exist AND contain correct content
- **Merge without diagnostics**: Always check match rates and unmatched cases after every join
- **Zero vs NA confusion**: Event data missing country-years should be zero, not NA

## For Script Dependencies:
1. Before running R scripts, verify required packages are available:
   ```bash
   Rscript -e 'packages <- c("tidyverse", "fixest"); missing <- packages[!packages %in% installed.packages()[,"Package"]]; if(length(missing)) cat("Missing:", paste(missing, collapse=", "))'
   ```
2. Adapt the package list from the script's `library()` calls
3. Warn if packages are missing — do not auto-install without user confirmation

## For Cross-File References:
1. Verify all `.rds` and `.csv` files loaded in R scripts exist (or will be created by earlier scripts)
2. Verify coding output CSVs match expected schema (country, year, variable columns)

## For Replication Package Completeness:
1. Verify `Replication/README.md` exists and lists all scripts
2. Verify numbered scripts exist in order (no gaps: 01, 02, 03, not 01, 03)
3. Verify `data/raw/` has data files or `01_download.R` creates them
4. Verify `data/processed/` is populated after running scripts
5. Run `00_master.R` if it exists and verify it completes without error

---

## Verification Checklist:
```
[ ] Output file created successfully
[ ] No script execution errors
[ ] Merge diagnostics present — data processing
[ ] Script dependencies available — R scripts
[ ] Cross-file references resolve — data files and scripts
[ ] Replication package complete — if data scripts modified
[ ] Coding output CSVs match expected schema
[ ] Calibration metrics computed and reported
[ ] Reported results to user
```
