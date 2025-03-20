import streamlit as st
import pandas as pd
import plotly.express as px

df_orders = pd.read_csv('orders_processed.csv', parse_dates=['order_date']) 

# Streamlit dashboard layout
st.title('Sales Dashboard')

# Question 1: Top 10 Revenue Generating Products
st.subheader('Top 10 Revenue Generating Products')
df_product_revenue = df_orders.groupby('product_id')['sale_price'].sum().reset_index()
df_product_revenue = df_product_revenue.sort_values('sale_price', ascending=False).head(10)

# Display the data in a table
st.dataframe(df_product_revenue)

# Plotting the revenue of top 10 products with Plotly (Interactive)
fig = px.bar(df_product_revenue, x='product_id', y='sale_price', title='Top 10 Revenue Generating Products')
fig.update_layout(xaxis_title='Product ID', yaxis_title='Total Revenue')
st.plotly_chart(fig)

# Question 2: Top 5 Highest Selling Products by Region
st.subheader('Top 5 Highest Selling Products by Region')
df_region_sales = df_orders.groupby(['region', 'product_id'])['quantity'].sum().reset_index()
df_region_sales = df_region_sales.sort_values(['region', 'quantity'], ascending=[True, False])
df_region_top5 = df_region_sales.groupby('region').head(5)

# Display the data in a table
st.dataframe(df_region_top5)

# Plotting the top-selling products by region with Plotly (Interactive)
fig = px.bar(df_region_top5, x='product_id', y='quantity', color='region',
             title='Top 5 Highest Selling Products in Each Region')
fig.update_layout(xaxis_title='Product ID', yaxis_title='Total Sales')
st.plotly_chart(fig)

# Question 3: Month-over-Month Growth Comparison for 2022 and 2023
st.subheader('Month Over Month Growth Comparison for 2022 and 2023')

# Filter data for 2022 and 2023
df_2022 = df_orders[df_orders['order_date'].dt.year == 2022]
df_2023 = df_orders[df_orders['order_date'].dt.year == 2023]

# Group by month and calculate total sales
df_2022_monthly = df_2022.groupby(df_2022['order_date'].dt.month)['sale_price'].sum().reset_index()
df_2023_monthly = df_2023.groupby(df_2023['order_date'].dt.month)['sale_price'].sum().reset_index()

# Merge the two years' data on month
df_growth = pd.merge(df_2022_monthly, df_2023_monthly, on='order_date', how='left', suffixes=('_2022', '_2023'))

# Calculate month-over-month growth
df_growth['month_over_month_growth'] = ((df_growth['sale_price_2023'] - df_growth['sale_price_2022']) / df_growth['sale_price_2022']) * 100

# Display the data in a table
st.dataframe(df_growth)

# Plotting month-over-month growth with Plotly (Interactive)
fig = px.line(df_growth, x='order_date', y='month_over_month_growth', markers=True, title='Month-over-Month Growth Comparison for 2022 and 2023')
fig.update_layout(xaxis_title='Month', yaxis_title='Growth (%)')
st.plotly_chart(fig)

# Question 4: Highest Sales Month by Category
st.subheader('Highest Sales Month by Category')
df_category_sales = df_orders.groupby([df_orders['category'], df_orders['order_date'].dt.month])['sale_price'].sum().reset_index()

# Find the highest sales month for each category
df_category_sales['rank'] = df_category_sales.groupby('category')['sale_price'].rank(method='first', ascending=False)
df_category_sales = df_category_sales[df_category_sales['rank'] == 1]

# Display the data in a table
st.dataframe(df_category_sales)

# Plotting the highest sales month for each category with Plotly (Interactive)
df_category_sales['month_category'] = df_category_sales['category'] + ' - ' + df_category_sales['order_date'].astype(str)
fig = px.bar(df_category_sales, x='month_category', y='sale_price', title='Highest Sales Month by Category')
fig.update_layout(xaxis_title='Month and Category', yaxis_title='Sales')
st.plotly_chart(fig)

# Question 5: Subcategory Growth by Profit in 2023 vs 2022
st.subheader('Subcategory Growth by Profit in 2023 vs 2022')

# Filter data for 2022 and 2023
df_2022_profit = df_orders[df_orders['order_date'].dt.year == 2022].groupby('sub_category')['profit'].sum().reset_index()
df_2023_profit = df_orders[df_orders['order_date'].dt.year == 2023].groupby('sub_category')['profit'].sum().reset_index()

# Merge the two years' profit data
df_profit_growth = pd.merge(df_2022_profit, df_2023_profit, on='sub_category', how='left', suffixes=('_2022', '_2023'))

# Calculate the profit growth
df_profit_growth['profit_growth'] = ((df_profit_growth['profit_2023'] - df_profit_growth['profit_2022']) / df_profit_growth['profit_2022']) * 100

# Display the data in a table
st.dataframe(df_profit_growth)

# Plotting profit growth by subcategory with Plotly (Interactive)
fig = px.bar(df_profit_growth, x='sub_category', y='profit_growth', title='Subcategory Growth by Profit in 2023 vs 2022')
fig.update_layout(xaxis_title='Subcategory', yaxis_title='Profit Growth (%)')
st.plotly_chart(fig)
