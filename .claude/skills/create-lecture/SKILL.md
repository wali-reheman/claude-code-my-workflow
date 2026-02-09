---
name: create-lecture
description: Create a new Beamer lecture from papers, existing slides, R scripts, and other materials. Guides the content creation process with notation consistency, pedagogical patterns, and collaborative iteration.
argument-hint: "[Topic name, e.g., 'Synthetic Control' or 'Regression Discontinuity']"
---

# Lecture Creation Workflow

Create a beautiful, pedagogically excellent Beamer lecture deck.

**This is a collaborative, iterative process. The instructor drives the vision; Claude is a thinking partner.**

---

## CONSTRAINTS (Non-Negotiable)

1. **Read the knowledge base FIRST** — notation registry, narrative arc, applications database
2. Every new symbol MUST be checked against the notation registry
3. Motivation before formalism — no exceptions
4. Worked example within 2 slides of every definition
5. Max 2 colored boxes per slide
6. No `\pause` or overlay commands (check project rules)
7. Transition slides at major conceptual pivots
8. Thread at least 1 running empirical application throughout
9. All citations verified against the bibliography
10. **Work in batches of 5-10 slides** — share for feedback, don't bulk-dump

---

## WORKFLOW

### Phase 0: Intake & Context
- Read knowledge base and creation guide
- Inventory provided materials (papers, slides, code)
- Read previous lecture's structure and ending
- State pedagogical goal, get user confirmation

### Phase 1: Paper Analysis (When Papers Provided)
- Split into chunks, extract key ideas
- Map paper notation → course notation
- Identify slide-worthy content
- Present summary for approval

### Phase 2: Structure Proposal
- Propose outline (5-Act or 3-Part template)
- List TikZ diagrams and R figures needed
- List new notation to introduce
- **GATE: User approves before Phase 3**

### Phase 3: Draft Slides (Iterative)
- Work in batches of 5-10 slides
- Check notation, apply creation patterns
- Quality checks during drafting

### Phase 4: Figures & Code
- R scripts following conventions
- TikZ diagrams in Beamer source (single source of truth)
- Save RDS for future Quarto integration

### Phase 5: Polish & Review

**5a. Compile & Verify**
- Full 3-pass XeLaTeX compilation
- Run verifier agent: compilation check, overfull hbox count, citation resolution

**5b. Automated Review (parallel agents)**

Run these review agents in parallel — they are the same agents the orchestrator dispatches for `.tex` slide files:

| Agent | What It Checks |
|-------|---------------|
| `proofreader` | Grammar, typos, consistency, academic quality |
| `slide-auditor` | Overflow, font sizes, box fatigue, spacing |
| `pedagogy-reviewer` | Narrative arc, notation clarity, pacing |
| `tikz-reviewer` | TikZ diagram quality (if TikZ present) |
| `domain-reviewer` | Substantive correctness (if configured) |

**5c. Fix Round**
- Apply fixes from reviews: Critical → Major → Minor
- Re-compile to confirm fixes are clean
- Score against quality-gates rubric (`.claude/rules/quality-gates.md`)

**5d. Final Polish**
- Run Devil's Advocate (`/devils-advocate`) for pedagogical challenge
- Update knowledge base with new notation
- Update session log

**Note:** The orchestrator protocol governs the review-fix loop. If `/create-lecture` is invoked via the orchestrator (e.g., as part of a plan), the full verify → review → fix → score loop runs automatically. If invoked standalone, Phase 5b-5c runs once (no looping) and presents results.

---

## Post-Creation Checklist

```
[ ] Lecture compiles without errors
[ ] No overfull hbox > 10pt
[ ] All citations resolve
[ ] Every definition has motivation + worked example
[ ] Max 2 colored boxes per slide
[ ] 2-3 Socratic questions embedded
[ ] Transition slides between sections
[ ] At least 1 running application threaded throughout
[ ] New notation added to knowledge base
[ ] Session log updated
[ ] Review agents run (proofreader, slide-auditor, pedagogy-reviewer)
[ ] Quality score >= 80 (commit threshold)
```
