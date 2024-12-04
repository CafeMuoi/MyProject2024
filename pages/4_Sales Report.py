# pages/sales_report.py
import streamlit as st
import pandas as pd
import plotly.express as px

def sales_report():
    st.title("📊 Sales Report")
    
    # Load sales data
    df = pd.read_csv("sales.csv")
    
    # Sidebar filters
    st.sidebar.header("Sales Report Filters")
    regions = st.sidebar.multiselect(
        "Select Regions", 
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )
    categories = st.sidebar.multiselect(
        "Select Categories",
        options=df["Category"].unique(), 
        default=df["Category"].unique()
    )
    
    # Filter dataframe
    df_selection = df.query("Region == @regions & Category == @categories")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{df_selection['TotalPrice'].sum():,.0f}")
    col2.metric("Total Quantity", f"{df_selection['Quantity'].sum():,.0f}")
    col3.metric("Average Unit Price", f"{df_selection['UnitPrice'].mean():,.2f}")
    
    # Sales by Region Chart
    st.subheader("Sales by Region")
    fig_region = px.pie(df_selection, values='TotalPrice', names='Region', title='Sales Distribution')
    st.plotly_chart(fig_region, use_container_width=True)
    
    # Sales Trend
    st.subheader("Sales Trend")
    df_selection['OrderDate'] = pd.to_datetime(df_selection['OrderDate'])
    sales_trend = df_selection.groupby(df_selection['OrderDate'].dt.to_period('M'))['TotalPrice'].sum()
    fig_trend = px.line(x=sales_trend.index.astype(str), y=sales_trend.values, 
                        labels={'x': 'Month', 'y': 'Total Sales'})
    st.plotly_chart(fig_trend, use_container_width=True)


def main():
    sales_report()  # Gọi hàm báo cáo

if __name__ == "__main__":
    main()