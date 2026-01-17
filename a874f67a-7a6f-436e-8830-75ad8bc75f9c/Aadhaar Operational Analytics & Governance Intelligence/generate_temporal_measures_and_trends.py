import pandas as pd
import numpy as np

# Prepare datasets for temporal analysis
enrolment_temporal = unified_enrolment.copy()
demographic_temporal = unified_demographic.copy()
biometric_temporal = unified_biometric.copy()

# Add total columns
enrolment_temporal['total_enrolments'] = (enrolment_temporal['age_0_5'] + 
                                           enrolment_temporal['age_5_17'] + 
                                           enrolment_temporal['age_18_greater'])
demographic_temporal['total_demo_updates'] = (demographic_temporal['demo_age_5_17'] + 
                                               demographic_temporal['demo_age_17_'])
biometric_temporal['total_bio_updates'] = (biometric_temporal['bio_age_5_17'] + 
                                            biometric_temporal['bio_age_17_'])

# DATE-WISE AGGREGATIONS
daily_enrolment = enrolment_temporal.groupby('Date')['total_enrolments'].sum().reset_index()
daily_demographic = demographic_temporal.groupby('Date')['total_demo_updates'].sum().reset_index()
daily_biometric = biometric_temporal.groupby('Date')['total_bio_updates'].sum().reset_index()

daily_trends = daily_enrolment.merge(daily_demographic, on='Date', how='outer')
daily_trends = daily_trends.merge(daily_biometric, on='Date', how='outer')
daily_trends = daily_trends.fillna(0).sort_values('Date')
daily_trends['total_operations'] = (daily_trends['total_enrolments'] + 
                                     daily_trends['total_demo_updates'] + 
                                     daily_trends['total_bio_updates'])

# MONTH-WISE AGGREGATIONS
monthly_enrolment = enrolment_temporal.groupby('Month_Year')['total_enrolments'].sum().reset_index()
monthly_demographic = demographic_temporal.groupby('Month_Year')['total_demo_updates'].sum().reset_index()
monthly_biometric = biometric_temporal.groupby('Month_Year')['total_bio_updates'].sum().reset_index()

monthly_trends = monthly_enrolment.merge(monthly_demographic, on='Month_Year', how='outer')
monthly_trends = monthly_trends.merge(monthly_biometric, on='Month_Year', how='outer')
monthly_trends = monthly_trends.fillna(0).sort_values('Month_Year')
monthly_trends['total_operations'] = (monthly_trends['total_enrolments'] + 
                                       monthly_trends['total_demo_updates'] + 
                                       monthly_trends['total_bio_updates'])

# Calculate MoM Growth
monthly_trends['enrolment_mom_growth'] = monthly_trends['total_enrolments'].pct_change() * 100
monthly_trends['demo_mom_growth'] = monthly_trends['total_demo_updates'].pct_change() * 100
monthly_trends['bio_mom_growth'] = monthly_trends['total_bio_updates'].pct_change() * 100
monthly_trends['operations_mom_growth'] = monthly_trends['total_operations'].pct_change() * 100

# Calculate MoM Acceleration (second derivative)
monthly_trends['enrolment_mom_acceleration'] = monthly_trends['enrolment_mom_growth'].diff()
monthly_trends['operations_mom_acceleration'] = monthly_trends['operations_mom_growth'].diff()

# YEAR-WISE AGGREGATIONS - Handle NaN values properly
enrolment_temporal['Year_int'] = enrolment_temporal['Year'].fillna(0).astype(int)
demographic_temporal['Year_int'] = demographic_temporal['Year'].fillna(0).astype(int)
biometric_temporal['Year_int'] = biometric_temporal['Year'].fillna(0).astype(int)

# Filter out year 0 (NaN values)
enrolment_temporal_valid = enrolment_temporal[enrolment_temporal['Year_int'] > 0]
demographic_temporal_valid = demographic_temporal[demographic_temporal['Year_int'] > 0]
biometric_temporal_valid = biometric_temporal[biometric_temporal['Year_int'] > 0]

yearly_enrolment = enrolment_temporal_valid.groupby('Year_int')['total_enrolments'].sum().reset_index()
yearly_demographic = demographic_temporal_valid.groupby('Year_int')['total_demo_updates'].sum().reset_index()
yearly_biometric = biometric_temporal_valid.groupby('Year_int')['total_bio_updates'].sum().reset_index()

yearly_trends = yearly_enrolment.merge(yearly_demographic, on='Year_int', how='outer')
yearly_trends = yearly_trends.merge(yearly_biometric, on='Year_int', how='outer')
yearly_trends = yearly_trends.fillna(0).sort_values('Year_int')
yearly_trends['total_operations'] = (yearly_trends['total_enrolments'] + 
                                      yearly_trends['total_demo_updates'] + 
                                      yearly_trends['total_bio_updates'])

# Calculate YoY Growth
yearly_trends['enrolment_yoy_growth'] = yearly_trends['total_enrolments'].pct_change() * 100
yearly_trends['demo_yoy_growth'] = yearly_trends['total_demo_updates'].pct_change() * 100
yearly_trends['bio_yoy_growth'] = yearly_trends['total_bio_updates'].pct_change() * 100
yearly_trends['operations_yoy_growth'] = yearly_trends['total_operations'].pct_change() * 100

# Display summary statistics
print("=" * 80)
print("TEMPORAL MEASURES SUMMARY")
print("=" * 80)

print(f"\nDAILY TRENDS:")
print(f"  Total Days with Activity: {len(daily_trends)}")
print(f"  Avg Daily Enrolments: {daily_trends['total_enrolments'].mean():,.0f}")
print(f"  Avg Daily Demographic Updates: {daily_trends['total_demo_updates'].mean():,.0f}")
print(f"  Avg Daily Biometric Updates: {daily_trends['total_bio_updates'].mean():,.0f}")
print(f"  Avg Daily Total Operations: {daily_trends['total_operations'].mean():,.0f}")
print(f"  Peak Daily Operations: {daily_trends['total_operations'].max():,.0f} on {daily_trends.loc[daily_trends['total_operations'].idxmax(), 'Date'].strftime('%Y-%m-%d')}")

print(f"\nMONTHLY TRENDS:")
print(f"  Total Months with Activity: {len(monthly_trends)}")
print(f"  Avg Monthly Enrolments: {monthly_trends['total_enrolments'].mean():,.0f}")
print(f"  Avg Monthly Demographic Updates: {monthly_trends['total_demo_updates'].mean():,.0f}")
print(f"  Avg Monthly Biometric Updates: {monthly_trends['total_bio_updates'].mean():,.0f}")
print(f"  Peak Month: {monthly_trends.loc[monthly_trends['total_operations'].idxmax(), 'Month_Year']} with {monthly_trends['total_operations'].max():,.0f} operations")
print(f"  Avg MoM Enrolment Growth: {monthly_trends['enrolment_mom_growth'].mean():.2f}%")
print(f"  Avg MoM Operations Growth: {monthly_trends['operations_mom_growth'].mean():.2f}%")

print(f"\nYEARLY TRENDS:")
print(f"  Total Years with Activity: {len(yearly_trends)}")
print(f"  Year-over-Year Growth:")
for _, row in yearly_trends.iterrows():
    if pd.notna(row['enrolment_yoy_growth']):
        print(f"    {int(row['Year_int'])}: Enrolments {row['enrolment_yoy_growth']:+.1f}%, Operations {row['operations_yoy_growth']:+.1f}%")

print("=" * 80)
