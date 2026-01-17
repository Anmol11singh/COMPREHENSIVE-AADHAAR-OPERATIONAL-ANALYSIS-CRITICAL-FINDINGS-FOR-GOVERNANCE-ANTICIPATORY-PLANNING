import pandas as pd
import numpy as np

print("=" * 90)
print("SYSTEM RESILIENCE & RECOVERY TIME QUANTIFICATION")
print("=" * 90)

# Quantify how system responds to and recovers from high-load events
# Measure resilience and recovery times from anomalies and stress periods

print(f"\n🔧 METHODOLOGY:")
print(f"  - Identify stress events (anomalies and high-load periods)")
print(f"  - Measure recovery time back to baseline performance")
print(f"  - Calculate resilience metrics (capacity utilization, degradation)")
print(f"  - Quantify system stability and shock absorption")

# Use anomaly detection results as stress events
stress_events = daily_anomalies.copy()
stress_events = stress_events.sort_values('Date')

print(f"\n" + "=" * 90)
print("STRESS EVENT IDENTIFICATION")
print("=" * 90)

print(f"\n📊 IDENTIFIED STRESS EVENTS: {len(stress_events)}")
print(f"\n  Recent stress events:")
for _, event in stress_events.head(10).iterrows():
    event_types = []
    if event['is_spike_zscore']:
        event_types.append('Z-score spike')
    if event['is_spike_iqr']:
        event_types.append('IQR spike')
    if event['is_drop_iqr']:
        event_types.append('IQR drop')
    print(f"    {event['Date'].strftime('%Y-%m-%d')}: {event['total_operations']:,.0f} ops ({', '.join(event_types)})")

# Recovery time analysis
print(f"\n" + "=" * 90)
print("RECOVERY TIME ANALYSIS")
print("=" * 90)

baseline_ops = daily_trends['total_operations'].median()
recovery_threshold = baseline_ops * 1.2  # Within 20% of baseline is considered recovered

print(f"\n📊 RECOVERY METRICS:")
print(f"  Baseline operational level: {baseline_ops:,.0f} operations/day")
print(f"  Recovery threshold (120% of baseline): {recovery_threshold:,.0f} operations/day")

# Analyze recovery from each stress event
recovery_analysis = []

for i, event in stress_events.iterrows():
    event_date = event['Date']
    event_load = event['total_operations']
    
    # Look ahead to find when operations return below recovery threshold
    future_ops = daily_trends[daily_trends['Date'] > event_date].copy()
    
    if len(future_ops) > 0:
        # Find first day operations return below threshold
        recovered = future_ops[future_ops['total_operations'] <= recovery_threshold]
        
        if len(recovered) > 0:
            recovery_date = recovered.iloc[0]['Date']
            recovery_days = (recovery_date - event_date).days
            
            # Calculate peak excess load
            peak_excess = ((event_load - baseline_ops) / baseline_ops) * 100
            
            recovery_analysis.append({
                'event_date': event_date,
                'event_load': event_load,
                'recovery_date': recovery_date,
                'recovery_days': recovery_days,
                'peak_excess_pct': peak_excess,
                'event_type': 'spike' if event_load > baseline_ops else 'drop'
            })

recovery_df = pd.DataFrame(recovery_analysis)

if len(recovery_df) > 0:
    avg_recovery_days = recovery_df['recovery_days'].mean()
    median_recovery_days = recovery_df['recovery_days'].median()
    max_recovery_days = recovery_df['recovery_days'].max()
    
    print(f"\n📈 RECOVERY TIME STATISTICS:")
    print(f"  Average recovery time: {avg_recovery_days:.1f} days")
    print(f"  Median recovery time: {median_recovery_days:.1f} days")
    print(f"  Maximum recovery time: {max_recovery_days:.0f} days")
    
    print(f"\n  Recovery time breakdown:")
    recovery_counts = recovery_df['recovery_days'].value_counts().sort_index()
    for days, count in recovery_counts.head(5).items():
        print(f"    {days} days: {count} events")
    
    # Show specific recovery examples
    print(f"\n  Recent recovery examples:")
    for _, rec in recovery_df.head(5).iterrows():
        print(f"    {rec['event_date'].strftime('%Y-%m-%d')} spike ({rec['peak_excess_pct']:+.0f}% above baseline) ")
        print(f"      → Recovered by {rec['recovery_date'].strftime('%Y-%m-%d')} ({rec['recovery_days']} days)")
else:
    print(f"\n  ℹ️ Insufficient data to calculate recovery times")
    print(f"     (stress events may be at end of dataset)")
    avg_recovery_days = np.nan

# Resilience metrics
print(f"\n" + "=" * 90)
print("SYSTEM RESILIENCE METRICS")
print("=" * 90)

# Calculate operational capacity metrics
max_observed_load = daily_trends['total_operations'].max()
avg_load = daily_trends['total_operations'].mean()
capacity_utilization = (avg_load / max_observed_load) * 100

# Stress absorption capacity
p99_load = daily_trends['total_operations'].quantile(0.99)
stress_absorption_capacity = ((p99_load - baseline_ops) / baseline_ops) * 100

# Load volatility as inverse resilience
load_cv = (daily_trends['total_operations'].std() / daily_trends['total_operations'].mean()) * 100

# Calculate frequency of stress events
total_days = len(daily_trends)
stress_event_frequency = (len(stress_events) / total_days) * 100

print(f"\n📊 RESILIENCE INDICATORS:")
print(f"\n1. OPERATIONAL CAPACITY:")
print(f"   Maximum observed load: {max_observed_load:,.0f} operations/day")
print(f"   Average load: {avg_load:,.0f} operations/day")
print(f"   Capacity utilization: {capacity_utilization:.1f}%")
print(f"   Interpretation: {'High efficiency' if capacity_utilization > 50 else 'Low utilization - excess capacity available'}")

print(f"\n2. STRESS ABSORPTION CAPACITY:")
print(f"   99th percentile load: {p99_load:,.0f} operations/day")
print(f"   Stress absorption: {stress_absorption_capacity:+.0f}% above baseline")
print(f"   Interpretation: System can handle {stress_absorption_capacity:.0f}% surge above baseline")

print(f"\n3. STABILITY METRICS:")
print(f"   Coefficient of variation: {load_cv:.1f}%")
print(f"   Stress event frequency: {stress_event_frequency:.1f}% of days")
print(f"   Interpretation: {'High volatility' if load_cv > 100 else 'Moderate volatility' if load_cv > 50 else 'Stable operations'}")

if not np.isnan(avg_recovery_days):
    print(f"\n4. RECOVERY PERFORMANCE:")
    print(f"   Average recovery time: {avg_recovery_days:.1f} days")
    print(f"   Recovery speed: {'Fast' if avg_recovery_days < 2 else 'Moderate' if avg_recovery_days < 5 else 'Slow'}")
    print(f"   Interpretation: System returns to baseline in {avg_recovery_days:.1f} days on average")

# System resilience score
print(f"\n" + "=" * 90)
print("SYSTEM RESILIENCE SCORE")
print("=" * 90)

# Calculate composite resilience score (0-100)
# Higher is better
components = []

# Low stress frequency is good (max 10 points if <5% days are stress events)
stress_freq_score = max(0, min(10, 10 * (1 - (stress_event_frequency / 20))))
components.append(('Stress Event Frequency', stress_freq_score))

# Low volatility is good (max 20 points if CV < 50%)
volatility_score = max(0, min(20, 20 * (1 - (load_cv / 200))))
components.append(('Load Stability', volatility_score))

# High spare capacity is good (max 30 points if utilization < 50%)
spare_capacity_score = max(0, min(30, 30 * (1 - (capacity_utilization / 100))))
components.append(('Spare Capacity', spare_capacity_score))

# Fast recovery is good (max 20 points if < 2 days)
if not np.isnan(avg_recovery_days):
    recovery_score = max(0, min(20, 20 * (1 - (avg_recovery_days / 10))))
else:
    recovery_score = 10  # Neutral score if no data
components.append(('Recovery Speed', recovery_score))

# High absorption capacity is good (max 20 points if >500% baseline)
absorption_score = min(20, (stress_absorption_capacity / 500) * 20)
components.append(('Stress Absorption', absorption_score))

total_resilience_score = sum([s for _, s in components])

print(f"\n🏆 COMPOSITE RESILIENCE SCORE: {total_resilience_score:.1f} / 100")
print(f"\n  Component breakdown:")
for component, score in components:
    print(f"    {component}: {score:.1f} points")

print(f"\n  Overall assessment:")
if total_resilience_score >= 75:
    assessment = "EXCELLENT - System demonstrates strong resilience and recovery capability"
elif total_resilience_score >= 50:
    assessment = "GOOD - System shows adequate resilience with room for improvement"
elif total_resilience_score >= 30:
    assessment = "MODERATE - System faces challenges; capacity planning recommended"
else:
    assessment = "CONCERNING - System under significant stress; immediate intervention needed"
print(f"    {assessment}")

# Recommendations
print(f"\n" + "=" * 90)
print("RESILIENCE IMPROVEMENT RECOMMENDATIONS")
print("=" * 90)

print(f"\n📋 PRIORITY ACTIONS:")

if stress_event_frequency > 15:
    print(f"  🔴 HIGH: Stress events occur in {stress_event_frequency:.1f}% of days")
    print(f"     → Increase baseline capacity to reduce frequency of overload")

if load_cv > 100:
    print(f"  🔴 HIGH: High load volatility (CV = {load_cv:.1f}%)")
    print(f"     → Implement demand smoothing and better forecasting")

if not np.isnan(avg_recovery_days) and avg_recovery_days > 3:
    print(f"  🟠 MEDIUM: Slow recovery time ({avg_recovery_days:.1f} days)")
    print(f"     → Develop faster incident response protocols")

if capacity_utilization > 70:
    print(f"  🟠 MEDIUM: High capacity utilization ({capacity_utilization:.1f}%)")
    print(f"     → Plan for capacity expansion to maintain headroom")

if stress_absorption_capacity < 200:
    print(f"  🟡 LOW: Limited surge capacity ({stress_absorption_capacity:.0f}% above baseline)")
    print(f"     → Build buffer capacity for unexpected demand spikes")

print(f"\n✅ System resilience quantified")
print(f"   - Recovery time: {avg_recovery_days:.1f} days average" if not np.isnan(avg_recovery_days) else "   - Recovery time: Insufficient data")
print(f"   - Resilience score: {total_resilience_score:.0f}/100")
print(f"   - Stress absorption: {stress_absorption_capacity:.0f}% surge capacity")
print(f"   - Capacity utilization: {capacity_utilization:.1f}%")
