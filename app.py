import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Retail Sales Intelligence Platform",
    page_icon="📊",
    layout="wide"
)


# ================= GLOBAL CSS =================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1rem;
}

[data-testid="metric-container"] {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.06);
}

h1 {
    font-weight: 800;
}

h2 {
    font-weight: 700;
}

h3 {
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ================= HEADER =================

st.title("📊 Business Intelligence Analytics Platform")

st.caption(
    "Executive-level analytics dashboard powered by Python, SQL, and Machine Learning"
)

st.divider()


# ================= LOAD DATA =================

df = pd.read_csv("train.csv")

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

df['Month-Year'] = df['Order Date'].dt.to_period('M').astype(str)

df['Year'] = df['Order Date'].dt.year

df["Profit"] = df["Sales"] * 0.18


# ================= SIDEBAR =================

st.sidebar.title("⚙ Dashboard Controls")

st.sidebar.markdown("Filter analytics dynamically")

region = st.sidebar.multiselect(
    "Region",
    df['Region'].unique(),
    default=df['Region'].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df['Category'].unique(),
    default=df['Category'].unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df['Order Date'].min(), df['Order Date'].max()]
)


df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['Order Date'] >= pd.to_datetime(date_range[0])) &
    (df['Order Date'] <= pd.to_datetime(date_range[1]))
]


# ================= KPI SECTION =================

st.subheader("📈 Performance Overview")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Revenue", f"${round(df['Sales'].sum(),2):,}")
k2.metric("Profit", f"${round(df['Profit'].sum(),2):,}")
k3.metric("Orders", df['Order ID'].nunique())
k4.metric("Customers", df['Customer ID'].nunique())
k5.metric("Avg Order", f"${round(df['Sales'].mean(),2)}")


st.divider()


# ================= TREND SECTION =================

c1, c2 = st.columns(2)

with c1:

    st.subheader("📅 Monthly Revenue Trend")

    monthly_sales = df.groupby("Month-Year")["Sales"].sum()

    st.line_chart(monthly_sales)


with c2:

    st.subheader("📊 Yearly Revenue Trend")

    yearly_sales = df.groupby("Year")["Sales"].sum()

    st.line_chart(yearly_sales)


st.divider()


# ================= CATEGORY + REGION =================

c1, c2 = st.columns(2)

with c1:

    st.subheader("📦 Category Contribution")

    category_sales = df.groupby("Category")["Sales"].sum()

    fig, ax = plt.subplots()

    ax.pie(
        category_sales,
        labels=category_sales.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)


with c2:

    st.subheader("🌍 Region Performance")

    region_sales = df.groupby("Region")["Sales"].sum()

    st.bar_chart(region_sales)


st.divider()


# ================= SEGMENT ANALYSIS =================

st.subheader("👥 Customer Segmentation")

segment_sales = df.groupby("Segment")["Sales"].sum()

st.bar_chart(segment_sales)


st.divider()


# ================= PROFIT DISTRIBUTION =================

st.subheader("💰 Profit by Region")

profit_region = df.groupby("Region")["Profit"].sum()

st.bar_chart(profit_region)


st.divider()


# ================= TOP PRODUCTS =================

st.subheader("🏆 Top Performing Products")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)


st.divider()


# ================= CORRELATION =================

st.subheader("🔥 Feature Correlation Matrix")

numeric_df = df.select_dtypes(include=np.number).dropna(axis=1, how="all")

if len(numeric_df.columns) > 1:

    fig, ax = plt.subplots(figsize=(6,4))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm"
    )

    st.pyplot(fig)


st.divider()


# ================= SQL ANALYTICS =================

st.subheader("🗄 SQL Analytics Snapshot")

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


st.divider()


# ================= FORECAST SECTION =================

st.subheader("🤖 Sales Forecast Engine")

forecast_df = df.groupby("Year")["Sales"].sum().reset_index()

X = forecast_df["Year"].values.reshape(-1,1)

y = forecast_df["Sales"].values

model = LinearRegression()

model.fit(X,y)

future_year = np.array([[forecast_df["Year"].max()+1]])

prediction = model.predict(future_year)

st.success(
    f"Projected revenue for {future_year[0][0]} ≈ ${round(prediction[0],2):,}"
)


prediction_existing = model.predict(X)

score = r2_score(y, prediction_existing)

st.metric("Forecast Confidence (R²)", round(score,3))


growth = st.slider("Scenario Simulation (%)", 0, 50, 10)

future_sales = prediction[0] * (1 + growth/100)

st.info(
    f"Simulated future revenue after {growth}% growth ≈ ${round(future_sales,2):,}"
)


st.divider()


# ================= EXECUTIVE INSIGHTS =================

st.subheader("📌 Executive Insights")

top_region = df.groupby("Region")["Sales"].sum().idxmax()

top_category = df.groupby("Category")["Sales"].sum().idxmax()

st.success(f"{top_region} region leads revenue generation")

st.info(f"{top_category} category dominates overall performance")

st.warning("Revenue concentration is heavily dependent on top cities")


st.divider()


# ================= DOWNLOAD SECTION =================

st.subheader("⬇ Export Filtered Dataset")

csv = df.to_csv(index=False).encode()

st.download_button(
    "Download CSV",
    csv,
    "filtered_sales.csv"
)


# ================= FOOTER =================

st.caption(
    "Built by Apoorv Pachori • Retail Sales Intelligence Platform • 2026"
)