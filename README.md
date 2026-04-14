[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22749448&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Team Members and Roles

- Lailah — Project coordination and report integration
- Stevie — Data acquisition and cleaning pipeline
- Isabelle — Exploratory analysis and visualization
- Sienna — Documentation, QA checks, and reproducibility

## Research Question

How do U.S. REIT performance metrics vary with changes in U.S. 15-year mortgage rates over time?  
This project builds a year-level panel to evaluate whether rate environments are associated with systematic differences in average REIT returns and market equity.

## Dataset Overview

### Primary Dataset (REIT)
- Source file: `data/raw/REIT_sample_2000_2024_All_Variables.csv`
- Script: `code/fetch_reit_data.py`
- Clean output: `data/processed/reit_clean.csv`
- Key variables used: `usdret`, `market_equity`, `date` → annual `year`

### Supplementary Dataset (FRED)
- Source file: `data/raw/MORTGAGE15US.csv`
- Script: `code/fetch_fred_data.py`
- Clean output: `data/processed/fred_clean.csv`
- Key variable used: `MORTGAGE15US` (weekly) → annual average by `year`

## Preliminary Hypotheses

1. Higher average mortgage rates are associated with lower average annual REIT returns.
2. Higher mortgage-rate environments are associated with lower average REIT market equity.
3. Years with large increases in mortgage rates show weaker REIT outcomes than stable-rate years.
4. The REIT–rate relationship is not constant over time and may vary across macroeconomic periods.

## Project Structure

- **code/** — Project scripts. Use `config_paths.py` for relative paths.
	- `fetch_reit_data.py` — Fetch + clean primary REIT dataset
	- `fetch_fred_data.py` — Fetch + clean supplementary FRED dataset
	- `merge_final_panel.py` — Merge processed datasets into final panel
- **data/raw/** — Raw source files + standardized raw extracts
- **data/processed/** — Cleaned dataset outputs (`*_clean.csv`)
- **data/final/** — Final merged panel + data dictionary
- **results/figures/** — Visualizations
- **results/tables/** — Summary tables/regression tables
- **results/reports/** — Milestone writeups
- **tests/** — Test placeholders

Run `python code/config_paths.py` to verify paths.

## How to Run the Pipeline (Step-by-Step)

Run scripts from the project root:

1. Verify project paths and directories:
	- `python code/config_paths.py`
2. Build primary cleaned dataset from REIT source:
	- `python code/fetch_reit_data.py`
3. Build supplementary cleaned dataset from FRED source:
	- `python code/fetch_fred_data.py`
4. Merge cleaned files into final analysis panel:
	- `python code/merge_final_panel.py`

## Key Outputs

- Raw extracts:
- `data/raw/reit_raw.csv`
- `data/raw/fred_raw.csv`
- Processed datasets:
- `data/processed/reit_clean.csv`
- `data/processed/fred_clean.csv`
- Final panel:
- `data/final/reit_fred_analysis_panel.csv`

## Milestone 3 Econometric Analysis

The M3 submission is built around `code/capstone_models.py`, which estimates panel fixed-effects models for annual REIT returns and log market equity against lagged U.S. 15-year mortgage rates and firm controls.

### M3 Deliverables

- [Milestone 3 full report](M3/Milestone%203:%20Econometric%20Models)
- [M3 interpretation memo](M3/M3_interpretation.md) - narrative interpretation of the econometric results
- `results/tables/M3_regression_table.csv` and `results/tables/M3_regression_table.md` - main Model A results
- `results/tables/M3_breusch_pagan.csv` and `results/tables/M3_vif.csv` - diagnostics
- `results/tables/M3_lag_robustness.csv`, `results/tables/M3_outlier_exclusion.csv`, and `results/tables/M3_subsample_robustness.csv` - robustness checks
- `results/tables/M3_standard_vs_clustered.csv` - standard error comparison
- `results/tables/M3_model_b_comparison.csv` and `results/tables/M3_model_b_feature_importance.csv` - predictive benchmark
- `results/figures/M3_residuals_vs_fitted.png`, `results/figures/M3_qq_plot.png`, `results/figures/M3_lag_robustness.png`, `results/figures/M3_model_b_predictions.png`, and `results/figures/M3_model_b_feature_importance.png` - required plots

### M3 Model Summary

- Returns FE sample size: 2,428
- Log market equity FE sample size: 2,429
- Mortgage-rate coefficient in returns model: -0.0007 with p = 0.8955
- Mortgage-rate coefficient in log market equity model: -0.1141 with p = 0.0021
- Breusch-Pagan test: strong evidence of heteroskedasticity, so clustered standard errors are used
