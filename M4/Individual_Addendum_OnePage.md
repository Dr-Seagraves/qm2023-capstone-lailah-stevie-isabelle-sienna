Individual Addendum — QM 2023 Capstone
Name: [Your Name]    Team: Lailah, Stevie, Isabelle, Sienna    Date: May 1, 2026

Research question
How do changes in U.S. 15‑year mortgage rates relate to REIT performance and firm characteristics over time?

Short answer (empirical, M1–M4)
- Sample: 286 REITs, 2000–2023, final panel n = 2,965 (analysis n ≈ 2,428 for returns).
- Main finding: Higher 15‑year mortgage rates are associated with weaker REIT valuations but not with statistically significant changes in annual REIT returns.
  - REIT annual return (FE baseline, lag 2): coef = -0.0007, p = 0.8955 (NS).
  - Log market equity (FE baseline, lag 2): coef = -0.1141, p = 0.0021 (significant).
- Interpretation: Rate shocks transmit primarily through valuation channels (discount‑rate, refinancing/cap‑rate effects). Firm finance characteristics (debt/assets, cash/assets, book‑to‑market) predict valuation levels.

My contributions (concise, by milestone)
- M1 (Data pipeline): implemented cleaning, annual aggregation, and merge verification; documented sample attrition (31.6% rows dropped; 83 entities lost). Hours: [__].
- M2 (EDA): produced lag analysis and EDA summaries that informed lag choice and crisis controls; documented data‑quality flags. Hours: [__].
- M3 (Econometrics): implemented FE pipeline (`code/capstone_models.py`), diagnostics (Breusch‑Pagan, VIF), and robustness checks (lags, crisis exclusion, subsamples, TWFE absorption). Hours: [__].
- M4 (Memo): wrote interpretation language tying M3 outputs to investment implications and limitations; synchronized tables/figures. Hours: [__].

Defended methodological decision (one line)
- Use entity FE + year trend + crisis indicators with two‑way clustered SEs: preserves estimability of a national annual mortgage regressor (strict two‑way FE would absorb it), while providing conservative inference (see `results/tables/M3_twfe_absorption_check.csv`).

Primary limitation (one line)
- Annual aggregation and a national regressor limit high‑frequency identification of return dynamics; valuation effects are clearer than return predictability. Mitigation: higher‑frequency analysis or interactions with firm refinancing exposure.

AI use (brief)
- GitHub Copilot assisted with coding and documentation; all outputs and interpretations were validated by the team (see `AI_AUDIT_APPENDIX.md`).

Attestation
I certify the statements above are accurate to the best of my knowledge.
Signature: ________________________    Date: ___________

Notes to finalize before PDF export
- Replace bracketed fields with your name/hours/percentage.
- Export filename: Individual_Addendum_[YourLastName].pdf
- For a one‑page PDF: 11–12 pt font, 1" margins, single column; keep text unchanged.
