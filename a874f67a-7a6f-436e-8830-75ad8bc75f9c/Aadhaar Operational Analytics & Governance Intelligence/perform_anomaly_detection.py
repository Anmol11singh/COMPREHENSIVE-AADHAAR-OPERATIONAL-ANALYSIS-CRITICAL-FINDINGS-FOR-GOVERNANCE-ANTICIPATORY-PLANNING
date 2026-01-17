import pandas as pd
import numpy as np

# Anomaly detection using statistical methods (IQR and Z-score)

# 1. DAILY ANOMALIES
daily_stats = daily_trends.copy()

# Calculate statistics for daily operations
mean_daily_ops = daily_stats['total_operations'].mean()
std_daily_ops = daily_stats['total_operations'].std()
q1_daily = daily_stats['total_operations'].quantile(0.25)
q3_daily = daily_stats['total_operations'].quantile(0.75)
iqr_daily = q3_daily - q1_daily

# Define thresholds
daily_zscore_threshold = 2.5  # 2.5 standard deviations
daily_iqr_lower = q1_daily - (1.5 * iqr_daily)
daily_iqr_upper = q3_daily + (1.5 * iqr_daily)

# Detect anomalies
daily_stats['z_score'] = np.abs((daily_stats['total_operations'] - mean_daily_ops) / std_daily_ops)
daily_stats['is_spike_zscore'] = daily_stats['z_score'] > daily_zscore_threshold
daily_stats['is_spike_iqr'] = daily_stats['total_operations'] > daily_iqr_upper
daily_stats['is_drop_iqr'] = daily_stats['total_operations'] < daily_iqr_lower
daily_stats['is_anomaly'] = daily_stats['is_spike_zscore'] | daily_stats['is_spike_iqr'] | daily_stats['is_drop_iqr']

daily_anomalies = daily_stats[daily_stats['is_anomaly']]

# 2. MONTHLY ANOMALIES
monthly_stats = monthly_trends.copy()

# Calculate statistics for monthly operations
mean_monthly_ops = monthly_stats['total_operations'].mean()
std_monthly_ops = monthly_stats['total_operations'].std()
q1_monthly = monthly_stats['total_operations'].quantile(0.25)
q3_monthly = monthly_stats['total_operations'].quantile(0.75)
iqr_monthly = q3_monthly - q1_monthly

# Define thresholds
monthly_zscore_threshold = 2.0
monthly_iqr_lower = q1_monthly - (1.5 * iqr_monthly)
monthly_iqr_upper = q3_monthly + (1.5 * iqr_monthly)

# Detect anomalies
monthly_stats['z_score'] = np.abs((monthly_stats['total_operations'] - mean_monthly_ops) / std_monthly_ops)
monthly_stats['is_spike_zscore'] = monthly_stats['z_score'] > monthly_zscore_threshold
monthly_stats['is_spike_iqr'] = monthly_stats['total_operations'] > monthly_iqr_upper
monthly_stats['is_drop_iqr'] = monthly_stats['total_operations'] < monthly_iqr_lower
monthly_stats['is_anomaly'] = monthly_stats['is_spike_zscore'] | monthly_stats['is_spike_iqr'] | monthly_stats['is_drop_iqr']

monthly_anomalies = monthly_stats[monthly_stats['is_anomaly']]

# 3. VOLATILITY ANALYSIS
# Calculate coefficient of variation (CV) as a measure of volatility
daily_cv = (std_daily_ops / mean_daily_ops) * 100
monthly_cv = (std_monthly_ops / mean_monthly_ops) * 100

# Growth rate volatility
growth_volatility = monthly_stats['operations_mom_growth'].std()

# 4. PEAK PERIODS IDENTIFICATION
# Top 5 daily peaks
top_daily_peaks = daily_stats.nlargest(5, 'total_operations')[['Date', 'total_operations', 'total_enrolments', 'total_demo_updates', 'total_bio_updates']]

# Top 3 monthly peaks
top_monthly_peaks = monthly_stats.nlargest(3, 'total_operations')[['Month_Year', 'total_operations', 'total_enrolments', 'total_demo_updates', 'total_bio_updates']]

# Display results
print("=" * 90)
print("ANOMALY DETECTION & VOLATILITY ANALYSIS")
print("=" * 90)

print("\nDAILY ANOMALIES:")
print(f"  Detection Thresholds:")
print(f"    - Z-Score Threshold: {daily_zscore_threshold} std devs")
print(f"    - IQR Upper Bound: {daily_iqr_upper:,.0f} operations")
print(f"    - IQR Lower Bound: {daily_iqr_lower:,.0f} operations")
print(f"\n  Anomalies Detected: {len(daily_anomalies)} out of {len(daily_stats)} days")
if len(daily_anomalies) > 0:
    print(f"\n  Anomalous Days:")
    for _anom_idx, anom in daily_anomalies.iterrows():
        anom_type = []
        if anom['is_spike_zscore']:
            anom_type.append(f"Z-score spike ({anom['z_score']:.2f})")
        if anom['is_spike_iqr']:
            anom_type.append("IQR spike")
        if anom['is_drop_iqr']:
            anom_type.append("IQR drop")
        print(f"    {anom['Date'].strftime('%Y-%m-%d')}: {anom['total_operations']:,.0f} ops - {', '.join(anom_type)}")

print("\nMONTHLY ANOMALIES:")
print(f"  Detection Thresholds:")
print(f"    - Z-Score Threshold: {monthly_zscore_threshold} std devs")
print(f"    - IQR Upper Bound: {monthly_iqr_upper:,.0f} operations")
print(f"    - IQR Lower Bound: {monthly_iqr_lower:,.0f} operations")
print(f"\n  Anomalies Detected: {len(monthly_anomalies)} out of {len(monthly_stats)} months")
if len(monthly_anomalies) > 0:
    print(f"\n  Anomalous Months:")
    for _anom_idx2, anom in monthly_anomalies.iterrows():
        anom_type = []
        if anom['is_spike_zscore']:
            anom_type.append(f"Z-score spike ({anom['z_score']:.2f})")
        if anom['is_spike_iqr']:
            anom_type.append("IQR spike")
        if anom['is_drop_iqr']:
            anom_type.append("IQR drop")
        print(f"    {anom['Month_Year']}: {anom['total_operations']:,.0f} ops - {', '.join(anom_type)}")

print("\nVOLATILITY METRICS:")
print(f"  Daily Coefficient of Variation: {daily_cv:.2f}%")
print(f"  Monthly Coefficient of Variation: {monthly_cv:.2f}%")
print(f"  MoM Growth Rate Volatility (Std Dev): {growth_volatility:.2f}%")

print("\nPEAK PERIODS:")
print(f"\n  Top 5 Daily Peaks:")
for _peak_idx, peak in top_daily_peaks.iterrows():
    print(f"    {peak['Date'].strftime('%Y-%m-%d')}: {peak['total_operations']:,.0f} operations")

print(f"\n  Top 3 Monthly Peaks:")
for _peak_idx2, peak in top_monthly_peaks.iterrows():
    print(f"    {peak['Month_Year']}: {peak['total_operations']:,.0f} operations")

print("=" * 90)
