# 01_data_exploration.py
# ============================================
# STEP 1: EXPLORE THE DATASET
# ============================================

import pandas as pd
import os
import sys

print("=" * 60)
print("CUSTOMER SEGMENTATION PROJECT - STEP 1: DATA EXPLORATION")
print("=" * 60)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_dir = os.path.join(project_dir, 'data')

print(f"\n📁 Project Directory: {project_dir}")
print(f"📁 Data Directory: {data_dir}")

# Check if data directory exists
if not os.path.exists(data_dir):
    print("\n❌ ERROR: Data folder not found!")
    print("Please make sure you have:")
    print("1. Created a 'data' folder in your project directory")
    print("2. Downloaded and extracted the dataset into the data folder")
    sys.exit(1)

# List all CSV files in data directory
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
print(f"\n📊 Found {len(csv_files)} CSV files:")

for i, file in enumerate(csv_files, 1):
    file_size = os.path.getsize(os.path.join(data_dir, file)) / 1024  # KB
    print(f"   {i}. {file} ({file_size:.1f} KB)")

# Function to explore each dataset
def explore_dataset(file_name):
    print(f"\n{'-' * 40}")
    print(f"📋 Exploring: {file_name}")
    print(f"{'-' * 40}")
    
    file_path = os.path.join(data_dir, file_name)
    
    try:
        # Load the data
        df = pd.read_csv(file_path)
        
        # Basic information
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        # Show column names
        print(f"\n   Columns:")
        for col in df.columns[:10]:  # Show first 10 columns
            print(f"      • {col}")
        if len(df.columns) > 10:
            print(f"      ... and {len(df.columns) - 10} more")
        
        # Show data types
        print(f"\n   Data Types:")
        for dtype in df.dtypes.value_counts().items():
            print(f"      • {dtype[0]}: {dtype[1]}")
        
        # Check for missing values
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        if len(missing_cols) > 0:
            print(f"\n   ⚠️ Missing Values Found:")
            for col, count in missing_cols.items():
                pct = (count / len(df)) * 100
                print(f"      • {col}: {count:,} ({pct:.1f}%)")
        else:
            print(f"\n   ✅ No missing values")
        
        # Show first few rows
        print(f"\n   First 3 rows:")
        print(df.head(3).to_string(index=False))
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading {file_name}: {str(e)}")
        return None

# Explore the most important datasets for customer segmentation
print("\n" + "=" * 60)
print("ANALYZING KEY DATASETS FOR CUSTOMER SEGMENTATION")
print("=" * 60)

# 1. Customers Dataset
customers_df = explore_dataset('olist_customers_dataset.csv')
if customers_df is not None:
    print(f"\n✅ Unique customers: {customers_df['customer_unique_id'].nunique():,}")
    print(f"✅ States covered: {customers_df['customer_state'].nunique()}")
    print(f"✅ Cities covered: {customers_df['customer_city'].nunique():,}")

# 2. Orders Dataset
orders_df = explore_dataset('olist_orders_dataset.csv')
if orders_df is not None:
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    print(f"\n✅ Date range: {orders_df['order_purchase_timestamp'].min()} to {orders_df['order_purchase_timestamp'].max()}")
    print(f"✅ Order statuses: {orders_df['order_status'].unique().tolist()}")

# 3. Order Items Dataset
items_df = explore_dataset('olist_order_items_dataset.csv')
if items_df is not None:
    print(f"\n✅ Average price: R${items_df['price'].mean():.2f}")
    print(f"✅ Total revenue: R${items_df['price'].sum():,.2f}")
    print(f"✅ Average freight: R${items_df['freight_value'].mean():.2f}")

# 4. Payments Dataset
payments_df = explore_dataset('olist_order_payments_dataset.csv')
if payments_df is not None:
    print(f"\n✅ Payment types: {payments_df['payment_type'].unique().tolist()}")
    print(f"✅ Average payment: R${payments_df['payment_value'].mean():.2f}")

print("\n" + "=" * 60)
print("✅ DATA EXPLORATION COMPLETE!")
print("=" * 60)
print("\nNext step: Run 02_data_preparation.py")