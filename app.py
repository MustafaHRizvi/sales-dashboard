import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Setup the database connection (use your actual connection details)
# Connection string (replace with your actual values)
host = 'localhost'
port = 5432
dbname = 'postgres'
user = 'postgres'
password = '1234'

# Create a connection string for SQLAlchemy
conn_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

# Create SQLAlchemy engine
engine = create_engine(conn_str)

# Function to load data from SQL
def load_data(query):
    return pd.read_sql(query, con=engine)

# Streamlit dashboard layout
st.title('Sales Dashboard')


# Question 1: Top 10 highest revenue-generating products
st.subheader('Top 10 Revenue Generating Products')
query = """
SELECT product_id, SUM(sale_price) AS total_revenue
FROM df_orders
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;
"""
df = load_data(query)

# Display the data in a table
st.dataframe(df)

# Plotting the revenue of top 10 products with Plotly (Interactive)
fig = px.bar(df, x='product_id', y='total_revenue', title='Top 10 Revenue Generating Products')
fig.update_layout(xaxis_title='Product ID', yaxis_title='Total Revenue')
st.plotly_chart(fig)

# Question 2: Top 5 highest-selling products in each region
st.subheader('Top 5 Highest Selling Products by Region')
query = """
SELECT region, product_id, SUM(quantity) AS total_sales
FROM df_orders
GROUP BY region, product_id
ORDER BY region, total_sales DESC;
"""
df = load_data(query)
df_region = df.groupby('region').head(5)  # Top 5 per region

# Display the data in a table
st.dataframe(df_region)

# Plotting the top-selling products by region with Plotly (Interactive)
fig = px.bar(df_region, x='product_id', y='total_sales', color='region',
             title='Top 5 Highest Selling Products in Each Region')
fig.update_layout(xaxis_title='Product ID', yaxis_title='Total Sales')
st.plotly_chart(fig)

# Question 3: Month-over-month growth comparison for 2022 and 2023
st.subheader('Month Over Month Growth Comparison for 2022 and 2023')
query = """
SELECT 
    a.month,
    a.total_sales AS total_sales_2022,
    b.total_sales AS total_sales_2023,
    CASE
        WHEN b.total_sales IS NULL THEN NULL
        ELSE (b.total_sales - a.total_sales) / a.total_sales * 100
    END AS month_over_month_growth
FROM 
    (SELECT 
        EXTRACT(MONTH FROM order_date) AS month,
        SUM(sale_price) AS total_sales
    FROM 
        df_orders
    WHERE 
        EXTRACT(YEAR FROM order_date) = 2022
    GROUP BY 
        EXTRACT(MONTH FROM order_date)
    ) a
LEFT JOIN 
    (SELECT 
        EXTRACT(MONTH FROM order_date) AS month,
        SUM(sale_price) AS total_sales
    FROM 
        df_orders
    WHERE 
        EXTRACT(YEAR FROM order_date) = 2023
    GROUP BY 
        EXTRACT(MONTH FROM order_date)
    ) b
ON 
    a.month = b.month
ORDER BY 
    a.month;
"""
df = load_data(query)

# Display the data in a table
st.dataframe(df)

# Plotting month-over-month growth with Plotly (Interactive)
fig = px.line(df, x='month', y='month_over_month_growth', markers=True, title='Month-over-Month Growth Comparison for 2022 and 2023')
fig.update_layout(xaxis_title='Month', yaxis_title='Growth (%)')
st.plotly_chart(fig)

# Question 4: Highest sales month by category
st.subheader('Highest Sales Month by Category')
query = """
SELECT a.category, a.month, a.sales
FROM (
    SELECT 
        category, 
        EXTRACT(MONTH FROM order_date) AS month,
        EXTRACT(YEAR FROM order_date) AS year,
        SUM(sale_price) AS sales,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(sale_price) DESC) AS rank
    FROM 
        df_orders
    GROUP BY 
        category, EXTRACT(MONTH FROM order_date), EXTRACT(YEAR FROM order_date)
) a
WHERE a.rank = 1
ORDER BY a.category, a.month;
"""
df = load_data(query)

# Display the data in a table
st.dataframe(df)

# Plotting the highest sales month for each category with Plotly (Interactive)
df['month_category'] = df['category'] + ' - ' + df['month'].astype(str)
fig = px.bar(df, x='month_category', y='sales', title='Highest Sales Month by Category')
fig.update_layout(xaxis_title='Month and Category', yaxis_title='Sales')
st.plotly_chart(fig)

# Question 5: Subcategory growth by profit in 2023 vs 2022
st.subheader('Subcategory Growth by Profit in 2023 vs 2022')
query = """
SELECT a.sub_category, a.profit as profit_2022, b.profit as profit_2023,
(b.profit - a.profit) / a.profit * 100 as profit_growth
FROM
(SELECT sub_category, extract(year from order_date) as year, sum(profit) as profit
FROM df_orders
WHERE extract(year from order_date) = 2022
GROUP BY sub_category, extract(year from order_date)) a
LEFT JOIN
(SELECT sub_category, extract(year from order_date) as year, sum(profit) as profit
FROM df_orders
WHERE extract(year from order_date) = 2023
GROUP BY sub_category, extract(year from order_date)) b
ON a.sub_category = b.sub_category
ORDER BY profit_growth desc
LIMIT 5
"""
df = load_data(query)

# Display the data in a table
st.dataframe(df)

# Plotting profit growth by subcategory with Plotly (Interactive)
fig = px.bar(df, x='sub_category', y='profit_growth', title='Subcategory Growth by Profit in 2023 vs 2022')
fig.update_layout(xaxis_title='Subcategory', yaxis_title='Profit Growth (%)')
st.plotly_chart(fig)
