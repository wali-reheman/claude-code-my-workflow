---
name: create-paper
description: End-to-end manuscript creation orchestrator. Guides a paper from outline through section drafting, methodology review, and submission readiness. Chains /paper-outline, /draft-section, /reviewer-2, and /submission-checklist into a phased, gate-controlled workflow.
argument-hint: "[paper topic or title] [--journal APSR] [--design DID] [--resume phase-N]"
---

# /create-paper — Manuscript Creation Orchestrator

Guide a research paper from blank page to submission-ready manuscript through a phased, gate-controlled workflow.

**This is the manuscript equivalent of `/create-lecture`.** The researcher drives the vision, Claude orchestrates the pipeline, and quality gates ensure nothing ships broken.

**Philosophy:** Papers are not written in one pass. They are built in phases, with the researcher making critical decisions at each gate. This skill manages the pipeline; the researcher makes the calls.

---

## What This Skill Does

1. **Orchestrates** the full paper pipeline: outline → draft → review → submit
2. **Chains** four skills in sequence: `/paper-outline` → `/draft-section` (×N) → `/reviewer-2` → `/submission-checklist`
3. **Manages gates** between phases — the researcher approves before proceeding
4. **Tracks progress** with a persistent plan file that survives context compression
5. **Supports resumption** — pick up where you left off with `--resume`
6. **Runs review agents** automatically at appropriate phases

---

## What This Skill Does NOT Do

- Write the entire paper autonomously without input (every phase has a gate)
- Run your R analysis (that's a prerequisite — bring your tables/figures)
- Replace your judgment on theory, argument, or framing
- Guarantee acceptance (it prepares you; journals decide)

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `[topic]` | YES (unless `--resume`) | Paper topic, title, or research question |
| `--journal` | NO | Target journal (default: APSR). Propagated to all sub-skills |
| `--design` | NO | Research design type. Propagated to `/paper-outline` and `/reviewer-2` |
| `--resume phase-N` | NO | Resume from a specific phase (reads plan file for context) |
| `--fast` | NO | Skip optional review rounds — only run mandatory gates |
| `--r-and-r` | NO | R&R mode: skip Phases 1-3, start from Phase 4 (revision) with existing manuscript |

---

## The Pipeline

```
/create-paper "Electoral Violence and Voter Turnout" --journal APSR --design DID
│
├── Phase 1: OUTLINE                 ← /paper-outline
│     → folder structure, section skeleton, word budget
│     GATE 1: User approves structure
│
├── Phase 2: INPUTS                  ← researcher provides materials
│     → papers, data, R output, existing drafts
│     GATE 2: User confirms inputs are ready
│
├── Phase 3: DRAFT                   ← /draft-section (×N sections)
│     → section-by-section drafting in recommended order
│     → citation verification + voice audit per section
│     GATE 3: User approves full draft
│
├── Phase 4: REVIEW                  ← /reviewer-2 + review agents
│     → methodology review (hostile)
│     → proofreading, causal language audit
│     → fix rounds (orchestrator loop)
│     GATE 4: User approves revisions
│
├── Phase 5: POLISH                  ← final editing pass
│     → anonymization, word count, formatting
│     → cover letter draft
│     GATE 5: User approves final version
│
└── Phase 6: SUBMISSION CHECK        ← /submission-checklist
      → 60+ pass/fail checks
      → READY / NOT READY verdict
      → hand off to user for actual submission
```

---

## Phase Details

### Phase 1: OUTLINE

**Invoke:** `/paper-outline [topic] --journal [journal] --design [design]`

This phase creates:
- Manuscript folder structure (`Manuscripts/[short_name]/`)
- Section skeleton with word budgets
- Hypothesis stubs matched to design type
- `main.tex` and `appendix.tex` templates
- Plan file saved to `quality_reports/plans/`

**Gate 1 — Structure Approval:**
Present the outline and ask:
- "Does this section structure match your argument?"
- "Are the word allocations reasonable?"
- "Is the hypothesis format correct for your design?"
- "Any sections to add, remove, or reorder?"

**Do not proceed until the user explicitly approves.**

After approval, update the plan file: `Status: Phase 1 COMPLETE`.

---

### Phase 2: INPUTS

**No skill invoked — this is a researcher-driven phase.**

Guide the researcher to provide:

```
## Materials Checklist

### Required Before Drafting
- [ ] R analysis scripts (or link to existing scripts)
- [ ] Generated tables (.tex fragments in tables/ folder)
- [ ] Generated figures (PDF/SVG in figures/ folder)
- [ ] Key papers for literature review (upload to `master_supporting_docs/supporting_papers/`)
- [ ] Data description (source, access, time period, unit of analysis)

### Required Before Results Section
- [ ] Main results table(s) — at minimum Table 1
- [ ] At least one robustness check
- [ ] Any heterogeneity/mechanism results

### Optional but Recommended
- [ ] Existing draft text (any stage — will be incorporated)
- [ ] Conference presentation slides
- [ ] Reviewer comments (if R&R — triggers revision mode)
- [ ] Pre-analysis plan (if registered)
```

#### PDF Processing for Supporting Papers

When the user uploads papers to `master_supporting_docs/supporting_papers/`, **follow the safe PDF processing protocol** (see `.claude/rules/pdf-processing.md`) before attempting to read any PDF:

1. **Check each PDF's size and page count** (`pdfinfo`, `ls -lh`) — NEVER read a PDF directly without checking first
2. **If >20 pages or >10MB:** split into 5-page chunks using Ghostscript, saving chunks to a subfolder named after the paper
3. **Process chunks one at a time** — extract key arguments, identification strategy, results, and citations
4. **If papers were already split in a prior session**, read the existing chunks instead of re-splitting
5. **Summarize each paper** in the plan file (1-2 sentences: what it argues, what method, what finding) for persistence across sessions

This step is critical — skipping it risks crashing the session on large PDFs.

**Gate 2 — Inputs Ready:**
Check which inputs are available and assess readiness:
- If tables/figures exist → ready for results drafting
- If no R output yet → can still draft introduction, literature, design sections
- If supporting papers provided and processed → ready for literature review

**Partial starts are fine.** The pipeline adapts:
- Draft sections that don't need R output first (introduction, literature, design)
- Return to results/discussion when R output is ready
- The plan file tracks which sections are drafted and which are pending

After assessment, update the plan file: `Status: Phase 2 COMPLETE (partial: [list what's missing])`.

---

### Phase 3: DRAFT

**Invoke:** `/draft-section [section]` for each section, in recommended order.

#### Default Drafting Order

The order depends on what inputs are available:

**If R output exists (full pipeline):**
1. `introduction` — establishes the puzzle and argument
2. `design` — anchors the methodology
3. `results` — reports findings (requires tables/figures)
4. `literature` — builds toward hypotheses (informed by results framing)
5. `discussion` — closes the loop
6. `abstract` — synthesizes everything (always last)

**If R output does NOT exist yet (partial pipeline):**
1. `introduction` — can draft with provisional findings
2. `literature` — independent of R output
3. `design` — can draft with planned (not actual) methodology
4. PAUSE — wait for R output
5. `results` → `discussion` → `abstract` after R output arrives

#### Section Drafting Protocol

For each section:

1. **Announce:** "Drafting [section]. Budget: ~[N] words. Mode: [scaffold/full-prose/adaptive]."
2. **Invoke:** `/draft-section [section] --journal [journal] --file [manuscript path]`
3. **Present output** with citation verification report and voice audit summary
4. **Mini-gate:** "Does this section capture your argument? Any changes before moving to the next?"

The user can:
- **Approve** → move to next section
- **Request changes** → revise before moving on
- **Switch to scaffold mode** → if they want to write this section themselves
- **Skip** → come back to this section later
- **Provide additional input** → papers, notes, preferences for this section

#### Between Sections

After every 2-3 sections, run a quick consistency check:
- Do the sections reference each other correctly?
- Is the argument thread coherent?
- Are notation and terminology consistent?
- Is the cumulative word count on budget?

**Gate 3 — Full Draft Approval:**
When all sections are drafted, present a manuscript overview:

```
## Full Draft Overview

**Total word count:** [N] / [limit]
**Sections drafted:** [list with word counts]
**Citations:** [N] verified, [M] unverified, [K] newly added
**Voice audit:** [N] AI patterns fixed
**Scaffolded sections:** [list, if any — these need researcher input]

### Argument Thread
[1-paragraph summary of how the introduction → literature → design → results → discussion flows]

### Open Items
- [UNVERIFIED] citations requiring manual check: [list]
- [VERIFY INTERPRETATION] markers in results: [list]
- [YOUR ANALYSIS] placeholders in scaffolded sections: [list]
```

**Do not proceed to Phase 4 until the user approves the draft and resolves all `[YOUR ANALYSIS]` placeholders.**

After approval, update the plan file: `Status: Phase 3 COMPLETE`.

---

### Phase 4: REVIEW

**Invoke:** `/reviewer-2 Manuscripts/[paper_name]/`

Plus additional review agents in parallel:

| Agent | What It Reviews | Parallel? |
|---|---|---|
| `methodology-reviewer` (via `/reviewer-2`) | Research design, identification, robustness | First |
| `proofreader` | Grammar, typos, style | Yes (after reviewer-2) |
| `domain-reviewer` | Substantive accuracy (if configured) | Yes |

#### Review-Fix Loop

After reviews complete, enter the orchestrator loop (from `orchestrator-protocol.md`):

```
Reviews received
  │
  Step 1: Prioritize issues (Critical → Major → Minor)
  Step 2: Fix critical issues (compilation, citation, math errors)
  Step 3: Fix major issues (causal language, missing checks, content gaps)
  Step 4: Fix minor issues (style, spacing, polish)
  Step 5: Re-verify (compile, word count, citations)
  Step 6: Re-run relevant reviews if critical/major fixes were made
  │
  └── Max 3 review-fix rounds for the manuscript
```

#### Handling /reviewer-2 Verdicts

| Verdict | Action |
|---|---|
| **ACCEPT** | Proceed to Phase 5 |
| **MINOR REVISION** | Fix issues, re-run `/reviewer-2` once. Then proceed. |
| **MAJOR REVISION** | Present findings to user. Discuss whether to address now or note as limitations. User decides. |
| **REJECT** | Stop. Present the fundamental design flaw to the user. This requires researcher intervention, not skill fixes. |

**Gate 4 — Review Approval:**
Present the consolidated review summary:

```
## Review Summary

**Reviewer 2 verdict:** [verdict]
**Proofreader:** [N] issues found, [M] fixed
**Causal language:** [PASS / N issues]

### Issues Fixed
- [list with severity]

### Remaining Issues (User Decision Required)
- [list — these are judgment calls, not mechanical fixes]

### Robustness Gaps
- [from /reviewer-2 — checks present vs missing]
```

After approval, update the plan file: `Status: Phase 4 COMPLETE`.

---

### Phase 5: POLISH

Final editing pass before submission checks.

#### 5a: Anonymization

If target journal requires blind review (check `manuscript-conventions.md` Section 7):

1. Create `main_anonymous.tex` from `main.tex`
2. Run the anonymization checklist (Section 4 of `manuscript-conventions.md`):
   - Strip author names, affiliations, acknowledgments
   - Handle self-citations
   - Check PDF metadata
3. Present the anonymized version for user review

#### 5b: Word Count Final Check

- Count words in the final manuscript
- Compare to journal limit
- If over: flag the longest sections and suggest cuts
- If under: note available budget for expansion

#### 5c: Cover Letter Draft

Draft `cover_letter.tex` with:
- Addressee (editor of target journal)
- 1-paragraph summary of the paper and its contribution
- Why it fits this journal
- Confirmation of originality and no simultaneous submission
- Author contact information placeholder

Present for user review — **the user must personalize this.**

#### 5d: Formatting Final Pass

- Verify table format (booktabs, caption placement, star definitions)
- Verify figure format (caption placement, resolution, grayscale readability)
- Verify equation numbering
- Verify appendix numbering and cross-references
- Verify citation format matches target journal (APSA vs APA)

**Gate 5 — Final Version Approval:**
Present the polished manuscript with all changes from this phase.

After approval, update the plan file: `Status: Phase 5 COMPLETE`.

---

### Phase 6: SUBMISSION CHECK

**Invoke:** `/submission-checklist Manuscripts/[paper_name] --journal [journal]`

This runs 60+ automated checks and produces a READY / NOT READY verdict.

**If READY:**
```
## 🎯 Manuscript Ready for Submission

**Journal:** [target]
**All checks passed.** No FAIL items.

### Submission Package
- [ ] Upload `main_anonymous.tex` (compiled PDF) to journal portal
- [ ] Upload `appendix.tex` (compiled PDF)
- [ ] Upload `cover_letter.tex` (compiled PDF)
- [ ] Upload replication package to Dataverse (if required)
- [ ] Double-check journal portal for any additional requirements
```

**If NOT READY:**
Present the FAIL items with specific fix instructions. Fix them, then re-run `/submission-checklist`.

After passing, update the plan file: `Status: Phase 6 COMPLETE — READY FOR SUBMISSION`.

---

## Resumption

Papers take weeks or months. This skill is designed for interruption and resumption.

### `--resume phase-N`

When resuming:

1. Read the plan file from `quality_reports/plans/` for this paper
2. Read `./PROJECT_MEMORY.md` for any `[LEARN]` entries added since last session
3. Read the manuscript file for current state
4. Check `git log` for recent changes
5. State what has been completed and what's next
6. Pick up from the specified phase

### Automatic Resumption Detection

If no `--resume` flag but a plan file exists for this topic:
- Detect the current phase from the plan file
- Ask: "I found an in-progress plan for [paper]. You're at Phase [N]. Resume from there?"

### Plan File Updates

The plan file is the persistent memory for this paper. It tracks:

```markdown
# Plan: [Paper Title]

**Status:** Phase [N] IN PROGRESS
**Journal:** [target]
**Design:** [type]
**Created:** [date]
**Last updated:** [date]

## Progress
- [x] Phase 1: Outline — COMPLETE (2026-02-08)
- [x] Phase 2: Inputs — COMPLETE (2026-02-09)
- [ ] Phase 3: Draft — IN PROGRESS
  - [x] introduction (1,180 words)
  - [x] design (1,650 words)
  - [ ] results — waiting for R output
  - [ ] literature
  - [ ] discussion
  - [ ] abstract
- [ ] Phase 4: Review
- [ ] Phase 5: Polish
- [ ] Phase 6: Submission Check

## Word Budget
| Section | Budget | Actual | Status |
|---------|--------|--------|--------|
| Introduction | 1,200 | 1,180 | ✓ |
| Literature | 2,200 | — | pending |
| Design | 1,700 | 1,650 | ✓ |
| Results | 2,200 | — | pending |
| Discussion | 1,200 | — | pending |
| Abstract | 175 | — | pending |
| **Total** | **8,500** | **2,830** | |

## Decisions Log
- [date] Structure: Combined lit review and theory into single section
- [date] Hypothesis format: H1/H2 (quantitative)
- [date] Results: Scaffold mode chosen by user for Table 2 interpretation
- [date] Reviewer-2 verdict: MINOR — added parallel trends test

## Open Items
- [ ] R output for robustness checks needed
- [ ] Verify interpretation of coefficient in Table 2
- [ ] 2 unverified citations to check
```

---

## R&R Mode (`--r-and-r`)

When revising after a Revise & Resubmit decision:

1. **Skip Phases 1-3** — the paper already exists
2. **Start at a modified Phase 4:**
   - Read the existing manuscript
   - Read the reviewer comments (user provides these)
   - Create `response_to_reviewers.tex` structure
   - For each reviewer comment:
     - Assess what section(s) need revision
     - Invoke `/draft-section [section] --revise "reviewer comment"` for each
     - Track changes for `latexdiff`
3. **Phase 5:** Generate tracked-changes version + response document
4. **Phase 6:** Run `/submission-checklist` on revised manuscript

The R&R plan file uses a different structure:

```markdown
## Reviewer Comments Tracker
| # | Reviewer | Comment Summary | Status | Section Affected |
|---|---------|-----------------|--------|-----------------|
| 1 | R1 | Parallel trends concern | Fixed | Design (p.14) |
| 2 | R1 | Alternative DV requested | Fixed | Results (new Table A3) |
| 3 | R2 | Lit review missing X | In progress | Literature |
| 4 | R2 | Scope conditions unclear | Pending | Discussion |
| 5 | Editor | Shorten introduction | Fixed | Introduction |
```

---

## Orchestrator Integration

When this skill is invoked, it activates the orchestrator protocol:

1. **Phase 1-2:** Standard plan-first workflow (plan → approve → implement)
2. **Phase 3:** Orchestrator manages section drafting with verification after each section
3. **Phase 4:** Orchestrator runs the review-fix loop (max 3 rounds for manuscripts)
4. **Phase 5-6:** Orchestrator runs final verification

**Agent selection for manuscripts** (extends `orchestrator-protocol.md`):

| Files Modified | Agents to Run | Parallel? |
|---|---|---|
| `Manuscripts/**/*.tex` | proofreader, domain-reviewer (if configured) | Yes |
| `Manuscripts/**/*.tex` (design section) | + methodology-reviewer (via `/reviewer-2`) | After above |
| `Replication/**/*.R` | r-reviewer | Yes (with proofreader) |
| `Bibliography_base.bib` | validate-bib logic | Yes |

---

## Comparison: `/create-paper` vs `/create-lecture`

| Aspect | `/create-lecture` | `/create-paper` |
|---|---|---|
| **Timeline** | Single session | Multiple sessions (weeks/months) |
| **Output** | 40-80 slides | 8,000-14,000 word manuscript |
| **Phases** | 6 (Intake → Polish) | 6 (Outline → Submission) |
| **Gates** | 1 main gate (Phase 2) | 6 gates (every phase) |
| **Resumption** | Rarely needed | Always needed (`--resume`) |
| **Review** | Devil's advocate + slide auditor | Reviewer-2 + proofreader |
| **Quality metric** | Score 0-100 | Categorical verdict + READY/NOT READY |
| **Iteration unit** | 5-10 slides | 1 section at a time |
| **R&R support** | N/A | Yes (`--r-and-r`) |

---

## Integration Points

| Component | Connection |
|---|---|
| **`/paper-outline`** | Phase 1 — creates the skeleton |
| **`/draft-section`** | Phase 3 — drafts each section |
| **`/reviewer-2`** | Phase 4 — hostile methodology review |
| **`/submission-checklist`** | Phase 6 — final pass/fail gate |
| **`/validate-bib`** | Phase 5 — bibliography cross-reference |
| **`manuscript-conventions.md`** | Source of truth for all formatting rules |
| **`robustness-checklists.md`** | Loaded by `/reviewer-2` for design-specific checks |
| **`orchestrator-protocol.md`** | Governs the review-fix loop in Phase 4 |
| **`plan-first-workflow.md`** | Governs Phase 1 planning and plan file persistence |
| **`proofreader` agent** | Phase 4 review |
| **`domain-reviewer` agent** | Phase 4 review (if configured) |
| **`r-reviewer` agent** | Phase 4 review (if R code modified) |
| **`scientific-writing`** | Invoked by `/draft-section` for prose generation |
| **`citation-management`** | Invoked by `/draft-section` for citation verification |
| **`humanizer`** | Invoked by `/draft-section` for voice audit |

---

## Principles

1. **Phases, not passes.** Papers are built in discrete phases, each with clear inputs, outputs, and gates.
2. **Gates are non-negotiable.** The researcher approves at every phase. No autonomous end-to-end execution.
3. **Resumption is the norm.** Papers take weeks. Every decision persists in the plan file.
4. **Adapt to what exists.** Partial inputs are fine — draft what you can, pause for what you can't.
5. **Reviews are investments.** Running `/reviewer-2` before submission saves months of rejection cycles.
6. **The researcher writes the paper.** Claude orchestrates, drafts, verifies, and reviews — but the argument, the theory, and the judgment are the researcher's.
7. **Track everything.** The plan file is the paper's institutional memory across sessions.
