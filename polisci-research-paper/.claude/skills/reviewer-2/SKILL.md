---
name: reviewer-2
description: Research design devil's advocate. Auto-detects your methodology (DID, RDD, IV, conjoint, process tracing, QCA, text-as-data, formal theory, etc.) and interrogates identification, estimator choice, robustness architecture, transparency, and external validity. Produces a hostile but constructive Reviewer 2 report with the 3 most devastating questions and a design-specific robustness checklist. Read-only — never edits files.
argument-hint: "[optional: specific file, folder, or design type to focus on]"
---

# /reviewer-2 — Research Design Devil's Advocate

Interrogate your project's research design the way a hostile journal referee would — before you submit.

**Philosophy:** "Better to hear this from Claude than from Reviewer 2 at APSR."

---

## What This Skill Does

1. **Detects** your research design type from project files (R code, manuscripts)
2. **Runs 4 universal lenses** (theory-method alignment, measurement, transparency, external validity)
3. **Loads design-specific modules** (DID, RDD, IV, conjoint, process tracing, QCA, etc.)
4. **Produces** a Reviewer 2 report with the 3 most devastating questions and a robustness checklist
5. **Never edits files** — report only

---

## What This Skill Does NOT Do

- Edit files (read-only — use the report to decide what to fix)
- Check math correctness (that's `domain-reviewer`)
- Check writing quality (that's `proofreader`)
- Score on 0-100 (design quality is categorical: ACCEPT / MINOR / MAJOR / REJECT)
- Replace actual peer review (it's a preparation tool)

---

## Workflow

```
Phase 0: Detect design type from project files
    │
Phase 1: Run 4 universal lenses
    │    Lens 1: Theory-Method Alignment
    │    Lens 2: Data & Measurement Interrogation
    │    Lens 3: Transparency & Reproducibility
    │    Lens 4: External Validity & Generalizability
    │
Phase 2: Load and run design-specific module(s)
    │    (from .claude/rules/robustness-checklists.md)
    │
Phase 3: Synthesize into Reviewer 2 Report
    │    → 3 Most Devastating Questions
    │    → Design-specific robustness checklist (present vs missing)
    │    → Verdict: ACCEPT / MINOR / MAJOR / REJECT
    │
Save report to quality_reports/
```

---

## Steps

### Step 0: Parse Arguments

Parse `$ARGUMENTS` for optional focus:
- If a **filename** is given: focus on that file and its associated code/bibliography
- If a **folder** is given (e.g., `Manuscripts/paper_title/`): scan that folder
- If a **design type** is given (e.g., "DID", "conjoint"): skip auto-detection, load that module directly
- If **no argument**: scan the entire project

### Step 1: Inventory Project Files

Read the project structure to understand what exists:

1. **Manuscripts:** Glob `Manuscripts/**/*.tex`
2. **R scripts:** Glob `scripts/**/*.R`, `Replication/**/*.R`
4. **Data:** Glob `Replication/data/**/*`, `data/**/*`
5. **Bibliography:** Read `Bibliography_base.bib`
6. **Memory:** Read `./PROJECT_MEMORY.md` for `[LEARN:methodology]` entries
7. **Supporting papers:** Glob `master_supporting_docs/supporting_papers/**`
   - **Follow the safe PDF processing protocol** (see `.claude/rules/pdf-processing.md`):
     1. Check each PDF's size and page count (`pdfinfo`, `ls -lh`) — NEVER read a PDF directly without checking first
     2. If >20 pages or >10MB: split into 5-page chunks using Ghostscript before reading
     3. Process chunks one at a time; focus on methodology, identification, and results sections
     4. For `/reviewer-2` specifically: prioritize the design/methods and results chunks — skip literature review and appendix chunks unless needed for cross-referencing
   - If papers were already split in a prior session, read the existing chunks instead of re-splitting

If the project has very few files (e.g., no R code yet), note this as a limitation — the review will be less thorough without code to cross-reference.

### Step 2: Design Detection (Phase 0)

Scan R scripts and manuscript text for design signals. Use the detection heuristics from the `methodology-reviewer` agent specification.

**Rules:**
- Multiple designs can be detected (e.g., "DID with Bayesian estimation" loads Module A + Module M)
- If detection is ambiguous, state what you found and ask the user to confirm
- If no R code exists (qualitative project), detection relies on manuscript text
- If nothing is detected, proceed with universal lenses only and note the limitation

**State the detected design(s) explicitly before proceeding.**

### Step 3: Launch Methodology Reviewer Agent

Launch the `methodology-reviewer` agent with a prompt that includes:

1. The detected design type(s)
2. The files to read (from Step 1 inventory)
3. Instructions to:
   - Run all 4 universal lenses
   - Read `.claude/rules/robustness-checklists.md` and apply the relevant module(s)
   - Cross-reference manuscript claims against R code
   - Produce the full report in the specified format

The agent runs as a **Task** with `subagent_type: methodology-reviewer`.

**IMPORTANT:** The agent is read-only. If it suggests edits, those are recommendations in the report, not actions to take.

### Step 4: Optionally Invoke Installed Skills for Deep Checks

If the methodology-reviewer's findings suggest deeper investigation is warranted, you MAY invoke these installed skills for specific sub-checks:

| Installed Skill | When to Invoke |
|---|---|
| `scientific-critical-thinking` | When the identification strategy is novel or complex and needs systematic bias assessment |
| `statistical-analysis` | When power analysis, assumption checks, or specific hypothesis tests need verification |
| `peer-review` | When a full manuscript exists and you want a broader review beyond just design |
| `citation-management` | When methodological citations need verification (e.g., "is that really what Roth 2022 says?") |

These are optional enhancements, not required steps. The methodology-reviewer agent handles the core review.

### Step 5: Synthesize and Save Report

After the methodology-reviewer agent returns:

1. **Review the agent's report** for completeness
2. **Add cross-cutting observations** that span multiple lenses (e.g., a measurement problem that also affects identification)
3. **Synthesize the 3 Most Devastating Questions** — these should be:
   - Specific (reference exact claims, variables, files)
   - Constructive (include how to address each)
   - Prioritized (#1 is the most damaging)
4. **Assign the verdict:**

| Verdict | Criteria |
|---|---|
| **ACCEPT** | Design is sound, robustness adequate, transparency sufficient. Minor suggestions only. No critical or major issues. |
| **MINOR REVISION** | Design is sound but missing some standard checks. All issues addressable in 1-2 weeks. No critical issues, 1-3 major issues. |
| **MAJOR REVISION** | Design has addressable weaknesses. Core identification may be salvageable with additional tests or alternative estimators. 1+ critical or 4+ major issues. |
| **REJECT** | Fundamental design flaw not fixable with revisions. Theory-method mismatch, implausible identification, or fatal data problems. |

5. **Save report** to `quality_reports/[project_or_file]_reviewer2_report.md`

### Step 6: Present Summary to User

After saving the report, present a concise summary:

```
## Reviewer 2 Summary

**Design detected:** [type(s)]
**Verdict:** [ACCEPT / MINOR / MAJOR / REJECT]

### The 3 Most Devastating Questions
1. [question — 1 sentence]
2. [question — 1 sentence]
3. [question — 1 sentence]

### Robustness Gaps
- [N] tests present, [M] tests missing from the [design type] checklist
- **Priority addition:** [the single most impactful missing check]

### Full report saved to:
`quality_reports/[name]_reviewer2_report.md`
```

---

## Report Format

The full report follows the template specified in the `methodology-reviewer` agent. Key sections:

1. **Header:** Date, detected design(s), verdict
2. **The 3 Most Devastating Questions** (with "why it's devastating" and "how to address it")
3. **Universal Lens Findings** (Lenses 1-4, each with severity rating)
4. **Design-Specific Findings** (identification, estimator alignment, robustness checklist)
5. **Verdict Justification** (table of criteria)
6. **What's Actually Strong** (2-3 genuine strengths)
7. **Recommended Methodological Reading** (2-3 papers relevant to this project's weaknesses)

---

## Design Types Supported

### Quantitative Causal Inference
| Module | Trigger Keywords |
|---|---|
| A: Difference-in-Differences | `feols`, `att_gt`, parallel trends, staggered |
| B: Regression Discontinuity | `rdrobust`, cutoff, bandwidth, running variable |
| C: Instrumental Variables | `ivreg`, 2SLS, instrument, first stage |
| D: Matching / Weighting | `MatchIt`, propensity score, entropy balancing |
| E: Synthetic Control | `Synth`, `gsynth`, donor pool |
| N: ML for Causal Inference | `causal_forest`, `DoubleML`, post-LASSO |

### Experimental
| Module | Trigger Keywords |
|---|---|
| F: Survey & Conjoint | `cregg`, AMCE, conjoint, vignette |
| G: Field & Lab Experiments | `randomizr`, `DeclareDesign`, treatment assignment |

### Text & Computational
| Module | Trigger Keywords |
|---|---|
| H: Text-as-Data / NLP | `quanteda`, `stm`, topic model, sentiment |
| L: Network Analysis | `ergm`, `statnet`, network formation |
| O: Measurement / Scaling | `mirt`, `lavaan`, IRT, latent variable |

### Qualitative & Set-Theoretic
| Module | Trigger Keywords |
|---|---|
| I: Process Tracing | causal mechanism, smoking gun, hoop test |
| J: Comparative Cases | most similar, most different, Mill's method |
| K: QCA | fuzzy set, truth table, necessity, sufficiency |

### Other
| Module | Trigger Keywords |
|---|---|
| M: Bayesian | `brms`, `rstan`, posterior, prior |
| P: Multi-Level / Hierarchical | `lme4`, `lmerTest`, multilevel, random intercept |
| Q: Formal Theory | Nash equilibrium, subgame perfect, mechanism design |
| R: Descriptive Inference | describe, patterns, typology, no causal claim |

---

## Integration Points

| Existing Component | How `/reviewer-2` Connects |
|---|---|
| **Orchestrator (Step 3: REVIEW)** | Can be called during review step for manuscripts |
| **`domain-reviewer` agent** | Complementary: domain-reviewer checks math, `/reviewer-2` checks design |
| **`r-reviewer` agent** | Complementary: r-reviewer checks code quality, `/reviewer-2` checks estimator choice |
| **`replication-protocol` rule** | Lens 3 verifies replication protocol compliance |
| **Quality gates** | Categorical verdict complements numeric quality score |

---

## Principles

1. **Be hostile but constructive.** Every criticism has a suggested fix.
2. **Read the actual code.** Don't just review the methods section — verify claims against R scripts.
3. **Be design-aware.** A DID paper needs different checks than a process-tracing paper. Don't apply the wrong checklist.
4. **Acknowledge strengths.** Not everything is wrong. Name what the project does well.
5. **Prioritize ruthlessly.** The 3 most devastating questions should be the things that would sink a submission.
6. **Stay in your lane.** Design, not writing. Identification, not formatting. Estimators, not pedagogy.
7. **Cite your concerns.** When flagging an issue, cite the methodological paper that supports your concern.
8. **Never edit files.** This is a review, not a fix. The user decides what to change.
