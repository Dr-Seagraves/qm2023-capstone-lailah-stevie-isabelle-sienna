# 🎯 How to Generate All 8 Required M2 Plots

## Quick Overview

I've created everything you need to generate all 8 required M2 plots. You have **2 options**:

### **Option 1: Use Jupyter Notebook (RECOMMENDED) ✨**
### **Option 2: Run Python Script (Alternative)**

---

## 📌 Option 1: Generate Plots in Jupyter Notebook (EASIEST)

### Step-by-Step Instructions:

1. **Open the Jupyter Notebook** in VS Code
   - File: `capstone_eda.ipynb`
   - Location: `/workspaces/qm2023-capstone-lailah-stevie-isabelle-sienna/`

2. **Select Python Kernel**
   - Jupyter will prompt you to select a kernel
   - Choose "Python 3" or the default available kernel

3. **Execute All Cells**
   - Top menu: **Kernel → Restart & Run All**
   - OR: Use keyboard shortcut (depends on your setup)

4. **Wait for Completion** (takes 2-5 minutes)
   - Each plot will be generated and displayed in the notebook
   - Output confirms: "Plot X saved: M2_0X_*.png"

5. **Verify Plots Were Created**
   - Check folder: `results/figures/`
   - Should contain 8 PNG files:
     - M2_01_correlation_heatmap.png
     - M2_02_timeseries_outcome.png
     - M2_03_dualaxis_comovement.png
     - M2_04_lagged_effects.png
     - M2_05_group_boxplots.png
     - M2_06_sensitivity_analysis.png
     - M2_07_scatter_controls.png
     - M2_08_decomposition.png

---

## 📌 Option 2: Run Python Script (ALTERNATIVE)

If the Jupyter notebook doesn't work, use the standalone script:

### Prerequisites:
Install required packages (one-time only):
```bash
pip install pandas numpy matplotlib seaborn statsmodels
```

### Run the Script:

**In Terminal, execute:**
```bash
cd /workspaces/qm2023-capstone-lailah-stevie-isabelle-sienna
python3 generate_plots.py
```

**Expected Output:**
```
================================================================================
MILESTONE 2: EDA DASHBOARD - PLOT GENERATION
================================================================================

📂 Loading data from: .../data/final/reit_fred_analysis_panel.csv
✓ Dataset loaded: 3456 rows × 25 columns

📊 Variable Classification:
   Outcome variables: ['reit_avg_usdret']
   Driver variables: ['fred_avg_mortgage15us']
   Control variables: 22 identified

[1/8] Generating Correlation Heatmap...
   ✓ Saved: M2_01_correlation_heatmap.png
[2/8] Generating Time Series...
   ✓ Saved: M2_02_timeseries_outcome.png
[3/8] Generating Dual-Axis Comovement Plot...
   ✓ Saved: M2_03_dualaxis_comovement.png
[4/8] Generating Lagged Effects Analysis...
   ✓ Saved: M2_04_lagged_effects.png
[5/8] Generating Group Box Plots...
   ✓ Saved: M2_05_group_boxplots.png
[6/8] Generating Sensitivity Analysis...
   ✓ Saved: M2_06_sensitivity_analysis.png
[7/8] Generating Scatter Plots...
   ✓ Saved: M2_07_scatter_controls.png
[8/8] Generating Time Series Decomposition...
   ✓ Saved: M2_08_decomposition.png

================================================================================
✅ PLOT GENERATION COMPLETE
================================================================================

📊 Generated 8 plots saved to: .../results/figures/
```

---

## 🎨 The 8 Plots Explained

### Plot 1: Correlation Heatmap
- **What it shows**: Correlation between all variables
- **Colors**: Red = negative correlation, Blue = positive correlation
- **Use**: Identify key relationships

### Plot 2: Time Series
- **What it shows**: REIT returns over time
- **Patterns**: Volatility clustering, trends, crisis periods
- **Use**: Understand temporal patterns

### Plot 3: Dual-Axis Co-movement
- **What it shows**: Returns (left axis) vs. Mortgage Rates (right axis)
- **Relationship**: Usually move in opposite directions (inverse)
- **Use**: Visualize main driver effect

### Plot 4: Lagged Effects
- **What it shows**: Correlation at different time lags (0-12 months)
- **Optimal lag**: The lag with highest correlation magnitude
- **Use**: Determine timing for M3 model specifications

### Plot 5: Group Box Plots
- **What it shows**: Return distributions across time periods
- **Periods**: Normal, 2008 Crisis, 2020 COVID, 2022+ Rates
- **Use**: Compare volatility and medians across periods

### Plot 6: Sensitivity Analysis
- **What it shows**: How sensitive returns are to rates in each period
- **Colors**: Red (sensitive), Orange (moderate), Green (resilient)
- **Use**: Identify heterogeneous effects across regimes

### Plot 7: Scatter Plots (Controls)
- **What it shows**: Individual control variable relationships with returns
- **Red line**: Linear regression fit
- **Use**: Assess control variable importance

### Plot 8: Time Series Decomposition
- **What it shows**: 4 panels - Observed, Trend, Seasonal, Residual
- **Use**: Separate long-term vs. short-term vs. random variation

---

## ✅ Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'pandas'"
**Solution**: Install packages:
```bash
pip install pandas numpy matplotlib seaborn statsmodels
```

### Problem: Notebook cells won't run
**Solution 1**: Restart kernel
  - Jupyter menu: Kernel → Restart Kernel

**Solution 2**: Check Python version  
  - Run: `python3 --version` (should be 3.8+)

**Solution 3**: Use the Python script (Option 2) instead

### Problem: "FileNotFoundError: reit_fred_analysis_panel.csv"
**Solution**: Make sure M1 data was generated
  - Check: `data/final/reit_fred_analysis_panel.csv` exists
  - If missing, run M1 first

### Problem: Plots generated but look wrong/empty
**Solution**: 
  - Check that data file has valid numeric columns
  - Try regenerating with the Python script
  - Verify data has enough observations

---

## 📁 File Locations

```
Your Project Root:
/workspaces/qm2023-capstone-lailah-stevie-isabelle-sienna/

Notebook to run:
├── capstone_eda.ipynb

Python scripts:
├── generate_plots.py       (standalone script)
├── run_eda_plots.py        (alternative script)

Data input:
└── data/final/reit_fred_analysis_panel.csv

Output location:
└── results/figures/        (where 8 PNG files will appear)
    ├── M2_01_correlation_heatmap.png
    ├── M2_02_timeseries_outcome.png
    ├── M2_03_dualaxis_comovement.png
    ├── M2_04_lagged_effects.png
    ├── M2_05_group_boxplots.png
    ├── M2_06_sensitivity_analysis.png
    ├── M2_07_scatter_controls.png
    └── M2_08_decomposition.png
```

---

## ⚡ Quick Command Reference

### Run Jupyter Notebook
```bash
jupyter notebook capstone_eda.ipynb
```

### Run Python Script
```bash
cd /workspaces/qm2023-capstone-lailah-stevie-isabelle-sienna
python3 generate_plots.py
```

### Check if plots exist
```bash
ls -la results/figures/M2_*.png
```

### View a specific plot
```bash
# Linux/Mac
open results/figures/M2_01_correlation_heatmap.png

# Or view in VS Code
# Right-click file > Open Preview
```

---

## ✨ Next Steps After Plots Are Generated

1. **Verify all 8 PNG files exist** in `results/figures/`
2. **Review the plots** in the Jupyter notebook (scroll up to see them)
3. **Read the captions** for economic interpretation
4. **Commit to GitHub**:
   ```bash
   git add capstone_eda.ipynb
   git add results/figures/M2_*.png
   git commit -m "Milestone 2: Generated all 8 EDA plots"
   git push origin main
   ```
5. **Submit to course** system

---

## 🎯 Summary

| Method | Pros | Cons |
|--------|------|------|
| **Jupyter Notebook** | Interactive, see plots immediately, easy | Requires Jupyter/VS Code |
| **Python Script** | Standalone, no Jupyter needed, fast | Must install packages first |

**Recommendation**: Try Jupyter first (Option 1). If that doesn't work, use the Python script (Option 2).

---

**Need help?** Check the troubleshooting section above or review the script comments for more details.

**Status**: ✅ Ready to generate plots!
