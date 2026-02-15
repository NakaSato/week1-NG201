import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_dynamic_filters import DynamicFilters

# Page config
st.set_page_config(
    page_title="Sales Data Dashboard",
    layout="wide",
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('sales_data_sample 2.xls')
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    return df

df = load_data()

# Main content
st.title("Sales Data Dashboard")

# Filters at the top
with st.container(border=True):
    st.markdown("### Filters")
    dynamic_filters = DynamicFilters(df, filters=['YEAR_ID', 'COUNTRY', 'PRODUCTLINE'])
    # Display filters in 3 columns at the top
    dynamic_filters.display_filters(location='columns', num_columns=3, gap='small')

# Apply filters and get the filtered dataframe
filtered_df = dynamic_filters.filter_df()

# KPI Metrics
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_sales = filtered_df['SALES'].sum()
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        total_orders = filtered_df['ORDERNUMBER'].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    with col3:
        avg_order_value = filtered_df['SALES'].mean()
        st.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    with col4:
        total_quantity = filtered_df['QUANTITYORDERED'].sum()
        st.metric("Total Quantity", f"{total_quantity:,}")

st.markdown("---")

# Charts Row 1
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales by Product Line")
        sales_by_product = filtered_df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
        fig1 = px.bar(
            sales_by_product,
            x='PRODUCTLINE',
            y='SALES',
            color='SALES',
            color_continuous_scale='Blues',
            title="Total Sales by Product Line"
        )
        st.plotly_chart(fig1, width='stretch')
    with col2:
        st.subheader("Sales by Country")
        sales_by_country = filtered_df.groupby('COUNTRY')['SALES'].sum().reset_index()
        fig2 = px.pie(
            sales_by_country,
            values='SALES',
            names='COUNTRY',
            title="Sales Distribution by Country"
        )
        st.plotly_chart(fig2, width='stretch')

# Charts Row 2
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales Trend Over Time")
        sales_trend = filtered_df.groupby(filtered_df['ORDERDATE'].dt.to_period('M'))['SALES'].sum().reset_index()
        sales_trend['ORDERDATE'] = sales_trend['ORDERDATE'].astype(str)
        fig3 = px.line(
            sales_trend,
            x='ORDERDATE',
            y='SALES',
            title="Monthly Sales Trend",
            markers=True
        )
        st.plotly_chart(fig3, width='stretch')
    with col2:
        st.subheader("Sales by Deal Size")
        sales_by_dealsize = filtered_df.groupby('DEALSIZE')['SALES'].sum().reset_index()
        fig4 = px.bar(
            sales_by_dealsize,
            x='DEALSIZE',
            y='SALES',
            color='DEALSIZE',
            title="Sales by Deal Size"
        )
        st.plotly_chart(fig4, width='stretch')

# Charts Row 3
with st.container(border=True):
    st.subheader("Top 10 Customers by Sales")
    top_customers = filtered_df.groupby('CUSTOMERNAME')['SALES'].sum().nlargest(10).reset_index()
    fig5 = px.bar(
        top_customers,
        x='SALES',
        y='CUSTOMERNAME',
        orientation='h',
        color='SALES',
        title="Top 10 Customers"
    )
    fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig5, width='stretch')

# Data Table
with st.container(border=True):
    st.subheader("Data Preview")
    st.dataframe(
        filtered_df[['ORDERNUMBER', 'ORDERDATE', 'CUSTOMERNAME', 'PRODUCTLINE', 'SALES', 'QUANTITYORDERED', 'COUNTRY']].head(20),
        width='stretch'
    )

# Statistics Summary
with st.container(border=True):
    st.subheader("Statistical Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Numerical Columns Statistics:**")
        st.dataframe(filtered_df[['SALES', 'QUANTITYORDERED', 'PRICEEACH', 'MSRP']].describe())
    with col2:
        st.write("**Sales by Year:**")
        sales_by_year = filtered_df.groupby('YEAR_ID').agg({
            'SALES': ['sum', 'mean', 'count']
        }).round(2)
        sales_by_year.columns = ['Total Sales', 'Avg Sales', 'Order Count']
        st.dataframe(sales_by_year)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: grey; padding: 20px 0;">
        <p>Mr.Chanthawat Kiriyadee | 2410717302003 | คณะวิศวกรรมศาสตร์ | <a href="mailto:2410717302003@live4.utcc.ac.th">2410717302003@live4.utcc.ac.th</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
