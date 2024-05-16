import dash, dash.dependencies as dd
import pandas as pd
from datetime import datetime

import plotly.subplots as sp, plotly.express as px, plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html, callback
from dash.dependencies import Input, Output

################### READING DATA ###################
df = pd.read_csv(r"Z:\Data\RIDERSHIP\RidershipData.csv")
# df = pd.read_csv(r"RidershipData.csv")

date_format = '%Y/%m/%d'
df['Day'] = pd.to_datetime(df['Day'], format=date_format)

# Define the order of days of the week in chronological order
days_of_week_order = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]

################### DASH APP ###################
dash.register_page(__name__)

layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='riders-selector',
            options=[
                {'label': 'Riders On', 'value': 'Riders On'},
                {'label': 'Riders Off', 'value': 'Riders Off'}
            ],
            value='Riders On',
            style={'width': '75%', 'display': 'inline-block', 'font-family': 'Segoe UI'}),
        dcc.Dropdown(
            id='route-selector',
            options=[
                {'label': route, 'value': route} for route in df['Route'].unique()
            ],
            multi=False,
            value='Waltham Shuttle',
            style={'width': '75%', 'display': 'inline-block','font-family': 'Segoe UI'}),
        dcc.Dropdown(
            id='aggregation-selector',
            options=[
                {'label': 'Sum', 'value': 'sum'},
                {'label': 'Average', 'value': 'avg'}
            ],
            value='sum',
            style={'width': '75%', 'display': 'inline-block', 'font-family': 'Segoe UI'}),
        dcc.DatePickerRange(
            id='date-slider',
            start_date=df['Day'].min(),
            end_date=df['Day'].max(),
            style={'width': '75%', 'display': 'inline-block', 'font-family': 'Segoe UI'}
        ),
    ], style={'display': 'flex'}),

    # TOP/BOTTOM 5 STOPS SUM
    dcc.Graph(id='top-5-bar-chart', style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(id='bottom-5-bar-chart', style={'width': '48%', 'display': 'inline-block'}),

    #TOP/BOTTOM 5 STOPS BY DAY OF WEEK
    dcc.Graph(id='top-stops-graph'),
    dcc.Graph(id='bottom-stops-graph')
])

###### TOP/BOTTOM 5 OVERALL ######
@callback(
    Output('top-5-bar-chart', 'figure'),
    [Input('route-selector', 'value'),
     Input('date-slider', 'start_date'),
     Input('date-slider', 'end_date'),
     Input('riders-selector', 'value')]
)
def update_top_5_chart(selected_route, start_date, end_date, selected_riders):
    filtered_df = df[(df['Route'] == selected_route) &
                     (df['Day'] >= start_date) &
                     (df['Day'] <= end_date)]
    
    sorted_df = filtered_df.groupby(['Stop'])[selected_riders].sum().sort_values(ascending=False).head(5)
    
    title = f'Top 5 Stops by {selected_riders} for Route {selected_route}'
    fig = px.bar(sorted_df, x=selected_riders, y=sorted_df.index, title=title, color_discrete_sequence=['green'], text_auto=True, orientation='h')  # Set orientation to 'h' for horizontal bars
    return fig

@callback(
    Output('bottom-5-bar-chart', 'figure'),
    [Input('route-selector', 'value'),
     Input('date-slider', 'start_date'),
     Input('date-slider', 'end_date'),
     Input('riders-selector', 'value')]
)
def update_bottom_5_chart(selected_route, start_date, end_date, selected_riders):
    filtered_df = df[(df['Route'] == selected_route) &
                     (df['Day'] >= start_date) &
                     (df['Day'] <= end_date)]
    
    sorted_df = filtered_df.groupby(['Stop'])[selected_riders].sum().sort_values().head(5)
    
    title = f'Bottom 5 Stops by {selected_riders} for Route {selected_route}'
    fig = px.bar(sorted_df, x=selected_riders, y=sorted_df.index, title=title, color_discrete_sequence=['red'], text_auto=True, orientation='h')  # Set orientation to 'h' for horizontal bars
    return fig

###### TOP/BOTTOM 5 BY DAY OF WEEK ######
@callback(
    [Output('top-stops-graph', 'figure'), Output('bottom-stops-graph', 'figure')],
    [Input('riders-selector', 'value'), Input('route-selector', 'value'), Input('aggregation-selector', 'value'),
     Input('date-slider', 'start_date'), Input('date-slider', 'end_date')]
)
def update_graphs(riders_option, selected_route, aggregation_option, start_date, end_date):
    filtered_df = df[(df['Route'] == selected_route) & (df['Day'] >= start_date) & (df['Day'] <= end_date)]

    if aggregation_option == 'sum':
        grouped_df = filtered_df.groupby(['Stop', 'Day Of Week'])[riders_option].sum().reset_index()
    else:
        grouped_df = filtered_df.groupby(['Stop', 'Day Of Week'])[riders_option].mean().reset_index()

    # Get the top 5 stops with the all-time highest Riders On/Off
    top_stops = grouped_df.groupby('Stop')[riders_option].sum().nlargest(5).index
    bottom_stops = grouped_df.groupby('Stop')[riders_option].sum().nsmallest(5).index

    # Create DataFrames to store daily data for top and bottom stops
    top_daily_data = grouped_df[grouped_df['Stop'].isin(top_stops)]
    bottom_daily_data = grouped_df[grouped_df['Stop'].isin(bottom_stops)]

    # Create a color mapping for stops
    color_mapping = {}
    common_stops = set(top_stops).intersection(bottom_stops)
    for stop in common_stops:
        color_mapping[stop] = px.colors.qualitative.Plotly[len(color_mapping) % len(px.colors.qualitative.Plotly)]

    # Create clustered vertical bar charts for the top and bottom stops with common color mapping
    fig_top = px.bar(top_daily_data, 
                     x='Day Of Week', 
                     y=riders_option, 
                     color='Stop',
                     title=f'Highest 5 Stops for {riders_option} by Day of Week', 
                     barmode='group',
                     color_discrete_map=color_mapping,
                     text_auto=True)  # Updated title and color mapping
    fig_bottom = px.bar(bottom_daily_data, 
                        x='Day Of Week', 
                        y=riders_option, color='Stop',
                        title=f'Lowest 5 Stops for {riders_option} by Day of Week', 
                        barmode='group',
                        color_discrete_map=color_mapping,
                        text_auto=True)  # Updated title and color mapping

    # Sort days of the week in chronological order
    fig_top.update_xaxes(categoryorder='array', categoryarray=days_of_week_order)
    fig_bottom.update_xaxes(categoryorder='array', categoryarray=days_of_week_order)
    
    return fig_top, fig_bottom