# Import libraries for data handling, randomization, and file management
import pandas as pd
import numpy as np               
from faker import Faker           
import random                     
from datetime import datetime, timedelta  
import os        

# Initialize Faker to simulate realistic data
fake = Faker()

# Set seed so results are reproducible(same dataset every run)
np.random.seed(42)
random.seed(42)

# Number of rows (transactions) to generate for dataset
N_ROWS = 10000 

# Product catalog simulates real grocery store inventory
# Each tuple has = (product_id, product_name, category, price)
product_catalog = [
    ("P001", "Milk", "Dairy", 3.99),
    ("P002", "Bread", "Bakery", 2.49),
    ("P003", "Eggs", "Dairy", 4.29),
    ("P004", "Bananas", "Produce", 1.29),
    ("P005", "Apples", "Produce", 2.99),
    ("P006", "Chips", "Snacks", 3.49),
    ("P007", "Soda", "Beverages", 1.99),
    ("P008", "Juice", "Beverages", 3.79),
    ("P009", "Ice Cream", "Frozen", 5.49),
    ("P010", "Detergent", "Household", 8.99),
    ("P011", "Soap", "Personal Care", 2.99),
    ("P012", "Yogurt", "Dairy", 1.49),
    ("P013", "Cookies", "Snacks", 3.99),
    ("P014", "Pizza", "Frozen", 6.99),
    ("P015", "Paper Towels", "Household", 7.49),
]

# Simulating different regions where stores operate
regions = ["Midwest", "South", "West", "Northeast"]

# Different payment methods customers can use
payment_methods = ["Credit Card", "Debit Card", "Cash", "Mobile Pay"]

# Store IDs to simulate multiple store locations
store_ids = ["S101", "S102", "S103", "S104", "S105"]

# 1000 unique customers
customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, 1001)]

# Define date range for transactions (1 year of data)
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

# Store all transaction rows
rows = []

# Loop to generate each transaction
for i in range(1, N_ROWS + 1):

    # Unique transaction ID
    transaction_id = f"T{str(i).zfill(6)}"

    # Randomly assign customer, store, and region
    customer_id = random.choice(customer_ids)
    store_id = random.choice(store_ids)
    region = random.choice(regions)

    # Pick random product from catalog
    product_id, product_name, product_category, unit_price = random.choice(product_catalog)

    # Quantity distribution (most people buy 1–2 items)
    quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.35, 0.30, 0.18, 0.10, 0.07])

    # Whether customer is part of loyalty program
    loyalty_member = random.choice(["Yes", "No"])

    # Payment method used
    payment_method = random.choice(payment_methods)

    # Generate random transaction date within range
    random_days = random.randint(0, (end_date - start_date).days)
    transaction_date = start_date + timedelta(days=random_days)

    # Calculate total amount = quantity * price
    total_amount = round(quantity * unit_price, 2)

    # Basket size is number of items in cart
    basket_size = random.randint(1, 8)

    # Append all values to rows list
    rows.append([
        transaction_id,
        customer_id,
        transaction_date,
        store_id,
        region,
        product_id,
        product_category,
        product_name,
        quantity,
        unit_price,
        total_amount,
        payment_method,
        loyalty_member,
        basket_size
    ])

# Convert list into pandas DataFrame
df = pd.DataFrame(rows, columns=[
    "transaction_id", "customer_id", "transaction_date", "store_id", "region",
    "product_id", "product_category", "product_name", "quantity", "unit_price",
    "total_amount", "payment_method", "loyalty_member", "basket_size"
])

# data quality issues
issue_indices = np.random.choice(df.index, size=50, replace=False)
# Negative quantity (invalid)
df.loc[issue_indices[:10], "quantity"] = -1
# Missing price (common real-world issue)
df.loc[issue_indices[10:20], "unit_price"] = np.nan
# Unknown category (data inconsistency)
df.loc[issue_indices[20:30], "product_category"] = "Unknown"
# Negative total amount (wrong calculation / bug)
df.loc[issue_indices[30:40], "total_amount"] = -5.00
# Missing customer ID (critical issue)
df.loc[issue_indices[40:50], "customer_id"] = None


# Save dataset to CSV format
df.to_csv("data/raw/retail_transactions.csv", index=False)

# First few rows of dataset
print(df.head())