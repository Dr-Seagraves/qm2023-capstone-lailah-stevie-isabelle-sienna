REIT Investment Memo — QM 2023 Capstone
Date: May 1, 2026
Research question: How do changes in U.S. 15‑year mortgage rates relate to REIT performance and firm characteristics over time?

Executive summary
- Main empirical finding (M1–M4): In our annual panel (286 REITs, 2000–2023, analysis n ≈ 2,428 for returns), increases in the U.S. 15‑year mortgage rate are associated with significant declines in REIT valuation levels but not with statistically significant changes in annual REIT returns.
  - Returns model (FE baseline, mortgage_lag2): coef = -0.0007, p = 0.8955 (not significant).
  - Log market equity (FE baseline, mortgage_lag2): coef = -0.1141, p = 0.0021 (statistically significant).
- Practical implication: Rate shocks show up more clearly in valuation channels (discount‑rate and refinancing effects). For portfolio tilts, prioritize balance‑sheet resilience and valuation exposure rather than assuming predictable short‑term return losses from rate hikes.

Key empirical evidence (selected)
- Data and pipeline: final analysis file `data/final/reit_fred_analysis_panel.csv` (n = 2,965); merge and cleaning documented in `M1/M1_data_quality_report.md`.
- EDA: optimal driver lag informed by M2 lag-analysis (lags 2–3 preferred); crisis sensitivity illustrated in `M2/M2_EDA_summary.md`.
- Main model and diagnostics: `code/capstone_models.py` produced FE baseline, TWFE absorption check, Breusch‑Pagan and VIF diagnostics, and robustness tables under `results/tables/` and figures under `results/figures/`.
  - See `results/tables/M3_key_results.csv` and `results/tables/M3_regression_table_detailed.csv` for coefficients and inference.

Portfolio recommendations (tactical guidance)
- Aggregate stance: Neutral to slight overweight on high‑quality REIT exposure — valuation risks are meaningful, but annual return predictability is weak.
- Overweight (selective): REITs with low leverage, stable cash flows, long‑duration leases, and high-quality tenant bases (industrial and certain multifamily exposures are typical examples). Rationale: lower refinancing sensitivity and stronger valuation support under rate stress.
- Reduce / underweight: REITs with high debt/assets, short lease profiles, or concentrated exposure to structurally challenged property types (broad retail and office exposures warrant caution unless quality/lease covenants are strong).
- Implementation notes: Favor security‑level credit analysis, covenant/loan maturity screens, and valuation re‑sizing rules rather than broad sector bets when possible.

Scenario analysis (illustrative)
- The returns FE coefficient is near zero, so predicted annual-return impacts from plausible rate moves are small and statistically indistinguishable from zero. Valuation channel magnitudes (log market equity) are more meaningful:
  - A 5.25 percentage‑point increase (2022–23 style hike) implies an estimated log‑equity effect ≈ -0.599, corresponding to roughly -45% in level terms; interpret cautiously (long‑run valuation channel, not a single‑year realized return).
- Recommended scenario posture: maintain liquidity and reduce concentrated exposure to high‑refinancing‑risk names; tilt to lower‑leverage, higher‑quality names to capture potential recovery if rates fall.

Risk assessment
- Model risks: FE assumption (time‑invariant unobservables) may be violated if firms restructures portfolios; national regressor identification relies on time variation and is sensitive to omitted macro shocks.
- Market risks: rate volatility, sector‑specific structural shocks (e.g., retail disruption), and liquidity drying in downturns can amplify realized losses beyond valuation‑level estimates.
- Operational risks: data coverage (annual aggregation), measurement error in firm characteristics, and model specification choices (lag selection) affect quantitative forecasts.

Caveats and limitations
- Annual aggregation smooths short‑run dynamics; identification of return timing is limited. Strict TWFE absorbs national annual regressors—thus we report an estimable baseline (entity FE + year trend + crisis controls) and the TWFE absorption check for transparency.
- External validity: results are conditional on 2000–2023 sample composition and may not generalize to materially different macro regimes.

Recommended next steps (M4 / post‑capstone)
1. Short‑run analysis: repeat key tests at monthly/quarterly frequency to recover timing of return responses and distributed‑lag effects.
2. Exposure screens: build automated refinancing‑maturity and leverage dashboards to identify at‑risk issuers.
3. Heterogeneity: estimate interactions between rate moves and pre‑period leverage or geographic concentration to find cross‑sectional sensitivities.

References and outputs
- See project outputs: `M1/M1_data_quality_report.md`, `M2/M2_EDA_summary.md`, `M3/M3_econometric_models.md`, `M3/M3_interpretation.md`, and `results/tables/*` and `results/figures/*`.

Signature: ________________________    Date: ___________
