import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Load dataset
df = pd.read_csv("train.csv")

print("Dataset Loaded Successfully\n")

# Show dataset structure
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Create Month-Year column (FIXED for SQLite compatibility)
df['Month-Year'] = df['Order Date'].dt.to_period('M').astype(str)


# ================= BUSINESS KPI SUMMARY =================

total_sales = round(df['Sales'].sum(), 2)

print("\n===== BUSINESS KPI SUMMARY =====")

print("Total Sales:", total_sales)


# Sales by Region
region_sales = df.groupby('Region')['Sales'].sum().round(2)

print("\nSales by Region:")
print(region_sales)


# Sales by Category
category_sales = df.groupby('Category')['Sales'].sum().round(2)

print("\nSales by Category:")
print(category_sales)


# Top 5 Cities by Sales
top_cities = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Cities by Sales:")
print(top_cities)


# ================= MONTHLY SALES TREND CHART =================

monthly_sales = df.groupby('Month-Year')['Sales'].sum()

plt.figure(figsize=(12,6))
monthly_sales.plot(marker='o')

plt.title("Monthly Sales Trend")
plt.xlabel("Month-Year")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("monthly_sales_trend.png")

print("\nMonthly sales trend chart saved as monthly_sales_trend.png")


# ================= EXPORT EXCEL REPORT =================

summary_region = df.groupby('Region')['Sales'].sum().reset_index()
summary_category = df.groupby('Category')['Sales'].sum().reset_index()

with pd.ExcelWriter("sales_report.xlsx", engine="openpyxl") as writer:

    df.to_excel(writer, sheet_name="Raw Data", index=False)
    summary_region.to_excel(writer, sheet_name="Region Summary", index=False)
    summary_category.to_excel(writer, sheet_name="Category Summary", index=False)

print("\nExcel report saved as sales_report.xlsx")


# ================= DATABASE STORAGE (SQLITE) =================

conn = sqlite3.connect("sales.db")

df.to_sql("sales_data", conn, if_exists="replace", index=False)

print("\nDatabase saved as sales.db")


# SQL Query: Sales by Region

query_region = pd.read_sql_query(
    """
    SELECT Region, ROUND(SUM(Sales),2) AS Total_Sales
    FROM sales_data
    GROUP BY Region
    """,
    conn
)

print("\nSQL Query Result - Sales by Region:")
print(query_region)


# SQL Query: Top 5 Cities

query_cities = pd.read_sql_query(
    """
    SELECT City, ROUND(SUM(Sales),2) AS Total_Sales
    FROM sales_data
    GROUP BY City
    ORDER BY Total_Sales DESC
    LIMIT 5
    """,
    conn
)

print("\nSQL Query Result - Top 5 Cities:")
print(query_cities)


conn.close()