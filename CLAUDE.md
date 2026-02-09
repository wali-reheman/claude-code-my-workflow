# CLAUDE.MD — Academic Project Development with Claude Code

<!-- ============================================================
     HOW TO USE THIS TEMPLATE:
     1. Replace all [BRACKETED PLACEHOLDERS] with your project info
     2. Delete sections that don't apply to your project
     3. Add domain-specific sections as needed
     4. This file is read by Claude at the start of every session
     ============================================================ -->

**Last Updated:** [DATE]
**Project:** [YOUR PROJECT NAME] (e.g., "Econ 730 — Causal Panel Data")
**Institution:** [YOUR INSTITUTION]
**Working Branch:** main

---

## Quick Reference: Available Skills & Agents

| Command | What It Does |
|---------|-------------|
| `/compile-latex [filename]` | 3-pass XeLaTeX compilation with bibtex |
| `/deploy [LectureN]` | Render Quarto slides and sync to GitHub Pages |
| `/extract-tikz [LectureN]` | TikZ diagrams to PDF to SVG with 0-based indexing |
| `/proofread [filename]` | Grammar/typo/overflow review and report |
| `/visual-audit [filename]` | Slide layout audit for overflow and consistency |
| `/pedagogy-review [filename]` | PhD-student lens: narrative, notation, pacing review |
| `/review-r [file or LectureN]` | R code review: quality, reproducibility, correctness |
| `/qa-quarto [LectureN]` | Adversarial Quarto vs Beamer QA: critic finds issues, fixer resolves |
| `/slide-excellence [filename]` | Combined visual + pedagogical + proofreading review |
| `/translate-to-quarto [filename]` | Full Beamer to Quarto translation workflow |
| `/validate-bib` | Cross-reference citations vs bibliography file |
| `/devils-advocate` | Challenge slide design with pedagogical questions |
| `/reviewer-2` | Research design devil's advocate: identification, estimator, robustness, transparency |
| `/paper-outline [topic]` | Manuscript skeleton: folder structure, section outline, word budget, hypothesis stubs |
| `/draft-section [section]` | Draft a manuscript section with citation verification, voice audit, word budget |
| `/submission-checklist [paper]` | Pre-submission quality gate: completeness, formatting, anonymization, replication |
| `/create-paper [topic]` | End-to-end manuscript orchestrator: outline → draft → review → submit |
| `/prep-data [task]` | Data processing: download, standardize codes, merge panels, validate joins, document |
| `/create-lecture` | Full lecture creation workflow |
| `/commit [message]` | Stage, commit, create PR, and merge to main |

**Agents** (available for delegation): `proofreader`, `slide-auditor`, `pedagogy-reviewer`, `r-reviewer`, `tikz-reviewer`, `beamer-translator`, `quarto-critic`, `quarto-fixer`, `verifier`, `domain-reviewer`, `methodology-reviewer`, `polisci-data-engineer`

**Rules** (auto-loaded): See `.claude/rules/` for domain-specific rules on LaTeX, Quarto, R, verification, proofreading, quality gates, robustness checklists, manuscript conventions, and panel data conventions.

**Required Installed Skills** (external — not included in this template):

Some skills chain external MCP-installed skills for enhanced functionality. The workflow degrades gracefully if these are absent — Claude will perform the work directly instead of delegating — but for best results, install them:

| Installed Skill | Used By | Purpose |
|----------------|---------|---------|
| `scientific-writing` | `/draft-section` | IMRAD structure, reporting guidelines, flowing prose |
| `citation-management` | `/draft-section`, `/validate-bib` | Google Scholar/PubMed search, BibTeX generation |
| `humanizer` | `/draft-section` | Remove AI-generated writing patterns |
| `statistical-analysis` | `/reviewer-2` (optional) | Power analysis, assumption checks |
| `scientific-critical-thinking` | `/reviewer-2` (optional) | Bias assessment, evidence quality |
| `peer-review` | `/reviewer-2` (optional) | Broader manuscript evaluation |

To check which are installed, run: `/` then look at the autocomplete list.

---

## Project Overview

<!-- Describe your project in 2-3 paragraphs. What is it? Who is it for? -->

[DESCRIBE YOUR PROJECT HERE]

This repository is designed for multi-platform collaboration using:
- **GitHub** for version control and cross-computer synchronization
- **Overleaf** (optional) for LaTeX editing and compilation
- **Claude Code** for slide development, content creation, and research assistance

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.MD                          # This file — Claude's guide
├── .claude/                           # Claude Code configuration
│   ├── settings.json                  # Project permissions + hooks
│   ├── rules/                         # Domain-specific rules (auto-loaded)
│   ├── skills/                        # Slash commands (/deploy, /proofread, etc.)
│   └── agents/                        # Specialized agents (proofreader, verifier, etc.)
├── Bibliography_base.bib              # Centralized bibliography
├── Figures/                           # Course figures and images
├── Preambles/                         # LaTeX headers and style files
│   └── header.tex
├── Slides/                            # LaTeX/Beamer lecture slides
│   ├── Lecture01_Topic.tex
│   └── ...
├── Quarto/                            # Quarto/RevealJS slides
│   ├── Lecture1_Topic.qmd
│   └── your-theme.scss               # Custom theme
├── docs/                              # GitHub Pages deployment (auto-generated)
│   ├── index.html
│   └── slides/
├── Manuscripts/                       # Research papers for publication
│   └── paper_name/                    # One folder per paper
│       ├── main.tex                   # Authoritative manuscript source
│       ├── main_anonymous.tex         # Blinded version for review
│       ├── appendix.tex               # Online appendix
│       ├── cover_letter.tex           # Journal cover letter
│       ├── response_to_reviewers.tex  # R&R response (when needed)
│       ├── figures/                   # Paper-specific figures
│       ├── tables/                    # Generated .tex table fragments
│       └── submission/                # Final submission package
├── Replication/                       # Replication packages for papers
│   ├── README.md                      # Software versions, data sources, run order
│   ├── data/                          # Raw and processed data
│   ├── code/                          # Numbered scripts (00_master, 01_clean, etc.)
│   └── output/                        # Generated tables, figures, logs
├── scripts/                           # Utility scripts
│   ├── sync_to_docs.sh               # Renders Quarto & syncs to docs/
│   └── R/                             # R scripts for figures and analysis
├── quality_reports/                    # Review agent reports (auto-generated)
│   ├── plans/                         # Saved implementation plans
│   └── session_logs/                  # Session history and decision logs
└── master_supporting_docs/            # Supporting materials
    ├── supporting_papers/             # Academic papers (auto-split into chunks)
    └── supporting_slides/             # Existing slides to upgrade
```

---

## Working Philosophy

### Collaborative Partnership Approach

Claude serves as your **collaborative partner**, not a fully autonomous agent:

- **You drive the vision** — provide papers, concepts, and aesthetic preferences
- **Claude proposes designs** — creates slide structures and content arrangements
- **You iterate together** — refine until excellent
- **You maintain control** — final decisions always rest with you

### Communication Style

- **Devil's advocate mode** — challenge assumptions and explore alternative presentations
- **Reference validation** — every citation and claim verified for accuracy
- **Aesthetic excellence** — all slides should be visually compelling
- **Understanding > speed** — getting it right matters more than getting it fast

### Plan-First Approach

For any non-trivial task, Claude enters **plan mode first** before writing code:

1. **Plan** — draft an approach, list files to modify, identify risks
2. **Save** — write the plan to `quality_reports/plans/` so it survives context compression
3. **Review** — present the plan and wait for your approval
4. **Implement** — only then begin making changes

See `.claude/rules/plan-first-workflow.md` for the full protocol.

> **Never use `/clear`.** Rely on auto-compression to manage long conversations. `/clear` destroys all context; auto-compression preserves what matters.

### Contractor Mode (Orchestrator)

After a plan is approved, Claude operates in **contractor mode**: implement, verify, review with agents, fix issues, and re-verify — all autonomously. The user sees a summary when the work meets quality standards or review rounds are exhausted. See `.claude/rules/orchestrator-protocol.md`.

When you say "just do it", the orchestrator skips the final approval pause and auto-commits if the score is 80+.

### Continuous Learning with [LEARN] Tags

When Claude makes a mistake or you correct a misconception, tag the correction:

```
[LEARN:notation] T_t = 1{t=2} is deterministic → use T_i ∈ {1,2}
[LEARN:citation] Post-LASSO is Belloni (2013), NOT Belloni (2014)
[LEARN:r-code] Package X: ALWAYS include intercept in design matrix
```

These corrections persist in `MEMORY.md` across sessions and prevent the same mistake from recurring.

---

## CRITICAL: Single Source of Truth Principle

**NEVER duplicate content. Always extract from the original source.**

When content exists in multiple formats (e.g., Beamer PDF and Quarto HTML), there must be ONE authoritative source that all other versions derive from.

| Content Type | Source of Truth | Derived From |
|--------------|-----------------|--------------|
| Slide content | Beamer `.tex` file | Quarto `.qmd` derived from it |
| TikZ diagrams | Beamer `.tex` file | extract_tikz.tex, SVG, docs/ |
| Bibliography | `Bibliography_base.bib` | All `.tex` files reference it |
| Figures/images | `Figures/` directory | `docs/Figures/` via sync script |
| Manuscript content | `Manuscripts/paper_name/main.tex` | `main_anonymous.tex`, appendix, submission package |
| Replication data | `Replication/data/raw/` | `Replication/data/processed/` via numbered scripts |
| Tables/figures (papers) | R scripts in `Replication/code/` | `.tex` fragments in `Manuscripts/paper_name/tables/` |

> **Modify the original source, then regenerate all derived versions automatically.**

---

## Slide Development Workflow

### 1. Input Stage
Provide one or more of:
- Academic papers (upload to `master_supporting_docs/supporting_papers/`)
- Topic descriptions or learning objectives
- Existing slides to upgrade (`master_supporting_docs/supporting_slides/`)

### 2. Design Stage
Claude will:
- Analyze the material thoroughly
- Validate all references and claims
- Propose slide structure
- Play devil's advocate on structure
- Await your feedback

### 3. Iteration Stage
Collaborate to:
- Refine content organization
- Enhance visual aesthetics
- Improve pedagogical flow
- Validate technical accuracy

### 4. Output Stage
Final deliverables:
- **Beamer slides** (`.tex`) with polished design
- **Quarto slides** (`.qmd`) for web deployment (optional)
- Supporting R scripts and figures

---

## Manuscript Development Workflow

Use `/create-paper [topic]` for end-to-end orchestration, or individual skills for specific steps.

### 1. Outline Stage (`/paper-outline`)
- Define research question, hypotheses, and contribution
- Generate folder structure (`Manuscripts/paper_name/`)
- Produce section outline with word budgets
- Identify key citations and datasets needed

### 2. Data & Analysis Stage (`/prep-data`)
- Download and clean datasets (V-Dem, WDI, Polity, ACLED, etc.)
- Merge panels with full diagnostics (match rates, unmatched cases)
- Construct variables and generate numbered scripts (`01_`-`04_`)
- Document everything in `data/codebook.md`

### 3. Drafting Stage (`/draft-section`)
- Draft sections one at a time with citation verification
- Voice audit: remove AI patterns, enforce academic register
- Track word budget (actual vs target per section)
- Each section verified against R code and data

### 4. Review Stage (`/reviewer-2`)
- Auto-detect research design (DID, RDD, IV, conjoint, process tracing, etc.)
- Run 4 universal lenses + design-specific robustness checklist
- Produce "3 Most Devastating Questions" report
- Verdict: ACCEPT / MINOR / MAJOR / REJECT

### 5. Submission Stage (`/submission-checklist`)
- Completeness check (all sections, figures, tables present)
- Formatting for target journal
- Anonymization verification (blinded version)
- Replication package validation
- Final submission package assembly

---

## Data Processing Workflow

Use `/prep-data [task]` for guided data work, or `/prep-data --audit` to review existing scripts.

### Supported Datasets
V-Dem, Polity V, World Bank WDI, ACLED, UCDP-GED, Afrobarometer, WVS, COW, Gleditsch-Ward, and 20+ others. See `.claude/rules/panel-data-conventions.md` for the full reference.

### Key Principles
1. **Never merge by country name** — always use standardized country codes (COW, ISO-3, or GW)
2. **Diagnostics after every merge** — match rate, unmatched cases, row count validation
3. **Recode before merge** — Polity special codes (-66, -77, -88), V-Dem variable selection, WDI aggregate filtering
4. **Zero is data, NA is missing** — event datasets must create zero-event country-years explicitly
5. **Document everything** — codebook with sources, download dates, variable definitions, cleaning decisions

### Script Naming Convention
```
Replication/code/
├── 00_master.R           # Runs all scripts in order
├── 01_download.R         # Fetch raw data
├── 02_clean_[dataset].R  # One per data source
├── 03_merge.R            # Combine panels with diagnostics
├── 04_construct.R        # Create analysis variables
├── 05_analysis.R         # Estimation (not data processing)
└── 06_figures.R          # Generate tables and figures
```

---

## Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** A Stop hook enforces this automatically.

See `.claude/rules/verification-protocol.md` for the full checklist.

**Quick summary:**
- **Quarto:** Run `./scripts/sync_to_docs.sh LectureN`, verify HTML renders
- **LaTeX:** Compile with xelatex (3 passes), check for overfull hbox
- **Manuscripts:** 3-pass xelatex + bibtex, check undefined citations/references, word count, anonymization
- **Data processing:** Run scripts in order, check merge diagnostics, verify panel dimensions
- **TikZ to SVG:** Use `pdf2svg` with **0-based indexing**
- **Always** use `sync_to_docs.sh` instead of manual copying

---

## Quality Gates

| Threshold | When | What It Means |
|-----------|------|--------------|
| **80/100** | Commit | Good enough to save progress |
| **90/100** | PR | High quality, ready for deployment |
| **95/100** | Excellence | Aspirational target |

Rubrics exist for: Quarto slides, Beamer slides, R scripts, manuscripts, and data processing scripts. See `.claude/rules/quality-gates.md` for full scoring tables.

---

## Design Principles

### Visual Excellence
- Clean, uncluttered layouts
- Strategic use of whitespace
- Consistent color schemes
- High-quality figures and diagrams
- Professional typography

### Pedagogical Clarity
- One key idea per slide
- Progressive revelation of complex concepts
- Visual metaphors and intuitive diagrams
- Smooth narrative flow between slides

### Technical Rigor
- All references validated and accurate
- Mathematical notation consistent and precise
- Code examples tested and functional
- Citations properly formatted in BibTeX

---

<!-- ============================================================
     CUSTOMIZE: Add your Beamer environments and CSS classes below
     ============================================================ -->

## Beamer Custom Environments

<!-- List your custom LaTeX environments here. Example: -->

| Environment | Effect | Use Case |
|-------------|--------|----------|
| `keybox` | Gold background box | Key points |
| `highlightbox` | Gold left-accent box | Highlights |
| `methodbox` | Blue left-accent box | Technical methods |
| `definitionbox[Title]` | Blue-bordered titled box | Formal definitions |

<!-- Add more as you build your theme -->

## Quarto CSS Classes

<!-- List your custom CSS classes here. Example: -->

| Class | Effect | Use Case |
|-------|--------|----------|
| `.smaller` | 85% font | Dense content slides |
| `.positive` | Green bold | Good annotations |
| `.negative` | Red bold | Problematic annotations |

---

## Technical Notes

### LaTeX Compilation

**Always compile with XeLaTeX, not pdflatex:**

```bash
cd Slides
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode filename.tex
BIBINPUTS=..:$BIBINPUTS bibtex filename
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode filename.tex
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode filename.tex
```

### Deploying Quarto Slides

```bash
./scripts/sync_to_docs.sh              # All lectures
./scripts/sync_to_docs.sh Lecture2     # Specific lecture
```

### Git Workflow

- Main branch: `main`
- Commit regularly with descriptive messages
- Use PRs for significant changes
- Run proofreading before every PR

---

## Session Startup Ritual

Start each session with:

```
Claude, please:
1. Read CLAUDE.MD to understand our workflow
2. Check recent git commits to see what changed
3. Check MEMORY.md for learned corrections from past sessions
4. Check quality_reports/plans/ for any in-progress plans
5. Check quality_reports/session_logs/ for the most recent session log
6. Look at the lecture/slides we're working on
7. State what you understand our goals to be
```

### Session End Protocol

Before ending a session:
1. Save a session log to `quality_reports/session_logs/YYYY-MM-DD_description.md`
2. Commit significant changes with descriptive messages
3. Update CLAUDE.MD if workflow changed
4. Note any unresolved questions in the session log

---

## Current Project State

<!-- Update these tables as you develop your project -->

### Lectures

| Lecture | Beamer | Quarto | Key Content |
|---------|--------|--------|-------------|
| 1: [Topic] | `Lecture01_Topic.tex` | `Lecture1_Topic.qmd` | [Brief description] |
| 2: [Topic] | `Lecture02_Topic.tex` | — | [Brief description] |

### Manuscripts

| Paper | Status | Location | Target Journal |
|-------|--------|----------|---------------|
| [Paper title] | [Draft / Under review / R&R / Accepted] | `Manuscripts/paper_name/` | [Journal name] |

### Replication Packages

| Paper | Scripts | Data Sources | Status |
|-------|---------|-------------|--------|
| [Paper title] | `Replication/code/01_`-`04_` | [V-Dem, WDI, Polity, etc.] | [In progress / Complete] |

---

## Proofreading Protocol (MANDATORY)

**Every lecture and manuscript file MUST be reviewed before any commit or PR.** Use `/proofread` to run the proofreading agent.

The proofreader auto-detects file type: slides get overflow/box checks, manuscripts get paragraph coherence/section transition/academic voice checks. Both get grammar, typos, consistency, and citation verification.

**Key rule:** The agent must NEVER apply changes directly. It proposes changes via a report in `quality_reports/`, then waits for your approval.

---

## Devil's Advocate Protocol

When designing slides, Claude will proactively:

1. **Challenge presentation choices** — "Could this be clearer if we showed X before Y?"
2. **Question pedagogical flow** — "Will students have the background for this notation?"
3. **Probe for gaps** — "Should we include an intuitive example before the formal proof?"
4. **Explore alternatives** — "Here are three ways to visualize this concept..."

---

## PDF Management

Long PDFs can challenge Claude's processing. Upload full PDFs to `master_supporting_docs/supporting_papers/` — Claude will automatically split them into 5-page chunks for safe processing.

See `.claude/rules/pdf-processing.md` for details.

---

## Reference Validation Protocol

For every slide deck, Claude will:

1. **Verify citations** — confirm paper exists, authors correct, year accurate
2. **Check claims** — validate assertions match source material
3. **Cross-reference** — ensure consistency across materials
4. **Document sources** — maintain bibliography with complete entries

---

## Quick Reference Commands

```bash
# Compile LaTeX (3-pass)
cd Slides && TEXINPUTS=../Preambles:$TEXINPUTS xelatex file.tex

# Deploy Quarto to GitHub Pages
./scripts/sync_to_docs.sh LectureN

# Run quality score
python scripts/quality_score.py Quarto/file.qmd

# Add a paper (Claude auto-splits)
cp paper.pdf master_supporting_docs/supporting_papers/
```

---

**Ready to begin? Start by customizing this CLAUDE.md for your project, then upload your materials!**
