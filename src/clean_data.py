# Import libraries
import pandas as pd
import os

# Loads the CSV into a pandas
df = pd.read_csv("data/raw/retail_transactions.csv")

# Dictionary to store data quality metrics
quality_report = {}

# Count total rows before cleaning
quality_report["total_rows_before"] = len(df)

# Count missing customer IDs
quality_report["missing_customer_id"] = df["customer_id"].isna().sum()

# Count missing unit prices
quality_report["missing_unit_price"] = df["unit_price"].isna().sum()

# Count negative quantities
quality_report["negative_quantity"] = (df["quantity"] < 0).sum()

# Count negative total amounts
quality_report["negative_total_amount"] = (df["total_amount"] < 0).sum()

# Count unknown categories
quality_report["unknown_category"] = (df["product_category"] == "Unknown").sum()

# Count duplicate rows
quality_report["duplicate_rows"] = df.duplicated().sum()

# Clean data
df_clean = df.copy()

# Drop rows with missing customer IDs and unit prices
df_clean = df_clean.dropna(subset=["customer_id", "unit_price"])

# Drop rows with negative quantities
df_clean = df_clean[df_clean["quantity"] > 0]

# Drop rows with negative total amounts
df_clean = df_clean[df_clean["total_amount"] > 0]

# Drop rows with unknown categories
df_clean = df_clean[df_clean["product_category"] != "Unknown"]

# Drop duplicate rows
df_clean = df_clean.drop_duplicates()

# Count total rows after cleaning
quality_report["total_rows_after"] = len(df_clean)

# Count rows removed
quality_report["rows_removed"] = quality_report["total_rows_before"] - quality_report["total_rows_after"]

os.makedirs("data/processed", exist_ok=True)
os.makedirs("outputs/tables", exist_ok=True)
# Save cleaned dataset to CSV format
df_clean.to_csv("data/processed/retail_transactions_clean.csv", index=False)

# Dataframe to store data quality metrics
report_df = pd.DataFrame(list(quality_report.items()), columns=["metric", "value"])

# Save data quality report to CSV format
report_df.to_csv("outputs/tables/data_quality_report.csv", index=False)
print(report_df)