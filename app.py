import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Analytics Dashboard")
st.markdown(
    """
    #### Interactive Business Intelligence Dashboard
    Analyze sales performance, profit, customers, and product trends using interactive visualizations.
    """
)
st.markdown("---")

def kpi_card(title, value, color):
    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:10px;
            text-align:center;
            color:white;
            box-shadow:2px 2px 10px rgba(0,0,0,0.2);
        ">
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Load Data
df = pd.read_csv("data/samplesuperstore.csv")


st.subheader("Dataset Preview")
st.write(f"Total Records: {len(df)}")


st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart--v1.png",
    width=80
)

st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("---")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=True
)

df["Year"] = df["Order Date"].dt.year


region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["Region"].unique().tolist())
)

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

segment = st.sidebar.selectbox(
    "Select Segment",
    ["All"] + sorted(df["Segment"].unique().tolist())
)

state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df["State/Province"].unique().tolist())
)

year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(df["Year"].unique().tolist())
)

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if segment != "All":
    filtered_df = filtered_df[
        filtered_df["Segment"] == segment
    ]

if state != "All":
    filtered_df = filtered_df[
        filtered_df["State/Province"] == state
    ]

if year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == year
    ]
# ============================
# KPI Calculations
# ============================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("💰 Total Sales", f"${total_sales:,.0f}", "#1f77b4")

with col2:
    kpi_card("💵 Total Profit", f"${total_profit:,.0f}", "#2ca02c")

with col3:
    kpi_card("📦 Orders", total_orders, "#ff7f0e")

with col4:
    kpi_card("👥 Customers", total_customers, "#9467bd")

st.markdown("---")
st.subheader("📈 Sales Performance")
col1, col2 = st.columns(2)
# ==========================
# Monthly Sales Trend
# ==========================

filtered_df["Order Date"] = pd.to_datetime(
    filtered_df["Order Date"],
    format="mixed",
    dayfirst=True
)

filtered_df["YearMonth"] = filtered_df["Order Date"].dt.to_period("M")

monthly_sales = (
    filtered_df.groupby("YearMonth")["Sales"]
    .sum()
    .reset_index()
)
monthly_sales["YearMonth"] = monthly_sales["YearMonth"].astype(str)

fig_month = px.line(
    monthly_sales,
    x="YearMonth",
    y="Sales",
    title="📈 Monthly Sales Trend",
    markers=True
)
fig_month.update_traces(
    line=dict(width=4),
    marker=dict(size=8)
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales ($)"
)
with col1:
    st.plotly_chart(fig_month, use_container_width=True)

# ==========================
# Sales by Category
# ==========================

sales_category = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig_category = px.pie(
    sales_category,
    names="Category",
    values="Sales",
    hole=0.5,
    title="🥧 Sales by Category"
)

fig_category.update_layout(
    template="plotly_white",
    title_x=0.3,
    font=dict(size=14)
)

with col2:
    st.plotly_chart(fig_category, use_container_width=True)
# ==========================
# Sales by Region
# ==========================
col3, col4 = st.columns(2)

sales_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    color="Region",
    title="Sales by Region"
)

fig_region.update_layout(
    template="plotly_white",
    title_x=0.3,
    font=dict(size=14)
)

with col3:
    st.plotly_chart(fig_region, use_container_width=True)

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)
fig_product = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="🏆 Top 10 Products"
)


fig_product.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=500
)
with col4:
    st.plotly_chart(fig_product, use_container_width=True)

col5, col6 = st.columns(2)

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig_customer = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    title="Top 10 Customers"
)
fig_customer.update_layout(
    template="plotly_white",
    title_x=0.3,
    font=dict(size=14)
)

with col5:
    st.plotly_chart(fig_customer, use_container_width=True)

segment_sales = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

fig_segment = px.bar(
    segment_sales,
    x="Segment",
    y="Sales",
    color="Segment",
    title="Sales by Segment"
)

fig_segment.update_layout(
    template="plotly_white",
    title_x=0.3,
    font=dict(size=14)
)

with col6:
    st.plotly_chart(fig_segment, use_container_width=True)

st.markdown("---")

st.subheader("📄 Sales Details")

st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "smaplesuperstore.csv",
    "text/csv"
)

st.markdown("---")

st.info(
    f"""
    **Dashboard Summary**

    - Total Records: {len(filtered_df):,}
    - Regions: {filtered_df['Region'].nunique()}
    - Categories: {filtered_df['Category'].nunique()}
    - Customers: {filtered_df['Customer Name'].nunique()}
    """
)