
from dash import html, dcc, Input, Output, callback, State
from visualisation.active_years_figure import get_active_years_fig
from preprocessing.loadDatasets import get_country_list
from navbar import get_navbar
import dash



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


def register_profiles_callbacks(app, missions_df):
    @app.callback(
        Output('url', 'pathname'),
        Input('active-years-fig', 'clickData'),
        prevent_initial_call=True
    )

    def go_to_mission_log(clickData):
        if clickData and 'points' in clickData and clickData['points']:
            detail = clickData['points'][0]['customdata']
            try:
                idx = missions_df[missions_df['Detail'] == detail].index[0]
                return f"/mission/{idx}"
            except Exception:
                pass
        return dash.no_update

    """
    def go_to_mission_log(clickData):
        if clickData and 'points' in clickData and clickData['points']:
            detail = clickData['points'][0]['customdata']
            # Find the mission's index (row) in missions_df
            try:
                idx = missions_df[missions_df['Detail'] == detail].index[0]
                page_size = 15
                page = idx // page_size + 1
                # Use anchor to scroll to the mission card
                #return f"/logs/{page}#mission-{idx}"
                return f"/logs/{page}"
            except Exception:
                pass
        return dash.no_update
    """