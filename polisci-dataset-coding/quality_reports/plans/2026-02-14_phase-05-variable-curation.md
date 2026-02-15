# Plan: Phase 0.5 — Variable Curation Step for `/create-dataset`

**Date:** 2026-02-14
**Status:** DRAFT
**Task:** Add an optional Variable Curation step between the pre-coding interview (Step 0) and codebook design (Step 1) that transforms a large brainstormed variable list into a curated, prioritized, costed set.

---

## Context

The `/create-dataset` workflow currently jumps from "what is your concept?" (Step 0) directly to "let's design codebook entries" (Step 1). When a user arrives with a 160-variable brainstorm across 9 dimensions (like the secularization example in `variable_list_example.txt`), Step 1 would attempt to build full codebook entries for ALL of them — anchor examples, inclusion/exclusion criteria, scale justifications × 160 variables. That's absurd in cost and effort.

The gap: there is no structured step for curating a brainstorm into a codable set. Phase 0.5 fills this gap with four passes: dimension architecture review, variable-level triage, cost-benefit summary, and gap suggestions. It's optional — only triggered when the user provides a pre-existing variable list.

---

## Files to Modify (3 files)

### 1. `polisci-dataset-coding/.claude/skills/create-dataset/SKILL.md`

**Changes:**

- **Pipeline diagram (lines 78-127):** Insert Step 0.5 block (6 lines) between Step 0 and Step 1
- **New section:** `### Step 0.5: Variable Curation (Optional)` — insert between Step 0 GATE (line 212) and Step 1 (line 216). Contains:
  - Trigger condition (>15 variables or user request)
  - Edge cases (<15, >200, no dimension structure)
  - Pass 1: Dimension Architecture Review
  - Pass 2: Variable-Level Triage (one integrated table per dimension with 6 lenses: relevance, redundancy, coverage, temporal profile, codability, scale type)
  - Pass 3: Cost-Benefit Summary (tier counts + cell/cost projections)
  - Pass 4: Gap Suggestions (Claude-proposed additions)
  - Output: `curation_report.md` + `curated_variables.md`
  - GATE: User approves curated list
- **Step 0 Phase 0a (after line 139, Q2):** Add adaptive follow-up — check if user has a pre-existing variable brainstorm list
- **Step 0 GATE (line 212):** Add note about variable list location in interview summary
- **Step 0e Q16 (line 210):** Add range estimate note when N_variables is TBD pending curation
- **Step 1 item 1 (line 218):** Add conditional — if Phase 0.5 was run, build codebook ONLY for approved curated list; if not, generate from scratch as before

### 2. `polisci-dataset-coding/.claude/rules/dataset-construction-conventions.md`

**Changes:**

- **New Section 21: Variable Curation Standards** — insert after Section 20 (Evidence Source Hierarchy, ends line 1315) and before Integration Points (line 1317). Contains:
  - When curation applies (>15 variables, optional)
  - Tier definitions (Core / Recommended / Optional / Drop) with criteria and Step 1 implications
  - Six assessment lenses with detailed definitions
  - Flag variable rules
  - Cost estimation formula and per-cell cost ranges
  - Curation report format reference
  - 7 rules governing curation decisions
- **Integration Points table (line 1317-1328):** Add `curation_report.md` and `curated_variables.md` references
- **Paths frontmatter (lines 1-10):** Add `"Replication/data/coded/curation_report.md"` and `"Replication/data/coded/curated_variables.md"`

### 3. `polisci-dataset-coding/CLAUDE.md`

**Changes:**

- **Pipeline diagram (lines 170-199):** Insert Step 0.5 line between Step 0 (line 175) and Step 1 (line 176)
- **Folder structure (lines 71-106):** Add `curation_report.md` and `curated_variables.md` to `coded/` listing (after line 89, `interview_summary.md`)

---

## Key Design Decisions

1. **Phase 0.5 is OPTIONAL** — triggered when user provides a variable list with >15 variables, or explicitly requests curation. If user arrives with just a concept name, skip to Step 1.
2. **Pass 2 is ONE integrated pass per dimension**, not 6 separate passes. All lenses evaluated simultaneously.
3. **Scale type recommendations are coarse** (binary / ordinal 0-2 / ordinal 0-4 / flag / composite). Step 1 designs actual scale content.
4. **Pass 4 (Gap Suggestions)** adds variables Claude thinks are missing, clearly marked as `[Claude-proposed]`. Max 10-15.
5. **Every recommendation ties back to the research question** — no "this seems interesting" without connection to stated research design.
6. **Tier assignment**: Core (directly tests RQ + codable + unique), Recommended (supports RQ + codable + unique, OR core relevance but low codability), Optional (supporting + low codability or low coverage), Drop (tangential, redundant, or uncodable + low coverage).
7. **Output saved to disk**: `curation_report.md` (full analysis) + `curated_variables.md` (clean approved list for Step 1).
8. **No changes to production-protocol.md** — curation is design-time only.

---

## Implementation Order

1. **Conventions Section 21** — reference document (conventions before SKILL.md so the skill can reference it)
2. **Conventions frontmatter + Integration Points** — update references
3. **SKILL.md Phase 0.5 section** — the main content
4. **SKILL.md pipeline diagram** — update
5. **SKILL.md cross-references** — Step 0 follow-up, Step 0 GATE, Step 0e estimate, Step 1 conditional
6. **CLAUDE.md pipeline + folder structure** — update

---

## Verification

- [ ] SKILL.md pipeline diagram shows Step 0.5 between Step 0 and Step 1
- [ ] Phase 0.5 section includes all 4 passes with output templates
- [ ] Trigger condition is clear (>15 variables or explicit request)
- [ ] Edge cases handled (<15, >200, no dimension structure, user says "skip curation")
- [ ] Step 0 Phase 0a has adaptive follow-up about variable list
- [ ] Step 0 GATE mentions variable list in interview summary
- [ ] Step 1 has conditional for curated vs from-scratch variable generation
- [ ] Conventions Section 21 defines tier criteria, 6 lenses, flag variable rules, cost formula
- [ ] Integration Points table includes new output files
- [ ] Conventions paths frontmatter includes curation artifacts
- [ ] CLAUDE.md pipeline shows Step 0.5
- [ ] CLAUDE.md folder structure lists curation_report.md and curated_variables.md
- [ ] No changes to production-protocol.md (confirmed: not needed)
- [ ] Question numbering unaffected (Phase 0.5 uses Pass 1-4, not Q17+)
