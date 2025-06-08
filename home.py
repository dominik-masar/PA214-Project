# pages/home.py
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
        html.Div(get_planet_layout(), style={'width': '70%', 'height': '120px', 'display': 'inline-block'}),
        html.Div([
            dcc.Input(id='search-input', type='text', placeholder='Search...'),
            html.Button('Search', id='search-button', n_clicks=0),
            html.Button('Reset', id='reset-button', n_clicks=0),
            dcc.Store(id='trigger-update')
        ], style={'width': '20%', 'display': 'inline-block', 'margin-left': '10px'}),
        html.Div([
            html.Div([dcc.Graph(id='map-fig', figure=map_figure)], style={'width': '65%', 'height': '100%', 'display': 'inline-block'}),
            html.Div(id='sidebar-fig', style={'width': '30%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'gap': '5%', 'height': '700px'}),
        html.Div(get_timeline_layout(), style={'width': '100%', 'display': 'inline-block'}),
    ])

