# M3 Interpretation Memo

## Model A Headline

A one percentage point increase in the U.S. 15-year mortgage rate two years earlier is associated with a -0.0007 change in annual REIT returns (p = 0.8955). In the log market equity specification, the same lagged mortgage-rate change is associated with a -0.1141 change in log market equity (p = 0.0021).

The return estimate is not statistically distinguishable from zero, but the market-equity specification is more precise. That pattern indicates that annual mortgage-rate variation is more visible in valuation levels than in annual return averages.

## Economic Interpretation

Three channels are the most plausible.

First, the leverage channel: higher mortgage rates raise refinancing and acquisition costs for REITs.

Second, the discount-rate channel: higher rates lower the present value of future property cash flows, which is consistent with the market-equity result.

Third, the capitalization-rate channel: a higher-rate environment raises cap rates and compresses REIT valuations.

## Model B Summary

The prediction benchmark uses a year-based train/test split (2018 and earlier for training; 2019 and later for testing). Among the learned models, the best out-of-sample R² in this run belongs to Random Forest with test R² = -0.1922 and RMSE = 0.0310.

## Diagnostics

Breusch-Pagan F p-value: 8.2767e-51. This indicates heteroskedasticity, so clustered standard errors are the right default.

Maximum VIF: 11.84. The main collinearity issue comes from the common time trend and mortgage-rate series, which is expected in a macro panel.

## Robustness

Alternative lag checks are saved in the lag robustness table. The largest absolute coefficient across lags is Lag 3 with coefficient 0.0085.

The crisis-exclusion specification and the large-vs-small subsample results do not change the sign of the mortgage-rate effect, which supports the baseline finding.

## Caveats

This is a reduced-form annual panel. Because the mortgage-rate regressor is national and common to all firms, identification comes from time variation, not cross-sectional differences.

Annual aggregation also smooths short-run monthly dynamics, so the model should be interpreted as a longer-run association rather than a high-frequency forecasting engine.

## Two-Way FE Appendix Note

As a specification check, a strict two-way fixed-effects model with entity and full year dummies was evaluated conceptually. In that setup, the mortgage-rate regressor is fully absorbed because it is common to all entities within each year. As a result, the mortgage-rate coefficient is not separately identified under saturated year effects.

The reported baseline therefore uses entity fixed effects plus a year trend and crisis indicators, while retaining two-way clustered standard errors (entity and year). This keeps macro-time controls in the model without mechanically removing the national mortgage-rate signal.

## Outputs

- results/tables/M3_regression_table.csv
- results/tables/M3_regression_table.md
- results/tables/M3_breusch_pagan.csv
- results/tables/M3_vif.csv
- results/tables/M3_standard_vs_clustered.csv
- results/tables/M3_lag_robustness.csv
- results/tables/M3_outlier_exclusion.csv
- results/tables/M3_subsample_robustness.csv
- results/tables/M3_model_b_comparison.csv
- results/tables/M3_model_b_feature_importance.csv
- results/figures/M3_residuals_vs_fitted.png
- results/figures/M3_qq_plot.png
- results/figures/M3_lag_robustness.png
- results/figures/M3_model_b_predictions.png
- results/figures/M3_model_b_feature_importance.png
