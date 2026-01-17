import pandas as pd
import numpy as np
from scipy import stats

# Lead-lag analysis between demographic/biometric updates and operational load
# Quantify the relationship between updates and system load patterns

print("=" * 90)
print("LEAD-LAG ANALYSIS: UPDATES vs OPERATIONAL LOAD")
print("=" * 90)

# Prepare daily time series for cross-correlation
daily_ops_ts = daily_trends.copy()
daily_ops_ts = daily_ops_ts.sort_values('Date').reset_index(drop=True)

# Define operational load and update metrics
daily_ops_ts['update_volume'] = daily_ops_ts['total_demo_updates'] + daily_ops_ts['total_bio_updates']
daily_ops_ts['operational_load'] = daily_ops_ts['total_operations']

# Fill NaN values with 0 for correlation analysis
daily_ops_ts['update_volume'] = daily_ops_ts['update_volume'].fillna(0)
daily_ops_ts['operational_load'] = daily_ops_ts['operational_load'].fillna(0)
daily_ops_ts['total_demo_updates'] = daily_ops_ts['total_demo_updates'].fillna(0)
daily_ops_ts['total_bio_updates'] = daily_ops_ts['total_bio_updates'].fillna(0)

# Cross-correlation analysis for different lags
max_lag = 7  # Examine up to 7 days of lag
correlations = []

for lag in range(-max_lag, max_lag + 1):
    if lag < 0:
        # Updates lead operational load (negative lag)
        update_series = daily_ops_ts['update_volume'].iloc[:lag].values
        load_series = daily_ops_ts['operational_load'].iloc[-lag:].values
    elif lag > 0:
        # Operational load leads updates (positive lag)
        update_series = daily_ops_ts['update_volume'].iloc[lag:].values
        load_series = daily_ops_ts['operational_load'].iloc[:-lag].values
    else:
        # Contemporaneous relationship
        update_series = daily_ops_ts['update_volume'].values
        load_series = daily_ops_ts['operational_load'].values
    
    if len(update_series) > 1 and len(load_series) > 1:
        corr, p_value = stats.pearsonr(update_series, load_series)
        correlations.append({
            'lag_days': lag,
            'correlation': corr,
            'p_value': p_value
        })

lag_df = pd.DataFrame(correlations)
lag_df['significant'] = lag_df['p_value'] < 0.05

# Find strongest lead-lag relationship
max_corr_idx = lag_df['correlation'].abs().idxmax()
strongest_lag = lag_df.loc[max_corr_idx]

print(f"\n🔍 CROSS-CORRELATION RESULTS")
print(f"\nStrongest correlation found at lag = {strongest_lag['lag_days']} days")
print(f"  Correlation coefficient: {strongest_lag['correlation']:.4f}")
print(f"  P-value: {strongest_lag['p_value']:.6f}")
print(f"  Statistical significance: {'Yes (p < 0.05)' if strongest_lag['significant'] else 'No (p >= 0.05)'}")

if strongest_lag['lag_days'] < 0:
    print(f"\n📌 Interpretation: Update volume LEADS operational load by {abs(strongest_lag['lag_days'])} days")
    print(f"   Updates serve as a {abs(strongest_lag['lag_days'])}-day early warning indicator for system load")
elif strongest_lag['lag_days'] > 0:
    print(f"\n📌 Interpretation: Operational load LEADS update volume by {strongest_lag['lag_days']} days")
    print(f"   System load spikes precede update activity by {strongest_lag['lag_days']} days")
else:
    print(f"\n📌 Interpretation: Contemporaneous relationship - updates and load occur simultaneously")

# Examine significant lags
significant_lags = lag_df[lag_df['significant']].sort_values('correlation', ascending=False, key=abs)
print(f"\nAll statistically significant lead-lag relationships (p < 0.05):")
if len(significant_lags) > 0:
    for _, row in significant_lags.iterrows():
        direction = "Updates lead" if row['lag_days'] < 0 else ("Load leads" if row['lag_days'] > 0 else "Simultaneous")
        print(f"  Lag {row['lag_days']:+2d} days: r={row['correlation']:+.4f}, p={row['p_value']:.6f} ({direction})")
else:
    print("  No statistically significant lags found")

# Separate analysis for demographic vs biometric updates
print(f"\n" + "=" * 90)
print("SEPARATE ANALYSIS: DEMOGRAPHIC vs BIOMETRIC UPDATES")
print("=" * 90)

# Demographic update lead-lag
demo_correlations = []
for lag in range(-max_lag, max_lag + 1):
    if lag < 0:
        demo_series = daily_ops_ts['total_demo_updates'].iloc[:lag].values
        load_series = daily_ops_ts['operational_load'].iloc[-lag:].values
    elif lag > 0:
        demo_series = daily_ops_ts['total_demo_updates'].iloc[lag:].values
        load_series = daily_ops_ts['operational_load'].iloc[:-lag].values
    else:
        demo_series = daily_ops_ts['total_demo_updates'].values
        load_series = daily_ops_ts['operational_load'].values
    
    if len(demo_series) > 1 and len(load_series) > 1:
        corr, p_value = stats.pearsonr(demo_series, load_series)
        demo_correlations.append({
            'lag_days': lag,
            'correlation': corr,
            'p_value': p_value
        })

demo_lag_df = pd.DataFrame(demo_correlations)
demo_lag_df['significant'] = demo_lag_df['p_value'] < 0.05
strongest_demo_lag = demo_lag_df.loc[demo_lag_df['correlation'].abs().idxmax()]

print(f"\n📊 DEMOGRAPHIC UPDATES:")
print(f"  Strongest correlation at lag = {strongest_demo_lag['lag_days']} days")
print(f"  Correlation: {strongest_demo_lag['correlation']:.4f}, P-value: {strongest_demo_lag['p_value']:.6f}")

# Biometric update lead-lag
bio_correlations = []
for lag in range(-max_lag, max_lag + 1):
    if lag < 0:
        bio_series = daily_ops_ts['total_bio_updates'].iloc[:lag].values
        load_series = daily_ops_ts['operational_load'].iloc[-lag:].values
    elif lag > 0:
        bio_series = daily_ops_ts['total_bio_updates'].iloc[lag:].values
        load_series = daily_ops_ts['operational_load'].iloc[:-lag].values
    else:
        bio_series = daily_ops_ts['total_bio_updates'].values
        load_series = daily_ops_ts['operational_load'].values
    
    if len(bio_series) > 1 and len(load_series) > 1:
        corr, p_value = stats.pearsonr(bio_series, load_series)
        bio_correlations.append({
            'lag_days': lag,
            'correlation': corr,
            'p_value': p_value
        })

bio_lag_df = pd.DataFrame(bio_correlations)
bio_lag_df['significant'] = bio_lag_df['p_value'] < 0.05
strongest_bio_lag = bio_lag_df.loc[bio_lag_df['correlation'].abs().idxmax()]

print(f"\n📊 BIOMETRIC UPDATES:")
print(f"  Strongest correlation at lag = {strongest_bio_lag['lag_days']} days")
print(f"  Correlation: {strongest_bio_lag['correlation']:.4f}, P-value: {strongest_bio_lag['p_value']:.6f}")

# Monthly lead-lag analysis
monthly_ops_ts = monthly_trends.copy()
monthly_ops_ts['update_volume'] = monthly_ops_ts['total_demo_updates'] + monthly_ops_ts['total_bio_updates']
monthly_ops_ts['operational_load'] = monthly_ops_ts['total_operations']

# Calculate contemporaneous correlation for monthly data
if len(monthly_ops_ts) > 2:
    monthly_corr, monthly_p = stats.pearsonr(
        monthly_ops_ts['update_volume'], 
        monthly_ops_ts['operational_load']
    )
    print(f"\n📅 MONTHLY CORRELATION:")
    print(f"  Updates vs Load: r={monthly_corr:.4f}, p={monthly_p:.6f}")
    print(f"  Significance: {'Strong relationship' if abs(monthly_corr) > 0.7 else 'Moderate relationship' if abs(monthly_corr) > 0.4 else 'Weak relationship'}")

# Calculate Granger causality proxy using lagged regression
print(f"\n" + "=" * 90)
print("PREDICTIVE VALUE ANALYSIS")
print("=" * 90)

# Simple lagged regression to test if updates predict future load
if len(daily_ops_ts) > 7:
    # Create lagged features
    for i in [1, 2, 3, 7]:
        daily_ops_ts[f'update_lag_{i}'] = daily_ops_ts['update_volume'].shift(i)
    
    # Drop NaN values
    regression_data = daily_ops_ts.dropna()
    
    if len(regression_data) > 10:
        # Calculate simple correlation of lagged updates with current load
        lag_predictive = []
        for i in [1, 2, 3, 7]:
            if f'update_lag_{i}' in regression_data.columns:
                corr, p = stats.pearsonr(
                    regression_data[f'update_lag_{i}'], 
                    regression_data['operational_load']
                )
                lag_predictive.append({
                    'lag': i,
                    'correlation': corr,
                    'p_value': p
                })
        
        predictive_df = pd.DataFrame(lag_predictive)
        print(f"\nPredictive power of past updates on current operational load:")
        for _, row in predictive_df.iterrows():
            sig = "✓" if row['p_value'] < 0.05 else "✗"
            print(f"  {row['lag']}-day lag: r={row['correlation']:+.4f}, p={row['p_value']:.6f} {sig}")

print(f"\n✅ Lead-lag analysis complete")
print(f"   - Cross-correlation performed across {-max_lag} to +{max_lag} day lags")
print(f"   - Separate analysis for demographic and biometric updates")
print(f"   - Predictive value quantified for operational planning")
