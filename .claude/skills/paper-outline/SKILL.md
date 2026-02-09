---
name: paper-outline
description: Create a manuscript skeleton with section structure, word budget, hypothesis stubs, and empty files. Sets up the foundation for /draft-section to build on.
disable-model-invocation: true
argument-hint: "[paper title or topic] [--journal APSR] [--design DID]"
---

# /paper-outline — Manuscript Skeleton Generator

Create the structural foundation for a new manuscript: folder structure, section outline, word budget, hypothesis stubs, and empty files ready for `/draft-section`.

**Philosophy:** A paper's structure determines its success as much as its content. This skill front-loads structural decisions so that drafting is focused and efficient.

---

## What This Skill Does

1. **Creates** the manuscript folder structure (from `manuscript-conventions.md` Section 1)
2. **Proposes** a section outline with argument flow
3. **Calculates** word budget per section based on target journal
4. **Stubs** hypothesis formatting matched to method tradition
5. **Generates** a working title and abstract placeholder
6. **Creates** empty `main.tex` with preamble, section headers, and `\input{}` stubs
7. **Saves** the outline as the active plan for `/draft-section` to consume

---

## What This Skill Does NOT Do

- Write prose (that's `/draft-section`)
- Choose your research design (that's your job)
- Create R analysis scripts (that's separate)
- Review methodology (that's `/reviewer-2`)

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `[topic]` | YES | Paper topic, title, or research question |
| `--journal` | NO | Target journal (default: APSR). Affects word limits, citation style, structure |
| `--design` | NO | Research design type (DID, RDD, IV, conjoint, etc.). Affects hypothesis format and design section stub |
| `--sections` | NO | Custom section list (default: standard IMRAD for polisci) |

---

## Workflow

### Step 1: Parse Arguments & Read Conventions

1. Parse `$ARGUMENTS` for topic, journal, and design type
2. Read `manuscript-conventions.md` for:
   - Folder structure (Section 1)
   - Document structure (Section 2)
   - Journal requirements (Section 7)
   - Hypothesis formatting rules (Section 2)
3. Read `MEMORY.md` for relevant `[LEARN]` entries
4. Check if a manuscript folder for this topic already exists

### Step 2: Propose Structure

Present the proposed outline to the user:

```
## Proposed Manuscript Structure: [Topic]

**Target journal:** [journal] ([word limit] words)
**Research design:** [type] (detected or specified)

### Outline

1. **Introduction** (~[N] words, [%]%)
   - Puzzle: [1-sentence description of the gap]
   - Preview: [1-sentence summary of approach and finding direction]

2. **Literature Review / Theory** (~[N] words, [%]%)
   - [Lit strand 1]: [key debate or gap]
   - [Lit strand 2]: [how it connects to your argument]
   - Hypotheses: [format based on design — H1/H2 or Propositions or RQs]

3. **Research Design** (~[N] words, [%]%)
   - Data: [source placeholder]
   - Treatment/IV/Running variable: [placeholder]
   - Identification: [strategy based on design type]
   - Estimation: [equation placeholder]

4. **Results** (~[N] words, [%]%)
   - Main results (Table 1-2)
   - Robustness summary (full tables → Appendix A)
   - [Heterogeneity / Mechanisms if applicable]

5. **Discussion / Conclusion** (~[N] words, [%]%)
   - Summary of findings
   - Limitations
   - Implications

**Total:** ~[N] words (limit: [M])
**Appendix budget:** [if applicable, e.g., "JOP: 25 pages max"]
```

**GATE: Wait for user approval before creating files.**

### Step 3: Create Folder Structure

After approval, create the manuscript folder:

```bash
Manuscripts/
└── [paper_short_name]/
    ├── main.tex              # Manuscript with section headers
    ├── main_anonymous.tex    # Created later (before submission)
    ├── appendix.tex          # Appendix skeleton
    ├── figures/              # Empty, ready for R output
    ├── tables/               # Empty, ready for R output
    └── submission/           # Empty, for final package
```

### Step 4: Generate main.tex Skeleton

Create `main.tex` with:

1. **Preamble** referencing `../../Preambles/header.tex` (or appropriate preamble)
2. **Title, author, abstract placeholders**
3. **Section headers** matching the approved outline
4. **Word budget comments** at each section header:
   ```latex
   % === INTRODUCTION ===
   % Budget: ~1,200 words (12% of 10,000)
   % Must contain: puzzle, significance, preview, contributions
   \section{Introduction}

   % [Draft with /draft-section introduction]
   ```
5. **Hypothesis stubs** in the theory section, formatted per design type:
   ```latex
   % Hypothesis format: Quantitative (numbered, italicized)
   \textit{H1: [Directional prediction derived from theory above.]}

   \textit{H2: [Second prediction, if applicable.]}
   ```
6. **`\input{}` stubs** for tables:
   ```latex
   % \input{tables/table1.tex}  % Main results — create with R
   % \input{tables/table2.tex}  % Robustness — create with R
   ```
7. **Bibliography reference:**
   ```latex
   \bibliography{../../Bibliography_base}
   ```

### Step 5: Generate appendix.tex Skeleton

Create a minimal appendix with:
- Appendix section headers (Robustness, Data Construction, Additional Results)
- Numbering convention comments (Table A1, A2... Figure A1...)
- `\input{}` stubs for appendix tables

### Step 6: Save as Active Plan

Save the outline to `quality_reports/plans/YYYY-MM-DD_paper-[short-name].md` with:

- **Status:** APPROVED
- **Journal:** target journal and word limit
- **Design:** detected or specified research design
- **Section breakdown** with word budgets
- **File paths** for all created files
- **Next steps:** which sections to draft first (recommend: Introduction → Design → Results → Literature → Discussion → Abstract)

This plan file is consumed by `/draft-section` to enforce word budgets and section conventions.

### Step 7: Present Summary

```
## /paper-outline Summary

**Paper:** [title/topic]
**Journal:** [target] ([word limit] words)
**Design:** [type]

### Files Created
- `Manuscripts/[name]/main.tex` — manuscript skeleton with [N] section headers
- `Manuscripts/[name]/appendix.tex` — appendix skeleton
- `Manuscripts/[name]/figures/` — empty directory
- `Manuscripts/[name]/tables/` — empty directory

### Word Budget
| Section | Words | % |
|---------|-------|---|
| Introduction | [N] | [%] |
| Literature/Theory | [N] | [%] |
| Design | [N] | [%] |
| Results | [N] | [%] |
| Discussion | [N] | [%] |
| **Total** | **[N]** | **100%** |
| Abstract | [N] words (separate) |

### Recommended Drafting Order
1. `/draft-section introduction` — establishes the argument
2. `/draft-section design` — anchors methodology
3. `/draft-section results` — requires R output first
4. `/draft-section literature` — builds toward hypotheses
5. `/draft-section discussion` — closes the loop
6. `/draft-section abstract` — synthesizes everything (last)

### Plan saved to:
`quality_reports/plans/[filename]`
```

---

## Design-Specific Stubs

The skeleton adapts based on `--design`:

| Design | Design Section Includes | Hypothesis Format |
|---|---|---|
| **DID** | Parallel trends discussion, treatment timing, staggered adoption | Numbered H1, H2 |
| **RDD** | Running variable, cutoff, bandwidth selection, McCrary test | Numbered H1, H2 |
| **IV** | First stage, exclusion restriction, instrument relevance | Numbered H1, H2 |
| **Matching** | Selection on observables, balance diagnostics | Numbered H1, H2 |
| **Conjoint/Survey** | Experimental design, randomization, AMCE definition | Numbered H1, H2 |
| **Process tracing** | Case selection, evidence types, alternative explanations | Propositions / expectations |
| **QCA** | Conditions, calibration, truth table | Sufficiency/necessity claims |
| **Formal theory** | Model setup, equilibrium concept, comparative statics | Predictions from propositions |
| **Descriptive** | Measurement strategy, data sources | Research questions (RQ1, RQ2) |
| **Text-as-data** | Corpus description, preprocessing, validation | Numbered H1, H2 or RQs |

---

## Integration Points

| Component | Connection |
|---|---|
| **`manuscript-conventions.md`** | Source of all structural rules |
| **`/draft-section`** | Consumes the plan and skeleton files this skill creates |
| **`/submission-checklist`** | Final gate after all sections are drafted |
| **`/reviewer-2`** | Run on design section to check methodology |
| **Orchestrator** | If called from a plan, orchestrator manages the creation loop |
