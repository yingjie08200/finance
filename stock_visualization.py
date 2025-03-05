import yfinance as yf
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__)

# Default stock tickers
STOCK_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',
    'TSLA', 'NVDA', 'JPM', 'BAC', 'WMT'
]

# Time periods
TIME_PERIODS = [
    {'label': '1 Month', 'value': '1mo'},
    {'label': '3 Months', 'value': '3mo'},
    {'label': '6 Months', 'value': '6mo'},
    {'label': '1 Year', 'value': '1y'},
    {'label': '2 Years', 'value': '2y'},
    {'label': '5 Years', 'value': '5y'}
]

# App layout
app.layout = html.Div([
    html.H1('Stock Price Visualizer', 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
    
    html.Div([
        # Stock selection dropdown
        html.Div([
            html.Label('Select Stock:', 
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='stock-ticker-dropdown',
                options=[{'label': ticker, 'value': ticker} for ticker in STOCK_TICKERS],
                value='AAPL',
                style={'width': '200px'}
            ),
        ], style={'marginRight': '20px', 'display': 'inline-block'}),
        
        # Custom ticker input
        html.Div([
            html.Label('Or Enter Custom Ticker:', 
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.Input(
                id='custom-ticker-input',
                type='text',
                placeholder='Enter ticker...',
                style={'width': '150px'}
            ),
        ], style={'marginRight': '20px', 'display': 'inline-block'}),
        
        # Time period dropdown
        html.Div([
            html.Label('Select Time Period:', 
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='time-period-dropdown',
                options=TIME_PERIODS,
                value='1y',
                style={'width': '150px'}
            ),
        ], style={'display': 'inline-block'}),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Error message div
    html.Div(id='error-message', 
             style={'color': 'red', 'textAlign': 'center', 'marginTop': '10px'}),
    
    # Graph
    dcc.Graph(id='stock-graph')
], style={'padding': '20px'})

@app.callback(
    [Output('stock-graph', 'figure'),
     Output('error-message', 'children')],
    [Input('stock-ticker-dropdown', 'value'),
     Input('custom-ticker-input', 'value'),
     Input('time-period-dropdown', 'value')]
)
def update_graph(selected_ticker, custom_ticker, period):
    # Use custom ticker if provided, otherwise use selected ticker
    ticker_symbol = custom_ticker.strip().upper() if custom_ticker else selected_ticker
    
    try:
        # Fetch stock data
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period=period)
        
        if hist.empty:
            return {}, f"No data found for ticker {ticker_symbol}"
        
        # Create the candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close']
        )])
        
        # Update the layout
        fig.update_layout(
            title=f'{ticker_symbol} Stock Price',
            yaxis_title='Stock Price (USD)',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        return fig, ''
        
    except Exception as e:
        return {}, f"Error fetching data for {ticker_symbol}. Please check the ticker symbol."

if __name__ == '__main__':
    app.run(debug=True) 