# Data Dictionary

This file defines variables in the final analysis panel (`dataset_analysis_panel.csv`).

## Panel Keys

| Variable | Type | Description |
|---|---|---|
| `unit_id` | string | Cross-sectional unit identifier (e.g., city, school district, county). |
| `year` | integer | Calendar year for the observation. |

## Dataset-Specific Variables

| Variable | Type | Source | Description |
|---|---|---|---|
| `dataset1_value` | numeric | `dataset1_clean.csv` | Primary outcome or explanatory variable from dataset 1. |
| `dataset2_value` | numeric | `dataset2_clean.csv` | Supplementary variable from dataset 2. |
| `dataset3_value` | numeric | `dataset3_clean.csv` (optional) | Optional supplementary variable from dataset 3. |

## Notes

- Update this dictionary as variable names are finalized.
- If units or transformations are applied (e.g., log, z-score), document them here.
