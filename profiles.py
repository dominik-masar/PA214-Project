# pages/profiles.py
from dash import html, dcc, Input, Output
from visualisation.active_years_figure import get_active_years_fig
from preprocessing.loadDatasets import get_country_list
from navbar import get_navbar



def get_profiles_layout(app, available_countries):
    return html.Div([
        get_navbar(),
        dcc.RadioItems(
            id='bottom-view-toggle',
            options=[
                {'label': 'Astronauts', 'value': 'astronauts'},
                {'label': 'Companies', 'value': 'companies'}
            ],
            value='astronauts',
            labelStyle={'display': 'inline-block', 'margin-right': '20px'}
        ),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in sorted(available_countries)],
            value='USA',
            clearable=False
        ),
        dcc.Graph(id='active-years-fig', config={'scrollZoom': True}, style={'height': '600px'})
    ])
