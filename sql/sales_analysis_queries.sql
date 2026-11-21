-- 1. Overall KPIs
SELECT
    SUM(Revenue) AS total_revenue,
    SUM(Profit) AS total_profit,
    COUNT(DISTINCT Order_ID) AS total_orders,
    SUM(Quantity) AS units_sold,
    AVG(Revenue) AS average_order_revenue
FROM sales_clean;

-- 2. Monthly revenue and profit trend
SELECT
    YEAR(Order_Date) AS sales_year,
    MONTH(Order_Date) AS sales_month,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit
FROM sales_clean
GROUP BY YEAR(Order_Date), MONTH(Order_Date)
ORDER BY sales_year, sales_month;

-- 3. Revenue by region
SELECT Region, SUM(Revenue) AS revenue, SUM(Profit) AS profit
FROM sales_clean
GROUP BY Region
ORDER BY revenue DESC;

-- 4. Top 10 products by revenue
SELECT Product, Category, SUM(Revenue) AS revenue, SUM(Quantity) AS units
FROM sales_clean
GROUP BY Product, Category
ORDER BY revenue DESC
LIMIT 10;

-- 5. Sales representative performance
SELECT Sales_Rep, SUM(Revenue) AS revenue, SUM(Profit) AS profit,
       COUNT(DISTINCT Order_ID) AS orders
FROM sales_clean
GROUP BY Sales_Rep
ORDER BY revenue DESC;

-- 6. Category performance and profit margin
SELECT Category, SUM(Revenue) AS revenue, SUM(Profit) AS profit,
       SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin
FROM sales_clean
GROUP BY Category
ORDER BY revenue DESC;

-- 7. Discount impact
SELECT Discount, COUNT(*) AS order_lines, SUM(Revenue) AS revenue,
       SUM(Profit) AS profit
FROM sales_clean
GROUP BY Discount
ORDER BY Discount;

-- 8. Cities with highest revenue
SELECT City, Region, SUM(Revenue) AS revenue
FROM sales_clean
GROUP BY City, Region
ORDER BY revenue DESC
LIMIT 10;

-- 9. Monthly growth using window function (MySQL 8+)
WITH monthly AS (
    SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS year_month,
           SUM(Revenue) AS revenue
    FROM sales_clean
    GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
)
SELECT year_month, revenue,
       LAG(revenue) OVER (ORDER BY year_month) AS previous_month_revenue,
       (revenue - LAG(revenue) OVER (ORDER BY year_month))
       / NULLIF(LAG(revenue) OVER (ORDER BY year_month), 0) AS growth_rate
FROM monthly
ORDER BY year_month;

-- 10. Identify low-margin products
SELECT Product, Category, SUM(Revenue) AS revenue, SUM(Profit) AS profit,
       SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin
FROM sales_clean
GROUP BY Product, Category
HAVING profit_margin < 0.15
ORDER BY profit_margin;
