import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Title
st.title("📊 Retail Sales Performance Dashboard")

st.markdown("Interactive analytics of retail sales dataset")

# Load dataset
df = pd.read_csv("train.csv")

# Convert date column
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Create Month-Year column
df['Month-Year'] = df['Order Date'].dt.to_period('M').astype(str)

# ================= KPI SECTION =================

st.subheader("📈 Key Business Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${round(df['Sales'].sum(),2)}")

col2.metric("Total Orders", df['Order ID'].nunique())

col3.metric("Total Customers", df['Customer ID'].nunique())

st.markdown("---")


# ================= FILTER =================

region_filter = st.selectbox(
    "Select Region",
    ["All"] + list(df['Region'].unique())
)

if region_filter != "All":
    df = df[df['Region'] == region_filter]


# ================= CHARTS =================

st.subheader("📊 Visual Analysis")

col1, col2 = st.columns(2)


# Monthly Sales Trend

with col1:

    monthly_sales = df.groupby('Month-Year')['Sales'].sum()

    fig, ax = plt.subplots(figsize=(6,4))

    monthly_sales.plot(ax=ax)

    ax.set_title("Monthly Sales Trend")

    st.pyplot(fig)


# Category Distribution

with col2:

    category_sales = df.groupby('Category')['Sales'].sum()

    fig, ax = plt.subplots(figsize=(6,4))

    ax.pie(
        category_sales,
        labels=category_sales.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Category Contribution")

    st.pyplot(fig)


st.markdown("---")


# ================= TOP CITIES =================

st.subheader("🏙 Top Performing Cities")

top_cities = (
    df.groupby('City')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_cities)


st.markdown("---")


# ================= DATA VIEW =================

st.subheader("📄 Raw Dataset Preview")

st.dataframe(df)