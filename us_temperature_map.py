import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime
import time
import numpy as np

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
import random

# Function to generate random temperatures instead of calling the API
def generate_random_temperature():
    """Generate a random temperature between 0°F and 100°F"""
    return round(random.uniform(0, 100), 1)

def get_temperature(lat, lon):
    """Get temperature for a given latitude and longitude"""
    return generate_random_temperature()

def update_temperatures():
    """Update temperatures for all cities"""
    temperatures = []
    for _, row in df.iterrows():
        temp = get_temperature(row['Latitude'], row['Longitude'])
        temperatures.append(temp if temp is not None else float('nan'))
    return temperatures

def create_temperature_grid():
    """Create a grid of temperature points for heatmap"""
    lat_min, lat_max = df['Latitude'].min(), df['Latitude'].max()
    lon_min, lon_max = df['Longitude'].min(), df['Longitude'].max()
    
    # Create a grid of points
    lat_points = np.linspace(lat_min, lat_max, 50)
    lon_points = np.linspace(lon_min, lon_max, 50)
    
    # Create meshgrid
    lon_grid, lat_grid = np.meshgrid(lon_points, lat_points)
    
    # Get temperatures for grid points
    temperatures = []
    for lat, lon in zip(lat_grid.flatten(), lon_grid.flatten()):
        temp = get_temperature(lat, lon)
        temperatures.append(temp if temp is not None else float('nan'))
    
    return lat_grid, lon_grid, np.array(temperatures).reshape(lat_grid.shape)

# App layout
app.layout = html.Div([
    html.H1('US Temperature Heatmap',
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
        
        # Temperature Range Filter
        html.Div([
            html.Label('Temperature Range:',
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.RangeSlider(
                id='temp-range-slider',
                min=0,
                max=120,
                step=5,
                value=[0, 120],
                marks={
                    0: '0°F',
                    30: '30°F',
                    60: '60°F',
                    90: '90°F',
                    120: '120°F'
                }
            )
        ], style={'width': '400px', 'display': 'inline-block', 'marginRight': '20px'}),
        
        # Update Interval
        dcc.Interval(
            id='interval-component',
            interval=300000,  # Update every 5 minutes (300000 milliseconds)
            n_intervals=0
        ),
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
     Output('info-panel', 'children')],
    [Input('region-dropdown', 'value'),
     Input('interval-component', 'n_intervals'),
     Input('temp-range-slider', 'value')]
)
def update_map(selected_region, n_intervals, temp_range):
    # Filter data based on selected region
    filtered_df = df.copy()
    if selected_region != 'ALL':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    
    # Get current temperatures
    filtered_df['Temperature'] = update_temperatures()
    
    # Create temperature grid for heatmap
    lat_grid, lon_grid, temp_grid = create_temperature_grid()
    
    # Create the map
    fig = go.Figure()
    
    # Add heatmap layer
    fig.add_trace(go.Densitymapbox(
        lat=lat_grid.flatten(),
        lon=lon_grid.flatten(),
        z=temp_grid.flatten(),
        colorscale='RdYlBu_r',  # Red-Yellow-Blue (reversed)
        zmin=temp_range[0],
        zmax=temp_range[1],
        radius=20,
        showscale=True,
        colorbar=dict(
            title='Temperature (°F)',
          #  titleside='right'
        )
    ))
    
    # Add city points
    fig.add_trace(go.Scattermapbox(
        lat=filtered_df['Latitude'],
        lon=filtered_df['Longitude'],
        mode='markers+text',
        marker=dict(
            size=10,
            color=filtered_df['Temperature'],
            colorscale='RdYlBu_r',
            cmin=temp_range[0],
            cmax=temp_range[1],
            showscale=False
        ),
        text=filtered_df['City'],
        textposition='top center',
        hoverinfo='text',
        hovertext=filtered_df.apply(lambda row: f"{row['City']}<br>Temperature: {row['Temperature']:.1f}°F", axis=1)
    ))
    
    # Update map layout
    fig.update_layout(
        mapbox_style='carto-positron',
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=700,
        title_x=0.5,
        clickmode='event+select',
        mapbox=dict(
            bearing=0,
            pitch=0,
            zoom=3,
            center=dict(lat=39.8283, lon=-98.5795)
        )
    )
    
    # Create information panel content
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info_content = [
        html.H3('Summary Information', style={'marginBottom': '15px'}),
        html.Div([
            html.P(f"Last Updated: {current_time}"),
            html.P(f"Cities Shown: {len(filtered_df)}"),
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
    
    return fig, info_content

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
    city_name = clickData['points'][0]['text']
    city_data = df[df['City'] == city_name].iloc[0]
    temperature = city_data['Temperature']
    
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
    app.run(host='127.0.0.1', port=12357, debug=True) 