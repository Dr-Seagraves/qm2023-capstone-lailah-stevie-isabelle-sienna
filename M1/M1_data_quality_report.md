# M1 Data Quality Report

## Project
- Team: Lailah, Stevie, Isabelle, Sienna
- Research question: How do changes in U.S. 15-year mortgage rates relate to REIT performance and firm-level characteristics over time?

## 1) Data Sources (Primary + Supplementary)

### Primary source: REIT panel
- File: `data/raw/REIT_sample_2000_2024_All_Variables.csv`
- Unit/time granularity in source: firm-month observations
- Raw rows/columns: 48,019 rows, 22 columns
- Standardized raw extract: `data/raw/reit_raw.csv` (48,019 rows, 20 columns)
- Cleaned output: `data/processed/reit_clean.csv` (4,335 rows, 21 columns)
- Cleaned unit/time granularity: entity-year (`unit_id=permno`, `year`)

### Supplementary source: FRED mortgage rates
- File: `data/raw/MORTGAGE15US.csv`
- Unit/time granularity in source: weekly U.S. time series
- Raw rows/columns: 1,252 rows, 2 columns
- Standardized raw extract: `data/raw/fred_raw.csv` (1,252 rows, 2 columns)
- Cleaned output: `data/processed/fred_clean.csv` (24 rows, 6 columns)
- Cleaned unit/time granularity: year-level macro controls

## 2) Cleaning Decisions (with counts + economic justification)

### REIT cleaning decisions
1. **Entity-year aggregation (month → year):**
   - Before: 48,019 monthly rows
   - After: 4,335 entity-year rows
   - Economic justification: annual panels reduce high-frequency noise and align with annual accounting fields (assets, sales, net income), making regression coefficients easier to interpret in a macro-finance setting.

2. **Key validation and deduplication (`unit_id`, `year`):**
   - Missing keys in cleaned REIT data: 0
   - Duplicate entity-year keys in cleaned REIT data: 0
   - Economic justification: one firm-year per observation avoids pseudo-replication and prevents biased standard errors from duplicate panel records.

3. **Numeric standardization:**
   - Converted financial/risk inputs to numeric and aggregated annual means for variables including returns, price, market equity, assets, sales, income, leverage/liquidity ratios, valuation, and beta.
   - Economic justification: consistent numeric types are required for valid model estimation and comparable effect sizes.

### FRED cleaning decisions
1. **Weekly-to-annual transformation:**
   - Before: 1,252 weekly rows
   - After: 24 annual rows (2000–2023)
   - Economic justification: annual macro controls match the panel year index and reduce frequency mismatch bias.

2. **Supplementary feature expansion:**
   - Created `fred_avg_mortgage15us`, `fred_min_mortgage15us`, `fred_max_mortgage15us`, `fred_std_mortgage15us`, and `fred_obs_weeks`.
   - Economic justification: average, dispersion, and range capture both level and volatility of financing conditions that may affect REIT outcomes.

## 3) Merge Strategy and Verification

### Merge strategy
- Base table: `data/processed/reit_clean.csv`
- Supplementary table: `data/processed/fred_clean.csv`
- Join rule: **inner join on `year`** (to ensure complete supplementary controls in final analysis file)
- Script: `code/merge_final_panel.py`

### Merge verification results
- REIT cleaned rows before merge: 4,335
- Final merged rows: 2,965
- Rows dropped at merge: 1,370 (**31.6%**) due to non-overlapping years
- Year coverage change: REIT 1986–2024 (39 years) → Final 2000–2023 (24 years)
- Entity counts: 369 (REIT cleaned) → 286 (final), entities lost: 83
- Final key integrity:
  - Missing `unit_id`/`year`: 0
  - Duplicate (`unit_id`, `year`) keys: 0

## 4) Final Dataset Summary (sample statistics)

- Final dataset: `data/final/reit_fred_analysis_panel.csv`
- Shape: 2,965 rows × 26 columns
- Structure: long panel (Entity × Time)
- Entities: 286
- Years: 2000–2023 (24 years)

### Key variable sample statistics
- `reit_avg_usdret`: n=2,954, mean=0.0114, min=-0.2734, max=0.2851
- `reit_avg_market_equity`: n=2,965, mean=4,269.9614, min=10.3437, max=118,259.0740
- `reit_avg_assets`: n=2,955, mean=4,442.8889, min=1.4132, max=82,438.9730
- `reit_avg_net_income`: n=2,944, mean=105.6937, min=-1,403.4568, max=4,383.9118
- `fred_avg_mortgage15us`: n=2,965, mean=4.3676, min=2.2719, max=7.7183

### Missingness snapshot in final dataset
- `reit_avg_usdret`: 11 missing (0.37%)
- `reit_avg_market_equity`: 0 missing (0.00%)
- `reit_avg_assets`: 10 missing (0.34%)
- `reit_avg_sales`: 21 missing (0.71%)
- `reit_avg_net_income`: 21 missing (0.71%)
- `reit_avg_roe`: 170 missing (5.73%)
- `reit_avg_beta`: 220 missing (7.42%)
- `fred_avg_mortgage15us`: 0 missing (0.00%)

## 5) Reproducibility Checklist

- [x] Raw source files are stored in `data/raw/`
- [x] Path management uses `code/config_paths.py` (relative paths)
- [x] Primary cleaning script documented: `code/fetch_reit_data.py`
- [x] Supplementary cleaning script documented: `code/fetch_fred_data.py`
- [x] Merge script documented: `code/merge_final_panel.py`
- [x] Final analysis dataset produced at `data/final/reit_fred_analysis_panel.csv`
- [x] Key integrity checks run (missing/duplicate key checks)
- [x] Summary statistics printed during pipeline execution

## 6) Ethical Considerations (What data are we losing?)

1. **Time-period exclusion risk:**
   - Inner-join merge removes all REIT observations outside FRED overlap years (2000–2023), dropping 1,370 rows and 15 years of REIT history.
   - Risk: conclusions may not generalize to pre-2000 or post-2023 market conditions.

2. **Entity composition shift:**
   - 83 entities are lost after merge due to year overlap restrictions.
   - Risk: survivorship/composition effects can bias estimated relationships if dropped entities differ systematically (size, leverage, risk).

3. **Missing financial-ratio fields:**
   - Variables like ROE and beta retain non-trivial missingness.
   - Risk: complete-case modeling may overrepresent firms with richer reporting histories.

4. **Aggregation trade-off:**
   - Monthly/weekly dynamics are summarized into annual measures.
   - Risk: short-run shocks and timing effects are muted, which may understate volatility-linked mechanisms.

Mitigation approach for later milestones: report sample restrictions explicitly, run sensitivity checks (e.g., alternative merge rule or restricted balanced years), and compare results with/without high-missingness variables.
