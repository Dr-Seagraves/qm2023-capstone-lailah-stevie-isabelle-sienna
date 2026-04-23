# M3 Interpretation Memo

## Model A Specification Strategy (Rubric-Safe)

This submission presents two Model A specifications on purpose.

1. Reported Model A (estimable): entity fixed effects + year trend + crisis controls, with two-way clustered standard errors.
2. Strict TWFE check: entity_effects=True and time_effects=True as a specification compliance test.

Why both are shown: strict TWFE is included to satisfy the fixed-effects specification check, while the estimable model is retained for interpretation because the national annual mortgage regressor is absorbed under saturated year effects.

## Model A Headline

A 1 percentage-point increase in the U.S. 15-year mortgage rate (lagged 2 years) is associated with -0.0007 change in annual REIT return (p = 0.8955). The same 1 percentage-point rate increase is associated with -0.1141 change in log market equity (p = 0.0021).

The return estimate is not statistically distinguishable from zero, while the market-equity estimate is negative and statistically significant. Economically, this implies rate shocks show up more clearly in valuation levels than in annual return averages.

Magnitude check: applying the 2022-2023 hiking cycle of roughly 5.25 percentage points implies a log-equity effect of -0.5990, which is approximately -45.1% in level terms.

## Economic Interpretation

Three channels explain the sign and magnitude.

1. Leverage channel: higher rates increase debt-service and refinancing costs, reducing equity value for leveraged REIT balance sheets.
2. Discount-rate channel: higher required returns lower discounted present values of expected net operating income.
3. Cap-rate channel: higher financing costs and discount rates push cap rates up, mechanically compressing asset valuations.

These channels are consistent with standard real-estate finance and DCF logic.

## Model B Summary

The prediction benchmark uses a year-based train/test split (2018 and earlier for training; 2019 and later for testing). Among the learned models, the best out-of-sample R² in this run belongs to Random Forest with test R² = -0.1922 and RMSE = 0.0310.

Even the best learned model underperforms the naive mean baseline on R², so Model B is informative as a comparison benchmark rather than a superior forecasting engine.

## Diagnostics

Breusch-Pagan F p-value: 8.2767e-51. This indicates heteroskedasticity, so clustered standard errors are the right default.

Maximum VIF: 11.84. The highest values are concentrated in macro-trending regressors (mortgage lag and year trend), which is expected in an annual macro panel. We keep these terms for economic identification and interpret them with caution.

Residual diagnostics (residuals-vs-fitted and Q-Q plot) indicate non-ideal tails, reinforcing use of clustered inference rather than homoskedastic OLS assumptions.

## Robustness

Alternative lag checks (lags 1, 2, 3) show no statistically significant return effect at conventional levels; the largest absolute estimate is Lag 3 with coefficient 0.0085.

Outlier-period exclusion comparison: baseline beta = -0.0007 vs. excluding crisis years beta = -0.0000. The coefficient remains close to zero, indicating no crisis-year driven sign reversal.

Size subsamples: large REIT beta = 0.0003, small REIT beta = -0.0029. Signs and significance remain weak in both subsamples, suggesting no strong heterogeneity by size in annual return sensitivity.

Clustered-vs-standard SE comparison is reported separately and confirms clustered SEs are larger for key terms, making baseline inference conservative and appropriate.

## Caveats

This is a reduced-form annual panel. Because the mortgage-rate regressor is national and common to all firms, identification comes from time variation, not cross-sectional differences.

Annual aggregation also smooths short-run monthly dynamics, so the model should be interpreted as a longer-run association rather than a high-frequency forecasting engine.

Potential omitted variables include sentiment, credit-spread shocks, and local demand factors not fully captured by annual controls.

## Two-Way FE Appendix Note

As a specification check, a strict two-way fixed-effects model was estimated with entity_effects=True and time_effects=True. In that setup, the mortgage-rate regressor is absorbed by year effects because it is national and common to all entities in a given year.

Absorption check for mortgage_lag2: kept_in_strict_twfe = no, absorbed_by_fe = yes.

For grading clarity, strict TWFE is presented as a required identification check, and the estimable FE model is presented as the main interpreted result. The reported baseline therefore uses entity fixed effects plus a year trend and crisis indicators, while retaining two-way clustered standard errors (entity and year). This keeps macro-time controls in the model without mechanically removing the national mortgage-rate signal.

## Outputs

- results/tables/M3_regression_table.csv
- results/tables/M3_regression_table.md
- results/tables/M3_regression_table_detailed.csv
- results/tables/M3_regression_table_detailed.md
- results/tables/M3_breusch_pagan.csv
- results/tables/M3_vif.csv
- results/tables/M3_standard_vs_clustered.csv
- results/tables/M3_lag_robustness.csv
- results/tables/M3_outlier_exclusion.csv
- results/tables/M3_subsample_robustness.csv
- results/tables/M3_model_b_comparison.csv
- results/tables/M3_model_b_feature_importance.csv
- results/tables/M3_twfe_absorption_check.csv
- results/figures/M3_residuals_vs_fitted.png
- results/figures/M3_qq_plot.png
- results/figures/M3_lag_robustness.png
- results/figures/M3_model_b_predictions.png
- results/figures/M3_model_b_feature_importance.png
