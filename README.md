# Sales Performance Dashboard

## Project Overview

An end-to-end sales analytics portfolio project built using Python. The project uses a sales dataset to demonstrate data cleaning, exploratory data analysis (EDA), and interactive dashboard development.

Python libraries are used to clean, analyse, and visualize sales data, while Streamlit provides an interactive dashboard for exploring business performance.

> **Note:** This project uses a dataset for portfolio and learning purposes. Its results should not be interpreted as actual company performance.

## Tech Stack

- **Python:** Core programming language
- **Pandas:** Data cleaning and manipulation
- **NumPy:** Numerical operations
- **Matplotlib:** Data visualization
- **Plotly:** Interactive charts
- **Streamlit:** Interactive dashboard
- **CSV:** Dataset storage

## Project Workflow

1. Load and inspect the raw sales dataset.
2. Identify and handle missing values, duplicate records, and data quality issues.
3. Clean and prepare the dataset using Pandas.
4. Export the cleaned dataset as a CSV file.
5. Perform exploratory data analysis to identify sales trends and patterns.
6. Generate visualizations and summary reports.
7. Build an interactive dashboard using Streamlit.

## Project Structure

```text
sales_performance_dashboard_project/
│
├── data/
│   └── sales_clean.csv
│
├── scripts/
│   ├── clean_sales_data.py
│   └── exploratory_analysis.py
│
├── outputs/
│   └── eda/
│
├── app.py
├── requirements.txt
└── README.md
```

## Dashboard Features

- **Executive Overview:** Revenue, profit, orders, and profit margin.
- **Sales Trends:** Monthly revenue and profit analysis.
- **Category Analysis:** Revenue comparison across product categories.
- **Regional Analysis:** Regional sales performance.
- **Product Analysis:** Top-performing products.
- **Sales Representative Analysis:** Performance comparison.
- **Interactive Filters:** Filter dashboard data by region and category.
- **Raw Data View:** Explore the filtered dataset.

## How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd sales_performance_dashboard_project
```

### 3. Create and activate a virtual environment (optional)

```bash
python -m venv Virtual
```

Windows PowerShell:

```powershell
.\Virtual\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## Learning Outcomes

Through this project, I practised:

- Data cleaning and preprocessing using Pandas.
- Handling missing values and duplicate records.
- Exploratory data analysis.
- Data visualization using Matplotlib and Plotly.
- Building interactive dashboards with Streamlit.
- Extracting useful insights from sales data.

## Future Improvements

- Add SQL-based business analysis.
- Build a Power BI dashboard.
- Add more advanced business insights.
- Deploy the dashboard online.

## Author

**Suryansh Barnawal**


