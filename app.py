
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_clean.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

# ==========================================
# 3. DASHBOARD TITLE
# ==========================================

st.title("📊 Sales Performance Dashboard")
st.markdown("### Business Sales Analysis & Performance Insights")

st.divider()

# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Dashboard Filters")

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

categories = ["All"] + sorted(
    df["Category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

# Filter dataset
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# ==========================================
# 5. KPI CALCULATIONS
# ==========================================

total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_units = filtered_df["Quantity"].sum()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

# ==========================================
# 6. KPI CARDS
# ==========================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

col2.metric(
    "Total Profit",
    f"{total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

# ==========================================
# 7. MONTHLY SALES TREND
# ==========================================

st.subheader("Monthly Sales Performance")

filtered_df["Year_Month"] = (
    filtered_df["Order_Date"].dt.to_period("M").astype(str)
)

monthly_sales = filtered_df.groupby(
    "Year_Month"
).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum")
).reset_index()

fig_monthly = px.line(
    monthly_sales,
    x="Year_Month",
    y=["Revenue", "Profit"],
    markers=True,
    title="Monthly Revenue and Profit Trend"
)

st.plotly_chart(
    fig_monthly,
    use_container_width="stretch"
)

# ==========================================
# 8. CATEGORY PERFORMANCE
# ==========================================

st.subheader("Category Performance")

category_sales = filtered_df.groupby(
    "Category"
)["Revenue"].sum().reset_index()

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Revenue",
    color="Category",
    title="Revenue by Category"
)

st.plotly_chart(
    fig_category,
    use_container_width="stretch"
)

# ==========================================
# 9. REGIONAL PERFORMANCE
# ==========================================

st.subheader("Regional Performance")

region_sales = filtered_df.groupby(
    "Region"
)["Revenue"].sum().reset_index()

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Revenue",
    color="Region",
    title="Revenue by Region"
)

st.plotly_chart(
    fig_region,
    use_container_width="stretch"
)

# ==========================================
# 10. TOP 10 PRODUCTS
# ==========================================

st.subheader("Top 10 Products")

top_products = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products.sort_values("Revenue"),
    x="Revenue",
    y="Product",
    orientation="h",
    title="Top 10 Products by Revenue"
)

st.plotly_chart(
    fig_products,
    use_container_width="stretch"
)

# ==========================================
# 11. SALES REPRESENTATIVE PERFORMANCE
# ==========================================

st.subheader("Sales Representative Performance")

rep_sales = filtered_df.groupby(
    "Sales_Rep"
)["Revenue"].sum().reset_index()

rep_sales = rep_sales.sort_values(
    "Revenue", ascending=False
).head(10)

fig_rep = px.bar(
    rep_sales,
    x="Sales_Rep",
    y="Revenue",
    title="Top 10 Sales Representatives"
)

st.plotly_chart(
    fig_rep,
    use_container_width="stretch"
)

# ==========================================
# 12. RAW DATA TABLE
# ==========================================

st.subheader("Sales Data")

st.dataframe(
    filtered_df,
    use_container_width="stretch"
)

# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.success("Sales Performance Dashboard loaded successfully!")
st.caption("Developed using Python, Pandas, Streamlit and Plotly.")
