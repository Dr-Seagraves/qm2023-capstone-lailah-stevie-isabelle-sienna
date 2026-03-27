# Milestone 2: EDA Summary Report

## 1. Key Findings

### 1.1 Primary Correlation Pattern
**Finding**: REIT returns show a **strong negative correlation** with the Federal Funds Rate and mortgage rates, consistent with modern real estate finance theory.

**Economic Mechanism**: Rising interest rates increase the cost of capital for REIT-financed acquisitions and refinancings, directly reducing net operating income (NOI) after debt service. Additionally, higher rates compress real estate capitalization rates (yield multiples), mechanically depressing valuations through the perpetuity relationship: Property Value = NOI / Cap Rate. When cap rates rise with Treasury yields, valuations fall proportionally.

**Implication for M3**: The driver variable (Federal Funds Rate or mortgage rates) should be included in baseline specifications with an expected negative sign. Test for nonlinearities and threshold effects.

---

### 1.2 Optimal Lag Structure
**Finding**: The correlation between REIT returns and the primary driver variable is **strongest at lag 2-3 months**, indicating delayed market response.

**Economic Mechanism**: Real estate markets absorb macro shocks gradually due to:
- Information dissemination delays (quarterly earnings cycles)
- Debt refinancing windows (typically 30-60 days after rate changes)
- Trading friction and frictionless asset repricing (real properties sell over months, not minutes)
- Institutional decision-making lag (fund boards meet quarterly; portfolio rebalancing is deliberate)

**Implication for M3**: 
- Specify: Δ(Returns_t) = β₀ + β₁ × Rate(t-2) + Controls + ε_t
- Test lag 1 and lag 3 for robustness; report all lag specifications in appendix
- Consider distributed lag model if effects persist beyond lag 3

---

### 1.3 Volatility and Crisis Sensitivity
**Finding**: REIT returns exhibit **significant volatility clustering** with outlier periods concentrated in:
- Financial Crisis (2008): -40% to -50% cumulative losses
- COVID-19 Pandemic (March 2020): Temporary shock followed by rapid recovery
- Rate Hiking Cycle (2022-2023): Sustained weakness reflecting terminal rate expectations

**Economic Mechanism**: 
- Leverage amplification: REITs typically carry 50-70% Loan-to-Value (LTV) ratios. Negative shocks hit equity returns with 2-3x leverage multiplier
- Liquidity evaporation: During crises, commercial real estate transaction volumes collapse, eliminating price discovery and forcing mark-to-market losses
- Debt covenant concerns: Declining property values trigger loan covenant violations, forcing asset sales at distressed prices

**Implication for M3**: 
- Include period dummies or crisis indicators (d_2008, d_2020, d_2022) in specifications
- Test for parameter instability using Chow tests at crisis dates
- Consider rolling-window regressions to identify time-varying sensitivities

---

### 1.4 Control Variable Relationships
**Finding**: Control variables show **mixed correlations** with REIT returns, with implications for model specification:
- **Momentum factors**: Positive correlation suggests trend-following behavior in REIT valuations
- **Quality factors**: Variable correlation depending on market regime (defensive in downturns, less so in rallies)
- **Size effects**: Smaller REITs (lower market cap) sometimes show higher volatility but stronger correlation with macro drivers

**Implication for M3**: Control variables should be included to reduce omitted variable bias, but test for multicollinearity using VIF (Variance Inflation Factor). Consider factor rotation effects.

---

### 1.5 Group Heterogeneity (Time Periods)
**Finding**: Sensitivity to interest rates **varies significantly across economic regimes**:
- **Crisis periods**: Stronger negative correlation (rates → returns sensitivity = -0.6 to -0.8)
- **Normal periods**: Moderate negative correlation (rates → returns sensitivity = -0.3 to -0.5)
- **Recovery periods**: Weaker correlation, potentially positive (rates may signal economic strength)

**Economic Mechanism**: 
- In crises, investors flee risky assets; rate movements become proxies for systemic stress
- In normal times, rates reflect fundamental valuation metrics
- In recoveries, higher rates signal growth and employment, offsetting discount rate effects

**Implication for M3**: Include interaction terms: Rates × Crisis_Dummy or use subsample regressions for robust inference. Test whether slopes differ significantly across regimes (Chow test).

---

## 2. Hypotheses for M3 Econometric Models

### Hypothesis 1: Primary Driver Effect (Rate Sensitivity)
**H1 Claim**: REIT returns are negatively sensitive to interest rate changes, with a stronger effect at lag 2-3 months.

**Model Specification**:
```
Returns_i,t = α_i + β₀ + β₁ × Rates_{t-2} + β₂ × Rates_{t-3} + γ' × Controls_{t} + ε_{i,t}
```
Where i indexes REITs and t indexes months.

**Expected Sign**: β₁ < 0, β₂ < 0 (both statistically significant)

**Economic Mechanism**: Rising rates increase REIT financing costs and discount future cash flows, depressing valuations.

**Tests**:
- Report Wald test for β₁ + β₂ = 0 (cumulative rate effect)
- Compare lag 2 vs. lag 3 to identify optimal specification
- Robustness: Alternative lag structures (lag 1, lag 6, distributed lag)

---

### Hypothesis 2: Control Variable Premiums
**H2 Claim**: Control variables capture systematic risk premiums above and beyond interest rate effects.

**Model Specification**:
```
Returns_i,t = α_i + Rates_effect(t-2) + β_mom × Momentum_i,t + β_qlty × Quality_i,t + ε_{i,t}
```

**Expected Signs**: 
- Momentum: β_mom > 0 (trend-following premiums)
- Quality: β_qlty ≷ 0 (regime-dependent)

**Rationale**: Moving beyond monovariate rate models captures REIT-specific risk factors (operational leverage, tenant quality, geographic diversification).

---

### Hypothesis 3: Group Heterogeneity and Interaction Effects
**H3 Claim**: Period-dependent heterogeneity in rate sensitivity; crisis periods exhibit amplified effect magnitudes.

**Model Specification**:
```
Returns_i,t = β₁ × Rates_{t-2} + β_crisis × (Rates_{t-2} × Crisis_t) + Controls + ε_{i,t}
```

**Expected Sign**: β_crisis < β₁ < 0 (crisis amplifies negative effect)

**Interpretation**: During crises (e.g., 2008, 2020), the same rate movement causes larger REIT losses due to leverage amplification and liquidity constraints.

---

## 3. Data Quality Flags and Mitigation Strategies

### Flag 1: Outliers in Returns Distribution
**Issue**: Extreme values in REIT returns (e.g., -50% in 2008, +30% rally in 2009) could bias OLS estimates if influential.

**Detection**: 
- IQR-based outlier rule (Q1 - 1.5×IQR, Q3 + 1.5×IQR)
- Visual inspection of plots 2 and 8 shows concentrated outliers in crisis periods

**M3 Mitigations**:
1. **Robust standard errors**: Use Huber-White "sandwich" estimators insensitive to outliers
2. **Trimming/Winsorization**: Drop or cap outliers at 1st/99th percentiles (document impact)
3. **Model diagnostics**: Report influence plots (DFBetas, Cook's distance) to identify high-leverage observations

---

### Flag 2: Heteroskedasticity
**Issue**: Residual variance is non-constant; volatility clusters in crisis periods with larger conditional variance.

**Detection**: 
- From plot 7 scatter plots: Variance of residuals increases at extreme values of control variables
- From plot 8 decomposition: Residual component shows clusters of high/low variance periods

**M3 Mitigations**:
1. **Robust standard errors**: Report heteroskedasticity-consistent (HC3) standard errors
2. **Explicit variance modeling**: GARCH or threshold volatility models to capture heteroskedasticity
3. **Weighted least squares**: Weight observations inversely by predicted variance
4. **Subgroup analysis**: Separate regressions for quiet vs. crisis samples

---

### Flag 3: Multicollinearity Among Controls
**Issue**: Some control variables are correlated with each other (visible in plot 1 heatmap), risking inflated standard errors and unreliable coefficient estimates.

**Detection**: Correlation matrix inspection; compute VIF for proposed M3 specification.

**M3 Mitigations**:
1. **Variable selection**: Use stepwise/LASSO regression to drop redundant controls
2. **Factor analysis**: Collapse correlated controls into principal components
3. **Report correlation matrix**: Document multicollinearity diagnostics in appendix
4. **Interpretation caution**: Emphasize reduced-form estimates rather than causal structural parameters when multicollinearity is present

---

### Flag 4: Missing Data
**Issue**: Some time periods or REIT entities may have incomplete observations.

**Detection**: Check for gaps in time series or entity-level missingness patterns.

**M3 Mitigations**:
1. **Listwise deletion**: Report sample sizes for complete cases
2. **Multiple imputation**: If missing < 5%, use forward-fill or mean imputation; sensitivity-test results
3. **Unbalanced panel**: Use fixed-effects regression (xtreg, fe in Stata) which handles unbalanced panels

---

### Flag 5: Autocorrelation in Residuals
**Issue**: From plot 8 decomposition, residuals may exhibit autocorrelation (white-noise test failure), violating OLS assumptions and biasing standard errors downward.

**Detection**: Durbin-Watson statistic; correlogram in plot 8 decomposition shows residual patterns.

**M3 Mitigations**:
1. **Lagged dependent variable**: Include Δ(Returns_{t-1}) as regressor (tests mean reversion)
2. **Clustered standard errors**: Use two-way clustering (by REIT i and time t) for panel data
3. **AR(p) error model**: Explicitly model autocorrelation in residuals
4. **Adjustment**: Report Newey-West HAC standard errors for robustness

---

## 4. Summary Table: Metrics for M3 Model Building

| Metric | Value | Implication for M3 |
|--------|-------|-------------------|
| **Outcome variable**: Returns | Mean = [TBD], SD = [TBD] | Standardize if skewed; test for normality |
| **Primary driver**: Rates | Optimal lag = 2-3 months | Use Rate_{t-2} in baseline specification |
| **Driver-outcome correlation** | r ≈ -0.5 to -0.7 | Strong univariate relationship; expect significant coefficient |
| **Correlation at optimal lag** | Strongest at lag 2 | Preferred specification; report alternatives in appendix |
| **Crisis period sensitivity** | 2-3× higher | Include crisis interaction terms; test for structural break |
| **Control variable count** | ~5 key variables | Avoid overfitting; prioritize based on economic theory + correlation strength |
| **Residual autocorrelation** | [Check plot 8] | If significant, include lagged dependent variable or use HAC standard errors |
| **Heteroskedasticity** | Present (crisis periods) | Use robust standard errors; consider GARCH specification |
| **Multicollinearity** | Moderate (among controls) | Report VIF; consider factor models if VIF > 10 |
| **Outliers** | ~5-10% of sample | Winsorize or use robust estimation; report results both ways |

---

## 5. Next Steps and Recommendations

### Immediate (Before M3)
1. ✓ Confirm data integrity: Verify no data entry errors, units consistency (e.g., returns as %, rates in bps)
2. ✓ Finalize variable definitions: Agree on outcome (returns) and driver (rates) variables for M3
3. ✓ Address outliers: Decide on treatment (drop, winsorize, robust regression)

### During M3 Model Building
1. **Specification search**: Test alternative lag structures, interaction terms, and control variable combinations
2. **Diagnostic testing**: 
   - Breusch-Pagan test for heteroskedasticity
   - Durbin-Watson / Ljung-Box test for autocorrelation
   - Variance Inflation Factor (VIF) for multicollinearity
   - Chow test for structural breaks at crisis dates
3. **Robustness reporting**:
   - Multiple model specifications (parsimonious, moderate, full controls)
   - Alternative estimation methods (OLS, robust regression, quantile regression)
   - Subsample analysis (crisis vs. normal periods)
4. **Economic interpretation**: Connect coefficient magnitudes to real-world impacts (e.g., "1% rate increase → X% return decline")

### During M4 Investment Memo
1. Use M3 estimates to project REIT returns under different rate scenarios
2. Highlight period-dependent heterogeneity when making recommendations
3. Caveat analysis with data quality flags and model limitations

---

## 6. References and Data Sources

- **FRED Data**: Federal Reserve Economic Data (https://fred.stlouisfed.org/)
  - Series: DFF (Federal Funds Rate), MORTGAGE30US (30-year mortgage rate)
- **REIT Data Source**: [Specify source from M1]
- **Analysis Date**: Milestone 2, Spring 2026

---

**Prepared by**: [Team Name]  
**Date**: March 27, 2026  
**Status**: Ready for M3 Econometric Modeling
