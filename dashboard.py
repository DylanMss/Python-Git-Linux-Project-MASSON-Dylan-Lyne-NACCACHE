import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime

app = dash.Dash(__name__)
server = app.server  # pour déploiement

# --- FONCTIONS OUTILS ---

def load_data():
    """
    Charge le CSV contenant: timestamp (datetime), price (float)
    et trie par ordre chronologique.
    """
    df = pd.read_csv('prices.csv', parse_dates=['timestamp'])
    df.sort_values('timestamp', inplace=True)
    return df

def info_card(title, value, subtext=None):
    """
    Petite "card" d'information pour un affichage stylé.
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
    Page principale du Dashboard, avec le graphique,
    les informations top-info et le rapport quotidien.
    """
    return html.Div(
        style={'fontFamily': 'Arial, sans-serif', 'margin': '0 auto', 'maxWidth': '800px', 'padding': '20px'},
        children=[
            # Titre et logo
            html.Div(
                style={'display': 'flex', 'alignItems': 'center'},
                children=[
                    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg',
                             style={'width': '60px', 'marginRight': '10px'}),
                    html.H1("Bitcoin Dashboard", style={'margin': '0'})
                ]
            ),
            html.Div(id='top-info', style={'marginTop': '20px'}),

            # Sélecteur d'intervalle pour le graphe
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
                        value='24H',  # bouton par défaut sur 24H
                        inline=True,
                        style={'marginBottom': '10px'}
                    )
                ]
            ),

            dcc.Graph(id='price-graph', style={'height': '400px'}),

            # Onglet Basic uniquement
            dcc.Tabs(
                id='tabs',
                value='tab-basic',
                children=[
                    dcc.Tab(label='Basic', value='tab-basic', children=[
                        html.Div(id='basic-content', style={'padding': '10px'})
                    ])
                ]
            ),

            # Zone du rapport quotidien
            html.Div(id='daily-report', style={'marginTop': '20px'})
        ]
    )

# --- NAVIGATION (layout principal) ---

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Barre de navigation
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
            dcc.Link("Présentation", href="/", style={
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

    # Contenu de la page
    html.Div(id='page-content')
])

# --- CALLBACK DE NAVIGATION ---

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/dashboard":
        return dashboard_page()
    else:
        # Par défaut, on renvoie la page de présentation
        return presentation_page()

# --- CALLBACKS DU DASHBOARD ---

@app.callback(
    Output('top-info', 'children'),
    Output('price-graph', 'figure'),
    Input('range-selector', 'value')
)
def update_dashboard(selected_range):
    """
    Met à jour la zone "top-info" (ex: dernier prix + heure)
    et le graphique, selon l'intervalle (1H, 24H, 7D).
    """
    df = load_data()
    if df.empty:
        return html.Div("Pas de données"), go.Figure()

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

    # Définir l'intervalle pour le graphique
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
    Onglet Basic : calcule open, high, low, close sur l'intervalle (1H, 24H, 7D)
    """
    df = load_data()
    if df.empty:
        return html.Div("No data")

    # Filtrage selon l'intervalle
    now = df['timestamp'].max()
    if selected_range == '1H':
        start_time = now - pd.Timedelta(hours=1)
    elif selected_range == '24H':
        start_time = now - pd.Timedelta(hours=24)
    else:
        start_time = now - pd.Timedelta(days=7)

    filtered = df[df['timestamp'] >= start_time].copy()
    if filtered.empty:
        return html.Div("Aucune donnée pour cet intervalle.")
    else:
        filtered.sort_values('timestamp', inplace=True)
        open_ = filtered.iloc[0]['price']
        close_ = filtered.iloc[-1]['price']
        high_ = filtered['price'].max()
        low_ = filtered['price'].min()
        basic_layout = html.Div([
            html.H4(f"Open:  ${open_:,.2f}"),
            html.H4(f"High:  ${high_:,.2f}"),
            html.H4(f"Low:   ${low_:,.2f}"),
            html.H4(f"Close: ${close_:,.2f}")
        ])
        return basic_layout

@app.callback(
    Output('daily-report', 'children'),
    Input('range-selector', 'value')  # Utilisé pour déclencher la mise à jour du rapport quotidien
)
def update_daily_report(selected_range):
    """
    Affiche le rapport quotidien mis à jour à 20h chaque jour.
    Si l'heure actuelle est avant 20h, le rapport de la veille est affiché.
    Calcule : open, close, high, low, volatilité et évolution.
    """
    df = load_data()
    if df.empty:
        return html.Div("Pas de données pour le rapport quotidien.")

    # Si l'heure actuelle est avant 20h, on affiche le rapport de la veille
    now = pd.Timestamp.now()
    report_date = now.normalize()
    if now.hour < 20:
        report_date = report_date - pd.Timedelta(days=1)

    day_start = report_date
    day_end = report_date + pd.Timedelta(days=1)
    day_data = df[(df['timestamp'] >= day_start) & (df['timestamp'] < day_end)]

    if day_data.empty:
        return html.Div(f"Aucune donnée pour le {report_date.date()}.")

    day_data.sort_values('timestamp', inplace=True)
    open_price = day_data.iloc[0]['price']
    close_price = day_data.iloc[-1]['price']
    high_price = day_data['price'].max()
    low_price = day_data['price'].min()
    # Calcul de la volatilité en pourcentage
    volatility = (high_price - low_price) / open_price * 100
    evolution = (close_price - open_price) / open_price * 100

    report_layout = html.Div([
        html.H3(f"Rapport quotidien du {report_date.date()} à 20h"),
        html.P(f"Open:  ${open_price:,.2f}"),
        html.P(f"Close: ${close_price:,.2f}"),
        html.P(f"High:  ${high_price:,.2f}"),
        html.P(f"Low:   ${low_price:,.2f}"),
        html.P(f"Volatilité: {volatility:.2f}%"),
        html.P(f"Évolution:  {evolution:.2f}%")
    ], style={
        'border': '1px solid #ccc',
        'padding': '10px',
        'borderRadius': '8px',
        'marginTop': '20px',
        'textAlign': 'center'
    })

    return report_layout

if __name__ == '__main__':
    app.run_server(debug=True)
