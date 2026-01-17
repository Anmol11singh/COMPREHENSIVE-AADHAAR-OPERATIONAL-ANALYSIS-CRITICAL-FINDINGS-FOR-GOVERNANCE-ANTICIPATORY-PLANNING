import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# Set Zerve design system colors
bg_color = '#1D1D20'
text_color = '#fbfbff'
secondary_text = '#909094'
zerve_colors = ['#A1C9F4', '#FFB482', '#8DE5A1', '#FF9F9B', '#D0BBFF', '#1F77B4']
highlight_color = '#ffd400'
warning_color = '#f04438'

# Create figure with multiple subplots
fig = plt.figure(figsize=(16, 12))
fig.patch.set_facecolor(bg_color)

# 1. Daily Operations Trend with Anomalies
ax1 = plt.subplot(3, 2, 1)
ax1.set_facecolor(bg_color)
ax1.plot(daily_stats['Date'], daily_stats['total_operations'], 
         color=zerve_colors[0], linewidth=2, label='Daily Operations')
# Highlight anomalies
anomaly_mask = daily_stats['is_anomaly']
ax1.scatter(daily_stats[anomaly_mask]['Date'], 
           daily_stats[anomaly_mask]['total_operations'],
           color=warning_color, s=100, zorder=5, label='Anomalies', alpha=0.8)
ax1.set_title('Daily Operations with Anomaly Detection', 
              fontsize=14, fontweight='bold', color=text_color, pad=15)
ax1.set_xlabel('Date', fontsize=11, color=text_color)
ax1.set_ylabel('Operations', fontsize=11, color=text_color)
ax1.tick_params(colors=text_color, labelsize=9)
ax1.legend(facecolor=bg_color, edgecolor=secondary_text, labelcolor=text_color, fontsize=9)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax1.grid(False)

# 2. Monthly Operations Trend
ax2 = plt.subplot(3, 2, 2)
ax2.set_facecolor(bg_color)
months_sorted = pd.to_datetime(monthly_stats['Month_Year'], errors='coerce')
valid_months = ~months_sorted.isna()
ax2.bar(range(len(monthly_stats[valid_months])), 
       monthly_stats[valid_months]['total_operations'],
       color=zerve_colors[0], alpha=0.8, width=0.7)
ax2.set_title('Monthly Operations Volume', 
              fontsize=14, fontweight='bold', color=text_color, pad=15)
ax2.set_xlabel('Month', fontsize=11, color=text_color)
ax2.set_ylabel('Operations', fontsize=11, color=text_color)
ax2.tick_params(colors=text_color, labelsize=9)
ax2.set_xticks(range(len(monthly_stats[valid_months])))
ax2.set_xticklabels(monthly_stats[valid_months]['Month_Year'], rotation=45, ha='right')
ax2.grid(False)

# 3. Operations Composition (Daily Average)
ax3 = plt.subplot(3, 2, 3)
ax3.set_facecolor(bg_color)
avg_enrolments = daily_stats['total_enrolments'].mean()
avg_demo = daily_stats['total_demo_updates'].mean()
avg_bio = daily_stats['total_bio_updates'].mean()
operations_breakdown = [avg_enrolments, avg_demo, avg_bio]
operations_labels = ['Enrolments', 'Demo Updates', 'Bio Updates']
bars = ax3.barh(operations_labels, operations_breakdown, 
               color=[zerve_colors[0], zerve_colors[1], zerve_colors[2]], alpha=0.85)
ax3.set_title('Average Daily Operations Breakdown', 
              fontsize=14, fontweight='bold', color=text_color, pad=15)
ax3.set_xlabel('Average Daily Volume', fontsize=11, color=text_color)
ax3.tick_params(colors=text_color, labelsize=9)
ax3.grid(False)
# Add value labels
for i, (bar, val) in enumerate(zip(bars, operations_breakdown)):
    ax3.text(val + val*0.02, i, f'{val:,.0f}', 
            va='center', color=text_color, fontsize=9)

# 4. Month-over-Month Growth Rates
ax4 = plt.subplot(3, 2, 4)
ax4.set_facecolor(bg_color)
valid_growth = monthly_stats[valid_months & monthly_stats['operations_mom_growth'].notna()]
ax4.plot(range(len(valid_growth)), valid_growth['operations_mom_growth'],
        color=zerve_colors[2], marker='o', linewidth=2, markersize=6)
ax4.axhline(y=0, color=secondary_text, linestyle='--', linewidth=1, alpha=0.5)
ax4.set_title('Month-over-Month Growth Rate', 
              fontsize=14, fontweight='bold', color=text_color, pad=15)
ax4.set_xlabel('Month', fontsize=11, color=text_color)
ax4.set_ylabel('Growth Rate (%)', fontsize=11, color=text_color)
ax4.tick_params(colors=text_color, labelsize=9)
ax4.set_xticks(range(len(valid_growth)))
ax4.set_xticklabels(valid_growth['Month_Year'], rotation=45, ha='right')
ax4.grid(False)

# 5. Enrolments by Age Group Distribution
ax5 = plt.subplot(3, 2, 5)
ax5.set_facecolor(bg_color)
age_groups = ['Age 0-5', 'Age 5-17', 'Age 18+']
age_values = [total_enrolments_age_0_5, total_enrolments_age_5_17, total_enrolments_age_18_plus]
bars = ax5.bar(age_groups, age_values, 
              color=[zerve_colors[3], zerve_colors[4], zerve_colors[5]], alpha=0.85)
ax5.set_title('Total Enrolments by Age Group', 
              fontsize=14, fontweight='bold', color=text_color, pad=15)
ax5.set_ylabel('Total Enrolments', fontsize=11, color=text_color)
ax5.tick_params(colors=text_color, labelsize=9)
ax5.grid(False)
# Add percentage labels
for bar, val in zip(bars, age_values):
    pct = (val / total_enrolments) * 100
    ax5.text(bar.get_x() + bar.get_width()/2, val + val*0.02, 
            f'{pct:.1f}%', ha='center', va='bottom', color=text_color, fontsize=9)

# 6. Volatility Comparison
ax6 = plt.subplot(3, 2, 6)
ax6.set_facecolor(bg_color)
volatility_labels = ['Daily CV', 'Monthly CV', 'Growth Volatility']
volatility_values = [daily_cv, monthly_cv, growth_volatility]
bars = ax6.bar(volatility_labels, volatility_values, 
              color=[zerve_colors[1], zerve_colors[1], zerve_colors[1]], alpha=0.85)
ax6.set_title('Volatility Measures', 
              fontsize=14, fontweight='bold', color=text_color, pad=15)
ax6.set_ylabel('Coefficient (%)', fontsize=11, color=text_color)
ax6.tick_params(colors=text_color, labelsize=9)
ax6.grid(False)
# Add value labels
for bar, val in zip(bars, volatility_values):
    ax6.text(bar.get_x() + bar.get_width()/2, val + val*0.02, 
            f'{val:.1f}%', ha='center', va='bottom', color=text_color, fontsize=9)

plt.tight_layout()
print("Volume metrics visualization complete")
