import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import sqlite3
from datetime import datetime

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from config import SQLITE_DB

# Set page config
st.set_page_config(
    page_title="Northwind Data Warehouse Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("Northwind Data Warehouse Dashboard")

# Connect to database
@st.cache_data
def load_data():
    conn = sqlite3.connect(SQLITE_DB)
    sales_df = pd.read_sql("""
        SELECT fs.*, 
               dc.CompanyName, dc.Country, dc.City,
               dp.ProductName, dp.CategoryName, dp.SupplierCountry
        FROM fact_sales fs
        JOIN dim_customer dc ON fs.CustomerID = dc.CustomerID
        JOIN dim_product dp ON fs.ProductID = dp.ProductID
    """, conn)
    conn.close()
    
    # Convert OrderDate to datetime
    sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'])
    
    return sales_df

# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Sidebar - OLAP Operations Selection
st.sidebar.header("OLAP Operations")
operation = st.sidebar.selectbox(
    "Select OLAP Operation",
    ["Roll-up & Drill-down", "Slice & Dice", "Pivot Analysis"]
)

# Common Filters (Slice operation)
st.sidebar.header("Global Filters (Slice)")
selected_years = st.sidebar.multiselect(
    "Select Years",
    options=sorted(df['OrderDate'].dt.year.unique()),
    default=sorted(df['OrderDate'].dt.year.unique())[-3:]
)

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df['Country'].unique()),
    default=sorted(df['Country'].unique())[:5]
)

# Apply global filters
if selected_years:
    df = df[df['OrderDate'].dt.year.isin(selected_years)]
if selected_countries:
    df = df[df['Country'].isin(selected_countries)]

# Main Content based on selected operation
if operation == "Roll-up & Drill-down":
    st.header("Roll-up & Drill-down Analysis")
    
    # Dimension Selection
    dimension = st.radio(
        "Select Dimension",
        ["Time", "Geography", "Product"],
        horizontal=True
    )
    
    if dimension == "Time":
        level = st.selectbox(
            "Select Time Level",
            ["Year", "Quarter", "Month", "Day"]
        )
        
        df['Year'] = df['OrderDate'].dt.year.astype(int)
        df['Quarter'] = df['OrderDate'].dt.to_period('Q').astype(str)
        df['Month'] = df['OrderDate'].dt.strftime('%Y-%m')
        df['Day'] = df['OrderDate'].dt.strftime('%Y-%m-%d')
        
        if level == "Year":
            agg_data = df.groupby('Year')['RevenueEUR'].sum().reset_index()
            x_col = 'Year'
            # Add formatting for year axis
            fig = px.bar(agg_data, x=x_col, y='RevenueEUR',
                        title=f'Revenue by {level}',
                        labels={'RevenueEUR': 'Revenue (EUR)', 'Year': 'Year'},
                        text=agg_data['RevenueEUR'].round(2))
            fig.update_traces(texttemplate='€%{text:,.0f}', textposition='outside')
            fig.update_xaxes(tickformat='d', dtick=1)  # Force integer ticks for years
            st.plotly_chart(fig, use_container_width=True)
        elif level == "Quarter":
            agg_data = df.groupby('Quarter')['RevenueEUR'].sum().reset_index()
            x_col = 'Quarter'
        elif level == "Month":
            agg_data = df.groupby('Month')['RevenueEUR'].sum().reset_index()
            x_col = 'Month'
        else:
            agg_data = df.groupby('Day')['RevenueEUR'].sum().reset_index()
            x_col = 'Day'
        
        fig = px.bar(agg_data, x=x_col, y='RevenueEUR',
                    title=f'Revenue by {level}',
                    labels={'RevenueEUR': 'Revenue (EUR)'},
                    text=agg_data['RevenueEUR'].round(2))
        fig.update_traces(texttemplate='€%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
    elif dimension == "Geography":
        level = st.selectbox(
            "Select Geographic Level",
            ["Country", "City"]
        )
        
        if level == "Country":
            agg_data = df.groupby('Country')['RevenueEUR'].sum().reset_index()
            x_col = 'Country'
        else:
            agg_data = df.groupby(['Country', 'City'])['RevenueEUR'].sum().reset_index()
            x_col = 'City'
        
        agg_data = agg_data.sort_values('RevenueEUR', ascending=True)
        
        fig = px.bar(agg_data, x='RevenueEUR', y=x_col,
                    title=f'Revenue by {level}',
                    labels={'RevenueEUR': 'Revenue (EUR)'},
                    text=agg_data['RevenueEUR'].round(2),
                    orientation='h')
        fig.update_traces(texttemplate='€%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        if level == "City":
            st.dataframe(
                agg_data.style.format({'RevenueEUR': '€{:,.2f}'}),
                use_container_width=True
            )
    
    else:  # Product
        level = st.selectbox(
            "Select Product Level",
            ["Category", "Product"]
        )
        
        if level == "Category":
            agg_data = df.groupby('CategoryName')['RevenueEUR'].sum().reset_index()
            x_col = 'CategoryName'
        else:
            selected_category = st.selectbox(
                "Select Category to View Products",
                options=sorted(df['CategoryName'].unique())
            )
            agg_data = df[df['CategoryName'] == selected_category].groupby('ProductName')['RevenueEUR'].sum().reset_index()
            x_col = 'ProductName'
        
        agg_data = agg_data.sort_values('RevenueEUR', ascending=True)
        
        fig = px.bar(agg_data, x='RevenueEUR', y=x_col,
                    title=f'Revenue by {level}',
                    labels={'RevenueEUR': 'Revenue (EUR)'},
                    text=agg_data['RevenueEUR'].round(2),
                    orientation='h')
        fig.update_traces(texttemplate='€%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

elif operation == "Slice & Dice":
    st.header("Slice & Dice Analysis")
    
    # Additional dice filters
    col1, col2 = st.columns(2)
    with col1:
        dice_dimension1 = st.selectbox(
            "Select First Dimension",
            ["Country", "CategoryName", "Year", "SupplierCountry"]
        )
    with col2:
        dice_dimension2 = st.selectbox(
            "Select Second Dimension",
            ["CategoryName", "Country", "Year", "SupplierCountry"],
            index=1
        )
    
    if dice_dimension1 != dice_dimension2:
        # Prepare data for selected dimensions
        if "Year" in [dice_dimension1, dice_dimension2]:
            df['Year'] = df['OrderDate'].dt.year.astype(int)
        
        agg_data = df.groupby([dice_dimension1, dice_dimension2])['RevenueEUR'].sum().reset_index()
        
        # Create interactive heatmap
        pivot_data = agg_data.pivot(index=dice_dimension1, columns=dice_dimension2, values='RevenueEUR')
        
        fig = px.imshow(pivot_data,
                       labels=dict(x=dice_dimension2, y=dice_dimension1, color="Revenue (EUR)"),
                       aspect="auto",
                       title=f'Revenue Heatmap: {dice_dimension1} vs {dice_dimension2}')
        
        fig.update_traces(text=pivot_data.round(2), texttemplate="€%{text:,.0f}")
        fig.update_layout(coloraxis_colorbar_title="Revenue (EUR)")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed data
        st.subheader("Detailed Data View")
        st.dataframe(
            agg_data.pivot_table(
                values='RevenueEUR',
                index=dice_dimension1,
                columns=dice_dimension2,
                aggfunc='sum'
            ).style.format("€{:,.2f}"),
            use_container_width=True
        )
    else:
        st.warning("Please select different dimensions for analysis")

else:  # Pivot Analysis
    st.header("Pivot Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rows = st.selectbox(
            "Select Row Dimension",
            ["Country", "CategoryName", "SupplierCountry", "Year"]
        )
    
    with col2:
        cols = st.selectbox(
            "Select Column Dimension",
            ["CategoryName", "Country", "SupplierCountry", "Year"],
            index=1
        )
    
    with col3:
        agg_func = st.selectbox(
            "Select Aggregation",
            ["Sum", "Average", "Count", "Min", "Max"]
        )
    
    if rows != cols:
        # Prepare data
        if "Year" in [rows, cols]:
            df['Year'] = df['OrderDate'].dt.year.astype(int)
        
        # Create pivot table
        if agg_func == "Sum":
            agg_method = 'sum'
            value_col = 'RevenueEUR'
            format_str = "€{:,.2f}"
        elif agg_func == "Average":
            agg_method = 'mean'
            value_col = 'RevenueEUR'
            format_str = "€{:,.2f}"
        elif agg_func == "Count":
            agg_method = 'count'
            value_col = 'OrderID'  # Count orders instead of revenue
            format_str = "{:,.0f}"  # Integer format for counts
        elif agg_func == "Min":
            agg_method = 'min'
            value_col = 'RevenueEUR'
            format_str = "€{:,.2f}"
        else:
            agg_method = 'max'
            value_col = 'RevenueEUR'
            format_str = "€{:,.2f}"
        
        pivot_table = pd.pivot_table(
            df,
            values=value_col,
            index=rows,
            columns=cols,
            aggfunc=agg_method,
            fill_value=0
        )
        
        # Add totals
        pivot_table['Total'] = pivot_table.sum(axis=1)
        pivot_table.loc['Total'] = pivot_table.sum()
        
        # Display pivot table
        st.dataframe(
            pivot_table.style.format(format_str),
            use_container_width=True
        )
        
        # Visualization
        fig = px.imshow(pivot_table.iloc[:-1, :-1],  # Exclude totals from heatmap
                       labels=dict(x=cols, y=rows, color=f"{agg_func}"),
                       aspect="auto",
                       title=f'{agg_func} Analysis: {rows} vs {cols}')
        
        fig.update_traces(text=pivot_table.iloc[:-1, :-1].round(2), 
                         texttemplate="%{text:,.0f}" if agg_func == "Count" else "€%{text:,.0f}")
        fig.update_layout(coloraxis_colorbar_title=agg_func)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select different dimensions for rows and columns")

# Footer
st.markdown("---")
st.markdown("Data source: Northwind Database | Last updated: Daily")
