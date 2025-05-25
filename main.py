import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from visualisation.barchartFigure import barchart_fig
from visualisation.mapGeo import map_fig
from visualisation.bottomView import get_bottom_fig #TODO rename

DATASET_FILENAME = "datasets/space_with_geo_with_countries.csv"

# Load data
df = pd.read_csv(DATASET_FILENAME)

# Create figures
main_fig = map_fig(df)
bar_fig = barchart_fig(df, 2000) # TODO: insert variable year
active_years_fig = get_bottom_fig()  # Default: astronauts from U.S.

main_fig.update_layout(height=700)
bar_fig.update_layout(height=700)
active_years_fig.update_layout(height=700)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with 80:20 ratio
app.layout = html.Div([
    html.Div([dcc.Graph(figure=main_fig)], style={'width': '70%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(figure=bar_fig)], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(figure=active_years_fig)])
])

if __name__ == '__main__':
    app.run(debug=True)