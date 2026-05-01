# Individual Addendum Template
## QM 2023 Capstone Project - Milestone 4

Note: This is an evidence-backed draft based on repository artifacts. Replace bracketed fields so the statement reflects your actual personal contribution accurately.

Name: [Your Name]
Team: Lailah, Stevie, Isabelle, Sienna
Date: [May 1, 2026]

## Research Question Answer (Using M1-M4 Data)

Research question: How do changes in U.S. 15-year mortgage rates relate to REIT performance and firm-level characteristics over time?

Answer:
- In our annual panel (286 REITs, 2,965 observations, 2000-2023), higher 15-year mortgage rates are associated with weaker REIT valuation levels, but not with a statistically significant change in annual REIT returns.
- Specifically, in the M3 fixed-effects baseline with entity FE, year trend, crisis controls, and two-way clustered SEs, a 1 percentage-point increase in mortgage rate (lag 2) is associated with:
	- REIT annual return: coefficient = -0.0007, p = 0.8955 (not statistically significant)
	- Log market equity: coefficient = -0.1141, p = 0.0021 (negative and statistically significant)
- Interpretation: rate increases appear to transmit more clearly through valuation channels (discount rates, refinancing costs, cap-rate pressure) than through annual average return variation.
- Firm-level characteristics matter for valuation outcomes: higher debt/assets, higher cash/assets, and higher book-to-market are all significantly associated with lower log market equity in the baseline model, while return sensitivity to mortgage rates remains weak across robustness checks.

Evidence files:
- [results/tables/M3_key_results.csv](results/tables/M3_key_results.csv)
- [results/tables/M3_regression_table_detailed.csv](results/tables/M3_regression_table_detailed.csv)
- [results/tables/M3_lag_robustness.csv](results/tables/M3_lag_robustness.csv)
- [results/tables/M3_outlier_exclusion.csv](results/tables/M3_outlier_exclusion.csv)
- [results/tables/M3_subsample_robustness.csv](results/tables/M3_subsample_robustness.csv)

## 1. Personal Contribution to Capstone Milestones

### Milestone 1: Data Pipeline (Week 5)
Tasks completed:
- Built and documented data-quality checks for source, cleaned, and merged datasets (row counts, key integrity, year/entity coverage).
- Verified panel key integrity after merge (`unit_id`, `year`): no missing keys and no duplicate keys in final analysis file.
- Documented merge attrition and sample-shift implications (31.6% row drop from non-overlapping years; 83 entities lost) and recorded ethical/data-loss caveats.

Hours spent: [__] hours

Key deliverable:
- M1 data quality reporting and reproducibility documentation in [M1/M1_data_quality_report.md](M1/M1_data_quality_report.md)

### Milestone 2: EDA Dashboard (Week 10)
Tasks completed:
- Implemented/validated the lagged-effects workflow and interpretation pipeline used to motivate later model lags.
- Supported EDA finding synthesis linking plots to econometric hypotheses (negative rate-return relationship, crisis sensitivity, and lag structure).
- Drafted or refined data-quality flags and mitigation recommendations for M3 (heteroskedasticity, multicollinearity, outliers, autocorrelation).

Hours spent: [__] hours

Key deliverable:
- EDA findings and M3 handoff in [M2/M2_EDA_summary.md](M2/M2_EDA_summary.md)

### Milestone 3: Econometric Models (Week 14)
Tasks completed:
- Specified and executed the fixed-effects panel workflow with entity FE, time trend, crisis controls, and two-way clustered SEs.
- Added diagnostics and robustness checks: Breusch-Pagan, VIF, lag robustness, crisis exclusion, size subsamples, and standard-vs-clustered SE comparison.
- Implemented strict TWFE absorption check and documented why the national annual mortgage-rate regressor is absorbed under saturated year FE.

Hours spent: [__] hours

Key deliverable:
- M3 econometric pipeline and outputs in [code/capstone_models.py](code/capstone_models.py), [M3/M3_econometric_models.md](M3/M3_econometric_models.md), [M3/M3_interpretation.md](M3/M3_interpretation.md)

### Milestone 4: Final Investment Memo (Week 14)
Tasks completed:
- Consolidated M3 outputs into memo-ready narrative language, including interpretation of statistical significance and economic channels.
- Wrote the final direct answer to the project research question and ensured claims matched model evidence and uncertainty.
- Aligned conclusions with robustness evidence and limitations so recommendations remained consistent with what the data supports.
- Performed final consistency checks across tables, figures, and references in project documentation.

Hours spent: [__] hours

Key deliverable:
- Final interpretation/memo-ready content and output reconciliation in [M3/M3_interpretation.md](M3/M3_interpretation.md) and [README.md](README.md)

### Total Estimated Contribution
Total hours across all milestones: [__] hours

Percentage of team workload: [__]%

Role(s) on team:
- [Example: Econometrics Lead (M3), EDA/Methods Support (M2), QA & Documentation Lead (M4)]

## 2. One Defended Methodological Decision

Decision:
- Use entity fixed effects plus a year trend and crisis indicators (with two-way clustered SEs) for the interpreted baseline, while separately reporting a strict TWFE absorption check.

Reasoning:
- Data evidence: In a strict TWFE model, the national annual mortgage-rate regressor is absorbed by year fixed effects and is not estimable (see [results/tables/M3_twfe_absorption_check.csv](results/tables/M3_twfe_absorption_check.csv)).
- Economic/statistical reasoning: Because the mortgage rate is common across entities in each year, saturated year FE remove the identifying time variation in that regressor.
- Robustness and transparency: We still documented strict TWFE for compliance, but interpreted the estimable FE model with conservative clustered inference.

Alternative considered (and why rejected):
- We considered using strict entity+year FE as the only reported model. We rejected this as the sole interpreted specification because it eliminates the mortgage-rate coefficient entirely, which prevents answering the central research question about rate sensitivity.

## 3. One Key Limitation of Our Analysis

Limitation:
- Annual aggregation and a national macro regressor limit identification strength for return sensitivity and likely smooth short-run dynamics.

Why this matters:
- The mortgage-rate coefficient in the annual return FE model is near zero and not statistically significant (p = 0.8955), while valuation-level effects are significant in log market equity. This pattern suggests annual averaging may dilute faster-moving financing and repricing channels that appear at higher frequency.
- Since identification mainly comes from time variation in a common national regressor, omitted macro shocks or regime shifts can still confound interpretation even with FE, trend controls, and clustering.

Potential mitigation:
- Use higher-frequency panel data (monthly/quarterly) with distributed lag structure and richer macro controls (e.g., credit spreads, term spread, sentiment/risk proxies).
- Add alternative identification strategies, such as interacting rate changes with pre-period leverage/refinancing exposure, to recover cross-sectional heterogeneity in sensitivity.
- As a practical extension for M4 recommendations, distinguish valuation-risk messaging from return-forecast messaging, since the current data show stronger evidence for valuation effects than annual return predictability.

## 4. AI Audit Notes (If Applicable)

AI Tools Used:
- GitHub Copilot
- [Optional: ChatGPT / Claude / Other]

Specific AI Use Examples:

Example 1:
- Task: Build and debug M3 panel econometric pipeline and robustness outputs.
- Prompt: "Build the M3 econometric pipeline for annual REIT metrics versus U.S. 15-year mortgage rates; include diagnostics and robustness checks."
- Output: Draft/refined pipeline code, diagnostics exports, and documentation updates.
- Verification: Re-ran full pipeline and validated expected files and statistics in results tables/figures.
- Critique: Initial drafts required manual corrections for specification framing and file/path consistency.

Example 2:
- Task: Documentation synchronization between model outputs and reports.
- Prompt: "Update README and M3 report language to match generated outputs and file locations."
- Output: Revised report sections and references.
- Verification: Cross-checked paths, key coefficients, and p-values against CSV outputs.
- Critique: AI-generated prose needed tightening to avoid over-claiming causal conclusions.

Overall AI Use:
- [__]% of my work involved AI assistance (primarily coding acceleration, debugging, and formatting support), with all final interpretations and methodological decisions reviewed by me.

## 5. Self-Reflection

What did I do particularly well on this capstone?
- I was strongest in translating econometric implementation details into defensible, rubric-aligned reporting without overstating findings.

What could I have improved?
- I could have begun robustness packaging and memo harmonization earlier to reduce final-week integration pressure.

What did I learn from this capstone project?
- I learned that model identification constraints can be as important as model fit, especially in panel settings with national macro regressors.
- I also improved at connecting diagnostics (heteroskedasticity, multicollinearity, absorption checks) to practical modeling choices instead of treating tests as a checklist.
- Most importantly, I gained confidence in executing and defending an end-to-end empirical workflow from data engineering through final communication.

## 6. Attestation

By submitting this individual addendum, I affirm that:
- All contributions listed above are accurate and honest.
- I have not exaggerated my role or minimized teammates' contributions.
- I understand this addendum may be used to adjust my individual grade relative to the team grade.
- I take full responsibility for my work and any errors in the sections I authored.

Signature: [Type full name or sign in PDF]    Date: [__]

## Quick Finalization Checklist

- Replace all bracketed fields ([...]) with your actual details.
- Adjust milestone tasks so they match your personal work only.
- Ensure team percentages across members sum to 100%.
- Export to PDF as: `Individual_Addendum_[YourLastName].pdf`
