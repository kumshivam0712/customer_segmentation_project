# 04_rfm_segmentation.py
# ============================================
# STEP 4: RFM SEGMENTATION
# ============================================

import pandas as pd
import numpy as np
import os

print("=" * 60)
print("CUSTOMER SEGMENTATION PROJECT - STEP 4: RFM SEGMENTATION")
print("=" * 60)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_dir = os.path.join(project_dir, 'data')

# Load customer metrics
print(f"\n📂 Loading customer metrics...")
metrics_file = os.path.join(data_dir, 'customer_metrics.csv')

if not os.path.exists(metrics_file):
    print("❌ ERROR: customer_metrics.csv not found!")
    print("Please run 03_customer_metrics.py first")
    exit()

customers = pd.read_csv(metrics_file)
print(f"   ✅ Loaded {len(customers):,} customer records")

# Function to create RFM scores
print("\n📊 Creating RFM scores (1-5 scale)...")

def create_rfm_scores(df):
    """
    Create RFM scores for each customer
    """
    df_copy = df.copy()
    
    # Recency score: lower days = higher score
    # Use quantiles to create 5 groups
    try:
        df_copy['r_quartile'] = pd.qcut(df_copy['recency_days'], q=5, labels=False, duplicates='drop')
        # Reverse so that lower recency gets higher score
        df_copy['r_score'] = 5 - df_copy['r_quartile']
    except:
        # If quantiles fail, use manual bins
        bins = [0, 30, 60, 90, 180, df_copy['recency_days'].max()]
        df_copy['r_score'] = pd.cut(df_copy['recency_days'], bins=bins, labels=[5,4,3,2,1])
    
    # Frequency score: higher frequency = higher score
    try:
        df_copy['f_score'] = pd.qcut(df_copy['frequency'].rank(method='first'), q=5, labels=False, duplicates='drop') + 1
    except:
        # If quantiles fail, use manual bins
        bins = [0, 1, 2, 3, 5, df_copy['frequency'].max()]
        df_copy['f_score'] = pd.cut(df_copy['frequency'], bins=bins, labels=[1,2,3,4,5])
    
    # Monetary score: higher spend = higher score
    try:
        df_copy['m_score'] = pd.qcut(df_copy['monetary'].rank(method='first'), q=5, labels=False, duplicates='drop') + 1
    except:
        # If quantiles fail, use manual bins
        bins = [0, 100, 500, 1000, 2000, df_copy['monetary'].max()]
        df_copy['m_score'] = pd.cut(df_copy['monetary'], bins=bins, labels=[1,2,3,4,5])
    
    # Convert to integers
    df_copy['r_score'] = df_copy['r_score'].astype(int)
    df_copy['f_score'] = df_copy['f_score'].astype(int)
    df_copy['m_score'] = df_copy['m_score'].astype(int)
    
    # Calculate total RFM score
    df_copy['rfm_total'] = df_copy['r_score'] + df_copy['f_score'] + df_copy['m_score']
    
    return df_copy

# Apply RFM scoring
customers = create_rfm_scores(customers)

print("\n📈 RFM Score Distribution:")
print(f"   Recency scores (1-5):")
print(customers['r_score'].value_counts().sort_index().to_string())
print(f"\n   Frequency scores (1-5):")
print(customers['f_score'].value_counts().sort_index().to_string())
print(f"\n   Monetary scores (1-5):")
print(customers['m_score'].value_counts().sort_index().to_string())

# Define segment function
print("\n🏷️ Assigning customer segments...")

def assign_segment(row):
    """
    Assign customer segment based on RFM scores
    """
    r = row['r_score']
    f = row['f_score']
    m = row['m_score']
    
    # Champions: high on everything (bought recently, buy often, spend a lot)
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    
    # Loyal Customers: high frequency, good spenders
    elif f >= 4 and m >= 4:
        return 'Loyal Customers'
    
    # Potential Loyalists: recent buyers, average spend
    elif r >= 4 and m >= 3:
        return 'Potential Loyalists'
    
    # New Customers: recent buyers, low frequency
    elif r >= 4 and f <= 2:
        return 'New Customers'
    
    # Promising: recent buyers, average metrics
    elif r >= 4:
        return 'Promising'
    
    # Need Attention: average recency and frequency
    elif r == 3 and f >= 3 and m >= 3:
        return 'Need Attention'
    
    # At Risk - High Value: haven't bought recently, but used to be good
    elif r <= 2 and f >= 3 and m >= 4:
        return 'At Risk - High Value'
    
    # At Risk: haven't bought recently, average spend
    elif r <= 2 and m >= 2:
        return 'At Risk'
    
    # Hibernating: long time no buy, low spend
    elif r <= 2 and m <= 2:
        return 'Hibernating'
    
    # Lost: very long time no buy, very low spend
    elif r == 1 and m == 1:
        return 'Lost'
    
    # Everything else
    else:
        return 'Other'

# Apply segment assignment
customers['segment'] = customers.apply(assign_segment, axis=1)

# Show segment distribution
print("\n📊 SEGMENT DISTRIBUTION")
print("-" * 40)
segment_counts = customers['segment'].value_counts()
segment_percentages = (segment_counts / len(customers) * 100).round(1)

for segment in segment_counts.index:
    print(f"   {segment}:")
    print(f"      Count: {segment_counts[segment]:,}")
    print(f"      Percentage: {segment_percentages[segment]}%")

# Calculate segment metrics
print("\n💰 SEGMENT METRICS")
print("-" * 40)

segment_analysis = customers.groupby('segment').agg({
    'customer_id': 'count',
    'monetary': ['sum', 'mean', 'median'],
    'frequency': 'mean',
    'recency_days': 'mean',
    'avg_order_value': 'mean',
    'r_score': 'mean',
    'f_score': 'mean',
    'm_score': 'mean'
}).round(2)

segment_analysis.columns = ['customer_count', 'total_revenue', 'avg_spent', 'median_spent',
                           'avg_orders', 'avg_recency', 'avg_order_value',
                           'avg_r', 'avg_f', 'avg_m']

# Calculate percentage of total customers and revenue
segment_analysis['customer_pct'] = (segment_analysis['customer_count'] / len(customers) * 100).round(1)
segment_analysis['revenue_pct'] = (segment_analysis['total_revenue'] / segment_analysis['total_revenue'].sum() * 100).round(1)

# Sort by average spend
segment_analysis = segment_analysis.sort_values('avg_spent', ascending=False)

print("\nSegment Performance Summary:")
print(segment_analysis.to_string())

# Identify key insights
print("\n🔑 KEY INSIGHTS")
print("-" * 40)

# Top segments by revenue
top_revenue_segments = segment_analysis.nlargest(3, 'revenue_pct')
print(f"\nTop 3 segments by revenue:")
for segment in top_revenue_segments.index:
    print(f"   • {segment}: {top_revenue_segments.loc[segment, 'revenue_pct']}% of revenue, {top_revenue_segments.loc[segment, 'customer_pct']}% of customers")

# Segments needing attention
at_risk_segments = ['At Risk', 'At Risk - High Value', 'Hibernating', 'Lost']
at_risk_data = segment_analysis[segment_analysis.index.isin(at_risk_segments)]
if not at_risk_data.empty:
    print(f"\n⚠️ At-risk segments total:")
    print(f"   • Customers: {at_risk_data['customer_count'].sum():,} ({at_risk_data['customer_pct'].sum():.1f}%)")
    print(f"   • Revenue at risk: R${at_risk_data['total_revenue'].sum():,.2f} ({at_risk_data['revenue_pct'].sum():.1f}%)")

# Save segmented data
print("\n💾 Saving segmented customer data...")
segmented_file = os.path.join(data_dir, 'segmented_customers.csv')
customers.to_csv(segmented_file, index=False)
print(f"   ✅ Saved to: {segmented_file}")

# Save segment analysis
analysis_file = os.path.join(project_dir, 'reports', 'segment_analysis.csv')
segment_analysis.to_csv(analysis_file)
print(f"   ✅ Segment analysis saved to: {analysis_file}")

print("\n" + "=" * 60)
print("✅ RFM SEGMENTATION COMPLETE!")
print("=" * 60)
print("\nNext step: Run 05_visualizations.py")