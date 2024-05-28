# market/dash_apps/dash_plot.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.express as px
from market.models import MarketData
import pandas as pd

# Create a DjangoDash app instance
app = DjangoDash('SimpleMarket')

# Function to fetch and prepare data from the database
def get_data():
    data = MarketData.objects.all()
    df = pd.DataFrame(list(data.values()))
    return df

# Define the layout of the Dash app
app.layout = html.Div([
    dcc.Dropdown(
        id='vendor-dropdown',
        options=[
            {'label': vendor, 'value': vendor}
            for vendor in MarketData.objects.values_list('vendor_details', flat=True).distinct()
        ],
        value=None,
        placeholder="Select a vendor"
    ),
    dcc.Graph(id='vendor-graph')
])

# Define callback to update the graph based on selected vendor
@app.callback(
    Output('vendor-graph', 'figure'),
    [Input('vendor-dropdown', 'value')]
)
def update_graph(selected_vendor):
    df = get_data()
    if selected_vendor:
        df = df[df['vendor_details'] == selected_vendor]
    fig = px.bar(df, x='product_name', y='price', title=f'Product Prices from {selected_vendor}')
    return fig
