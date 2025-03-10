import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import asyncio
import time

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button('Perform Task', id='button'),
    html.Div(id='output')
])

@app.callback(
    Output('output', 'children'),
    Input('button', 'n_clicks'),
    prevent_initial_call=True
)
async def perform_task(n_clicks):
    # Simulate a long-running task
    await asyncio.sleep(2)
    return f"Task completed after {n_clicks} clicks."

if __name__ == '__main__':
    app.run(debug=True)