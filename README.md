[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22749448&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Project Structure

- **code/** — Python scripts and notebooks. Use `config_paths.py` for paths.
- **data/raw/** — Original data (read-only)
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite

Run `python code/config_paths.py` to verify paths.



Research Question: How sensitive are regional home prices to mortgage rate changes, and do urban and
suburban markets respond differently?
Datasets:
Dataset Source What It Provides
Shiller Home Price
Data
Open Dataset Catalog
(Shiller Data)
FRED pandas-datareader API
Long-run U.S. home price index (national +
metro-level)
30-Year Mortgage Rate, Housing Starts,
Unemployment by state
BLS (Bureau of Labor
Statistics) Open Dataset Catalog Metro-level employment and wage growth
Key Variables:
Outcome: Year-over-year home price growth (%) by metro
2 / 11
Driver: 30-year fixed mortgage rate (lagged 1-3 months)
Controls: Local unemployment rate, wage growth, housing permits
Groups: Urban core vs. suburban vs. rural metros
Why It's Interesting: Mortgage rates went from 3% to 7.5% in 2022-2023 -- the fastest increase in 40 years.
Everyone expected a housing crash. It didn't happen everywhere, and the suburban "Zoom towns" responded
very differently from urban cores. Your analysis tests whether market type predicts rate sensitivity.
