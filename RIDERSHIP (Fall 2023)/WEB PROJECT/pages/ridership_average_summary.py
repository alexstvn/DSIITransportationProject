import dash, dash.dependencies as dd
import pandas as pd
from datetime import datetime
import os
import plotly.subplots as sp, plotly.express as px, plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html, callback
from dash.dependencies import Input, Output

################### READING DATA ###################
# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the full path to the CSV file
file_path = os.path.join(script_dir, '..','..', 'InputData', 'RidershipData.csv')

# Read the CSV file
df = pd.read_csv(file_path)

################### MODIFY DATA ###################
#removing cancelled trips, skipped/waiting stops (bc no riders getting on)
df.drop(df[df['Ride State'] == 'Cancelled'].index, inplace = True)
df.drop(df[df['Stop State'] == 'Skipped'].index, inplace = True)
df.drop(df[df['Stop State'] == 'Awaiting'].index, inplace = True)

# converting to datetime
date_format = '%Y/%m/%d'
df['Day'] = pd.to_datetime(df['Day'], format=date_format)

#trimming to include time only
ind = df.iloc[0]['Scheduled Time'].find(" ")
df['Scheduled Time'] = df['Scheduled Time'].str[ind+1:]

ind = df.iloc[0]['Actual Arrival'].find(" ")
df['Actual Arrival'] = df['Actual Arrival'].str[ind+1:]

time_format = "%H:%M:%S"
df['Scheduled Time'] = pd.to_datetime(df['Scheduled Time'], format=time_format).dt.time


################### DASH APP ###################
# DELETE WHEN DEBUGGED
dash.register_page(__name__)

#Layout
layout = html.Div([
    html.H1("Average Riders On and Off by Scheduled Time",
        style = {'font-family': 'Segoe UI', 'padding': '0 2em'}),
    
    # DROPDOWN MENU
    html.Div([
        # ROUTE DROPDOWN
        html.Div([
            dcc.Dropdown(
                id="route-selector",
                options=[{'label': route, 'value': route} for route in df['Route'].unique()],
                value=df['Route'].unique()[0],
                style = {'font-family': 'Segoe UI', 'padding': '0 2em'}
            ),
            dcc.Dropdown(
                id='stop-selector',
                options=[],  # Initialize with an empty list
                value=[],
                multi=True,
                style={'max-height': '95px', 'overflow-y': 'auto','font-family': 'Segoe UI', 'padding-left': '2em'}
        )], style={'width': '75%'}),

        # DATE SLICER SLIDER
        html.Div([
            dcc.DatePickerRange(
                id='date-slider',
                start_date=df['Day'].min(),
                end_date=df['Day'].max(),
                display_format='YYYY-MM-DD',
                style = {'font-family': 'Segoe UI', 'padding': '0 2em'}
            )
        ], style={'width': '75%'})
    ], style={'display': 'flex'}),
    
    # AVERAGE STOP RIDERSHIP GRAPH
    dcc.Graph(id='stop-bar-chart'),

    # STOP DROPDOWN - Empty initially, to be populated based on route selection
        html.Div([
            html.Label("\nSelect Stop:",
                style = {'font-family': 'Segoe UI', 'padding': '0 2em'}),
            dcc.Dropdown(
                id="stop-dropdown",
                options=[],
                value='Admissions',
                style = {'font-family': 'Segoe UI', 'padding': '0 2em'}
            ),
        ], style={'width': '75%'}),
    dcc.Graph(id="ridership-time-graph",
        style = {'font-family': 'Segoe UI', 'padding': '0 2em'})
])

# Callback to update the stop-selector options and initial value based on the selected route
@callback(
    [Output('stop-selector', 'options'),
     Output('stop-selector', 'value')],  # Set the initial value of stop-selector
    Input('route-selector', 'value')
)
def update_stop_selector_options(selected_route):
    # Filter stops based on the selected route
    stops_for_route = df[df['Route'] == selected_route]['Stop'].unique()
    stop_options = [{'label': stop, 'value': stop} for stop in stops_for_route]
    return stop_options, stops_for_route  # Set the initial value

#RIDERSHIP BY STOP
@callback(
    Output('stop-bar-chart', 'figure'),
    [Input('route-selector', 'value'),
     Input('date-slider', 'start_date'),
     Input('date-slider', 'end_date'),
     Input('stop-selector', 'value')]
)
def update_stop_chart(selected_route, start_date, end_date, selected_stops):
    filtered_df = df[(df['Route'] == selected_route) & (df['Stop'].isin(selected_stops))]
    
    avg_stop_data = filtered_df.groupby('Stop')[['Riders On', 'Riders Off']].mean().reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Riders On', x=avg_stop_data['Stop'], y=avg_stop_data['Riders On']),
        go.Bar(name='Riders Off', x=avg_stop_data['Stop'], y=avg_stop_data['Riders Off'])
    ])
    
    fig.update_layout(barmode='group', title=f'Average Riders On and Off at Stops for Route {selected_route}')
    return fig

#FOR RIDERSHIP BY SCHEDULED TIME
@callback(
    Output("stop-dropdown", "options"),
    Input("route-selector", "value")
)
def update_stop_options(selected_route):
    if selected_route is None:
        # Handle the case when no route is selected
        return []
    
    stop_options = [{'label': stop, 'value': stop} for stop in df[df['Route'] == selected_route]['Stop'].unique()]
    return stop_options

@callback(
    Output("ridership-time-graph", "figure"),
    [Input("stop-dropdown", "value"), 
     Input("route-selector", "value"),
     Input("date-slider", "start_date"), Input("date-slider", "end_date")]
)
def update_graph(selected_stop, selected_route, start_date, end_date):
    filtered_data = df[(df['Stop'] == selected_stop) & (df['Route'] == selected_route)
                      & (df['Day'] >= start_date) & (df['Day'] <= end_date)]
    avg_riders = filtered_data.groupby('Scheduled Time')[['Riders On', 'Riders Off']].mean().reset_index()
    
#     fig = make_subplots()
#     fig.add_trace(go.Bar(x=avg_riders['Scheduled Time'], y=avg_riders['Riders On']))
    
    fig = go.Figure(data=[
        go.Bar(x=avg_riders['Scheduled Time'], y=avg_riders['Riders On'], name='Riders On'),
        go.Bar(x=avg_riders['Scheduled Time'], y=avg_riders['Riders Off'], name='Riders Off')
    ])
    
    fig.update_layout(barmode='stack',
                      title=f"Average Riders On/Off for Stop: {selected_stop}, Route: {selected_route}",
                      xaxis_title="Scheduled Time",
                      yaxis_title="Average Riders On/Off",
                      font=dict(family='Segoe UI', size=12, color='black'))
    
    return fig