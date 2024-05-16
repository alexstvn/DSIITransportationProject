import dash, dash.dependencies as dd
import pandas as pd
from datetime import datetime

import plotly.subplots as sp, plotly.express as px, plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html, callback
from dash.dependencies import Input, Output

pd.options.mode.chained_assignment = None  # default='warn'

################### READING DATA ###################
df = pd.read_csv(r"Z:\Data\RIDERSHIP\Spring24_RidershipData.csv")
# df = pd.read_csv(r"RidershipData.csv")

columns_to_remove = ['Actual Arrival', 'Actual Departure', 'Riders On', 'Riders Off', 'Riders Left']
df = df.drop(columns=columns_to_remove)

#convert to datetime
df['Scheduled Date/Time'] = pd.to_datetime(df['Scheduled Time'], format='%Y-%m-%d %H:%M:%S')
df['Scheduled Hour'] = pd.to_datetime(df['Scheduled Time']).dt.strftime('%H:%M')

#make 'Capacity Reached' Column
df['Capacity Reached'] = (df['Riders Cumulative'] / df['Vehicle Capacity']) * 100

# Define a custom sorting order for 'Day Of Week'
custom_day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Use the custom sorting order to sort the DataFrame
df['Day Of Week'] = pd.Categorical(df['Day Of Week'], categories=custom_day_order, ordered=True)
df = df.sort_values('Day Of Week')

# Default values for Min and Max
default_min_value = 95
default_max_value = 100

################### DASH APP ###################
dash.register_page(__name__)

#App Layout
layout = html.Div([
    html.H1("Frequency of Vehicle Capacity Being Reached",
        style = {'font-family': 'Segoe UI', 'padding': '0 0.5em'}),
    # DEFAULT FILTERS
    html.Div([
        dcc.Dropdown(
            id='route-dropdown',
            options=[{'label': route, 'value': route} for route in df['Route'].unique()],
            value=df['Route'].unique()[1],
            style={'font-family': 'Segoe UI', 'width': '50%', 'display': 'inline-block'}
        ),
        dcc.DatePickerRange(
            id='date-picker-range',
            display_format='dd, MM-DD-YYYY',
            start_date=df['Scheduled Date/Time'].min(),
            end_date=df['Scheduled Date/Time'].max(),
            style={'font-family': 'Segoe UI', 'font-size': '16px', 'width': '50%', 'display': 'inline-block'}
        ),
    ], style={'align-items': 'center', 'width': '100%'}),

    # MINIMUM/MAXIMUM PERCENTAGE OF CAPACITY REACHED
    html.Label("Select Minimum and Maximum Percentage (0-100):",
                style={'font-family': 'Segoe UI', 'padding': '0 2em'}),
    html.Div([
        dcc.RangeSlider(
            id='capacity-range-slider',
            min=0,
            max=100,
            step=1,  # Allow selection by 1
            value=[95, 100],  # Default selection
            marks={i: str(i) if i % 5 == 0 else '' for i in range(0, 101)},  # Show marks at every 5
            tooltip={'placement': 'bottom', 'always_visible': True}
        ),
        html.Div(id='output-container-range-slider')

    ]),

    #CAPACITY REACHED BY DAY
    dcc.Graph(id='capacity-stop-reached'),
    
    # CAPACITY REACHED BY TIME
    dcc.Dropdown(
        id='day-of-week-dropdown',
        style={'font-family': 'Segoe UI', 'font-size': '16px', 'width': '50%'}
    ),
    dcc.Graph(id='hourly-capacity-reached'),
], style={'padding': '1em'})

# Create a callback to dynamically update 'Day Of Week' dropdown options based on the selected route
@callback(
    dd.Output('day-of-week-dropdown', 'options'),
    dd.Output('day-of-week-dropdown', 'value'),  # Set the default value
    dd.Input('route-dropdown', 'value')
)
def update_day_of_week_options(selected_route):
    days_of_week = []
    if selected_route is None:
        # If no route is selected, use all days_of_week options and set the default to the first option
        options = [{'label': day, 'value': day} for day in days_of_week]
        default_value = days_of_week[0]
    else:
        # Filter the days_of_week based on the selected route's data
        available_days = df[df['Route'] == selected_route]['Day Of Week'].unique()
        options = [{'label': day, 'value': day} for day in available_days]
        default_value = available_days[0] if available_days else None  # Set the default to the first available day

    return options, default_value

# Callback to update the bar chart
@callback(
    Output('capacity-stop-reached', 'figure'),
    [Input('route-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('capacity-range-slider', 'value')]  # Use the range slider value
)
def update_capacity_stop_reached(selected_route, start_date, end_date, capacity_range):
    min_value, max_value = capacity_range

    filtered_df = df[(df['Route'] == selected_route) &
                     (df['Scheduled Date/Time'] >= start_date) &
                     (df['Scheduled Date/Time'] <= end_date) &
                     (df['Capacity Reached'] >= min_value) &
                     (df['Capacity Reached'] <= max_value)]

    # Group the filtered data by 'Day Of Week' and 'Vehicle Capacity' and count the rows
    grouped_df = filtered_df.groupby(['Day Of Week', 'Vehicle Capacity']).size().reset_index(name='Count')

    # Convert 'Vehicle Capacity' to string
    grouped_df['Vehicle Capacity'] = grouped_df['Vehicle Capacity'].astype(str)

    fig = px.bar(
        grouped_df,
        x='Day Of Week',
        y='Count',
        color='Vehicle Capacity',
        title='Frequency of Capacity Reached by Day of Week',
        labels={'Count': 'Frequency of Capacity Reached'},
    )

    return fig

# Update the callback to generate the bar chart based on user input
@callback(
    dd.Output('hourly-capacity-reached', 'figure'),
    [dd.Input('route-dropdown', 'value'),
     dd.Input('date-picker-range', 'start_date'),
     dd.Input('date-picker-range', 'end_date'),
     dd.Input('capacity-range-slider', 'value'),  # Use the range slider value
     dd.Input('day-of-week-dropdown', 'value')]
)
def update_hourly_capacity_reached(selected_route, start_date, end_date, capacity_range, selected_day):
    min_value, max_value = capacity_range

    if selected_route is None:
        # Return an empty figure if no route is selected
        return {}

    filtered_df = df[(df['Route'] == selected_route) &
                     (df['Scheduled Date/Time'] >= start_date) &
                     (df['Scheduled Date/Time'] <= end_date) &
                     (df['Capacity Reached'] >= min_value) &
                     (df['Capacity Reached'] <= max_value) &
                     (df['Day Of Week'] == selected_day)]

    # Group by 'Scheduled Hour' and calculate the count
    grouped_df = filtered_df.groupby(['Scheduled Hour']).size().reset_index(name='Count')

    # Create a figure
    fig = go.Figure()

    # Set a constant color for all bars
    bar_color = '#6495ed'  # You can choose a different color

    # Iterate through all possible 'Scheduled Hour' values
    for hour, count in zip(grouped_df['Scheduled Hour'], grouped_df['Count']):
        # Convert military time to 12-hour time format
        scheduled_time = datetime.strptime(hour, "%H:%M").strftime("%I:%M %p")
        
        # Get the list of associated 'Stop' information
        stop_info = ', '.join(filtered_df[filtered_df['Scheduled Hour'] == hour]['Stop'].tolist())

        # Remove "Count: " from the text on the bars
        text = f'Stops: {stop_info}<br>{count}'

        # Add a bar trace for each 'Scheduled Hour' with the same color
        trace = go.Bar(
            x=[scheduled_time],  # Use the 12-hour time format
            y=[count],
            text=[text],
            name=scheduled_time,  # Use the 12-hour time format as the label
            marker_color=bar_color,  # Set the bar color to a single color
            textfont=dict(color=bar_color)
        )
        fig.add_trace(trace)

    # Update the layout
    fig.update_layout(
        title=f'Frequency of Capacity Reached by Hour for {selected_day}',
        xaxis_title='Scheduled Hour',
        yaxis_title='Frequency of Capacity Reached',
        showlegend=False,
        font=dict(family='Segoe UI', size=16)
    )

    return fig