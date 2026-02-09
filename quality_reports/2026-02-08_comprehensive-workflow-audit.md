# Comprehensive Workflow Audit Report

**Date:** 2026-02-08
**Scope:** 20 skills, 12 agents, 16 rules, CLAUDE.md, cross-component integration
**Methodology:** 4 parallel audit agents (skills, agents, rules, integration)

---

## Executive Summary

**Overall assessment: Strong foundation with specific gaps in manuscript/data workflows.**

The slide-focused infrastructure (Beamer, Quarto, TikZ, R figures) is mature and well-integrated. The recently added manuscript infrastructure (`/create-paper`, `/reviewer-2`, `/draft-section`, `/prep-data`) is comprehensive but not yet fully wired into the existing quality/verification/scoring systems. The data processing pipeline is thorough but the `polisci-data-engineer` agent has a frontmatter issue.

**By the numbers:**
- 5 Critical issues (require fixes)
- 8 Major issues (should fix)
- 10 Minor issues (polish when convenient)

---

## CRITICAL ISSUES (5)

### C1: No manuscript scoring rubric in quality-gates.md
**Location:** `.claude/rules/quality-gates.md`
**Problem:** Quality gates define scoring for Quarto slides, Beamer slides, and R scripts — but NOT for manuscripts (`.tex` in `Manuscripts/`). The orchestrator loop scores against quality-gates, so manuscripts go through the loop with no rubric to score against.
**Impact:** `/create-paper` Phase 4 (REVIEW) cannot produce a meaningful quality score. The orchestrator has no threshold to compare against.
**Fix:** Add a `## Manuscripts (.tex files)` section with Critical/Major/Minor deduction tables. Also add `Manuscripts/**/*.tex` to the `paths:` frontmatter.

### C2: No manuscript verification procedures
**Location:** `.claude/rules/verification-protocol.md` + `.claude/agents/verifier.md`
**Problem:** Verification protocol covers Quarto, Beamer slides, R scripts, TikZ, and deployment — but has NO section for manuscripts. The verifier agent similarly lacks manuscript procedures.
**Impact:** Orchestrator Step 2 (VERIFY) and Step 5 (RE-VERIFY) have nothing to run for manuscripts.
**Fix:** Add `## For Manuscripts (.tex in Manuscripts/)` section covering: xelatex compilation, bibtex pass, word count check, anonymization verification (for blinded versions), table/figure reference integrity. Also add `Manuscripts/**` to both files' `paths:`.

### C3: polisci-data-engineer agent has wrong frontmatter
**Location:** `.claude/agents/polisci-data-engineer.md` lines 4-7
**Problem:** Has `paths:` instead of `tools:` and `model:` fields. Agent frontmatter should have `name`, `description`, `tools`, and optionally `model`. The `paths:` field is for rules, not agents.
**Impact:** Agent may not function correctly when dispatched by the orchestrator. Claude Code may not know what tools this agent can use.
**Fix:** Replace `paths:` with `tools: Read, Grep, Glob` and add `model: inherit` (or `sonnet`). The `paths:` concept doesn't apply to agents — they're dispatched explicitly, not auto-loaded.

### C4: Proofreader scoped to "lecture slides" only
**Location:** `.claude/agents/proofreader.md` line 3 + line 8
**Problem:** Description says "academic lecture slides" and instructions say "for academic lecture slides." But the orchestrator dispatches proofreader for manuscripts too (orchestrator-protocol.md agent selection table, row for `.tex (Manuscripts)`).
**Impact:** When proofreading manuscripts, the agent applies slide-specific checks (overflow, box fatigue) instead of manuscript-specific checks (section transitions, paragraph flow, academic voice).
**Fix:** Extend the proofreader to handle manuscripts: add a `### For Manuscripts (.tex)` section with manuscript-specific checks (paragraph coherence, section transitions, formal academic tone, consistent terminology, abstract quality). Or create a separate `manuscript-proofreader` agent.

### C5: Inconsistent severity scales across agents
**Location:** Multiple agents
**Problem:** Two severity systems coexist:
  - **proofreader, slide-auditor:** `High / Medium / Low`
  - **polisci-data-engineer, methodology-reviewer, domain-reviewer, r-reviewer:** `Critical / Major / Minor`
**Impact:** The orchestrator Step 4 (FIX) prioritizes by `Critical → Major → Minor`. When proofreader/slide-auditor return `High/Medium/Low`, the orchestrator can't consistently triage.
**Fix:** Standardize all agents to `Critical / Major / Minor`. Update proofreader and slide-auditor report format sections.

---

## MAJOR ISSUES (8)

### M1: `/create-paper` loop limit override not formalized
**Location:** `/create-paper` SKILL.md lines ~257, ~479 vs `orchestrator-protocol.md` line 90
**Problem:** `/create-paper` specifies max 3 review-fix rounds, but the orchestrator default is 5. The skill states this as an "intentional override" but the orchestrator has no formal mechanism for skill-specific overrides.
**Impact:** Ambiguity about which limit applies. Future skills may also need overrides.
**Fix:** Add a "Skill-Specific Overrides" section to `orchestrator-protocol.md` documenting that skills can set `max_review_rounds` and the orchestrator respects it.

### M2: `/create-lecture` doesn't chain downstream skills
**Location:** `.claude/skills/create-lecture/SKILL.md`
**Problem:** Unlike `/create-paper` (which chains `/paper-outline` → `/draft-section` → `/reviewer-2` → `/submission-checklist`), `/create-lecture` doesn't invoke `/proofread`, `/visual-audit`, or `/pedagogy-review` as sub-steps. It has its own ad-hoc review process.
**Impact:** `/create-lecture` outputs don't get the same systematic quality assurance as `/create-paper`.
**Fix:** Update `/create-lecture` to invoke review skills in its quality assurance phase, or at minimum document that the orchestrator handles review via agent dispatch.

### M3: Missing installed skills documentation
**Location:** `/draft-section` SKILL.md references `scientific-writing`, `citation-management`, `humanizer`
**Problem:** These are MCP-installed skills (external), not local files. If a user clones this template without those skills installed, `/draft-section` will fail at steps that invoke them.
**Impact:** Template portability — new users won't know they need these installed skills.
**Fix:** Add a "Required Installed Skills" section to CLAUDE.md listing external dependencies and installation instructions. Add graceful degradation to `/draft-section` (check if skill exists before invoking; if not, do the work directly).

### M4: `r-code-conventions.md` has overly broad paths
**Location:** `.claude/rules/r-code-conventions.md` line 3
**Problem:** `paths: ["**/*.R"]` matches ANY `.R` file in the entire repo, including inside `master_supporting_docs/` or `node_modules/` (if they existed). The other two paths (`Figures/**/*.R`, `scripts/**/*.R`) are redundant because `**/*.R` already covers them.
**Impact:** Rule may load unnecessarily for R files that aren't part of the project's code.
**Fix:** Replace with specific paths: `scripts/**/*.R`, `Figures/**/*.R`, `Replication/**/*.R`.

### M5: No integration between verification-protocol and quality-gates
**Location:** `verification-protocol.md` and `quality-gates.md`
**Problem:** Verification checks pass/fail (does it compile?). Quality gates assign scores (how good is it?). But neither references the other. The orchestrator runs them in sequence (Step 2 VERIFY, Step 6 SCORE) but the documents don't cross-reference.
**Impact:** Users reading either document don't see the full picture.
**Fix:** Add cross-references: verification-protocol should note "After verification passes, quality-gates scoring applies." Quality-gates should note "Scoring assumes verification has passed (compilation success is a prerequisite, not a scored item)."

### M6: `methodology-reviewer` agent missing `model:` field
**Location:** `.claude/agents/methodology-reviewer.md` frontmatter
**Problem:** Has `name`, `description`, `tools` — but no `model:` field. Other complex review agents specify `model: opus` or `model: sonnet`.
**Impact:** Will inherit the default model, which may not be ideal for deep research design review.
**Fix:** Add `model: sonnet` (or `opus` for thorough review). Also affects `domain-reviewer.md` and `pedagogy-reviewer.md` which are missing `model:` too.

### M7: `quality-gates.md` paths don't include manuscripts or data
**Location:** `.claude/rules/quality-gates.md` frontmatter
**Problem:** `paths:` only includes `Slides/**/*.tex`, `Quarto/**/*.qmd`, `scripts/**/*.R`. Missing: `Manuscripts/**`, `Replication/**`, `data/**`.
**Impact:** Quality gates rule won't auto-load when working on manuscripts or data processing.
**Fix:** Add `Manuscripts/**/*.tex`, `Replication/**/*.R`, `Replication/data/**` to paths.

### M8: Session log template not provided
**Location:** `plan-first-workflow.md` Rule 5
**Problem:** Rule 5 describes 3 logging behaviors (post-plan, incremental, end-of-session) but provides no template file. Users/Claude must invent the format each time.
**Impact:** Inconsistent session logs across sessions.
**Fix:** Create `quality_reports/session_logs/_template.md` with sections for Goal, Plan Summary, Key Decisions, Incremental Updates, End-of-Session Summary, Open Questions.

---

## MINOR ISSUES (10)

### m1: Beamer-Quarto sync mapping table is empty placeholder
**Location:** `.claude/rules/beamer-quarto-sync.md`
**Note:** This is a template repo — placeholder tables are expected. Add a comment saying "Populate this table with your custom environments."

### m2: Agent frontmatter inconsistency (model field)
**Agents missing `model:` field:** methodology-reviewer, domain-reviewer, pedagogy-reviewer
**Agents with `model: inherit`:** proofreader, slide-auditor, tikz-reviewer, verifier
**Agents with explicit model:** quarto-critic (opus), quarto-fixer (sonnet), r-reviewer (sonnet), beamer-translator (opus)
**Fix:** Add `model: inherit` to the 3 missing agents for consistency.

### m3: Cross-reference format inconsistency in rules
Some rules reference others as `.claude/rules/filename.md`, others just say "see filename.md". Standardize to full relative paths.

### m4: `r-code-conventions.md` redundant paths
As noted in M4, `Figures/**/*.R` and `scripts/**/*.R` are subsets of `**/*.R`. If keeping `**/*.R`, remove the redundant entries.

### m5: No git workflow rule
No rule documents branch naming, commit message conventions, or PR workflow. CLAUDE.md mentions "main" branch but conventions are informal.
**Suggestion:** Create `.claude/rules/git-conventions.md` if multi-author workflows are anticipated.

### m6: No figure quality standards for R/Python output
TikZ has `tikz-visual-quality.md`, but R-generated figures (ggplot2, plotly) only have scattered checks in `r-code-conventions.md`. No unified figure quality rule.
**Suggestion:** Create `.claude/rules/figure-quality.md` covering resolution, color palettes, label sizes, theme consistency.

### m7: Robustness checklists missing some methods
`robustness-checklists.md` covers 18 design types (Modules A-R) but lacks: mediation analysis, survival/duration models, spatial analysis, panel cointegration. These can be added as needed.

### m8: `knowledge-base-template.md` all empty
Expected for a template repo. Consider adding a comment at the top: "Fill in the tables below with your domain-specific knowledge."

### m9: CLAUDE.md Quick Reference table inconsistent with actual skills
CLAUDE.md lists 20 skills in the table but descriptions may not perfectly match SKILL.md `description:` fields. A periodic sync check would help.

### m10: No documentation for the quality_reports/ folder structure
`quality_reports/` has `plans/` and `session_logs/` subdirectories. Should also document that review agent reports go in the root of `quality_reports/`.

---

## AUDIT VERIFICATION

### False Positives Dismissed
- Rules audit flagged "20 skills missing" — **FALSE**: all 20 skills exist in `.claude/skills/`
- Rules audit flagged "MEMORY.md missing" — **FALSE**: `MEMORY.md` exists at repo root
- Rules audit flagged "`quality_score.py` missing" — **FALSE**: `scripts/quality_score.py` exists

### Confirmed Findings
All 5 Critical and 8 Major issues above were verified against actual file contents.

---

## RECOMMENDED PRIORITY ORDER

### Phase 1: Critical Fixes (do now)
1. **C3** — Fix `polisci-data-engineer` frontmatter (2 min)
2. **C5** — Standardize severity scales in proofreader + slide-auditor (10 min)
3. **C1** — Add manuscript scoring rubric to quality-gates.md (15 min)
4. **C2** — Add manuscript verification to verification-protocol.md + verifier agent (20 min)
5. **C4** — Extend proofreader for manuscripts (15 min)

### Phase 2: Major Improvements (do soon)
6. **M1** — Formalize skill-specific overrides in orchestrator (5 min)
7. **M4** — Fix r-code-conventions paths (2 min)
8. **M6** — Add missing model fields to agents (2 min)
9. **M7** — Extend quality-gates paths (2 min)
10. **M5** — Add cross-references between verification and quality-gates (5 min)
11. **M3** — Document installed skill dependencies (10 min)
12. **M8** — Create session log template (5 min)
13. **M2** — Update /create-lecture to chain skills (30 min)

### Phase 3: Polish (when convenient)
14. m1-m10 as time permits

---

## STATISTICS

| Component | Count | Critical | Major | Minor |
|-----------|-------|----------|-------|-------|
| Skills (20) | 0 | 1 (M3) | 1 (m9) | — |
| Agents (12) | 2 (C3, C4) | 1 (C5) | 2 (M6, m2) | — |
| Rules (16) | 2 (C1, C2) | 4 (M1, M4, M5, M7) | 5 (m1, m3, m4, m8, m10) | — |
| Integration | 1 (C5) | 2 (M2, M8) | 2 (m5, m6) | — |
| **Total** | **5** | **8** | **10** | — |
