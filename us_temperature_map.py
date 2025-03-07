import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime
import time

# Initialize the Dash app
app = dash.Dash(__name__)

# Define major US cities data
us_cities = {
    'City': [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
        'Miami', 'Atlanta', 'Boston', 'San Francisco', 'Detroit',
        'Seattle', 'Denver', 'Las Vegas', 'Minneapolis', 'Orlando',
        'Portland', 'Kansas City', 'New Orleans', 'Salt Lake City', 'Nashville'
    ],
    'Latitude': [
        40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
        39.9526, 29.4241, 32.7157, 32.7767, 37.3382,
        25.7617, 33.7490, 42.3601, 37.7749, 42.3314,
        47.6062, 39.7392, 36.1699, 44.9778, 28.5383,
        45.5155, 39.0997, 29.9511, 40.7608, 36.1627
    ],
    'Longitude': [
        -74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
        -75.1652, -98.4936, -117.1611, -96.7970, -121.8863,
        -80.1918, -84.3880, -71.0589, -122.4194, -83.0458,
        -122.3321, -104.9903, -115.1398, -93.2650, -81.3792,
        -122.6789, -94.5786, -90.0715, -111.8910, -86.7816
    ],
    'Region': [
        'Northeast', 'West', 'Midwest', 'South', 'Southwest',
        'Northeast', 'South', 'West', 'South', 'West',
        'Southeast', 'Southeast', 'Northeast', 'West', 'Midwest',
        'Northwest', 'Mountain', 'Southwest', 'Midwest', 'Southeast',
        'Northwest', 'Midwest', 'South', 'Mountain', 'South'
    ]
}

# Create DataFrame
df = pd.DataFrame(us_cities)

# OpenWeatherMap API configuration
API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_temperature(lat, lon):
    """Get temperature for a given latitude and longitude"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'imperial'  # Use Fahrenheit
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        return data['main']['temp']
    except:
        return None

def update_temperatures():
    """Update temperatures for all cities"""
    temperatures = []
    for _, row in df.iterrows():
        temp = get_temperature(row['Latitude'], row['Longitude'])
        temperatures.append(temp if temp is not None else float('nan'))
    return temperatures

# App layout
app.layout = html.Div([
    html.H1('US Temperature Map',
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
    
    html.Div([
        # Region Filter
        html.Div([
            html.Label('Filter by Region:',
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'All Regions', 'value': 'ALL'}] + 
                        [{'label': region, 'value': region} for region in sorted(df['Region'].unique())],
                value='ALL',
                style={'width': '300px'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '20px'}),
        
        # Zoom Level Control
        html.Div([
            html.Label('Zoom Level:',
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            html.Div([
                dcc.Slider(
                    id='zoom-slider',
                    min=2,
                    max=6,
                    step=0.5,
                    value=3,
                    marks={
                        2: 'Country',
                        3: 'Region',
                        4: 'State',
                        5: 'City',
                        6: 'Street'
                    }
                )
            ], style={'width': '300px'})
        ], style={'display': 'inline-block', 'marginRight': '20px'}),
        
        # Zoom Buttons
        html.Div([
            html.Button('Zoom In', id='zoom-in-btn', n_clicks=0,
                       style={'marginRight': '10px', 'padding': '5px 15px'}),
            html.Button('Zoom Out', id='zoom-out-btn', n_clicks=0,
                       style={'padding': '5px 15px'}),
        ], style={'display': 'inline-block'}),
        
        # Update Interval
        dcc.Interval(
            id='interval-component',
            interval=300000,  # Update every 5 minutes (300000 milliseconds)
            n_intervals=0
        ),
        
        # Store the current zoom level
        dcc.Store(id='current-zoom', data=3),
        # Store the current center coordinates
        dcc.Store(id='current-center', data={'lat': 39.8283, 'lon': -98.5795}),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Main content container with map and details panel
    html.Div([
        # Left side - Map
        html.Div([
            dcc.Graph(id='temperature-map',
                     style={'height': '700px'},
                     config={
                         'displayModeBar': True,
                         'scrollZoom': True,
                         'modeBarButtonsToAdd': ['zoomInMapbox', 'zoomOutMapbox', 'resetViewMapbox']
                     })
        ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        # Right side - Details Panel
        html.Div([
            html.Div([
                html.H3('Temperature Details', style={'marginBottom': '15px', 'color': '#2c3e50'}),
                html.Div(id='selected-city-details', children=[
                    html.P("Click on a city in the map to see detailed information.",
                          style={'font-style': 'italic', 'color': '#666'})
                ])
            ], style={
                'padding': '20px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'height': '650px',
                'overflowY': 'auto'
            })
        ], style={'width': '28%', 'display': 'inline-block', 'vertical-align': 'top', 'marginLeft': '2%'}),
    ]),
    
    # Bottom Information Panel
    html.Div(id='info-panel',
             style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa',
                    'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
], style={'padding': '20px', 'backgroundColor': 'white'})

@app.callback(
    [Output('temperature-map', 'figure'),
     Output('info-panel', 'children'),
     Output('current-zoom', 'data'),
     Output('current-center', 'data')],
    [Input('region-dropdown', 'value'),
     Input('interval-component', 'n_intervals'),
     Input('zoom-slider', 'value'),
     Input('zoom-in-btn', 'n_clicks'),
     Input('zoom-out-btn', 'n_clicks')],
    [State('current-zoom', 'data'),
     State('current-center', 'data'),
     State('temperature-map', 'figure')]
)
def update_map(selected_region, n_intervals, slider_zoom, zoom_in_clicks, zoom_out_clicks, 
               current_zoom, current_center, current_figure):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle zoom changes
    if trigger_id == 'zoom-slider':
        new_zoom = slider_zoom
    elif trigger_id == 'zoom-in-btn':
        new_zoom = min(current_zoom + 0.5, 6)
    elif trigger_id == 'zoom-out-btn':
        new_zoom = max(current_zoom - 0.5, 2)
    else:
        new_zoom = current_zoom

    # Update center if available in current figure
    new_center = current_center
    if current_figure and 'layout' in current_figure and 'mapbox' in current_figure['layout']:
        if 'center' in current_figure['layout']['mapbox']:
            new_center = current_figure['layout']['mapbox']['center']
    
    # Filter data based on selected region
    filtered_df = df.copy()
    if selected_region != 'ALL':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    
    # Get current temperatures
    filtered_df['Temperature'] = update_temperatures()
    
    # Create the map
    fig = px.scatter_mapbox(filtered_df,
                           lat='Latitude',
                           lon='Longitude',
                           hover_name='City',
                           hover_data=['Temperature', 'Region'],
                           color='Temperature',
                           size=[20] * len(filtered_df),
                           color_continuous_scale='RdYlBu_r',
                           zoom=new_zoom,
                           center=new_center,
                           title='Current Temperatures (°F)')
    
    # Update map layout
    fig.update_layout(
        mapbox_style='carto-positron',
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=700,
        title_x=0.5,
        clickmode='event+select',
        coloraxis_colorbar_title='Temperature (°F)',
        mapbox=dict(
            bearing=0,
            pitch=0,
            zoom=new_zoom,
            center=new_center
        )
    )
    
    # Create information panel content
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info_content = [
        html.H3('Summary Information', style={'marginBottom': '15px'}),
        html.Div([
            html.P(f"Last Updated: {current_time}"),
            html.P(f"Cities Shown: {len(filtered_df)}"),
            html.P(f"Current Zoom Level: {new_zoom:.1f}"),
            html.Div([
                html.P("Temperature Statistics:"),
                html.Ul([
                    html.Li(f"Average: {filtered_df['Temperature'].mean():.1f}°F"),
                    html.Li(f"Minimum: {filtered_df['Temperature'].min():.1f}°F"),
                    html.Li(f"Maximum: {filtered_df['Temperature'].max():.1f}°F")
                ])
            ])
        ])
    ]
    
    return fig, info_content, new_zoom, new_center

@app.callback(
    Output('selected-city-details', 'children'),
    [Input('temperature-map', 'clickData')]
)
def display_city_details(clickData):
    if not clickData:
        return [
            html.P("Click on a city in the map to see detailed information.",
                  style={'font-style': 'italic', 'color': '#666'})
        ]
    
    # Get the clicked city's data
    city_name = clickData['points'][0]['hovertext']
    city_data = df[df['City'] == city_name].iloc[0]
    temperature = clickData['points'][0]['customdata'][0]
    
    return [
        html.H4(city_data['City'], style={'color': '#2c3e50', 'marginBottom': '20px'}),
        html.Div([
            html.P('Current Temperature:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(f"{temperature:.1f}°F", style={'marginLeft': '20px', 'marginBottom': '15px', 'fontSize': '24px'}),
            
            html.P('Region:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(city_data['Region'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Location:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(f"Latitude: {city_data['Latitude']:.4f}°", style={'marginLeft': '20px', 'marginBottom': '5px'}),
            html.P(f"Longitude: {city_data['Longitude']:.4f}°", style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.Hr(style={'marginY': '20px'}),
            
            html.P("Click another city on the map to see its details.",
                  style={'font-style': 'italic', 'color': '#666', 'marginTop': '20px'})
        ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px'})
    ]

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12356, debug=True) 