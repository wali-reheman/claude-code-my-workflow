---
paths:
  - "Slides/**/*.tex"
  - "Quarto/**/*.qmd"
  - "Manuscripts/**/*.tex"
  - "Replication/**/*.R"
  - "docs/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

**After verification passes**, quality scoring applies (see `.claude/rules/quality-gates.md`). Verification checks whether outputs work; quality gates check whether they're good enough.

---

## For Quarto/HTML Slides:
1. Run `./scripts/sync_to_docs.sh` (or `./scripts/sync_to_docs.sh LectureN`) to render and deploy
2. Open the HTML in browser: `open docs/slides/LectureX.html`
3. Verify images display by reading 2-3 image files to confirm valid content
4. Check HTML source for correct image paths
5. Check for overflow by scanning dense slides
6. Verify environment parity: every Beamer box environment has a CSS equivalent in the QMD
7. Report verification results

## For LaTeX/Beamer Slides:
1. Compile with xelatex and check for errors
2. Open the PDF to verify figures render
3. Check for overfull hbox warnings

## For Manuscripts (.tex in Manuscripts/):
1. Compile with xelatex (3-pass with bibtex):
   ```bash
   cd Manuscripts/paper_name
   TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
   BIBINPUTS=../..:$BIBINPUTS bibtex main
   TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
   TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
   ```
2. Check for errors: grep log for `! ` (LaTeX errors) and `Warning` (especially undefined references)
3. Verify no undefined citations: grep log for `Citation .* undefined`
4. Verify no broken cross-references: grep log for `Reference .* undefined`
5. Check word count is within target (if specified): `texcount -inc main.tex`
6. If blinded version exists (`main_anonymous.tex`):
   - Compile it separately
   - Grep the PDF text for author names, institution names, and self-citations
   - Any match = anonymization failure
7. Verify all `\input{}` files exist (tables, figures)
8. Report verification results

## For Data Processing Scripts (.R in Replication/):
1. Run scripts in numbered order: `Rscript Replication/code/01_download.R` etc.
2. Verify output datasets were created with non-zero size
3. Check that merge diagnostics were printed (grep output for match rates)
4. Verify final panel dimensions: expected N countries × T years
5. Spot-check: are there observations from aggregate entities (World, regions)?

## For TikZ Diagrams in HTML/Quarto:
1. Browsers **cannot** display PDF images inline — ALWAYS convert to SVG
2. Use SVG (vector format) for crisp rendering: `pdf2svg input.pdf output.svg`
3. **NEVER use PNG for diagrams** — PNG is raster and looks blurry
4. Verify SVG files contain valid XML/SVG markup
5. Copy SVGs to `docs/Figures/LectureX/` via `sync_to_docs.sh`
6. **Freshness check:** Before using any TikZ SVG, verify extract_tikz.tex matches current Beamer source

## For R Scripts (Analysis):
1. Run `Rscript scripts/R/filename.R`
2. Verify output files (PDF, RDS) were created with non-zero size
3. Spot-check estimates for reasonable magnitude

---

## Common Pitfalls:
- **PDF images in HTML**: Browsers don't render PDFs inline → convert to SVG
- **Relative paths**: `../Figures/` works from `Quarto/` but not from `docs/slides/` → use `sync_to_docs.sh`
- **Assuming success**: Always verify output files exist AND contain correct content
- **Stale TikZ SVGs**: extract_tikz.tex diverges from Beamer source → always diff-check
- **Manuscript TEXINPUTS**: Manuscripts are nested deeper — adjust `../../Preambles` path accordingly
- **Anonymization false sense of security**: grep the PDF *text*, not just the .tex source — macros can expand to reveal names

## For Manuscript PDF Metadata (Anonymization):
1. After compiling blinded version, check PDF metadata:
   ```bash
   pdfinfo main_anonymous.pdf | grep -i "author\|creator\|producer\|title"
   ```
2. Author field should NOT contain actual author names
3. If metadata leaks identity: add `\hypersetup{pdfauthor={}, pdfcreator={}}` to preamble
4. Check PDF bookmarks don't contain identifying information

## For Script Dependencies:
1. Before running R scripts, verify required packages are available:
   ```bash
   Rscript -e 'packages <- c("tidyverse", "fixest"); missing <- packages[!packages %in% installed.packages()[,"Package"]]; if(length(missing)) cat("Missing:", paste(missing, collapse=", "))'
   ```
2. Adapt the package list from the script's `library()` calls
3. Warn if packages are missing — do not auto-install without user confirmation

## For Cross-File References:
1. Verify all `\input{}` and `\include{}` targets exist in manuscripts
2. Verify all figure files referenced in `.tex` or `.qmd` exist on disk
3. Verify all `.rds` files loaded in R scripts exist (or will be created by earlier scripts)

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
[ ] No compilation/render errors
[ ] Images/figures display correctly
[ ] Paths resolve in deployment location (docs/) — slides only
[ ] Cross-references and citations all resolve — manuscripts
[ ] Anonymization verified (source AND PDF metadata) — blinded manuscripts
[ ] Merge diagnostics present — data processing
[ ] Script dependencies available — R scripts
[ ] Cross-file references resolve — manuscripts and slides
[ ] Replication package complete — if data scripts modified
[ ] Opened in browser/viewer to confirm visual appearance
[ ] Reported results to user
```
