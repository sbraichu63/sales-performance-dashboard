# Power BI Dashboard Build Guide

## Data import
1. Open Power BI Desktop.
2. Get Data > Text/CSV > select `data/sales_clean.csv`.
3. Confirm data types: Order_Date = Date; Quantity = Whole number/Decimal; Unit_Price, Revenue, Cost, Profit = Decimal; Discount = Decimal.
4. Create a date table (Modeling > New table):

```DAX
DateTable =
ADDCOLUMNS(
    CALENDAR(MIN(sales_clean[Order_Date]), MAX(sales_clean[Order_Date])),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month", FORMAT([Date], "MMM"),
    "Year-Month", FORMAT([Date], "YYYY-MM")
)
```
5. Create relationship DateTable[Date] -> sales_clean[Order_Date] (one-to-many).
6. Sort DateTable[Month] by DateTable[Month Number].

## Measures (Modeling > New measure)
```DAX
Total Revenue = SUM(sales_clean[Revenue])
Total Profit = SUM(sales_clean[Profit])
Total Orders = DISTINCTCOUNT(sales_clean[Order_ID])
Units Sold = SUM(sales_clean[Quantity])
Profit Margin = DIVIDE([Total Profit], [Total Revenue], 0)
Average Order Revenue = DIVIDE([Total Revenue], [Total Orders], 0)
Revenue LY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DateTable[Date]))
Revenue YoY % = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0)
```

## Page 1 — Executive Overview
- KPI cards: Total Revenue, Total Profit, Total Orders, Units Sold, Profit Margin.
- Line chart: DateTable[Year-Month] on X axis; Total Revenue on Y.
- Clustered bar: Region on axis; Total Revenue and Total Profit as values.
- Donut: Category with Total Revenue.
- Slicers: Year, Region, Category.

## Page 2 — Product Analysis
- Bar chart: Product by Total Revenue (Top N = 10).
- Treemap: Category > Product by Total Revenue.
- Matrix: Category, Product, Revenue, Profit, Profit Margin.
- Slicer: Category.

## Page 3 — Regional Analysis
- Bar chart: Region by Revenue.
- Map (optional): City by Revenue if geocoding is reliable.
- Matrix: Region, City, Revenue, Profit, Orders.
- Slicers: Year, Region.

## Page 4 — Sales Rep Analysis
- Bar chart: Sales_Rep by Revenue (descending).
- Scatter chart: Revenue vs Profit by Sales_Rep.
- Table: Sales_Rep, Revenue, Profit, Orders, Profit Margin.
- Conditional formatting: Revenue and Profit.

## Formatting checklist
- Use a consistent theme and restrained palette.
- Format revenue/profit as currency.
- Profit Margin and YoY as percentages.
- Add clear page titles and descriptive chart titles.
- Add tooltips and cross-filtering.
- Keep slicers aligned and use consistent spacing.
- Verify that totals respond correctly to slicers.
