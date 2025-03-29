import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from config import DWH_PATH
import os

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Northwind Data Warehouse Dashboard", className="text-center my-4"),
            html.Hr()
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sales Overview"),
                dbc.CardBody([
                    dcc.Graph(id='sales-trend')
                ])
            ], className="mb-4")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top Products"),
                dbc.CardBody([
                    dcc.Graph(id='top-products')
                ])
            ], className="mb-4")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top Customers"),
                dbc.CardBody([
                    dcc.Graph(id='top-customers')
                ])
            ], className="mb-4")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Geographic Distribution"),
                dbc.CardBody([
                    dcc.Graph(id='geo-distribution')
                ])
            ])
        ])
    ])
], fluid=True)

def get_data():
    """Get data from the data warehouse."""
    conn = sqlite3.connect(DWH_PATH)
    
    # Get sales data
    sales_df = pd.read_sql("""
        SELECT 
            d.Year,
            d.Month,
            SUM(f.RevenueEUR) as TotalRevenue
        FROM fact_sales f
        JOIN dim_date d ON f.OrderDate = d.OrderDate
        GROUP BY d.Year, d.Month
        ORDER BY d.Year, d.Month
    """, conn)
    
    # Get top products
    top_products = pd.read_sql("""
        SELECT 
            p.ProductName,
            SUM(f.RevenueEUR) as TotalRevenue,
            SUM(f.Quantity) as TotalQuantity
        FROM fact_sales f
        JOIN dim_product p ON f.ProductID = p.ProductID
        GROUP BY p.ProductName
        ORDER BY TotalRevenue DESC
        LIMIT 10
    """, conn)
    
    # Get top customers
    top_customers = pd.read_sql("""
        SELECT 
            c.CompanyName,
            SUM(f.RevenueEUR) as TotalRevenue
        FROM fact_sales f
        JOIN dim_customer c ON f.CustomerID = c.CustomerID
        GROUP BY c.CompanyName
        ORDER BY TotalRevenue DESC
        LIMIT 10
    """, conn)
    
    # Get geographic distribution
    geo_dist = pd.read_sql("""
        SELECT 
            c.Country,
            c.City,
            SUM(f.RevenueEUR) as TotalRevenue
        FROM fact_sales f
        JOIN dim_customer c ON f.CustomerID = c.CustomerID
        GROUP BY c.Country, c.City
    """, conn)
    
    conn.close()
    return sales_df, top_products, top_customers, geo_dist

@app.callback(
    [Output('sales-trend', 'figure'),
     Output('top-products', 'figure'),
     Output('top-customers', 'figure'),
     Output('geo-distribution', 'figure')],
    [Input('sales-trend', 'id')]
)
def update_graphs(_):
    sales_df, top_products, top_customers, geo_dist = get_data()
    
    # Sales trend
    sales_fig = px.line(sales_df, 
                        x='Month', 
                        y='TotalRevenue',
                        title='Monthly Sales Trend',
                        labels={'TotalRevenue': 'Revenue (EUR)'})
    
    # Top products
    products_fig = px.bar(top_products,
                         x='ProductName',
                         y='TotalRevenue',
                         title='Top 10 Products by Revenue',
                         labels={'TotalRevenue': 'Revenue (EUR)'})
    
    # Top customers
    customers_fig = px.bar(top_customers,
                          x='CompanyName',
                          y='TotalRevenue',
                          title='Top 10 Customers by Revenue',
                          labels={'TotalRevenue': 'Revenue (EUR)'})
    
    # Geographic distribution
    geo_fig = px.scatter_geo(geo_dist,
                            lat='Latitude',
                            lon='Longitude',
                            size='TotalRevenue',
                            hover_name='City',
                            title='Sales Distribution by Location',
                            labels={'TotalRevenue': 'Revenue (EUR)'})
    
    return sales_fig, products_fig, customers_fig, geo_fig

if __name__ == '__main__':
    app.run_server(debug=True) 