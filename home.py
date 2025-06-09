
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
            html.Div(get_planet_layout(), id='planets-col', style={
                'width': '10%',
                'height': '100%',
                'display': 'flex',
                'flexDirection': 'column'
            }),
            html.Div([dcc.Graph(id='map-fig', figure=map_figure, config={'responsive': True}, style={'height': '100%', 'width': '100%', 'paddingLeft': '1%', 'paddingRight': '1%'})], style={
                'width': '70%',
                'height': '100%',
                'display': 'flex',
                'flexDirection': 'column'
            }),
            html.Div(id='sidebar-fig', style={
                'width': '20%',
                'height': '100%',
                'display': 'flex',
                'flexDirection': 'column'
            }),
        ], style={
            'display': 'flex',
            'height': '55vh',
            'width': '96%',
            'paddingTop': '2%',
            'paddingBottom': '1%',
            'paddingLeft': '2%',
            'paddingRight': '2%',
            'margin': '0'
        }),
        html.Div(get_timeline_layout(), style={
            'width': '96%',
            'height': '28vh',
            'paddingLeft': '2%',
            'margin': '0'
        }),
    ], style={'height': '100vh', 'width': '100%'})