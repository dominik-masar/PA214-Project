import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from visualisation.barchartFigure import barchart_fig
from visualisation.mapGeo import map_fig

# Load data
df = pd.read_csv("datasets/space_with_geo-firstAttempt.csv")

# Create figures
main_fig = map_fig()
bar_fig = barchart_fig(df)

main_fig.update_layout(height=700)  # Adjust height to your liking
bar_fig.update_layout(height=700)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with 80:20 ratio
app.layout = html.Div([
    html.Div([dcc.Graph(figure=main_fig)], style={'width': '80%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(figure=bar_fig)], style={'width': '20%', 'display': 'inline-block'})
])

if __name__ == '__main__':
    app.run(debug=True)