import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

print("Generating datasets...")

# Sales data - main dataset
def generate_sales_data(n=5000):
    
    start = datetime(2022, 1, 1)
    dates = [start + timedelta(days=random.randint(0, 1095)) for _ in range(n)]
    
    categories = ['Technology', 'Furniture', 'Office Supplies']
    subcats = {
        'Technology': ['Phones', 'Computers', 'Accessories', 'Copiers'],
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Paper', 'Binders', 'Art', 'Storage', 'Labels']
    }
    
    regions = ['East', 'West', 'Central', 'South']
    segments = ['Consumer', 'Corporate', 'Home Office']
    
    data = []
    for i in range(n):
        cat = random.choice(categories)
        subcat = random.choice(subcats[cat])
        region = random.choice(regions)
        segment = random.choice(segments)
        
        # pricing logic based on category
        if cat == 'Technology':
            price = random.uniform(50, 2000)
        elif cat == 'Furniture':
            price = random.uniform(100, 1500)
        else:
            price = random.uniform(5, 300)
        
        qty = random.randint(1, 10)
        discount = random.choice([0, 0.1, 0.15, 0.2, 0.25])
        
        sales = price * qty * (1 - discount)
        profit = sales * random.uniform(0.05, 0.35)
        
        data.append({
            'Order_ID': f'ORD-{i+1000}',
            'Order_Date': dates[i],
            'Ship_Date': dates[i] + timedelta(days=random.randint(1, 7)),
            'Category': cat,
            'Sub_Category': subcat,
            'Product_Name': f'{subcat} {random.randint(100,999)}',
            'Sales': round(sales, 2),
            'Quantity': qty,
            'Discount': discount,
            'Profit': round(profit, 2),
            'Region': region,
            'Segment': segment,
            'Customer_ID': f'CUST-{random.randint(1000, 9999)}',
            'State': random.choice(['California', 'Texas', 'New York', 'Florida', 
                                   'Illinois', 'Pennsylvania', 'Ohio', 'Georgia'])
        })
    
    return pd.DataFrame(data)


# Operations/manufacturing data
def generate_operations_data(n=2000):
    
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
    
    data = []
    for date in dates:
        for shift in ['Morning', 'Evening', 'Night']:
            production = random.randint(800, 1200)
            defects = int(production * random.uniform(0.01, 0.05))
            downtime = random.randint(0, 120)  # minutes
            
            data.append({
                'Date': date,
                'Shift': shift,
                'Units_Produced': production,
                'Defects': defects,
                'Defect_Rate': round(defects/production, 4),
                'Downtime_Minutes': downtime,
                'Efficiency': round(random.uniform(0.75, 0.98), 3),
                'Energy_Used': random.randint(500, 800),
                'Labor_Hours': random.randint(150, 200)
            })
    
    return pd.DataFrame(data)


# Financial data
def generate_financial_data():
    
    months = pd.date_range('2022-01-01', '2024-12-31', freq='MS')
    
    data = []
    base_revenue = 500000
    
    for i, month in enumerate(months):
        # add growth trend and seasonality
        trend = base_revenue * (1 + 0.015 * i)
        seasonal = trend * (1 + 0.1 * np.sin(2 * np.pi * i / 12))
        revenue = seasonal + random.uniform(-20000, 30000)
        
        cogs = revenue * random.uniform(0.55, 0.65)
        opex = revenue * random.uniform(0.20, 0.30)
        profit = revenue - cogs - opex
        
        data.append({
            'Month': month,
            'Revenue': round(revenue, 2),
            'COGS': round(cogs, 2),
            'Operating_Expenses': round(opex, 2),
            'Gross_Profit': round(revenue - cogs, 2),
            'Net_Profit': round(profit, 2),
            'Budget_Revenue': round(revenue * random.uniform(0.9, 1.1), 2),
            'Cash_Flow': round(profit * random.uniform(0.8, 1.2), 2)
        })
    
    return pd.DataFrame(data)


# Customer analytics
def generate_customer_data(n=1500):
    
    data = []
    for i in range(n):
        signup_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460))
        purchases = random.randint(1, 50)
        avg_order = random.uniform(50, 500)
        lifetime_value = purchases * avg_order
        
        # churn logic
        days_since_last = random.randint(0, 365)
        churned = 1 if days_since_last > 180 else 0
        
        data.append({
            'Customer_ID': f'CUST-{i+1000}',
            'Signup_Date': signup_date,
            'Total_Purchases': purchases,
            'Avg_Order_Value': round(avg_order, 2),
            'Lifetime_Value': round(lifetime_value, 2),
            'Days_Since_Last_Purchase': days_since_last,
            'Churned': churned,
            'Satisfaction_Score': random.randint(1, 5),
            'Support_Tickets': random.randint(0, 10),
            'Segment': random.choice(['High Value', 'Medium Value', 'Low Value'])
        })
    
    return pd.DataFrame(data)


# Generate all datasets
print("Creating sales data...")
sales_df = generate_sales_data(5000)

print("Creating operations data...")
operations_df = generate_operations_data()

print("Creating financial data...")
financial_df = generate_financial_data()

print("Creating customer data...")
customer_df = generate_customer_data(1500)

# Save to CSV
sales_df.to_csv('superstore_sales.csv', index=False)
operations_df.to_csv('operations_data.csv', index=False)
financial_df.to_csv('financial_data.csv', index=False)
customer_df.to_csv('customer_data.csv', index=False)

print("\nDatasets created successfully!")
print(f"Sales records: {len(sales_df)}")
print(f"Operations records: {len(operations_df)}")
print(f"Financial records: {len(financial_df)}")
print(f"Customer records: {len(customer_df)}")
print("\nFiles saved in current directory.")