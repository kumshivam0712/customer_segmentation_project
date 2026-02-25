# 06_final_report.py
# ============================================
# STEP 6: GENERATE FINAL REPORT
# ============================================

import pandas as pd
import numpy as np
import os
from datetime import datetime

print("=" * 60)
print("CUSTOMER SEGMENTATION PROJECT - STEP 6: FINAL REPORT")
print("=" * 60)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_dir = os.path.join(project_dir, 'data')
reports_dir = os.path.join(project_dir, 'reports')
figures_dir = os.path.join(project_dir, 'figures')

# Create reports directory if it doesn't exist
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)
    print(f"\n📁 Created reports directory: {reports_dir}")

# Load data
print(f"\n📂 Loading customer segments...")
segmented_file = os.path.join(data_dir, 'segmented_customers.csv')

if not os.path.exists(segmented_file):
    print("❌ ERROR: segmented_customers.csv not found!")
    print("Please run 04_rfm_segmentation.py first")
    exit()

customers = pd.read_csv(segmented_file)
print(f"   ✅ Loaded {len(customers):,} customer records")

# ============================================
# SECTION 1: Executive Summary Calculations
# ============================================
print("\n📝 Generating Executive Summary...")

total_customers = len(customers)
total_revenue = customers['monetary'].sum()
avg_customer_value = customers['monetary'].mean()
repeat_rate = (customers['frequency'] > 1).mean() * 100

# Get segment summaries
segment_summary = customers.groupby('segment').agg({
    'customer_id': 'count',
    'monetary': ['sum', 'mean'],
    'frequency': 'mean',
    'recency_days': 'mean'
}).round(2)

segment_summary.columns = ['count', 'revenue', 'avg_spend', 'avg_orders', 'avg_recency']
segment_summary['pct_customers'] = (segment_summary['count'] / total_customers * 100).round(1)
segment_summary['pct_revenue'] = (segment_summary['revenue'] / total_revenue * 100).round(1)

# ============================================
# SECTION 2: Generate HTML Report
# ============================================
print("\n📄 Creating HTML report...")

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Customer Segmentation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .summary-box {{
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .metric {{
            display: inline-block;
            width: 200px;
            padding: 20px;
            margin: 10px;
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
        }}
        .metric-label {{
            font-size: 14px;
        }}
        .segment-card {{
            background-color: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #27ae60;
        }}
        .segment-name {{
            font-size: 18px;
            font-weight: bold;
            color: #27ae60;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Customer Segmentation Analysis Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary-box">
            <h2>Executive Summary</h2>
            <p>This report presents a comprehensive customer segmentation analysis based on RFM (Recency, Frequency, Monetary) metrics. The analysis covers <strong>{total_customers:,}</strong> customers with total revenue of <strong>R${total_revenue:,.2f}</strong>.</p>
        </div>
        
        <h2>📈 Key Metrics</h2>
        <div style="text-align: center;">
            <div class="metric">
                <div class="metric-value">{total_customers:,}</div>
                <div class="metric-label">Total Customers</div>
            </div>
            <div class="metric">
                <div class="metric-value">R${total_revenue:,.0f}</div>
                <div class="metric-label">Total Revenue</div>
            </div>
            <div class="metric">
                <div class="metric-value">R${avg_customer_value:,.0f}</div>
                <div class="metric-label">Avg Customer Value</div>
            </div>
            <div class="metric">
                <div class="metric-value">{repeat_rate:.1f}%</div>
                <div class="metric-label">Repeat Customer Rate</div>
            </div>
        </div>
        
        <h2>🎯 Segment Distribution</h2>
        <table>
            <tr>
                <th>Segment</th>
                <th>Customers</th>
                <th>% of Total</th>
                <th>Total Revenue</th>
                <th>% of Revenue</th>
                <th>Avg Spend</th>
                <th>Avg Orders</th>
            </tr>
"""

# Add rows for each segment
for segment in segment_summary.index:
    row = segment_summary.loc[segment]
    html_content += f"""
            <tr>
                <td><strong>{segment}</strong></td>
                <td>{row['count']:,.0f}</td>
                <td>{row['pct_customers']}%</td>
                <td>R${row['revenue']:,.2f}</td>
                <td>{row['pct_revenue']}%</td>
                <td>R${row['avg_spend']:,.2f}</td>
                <td>{row['avg_orders']:.1f}</td>
            </tr>
    """

html_content += """
        </table>
        
        <h2>📊 Visual Analysis</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <h3>Segment Distribution</h3>
                <img src="../figures/segment_distribution_pie.png" alt="Segment Distribution">
            </div>
            <div>
                <h3>Average Spend by Segment</h3>
                <img src="../figures/avg_spend_by_segment.png" alt="Average Spend">
            </div>
            <div>
                <h3>Revenue Contribution</h3>
                <img src="../figures/revenue_by_segment.png" alt="Revenue Contribution">
            </div>
            <div>
                <h3>RFM Heatmap</h3>
                <img src="../figures/rfm_heatmap.png" alt="RFM Heatmap">
            </div>
        </div>
        
        <h2>💡 Segment Descriptions & Recommendations</h2>
"""

# Segment descriptions and recommendations
segment_info = {
    'Champions': {
        'desc': 'Your best customers who buy frequently, spend the most, and purchased recently.',
        'rec': 'VIP treatment, exclusive offers, early access to new products, referral programs.'
    },
    'Loyal Customers': {
        'desc': 'Regular customers with high frequency and good spending habits.',
        'rec': 'Loyalty programs, cross-selling, personalized recommendations.'
    },
    'Potential Loyalists': {
        'desc': 'Recent customers with good spending who show promise.',
        'rec': 'Engagement emails, second purchase incentives, product recommendations.'
    },
    'New Customers': {
        'desc': 'First-time or very recent buyers with low frequency.',
        'rec': 'Welcome series, educational content, easy reorder options.'
    },
    'Promising': {
        'desc': 'Recent buyers with average metrics who could become loyal.',
        'rec': 'Nurture campaigns, targeted offers based on first purchase.'
    },
    'Need Attention': {
        'desc': 'Average customers who need a little push to become better.',
        'rec': 'Re-engagement emails, special discounts, feedback requests.'
    },
    'At Risk - High Value': {
        'desc': 'Previously high-value customers who haven\'t bought recently.',
        'rec': 'Urgent reactivation campaigns, special "we miss you" offers.'
    },
    'At Risk': {
        'desc': 'Customers showing signs of disengagement.',
        'rec': 'Win-back campaigns, satisfaction surveys, limited-time offers.'
    },
    'Hibernating': {
        'desc': 'Long-time no purchase, low engagement.',
        'rec': 'Last-chance reactivation, big discount offers.'
    },
    'Lost': {
        'desc': 'Very long time since last purchase, minimal spending.',
        'rec': 'Consider removing from active marketing, focus elsewhere.'
    },
    'Other': {
        'desc': 'Customers who don\'t fit neatly into other categories.',
        'rec': 'Monitor behavior, analyze for patterns.'
    }
}

for segment, info in segment_info.items():
    if segment in segment_summary.index:
        html_content += f"""
        <div class="segment-card">
            <div class="segment-name">{segment}</div>
            <p><strong>Description:</strong> {info['desc']}</p>
            <p><strong>Recommendation:</strong> {info['rec']}</p>
        </div>
        """

# Geographic Insights
html_content += """
        <h2>📍 Geographic Insights</h2>
"""

# Add geographic insights
top_states = customers['state'].value_counts().head(5)
html_content += "<table><tr><th>State</th><th>Customers</th><th>%</th><th>Top Segment</th></tr>"
for state, count in top_states.items():
    pct = round((count / total_customers * 100), 1)  # FIXED: using round() function
    top_segment = customers[customers['state'] == state]['segment'].mode()[0]
    html_content += f"<tr><td>{state}</td><td>{count:,}</td><td>{pct}%</td><td>{top_segment}</td></tr>"
html_content += "</table>"

# Action Plan
html_content += """
        <h2>📋 Action Plan</h2>
        <table>
            <tr>
                <th>Priority</th>
                <th>Action</th>
                <th>Target Segment</th>
                <th>Expected Impact</th>
            </tr>
            <tr>
                <td>High</td>
                <td>Launch VIP program with exclusive perks</td>
                <td>Champions</td>
                <td>Increase retention, get referrals</td>
            </tr>
            <tr>
                <td>High</td>
                <td>Urgent reactivation campaign</td>
                <td>At Risk - High Value</td>
                <td>Recover 20% of at-risk revenue</td>
            </tr>
            <tr>
                <td>Medium</td>
                <td>Welcome series optimization</td>
                <td>New Customers</td>
                <td>Improve second purchase rate</td>
            </tr>
            <tr>
                <td>Medium</td>
                <td>Loyalty program enhancements</td>
                <td>Loyal Customers</td>
                <td>Increase order frequency</td>
            </tr>
            <tr>
                <td>Low</td>
                <td>Last-chance win-back campaign</td>
                <td>Hibernating/Lost</td>
                <td>Recover some lost customers</td>
            </tr>
        </table>
        
        <h2>📊 Success Metrics to Track</h2>
        <ul>
            <li><strong>Segment Migration:</strong> Track how customers move between segments over time</li>
            <li><strong>Reactivation Rate:</strong> % of at-risk customers who return to purchase</li>
            <li><strong>Average Order Value by Segment:</strong> Monitor changes in spending patterns</li>
            <li><strong>Customer Lifetime Value:</strong> Calculate CLV for each segment</li>
            <li><strong>Retention Rate:</strong> % of customers who continue purchasing</li>
        </ul>
        
        <div class="footer">
            <p>This report was automatically generated as part of the Customer Segmentation Project.</p>
            <p>Data source: Brazilian E-Commerce Public Dataset by Olist</p>
        </div>
    </div>
</body>
</html>
"""

# Save HTML report
html_file = os.path.join(reports_dir, 'customer_segmentation_report.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"   ✅ HTML report saved to: {html_file}")

# ============================================
# SECTION 3: Create CSV Summary Report
# ============================================
print("\n📊 Creating CSV summary report...")

# Create detailed segment summary
summary_data = []
for segment in segment_summary.index:
    segment_customers = customers[customers['segment'] == segment]
    
    # Calculate top state safely
    if not segment_customers.empty:
        top_state = segment_customers['state'].mode()[0] if len(segment_customers['state'].mode()) > 0 else 'N/A'
    else:
        top_state = 'N/A'
    
    summary_data.append({
        'Segment': segment,
        'Customer Count': int(segment_summary.loc[segment, 'count']),
        'Percentage of Customers': float(segment_summary.loc[segment, 'pct_customers']),
        'Total Revenue': float(segment_summary.loc[segment, 'revenue']),
        'Percentage of Revenue': float(segment_summary.loc[segment, 'pct_revenue']),
        'Average Spend': float(segment_summary.loc[segment, 'avg_spend']),
        'Average Orders': float(segment_summary.loc[segment, 'avg_orders']),
        'Average Recency (days)': float(segment_summary.loc[segment, 'avg_recency']),
        'Average RFM Score': float(segment_customers['rfm_total'].mean()) if not segment_customers.empty else 0,
        'Repeat Customer Rate': float((segment_customers['frequency'] > 1).mean() * 100) if not segment_customers.empty else 0,
        'Top State': top_state
    })

summary_df = pd.DataFrame(summary_data)
summary_df = summary_df.sort_values('Total Revenue', ascending=False)

csv_summary_file = os.path.join(reports_dir, 'segment_summary.csv')
summary_df.to_csv(csv_summary_file, index=False)
print(f"   ✅ CSV summary saved to: {csv_summary_file}")

# ============================================
# SECTION 4: Create Executive Summary TXT
# ============================================
print("\n📝 Creating executive summary text file...")

# Calculate at-risk totals
at_risk_customers = customers[customers['segment'].str.contains('At Risk|Hibernating|Lost', na=False)]
at_risk_count = len(at_risk_customers)
at_risk_revenue = at_risk_customers['monetary'].sum()

# Top states total
top_states_total = top_states.sum()
top_states_pct = round((top_states_total / total_customers * 100), 1)

txt_content = f"""
============================================
CUSTOMER SEGMENTATION ANALYSIS - EXECUTIVE SUMMARY
============================================

Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW
--------------------------------------------
Total Customers Analyzed: {total_customers:,}
Total Revenue: R${total_revenue:,.2f}
Average Customer Value: R${avg_customer_value:,.2f}
Repeat Customer Rate: {repeat_rate:.1f}%

KEY FINDINGS
--------------------------------------------
1. Top 3 Segments by Revenue:
"""

# Add top 3 segments
top_3 = summary_df.nlargest(3, 'Total Revenue')[['Segment', 'Total Revenue', 'Percentage of Revenue']]
for _, row in top_3.iterrows():
    txt_content += f"   • {row['Segment']}: R${row['Total Revenue']:,.2f} ({row['Percentage of Revenue']:.1f}%)\n"

txt_content += f"""
2. At-Risk Customers:
   • Total at-risk customers: {at_risk_count:,}
   • Revenue at risk: R${at_risk_revenue:,.2f}

3. Geographic Concentration:
   • Top state: {top_states.index[0]} ({top_states.values[0]:,} customers)
   • Top 5 states account for {top_states_pct}% of customers

RECOMMENDATIONS
--------------------------------------------
1. Immediate Actions (Next 30 days):
   - Launch VIP program for Champions
   - Reactivation campaign for At-Risk High Value
   - Optimize welcome series for New Customers

2. Short-term Initiatives (60-90 days):
   - Implement segment-based email marketing
   - Create loyalty program structure
   - A/B test offers for different segments

3. Long-term Strategy (6+ months):
   - Build predictive churn model
   - Implement personalized recommendations
   - Develop segment-based inventory planning

NEXT STEPS
--------------------------------------------
1. Review segment definitions with marketing team
2. Set up tracking for segment migration
3. Plan first reactivation campaign
4. Schedule monthly segment analysis review

============================================
Report generated automatically by Customer Segmentation Project
============================================
"""

txt_file = os.path.join(reports_dir, 'executive_summary.txt')
with open(txt_file, 'w') as f:
    f.write(txt_content)
print(f"   ✅ Executive summary saved to: {txt_file}")

print("\n" + "=" * 60)
print("✅ FINAL REPORT GENERATION COMPLETE!")
print("=" * 60)
print(f"\n📁 All reports saved to: {reports_dir}")
print("\nFiles created:")
print(f"   • {html_file}")
print(f"   • {csv_summary_file}")
print(f"   • {txt_file}")

# Check if figures exist
if os.path.exists(figures_dir):
    figure_count = len([f for f in os.listdir(figures_dir) if f.endswith('.png')])
    print(f"\n📊 {figure_count} visualizations in: {figures_dir}")
else:
    print(f"\n⚠️  No figures folder found at: {figures_dir}")

print("\n" + "=" * 60)
print("🎉 PROJECT COMPLETE! 🎉")
print("=" * 60)
print("\nTo view your results:")
print(f"   1. HTML Report: start {html_file}")
print(f"   2. Figures: explorer {figures_dir}")
print(f"   3. Summary: notepad {txt_file}")