import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go

# CSV
df = pd.read_csv('prices.csv')

# Convert timestamp column
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Get the latest price and update time
last_row = df.iloc[-1]
last_price = last_row["price"]
last_update = last_row["timestamp"]

# Dash app
app = dash.Dash(__name__)


app.layout = html.Div(style={'backgroundColor': '#FFFAF0', 'color': '#333', 'padding': '20px', 'fontFamily': 'Arial'}, children=[

    html.H1("🚀 Bitcoin Price Tracker", 
            style={'textAlign': 'center', 'color': '#FF5733', 'fontSize': '32px', 'fontWeight': 'bold'}),

    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}, children=[
        html.Div(style={
            'backgroundColor': '#FF5733', 'color': 'white', 'padding': '20px', 'borderRadius': '15px',
            'boxShadow': '5px 5px 15px rgba(0,0,0,0.2)', 'width': '300px', 'textAlign': 'center'
        }, children=[
            html.P("💰 Latest Price", style={'fontSize': '20px', 'fontWeight': 'bold'}),
            html.P(f"${last_price}", style={'fontSize': '30px', 'fontWeight': 'bold', 'color': '#FFD700'}),
            html.P(f"🕒 Last Updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')}", style={'fontSize': '14px'})
        ])
    ]),

    dcc.Graph(
        id="price-chart",
        figure={
            "data": [
                go.Scatter(
                    x=df["timestamp"],
                    y=df["price"],
                    mode="lines+markers",
                    name="Bitcoin Price",
                    line=dict(color='#33FF57', width=3),
                    marker=dict(color='#FF33A8', size=8, symbol='circle')
                )
            ],
            "layout": go.Layout(
                title="📈 Bitcoin Price Evolution",
                title_font=dict(color='#333', size=24),
                xaxis={"title": "Date & Time", "color": "#333", "gridcolor": "#DDD"},
                yaxis={"title": "Price (USD)", "color": "#333", "gridcolor": "#DDD"},
                paper_bgcolor="#FFFAF0",
                plot_bgcolor="#FFF5EE"
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
