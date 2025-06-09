
from dash import html, dcc, Input, Output, callback, State
from visualisation.active_years_figure import get_active_years_fig

from navbar import get_navbar
import dash



def get_profiles_layout(app, available_countries, view_type='astronauts'):
    # Count records for each country
    if view_type == 'astronauts':
        df = app.astronauts_df
        country_col = 'Profile.Nationality'
        group_col = 'Profile.Name'
        country_counts = app.astronauts_country_counts.reindex(sorted(available_countries), fill_value=0)
        default_country = 'Germany'
    else:
        df = app.missions_df
        country_col = 'Country'
        group_col = 'Company Name'
        country_counts = app.missions_country_counts.reindex(sorted(available_countries), fill_value=0)
        default_country = 'USA'
        

    dropdown_options = [
        {'label': f"All ({df[group_col].nunique()})", 'value': 'all'}
    ] + [
        {'label': f"{country} ({country_counts[country]})", 'value': country}
        for country in sorted(available_countries)
    ]


    return html.Div([
        get_navbar(),
        html.Div(
            [
            html.H2(
                "Astronauts Active Years" if view_type == 'astronauts' else "Companies Active Years",
                style={'margin': '0', 'flex': '1', 'textAlign': 'left'}
            ),
            dcc.Dropdown(
                id='country-dropdown',
                options=dropdown_options,
                value=default_country,
                clearable=False,
                style={'width': '300px', 'marginLeft': 'auto', 'marginRight': '10px'}
            ),
            ],
            style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'marginTop': '20px',
            'marginBottom': '20px'
            }
        ),
        dcc.Graph(
            id='active-years-fig',
            config={'scrollZoom': False}
        ),
        dcc.Store(id='view-type', data=view_type)
        ])

def register_profiles_callbacks(app, missions_df):
    @app.callback(
        Output('url', 'pathname'),
        Input('active-years-fig', 'clickData'),
        prevent_initial_call=True
    )

    def go_to_mission_log(clickData):
        if clickData and 'points' in clickData and clickData['points']:
            point = clickData['points'][0]
            detail = point.get('customdata')
            if detail:
                try:
                    idx = missions_df[missions_df['Detail'] == detail].index[0]
                    return f"/mission/{idx}"
                except Exception:
                    pass
        return dash.no_update
