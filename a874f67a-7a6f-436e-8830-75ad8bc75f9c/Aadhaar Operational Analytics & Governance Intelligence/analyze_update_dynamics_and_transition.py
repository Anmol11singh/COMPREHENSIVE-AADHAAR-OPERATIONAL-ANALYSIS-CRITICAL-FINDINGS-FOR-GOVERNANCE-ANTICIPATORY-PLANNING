import pandas as pd
import numpy as np

# Analyze enrolment-to-maintenance transition and update fatigue
# Need to look at temporal patterns and cohort transitions

# Combine all data with dates for temporal analysis
enrol_temporal = unified_enrolment.copy()
enrol_temporal['operation_type'] = 'enrolment'

demo_temporal = unified_demographic.copy()
demo_temporal['operation_type'] = 'demographic_update'

bio_temporal = unified_biometric.copy()
bio_temporal['operation_type'] = 'biometric_update'

# Standardize columns for unified analysis
enrol_temporal['operations'] = enrol_temporal[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)
demo_temporal['operations'] = demo_temporal[['demo_age_5_17', 'demo_age_17_']].sum(axis=1)
bio_temporal['operations'] = bio_temporal[['bio_age_5_17', 'bio_age_17_']].sum(axis=1)

# Create unified operations view
enrol_ops = enrol_temporal[['Date', 'state', 'district', 'operation_type', 'operations', 'Month', 'Month_Year']].copy()
demo_ops = demo_temporal[['Date', 'state', 'district', 'operation_type', 'operations', 'Month', 'Month_Year']].copy()
bio_ops = bio_temporal[['Date', 'state', 'district', 'operation_type', 'operations', 'Month', 'Month_Year']].copy()

all_operations = pd.concat([enrol_ops, demo_ops, bio_ops], ignore_index=True)

# --- TRANSITION POINT ANALYSIS ---
# Group by date and operation type to identify transition points
daily_by_type = all_operations.groupby(['Date', 'operation_type'])['operations'].sum().reset_index()
daily_pivot = daily_by_type.pivot(index='Date', columns='operation_type', values='operations').fillna(0).reset_index()
daily_pivot = daily_pivot.sort_values('Date')

# Calculate daily update-to-enrolment ratio to identify when updates dominate
if 'enrolment' in daily_pivot.columns:
    daily_pivot['total_updates'] = daily_pivot.get('demographic_update', 0) + daily_pivot.get('biometric_update', 0)
    daily_pivot['update_to_enrol_ratio'] = daily_pivot['total_updates'] / daily_pivot['enrolment'].replace(0, np.nan)
    
    # Find transition point where updates consistently exceed enrolments
    transition_threshold = 1.0  # Updates equal or exceed enrolments
    daily_pivot['update_dominates'] = daily_pivot['update_to_enrol_ratio'] > transition_threshold
    
    # Find first sustained transition point (3+ consecutive days)
    daily_pivot['consecutive_update_dominance'] = daily_pivot['update_dominates'].rolling(window=3, min_periods=3).sum()
    transition_dates = daily_pivot[daily_pivot['consecutive_update_dominance'] >= 3]
    
    if len(transition_dates) > 0:
        transition_point = transition_dates.iloc[0]['Date']
        print("=== ENROLMENT-TO-MAINTENANCE TRANSITION ANALYSIS ===")
        print(f"\nTransition point identified: {transition_point.strftime('%Y-%m-%d')}")
        print(f"Date when updates began consistently exceeding enrolments (3-day window)")
    else:
        print("=== ENROLMENT-TO-MAINTENANCE TRANSITION ANALYSIS ===")
        print("\nNo clear transition point found - enrolments remain dominant or pattern is mixed")

# Monthly transition analysis
monthly_by_type = all_operations.groupby(['Month_Year', 'operation_type'])['operations'].sum().reset_index()
monthly_pivot = monthly_by_type.pivot(index='Month_Year', columns='operation_type', values='operations').fillna(0).reset_index()

if 'enrolment' in monthly_pivot.columns:
    monthly_pivot['total_updates'] = monthly_pivot.get('demographic_update', 0) + monthly_pivot.get('biometric_update', 0)
    monthly_pivot['update_to_enrol_ratio'] = monthly_pivot['total_updates'] / monthly_pivot['enrolment'].replace(0, np.nan)
    monthly_pivot = monthly_pivot.sort_values('Month_Year')
    
    print(f"\nMonthly Update-to-Enrolment Ratios:")
    print(monthly_pivot[['Month_Year', 'enrolment', 'total_updates', 'update_to_enrol_ratio']].to_string(index=False))

# --- UPDATE FATIGUE ANALYSIS ---
# Analyze temporal distribution of updates to identify fatigue patterns
# Look at growth rates and volatility over time

monthly_demo = demo_temporal.groupby('Month_Year')['operations'].sum().reset_index()
monthly_demo = monthly_demo.sort_values('Month_Year')
monthly_demo['demo_pct_change'] = monthly_demo['operations'].pct_change() * 100

monthly_bio = bio_temporal.groupby('Month_Year')['operations'].sum().reset_index()
monthly_bio = monthly_bio.sort_values('Month_Year')
monthly_bio['bio_pct_change'] = monthly_bio['operations'].pct_change() * 100

print(f"\n=== UPDATE FATIGUE ANALYSIS ===")
print(f"\nDemographic Update Monthly Growth Rates:")
print(monthly_demo[['Month_Year', 'operations', 'demo_pct_change']].to_string(index=False))

print(f"\nBiometric Update Monthly Growth Rates:")
print(monthly_bio[['Month_Year', 'operations', 'bio_pct_change']].to_string(index=False))

# Identify potential fatigue periods (negative growth)
demo_fatigue_months = monthly_demo[monthly_demo['demo_pct_change'] < 0]['Month_Year'].tolist()
bio_fatigue_months = monthly_bio[monthly_bio['bio_pct_change'] < 0]['Month_Year'].tolist()

print(f"\nDemographic update fatigue periods (negative growth): {demo_fatigue_months if demo_fatigue_months else 'None identified'}")
print(f"Biometric update fatigue periods (negative growth): {bio_fatigue_months if bio_fatigue_months else 'None identified'}")

# Calculate update velocity trends
demo_velocity_trend = monthly_demo['demo_pct_change'].mean()
bio_velocity_trend = monthly_bio['bio_pct_change'].mean()

print(f"\nAverage demographic update velocity: {demo_velocity_trend:.2f}% per month")
print(f"Average biometric update velocity: {bio_velocity_trend:.2f}% per month")

if demo_velocity_trend < 0 or bio_velocity_trend < 0:
    print("⚠ Warning: Negative average growth indicates system-wide update fatigue")
else:
    print("✓ Positive growth velocity - updates are increasing over time")

print("\n✓ Update dynamics analyzed: transition points and fatigue patterns identified")
