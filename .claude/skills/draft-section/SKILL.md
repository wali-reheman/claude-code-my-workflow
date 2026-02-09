---
name: draft-section
description: Draft a manuscript section with citation verification, academic voice audit, word budget enforcement, and version tracking. Chains scientific-writing, citation-management, and humanizer skills. Supports R&R mode with --revise flag.
disable-model-invocation: true
argument-hint: "[section name, e.g., 'introduction' or 'results'] [--revise 'reviewer comment'] [--scaffold] [--full-prose]"
---

# /draft-section — Manuscript Section Drafting

Draft a single section of an academic manuscript with rigorous citation verification, word budget awareness, and polisci-appropriate academic voice.

**Philosophy:** Writing is the researcher's voice. This skill produces clean, verified, convention-compliant prose — or scaffolded outlines that the researcher fills in. The default mode is adaptive: Claude uses its best judgment based on the section type, the user's past preferences, and the complexity of the content.

---

## What This Skill Does

1. **Reads** manuscript conventions, existing sections, and input materials
2. **Drafts** a section following polisci manuscript structure (from `manuscript-conventions.md`)
3. **Verifies every citation** — no hallucinated references leave this skill
4. **Audits voice** — detects and removes AI writing patterns
5. **Enforces word budget** — respects journal limits and section proportions
6. **Tracks versions** — saves previous drafts before overwriting
7. **Supports R&R mode** — targeted revisions responding to specific reviewer comments

---

## What This Skill Does NOT Do

- Write an entire paper at once (use `/paper-outline` first, then `/draft-section` per section)
- Choose your research design or methodology (that's your job)
- Fabricate results or statistical findings (reports numbers from YOUR code/tables only)
- Replace your analytical voice (scaffolding mode available for sensitive sections)
- Check research design quality (that's `/reviewer-2`)

---

## CONSTRAINTS (Non-Negotiable)

1. **Every citation must be verified** — tagged `[UNVERIFIED]` if not confirmed in `Bibliography_base.bib` or via `citation-management` skill
2. **Every numerical claim must be traceable** — tagged `[VERIFY: source]` if not directly from a table/figure in the manuscript
3. **Word budget is binding** — warn if section exceeds its proportion; hard-stop at journal limit
4. **Save before overwrite** — if a section file exists, copy to `_prev` before writing
5. **Never invent results** — only report what exists in R output, tables, or figures
6. **Causal language must match design** — enforce the hierarchy from `manuscript-conventions.md` Section 3

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `[section]` | YES | Section to draft: `abstract`, `introduction`, `literature`, `theory`, `design`, `results`, `discussion`, `conclusion`, `appendix` |
| `--revise "comment"` | NO | R&R mode: revise an existing section in response to a specific reviewer comment |
| `--scaffold` | NO | Force scaffolding mode: produce an outline with `[YOUR ANALYSIS]` markers instead of full prose |
| `--full-prose` | NO | Force full prose mode: write complete flowing text |
| `--journal APSR` | NO | Override target journal (uses plan file or default if not specified) |
| `--file path/to/main.tex` | NO | Specify manuscript file (auto-detects if only one manuscript exists) |

If neither `--scaffold` nor `--full-prose` is given, Claude uses **adaptive mode** (see Step 5).

---

## Workflow

### Step 0: Parse Arguments & Detect Context

1. Parse `$ARGUMENTS` for section name, flags, and options
2. **Locate the manuscript:**
   - If `--file` given: use that file
   - Else: glob `Manuscripts/**/main.tex` and `Manuscripts/**/main.qmd`
   - If multiple manuscripts exist and no `--file`: ask the user which one
   - If no manuscript exists: inform user to run `/paper-outline` first
3. **Detect R&R mode:** if `--revise` flag present, activate R&R workflow (Step 8)
4. **Check for existing plan:** read `quality_reports/plans/` for an active plan that specifies journal, word limits, or section assignments

### Step 1: Read Conventions & Context

Read these files to establish constraints:

1. **`manuscript-conventions.md`** — structure, formatting, causal language hierarchy
2. **The manuscript file** (`main.tex` / `main.qmd`) — read existing sections for voice, notation, argument flow
3. **`Bibliography_base.bib`** — the authoritative citation source
4. **`MEMORY.md`** — check for `[LEARN:writing]`, `[LEARN:citation]`, `[LEARN:style]` entries
5. **R output** (if results/discussion section):
   - Glob `Manuscripts/*/tables/*.tex` for table fragments
   - Glob `Manuscripts/*/figures/*` for figure files
   - Glob `scripts/**/*.R` or `Replication/**/*.R` for analysis scripts
6. **Supporting papers** (if literature/theory section):
   - Check `master_supporting_docs/supporting_papers/` for relevant materials

### Step 2: Establish Word Budget

Calculate the section's word allocation:

1. **Get total limit:**
   - From `--journal` flag → look up in `manuscript-conventions.md` Section 7
   - From active plan file → use specified limit
   - Default: 10,000 words (conservative AJPS limit)

2. **Calculate section proportion:**

   | Section | % of Total | At 10K Total |
   |---|---|---|
   | Abstract | N/A | 150-200 words (journal-specific) |
   | Introduction | 10-15% | 1,000-1,500 |
   | Literature / Theory | 20-25% | 2,000-2,500 |
   | Research Design | 15-20% | 1,500-2,000 |
   | Results | 20-25% | 2,000-2,500 |
   | Discussion / Conclusion | 10-15% | 1,000-1,500 |

3. **Check existing sections:** if other sections are already written, calculate remaining budget
4. **State the budget:** before drafting, tell the user: "This section has a budget of ~X words (Y% of Z total for [journal])."

### Step 3: Read Input Materials

Based on the section type, gather specific inputs:

| Section | Primary Inputs |
|---|---|
| `abstract` | All existing sections (synthesize) |
| `introduction` | Supporting papers, theory section outline, main results |
| `literature` / `theory` | Supporting papers, bibliography, hypothesis structure |
| `design` | R scripts (for estimator details), data codebook, robustness checklists |
| `results` | R output tables, figures, analysis scripts |
| `discussion` / `conclusion` | Results section, introduction (to close the loop), limitations |
| `appendix` | Robustness R scripts, additional tables/figures |

**For results sections specifically:**
- Read actual R output files — NEVER invent coefficients, standard errors, or p-values
- Extract exact numbers from `.tex` table fragments
- Tag any magnitude interpretations with `[VERIFY INTERPRETATION]` — the researcher must confirm that "large effect" or "substantively meaningful" matches their domain knowledge

### Step 4: Invoke `scientific-writing` Skill

Use the `scientific-writing` installed skill for the core drafting:

1. **Create a section outline** with key points and logical flow
2. **Convert to flowing prose** following IMRAD conventions
3. **Pass section-specific instructions:**

   | Section | Special Instructions |
   |---|---|
   | `abstract` | Follow I-P-M-R-D pattern from `manuscript-conventions.md`. Do NOT start with "This paper..." |
   | `introduction` | Must contain: puzzle, significance, preview, contributions (in order). Check if working abstract exists and align. |
   | `literature` | Build toward YOUR argument — not a survey. End with hypotheses. Match hypothesis format to method tradition. |
   | `theory` | Derive testable implications. Every hypothesis must follow from prior theoretical argument. |
   | `design` | Include: data source, variable operationalization, identification strategy, estimation equation. Use appropriate causal language. |
   | `results` | Main findings first. Numbers from R output ONLY. Brief robustness summary (full tables in appendix). Tag interpretations. |
   | `discussion` | Summary (1 para, not recap). Honest limitations. Specific implications. Future directions. |
   | `conclusion` | If separate from discussion: shorter, focused on contribution and broader significance. |
   | `appendix` | Structure per `manuscript-conventions.md` Section 5. Context paragraph before each table. Numbering: A1, A2... B1, B2... Cross-reference all items in main text. |

### Step 5: Determine Output Mode (Adaptive)

Choose the output mode based on context:

**If `--scaffold` flag:** Force scaffolding mode.
**If `--full-prose` flag:** Force full prose mode.
**If neither flag (adaptive mode):** Claude decides based on:

| Factor | Leans Scaffold | Leans Full Prose |
|---|---|---|
| Section type | Results, Discussion | Literature, Design, Introduction |
| Section has many numerical claims | YES — researcher should verify each | — |
| Theory section with original argument | YES — researcher's voice is essential | — |
| Boilerplate structure (design description) | — | YES — straightforward to draft |
| User's past preference (check MEMORY.md for `[LEARN:writing-mode]`) | Follow learned preference | Follow learned preference |
| First draft vs revision | Scaffold for first draft of novel content | Full prose for revisions and standard sections |

**Scaffolding mode output:**
```latex
% === INTRODUCTION ===
% Budget: ~1,200 words

% [PARA 1: THE PUZZLE]
% Hook: [describe the empirical puzzle or policy question]
% Key fact or striking statistic that motivates the paper
[YOUR OPENING — what draws the reader in?]

% [PARA 2: WHY IT MATTERS]
Understanding [topic] matters because [significance].
[YOUR ANALYSIS — connect to broader literature/policy debate]

% [PARA 3: WHAT WE DO AND FIND]
We exploit [identification strategy] using [data] to estimate [outcome].
Our main finding is that [direction and magnitude from Table X].
[VERIFY INTERPRETATION: is this "large" in context?]

% [PARA 4: CONTRIBUTIONS]
% Contribution 1: [fills gap in literature X]
% Contribution 2: [methodological advance Y]
% Contribution 3: [policy implication Z]
[YOUR FRAMING — what is truly new here?]
```

**Full prose mode output:** Complete flowing paragraphs ready for the manuscript, with verification tags inline where needed.

### Step 6: Citation Verification Gate

**This step is mandatory and cannot be skipped.**

For every citation in the draft:

1. **Check `Bibliography_base.bib`** — is there a matching entry?
2. **If found:** verify author names and year match the in-text citation format
3. **If NOT found:**
   - Invoke the `citation-management` skill to search for the paper
   - If found and confirmed real: add to bibliography and mark `[ADDED TO BIB]`
   - If uncertain: tag as `[UNVERIFIED: Author Year — could not confirm this reference exists. Verify before submission.]`
4. **Never silently drop a citation** — either verify it or tag it visibly

**Output a citation report at the end:**
```
## Citation Verification Report
- Total citations in section: N
- Verified against Bibliography_base.bib: N
- Newly added to bibliography: N  [ADDED TO BIB]
- UNVERIFIED (require manual check): N  [UNVERIFIED]
```

### Step 7: Academic Voice Audit

Run the `humanizer` installed skill on the draft, PLUS these polisci-specific checks:

**AI Writing Patterns to Detect and Fix:**

| Pattern | Example | Fix |
|---|---|---|
| Inflated significance claims | "This groundbreaking study reveals..." | "This paper examines..." |
| Hedge stacking | "It could potentially be argued that perhaps..." | Pick one hedge or remove all |
| Filler transitions | "It is important to note that..." | Delete — start with the point |
| Listing with "Furthermore, Moreover, Additionally" | Three consecutive paragraphs starting with these | Vary transitions or restructure |
| Vague attribution | "Scholars have argued..." | Cite specific scholars |
| Em dash overuse | Multiple em dashes per paragraph | Replace most with commas or parentheses |
| Rule-of-three lists | "economic, political, and social" appearing repeatedly | Vary structure |
| Promotional language | "This innovative approach..." | "This approach..." |
| Passive voice clusters | Three+ consecutive passive sentences | Mix in active voice |

**Polisci-specific checks:**
- Causal language matches design strength (from `manuscript-conventions.md` Section 3)
- "Impact" not used as a verb (prefer "affect" or "is associated with")
- Methods lowercase unless proper noun ("difference-in-differences" not "Difference-in-Differences")
- APSA citation format (no comma before year, "and" not "&")
- Oxford comma present

### Step 8: R&R Mode (when `--revise` flag is present)

When revising in response to a reviewer comment:

1. **Read the reviewer comment** from the `--revise` flag
2. **Read the existing section** in the manuscript
3. **Read `response_to_reviewers.tex`** if it exists (for context on other revisions)
4. **Draft the revision:**
   - Make targeted changes addressing the specific comment
   - Minimize disruption to surrounding text
   - Maintain consistency with other sections
5. **Draft the response paragraph:**
   - Quote the reviewer comment
   - Explain what was changed and where
   - Reference exact page/section numbers
   - Save to a temporary file for inclusion in `response_to_reviewers.tex`
6. **Generate a diff summary:** list exact changes made (for `latexdiff` later)

### Step 9: Version Tracking & Save

1. **If the section already exists in the manuscript:**
   - Copy the current version to `Manuscripts/paper_name/main_prev_YYYYMMDD.tex`
   - Only keep the 3 most recent `_prev` files (delete older ones)
2. **Write the new section** to the manuscript file
3. **Update word count:** calculate and report actual word count vs budget

### Step 10: Present Results

Present a structured summary:

```
## /draft-section Summary

**Section:** [name]
**Mode:** [Scaffold / Full Prose / Adaptive → chosen mode]
**Word count:** [N] words (budget: [M], journal limit: [L])
**Journal:** [target journal]

### Citation Verification
- [N] verified, [M] newly added, [K] UNVERIFIED (require manual check)

### Voice Audit
- [N] AI patterns detected and fixed
- Causal language: [PASS / N issues flagged]

### Version Tracking
- Previous version saved to: [path]

### Items Requiring Your Attention
- [List of [UNVERIFIED] citations]
- [List of [VERIFY INTERPRETATION] markers]
- [List of [YOUR ANALYSIS] placeholders if scaffold mode]
```

---

## Section-Specific Conventions Reference

Quick reference for what each section must contain (detailed in `manuscript-conventions.md` Section 2):

| Section | Must Contain | Anti-Patterns |
|---|---|---|
| **Abstract** | Puzzle → Method → Finding → Implication | Starting with "This paper..."; no results stated; exceeds word limit |
| **Introduction** | Puzzle, significance, preview, contributions | "This is understudied" as motivation; no results preview; contributions vague |
| **Literature** | Builds toward YOUR argument | Survey of everything; no gap identification; hypotheses disconnected from theory |
| **Theory** | Testable implications derived from logic | Hypotheses without theoretical grounding; non-directional when theory predicts direction |
| **Design** | Data, variables, identification, estimation | No identification strategy stated; causal language mismatch |
| **Results** | Main findings first, robustness summary | Core results hidden in appendix; invented numbers; overclaiming |
| **Discussion** | Summary, limitations, implications, future | Section-by-section recap; generic "more research needed" |

---

## Abstract Timing

The abstract can be drafted at **any stage**:

- **Working abstract (early):** Draft after the introduction to clarify the paper's framing. Tag as `% WORKING ABSTRACT — revise after results are final`
- **Final abstract (late):** Draft after all other sections are complete, synthesizing the final argument and results

The skill handles both cases. If results sections don't exist yet, the abstract will note `[RESULTS PENDING]` where findings would go.

---

## Skill Chaining

This skill invokes other installed skills in sequence:

```
/draft-section [section]
  │
  ├── Step 4: scientific-writing (core prose generation)
  │
  ├── Step 6: citation-management (verify every reference)
  │
  └── Step 7: humanizer (voice audit and cleanup)
```

**Optimization:** Steps 6 and 7 run after the draft is complete, not during. This avoids multiple passes over the same text. The `scientific-writing` skill produces the raw draft; `citation-management` and `humanizer` refine it in a single post-processing pass.

---

## Integration Points

| Component | Connection |
|---|---|
| **`manuscript-conventions.md`** | Source of all formatting rules, section structure, causal language, citation style |
| **`/paper-outline`** | Should be run BEFORE `/draft-section` to establish structure and word budget |
| **`/submission-checklist`** | Should be run AFTER all sections are drafted to verify completeness |
| **`/reviewer-2`** | If design section is drafted, run `/reviewer-2` to check methodology claims |
| **`/validate-bib`** | Run after drafting to cross-check all citations |
| **`scientific-writing`** | Core prose generation (installed skill) |
| **`citation-management`** | Citation verification and BibTeX generation (installed skill) |
| **`humanizer`** | AI writing pattern detection and removal (installed skill) |
| **`r-reviewer`** | If results section references R code, run to verify code quality |
| **Orchestrator** | When invoked from a plan, the orchestrator governs the verify-review-fix loop |

---

## Principles

1. **The researcher's voice matters.** Adapt output mode to the section — don't force full prose where the researcher's original analysis belongs.
2. **No hallucinated citations.** Every reference is verified or visibly tagged. This is the hardest constraint and the most important.
3. **No invented results.** Numbers come from R output or tables — never from the model's training data.
4. **Word budgets are real.** Political science journals enforce limits. Exceeding them wastes the researcher's time.
5. **Causal language is earned.** The words you use must match the strength of your identification strategy.
6. **Version safety.** Never destroy previous work. Save before overwriting.
7. **Transparency over polish.** A draft with visible `[UNVERIFIED]` tags is better than a polished draft with hidden errors.
