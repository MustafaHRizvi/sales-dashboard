# Sales Dashboard and Data Analysis

This repository contains a Streamlit dashboard for visualizing and analyzing sales data. It includes an interactive Streamlit app for displaying key business insights and trends, as well as a Jupyter Notebook for data cleaning, preprocessing, and exploratory data analysis (EDA).

## Repository Contents:
- **app_sql.py**: The Streamlit application that uses SQL queries for the dashboard. It includes various interactive visualizations, such as:
  - Top 10 revenue-generating products.
  - Highest-selling products in each region.
  - Month-over-month growth comparison for 2022 and 2023.
  - Highest sales month by category.
  - Subcategory growth by profit in 2023 vs 2022.

- **app_pandas.py**: The same as the SQL version but uses Pandas instead. This version was created to allow the dashboard to be hosted on the Streamlit Community Cloud.

- **[Live Dashboard](https://mustafahrizvi-sales-dashboard-app-pandas-2eagui.streamlit.app/)**: A live version of the Streamlit dashboard hosted on Streamlit Community Cloud.

- **retail_orders_kaggle.ipynb**: A Jupyter Notebook containing the data cleaning, preprocessing, and exploratory data analysis (EDA) steps used to prepare the dataset for analysis and visualization. The notebook includes:
  - Handling missing values.
  - Data transformations (e.g., feature engineering).

- **orders.csv**: The original dataset downloaded from Kaggle using the Kaggle API. This file contains the raw sales data.

- **orders_processed.csv**: The cleaned and processed dataset generated as the output of the `retail_orders_kaggle.ipynb` notebook. This file is used as the input for the Streamlit dashboard.

## Technologies Used:
- Streamlit for building the interactive dashboard.
- Pandas for data manipulation and analysis.
- Plotly and Seaborn for interactive and static visualizations.
- SQLAlchemy for querying a PostgreSQL database.