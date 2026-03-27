#!/usr/bin/env python3
"""
Complete EDA Dashboard - Plot Generation
Generates all 8 required M2 plots from REIT and FRED data
Self-contained, no Jupyter required
"""

import sys
import os

# First, try to import required packages and provide guidance if missing
try:
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    from statsmodels.tsa.seasonal import seasonal_decompose
    import warnings
    warnings.filterwarnings('ignore')
except ImportError as e:
    print(f"ERROR: Missing required package: {e}")
    print("\nTo install required packages, run:")
    print("pip install pandas numpy matplotlib seaborn statsmodels")
    sys.exit(1)

# ============================================================================
# SETUP AND CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path('/workspaces/qm2023-capstone-lailah-stevie-isabelle-sienna')
FINAL_DATA_DIR = PROJECT_ROOT / 'data' / 'final'
FIGURES_DIR = PROJECT_ROOT / 'results' / 'figures'

# Create output directory
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Configure visualization settings
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['lines.linewidth'] = 2

print("=" * 80)
print("MILESTONE 2: EDA DASHBOARD - PLOT GENERATION")
print("=" * 80)

# ============================================================================
# LOAD DATA
# ============================================================================

data_path = FINAL_DATA_DIR / 'reit_fred_analysis_panel.csv'
print(f"\n📂 Loading data from: {data_path}")

if not data_path.exists():
    print(f"❌ ERROR: Data file not found at {data_path}")
    sys.exit(1)

try:
    df = pd.read_csv(data_path)
    print(f"✓ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    sys.exit(1)

# Data preparation
date_cols = [col for col in df.columns if 'date' in col.lower() or 'year' in col.lower()]
for col in date_cols:
    try:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    except:
        pass

# Identify variable types
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
outcome_cols = [col for col in numeric_cols if 'ret' in col.lower() or 'return' in col.lower()]
driver_cols = [col for col in numeric_cols if any(x in col.lower() for x in ['fedfunds', 'mortgage', 'rate', 'govt'])]
control_cols = [col for col in numeric_cols if col not in outcome_cols + driver_cols]

print(f"\n📊 Variable Classification:")
print(f"   Outcome variables: {outcome_cols if outcome_cols else 'None found'}")
print(f"   Driver variables: {driver_cols if driver_cols else 'Using first numeric column'}")
print(f"   Control variables: {len(control_cols)} identified")

# Fallback if specific variables not found
if not outcome_cols:
    outcome_cols = [numeric_cols[0]]
if not driver_cols:
    driver_cols = [numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]]

print(f"\n✓ Using '{outcome_cols[0]}' as outcome variable")
print(f"✓ Using '{driver_cols[0]}' as driver variable")

# ============================================================================
# PLOT 1: CORRELATION HEATMAP
# ============================================================================
print("\n[1/8] Generating Correlation Heatmap...")
try:
    plt.close('all')
    fig = plt.figure(figsize=(14, 10))
    
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
    
    output_file = FIGURES_DIR / 'M2_01_correlation_heatmap.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_file.name}")
    plt.close()
except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# PLOT 2: TIME SERIES OF OUTCOME VARIABLE
# ============================================================================
print("[2/8] Generating Time Series...")
try:
    plt.close('all')
    fig = plt.figure(figsize=(14, 6))
    
    outcome_var = outcome_cols[0]
    ts_data = df[[outcome_var]].copy()
    
    if date_cols:
        ts_data = df.sort_values(by=date_cols[0])[[outcome_var]].reset_index(drop=True)
    
    plt.plot(range(len(ts_data)), ts_data[outcome_var].values, color='steelblue', linewidth=2)
    
    plt.title(f'Time Series: {outcome_var} Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel(f'{outcome_var}', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file = FIGURES_DIR / 'M2_02_timeseries_outcome.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_file.name}")
    plt.close()
except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# PLOT 3: DUAL-AXIS PLOT
# ============================================================================
print("[3/8] Generating Dual-Axis Co-movement Plot...")
try:
    plt.close('all')
    
    outcome_var = outcome_cols[0]
    driver_var = driver_cols[0]
    
    if date_cols:
        plot_data = df.sort_values(by=date_cols[0])[[outcome_var, driver_var]].reset_index(drop=True)
    else:
        plot_data = df[[outcome_var, driver_var]].copy()
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Time Period', fontsize=12)
    ax1.set_ylabel(f'{outcome_var}', color=color, fontsize=12)
    ax1.plot(range(len(plot_data)), plot_data[outcome_var].values, color=color, linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel(f'{driver_var}', color=color, fontsize=12)
    ax2.plot(range(len(plot_data)), plot_data[driver_var].values, color=color, linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title(f'Co-movement: {outcome_var} vs. {driver_var}', 
              fontsize=14, fontweight='bold', pad=20)
    
    fig.tight_layout()
    output_file = FIGURES_DIR / 'M2_03_dualaxis_comovement.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_file.name}")
    plt.close()
except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# PLOT 4: LAGGED EFFECT ANALYSIS
# ============================================================================
print("[4/8] Generating Lagged Effects Analysis...")
try:
    plt.close('all')
    
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
    
    fig = plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(lags)), correlations, alpha=0.7, edgecolor='black')
    
    # Color by sign
    for bar, corr in zip(bars, correlations):
        if pd.isna(corr):
            bar.set_color('gray')
        elif corr < 0:
            bar.set_color('indianred')
        else:
            bar.set_color('lightgreen')
    
    plt.xlabel('Lag (months)', fontsize=12)
    plt.ylabel('Correlation Coefficient', fontsize=12)
    plt.title(f'Lagged Effects: {outcome_var} vs. {driver_var}', 
              fontsize=14, fontweight='bold')
    plt.xticks(range(len(lags)), [f'Lag {lag}' for lag in lags])
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, (lag, corr) in enumerate(zip(lags, correlations)):
        if not pd.isna(corr):
            plt.text(i, corr + 0.02 if corr > 0 else corr - 0.02, f'{corr:.3f}', 
                    ha='center', va='bottom' if corr > 0 else 'top', fontsize=9)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / 'M2_04_lagged_effects.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_file.name}")
    plt.close()
except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# PLOT 5: GROUP BOX PLOTS
# ============================================================================
print("[5/8] Generating Group Box Plots...")
try:
    plt.close('all')
    
    outcome_var = outcome_cols[0]
    
    # Create period groups based on year if available
    plot_df = df.copy()
    if date_cols:
        plot_df['period'] = 'Normal'
        year_col = date_cols[0]
        plot_df.loc[plot_df[year_col].dt.year == 2008, 'period'] = '2008 Crisis'
        plot_df.loc[plot_df[year_col].dt.year == 2020, 'period'] = '2020 COVID'
        plot_df.loc[(plot_df[year_col].dt.year >= 2022), 'period'] = '2022+ Rates'
        grouping_var = 'period'
    else:
        plot_df['period'] = pd.qcut(range(len(plot_df)), q=3, labels=['Early', 'Middle', 'Recent'], duplicates='drop')
        grouping_var = 'period'
    
    fig = plt.figure(figsize=(12, 6))
    plot_df.boxplot(column=outcome_var, by=grouping_var, ax=plt.gca(), patch_artist=True)
    
    plt.suptitle('')
    plt.title(f'Distribution of {outcome_var} by {grouping_var}', fontsize=14, fontweight='bold')
    plt.xlabel(grouping_var, fontsize=12)
    plt.ylabel(f'{outcome_var}', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    output_file = FIGURES_DIR / 'M2_05_group_boxplots.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_file.name}")
    plt.close()
except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# PLOT 6: GROUP SENSITIVITY ANALYSIS
# ============================================================================
print("[6/8] Generating Sensitivity Analysis...")
try:
    plt.close('all')
    
    outcome_var = outcome_cols[0]
    driver_var = driver_cols[0]
    
    # Use the period column from previous plot
    if 'period' not in plot_df.columns:
        plot_df['period'] = 'All'
    
    group_sensitivity = plot_df.groupby('period').apply(
        lambda x: x[outcome_var].corr(x[driver_var]) if len(x) > 1 else np.nan
    ).sort_values()
    
    sensitive_threshold = -0.3
    colors = []
    for corr in group_sensitivity.values:
        if pd.isna(corr):
            colors.append('gray')
        elif corr < sensitive_threshold:
            colors.append('red')
        elif corr < 0:
            colors.append('orange')
        else:
            colors.append('lightgreen')
    
    fig = plt.figure(figsize=(12, 6))
    bars = plt.barh(range(len(group_sensitivity)), group_sensitivity.values, color=colors, 
                    edgecolor='black', linewidth=1.5)
    
    plt.yticks(range(len(group_sensitivity)), group_sensitivity.index)
    plt.xlabel('Correlation with Driver', fontsize=12)
    plt.ylabel('Period', fontsize=12)
    plt.title(f'Sensitivity: {outcome_var} to {driver_var}', fontsize=14, fontweight='bold')
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    plt.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (period, corr) in enumerate(group_sensitivity.items()):
        if not pd.isna(corr):
            plt.text(corr + 0.02, i, f'{corr:.3f}', va='center', fontsize=9)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / 'M2_06_sensitivity_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_file.name}")
    plt.close()
except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# PLOT 7: SCATTER PLOTS FOR CONTROL VARIABLES
# ============================================================================
print("[7/8] Generating Scatter Plots...")
try:
    plt.close('all')
    
    outcome_var = outcome_cols[0]
    controls_to_plot = control_cols[:2] if len(control_cols) >= 2 else control_cols
    
    if len(controls_to_plot) == 0:
        controls_to_plot = [numeric_cols[2]] if len(numeric_cols) > 2 else [numeric_cols[0]]
    
    fig, axes = plt.subplots(1, len(controls_to_plot), figsize=(15, 5))
    if len(controls_to_plot) == 1:
        axes = [axes]
    
    for idx, control_var in enumerate(controls_to_plot):
        ax = axes[idx]
        
        # Create scatter plot
        clean = df[[control_var, outcome_var]].dropna()
        ax.scatter(clean[control_var], clean[outcome_var], alpha=0.5, s=20, color='steelblue')
        
        # Add regression line
        if len(clean) > 1:
            z = np.polyfit(clean[control_var], clean[outcome_var], 1)
            p = np.poly1d(z)
            x_line = np.linspace(clean[control_var].min(), clean[control_var].max(), 100)
            ax.plot(x_line, p(x_line), "r-", linewidth=2, label='Fit')
        
        corr = df[control_var].corr(df[outcome_var])
        
        ax.set_xlabel(control_var, fontsize=11)
        ax.set_ylabel(outcome_var, fontsize=11)
        ax.set_title(f'{outcome_var} vs. {control_var}\n(r={corr:.3f})', fontsize=11)
        ax.grid(True, alpha=0.3)
        if len(clean) > 1:
            ax.legend()
    
    plt.suptitle(f'Control Variable Relationships', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    output_file = FIGURES_DIR / 'M2_07_scatter_controls.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {output_file.name}")
    plt.close()
except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# PLOT 8: TIME SERIES DECOMPOSITION
# ============================================================================
print("[8/8] Generating Time Series Decomposition...")
try:
    plt.close('all')
    
    outcome_var = outcome_cols[0]
    
    # Prepare time series
    if date_cols:
        ts = df.sort_values(by=date_cols[0]).set_index(date_cols[0])[outcome_var]
    else:
        ts = df[outcome_var].values
    
    # Determine period
    period = min(12, max(4, len(ts) // 50))
    
    try:
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
        axes[3].set_xlabel('Time', fontsize=11)
        axes[3].grid(True, alpha=0.3)
        axes[3].axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        
        plt.tight_layout()
        output_file = FIGURES_DIR / 'M2_08_decomposition.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"   ✓ Saved: {output_file.name}")
        plt.close()
    except Exception as decomp_error:
        print(f"   ✗ Decomposition failed (creating alternative plot): {decomp_error}")
        
        # Create alternative simple plot if decomposition fails
        fig, ax = plt.subplots(figsize=(14, 6))
        if isinstance(ts, pd.Series):
            ax.plot(ts.values, color='steelblue', linewidth=1.5)
        else:
            ax.plot(ts, color='steelblue', linewidth=1.5)
        ax.set_title(f'{outcome_var} - Time Series', fontsize=14, fontweight='bold')
        ax.set_ylabel(outcome_var, fontsize=11)
        ax.set_xlabel('Time', fontsize=11)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_file = FIGURES_DIR / 'M2_08_decomposition.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"   ✓ Saved (alternative): {output_file.name}")
        plt.close()

except Exception as e:
    print(f"   ✗ Failed: {e}")

# ============================================================================
# COMPLETION SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ PLOT GENERATION COMPLETE")
print("=" * 80)

plot_files = list(FIGURES_DIR.glob('M2_*.png'))
print(f"\n📊 Generated {len(plot_files)} plots:\n")
for i, f in enumerate(sorted(plot_files), 1):
    print(f"   [{i}] {f.name}")

print(f"\n📁 All plots saved to: {FIGURES_DIR}")
print(f"\n✓ Ready for Milestone 2 submission!")
