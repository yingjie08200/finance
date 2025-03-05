import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Multi-Stock Price Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H3("Stock Symbols (comma-separated):", style={'marginRight': '10px'}),
            dcc.Input(
                id='stock-input',
                value='AAPL,MSFT,GOOGL,AMZN',
                type='text',
                style={'fontSize': '18px', 'width': '300px'}
            ),
        ], style={'display': 'flex', 'alignItems': 'center'}),

        html.Div([
            html.H3("Select Time Period:", style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='time-period',
                options=[
                    {'label': '1 Month', 'value': '1mo'},
                    {'label': '3 Months', 'value': '3mo'},
                    {'label': '6 Months', 'value': '6mo'},
                    {'label': '1 Year', 'value': '1y'},
                    {'label': '5 Years', 'value': '5y'}
                ],
                value='1y',
                style={'width': '200px', 'fontSize': '18px'}
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginLeft': '30px'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),

    html.Button('Update Charts', id='update-button',
                style={'fontSize': '18px', 'margin': '10px auto', 'display': 'block'}),

    html.Div(id='charts-container', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
])


# Callback to update the graphs based on user input
@app.callback(
    Output('charts-container', 'children'),
    [Input('update-button', 'n_clicks')],
    [State('stock-input', 'value'),
     State('time-period', 'value')]
)
def update_graphs(n_clicks, stock_symbols_input, time_period):
    if stock_symbols_input is None or stock_symbols_input.strip() == '':
        return html.Div("Please enter at least one stock symbol.")

    # Parse multiple stock symbols
    stock_symbols = [symbol.strip() for symbol in stock_symbols_input.split(',')]

    # Limit to 4 stocks if more are provided
    if len(stock_symbols) > 4:
        stock_symbols = stock_symbols[:4]

    # Map dropdown values to datetime periods
    period_map = {
        '1mo': 30,
        '3mo': 90,
        '6mo': 180,
        '1y': 365,
        '5y': 1825
    }

    days = period_map[time_period]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    charts = []

    for symbol in stock_symbols:
        if not symbol:
            continue

        try:
            # Download stock data
            df = yf.download(symbol, start=start_date, end=end_date)

            if df.empty:
                charts.append(html.Div([
                    html.H3(f"No data found for {symbol}"),
                ], style={'width': '48%', 'margin': '1%', 'backgroundColor': '#f8f9fa', 'padding': '10px',
                          'borderRadius': '5px'}))
                continue

            # Create the candlestick chart
            candlestick = go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            )

            # Create the moving averages
            ma50 = go.Scatter(
                x=df.index,
                y=df['Close'].rolling(window=50).mean(),
                line=dict(color='orange', width=2),
                name='50-day MA'
            )

            ma200 = go.Scatter(
                x=df.index,
                y=df['Close'].rolling(window=200).mean(),
                line=dict(color='red', width=2),
                name='200-day MA'
            )

            # Create the figure
            fig = go.Figure(data=[candlestick, ma50, ma200])

            # Calculate performance metrics
            start_price = df['Close'].iloc[0]
            end_price = df['Close'].iloc[-1]
            percent_change = ((end_price - start_price) / start_price) * 100

            # Update layout
            fig.update_layout(
                title=f"{symbol} ({time_period}): {percent_change:.2f}%",
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )

            # Add the chart to our list
            chart_div = html.Div([
                dcc.Graph(figure=fig),
                html.Div([
                    html.Div([
                        html.P(f"Start: ${start_price:.2f}", style={'margin': '5px'}),
                        html.P(f"End: ${end_price:.2f}", style={'margin': '5px'}),
                    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                    html.P(f"Change: {percent_change:.2f}%",
                           style={'margin': '5px', 'fontWeight': 'bold',
                                  'color': 'green' if percent_change >= 0 else 'red',
                                  'textAlign': 'center'})
                ], style={'backgroundColor': '#f8f9fa', 'padding': '10px', 'borderRadius': '5px'})
            ], style={'width': '48%', 'margin': '1%'})

            charts.append(chart_div)

        except Exception as e:
            charts.append(html.Div([
                html.H3(f"Error loading data for {symbol}"),
                html.P(str(e))
            ], style={'width': '48%', 'margin': '1%', 'backgroundColor': '#f8f9fa', 'padding': '10px',
                      'borderRadius': '5px'}))

    # If no valid charts were created
    if not charts:
        return html.Div("No valid stock data found. Please check the symbols and try again.")

    return charts


# Run the app
if __name__ == '__main__':
    app.run(debug=True)