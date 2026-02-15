# Replication Package

**Paper:** [Your Paper Title]
**Authors:** [Your Name(s)]
**Date:** [YYYY-MM-DD]

---

## Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| R | ≥ 4.3.0 | All analysis |
| [Package 1] | ≥ X.Y | [What it does] |
| [Package 2] | ≥ X.Y | [What it does] |

## Data Sources

| Dataset | Source | Download Date | Version | File |
|---------|--------|---------------|---------|------|
| [e.g., V-Dem] | [URL] | [YYYY-MM-DD] | [v14] | `data/raw/vdem.csv` |
| [e.g., WDI] | [URL] | [YYYY-MM-DD] | [latest] | `data/raw/wdi.csv` |

## Instructions

Run all scripts from the repository root:

```bash
# Option 1: Run master script (executes all in order)
Rscript Replication/code/00_master.R

# Option 2: Run individually
Rscript Replication/code/01_download.R       # Fetch raw data
Rscript Replication/code/02_clean_[name].R   # Clean each dataset
Rscript Replication/code/03_merge.R          # Merge panels
Rscript Replication/code/04_construct.R      # Create analysis variables
Rscript Replication/code/05_analysis.R       # Run estimations
Rscript Replication/code/06_figures.R        # Generate tables/figures
```

## Directory Structure

```
Replication/
├── README.md          # This file
├── code/
│   ├── 00_master.R    # Runs all scripts in order
│   ├── 01_download.R  # Fetch raw data
│   ├── 02_clean_*.R   # One per data source
│   ├── 03_merge.R     # Combine panels with diagnostics
│   ├── 04_construct.R # Create analysis variables
│   ├── 05_analysis.R  # Estimation
│   └── 06_figures.R   # Tables and figures
├── data/
│   ├── raw/           # Downloaded data (never modified)
│   └── processed/     # Cleaned and merged data
└── output/            # Generated tables, figures, logs
```

## Runtime

- Total: ~[X] minutes on [machine description]
- Most time-intensive: [script name] (~[X] min)

## Notes

- All paths are relative to the repository root
- Raw data files are not included due to size/licensing — run `01_download.R` first
- Random seed: set in each script header (YYYYMMDD format)
