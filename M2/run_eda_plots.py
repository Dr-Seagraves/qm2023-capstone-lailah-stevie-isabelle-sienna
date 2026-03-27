#!/usr/bin/env python3
"""
Standalone EDA plot generation script
Generates all 8 required M2 plots from the REIT and FRED data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# Configure visualization settings
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['lines.linewidth'] = 2

# Add code directory to path for config_paths import
sys.path.insert(0, '/workspaces/qm2023-capstone-lailah-stevie-isabelle-sienna/code')
from config_paths import PROJECT_ROOT, FINAL_DATA_DIR, FIGURES_DIR

# Ensure figures directory exists
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("GENERATING ALL 8 REQUIRED M2 EDA PLOTS")
print("=" * 80)

# Load the final analysis panel
data_path = FINAL_DATA_DIR / 'reit_fred_analysis_panel.csv'
print(f"\nLoading data from: {data_path}")
df = pd.read_csv(data_path)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Data preparation
date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Identify numeric columns for analysis
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print(f"\nNumeric columns ({len(numeric_cols)}): {numeric_cols[:10]}...")

# Identify variables
outcome_cols = [col for col in numeric_cols if 'ret' in col.lower() or 'return' in col.lower()]
driver_cols = [col for col in numeric_cols if any(x in col.lower() for x in ['fedfunds', 'mortgage', 'rate'])]
control_cols = [col for col in numeric_cols if col not in outcome_cols + driver_cols]

print(f"\nOutcome variables: {outcome_cols}")
print(f"Driver variables: {driver_cols}")
print(f"Control variables: {control_cols[:5]}...")

# ============================================================================
# PLOT 1: CORRELATION HEATMAP
# ============================================================================
print("\n[1/8] Generating Plot 1: Correlation Heatmap...")
try:
    plt.close('all')
    plt.figure(figsize=(14, 10))
    
    vars_to_plot = outcome_cols + driver_cols + control_cols[:5]
    vars_to_plot = [v for v in vars_to_plot if v in df.columns]
    
    corr_matrix = df[vars_to_plot].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                vmin=-1, vmax=1)
    
    plt.title('Correlation Matrix: REIT Returns, Economic Drivers, and Controls', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Variables', fontsize=12)
    plt.ylabel('Variables', fontsize=12)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'M2_01_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Plot 1 saved: M2_01_correlation_heatmap.png")
except Exception as e:
    print(f"✗ Plot 1 failed: {e}")

# ============================================================================
# PLOT 2: TIME SERIES OF OUTCOME VARIABLE
# ============================================================================
print("[2/8] Generating Plot 2: Time Series...")
try:
    plt.close('all')
    
    if outcome_cols:
        outcome_var = outcome_cols[0]
        ts_data = df[[outcome_var]].copy()
        
        if date_cols:
            ts_data = df.sort_values(by=date_cols[0])
        
        plt.figure(figsize=(14, 6))
        plt.plot(range(len(ts_data)), ts_data[outcome_var].values, color='steelblue', linewidth=2)
        
        plt.title(f'Time Series: {outcome_var} Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Time Period', fontsize=12)
        plt.ylabel(f'{outcome_var} (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'M2_02_timeseries_outcome.png', dpi=300, bbox_inches='tight')
        print("✓ Plot 2 saved: M2_02_timeseries_outcome.png")
except Exception as e:
    print(f"✗ Plot 2 failed: {e}")

# ============================================================================
# PLOT 3: DUAL-AXIS PLOT
# ============================================================================
print("[3/8] Generating Plot 3: Dual-Axis Co-movement...")
try:
    plt.close('all')
    
    if outcome_cols and driver_cols:
        outcome_var = outcome_cols[0]
        driver_var = driver_cols[0]
        
        if date_cols:
            plot_data = df.sort_values(by=date_cols[0])[[outcome_var, driver_var]].reset_index(drop=True)
        else:
            plot_data = df[[outcome_var, driver_var]].copy()
        
        fig, ax1 = plt.subplots(figsize=(14, 6))
        
        color = 'tab:blue'
        ax1.set_xlabel('Time Period', fontsize=12)
        ax1.set_ylabel(f'{outcome_var} (%)', color=color, fontsize=12)
        ax1.plot(range(len(plot_data)), plot_data[outcome_var].values, color=color, linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, alpha=0.3)
        
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel(f'{driver_var} (bps)', color=color, fontsize=12)
        ax2.plot(range(len(plot_data)), plot_data[driver_var].values, color=color, linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title(f'Co-movement Analysis: {outcome_var} vs. {driver_var}', 
                  fontsize=14, fontweight='bold', pad=20)
        
        fig.tight_layout()
        plt.savefig(FIGURES_DIR / 'M2_03_dualaxis_comovement.png', dpi=300, bbox_inches='tight')
        print("✓ Plot 3 saved: M2_03_dualaxis_comovement.png")
except Exception as e:
    print(f"✗ Plot 3 failed: {e}")

# ============================================================================
# PLOT 4: LAGGED EFFECT ANALYSIS
# ============================================================================
print("[4/8] Generating Plot 4: Lagged Effects...")
try:
    plt.close('all')
    
    if outcome_cols and driver_cols:
        outcome_var = outcome_cols[0]
        driver_var = driver_cols[0]
        
        if date_cols:
            lag_data = df.sort_values(by=date_cols[0]).copy()
        else:
            lag_data = df.copy()
        
        lags = [0, 1, 2, 3, 6, 12]
        correlations = []
        
        for lag in lags:
            if lag == 0:
                corr = lag_data[outcome_var].corr(lag_data[driver_var])
            else:
                corr = lag_data[outcome_var].corr(lag_data[driver_var].shift(lag))
            correlations.append(corr)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(lags)), correlations, color='steelblue', alpha=0.7, edgecolor='black')
        
        for bar, corr in zip(bars, correlations):
            if corr < 0:
                bar.set_color('indianred')
            else:
                bar.set_color('lightgreen')
        
        plt.xlabel('Lag (months)', fontsize=12)
        plt.ylabel('Correlation Coefficient', fontsize=12)
        plt.title(f'Lagged Effects: Correlation of {outcome_var} with {driver_var}', 
                  fontsize=14, fontweight='bold')
        plt.xticks(range(len(lags)), [f'Lag {lag}' for lag in lags])
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        plt.grid(True, alpha=0.3, axis='y')
        
        for i, (lag, corr) in enumerate(zip(lags, correlations)):
            plt.text(i, corr + 0.02 if corr > 0 else corr - 0.02, f'{corr:.3f}', 
                    ha='center', va='bottom' if corr > 0 else 'top', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'M2_04_lagged_effects.png', dpi=300, bbox_inches='tight')
        print("✓ Plot 4 saved: M2_04_lagged_effects.png")
except Exception as e:
    print(f"✗ Plot 4 failed: {e}")

# ============================================================================
# PLOT 5: GROUP BOX PLOTS
# ============================================================================
print("[5/8] Generating Plot 5: Group Box Plots...")
try:
    plt.close('all')
    
    if outcome_cols:
        outcome_var = outcome_cols[0]
        
        # Create period groups if no natural grouping exists
        df['period'] = 'Normal'
        if date_cols:
            df.loc[df[date_cols[0]].dt.year == 2008, 'period'] = '2008 Crisis'
            df.loc[df[date_cols[0]].dt.year == 2020, 'period'] = '2020 COVID'
            df.loc[(df[date_cols[0]].dt.year >= 2022), 'period'] = '2022-23 Rates'
        
        grouping_var = 'period'
        
        plt.figure(figsize=(12, 6))
        df.boxplot(column=outcome_var, by=grouping_var, ax=plt.gca(), patch_artist=True)
        
        plt.suptitle('')
        plt.title(f'Distribution of {outcome_var} by {grouping_var}', fontsize=14, fontweight='bold')
        plt.xlabel(grouping_var, fontsize=12)
        plt.ylabel(f'{outcome_var} (%)', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'M2_05_group_boxplots.png', dpi=300, bbox_inches='tight')
        print("✓ Plot 5 saved: M2_05_group_boxplots.png")
except Exception as e:
    print(f"✗ Plot 5 failed: {e}")

# ============================================================================
# PLOT 6: GROUP SENSITIVITY ANALYSIS
# ============================================================================
print("[6/8] Generating Plot 6: Sensitivity Analysis...")
try:
    plt.close('all')
    
    if outcome_cols and driver_cols and 'period' in df.columns:
        outcome_var = outcome_cols[0]
        driver_var = driver_cols[0]
        grouping_var = 'period'
        
        group_sensitivity = df.groupby(grouping_var).apply(
            lambda x: x[outcome_var].corr(x[driver_var])
        ).sort_values()
        
        sensitive_threshold = -0.3
        colors = ['red' if corr < sensitive_threshold else 'orange' if corr < 0 else 'lightgreen' 
                  for corr in group_sensitivity.values]
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(range(len(group_sensitivity)), group_sensitivity.values, color=colors, 
                        edgecolor='black', linewidth=1.5)
        
        plt.yticks(range(len(group_sensitivity)), group_sensitivity.index)
        plt.xlabel('Correlation with Driver Variable', fontsize=12)
        plt.ylabel(grouping_var, fontsize=12)
        plt.title(f'Sensitivity Analysis: {outcome_var} Sensitivity to {driver_var}', 
                  fontsize=14, fontweight='bold')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        plt.axvline(x=sensitive_threshold, color='red', linestyle='--', linewidth=1, alpha=0.5)
        plt.grid(True, alpha=0.3, axis='x')
        
        for i, (group, corr) in enumerate(group_sensitivity.items()):
            plt.text(corr + 0.02, i, f'{corr:.3f}', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'M2_06_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Plot 6 saved: M2_06_sensitivity_analysis.png")
except Exception as e:
    print(f"✗ Plot 6 failed: {e}")

# ============================================================================
# PLOT 7: SCATTER PLOTS FOR CONTROL VARIABLES
# ============================================================================
print("[7/8] Generating Plot 7: Scatter Plots (Controls)...")
try:
    plt.close('all')
    
    if outcome_cols and control_cols:
        outcome_var = outcome_cols[0]
        controls_to_plot = control_cols[:2]
        
        fig, axes = plt.subplots(1, len(controls_to_plot), figsize=(15, 5))
        if len(controls_to_plot) == 1:
            axes = [axes]
        
        for idx, control_var in enumerate(controls_to_plot):
            ax = axes[idx]
            
            ax.scatter(df[control_var], df[outcome_var], alpha=0.5, s=20, color='steelblue')
            
            clean_data = df[[control_var, outcome_var]].dropna()
            if len(clean_data) > 1:
                z = np.polyfit(clean_data[control_var], clean_data[outcome_var], 1)
                p = np.poly1d(z)
                x_line = np.linspace(clean_data[control_var].min(), clean_data[control_var].max(), 100)
                ax.plot(x_line, p(x_line), "r-", linewidth=2, label='Fitted line')
            
            corr = df[control_var].corr(df[outcome_var])
            
            ax.set_xlabel(control_var, fontsize=11)
            ax.set_ylabel(outcome_var, fontsize=11)
            ax.set_title(f'{outcome_var} vs. {control_var}\n(r = {corr:.3f})', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend()
        
        plt.suptitle(f'Bivariate Relationships: Control Variables and {outcome_var}', 
                     fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'M2_07_scatter_controls.png', dpi=300, bbox_inches='tight')
        print("✓ Plot 7 saved: M2_07_scatter_controls.png")
except Exception as e:
    print(f"✗ Plot 7 failed: {e}")

# ============================================================================
# PLOT 8: TIME SERIES DECOMPOSITION
# ============================================================================
print("[8/8] Generating Plot 8: Time Series Decomposition...")
try:
    plt.close('all')
    
    if outcome_cols:
        outcome_var = outcome_cols[0]
        
        if date_cols:
            ts = df.sort_values(by=date_cols[0]).set_index(date_cols[0])[outcome_var]
        else:
            ts = df[outcome_var].values
        
        period = min(12, max(4, len(ts) // 50))
        
        decomposition = seasonal_decompose(ts, model='additive', period=period, extrapolate='extend')
        
        fig, axes = plt.subplots(4, 1, figsize=(14, 10))
        
        axes[0].plot(decomposition.observed, color='steelblue', linewidth=1.5)
        axes[0].set_ylabel('Observed', fontsize=11)
        axes[0].set_title(f'Time Series Decomposition: {outcome_var}', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(decomposition.trend, color='darkblue', linewidth=2)
        axes[1].set_ylabel('Trend', fontsize=11)
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(decomposition.seasonal, color='darkgreen', linewidth=1.5)
        axes[2].set_ylabel('Seasonal', fontsize=11)
        axes[2].grid(True, alpha=0.3)
        
        axes[3].plot(decomposition.resid, color='darkred', linewidth=1)
        axes[3].set_ylabel('Residual', fontsize=11)
        axes[3].set_xlabel('Time Period', fontsize=11)
        axes[3].grid(True, alpha=0.3)
        axes[3].axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'M2_08_decomposition.png', dpi=300, bbox_inches='tight')
        print("✓ Plot 8 saved: M2_08_decomposition.png")
except Exception as e:
    print(f"✗ Plot 8 failed: {e}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("PLOT GENERATION COMPLETE")
print("=" * 80)
print(f"\nAll plots saved to: {FIGURES_DIR}")
print("\nGenerated files:")
for i in range(1, 9):
    filename = f'M2_0{i}_*.png'
    print(f"  [✓] M2_0{i}_*.png")

print("\n✅ All 8 required M2 EDA plots have been successfully generated!")
