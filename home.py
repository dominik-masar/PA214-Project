
from dash import html, dcc
from visualisation.map_figure import map_fig
from visualisation.timeline_figure import get_timeline_layout
from visualisation.planets_figure import get_planet_layout
from navbar import get_navbar


def get_home_layout(app):
    missions_df = app.missions_df
    map_figure = map_fig(missions_df, app.max_missions)

    return html.Div([
        get_navbar(),
        html.Div([
            html.Div(get_planet_layout(), style={'width': '10%', 'height': '100%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='map-fig', figure=map_figure)], style={'width': '70%', 'height': '100%', 'display': 'inline-block'}),
            html.Div(id='sidebar-fig', style={'width': '20%', 'height': '100%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'gap': '5%', 'height': '50%', 'paddingTop': '2%'}),
        html.Div(get_timeline_layout(), style={'width': '100%', 'height': '5%', 'paddingTop': '2%', 'display': 'inline-block'}),
        ])

