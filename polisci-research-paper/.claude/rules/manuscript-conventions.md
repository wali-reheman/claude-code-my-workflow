---
paths:
  - "Manuscripts/**"
  - "Replication/**"
---

# Manuscript Conventions for Political Science

**Purpose:** Establish folder structure, writing conventions, formatting standards, and submission requirements for academic manuscripts. This rule is the foundation that all paper-writing skills build on.

**Scope:** This rule covers structure, formatting, and presentation. It does NOT cover:

| Concern | Handled By |
|---|---|
| R code quality | `r-code-conventions.md` |
| Replication verification (matching gold standard numbers) | `replication-protocol.md` |
| Research design and methodology | `methodology-reviewer` agent + `robustness-checklists.md` |
| Math correctness | `domain-reviewer` agent |
| Grammar and typos | `proofreader` agent (extend paths to include `Manuscripts/**`) |
| Quality scoring thresholds | `quality-gates.md` |
| Bibliography cross-referencing | `/validate-bib` skill (extend to scan `Manuscripts/**/*.tex`) |

---

## Section 1: Manuscript Folder Structure

Every paper lives in its own subdirectory under `Manuscripts/`.

```
Manuscripts/
└── paper_short_name/
    ├── main.tex                    # Authoritative source (or main.qmd)
    ├── main_anonymous.tex          # Blinded version for review
    ├── appendix.tex                # Online appendix / supplementary materials
    ├── cover_letter.tex            # Journal cover letter
    ├── response_to_reviewers.tex   # R&R response document (when needed)
    ├── figures/                    # Paper-specific figures (symlinks OK to Figures/)
    ├── tables/                     # Generated tables (.tex fragments from R)
    └── submission/                 # Final submission package
        ├── manuscript.pdf
        ├── appendix.pdf
        ├── cover_letter.pdf
        └── replication_package/    # Or link to Dataverse deposit
            ├── README.md
            ├── data/
            │   ├── raw/
            │   └── processed/
            ├── code/
            │   ├── 00_master.R     # Runs everything in order
            │   ├── 01_clean.R
            │   ├── 02_analysis.R
            │   └── 03_figures_tables.R
            └── output/
                ├── tables/
                └── figures/
```

### Source of Truth Hierarchy

| Content | Source of Truth | Derived From |
|---|---|---|
| Manuscript text | `main.tex` | `main_anonymous.tex` derived by stripping identifiers |
| Tables | R scripts → `.tex` fragments in `tables/` | `\input{}` into `main.tex` |
| Figures | R scripts → PDF/SVG in `figures/` | `\includegraphics{}` in `main.tex` |
| Shared figures (with slides) | `Figures/` directory is canonical | `Manuscripts/paper/figures/` contains symlinks or copies |
| Bibliography | `Bibliography_base.bib` | All `.tex` files reference it |
| Appendix tables | Same R scripts → separate output | `\input{}` into `appendix.tex` |

**Rule:** Modify R scripts to regenerate tables/figures. Never hand-edit `.tex` table fragments directly.

---

## Section 2: Document Structure Convention

### Standard Manuscript Structure

```
1. Title Page
   - Title
   - Authors, affiliations, contact info
   - Abstract (150-200 words — see journal table in Section 7)
   - Keywords (3-5, specific)
   - Word count
   - Acknowledgments
   [Entire title page removed in anonymous version]

2. Introduction (10-15% of word count)

3. Literature Review / Theory (20-25%)

4. Research Design (15-20%)

5. Results (20-25%)

6. Discussion / Conclusion (10-15%)

7. References

8. Tables and Figures
   [Inline or at end — see journal table in Section 7]

9. Online Appendix (separate file: appendix.tex)
```

### Section Content Guidelines

**Introduction** must contain, roughly in this order:
1. The puzzle or question (first paragraph — hook the reader)
2. Why it matters (substantive significance, not "this is understudied")
3. What we do and find (brief preview of design, data, and main result — with direction)
4. What this contributes (1-3 specific contributions to the literature)
5. Roadmap (optional — some journals/reviewers consider this filler; omit if short paper)

**Literature Review / Theory:**
- Frame as building toward YOUR argument, not a survey of everything written
- End with testable implications or hypotheses (see hypothesis formatting below)
- Every cited paper should serve a purpose: establish gap, provide foundation, or present alternative

**Research Design:**
- Data source and access (with data availability statement — see Section 8)
- Variable operationalization (treatment, outcome, covariates)
- Identification strategy with explicit assumptions
- Estimation procedure with equation(s)
- For qualitative: case selection logic, evidence sources, analytic procedure

**Results:**
- Main findings first (Table 1-2 / Figure 1-2)
- Brief robustness summary (full tables in appendix — see Section 5)
- Heterogeneity analysis (if applicable)
- Mechanism evidence (if applicable)
- Do NOT put core results in the appendix — reviewers will miss them

**Discussion / Conclusion:**
- Summary of findings (1 paragraph, not a section-by-section recap)
- Limitations (honest, specific — not generic "more research is needed")
- Implications (policy and/or theoretical)
- Future research directions (specific, not vague)

### Abstract Convention

Political science abstracts are **unstructured** (no headings). But they should contain these elements in roughly this order:

1. **The puzzle/gap** (1-2 sentences) — what don't we know?
2. **What this paper does** (1 sentence) — "We argue/show/test..."
3. **How** (1-2 sentences) — design and data, briefly
4. **Key finding** (1-2 sentences) — the main result, with direction and magnitude if possible
5. **Why it matters** (1 sentence) — the contribution or implication

**Abstract anti-patterns to avoid:**
- Describes the paper but never states the finding ("We examine..." with no result)
- No methods mention at all
- Restates the conclusion section verbatim
- Exceeds the journal's word limit (check Section 7)
- Begins with "This paper..." (start with the puzzle instead)

### Hypothesis Formatting

Match hypothesis format to methodological tradition:

| Method Tradition | Format | Example |
|---|---|---|
| **Quantitative** | Numbered, displayed, italicized | *H1: Increased media access reduces ethnic voting in diverse districts.* |
| **Qualitative** | "Propositions," "expectations," or "observable implications" — not numbered H's | "We expect that elite cues mediate the relationship between..." |
| **Formal theory** | "Predictions" or "comparative statics" derived from model | *Prediction 1 (from Proposition 2): As c increases, equilibrium...* |
| **Descriptive** | "Research questions" (RQ1, RQ2), not hypotheses | *RQ1: How does the distribution of X vary across...* |

**Rules:**
- Every hypothesis must be derived from the preceding theory section — never present hypotheses without prior theoretical justification
- State direction (positive/negative) when theory makes a directional prediction
- If theory is ambiguous about direction, state so explicitly — don't present a non-directional hypothesis as if it were directional
- Number consecutively (H1, H2, H3) and reference by number in results

### Appendix Numbering Convention

- **Single appendix:** Tables are A1, A2, A3. Figures are A1, A2, A3 (separate numbering sequence from tables).
- **Multiple appendices:** Numbering restarts per appendix. Appendix A: Table A1, A2; Appendix B: Table B1, B2.
- **Appendix naming:** Use capital letters ("Appendix A," "Appendix B"), NOT numbers ("Appendix 1") or combinations ("Appendix A1").
- **Online appendix:** Same numbering conventions apply.
- **Cross-reference:** Every appendix table/figure must be cited at least once in the main text.

---

## Section 3: Writing Conventions

### Register and Style

- **Formal academic register** throughout — no contractions, no colloquialisms
- **First person:**
  - Multi-authored papers: always "we"
  - Single-authored papers: "I" or "we" are both acceptable — **be consistent throughout**
  - NEVER use "the author" or "the present author" — it is the worst of both worlds
- **Active voice** preferred over passive where possible ("We estimate..." not "The model was estimated...")
- **Tense:**
  - Present tense for claims and established facts ("Voters respond to...")
  - Past tense for what was done ("We collected data from...")
  - Present tense for results being presented ("Table 2 shows that...")
- **No bullet points in manuscripts** — flowing prose only (unlike slides)
- **Oxford comma:** YES — APSA style requires it
- **Capitalization:** Lowercase for methods unless at sentence start
  - "difference-in-differences" not "Difference-in-Differences"
  - "regression discontinuity design" not "Regression Discontinuity Design"
  - Exception: proper nouns within method names ("Bayesian," "Nash equilibrium")
- **Hyphenation:**
  - "difference-in-differences" (hyphenated as compound modifier)
  - "event-study plot" (compound modifier before noun)
  - "the results of the event study" (no hyphen when not modifying a noun)
- **Numbers:** Spell out one through nine; use numerals for 10+. Always use numerals with units ("3 percentage points") or in technical contexts ("2SLS," "Table 3").

### Causal Language Hierarchy

**The language in the abstract, results, and conclusion MUST match the strength of the identification strategy.** Overclaiming is the fastest way to a desk rejection or hostile review.

| Design Strength | Acceptable Language | DO NOT Use |
|---|---|---|
| Randomized experiment (field, lab, survey) | "effect," "causal effect," "causes," "increases/decreases" | — |
| Strong quasi-experiment (RDD with sharp cutoff, DID with credible parallel trends) | "effect," "causal estimate," "the treatment increases..." | — |
| IV with defensible exclusion restriction | "effect on compliers," "local average treatment effect" | "general effect," "universal effect" |
| Matching / weighting (selection on observables) | "estimated effect conditional on observables," "association consistent with..." | "causal effect" without explicit hedging about unobservables |
| Observational / correlational | "association," "relationship," "correlation," "is associated with," "predicts" | "effect," "impact," "causes," "leads to" |
| Descriptive | "pattern," "distribution," "varies with," "co-occurs with" | anything implying causation |

**Red flags to check before submission:**
- Abstract says "effect" but design section describes observational data with no identification strategy
- Results use "increases" and "decreases" when the method only supports "is associated with"
- Conclusion makes policy recommendations implying causation when the design only supports correlations
- The word "impact" used as a verb (common in popular writing, not in rigorous academic prose — prefer "affect" for causal claims, "is associated with" for correlational)

**Rule:** If `/reviewer-2` rates the identification strategy as VULNERABLE or below, audit all causal language in the manuscript and downgrade as needed.

### Citation Conventions (APSA Author-Date)

The default citation style for political science. Based on Chicago Manual of Style, Author-Date variant.

**In-text format:**
- `(Author Year)` — NO comma between author and year
- `(Author Year, 123)` — comma only before page numbers
- `Author (Year)` — when author is grammatical subject of the sentence
- Two authors: `(Taylor and Brown 2019)` — "and" not "&"
- Three or more: `(Johnson et al. 2020)` — at ALL occurrences (no first-occurrence full listing)
- Multiple citations: `(Author1 2019; Author2 2020)` — semicolons, chronological order within parentheses
- Same author, multiple years: `(Smith 2018, 2020)`
- Same author, same year: `(Smith 2020a, 2020b)`

**Rules:**
- Never use ibid, op. cit., or similar abbreviations — always repeat the full citation
- Self-citations in anonymous version: replace with `(Author Year)` or `(Redacted for review)` and remove from reference list
- Every in-text citation must have a corresponding reference list entry (and vice versa — `/validate-bib` checks this)
- Section heading for reference list: "References" — NOT "Bibliography" (APSA/Chicago convention)

**Exception — CPS uses APA style:** If submitting to Comparative Political Studies, switch to APA format (Author, Year) with comma, ampersand for multiple authors, etc. See journal table in Section 7.

### Table Conventions

- **Style:** Booktabs (no vertical lines; `\toprule`, `\midrule`, `\bottomrule` only)
- **Caption:** ABOVE the table
- **Notes:** BELOW the table in a `\tablenotes` or `\begin{tablenotes}` environment
- **Significance stars:** Define consistently. Standard: `* p < 0.10, ** p < 0.05, *** p < 0.01`
  - Some journals prefer 0.05 threshold only (no 0.10 stars) — check journal norms
  - Always define stars in a table note, even if "standard"
- **Standard errors:** In parentheses `(0.045)`, NOT brackets `[0.045]`
- **Decimal places:** Be consistent throughout:
  - Coefficients: 2-3 decimal places
  - Standard errors: 2-3 decimal places (match coefficients)
  - P-values: 3 decimal places
  - Percentages: 1 decimal place
  - N (sample size): no decimals, use comma separators for thousands
- **Decimal alignment:** Align decimal points within columns
- **Column headers:** Informative model names, not just "(1) (2) (3)"
  - Good: "(1) Baseline  (2) Controls  (3) IV"
  - Bad: "(1) (2) (3)"
- **Bottom rows:** Always include: N, R-squared (or equivalent fit statistic), fixed effects indicators, clustering level
- **Self-contained:** Table + caption + notes should be interpretable without reading the text

### Figure Conventions

- **Caption:** BELOW the figure
- **Resolution:** 300+ DPI for raster images; PDF or SVG preferred for vector graphics
- **Grayscale readability:** Color is fine but the figure must be interpretable in grayscale (don't rely solely on color to distinguish categories — use shapes, patterns, or labels too)
- **Self-contained:** Figure + caption should convey the main message without reading the text
- **Axis labels:** Full, informative names — not variable codes ("Share of Ethnic Vote (%)" not "pct_eth_vote")
- **Source note:** Required if data is not from the paper's own analysis
- **Dimensions:** For journal submission, typically 6-7 inches wide (single column) or 3-3.5 inches (double column). Check journal specs.
- **File format:** PDF for LaTeX manuscripts; TIFF or EPS sometimes required by publishers for production

### Equation Conventions

- **Numbered:** Number all equations that are referenced in the text
- **Consistent notation:** Must match notation in slides (if slides exist for this paper) and the project's notation registry in the knowledge base
- **Key variables defined on first use** — either inline or in a paragraph immediately following the equation
- **Subscripts/superscripts:** Avoid overloading. If a variable has 4 subscripts, the notation needs simplification.
- **Displayed vs inline:** Key model specifications should be displayed (not inline). Inline math is fine for brief references to variables.

### Footnote Conventions

- **Substantive only** — never use footnotes for citations (those go in-text per APSA style)
- **Keep short** — if more than 3-4 sentences, the content belongs in the main text or appendix
- **Never put results in footnotes** — they will be missed by reviewers and readers
- **Do not use footnotes for robustness checks** — those belong in the appendix with proper tables
- **Acceptable uses:** Clarifying a data coding decision, noting a minor institutional detail, brief acknowledgment of a tangential point

---

## Section 4: Anonymization Protocol

Mechanical checklist for creating `main_anonymous.tex` from `main.tex`:

### Content to Remove

- [ ] Author names, affiliations, contact info from title page
- [ ] Acknowledgments section (or replace with "[Acknowledgments redacted for review]")
- [ ] Funding/grant disclosures
- [ ] Conference presentation history that identifies authors
- [ ] References to author's university/department in text ("at [University]" → "at [redacted]")
- [ ] References to author's previous work when identifying ("As I showed in..." → remove or rephrase)

### Self-Citations

- [ ] Replace identifying self-citations: `\citet{MyPaper2023}` → "(Author Year)" or "(Redacted for review)"
- [ ] Remove self-cited entries from the reference list
- [ ] If a self-citation is essential for the argument and cannot be removed without damaging the paper, keep it in third person: "(Author 2023) finds that..." — but this is risky

### Metadata and Files

- [ ] Check PDF metadata (author field, title, keywords) — strip identifying info
- [ ] Check LaTeX `\author{}`, `\affiliation{}`, `\thanks{}` — remove or comment out
- [ ] Check figure/table source notes for institutional references
- [ ] Check data descriptions for institution-specific data access details
- [ ] Supplementary materials also anonymized
- [ ] Filename does NOT contain author names

### Verify Anonymization

- [ ] Compile `main_anonymous.tex` and search the PDF for author surnames
- [ ] Search for university/institution names
- [ ] Search for grant numbers or funding agency names
- [ ] Read the paper as a stranger — could you guess the author from the content?

---

## Section 5: Appendix & Supplementary Materials Convention

### What Goes Where

| Content | Main Text | Appendix |
|---|---|---|
| Primary specifications / main results (2-3 tables) | YES | NO — never hide core results |
| Robustness checks | Brief summary sentence per check | Full tables |
| Alternative specifications | Reference in text | Full tables |
| Balance tables (matching, experiments) | Summarize in text | Full table |
| Data construction details | Brief in design section | Full documentation |
| Extended model results | NO | YES |
| Proofs (formal theory) | Key results only | Full proofs |
| Variable definitions / codebook | NO | YES |
| Additional figures (mechanism, heterogeneity) | 1-2 key figures | Remaining figures |
| Pre-analysis plan deviations | Mention in text | Full list |
| Survey instruments / stimuli | NO | YES |

### Structure of appendix.tex

```latex
\appendix

% Appendix A: Robustness Checks
\section{Robustness Checks}
% Tables A1, A2, A3...
% Brief context paragraph before each table explaining what it tests

% Appendix B: Data Construction
\section{Data Construction}
% Detailed variable definitions, coding decisions, sources

% Appendix C: Additional Results
\section{Additional Results}
% Heterogeneity, mechanisms, alternative specifications
```

### Rules

- **Every appendix item must be cited** at least once in the main text ("See Appendix Table A3")
- **Self-contained context:** Each appendix table should have a brief introductory sentence explaining what it tests, so a reader doesn't need to flip back to the main text
- **Length limits:** Check your target journal (JOP caps at 25 pages; others vary). If your appendix exceeds the limit, prioritize the checks that address the most likely reviewer concerns.
- **Own bibliography:** Appendix typically references the main paper's bibliography. If the appendix introduces new citations not in the main text, include them in the main reference list.
- **Numbering:** See Section 2 for appendix numbering conventions (A1, A2... B1, B2...)

---

## Section 6: Response to Reviewers Convention

### When to Create

After receiving a Revise & Resubmit (R&R) decision. Create `response_to_reviewers.tex` in the paper's manuscript folder.

### Structure

```latex
\section*{Summary of Revisions}

% 1 paragraph: what changed at a high level, acknowledge reviewer contributions

\section*{Editor Comments}

\begin{quote}
[Verbatim quote of editor's comment 1]
\end{quote}

\textbf{Response:} [Your response. Reference exact page/line/section for each change.]
We have revised Section 3.2 (pp. 12-14) to address this concern. Specifically, we now...

% Repeat for each editor comment

\section*{Reviewer 1}

\begin{quote}
[Verbatim quote of Reviewer 1's comment 1]
\end{quote}

\textbf{Response:} [Your response.]

\begin{quote}
[Verbatim quote of Reviewer 1's comment 2]
\end{quote}

\textbf{Response:} [Your response.]

% Repeat for all comments from all reviewers

\section*{Reviewer 2}

% Same format
```

### Rules

1. **Quote verbatim.** Never paraphrase or shorten reviewer comments. Copy them exactly as written.
2. **Address every comment.** Even if the response is "We respectfully disagree because..." — no comment should be ignored.
3. **Reference exact locations.** For every change, state where it appears: "See revised Section 4.1, paragraph 3 (p. 15)" or "See new Table A4 in the Appendix."
4. **If you disagree:** Explain why with evidence, data, or citations. Never dismiss ("The reviewer is mistaken"). Frame as: "We appreciate this concern. We have considered this carefully and believe the current approach is preferable because..."
5. **If you cannot make a requested change:** Explain the constraint honestly ("The data does not allow us to test this directly, but we have added a discussion of this limitation on p. 22").
6. **Provide two manuscript versions:**
   - Clean final version (the revised `main.tex` compiled to PDF)
   - Tracked-changes version (use `latexdiff` to generate: `latexdiff main_old.tex main.tex > main_diff.tex`)
7. **Organize by reviewer.** Do not reorganize comments thematically — keep the original reviewer numbering so editors can cross-reference easily.
8. **Be concise but thorough.** Long-winded responses signal defensiveness. Short, specific, evidence-backed responses signal confidence.

### latexdiff Workflow

```bash
# Generate tracked-changes version for resubmission
# Requires latexdiff installed (texlive-extra-utils)
latexdiff Manuscripts/paper/main_v1.tex Manuscripts/paper/main.tex > Manuscripts/paper/main_diff.tex
cd Manuscripts/paper && xelatex main_diff.tex
```

---

## Section 7: Journal Requirements Quick Reference

Check this table when targeting a specific journal. Word limits and policies are as of 2026 — verify against current journal website before submission.

### Word Limits and Counting

| Journal | Article Limit | Note Limit | Count INCLUDES | Count EXCLUDES |
|---|---|---|---|---|
| **APSR** | 11,000 | 7,000 | Main text | Refs, appendix |
| **AJPS** | 10,000 | 4,000 | Text, footnotes, in-text refs, table/fig headers, print appendix | Title page, abstract, ref list, online SI, math notation |
| **JOP** | ~10,000 | — | Main text | — |
| **PSRM** | 9,000 | — | Text, tables, figs, footnotes, refs, appendix | Online SI only |
| **PRQ** | 10,000 | — | Text, tables, citations, footnotes, refs | — |
| **World Politics** | 12,500 | — | Notes, refs | Tables, figures, appendix |
| **CPS** | 12,000 | — | Abstract, notes, refs, tables, figs | — |
| **IO** | 14,000 | 8,000 (notes), 10,000 (essays) | Tables, figures, notes | Bibliography |

### Review Type and Citation Style

| Journal | Review Type | Citation Style | Figs/Tables Placement |
|---|---|---|---|
| **APSR** | Double-blind | APSA author-date | In text |
| **AJPS** | Double-blind | APSA author-date | In text |
| **JOP** | Double-blind | Chicago author-date | In text |
| **PSRM** | Single-blind (default; double-blind optional) | Author-date | In text |
| **PRQ** | Double-blind | Author-date (converted to PRQ style if accepted) | End of document |
| **World Politics** | **Triple-blind** | House style (request from publisher) | In text |
| **CPS** | Partial triple-blind | **APA** (not APSA) | **In text (mandatory)** |
| **IO** | Standard | Author-date | In text |

### Replication Policies

| Journal | Policy | Repository | Verification |
|---|---|---|---|
| **APSR** | Required | Various | Author responsibility |
| **AJPS** | **Mandatory, verified BEFORE publication** | AJPS Dataverse (Harvard) | **Odum Institute verifies** |
| **JOP** | Mandatory, acceptance conditional | JOP Dataverse (Harvard) | Journal staff |
| **PSRM** | Mandatory, acceptance conditional | PSRM Dataverse (Harvard) | PSRM staff assess |
| **PRQ** | Expected, data availability statement required | Public repository (author's choice) | — |
| **World Politics** | Not specified | — | — |
| **CPS** | Mandatory, acceptance conditional | CPS Dataverse (Harvard) | Journal staff |
| **IO** | Mandatory (data + code + formal proofs) | Not specified | — |

### Special Requirements

| Journal | Notable Requirement |
|---|---|
| **APSR** | Accepts Registered Reports |
| **AJPS** | Odum Institute verification before publication; 4,000-word research notes (methods/meta-analysis only) |
| **JOP** | 25-page max online appendix; accepts Registered Reports |
| **PSRM** | 120-word max abstract; optional anonymous review; authors may recommend reviewers |
| **PRQ** | Times New Roman 12pt required; no submission fees |
| **World Politics** | No policy pieces or journalistic narratives; triple-blind (most stringent anonymization) |
| **CPS** | Uses APA style (not APSA); figures/tables MUST be inline (not at end) |
| **IO** | ORCID required; formal model proofs required at initial submission; 20-page max SI |

### Registered Reports

Some journals now accept Registered Reports (results-agnostic review):

| Journal | Accepts RRs |
|---|---|
| APSR | Yes |
| JOP | Yes |
| JEPS (Journal of Experimental Political Science) | Yes |
| Research & Politics | Yes |

**Stage 1:** Introduction + hypotheses + detailed methods + analysis plan. Reviewed BEFORE data collection. Decision is results-agnostic.

**Stage 2:** Full paper with results. Reviewed after data collection. Evaluated on adherence to Stage 1 plan (deviations must be justified).

**Timeline:** Typically 6 months between Stage 1 acceptance and Stage 2 submission.

---

## Section 8: Replication Package Standards

What a submission-ready replication package must contain, synthesized from journal requirements, DA-RT, and TOP Guidelines.

### Folder Structure

```
replication_package/
├── README.md              # REQUIRED — see template below
├── data/
│   ├── raw/               # Original data files (or access instructions if restricted)
│   ├── processed/         # Cleaned data used in analysis
│   └── codebook.md        # Variable definitions, coding decisions, sources
├── code/
│   ├── 00_master.R        # Runs everything in sequence
│   ├── 01_clean_data.R    # Data cleaning and preparation
│   ├── 02_analysis.R      # Main analysis (produces main text tables)
│   ├── 03_robustness.R    # Robustness checks (produces appendix tables)
│   ├── 04_figures.R       # All figures (main + appendix)
│   └── sessionInfo.txt    # R session info (or renv.lock for reproducibility)
├── output/
│   ├── tables/            # Generated .tex table fragments
│   ├── figures/           # Generated figure files (PDF/SVG)
│   └── log/               # Execution logs proving successful run
└── LICENSE                # Data license if applicable
```

### README Template

```markdown
# Replication Package: [Paper Title]

**Authors:** [Names]
**Journal:** [Target journal]
**Date:** [YYYY-MM-DD]

## Software Requirements

- R version: [e.g., 4.3.2]
- Key packages (with versions):
  - fixest (0.11.1)
  - ggplot2 (3.4.4)
  - [list all non-base packages used]

## Data Sources

| Dataset | Source | Access | File |
|---------|--------|--------|------|
| [Name] | [URL or institution] | Public / Restricted / Proprietary | `data/raw/filename.csv` |

[For restricted data: describe access procedure, contact information, licensing]

## Instructions

1. Set working directory to this folder
2. Run `code/00_master.R` — this executes all scripts in order
3. Expected runtime: [estimate]
4. All output will appear in `output/tables/` and `output/figures/`

## Output Files

| Script | Produces | Corresponds To |
|--------|----------|----------------|
| `02_analysis.R` | `output/tables/table1.tex` | Table 1 in manuscript |
| `02_analysis.R` | `output/tables/table2.tex` | Table 2 in manuscript |
| `04_figures.R` | `output/figures/figure1.pdf` | Figure 1 in manuscript |
| `03_robustness.R` | `output/tables/tableA1.tex` | Table A1 in appendix |

## Contact

[Corresponding author email for questions about replication]
```

### Data Availability Statement Templates

Include one of these in the manuscript (typically as a footnote to the first page or in the research design section):

**Public data:**
> "Replication data and code are available at [Dataverse DOI/URL]."

**Restricted data with public code:**
> "The data used in this study are available from [source] under [license/agreement]. Restrictions apply to the availability of these data. Code to reproduce all analyses is available at [URL]."

**Proprietary data:**
> "The data were obtained under a data use agreement with [institution] that does not permit public redistribution. The authors will provide guidance on obtaining access upon request. Replication code is available at [URL]."

**Mixed sources:**
> "Survey data are available at [URL]. Administrative records are available from [agency] under [data use agreement]. Code to reproduce all analyses is available at [URL]."

**No data (formal theory or conceptual):**
> "This article does not use empirical data. Formal proofs are provided in the appendix."

---

## Integration Points

| Component | Connection |
|---|---|
| **`/reviewer-2`** | Lens 3 (Transparency) checks replication package against Section 8 standards |
| **`proofreader` agent** | Should extend `paths:` to include `Manuscripts/**` for manuscript proofreading |
| **`domain-reviewer` agent** | Should extend scope to review manuscripts (not just slides) |
| **`/validate-bib`** | Should scan `Manuscripts/**/*.tex` in addition to `Slides/*.tex` |
| **`quality-gates.md`** | Future: add manuscript-specific rubric (abstract, section flow, references) |
| **`single-source-of-truth.md`** | Section 1 defines where manuscripts sit in the source hierarchy |
| **`replication-protocol.md`** | Section 8 complements with submission-ready package structure |
| **`robustness-checklists.md`** | Section 5 defines how robustness checks are PRESENTED (main vs appendix) |
| **`/draft-section`** | Enforces these conventions during section drafting |
| **`/paper-outline`** | Creates manuscript skeleton following Section 1 structure and Section 7 journal limits |
| **`/submission-checklist`** | Checks against Sections 4, 5, 7, and 8 before journal submission |
| **`/create-paper`** | End-to-end orchestrator chaining outline → draft → review → submission |
| **`/prep-data`** | Data processing skill; produces replication-ready data following Section 8 structure |
| **`panel-data-conventions.md`** | Dataset-specific cleaning protocols, merge standards, identifier systems |
| **`polisci-data-engineer` agent** | Reviews data processing code against panel data conventions |
