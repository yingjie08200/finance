import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

# Sample data (using Plotly's built-in datasets)
df = px.data.tips()
df_stocks = px.data.stocks()

# Sample data for funnel chart
funnel_data = pd.DataFrame({
    'stage': ['Website Visits', 'Downloads', 'Prospects', 'Negotiations', 'Deals'],
    'value': [1000, 750, 500, 250, 100]
})

# Sample data for polar chart
theta = np.linspace(0, 2*np.pi, 8)
r = np.random.rand(8)*5
polar_data = pd.DataFrame({
    'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
    'r': r
})

# Supported chart types
chart_types = [
    'Line',
    'Bar',
    'Scatter',
    'Histogram',
    'Box',
    'Violin',
    'Pie',
    'Heatmap',
    'Density Contour',
    'Sunburst',
    'Strip',
    'Polar',
    'Funnel',
    'Treemap',
    'Parallel Coordinates',
    'Area',
    'Candlestick',
    'Funnel',
    'Choropleth',
    'Scatter Map'
]

# CSS for code formatting
code_style = {
    'backgroundColor': 'white',  # Changed from dark to white background
    'fontFamily': 'Consolas, Monaco, "Andale Mono", monospace',
    'padding': '15px',
    'borderRadius': '6px',
    'overflowX': 'auto',
    'fontSize': '13px',
    'border': '1px solid #ddd',  # Lighter border color
    'marginTop': '10px',
    'whiteSpace': 'pre-wrap',
    'color': '#333',  # Changed from light gray to dark gray text
    'lineHeight': '1.5',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'  # Subtle shadow
}

# CSS for syntax highlighting
syntax_highlight_style = '''
<style>
    .python-code {
        color: #abb2bf;
    }
    .python-code .comment { color: #98c379; }  /* Green */
    .python-code .string { color: #e5c07b; }   /* Yellow */
    .python-code .keyword { color: #c678dd; }   /* Purple */
    .python-code .function { color: #61afef; }  /* Blue */
    .python-code .number { color: #d19a66; }    /* Orange */
    .python-code .import { color: #e06c75; }    /* Red */
</style>
'''

def highlight_python_code(code):
    """Format Python code for display"""
    # Simply return the code as is, without HTML tags
    return code

# CSS for radio items list
radio_style = {
    'maxHeight': '300px',
    'overflowY': 'auto',
    'border': '1px solid #ddd',
    'borderRadius': '4px',
    'padding': '10px',
    'backgroundColor': 'white'
}

radio_item_style = {
    'padding': '8px',
    'margin': '2px 0',
    'cursor': 'pointer',
    'borderRadius': '4px',
    'transition': 'background-color 0.2s'
}

radio_item_checked_style = {
    'backgroundColor': '#e6f3ff',
    'fontWeight': 'bold'
}

# Reference information for each chart type
chart_references = {
    'Line': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.line.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for x-axis
• y: Column name for y-axis
• color: Column name for color encoding
• line_dash: Column name for line dash pattern
• markers: Show markers (boolean)
• line_shape: Line interpolation ('linear', 'spline', etc.)''',
        'use_cases': 'Best for showing trends over time or continuous data sequences.'
    },
    'Bar': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.bar.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for x-axis
• y: Column name for y-axis
• color: Column name for color encoding
• barmode: Bar arrangement ('group', 'stack', 'relative')
• text: Column name for bar text labels''',
        'use_cases': 'Ideal for comparing quantities across categories.'
    },
    'Scatter': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.scatter.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for x-axis
• y: Column name for y-axis
• color: Column name for color encoding
• size: Column name for marker size
• trendline: Add regression line ('ols', 'lowess')
• hover_data: Additional data for hover tooltip''',
        'use_cases': 'Perfect for showing relationships between variables and identifying patterns.'
    },
    'Histogram': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.histogram.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for data distribution
• nbins: Number of histogram bins
• histnorm: Histogram normalization
• cumulative: Show cumulative distribution
• histfunc: Histogram aggregation function''',
        'use_cases': 'Used to visualize data distribution and frequency analysis.'
    },
    'Box': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.box.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for categories
• y: Column name for values
• color: Column name for color encoding
• points: Show individual points ('all', 'outliers', False)
• notched: Show notched box plot
• quartilemethod: Method for computing quartiles''',
        'use_cases': 'Excellent for showing data distribution and identifying outliers across categories.'
    },
    'Violin': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.violin.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for categories
• y: Column name for values
• color: Column name for color encoding
• box: Show inner box plot
• points: Show individual points
• violinmode: Violin arrangement ('group', 'overlay')''',
        'use_cases': 'Shows the distribution shape of data across different categories.'
    },
    'Pie': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.pie.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• values: Column name for sector values
• names: Column name for sector names
• color: Column name for color encoding
• hole: Size of center hole (0-1) for donut chart
• pull: Pull sectors apart''',
        'use_cases': 'Best for showing part-to-whole relationships and composition.'
    },
    'Heatmap': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.density_heatmap.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for x-axis
• y: Column name for y-axis
• z: Column name for values (optional)
• color_continuous_scale: Color scale
• nbinsx/nbinsy: Number of bins''',
        'use_cases': 'Visualize 2D distribution of data points or show correlation patterns.'
    },
    'Density Contour': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.density_contour.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for x-axis
• y: Column name for y-axis
• color_continuous_scale: Color scale
• nbinsx/nbinsy: Number of bins
• histfunc: Aggregation function''',
        'use_cases': 'Shows density of 2D data using contour lines, good for identifying clusters.'
    },
    'Sunburst': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.sunburst.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• path: List of columns for hierarchy levels
• values: Column name for sector sizes
• color: Column name for color encoding
• maxdepth: Maximum depth of hierarchy to show''',
        'use_cases': 'Visualize hierarchical data and show part-to-whole relationships at multiple levels.'
    },
    'Strip': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.strip.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for categories
• y: Column name for values
• color: Column name for color encoding
• hover_data: Additional hover information
• stripmode: Strip arrangement''',
        'use_cases': 'Shows individual data points along categorical axes, good for small to medium datasets.'
    },
    'Polar': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.scatter_polar.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• r: Column name for radial values
• theta: Column name for angular values
• color: Column name for color encoding
• symbol: Column name for marker symbols
• direction: Clock direction ('clockwise', 'counterclockwise')''',
        'use_cases': 'Visualize cyclical data or directional/angular relationships.'
    },
    'Funnel': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.funnel.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for values
• y: Column name for stages
• color: Column name for color encoding
• textinfo: Text display options
• textposition: Position of text labels''',
        'use_cases': 'Visualize sequential data with decreasing values, like sales/conversion funnels.'
    },
    'Treemap': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.treemap.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• path: List of columns for hierarchy levels
• values: Column name for tile sizes
• color: Column name for color encoding
• maxdepth: Maximum depth of hierarchy to show''',
        'use_cases': 'Show hierarchical data as nested rectangles, good for space-filling visualizations.'
    },
    'Parallel Coordinates': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.parallel_coordinates.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• dimensions: List of columns to include
• color: Column name for color encoding
• labelangle: Angle of axis labels
• rangefont: Font settings for range values''',
        'use_cases': 'Explore multivariate data and identify patterns across multiple dimensions.'
    },
    'Area': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.area.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• x: Column name for x-axis
• y: Column name for y-axis
• color: Column name for color encoding
• line_group: Column name for line grouping
• groupnorm: Type of normalization''',
        'use_cases': 'Show cumulative totals over time or compare proportions in a whole.'
    },
    'Candlestick': {
        'doc_url': 'https://plotly.com/python/candlestick-charts/',
        'key_params': '''Key Parameters:
• x: Time/date values
• open: Opening values
• high: High values
• low: Low values
• close: Closing values
• increasing_line_color: Color for increasing periods
• decreasing_line_color: Color for decreasing periods''',
        'use_cases': 'Visualize price movements in financial data, showing open, high, low, and close values.'
    },
    'Choropleth': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• locations: Column name for location IDs
• locationmode: Location ID format
• color: Column name for color values
• scope: Map scope (e.g., 'usa', 'world')
• color_continuous_scale: Color scale for values''',
        'use_cases': 'Visualize geographical data with color-coded regions on a map.'
    },
    'Scatter Map': {
        'doc_url': 'https://plotly.com/python-api-reference/generated/plotly.express.scatter_mapbox.html',
        'key_params': '''Key Parameters:
• data_frame: Input data (pandas DataFrame)
• lat: Column name for latitude values
• lon: Column name for longitude values
• hover_name: Column name for hover title
• hover_data: List of columns for hover tooltip
• color: Column name for color encoding
• zoom: Initial zoom level
• map_style: Map style ('open-street-map', 'carto-positron', etc.)''',
        'use_cases': 'Visualize geographical point data on an interactive map.'
    }
}

# Default reference for unsupported chart types
default_reference = {
    'doc_url': 'https://plotly.com/python/plotly-express/',
    'key_params': '''General Parameters:
• data_frame: Input data (pandas DataFrame)
• title: Chart title
• labels: Axis and legend labels
• color: Color encoding
• hover_data: Additional hover information''',
    'use_cases': 'Refer to the Plotly Express documentation for specific use cases.'
}

app.layout = html.Div(
    style={'display': 'flex'},
    children=[
        # Control panel (left side)
        html.Div(
            style={
                'width': '30%',
                'padding': '20px',
                'background': '#f8f9fa',
                'overflowY': 'auto',
                'height': '100vh',
                'borderRight': '1px solid #eee'  # Moved border to right side
            },
            children=[
                html.H3("Chart Controls", style={'textAlign': 'center'}),
                html.Label("Select Chart Type:", style={'margin': '15px 0', 'display': 'block'}),
                dcc.RadioItems(
                    id='chart-type',
                    options=[{'label': ct, 'value': ct} for ct in chart_types],
                    value='Scatter',
                    style=radio_style,
                    inputStyle={'marginRight': '10px'},
                    labelStyle=radio_item_style,
                    className='radio-items'
                ),
                # Add histogram toggle switch (will be shown only for heatmap)
                html.Div(
                    id='histogram-toggle-container',
                    style={'display': 'none', 'margin': '15px 0'},
                    children=[
                        html.Label("Show Histograms:", style={'marginRight': '10px'}),
                        dcc.Checklist(
                            id='show-histograms',
                            options=[{'label': '', 'value': True}],
                            value=[True],
                            style={'display': 'inline-block'}
                        )
                    ]
                ),
                html.Div(id='chart-description', style={'margin': '20px 0'}),
                
                # Code example section with syntax highlighting
                html.Div([
                    html.H4("Code Example:", style={'marginBottom': '10px'}),
                    html.Div([
                        dcc.Markdown(
                            id='code-example',
                            style={
                                'backgroundColor': 'white',
                                'color': '#333',
                                'padding': '15px',
                                'borderRadius': '6px',
                                'fontFamily': 'Consolas, Monaco, "Andale Mono", monospace',
                                'fontSize': '13px',
                                'whiteSpace': 'pre-wrap',
                                'border': '1px solid #ddd',
                                'marginTop': '10px',
                                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
                            }
                        )
                    ])
                ], style={'marginTop': '30px'}),

                # Reference section
                html.Div([
                    html.H4("Reference:", style={'marginBottom': '10px', 'marginTop': '30px'}),
                    html.A(
                        "Official Documentation",
                        id='doc-link',
                        target='_blank',
                        style={'display': 'block', 'marginBottom': '10px'}
                    ),
                    html.Div([
                        html.H5("Key Parameters:", style={'marginBottom': '5px'}),
                        html.Div(id='key-params', style=code_style)
                    ]),
                    html.Div([
                        html.H5("Common Use Cases:", style={'marginBottom': '5px', 'marginTop': '10px'}),
                        html.Div(id='use-cases', style={'fontStyle': 'italic'})
                    ])
                ])
            ]
        ),
        
        # Main content area (right side)
        html.Div(
            style={
                'width': '70%',
                'padding': '20px'
            },
            children=[
                dcc.Graph(id='graph-output')
            ]
        )
    ]
)

# Add custom CSS for hover effect
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Plotly Express Chart Gallery</title>
        <style>
            .radio-items label:hover {
                background-color: #f0f0f0;
            }
            .radio-items input[type="radio"]:checked + label {
                background-color: #e6f3ff;
                font-weight: bold;
            }
            .python-code {
                color: #abb2bf;
            }
            .python-code .comment { color: #98c379; }  /* Green */
            .python-code .string { color: #e5c07b; }   /* Yellow */
            .python-code .keyword { color: #c678dd; }   /* Purple */
            .python-code .function { color: #61afef; }  /* Blue */
            .python-code .number { color: #d19a66; }    /* Orange */
            .python-code .import { color: #e06c75; }    /* Red */
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Add callback to show/hide histogram toggle
@app.callback(
    Output('histogram-toggle-container', 'style'),
    [Input('chart-type', 'value')]
)
def toggle_histogram_control(chart_type):
    if chart_type == 'Heatmap':
        return {'display': 'block', 'margin': '15px 0'}
    return {'display': 'none'}

@app.callback(
    [Output('graph-output', 'figure'),
     Output('chart-description', 'children'),
     Output('code-example', 'children'),
     Output('doc-link', 'href'),
     Output('key-params', 'children'),
     Output('use-cases', 'children')],
    [Input('chart-type', 'value'),
     Input('show-histograms', 'value')]
)
def update_graph(chart_type, show_histograms):
    title = f"{chart_type} Chart Demo"
    description = ""
    code_example = ""
    
    # Get reference information
    ref = chart_references.get(chart_type, default_reference)
    doc_url = ref['doc_url']
    key_params = ref['key_params']
    use_cases = ref['use_cases']

    if chart_type == 'Line':
        fig = px.line(df, x='day', y='total_bill', color='sex',
                     title=title,
                     labels={'total_bill': 'Total Bill ($)', 'day': 'Day of Week'})
        description = "Shows daily total bills by gender."
        code_example = """# Line chart example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create line chart
fig = px.line(
    df, 
    x='day', 
    y='total_bill', 
    color='sex',
    title='Line Chart Demo',
    labels={'total_bill': 'Total Bill ($)', 'day': 'Day of Week'}
)

fig.show()  # Display the figure"""

    elif chart_type == 'Bar':
        fig = px.bar(df, x='day', y='tip', color='sex', barmode='group',
                    title=title,
                    labels={'tip': 'Tip Amount ($)'})
        description = "Compares tip amounts by day and gender."
        code_example = """# Bar chart example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create bar chart
fig = px.bar(
    df, 
    x='day', 
    y='tip', 
    color='sex', 
    barmode='group',
    title='Bar Chart Demo',
    labels={'tip': 'Tip Amount ($)'}
)

fig.show()  # Display the figure"""

    elif chart_type == 'Scatter':
        fig = px.scatter(df, x='total_bill', y='tip', color='sex',
                        trendline='ols',
                        title=title,
                        labels={'total_bill': 'Total Bill ($)', 'tip': 'Tip Amount ($)'},
                        hover_data=['size', 'time'])
        description = "Shows relationship between bill and tip with regression line, colored by gender."
        code_example = """# Scatter plot example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create scatter plot with trendline
fig = px.scatter(
    df, 
    x='total_bill', 
    y='tip', 
    color='sex',
    trendline='ols',
    title='Scatter Plot Demo',
    labels={'total_bill': 'Total Bill ($)', 'tip': 'Tip Amount ($)'},
    hover_data=['size', 'time']
)

fig.show()  # Display the figure"""

    elif chart_type == 'Histogram':
        fig = px.histogram(df, x='total_bill', color='sex', nbins=30,
                          title=title,
                          labels={'total_bill': 'Total Bill ($)'})
        description = "Distribution of total bill amounts."
        code_example = """# Histogram example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create histogram
fig = px.histogram(
    df, 
    x='total_bill', 
    color='sex', 
    nbins=30,
    title='Histogram Demo',
    labels={'total_bill': 'Total Bill ($)'}
)

fig.show()  # Display the figure"""

    elif chart_type == 'Box':
        fig = px.box(df, x='day', y='tip', color='sex', points='all',
                    title=title,
                    labels={'tip': 'Tip Amount ($)'})
        description = "Box plot showing tip distributions by day and gender."
        code_example = """# Box plot example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create box plot
fig = px.box(
    df, 
    x='day', 
    y='tip', 
    color='sex', 
    points='all',
    title='Box Plot Demo',
    labels={'tip': 'Tip Amount ($)'}
)

fig.show()  # Display the figure"""

    elif chart_type == 'Violin':
        fig = px.violin(df, x='day', y='tip', color='sex', box=True,
                       title=title,
                       labels={'tip': 'Tip Amount ($)'})
        description = "Violin plot with embedded box plots."
        code_example = """# Violin plot example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create violin plot
fig = px.violin(
    df, 
    x='day', 
    y='tip', 
    color='sex', 
    box=True,
    title='Violin Plot Demo',
    labels={'tip': 'Tip Amount ($)'}
)

fig.show()  # Display the figure"""

    elif chart_type == 'Pie':
        pie_df = df.groupby('day').size().reset_index(name='counts')
        fig = px.pie(pie_df, values='counts', names='day',
                    title=title, hole=0.3)
        description = "Distribution of data points by day (donut style)."
        code_example = """# Pie chart example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset
pie_df = df.groupby('day').size().reset_index(name='counts')

# Create pie chart (donut style)
fig = px.pie(
    pie_df, 
    values='counts', 
    names='day',
    title='Pie Chart Demo', 
    hole=0.3
)

fig.show()  # Display the figure"""

    elif chart_type == 'Heatmap':
        # Create heatmap with optional histograms
        marginal_x = "histogram" if show_histograms and True in show_histograms else None
        marginal_y = "histogram" if show_histograms and True in show_histograms else None
        
        fig = px.density_heatmap(df, x='total_bill', y='tip',
                                title=title,
                                labels={'total_bill': 'Total Bill ($)'},
                                text_auto=True,  # Show count numbers
                                marginal_x=marginal_x,  # Add histogram on x-axis if enabled
                                marginal_y=marginal_y)  # Add histogram on y-axis if enabled
        description = "Density heatmap of bill and tip correlations with count labels."
        code_example = f"""# Heatmap example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create density heatmap
fig = px.density_heatmap(
    df, 
    x='total_bill', 
    y='tip',
    title='Heatmap Demo',
    labels={{'total_bill': 'Total Bill ($)'}},
    text_auto=True,  # Show count numbers
    marginal_x="{marginal_x}",  # Add histogram on x-axis
    marginal_y="{marginal_y}"  # Add histogram on y-axis
)

fig.show()  # Display the figure"""

    elif chart_type == 'Density Contour':
        fig = px.density_contour(df, x='total_bill', y='tip',
                                title=title,
                                labels={'total_bill': 'Total Bill ($)'})
        description = "Contour lines showing data density."
        code_example = """# Density contour example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create density contour plot
fig = px.density_contour(
    df, 
    x='total_bill', 
    y='tip',
    title='Density Contour Demo',
    labels={'total_bill': 'Total Bill ($)'}
)

fig.show()  # Display the figure"""

    elif chart_type == 'Sunburst':
        fig = px.sunburst(df, path=['day', 'sex'], values='tip',
                         title=title,
                         color='sex')
        description = "Hierarchical visualization of tip amounts by day and gender."
        code_example = """# Sunburst chart example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create sunburst chart
fig = px.sunburst(
    df, 
    path=['day', 'sex'], 
    values='tip',
    title='Sunburst Chart Demo',
    color='sex'
)

fig.show()  # Display the figure"""

    elif chart_type == 'Strip':
        fig = px.strip(df, x='day', y='tip', color='sex',
                      title=title,
                      labels={'tip': 'Tip Amount ($)'},
                      hover_data=['total_bill', 'size'])
        description = "Strip plot showing individual tip values by day and gender."
        code_example = """# Strip plot example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create strip plot
fig = px.strip(
    df, 
    x='day', 
    y='tip', 
    color='sex',
    title='Strip Plot Demo',
    labels={'tip': 'Tip Amount ($)'},
    hover_data=['total_bill', 'size']
)

fig.show()  # Display the figure"""

    elif chart_type == 'Polar':
        fig = px.scatter_polar(polar_data, r='r', theta='theta',
                             title=title)
        description = "Polar chart showing directional data distribution."
        code_example = """# Polar chart example
import plotly.express as px
import numpy as np
import pandas as pd

# Generate sample data
theta = np.linspace(0, 2*np.pi, 8)
r = np.random.rand(8)*5
polar_data = pd.DataFrame({
    'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
    'r': r
})

# Create polar chart
fig = px.scatter_polar(
    polar_data, 
    r='r', 
    theta='theta',
    title='Polar Chart Demo'
)

fig.show()  # Display the figure"""

    elif chart_type == 'Funnel':
        fig = px.funnel(funnel_data, x='value', y='stage',
                       title=title)
        description = "Funnel chart showing conversion stages."
        code_example = """# Funnel chart example
import plotly.express as px
import pandas as pd

# Create sample data
funnel_data = pd.DataFrame({
    'stage': ['Website Visits', 'Downloads', 'Prospects', 'Negotiations', 'Deals'],
    'value': [1000, 750, 500, 250, 100]
})

# Create funnel chart
fig = px.funnel(
    funnel_data, 
    x='value', 
    y='stage',
    title='Funnel Chart Demo'
)

fig.show()  # Display the figure"""

    elif chart_type == 'Treemap':
        fig = px.treemap(df, path=[px.Constant("all"), 'day', 'sex'],
                        values='total_bill',
                        title=title)
        description = "Treemap showing bill distribution by day and gender."
        code_example = """# Treemap example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create treemap
fig = px.treemap(
    df, 
    path=[px.Constant("all"), 'day', 'sex'],
    values='total_bill',
    title='Treemap Demo'
)

fig.show()  # Display the figure"""

    elif chart_type == 'Parallel Coordinates':
        fig = px.parallel_coordinates(df, 
                                    dimensions=['total_bill', 'tip', 'size'],
                                    color='day',
                                    title=title)
        description = "Parallel coordinates showing relationships between numerical variables."
        code_example = """# Parallel coordinates example
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create parallel coordinates plot
fig = px.parallel_coordinates(
    df, 
    dimensions=['total_bill', 'tip', 'size'],
    color='day',
    title='Parallel Coordinates Demo'
)

fig.show()  # Display the figure"""

    elif chart_type == 'Area':
        # Reshape the stock data for area plot
        df_stocks_melted = df_stocks.melt(
            id_vars=['date'],
            value_vars=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
            var_name='company',
            value_name='price'
        )
        fig = px.area(df_stocks_melted, 
                     x='date', 
                     y='price',
                     color='company',
                     title=title,
                     labels={'price': 'Stock Price ($)', 'date': 'Date', 'company': 'Company'})
        description = "Area chart showing stock prices over time for different companies."
        code_example = """# Area chart example
import plotly.express as px
import pandas as pd

# Sample data
df_stocks = px.data.stocks()  # Plotly's built-in dataset

# Reshape the data from wide to long format
df_stocks_melted = df_stocks.melt(
    id_vars=['date'],
    value_vars=['GOOG', 'AAPL', 'AMZN', 'FB', 'NFLX', 'MSFT'],
    var_name='company',
    value_name='price'
)

# Create area chart
fig = px.area(
    df_stocks_melted, 
    x='date', 
    y='price',
    color='company',
    title='Area Chart Demo',
    labels={'price': 'Stock Price ($)', 'date': 'Date', 'company': 'Company'}
)

fig.show()  # Display the figure"""

    elif chart_type == 'Candlestick':
        # For candlestick, we'll create placeholder data since px doesn't have a direct candlestick function
        description = "Candlestick charts require plotly.graph_objects instead of plotly.express"
        code_example = """# Candlestick chart example
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)
dates = pd.date_range('20200101', periods=20)
data = pd.DataFrame({
    'Date': dates,
    'Open': np.random.normal(100, 5, 20),
    'High': None,
    'Low': None,
    'Close': None
})

# Populate High, Low, Close based on Open
for i in range(len(data)):
    data.loc[i, 'Close'] = data.loc[i, 'Open'] * (1 + np.random.normal(0, 0.02))
    data.loc[i, 'High'] = max(data.loc[i, 'Open'], data.loc[i, 'Close']) * (1 + abs(np.random.normal(0, 0.01)))
    data.loc[i, 'Low'] = min(data.loc[i, 'Open'], data.loc[i, 'Close']) * (1 - abs(np.random.normal(0, 0.01)))

# Create candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=data['Date'],
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
)])

fig.update_layout(title='Candlestick Chart Demo', xaxis_title='Date', yaxis_title='Price')
fig.show()  # Display the figure"""
        # Create a placeholder figure since we don't have real candlestick data
        import plotly.graph_objects as go
        dates = pd.date_range('20200101', periods=20)
        np.random.seed(42) 
        open_prices = np.random.normal(100, 5, 20)
        close_prices = [op * (1 + np.random.normal(0, 0.02)) for op in open_prices]
        high_prices = [max(o, c) * (1 + abs(np.random.normal(0, 0.01))) for o, c in zip(open_prices, close_prices)]
        low_prices = [min(o, c) * (1 - abs(np.random.normal(0, 0.01))) for o, c in zip(open_prices, close_prices)]
        fig = go.Figure(data=[go.Candlestick(
            x=dates,
            open=open_prices,
            high=high_prices,
            low=low_prices,
            close=close_prices
        )])
        fig.update_layout(title=title)

    elif chart_type == 'Choropleth':
        # Create a simple choropleth map with US states
        us_data = pd.DataFrame({
            'state': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                     'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                     'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                     'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                     'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
            'value': np.random.randint(10, 100, 50)
        })
        fig = px.choropleth(us_data, 
                         locations='state', 
                         locationmode="USA-states", 
                         scope="usa",
                         color='value',
                         color_continuous_scale="Viridis",
                         title=title)
        description = "Choropleth map showing data by US state."
        code_example = """# Choropleth map example
import plotly.express as px
import pandas as pd
import numpy as np

# Create sample data for US states
us_data = pd.DataFrame({
    'state': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
             'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
             'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
             'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
             'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
    'value': np.random.randint(10, 100, 50)  # Random values for demonstration
})

# Create choropleth map
fig = px.choropleth(
    us_data, 
    locations='state', 
    locationmode="USA-states", 
    scope="usa",
    color='value',
    color_continuous_scale="Viridis",
    title='Choropleth Map Demo'
)

fig.show()  # Display the figure"""

    elif chart_type == 'Scatter Map':
        # Load US cities data
        us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
        
        fig = px.scatter_mapbox(us_cities, 
                              lat="lat", 
                              lon="lon", 
                              hover_name="City", 
                              hover_data=["State", "Population"],
                              color_discrete_sequence=["fuchsia"], 
                              zoom=3)
        
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":30,"l":0,"b":0},  # Added small top margin for title
            title=title
        )
        
        description = "Interactive map showing top 1000 US cities with population data."
        code_example = """# Scatter Map example
import plotly.express as px
import pandas as pd

# Load US cities data
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

# Create scatter map
fig = px.scatter_mapbox(
    us_cities, 
    lat="lat", 
    lon="lon", 
    hover_name="City", 
    hover_data=["State", "Population"],
    color_discrete_sequence=["fuchsia"], 
    zoom=3
)

# Update layout
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0}
)

fig.show()  # Display the figure"""

    else:
        fig = px.scatter(df, x='total_bill', y='tip', title='Default Plot')
        description = "Default scatter plot between bill and tip."
        code_example = """# Default scatter plot
import plotly.express as px

# Sample data
df = px.data.tips()  # Plotly's built-in dataset

# Create scatter plot
fig = px.scatter(
    df, 
    x='total_bill', 
    y='tip',
    title='Default Plot'
)

fig.show()  # Display the figure"""

    # Format code example for markdown display
    code_example = f"```python\n{code_example}\n```"
    
    return fig, description, code_example, doc_url, key_params, use_cases

if __name__ == '__main__':
    app.run(debug=True, port=12345)