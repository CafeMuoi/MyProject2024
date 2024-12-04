import streamlit as st
import pandas as pd
import plotly.express as px

def customer_report():
    st.title("👥 Customer Insights")
    
    # Load sales data
    df = pd.read_csv("sales.csv")
    
    # Sidebar filters
    st.sidebar.header("Customer Report Filters")
    regions = st.sidebar.multiselect(
        "Select Regions", 
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )
    cities = st.sidebar.multiselect(
        "Select Cities",
        options=df["City"].unique(), 
        default=df["City"].unique()
    )
    
    # Filter dataframe
    df_selection = df.query("Region == @regions & City == @cities")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customer Sales", f"{df_selection['TotalPrice'].sum():,.0f}")
    col2.metric("Number of Cities", len(df_selection['City'].unique()))
    col3.metric("Average Order Value", f"{df_selection['TotalPrice'].mean():,.2f}")
    
    # Sales by City
    st.subheader("Sales Distribution by City")
    city_sales = df_selection.groupby('City')['TotalPrice'].sum()
    fig_city = px.bar(x=city_sales.index, y=city_sales.values, 
                      labels={'x': 'City', 'y': 'Total Sales'})
    st.plotly_chart(fig_city, use_container_width=True)
    
    # Regional Performance
    st.subheader("Regional Performance")
    fig_region = px.pie(df_selection, values='TotalPrice', names='Region', 
                        title='Sales Distribution by Region')
    st.plotly_chart(fig_region, use_container_width=True)

def main():
    customer_report()
if __name__ == "__main__":
    main()
