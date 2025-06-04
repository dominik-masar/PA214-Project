from dash.dependencies import Output, Input, State
from dash import html, dcc
from visualisation.barchart_figure import barchart_fig

def register_sidebar_callbacks(app):
    @app.callback(
        Output('search-input', 'value'),
        Output('trigger-update', 'data', allow_duplicate = True),
        Input('reset-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset(n_clicks):
        return "", {"reset_triggered": True, "search_triggered": False}
    

    @app.callback(
        Output('trigger-update', 'data', allow_duplicate = True),
        Input('search-button', 'n_clicks'),
        State('search-input', 'value'),
        prevent_initial_call=True
    )
    def search(n_clicks, search_term):
        if search_term and search_term.strip():
            app.filtered_df = app.missions_df[app.missions_df['Detail'].str.contains(search_term, na=False, case=False)]
            return {"search_triggered": True}
        return {"search_triggered": False}


    @app.callback(
        Output('sidebar-fig', 'children'),
        Input('trigger-update', 'data'),
        Input("selected-years", "data")
    )
    def update_output(trigger_data, year_range):
        start, end = year_range

        if trigger_data and trigger_data['search_triggered']:
            df = app.filtered_df
            filtered_df = df[(df['Year'] >= start) & (df['Year'] <= end)]
            if filtered_df.empty:
                return html.Div("No results found.")

            return html.Div([
                html.Ul([
                    html.Li(f"{row['Detail']} ({row['Year']})")
                    for _, row in filtered_df.iterrows()
                ])
            ], style={
                'height': '700px',
                'overflowY': 'scroll',
                'border': '1px solid #ccc',
                'padding': '10px'
            })

        df = app.missions_df
        filtered_df = df[(df['Year'] >= start) & (df['Year'] <= end)]

        fig = barchart_fig(filtered_df, app.color_map)
        return dcc.Graph(id='bar-fig', figure=fig, config={'staticPlot': True})
