# CLAUDE.MD — Political Science Research Paper Workflow

**Project:** [YOUR PROJECT NAME]
**Institution:** [YOUR INSTITUTION]
**Working Branch:** main

---

## Quick Reference: Available Skills & Agents

| Command | What It Does |
|---------|-------------|
| `/create-paper [topic]` | End-to-end manuscript orchestrator: outline, draft, review, submit |
| `/paper-outline [topic]` | Manuscript skeleton: folder structure, section outline, word budget |
| `/draft-section [section]` | Draft a manuscript section with citation verification and voice audit |
| `/reviewer-2` | Research design devil's advocate: identification, estimator, robustness |
| `/submission-checklist [paper]` | Pre-submission quality gate: completeness, formatting, anonymization |
| `/prep-data [task]` | Data processing: download, standardize codes, merge panels, validate |
| `/review-r [file]` | R code review: quality, reproducibility, correctness |
| `/validate-bib` | Cross-reference citations vs bibliography file |
| `/proofread [filename]` | Grammar/typo/overflow review and report |
| `/commit [message]` | Stage, commit, create PR, and merge to main |

**Agents:** `proofreader`, `methodology-reviewer`, `domain-reviewer`, `r-reviewer`, `polisci-data-engineer`, `verifier`

**Required Installed Skills** (external — not included):

| Installed Skill | Used By | Purpose |
|----------------|---------|---------|
| `scientific-writing` | `/draft-section` | IMRAD structure, flowing prose |
| `citation-management` | `/draft-section`, `/validate-bib` | Google Scholar/PubMed search, BibTeX |
| `humanizer` | `/draft-section` | Remove AI writing patterns |

---

## Project Overview

This is a standalone workflow template for writing political science research papers with Claude Code. It covers the full lifecycle:

1. **Outline** — structure, word budget, hypothesis stubs
2. **Data processing** — download, clean, merge datasets
3. **Drafting** — section-by-section with citation verification
4. **Review** — hostile methodology review, proofreading
5. **Submission** — 60+ automated checks, anonymization, replication package

Copy this folder to start a new paper project. All skills, agents, and rules are self-contained.

---

## Folder Structure

```
[your-paper]/
├── CLAUDE.md                          # This file
├── .claude/                           # Claude Code configuration
│   ├── settings.json                  # Project permissions + hooks
│   ├── rules/                         # Domain-specific rules (auto-loaded)
│   ├── skills/                        # Slash commands
│   └── agents/                        # Specialized agents
├── Bibliography_base.bib              # Centralized bibliography
├── Manuscripts/                       # Research papers
│   └── example_paper/
│       ├── main.tex                   # Authoritative manuscript source
│       ├── main_anonymous.tex         # Blinded version for review
│       ├── appendix.tex               # Online appendix
│       ├── cover_letter.tex           # Journal cover letter
│       ├── figures/                   # Paper-specific figures
│       ├── tables/                    # Generated .tex table fragments
│       └── submission/                # Final submission package
├── Replication/                       # Replication packages
│   ├── code/                          # Numbered scripts (00_master, 01_clean, etc.)
│   ├── data/                          # Raw and processed data
│   └── output/                        # Generated tables, figures
├── master_supporting_docs/            # Supporting materials
│   └── supporting_papers/             # Academic papers for literature review
├── quality_reports/                   # Review agent reports
│   ├── plans/                         # Saved implementation plans
│   └── session_logs/                  # Session history
├── scripts/                           # Utility scripts
│   └── log-reminder.py               # Session log reminder hook
└── PROJECT_MEMORY.md                  # Learned corrections
```

---

## Working Philosophy

### Plan-First Approach

For any non-trivial task, Claude enters **plan mode first**:
1. Draft an approach, list files to modify
2. Save the plan to `quality_reports/plans/`
3. Wait for your approval
4. Implement via the orchestrator protocol

### Continuous Learning

Tag corrections with `[LEARN:category]` — they are appended to `PROJECT_MEMORY.md` and persist across sessions.

### Quality Gates

| Threshold | When | What It Means |
|-----------|------|--------------|
| **80/100** | Commit | Good enough to save progress |
| **90/100** | PR | High quality, ready for deployment |

---

## Manuscript Workflow

```
/create-paper "Your Paper Title" --journal APSR --design DID
  |
  Phase 1: OUTLINE        <- /paper-outline
  Phase 2: INPUTS         <- you provide papers, R output
  Phase 3: DRAFT          <- /draft-section (per section)
  Phase 4: REVIEW         <- /reviewer-2 + proofreader
  Phase 5: POLISH         <- anonymization, formatting
  Phase 6: SUBMISSION     <- /submission-checklist
```

---

## Data Processing

```
/prep-data "merge V-Dem and WDI for country-year panel 1990-2023"
```

Key principles:
- Never merge by country name — use standardized codes (COW, ISO-3)
- Diagnostics after every merge
- Recode before merge (Polity special codes, WDI aggregates)
- Document everything in codebook

---

## Session Startup

```
Claude, please:
1. Read CLAUDE.MD
2. Check recent git commits
3. Read PROJECT_MEMORY.md
4. Check quality_reports/plans/ for in-progress plans
5. State what you understand our goals to be
```

---

## Getting Started

1. Rename the `example_paper/` folder to your paper's short name
2. Update this CLAUDE.md with your project details
3. Upload supporting papers to `master_supporting_docs/supporting_papers/`
4. Run `/paper-outline "your topic" --journal [target]` to begin
