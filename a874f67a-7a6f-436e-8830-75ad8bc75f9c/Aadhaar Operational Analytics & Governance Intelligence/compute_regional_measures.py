import pandas as pd
import numpy as np

# Regional measures for state and district levels
# Calculate enrolment, update volumes, ratios, and stress scores

# --- STATE-LEVEL ANALYSIS ---
# Enrolments by state
state_enrolment = unified_enrolment.groupby('state').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum', 
    'age_18_greater': 'sum'
}).reset_index()
state_enrolment['total_enrolments'] = state_enrolment[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)

# Demographic updates by state
state_demographic = unified_demographic.groupby('state').agg({
    'demo_age_5_17': 'sum',
    'demo_age_17_': 'sum'
}).reset_index()
state_demographic['total_demo_updates'] = state_demographic[['demo_age_5_17', 'demo_age_17_']].sum(axis=1)

# Biometric updates by state
state_biometric = unified_biometric.groupby('state').agg({
    'bio_age_5_17': 'sum',
    'bio_age_17_': 'sum'
}).reset_index()
state_biometric['total_bio_updates'] = state_biometric[['bio_age_5_17', 'bio_age_17_']].sum(axis=1)

# Merge state-level data
state_metrics = state_enrolment.merge(state_demographic, on='state', how='outer').merge(state_biometric, on='state', how='outer')
state_metrics = state_metrics.fillna(0)

# Calculate state-level ratios and total updates
state_metrics['total_updates'] = state_metrics['total_demo_updates'] + state_metrics['total_bio_updates']
state_metrics['demo_to_enrolment_ratio'] = state_metrics['total_demo_updates'] / state_metrics['total_enrolments'].replace(0, np.nan)
state_metrics['bio_to_enrolment_ratio'] = state_metrics['total_bio_updates'] / state_metrics['total_enrolments'].replace(0, np.nan)
state_metrics['updates_to_enrolment_ratio'] = state_metrics['total_updates'] / state_metrics['total_enrolments'].replace(0, np.nan)

# Calculate state stress score (higher ratio = higher stress)
state_metrics['stress_score'] = state_metrics['updates_to_enrolment_ratio']
state_metrics['stress_rank'] = state_metrics['stress_score'].rank(ascending=False, method='dense')

# State rankings by volume
state_metrics['enrolment_rank'] = state_metrics['total_enrolments'].rank(ascending=False, method='dense')
state_metrics['update_rank'] = state_metrics['total_updates'].rank(ascending=False, method='dense')

print("=== STATE-LEVEL REGIONAL MEASURES ===")
print(f"\nTotal states analyzed: {len(state_metrics)}")
print(f"\nTop 10 States by Enrolment Volume:")
print(state_metrics.nlargest(10, 'total_enrolments')[['state', 'total_enrolments', 'enrolment_rank']].to_string(index=False))
print(f"\nTop 10 States by Update Volume:")
print(state_metrics.nlargest(10, 'total_updates')[['state', 'total_updates', 'update_rank']].to_string(index=False))
print(f"\nTop 10 States by Stress Score (Updates/Enrolment Ratio):")
print(state_metrics.nlargest(10, 'stress_score')[['state', 'stress_score', 'updates_to_enrolment_ratio', 'stress_rank']].to_string(index=False))

# --- DISTRICT-LEVEL ANALYSIS ---
# Enrolments by district
district_enrolment = unified_enrolment.groupby(['state', 'district']).agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
}).reset_index()
district_enrolment['total_enrolments'] = district_enrolment[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)

# Demographic updates by district
district_demographic = unified_demographic.groupby(['state', 'district']).agg({
    'demo_age_5_17': 'sum',
    'demo_age_17_': 'sum'
}).reset_index()
district_demographic['total_demo_updates'] = district_demographic[['demo_age_5_17', 'demo_age_17_']].sum(axis=1)

# Biometric updates by district
district_biometric = unified_biometric.groupby(['state', 'district']).agg({
    'bio_age_5_17': 'sum',
    'bio_age_17_': 'sum'
}).reset_index()
district_biometric['total_bio_updates'] = district_biometric[['bio_age_5_17', 'bio_age_17_']].sum(axis=1)

# Merge district-level data
district_metrics = district_enrolment.merge(district_demographic, on=['state', 'district'], how='outer').merge(district_biometric, on=['state', 'district'], how='outer')
district_metrics = district_metrics.fillna(0)

# Calculate district-level ratios
district_metrics['total_updates'] = district_metrics['total_demo_updates'] + district_metrics['total_bio_updates']
district_metrics['demo_to_enrolment_ratio'] = district_metrics['total_demo_updates'] / district_metrics['total_enrolments'].replace(0, np.nan)
district_metrics['bio_to_enrolment_ratio'] = district_metrics['total_bio_updates'] / district_metrics['total_enrolments'].replace(0, np.nan)
district_metrics['updates_to_enrolment_ratio'] = district_metrics['total_updates'] / district_metrics['total_enrolments'].replace(0, np.nan)

# Calculate district stress score
district_metrics['stress_score'] = district_metrics['updates_to_enrolment_ratio']
district_metrics['stress_rank'] = district_metrics['stress_score'].rank(ascending=False, method='dense')

# District rankings by volume
district_metrics['enrolment_rank'] = district_metrics['total_enrolments'].rank(ascending=False, method='dense')
district_metrics['update_rank'] = district_metrics['total_updates'].rank(ascending=False, method='dense')

print(f"\n=== DISTRICT-LEVEL REGIONAL MEASURES ===")
print(f"\nTotal districts analyzed: {len(district_metrics)}")
print(f"\nTop 10 Districts by Enrolment Volume:")
print(district_metrics.nlargest(10, 'total_enrolments')[['state', 'district', 'total_enrolments', 'enrolment_rank']].to_string(index=False))
print(f"\nTop 10 Districts by Update Volume:")
print(district_metrics.nlargest(10, 'total_updates')[['state', 'district', 'total_updates', 'update_rank']].to_string(index=False))
print(f"\nTop 10 Districts by Stress Score (Updates/Enrolment Ratio):")
print(district_metrics.nlargest(10, 'stress_score')[['state', 'district', 'stress_score', 'updates_to_enrolment_ratio', 'stress_rank']].to_string(index=False))

print("\n✓ Regional measures computed: state/district rankings, volumes, ratios, and stress scores created")
