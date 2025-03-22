import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
import datetime

# Load CSV file
df = pd.read_csv('prices.csv')

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date

# Get today's date
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# Determine which day's report to use
current_time = datetime.datetime.now().strftime('%H:%M')
if current_time >= "16:00":
    report_date = today  # If it's after 16:00, use today's report
else:
    report_date = yesterday  # Before 16:00, show yesterday’s report

# Compute daily metrics
daily_metrics = df.groupby('date').agg(
    open_price=('price', 'first'),
    close_price=('price', 'last'),
    min_price=('price', 'min'),
    max_price=('price', 'max'),
    volatility=('price', lambda x: x.std()),  # Standard deviation
)

daily_metrics['percentage_change'] = (
    (daily_metrics['close_price'] - daily_metrics['open_price']) / daily_metrics['open_price']
) * 100

# Save report data separately
report_file = "daily_report.csv"
daily_metrics.to_csv(report_file)

# Load latest report if available
try:
    report_df = pd.read_csv("daily_report.csv")
    latest_report = report_df[report_df['date'] == str(report_date)].iloc[-1]  # Ensure correct date is used
except (FileNotFoundError, IndexError):
    latest_report = None

# Get latest available price
last_price = df.iloc[-1]["price"]
last_update = df.iloc[-1]["timestamp"]

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Bitcoin Price Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),

    # Display last updated price
    html.Div([
        html.H3(f"Last Price: ${last_price:.2f}", style={'color': '#2980b9'}),
        html.P(f"Last Update: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    ], style={'textAlign': 'center', 'backgroundColor': '#ecf0f1', 'padding': '10px', 'borderRadius': '10px'}),

    # Bitcoin Price Graph
    dcc.Graph(
        id="price-graph",
        figure={
            "data": [
                go.Scatter(
                    x=df["timestamp"],
                    y=df["price"],
                    mode="lines+markers",
                    name="Bitcoin Price"
                )
            ],
            "layout": go.Layout(
                title="Bitcoin Price Evolution",
                xaxis={"title": "Date and Time"},
                yaxis={"title": "Price (USD)"},
                plot_bgcolor="#f4f4f4"
            )
        }
    ),

    # Bitcoin Price Stats Section
    html.Div([
        html.H3("Bitcoin (BTC) Price Stats", style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.Div([
            html.Div([
                html.P("Opening Price", style={'fontWeight': 'bold'}),
                html.P(f"${latest_report['open_price']:.2f}" if latest_report is not None else "N/A")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
            html.Div([
                html.P("Closing Price", style={'fontWeight': 'bold'}),
                html.P(f"${latest_report['close_price']:.2f}" if latest_report is not None else "N/A")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
            html.Div([
                html.P("24h Range", style={'fontWeight': 'bold'}),
                html.P(f"${latest_report['min_price']:.2f} - ${latest_report['max_price']:.2f}" if latest_report is not None else "N/A")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
            html.Div([
                html.P("Price Change (%)", style={'fontWeight': 'bold'}),
                html.P(f"{latest_report['percentage_change']:.2f}%" if latest_report is not None else "N/A")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
            html.Div([
                html.P("Volatility", style={'fontWeight': 'bold'}),
                html.P(f"{latest_report['volatility']:.4f}" if latest_report is not None else "N/A")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '10px'}),
    ], style={'backgroundColor': '#ecf0f1', 'padding': '15px', 'borderRadius': '10px', 'marginTop': '20px'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
