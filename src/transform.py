import pandas as pd
from config import CITY_FIXES, COUNTRY_FIXES

def handle_missing_values(df, placeholder='Unknown'):
    """Fill missing values in DataFrame with placeholder."""
    return df.fillna(placeholder)

def remove_duplicates(df):
    """Remove duplicate rows from DataFrame."""
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        print(f"{duplicate_count} duplicate rows found. Removing them.")
        return df.drop_duplicates()
    return df

def clean_dataframes(dataframes):
    """Clean all DataFrames by handling missing values and duplicates."""
    cleaned_dfs = {}
    for name, df in dataframes.items():
        print(f"\n--- {name} ---")
        print("Null values before filling:")
        print(df.isna().sum()[df.isna().sum() > 0])
        
        df = handle_missing_values(df)
        df = remove_duplicates(df)
        
        cleaned_dfs[name] = df
        print(f"{name}: nulls filled and duplicates handled.")
    return cleaned_dfs

def create_dimensions(tables):
    """Create dimension tables from source tables."""
    # dim_customer
    dim_customer = tables['customers'][[
        'CustomerID', 'CompanyName', 'ContactName', 'City', 'Country'
    ]].copy()
    
    # dim_product
    dim_product = tables['products'].merge(
        tables['categories'], on='CategoryID', how='left'
    ).merge(
        tables['suppliers'], on='SupplierID', how='left'
    )
    
    dim_product = dim_product[[
        'ProductID', 'ProductName', 'CategoryName', 'CompanyName', 'Country'
    ]].rename(columns={
        'CompanyName': 'SupplierName',
        'Country': 'SupplierCountry'
    })
    
    # dim_date
    tables['orders']['OrderDate'] = pd.to_datetime(tables['orders']['OrderDate'], format='mixed')
    dim_date = tables['orders'][['OrderID', 'OrderDate']].copy()
    dim_date['Year'] = dim_date['OrderDate'].dt.year
    dim_date['Month'] = dim_date['OrderDate'].dt.month
    dim_date['Day'] = dim_date['OrderDate'].dt.day
    
    return {
        'dim_customer': dim_customer,
        'dim_product': dim_product,
        'dim_date': dim_date
    }

def create_fact_table(tables):
    """Create fact table from source tables."""
    fact_sales = tables['order_details'].merge(
        tables['orders'][['OrderID', 'CustomerID', 'OrderDate']], 
        on='OrderID', how='left'
    ).merge(
        tables['products'][['ProductID', 'ProductName']], 
        on='ProductID', how='left'
    )
    
    fact_sales['OrderDate'] = pd.to_datetime(fact_sales['OrderDate'])
    fact_sales['RevenueUSD'] = fact_sales['UnitPrice'] * fact_sales['Quantity']
    
    return fact_sales[[
        'OrderID', 'CustomerID', 'ProductID', 'OrderDate', 
        'Quantity', 'UnitPrice', 'Discount', 'RevenueUSD'
    ]]

def enrich_customer_dimension(dim_customer, world_cities):
    """Enrich customer dimension with additional geographic data."""
    # Create lowercase versions for matching
    dim_customer['City_lower'] = dim_customer['City'].str.lower()
    dim_customer['Country_lower'] = dim_customer['Country'].str.lower()
    world_cities['city_lower'] = world_cities['city'].str.lower()
    world_cities['country_lower'] = world_cities['country'].str.lower()
    
    # Apply fixes to standardized city and country columns
    dim_customer['City_lower'] = dim_customer['City_lower'].replace(CITY_FIXES)
    dim_customer['Country_lower'] = dim_customer['Country_lower'].replace(COUNTRY_FIXES)
    
    # Join with world cities data
    enriched_customer = dim_customer.merge(
        world_cities,
        left_on=['City_lower', 'Country_lower'],
        right_on=['city_lower', 'country_lower'],
        how='left'
    )
    
    # Select and rename final columns
    return enriched_customer[[
        'CustomerID', 'CompanyName', 'ContactName', 'City', 'Country',
        'admin_name', 'lat', 'lng', 'population'
    ]].rename(columns={
        'admin_name': 'Region',
        'lat': 'Latitude',
        'lng': 'Longitude',
        'population': 'CityPopulation'
    }) 