import pandas as pd
import numpy as np

# Pareto analysis: Identify 80/20 contributors for dates, months, states, and districts
# This reveals high-impact periods and regions

print("=== PARETO ANALYSIS: 80/20 PRINCIPLE ===\n")

# Helper function for Pareto analysis
def pareto_analysis(df, group_col, value_col, analysis_name):
    """Perform Pareto analysis on grouped data"""
    grouped = df.groupby(group_col)[value_col].sum().reset_index()
    grouped = grouped.sort_values(value_col, ascending=False)
    grouped['cumulative_value'] = grouped[value_col].cumsum()
    total_value = grouped[value_col].sum()
    grouped['cumulative_pct'] = (grouped['cumulative_value'] / total_value) * 100
    grouped['value_pct'] = (grouped[value_col] / total_value) * 100
    
    # Find 80% threshold
    pareto_80_contributors = grouped[grouped['cumulative_pct'] <= 80]
    total_contributors = len(grouped)
    vital_few = len(pareto_80_contributors)
    vital_few_pct = (vital_few / total_contributors) * 100
    
    print(f"--- {analysis_name} ---")
    print(f"Total {group_col}: {total_contributors}")
    print(f"Contributors to 80% of volume: {vital_few} ({vital_few_pct:.1f}%)")
    print(f"Pareto validation: {'✓ 80/20 principle holds' if vital_few_pct <= 30 else '⚠ Distribution more balanced than 80/20'}")
    print(f"\nTop 10 {group_col} (vital few):")
    print(pareto_80_contributors.head(10)[[group_col, value_col, 'cumulative_pct']].to_string(index=False))
    print()
    
    return grouped, pareto_80_contributors

# --- DATE-LEVEL PARETO ANALYSIS ---
# Create date-level aggregation from all operations
date_enrol = unified_enrolment.groupby('Date').agg({'age_0_5': 'sum', 'age_5_17': 'sum', 'age_18_greater': 'sum'}).sum(axis=1).reset_index()
date_enrol.columns = ['Date', 'operations']

date_demo = unified_demographic.groupby('Date').agg({'demo_age_5_17': 'sum', 'demo_age_17_': 'sum'}).sum(axis=1).reset_index()
date_demo.columns = ['Date', 'operations']

date_bio = unified_biometric.groupby('Date').agg({'bio_age_5_17': 'sum', 'bio_age_17_': 'sum'}).sum(axis=1).reset_index()
date_bio.columns = ['Date', 'operations']

all_dates = pd.concat([date_enrol, date_demo, date_bio], ignore_index=True)
date_pareto, date_vital = pareto_analysis(all_dates, 'Date', 'operations', 'DATE-LEVEL PARETO')

# --- MONTH-LEVEL PARETO ANALYSIS ---
month_enrol = unified_enrolment.groupby('Month_Year').agg({'age_0_5': 'sum', 'age_5_17': 'sum', 'age_18_greater': 'sum'}).sum(axis=1).reset_index()
month_enrol.columns = ['Month_Year', 'operations']

month_demo = unified_demographic.groupby('Month_Year').agg({'demo_age_5_17': 'sum', 'demo_age_17_': 'sum'}).sum(axis=1).reset_index()
month_demo.columns = ['Month_Year', 'operations']

month_bio = unified_biometric.groupby('Month_Year').agg({'bio_age_5_17': 'sum', 'bio_age_17_': 'sum'}).sum(axis=1).reset_index()
month_bio.columns = ['Month_Year', 'operations']

all_months = pd.concat([month_enrol, month_demo, month_bio], ignore_index=True)
month_pareto, month_vital = pareto_analysis(all_months, 'Month_Year', 'operations', 'MONTH-LEVEL PARETO')

# --- STATE-LEVEL PARETO ANALYSIS ---
# Use pre-computed state metrics
state_ops = state_metrics[['state', 'total_updates']].copy()
state_ops.columns = ['state', 'operations']
state_pareto, state_vital = pareto_analysis(state_ops, 'state', 'operations', 'STATE-LEVEL PARETO')

# --- DISTRICT-LEVEL PARETO ANALYSIS ---
# Use pre-computed district metrics
district_ops = district_metrics[['state', 'district', 'total_updates']].copy()
district_ops['state_district'] = district_ops['state'] + ' - ' + district_ops['district']
district_ops_agg = district_ops[['state_district', 'total_updates']].copy()
district_ops_agg.columns = ['state_district', 'operations']
district_pareto, district_vital = pareto_analysis(district_ops_agg, 'state_district', 'operations', 'DISTRICT-LEVEL PARETO')

# --- SUMMARY OF PARETO FINDINGS ---
print("\n=== PARETO ANALYSIS SUMMARY ===")
print(f"Date contributors to 80%: {len(date_vital)}/{len(date_pareto)} ({len(date_vital)/len(date_pareto)*100:.1f}%)")
print(f"Month contributors to 80%: {len(month_vital)}/{len(month_pareto)} ({len(month_vital)/len(month_pareto)*100:.1f}%)")
print(f"State contributors to 80%: {len(state_vital)}/{len(state_pareto)} ({len(state_vital)/len(state_pareto)*100:.1f}%)")
print(f"District contributors to 80%: {len(district_vital)}/{len(district_pareto)} ({len(district_vital)/len(district_pareto)*100:.1f}%)")

# Identify the single highest impact contributors
top_date = date_vital.iloc[0]['Date'] if len(date_vital) > 0 else None
top_month = month_vital.iloc[0]['Month_Year'] if len(month_vital) > 0 else None
top_state = state_vital.iloc[0]['state'] if len(state_vital) > 0 else None
top_district = district_vital.iloc[0]['state_district'] if len(district_vital) > 0 else None

print(f"\nHighest Impact Contributors:")
print(f"  Date: {top_date}")
print(f"  Month: {top_month}")
print(f"  State: {top_state}")
print(f"  District: {top_district}")

print("\n✓ Pareto analysis complete: 80/20 contributors identified for dates, months, states, and districts")
