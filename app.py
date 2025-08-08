from flask import Flask, render_template, request, jsonify
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.DARKLY])

# Sample data - replace with real API calls
def get_crypto_data():
    """Get crypto price data from CoinGecko API"""
    try:
        # Bitcoin data
        btc_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
        btc_response = requests.get(btc_url)
        btc_data = btc_response.json()
        
        # Ethereum data
        eth_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
        eth_response = requests.get(eth_url)
        eth_data = eth_response.json()
        
        return {
            'bitcoin': {
                'price': btc_data['bitcoin']['usd'],
                'change_24h': btc_data['bitcoin']['usd_24h_change'],
                'market_cap': btc_data['bitcoin']['usd_market_cap']
            },
            'ethereum': {
                'price': eth_data['ethereum']['usd'],
                'change_24h': eth_data['ethereum']['usd_24h_change'],
                'market_cap': eth_data['ethereum']['usd_market_cap']
            }
        }
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return {
            'bitcoin': {'price': 45000, 'change_24h': 2.5, 'market_cap': 850000000000},
            'ethereum': {'price': 2800, 'change_24h': 1.8, 'market_cap': 350000000000}
        }

def generate_portfolio_data():
    """Generate sample portfolio data"""
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    
    # Sample portfolio values
    portfolio_values = []
    base_value = 10000
    
    for date in dates:
        # Add some volatility
        volatility = 0.02
        change = (pd.np.random.random() - 0.5) * volatility
        value = base_value * (1 + change)
        portfolio_values.append(value)
        base_value = value
    
    return pd.DataFrame({
        'Date': dates,
        'Portfolio Value': portfolio_values
    })

# Sample addresses (replace with real addresses)
SAMPLE_ADDRESSES = {
    'bitcoin': [
        '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy'
    ],
    'ethereum': [
        '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
        '0x1234567890123456789012345678901234567890'
    ]
}

# Dashboard layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🚀 Crypto Portfolio Dashboard", 
                   className="text-center text-primary mb-4"),
            html.Hr()
        ])
    ]),
    
    # Price Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Bitcoin", className="card-title"),
                    html.H2(f"${get_crypto_data()['bitcoin']['price']:,.2f}", 
                           className="text-success"),
                    html.P(f"24h: {get_crypto_data()['bitcoin']['change_24h']:+.2f}%",
                           className="text-muted")
                ])
            ], className="mb-3")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Ethereum", className="card-title"),
                    html.H2(f"${get_crypto_data()['ethereum']['price']:,.2f}", 
                           className="text-info"),
                    html.P(f"24h: {get_crypto_data()['ethereum']['change_24h']:+.2f}%",
                           className="text-muted")
                ])
            ], className="mb-3")
        ], width=6)
    ]),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Portfolio Performance"),
                dbc.CardBody([
                    dcc.Graph(id='portfolio-chart')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Market Cap Distribution"),
                dbc.CardBody([
                    dcc.Graph(id='market-cap-pie')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Address Tracking
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Address Balances"),
                dbc.CardBody([
                    html.Div(id='address-table')
                ])
            ])
        ])
    ]),
    
    # Update interval
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    )
], fluid=True, className="p-4")

# Callback for portfolio chart
@app.callback(
    Output('portfolio-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_portfolio_chart(n):
    df = generate_portfolio_data()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Portfolio Value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#00ff88', width=3)
    ))
    
    fig.update_layout(
        title="Portfolio Performance Over Time",
        xaxis_title="Date",
        yaxis_title="Value (USD)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

# Callback for market cap pie chart
@app.callback(
    Output('market-cap-pie', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_market_cap_pie(n):
    crypto_data = get_crypto_data()
    
    labels = ['Bitcoin', 'Ethereum']
    values = [crypto_data['bitcoin']['market_cap'], crypto_data['ethereum']['market_cap']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=['#f7931a', '#627eea']
    )])
    
    fig.update_layout(
        title="Market Cap Distribution",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

# Callback for address table
@app.callback(
    Output('address-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_address_table(n):
    table_rows = []
    
    # Bitcoin addresses
    for i, addr in enumerate(SAMPLE_ADDRESSES['bitcoin']):
        table_rows.append(
            dbc.Row([
                dbc.Col("Bitcoin", width=2),
                dbc.Col(addr[:20] + "...", width=6),
                dbc.Col("0.5 BTC", width=2),
                dbc.Col("$22,500", width=2)
            ], className="mb-2")
        )
    
    # Ethereum addresses
    for i, addr in enumerate(SAMPLE_ADDRESSES['ethereum']):
        table_rows.append(
            dbc.Row([
                dbc.Col("Ethereum", width=2),
                dbc.Col(addr[:20] + "...", width=6),
                dbc.Col("2.5 ETH", width=2),
                dbc.Col("$7,000", width=2)
            ], className="mb-2")
        )
    
    return table_rows

# Flask routes
@server.route('/')
def index():
    return app.index()

@server.route('/api/crypto-data')
def api_crypto_data():
    return jsonify(get_crypto_data())

@server.route('/api/addresses')
def api_addresses():
    return jsonify(SAMPLE_ADDRESSES)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
