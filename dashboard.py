import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime

app = dash.Dash(__name__)
server = app.server  # pour le déploiement

# --- FONCTIONS UTILITAIRES ---

def load_data():
    """
    Charge le fichier CSV contenant : timestamp (datetime), price (float),
    et trie les données par ordre chronologique.
    """
    df = pd.read_csv('prices.csv', parse_dates=['timestamp'])
    df.sort_values('timestamp', inplace=True)
    return df

def info_card(title, value, subtext=None):
    """
    Renvoie une "card" d'information pour un affichage propre.
    """
    return html.Div(
        style={
            'display': 'inline-block',
            'border': '1px solid #ccc',
            'borderRadius': '8px',
            'padding': '10px',
            'margin': '5px',
            'width': '180px',
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
    Page de présentation affichant les créateurs et une brève explication.
    """
    return html.Div(
        style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'},
        children=[
            html.H1("Presentation", style={'textAlign': 'center'}),
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
    Page principale du dashboard avec le graphique, les cards d'information,
    et le rapport quotidien.
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

            # Sélecteur d'intervalle pour le graphique
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
                        value='24H',  # valeur par défaut
                        inline=True,
                        style={'marginBottom': '10px'}
                    )
                ]
            ),

            # Graphique du prix
            dcc.Graph(id='price-graph', style={'height': '400px'}),

            # Onglets (ici, seul l'onglet "Basic" est utilisé)
            dcc.Tabs(
                id='tabs',
                value='tab-basic',
                children=[
                    dcc.Tab(label='Basic', value='tab-basic', children=[
                        html.Div(id='basic-content', style={'padding': '10px'})
                    ])
                ]
            ),

            # Section du rapport quotidien
            html.H2("Daily Report (mis à jour à 20h)", style={'marginTop': '30px'}),
            html.Div(id='daily-report', style={'display': 'flex', 'flexWrap': 'wrap'})
        ]
    )

# --- LAYOUT PRINCIPAL ET NAVIGATION ---

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

    # Contenu de la page
    html.Div(id='page-content')
])

# --- CALLBACKS DE ROUTING ---

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/dashboard":
        return dashboard_page()
    else:
        # Par défaut, afficher la page de présentation
        return presentation_page()

# --- CALLBACKS DU DASHBOARD ---

@app.callback(
    Output('top-info', 'children'),
    Output('price-graph', 'figure'),
    Input('range-selector', 'value')
)
def update_dashboard(selected_range):
    """
    Met à jour la section top-info (prix actuel + heure) et le graphique en fonction de l'intervalle (1H, 24H, 7D).
    Les timestamps sont utilisés tels quels depuis le CSV.
    """
    df = load_data()
    if df.empty:
        return html.Div("No data available."), go.Figure()

    # Récupération du dernier prix et du timestamp
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
    Calcule et affiche les indicateurs open, high, low, close pour l'intervalle sélectionné.
    """
    df = load_data()
    if df.empty:
        return html.Div("No data available.")

    now = df['timestamp'].iloc[-1]
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
    Input('range-selector', 'value')  # Cet input permet juste de déclencher l'update
)
def update_daily_report(selected_range):
    """
    Affiche le rapport quotidien (mis à jour à 20h) avec open, close, high, low, volatilité et évolution.
    On utilise uniquement les données du CSV (timestamp et price).
    """
    df = load_data()
    if df.empty:
        return html.Div("No data for daily report.")

    now = pd.Timestamp.now()
    report_date = now.normalize()
    # Si avant 20h, afficher le rapport de la veille
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

    # Calcul de la volatilité en % (différence relative entre high et low par rapport à l'open)
    volatility = (high_price - low_price) / open_price * 100
    evolution = (close_price - open_price) / open_price * 100

    report_layout = html.Div([
        html.H3(f"Daily report for {report_date.date()} at 20:00"),
        html.P(f"Open:  ${open_price:,.2f}"),
        html.P(f"Close: ${close_price:,.2f}"),
        html.P(f"High:  ${high_price:,.2f}"),
        html.P(f"Low:   ${low_price:,.2f}"),
        html.P(f"Volatility: {volatility:.2f}%", style={'fontWeight': 'bold'}),
        html.P(f"Evolution: {evolution:.2f}%", style={
            'color': 'green' if evolution >= 0 else 'red',
            'fontWeight': 'bold'
        })
    ], style={
        'border': '1px solid #ccc',
        'padding': '10px',
        'borderRadius': '8px',
        'marginTop': '20px',
        'textAlign': 'center'
    })

    return report_layout

if __name__ == '__main__':
    # Pour le développement, utilisez app.run_server (assurez-vous de choisir un port différent si nécessaire)
    app.run_server(debug=True, host='0.0.0.0', port=8051)
