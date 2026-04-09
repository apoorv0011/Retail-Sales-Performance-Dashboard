import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


# ================= PAGE CONFIG =================

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

st.title("📊 Retail Sales Performance Analytics Dashboard")

st.markdown("Interactive business intelligence dashboard built using Python + Streamlit")


# ================= LOAD DATA =================

df = pd.read_csv("train.csv")

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

df['Month-Year'] = df['Order Date'].dt.to_period('M').astype(str)

df['Year'] = df['Order Date'].dt.year


# ================= KPI SECTION =================

st.subheader("📈 Key Business Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${round(df['Sales'].sum(),2)}")

col2.metric("Total Orders", df['Order ID'].nunique())

col3.metric("Total Customers", df['Customer ID'].nunique())

col4.metric("Avg Order Value", f"${round(df['Sales'].mean(),2)}")

st.markdown("---")


# ================= FILTER SECTION =================

st.subheader("🔍 Filter Data")

region_filter = st.selectbox(
    "Select Region",
    ["All"] + list(df['Region'].unique())
)

category_filter = st.selectbox(
    "Select Category",
    ["All"] + list(df['Category'].unique())
)

if region_filter != "All":
    df = df[df['Region'] == region_filter]

if category_filter != "All":
    df = df[df['Category'] == category_filter]

st.markdown("---")


# ================= MONTHLY SALES TREND =================

st.subheader("📅 Monthly Sales Trend")

monthly_sales = df.groupby('Month-Year')['Sales'].sum()

st.line_chart(monthly_sales)


# ================= YEARLY SALES TREND =================

st.subheader("📊 Yearly Sales Trend")

yearly_sales = df.groupby('Year')['Sales'].sum()

st.line_chart(yearly_sales)


# ================= CATEGORY DISTRIBUTION =================

st.subheader("📦 Category Contribution")

category_sales = df.groupby('Category')['Sales'].sum()

fig, ax = plt.subplots()

ax.pie(
    category_sales,
    labels=category_sales.index,
    autopct="%1.1f%%"
)

st.pyplot(fig)


# ================= REGION PERFORMANCE =================

st.subheader("🌍 Region-wise Performance")

region_sales = df.groupby("Region")["Sales"].sum()

st.bar_chart(region_sales)


# ================= TOP PRODUCTS =================

st.subheader("🏆 Top Performing Products")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_products)


# ================= TOP CITIES =================

st.subheader("🏙 Top Performing Cities")

top_cities = (
    df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_cities)


# ================= SQL ANALYTICS SECTION =================

st.subheader("🗄 SQL Query Analytics")

conn = sqlite3.connect("sales.db")

query = """
SELECT Category,
ROUND(SUM(Sales),2) as Total_Sales
FROM sales_data
GROUP BY Category
"""

sql_result = pd.read_sql_query(query, conn)

st.dataframe(sql_result)

conn.close()


# ================= DOWNLOAD REPORT =================

st.subheader("⬇ Download Analytics Report")

with open("sales_report.xlsx", "rb") as file:
    st.download_button(
        label="Download Excel Report",
        data=file,
        file_name="sales_report.xlsx"
    )


# ================= BUSINESS INSIGHTS =================

st.subheader("💡 Key Business Insights")

st.success("West region generates highest overall revenue")

st.info("Technology category contributes the largest share of total sales")

st.warning("Top 5 cities contribute disproportionately high revenue concentration")


# ================= RAW DATA VIEW =================

st.subheader("📄 Dataset Preview")

st.dataframe(df)