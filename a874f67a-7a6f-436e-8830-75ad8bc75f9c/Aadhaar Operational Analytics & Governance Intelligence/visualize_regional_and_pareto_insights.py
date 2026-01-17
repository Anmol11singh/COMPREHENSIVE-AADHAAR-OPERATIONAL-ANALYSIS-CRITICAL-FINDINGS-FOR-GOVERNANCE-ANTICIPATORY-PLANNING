import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Zerve design system
bg_color = '#1D1D20'
text_color = '#fbfbff'
secondary_text = '#909094'
zerve_colors = ['#A1C9F4', '#FFB482', '#8DE5A1', '#FF9F9B', '#D0BBFF', '#1F77B4']
highlight_color = '#ffd400'
warning_color = '#f04438'

# === CHART 1: Top 10 States by Stress Score ===
fig1, ax1 = plt.subplots(figsize=(12, 7), facecolor=bg_color)
ax1.set_facecolor(bg_color)

top_stress_states = state_metrics.nlargest(10, 'stress_score').sort_values('stress_score')
bars1 = ax1.barh(range(len(top_stress_states)), top_stress_states['stress_score'], 
                 color=zerve_colors[3], edgecolor=text_color, linewidth=0.5)

ax1.set_yticks(range(len(top_stress_states)))
ax1.set_yticklabels(top_stress_states['state'], color=text_color, fontsize=10)
ax1.set_xlabel('Stress Score (Updates/Enrolment Ratio)', color=text_color, fontsize=11, fontweight='bold')
ax1.set_title('Top 10 States by Operational Stress Score', color=text_color, fontsize=14, fontweight='bold', pad=20)
ax1.tick_params(axis='x', colors=text_color)
ax1.tick_params(axis='y', colors=text_color)
ax1.spines['bottom'].set_color(secondary_text)
ax1.spines['left'].set_color(secondary_text)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for spine in ax1.spines.values():
    if spine.get_visible():
        spine.set_linewidth(0.5)

for _viz_i, (idx, row) in enumerate(top_stress_states.iterrows()):
    ax1.text(row['stress_score'] + 2, _viz_i, f"{row['stress_score']:.1f}", 
             va='center', color=text_color, fontsize=9)

plt.tight_layout()
plt.show()

# === CHART 2: Top 15 Districts by Total Updates ===
fig2, ax2 = plt.subplots(figsize=(12, 8), facecolor=bg_color)
ax2.set_facecolor(bg_color)

top_districts = district_metrics.nlargest(15, 'total_updates').sort_values('total_updates')
district_labels = [f"{row['district']}, {row['state']}" for _, row in top_districts.iterrows()]

bars2 = ax2.barh(range(len(top_districts)), top_districts['total_updates']/1000, 
                 color=zerve_colors[0], edgecolor=text_color, linewidth=0.5)

ax2.set_yticks(range(len(top_districts)))
ax2.set_yticklabels(district_labels, color=text_color, fontsize=9)
ax2.set_xlabel('Total Updates (thousands)', color=text_color, fontsize=11, fontweight='bold')
ax2.set_title('Top 15 Districts by Update Volume', color=text_color, fontsize=14, fontweight='bold', pad=20)
ax2.tick_params(axis='x', colors=text_color)
ax2.tick_params(axis='y', colors=text_color)
ax2.spines['bottom'].set_color(secondary_text)
ax2.spines['left'].set_color(secondary_text)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for spine in ax2.spines.values():
    if spine.get_visible():
        spine.set_linewidth(0.5)

for _viz_i2, val in enumerate(top_districts['total_updates']/1000):
    ax2.text(val + 10, _viz_i2, f"{val:.0f}K", va='center', color=text_color, fontsize=8)

plt.tight_layout()
plt.show()

# === CHART 3: Pareto Chart - State Contribution to Total Updates ===
fig3, ax3 = plt.subplots(figsize=(14, 7), facecolor=bg_color)
ax3.set_facecolor(bg_color)

pareto_states = state_pareto.head(20)
x_pos = range(len(pareto_states))

ax3.bar(x_pos, pareto_states['value_pct'], color=zerve_colors[1], 
        edgecolor=text_color, linewidth=0.5, alpha=0.8, label='Individual Contribution (%)')

ax3_twin = ax3.twinx()
ax3_twin.plot(x_pos, pareto_states['cumulative_pct'], color=highlight_color, 
              marker='o', linewidth=2.5, markersize=5, label='Cumulative %')
ax3_twin.axhline(y=80, color=warning_color, linestyle='--', linewidth=1.5, label='80% Threshold')

ax3.set_xticks(x_pos)
ax3.set_xticklabels(pareto_states['state'], rotation=45, ha='right', color=text_color, fontsize=9)
ax3.set_ylabel('Individual Contribution (%)', color=text_color, fontsize=11, fontweight='bold')
ax3.set_xlabel('State', color=text_color, fontsize=11, fontweight='bold')
ax3.set_title('Pareto Analysis: State Contribution to Total Updates (Top 20)', 
              color=text_color, fontsize=14, fontweight='bold', pad=20)
ax3.tick_params(axis='x', colors=text_color)
ax3.tick_params(axis='y', colors=text_color)

ax3_twin.set_ylabel('Cumulative Contribution (%)', color=text_color, fontsize=11, fontweight='bold')
ax3_twin.tick_params(axis='y', colors=text_color)
ax3_twin.set_ylim(0, 105)

ax3.spines['bottom'].set_color(secondary_text)
ax3.spines['left'].set_color(secondary_text)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3_twin.spines['bottom'].set_color(secondary_text)
ax3_twin.spines['right'].set_color(secondary_text)
ax3_twin.spines['top'].set_visible(False)
ax3_twin.spines['left'].set_visible(False)

for spine in ax3.spines.values():
    if spine.get_visible():
        spine.set_linewidth(0.5)
for spine in ax3_twin.spines.values():
    if spine.get_visible():
        spine.set_linewidth(0.5)

lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_twin.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left', 
           facecolor=bg_color, edgecolor=secondary_text, labelcolor=text_color, fontsize=9)

plt.tight_layout()
plt.show()

# === CHART 4: Monthly Update Fatigue Pattern ===
fig4, ax4 = plt.subplots(figsize=(12, 6), facecolor=bg_color)
ax4.set_facecolor(bg_color)

monthly_valid = monthly_demo[monthly_demo['Month_Year'] != 'NaT'].copy()
x_months = range(len(monthly_valid))

ax4.plot(x_months, monthly_valid['demo_pct_change'], color=zerve_colors[2], 
         marker='o', linewidth=2, markersize=6, label='Demographic Updates')

monthly_bio_valid = monthly_bio[monthly_bio['Month_Year'] != 'NaT'].copy()
ax4.plot(x_months, monthly_bio_valid['bio_pct_change'], color=zerve_colors[4], 
         marker='s', linewidth=2, markersize=6, label='Biometric Updates')

ax4.axhline(y=0, color=warning_color, linestyle='--', linewidth=1.5, alpha=0.7, label='Zero Growth')

ax4.set_xticks(x_months)
ax4.set_xticklabels(monthly_valid['Month_Year'], rotation=45, ha='right', color=text_color, fontsize=9)
ax4.set_ylabel('Monthly Growth Rate (%)', color=text_color, fontsize=11, fontweight='bold')
ax4.set_xlabel('Month', color=text_color, fontsize=11, fontweight='bold')
ax4.set_title('Update Fatigue Analysis: Monthly Growth Patterns', 
              color=text_color, fontsize=14, fontweight='bold', pad=20)
ax4.tick_params(axis='x', colors=text_color)
ax4.tick_params(axis='y', colors=text_color)
ax4.legend(facecolor=bg_color, edgecolor=secondary_text, labelcolor=text_color, fontsize=10)

ax4.spines['bottom'].set_color(secondary_text)
ax4.spines['left'].set_color(secondary_text)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

for spine in ax4.spines.values():
    if spine.get_visible():
        spine.set_linewidth(0.5)

plt.tight_layout()
plt.show()

# === CHART 5: State Rankings Comparison ===
fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(16, 7), facecolor=bg_color)
ax5a.set_facecolor(bg_color)
ax5b.set_facecolor(bg_color)

top10_enrol = state_metrics.nlargest(10, 'total_enrolments').sort_values('total_enrolments', ascending=True)
ax5a.barh(range(len(top10_enrol)), top10_enrol['total_enrolments']/1000, 
          color=zerve_colors[5], edgecolor=text_color, linewidth=0.5)
ax5a.set_yticks(range(len(top10_enrol)))
ax5a.set_yticklabels(top10_enrol['state'], color=text_color, fontsize=10)
ax5a.set_xlabel('Enrolments (thousands)', color=text_color, fontsize=11, fontweight='bold')
ax5a.set_title('Top 10 States by Enrolment Volume', color=text_color, fontsize=13, fontweight='bold', pad=15)
ax5a.tick_params(axis='both', colors=text_color)
ax5a.spines['bottom'].set_color(secondary_text)
ax5a.spines['left'].set_color(secondary_text)
ax5a.spines['top'].set_visible(False)
ax5a.spines['right'].set_visible(False)

top10_updates = state_metrics.nlargest(10, 'total_updates').sort_values('total_updates', ascending=True)
ax5b.barh(range(len(top10_updates)), top10_updates['total_updates']/1000000, 
          color=zerve_colors[1], edgecolor=text_color, linewidth=0.5)
ax5b.set_yticks(range(len(top10_updates)))
ax5b.set_yticklabels(top10_updates['state'], color=text_color, fontsize=10)
ax5b.set_xlabel('Updates (millions)', color=text_color, fontsize=11, fontweight='bold')
ax5b.set_title('Top 10 States by Update Volume', color=text_color, fontsize=13, fontweight='bold', pad=15)
ax5b.tick_params(axis='both', colors=text_color)
ax5b.spines['bottom'].set_color(secondary_text)
ax5b.spines['left'].set_color(secondary_text)
ax5b.spines['top'].set_visible(False)
ax5b.spines['right'].set_visible(False)

for ax in [ax5a, ax5b]:
    for spine in ax.spines.values():
        if spine.get_visible():
            spine.set_linewidth(0.5)

plt.tight_layout()
plt.show()

print("✓ Regional and Pareto visualizations created")
print("Charts: State stress scores, district volumes, Pareto analysis, update fatigue, state rankings")
