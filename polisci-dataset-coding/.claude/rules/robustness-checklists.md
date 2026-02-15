---
paths:
  - "Replication/data/coded/**"
  - "Replication/**/*.R"
---

# Robustness Checklists for AI-Coded Datasets

**Purpose:** Structured checklist for the `coding-reliability-reviewer` agent and `/reviewer-2` (Module Y). Contains the quality checks, reliability standards, and key citations for evaluating AI-coded cross-national datasets.

**How this file is used:** The methodology-reviewer agent loads Module Y when reviewing papers that use AI-coded data. The coding-reliability-reviewer uses `dataset-construction-conventions.md` directly for its review protocol, but this module provides the external-facing checklist for downstream consumers of the data.

---

## Module Y: AI-Coded Dataset

### Core Questions to Interrogate

1. **External validation:** Was the AI coder validated against human expert judgments? What was the agreement rate and sample size?
2. **Evidence fabrication:** Were evidence citations audited for hallucination? What was the verification rate?
3. **Temporal contamination:** Could the AI's knowledge of future events influence coding of past years? What enforcement mechanisms were used?
4. **Prompt sensitivity:** How stable are codings across different prompt wordings? Would rephrasing the question change the data?
5. **Coverage honesty:** Does the dataset acknowledge where the AI lacks knowledge, or does it fill gaps with confident-sounding guesses?

### Robustness Checklist

**Pre-Coding Quality:**
- [ ] Behavioral pre-testing performed (label compliance, definition recall, example classification)
- [ ] Label semantics check passed (< 20% score change with neutral labels)
- [ ] Scale direction check passed (< 10% score change with reversed scale)
- [ ] Inclusion/exclusion criteria present for each variable (Halterman-Keith format)
- [ ] Prompt variant testing performed (3 variants, cross-variant ICC >= 0.80)

**Calibration & Validation:**
- [ ] Calibration against established dataset (ICC >= 0.75) or proxy correlations (>= 3/5 at |r| >= 0.4)
- [ ] Gold-standard validation set >= 200 cells, stratified across regions/decades/score levels
- [ ] Gold-standard coded BLIND (expert did not see AI scores)
- [ ] Gold-standard validation ICC >= 0.60
- [ ] Hallucination audit performed (verification rate reported)
- [ ] Hallucination verification rate >= 80%

**Production Reliability:**
- [ ] Multi-run majority voting (3 runs per cell) or documented justification for opt-out
- [ ] Majority vote agreement rates reported (% 3/3, 2/3, 0/3)
- [ ] All 0/3 (tie) cells resolved via tiebreaker or human adjudication
- [ ] Sentinel drift monitoring performed (50 embedded known-answer cells, checked every 10 batches)
- [ ] No red-alert drift events (or documented response to alerts)
- [ ] Temporal boundary enforcement described and evidenced
- [ ] Evidence dates verified as preceding coding years

**Extended Reliability (if claimed):**
- [ ] Prompt sensitivity test performed (agreement >= 80%, ICC >= 0.80)
- [ ] Adversarial stability test (flip rate <= 15%)
- [ ] Construct validity checked (correlation with observable outcomes)

**Coverage & Transparency:**
- [ ] UNABLE_TO_CODE option available and rate reported by region
- [ ] Confidence distribution disclosed (overall and by region/decade)
- [ ] Full prompt templates published in methodology report
- [ ] AI model version and date documented
- [ ] "How this differs from expert-coded data" section present
- [ ] Downstream bias correction documented (Egami et al. 2024 DSL estimator referenced)

### Key Citations
- Krippendorff, K. (2018). *Content Analysis: An Introduction to Its Methodology.* 4th ed. SAGE.
- Grimmer, J. & Stewart, B. (2013). "Text as Data: The Promise and Pitfalls of Automatic Content Analysis." *Political Analysis.*
- Coppedge, M. et al. (2024). "V-Dem Methodology." *V-Dem Institute Working Paper.*
- Gilardi, F., Alizadeh, M. & Kubli, M. (2023). "ChatGPT Outperforms Crowd Workers for Text-Annotation Tasks." *PNAS.*
- Halterman, A. & Keith, K. (2024). "Codebook LLMs: Evaluating LLMs as Measurement Tools for Political Science Concepts." *Political Analysis.*
- Egami, N., Hartman, E. & Yin, G. (2024). "Using Imperfect Surrogates for Downstream Inference: Design-based Supervised Learning for Social Science Applications of LLMs." *NeurIPS.*
- Wang, X. et al. (2023). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." *ICLR.*
- Carlson, D. et al. (2025). "Variance-Aware LLM Annotation for Strategy Research." *Strategic Management Journal.*
- Imran, A. et al. (2025). "OLAF: An Open Annotation Framework for LLM-Based Annotation." *arXiv:2512.15979.*

### Common Mistakes
- No human validation at all (most common and most damaging for credibility)
- Reporting Krippendorff's alpha for AI self-agreement (alpha is for inter-coder; use ICC for test-retest)
- No hallucination audit (evidence citations may be fabricated)
- Not disclosing prompt templates (makes replication impossible)
- Treating AI confidence ratings as calibrated without verification
- Assuming regional coverage is uniform (AI knows more about some regions)
- Using the word "expert" to describe AI coding in publications
- Reporting only one reliability metric (need calibration + human validation + hallucination rate at minimum)
- **Single-run coding without majority voting** — no empirical reliability measure per cell
- **No behavioral pre-testing** — assuming the model follows the codebook without verification
- **No drift monitoring** — quality may degrade across 100+ batches without detection
- **Gold-standard too small** — fewer than 200 cells cannot support DSL correction or meaningful ICC
- **Using AI-coded labels directly in regression** without Egami et al. (2024) correction — produces biased coefficients
- **No prompt variant testing** — coding may be fragile to minor wording changes
- **Gold-standard contamination** — expert saw AI scores before coding (invalidates the validation)
