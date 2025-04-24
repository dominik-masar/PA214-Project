import dash
from dash import html, dcc, Input, Output
import pandas as pd
from visualisation.barchartFigure import barchart_fig
from visualisation.mapGeo import map_fig
from visualisation.bottomView import get_bottom_fig #TODO rename

DATASET_FILENAME = "datasets/space_with_geo_with_countries.csv"

# Load data
df = pd.read_csv(DATASET_FILENAME)

# Create figures
main_fig = map_fig()
bar_fig = barchart_fig(df, 2000)  # TODO: insert variable year
timeline_fig = get_bottom_fig()  # Default: astronauts from U.S.

main_fig.update_layout(height=700)
bar_fig.update_layout(height=700)
timeline_fig.update_layout(height=700)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with timeline at the bottom
app.layout = html.Div([
    html.Div([
        dcc.Graph(figure=main_fig)
    ], style={'width': '70%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(figure=bar_fig)
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Hr(),

    html.Div([
        dcc.Graph(figure=timeline_fig)
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
