import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "sales_raw.csv"
CLEAN_PATH = ROOT / "data" / "sales_clean.csv"

df = pd.read_csv(RAW_PATH, parse_dates=["Order_Date"])
print("Raw shape:", df.shape)
print("Missing values:\n", df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())

# Remove exact duplicate records.
df = df.drop_duplicates()

# Remove duplicate order IDs, keeping the first record.
df = df.drop_duplicates(subset=["Order_ID"], keep="first")

# Standardize text fields.
for col in ["Region", "City", "Sales_Rep", "Category", "Product"]:
    df[col] = df[col].astype("string").str.strip()

# Fill categorical missing values with a transparent placeholder.
df["Region"] = df["Region"].fillna("Unknown")
df["City"] = df["City"].fillna("Unknown")
df["Sales_Rep"] = df["Sales_Rep"].fillna("Unassigned")

# Missing discounts are assumed to be zero; document this assumption.
df["Discount"] = df["Discount"].fillna(0)

# Validate numeric columns and remove impossible values.
numeric_cols = ["Quantity", "Unit_Price", "Discount", "Revenue", "Cost", "Profit"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Order_Date", "Quantity", "Unit_Price"])
df = df[(df["Quantity"] > 0) & (df["Unit_Price"] > 0)]
df["Discount"] = df["Discount"].clip(0, 0.80)

# Flag extreme quantity outliers using the IQR method; cap rather than delete.
q1 = df["Quantity"].quantile(0.25)
q3 = df["Quantity"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
df["Quantity_Outlier_Flag"] = df["Quantity"] > upper_bound
df["Quantity"] = df["Quantity"].clip(upper=upper_bound)

# Recalculate financial measures so they are internally consistent.
df["Revenue"] = df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"])
df["Profit"] = df["Revenue"] - df["Cost"]
df["Profit_Margin"] = np.where(df["Revenue"] != 0, df["Profit"] / df["Revenue"], 0)

# Create fields useful for Power BI.
df["Year"] = df["Order_Date"].dt.year
df["Month_Number"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
df["Year_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

df = df.sort_values("Order_Date")
df.to_csv(CLEAN_PATH, index=False)

print("Cleaned shape:", df.shape)
print("Cleaned file saved:", CLEAN_PATH)
print("Quantity outliers flagged:", int(df["Quantity_Outlier_Flag"].sum()))
