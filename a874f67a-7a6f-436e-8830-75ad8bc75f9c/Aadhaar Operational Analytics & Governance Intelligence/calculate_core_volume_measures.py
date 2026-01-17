import pandas as pd
import numpy as np

# Calculate total enrolments by age group
total_enrolments_age_0_5 = unified_enrolment['age_0_5'].sum()
total_enrolments_age_5_17 = unified_enrolment['age_5_17'].sum()
total_enrolments_age_18_plus = unified_enrolment['age_18_greater'].sum()
total_enrolments = total_enrolments_age_0_5 + total_enrolments_age_5_17 + total_enrolments_age_18_plus

# Calculate total demographic updates by age group
total_demo_updates_5_17 = unified_demographic['demo_age_5_17'].sum()
total_demo_updates_17_plus = unified_demographic['demo_age_17_'].sum()
total_demo_updates = total_demo_updates_5_17 + total_demo_updates_17_plus

# Calculate total biometric updates by age group
total_bio_updates_5_17 = unified_biometric['bio_age_5_17'].sum()
total_bio_updates_17_plus = unified_biometric['bio_age_17_'].sum()
total_bio_updates = total_bio_updates_5_17 + total_bio_updates_17_plus

# Calculate total updates
total_updates = total_demo_updates + total_bio_updates

# Calculate ratios
demo_to_enrolment_ratio = total_demo_updates / total_enrolments if total_enrolments > 0 else 0
bio_to_enrolment_ratio = total_bio_updates / total_enrolments if total_enrolments > 0 else 0
updates_to_enrolment_ratio = total_updates / total_enrolments if total_enrolments > 0 else 0

# Calculate Operational Load Index (weighted combination of enrolments and updates)
# OLI = normalized sum of activities, with updates weighted higher due to complexity
oli = (total_enrolments + (total_updates * 1.5)) / 1000  # Scaled per 1000 operations

# Create core metrics summary
core_metrics = {
    'Total Enrolments': total_enrolments,
    'Enrolments Age 0-5': total_enrolments_age_0_5,
    'Enrolments Age 5-17': total_enrolments_age_5_17,
    'Enrolments Age 18+': total_enrolments_age_18_plus,
    'Total Demographic Updates': total_demo_updates,
    'Demo Updates Age 5-17': total_demo_updates_5_17,
    'Demo Updates Age 17+': total_demo_updates_17_plus,
    'Total Biometric Updates': total_bio_updates,
    'Bio Updates Age 5-17': total_bio_updates_5_17,
    'Bio Updates Age 17+': total_bio_updates_17_plus,
    'Total Updates (Demo + Bio)': total_updates,
    'Demo/Enrolment Ratio': round(demo_to_enrolment_ratio, 4),
    'Bio/Enrolment Ratio': round(bio_to_enrolment_ratio, 4),
    'Updates/Enrolment Ratio': round(updates_to_enrolment_ratio, 4),
    'Operational Load Index': round(oli, 2)
}

# Display core metrics
print("=" * 70)
print("CORE VOLUME MEASURES")
print("=" * 70)
print("\nENROLMENT VOLUMES:")
print(f"  Total Enrolments: {total_enrolments:,}")
print(f"    - Age 0-5: {total_enrolments_age_0_5:,} ({total_enrolments_age_0_5/total_enrolments*100:.1f}%)")
print(f"    - Age 5-17: {total_enrolments_age_5_17:,} ({total_enrolments_age_5_17/total_enrolments*100:.1f}%)")
print(f"    - Age 18+: {total_enrolments_age_18_plus:,} ({total_enrolments_age_18_plus/total_enrolments*100:.1f}%)")

print("\nUPDATE VOLUMES:")
print(f"  Total Demographic Updates: {total_demo_updates:,}")
print(f"    - Age 5-17: {total_demo_updates_5_17:,} ({total_demo_updates_5_17/total_demo_updates*100:.1f}%)")
print(f"    - Age 17+: {total_demo_updates_17_plus:,} ({total_demo_updates_17_plus/total_demo_updates*100:.1f}%)")
print(f"  Total Biometric Updates: {total_bio_updates:,}")
print(f"    - Age 5-17: {total_bio_updates_5_17:,} ({total_bio_updates_5_17/total_bio_updates*100:.1f}%)")
print(f"    - Age 17+: {total_bio_updates_17_plus:,} ({total_bio_updates_17_plus/total_bio_updates*100:.1f}%)")
print(f"  Total Updates (Demo + Bio): {total_updates:,}")

print("\nRATIOS & OPERATIONAL METRICS:")
print(f"  Demographic/Enrolment Ratio: {demo_to_enrolment_ratio:.4f}")
print(f"  Biometric/Enrolment Ratio: {bio_to_enrolment_ratio:.4f}")
print(f"  Total Updates/Enrolment Ratio: {updates_to_enrolment_ratio:.4f}")
print(f"  Operational Load Index: {oli:,.2f}")
print("=" * 70)
