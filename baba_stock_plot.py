# Install required libraries if not already installed
# !pip install yfinance plotly pandas

import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Fetch BABA stock data
ticker = "BABA"
stock_data = yf.Ticker(ticker).history(period="1y")

# Check if data is available
if stock_data.empty:
    print(f"No data found for {ticker}")
else:
    # Calculate moving averages
    stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()

    # Create candlestick chart
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name=f"{ticker} Candlestick"
    ))

    # Add moving averages
    fig.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['50_MA'],
        name='50-Day MA',
        line=dict(color='blue', width=1)
    ))
    
    fig.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['200_MA'],
        name='200-Day MA',
        line=dict(color='red', width=1)
    ))

    # Update layout
    fig.update_layout(
        title=f"{ticker} Stock Price (Last 1 Year)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=True,
        template='plotly_dark'
    )

    # Show the plot
    fig.show()