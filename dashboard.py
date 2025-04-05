import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime

app = dash.Dash(__name__)
server = app.server  # for deployment

# --- UTILITY FUNCTIONS ---

def load_data():
    """
    Loads the CSV file containing: timestamp (datetime), price (float),
    and sorts it chronologically.
    """
    df = pd.read_csv('prices.csv', parse_dates=['timestamp'])
    df.sort_values('timestamp', inplace=True)
    return df

def info_card(title, value, subtext=None):
    """
    Small info card for clean display.
    """
    return html.Div(
        style={
            'display': 'inline-block',
            'border': '1px solid #ccc',
            'borderRadius': '8px',
            'padding': '10px',
            'margin': '5px',
            'width': '100vw',
            'textAlign': 'center'
        },
        children=[
            html.H4(title, style={'margin': '5px 0'}),
            html.H2(value, style={'margin': '5px 0', 'color': '#2c3e50'}),
            html.Div(subtext if subtext else "", style={'fontSize': '12px', 'color': '#7f8c8d'})
        ]
    )

# --- PAGES ---

def presentation_page():
    """
    Presentation page, displaying the project creators: Lyne and Dylan, 
    and briefly explaining why Bitcoin was chosen.
    """
    return html.Div(
        style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'},
        children=[
            html.H1("Presentation", style={'textAlign': 'center'}),
            html.Div(
                style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '20px'},
                children=[

                ]
            ),
            html.Div(
                style={'maxWidth': '800px', 'margin': '20px auto', 'lineHeight': '1.5'},
                children=[
                            html.P("This project was created by Lyne Naccache and Dylan Masson."),
                            html.P(
                            "We chose to analyze Bitcoin because it is a highly dynamic financial asset, "
                            "making it ideal for continuous scraping and real-time dashboard tracking. "
                            "The data is scraped directly from https://www.coindesk.com/price/bitcoin."
                            )
                ]
            )
        ]
    )

def dashboard_page():
    """
    Main dashboard page, with the graph,
    top-info cards, and daily report section.
    """
    return html.Div(
        style={'fontFamily': 'Arial, sans-serif', 'margin': '0 auto', 'maxWidth': '800px', 'padding': '20px'},
        children=[
            # Title and logo
            html.Div(
                style={'display': 'flex', 'alignItems': 'center'},
                children=[
                    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg',
                             style={'width': '60px', 'marginRight': '10px'}),
                    html.H1("Bitcoin Dashboard", style={'margin': '0'})
                ]
            ),
            html.Div(id='top-info', style={'marginTop': '20px'}),

            # Interval selector for the graph
            html.Div(
                style={'marginTop': '20px'},
                children=[
                    dcc.RadioItems(
                        id='range-selector',
                        options=[
                            {'label': '1H', 'value': '1H'},
                            {'label': '24H', 'value': '24H'},
                            {'label': '7D', 'value': '7D'},
                        ],
                        value='24H',  # default button on 24H
                        inline=True,
                        style={'marginBottom': '10px'}
                    )
                ]
            ),

            dcc.Graph(id='price-graph', style={'height': '400px'}),

            # Basic tab only
            dcc.Tabs(
                id='tabs',
                value='tab-basic',
                children=[
                    dcc.Tab(label='Basic', value='tab-basic', children=[
                        html.Div(id='basic-content', style={'padding': '10px'})
                    ])
                ]
            ),

            # Daily Report Area
            html.Div(id='daily-report', style={'marginTop': '20px'})
        ]
    )

# --- MAIN LAYOUT AND NAVIGATION ---

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Navigation bar
    html.Nav(
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'backgroundColor': '#f8f9fa',
            'padding': '10px',
            'marginBottom': '20px'
        },
        children=[
            dcc.Link("Presentation", href="/", style={
                'margin': '0 20px',
                'textDecoration': 'none',
                'color': '#007BFF',
                'fontWeight': 'bold'
            }),
            dcc.Link("Dashboard", href="/dashboard", style={
                'margin': '0 20px',
                'textDecoration': 'none',
                'color': '#007BFF',
                'fontWeight': 'bold'
            })
        ]
    ),

    # Page content
    html.Div(id='page-content')
])

# --- ROUTING CALLBACK ---

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/dashboard":
        return dashboard_page()
    else:
        # By default, we return the presentation page
        return presentation_page()

# --- DASHBOARD CALLBACKS ---

@app.callback(
    Output('top-info', 'children'),
    Output('price-graph', 'figure'),
    Input('range-selector', 'value')
)
def update_dashboard(selected_range):
    """
    Updates top-info section (e.g., latest price + time)
    and graph depending on selected interval (1H, 24H, 7D).
    """
    df = load_data()
    if df.empty:
        return html.Div("No data available."), go.Figure()

    # Dernier prix et son timestamp
    latest_price = df['price'].iloc[-1]
    latest_timestamp = df['timestamp'].iloc[-1]
    last_time_str = latest_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    top_info_layout = html.Div(
        style={'display': 'flex', 'flexWrap': 'wrap'},
        children=[
            info_card("BTC Price", f"${latest_price:,.2f}"),
            info_card("Last update", last_time_str)
        ]
    )

    # Set the interval for the chart
    now = df['timestamp'].max()
    if selected_range == '1H':
        start_time = now - pd.Timedelta(hours=1)
    elif selected_range == '24H':
        start_time = now - pd.Timedelta(hours=24)
    else:  # '7D'
        start_time = now - pd.Timedelta(days=7)

    filtered_df = df[df['timestamp'] >= start_time]

    fig = go.Figure(
        data=[go.Scatter(
            x=filtered_df['timestamp'],
            y=filtered_df['price'],
            mode='lines+markers',
            line=dict(color='#27ae60', width=2),
            name='BTC Price'
        )],
        layout=go.Layout(
            title=f"Bitcoin Price ({selected_range})",
            xaxis=dict(title="Time"),
            yaxis=dict(title="Price (USD)"),
            margin=dict(l=50, r=50, t=50, b=50)
        )
    )

    return top_info_layout, fig

@app.callback(
    Output('basic-content', 'children'),
    Input('range-selector', 'value')
)
def update_basic(selected_range):
    """
    Calculates open, high, low, close for the selected interval (1H, 24H, 7D)
    """
    df = load_data()
    if df.empty:
        return html.Div("No data available.")

    # Filtering by interval
    now = df['timestamp'].max()
    if selected_range == '1H':
        start_time = now - pd.Timedelta(hours=1)
    elif selected_range == '24H':
        start_time = now - pd.Timedelta(hours=24)
    else:
        start_time = now - pd.Timedelta(days=7)

    filtered = df[df['timestamp'] >= start_time].copy()
    if filtered.empty:
        return html.Div("No data for this interval.")
    else:
        filtered.sort_values('timestamp', inplace=True)
        open_ = filtered.iloc[0]['price']
        close_ = filtered.iloc[-1]['price']
        high_ = filtered['price'].max()
        low_ = filtered['price'].min()
        basic_layout = html.Div([
            html.H3("Price Summary", style={'marginBottom': '15px'}),
            html.H4(f"Open:  ${open_:,.2f}"),
            html.H4(f"High:  ${high_:,.2f}"),
            html.H4(f"Low:   ${low_:,.2f}"),
            html.H4(f"Close: ${close_:,.2f}")
        ])
        return basic_layout

@app.callback(
    Output('daily-report', 'children'),
    Input('range-selector', 'value')  # Used to trigger the daily report update
)
def update_daily_report(selected_range):
    """
    Displays daily report at 8 PM.
    If before 8 PM, shows the previous day's report.
    Calculates: open, close, high, low, volatility, and evolution.
    """
    df = load_data()
    if df.empty:
        return html.Div("No data for daily report.")

    # If the current time is before 8 p.m., the report from the previous day is displayed.
    now = pd.Timestamp.now()
    report_date = now.normalize()
    if now.hour < 20:
        report_date = report_date - pd.Timedelta(days=1)

    day_start = report_date
    day_end = report_date + pd.Timedelta(days=1)
    day_data = df[(df['timestamp'] >= day_start) & (df['timestamp'] < day_end)]

    if day_data.empty:
        return html.Div(f"No data for {report_date.date()}.")

    day_data.sort_values('timestamp', inplace=True)
    open_price = day_data.iloc[0]['price']
    close_price = day_data.iloc[-1]['price']
    high_price = day_data['price'].max()
    low_price = day_data['price'].min()

    # Calculation of volatility in percentage
    volatility = (high_price - low_price) / open_price * 100
    evolution = (close_price - open_price) / open_price * 100

    report_layout = html.Div([
        html.H3(f"Daily report for {report_date.date()} at 8 PM"),
        html.P(f"Open:  ${open_price:,.2f}"),
        html.P(f"Close: ${close_price:,.2f}"),
        html.P(f"High:  ${high_price:,.2f}"),
        html.P(f"Low:   ${low_price:,.2f}"),
        html.P(f"Volatility: {volatility:.2f}%", style={'fontWeight': 'bold'}),
        html.P(
                f"Evolution: {evolution:.2f}%",
                style={
                    'color': 'green' if evolution >= 0 else 'red',
                    'fontWeight': 'bold'
    }
)

    ], style={
        'border': '1px solid #ccc',
        'padding': '10px',
        'borderRadius': '8px',
        'marginTop': '20px',
        'textAlign': 'center'
    })

    return report_layout

if __name__ == '__main__':
    app.run(debug=True)
