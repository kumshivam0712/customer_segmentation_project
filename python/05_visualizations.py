# 05_visualizations.py
# ============================================
# STEP 5: CREATE VISUALIZATIONS
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for better looking charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 60)
print("CUSTOMER SEGMENTATION PROJECT - STEP 5: VISUALIZATIONS")
print("=" * 60)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_dir = os.path.join(project_dir, 'data')
figures_dir = os.path.join(project_dir, 'figures')

# Create figures directory if it doesn't exist
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)
    print(f"\n📁 Created figures directory: {figures_dir}")

# Load segmented data
print(f"\n📂 Loading segmented customer data...")
segmented_file = os.path.join(data_dir, 'segmented_customers.csv')

if not os.path.exists(segmented_file):
    print("❌ ERROR: segmented_customers.csv not found!")
    print("Please run 04_rfm_segmentation.py first")
    exit()

customers = pd.read_csv(segmented_file)
print(f"   ✅ Loaded {len(customers):,} customer records")

# ============================================
# CHART 1: Segment Distribution (Pie Chart)
# ============================================
print("\n📊 Creating Chart 1: Segment Distribution Pie Chart...")

plt.figure(figsize=(12, 8))
segment_counts = customers['segment'].value_counts()

# Use a colormap for better visuals
colors = plt.cm.Set3(np.linspace(0, 1, len(segment_counts)))

# Create pie chart
plt.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%',
        colors=colors, startangle=90, explode=[0.05] * len(segment_counts))
plt.title('Customer Segment Distribution', fontsize=16, fontweight='bold', pad=20)

# Add a circle at the center to make it a donut chart (optional)
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.axis('equal')
plt.tight_layout()

# Save the chart
pie_chart_file = os.path.join(figures_dir, 'segment_distribution_pie.png')
plt.savefig(pie_chart_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {pie_chart_file}")

# ============================================
# CHART 2: Average Spend by Segment (Bar Chart)
# ============================================
print("📊 Creating Chart 2: Average Spend by Segment...")

plt.figure(figsize=(14, 7))
avg_spend = customers.groupby('segment')['monetary'].mean().sort_values()

# Create horizontal bar chart
colors = plt.cm.viridis(np.linspace(0, 0.9, len(avg_spend)))
bars = plt.barh(range(len(avg_spend)), avg_spend.values, color=colors)

# Customize the chart
plt.yticks(range(len(avg_spend)), avg_spend.index, fontsize=11)
plt.xlabel('Average Total Spent (R$)', fontsize=12)
plt.title('Average Customer Value by Segment', fontsize=16, fontweight='bold', pad=20)

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, avg_spend.values)):
    plt.text(val + 50, bar.get_y() + bar.get_height()/2, 
             f'R${val:,.0f}', va='center', fontsize=10)

# Add grid for better readability
plt.grid(axis='x', alpha=0.3)

plt.tight_layout()

# Save the chart
bar_chart_file = os.path.join(figures_dir, 'avg_spend_by_segment.png')
plt.savefig(bar_chart_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {bar_chart_file}")

# ============================================
# CHART 3: Revenue Contribution (Pie Chart)
# ============================================
print("📊 Creating Chart 3: Revenue Contribution...")

plt.figure(figsize=(12, 8))
revenue_by_segment = customers.groupby('segment')['monetary'].sum().sort_values()

# Calculate percentages
revenue_pct = (revenue_by_segment / revenue_by_segment.sum() * 100).round(1)

# Create explode effect for top segments
explode = [0.1 if i < 3 else 0 for i in range(len(revenue_by_segment))]

# Create pie chart
plt.pie(revenue_by_segment.values, labels=[f'{s}\n({p}%)' for s, p in zip(revenue_by_segment.index, revenue_pct)],
        autopct='', startangle=90, explode=explode, colors=plt.cm.tab20(np.linspace(0, 1, len(revenue_by_segment))))
plt.title('Revenue Contribution by Segment', fontsize=16, fontweight='bold', pad=20)

plt.axis('equal')
plt.tight_layout()

# Save the chart
revenue_pie_file = os.path.join(figures_dir, 'revenue_by_segment.png')
plt.savefig(revenue_pie_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {revenue_pie_file}")

# ============================================
# CHART 4: RFM Heatmap
# ============================================
print("📊 Creating Chart 4: RFM Heatmap...")

# Create pivot table
rfm_pivot = customers.pivot_table(
    values='monetary', 
    index='r_score', 
    columns='f_score', 
    aggfunc='mean',
    fill_value=0
)

plt.figure(figsize=(10, 8))

# Create heatmap
sns.heatmap(rfm_pivot, annot=True, fmt='.0f', cmap='YlOrRd',
            xticklabels=['1', '2', '3', '4', '5'],
            yticklabels=['5', '4', '3', '2', '1'],
            cbar_kws={'label': 'Average Spend (R$)'})

plt.xlabel('Frequency Score', fontsize=12)
plt.ylabel('Recency Score', fontsize=12)
plt.title('RFM Analysis: Average Spend by Recency and Frequency', 
          fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()

# Save the chart
heatmap_file = os.path.join(figures_dir, 'rfm_heatmap.png')
plt.savefig(heatmap_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {heatmap_file}")

# ============================================
# CHART 5: Geographic Distribution
# ============================================
print("📊 Creating Chart 5: Top States by Customer Count...")

plt.figure(figsize=(14, 7))
top_states = customers['state'].value_counts().head(10)

# Create color gradient
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(top_states)))

# Create bar chart
bars = plt.bar(range(len(top_states)), top_states.values, color=colors)

# Customize
plt.xticks(range(len(top_states)), top_states.index, fontsize=12)
plt.xlabel('State', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.title('Top 10 States by Customer Count', fontsize=16, fontweight='bold', pad=20)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, top_states.values)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
             f'{val:,}', ha='center', va='bottom', fontsize=10)

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Save the chart
geo_file = os.path.join(figures_dir, 'top_states.png')
plt.savefig(geo_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {geo_file}")

# ============================================
# CHART 6: Recency Distribution
# ============================================
print("📊 Creating Chart 6: Customer Recency Distribution...")

plt.figure(figsize=(14, 7))

# Create recency groups - FIXED: bins must be in increasing order
bins = [0, 30, 60, 90, 180, 365, 730, customers['recency_days'].max() + 1]
labels = ['<30 days', '30-60 days', '60-90 days', '90-180 days', 
          '180-365 days', '1-2 years', '>2 years']

# Make sure bins are strictly increasing
bins = sorted(bins)  # Just to be safe

customers['recency_group'] = pd.cut(customers['recency_days'], bins=bins, labels=labels, right=False)

recency_dist = customers['recency_group'].value_counts().sort_index()

# Create bar chart
colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(recency_dist)))
bars = plt.bar(range(len(recency_dist)), recency_dist.values, color=colors)

# Customize
plt.xticks(range(len(recency_dist)), recency_dist.index, rotation=45, fontsize=11)
plt.xlabel('Time Since Last Purchase', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.title('Customer Recency Distribution', fontsize=16, fontweight='bold', pad=20)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, recency_dist.values)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'{val:,}', ha='center', va='bottom', fontsize=10)

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Save the chart
recency_file = os.path.join(figures_dir, 'recency_distribution.png')
plt.savefig(recency_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {recency_file}")
# ============================================
# CHART 7: Segment Composition by State
# ============================================
print("📊 Creating Chart 7: Segment Composition by Top States...")

# Get top 5 states
top_5_states = customers['state'].value_counts().head(5).index

# Filter data for top states
state_segment_data = customers[customers['state'].isin(top_5_states)]

# Create cross-tabulation
segment_by_state = pd.crosstab(
    state_segment_data['state'], 
    state_segment_data['segment'],
    normalize='index'
) * 100

plt.figure(figsize=(14, 8))
segment_by_state.plot(kind='bar', stacked=True, colormap='tab20', ax=plt.gca())

plt.xlabel('State', fontsize=12)
plt.ylabel('Percentage of Customers', fontsize=12)
plt.title('Customer Segment Composition by State', fontsize=16, fontweight='bold', pad=20)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Save the chart
state_composition_file = os.path.join(figures_dir, 'state_composition.png')
plt.savefig(state_composition_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {state_composition_file}")

# ============================================
# CHART 8: Customer Value Distribution
# ============================================
print("📊 Creating Chart 8: Customer Value Distribution...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Histogram of customer spend
axes[0].hist(customers['monetary'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Total Spend (R$)', fontsize=12)
axes[0].set_ylabel('Number of Customers', fontsize=12)
axes[0].set_title('Distribution of Customer Spend', fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

# Box plot of spend by segment (top segments only)
top_segments = customers['segment'].value_counts().head(6).index
segment_spend_data = [customers[customers['segment'] == s]['monetary'] for s in top_segments]

bp = axes[1].boxplot(segment_spend_data, labels=top_segments, patch_artist=True)
for patch, color in zip(bp['boxes'], plt.cm.Set3(np.linspace(0, 1, len(top_segments)))):
    patch.set_facecolor(color)

axes[1].set_ylabel('Total Spend (R$)', fontsize=12)
axes[1].set_title('Spend Distribution by Segment', fontsize=14, fontweight='bold')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(alpha=0.3)

plt.tight_layout()

# Save the chart
value_dist_file = os.path.join(figures_dir, 'value_distribution.png')
plt.savefig(value_dist_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved to: {value_dist_file}")

print("\n" + "=" * 60)
print(f"✅ ALL VISUALIZATIONS COMPLETE!")
print(f"📁 Charts saved to: {figures_dir}")
print("=" * 60)
print("\nNext step: Run 06_final_report.py")