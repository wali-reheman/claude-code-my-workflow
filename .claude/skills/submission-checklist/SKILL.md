---
name: submission-checklist
description: Final pre-submission gate for journal manuscripts. Checks completeness, formatting, anonymization, word count, bibliography, replication package, and journal-specific requirements. Read-only — produces a checklist report, never edits files.
argument-hint: "[paper folder, e.g., 'Manuscripts/my_paper'] [--journal APSR]"
---

# /submission-checklist — Pre-Submission Quality Gate

The final check before submitting a manuscript to a journal. Produces a comprehensive pass/fail checklist covering every requirement from `manuscript-conventions.md`.

**Philosophy:** Desk rejections for formatting errors are entirely preventable. This skill catches them before the editor does.

---

## What This Skill Does

1. **Reads** the manuscript, appendix, bibliography, and replication materials
2. **Checks** every requirement from `manuscript-conventions.md` Sections 1-8
3. **Validates** journal-specific requirements (word count, citation style, formatting)
4. **Verifies** anonymization completeness (for blind review journals)
5. **Cross-references** citations against bibliography
6. **Checks** replication package completeness
7. **Produces** a pass/fail report with specific fix instructions

---

## What This Skill Does NOT Do

- Edit files (read-only — fix issues yourself or with Claude's help after reviewing the report)
- Check research design quality (that's `/reviewer-2`)
- Check writing quality (that's `proofreader` or `humanizer`)
- Submit the paper (that's always your job)

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `[paper folder]` | YES | Path to manuscript folder (e.g., `Manuscripts/my_paper`) |
| `--journal` | NO | Target journal (overrides plan file or auto-detection) |
| `--skip-replication` | NO | Skip replication package checks (e.g., for theory papers) |
| `--skip-anonymization` | NO | Skip anonymization checks (e.g., for single-blind journals) |

---

## Workflow

### Step 1: Inventory Files

Glob the manuscript folder and catalog what exists:

```
Required files:
  [ ] main.tex (or main.qmd)
  [ ] appendix.tex (if applicable)
  [ ] figures/ directory with figure files
  [ ] tables/ directory with table fragments

For submission:
  [ ] main_anonymous.tex (for blind review)
  [ ] submission/ folder
  [ ] cover_letter.tex

For replication:
  [ ] Replication package (local or Dataverse link)
```

### Step 2: Determine Target Journal

1. Check `--journal` flag
2. Check active plan in `quality_reports/plans/`
3. Check manuscript preamble for journal class/template
4. If none found: ask the user

### Step 3: Run Checklist

Execute all checks in order. Each check produces PASS, FAIL, or WARN.

---

## The Checklist

### A. Document Completeness

| # | Check | How | Severity |
|---|---|---|---|
| A1 | All standard sections present | Scan for `\section{Introduction}`, `\section{Conclusion}` etc. | FAIL |
| A2 | Abstract exists and has content | Check `\begin{abstract}` | FAIL |
| A3 | Abstract within word limit | Count words, compare to journal table | FAIL |
| A4 | Keywords present (if journal requires) | Check for `\keywords{}` | WARN |
| A5 | Word count within journal limit | Count main text words, compare to Section 7 table | FAIL |
| A6 | Title page complete (non-anonymous version) | Author, affiliation, contact, acknowledgments | WARN |
| A7 | Data availability statement present | Scan for data availability language | WARN |

### B. Formatting Compliance

| # | Check | How | Severity |
|---|---|---|---|
| B1 | Citation format matches journal | APSA (no comma) vs APA (comma) — check Section 7 | FAIL |
| B2 | All `\cite` commands resolve | Cross-reference against `.bib` file | FAIL |
| B3 | No orphan citations (in bib but not cited) | Compare bib entries to in-text citations | WARN |
| B4 | Table format: booktabs, caption above, notes below | Scan table environments | WARN |
| B5 | Figure format: caption below, sufficient resolution | Check figure inclusions | WARN |
| B6 | Table/figure placement matches journal requirement | Inline vs end-of-document (Section 7) | FAIL |
| B7 | Significance stars defined in table notes | Scan for star definitions | WARN |
| B8 | Standard errors in parentheses (not brackets) | Regex scan of tables | WARN |
| B9 | Equations numbered (those referenced in text) | Check `\ref` against equation labels | WARN |
| B10 | Footnotes are substantive (not citations or results) | Scan footnote content | WARN |
| B11 | Oxford comma used consistently | Spot-check lists | WARN |
| B12 | Methods lowercase (except proper nouns) | Scan for "Difference-in-Differences" etc. | WARN |

### C. Causal Language Audit

| # | Check | How | Severity |
|---|---|---|---|
| C1 | Design type identified | Check design section for identification strategy | WARN |
| C2 | Abstract causal language matches design strength | Compare to hierarchy in Section 3 | FAIL |
| C3 | Results causal language matches design strength | Scan results for "effect," "causes," etc. | FAIL |
| C4 | Conclusion causal language matches design strength | Scan conclusion section | FAIL |
| C5 | "Impact" not used as a verb | Scan for "impacts" as verb | WARN |
| C6 | Hypotheses formatted per method tradition | Check H1/propositions/RQs format | WARN |
| C7 | Every hypothesis has prior theoretical derivation | Check that theory section precedes hypotheses | WARN |

### D. Anonymization (for blind review journals)

| # | Check | How | Severity |
|---|---|---|---|
| D1 | `main_anonymous.tex` exists | File check | FAIL |
| D2 | No author names in anonymous version | Scan for names from title page | FAIL |
| D3 | No institutional references | Scan for university/department names | FAIL |
| D4 | Self-citations handled | Check for identifying self-citations | FAIL |
| D5 | Acknowledgments removed/redacted | Scan for acknowledgments section | FAIL |
| D6 | PDF metadata clean | Check for author in PDF properties | WARN |
| D7 | Filename does not contain author name | Check filename | WARN |
| D8 | Supplementary materials also anonymized | Check appendix for identifying info | FAIL |

### E. Appendix & Supplementary Materials

| # | Check | How | Severity |
|---|---|---|---|
| E1 | Every appendix table/figure cited in main text | Cross-reference | FAIL |
| E2 | Appendix numbering correct (A1, A2... B1, B2...) | Scan labels | WARN |
| E3 | Appendix within page limit (if journal specifies) | Count pages | FAIL |
| E4 | Main results NOT hidden in appendix | Check that Tables 1-2 are in main text | WARN |
| E5 | Each appendix item has context paragraph | Scan for text before tables | WARN |

### F. Bibliography Quality

| # | Check | How | Severity |
|---|---|---|---|
| F1 | All cited works in reference list | Invoke `/validate-bib` logic | FAIL |
| F2 | All reference list entries cited in text | Check for orphans | WARN |
| F3 | Required bib fields present (author, title, year, journal) | Scan bib entries | WARN |
| F4 | No obviously wrong years (>2026, <1800) | Range check | WARN |
| F5 | Author names properly formatted | Scan for common errors | WARN |
| F6 | Reference section titled "References" (not "Bibliography") | Check section heading | WARN |
| F7 | "et al." used correctly (3+ authors, all occurrences) | Spot-check | WARN |

### G. Replication Package (unless `--skip-replication`)

| # | Check | How | Severity |
|---|---|---|---|
| G1 | Replication folder exists with correct structure | Check against Section 8 template | FAIL |
| G2 | README.md present with required fields | Check template compliance | FAIL |
| G3 | Master script (00_master.R) exists | File check | FAIL |
| G4 | All scripts referenced in README exist | Cross-reference | FAIL |
| G5 | Data files present (or access instructions for restricted data) | Check data/ folder | WARN |
| G6 | sessionInfo.txt or renv.lock present | File check | WARN |
| G7 | Output table/figure files match manuscript references | Cross-reference `\input{}` and `\includegraphics{}` | FAIL |
| G8 | Codebook present | Check for codebook.md or similar | WARN |
| G9 | Data availability statement in manuscript matches package | Compare | WARN |

### H. Journal-Specific Requirements

| # | Check | How | Severity |
|---|---|---|---|
| H1 | Specific font requirement met (e.g., PRQ: Times New Roman 12pt) | Check documentclass/font settings | WARN |
| H2 | ORCID included (if required, e.g., IO) | Check author block | WARN |
| H3 | Formal proofs at initial submission (if required, e.g., IO) | Check for proof environments | WARN |
| H4 | Registered Report stage compliance (if applicable) | Check against Section 7 RR requirements | WARN |
| H5 | CPS: figures/tables inline (mandatory) | Check placement | FAIL |
| H6 | CPS: APA style (not APSA) | Check citation format | FAIL |
| H7 | World Politics: triple-blind compliance | Extra anonymization checks | FAIL |

---

## Report Format

```markdown
# Submission Checklist Report: [Paper Title]

**Date:** [YYYY-MM-DD]
**Target journal:** [journal]
**Manuscript:** [path]

## Verdict: [READY / NOT READY]

### Summary
- **PASS:** [N] checks
- **FAIL:** [N] checks (must fix before submission)
- **WARN:** [N] checks (recommended fixes)

---

### FAILURES (Must Fix)

#### [F1] [Check name]
**Status:** FAIL
**Details:** [specific description of what's wrong]
**Fix:** [exact instruction for how to fix]
**Location:** [file:line or section reference]

[Repeat for each FAIL]

---

### WARNINGS (Recommended)

#### [W1] [Check name]
**Status:** WARN
**Details:** [description]
**Fix:** [suggestion]

[Repeat for each WARN]

---

### PASSES

[List of all passing checks — collapsed/brief]

---

### Pre-Submission Actions

1. [ ] Fix all FAIL items above
2. [ ] Review WARN items and fix as appropriate
3. [ ] Compile final PDF from `main_anonymous.tex`
4. [ ] Generate tracked-changes PDF (if R&R): `latexdiff main_v1.tex main.tex > main_diff.tex`
5. [ ] Upload to journal submission system
6. [ ] Upload replication package to Dataverse (if required)
```

### Report Saved To

`quality_reports/[paper_name]_submission_checklist.md`

---

## Integration Points

| Component | Connection |
|---|---|
| **`manuscript-conventions.md`** | Source of all formatting and structural rules |
| **`/draft-section`** | Should be run before this skill — all sections must be drafted |
| **`/paper-outline`** | Provides the plan with journal target and word budget |
| **`/reviewer-2`** | Complementary: checks design quality (this checks formatting) |
| **`/validate-bib`** | Checklist Section F invokes the same citation cross-referencing logic |
| **`proofreader` agent** | Run separately for grammar/typo checking (this skill doesn't check prose quality) |
| **`humanizer`** | Run separately for AI writing pattern detection |
| **Orchestrator** | Can be called as the final step in a paper-writing plan |

---

## Principles

1. **Read-only.** This skill produces a report. It never edits files.
2. **Specific.** Every FAIL and WARN includes the exact location and a specific fix instruction.
3. **Journal-aware.** The same manuscript may pass for one journal and fail for another.
4. **Completeness over speed.** Check everything. A desk rejection costs months.
5. **Binary verdict.** READY means zero FAILs. Any FAIL = NOT READY.
