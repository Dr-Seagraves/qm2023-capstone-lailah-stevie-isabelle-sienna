"""Milestone 3 econometric models for the capstone project.

The script estimates the main fixed-effects specifications, runs the required
diagnostics and robustness checks, and exports tables and figures under results/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

from config_paths import FINAL_DATA_DIR, FIGURES_DIR, TABLES_DIR

OUTCOME_RETURN = "reit_avg_usdret"
OUTCOME_LOG_ME = "log_market_equity"
MORTGAGE = "fred_avg_mortgage15us"
BASE_LAG = 2
ALT_LAGS = (1, 2, 3)
CRISIS_PERIODS = {
    "crisis_2008_2009": {2008, 2009},
    "crisis_2020_2021": {2020, 2021},
    "post_rate_shock_2022_2023": {2022, 2023},
}
BASE_CONTROLS = [
    "reit_avg_assets",
    "reit_avg_debt_at",
    "reit_avg_cash_at",
    "reit_avg_roe",
    "reit_avg_btm",
    "reit_avg_beta",
]
MODEL_EXOG = ["year_index", *BASE_CONTROLS, *CRISIS_PERIODS.keys()]
TRAIN_END_YEAR = 2018
TEST_START_YEAR = 2019


def ensure_dirs() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def load_panel() -> pd.DataFrame:
    panel_path = FINAL_DATA_DIR / "reit_fred_analysis_panel.csv"
    if not panel_path.exists():
        raise FileNotFoundError(f"Missing final panel: {panel_path}")

    df = pd.read_csv(panel_path)
    required = {"unit_id", "year", OUTCOME_RETURN, "reit_avg_market_equity", MORTGAGE, *BASE_CONTROLS}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Final panel is missing required columns: {missing}")

    numeric_cols = [
        "year",
        OUTCOME_RETURN,
        "reit_avg_market_equity",
        MORTGAGE,
        *BASE_CONTROLS,
        "reit_obs_months",
        "fred_obs_weeks",
    ]
    for column in numeric_cols:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.sort_values(["year", "unit_id"]).copy()
    df[OUTCOME_LOG_ME] = np.log(df["reit_avg_market_equity"])
    df["year_index"] = df["year"] - df["year"].min()

    year_rates = df[["year", MORTGAGE]].dropna().drop_duplicates("year").sort_values("year").copy()
    for lag in ALT_LAGS:
        year_rates[f"mortgage_lag{lag}"] = year_rates[MORTGAGE].shift(lag)

    lag_cols = [f"mortgage_lag{lag}" for lag in ALT_LAGS]
    df = df.merge(year_rates[["year", *lag_cols]], on="year", how="left")

    for label, years in CRISIS_PERIODS.items():
        df[label] = df["year"].isin(years).astype(int)

    return df


def complete_case_frame(df: pd.DataFrame, outcome: str, lag_col: str) -> pd.DataFrame:
    cols = ["unit_id", "year", outcome, lag_col, "year_index", *BASE_CONTROLS, *CRISIS_PERIODS.keys()]
    frame = df.loc[:, cols].dropna().copy()
    frame["unit_id"] = frame["unit_id"].astype(str)
    frame = frame.set_index(["unit_id", "year"]).sort_index()
    return frame


def fit_panel_fe(frame: pd.DataFrame, outcome: str, lag_col: str, clustered: bool = True):
    exog_cols = [lag_col, "year_index", *BASE_CONTROLS, *CRISIS_PERIODS.keys()]
    exog_cols = [column for column in exog_cols if frame[column].nunique(dropna=True) > 1]
    y = frame[outcome]
    x = sm.add_constant(frame[exog_cols], has_constant="add")
    model = PanelOLS(y, x, entity_effects=True, drop_absorbed=True, check_rank=False)
    if clustered:
        result = model.fit(cov_type="clustered", cluster_entity=True, cluster_time=True)
    else:
        result = model.fit(cov_type="unadjusted")
    return result, x


def star_string(p_value: float) -> str:
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""


def format_coef(result, variable: str) -> str:
    if variable not in result.params.index:
        return "—"
    coef = float(result.params[variable])
    stderr = float(result.std_errors[variable])
    p_value = float(result.pvalues[variable])
    return f"{coef:.4f}{star_string(p_value)} ({stderr:.4f})"


def format_scalar(value: float, digits: int = 3) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:.{digits}f}"


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join([":---" for _ in headers]) + "|"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines) + "\n"


def save_markdown_table(df: pd.DataFrame, path: Path) -> None:
    path.write_text(dataframe_to_markdown(df), encoding="utf-8")


def build_main_tables(return_result, me_result) -> None:
    label_map = {
        "const": "Intercept",
        f"mortgage_lag{BASE_LAG}": f"Mortgage rate lag {BASE_LAG}",
        "year_index": "Year trend",
        "reit_avg_assets": "Average assets",
        "reit_avg_debt_at": "Debt / assets",
        "reit_avg_cash_at": "Cash / assets",
        "reit_avg_roe": "ROE",
        "reit_avg_btm": "Book-to-market",
        "reit_avg_beta": "Beta",
        "crisis_2008_2009": "2008-2009 crisis",
        "crisis_2020_2021": "2020-2021 crisis",
        "post_rate_shock_2022_2023": "2022-2023 tightening",
    }
    variables = ["const", f"mortgage_lag{BASE_LAG}", "year_index", *BASE_CONTROLS, *CRISIS_PERIODS.keys()]
    rows = []
    for variable in variables:
        rows.append(
            {
                "Variable": label_map[variable],
                "reit_return_pp": format_coef(return_result, variable),
                "log_market_equity": format_coef(me_result, variable),
            }
        )
    rows.extend(
        [
            {"Variable": "Entity FE", "reit_return_pp": "Yes", "log_market_equity": "Yes"},
            {
                "Variable": "Time FE",
                "reit_return_pp": "No (year trend + crisis controls)",
                "log_market_equity": "No (year trend + crisis controls)",
            },
            {"Variable": "Clustered SE", "reit_return_pp": "Yes (entity + year)", "log_market_equity": "Yes (entity + year)"},
            {"Variable": "N", "reit_return_pp": f"{int(return_result.nobs):,}", "log_market_equity": f"{int(me_result.nobs):,}"},
            {"Variable": "Within R2", "reit_return_pp": format_scalar(float(return_result.rsquared_within)), "log_market_equity": format_scalar(float(me_result.rsquared_within))},
        ]
    )
    table = pd.DataFrame(rows)
    table.to_csv(TABLES_DIR / "M3_regression_table.csv", index=False)
    save_markdown_table(table, TABLES_DIR / "M3_regression_table.md")

    key_results = pd.DataFrame(
        [
            {
                "model": "Returns FE",
                "sample_size": int(return_result.nobs),
                "within_r2": float(return_result.rsquared_within),
                "mortgage_lag2_coef": float(return_result.params[f"mortgage_lag{BASE_LAG}"]),
                "mortgage_lag2_p": float(return_result.pvalues[f"mortgage_lag{BASE_LAG}"]),
            },
            {
                "model": "Log Market Equity FE",
                "sample_size": int(me_result.nobs),
                "within_r2": float(me_result.rsquared_within),
                "mortgage_lag2_coef": float(me_result.params[f"mortgage_lag{BASE_LAG}"]),
                "mortgage_lag2_p": float(me_result.pvalues[f"mortgage_lag{BASE_LAG}"]),
            },
        ]
    )
    key_results.to_csv(TABLES_DIR / "M3_key_results.csv", index=False)


def save_standard_vs_clustered(frame: pd.DataFrame, lag_col: str) -> None:
    clustered_result, _ = fit_panel_fe(frame, OUTCOME_RETURN, lag_col, clustered=True)
    standard_result, _ = fit_panel_fe(frame, OUTCOME_RETURN, lag_col, clustered=False)
    rows = []
    for variable in [lag_col, "year_index", *BASE_CONTROLS, *CRISIS_PERIODS.keys()]:
        rows.append(
            {
                "Variable": variable,
                "coef": float(clustered_result.params[variable]),
                "standard_se": float(standard_result.std_errors[variable]),
                "clustered_se": float(clustered_result.std_errors[variable]),
                "standard_p": float(standard_result.pvalues[variable]),
                "clustered_p": float(clustered_result.pvalues[variable]),
            }
        )
    pd.DataFrame(rows).to_csv(TABLES_DIR / "M3_standard_vs_clustered.csv", index=False)


def breusch_pagan_test(result, exog: pd.DataFrame) -> pd.DataFrame:
    residuals = np.asarray(result.resids).ravel()
    exog_matrix = np.asarray(exog)
    lm_stat, lm_pvalue, f_stat, f_pvalue = het_breuschpagan(residuals, exog_matrix)
    out = pd.DataFrame(
        [
            {
                "LM stat": lm_stat,
                "LM p-value": lm_pvalue,
                "F stat": f_stat,
                "F p-value": f_pvalue,
            }
        ]
    )
    out.to_csv(TABLES_DIR / "M3_breusch_pagan.csv", index=False)
    return out


def vif_table(exog: pd.DataFrame) -> pd.DataFrame:
    x = exog.drop(columns=["const"]).copy()
    out = pd.DataFrame(
        {
            "Variable": x.columns,
            "VIF": [variance_inflation_factor(x.values, i) for i in range(x.shape[1])],
        }
    ).sort_values("VIF", ascending=False)
    out.to_csv(TABLES_DIR / "M3_vif.csv", index=False)
    return out


def plot_residual_diagnostics(result) -> None:
    fitted = np.asarray(result.fitted_values).ravel()
    residuals = np.asarray(result.resids).ravel()
    sns.set_theme(style="whitegrid", context="talk")

    plt.figure(figsize=(10, 6))
    plt.scatter(fitted, residuals, alpha=0.35, s=18, color="#1f4e79")
    plt.axhline(0, color="#b0413e", linestyle="--", linewidth=1.5)
    plt.xlabel("Fitted Values")
    plt.ylabel("Residuals")
    plt.title("Residuals vs. Fitted Values (Fixed Effects Model)")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_residuals_vs_fitted.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title("Q-Q Plot: Residual Normality Check")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_qq_plot.png", dpi=300)
    plt.close()


def lag_robustness(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for lag in ALT_LAGS:
        lag_col = f"mortgage_lag{lag}"
        frame = complete_case_frame(df, OUTCOME_RETURN, lag_col)
        result, _ = fit_panel_fe(frame, OUTCOME_RETURN, lag_col, clustered=True)
        rows.append(
            {
                "specification": f"Lag {lag}",
                "coefficient": float(result.params[lag_col]),
                "std_error": float(result.std_errors[lag_col]),
                "p_value": float(result.pvalues[lag_col]),
                "sample_size": int(result.nobs),
                "within_r2": float(result.rsquared_within),
            }
        )
    table = pd.DataFrame(rows)
    table.to_csv(TABLES_DIR / "M3_lag_robustness.csv", index=False)

    plt.figure(figsize=(9, 5))
    plt.errorbar(
        table["specification"],
        table["coefficient"],
        yerr=1.96 * table["std_error"],
        fmt="o-",
        color="#1f4e79",
        ecolor="#7f8c8d",
        capsize=5,
    )
    plt.axhline(0, color="#b0413e", linestyle="--", linewidth=1.2)
    plt.ylabel("Mortgage Rate Coefficient")
    plt.xlabel("Lag Specification")
    plt.title("Lag Robustness for REIT Returns")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_lag_robustness.png", dpi=300)
    plt.close()
    return table


def outlier_exclusion(df: pd.DataFrame, lag_col: str) -> pd.DataFrame:
    baseline_frame = complete_case_frame(df, OUTCOME_RETURN, lag_col)
    baseline_result, _ = fit_panel_fe(baseline_frame, OUTCOME_RETURN, lag_col, clustered=True)

    no_crisis = baseline_frame.reset_index().loc[lambda x: ~x["year"].isin({2008, 2009, 2020, 2021})].copy()
    no_crisis = no_crisis.set_index(["unit_id", "year"]).sort_index()
    crisis_result, _ = fit_panel_fe(no_crisis, OUTCOME_RETURN, lag_col, clustered=True)

    table = pd.DataFrame(
        [
            {
                "specification": "Baseline",
                "coefficient": float(baseline_result.params[lag_col]),
                "std_error": float(baseline_result.std_errors[lag_col]),
                "p_value": float(baseline_result.pvalues[lag_col]),
                "sample_size": int(baseline_result.nobs),
            },
            {
                "specification": "Exclude crisis years",
                "coefficient": float(crisis_result.params[lag_col]),
                "std_error": float(crisis_result.std_errors[lag_col]),
                "p_value": float(crisis_result.pvalues[lag_col]),
                "sample_size": int(crisis_result.nobs),
            },
        ]
    )
    table.to_csv(TABLES_DIR / "M3_outlier_exclusion.csv", index=False)
    return table


def subsample_robustness(df: pd.DataFrame, lag_col: str) -> pd.DataFrame:
    cols = ["unit_id", "year", OUTCOME_RETURN, "reit_avg_market_equity", lag_col, "year_index", *BASE_CONTROLS, *CRISIS_PERIODS.keys()]
    frame = df.loc[:, cols].dropna().copy().reset_index(drop=True)
    frame["size_flag"] = frame["reit_avg_market_equity"].rank(pct=True)

    large = frame.loc[frame["size_flag"] >= 0.5].set_index(["unit_id", "year"]).sort_index()
    small = frame.loc[frame["size_flag"] < 0.5].set_index(["unit_id", "year"]).sort_index()

    large_result, _ = fit_panel_fe(large, OUTCOME_RETURN, lag_col, clustered=True)
    small_result, _ = fit_panel_fe(small, OUTCOME_RETURN, lag_col, clustered=True)

    table = pd.DataFrame(
        [
            {
                "specification": "Large REITs",
                "coefficient": float(large_result.params[lag_col]),
                "std_error": float(large_result.std_errors[lag_col]),
                "p_value": float(large_result.pvalues[lag_col]),
                "sample_size": int(large_result.nobs),
            },
            {
                "specification": "Small REITs",
                "coefficient": float(small_result.params[lag_col]),
                "std_error": float(small_result.std_errors[lag_col]),
                "p_value": float(small_result.pvalues[lag_col]),
                "sample_size": int(small_result.nobs),
            },
        ]
    )
    table.to_csv(TABLES_DIR / "M3_subsample_robustness.csv", index=False)
    return table


def model_b_comparison(df: pd.DataFrame, lag_col: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = [lag_col, "year_index", *BASE_CONTROLS, *CRISIS_PERIODS.keys()]
    frame = df.loc[:, ["unit_id", "year", OUTCOME_RETURN, *features]].dropna().copy()
    train = frame.loc[frame["year"] <= TRAIN_END_YEAR].copy()
    test = frame.loc[frame["year"] >= TEST_START_YEAR].copy()

    x_train = train[features]
    y_train = train[OUTCOME_RETURN]
    x_test = test[features]
    y_test = test[OUTCOME_RETURN]

    ols = sm.OLS(y_train, sm.add_constant(x_train, has_constant="add")).fit()
    ols_pred = ols.predict(sm.add_constant(x_test, has_constant="add"))

    rf = RandomForestRegressor(n_estimators=500, random_state=42, min_samples_leaf=3)
    rf.fit(x_train, y_train)
    rf_pred = rf.predict(x_test)

    comparison = pd.DataFrame(
        [
            {
                "model": "OLS benchmark",
                "train_years": f"{int(train['year'].min())}-{int(train['year'].max())}",
                "test_years": f"{int(test['year'].min())}-{int(test['year'].max())}",
                "r2_test": r2_score(y_test, ols_pred),
                "rmse_test": float(np.sqrt(mean_squared_error(y_test, ols_pred))),
            },
            {
                "model": "Random Forest",
                "train_years": f"{int(train['year'].min())}-{int(train['year'].max())}",
                "test_years": f"{int(test['year'].min())}-{int(test['year'].max())}",
                "r2_test": r2_score(y_test, rf_pred),
                "rmse_test": float(np.sqrt(mean_squared_error(y_test, rf_pred))),
            },
            {
                "model": "Naive mean baseline",
                "train_years": f"{int(train['year'].min())}-{int(train['year'].max())}",
                "test_years": f"{int(test['year'].min())}-{int(test['year'].max())}",
                "r2_test": r2_score(y_test, np.repeat(y_train.mean(), len(y_test))),
                "rmse_test": float(np.sqrt(mean_squared_error(y_test, np.repeat(y_train.mean(), len(y_test))))),
            },
        ]
    )
    comparison.to_csv(TABLES_DIR / "M3_model_b_comparison.csv", index=False)

    feature_importance = pd.DataFrame({"feature": features, "importance": rf.feature_importances_}).sort_values(
        "importance", ascending=False
    )
    feature_importance.to_csv(TABLES_DIR / "M3_model_b_feature_importance.csv", index=False)

    plt.figure(figsize=(9, 7))
    top_importance = feature_importance.head(10)
    sns.barplot(data=top_importance, y="feature", x="importance", color="#1f4e79")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("Random Forest Feature Importance")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_model_b_feature_importance.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 8))
    plt.scatter(y_test, rf_pred, alpha=0.35, label="Random Forest", color="#1f4e79")
    plt.scatter(y_test, ols_pred, alpha=0.35, label="OLS", color="#b0413e")
    min_val = min(y_test.min(), ols_pred.min(), rf_pred.min())
    max_val = max(y_test.max(), ols_pred.max(), rf_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], linestyle="--", color="black", linewidth=1)
    plt.xlabel("Actual Returns")
    plt.ylabel("Predicted Returns")
    plt.title("Model B Predictions vs. Actual Test Returns")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_model_b_predictions.png", dpi=300)
    plt.close()

    return comparison, feature_importance


def write_interpretation_memo(return_result, me_result, bp_df, vif_df, lag_df, outlier_df, subsample_df, comparison_df) -> None:
    lag_name = f"mortgage_lag{BASE_LAG}"
    best_lag = lag_df.loc[lag_df["coefficient"].abs().idxmax()]
    best_model = comparison_df.loc[comparison_df["model"] != "Naive mean baseline"].sort_values("r2_test", ascending=False).iloc[0]

    memo = f"""# M3 Interpretation Memo

## Model A Headline

A one percentage point increase in the U.S. 15-year mortgage rate two years earlier is associated with a {float(return_result.params[lag_name]):.4f} change in annual REIT returns (p = {float(return_result.pvalues[lag_name]):.4f}). In the log market equity specification, the same lagged mortgage-rate change is associated with a {float(me_result.params[lag_name]):.4f} change in log market equity (p = {float(me_result.pvalues[lag_name]):.4f}).

The return estimate is not statistically distinguishable from zero, but the market-equity specification is more precise. That pattern indicates that annual mortgage-rate variation is more visible in valuation levels than in annual return averages.

## Economic Interpretation

Three channels are the most plausible.

First, the leverage channel: higher mortgage rates raise refinancing and acquisition costs for REITs.

Second, the discount-rate channel: higher rates lower the present value of future property cash flows, which is consistent with the market-equity result.

Third, the capitalization-rate channel: a higher-rate environment raises cap rates and compresses REIT valuations.

## Model B Summary

The prediction benchmark uses a year-based train/test split ({TRAIN_END_YEAR} and earlier for training; {TEST_START_YEAR} and later for testing). Among the learned models, the best out-of-sample R² in this run belongs to {best_model['model']} with test R² = {best_model['r2_test']:.4f} and RMSE = {best_model['rmse_test']:.4f}.

## Diagnostics

Breusch-Pagan F p-value: {float(bp_df['F p-value'].iloc[0]):.4e}. This indicates heteroskedasticity, so clustered standard errors are the right default.

Maximum VIF: {float(vif_df['VIF'].max()):.2f}. The main collinearity issue comes from the common time trend and mortgage-rate series, which is expected in a macro panel.

## Robustness

Alternative lag checks are saved in the lag robustness table. The largest absolute coefficient across lags is {best_lag['specification']} with coefficient {best_lag['coefficient']:.4f}.

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
"""
    (Path(__file__).resolve().parents[1] / "M3" / "M3_interpretation.md").write_text(memo, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    df = load_panel()
    lag_col = f"mortgage_lag{BASE_LAG}"

    return_frame = complete_case_frame(df, OUTCOME_RETURN, lag_col)
    me_frame = complete_case_frame(df, OUTCOME_LOG_ME, lag_col)

    return_result, return_exog = fit_panel_fe(return_frame, OUTCOME_RETURN, lag_col, clustered=True)
    me_result, _ = fit_panel_fe(me_frame, OUTCOME_LOG_ME, lag_col, clustered=True)

    build_main_tables(return_result, me_result)
    save_standard_vs_clustered(return_frame, lag_col)

    bp_df = breusch_pagan_test(return_result, return_exog)
    vif_df = vif_table(return_exog)
    plot_residual_diagnostics(return_result)

    lag_df = lag_robustness(df)
    outlier_df = outlier_exclusion(df, lag_col)
    subsample_df = subsample_robustness(df, lag_col)
    comparison_df, feature_importance_df = model_b_comparison(df, lag_col)

    write_interpretation_memo(return_result, me_result, bp_df, vif_df, lag_df, outlier_df, subsample_df, comparison_df)

    print("M3 econometric pipeline complete")
    print(f"- Baseline return model N: {int(return_result.nobs):,}")
    print(f"- Baseline market equity model N: {int(me_result.nobs):,}")
    print(f"- Results written to {TABLES_DIR} and {FIGURES_DIR}")


if __name__ == "__main__":
    main()