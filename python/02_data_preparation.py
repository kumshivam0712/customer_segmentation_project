# 02_data_preparation.py
# ============================================
# STEP 2: PREPARE AND CLEAN THE DATA
# ============================================

import pandas as pd
import numpy as np
import os
from datetime import datetime

print("=" * 60)
print("CUSTOMER SEGMENTATION PROJECT - STEP 2: DATA PREPARATION")
print("=" * 60)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_dir = os.path.join(project_dir, 'data')

print(f"\n📂 Loading datasets from: {data_dir}")

# Check if data directory exists
if not os.path.exists(data_dir):
    print(f"❌ ERROR: Data folder not found at {data_dir}")
    print("Please make sure you have:")
    print("1. Created a 'data' folder in your project directory")
    print("2. Downloaded and extracted the dataset into the data folder")
    exit(1)

# Load all necessary datasets
print("\n1️⃣ Loading customers dataset...")
customers_file = os.path.join(data_dir, 'olist_customers_dataset.csv')
if not os.path.exists(customers_file):
    print(f"❌ ERROR: Cannot find {customers_file}")
    exit(1)
customers = pd.read_csv(customers_file)
print(f"   ✅ Loaded {len(customers):,} customer records")

print("\n2️⃣ Loading orders dataset...")
orders_file = os.path.join(data_dir, 'olist_orders_dataset.csv')
if not os.path.exists(orders_file):
    print(f"❌ ERROR: Cannot find {orders_file}")
    exit(1)
orders = pd.read_csv(orders_file)
print(f"   ✅ Loaded {len(orders):,} order records")

print("\n3️⃣ Loading order items dataset...")
items_file = os.path.join(data_dir, 'olist_order_items_dataset.csv')
if not os.path.exists(items_file):
    print(f"❌ ERROR: Cannot find {items_file}")
    exit(1)
items = pd.read_csv(items_file)
print(f"   ✅ Loaded {len(items):,} order item records")

print("\n4️⃣ Loading payments dataset...")
payments_file = os.path.join(data_dir, 'olist_order_payments_dataset.csv')
if not os.path.exists(payments_file):
    print(f"❌ ERROR: Cannot find {payments_file}")
    exit(1)
payments = pd.read_csv(payments_file)
print(f"   ✅ Loaded {len(payments):,} payment records")

# Convert date columns to datetime
print("\n📅 Converting date columns...")
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
print("   ✅ Dates converted")

# Filter for delivered orders only
print("\n🔍 Filtering for delivered orders...")
initial_order_count = len(orders)
delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
delivered_count = len(delivered_orders)
print(f"   ✅ {delivered_count:,} delivered orders out of {initial_order_count:,} total ({delivered_count/initial_order_count*100:.1f}%)")

# Merge datasets
print("\n🔄 Merging datasets...")

# Merge orders with items
print("   Merging orders with items...")
orders_items = pd.merge(delivered_orders, items, on='order_id', how='inner')
print(f"   → {len(orders_items):,} records")

# Merge with customers
print("   Adding customer information...")
complete_data = pd.merge(orders_items, customers, on='customer_id', how='inner')
print(f"   → {len(complete_data):,} records")

# Merge with payments
print("   Adding payment information...")
complete_data = pd.merge(complete_data, payments, on='order_id', how='left')
print(f"   → {len(complete_data):,} records")

# Calculate basic metrics
print("\n📊 Calculating basic metrics...")
complete_data['total_order_value'] = complete_data['price'] + complete_data['freight_value']
complete_data['purchase_year'] = complete_data['order_purchase_timestamp'].dt.year
complete_data['purchase_month'] = complete_data['order_purchase_timestamp'].dt.month
complete_data['purchase_dayofweek'] = complete_data['order_purchase_timestamp'].dt.dayofweek

print("\n📈 Dataset Summary:")
print(f"   • Date range: {complete_data['order_purchase_timestamp'].min()} to {complete_data['order_purchase_timestamp'].max()}")
print(f"   • Total revenue: R${complete_data['price'].sum():,.2f}")
print(f"   • Average order value: R${complete_data.groupby('order_id')['price'].sum().mean():.2f}")
print(f"   • Unique customers: {complete_data['customer_unique_id'].nunique():,}")
print(f"   • Unique orders: {complete_data['order_id'].nunique():,}")

# Check for missing values
print("\n🔍 Checking for missing values...")
missing_values = complete_data.isnull().sum()
missing_cols = missing_values[missing_values > 0]
if len(missing_cols) > 0:
    print("   ⚠️ Missing values found:")
    for col, count in missing_cols.items():
        pct = (count / len(complete_data)) * 100
        print(f"      • {col}: {count:,} ({pct:.1f}%)")
else:
    print("   ✅ No missing values")

# Save prepared data
print("\n💾 Saving prepared dataset...")
output_file = os.path.join(data_dir, 'prepared_data.csv')
complete_data.to_csv(output_file, index=False)
print(f"   ✅ Saved to: {output_file}")
print(f"   📁 File size: {os.path.getsize(output_file) / 1024**2:.1f} MB")

# Create a summary file
summary = {
    'total_records': len(complete_data),
    'unique_customers': complete_data['customer_unique_id'].nunique(),
    'unique_orders': complete_data['order_id'].nunique(),
    'unique_products': complete_data['product_id'].nunique(),
    'unique_sellers': complete_data['seller_id'].nunique(),
    'total_revenue': complete_data['price'].sum(),
    'avg_order_value': complete_data.groupby('order_id')['price'].sum().mean(),
    'date_range_start': complete_data['order_purchase_timestamp'].min(),
    'date_range_end': complete_data['order_purchase_timestamp'].max()
}

summary_df = pd.DataFrame([summary])
summary_file = os.path.join(data_dir, 'data_summary.csv')
summary_df.to_csv(summary_file, index=False)
print(f"\n📊 Summary saved to: {summary_file}")

print("\n" + "=" * 60)
print("✅ DATA PREPARATION COMPLETE!")
print("=" * 60)
print("\nNext step: Run 03_customer_metrics.py")