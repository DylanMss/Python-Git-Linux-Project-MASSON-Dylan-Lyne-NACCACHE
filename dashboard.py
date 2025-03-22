import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import datetime
import os

def load_data():
    df = pd.read_csv('prices.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    return df

def update_daily_report(df):
    daily_metrics = df.groupby('date').agg(
        open_price=('price', 'first'),
        close_price=('price', 'last'),
        min_price=('price', 'min'),
        max_price=('price', 'max'),
        volatility=('price', 'std')
    )
    daily_metrics['percentage_change'] = ((daily_metrics['close_price'] - daily_metrics['open_price']) /
                                            daily_metrics['open_price']) * 100
    daily_metrics.to_csv("daily_report.csv")
    return daily_metrics

def load_daily_report():
    if os.path.exists("daily_report.csv"):
        report_df = pd.read_csv("daily_report.csv")
        return report_df.iloc[-1]
    return None

df = load_data()

# Check if current time is exactly 20:00 (8 PM)
current_time = datetime.datetime.now().strftime('%H:%M')
if current_time == "20:00":
    update_daily_report(df)

report = load_daily_report()

last_row = df.iloc[-1]
last_price = float(last_row["price"])
last_update = last_row["timestamp"]

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Bitcoin Price Dashboard"),
    html.Div([
        html.H3(f"Last Price: ${last_price:,.2f}"),
        html.P(f"Last Update: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    ], style={"textAlign": "center", "marginBottom": "20px"}),
    dcc.Graph(
        id="price-graph",
        figure={
            "data": [
                go.Scatter(
                    x=df["timestamp"],
                    y=df["price"],
                    mode="lines+markers",
                    name="Bitcoin Price",
                    marker=dict(color="#e74c3c"),
                    line=dict(color="#2ecc71")
                )
            ],
            "layout": go.Layout(
                title="Bitcoin Price Evolution",
                xaxis={"title": "Date and Time"},
                yaxis={"title": "Price (USD)"},
                plot_bgcolor="#ecf0f1",
                paper_bgcolor="#bdc3c7"
            )
        }
    ),
    html.Div([
        html.H3("Daily Report (Updated at 20:00)", style={'textAlign': 'center'}),
        html.Div([
            html.P(f"Opening Price: ${float(report['open_price']):,.2f}") if report is not None else html.P("No report available"),
            html.P(f"Closing Price: ${float(report['close_price']):,.2f}") if report is not None else None,
            html.P(f"Percentage Change: {float(report['percentage_change']):.2f}%") if report is not None else None,
            html.P(f"Volatility: {float(report['volatility']):.4f}") if report is not None else None,
        ], style={"textAlign": "center", "backgroundColor": "#f1c40f", "padding": "15px", "borderRadius": "10px"})
    ], style={"marginTop": "20px"})
], style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#ecf0f1", "padding": "20px"})

if __name__ == '__main__':
    app.run_server(debug=True)
