# 03_customer_metrics.py
# ============================================
# STEP 3: CALCULATE CUSTOMER METRICS
# ============================================

import pandas as pd
import numpy as np
import os
from datetime import datetime

print("=" * 60)
print("CUSTOMER SEGMENTATION PROJECT - STEP 3: CUSTOMER METRICS")
print("=" * 60)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_dir = os.path.join(project_dir, 'data')

# Load prepared data
print(f"\n📂 Loading prepared data...")
data_file = os.path.join(data_dir, 'prepared_data.csv')

if not os.path.exists(data_file):
    print("❌ ERROR: prepared_data.csv not found!")
    print("Please run 02_data_preparation.py first")
    exit()

data = pd.read_csv(data_file)
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
print(f"   ✅ Loaded {len(data):,} records")

# Find the most recent date in the dataset
latest_date = data['order_purchase_timestamp'].max()
print(f"\n📅 Latest order date: {latest_date.date()}")

# Calculate customer metrics
print("\n📊 Calculating metrics for each customer...")

# Group by customer
customer_metrics = data.groupby('customer_unique_id').agg({
    # Recency: days since last purchase
    'order_purchase_timestamp': lambda x: (latest_date - x.max()).days,
    # Frequency: number of unique orders
    'order_id': 'nunique',
    # Monetary: total spent
    'price': 'sum',
    # Additional metrics
    'freight_value': 'sum',
    'customer_state': 'first',
    'customer_city': 'first'
}).reset_index()

# Rename columns
customer_metrics.columns = ['customer_id', 'recency_days', 'frequency', 
                            'monetary', 'total_freight', 'state', 'city']

print(f"   ✅ Calculated metrics for {len(customer_metrics):,} customers")

# Calculate additional metrics
print("\n📈 Calculating derived metrics...")

# Average order value
customer_metrics['avg_order_value'] = customer_metrics['monetary'] / customer_metrics['frequency']

# Customer lifetime (days between first and last purchase)
customer_lifetime = data.groupby('customer_unique_id')['order_purchase_timestamp'].agg(['min', 'max']).reset_index()
customer_lifetime['lifetime_days'] = (customer_lifetime['max'] - customer_lifetime['min']).dt.days
customer_metrics = pd.merge(customer_metrics, customer_lifetime[['customer_unique_id', 'lifetime_days']], 
                           left_on='customer_id', right_on='customer_unique_id', how='left')
customer_metrics.drop('customer_unique_id', axis=1, inplace=True)

# Flag for repeat customers
customer_metrics['is_repeat'] = (customer_metrics['frequency'] > 1).astype(int)

# Calculate average days between orders (for repeat customers)
def avg_days_between_orders(customer_id):
    customer_orders = data[data['customer_unique_id'] == customer_id]['order_purchase_timestamp'].sort_values()
    if len(customer_orders) > 1:
        return (customer_orders.iloc[-1] - customer_orders.iloc[0]).days / (len(customer_orders) - 1)
    return 0

# Apply to each customer (this may take a minute)
print("\n⏱️ Calculating average days between orders...")
customer_metrics['avg_days_between'] = customer_metrics['customer_id'].apply(avg_days_between_orders)

# Product diversity
product_diversity = data.groupby('customer_unique_id')['product_id'].nunique().reset_index()
product_diversity.columns = ['customer_id', 'unique_products']
customer_metrics = pd.merge(customer_metrics, product_diversity, on='customer_id', how='left')

print("\n📊 METRICS SUMMARY STATISTICS")
print("-" * 40)
metrics_to_show = ['recency_days', 'frequency', 'monetary', 'avg_order_value', 'lifetime_days']
for metric in metrics_to_show:
    print(f"\n{metric.upper()}:")
    print(f"   Min: {customer_metrics[metric].min():.0f}")
    print(f"   Average: {customer_metrics[metric].mean():.1f}")
    print(f"   Median: {customer_metrics[metric].median():.0f}")
    print(f"   Max: {customer_metrics[metric].max():.0f}")

# Show distribution of repeat vs one-time customers
repeat_count = customer_metrics['is_repeat'].sum()
one_time_count = len(customer_metrics) - repeat_count
print(f"\n🔄 Customer Types:")
print(f"   • One-time buyers: {one_time_count:,} ({one_time_count/len(customer_metrics)*100:.1f}%)")
print(f"   • Repeat buyers: {repeat_count:,} ({repeat_count/len(customer_metrics)*100:.1f}%)")

# Geographic distribution
print(f"\n🌎 Geographic Distribution:")
top_states = customer_metrics['state'].value_counts().head(5)
for state, count in top_states.items():
    pct = (count / len(customer_metrics)) * 100
    print(f"   • {state}: {count:,} customers ({pct:.1f}%)")

# Save metrics
print("\n💾 Saving customer metrics...")
metrics_file = os.path.join(data_dir, 'customer_metrics.csv')
customer_metrics.to_csv(metrics_file, index=False)
print(f"   ✅ Saved to: {metrics_file}")

# Create segment profiles for different groups
print("\n📋 Creating segment profiles...")

# Profile by frequency
freq_profiles = customer_metrics.groupby(pd.cut(customer_metrics['frequency'], 
                                                bins=[0, 1, 2, 3, 5, 10, 100])).agg({
    'customer_id': 'count',
    'monetary': ['mean', 'sum'],
    'recency_days': 'mean'
}).round(2)

print("\nProfiles by Order Frequency:")
print(freq_profiles)

# Profile by monetary value
value_bins = [0, 100, 500, 1000, 2000, 5000, 100000]
value_profiles = customer_metrics.groupby(pd.cut(customer_metrics['monetary'], bins=value_bins)).agg({
    'customer_id': 'count',
    'frequency': 'mean',
    'recency_days': 'mean'
}).round(2)

print("\nProfiles by Total Spend:")
print(value_profiles)

print("\n" + "=" * 60)
print("✅ CUSTOMER METRICS CALCULATED SUCCESSFULLY!")
print("=" * 60)
print("\nNext step: Run 04_rfm_segmentation.py")