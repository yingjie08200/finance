import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__)

# Prevent the default development server from running on 8050
app.config.suppress_callback_exceptions = True

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

def calculate_rsi(data, periods=14):
    """Calculate RSI for a given price series"""
    close_delta = data['Close'].diff()
    
    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    # Calculate the EWMA
    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi

def calculate_moving_averages(data):
    """Calculate moving averages for the price data"""
    ma20 = data['Close'].rolling(window=20).mean()
    ma60 = data['Close'].rolling(window=60).mean()
    ma200 = data['Close'].rolling(window=200).mean()
    return ma20, ma60, ma200

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
], style={'padding': '20px', 'backgroundColor': 'white'})

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
        
        # Calculate RSI and Moving Averages
        rsi = calculate_rsi(hist)
        ma20, ma60, ma200 = calculate_moving_averages(hist)
        
        # Create subplot with secondary y-axis
        fig = make_subplots(rows=2, cols=1, 
                           shared_xaxes=True,
                           vertical_spacing=0.03,
                           row_heights=[0.7, 0.3])

        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price',
                increasing_line_color='#26a69a',
                decreasing_line_color='#ef5350'
            ),
            row=1, col=1
        )

        # Add Moving Averages
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=ma20,
                name='20 MA',
                line=dict(color='#1976D2', width=1.5)
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=ma60,
                name='60 MA',
                line=dict(color='#FB8C00', width=1.5)
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=ma200,
                name='200 MA',
                line=dict(color='#E91E63', width=1.5)
            ),
            row=1, col=1
        )
        # Set RSI y-axis range from 0 to 100
        fig.update_yaxes(range=[0, 100], row=2, col=1)
        # Add border frame to RSI subplot
        fig.update_xaxes(showline=True, linewidth=5, linecolor='#2c3e50', row=2, col=1)
        fig.update_yaxes(showline=True, linewidth=5, linecolor='#2c3e50', row=2, col=1)
        fig.update_layout(
            xaxis_showgrid=True,
            yaxis_showgrid=True,
            xaxis_zeroline=False,
            yaxis_zeroline=False,
            plot_bgcolor='grey'
        )
        # Add RSI
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=rsi,
                name='RSI',
                line=dict(color='#2962ff', width=2)
            ),
            row=2, col=1
        )

        # Add RSI overbought/oversold lines
        fig.add_hline(y=70, line_color='#ef5350', line_dash='dash', row=2, col=1)
        fig.add_hline(y=30, line_color='#26a69a', line_dash='dash', row=2, col=1)
        
        # Update layout
        fig.update_layout(
            title=f'{ticker_symbol} Stock Price and RSI',
            yaxis_title='Stock Price (USD)',
            yaxis2_title='RSI',
            template='plotly_white',
            xaxis_rangeslider_visible=False,
            height=800,
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#2c3e50'),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.8)'
            )
        )

        # Update y-axes labels and styling
        fig.update_yaxes(title_text="Price", row=1, col=1, gridcolor='#eee')
        fig.update_yaxes(title_text="RSI", row=2, col=1, gridcolor='#eee')
        fig.update_xaxes(gridcolor='#eee')
        
        return fig, ''
        
    except Exception as e:
        return {}, f"Error fetching data for {ticker_symbol}. Please check the ticker symbol."

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12355, debug=True) 