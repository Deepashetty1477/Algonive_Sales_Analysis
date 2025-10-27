import pkgutil
if not hasattr(pkgutil, "find_loader"):
    import importlib.util
    pkgutil.find_loader = importlib.util.find_spec

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Load data
sales_df = pd.read_csv("data/retail_sales_dataset.csv")
forecast_df = pd.read_csv("outputs/sales_forecast.csv")

# Prepare data
sales_df['Date'] = pd.to_datetime(sales_df['Date'])
sales_df['Month'] = sales_df['Date'].dt.to_period('M').astype(str)
monthly_sales = sales_df.groupby('Month')['Total Amount'].sum().reset_index()

# Create the app
app = Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1("📊 Sales Data Analysis Dashboard", style={'textAlign': 'center'}),
    
    html.H3("Monthly Sales Trend"),
    dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Total Amount', markers=True,
                             title="Total Sales Over Time")),

    html.H3("Sales by Product Category"),
    dcc.Graph(figure=px.bar(sales_df, x='Product Category', y='Total Amount', color='Product Category',
                            title="Sales by Product Category", barmode='group')),

    html.H3("Gender-wise Sales Distribution"),
    dcc.Graph(figure=px.pie(sales_df, names='Gender', values='Total Amount',
                            title="Sales Distribution by Gender")),

    html.H3("📈 Sales Forecast (Next 30 Days)"),
    dcc.Graph(figure=px.line(forecast_df, x='ds', y='yhat',
                             title="Predicted Future Sales (Prophet Model)",
                             labels={'ds': 'Date', 'yhat': 'Predicted Sales'}))
])

if __name__ == '__main__':
    app.run(debug=False)


