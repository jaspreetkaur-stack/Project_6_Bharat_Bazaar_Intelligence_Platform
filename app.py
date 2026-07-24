import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Bharat Bazaar Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background:#F8FAFC;
}

h1,h2,h3{
    color:#0F172A;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:20px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
    border:1px solid #E5E7EB;
}

[data-testid="stMetricValue"]{
    color:#2563EB;
    font-size:32px;
    font-weight:bold;
}

[data-testid="stSidebar"]{
    background:#111827;
}

[data-testid="stSidebar"] *{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    path = Path("data/cleaned/cleaned_global_ecommerce_sales.csv")
    return pd.read_csv(path)

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("📌 Filters")

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Product_Category"].unique()),
    default=sorted(df["Product_Category"].unique())
)

payment = st.sidebar.multiselect(
    "Payment Method",
    sorted(df["Payment_Method"].unique()),
    default=sorted(df["Payment_Method"].unique())
)

filtered_df = df[
    (df["Country"].isin(country)) &
    (df["Product_Category"].isin(category)) &
    (df["Payment_Method"].isin(payment))
]

st.title("📊 Bharat Bazaar Intelligence Platform")
st.markdown("### End-to-End E-Commerce Analytics Dashboard")
# ==========================================
# KPI CALCULATIONS
# ==========================================

total_sales = filtered_df["Total_Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
avg_order_value = filtered_df["Total_Sales"].mean()

st.markdown("---")

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"${total_sales:,.0f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit:,.0f}"
    )

with col3:
    st.metric(
        label="🛒 Total Orders",
        value=f"{total_orders:,}"
    )

with col4:
    st.metric(
        label="📦 Avg Order Value",
        value=f"${avg_order_value:,.2f}"
    )

st.markdown("---")

# ==========================================
# DATA PREVIEW
# ==========================================

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)
# ==========================================
# VISUAL ANALYTICS
# ==========================================

st.markdown("---")
st.subheader("📊 Sales Analytics")

col1, col2 = st.columns(2)

# -----------------------------
# Sales by Country
# -----------------------------
country_sales = (
    filtered_df.groupby("Country", as_index=False)["Total_Sales"]
    .sum()
    .sort_values("Total_Sales", ascending=False)
)

fig_country = px.bar(
    country_sales,
    x="Country",
    y="Total_Sales",
    color="Total_Sales",
    title="🌍 Total Sales by Country",
    template="plotly_white"
)

fig_country.update_layout(
    height=450,
    xaxis_title="Country",
    yaxis_title="Sales"
)

col1.plotly_chart(fig_country, use_container_width=True)

# -----------------------------
# Product Category
# -----------------------------
category_sales = (
    filtered_df.groupby("Product_Category", as_index=False)["Total_Sales"]
    .sum()
)

fig_category = px.pie(
    category_sales,
    names="Product_Category",
    values="Total_Sales",
    hole=0.45,
    title="🛍️ Sales by Product Category"
)

fig_category.update_layout(height=450)

col2.plotly_chart(fig_category, use_container_width=True)

# ==========================================
# SECOND ROW
# ==========================================

col3, col4 = st.columns(2)

# -----------------------------
# Payment Method
# -----------------------------
payment_sales = (
    filtered_df.groupby("Payment_Method", as_index=False)["Total_Sales"]
    .sum()
)

fig_payment = px.bar(
    payment_sales,
    x="Payment_Method",
    y="Total_Sales",
    color="Payment_Method",
    title="💳 Sales by Payment Method",
    template="plotly_white"
)

fig_payment.update_layout(height=450)

col3.plotly_chart(fig_payment, use_container_width=True)

# -----------------------------
# Region Sales
# -----------------------------
region_sales = (
    filtered_df.groupby("Region", as_index=False)["Total_Sales"]
    .sum()
)

fig_region = px.line(
    region_sales,
    x="Region",
    y="Total_Sales",
    markers=True,
    title="📍 Sales by Region",
    template="plotly_white"
)

fig_region.update_layout(height=450)

col4.plotly_chart(fig_region, use_container_width=True)
# ==========================================
# PROFIT & CUSTOMER ANALYTICS
# ==========================================

st.markdown("---")
st.subheader("📈 Profit & Customer Insights")

col5, col6 = st.columns(2)

# -----------------------------
# Profit by Category
# -----------------------------
profit_category = (
    filtered_df.groupby("Product_Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig_profit = px.bar(
    profit_category,
    x="Product_Category",
    y="Profit",
    color="Profit",
    title="💹 Profit by Category",
    template="plotly_white"
)

fig_profit.update_layout(height=450)

col5.plotly_chart(fig_profit, use_container_width=True)

# -----------------------------
# Customer Segment
# -----------------------------
segment_sales = (
    filtered_df.groupby("Customer_Segment", as_index=False)["Total_Sales"]
    .sum()
)

fig_segment = px.pie(
    segment_sales,
    names="Customer_Segment",
    values="Total_Sales",
    hole=0.45,
    title="👥 Sales by Customer Segment"
)

fig_segment.update_layout(height=450)

col6.plotly_chart(fig_segment, use_container_width=True)

# ==========================================
# TOP SELLING PRODUCTS
# ==========================================

st.markdown("---")
st.subheader("🏆 Top 10 Selling Products")

top_products = (
    filtered_df.groupby("Product_Name", as_index=False)["Total_Sales"]
    .sum()
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)

fig_top_products = px.bar(
    top_products,
    x="Total_Sales",
    y="Product_Name",
    orientation="h",
    color="Total_Sales",
    title="Top 10 Products by Sales",
    template="plotly_white"
)

fig_top_products.update_layout(
    height=600,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig_top_products, use_container_width=True)
# ==========================================
# MACHINE LEARNING SALES PREDICTION
# ==========================================

st.markdown("---")
st.header("🤖 AI Sales Prediction")

try:
    model = joblib.load("models/best_random_forest_model.pkl")
    scaler = joblib.load("models/standard_scaler.pkl")

    c1, c2 = st.columns(2)

    with c1:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=5
        )

        unit_price = st.number_input(
            "Unit Price",
            min_value=1.0,
            value=100.0
        )

    with c2:
        discount = st.slider(
            "Discount (%)",
            0,
            50,
            10
        )

        shipping = st.number_input(
            "Shipping Cost",
            min_value=0.0,
            value=20.0
        )

    if st.button("🔮 Predict Sales"):

        sample = pd.DataFrame({
            "Quantity":[quantity],
            "Unit_Price":[unit_price],
            "Discount_Percent":[discount],
            "Shipping_Cost":[shipping]
        })

        sample_scaled = scaler.transform(sample)

        prediction = model.predict(sample_scaled)[0]

        st.success(f"💰 Predicted Sales: ${prediction:,.2f}")

except Exception as e:
    st.warning("Prediction model could not be loaded.")

# ==========================================
# DOWNLOAD FILTERED DATA
# ==========================================

st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;'>

### 🇮🇳 Bharat Bazaar Intelligence Platform

End-to-End Data Analytics & Machine Learning Dashboard

Built using

**Python | Streamlit | Plotly | Machine Learning | SQL | Power BI**

Made by **Jaspreet Kaur**

</div>
""",
unsafe_allow_html=True
)
# ==========================================
# BUSINESS INSIGHTS
# ==========================================

st.markdown("---")
st.header("📌 Business Insights")

top_country = (
    filtered_df.groupby("Country")["Total_Sales"]
    .sum()
    .idxmax()
)

top_category = (
    filtered_df.groupby("Product_Category")["Total_Sales"]
    .sum()
    .idxmax()
)

top_payment = (
    filtered_df.groupby("Payment_Method")["Total_Sales"]
    .sum()
    .idxmax()
)

st.success(f"🌍 Highest Sales Country: {top_country}")
st.success(f"🛍️ Best Product Category: {top_category}")
st.success(f"💳 Most Used Payment Method: {top_payment}")

st.info("""
### 📈 Recommendations

• Increase inventory for top-selling categories.

• Focus marketing campaigns in high-performing countries.

• Promote the most preferred payment method.

• Reduce discounts on highly profitable products.

• Optimize shipping cost to improve profit margin.
""")
st.sidebar.markdown("---")
st.sidebar.info("""
## 🇮🇳 Bharat Bazaar Intelligence Platform

**Developer:** Jaspreet Kaur

**Tech Stack**
- Python
- Streamlit
- Pandas
- Plotly
- SQL
- Machine Learning
- Power BI
""")
from datetime import datetime

st.caption(
    f"Last Updated: {datetime.now().strftime('%d %B %Y | %I:%M %p')}"
)
with st.expander("📈 Business Recommendations"):
    st.write("""
- Increase inventory for top-selling products.
- Focus marketing on high-performing countries.
- Improve shipping efficiency.
- Offer targeted discounts for low-performing categories.
- Strengthen customer retention programs.
""")
    st.subheader("📋 Dataset Summary")

summary = {
    "Rows": len(filtered_df),
    "Columns": len(filtered_df.columns),
    "Countries": filtered_df["Country"].nunique(),
    "Categories": filtered_df["Product_Category"].nunique()
}

st.json(summary)
st.success("✅ Dashboard Loaded Successfully")