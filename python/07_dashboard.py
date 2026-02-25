# 07_dashboard.py - Simple interactive dashboard
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
customers = pd.read_csv('../data/segmented_customers.csv')

print("=" * 50)
print("CUSTOMER SEGMENTATION DASHBOARD")
print("=" * 50)

while True:
    print("\n1. Show segment summary")
    print("2. Show top states")
    print("3. Show at-risk customers")
    print("4. Export segment details")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        summary = customers.groupby('segment').agg({
            'customer_id': 'count',
            'monetary': ['sum', 'mean']
        }).round(2)
        print("\n", summary)
        
    elif choice == '2':
        top_states = customers['state'].value_counts().head(10)
        print("\nTop 10 States:")
        for state, count in top_states.items():
            print(f"   {state}: {count:,} customers")
            
    elif choice == '3':
        at_risk = customers[customers['segment'].str.contains('At Risk|Hibernating', na=False)]
        print(f"\nAt-Risk Customers: {len(at_risk):,}")
        print(f"Revenue at Risk: R${at_risk['monetary'].sum():,.2f}")
        
    elif choice == '4':
        segment = input("Enter segment name: ")
        segment_data = customers[customers['segment'] == segment]
        filename = f"{segment.lower().replace(' ', '_')}_details.csv"
        segment_data.to_csv(filename, index=False)
        print(f"✅ Saved to {filename}")
        
    elif choice == '5':
        print("Goodbye!")
        break