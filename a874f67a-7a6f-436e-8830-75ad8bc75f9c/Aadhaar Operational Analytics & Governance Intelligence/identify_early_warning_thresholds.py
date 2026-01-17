import pandas as pd
import numpy as np

print("=" * 90)
print("EARLY WARNING SYSTEM: THRESHOLDS & PREDICTIVE SIGNALS")
print("=" * 90)

# Use existing anomaly detection thresholds as basis for early warning
# Combine with operational capacity metrics

print(f"\n🎯 THRESHOLD DEFINITION METHODOLOGY:")
print(f"  - Statistical thresholds based on historical IQR and Z-scores")
print(f"  - Operational capacity based on baseline performance")
print(f"  - Multi-level alert system: Yellow, Orange, Red")
print(f"  - Combines volume, velocity, and trend indicators")

# Define early warning thresholds
print(f"\n" + "=" * 90)
print("OPERATIONAL LOAD THRESHOLDS")
print("=" * 90)

# Baseline metrics from existing analysis
baseline_daily_ops = daily_trends['total_operations'].median()
baseline_std = daily_trends['total_operations'].std()
p75_daily = daily_trends['total_operations'].quantile(0.75)
p90_daily = daily_trends['total_operations'].quantile(0.90)
p95_daily = daily_trends['total_operations'].quantile(0.95)

print(f"\n📊 DAILY OPERATIONAL THRESHOLDS:")
print(f"  Baseline (Median): {baseline_daily_ops:,.0f} operations/day")
print(f"  Standard Deviation: {baseline_std:,.0f}")
print(f"\n  ⚠️ WARNING LEVELS:")
print(f"    🟡 YELLOW Alert (75th percentile): {p75_daily:,.0f} operations")
print(f"       → Elevated load - monitor closely")
print(f"    🟠 ORANGE Alert (90th percentile): {p90_daily:,.0f} operations")
print(f"       → High stress - prepare surge capacity")
print(f"    🔴 RED Alert (95th percentile): {p95_daily:,.0f} operations")
print(f"       → Critical load - activate emergency protocols")

# Growth rate thresholds
growth_threshold_warning = 50  # 50% growth triggers warning
growth_threshold_critical = 100  # 100% growth is critical

print(f"\n📈 GROWTH RATE THRESHOLDS (Day-over-Day):")
print(f"  🟡 YELLOW: >{growth_threshold_warning}% increase")
print(f"  🟠 ORANGE: >{growth_threshold_critical}% increase")
print(f"  🔴 RED: >{growth_threshold_critical * 1.5}% increase")

# Update velocity thresholds (based on lead-lag analysis)
print(f"\n" + "=" * 90)
print("UPDATE VOLUME EARLY WARNING INDICATORS")
print("=" * 90)

# Calculate typical update volumes
baseline_demo_updates = daily_trends['total_demo_updates'].median()
baseline_bio_updates = daily_trends['total_bio_updates'].median()

p75_demo = daily_trends['total_demo_updates'].quantile(0.75)
p90_demo = daily_trends['total_demo_updates'].quantile(0.90)

p75_bio = daily_trends['total_bio_updates'].quantile(0.75)
p90_bio = daily_trends['total_bio_updates'].quantile(0.90)

print(f"\n📊 DEMOGRAPHIC UPDATE THRESHOLDS:")
print(f"  Baseline (Median): {baseline_demo_updates:,.0f} updates/day")
print(f"  🟡 YELLOW: {p75_demo:,.0f} updates (75th percentile)")
print(f"  🟠 ORANGE: {p90_demo:,.0f} updates (90th percentile)")

print(f"\n📊 BIOMETRIC UPDATE THRESHOLDS:")
print(f"  Baseline (Median): {baseline_bio_updates:,.0f} updates/day")
print(f"  🟡 YELLOW: {p75_bio:,.0f} updates (75th percentile)")
print(f"  🟠 ORANGE: {p90_bio:,.0f} updates (90th percentile)")

# Predictive signals based on lead-lag analysis
print(f"\n" + "=" * 90)
print("PREDICTIVE SIGNALS & LEADING INDICATORS")
print("=" * 90)

print(f"\n🔮 EARLY WARNING SIGNALS:")
print(f"\n1. UPDATE VOLUME SURGE (1-4 day lead time):")
print(f"   → Demographic updates spike above {p75_demo:,.0f}")
print(f"   → Biometric updates spike above {p75_bio:,.0f}")
print(f"   Interpretation: Based on lead-lag analysis, update surges")
print(f"   correlate with operational load 1-4 days ahead")

print(f"\n2. MULTI-DAY SUSTAINED ELEVATION:")
print(f"   → 3+ consecutive days above {p75_daily:,.0f} operations")
print(f"   Interpretation: Sustained high load indicates systemic pressure,")
print(f"   not temporary spike")

print(f"\n3. VELOCITY ACCELERATION:")
print(f"   → Day-over-day growth exceeding {growth_threshold_warning}%")
print(f"   → 3-day moving average growth > 30%")
print(f"   Interpretation: Accelerating growth suggests imminent capacity issues")

print(f"\n4. REGIONAL CONCENTRATION:")
print(f"   → Top 3 states account for >50% of daily operations")
print(f"   → Single state exceeds 25% of daily operations")
print(f"   Interpretation: Geographic concentration creates bottleneck risk")

# Create alert classification function
def classify_alert_level(operations, demo_updates, bio_updates, growth_rate):
    """Classify operational status into alert levels"""
    alert_level = "GREEN"
    reasons = []
    
    # Check operational volume
    if operations >= p95_daily:
        alert_level = "RED"
        reasons.append(f"Operations at {operations:,.0f} (>95th percentile)")
    elif operations >= p90_daily:
        if alert_level != "RED":
            alert_level = "ORANGE"
        reasons.append(f"Operations at {operations:,.0f} (>90th percentile)")
    elif operations >= p75_daily:
        if alert_level not in ["RED", "ORANGE"]:
            alert_level = "YELLOW"
        reasons.append(f"Operations at {operations:,.0f} (>75th percentile)")
    
    # Check update volumes
    if demo_updates >= p90_demo:
        if alert_level not in ["RED"]:
            alert_level = "ORANGE"
        reasons.append(f"Demographic updates at {demo_updates:,.0f} (>90th percentile)")
    elif demo_updates >= p75_demo:
        if alert_level not in ["RED", "ORANGE"]:
            alert_level = "YELLOW"
        reasons.append(f"Demographic updates elevated ({demo_updates:,.0f})")
    
    if bio_updates >= p90_bio:
        if alert_level not in ["RED"]:
            alert_level = "ORANGE"
        reasons.append(f"Biometric updates at {bio_updates:,.0f} (>90th percentile)")
    elif bio_updates >= p75_bio:
        if alert_level not in ["RED", "ORANGE"]:
            alert_level = "YELLOW"
        reasons.append(f"Biometric updates elevated ({bio_updates:,.0f})")
    
    # Check growth rate
    if not np.isnan(growth_rate):
        if growth_rate > growth_threshold_critical * 1.5:
            alert_level = "RED"
            reasons.append(f"Critical growth rate: {growth_rate:.1f}%")
        elif growth_rate > growth_threshold_critical:
            if alert_level not in ["RED"]:
                alert_level = "ORANGE"
            reasons.append(f"High growth rate: {growth_rate:.1f}%")
        elif growth_rate > growth_threshold_warning:
            if alert_level not in ["RED", "ORANGE"]:
                alert_level = "YELLOW"
            reasons.append(f"Elevated growth rate: {growth_rate:.1f}%")
    
    return alert_level, reasons

# Apply to historical data
alert_analysis = daily_trends.copy()
alert_analysis['growth_rate'] = alert_analysis['total_operations'].pct_change() * 100
alert_analysis['alert_level'] = None
alert_analysis['alert_reasons'] = None

for idx, row in alert_analysis.iterrows():
    level, reasons = classify_alert_level(
        row['total_operations'],
        row['total_demo_updates'],
        row['total_bio_updates'],
        row['growth_rate']
    )
    alert_analysis.at[idx, 'alert_level'] = level
    alert_analysis.at[idx, 'alert_reasons'] = '; '.join(reasons) if reasons else 'Normal operations'

# Summarize alert history
print(f"\n" + "=" * 90)
print("HISTORICAL ALERT ANALYSIS")
print("=" * 90)

alert_counts = alert_analysis['alert_level'].value_counts()
print(f"\n📊 ALERT DISTRIBUTION (Historical Data):")
for level in ['GREEN', 'YELLOW', 'ORANGE', 'RED']:
    count = alert_counts.get(level, 0)
    pct = (count / len(alert_analysis)) * 100
    emoji = {'GREEN': '🟢', 'YELLOW': '🟡', 'ORANGE': '🟠', 'RED': '🔴'}.get(level, '')
    print(f"  {emoji} {level}: {count} days ({pct:.1f}%)")

# Show recent high-alert days
high_alerts = alert_analysis[alert_analysis['alert_level'].isin(['ORANGE', 'RED'])].copy()
if len(high_alerts) > 0:
    print(f"\n⚠️ HIGH-ALERT DAYS:")
    for _, alert in high_alerts.head(10).iterrows():
        print(f"  {alert['Date'].strftime('%Y-%m-%d')} [{alert['alert_level']}]: {alert['alert_reasons']}")
else:
    print(f"\n✅ No high-alert days in historical data")

# Recommendations
print(f"\n" + "=" * 90)
print("OPERATIONAL RECOMMENDATIONS")
print("=" * 90)

print(f"\n📋 MONITORING PROTOCOL:")
print(f"  1. Track daily operations against thresholds:")
print(f"     - GREEN (<{p75_daily:,.0f}): Normal monitoring")
print(f"     - YELLOW ({p75_daily:,.0f}-{p90_daily:,.0f}): Enhanced monitoring")
print(f"     - ORANGE ({p90_daily:,.0f}-{p95_daily:,.0f}): Alert senior management")
print(f"     - RED (>{p95_daily:,.0f}): Activate emergency response")

print(f"\n  2. Monitor leading indicators:")
print(f"     - Update volumes (1-4 day lead on operational load)")
print(f"     - Growth velocity (acceleration signals)")
print(f"     - Regional concentration (bottleneck risk)")

print(f"\n  3. Response protocols by alert level:")
print(f"     YELLOW → Prepare contingency resources")
print(f"     ORANGE → Deploy additional capacity, extended hours")
print(f"     RED → Emergency protocols, maximum capacity, executive escalation")

print(f"\n✅ Early warning system defined with actionable thresholds")
print(f"   - Multi-level alert framework (GREEN/YELLOW/ORANGE/RED)")
print(f"   - Predictive signals with 1-4 day lead time")
print(f"   - Clear operational response protocols")
