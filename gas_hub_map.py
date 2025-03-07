import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Define major natural gas hubs data
gas_hubs = {
    'Hub': [
        'Henry Hub',
        'AECO Hub',
        'Chicago Citygate',
        'Dominion South Point',
        'SoCal Citygate',
        'Waha Hub',
        'Algonquin Citygate',
        'Opal Hub',
        'Dawn Hub',
        'Malin Hub'
    ],
    'Price': [
        3.8, # Henry Hub (Louisiana)
        1.36, # AECO (Alberta)
        3.42, # Chicago
        4, # Dominion South (Pennsylvania)
        4, # SoCal (Los Angeles)
        4, # Waha (Texas)
        4.5, # Algonquin (Boston)
        4, # Opal (Wyoming)
        4, # Dawn (Ontario)
        4.2  # Malin (Oregon)
    ],
    'Volume': [
        685, # Henry Hub (Louisiana)
        253, # AECO (Alberta)
        536, # Chicago
        120, # Dominion South (Pennsylvania)
        230, # SoCal (Los Angeles)
        455, # Waha (Texas)
        241, # Algonquin (Boston)
        162, # Opal (Wyoming)
        253, # Dawn (Ontario)
        268  # Malin (Oregon)
    ],
    'Latitude': [
        30.2384, # Henry Hub (Louisiana)
        51.1784, # AECO (Alberta)
        41.8781, # Chicago
        40.4406, # Dominion South (Pennsylvania)
        34.0522, # SoCal (Los Angeles)
        31.5450, # Waha (Texas)
        42.3601, # Algonquin (Boston)
        41.7684, # Opal (Wyoming)
        42.9849, # Dawn (Ontario)
        42.0099  # Malin (Oregon)
    ],
    'Longitude': [
        -92.0184, # Henry Hub
        -114.1853, # AECO
        -87.6298, # Chicago
        -79.9959, # Dominion South
        -118.2437, # SoCal
        -103.0474, # Waha
        -71.0589, # Algonquin
        -110.7624, # Opal
        -81.2497, # Dawn
        -121.7297  # Malin
    ],
    'Description': [
        'Primary natural gas benchmark for North America',
        'Major Canadian trading hub in Alberta',
        'Major Midwest trading point',
        'Key hub for Marcellus/Utica shale gas',
        'Major Southern California distribution point',
        'Key hub for Permian Basin production',
        'Major Northeast US trading point',
        'Rocky Mountain regional hub',
        'Major storage and trading hub in Ontario',
        'Pacific Northwest regional hub'
    ],
    'Market_Area': [
        'Gulf Coast',
        'Western Canada',
        'Midwest',
        'Northeast',
        'West Coast',
        'Southwest',
        'Northeast',
        'Rocky Mountains',
        'Eastern Canada',
        'Pacific Northwest'
    ],
    'Additional_Info': [
        'Serves as the delivery point for NYMEX natural gas futures. Located in Erath, Louisiana. Connected to multiple interstate and intrastate pipelines.',
        'Located in Alberta, Canada. Major price point for Canadian natural gas. Connected to the NOVA Gas Transmission system.',
        'Major distribution point for Midwest markets. Connected to multiple major pipelines serving the region.',
        'Located in Appalachia. Key trading point for Marcellus shale gas production. Major supply point for Northeast markets.',
        'Primary trading point for Southern California market. Critical for California\'s natural gas supply.',
        'Located in West Texas. Major hub for Permian Basin production. Connected to multiple pipelines serving Texas and Mexico.',
        'Key supply point for New England markets. Critical during winter heating season.',
        'Services Rocky Mountain production. Connected to multiple interstate pipelines.',
        'Located in Ontario. Largest underground storage facility in Canada. Key supply point for Eastern Canadian and Northeast US markets.',
        'Important hub for Pacific Northwest and Northern California markets. Connected to Canadian and US supplies.'
    ]
}

# Create DataFrame
df = pd.DataFrame(gas_hubs)

# App layout
app.layout = html.Div([
    html.H1('Natural Gas Trading Hubs Map',
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
    
    html.Div([
        # Market Area Filter
        html.Div([
            html.Label('Filter by Market Area:',
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='market-area-dropdown',
                options=[{'label': area, 'value': area} for area in sorted(df['Market_Area'].unique())],
                value=[],  # Empty list means show all
                multi=True,
                style={'width': '300px'}
            ),
        ], style={'marginBottom': '20px'}),
    ], style={'textAlign': 'center'}),
    
    # Main content container with map and details panel
    html.Div([
        # Left side - Map
        html.Div([
            dcc.Graph(id='gas-hub-map',
                     style={'height': '700px'},
                     config={'displayModeBar': True})
        ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        # Right side - Details Panel
        html.Div([
            html.Div([
                html.H3('Hub Details', style={'marginBottom': '15px', 'color': '#2c3e50'}),
                html.Div(id='selected-hub-details', children=[
                    html.P("Click on a hub in the map to see detailed information.",
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
    html.Div(id='hub-info',
             style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa',
                    'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
], style={'padding': '20px', 'backgroundColor': 'white'})

@app.callback(
    [Output('gas-hub-map', 'figure'),
     Output('hub-info', 'children')],
    [Input('market-area-dropdown', 'value')]
)
def update_map(selected_areas):
    # Filter data based on selected market areas
    if selected_areas:
        filtered_df = df[df['Market_Area'].isin(selected_areas)]
    else:
        filtered_df = df
    # Add hub name labels to the dataframe for display
    filtered_df['text'] = filtered_df['Hub']
    # Create the map
    fig = px.scatter_mapbox(filtered_df,
                           lat='Latitude',
                           lon='Longitude',
                           hover_name='Hub',
                           hover_data=['Market_Area', 'Description'],
                           zoom=3,
                           text = 'text',
                           color = 'Price',
                           size = 'Volume',
                           center={'lat': 40, 'lon': -98},  # Center of North America
                           title='Natural Gas Trading Hubs')
    
    # Update map layout
    fig.update_layout(
        mapbox_style='carto-positron',  # Light map style
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=700,
        title_x=0.5,
        clickmode='event+select'
    )
    
    # Create information panel content
    info_content = [
        html.H3('Summary Information', style={'marginBottom': '15px'}),
        html.Div([
            html.P(f"Total Hubs Shown: {len(filtered_df)}"),
            html.P("Market Areas Shown:"),
            html.Ul([
                html.Li(area) for area in sorted(filtered_df['Market_Area'].unique())
            ])
        ])
    ]
    
    return fig, info_content

@app.callback(
    Output('selected-hub-details', 'children'),
    [Input('gas-hub-map', 'clickData')]
)
def display_hub_details(clickData):
    if not clickData:
        return [
            html.P("Click on a hub in the map to see detailed information.",
                  style={'font-style': 'italic', 'color': '#666'})
        ]
    
    # Get the clicked hub's data
    hub_name = clickData['points'][0]['hovertext']
    hub_data = df[df['Hub'] == hub_name].iloc[0]
    
    return [
        html.H4(hub_data['Hub'], style={'color': '#2c3e50', 'marginBottom': '20px'}),
        html.Div([
            html.P('Market Area:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(hub_data['Market_Area'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Location:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(f"Latitude: {hub_data['Latitude']:.4f}°", style={'marginLeft': '20px', 'marginBottom': '5px'}),
            html.P(f"Longitude: {hub_data['Longitude']:.4f}°", style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Description:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(hub_data['Description'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Additional Information:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(hub_data['Additional_Info'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.Hr(style={'marginY': '20px'}),
            
            html.P("Click another hub on the map to see its details.",
                  style={'font-style': 'italic', 'color': '#666', 'marginTop': '20px'})
        ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px'})
    ]

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12354, debug=True) 