import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Define global oil markets data
oil_markets = {
    'Market': [
        'WTI Cushing',
        'Brent',
        'Dubai Crude',
        'LOOP Sour',
        'Urals Mediterranean',
        'Bonny Light',
        'Tapis Crude',
        'Western Canadian Select',
        'Arab Light',
        'Oman Crude',
        'Maya Crude',
        'Daqing Crude'
    ],
    'Latitude': [
        35.9849,  # Cushing, Oklahoma
        57.9215,  # North Sea
        25.2532,  # Dubai
        29.0450,  # LOOP Terminal
        45.4642,  # Mediterranean
        4.7517,   # Bonny, Nigeria
        1.3521,   # Singapore
        51.0486,  # Hardisty, Alberta
        26.4207,  # Ras Tanura
        23.6100,  # Oman
        18.9261,  # Mexico
        46.5884   # Daqing, China
    ],
    'Longitude': [
        -96.7731, # Cushing
        1.8808,   # North Sea
        55.3657,  # Dubai
        -90.2083, # LOOP Terminal
        9.1900,   # Mediterranean
        7.1757,   # Bonny
        103.8198, # Singapore
        -111.3168,# Hardisty
        50.0963,  # Ras Tanura
        58.5400,  # Oman
        -91.9987, # Mexico
        125.1037  # Daqing
    ],
    'Type': [
        'Light Sweet Crude',
        'Light Sweet Crude',
        'Medium Sour Crude',
        'Sour Crude',
        'Medium Sour Crude',
        'Light Sweet Crude',
        'Light Sweet Crude',
        'Heavy Crude',
        'Medium Sour Crude',
        'Medium Sour Crude',
        'Heavy Sour Crude',
        'Medium Sweet Crude'
    ],
    'Region': [
        'North America',
        'Europe',
        'Middle East',
        'North America',
        'Europe/Asia',
        'Africa',
        'Asia Pacific',
        'North America',
        'Middle East',
        'Middle East',
        'Latin America',
        'Asia'
    ],
    'Description': [
        'Global benchmark for light sweet crude, delivered at Cushing, Oklahoma',
        'Major global benchmark for light sweet crude from the North Sea',
        'Middle Eastern benchmark crude, important for Asian markets',
        'US Gulf Coast benchmark for sour crude at Louisiana Offshore Oil Port',
        'Russian export blend, major benchmark for European refiners',
        'Nigerian light sweet crude, important for European and Asian markets',
        'Malaysian light sweet crude, benchmark for Asia-Pacific',
        'Canadian heavy crude benchmark, primarily traded in Alberta',
        'Saudi Arabian crude, major export grade to global markets',
        'Middle Eastern benchmark, delivered at Omani ports',
        'Mexican heavy sour crude, important for US Gulf Coast refiners',
        'Chinese domestic benchmark crude from largest oilfield'
    ],
    'Additional_Info': [
        'Primary NYMEX futures contract. Storage hub at Cushing with over 90 million barrels capacity. Key pricing point for US domestic production.',
        'ICE Brent futures are the most widely traded oil contracts globally. Represents output from multiple North Sea fields.',
        'Dubai Mercantile Exchange (DME) futures contract. Key benchmark for Middle Eastern exports to Asia.',
        'Deep water port facility handling VLCCs. Growing importance with US crude exports.',
        'Price reference for Russian oil exports. Traded primarily in Mediterranean and Rotterdam markets.',
        'Premium Nigerian crude grade. Important for gasoline and diesel production.',
        'Key marker for light sweet crude in Asia-Pacific. Trading hub in Singapore.',
        'Trades at discount to WTI. Major grade for Canadian oil sands production.',
        'Largest crude stream from Saudi Arabia. Sets Official Selling Prices (OSPs) for Asian buyers.',
        'DME Oman futures contract. Represents Middle Eastern medium sour crude exports.',
        'Traded primarily in US Gulf Coast. Important feedstock for complex refineries.',
        'Largest Chinese onshore oilfield production. Domestic pricing benchmark.'
    ]
}

# Create DataFrame
df = pd.DataFrame(oil_markets)

# Get unique regions and create options including "All Markets"
unique_regions = sorted(df['Region'].unique())
region_options = [{'label': 'All Markets', 'value': 'ALL'}] + [{'label': region, 'value': region} for region in unique_regions]

# App layout
app.layout = html.Div([
    html.H1('Global Oil Markets Map',
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
    
    html.Div([
        # Region Filter
        html.Div([
            html.Label('Filter by Region:',
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=region_options,
                value='ALL',  # Default to "All Markets"
                multi=True,
                style={'width': '300px'}
            ),
        ], style={'marginRight': '20px', 'display': 'inline-block'}),
        
        # Crude Type Filter
        html.Div([
            html.Label('Filter by Crude Type:',
                      style={'fontSize': '16px', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='type-dropdown',
                options=[{'label': type_, 'value': type_} for type_ in sorted(df['Type'].unique())],
                value=[],
                multi=True,
                style={'width': '300px'}
            ),
        ], style={'display': 'inline-block'}),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Main content container with map and details panel
    html.Div([
        # Left side - Map
        html.Div([
            dcc.Graph(id='oil-market-map',
                     style={'height': '700px'},
                     config={'displayModeBar': True})
        ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        # Right side - Details Panel
        html.Div([
            html.Div([
                html.H3('Market Details', style={'marginBottom': '15px', 'color': '#2c3e50'}),
                html.Div(id='selected-market-details', children=[
                    html.P("Click on a market in the map to see detailed information.",
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
    html.Div(id='market-info',
             style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa',
                    'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
], style={'padding': '20px', 'backgroundColor': 'white'})

@app.callback(
    [Output('oil-market-map', 'figure'),
     Output('market-info', 'children')],
    [Input('region-dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_map(selected_regions, selected_types):
    # Filter data based on selections
    filtered_df = df.copy()
    
    # Handle region filtering
    if selected_regions:
        if 'ALL' not in selected_regions:
            filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    
    # Handle type filtering
    if selected_types:
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_types)]
    
    # Create the map
    fig = px.scatter_mapbox(filtered_df,
                           lat='Latitude',
                           lon='Longitude',
                           hover_name='Market',
                           hover_data=['Type', 'Region'],
                           color='Type',
                           zoom=1.5,
                           center={'lat': 30, 'lon': 0},
                           title='Global Oil Markets')
    
    # Update map layout
    fig.update_layout(
        mapbox_style='carto-positron',
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=700,
        title_x=0.5,
        clickmode='event+select',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255, 255, 255, 0.8)'
        )
    )
    
    # Create information panel content
    info_content = [
        html.H3('Summary Information', style={'marginBottom': '15px'}),
        html.Div([
            html.P(f"Total Markets Shown: {len(filtered_df)}"),
            html.Div([
                html.P("Regions Shown:"),
                html.Ul([
                    html.Li(region) for region in sorted(filtered_df['Region'].unique())
                ]),
                html.P("Crude Types Shown:"),
                html.Ul([
                    html.Li(type_) for type_ in sorted(filtered_df['Type'].unique())
                ])
            ])
        ])
    ]
    
    return fig, info_content

@app.callback(
    Output('selected-market-details', 'children'),
    [Input('oil-market-map', 'clickData')]
)
def display_market_details(clickData):
    if not clickData:
        return [
            html.P("Click on a market in the map to see detailed information.",
                  style={'font-style': 'italic', 'color': '#666'})
        ]
    
    # Get the clicked market's data
    market_name = clickData['points'][0]['hovertext']
    market_data = df[df['Market'] == market_name].iloc[0]
    
    return [
        html.H4(market_data['Market'], style={'color': '#2c3e50', 'marginBottom': '20px'}),
        html.Div([
            html.P('Region:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(market_data['Region'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Crude Type:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(market_data['Type'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Location:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(f"Latitude: {market_data['Latitude']:.4f}°", style={'marginLeft': '20px', 'marginBottom': '5px'}),
            html.P(f"Longitude: {market_data['Longitude']:.4f}°", style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Description:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(market_data['Description'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.P('Additional Information:', style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.P(market_data['Additional_Info'], style={'marginLeft': '20px', 'marginBottom': '15px'}),
            
            html.Hr(style={'marginY': '20px'}),
            
            html.P("Click another market on the map to see its details.",
                  style={'font-style': 'italic', 'color': '#666', 'marginTop': '20px'})
        ], style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px'})
    ]

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12354, debug=True)