import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go

# Lire le CSV 
df = pd.read_csv('prices.csv')