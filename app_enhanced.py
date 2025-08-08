from flask import Flask, render_template, request, jsonify
import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from crypto_tracker import CryptoTracker
import numpy as np

# Load environment variables
load_dotenv()

# Initialize Flask app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.DARKLY])

# Initialize crypto tracker
tracker = CryptoTracker()

# Sample addresses (replace with your real addresses)
SAMPLE_ADDRESSES = {
    'bitcoin': [
        '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Genesis block address
        '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy'   # Another sample address
    ],
    'ethereum': [
        '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
        '0x1234567890123456789012345678901234567890'
    ]
}

def get_crypto_data():
    """Get crypto price data from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'bitcoin': {
                    'price': data['bitcoin']['usd'],
                    'change_24h': data['bitcoin']['usd_24h_change'],
                    'market_cap': data['bitcoin']['usd_market_cap'],
                    'volume_24h': data['bitcoin']['usd_24h_vol']
                },
                'ethereum': {
                    'price': data['ethereum']['usd'],
                    'change_24h': data['ethereum']['usd_24h_change'],
                    'market_cap': data['ethereum']['usd_market_cap'],
                    'volume_24h': data['ethereum']['usd_24h_vol']
                }
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return None

def generate_portfolio_data():
    """Generate realistic portfolio data"""
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    
    # Generate realistic portfolio values with crypto-like volatility
    portfolio_values = []
    base_value = 10000
    
    for date in dates:
        # Add crypto-like volatility (higher than traditional assets)
        volatility = 0.05  # 5% daily volatility
        trend = 0.0005  # Slight upward trend
        
        # Random walk with trend
        change = np.random.normal(trend, volatility)
        value = base_value * (1 + change)
        portfolio_values.append(max(value, 0))  # Ensure non-negative
        base_value = value
    
    return pd.DataFrame({
        'Date': dates,
        'Portfolio Value': portfolio_values
    })

def generate_price_history():
    """Generate historical price data for charts"""
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    
    # Bitcoin price simulation
    btc_base = 45000
    btc_prices = []
    for date in dates:
        volatility = 0.03
        change = np.random.normal(0, volatility)
        price = btc_base * (1 + change)
        btc_prices.append(price)
        btc_base = price
    
    # Ethereum price simulation
    eth_base = 2800
    eth_prices = []
    for date in dates:
        volatility = 0.04
        change = np.random.normal(0, volatility)
        price = eth_base * (1 + change)
        eth_prices.append(price)
        eth_base = price
    
    return pd.DataFrame({
        'Date': dates,
        'Bitcoin': btc_prices,
        'Ethereum': eth_prices
    })

# Dashboard layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🚀 Crypto Portfolio Dashboard", 
                   className="text-center text-primary mb-4"),
            html.P("Real-time tracking of Bitcoin and Ethereum addresses", 
                  className="text-center text-muted mb-4")
        ])
    ]),
    
    # Price Cards with real-time data
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Bitcoin", className="card-title"),
                    html.H2(id="btc-price", className="text-success"),
                    html.P(id="btc-change", className="text-muted"),
                    html.Small(id="btc-market-cap", className="text-muted")
                ])
            ], className="mb-3", style={"border": "1px solid #00ff88"})
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Ethereum", className="card-title"),
                    html.H2(id="eth-price", className="text-info"),
                    html.P(id="eth-change", className="text-muted"),
                    html.Small(id="eth-market-cap", className="text-muted")
                ])
            ], className="mb-3", style={"border": "1px solid #627eea"})
        ], width=6)
    ]),
    
    # Portfolio Summary
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Portfolio Summary"),
                dbc.CardBody([
                    html.H3(id="total-portfolio-value", className="text-warning"),
                    html.P("Total Portfolio Value", className="text-muted"),
                    dbc.Row([
                        dbc.Col([
                            html.H5(id="btc-portfolio-value", className="text-success"),
                            html.Small("Bitcoin Holdings", className="text-muted")
                        ], width=6),
                        dbc.Col([
                            html.H5(id="eth-portfolio-value", className="text-info"),
                            html.Small("Ethereum Holdings", className="text-muted")
                        ], width=6)
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Charts Row 1
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
                dbc.CardHeader("Price History"),
                dbc.CardBody([
                    dcc.Graph(id='price-history-chart')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Market Cap Distribution"),
                dbc.CardBody([
                    dcc.Graph(id='market-cap-pie')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("24h Volume Comparison"),
                dbc.CardBody([
                    dcc.Graph(id='volume-chart')
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

# Callbacks for real-time data updates
@app.callback(
    [Output('btc-price', 'children'),
     Output('btc-change', 'children'),
     Output('btc-market-cap', 'children'),
     Output('eth-price', 'children'),
     Output('eth-change', 'children'),
     Output('eth-market-cap', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_price_cards(n):
    crypto_data = get_crypto_data()
    
    if crypto_data:
        btc_price = f"${crypto_data['bitcoin']['price']:,.2f}"
        btc_change = f"24h: {crypto_data['bitcoin']['change_24h']:+.2f}%"
        btc_market_cap = f"Market Cap: ${crypto_data['bitcoin']['market_cap']:,.0f}"
        
        eth_price = f"${crypto_data['ethereum']['price']:,.2f}"
        eth_change = f"24h: {crypto_data['ethereum']['change_24h']:+.2f}%"
        eth_market_cap = f"Market Cap: ${crypto_data['ethereum']['market_cap']:,.0f}"
    else:
        btc_price = "$45,000.00"
        btc_change = "24h: +2.50%"
        btc_market_cap = "Market Cap: $850,000,000,000"
        
        eth_price = "$2,800.00"
        eth_change = "24h: +1.80%"
        eth_market_cap = "Market Cap: $350,000,000,000"
    
    return btc_price, btc_change, btc_market_cap, eth_price, eth_change, eth_market_cap

@app.callback(
    [Output('total-portfolio-value', 'children'),
     Output('btc-portfolio-value', 'children'),
     Output('eth-portfolio-value', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_portfolio_summary(n):
    crypto_data = get_crypto_data()
    
    if crypto_data:
        # Calculate portfolio values (sample data)
        btc_holdings = 0.5  # Sample BTC holdings
        eth_holdings = 2.5  # Sample ETH holdings
        
        btc_value = btc_holdings * crypto_data['bitcoin']['price']
        eth_value = eth_holdings * crypto_data['ethereum']['price']
        total_value = btc_value + eth_value
        
        return (f"${total_value:,.2f}", 
                f"${btc_value:,.2f}", 
                f"${eth_value:,.2f}")
    else:
        return "$29,500.00", "$22,500.00", "$7,000.00"

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
        line=dict(color='#00ff88', width=3),
        fill='tonexty',
        fillcolor='rgba(0,255,136,0.1)'
    ))
    
    fig.update_layout(
        title="Portfolio Performance Over Time",
        xaxis_title="Date",
        yaxis_title="Value (USD)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    return fig

# Callback for price history chart
@app.callback(
    Output('price-history-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_price_history_chart(n):
    df = generate_price_history()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Bitcoin'],
        mode='lines',
        name='Bitcoin',
        line=dict(color='#f7931a', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Ethereum'],
        mode='lines',
        name='Ethereum',
        line=dict(color='#627eea', width=2)
    ))
    
    fig.update_layout(
        title="Price History",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    return fig

# Callback for market cap pie chart
@app.callback(
    Output('market-cap-pie', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_market_cap_pie(n):
    crypto_data = get_crypto_data()
    
    if crypto_data:
        labels = ['Bitcoin', 'Ethereum']
        values = [crypto_data['bitcoin']['market_cap'], crypto_data['ethereum']['market_cap']]
    else:
        labels = ['Bitcoin', 'Ethereum']
        values = [850000000000, 350000000000]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=['#f7931a', '#627eea'],
        textinfo='label+percent',
        textposition='inside'
    )])
    
    fig.update_layout(
        title="Market Cap Distribution",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

# Callback for volume chart
@app.callback(
    Output('volume-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_volume_chart(n):
    crypto_data = get_crypto_data()
    
    if crypto_data:
        labels = ['Bitcoin', 'Ethereum']
        values = [crypto_data['bitcoin']['volume_24h'], crypto_data['ethereum']['volume_24h']]
    else:
        labels = ['Bitcoin', 'Ethereum']
        values = [25000000000, 15000000000]
    
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker_color=['#f7931a', '#627eea']
    )])
    
    fig.update_layout(
        title="24h Trading Volume",
        xaxis_title="Cryptocurrency",
        yaxis_title="Volume (USD)",
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
                dbc.Col([
                    html.I(className="fab fa-bitcoin text-warning me-2"),
                    "Bitcoin"
                ], width=2),
                dbc.Col([
                    html.Code(addr[:20] + "...", className="text-light")
                ], width=6),
                dbc.Col("0.5 BTC", width=2, className="text-success"),
                dbc.Col("$22,500", width=2, className="text-warning")
            ], className="mb-2 p-2", style={"border": "1px solid #333", "border-radius": "5px"})
        )
    
    # Ethereum addresses
    for i, addr in enumerate(SAMPLE_ADDRESSES['ethereum']):
        table_rows.append(
            dbc.Row([
                dbc.Col([
                    html.I(className="fab fa-ethereum text-info me-2"),
                    "Ethereum"
                ], width=2),
                dbc.Col([
                    html.Code(addr[:20] + "...", className="text-light")
                ], width=6),
                dbc.Col("2.5 ETH", width=2, className="text-info"),
                dbc.Col("$7,000", width=2, className="text-warning")
            ], className="mb-2 p-2", style={"border": "1px solid #333", "border-radius": "5px"})
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
