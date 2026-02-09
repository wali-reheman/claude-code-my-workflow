---
paths:
  - "Manuscripts/**"
  - "scripts/**/*.R"
  - "Slides/**/*.tex"
  - "Quarto/**/*.qmd"
  - "Replication/**"
---

# Design-Specific Robustness Checklists

**Purpose:** Structured checklists for the methodology-reviewer agent (`/reviewer-2`). Each module contains the identification assumptions to interrogate, the robustness tests to verify, and key citations for current best practice.

**How this file is used:** The methodology-reviewer agent detects the research design type (Phase 0), then reads the corresponding module(s) from this file to know exactly what to check.

---

## Module A: Difference-in-Differences

### Identification Assumptions to Interrogate

1. **Parallel trends:** Is it stated explicitly? Is there a pre-trends test (event study plot, not just a p-value)?
2. **No anticipation:** Could units change behavior before treatment onset?
3. **Staggered timing:** If treatment is staggered across units, TWFE is biased under heterogeneous treatment effects. Is a heterogeneity-robust estimator used?
4. **Stable composition:** Does the composition of treatment and control groups change over time?
5. **No spillover:** Could treated units affect control unit outcomes?

### Robustness Checklist

- [ ] Parallel pre-trends event study plot (with confidence intervals)
- [ ] Placebo treatment timing test (fake treatment at earlier date)
- [ ] Goodman-Bacon (2021) decomposition (if staggered)
- [ ] Heterogeneity-robust estimator — one of:
  - Callaway & Sant'Anna (2021): `did::att_gt()`
  - Sun & Abraham (2021): `fixest::sunab()`
  - de Chaisemartin & D'Haultfoeuille (2020): `DIDmultiplegt`
  - Borusyak, Jaravel & Spiess (2024): `didimputation`
- [ ] Oster (2019) bounds for selection on unobservables (`deltastar` threshold)
- [ ] Alternative control groups (e.g., not-yet-treated vs never-treated)
- [ ] Dropping always-treated or early-treated units
- [ ] Varying pre-treatment window length
- [ ] Covariate balance across treatment groups (pre-treatment levels)
- [ ] Sensitivity to treatment timing definition

### Key Citations
- Goodman-Bacon (2021). "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics.*
- Callaway & Sant'Anna (2021). "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics.*
- Roth (2022). "Pretest with Caution: Event-Study Estimates after Testing for Parallel Trends." *AER: Insights.*
- Roth, Sant'Anna, Bilinski & Poe (2023). "What's Trending in Difference-in-Differences?" *Journal of Econometrics.*

### Common Mistakes
- Using TWFE with staggered timing and heterogeneous effects (near-automatic Major flag in 2026)
- Pre-trends test has low power — passing it does not confirm parallel trends (Roth 2022)
- Conditioning on time-varying covariates that are themselves affected by treatment

---

## Module B: Regression Discontinuity

### Identification Assumptions to Interrogate

1. **Continuity:** Potential outcomes are continuous at the cutoff (no other discontinuity)
2. **No manipulation:** Units cannot precisely sort around the cutoff
3. **Running variable:** Is it truly continuous, or are there mass points / heaping?
4. **Local nature:** The estimate is valid only at the cutoff — extrapolation is unjustified

### Robustness Checklist

- [ ] McCrary (2008) / Cattaneo, Jansson & Ma (2020) density test (`rddensity`)
- [ ] Bandwidth sensitivity (half, double, Calonico-Cattaneo-Titiunik optimal)
- [ ] Polynomial order sensitivity (local linear vs quadratic vs cubic)
- [ ] Covariate balance at cutoff (predetermined covariates should not jump)
- [ ] Donut hole RDD (exclude observations closest to cutoff)
- [ ] Placebo cutoffs (test for discontinuities at non-cutoff values)
- [ ] RD plot with appropriate bin width (not hand-picked to look good)
- [ ] Fuzzy vs sharp distinction clear (if fuzzy: first stage presented)

### Key Citations
- Cattaneo, Idrobo & Titiunik (2019). *A Practical Introduction to Regression Discontinuity Designs.* Cambridge Elements.
- Cattaneo & Titiunik (2022). "Regression Discontinuity Designs." *Annual Review of Economics.*
- McCrary (2008). "Manipulation of the Running Variable in the Regression Discontinuity Design." *Journal of Econometrics.*

### Common Mistakes
- Choosing bandwidth to maximize significance
- Not presenting the McCrary density test
- Over-extrapolating RD results beyond a local neighborhood of the cutoff
- Using global polynomial fits (high-order polynomials across full support)

---

## Module C: Instrumental Variables

### Identification Assumptions to Interrogate

1. **Relevance:** Instrument predicts the endogenous variable (testable via first stage)
2. **Exclusion restriction:** Instrument affects outcome ONLY through the endogenous variable (not testable — must be argued)
3. **Independence / exogeneity:** Instrument is as-if randomly assigned (no confounders of instrument-outcome relationship)
4. **Monotonicity:** No defiers (all units who would take treatment if encouraged would also take it if not encouraged, or vice versa — but not both)

### Robustness Checklist

- [ ] First-stage F-statistic reported (threshold: > 104.7 per Lee et al. 2022 for 5% bias; > 10 is insufficient)
- [ ] Reduced form estimate presented (instrument → outcome directly)
- [ ] Exclusion restriction argument (narrative, not just asserted — what are the most plausible violations?)
- [ ] Weak-IV-robust inference (Anderson-Rubin test, tF procedure)
- [ ] Over-identification test (if multiple instruments: Sargan/Hansen J-test)
- [ ] Sensitivity to instrument definition or construction
- [ ] Plausibly exogenous framework (Conley, Hansen & Rossi 2012) for near-violations of exclusion
- [ ] LATE interpretation: who are the compliers? Are they policy-relevant?

### Key Citations
- Lee, McCrary, Moreira & Porter (2022). "Valid t-ratio Inference for IV." *American Economic Review.*
- Andrews, Stock & Sun (2019). "Weak Instruments in IV Regression." *Annual Review of Economics.*
- Conley, Hansen & Rossi (2012). "Plausibly Exogenous." *Review of Economics and Statistics.*

### Common Mistakes
- Citing F > 10 as sufficient (outdated rule — Lee et al. 2022 shows threshold is 104.7 for 5% worst-case bias)
- Not presenting the reduced form
- Exclusion restriction asserted without discussion of plausible violations
- Multiple instruments used for "efficiency" without over-ID testing

---

## Module D: Matching / Weighting

### Identification Assumptions to Interrogate

1. **Conditional independence / unconfoundedness:** Treatment assignment independent of potential outcomes, conditional on observed covariates (strong, untestable)
2. **Common support / overlap:** For every treated unit, there exist comparable control units
3. **No post-treatment conditioning:** Matching covariates must be pre-treatment
4. **Correct functional form:** Balance on observed covariates should not depend on model specification

### Robustness Checklist

- [ ] Balance tables (standardized mean differences < 0.1 per Imbens & Rubin 2015)
- [ ] Common support / overlap visualization
- [ ] Rosenbaum (2002) sensitivity bounds (how much hidden bias would break results?)
- [ ] Oster (2019) bounds for selection on unobservables
- [ ] Multiple matching algorithms (PSM vs CEM vs Mahalanobis vs entropy balancing)
- [ ] Varying caliper widths (for PSM)
- [ ] Sensitivity to covariate set (add/remove covariates)
- [ ] Propensity score model specification (logit vs probit, which covariates, interactions)
- [ ] Trimming / common support restrictions

### Key Citations
- Imbens & Rubin (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences.* Cambridge.
- Rosenbaum (2002). *Observational Studies.* Springer.
- Oster (2019). "Unobservable Selection and Coefficient Stability." *JBES.*
- King & Nielsen (2019). "Why Propensity Scores Should Not Be Used for Matching." *Political Analysis.*

### Common Mistakes
- Reporting p-values for balance instead of standardized differences
- Not assessing sensitivity to hidden bias (Rosenbaum bounds)
- Matching on post-treatment variables
- Using propensity score matching when other methods (CEM, entropy balancing) achieve better balance

---

## Module E: Synthetic Control

### Identification Assumptions to Interrogate

1. **No interference:** Donor pool units are unaffected by the treated unit's treatment
2. **Convex hull:** The treated unit's pre-treatment trajectory can be approximated by a weighted average of donors
3. **No anticipation:** The treated unit didn't change behavior before treatment
4. **Stable donor weights:** Weights that fit the pre-period also work in the post-period (absent treatment)

### Robustness Checklist

- [ ] Pre-treatment fit quality (RMSPE, visual inspection — gap should be near zero)
- [ ] Placebo-in-space (permutation across all donor units)
- [ ] Leave-one-out (drop each donor unit, check weight stability and fit)
- [ ] Placebo-in-time (assign fake treatment date, verify no effect)
- [ ] Ratio of post/pre RMSPE for inference
- [ ] Alternative predictor sets
- [ ] Weight concentration (is one donor dominating? Fragile if so)
- [ ] Augmented synthetic control (augsynth) for bias correction

### Key Citations
- Abadie, Diamond & Hainmueller (2010). "Synthetic Control Methods for Comparative Case Studies." *JASA.*
- Abadie (2021). "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects." *JEL.*
- Ben-Michael, Feller & Rothstein (2021). "The Augmented Synthetic Control Method." *JASA.*

### Common Mistakes
- Poor pre-treatment fit accepted without discussion
- No placebo tests (permutation inference)
- Weight heavily concentrated on one donor without sensitivity analysis
- Comparing to a poorly fitting synthetic control and claiming "no effect" when fit is inadequate

---

## Module F: Survey & Conjoint Experiments

### Identification Assumptions to Interrogate

1. **No profile-order effects:** Randomization handles this, but verify implementation
2. **Stability and no carryover:** Responses to one profile don't affect responses to subsequent profiles
3. **No attribute interaction effects beyond design:** If attributes interact in ways the design doesn't capture
4. **Respondent engagement:** Satisficing can bias AMCEs toward zero

### Threats Specific to Conjoint

- **AMCE interpretation:** Abramson et al. (2022) show AMCEs can indicate the OPPOSITE of majority preferences when preferences are heterogeneous. AMCEs measure marginal effects of changing one attribute, NOT "what people prefer"
- **Hypothetical bias:** Stated preferences may not match revealed behavior (Hainmueller et al. 2015 validation found close alignment in paired conjoint, but single-profile may diverge)
- **Demand effects:** Could respondents guess the hypothesis?
- **Social desirability:** Especially for sensitive topics (race, immigration, partisanship)
- **Profile realism:** Can all attribute combinations actually exist in reality?

### Robustness Checklist

- [ ] Pre-registration of design (attributes, levels, randomization scheme)
- [ ] Attention checks / satisficing diagnostics
- [ ] Subgroup heterogeneity analysis (AMCEs can mask preference polarization)
- [ ] Marginal means in addition to AMCEs (Leeper, Hobolt & Tilley 2020)
- [ ] Attribute order randomization verified
- [ ] Profile realism restrictions documented
- [ ] External validation against behavioral data (if possible)
- [ ] Sample demographics and representativeness reported
- [ ] Number of tasks per respondent justified (satisficing risk)
- [ ] Forced-choice vs rating: design choice justified

### Key Citations
- Hainmueller, Hopkins & Yamamoto (2014). "Causal Inference in Conjoint Analysis." *Political Analysis.*
- Abramson, Kocak, Magazinnik & Strezhnev (2022). "What Do We Learn about Voter Preferences from Conjoint Experiments?" *AJPS.*
- Leeper, Hobolt & Tilley (2020). "Measuring Subgroup Preferences in Conjoint Experiments." *Political Analysis.*
- Hainmueller, Hangartner & Yamamoto (2015). "Validating Vignette and Conjoint Survey Experiments." *PNAS.*

### Common Mistakes
- Interpreting AMCEs as "preferences" rather than marginal effects
- No discussion of hypothetical bias
- Convenience sample (MTurk/Prolific) with claims about general population preferences
- Too many tasks per respondent without satisficing checks

---

## Module G: Field & Lab Experiments

### Identification Assumptions to Interrogate

1. **Random assignment:** Was randomization properly implemented? (Not just claimed)
2. **SUTVA / no interference:** Treated units don't affect control units
3. **Excludability:** Treatment assignment affects outcomes only through treatment take-up
4. **No attrition bias:** Dropout is not differential across treatment arms

### Robustness Checklist

- [ ] Pre-analysis plan (PAP) registered (AsPredicted, OSF, EGAP, AEA)
- [ ] Deviations from PAP documented (any deviation without documentation is a red flag)
- [ ] Randomization balance table (F-test for joint significance)
- [ ] ITT (intent-to-treat) estimate reported (not just per-protocol)
- [ ] CACE/TOT (complier average causal effect) if non-compliance
- [ ] Attrition analysis (differential by treatment arm? Lee bounds?)
- [ ] Multiple hypothesis correction (Bonferroni, Benjamini-Hochberg FDR, Westfall-Young)
- [ ] Ex-ante power analysis reported (not ex-post — ex-post power is meaningless)
- [ ] Spillover / contamination assessment
- [ ] Lee (2009) bounds if differential attrition

### Key Citations
- Gerber & Green (2012). *Field Experiments: Design, Analysis, and Interpretation.* Norton.
- Humphreys, Sanchez de la Sierra & van der Windt (2013). "Social and Economic Impacts of Tuungane." EGAP.
- Dunning (2012). *Natural Experiments in the Social Sciences.* Cambridge.

### Common Mistakes
- No pre-analysis plan for a 2026 experiment (increasingly unacceptable)
- Reporting only significant outcomes without multiple testing correction
- Ex-post power analysis to "explain" null results
- Ignoring non-compliance (reporting per-protocol instead of ITT)

---

## Module H: Text-as-Data / NLP

### Identification Assumptions to Interrogate

1. **Measurement validity:** Does the text measure capture the theoretical concept?
2. **Corpus representativeness:** Is the text corpus representative of the population of texts you care about?
3. **Labeling consistency:** If supervised/LLM-coded, is coding reliable and replicable?
4. **Bag-of-words adequacy:** If using bag-of-words methods, is word order irrelevant for your concept?

### Robustness Checklist

- [ ] Validation against human coding (intercoder reliability: Krippendorff's alpha > 0.8)
- [ ] Multiple validation types (face + criterion + predictive — Grimmer & Stewart 2013)
- [ ] Sensitivity to preprocessing (stemming, stopwords, n-grams, min document frequency)
- [ ] Sensitivity to number of topics / model hyperparameters
- [ ] Sample texts presented for reader evaluation
- [ ] If LLM-coded: full prompt in appendix, multiple prompt variants tested, temperature documented
- [ ] Close reading of edge cases and misclassifications
- [ ] Corpus construction decisions documented (why these texts? What's excluded?)
- [ ] Dictionary validation (if dictionary method — Laver & Garry, LIWC, custom)
- [ ] Temporal stability of measurement (does the model work across time periods?)

### Key Citations
- Grimmer & Stewart (2013). "Text as Data." *Political Analysis.*
- Grimmer, Roberts & Stewart (2022). *Text as Data: A New Framework.* Princeton.
- Rodriguez & Spirling (2022). "Word Embeddings: What Works, What Doesn't, and How to Tell the Difference." *JOP.*

### Common Mistakes
- Treating topic model output as validated measurement without any validation
- No human-coded baseline for supervised methods
- Sensitivity to preprocessing decisions not tested
- LLM-as-coder without prompt sensitivity analysis

---

## Module I: Process Tracing (Qualitative)

### Core Framework

Process tracing examines within-case evidence to evaluate causal mechanisms. The standard framework (Beach & Pedersen 2013) specifies:

- **Entities:** Who/what participates in the causal process?
- **Activities:** What do they do that transmits causal force?
- **Evidence tests:** How strongly does each piece of evidence discriminate between alternative explanations?

### Evidence Test Types (Van Evera 1997, Beach & Pedersen 2013)

| Test | Uniqueness | Certainty | If passed | If failed |
|---|---|---|---|---|
| Straw-in-the-wind | Low | Low | Slightly more plausible | Slightly less plausible |
| Hoop test | Low | High | Still in contention | Eliminated |
| Smoking gun | High | Low | Strongly confirmed | Not eliminated |
| Doubly decisive | High | High | Confirmed | Eliminated |

### Rigor Checklist

- [ ] Mechanism specified with concrete entities and activities (not just "X leads to Y through Z")
- [ ] Each evidence piece classified by test type and inferential weight
- [ ] Alternative causal mechanisms explicitly considered and tested
- [ ] Prior probability assessment stated before examining evidence
- [ ] Case selection justified (why this case for mechanism testing — typical, deviant, most-likely, least-likely?)
- [ ] Source triangulation (multiple independent evidence types)
- [ ] Disconfirming evidence actively sought (not just confirmatory evidence)
- [ ] Bayesian updating logic explicit (how does each piece change confidence?)

### Key Citations
- Beach & Pedersen (2013). *Process-Tracing Methods: Foundations and Guidelines.* Michigan.
- Bennett & Checkel (2015). *Process Tracing: From Metaphor to Analytic Tool.* Cambridge.
- Mahoney (2012). "The Logic of Process Tracing Tests in the Social Sciences." *Sociological Methods & Research.*

### Common Mistakes
- Vague mechanism specification ("institutions matter" without specifying how)
- Cherry-picking confirmatory evidence
- Not considering alternative explanations systematically
- Informal Bayesian reasoning without making priors explicit

---

## Module J: Comparative Case Studies (Qualitative)

### Design Types

| Design | Logic | Strength | Weakness |
|---|---|---|---|
| Most Similar Systems (MSSD) | Mill's Method of Difference — similar cases, different outcomes | Controls for shared features | Requires truly comparable cases |
| Most Different Systems (MDSD) | Mill's Method of Agreement — different cases, same outcome | Identifies necessary conditions | Many potential causes |
| Typical case | Representative of a broader population | External validity | Limited causal leverage |
| Deviant case | Contradicts theoretical expectations | Theory-building | May be idiosyncratic |

### Rigor Checklist

- [ ] Case selection logic explicitly documented and justified
- [ ] Not selecting on the dependent variable (or justified if doing so — e.g., for necessary conditions)
- [ ] Within-case variation explored (not just cross-case comparison)
- [ ] Scope conditions for generalization stated explicitly
- [ ] Multiple data sources per case (triangulation)
- [ ] Equifinality considered (multiple causal paths to same outcome)
- [ ] Rival explanations addressed within each case
- [ ] Counterfactual reasoning explicit ("what would have happened without X?")
- [ ] Temporal sequence established (cause precedes effect)

### Key Citations
- Lijphart (1971). "Comparative Politics and the Comparative Method." *APSR.*
- Seawright & Gerring (2008). "Case Selection Techniques in Case Study Research." *Political Research Quarterly.*
- Mahoney & Goertz (2006). "A Tale of Two Cultures: Contrasting Quantitative and Qualitative Research." *Political Analysis.*

### Common Mistakes
- Selecting cases to confirm the hypothesis (rather than to test it)
- No discussion of scope conditions
- Treating correlation in two cases as causation
- Ignoring within-case temporal dynamics

---

## Module K: Qualitative Comparative Analysis (QCA)

### Core Concepts

- **Necessity:** The outcome is a subset of the condition (condition must be present for outcome to occur)
- **Sufficiency:** The condition is a subset of the outcome (condition guarantees outcome)
- **INUS causation:** A condition is an Insufficient but Necessary part of a condition which is itself Unnecessary but Sufficient

### Rigor Checklist

- [ ] Calibration documented with theoretical justification for membership thresholds
- [ ] Necessity analysis performed BEFORE sufficiency analysis (standard protocol)
- [ ] Truth table presented with case counts per configuration
- [ ] Consistency threshold justified (typically 0.8 for sufficiency, 0.9 for necessity)
- [ ] Limited diversity: logical remainders handling documented (conservative vs parsimonious vs intermediate solution)
- [ ] Intermediate solution with directional expectations justified theoretically
- [ ] Robustness to calibration thresholds (shift cutoffs by 0.05-0.1)
- [ ] Robustness to consistency thresholds
- [ ] Robustness to case addition or removal
- [ ] Coverage scores reported (how much of the outcome does each path explain?)

### Key Citations
- Ragin (2008). *Redesigning Social Inquiry: Fuzzy Sets and Beyond.* Chicago.
- Schneider & Wagemann (2012). *Set-Theoretic Methods for the Social Sciences.* Cambridge.
- Thomann & Maggetti (2020). "Designing Research with Qualitative Comparative Analysis." *Sociological Methods & Research.*

### Common Mistakes
- Arbitrary calibration cutoffs without theoretical justification
- Not testing necessity before sufficiency
- Reporting only the parsimonious solution without the intermediate
- No robustness checks for threshold sensitivity
- Treating QCA results as causal without case knowledge

---

## Module L: Network Analysis

### Identification Assumptions to Interrogate

1. **Network boundary:** Is the network boundary well-defined? (Who's in, who's out?)
2. **Tie definition:** Is the edge definition consistent and meaningful?
3. **Endogeneity:** Can you distinguish homophily from influence? (The reflection problem)
4. **Missing data:** Are missing ties really absent or just unobserved?

### Robustness Checklist

- [ ] ERGM goodness-of-fit (simulated networks reproduce key observed statistics)
- [ ] Degeneracy diagnostics (MCMC convergence, reasonable parameter estimates)
- [ ] Structural terms theoretically motivated (not just included for model fit)
- [ ] Sensitivity to alternative structural term specifications
- [ ] Temporal dynamics addressed (if longitudinal data — TERGM or STERGM)
- [ ] Unobserved heterogeneity addressed (frailty ERGM or latent space model)
- [ ] Alternative network boundary definitions tested
- [ ] Missing data sensitivity analysis

### Key Citations
- Cranmer & Desmarais (2011). "Inferential Network Analysis with Exponential Random Graph Models." *Political Analysis.*
- Cranmer, Leifeld, McClurg & Rolfe (2017). "Navigating the Range of Statistical Tools for Inferential Network Analysis." *AJPS.*

### Common Mistakes
- Standard regression on network data (ignoring tie interdependence)
- ERGM with degeneracy problems reported as "results"
- Confusing homophily with influence without longitudinal data
- No goodness-of-fit assessment

---

## Module M: Bayesian Analysis

### Identification Assumptions to Interrogate

1. **Prior specification:** Are priors substantively justified or default/convenience?
2. **Likelihood specification:** Is the data-generating model appropriate?
3. **Computational fidelity:** Has the posterior been accurately approximated?

### Robustness Checklist

- [ ] Prior sensitivity analysis (results under alternative reasonable priors)
- [ ] Convergence diagnostics (R-hat < 1.01, bulk and tail ESS adequate, no divergent transitions)
- [ ] Posterior predictive checks (simulated data from posterior matches observed data patterns)
- [ ] Prior predictive simulation (do priors generate plausible data ranges?)
- [ ] Model comparison (WAIC, LOO-CV, or Bayes factors — with prior sensitivity for BFs)
- [ ] Posterior distributions presented (not just point estimates and CIs)
- [ ] Parameterization sensitivity (centered vs non-centered, if relevant)

### Key Citations
- Gill (2014). *Bayesian Methods: A Social and Behavioral Sciences Approach.* CRC Press.
- Gelman, Carlin, Stern, Dunson, Vehtari & Rubin (2013). *Bayesian Data Analysis.* CRC Press.
- Gabry, Simpson, Vehtari, Betancourt & Gelman (2019). "Visualization in Bayesian Workflow." *JRSS-A.*

### Common Mistakes
- Flat / improper priors without justification
- No convergence diagnostics
- No prior sensitivity analysis (especially problematic for Bayes factors)
- Reporting posterior modes or means without uncertainty

---

## Module N: ML for Causal Inference

### Identification Assumptions to Interrogate

1. **DML:** Neyman-orthogonality of the score function. Cross-fitting (not just sample splitting).
2. **Post-LASSO:** Double selection (LASSO on BOTH outcome and treatment — single LASSO creates OVB)
3. **Causal forests:** Honesty condition (separate samples for tree building and estimation)
4. **All ML-causal:** The causal identification comes from the research design, not from the ML. ML handles nuisance estimation.

### Robustness Checklist

- [ ] DML: cross-fitting with K >= 2 folds documented
- [ ] DML: first-stage prediction quality reported (R-squared or similar)
- [ ] Post-LASSO: double selection procedure used (Belloni, Chernozhukov & Hansen 2014)
- [ ] Causal forests: honesty condition satisfied, minimum leaf size documented
- [ ] Sensitivity to ML algorithm choice (LASSO vs random forest vs boosting for nuisance)
- [ ] Sensitivity to tuning parameters (regularization, tree depth, etc.)
- [ ] Standard errors appropriate for the procedure (not naive post-selection SEs)
- [ ] Causal identification argument separate from ML estimation

### Key Citations
- Chernozhukov et al. (2018). "Double/Debiased Machine Learning." *Econometrics Journal.*
- Belloni, Chernozhukov & Hansen (2014). "Inference on Treatment Effects after Selection." *RES.*
- Athey & Wager (2019). "Estimating Treatment Effects with Causal Forests." *JASA.*
- Athey & Imbens (2019). "Machine Learning Methods That Economists Should Know About." *Annual Review of Economics.*

### Common Mistakes
- Using ML predictions directly as causal estimates (ML handles prediction, design handles identification)
- Single LASSO for variable selection (must be double selection)
- Post-selection inference with naive standard errors
- Not reporting first-stage prediction quality for DML

---

## Module O: Measurement / Scaling

### Identification Assumptions to Interrogate

1. **Construct validity:** Does the latent variable capture the intended concept?
2. **Measurement invariance:** Do items measure the same thing across groups/time?
3. **Attenuation from error:** Using noisy measures as regressors biases coefficients toward zero

### Robustness Checklist

- [ ] Attenuation bias correction (SIMEX, errors-in-variables, `lpmec`, split-sample IV)
- [ ] Measurement invariance tested (DIF for IRT; configural/metric/scalar for CFA)
- [ ] Sensitivity to alternative indices (V-Dem vs Polity vs Freedom House for democracy)
- [ ] Uncertainty propagation (draw from posteriors or bootstrap — not point estimates as fixed)
- [ ] IRT/CFA model fit assessed (item fit, person fit, RMSEA, CFI)
- [ ] Method of composition warning: drawing from posteriors and averaging regressions can INCREASE attenuation (Jerzak et al. 2024)

### Key Citations
- Jerzak, Libgober & Lundberg (2024). "Attenuation Bias with Latent Predictors." Working paper.
- Treier & Jackman (2008). "Democracy as a Latent Variable." *AJPS.*
- Coppedge et al. (2024). V-Dem Methodology (current version).

### Common Mistakes
- Treating latent variable point estimates as fixed regressors (ignoring measurement error)
- No sensitivity to alternative operationalizations
- Assuming measurement invariance without testing
- Method of composition presented as "propagating uncertainty" when it actually increases bias

---

## Module P: Multi-Level / Hierarchical Models

### Identification Assumptions to Interrogate

1. **Exchangeability:** Random effects are drawn from a common distribution (is this reasonable?)
2. **Correct nesting:** The hierarchical structure matches the data-generating process
3. **Sufficient higher-level N:** Variance components require adequate group-level sample size

### Robustness Checklist

- [ ] ICC reported for each level (how much variation at each level?)
- [ ] Sufficient higher-level N (>= 20-30 for stable variance estimates; Bryan & Jenkins 2016)
- [ ] Random effects specification theoretically justified (why random slopes for this variable?)
- [ ] Centering strategy documented (grand-mean vs group-mean) with interpretation
- [ ] Cross-level interactions substantively motivated (not data-mined)
- [ ] MAUP sensitivity (would results change with different boundary definitions?)
- [ ] Comparison to fixed effects specification (Hausman-type test or substantive argument)
- [ ] Convergence and identifiability checked (especially with complex random effects)

### Key Citations
- Gelman & Hill (2007). *Data Analysis Using Regression and Multilevel/Hierarchical Models.* Cambridge.
- Bryan & Jenkins (2016). "Multilevel Modelling of Country Effects." *European Sociological Review.*
- Arceneaux & Nickerson (2009). "Modeling Certainty with Clustered Data." *Political Analysis.*

### Common Mistakes
- 15 countries with country-level predictors (insufficient higher-level N)
- Random effects specification driven by model convergence rather than theory
- Ignoring MAUP when using electoral/administrative units
- Clustering SEs at wrong level (treatment assigned at cluster level but SEs at individual)

---

## Module Q: Formal Theory

### Core Questions

Formal theory papers have different rigor standards than empirical papers. The key questions are about internal consistency, not robustness to alternative specifications.

### Rigor Checklist

- [ ] Equilibrium existence proven (or conditions for existence stated)
- [ ] Uniqueness established (if multiple equilibria: selection criterion justified)
- [ ] Comparative statics clearly derived and signed
- [ ] Key assumptions substantively defensible (rationality, information structure, timing)
- [ ] Sensitivity to key parameters explored (which parameters drive the result?)
- [ ] Key assumptions relaxed in extensions or robustness section
- [ ] If empirical section exists: comparative statics mapped to testable predictions
- [ ] Model compared to alternative theoretical frameworks (why this model?)
- [ ] Off-equilibrium beliefs reasonable (if sequential/extensive-form)

### Key Citations
- Depends heavily on subfield. Common frameworks: spatial voting (Downs, Black), bargaining (Rubinstein, Powell), signaling (Spence, Fearon), mechanism design (Myerson).

### Common Mistakes
- Equilibrium existence assumed without proof
- Multiple equilibria with no selection argument
- Comparative statics that reverse under reasonable parameter values
- Disconnect between theoretical predictions and empirical tests

---

## Module R: Descriptive Inference

### Core Questions

Descriptive work is not "causal inference without identification" — it has its own standards. The key question is whether the description is rigorous, well-bounded, and not smuggling causal claims.

### Rigor Checklist

- [ ] Concept clearly defined and bounded (no conceptual stretching — Sartori 1970)
- [ ] No implicit causal claims disguised as description ("X is associated with Y" when framing implies causation)
- [ ] Evidence selection criteria transparent and justified
- [ ] No ecological fallacy (aggregate patterns attributed to individuals)
- [ ] No atomistic fallacy (individual patterns generalized without accounting for context)
- [ ] Alternative classifications or categorizations considered
- [ ] Scope conditions for generalization stated
- [ ] Temporal and spatial boundaries explicit
- [ ] Measurement strategy appropriate for the concept
- [ ] Uncertainty quantified (not just point estimates)

### Key Citations
- Gerring (2012). "Mere Description." *British Journal of Political Science.*
- Sartori (1970). "Concept Misformation in Comparative Politics." *APSR.*
- Lieberman (2005). "Nested Analysis as a Mixed-Method Strategy." *APSR.*

### Common Mistakes
- Descriptive work that implicitly makes causal claims through framing
- "Associated with" used 50 times in a paper that's clearly arguing for a causal effect
- No discussion of what the numbers mean substantively (just statistical reporting)
- Overgeneralization from a narrow sample without scope conditions
