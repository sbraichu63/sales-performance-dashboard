
# ============================================================
# SALES PERFORMANCE DASHBOARD
# Exploratory Data Analysis (EDA)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\n========== LOADING DATASET ==========")

df = pd.read_csv("data/sales_clean.csv")

# Convert date column
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"], errors="coerce"
)

# Create output directory
output_dir = Path("outputs/eda")
output_dir.mkdir(parents=True, exist_ok=True)

print("Dataset loaded successfully!")


# ============================================================
# 2. BASIC DATASET INFORMATION
# ============================================================

print("\n========== DATASET INFORMATION ==========")

print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe(include="all"))


# ============================================================
# 3. DATA QUALITY CHECKS
# ============================================================

print("\n========== DATA QUALITY CHECKS ==========")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

# Check invalid dates
print("\nInvalid Order Dates:")
print(df["Order_Date"].isnull().sum())


# ============================================================
# 4. SALES PERFORMANCE KPIs
# ============================================================

print("\n========== SALES PERFORMANCE KPIs ==========")

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Quantity"].sum()

profit_margin = (
    (total_profit / total_revenue) * 100
    if total_revenue != 0 else 0
)

average_order_value = (
    total_revenue / total_orders
    if total_orders != 0 else 0
)

average_profit_per_order = (
    total_profit / total_orders
    if total_orders != 0 else 0
)

average_selling_price = (
    total_revenue / total_units
    if total_units != 0 else 0
)

print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Units Sold: {total_units:,}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Average Order Value: {average_order_value:,.2f}")
print(f"Average Profit Per Order: {average_profit_per_order:,.2f}")
print(f"Average Revenue Per Unit: {average_selling_price:,.2f}")


# ============================================================
# 5. CATEGORY PERFORMANCE ANALYSIS
# ============================================================

print("\n========== CATEGORY PERFORMANCE ==========")

category_performance = df.groupby("Category").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum"),
    Total_Orders=("Order_ID", "nunique")
)

category_performance["Profit_Margin"] = np.where(
    category_performance["Total_Revenue"] != 0,
    category_performance["Total_Profit"]
    / category_performance["Total_Revenue"] * 100,
    0
)

category_performance = category_performance.sort_values(
    by="Total_Revenue", ascending=False
)

print(category_performance)


# ============================================================
# 6. REGIONAL PERFORMANCE ANALYSIS
# ============================================================

print("\n========== REGIONAL PERFORMANCE ==========")

region_performance = df.groupby("Region").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Orders=("Order_ID", "nunique"),
    Units_Sold=("Quantity", "sum")
)

region_performance["Profit_Margin"] = np.where(
    region_performance["Total_Revenue"] != 0,
    region_performance["Total_Profit"]
    / region_performance["Total_Revenue"] * 100,
    0
)

region_performance = region_performance.sort_values(
    by="Total_Revenue", ascending=False
)

print(region_performance)


# ============================================================
# 7. TOP 10 PRODUCTS
# ============================================================

print("\n========== TOP 10 PRODUCTS ==========")

top_products = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)


# ============================================================
# 8. BOTTOM 10 PRODUCTS
# ============================================================

print("\n========== BOTTOM 10 PRODUCTS ==========")

bottom_products = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=True)
    .head(10)
)

print(bottom_products)


# ============================================================
# 9. SALES REPRESENTATIVE ANALYSIS
# ============================================================

print("\n========== SALES REPRESENTATIVE PERFORMANCE ==========")

rep_performance = df.groupby("Sales_Rep").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Orders=("Order_ID", "nunique"),
    Units_Sold=("Quantity", "sum")
)

rep_performance = rep_performance.sort_values(
    by="Total_Revenue", ascending=False
)

print(rep_performance)


# ============================================================
# 10. MONTHLY SALES ANALYSIS
# ============================================================

print("\n========== MONTHLY SALES ANALYSIS ==========")

df["Year_Month"] = df["Order_Date"].dt.to_period("M")

monthly_performance = df.groupby("Year_Month").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order_ID", "nunique"),
    Units_Sold=("Quantity", "sum")
)

monthly_performance["Profit_Margin"] = np.where(
    monthly_performance["Revenue"] != 0,
    monthly_performance["Profit"]
    / monthly_performance["Revenue"] * 100,
    0
)

print(monthly_performance)


# ============================================================
# 11. QUARTERLY SALES ANALYSIS
# ============================================================

print("\n========== QUARTERLY SALES ANALYSIS ==========")

df["Quarter"] = df["Order_Date"].dt.to_period("Q")

quarterly_sales = df.groupby("Quarter").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order_ID", "nunique")
)

print(quarterly_sales)


# ============================================================
# 12. PROFITABILITY ANALYSIS
# ============================================================

print("\n========== PROFITABILITY ANALYSIS ==========")

profitable_orders = (df["Profit"] > 0).sum()
loss_orders = (df["Profit"] < 0).sum()
zero_profit_records = (df["Profit"] == 0).sum()

print("Profitable Records:", profitable_orders)
print("Loss-Making Records:", loss_orders)
print("Zero-Profit Records:", zero_profit_records)


# ============================================================
# 13. SAVE ANALYSIS RESULTS
# ============================================================

print("\n========== SAVING ANALYSIS RESULTS ==========")

category_performance.to_csv(
    output_dir / "category_performance.csv"
)

region_performance.to_csv(
    output_dir / "region_performance.csv"
)

top_products.to_csv(
    output_dir / "top_products.csv"
)

bottom_products.to_csv(
    output_dir / "bottom_products.csv"
)

rep_performance.to_csv(
    output_dir / "sales_rep_performance.csv"
)

monthly_performance.to_csv(
    output_dir / "monthly_performance.csv"
)

quarterly_sales.to_csv(
    output_dir / "quarterly_performance.csv"
)

print("Analysis results saved successfully!")


# ============================================================
# 14. DATA VISUALIZATION
# ============================================================

print("\n========== CREATING VISUALIZATIONS ==========")


# 14.1 MONTHLY REVENUE TREND

plt.figure(figsize=(12, 6))

monthly_performance["Revenue"].plot(
    kind="line",
    marker="o",
    linewidth=2
)

plt.title("Monthly Revenue Trend", fontsize=15)
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    output_dir / "monthly_revenue.png",
    dpi=300
)

plt.show()


# 14.2 MONTHLY PROFIT TREND

plt.figure(figsize=(12, 6))

monthly_performance["Profit"].plot(
    kind="line",
    marker="o",
    linewidth=2
)

plt.title("Monthly Profit Trend", fontsize=15)
plt.xlabel("Month")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    output_dir / "monthly_profit.png",
    dpi=300
)

plt.show()


# 14.3 REGIONAL REVENUE

plt.figure(figsize=(9, 5))

region_performance["Total_Revenue"].plot(
    kind="bar"
)

plt.title("Revenue by Region", fontsize=15)
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    output_dir / "regional_revenue.png",
    dpi=300
)

plt.show()


# 14.4 CATEGORY REVENUE

plt.figure(figsize=(9, 5))

category_performance["Total_Revenue"].plot(
    kind="bar"
)

plt.title("Revenue by Category", fontsize=15)
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    output_dir / "category_revenue.png",
    dpi=300
)

plt.show()


# 14.5 TOP 10 PRODUCTS

plt.figure(figsize=(10, 6))

top_products.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Products by Revenue", fontsize=15)
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig(
    output_dir / "top_products.png",
    dpi=300
)

plt.show()


# 14.6 SALES REPRESENTATIVE PERFORMANCE

top_reps = rep_performance.head(10)

plt.figure(figsize=(10, 6))

top_reps["Total_Revenue"].sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Sales Representatives", fontsize=15)
plt.xlabel("Revenue")
plt.ylabel("Sales Representative")
plt.tight_layout()

plt.savefig(
    output_dir / "sales_representatives.png",
    dpi=300
)

plt.show()


# 14.7 CATEGORY PROFIT COMPARISON

plt.figure(figsize=(9, 5))

category_performance[
    ["Total_Revenue", "Total_Profit"]
].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Category Revenue vs Profit", fontsize=15)
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    output_dir / "category_profit_comparison.png",
    dpi=300
)

plt.show()


# ============================================================
# 15. FINAL SUMMARY
# ============================================================

print("\n========== FINAL BUSINESS SUMMARY ==========")

print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Profit Margin: {profit_margin:.2f}%")

if not category_performance.empty:
    best_category = category_performance["Total_Revenue"].idxmax()
    print("Best Revenue Category:", best_category)

if not region_performance.empty:
    best_region = region_performance["Total_Revenue"].idxmax()
    print("Best Revenue Region:", best_region)

if not top_products.empty:
    best_product = top_products.index[0]
    print("Top Revenue Product:", best_product)

print("\n========== EDA COMPLETED SUCCESSFULLY ==========")
